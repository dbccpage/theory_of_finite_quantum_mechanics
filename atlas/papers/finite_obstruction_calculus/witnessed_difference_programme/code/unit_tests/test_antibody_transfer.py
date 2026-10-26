"""Independent finite quantifier and repaired-example regressions for ANT."""
from __future__ import annotations

import copy
import itertools
import json
from fractions import Fraction

import pytest
from antibody_transfer import checker as c
from antibody_transfer.replay_examples import example_input, replay, unsafe_binary_input


def test_replay_and_eleven_mutations():
    result = replay()
    assert result["status"] == "PASS"
    assert len(result["mutations"]) == 11
    assert all(m["status"] == "REFUSE" for m in result["mutations"])


def test_universal_iff_all_source_sound_sets_864_profiles():
    count = 0
    source, target = ["s0", "s1"], ["t0", "t1", "t2"]
    for smask, tmask, image in itertools.product(range(4), range(8), itertools.product([None, *source], repeat=3)):
        gs = {s for i, s in enumerate(source) if smask & (1 << i)}
        gt = {t for i, t in enumerate(target) if tmask & (1 << i)}
        adapter = {t: s for t, s in zip(target, image) if s is not None}
        p = {"source": {"id": "S", "carrier": source, "valid": sorted(gs), "profile": {}},
             "target": {"id": "T", "carrier": target, "valid": sorted(gt), "profile": {}},
             "adapter": adapter, "outside_domain": "not_applicable", "rules": [], "pool": target}
        all_sound_rules_safe = True
        for mask in range(4):
            rejection = {s for i, s in enumerate(source) if mask & (1 << i)}
            if rejection & gs:
                continue
            if any(t in gt and s in rejection for t, s in adapter.items()):
                all_sound_rules_safe = False
        assert c.transfer(p)["adapter_safe"] == all_sound_rules_safe
        count += 1
    assert count == 864


def test_unsafe_original_and_two_distinct_repairs():
    p = unsafe_binary_input()
    original = c.transfer(p)
    assert original["rules"][0]["source_sound"] is True
    assert original["rules"][0]["transfer_safe"] is False
    changed_adapter = copy.deepcopy(p)
    changed_adapter["adapter"]["1"] = "0"
    assert c.transfer(changed_adapter)["adapter_safe"] is True
    changed_rule = copy.deepcopy(p)
    changed_rule["rules"][0]["rejects"] = []
    assert c.transfer(changed_rule)["rules"][0]["admitted"] is True
    assert c.transfer(changed_rule)["adapter_safe"] is False
    assert p == unsafe_binary_input()


def test_failed_rule_does_not_change_admitted_accumulation():
    p = example_input()["transfer"]
    before = copy.deepcopy(p)
    before["rules"] = before["rules"][:1]
    assert c.transfer(p)["rejected"] == c.transfer(before)["rejected"] == ["curved"]
    assert c.transfer(p)["active_rules"] == ["circulation"]


def test_partial_adapter_passes_outside_domain_without_valid_coverage():
    p = unsafe_binary_input()
    del p["adapter"]["1"]
    report = c.transfer(p)
    assert report["adapter_safe"] is True
    assert report["valid_inputs_outside_domain"] == ["1"]
    assert report["retained"] == ["0", "1"]
    p["outside_domain"] = "reject"
    with pytest.raises(c.Refused):
        c.transfer(p)


def test_equal_metadata_does_not_prove_semantic_audit():
    p = unsafe_binary_input()
    p["target"]["valid"] = ["0"]
    p["adapter"] = {"0": "1", "1": "0"}
    assert p["source"]["profile"] == p["target"]["profile"]
    assert c.transfer(p)["adapter_safe"] is False


def test_source_validity_enlargement_keeps_audit_but_invalidates_rule():
    p = unsafe_binary_input()
    p["target"]["valid"] = ["0"]
    before = c.transfer(p)
    p["source"]["valid"] = ["0", "1"]
    after = c.transfer(p)
    assert before["adapter_safe"] and after["adapter_safe"]
    assert before["active_rules"] == ["D"] and after["active_rules"] == []


def test_singleton_many_preimages_and_duplicate_occurrences():
    p = unsafe_binary_input()
    p["target"]["valid"] = []
    p["adapter"] = {"0": "1", "1": "1"}
    assert c.transfer(p)["hits"] == 2
    p["pool"] = ["0", "1", "1", "1"]
    assert c.transfer(p)["hits"] == 4


