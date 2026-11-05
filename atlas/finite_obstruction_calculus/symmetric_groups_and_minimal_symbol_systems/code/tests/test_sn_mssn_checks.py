"""Call the shipped Paper 001 checkers. Do not reimplement them."""

from __future__ import annotations

import pytest

import sn_mssn_checks as checks


def test_demand_accounting_on_manuscript_register():
    account = checks.demand_account({"w1", "w2", "w3"}, {"w2"}, {"b1"})
    assert account.nxt == frozenset({"w1", "w3", "b1"})
    assert account.s_next == account.s - account.d + account.b
    assert account.s == 3 and account.d == 1 and account.b == 1


def test_demand_hypotheses_refuse():
    with pytest.raises(checks.DemandHypothesisError):
        checks.demand_account({"w1"}, {"missing"}, set())
    with pytest.raises(checks.DemandHypothesisError):
        checks.demand_account({"w1"}, set(), {"w1"})


def test_supplied_tag_separates_and_recovers_report():
    report = checks.supplied_tag_separates({"a": "o", "b": "o"}, {"a": 0, "b": 1}, "a", "b")
    assert report["separated"] is True
    assert report["recovered_left"] is True
    assert report["recovered_right"] is True


def test_recovery_implies_injectivity_and_three_failures():
    assert checks.old_image_injective(
        {"a": "ua", "b": "ub"}, {"ua": ("inl", "a"), "ub": ("inl", "b")}
    ) is True
    with pytest.raises(checks.RecoveryHypothesisError):
        checks.old_image_injective({"a": "same", "b": "same"}, {"same": ("inl", "a")})
    counters = checks.recovery_counterexamples()
    assert counters["off_image"]["injective"] is True
    assert counters["off_image"]["rejects_off_image"] is False
    assert counters["off_image"]["off_image_outcome"] == ("inl", "a")
    assert counters["observation"]["injective"] is True
    assert counters["observation"]["preserves_observation"] is False
    assert counters["repair"]["injective"] is True
    assert counters["repair"]["obstruction_before"] is True
    assert counters["repair"]["obstruction_after"] is True


def test_free_monoids_and_discrete_categories():
    binary = checks.free_monoids_nonisomorphic(("0", "1"), tuple("0123456789"))
    assert binary["left_count"] == 2
    assert binary["right_count"] == 10
    assert binary["nonisomorphic"] is True
    assert checks.free_monoids_nonisomorphic(("a", "b"), ("x", "y"))["nonisomorphic"] is False
    different = checks.discrete_categories_inequivalent(2, 26)
    assert different["left_iso_classes"] == 2
    assert different["right_iso_classes"] == 26
    assert different["inequivalent"] is True
    assert checks.discrete_categories_inequivalent(4, 4)["inequivalent"] is False


def test_three_contracts_and_code_collapse():
    contracts = checks.three_recovery_contracts()
    assert contracts["restricted"] == ("a",)
    assert contracts["refused_new"] == ("NON_DESCENT", "")
    assert contracts["erased_new"] == "a"
    assert contracts["old_word_refused"] == ("word", "a")
    assert contracts["contracts_differ"] is True
    collapse = checks.code_collapse_witness()
    assert collapse["aa"] == collapse["b"]
    assert collapse["collapsed"] is True


def test_components_homology_and_obstructions():
    graphs = checks.graph_component_report()
    assert graphs["empty"] == 2
    assert graphs["loop"] == 2
    assert graphs["edge"] == 1
    assert graphs["triangle"] == 1
    assert graphs["reduced_empty"] == 1
    assert graphs["loop_preserves_count"] is True
    assert graphs["edge_lowers_count"] is True
    assert checks.identity_retraction_recovers() == (2, -2)
    with pytest.raises(checks.ChainHypothesisError):
        checks.retraction_recovers_cycle((1,), (1,), (0,), (1,), (0,), (0,))
    two_point = checks.two_point_obstruction()
    assert two_point["admits_retraction"] is False
    assert sum(two_point["boundary"]) == 0
    assert any(coeff != 0 for coeff in two_point["boundary"])
    triangle = checks.triangle_obstruction()
    assert all(coeff == 0 for coeff in triangle["cycle_boundary"])
    assert triangle["face_boundary"] == triangle["cycle"]
    assert triangle["admits_retraction"] is False


def test_fiber_descent_chsh_edges_and_grammar():
    descent = checks.fiber_descent({"x": "y", "x2": "y"}, {"x": "z", "x2": "z"})
    assert descent["constant_on_fibers"] is True
    assert descent["descended"] == {"y": "z"}
    blocked = checks.fiber_descent({"x": "y", "x2": "y"}, {"x": "z", "x2": "z2"})
    assert blocked["constant_on_fibers"] is False
    assert blocked["descended"] is None
    chsh = checks.chsh_missed_orientation()
    assert chsh["selected"] == 0
    assert chsh["other"] == 4
    assert chsh["required_product"] == -1
    assert chsh["assignment_products"] == (1,)
    assert chsh["global_assignment_impossible"] is True
    edges = checks.edge_multiset_witness()
    assert edges["same_edge_multiset"] is True
    assert edges["same_traversal"] is False
    grammar = checks.grammar_inventory_matches()
    assert grammar["matches"] is True
    assert grammar["count"] == 22
    assert grammar["names"][0] == "raw_glyphs"
    assert grammar["names"][-1] == "rewrite_rule"
    assert grammar["mismatches"] == ()


def test_ledger_statuses_and_manuscript_boundaries():
    ledger = checks.ledger_status_report()
    assert ledger["count"] == 19
    assert ledger["statuses_closed"] is True
    assert ledger["proved_matches_coverage"] is True
    assert ledger["withdrawn_present"] is True
    bounds = checks.manuscript_boundaries()
    assert bounds["survivor_not_theorem"] is True
    assert bounds["physics_withdrawn"] is True
    assert bounds["archive_historical"] is True


def test_reproduction_entry_covers_proved_rows():
    report = checks.run_reproduction()
    assert report["ok"] is True
    assert report["proved_ids"] == checks.PROVED_IDS
    assert report["demand"]["s_next"] == 3
    assert report["monoids_nonisomorphic"] is True
    assert report["two_point_admits_retraction"] is False
    assert report["triangle_admits_retraction"] is False
    assert report["grammar_matches"] is True
    assert report["survivor_not_theorem"] is True
    assert report["physics_withdrawn"] is True
