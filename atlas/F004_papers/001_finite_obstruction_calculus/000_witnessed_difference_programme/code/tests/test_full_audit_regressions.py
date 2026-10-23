"""Counterexamples from the 2026-10-08 package review."""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as F
import json
from types import SimpleNamespace

import pytest
from sympy import Matrix

from additive_tensor.model import tensor_product
from coda_application.domain.authority import ExternalAuthority
from coda_application.domain.budget import NonTerminalBudgetGuard
from coda_application.domain.contracts import ProposalContract
from coda_application.domain.entities import TerminalKind
from coda_application.domain.firewall_engine import AuthorityFirewallEngine
from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator
from coda_application.tests.adversarial._support import make_problem
from coda_application.application import evaluate_evidence
from hermitianization.model import GaussianRational
from locality_smearing.checker import check_alternating, check_subdivision
from observer_completion.distinct_image import M, produce_completion, check_completion, produce_shelf, check_shelf
from state_effect_readout.model import StateFactor, BinaryEffectFactor, born_probability, depolarized_probability
from trotter_characteristic_polynomials import compute_exact_response_matrix
from witnessed_difference.cochains import FiniteComplex


def test_authority_binds_the_proposed_source_before_spending_grant():
    evaluated = make_problem(defect_cochain=Matrix([0, 0]))
    proposed = replace(evaluated, defect_cochain=Matrix([1, 1]))
    evidence = evaluate_evidence(evaluated)
    authority = ExternalAuthority("review-control", b"this-is-a-test-key-only")
    grant = authority.grant(evidence, "proposer")
    keys = authority.keyring()
    common = dict(evaluation=evidence, problem=evaluated, external_license_granted=grant,
                  keyring=keys, functional_evaluator=NativeFunctionalEvaluator())
    bad = AuthorityFirewallEngine.evaluate_authority(ProposalContract("proposer", proposed), **common)
    assert bad.terminal_kind is TerminalKind.REFUSED
    assert not keys.is_spent(grant)
    good = AuthorityFirewallEngine.evaluate_authority(ProposalContract("proposer", evaluated), **common)
    assert good.terminal_kind is TerminalKind.AUTHORIZED


def test_decision_seal_scope_is_explicit():
    evidence = evaluate_evidence(make_problem())
    assert evidence.is_sealed
    record = replace(evidence.layer_records[0], diagnostic_message="unsealed annotation")
    assert replace(evidence, layer_records=(record, *evidence.layer_records[1:])).is_sealed
    assert not replace(evidence, is_mathematically_valid=not evidence.is_mathematically_valid).is_sealed


@pytest.mark.parametrize("target", ["quotient", "both"])
@pytest.mark.parametrize("change", [M([[1, 0], [0, 1]], 2), M([[1, 2], [3, 5]], 2), M([[0, 1], [-1, 0]], 2)])
def test_completion_on_noncoordinate_repair_spaces(target, change):
    source = change @ M([[1], [0]], 1)
    repair = change @ M([[1], [1]], 1)
    observer = M([], 2)
    witness = produce_completion(source, repair, observer, target)
    assert witness["minimum"] == 1
    assert check_completion(source, repair, observer, witness)["accepted"]
    bad = deepcopy(witness)
    bad["dimensions"]["ambient"] = 1000000
    with pytest.raises(ValueError):
        check_completion(source, repair, observer, bad)
    bad = deepcopy(witness)
    bad["solves_original"] = True
    bad["admissible_operation"] = {"map": source.encode()}
    with pytest.raises(ValueError):
        check_completion(source, repair, observer, bad)


@pytest.mark.parametrize("field,value", [("indices", [-1]), ("indices", [True]), ("indices", [0, 0]), ("cost", 1.0), ("E", M([[0]], 1).encode())])
def test_shelf_claims_are_checked(field, value):
    source, repair, observer = M([[1]], 1), M([[]], 0), M([], 1)
    shelf, costs = (M([[1]], 1),), (F(1),)
    witness = produce_shelf(source, repair, observer, shelf, costs, "both")
    assert check_shelf(source, repair, observer, shelf, costs, "both", witness)["accepted"]
    witness[field] = value
    with pytest.raises((ValueError, TypeError)):
        check_shelf(source, repair, observer, shelf, costs, "both", witness)