def test_correct_gradient_and_projection_are_exact():
    p = example_input()["circulation"]
    d = [[Fraction(x) for x in row] for row in p["d0"]]
    f = [0, 1, 0]
    gradient = [sum(a * b for a, b in zip(row, f)) for row in d]
    assert gradient == [1, -1, 0]
    projected = [Fraction(1, 3), Fraction(1, 3), Fraction(2, 3)]
    potential = [0, Fraction(1, 3), Fraction(2, 3)]
    assert [sum(a * b for a, b in zip(row, potential)) for row in d] == projected
    report = c.circulation(p)
    assert {q["id"]: q["score"] for q in report["queries"]} == {
        "zero": "0", "gradient": "0", "curved": "2", "projected": "0"}


def test_positive_tolerance_requires_margin():
    p = example_input()["circulation"]
    p["queries"] = {"near": ["1/100", "0", "0"]}
    p["tolerance"] = "1/100"
    assert c.circulation(p)["queries"][0]["rejects"] is False
    p["tolerance"] = "1/200"
    assert c.circulation(p)["queries"][0]["rejects"] is True


@pytest.mark.parametrize("kind", ["annihilator", "capacity", "negative-weight", "shape"])
def test_false_dual_refused(kind):
    p = example_input()["circulation"]
    if kind == "annihilator":
        p["dual"] = ["1", "0", "0"]
    elif kind == "capacity":
        p["dual"] = ["2", "2", "-2"]
    elif kind == "negative-weight":
        p["weights"][0] = "-1"
    else:
        p["d0"][0].pop()
    with pytest.raises(c.Refused):
        c.circulation(p)


@pytest.mark.parametrize("k", [0, 1, 2, 5])
def test_truncation_failure_begins_at_derivative_degree_k(k):
    coefficients = ["0"] * (k + 1) + ["1"]
    integrand = ["0"] * k + [str(k + 1)]
    p = {"candidates": {"bad": coefficients}, "source_integrand": integrand,
         "target_integrand": integrand, "truncate_degree": k}
    report = c.polynomial_binding(p)
    assert report["adapter_safe"] is False
    assert report["rows"][0]["mapped_derivative"] == ["0"]


@pytest.mark.parametrize("n,v,g,setup", [(0, "0", "0", "0"), (0, "1", "0", "1"), (2, "0", "1", "0"), (2, "1", "1", "0")])
def test_cost_degenerate_divisions_and_zero_profit(n, v, g, setup):
    p = unsafe_binary_input()
    p["target"]["valid"] = []
    p["adapter"] = {"0": "1", "1": "1"}
    p["pool"] = ["0", "1"][:n]
    result = c.cost({"setup": setup, "guard": g, "evaluation": v, "units": "declared"}, p)
    assert result["profitable"] is False
    if not n or v == "0":
        assert result["fraction_threshold"] is None
    if n == 2 and v == g == "1":
        assert result["saving"] == "0"


def test_exact_worked_threshold_and_point_rule_can_pay_elsewhere():
    p = unsafe_binary_input()
    p["target"]["valid"] = ["0"]
    p["pool"] = ["1"] * 13 + ["0"] * 9987
    model = {"setup": "2", "guard": "1/1000", "evaluation": "1", "units": "declared"}
    assert c.cost(model, p)["hit_threshold"] == "12"
    assert c.cost(model, p)["saving"] == "1"
    p["pool"] = ["1"]
    model.update(setup="0", guard="0")
    assert c.cost(model, p)["profitable"] is True


def test_audit_cost_cases_and_no_cost_order_assumed():
    values = [c.audit_cost(p) for p in example_input()["audit_cost"]]
    assert [v["no_more_expensive"] for v in values] == [True, True, False, True, False, True]
    assert [v["strict_saving"] for v in values] == [False, True, False, False, False, False]
    assert all(v["rule_threshold"] is None for v in values[2:])


@pytest.mark.parametrize("value", [True, 1, 1.0, "1/1", "0.1", "-0"])
def test_exact_scalar_firewall(value):
    with pytest.raises(c.Refused):
        c.rational(value)


def test_stale_profile_binding_refused():
    p = example_input()
    receipt = c.evaluate(p)
    p["transfer"]["target"]["profile"]["tolerance"] = "1"
    with pytest.raises(c.Refused, match="differs"):
        c.verify(p, receipt)


def test_receipt_survives_sorted_json_object_serialization():
    p = example_input()
    receipt = c.evaluate(p)
    reloaded = json.loads(json.dumps(p, sort_keys=True))
    assert c.verify(reloaded, json.loads(json.dumps(receipt, sort_keys=True)))["status"] == "PASS"
