"""test_demo_pure_symbolic_6site.py: Tests for Pure Gamma38 6-Site Scaling & GIN Index Demo.
AuthorityEffect: None.
"""

from __future__ import annotations

import pytest
from blind_problem import assert_lexical_hygiene
from demo_pure_symbolic_6site import (
    WIRE_TURNS_6SITE,
    assert_wire_purity,
    run_pure_symbolic_6site,
)
from omega_engine_pfp.domain.tower.parser import (
    GAMMA_38,
    parse_packet,
    serialize_packet,
    validate_packet_semantics,
)


def test_wire_purity_and_ast_roundtrip_6site():
    """Verify that all wire packets are in Gamma38 and roundtrip through AST."""
    for turn_info in WIRE_TURNS_6SITE:
        in_wire = turn_info["input_wire"]
        out_wire = turn_info["expected_response_wire"]

        assert assert_wire_purity(in_wire) is True
        assert assert_wire_purity(out_wire) is True

        # Assert no illegal characters
        for ch in in_wire:
            assert ch in GAMMA_38
        for ch in out_wire:
            assert ch in GAMMA_38

        # Roundtrip
        in_parsed = parse_packet(in_wire)
        validate_packet_semantics(in_parsed)
        assert serialize_packet(in_parsed) == in_wire

        out_parsed = parse_packet(out_wire)
        validate_packet_semantics(out_parsed)
        assert serialize_packet(out_parsed) == out_wire


def test_lexical_hygiene_prompts_6site():
    """Verify that all prompts in 6-site wire turns contain zero forbidden domain words and pass wire purity."""
    for turn_info in WIRE_TURNS_6SITE:
        prompt = turn_info["grammar_prompt"]
        # Must not raise ValueError
        assert_lexical_hygiene(prompt)
        assert assert_wire_purity(prompt) is True
        assert assert_wire_purity(turn_info["wire_prompt"]) is True
        assert assert_wire_purity(turn_info["input_wire"]) is True


def test_6site_pure_symbolic_execution_offline():
    """Verify offline deterministic replay of 6-site pure wire scaling."""
    res = run_pure_symbolic_6site(live=False, write_receipt=False)

    assert res["all_turns_passed"] is True
    assert len(res["turns"]) == 4
    for t in res["turns"]:
        assert t["exact_match"] is True
        assert t["purity_ok"] is True
        assert "run_root_id" in t and len(t["run_root_id"]) == 64
        assert "candidate_id" in t and len(t["candidate_id"]) == 64
        assert "content_id" in t and len(t["content_id"]) == 64
        assert t["terminal_status"] == "TransportValidated"

    props = res["lattice_properties"]
    assert props["sites"] == 6
    assert props["nodes"] == 24
    assert props["plaquettes"] == 12
    assert props["breakup_subgraphs"] == 4096
    assert props["configurations"] == 33396
    assert props["cancelling_subgraphs"] == 72
    assert props["surviving_subgraphs"] == 4024
    assert props["cancelling_doublets_paired"] == 192

    assert res["exact_partition_z"] == 33012
    assert res["transfer_matrix_trace"] == 33012
    assert res["duality_gap"] == 0
    assert res["status"] == "HOST_STAGE_CHECKS_PASSED"



def test_live_without_key_cannot_silently_replay():
    with pytest.raises(ValueError, match="provider key"):
        run_pure_symbolic_6site(live=True)


@pytest.mark.parametrize("reply", ["op<<1100><liftreq>>", "answer: op<<1100><liftreq>>"])
def test_live_wrong_or_wrapped_wire_is_refused(monkeypatch, reply):
    import demo_pure_symbolic_6site as runner
    provider = {"choices": [{"message": {"content": reply}}]}
    monkeypatch.setattr(runner, "query_openrouter_wire", lambda **kwargs: (reply, 0.1, provider))
    result = runner.run_pure_symbolic_6site(live=True, api_key="test-only")
    assert not result["all_turns_passed"]
    assert result["status"] == "REFUSED"
    assert result["total_tokens"] is None
    assert all(turn["raw_reply"] == reply and turn["raw_provider_response"] == provider for turn in result["turns"])


def test_offline_provider_metrics_are_unknown_and_writes_are_explicit():
    result = run_pure_symbolic_6site()
    assert result["total_tokens"] is None
    assert result["total_latency_seconds"] is None
    assert not result["live_model_execution"]
    with pytest.raises(ValueError, match="explicit output_dir"):
        run_pure_symbolic_6site(write_receipt=True)


@pytest.fixture(scope="module")
def exact_math_replay():
    import demo_pure_symbolic_6site as runner
    return runner.verify_6site_scaling_gin()


@pytest.fixture(autouse=True)
def reuse_exact_math_replay(monkeypatch, exact_math_replay):
    import demo_pure_symbolic_6site as runner
    monkeypatch.setattr(runner, "verify_6site_scaling_gin", lambda: exact_math_replay)
