"""Letter-module behaviour added in v1.0.0: typing guards, multi-cycle R, gluing,
letter validation, Law 4 triggers, ledgers, intake refusals and the nine conjuncts."""

from dataclasses import replace
from fractions import Fraction as F
from itertools import product
from math import floor

import cochain
import pytest
from context_exposure import ContextWindowExtractor, glue
from descent import DescentProjector, ledger_entry
from exact_repair import ExactRepairSolver
from integration_tape import ExecutionTape, canonical_json, canonical_letter
from residual_projection import GraphResidualProjector, ResidualProjector
from structural_lift import StructuralLifter, l1_norm
from terminalization import (
    CONTINUATION_CONJUNCTS,
    ContinuationFacts,
    TerminalizationEvaluator,
    can_continue,
    failed_conjuncts,
)
from typed_refusal import INTAKE_REASONS, M_REASONS, OperationRequest, TypedRefusalGate

THETA_V = ["a", "b", "c", "d"]
THETA_E = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("a", "c")]


# -- E -------------------------------------------------------------------------


def test_exact_repair_guards():
    with pytest.raises(ValueError, match="UNKNOWN_VERTEX"):
        ExactRepairSolver(["a"], [("a", "b")])
    with pytest.raises(ValueError, match="SELF_LOOP"):
        ExactRepairSolver(["a"], [("a", "a")])
    solver = ExactRepairSolver(["a", "b"], [("a", "b")])
    with pytest.raises(ValueError, match="UNTYPED_DEFECT"):
        solver.solve({("b", "a"): F(1)})
    with pytest.raises(ValueError, match="NOT_EXACT"):
        solver.solve({("a", "b"): 0.5})


def test_exact_repair_fixes_a_gauge_per_component_and_discharges_to_zero():
    solver = ExactRepairSolver(["a", "b", "c", "d"], [("a", "b"), ("c", "d")])
    receipt = solver.solve({("a", "b"): F(2), ("c", "d"): F(-7)}, gauge_vertex="c")
    assert receipt.success and receipt.residual_norm == 0
    assert receipt.potential["c"] == 0 and receipt.potential["a"] == 0
    assert set(receipt.repaired.values()) == {F(0)}
    assert receipt.authority_effect == "None"


def test_exact_repair_refuses_any_cycle_with_circulation():
    solver = ExactRepairSolver(THETA_V, THETA_E)
    # Exact on the outer square but with circulation around the chord's triangle.
    receipt = solver.solve({("a", "b"): F(1), ("b", "c"): F(1), ("a", "c"): F(1)})
    assert not receipt.success and receipt.error == "REFUSED_NON_ZERO_CURL"


# -- R -------------------------------------------------------------------------


def test_single_cycle_projector_rejects_open_walks_and_untyped_edges():
    with pytest.raises(ValueError, match="NOT_A_CYCLE"):
        ResidualProjector([("a", "b"), ("c", "a")])
    projector = ResidualProjector([("a", "b"), ("b", "a")])
    with pytest.raises(ValueError, match="UNTYPED_DEFECT"):
        projector.project({("a", "c"): F(1)})
    assert projector.project({("a", "b"): F(2)}).cycle_coordinates == (F(2),)


def test_graph_projector_keeps_one_coordinate_per_independent_cycle():
    with pytest.raises(ValueError, match="MALFORMED_EDGE"):
        GraphResidualProjector(["a"], [("a", "a")])
    projector = GraphResidualProjector(THETA_V, THETA_E)
    assert projector.independent_cycles == 2
    with pytest.raises(ValueError, match="UNTYPED_DEFECT"):
        projector.project({("z", "a"): F(1)})
    x = {("a", "b"): F(1), ("b", "c"): F(2), ("c", "d"): F(0), ("d", "a"): F(-1), ("a", "c"): F(3)}
    receipt = projector.project(x)
    assert len(receipt.cycle_coordinates) == 2
    cx = cochain.Complex(tuple(THETA_V), tuple(THETA_E))
    vector = tuple(x[e] for e in THETA_E)
    rep = tuple(receipt.residual_component[e] for e in THETA_E)
    # R keeps the class: same Phi1 and same cycle coordinates, exact difference.
    assert cochain.phi1(cx, rep) == cochain.phi1(cx, vector)
    assert receipt.cycle_coordinates == cochain.cycle_coordinates(cx, vector)
    assert cochain.exact_potential(cx, tuple(a - b for a, b in zip(vector, rep))) is not None
    # Projecting the representative again changes nothing (idempotence).
    again = projector.project(receipt.residual_component)
    assert again.residual_component == receipt.residual_component
    exact_only = projector.project({("a", "b"): F(1), ("b", "c"): F(1), ("a", "c"): F(2), ("d", "a"): F(-2)})
    assert exact_only.status == "EXACT_TENSION_ONLY" and exact_only.residual_norm == 0