@pytest.mark.parametrize("value", [-100, 0.5, True])
def test_budget_ticks_cannot_remove_or_fractionalize_fuel(value):
    guard = NonTerminalBudgetGuard(max_steps=1)
    with pytest.raises(ValueError):
        guard.tick(value)
    assert guard.step_count == 0


def test_exact_boundaries_and_immutable_rectangular_factors():
    for value in (0.5, True):
        with pytest.raises(TypeError):
            GaussianRational(value, 0)
    data = [[1], [1], [1]]
    state = StateFactor(data)
    data[0][0] = 99
    effect = BinaryEffectFactor([[1]], [[0], [0]])
    assert state.dimension == 1 and state.denominator == 3
    assert born_probability(state, effect) == 1
    with pytest.raises(TypeError):
        depolarized_probability(state, effect, 0.5)
    assert not check_alternating([[0.5], [0.5]], 0, 0)
    assert not check_subdivision([1.0], 2, [F(1, 2), F(1, 2)])
    with pytest.raises(ValueError):
        tensor_product({"a|b": 1, "a": 1}, {"c": 1, "b|c": 1})
    with pytest.raises(ValueError):
        FiniteComplex((0, 1, 2), ((0, 1), (1, 2), (0, 2)), ((0, 1, 2), (2, 1, 0)))


def test_exported_quotient_adapter_refuses_inexact_inputs():
    owner = NativeFunctionalEvaluator()
    for value in (1.0, True):
        with pytest.raises(TypeError):
            owner.solve([{}], 1, [value])
    assert owner.solve([{}], 1, [F(1)]).distance == 1


@pytest.mark.parametrize("M,r", [(0, F(1, 10)), (True, F(1, 10)), (1, 0.1), (1, -1)])
def test_spectral_procedure_refuses_undeclared_inputs(M, r):
    with pytest.raises(ValueError):
        compute_exact_response_matrix(M, r)


def test_forged_native_success_is_not_evidence(monkeypatch):
    import native_wdp
    monkeypatch.setattr(native_wdp, "find_binary", lambda *args: "/untrusted-proposer")
    forged = {"status": "PASS", "phi1": "999", "is_exact": "false", "potential": {},
              "residual": {}, "authority_effect": "Execute"}
    monkeypatch.setattr(native_wdp.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=json.dumps(forged)))
    result = native_wdp.solve_native_obstruction(["a", "b"], [("a", "b")], {("a", "b"): F(1)})
    assert result.is_err


def test_native_edge_labels_preserve_spaces_and_refuse_commas():
    import native_wdp
    good = native_wdp.solve_native_obstruction([" a", "b"], [(" a", "b")], {(" a", "b"): F(1)})
    assert good.is_ok
    assert " a" in good.value["potential"]
    bad = native_wdp.solve_native_obstruction(["a,b", "c"], [("a,b", "c")], {("a,b", "c"): F(1)})
    assert bad.is_err


@pytest.mark.parametrize("tolerance", [1e-6, F(1, 10**6)])
def test_exact_u1_refuses_near_unit_gauges(tolerance):
    from witnessed_difference.quantum import make_connection, gauge_transform, holonomy
    from witnessed_difference.projective import GaussianRational as G
    unit = G(F(1), F(0))
    near = G(F(1), F(1, 10**4))
    original = make_connection(("a", "b"), (("a", "b", unit),), tolerance=tolerance).unwrap()
    assert make_connection(("a", "b"), (("a", "b", near),), tolerance=tolerance).is_err
    assert gauge_transform(original, {"a": near, "b": near}).is_err
    phase = G(F(3, 5), F(4, 5))
    changed = gauge_transform(original, {"a": unit, "b": phase}).unwrap()
    assert holonomy(changed, ("a", "b", "a")).unwrap() == unit


