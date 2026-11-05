"""Adversarial exactness, quotient, receipt and policy regressions."""

from dataclasses import replace
from fractions import Fraction as F

import cochain as c
import pytest
from automaton import State, Step, Witness, measure, run_tape
from context_exposure import ContextWindowExtractor
from descent import DescentProjector
from exact_repair import ExactRepairSolver
from integration_tape import ExecutionTape, canonical_json, entry_hash
from residual_projection import GraphResidualProjector, ResidualProjector
from structural_lift import StructuralLifter
from terminalization import CONTINUATION_CONJUNCTS, ContinuationFacts, TerminalizationEvaluator
from typed_refusal import OperationRequest, TypedRefusalGate

TRIANGLE = c.Complex(tuple("abc"), (("a", "b"), ("b", "c"), ("c", "a")))
FILLED = c.Complex(TRIANGLE.vertices, TRIANGLE.edges, (((0, 1), (1, 1), (2, 1)),))


def test_float_cancellation_cannot_certify_a_false_positive_phi1():
    vertices = tuple("abcdef")
    edges = (("a", "b"), ("d", "e"), ("a", "d"), ("b", "c"), ("e", "f"), ("c", "a"), ("f", "d"))
    cx = c.Complex(vertices, edges, weights=tuple(map(F, (10**16, 10**16, 1, 10**16, 10**16, 10**16, 10**16))))
    x = (0, 0, 1, 0, 0, 0, 0)
    assert c.phi1(cx, x) == 0
    with pytest.raises(c.CochainError, match="FLOAT_FORBIDDEN"):
        c.Phi1Certificate(F(1), dict.fromkeys(vertices, F(0)), (1e16, 1e16, 1.0, 1e16, 1e16, 1e16, 1e16))
    cert = c.phi1_certificate(cx, x)
    object.__setattr__(cert, "dual", (1e16,) * 7)
    assert not c.check_certificate(cx, x, cert)


@pytest.mark.parametrize("field,value", [("value", True), ("potential", {"a": 0.0}), ("dual", (False,))])
def test_certificate_fields_refuse_inexact_values(field, value):
    args = {"value": F(0), "potential": {"a": F(0)}, "dual": ()}
    args[field] = value
    with pytest.raises(c.CochainError):
        c.Phi1Certificate(**args)


def test_carriers_and_certificates_snapshot_inputs():
    vertices, edges, weights = list("abc"), list(TRIANGLE.edges), [1, 1, 1]
    cx = c.Complex(vertices, edges, weights=weights)
    weights[0] = 0
    edges.clear()
    vertices.clear()
    assert c.phi1(cx, (1, 0, 0)) == 1
    cert = c.phi1_certificate(cx, (1, 0, 0))
    with pytest.raises(TypeError):
        cert.potential["a"] = F(9)
    missing = c.Phi1Certificate(cert.value, {}, cert.dual)
    assert not c.check_certificate(cx, (1, 0, 0), missing)
    with pytest.raises(c.CochainError, match="MALFORMED_VERTEX"):
        c.Complex(("",), ())


def test_integer_matrix_solution_stays_exact():
    assert c.solve_consistent(((3, 1), (1, 1)), (1, 0)) == (F(1, 2), F(-1, 2))
    assert all(type(x) is F for x in c.solve_consistent(((3, 1), (1, 1)), (1, 0)))
    assert c.matmul(((),), ()) == ((),)
    assert c.solve_consistent((), ()) == ()


@pytest.mark.parametrize("call", [
    lambda: c.solve_consistent(((1,), (2,)), (1,)),
    lambda: c.solve_consistent(((1,),), (1, 2)),
    lambda: c.solve_consistent(((1, 2), (3,)), (1, 2)),
    lambda: c.matmul(((1, 2),), ((1,),)),
    lambda: c.matvec(((1, 2),), (1,)),
    lambda: c.transpose(((1,), (1, 2))),
    lambda: c.matmul(((1,),), ()),
    lambda: c.solve_consistent(((1.0,),), (1,)),
    lambda: c.deformation_obstruction(((True,),), ((1,),), ((0,),), ((0,),)),
])
def test_matrix_boundaries_refuse_truncation_and_inexact_scalars(call):
    with pytest.raises(c.CochainError):
        call()


@pytest.mark.parametrize("edges", [[("a", "b"), ("b", "a"), ("a", "c"), ("c", "a")],
                                    [("a", "a")], [("a", "b"), ("b", "a")] * 2])
