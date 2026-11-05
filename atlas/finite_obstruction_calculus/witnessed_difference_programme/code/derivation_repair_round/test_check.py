"""Labelled host fixtures for the repair verifier; no model execution evidence."""

import copy
from fractions import Fraction
from itertools import combinations

import pytest

from .check import instance, verify_antibody, verify_observation


def host_fixture():
    a = ["0"] * 4 + ["1"] * 4
    inst = instance(a)
    cheaper = []
    shelf = {item.name: item for item in inst.instruments}
    for count in range(3):
        for chosen in combinations(shelf, count):
            pair = next((x, y) for x, y in combinations(range(8), 2)
                        if inst.query[x] != inst.query[y]
                        and all(shelf[name].outcomes[x] == shelf[name].outcomes[y] for name in chosen))
            cheaper.append({"suite": list(chosen), "uncovered_pair": [inst.states[i] for i in pair]})
    return {"A": a, "fixed_suite": ["A", "B", "C"], "fixed_cost": "7", "cheaper_subsets": cheaper,
            "adaptive_cost": "4", "adaptive_tree": {"measure": "A", "branches": {
                "0": {"measure": "B", "branches": {"0": {"query": "1"}, "1": {"query": "2"}}},
                "1": {"measure": "C", "branches": {"0": {"query": "3"}, "1": {"query": "4"}}}}},
            "adaptive_lower_bound": {"state": "1", "forcing_pairs": [
                {"other": "3", "instrument": "B"}, {"other": "5", "instrument": "A"}]}}


def test_repaired_observation_fixture_and_original_control():
    proposed = host_fixture()
    before = copy.deepcopy(proposed)
    result = verify_observation(proposed)
    assert result["accepted"] is True
    assert result["fixed_cheaper_subsets_checked"] == 7
    assert result["fixed_cost"] == "7"
    assert result["actual_tree_worst_cost"] == "4"
    assert Fraction(result["adaptive_forcing_lower_bound"]) == 4
    assert proposed == before
    with pytest.raises(ValueError, match="unresolved pair"):
        verify_observation(proposed, original_table=True)


@pytest.mark.parametrize("mutation", ["missing_cheaper", "duplicate_cheaper", "wrong_cost", "false_leaf", "missing_branch", "false_lower"])
def test_actual_submitted_observation_witness_is_not_replaced(mutation):
    proposed = host_fixture()
    if mutation == "missing_cheaper":
        proposed["cheaper_subsets"].pop()
    elif mutation == "duplicate_cheaper":
        proposed["cheaper_subsets"].append(proposed["cheaper_subsets"][0])
    elif mutation == "wrong_cost":
        proposed["adaptive_cost"] = "3"
    elif mutation == "false_leaf":
        proposed["adaptive_tree"]["branches"]["0"]["branches"]["0"]["query"] = "4"
    elif mutation == "missing_branch":
        del proposed["adaptive_tree"]["branches"]["1"]
    else:
        proposed["adaptive_lower_bound"]["forcing_pairs"] = [{"other": "7", "instrument": "A"}]
    with pytest.raises(ValueError):
        verify_observation(proposed)


@pytest.mark.parametrize("kind,adapter,rejection,target_rejection", [
    ("adapter", {"0": "1", "1": "0"}, ["1"], ["0"]),
    ("rule", {"0": "0", "1": "1"}, [], []),
])
def test_universal_and_per_rule_repairs(kind, adapter, rejection, target_rejection):
    candidate = {"repair_kind": kind, "adapter": adapter, "D": rejection,
                 "claimed_rejected": target_rejection, "soundness_reason": "host test fixture"}
    report = verify_antibody(candidate)
    assert report["accepted"]
    assert report["checked_receipt"]["active_rules"] == ["D"]
    assert report["checked_receipt"]["adapter_safe"] is (kind == "adapter")


def test_original_unsafe_rule_cannot_be_promoted_by_accumulator_safety():
    candidate = {"repair_kind": "adapter", "adapter": {"0": "0", "1": "1"}, "D": ["1"],
                 "claimed_rejected": ["1"], "soundness_reason": "false source-only proof"}
    with pytest.raises(ValueError):
        verify_antibody(candidate)


def test_actual_truncated_generation_is_retained_as_refusal():
    from .check import replay
    from .round import ROOT

    report = replay(ROOT / "live_20261004")
    assert report["accepted"] is False
    assert report["status"] == "REFUSED_INCOMPLETE_PROVIDER_RESPONSE"
    assert report["mathematical_candidate_status"] == "NOT_PARSED_OR_EVALUATED"
    assert report["candidate_status"] == "NO_ACCEPTED_CANDIDATE"
    assert report["finish_reasons"] == ["length"]
    controls = report["negative_controls"]
    assert controls["printed_observation_table"]["indistinguishable_pair"] == ["1", "5"]
    assert controls["unsafe_original_accumulation"]["checker"]["rules"][0]["target_counterexamples"] == ["1"]
