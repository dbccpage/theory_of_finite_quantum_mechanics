"""Replay finite witnesses through existing owners; no private mathematical solver."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from omega_engine_operations.domain.rop.result import Ok
from omega_engine_education.pfp.infrastructure.yaml.nf.nf_harness import validate_contract_file
from omega_engine_education.pfp.infrastructure.yaml.nf.schema_pipeline import ROOT, audit_all_schemas
from omega_engine_projects.finite_to_continuum.code.native_bridge import evaluate_finite_bridge

DOSSIER = Path(__file__).resolve().parent


def main() -> None:
    results = []
    for filename, expected_success in (
        ("witness_valid.json", True),
        ("witness_near_miss.json", False),
    ):
        cases = json.loads((DOSSIER / filename).read_text(encoding="utf-8"))
        if not cases or len({c["id"] for c in cases}) != len(cases):
            raise ValueError("witness carrier is empty or has duplicate IDs")
        for case in cases:
            actual = evaluate_finite_bridge(case["request"])
            if not isinstance(actual, Ok):
                raise ValueError(f"{case['id']}: native transport or integrity refusal: {actual}")
            if actual.value["success"] is not expected_success or actual.value != case["outcome"]:
                raise ValueError(f"{case['id']}: witness did not replay exactly")
            if actual.value["authority_effect"] != "None":
                raise ValueError("unexpected authority effect")
            results.append({"id": case["id"], "native_success": expected_success, "replayed": True})
    inventory = audit_all_schemas()
    count = sum(len(s["tables"]) for s in inventory["schemas"])
    if count != 84 or any(
        not t["lossless_under_declared_fds"] for s in inventory["schemas"] for t in s["tables"]
    ):
        raise ValueError("schema inventory or projection evidence changed")
    contract = (
        ROOT
        / "omega_engine_education/documentation/150_normal_forms/contracts_normal_forms/nf.operational.schema-totality.yaml"
    )
    defects = validate_contract_file(contract)
    if defects:
        raise ValueError(f"SQL-TOTAL contract defects: {defects}")
    source_digests = {
        s["source"]: hashlib.sha256((ROOT / s["source"].split("::")[0]).read_bytes()).hexdigest()
        for s in inventory["schemas"]
    }
    output = {
        "schema_version": "omega.track2.checker-output.v1",
        "authority_effect": "None",
        "replays": results,
        "schema_sources": len(inventory["schemas"]),
        "table_declarations": count,
        "schema_source_sha256": source_digests,
        "sql_totality_contract_defects": [],
        "formal_build_executed_by_this_checker": False,
        "formal_check": "run lake --no-cache build in finite_to_continuum/lean4 separately",
    }
    (DOSSIER / "checker_output.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"PASS: {len(results)} native replays; {count} table declarations; SQL-TOTAL contract valid"
    )


if __name__ == "__main__":
    main()
