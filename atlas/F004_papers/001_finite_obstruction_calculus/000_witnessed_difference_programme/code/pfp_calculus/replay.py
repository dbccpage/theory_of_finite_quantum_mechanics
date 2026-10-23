"""Bind an archived model candidate to a host audit, extraction and evaluation.

Run from the paper's code directory with ``python -m pfp_calculus.replay``.
The source probe was round 4, not model Stages 1--4. These host records do not
retroactively assert that those model stages ran.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEMO_ID = "DEMO_001_CALCULUS_R03_R20"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(data: object) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False)


def object_sha(data: object) -> str:
    return digest(canonical(data).encode("utf-8"))


def strict_json(text: str) -> object:
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def refuse(value):
        raise ValueError("NONEXACT_JSON_NUMBER: " + value)

    return json.loads(text, object_pairs_hook=pairs, parse_float=refuse, parse_constant=refuse)


def sources() -> dict:
    manifest = json.loads((ROOT / "source_provenance.json").read_text(encoding="utf-8"))
    for row in manifest["files"]:
        if digest((ROOT / row["packaged_path"]).read_bytes()) != row["sha256"]:
            raise ValueError("ARCHIVE_SOURCE_CHANGED: " + row["packaged_path"])
    # The archival provider receipt has decimal timing and cost metadata. These
    # are retained as source declarations and never used for exact arithmetic.
    raw = (ROOT / "source/model_result.json").read_bytes()
    candidate = strict_json(raw.decode("utf-8"))
    receipt = json.loads((ROOT / "source/model_receipt.json").read_text(encoding="utf-8"))
    if canonical(receipt["candidate"]) != canonical(candidate):
        raise ValueError("ARCHIVE_RECEIPT_CANDIDATE_MISMATCH")
    problem = strict_json((ROOT / "source/problem_real.json").read_text(encoding="utf-8"))
    if candidate["input_sha256"] != object_sha(problem):
        raise ValueError("ARCHIVE_INPUT_MISMATCH")
    prompt = json.loads((ROOT / "source/round_04_prompt.json").read_text(encoding="utf-8"))
    seed = (ROOT / "source/seed.txt").read_bytes()
    if seed.decode("utf-8").strip() not in prompt["user_prompt"]:
        raise ValueError("ARCHIVE_SEED_PROMPT_MISMATCH")
    return {"manifest": manifest, "problem": problem, "seed": seed,
            "raw": raw, "candidate": candidate, "receipt": receipt}


def prepare(control: bool = False) -> dict:
    """Produce honestly labelled host records while retaining source bytes."""
    src = sources()
    candidate = copy.deepcopy(src["candidate"])
    if control:
        candidate["antiderivative_coefficients"] = ["0", "5"]
        raw = canonical(candidate).encode("utf-8")
        actor = "host_adversarial_control"
    else:
        raw = src["raw"]
        actor = "archived_model_round_04"
    return prepare_candidate(raw, actor)


def prepare_candidate(raw: bytes, actor: str) -> dict:
    """Bind externally retained response bytes without rewriting their witness."""
    src = sources()
    candidate = strict_json(raw.decode("utf-8"))
    candidate_id = actor + ":" + digest(raw)
    source = {"candidate_id": candidate_id, "actor": actor,
              "raw_response": raw.decode("utf-8"), "raw_sha256": digest(raw),
              "candidate_sha256": object_sha(candidate)}
    audit = {"owner": "host", "authority_effect": "None", "candidate_id": candidate_id,
             "parent_sha256": object_sha(source), "routing": "extract_for_check",
             "scope": "identity and source fidelity only; mathematical evaluation follows",
             "source_quote": src["seed"].decode("utf-8").strip()}
    extraction = {"owner": "host", "authority_effect": "None", "candidate_id": candidate_id,
                  "parent_sha256": object_sha(audit), "input_sha256": object_sha(src["problem"]),
                  "proposal": raw.decode("utf-8")}
    return {"demo_id": DEMO_ID, "authority_effect": "None",
            "seed": src["seed"].decode("utf-8"), "seed_sha256": digest(src["seed"]),
            "problem": src["problem"], "source": source, "audit": audit,
            "extraction": extraction}


def evaluate(packet: dict, *, retained_live_response: bytes | None = None) -> dict:
    """Execute the host Stage 5 obligation on the submitted bytes, fail closed."""
    src = sources()
    # This is a source-preserving import of the prepared campaign checker, not
    # the campaign's live runner (which implicitly loads environment files).
    from .source import calculus_reference_check as checker

    expected_fields = {"demo_id", "authority_effect", "seed", "seed_sha256", "problem",
                       "source", "audit", "extraction"}
    if type(packet) is not dict or set(packet) != expected_fields:
        raise ValueError("INVALID_PACKET")
    source, audit, extraction = packet["source"], packet["audit"], packet["extraction"]
    if packet["demo_id"] != DEMO_ID or packet["authority_effect"] != "None":
        raise ValueError("WRONG_DEMO_OR_AUTHORITY")
    if packet["seed"].encode("utf-8") != src["seed"] or packet["seed_sha256"] != digest(src["seed"]):
        raise ValueError("SEED_CHANGED")
    if canonical(packet["problem"]) != canonical(src["problem"]):
        raise ValueError("PROBLEM_CHANGED")
    actor = source.get("actor")
    if actor not in {"archived_model_round_04", "host_adversarial_control", "live_model_space_bunny"}:
        raise ValueError("UNKNOWN_SOURCE_ACTOR")
    raw = source["raw_response"].encode("utf-8")
    if actor == "archived_model_round_04" and raw != src["raw"]:
        raise ValueError("ARCHIVED_MODEL_BYTES_CHANGED")
    if actor == "live_model_space_bunny" and (retained_live_response is None or raw != retained_live_response):
        raise ValueError("LIVE_MODEL_BYTES_CHANGED_OR_UNBOUND")
    candidate_id = actor + ":" + digest(raw)
    candidate = strict_json(raw.decode("utf-8"))
    if source != {"candidate_id": candidate_id, "actor": actor, "raw_response": raw.decode("utf-8"),
                  "raw_sha256": digest(raw), "candidate_sha256": object_sha(candidate)}:
        raise ValueError("CANDIDATE_IDENTITY_MISMATCH")
    if audit != {"owner": "host", "authority_effect": "None", "candidate_id": candidate_id,
                 "parent_sha256": object_sha(source), "routing": "extract_for_check",
                 "scope": "identity and source fidelity only; mathematical evaluation follows",
                 "source_quote": src["seed"].decode("utf-8").strip()}:
        raise ValueError("AUDIT_BINDING_MISMATCH")
    if extraction != {"owner": "host", "authority_effect": "None", "candidate_id": candidate_id,
                      "parent_sha256": object_sha(audit), "input_sha256": object_sha(src["problem"]),
                      "proposal": raw.decode("utf-8")}:
        raise ValueError("EXTRACTION_BINDING_MISMATCH")
    # Replay the extracted proposal. There is no solver or expected-answer fallback.
    submitted = strict_json(extraction["proposal"])
    mathematical = checker.check(packet["problem"], submitted)
    observed_derivative, observed_endpoint = None, None
    try:
        primitive = checker.polynomial(submitted["antiderivative_coefficients"])
        lower, upper = (checker.rational(packet["problem"][name]) for name in ("lower", "upper"))
        observed_derivative = [str(x) for x in checker.derivative(primitive)]
        observed_endpoint = str(checker.evaluate(primitive, upper) - checker.evaluate(primitive, lower))
    except (KeyError, TypeError, ValueError):
        # Malformed witnesses retain their refusal receipt, without manufacturing
        # diagnostic values or replacing the submitted polynomial.
        pass
    return {"authority_effect": "None", "executor": "host", "stage": 5,
            "scope": "submitted candidate replay with host audit and extraction; not full staged campaign",
            "packet_sha256": object_sha(packet), "candidate_id": candidate_id,
            "candidate_sha256": object_sha(submitted), "checker_calls": 1,
            "checker_sha256": digest((ROOT / "source/calculus_reference_check.py").read_bytes()),
            "adapter_sha256": digest(Path(__file__).read_bytes()),
            "contract_sha256": digest((ROOT / "source/stage_5_contract.json").read_bytes()),
            "derivative_coefficients": observed_derivative,
            "endpoint_difference": observed_endpoint,
            "mathematical_receipt": mathematical}


def replay() -> dict:
    src = sources()
    cases = []
    for control in (False, True):
        packet = prepare(control)
        cases.append({"packet": packet, "host_receipt": evaluate(packet)})
    return {"authority_effect": "None", "new_provider_calls": 0,
            "archive_provider_metadata": {key: src["receipt"][key] for key in
                                          ("model", "generation_id", "prompt_tokens", "completion_tokens", "cost_usd")},
            "provider_metadata_status": "source-declared; not independently re-queried",
            "cases": cases,
            "remaining_obligations": ["Actual model Stages 1-4 and 6-8 for this calculus episode",
                                      "Integration into the general SG staged runner and its injected checker port"]}


if __name__ == "__main__":
    print(json.dumps(replay(), indent=2))
