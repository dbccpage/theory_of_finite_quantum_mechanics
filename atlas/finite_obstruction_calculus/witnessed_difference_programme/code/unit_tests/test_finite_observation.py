"""Counterexamples and certificate corruption tests for finite priced observation."""

from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as F

import pytest
from finite_observation import solver
from finite_observation.replay_examples import (
    adaptive_instance,
    build_bundle,
    fano_instance,
    fixtures,
    replay_bundle,
)
from finite_observation.solver import (
    Instance,
    Instrument,
    solve,
    unresolved_pairs,
    verify,
    verify_lp_pair,
)


def test_corrected_adaptive_gap_has_actual_forcing_pairs_and_strategy():
    instance = adaptive_instance()
    cert = solve(instance)
    assert verify(instance, cert).accepted
    assert (cert["fixed"]["value"], cert["adaptive"]["value"]) == ("7", "4")
    assert cert["adaptive"]["table"][255]["choice"] == 0
    assert cert["adaptive"]["table"][15]["choice"] == 1
    assert cert["adaptive"]["table"][240]["choice"] == 2
    for x, y, required in ((0, 2, 1), (0, 4, 0), (4, 6, 2)):
        assert [i for i, item in enumerate(instance.instruments) if item.outcomes[x] != item.outcomes[y]] == [required]


def test_submitted_adaptive_table_is_infeasible_not_four_versus_seven():
    instance = adaptive_instance(submitted=True)
    cert = solve(instance)
    assert verify(instance, cert).accepted
    assert cert["fixed"]["value"] is None and cert["adaptive"]["value"] is None
    assert cert["infeasible_pair"] == [0, 4]
    assert instance.query[0] != instance.query[4]
    assert all(item.outcomes[0] == item.outcomes[4] for item in instance.instruments)
    false_claim = deepcopy(cert)
    false_claim["fixed"]["suite_mask"] = 7
    false_claim["fixed"]["value"] = "7"
    false_claim["adaptive"]["value"] = "4"
    assert not verify(instance, false_claim).accepted


def test_miniature_has_two_unresolved_pairs_and_one_covered_pair():
    instance = fixtures()["infeasible_miniature"]
    assert unresolved_pairs(instance) == ((0, 1), (1, 2))
    assert all(item.outcomes[1] != item.outcomes[2] for item in instance.instruments)
    cert = solve(instance)
    assert verify(instance, cert).accepted and cert["infeasible_pair"] == [0, 1]


def test_fano_exact_integer_optimum_exceeds_verified_lp_optimum():
    instance = fano_instance()
    cert = solve(instance)
    assert verify(instance, cert).accepted and cert["fixed"]["value"] == "3"
    lp = verify_lp_pair(instance, (F(1, 3),) * 7, (F(1, 3),) * 7)
    assert lp == F(7, 3) < F(cert["fixed"]["value"])
    assert sum(int(row["sufficient"]) for row in cert["fixed"]["table"] if row["cost"] in ("0", "1", "2")) == 0
    false = deepcopy(cert)
    false["fixed"]["value"] = "7/3"
    assert not verify(instance, false).accepted
    with pytest.raises(ValueError, match="dual"):
        verify_lp_pair(instance, (F(1, 3),) * 7, (F(1),) * 7)


def test_visible_report_is_free_before_adaptive_measurements():
    instance = fixtures()["visible_report_resolves"]
    cert = solve(instance)
    assert verify(instance, cert).accepted
    assert cert["adaptive"]["table"][3]["value"] is None
    assert cert["fixed"]["value"] == cert["adaptive"]["value"] == "0"


def test_coarsening_increases_requirements_and_refinement_cannot_increase_price():
    fine = Instance(("a", "b"), ("a", "b"), ("0", "1"), (Instrument("test", ("0", "1"), F(2)),))
    coarse = replace(fine, visible=("*", "*"))
    assert unresolved_pairs(fine) == () and unresolved_pairs(coarse) == ((0, 1),)
    assert solve(fine)["fixed"]["value"] == "0"
    assert solve(coarse)["fixed"]["value"] == "2"


def test_every_splitting_instrument_separates_a_cross_question_pair_on_nonconstant_sets():
    instance = adaptive_instance()
    for mask in range(1, 256):
        members = [x for x in range(8) if mask & (1 << x)]
        if len({instance.query[x] for x in members}) <= 1:
            continue
        for item in instance.instruments:
            splits = len({item.outcomes[x] for x in members}) >= 2
            separates = any(instance.query[x] != instance.query[y] and item.outcomes[x] != item.outcomes[y]
                            for x in members for y in members)
            assert splits == separates


