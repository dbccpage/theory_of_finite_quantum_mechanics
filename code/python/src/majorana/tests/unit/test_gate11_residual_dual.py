"""Host tests for GATE11 residual dual (symbol_game fixtures)."""

from __future__ import annotations

from pathlib import Path

from omega_engine_pfp.fixtures.gate11_residual_dual import (
    frozen_fixtures,
    host_verify_self,
    parse_gate11_symbolic_reply,
)


COOKBOOK_REPLY = (
    Path(__file__).resolve().parents[2]
    / "omega_engine_product_planning_office"
    / "symbol_games_codex_fable_cookbook"
    / "runs"
    / "deepseek_reply_000.md"
)


def test_host_verify_self_pass() -> None:
    result = host_verify_self()
    assert result["overall_passed"] is True
    assert result["authority_effect"] == "None"
    assert result["source_kind"] == "frozen_self"
    ids = {c["id"] for c in result["checks"]}
    assert "G2_d1d0_zero" in ids
    assert "G4_exact" in ids
    assert "G5_survivor" in ids
    assert "G6_open" in ids


def test_three_frozen_fixtures() -> None:
    names = {f.name for f in frozen_fixtures()}
    assert names == {"Exact", "StabilizedSurvivor", "OpenObstruction"}


def test_ingest_deepseek_reply_000() -> None:
    if not COOKBOOK_REPLY.is_file():
        return  # skip if cookbook not checked out
    text = COOKBOOK_REPLY.read_text(encoding="utf-8")
    result = parse_gate11_symbolic_reply(text)
    assert result["overall_passed"] is True
    assert result["packet_id"] == "SG-OESOS-GATE11-FW8-001"
