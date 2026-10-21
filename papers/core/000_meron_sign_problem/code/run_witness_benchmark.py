"""Run finite witness tasks offline, or one budgeted request per named model.

A live run sends only the public fixture prompt. Credentials come from the
launching environment or an explicitly supplied env file, never discovery.
Raw prompts and provider responses are retained. No model output is a theorem.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import time
from decimal import Decimal, InvalidOperation
from pathlib import Path

from run_blind_benchmark import load_api_key
from witness_benchmark import (
    build_tasks,
    canonical_digest,
    make_prompt,
    positive_control,
    score_response,
)


def write_json(path: Path, value: object) -> None:
    def decimal_value(item):
        if isinstance(item, Decimal):
            return str(item)
        raise TypeError("unsupported receipt value")

    path.write_text(json.dumps(value, sort_keys=True, indent=2, default=decimal_value)
                    + "\n", encoding="utf-8", newline="\n")


def reserve_bound(prompt: str, max_tokens: int, pricing: dict) -> Decimal:
    """Bound text-token cost by prompt bytes plus framing and the output cap."""
    prompt_rate = Decimal(pricing["prompt"])
    completion_rate = Decimal(pricing["completion"])
    request_rate = Decimal(pricing.get("request", "0"))
    if any(not price.is_finite() or price < 0
           for price in (prompt_rate, completion_rate, request_rate)):
        raise ValueError("non-finite or negative model pricing")
    return ((len(prompt.encode("utf-8")) + 1024) * prompt_rate
            + max_tokens * completion_rate + request_rate)


def seconds_left(deadline: dt.datetime) -> float:
    return (deadline - dt.datetime.now(dt.timezone.utc)).total_seconds()


def source_hashes() -> dict[str, str]:
    """Bind every local executable module, including credential-loader imports."""
    root = Path(__file__).parent
    paths = sorted(root.glob("*.py")) + [root / "meron_schema.sql"]
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def reported_cost(usage: object) -> Decimal | None:
    """Keep missing billing unknown and reject malformed reported costs."""
    if not isinstance(usage, dict) or usage.get("cost") is None:
        return None
    raw = usage["cost"]
    if isinstance(raw, bool) or not isinstance(raw, (str, int, Decimal)):
        raise ValueError("invalid reported usage cost")
    try:
        value = Decimal(str(raw))
    except InvalidOperation as exc:
        raise ValueError("invalid reported usage cost") from exc
    if not value.is_finite() or value < 0:
        raise ValueError("invalid reported usage cost")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--models", nargs="+", default=[])
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--budget-usd", default="0")
    parser.add_argument("--max-tokens", type=int, default=3072)
    parser.add_argument("--deadline-utc")
    args = parser.parse_args()
    if len(args.models) != len(set(args.models)):
        parser.error("model IDs must be unique: one request per named model")
    if args.output_dir.exists():
        parser.error("output directory already exists; preserve previous receipts")
    try:
        ceiling = Decimal(args.budget_usd)
    except InvalidOperation:
        parser.error("budget must be a finite nonnegative decimal")
    if not ceiling.is_finite() or ceiling < 0 or args.max_tokens <= 0:
        parser.error("finite nonnegative budget and positive max tokens required")
    if args.live and (not args.models or ceiling <= 0 or not args.deadline_utc):
        parser.error("live mode requires models, positive explicit budget and UTC deadline")
    try:
        deadline = dt.datetime.fromisoformat(args.deadline_utc) if args.deadline_utc else None
    except ValueError:
        parser.error("deadline must be an ISO timestamp with a timezone")
    if deadline is not None and deadline.tzinfo is None:
        parser.error("deadline must include a timezone")
    if deadline is not None and seconds_left(deadline) <= 0:
        parser.error("deadline reached before execution")
    packet, truth = build_tasks()
    prompt = make_prompt(packet)
    args.output_dir.mkdir(parents=True)
    (args.output_dir / "prompt.txt").write_text(prompt, encoding="utf-8", newline="")
    write_json(args.output_dir / "public_inputs.json", packet)
    write_json(args.output_dir / "host_truth.json", truth)
    initial_sources = source_hashes()
    protocol = {
        "mode": "live" if args.live else "host_positive_control",
        "trials_per_available_model": 1 if args.live else 0,
        "requested_models": args.models, "fixture_q": "5/2",
        "public_input_sha256": canonical_digest(packet),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "source_sha256": initial_sources,
        "pass_criterion": "all components, reversing bits, complete pairs and sums pass",
        "analysis_scope": "four finite orbits; no discovery or model-comparison inference",
        "temperature": 0, "max_tokens": args.max_tokens,
        "seed": None, "seed_scope": "not requested; provider determinism is not assumed",
        "budget_ceiling_usd": str(ceiling),
        "deadline_utc": deadline.isoformat() if deadline else None,
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    write_json(args.output_dir / "protocol.json", protocol)
    if not args.live:
        raw = positive_control(truth)
        (args.output_dir / "host_control.txt").write_text(raw, encoding="utf-8", newline="")
        result = score_response(packet, truth, raw)
        final_sources = source_hashes()
        sources_unchanged = final_sources == initial_sources
        write_json(args.output_dir / "results.json", {
            "mode": "host_positive_control", "provider_calls": 0,
            "provider_usage": None, "result": result,
            "source_sha256_after": final_sources,
            "sources_unchanged": sources_unchanged,
        })
        print(json.dumps({"mode": "host_positive_control", "valid": result["valid"]}))
        return 0 if result["valid"] and sources_unchanged else 1

    import requests

    key = load_api_key(args.env_file)
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY unavailable under explicit configuration")
    response = requests.get("https://openrouter.ai/api/v1/models",
                            timeout=min(30, seconds_left(deadline)))
    response.raise_for_status()
    (args.output_dir / "catalog_response.json").write_bytes(response.content)
    catalog = {model["id"]: model for model in response.json()["data"]}
    retained_reservations = Decimal(0)
    known_reported_cost = Decimal(0)
    results = []
    for index, model in enumerate(args.models):
        if source_hashes() != initial_sources:
            results.append({"model": model, "status": "SOURCES_CHANGED"})
            break
        if seconds_left(deadline) <= 2:
            results.append({"model": model, "status": "DEADLINE_REACHED"})
            break
        if model not in catalog:
            results.append({"model": model, "status": "MODEL_UNAVAILABLE"})
            continue
        model_data = catalog[model]
        pricing = model_data["pricing"]
        maximum = model_data.get("top_provider", {}).get("max_completion_tokens")
        max_tokens = min(args.max_tokens, maximum) if maximum else args.max_tokens
        reservation = reserve_bound(prompt, max_tokens, pricing)
        if retained_reservations + reservation > ceiling:
            results.append({"model": model, "status": "BUDGET_REFUSED"})
            continue
        retained_reservations += reservation
        body = {
            "model": model, "messages": [{"role": "user", "content": prompt}],
            "temperature": 0, "max_tokens": max_tokens, "usage": {"include": True},
            "provider": {
                "data_collection": "deny", "sort": "price",
                "max_price": {
                    "prompt": float(Decimal(pricing["prompt"]) * 1000000),
                    "completion": float(Decimal(pricing["completion"]) * 1000000),
                },
            },
        }
        prefix = args.output_dir / f"call_{index:02d}"
        write_json(prefix.with_suffix(".request.json"), body)
        started = time.monotonic()
        entry = {"model": model, "reservation_usd": str(reservation), "pricing": pricing}
        halt = False
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": "Bearer " + key},
                json=body, timeout=min(90, seconds_left(deadline) - 1),
            )
            prefix.with_suffix(".response.json").write_bytes(response.content)
            entry["http_status"] = response.status_code
            response.raise_for_status()
            data = response.json(parse_float=Decimal)
            entry.update({
                "served_model": data.get("model"), "provider": data.get("provider"),
                "generation_id": data.get("id"), "usage": data.get("usage"),
                "finish_reason": data["choices"][0].get("finish_reason"),
            })
            cost = reported_cost(entry["usage"])
            entry["reported_cost_usd"] = None if cost is None else str(cost)
            entry["billing_status"] = "UNKNOWN" if cost is None else "PROVIDER_REPORTED"
            if cost is not None:
                known_reported_cost += cost
                if cost > reservation or known_reported_cost > ceiling:
                    entry["cost_bound_breached"] = True
                    halt = True
            raw = data["choices"][0]["message"].get("content") or ""
            prefix.with_suffix(".answer.txt").write_text(raw, encoding="utf-8", newline="")
            entry["score"] = score_response(packet, truth, raw)
            entry["status"] = ("TRUNCATED" if entry["finish_reason"] == "length"
                               else "COMPLETED")
            if halt:
                entry["status"] = "COST_BOUND_BREACHED"
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError, RecursionError) as exc:
            entry.update(status="REQUEST_FAILED", error_type=type(exc).__name__)
            if halt:
                entry["status"] = "COST_BOUND_BREACHED"
        if source_hashes() != initial_sources:
            entry["source_status"] = "SOURCES_CHANGED"
            entry["status"] = "SOURCES_CHANGED"
            halt = True
        entry["client_elapsed_seconds"] = time.monotonic() - started
        results.append(entry)
        write_json(args.output_dir / "results.json", {
            "mode": "live", "results": results,
            "retained_price_reservations_usd": str(retained_reservations),
            "budget_ceiling_usd": str(ceiling),
            "known_provider_reported_cost_usd": str(known_reported_cost),
            "source_sha256_after": source_hashes(),
            "sources_unchanged": source_hashes() == initial_sources,
            "cost_scope": "conditional price reservations; missing billing stays unknown",
        })
        if halt:
            break
    write_json(args.output_dir / "results.json", {
        "mode": "live", "results": results,
        "retained_price_reservations_usd": str(retained_reservations),
        "budget_ceiling_usd": str(ceiling),
        "known_provider_reported_cost_usd": str(known_reported_cost),
        "source_sha256_after": source_hashes(),
        "sources_unchanged": source_hashes() == initial_sources,
        "cost_scope": "conditional price reservations; missing billing stays unknown",
    })
    print(json.dumps({
        "mode": "live", "results": [
            {"model": result["model"], "status": result["status"],
             "valid": result.get("score", {}).get("valid")}
            for result in results
        ],
    }))
    return 0 if all(result["status"] in {"COMPLETED", "MODEL_UNAVAILABLE"}
                    for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