def test_native_certificate_containers_do_not_change_after_construction():
    from witnessed_difference.ports import (L1Solution, ObstructionSolveRequest,
                                           QuotientCertificate, WdpObstructionSolution)
    potential, residual, dual = {"a": F(0)}, {("a", "b"): F(1)}, {("a", "b"): F(1)}
    objects = [L1Solution(F(1), potential, residual, dual, False),
               QuotientCertificate(F(1), potential, residual, dual, False),
               WdpObstructionSolution(F(1), False, potential, residual, dual)]
    hashes = [hash(obj) for obj in objects]
    potential["a"] = F(99)
    residual[("a", "b")] = F(99)
    dual[("a", "b")] = F(99)
    for obj, digest in zip(objects, hashes):
        assert obj.potential["a"] == 0 and obj.residual[("a", "b")] == 1
        assert hash(obj) == digest
        with pytest.raises(TypeError):
            obj.residual[("a", "b")] = F(7)
    vertices, edges, values = ["a", "b"], [["a", "b"]], {("a", "b"): F(1)}
    request = ObstructionSolveRequest(vertices, edges, values, values)
    before = hash(request)
    vertices[0], edges[0][0], values[("a", "b")] = "changed", "changed", F(100)
    assert request.vertices == ("a", "b") and request.edges == (("a", "b"),)
    assert hash(request) == before and request.cochain[("a", "b")] == 1


def test_partial_projection_and_source_substitution_are_refused():
    from coda_application.domain.intake import intake, IntakeError
    from coda_application.domain.layers.layer3_cs import Layer3CS
    original = make_problem()
    assert Layer3CS.evaluate(original)[1]
    assert not Layer3CS.evaluate(replace(original, projection_map={0: 0}))[1]
    assert intake(original).digest != intake(replace(original, raw_data="different source")).digest
    with pytest.raises(IntakeError):
        intake(replace(original, raw_data={"not": "declared string"}))


def test_audit_checks_reported_gamma_and_zero_value_dual():
    from coda_application.application import _certificate_checks
    from coda_application.application import evaluate_coda_pipeline
    from coda_application.domain.value_objects import ExactRational
    from coda_application.domain.entities import ResidualPair
    from coda_application.tests.adversarial._support import witness
    problem = make_problem()
    outcome = evaluate_coda_pipeline(problem)
    assert all(ok for _, ok, _ in _certificate_checks(problem, outcome))
    wrong_gamma = replace(outcome, residual_pair=ResidualPair(ExactRational(0, 1), ExactRational(1, 1)))
    assert ("gamma2", False) in [(name, ok) for name, ok, _ in _certificate_checks(problem, wrong_gamma)]
    wrong_dual = replace(outcome, dual_witness=witness(2, 2))
    assert not all(ok for _, ok, _ in _certificate_checks(problem, wrong_dual))