def test_projection_conserves_the_defect():
    """DDC-R-03: raw = exact component + residual component, edge by edge."""
    projector = GraphResidualProjector(THETA_V, THETA_E)
    x = {("a", "b"): F(1, 2), ("b", "c"): F(-3), ("c", "d"): F(2), ("d", "a"): F(0), ("a", "c"): F(5, 3)}
    receipt = projector.project(x)
    for e in THETA_E:
        assert receipt.exact_component[e] + receipt.residual_component[e] == x[e]
    single = ResidualProjector([("a", "b"), ("b", "c"), ("c", "a")]).project({("a", "b"): F(1), ("b", "c"): F(2)})
    for e, value in {("a", "b"): F(1), ("b", "c"): F(2), ("c", "a"): F(0)}.items():
        assert single.exact_component[e] + single.residual_component[e] == value


def test_projectors_refuse_floats():
    with pytest.raises(ValueError, match="NOT_EXACT"):
        ResidualProjector([("a", "b"), ("b", "a")]).project({("a", "b"): 0.5})


def test_letter_boundaries_refuse_bools_and_keep_integer_rationals():
    """bool is an int subclass; 0 and 1 stay exact, True and False do not."""
    with pytest.raises(ValueError, match="target_dim must be an int"):
        DescentProjector(True)
    with pytest.raises(ValueError, match="NOT_EXACT"):
        DescentProjector(1).descend([True, 0])
    with pytest.raises(ValueError, match="NOT_EXACT"):
        DescentProjector(1).descend([0.5])
    kept = DescentProjector(1).descend([0, 1])
    assert kept.coarse_vector == (F(0),) and kept.loss_vector == (F(1),)

    lifter = StructuralLifter({"lce"})
    with pytest.raises(ValueError, match="NOT_EXACT"):
        lifter.lift([False], 1, "lce")
    with pytest.raises(ValueError, match="added_dims must be an int"):
        lifter.lift([F(1)], True, "lce")
    assert lifter.lift([0, 1], 0, "lce", trigger="ClosedResidual").lifted_vector == [F(0), F(1)]

    extractor = ContextWindowExtractor([("a", "b")])
    with pytest.raises(ValueError, match="NOT_EXACT"):
        extractor.expose({"a", "b"}, {("a", "b"): True})
    assert extractor.expose({"a", "b"}, {("a", "b"): 1}).internal_cochain == {("a", "b"): F(1)}

    gate = TypedRefusalGate({"here"}, {"w"})
    with pytest.raises(ValueError, match="NOT_EXACT"):
        gate.evaluate(OperationRequest("E", "here", "w", True, {}), F(1))
    with pytest.raises(ValueError, match="NOT_EXACT"):
        gate.evaluate(OperationRequest("E", "here", "w", F(1), {}), False)
    assert gate.evaluate(OperationRequest("E", "here", "w", 1, {}), 1) is None

    evaluator = TerminalizationEvaluator()
    with pytest.raises(TypeError):
        evaluator.evaluate(F(0), F(1), [], detector_adequate=1)
    with pytest.raises(TypeError):
        evaluator.evaluate(F(0), F(1), [], detector_adequate=0)
    with pytest.raises(ValueError, match="NOT_EXACT"):
        evaluator.evaluate(False, F(1), [])
    assert evaluator.evaluate(0, 1, [0]).verdict == "LOCAL_GREEN_FOR_SCOPE"


# -- C -------------------------------------------------------------------------


def test_context_exposure_glues_agreeing_windows_uniquely():
    edges = [("a", "b"), ("b", "c"), ("c", "d")]
    with pytest.raises(ValueError, match="SELF_LOOP"):
        ContextWindowExtractor([("a", "a")])
    extractor = ContextWindowExtractor(edges)
    ambient = {("a", "b"): F(1), ("b", "c"): F(2), ("c", "d"): F(3)}
    left = extractor.expose({"a", "b"}, ambient)
    right = extractor.expose({"c", "d"}, ambient)
    assert glue(left, right) == ambient
    other = extractor.expose({"c", "d"}, {("b", "c"): F(9), ("c", "d"): F(3)})
    assert glue(left, other) is None


