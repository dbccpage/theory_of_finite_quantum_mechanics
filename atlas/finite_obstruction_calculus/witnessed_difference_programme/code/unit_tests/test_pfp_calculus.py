"""Targeted custody and false-positive controls for the calculus paper replay."""

import copy

import pytest
from pfp_calculus.replay import evaluate, object_sha, prepare, replay


def test_archived_model_candidate_and_endpoint_false_positive():
    report = replay()
    valid, wrong = [case["host_receipt"] for case in report["cases"]]
    assert report["new_provider_calls"] == 0
    assert valid["mathematical_receipt"]["status"] == "checked_accept"
    assert wrong["mathematical_receipt"]["status"] == "invalid_witness"
    assert valid["endpoint_difference"] == wrong["endpoint_difference"] == "50"
    assert valid["derivative_coefficients"] == ["0", "1"]
    assert wrong["derivative_coefficients"] == ["5"]
    assert valid["candidate_id"] != wrong["candidate_id"]
    assert valid["checker_calls"] == wrong["checker_calls"] == 1
    assert valid["authority_effect"] == wrong["authority_effect"] == "None"


@pytest.mark.parametrize("field,subfield,value", [
    ("source", "candidate_id", "unrelated-candidate"),
    ("source", "raw_sha256", "0" * 64),
    ("audit", "candidate_id", "unrelated-candidate"),
    ("audit", "source_quote", "Invented source quotation"),
    ("audit", "parent_sha256", "0" * 64),
    ("audit", "authority_effect", "Grant"),
    ("extraction", "parent_sha256", "0" * 64),
    ("extraction", "proposal", '{"claimed_value":"50"}'),
    ("extraction", "input_sha256", "0" * 64),
    ("problem", "upper", "11"),
])
def test_boundaries_refuse_mutation(field, subfield, value):
    packet = prepare()
    packet[field][subfield] = value
    with pytest.raises(ValueError):
        evaluate(packet)


def test_extraction_cannot_replace_candidate_even_if_parent_digest_is_updated():
    packet = prepare()
    bad = prepare(True)
    packet["extraction"]["proposal"] = bad["extraction"]["proposal"]
    packet["extraction"]["parent_sha256"] = object_sha(packet["audit"])
    with pytest.raises(ValueError, match="EXTRACTION_BINDING"):
        evaluate(packet)


def test_replay_has_no_candidate_mutation():
    packet = prepare(True)
    before = copy.deepcopy(packet)
    result = evaluate(packet)
    assert packet == before
    assert result["mathematical_receipt"]["status"] == "invalid_witness"


def test_model_stage_provenance_is_not_fabricated():
    report = replay()
    assert len(report["remaining_obligations"]) == 2
    packet = report["cases"][0]["packet"]
    assert packet["audit"]["owner"] == packet["extraction"]["owner"] == "host"
    assert packet["source"]["actor"] == "archived_model_round_04"


def test_live_candidate_needs_independently_retained_response():
    from pfp_calculus.replay import prepare_candidate, sources

    raw = sources()["raw"]
    packet = prepare_candidate(raw, "live_model_space_bunny")
    with pytest.raises(ValueError, match="LIVE_MODEL_BYTES"):
        evaluate(packet)
    with pytest.raises(ValueError, match="LIVE_MODEL_BYTES"):
        evaluate(packet, retained_live_response=b"{}")
    result = evaluate(packet, retained_live_response=raw)
    assert result["mathematical_receipt"]["status"] == "checked_accept"


@pytest.mark.parametrize("metadata", [
    {"data": {"endpoints": []}},
    {"data": {"endpoints": [{"status": 0, "pricing": {"prompt": "0"}}]}},
    {"data": {"endpoints": [{"status": 0, "pricing": {"prompt": "0", "completion": "0.01"}}]}},
    {"data": {"endpoints": [{"status": 0, "pricing": {"prompt": "0", "completion": "0", "request": "1"}}]}},
])
def test_live_pricing_refuses_unknown_or_nonzero(metadata):
    from pfp_calculus.live_run import free_endpoints

    with pytest.raises(ValueError):
        free_endpoints(metadata)


def test_free_endpoint_and_two_level_packet():
    from pfp_calculus.live_run import free_endpoints, packet

    free_endpoints({"data": {"endpoints": [{"status": 0, "pricing": {"prompt": "0", "completion": "0"}}]}})
    assembled = packet()
    assert assembled["dispatch"]["model"] == "stealth/space-bunny-alpha"
    assert assembled["dispatch"]["max_requests"] == 1
    assert assembled["dispatch"]["allow_fallbacks"] is False
    assert '"claimed_value": "50"' not in assembled["user_prompt"]
    assert assembled["system_prompt"] and assembled["user_prompt"]


def test_retained_live_receipt_replays_without_network(monkeypatch):
    import json
    import urllib.request

    from pfp_calculus.live_run import replay_live
    from pfp_calculus.replay import ROOT

    def no_network(*args, **kwargs):
        raise AssertionError("replay must not contact a model")

    monkeypatch.setattr(urllib.request, "urlopen", no_network)
    run_dir = ROOT / "live_20261004"
    report = replay_live(run_dir)
    assert report == json.loads((run_dir / "host_receipt.json").read_text(encoding="utf-8"))
    assert report["acceptance"] is True
    assert report["model_calls_in_replay"] == 0
    assert report["provider_reported_cost_usd"] == 0