def test_mutation_runner_rejects_path_escape_and_misattributed_failure(tmp_path, monkeypatch):
    import importlib.util
    from pathlib import Path
    path = Path(__file__).resolve().parents[2] / "scripts" / "check_mutations.py"
    spec = importlib.util.spec_from_file_location("audit_check_mutations", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = tmp_path / "source"
    source.mkdir()
    (source / "valid.py").write_text("x = 1\n")
    monkeypatch.setattr(module, "PACKAGE", source)
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    with pytest.raises(RuntimeError):
        module._apply_mutation({"path": "code/witnessed_difference/../../outside.py"}, scratch)
    assert list(scratch.iterdir()) == []
    report = tmp_path / "results.xml"
    report.write_text('<testsuites><testsuite><testcase classname="code.tests.test_contract" name="test_expected"/>'
                      '<testcase classname="code.tests.test_contract" name="test_unrelated"><failure>assertion</failure></testcase>'
                      '</testsuite></testsuites>')
    assert not module._named_failures(report, ["code/tests/test_contract.py::test_expected"])
    assert module._named_failures(report, ["code/tests/test_contract.py::test_unrelated"])


def test_meron_extreme_integer_products_and_exact_psd():
    import numpy as np
    from meron_thermodynamic_limit import series as series
    from meron_thermodynamic_limit.checks import psd_exact
    from meron_thermodynamic_limit.positivity import w_norm_certificate, dimer_trial_certificate
    a = np.array([[-2**63]], dtype=np.int64)
    with pytest.raises(OverflowError):
        series._matmul(a, a)
    with pytest.raises(OverflowError):
        series._scaled(a, a[0])
    assert series._trace_of_product(a, a) == 2**126
    assert not psd_exact([[F(-1, 2)]])
    assert psd_exact([[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]])
    assert not psd_exact([[1, 2], [0, 1]])
    assert not psd_exact([[1, 0, 0], [0, 1]])
    with pytest.raises(ValueError):
        w_norm_certificate(F(-11, 2))
    for n, s in ((1, F(1)), (0, F(0)), (2, F(-2)), (2, 0.5)):
        with pytest.raises(ValueError):
            dimer_trial_certificate(n, s)
    assert dimer_trial_certificate(2, F(-1))["all_pass"]
    with pytest.raises(ValueError):
        series.fourier([F(1)], F(1, 2))


def test_binary_rank_against_exhaustive_image_and_suite_controls():
    import itertools
    import numpy as np
    import toric_code_observer_completion as tc
    vectors = tuple(np.array(v, dtype=int) for v in itertools.product((0, 1), repeat=3))
    for entries in itertools.product((0, 1), repeat=9):
        matrix = np.array(entries, dtype=int).reshape(3, 3)
        image_size = len({tuple(matrix @ v % 2) for v in vectors})
        assert 2 ** tc.gf2_rank(matrix) == image_size
    repairs = np.zeros((0, 1), dtype=int)
    empty = tc.minimum_cost_suite([np.array([1])], [F(1)], [], repairs)
    assert empty == {"feasible": True, "indices": (), "cost": 0}
    assert tc.check_minimum_cost_suite([np.array([1])], [F(1)], [], repairs, empty)["accepted"]
    errors = [np.array([0]), np.array([1])]
    good = tc.minimum_cost_suite([np.array([1])], [F(1)], errors, repairs)
    for change in ({"indices": (-1,)}, {"indices": (True,)}, {"indices": (0, 0)}, {"cost": 1.0}):
        with pytest.raises(ValueError):
            tc.check_minimum_cost_suite([np.array([1])], [F(1)], errors, repairs, {**good, **change})


def test_empty_report_dimension_and_finite_constructor_admission(monkeypatch):
    from witnessed_difference.quotient_observer import make_linear_quotient_observer, kernel_le
    from witnessed_difference.foundational_bridges import FiniteTransducer
    from witnessed_difference.quantum import IntegerWeights, PermutationIsometryEnvelope
    from witnessed_difference.symmetry import validate_permutation
    from witnessed_difference.retention_choices import relation_is_equivalence
    from witnessed_difference.obstruction import matrix_quotient_l1
    one = FiniteComplex(("a", "b"), (("a", "b"),), ())
    two = FiniteComplex(("a", "b", "c"), (("a", "b"), ("b", "c")), ())
    a = make_linear_quotient_observer(one, ()).unwrap()
    b = make_linear_quotient_observer(two, ()).unwrap()
    with pytest.raises(ValueError, match="source space"):
        kernel_le(a, b)
    assert kernel_le(a, a)
    for args in ((2, 1, ((0,),)), (1, 1, ((1,),)), (True, 0, ((),))):
        with pytest.raises(ValueError):
            FiniteTransducer(*args)
    with pytest.raises(ValueError):
        IntegerWeights((("a", True),))
    with pytest.raises(ValueError):
        PermutationIsometryEnvelope(1, (("a", "a"), ("a", "a")), ("a",))
    with pytest.raises(ValueError):
        validate_permutation((0.0, 1.0), 2)
    assert not relation_is_equivalence(1, frozenset({(0, 0), (1, 1)}))
    monkeypatch.setenv("WDP_FUNCTIONALS_BIN", "/nonexistent/declared-binary")
    assert matrix_quotient_l1(((0,),), (1,)).is_err


def test_progress_replay_refuses_dropped_or_renamed_fixture(tmp_path):
    import copy
    import json
    import pytest
    from certified_progress.replay import EVIDENCE, replay
    original = json.loads((EVIDENCE / "records.json").read_text())
    variants = []
    omitted = copy.deepcopy(original)
    omitted["records"].pop()
    variants.append(omitted)
    renamed = copy.deepcopy(original)
    renamed["records"][0]["name"] = "unreviewed-fixture"
    variants.append(renamed)
    duplicate = copy.deepcopy(original)
    duplicate["records"].append(duplicate["records"][0])
    variants.append(duplicate)
    for payload in variants:
        (tmp_path / "records.json").write_text(json.dumps(payload))
        with pytest.raises(ValueError):
            replay(tmp_path)
