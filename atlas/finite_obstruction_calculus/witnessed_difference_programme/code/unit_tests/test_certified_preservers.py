"""Adversarial checks of original-task binding and exact submitted witnesses."""

import importlib
import json
import os
from copy import deepcopy
from fractions import Fraction
from itertools import product
from pathlib import Path

import pytest
from certified_preservers.checker import check
from certified_preservers.examples import (
    graph_pocket,
    hadamard,
    qubit_countermodel,
    reference_problems,
    task,
)
from certified_preservers.model import (
    Carrier,
    Fuel,
    G,
    I,
    canonical_ray,
    digest,
    gaussian,
    matrix,
    strict_json,
    vector,
    wire,
)
from certified_preservers.propose import norm_class, propose
from certified_preservers.replay import produce, replay
from state_effect_readout.model import identity


@pytest.mark.parametrize("name", tuple(reference_problems()))
def test_original_examples_have_checked_submitted_witnesses(name):
    problem = reference_problems()[name]
    proposal = propose(problem)
    assert proposal["status"] == "PROPOSED"
    assert check(problem, proposal["certificate"]).status == "VERIFIED"


@pytest.mark.parametrize("value", [True, False, 1.0, float("nan"), "1.0", "1/1", [1]])
def test_inexact_or_malformed_scalars_are_rejected(value):
    with pytest.raises(ValueError):
        gaussian(value)


def test_exact_gaussian_scalar_is_admitted():
    assert gaussian(G(1, 0)) == G(1, 0)


@pytest.mark.parametrize("text", ['{"x":1,"x":2}', '{"x":NaN}', '{"x":1.0}'])
def test_decoder_has_one_strict_contract(text):
    with pytest.raises(ValueError):
        strict_json(text)


@pytest.mark.parametrize("gram", [[[1, 0], [0, -1]], [[1, 0], [0, 0]], [[1, 1], [0, 1]]])
def test_radical_or_indefinite_or_nonhermitian_input_is_not_positive(gram):
    with pytest.raises(ValueError):
        Carrier.from_wire(gram)


def test_wrong_preserver_frame_and_wrong_multiplier_are_rejected():
    problem = reference_problems()["hadamard"]
    certificate = propose(problem)["certificate"]
    changed = deepcopy(certificate)
    changed["evidence"]["multiplier"] = "2"
    assert check(problem, changed).status == "INVALID"
    changed = deepcopy(certificate)
    changed["evidence"]["matrix"] = wire(identity(2))
    assert check(problem, changed).status == "INVALID"


def test_wrong_task_and_wrong_coefficient_domain_are_rejected():
    problem = reference_problems()["reachable"]
    certificate = propose(problem)["certificate"]
    changed = deepcopy(problem)
    changed["target"] = [0, 1, 0]
    assert check(changed, certificate).status == "INVALID"
    changed["field"] = "F_2"
    assert check(changed, certificate).status == "MALFORMED"
    changed = deepcopy(problem)
    changed["gram"][0][0] = ["2", "0"]
    assert check(changed, certificate).status == "INVALID"


def test_checker_does_not_replace_a_false_submitted_witness(monkeypatch):
    problem = reference_problems()["reachable"]
    certificate = propose(problem)["certificate"]
    certificate["evidence"]["matrix"] = wire(identity(3))

    def refuse_proposer(*args, **kwargs):
        raise AssertionError("a checker called the proposer")

    monkeypatch.setattr("certified_preservers.propose.propose", refuse_proposer)
    assert check(problem, certificate).status == "INVALID"


def test_negative_certificate_and_exhaustion_are_different():
    problem = reference_problems()["norm_obstruction"]
    certificate = propose(problem)["certificate"]
    result = check(problem, certificate)
    assert result.status == "VERIFIED" and result.claim == "unitary_impossible"
    assert certificate["evidence"] == {"prime": 3, "valuation": -1}
    certificate["evidence"]["prime"] = 15
    assert check(problem, certificate).status == "INVALID"
    expensive = task("reachability", identity(2), source=[10, 1], target=[1, 0])
    stopped = propose(expensive, operation_limit=0)
    assert stopped == {"status": "UNDETERMINED", "operations": 0, "certificate": None}
    p = reference_problems()["hadamard"]
    assert check(p, propose(p)["certificate"], operation_limit=0).status == "UNDETERMINED"


def test_zero_branch_is_retained_and_cannot_be_called_success():
    problem = reference_problems()["zero_branch"]
    certificate = propose(problem)["certificate"]
    assert certificate["evidence"]["probability"] == "0"
    assert certificate["evidence"]["branch_vector"] == [["0", "0"], ["0", "0"]]
    certificate["claim"] = "positive_postselection"
    assert check(problem, certificate).status == "INVALID"


def test_full_projection_check_rejects_identity_even_if_it_fixes_target():
    problem = task("luders", identity(2), source=[1, 0], target=[1, 0])
    certificate = propose(problem)["certificate"]
    certificate["evidence"]["projection"] = wire(identity(2))
    assert check(problem, certificate).status == "INVALID"


def test_conjugation_branch_uses_the_declared_gram_matrix():
    gram = matrix([[2, I], [-I, 2]])
    problem = task("preserver", gram, frame=identity(2), images=[[1, 0], [0, -1]])
    certificate = {
        "schema": "wdp.preserver.certificate.v1",
        "problem_sha256": digest(problem),
        "claim": "global_semisimilarity",
        "evidence": {
            "matrix": wire(matrix([[1, 0], [0, -1]])),
            "branch": "conjugate",
            "multiplier": "1",
        },
    }
    assert check(problem, certificate).status == "VERIFIED"
    certificate["evidence"]["branch"] = "identity"
    assert check(problem, certificate).status == "INVALID"
    certificate["evidence"]["branch"] = "conjugate"
    certificate["evidence"]["matrix"] = wire(identity(2))
    assert check(problem, certificate).status == "INVALID"


