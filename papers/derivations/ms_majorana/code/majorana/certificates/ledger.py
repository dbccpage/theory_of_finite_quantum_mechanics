from __future__ import annotations
# SPDX-License-Identifier: Apache-2.0


import json
import hashlib
from pathlib import Path
from typing import Any

from omega_engine.crates.majorana.core.gf2_schema import mod2
from omega_engine.crates.majorana.carriers.parity_carrier import MajoranaParityCarrier
from omega_engine.crates.majorana.engines.terminalizer import terminalize


INTERPRETATIONS = {
    "Exact": "locally generated; certificate alpha repairs the residual",
    "ClosedResidual": "coherent but not locally repairable",
    "OpenObstruction": "propagates into a higher coherence contradiction",
    "RepresentationInvalid": "declared carrier fails shape validation or D1*D0 = 0",
    "TypedHarmonic": (
        "coherent, not locally repairable, and identified: a named class in "
        "H^1 with a certified l1-minimal witness"
    ),
}

CLASSIFIED_FIELDS = (
    "dim_h1",
    "class_coordinates",
    "class_id",
    "phi1_weight",
    "phi1_exact",
    "phi1_representative",
    "phi1_alpha",
    "phi1_searched",
    "phi1_coset_size",
    "phi1_verified",
    "terminal_reading",
    "authority_effect",
)


def canonical_json_bytes(payload: Any) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def stable_hash(payload: Any, domain: str) -> str:
    return hashlib.sha256(
        canonical_json_bytes({"domain": domain, "payload": payload})
    ).hexdigest()


def carrier_payload(d0: list[list[int]], d1: list[list[int]], residual: list[int]) -> dict[str, Any]:
    carrier = MajoranaParityCarrier(
        carrier_kind="majorana_parity_gf2",
        coefficient_field="GF2",
        D0=d0,
        D1=d1,
        residual=residual,
    ).normalized()
    return {
        "carrier_kind": carrier.carrier_kind,
        "coefficient_field": carrier.coefficient_field,
        "C0_dim": carrier.C0_dim,
        "C1_dim": carrier.C1_dim,
        "C2_dim": carrier.C2_dim,
        "D0": carrier.D0,
        "D1": carrier.D1,
        "residual": carrier.residual,
        "metadata": carrier.metadata,
    }


def ledger_row(d0: list[list[int]], d1: list[list[int]], residual: list[int]) -> dict[str, Any]:
    carrier = carrier_payload(d0, d1, residual)
    result = terminalize(d0, d1, residual)
    carrier_hash = stable_hash(carrier, domain="majorana_gf2_carrier")
    certificate_id = "cert_" + stable_hash(carrier, domain="majorana_gf2_certificate")

    q1_norm_val = result["q1_norm"]
    q1_norm_str = str(q1_norm_val) if q1_norm_val is not None else "null"

    replay_payload = {
        "certificate_id": certificate_id,
        "carrier_hash": carrier_hash,
        "terminal_status": result["terminal_status"],
        "q1_norm": q1_norm_str,
        "certificate_alpha": result["certificate_alpha"],
        "normal_form": result["normal_form"],
        "coherence_witness": result["coherence_witness"],
    }
    replay_hash = stable_hash(replay_payload, domain="majorana_gf2_replay")

    return {
        **carrier,
        "certificate_id": certificate_id,
        "carrier_hash": carrier_hash,
        "terminal_status": result["terminal_status"],
        "interpretation": INTERPRETATIONS.get(result["terminal_status"], ""),
        "reason": result.get("reason"),
        "certificate_alpha": result["certificate_alpha"],
        "normal_form": result["normal_form"],
        "coherence_witness": result["coherence_witness"],
        "q1_norm": q1_norm_str,
        "algebraic_class_id": result["algebraic_class_id"],
        "replay_hash": replay_hash,
    }