@pytest.mark.parametrize("mutation", ["omit_fixed", "omit_adaptive", "fixed_cost", "fixed_coverage", "adaptive_cost", "adaptive_choice", "authority", "bool_mask", "nan_cost"])
def test_complete_certificate_rejects_tampering(mutation):
    instance = adaptive_instance()
    cert = solve(instance)
    match mutation:
        case "omit_fixed": cert["fixed"]["table"].pop()
        case "omit_adaptive": cert["adaptive"]["table"].pop(15)
        case "fixed_cost": cert["fixed"]["table"][0]["cost"] = "7"
        case "fixed_coverage": cert["fixed"]["table"][0]["sufficient"] = True
        case "adaptive_cost": cert["adaptive"]["table"][15]["value"] = "0"
        case "adaptive_choice": cert["adaptive"]["table"][255]["choice"] = 1
        case "authority": cert["authority_effect"] = "Grant"
        case "bool_mask": cert["fixed"]["table"][0]["mask"] = False
        case "nan_cost": cert["adaptive"]["value"] = float("nan")
    result = verify(instance, cert)
    assert not result.accepted and result.code == "INVALID_CERTIFICATE"


def test_wrong_task_price_or_outcome_never_reuses_original_certificate():
    instance = adaptive_instance()
    cert = solve(instance)
    changed = (
        replace(instance, query=("changed",) + instance.query[1:]),
        replace(instance, instruments=(replace(instance.instruments[0], cost=F(2)),) + instance.instruments[1:]),
        replace(instance, instruments=(replace(instance.instruments[0], outcomes=("changed",) + instance.instruments[0].outcomes[1:]),) + instance.instruments[1:]),
    )
    assert all(verify(item, cert).code == "INPUT_MISMATCH" for item in changed)


def test_false_infeasibility_witness_is_rejected():
    instance = adaptive_instance(submitted=True)
    cert = solve(instance)
    cert["infeasible_pair"] = [0, 2]
    assert not verify(instance, cert).accepted


def test_replay_never_calls_solver_to_replace_submitted_table(monkeypatch):
    bundle = build_bundle()
    monkeypatch.setattr(solver, "solve", lambda *_: pytest.fail("checker called the solver"))
    assert replay_bundle(bundle)["adaptive_corrected"]["adaptive"] == "4"
    bundle["adaptive_corrected"]["certificate"]["adaptive"]["table"][255]["value"] = "1"
    with pytest.raises(ValueError, match="Bellman"):
        replay_bundle(bundle)


@pytest.mark.parametrize("price", [1, True, 1.0, F(0), F(-1)])
def test_price_contract_rejects_nonpositive_or_nonexact_data(price):
    instance = Instance(("a",), ("*",), ("0",), (Instrument("m", ("0",), price),))
    with pytest.raises(TypeError, match="positive exact"):
        solve(instance)


def test_empty_state_and_empty_shelf_are_supported_without_invented_observations():
    instance = Instance((), (), (), ())
    cert = solve(instance)
    assert verify(instance, cert).accepted
    assert cert["fixed"]["value"] == cert["adaptive"]["value"] == "0"


def test_resource_cap_refuses_before_exhaustion():
    states = tuple(str(i) for i in range(11))
    with pytest.raises(ValueError, match="cap"):
        solve(Instance(states, states, states, ()))


@pytest.mark.parametrize("text", ["1e1000000000", "1e-1000000000", "1.0", " 1", "1\n", "1_0", "１２", "1" * 4097])
def test_invalid_cost_syntax_never_reaches_fraction_construction(monkeypatch, text):
    monkeypatch.setattr(solver, "Fraction", lambda *_: pytest.fail("arithmetic before syntax admission"))
    with pytest.raises(TypeError, match="canonical"):
        solver._rational(text)


def test_cost_text_cap_accepts_sums_of_twelve_maximum_size_prices():
    size = 2**255
    instruments = tuple(Instrument(str(i), ("0", "1"), F(size-2, size-2*i-1)) for i in range(12))
    instance = Instance(("a", "b"), ("*", "*"), ("a", "b"), instruments)
    certificate = solve(instance)
    total = certificate["fixed"]["table"][-1]["cost"]
    assert len(total) > 160 and F(total).denominator.bit_length() > 256
    assert len(total) < solver.MAX_COST_TEXT
    assert verify(instance, certificate).accepted