def test_exposure_is_read_only_and_internal_edits_keep_the_boundary():
    """DDC-C-02 and DDC-C-04."""
    edges = [("a", "b"), ("b", "c"), ("c", "d")]
    extractor = ContextWindowExtractor(edges)
    ambient = {("a", "b"): F(1), ("b", "c"): F(2), ("c", "d"): F(3)}
    snapshot = dict(ambient)
    before = extractor.expose({"a", "b"}, ambient)
    assert ambient == snapshot
    edited = dict(ambient)
    for edge in before.internal_edges:
        edited[edge] = edited[edge] + 7
    after = extractor.expose({"a", "b"}, edited)
    assert after.boundary_cochain == before.boundary_cochain
    assert after.internal_cochain != before.internal_cochain


def test_boundary_of_an_intersection_lies_in_the_union_of_boundaries():
    edges = [(u, v) for u in "abcd" for v in "abcd" if u < v]
    extractor = ContextWindowExtractor(edges)
    windows = [set(), {"a"}, {"a", "b"}, {"b", "c"}, {"a", "c", "d"}, set("abcd")]
    for w1 in windows:
        for w2 in windows:
            both = set(extractor.expose(w1 & w2, {}).boundary_edges)
            union = set(extractor.expose(w1, {}).boundary_edges) | set(extractor.expose(w2, {}).boundary_edges)
            assert both <= union


# -- I -------------------------------------------------------------------------


def test_every_letter_including_I_enters_the_chain():
    tape = ExecutionTape()
    for letter in ("E", "R", "C", "I", "Lambda", "D", "M", "T"):
        tape.append(letter, {"x": F(3, 4), "n": 1, "flag": True, "none": None, "seq": (F(1), "s")})
    assert [e.letter for e in tape.get_entries()] == ["E", "R", "C", "I", "Λ", "D", "M", "T"]
    assert tape.verify_integrity()
    assert tape.get_entries()[0].payload["x"] == "3/4"
    with pytest.raises(ValueError, match="UNKNOWN_LETTER"):
        canonical_letter("Q")
    with pytest.raises(ValueError, match="FLOAT_FORBIDDEN"):
        canonical_json({"x": 0.5})
    with pytest.raises(ValueError, match="NOT_CANONICAL"):
        canonical_json({"x": object()})


@pytest.mark.parametrize(
    "mutate",
    [
        lambda e: replace(e, index=e.index + 1),
        lambda e: replace(e, prev_hash="0" * 64),
        lambda e: replace(e, letter="Q"),
        lambda e: replace(e, payload={"tampered": True}),
    ],
)
def test_tampering_is_located(mutate):
    tape = ExecutionTape()
    tape.append("E", {"k": 1})
    tape.append("T", {"k": 2})
    tape._entries[1] = mutate(tape._entries[1])
    assert tape.first_broken_index() == 1 and not tape.verify_integrity()


def test_a_self_consistent_forged_entry_breaks_the_link():
    from integration_tape import entry_hash

    tape = ExecutionTape()
    tape.append("E", {"k": 1})
    tape.append("T", {"k": 2})
    forged_prev = "0" * 64
    forged = replace(
        tape._entries[1],
        prev_hash=forged_prev,
        current_hash=entry_hash(1, forged_prev, "T", {"k": 2}),
    )
    tape._entries[1] = forged
    assert tape.first_broken_index() == 1


# -- Λ and D ---------------------------------------------------------------------


def test_lift_trigger_law_and_norm_preservation():
    lifter = StructuralLifter({"lce"})
    vector = [F(1), F(-2)]
    assert lifter.lift(vector, 2, "lce", trigger="ActiveClosureFailure").error == "REFUSED_LIFT_TRIGGER"
    assert lifter.lift(vector, -1, "lce").error == "INVALID_NEGATIVE_EXPANSION"
    ok = lifter.lift(vector, 3, "lce", trigger="ClosedResidual")
    assert ok.success and ok.trigger == "ClosedResidual"
    assert l1_norm(ok.lifted_vector) == l1_norm(vector)
    assert ok.lifted_vector[:2] == vector and ok.lifted_vector[2:] == [F(0)] * 3


