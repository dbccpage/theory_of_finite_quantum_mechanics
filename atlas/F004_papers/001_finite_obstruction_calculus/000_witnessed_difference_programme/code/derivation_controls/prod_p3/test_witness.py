from __future__ import annotations

from .witness import witness


def test_witness() -> None:
    w = witness()
    assert w["goal_id"] == "PROD-P3"
    assert w["runtime_package"] == "omega_engine_epistemic_immune_system"
    assert w["bundle_matches_parent"] is True
    assert w["sound_on_valid"] is True
    assert w["adapter_pullback_verified"] is True
    assert w["trace_verified"] is True
    assert w["transfer_accepted"] is True
    assert w["stale_parent_refused"] is True
    assert w["refusal_clause"] == "PARENT_DIGEST_MISMATCH"
    assert w["authority_effect"] == "None"