def test_single_cycle_formula_refuses_nonsimple_walks(edges):
    with pytest.raises(ValueError, match="NOT_A_SIMPLE_CYCLE"):
        ResidualProjector(edges)


def test_graph_dictionary_apis_reject_duplicate_edges_and_untyped_data():
    for cls in (GraphResidualProjector, ExactRepairSolver):
        with pytest.raises(ValueError, match="DUPLICATE_CARRIER"):
            cls(["a", "b"], [("a", "b")] * 2)
    with pytest.raises(ValueError, match="DUPLICATE_EDGE"):
        ContextWindowExtractor([("a", "b")] * 2)
    with pytest.raises(ValueError, match="UNTYPED_DEFECT"):
        ContextWindowExtractor([("a", "b")]).expose({"a"}, {("x", "y"): F(1)})
    solver = ExactRepairSolver(["a", "b"], [("a", "b")])
    for potential in ({"a": F(0)}, {"a": F(0), "b": 1.0}):
        with pytest.raises(ValueError):
            solver.coboundary_0(potential)
    with pytest.raises(ValueError, match="UNKNOWN_GAUGE_VERTEX"):
        solver.solve({}, "unknown")


def test_tape_checkpoint_detects_rehashed_replacement_and_truncation():
    tape = ExecutionTape()
    tape.append("C", {"x": [1]})
    tape.append("T", {"x": [2]})
    checkpoint = tape.checkpoint()
    old = tape._entries[-1]
    tape._entries[-1] = replace(old, payload={"x": [9]}, current_hash=entry_hash(1, old.prev_hash, "T", {"x": [9]}))
    assert tape.verify_integrity() and not tape.verify_integrity(checkpoint)
    tape._entries.pop()
    assert tape.verify_integrity() and not tape.verify_integrity(checkpoint)
    tape._entries[0] = replace(tape._entries[0], payload={"bad": 0.5})
    assert not tape.verify_integrity()


def test_tape_does_not_alias_payloads_or_silently_coerce_keys():
    tape = ExecutionTape()
    payload = {"x": [1]}
    entry = tape.append("E", payload)
    payload["x"].append(2)
    entry.payload["x"].append(3)
    tape.get_entries()[0].payload["x"].append(4)
    assert tape.get_entries()[0].payload == {"x": [1]}
    assert tape.verify_integrity(tape.checkpoint())
    with pytest.raises(ValueError, match="NON_STRING_KEY"):
        canonical_json({1: "lost", "1": "retained"})


def test_carrier_bound_replay_rejects_forged_diagnostics_and_quotients():
    forged = State("filled", (1, 1, 1), 0, 0)
    assert run_tape(forged, [Step("T", forged)]).lawful  # Abstract hypothesis only.
    assert run_tape(forged, [Step("T", forged)], carriers={"filled": FILLED}).violations == ("DiagnosticMismatch",)
    start = measure(TRIANGLE, (1, 0, 0), "hollow")
    after = measure(TRIANGLE, (-1, 0, 0), "hollow")
    assert run_tape(start, [Step("R", after)]).lawful
    assert run_tape(start, [Step("R", after)], carriers={"hollow": TRIANGLE}).violations == ("ResidualProjectionChangedClass",)
    assert run_tape(start, [], carriers={}).violations == ("UnknownCarrier",)
    assert run_tape(State("hollow", (), 0, 0), [], carriers={"hollow": TRIANGLE}).violations == ("COCHAIN_LENGTH",)
    zero = measure(TRIANGLE, (0, 0, 0), "hollow")
    assert not run_tape(zero, [Step("R", State("hollow", (1, 0, 0), 0, 0))], carriers={"hollow": TRIANGLE}).lawful
    good = run_tape(zero, [Step("R", zero), Step("T", zero)], carriers={"hollow": TRIANGLE})
    assert good.lawful and good.tape.verify_integrity()
    weighted = c.Complex(TRIANGLE.vertices, TRIANGLE.edges, weights=(F(2),) * 3)
    other = run_tape(zero, [Step("R", zero), Step("T", zero)], carriers={"hollow": weighted})
    assert other.lawful and other.tape.genesis_hash != good.tape.genesis_hash
    with pytest.raises(ValueError, match="UNKNOWN_CONTROL"):
        run_tape(zero, [], control="typo")
    with pytest.raises(ValueError, match="carrier"):
        State("", (), 0, 0)


