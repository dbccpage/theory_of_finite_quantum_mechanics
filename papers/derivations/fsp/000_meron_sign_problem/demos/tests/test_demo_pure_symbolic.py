"""Tests for pure Gamma38 symbolic runner in demos/code/demo_pure_symbolic_meron.py.
AuthorityEffect: None.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

DEMOS_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = DEMOS_DIR.parent / "code"
REPO_ROOT = DEMOS_DIR
for p in DEMOS_DIR.parents:
    if (p / "omega_engine_pfp").exists():
        REPO_ROOT = p
        break

if str(DEMOS_DIR / "code") not in sys.path:
    sys.path.insert(0, str(DEMOS_DIR / "code"))
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from demo_pure_symbolic_meron import (
    WIRE_TURNS,
    assert_wire_purity,
    execute_pure_symbolic_offline_replay,
)
from blind_problem import assert_lexical_hygiene
from omega_engine_pfp.domain import LlmTurnRunRootV1
from omega_engine_pfp.domain.tower.parser import (
    GAMMA_38,
    parse_packet,
    serialize_packet,
)


def test_pure_symbolic_offline_replay(tmp_path: Path):
    """Verify that pure symbolic offline replay emits valid DAG and certifies Z=912."""
    receipt = execute_pure_symbolic_offline_replay()

    assert receipt["receipt_id"] == "CERT-PURE-SYMBOLIC-PFP-2026-10-02"
    assert receipt["protocol"] == "Pure Gamma38 Symbolic Wire Dialog"
    assert receipt["alphabet_size"] == 38
    assert receipt["exact_partition_binary"] == "1110010000"
    assert receipt["exact_partition_integer"] == 912
    assert receipt["duality_gap"] == 0
    assert receipt["verified"] is True
    assert len(receipt["turns"]) == 4


def test_wire_purity_and_ast_roundtrip():
    """Verify that every turn wire string strictly adheres to Gamma38 and roundtrips losslessly."""
    for t in WIRE_TURNS:
        assert assert_wire_purity(t["input_wire"]) is True
        assert assert_wire_purity(t["expected_response_wire"]) is True
        assert assert_wire_purity(t["wire_prompt"]) is True

    with pytest.raises(ValueError, match="Illegal non-Gamma38"):
        assert_wire_purity("op<<11>_illegal_character_>")

    with pytest.raises(ValueError, match="Illegal non-Gamma38"):
        assert_wire_purity("op<<11>UPPERCASE>")


def test_wire_prompts_lexical_hygiene():
    """Verify that wire prompts pass strict substring lexical hygiene and contain zero English words."""
    for t in WIRE_TURNS:
        assert t["wire_prompt"] == t["input_wire"]
        assert t["grammar_prompt"] == t["input_wire"]
        prompt = t["wire_prompt"]
        assert_lexical_hygiene(prompt)
        assert assert_wire_purity(prompt) is True
        lower = prompt.lower()
        forbidden = [
            "meron", "fermion", "hamiltonian", "hubbard",
            "chandrasekharan", "wiese", "trotter", "fock",
            "anticommut", "quantum monte carlo", "qmc", "physics"
        ]
        for word in forbidden:
            assert word not in lower, f"Forbidden word '{word}' found in prompt: {prompt}"


def test_pure_symbolic_llm_turn_integration():
    """Verify that execute_pure_symbolic_offline_replay executes all 4 turns, generates valid LlmTurnRunRootV1 with TransportValidated terminal status, and validates AST invertibility and Gamma38 purity."""
    receipt = execute_pure_symbolic_offline_replay()

    assert receipt["verified"] is True
    assert len(receipt["turns"]) == 4

    for t in receipt["turns"]:
        assert "run_root_id" in t and len(t["run_root_id"]) == 64
        assert "candidate_id" in t and len(t["candidate_id"]) == 64
        assert "content_id" in t and len(t["content_id"]) == 64

        assert t["terminal_status"] == "TransportValidated"

        in_wire = t["input_wire"]
        out_wire = t["response_wire"]
        wire_prompt = t["wire_prompt"]
        assert in_wire == wire_prompt

        assert assert_wire_purity(in_wire) is True
        assert assert_wire_purity(out_wire) is True

        for ch in in_wire:
            assert ch in GAMMA_38
        for ch in out_wire:
            assert ch in GAMMA_38

        ast_in = parse_packet(in_wire)
        assert serialize_packet(ast_in) == in_wire

        ast_out = parse_packet(out_wire)
        assert serialize_packet(ast_out) == out_wire

    assert "run_roots" in receipt
    assert len(receipt["run_roots"]) == 4

    for i, root_dict in enumerate(receipt["run_roots"]):
        root = LlmTurnRunRootV1.from_dict(root_dict)
        turn_meta = receipt["turns"][i]

        assert root.run_root_id == turn_meta["run_root_id"]
        assert root.terminal_status == "TransportValidated"
        assert turn_meta["candidate_id"] in root.candidate_ids
        assert turn_meta["content_id"] in root.content_ids
        assert len(root.attempts) == 1
        assert root.attempts[0].disposition == "AcceptedForEvaluation"
        assert root.authority_effect == "None"



@pytest.mark.parametrize("bad_reply", ["op<<1100><liftreq>>", "op<<10010><0><1><1>>", "prose op<<10010><0><1110010000><1>>"])
def test_live_valid_wrong_packet_and_prose_are_refused(monkeypatch, bad_reply):
    import demo_pure_symbolic_meron as runner
    monkeypatch.setattr(runner, "query_openrouter_wire_turn", lambda *args: {"choices": [{"message": {"content": bad_reply}}]})
    result = runner.run_live_symbolic_trial("fixture", "unused")
    assert result["all_turns_passed"] is False
    assert result["turns"][-1]["passed"] is False
    assert result["turns"][-1]["raw_reply"] == bad_reply


def test_live_matching_packets_retain_prompt_and_provider(monkeypatch):
    import demo_pure_symbolic_meron as runner
    replies = iter(t["expected_response_wire"] for t in runner.WIRE_TURNS)
    monkeypatch.setattr(runner, "query_openrouter_wire_turn", lambda *args: {"id": "fixture", "choices": [{"message": {"content": next(replies)}}]})
    result = runner.run_live_symbolic_trial("fixture", "unused")
    assert result["all_turns_passed"] is True
    assert result["prompt_contains_answer"] is False
    assert all(t["prompt"] and t["raw_provider_response"]["id"] == "fixture" for t in result["turns"])


def test_offline_replay_preserves_retained_files():
    import demo_pure_symbolic_meron as runner
    paths = [runner.CERTIFIED_SYMBOLIC_RECEIPT, runner.SYMBOLIC_DAG_TRACE]
    before = [p.read_bytes() for p in paths]
    result = runner.execute_pure_symbolic_offline_replay()
    assert [p.read_bytes() for p in paths] == before
    assert result["evidence_scope"] == "deterministic_host_fixture"
    assert result["live_provider_evidence"] is False
    assert result["exact_partition_integer"] == result["transfer_matrix_trace"]
