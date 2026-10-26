"""Call the shipped Paper 000 checkers."""

from __future__ import annotations

import pytest

import genesis_checks as checks


def test_quotient_and_history_refuse_collapsed_answers():
    assert checks.quotient_factor({"x": "q", "y": "q"}, {"x": "yes", "y": "no"}) is None
    assert checks.quotient_factor({"x": "qx", "y": "qy"}, {"x": "yes", "y": "no"}) == {
        "qx": "yes",
        "qy": "no",
    }
    assert checks.history_auditor({"h1": "v", "h2": "v"}, {"h1": "s1", "h2": "s2"}) is None
    assert checks.history_auditor({"h1": "v1", "h2": "v2"}, {"h1": "s1", "h2": "s2"}) == {
        "v1": "s1",
        "v2": "s2",
    }


def test_admission_cost_and_pair_rounds():
    assert checks.single_admission_report() == {"datum": False, "form": False, "inst": False}
    assert checks.form_then_instance() is True
    assert checks.max_pair_rounds(4) == 6
    assert checks.monotone_pair_rounds(4) == 6
    assert checks.monotone_pair_rounds(0) == 0
    assert checks.monotone_pair_rounds(2) == 1


def test_endpoint_distinction_and_ledger():
    assert checks.endpoint_distinct("a", "b", False) is True
    with pytest.raises(checks.FactorError):
        checks.endpoint_distinct("a", "a", True)
    ledger = checks.ledger_status_report()
    assert ledger["ids_unique"] is True
    assert ledger["statuses_nonempty"] is True
    assert ledger["checked_ids_present"] is True
    assert ledger["toy_status_closure"] is False
    assert "WDP-P000-001" in ledger["ids"]
    assert "WDP-P000-025" in ledger["ids"]
    report = checks.run_reproduction()
    assert report["ok"] is True
    assert report["checked_ids"] == list(checks.CHECKED_IDS)