def classified_ledger_row(
    d0: list[list[int]],
    d1: list[list[int]],
    residual: list[int],
    budget: int | None = None,
    instance: str | None = None,
) -> dict[str, Any]:
    """A replayable row carrying the full five-terminal classification.

    Same carrier hash as ``ledger_row`` -- the carrier is the same object -- but
    a distinct replay domain, because the payload includes the cohomology and
    l1 fields. ``budget`` is part of the replayed input: a different budget can
    legitimately produce a different terminal, so it is recorded, not implied.
    """
    from omega_engine.crates.majorana.engines.classifier import DEFAULT_BUDGET, classify

    effective_budget = DEFAULT_BUDGET if budget is None else budget
    carrier = carrier_payload(d0, d1, residual)
    result = classify(d0, d1, residual, budget=effective_budget)
    carrier_hash = stable_hash(carrier, domain="majorana_gf2_carrier")
    certificate_id = "cert_" + stable_hash(
        {"carrier": carrier, "budget": effective_budget},
        domain="majorana_gf2_classified_certificate",
    )

    q1_norm_val = result["q1_norm"]
    payload = {
        "certificate_id": certificate_id,
        "carrier_hash": carrier_hash,
        "terminal_status": result["terminal_status"],
        "q1_norm": str(q1_norm_val) if q1_norm_val is not None else "null",
        "certificate_alpha": result["certificate_alpha"],
        "normal_form": result["normal_form"],
        "coherence_witness": result["coherence_witness"],
        "reason": result.get("reason"),
        "budget": effective_budget,
        **{key: result.get(key) for key in CLASSIFIED_FIELDS},
    }
    replay_hash = stable_hash(payload, domain="majorana_gf2_classified_replay")

    return {
        **carrier,
        "instance": instance,
        "budget": effective_budget,
        "certificate_id": certificate_id,
        "carrier_hash": carrier_hash,
        "terminal_status": result["terminal_status"],
        "interpretation": INTERPRETATIONS.get(result["terminal_status"], ""),
        "reason": result.get("reason"),
        "certificate_alpha": result["certificate_alpha"],
        "normal_form": result["normal_form"],
        "coherence_witness": result["coherence_witness"],
        "q1_norm": str(q1_norm_val) if q1_norm_val is not None else "null",
        "algebraic_class_id": result["algebraic_class_id"],
        **{key: result.get(key) for key in CLASSIFIED_FIELDS},
        "replay_hash": replay_hash,
    }


def write_classified_ledger(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as output:
        for row in rows:
            output.write(json.dumps(row, allow_nan=False, sort_keys=True) + "\n")


def verify_classified_ledger(path: Path) -> dict[str, Any]:
    """Recompute every classified row from its declared carrier and budget."""
    checked = 0
    failures: list[dict[str, Any]] = []

    non_replayed = {"D0", "D1", "residual", "budget", "instance"}

    with path.open("r", encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            checked += 1
            expected = classified_ledger_row(
                row["D0"],
                row["D1"],
                row["residual"],
                budget=row.get("budget"),
                instance=row.get("instance"),
            )
            for key in sorted(set(expected) - non_replayed):
                if row.get(key) != expected.get(key):
                    failures.append({
                        "line": line_number,
                        "field": key,
                        "expected": expected.get(key),
                        "actual": row.get(key),
                    })
            for key in sorted(set(row) - set(expected) - non_replayed):
                failures.append({
                    "line": line_number,
                    "field": key,
                    "expected": "<field not produced by the classifier>",
                    "actual": row.get(key),
                })

    return {
        "checked": checked,
        "verified": not failures,
        "failures": failures,
    }


def verify_ledger(path: Path) -> dict[str, Any]:
    checked = 0
    failures: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            checked += 1
            expected = ledger_row(row["D0"], row["D1"], row["residual"])

            comparable_keys = (
                "certificate_id",
                "carrier_hash",
                "terminal_status",
                "interpretation",
                "certificate_alpha",
                "normal_form",
                "coherence_witness",
                "q1_norm",
                "replay_hash",
            )
            for key in comparable_keys:
                if row.get(key) != expected.get(key):
                    failures.append({
                        "line": line_number,
                        "field": key,
                        "expected": expected.get(key),
                        "actual": row.get(key),
                    })

    return {
        "checked": checked,
        "verified": not failures,
        "failures": failures,
    }




