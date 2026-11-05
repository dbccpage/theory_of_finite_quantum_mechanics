"""One explicitly configured free-model request followed by exact host replay.

No retry, paid fallback, dotenv discovery or authority promotion. Source files
and raw response are retained before model content is parsed. The ordinary
paper replay remains provider-free.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from .replay import ROOT, canonical, digest, evaluate, prepare, prepare_candidate, sources

MODEL = "stealth/space-bunny-alpha"
ENDPOINTS_URL = "https://openrouter.ai/api/v1/models/" + MODEL + "/endpoints"


def packet() -> dict:
    src = sources()
    schema = json.loads((ROOT / "source/round_04_prompt.json").read_text(encoding="utf-8"))["response_schema"]
    system = (
        "PFP TWO-LEVEL CONTRACT. You propose a mathematical witness; the host evaluates it. "
        "AuthorityEffect is None. The original seed and admitted profile below are immutable. "
        "Use exact canonical rational strings and polynomial coefficients in ascending powers. "
        "No floats, explanation, markdown, extra fields or evaluation claims. Return exactly "
        "one JSON object satisfying response_schema. An endpoint number alone does not "
        "establish the polynomial derivative identity. The host will replay your actual witness."
    )
    user = {
        "original_seed": src["seed"].decode("utf-8"),
        "admitted_profile": src["problem"],
        "declaration": "Riemann integral over the real interval [0,10], measure dx; integer describes endpoints only.",
        "task": "Return a polynomial antiderivative and the exact endpoint difference. Copy the input hash supplied by the response schema.",
        "worked_example_for_different_problem": {
            "problem": "Integrate the constant function 2 on the real interval [0,3].",
            "antiderivative_coefficients": ["0", "2"],
            "derivative_coefficients": ["2"],
            "endpoint_difference": "6",
            "warning": "This example is not the requested problem or its answer."
        },
        "response_schema": schema,
    }
    return {"authority_effect": "None", "system_prompt": system,
            "user_prompt": json.dumps(user, indent=2), "response_schema": schema,
            "dispatch": {"model": MODEL, "max_tokens": 2048, "temperature": 0,
                         "max_requests": 1, "allow_fallbacks": False,
                         "response_format": {"type": "json_object"}}}


def free_endpoints(metadata: dict) -> None:
    endpoints = metadata.get("data", {}).get("endpoints", [])
    active = [entry for entry in endpoints if entry.get("status") == 0]
    if not active:
        raise ValueError("NO_ACTIVE_ENDPOINT")
    for entry in active:
        prices = entry.get("pricing", {})
        if not {"prompt", "completion"} <= prices.keys():
            raise ValueError("UNKNOWN_ENDPOINT_PRICE")
        if any(Decimal(str(price)) != 0 for price in prices.values()):
            raise ValueError("ENDPOINT_IS_NOT_FREE")


def replay_live(run_dir: Path) -> dict:
    """Replay durable actual provider bytes; no provider access is needed."""
    dispatched = json.loads((run_dir / "packet.json").read_text(encoding="utf-8"))
    if canonical(dispatched) != canonical(packet()):
        raise ValueError("DISPATCH_PACKET_CHANGED")
    raw = (run_dir / "provider_response.json").read_bytes()
    response = json.loads(raw)
    choices = response.get("choices", [])
    if len(choices) != 1 or choices[0].get("finish_reason") != "stop":
        raise ValueError("INCOMPLETE_PROVIDER_REPLY")
    content = choices[0]["message"].get("content")
    if type(content) is not str or not content:
        raise ValueError("EMPTY_PROVIDER_REPLY")
    live_raw = content.encode("utf-8")
    proposed = prepare_candidate(live_raw, "live_model_space_bunny")
    receipt = evaluate(proposed, retained_live_response=live_raw)
    control = prepare(True)
    control_receipt = evaluate(control)
    usage = response.get("usage") or {}
    cost = usage.get("cost", usage.get("total_cost"))
    return {
        "authority_effect": "None", "scope": "one live PFP proposal with host audit, extraction and Stage 5",
        "generation_id": response.get("id"), "model_reported": response.get("model"),
        "provider_response_sha256": digest(raw), "packet_sha256": digest((run_dir / "packet.json").read_bytes()),
        "raw_usage": usage, "provider_reported_cost_usd": cost,
        "billing_status": "PROVIDER_REPORTED" if cost is not None else "UNKNOWN",
        "model_calls_in_original_run": 1, "model_calls_in_replay": 0,
        "model_candidate": {"packet": proposed, "stage_5": receipt},
        "host_negative_control": {"packet": control, "stage_5": control_receipt},
        "acceptance": (receipt["mathematical_receipt"]["status"] == "checked_accept"
                       and control_receipt["mathematical_receipt"]["status"] == "invalid_witness"),
        "remaining_scope": "This single example does not claim the complete numbered eight-stage model campaign or all SG demonstrations."
    }


def run(env_file: Path, run_dir: Path) -> dict:
    # Import existing provider components only when a live request is explicitly
    # requested. The paper reference tests and replay need no engine imports.
    from omega_engine_operations.domain.rop.result import Err
    from omega_engine_woland.domain.types import CandidateRequest, DecodingParamsV1
    from omega_engine_woland.infrastructure.openrouter_transport import openrouter_transport

    run_dir.mkdir(parents=True, exist_ok=False)
    pfp = packet()
    (run_dir / "packet.json").write_text(json.dumps(pfp, indent=2) + "\n", encoding="utf-8")
    # JSON is a YAML 1.2 representation; this is the canonical combined packet.
    (run_dir / "packet.yaml").write_text(json.dumps(pfp, indent=2) + "\n", encoding="utf-8")
    with urllib.request.urlopen(ENDPOINTS_URL, timeout=30) as handle:
        metadata_bytes = handle.read(1_000_001)
    if len(metadata_bytes) > 1_000_000:
        raise ValueError("ENDPOINT_METADATA_TOO_LARGE")
    (run_dir / "endpoint_metadata.json").write_bytes(metadata_bytes)
    free_endpoints(json.loads(metadata_bytes))
    request = CandidateRequest(
        system=pfp["system_prompt"], user=pfp["user_prompt"],
        decoding=DecodingParamsV1(temperature=0, response_format={"type": "json_object"},
                                  allow_fallbacks=False, require_parameters=True))
    request.check_payload_ceiling()
    transport = openrouter_transport(env_file=env_file, environ={}, timeout=60)
    if isinstance(transport, Err):
        raise ValueError("PROVIDER_CONFIGURATION_REFUSAL: " + transport.error.code)
    (run_dir / "dispatch_started.json").write_text(json.dumps({
        "time_utc": datetime.now(timezone.utc).isoformat(), "model": MODEL,
        "max_tokens": 2048, "max_requests": 1, "fallbacks": False,
        "authority_effect": "None", "runner_sha256": digest(Path(__file__).read_bytes())}, indent=2), encoding="utf-8")
    raw = transport.value(MODEL, request, 2048)
    (run_dir / "provider_response.json").write_bytes(raw)
    report = replay_live(run_dir)
    (run_dir / "host_receipt.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["assemble", "run", "replay"])
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--run-dir", type=Path)
    args = parser.parse_args()
    if args.mode == "assemble":
        print(json.dumps(packet(), indent=2))
    elif args.mode == "replay":
        print(json.dumps(replay_live(args.run_dir), indent=2))
    else:
        if args.env_file is None or args.run_dir is None:
            parser.error("run requires an explicit env-file and fresh run-dir")
        result = run(args.env_file, args.run_dir)
        print(json.dumps({key: result[key] for key in
                          ("acceptance", "generation_id", "model_reported", "provider_reported_cost_usd", "billing_status")}))
