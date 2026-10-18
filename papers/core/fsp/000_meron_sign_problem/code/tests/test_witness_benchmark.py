"""Negative controls for the finite witness benchmark (no network)."""
from __future__ import annotations

import copy
import json

import pytest

from witness_benchmark import (
    build_tasks,
    canonical_digest,
    make_prompt,
    positive_control,
    score_response,
)


@pytest.fixture(scope="module")
def tasks():
    return build_tasks()


def test_source_generated_complete_witness_passes(tasks):
    packet, expected = tasks
    result = score_response(packet, expected, positive_control(expected))
    assert result["valid"]
    assert len(result["cases"]) == 4
    assert any(answer["reversing"] for answer in expected.values())
    assert any(not answer["reversing"] for answer in expected.values())


def test_public_inputs_have_no_computed_targets(tasks):
    packet, expected = tasks
    for task in packet["tasks"]:
        assert set(task) == {"id", "nodes", "edges", "weight", "signs"}
        assert "components" not in task and "total" not in task
    prompt = make_prompt(packet)
    assert all(word not in prompt.lower() for word in ("912", "19/27", "meron", "57", "199"))
    assert canonical_digest(packet) == canonical_digest(build_tasks()[0])
    changed, _ = build_tasks("7/2")
    assert canonical_digest(changed) != canonical_digest(packet)
    assert changed["tasks"][1]["signs"] == packet["tasks"][1]["signs"]


@pytest.mark.parametrize("mutation", ["pair", "coverage", "partition", "count", "float", "bool"])
def test_bad_witness_is_refused(tasks, mutation):
    packet, expected = tasks
    answers = copy.deepcopy(list(expected.values()))
    if mutation == "pair":
        answers[0]["pairs"][0][1] = answers[0]["pairs"][0][0]
    elif mutation == "coverage":
        answers[0]["pairs"].pop()
    elif mutation == "partition":
        answers[0]["components"][0].pop()
    elif mutation == "count":
        answers[0]["reversing"] = []
    elif mutation == "float":
        answers[0]["total"] = 0.0
    else:
        answers[0]["pairs"][0][0] = True
    assert not score_response(packet, expected, json.dumps({"answers": answers}))["valid"]


def test_duplicate_cases_keys_and_keyword_answers_are_refused(tasks):
    packet, expected = tasks
    answers = list(expected.values())
    assert not score_response(packet, expected, '{"answers":[],"answers":[]}')["valid"]
    answers = [answers[0]] * 4
    assert not score_response(packet, expected, json.dumps({"answers": answers}))["valid"]
    assert not score_response(packet, expected, '{"answers":"all witnesses prove cancellation"}')["valid"]


def test_deep_json_is_a_refusal_not_a_crash(tasks):
    packet, expected = tasks
    raw = "[" * 2000 + "0" + "]" * 2000
    result = score_response(packet, expected, raw)
    assert not result["valid"]
    assert result["errors"] in (["invalid_json"], ["response_shape"])


def test_cost_bound_and_bad_pricing():
    from decimal import Decimal, InvalidOperation

    from run_witness_benchmark import reserve_bound

    assert reserve_bound("a", 10, {
        "prompt": "0.001", "completion": "0.002", "request": "0.1"
    }) == Decimal("1.145")
    for bad in ("-1", "NaN", "Infinity"):
        with pytest.raises((ValueError, InvalidOperation)):
            reserve_bound("a", 10, {"prompt": bad, "completion": "0"})


def test_offline_cli_never_loads_credentials_or_network(monkeypatch, tmp_path):
    import sys

    import run_witness_benchmark as runner

    def forbidden(*args, **kwargs):
        raise AssertionError("offline mode attempted credential access")

    output = tmp_path / "control"
    monkeypatch.setattr(runner, "load_api_key", forbidden)
    monkeypatch.setattr(sys, "argv", ["runner", "--output-dir", str(output)])
    assert runner.main() == 0
    result = json.loads((output / "results.json").read_text(encoding="utf-8"))
    assert result["provider_calls"] == 0
    assert result["provider_usage"] is None
    assert result["mode"] == "host_positive_control"
    assert result["sources_unchanged"]
    protocol = json.loads((output / "protocol.json").read_text(encoding="utf-8"))
    assert "run_blind_benchmark.py" in protocol["source_sha256"]
    import hashlib

    assert hashlib.sha256((output / "prompt.txt").read_bytes()).hexdigest() == protocol["prompt_sha256"]
    with pytest.raises(SystemExit):
        runner.main()


def test_live_requires_budget_and_deadline_before_configuration(monkeypatch, tmp_path):
    import sys

    import run_witness_benchmark as runner

    monkeypatch.setattr(sys, "argv", [
        "runner", "--output-dir", str(tmp_path / "live"), "--live",
        "--models", "example/model",
    ])
    with pytest.raises(SystemExit):
        runner.main()
    assert not (tmp_path / "live").exists()


def test_duplicate_models_refused_before_output(monkeypatch, tmp_path):
    import sys

    import run_witness_benchmark as runner

    monkeypatch.setattr(sys, "argv", [
        "runner", "--output-dir", str(tmp_path / "repeat"), "--live",
        "--models", "example/model", "example/model", "--budget-usd", "1",
        "--deadline-utc", "2099-01-01T00:00:00+00:00",
    ])
    with pytest.raises(SystemExit):
        runner.main()
    assert not (tmp_path / "repeat").exists()


@pytest.mark.parametrize("raw", [True, 0.5, "-1", "NaN", "Infinity", "bad", []])
def test_invalid_reported_cost_refused(raw):
    from run_witness_benchmark import reported_cost

    with pytest.raises(ValueError):
        reported_cost({"cost": raw})
    assert reported_cost({}) is None


@pytest.mark.parametrize("cost_token,reservation", [
    ("2", "0"), ("1.0000000000000000000001", "1"),
])
def test_reported_cost_breach_halts_further_calls(monkeypatch, tmp_path, tasks,
                                                cost_token, reservation):
    import sys

    import requests

    import run_witness_benchmark as runner

    _, truth = tasks
    calls = []

    class Response:
        status_code = 200

        def __init__(self, data):
            self.data = data
            self.content = json.dumps(data).replace('"__cost__"', cost_token).encode()

        def raise_for_status(self):
            pass

        def json(self, **kwargs):
            return json.loads(self.content, **kwargs)

    catalog = {"data": [
        {"id": model, "pricing": {"prompt": "0", "completion": "0", "request": reservation}}
        for model in ("example/first", "example/second")
    ]}

    def post(*args, **kwargs):
        calls.append(kwargs["json"]["model"])
        return Response({"usage": {"cost": "__cost__"}, "choices": [{
            "finish_reason": "stop", "message": {"content": positive_control(truth)}
        }]})

    monkeypatch.setattr(requests, "get", lambda *a, **k: Response(catalog))
    monkeypatch.setattr(requests, "post", post)
    monkeypatch.setattr(runner, "load_api_key", lambda *a: "test-only")
    output = tmp_path / "breach"
    monkeypatch.setattr(sys, "argv", [
        "runner", "--output-dir", str(output), "--live", "--models",
        "example/first", "example/second", "--budget-usd", "1",
        "--deadline-utc", "2099-01-01T00:00:00+00:00",
    ])
    assert runner.main() == 1
    result = json.loads((output / "results.json").read_text(encoding="utf-8"))
    assert calls == ["example/first"]
    assert result["results"][0]["status"] == "COST_BOUND_BREACHED"
    assert result["known_provider_reported_cost_usd"] == cost_token