def test_descent_books_its_ledger():
    with pytest.raises(ValueError, match="NEGATIVE_TARGET_DIMENSION"):
        DescentProjector(-1)
    with pytest.raises(ValueError):
        DescentProjector(3).descend([F(1)])
    receipt = DescentProjector(2).descend([F(1), F(2), F(3, 2), F(1, 4)])
    entry = ledger_entry(receipt)
    assert entry["loss_scalar"] == F(7, 4) and not entry["is_lossless"]
    lossless = DescentProjector(1).descend([F(5), F(0)])
    assert lossless.is_lossless and ledger_entry(lossless)["loss_vector"] == [F(0)]


# -- M -------------------------------------------------------------------------


def test_ungrounded_locus_is_an_intake_refusal_that_never_enters_the_tape():
    gate = TypedRefusalGate({"here"}, {"w"})
    receipt = gate.evaluate(OperationRequest("E", "elsewhere", "w", F(1), {}), F(10))
    assert receipt.operation == "INTAKE" and not receipt.enters_ddc_trace
    assert receipt.refusal_code in INTAKE_REASONS and receipt.refusal_code not in M_REASONS
    in_trace = gate.evaluate(OperationRequest("E", "here", None, F(1), {}), F(10))
    assert in_trace.operation == "M" and in_trace.enters_ddc_trace
    assert not set(INTAKE_REASONS) & set(M_REASONS)


# -- T -------------------------------------------------------------------------


def _facts(**overrides):
    values = {name: True for name in CONTINUATION_CONJUNCTS}
    values.update(overrides)
    return ContinuationFacts(**values)


def test_can_continue_is_the_conjunction_of_the_nine_named_conjuncts():
    assert len(CONTINUATION_CONJUNCTS) == 9
    assert can_continue(_facts()) and failed_conjuncts(_facts()) == ()
    for name in CONTINUATION_CONJUNCTS:
        facts = _facts(**{name: False})
        assert not can_continue(facts) and failed_conjuncts(facts) == (name,)
    with pytest.raises(TypeError):
        _facts(budget_available=1)
    with pytest.raises(TypeError):
        _facts(adapter_sound=0)


def test_terminal_evaluator_refuses_to_seal_open_or_blind_states():
    evaluator = TerminalizationEvaluator()
    open_ = evaluator.evaluate(F(0), F(5), [], closure_defect=F(1))
    assert not open_.is_terminal and open_.verdict == "SEAL_REFUSED_OPEN_OBSTRUCTION"
    blind = evaluator.evaluate(F(0), F(5), [], detector_adequate=False)
    assert not blind.is_terminal and blind.verdict == "SEAL_REFUSED_DETECTOR_INADEQUATE"
    green = evaluator.evaluate(F(0), F(5), [])
    assert green.verdict == "LOCAL_GREEN_FOR_SCOPE" and green.authority_terminal == "F_term:REFUSED"


def test_exact_potentials_are_unique_up_to_a_constant_per_component():
    """DDC-E-01."""
    solver = ExactRepairSolver(["a", "b", "c", "d"], [("a", "b"), ("c", "d")])
    defect = {("a", "b"): F(2), ("c", "d"): F(-7)}
    first = solver.solve(defect, gauge_vertex="a").potential
    second = solver.solve(defect, gauge_vertex="b").potential
    shifts = {v: second[v] - first[v] for v in first}
    assert shifts["a"] == shifts["b"] and shifts["c"] == shifts["d"]


def test_new_lift_coordinates_are_orthogonal_to_the_old_image():
    """DDC-L-03."""
    lifter = StructuralLifter({"lce"})
    for vector in ([F(1), F(-2)], [F(3, 4), F(0)], [F(-5), F(7, 3)]):
        lifted = lifter.lift(vector, 2, "lce", trigger="ClosedResidual").lifted_vector
        for basis in ([F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]):
            assert sum((x * y for x, y in zip(lifted, basis)), F(0)) == 0


def test_loss_is_never_negative():
    """DDC-D-01."""
    for vector in product((F(-2), F(0), F(1, 3)), repeat=4):
        for target in range(5):
            assert DescentProjector(target).descend(list(vector)).loss_scalar >= 0


def test_budget_bounds_the_number_of_charged_steps():
    """DDC-T-01: at most floor(B0 / eps) steps of cost eps fit in budget B0."""
    for budget0 in (F(0), F(1), F(7, 2), F(10)):
        for eps in (F(1, 3), F(1), F(5, 2)):
            steps, budget = 0, budget0
            while budget >= eps:
                budget -= eps
                steps += 1
            assert steps == floor(budget0 / eps) and budget >= 0