def test_descent_ledgers_are_immutable_and_consistent():
    receipt = DescentProjector(1).descend([F(1), F(2)])
    with pytest.raises(TypeError):
        receipt.loss_vector[0] = F(0)
    for change in ({"loss_scalar": F(0)}, {"is_lossless": True}, {"target_dim": 2}, {"status": "LOSSLESS_DESCENT"}):
        with pytest.raises(ValueError, match="INVALID_LOSS_LEDGER"):
            replace(receipt, **change)


def test_lift_needs_an_explicit_trigger_and_snapshots_licences():
    licences = {"lce"}
    lifter = StructuralLifter(licences)
    licences.clear()
    assert lifter.lift([F(1)], 1, "lce").error == "REFUSED_LIFT_TRIGGER"
    assert lifter.lift([F(1)], 1, "lce", "ClosedResidual").success


@pytest.mark.parametrize("lookback", [0, 1, -1, True, 2.5])
def test_terminal_lookback_is_a_real_window(lookback):
    with pytest.raises(ValueError):
        TerminalizationEvaluator(lookback)


def test_negative_diagnostics_and_untyped_requests_are_refused():
    evaluator = TerminalizationEvaluator()
    for residual, history, gamma in ((-1, [], 0), (0, [-1], 0), (0, [], -1)):
        with pytest.raises(ValueError, match="NEGATIVE_DIAGNOSTIC"):
            evaluator.evaluate(residual, F(1), history, gamma)
    gate = TypedRefusalGate({"here"}, {"w"})
    assert gate.evaluate(OperationRequest("NOT_DDC", "here", "w", F(0), {}), F(0)).refusal_code == "REFUSED_UNTYPED"
    with pytest.raises(ValueError, match="NEGATIVE_BUDGET_OR_COST"):
        gate.evaluate(OperationRequest("E", "here", "w", F(-1), {}), F(0))


def test_explicit_continuation_facts_gate_terminal_admission():
    evaluator = TerminalizationEvaluator()
    values = dict.fromkeys(CONTINUATION_CONJUNCTS, True)
    assert not evaluator.evaluate(F(0), F(1), [], continuation_facts=ContinuationFacts(**values)).is_terminal
    for budget in (F(0), F(-1)):
        with pytest.raises(ValueError, match="CONTRADICTORY_BUDGET_FACT"):
            evaluator.evaluate(F(1), budget, [], continuation_facts=ContinuationFacts(**values))
    for name in CONTINUATION_CONJUNCTS:
        facts = ContinuationFacts(**(values | {name: False}))
        result = evaluator.evaluate(F(1), F(1), [], detector_adequate=facts.detector_adequate, continuation_facts=facts)
        assert result.is_terminal == (name != "detector_adequate")
    with pytest.raises(ValueError, match="CONTRADICTORY_DETECTOR_FACT"):
        evaluator.evaluate(F(1), F(1), [], continuation_facts=ContinuationFacts(**(values | {"detector_adequate": False})))
    assert evaluator.evaluate(F(0), F(1), [], continuation_facts=ContinuationFacts(**(values | {"outstanding_obligation": False}))).is_terminal


def test_attaching_a_face_must_pair_nontrivially_with_the_residual():
    cx = c.Complex(tuple("abcde"), (("a", "b"), ("b", "c"), ("c", "a"), ("a", "d"), ("d", "e"), ("e", "a")),
                   (tuple((i, 1) for i in range(6)),))
    x = (F(1, 3),) * 3 + (F(-1, 3),) * 3
    assert c.exact_potential(cx, x) is None and c.gamma2(cx, x) == 0


def test_cycle_dual_flow_and_priced_terminal_counterexamples():
    vertices = tuple("abcdef")
    edges = tuple(zip(vertices, vertices[1:] + vertices[:1]))
    cx = c.Complex(vertices, edges)
    cert = c.phi1_certificate(cx, (1, 0, 0, 0, 0, 0))
    assert cert.dual == (F(1),) * 6
    start = measure(TRIANGLE, (1, 0, 0), "hollow")
    zero = measure(TRIANGLE, (0, 0, 0), "coarse")
    assert run_tape(start, [Step("D", zero, Witness(loss_ledger=True)), Step("T", zero)]).lawful
