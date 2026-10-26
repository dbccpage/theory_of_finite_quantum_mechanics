"""Public constructor and target-binding boundaries from the F005 review."""
from dataclasses import replace

import coda_cs_core as cs
import pytest
from sympy import Matrix, Rational


def test_signal_requires_named_mapping_and_known_samples():
    with pytest.raises(TypeError, match="signal_id"):
        cs.ContinuumSignal(1, {})
    with pytest.raises(TypeError, match="samples"):
        cs.ContinuumSignal("s", [])
    signal = cs.ContinuumSignal("s", {0: 2})
    assert signal.snapshot_key == ("s", ((Rational(0), Rational(2)),))
    with pytest.raises(KeyError):
        signal.evaluate_at(Rational(1))
    with pytest.raises(TypeError):
        cs.ProfileMap(1, (Rational(0),))


def test_empty_tower_fails_authority_and_constant_query_stays_mathematical():
    assert cs.ShadowTower("empty", ()).all_slices_authorized() is False
    assert cs.ShadowTower("yes", (cs.ShadowSlice("s", 1, True),)).all_slices_authorized() is True
    assert cs.ShadowTower("no", (cs.ShadowSlice("s", 1, False),)).all_slices_authorized() is False
    query = cs.ContinuumQuery("constant", 0, lambda signal: Rational(0))
    assert query.evaluator(cs.ContinuumSignal("x", {})) == 0


def test_target_is_included_and_only_verified_receipt_is_returned(monkeypatch):
    signal = cs.ContinuumSignal("target", {0: 2})
    query = cs.ContinuumQuery("constant", 0, lambda signal: Rational(0))
    tower = cs.ShadowTower("tower", (cs.ShadowSlice("s", 1, True),))
    profile = cs.ProfileMap("p", (Rational(0),))
    kwargs = {"signal": signal, "query": query, "tower": tower, "profile": profile, "test_signals": [], "factored_evaluator": lambda vector: Rational(0), "d0_transition": Matrix([[1]]), "defect_1cochain": Matrix([0])}
    result = cs.evaluate_query_authority(**kwargs)
    assert result.inhabited and result.evaluated_value == 0
    with pytest.raises(TypeError, match="has_terminalizer"):
        cs.evaluate_query_authority(**kwargs, has_terminalizer="False")
    report = cs.verify_bridge_admissibility(query=query, tower=tower, profile=profile, test_signals=[signal], factored_evaluator=lambda vector: Rational(0), d0_transition=Matrix([[1]]), defect_1cochain=Matrix([0]))
    assert report.overall_admissible
    monkeypatch.setattr(cs, "verify_bridge_admissibility", lambda **kwargs: replace(report, verified_values={}))
    refused = cs.evaluate_query_authority(**kwargs)
    assert not refused.inhabited
    assert refused.refusal_code == "UnverifiedSignalTarget"