def test_generator_binding_and_leibniz_are_not_inferred_from_a_label():
    problem = reference_problems()["generator"]
    certificate = propose(problem)["certificate"]
    changed = deepcopy(certificate)
    changed["evidence"]["hermitian_generator"] = wire(identity(2))
    assert check(problem, changed).status == "INVALID"
    bad_table = deepcopy(problem)
    bad_table["derivation"][0][0][0] = ["1", "0"]
    certificate = propose(bad_table)["certificate"]
    assert check(bad_table, certificate).status == "INVALID"


def test_finite_graph_pockets_and_closed_support_countermodel():
    assert graph_pocket(3)["probability_comparisons"] == 36
    assert graph_pocket(4)["probability_comparisons"] == 120
    counterexample = qubit_countermodel()
    assert counterexample["before"] == "1/2" and counterexample["after"] == "4/5"


def test_rank_one_constructor_against_all_small_real_targets():
    # 26 original targets; no certificate is accepted from its norm class alone.
    checked = 0
    for coordinates in product((-1, 0, 1), repeat=3):
        if not any(coordinates):
            continue
        problem = task("reachability", identity(3), source=[1, 0, 0], target=coordinates)
        certificate = propose(problem)["certificate"]
        assert check(problem, certificate).status == "VERIFIED"
        expected = (
            "unitary_impossible" if sum(x * x for x in coordinates) == 3 else "unitary_reachable"
        )
        assert certificate["claim"] == expected
        checked += 1
    assert checked == 26


def test_phase_and_norm_class_representative_invariance():
    phase = G.of(Fraction(3, 5), Fraction(4, 5))
    assert phase.norm() == 1 and phase not in (G.of(1), G.of(-1), I, -I)
    assert norm_class(Fraction(3), Fuel(100)) == (3,)
    assert norm_class(Fraction(1, 3), Fuel(100)) == (3,)
    x = vector([1, 1, 1])
    carrier = Carrier(identity(3))
    scaled = tuple(G.of(Fraction(1, 2), Fraction(1, 3)) * z for z in x)
    assert canonical_ray(x) == canonical_ray(scaled)
    assert norm_class(carrier.norm(x), Fuel(1000)) == norm_class(carrier.norm(scaled), Fuel(1000))
    assert hadamard()[0][0].norm() == Fraction(1, 2)


def test_replay_checks_saved_candidate_before_regeneration(tmp_path: Path):
    import json

    path = tmp_path / "replay.json"
    envelope = produce()
    path.write_text(json.dumps(envelope), encoding="utf-8")
    assert replay(path) == {"status": "VERIFIED", "episodes": 8, "pockets": 2, "model_calls": 0}
    envelope["records"]["reachable"]["proposal"]["certificate"]["evidence"]["matrix"] = wire(
        identity(3)
    )
    path.write_text(json.dumps(envelope), encoding="utf-8")
    with pytest.raises(ValueError, match="submitted witness"):
        replay(path)
    envelope = produce()
    envelope["sources"]["certified_preservers/checker.py"] = "0" * 64
    path.write_text(json.dumps(envelope), encoding="utf-8")
    with pytest.raises(ValueError, match="source binding"):
        replay(path)


@pytest.mark.parametrize(
    "relative",
    (
        "certified_preservers/__init__.py",
        "certified_preservers/model.py",
        "certified_preservers/checker.py",
        "certified_preservers/propose.py",
        "certified_preservers/examples.py",
        "certified_preservers/replay.py",
        "hermitianization/model.py",
        "state_effect_readout/model.py",
    ),
)
def test_each_bound_source_refuses_same_byte_substitution(tmp_path, monkeypatch, relative):
    module = importlib.import_module("certified_preservers.replay")
    code = Path(module.__file__).parents[1]
    copied = tmp_path / "code"
    for name in module.source_hashes():
        target = copied / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((code / name).read_bytes())
    victim = copied / relative
    retained = tmp_path / "retained.py"
    retained.write_bytes(victim.read_bytes())
    victim.unlink()
    os.symlink(retained, victim)
    monkeypatch.setattr(module, "__file__", str(copied / "certified_preservers/replay.py"))
    with pytest.raises(ValueError, match="non-regular"):
        module.source_hashes()


def test_replay_control_refuses_same_byte_symlink(tmp_path):
    retained = tmp_path / "retained.json"
    retained.write_text(json.dumps(produce()), encoding="utf-8")
    control = tmp_path / "replay.json"
    os.symlink(retained, control)
    with pytest.raises(ValueError, match="non-regular"):
        replay(control)


def test_replay_refuses_control_changed_during_check(tmp_path, monkeypatch):
    module = importlib.import_module("certified_preservers.replay")
    control = tmp_path / "replay.json"
    control.write_text(json.dumps(produce()), encoding="utf-8")
    real_check = module.check

    def change_control(problem, certificate):
        result = real_check(problem, certificate)
        control.write_bytes(control.read_bytes() + b" ")
        return result

    monkeypatch.setattr(module, "check", change_control)
    with pytest.raises(ValueError, match="changed during"):
        replay(control)
