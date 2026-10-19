"""Source-bound companions for the six-module goal. Requires PyYAML.

An inventory or a passing package test never supplies a missing gate grade.
Existing reviewed assessments are referenced, not upgraded to L4 by title.
"""
import argparse
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
MODULES = ("combinatorics", "category_theory", "finite_probability",
           "fusion_categories", "general_relativity", "higher_category_theory")
HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}


def encoded(value):
    # JSON is a YAML 1.2 document; this keeps nulls and primitive types literal.
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def checked_reference(item):
    path = (ROOT / item["path"]).resolve()
    # Completed historical reviews can pin actual absolute provider/cache files.
    # These references are read and hashed; companion writes stay under ROOT.
    if not path.is_file() or digest(path) != item["sha256"]:
        raise ValueError("Stale or unavailable assessment reference: " + item["path"])


def prior_review(source):
    legacy = source.with_suffix(".score.yaml")
    if not legacy.exists():
        legacy = Path(str(source) + ".score.yaml")
    if not legacy.exists():
        return None, None
    record = yaml.safe_load(legacy.read_text(encoding="utf-8"))
    recorded = record.get("artifact", {}).get("sha256", record.get("source_sha256"))
    if recorded != digest(source):
        raise ValueError("Stale legacy score: " + str(legacy))
    if not record.get("is_complete"):
        return (legacy, record), None
    if (record.get("gates") != {f"G{i}": "A" for i in range(1, 6)}
            or record.get("score_token") != record.get("level", "") + "A"):
        raise ValueError("Unsupported completed legacy grades")
    primary = next(ROOT / item["path"] for item in record["evidence"]
                   if item["path"].endswith("/baseline.json")).parent.name
    metric = next(ROOT / item["path"] for item in record["evidence"]
                  if item["path"].endswith("-metrics/receipt.json")).parent
    batches = list(metric.glob("score_manifest-" + primary + "*.json"))
    relative = legacy.relative_to(ROOT).as_posix()
    recorded_score = digest(legacy)
    if not any(json.loads(batch.read_text(encoding="utf-8")).get(relative) == recorded_score for batch in batches):
        raise ValueError("Completed legacy record is absent from its immutable score manifests")
    assessment = None
    for item in record.get("evidence", []):
        if isinstance(item, dict) and item.get("scope", "").startswith("Explicit source-pinned gate assessment"):
            checked_reference(item)
            assessment = json.loads((ROOT / item["path"]).read_text(encoding="utf-8"))
            for reference in assessment.get("context_inputs", []) + assessment["evidence"] + assessment.get("proof_receipts", []):
                checked_reference(reference)
    if record.get("is_complete") and assessment is None:
        raise ValueError("Completed legacy score lacks its explicit review")
    return (legacy, record), assessment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    overrides_path = HERE / "contract_reviews.json"
    overrides = json.loads(overrides_path.read_text(encoding="utf-8")) if overrides_path.exists() else {}
    measurement_path = HERE / "structural_measurements.json"
    measurements = json.loads(measurement_path.read_text(encoding="utf-8")) if measurement_path.exists() else {}
    rows, failures = [], []
    for module in MODULES:
        for source in sorted((ROOT / "code/rust/src" / module).rglob("*.rs")):
            relative = source.relative_to(ROOT).as_posix()
            artifact = {**pin(source), "language": "Rust"}
            old, assessment = prior_review(source)
            override = overrides.get(relative)
            if override:
                if override["source_sha256"] != artifact["sha256"]:
                    raise ValueError("Stale contract review: " + relative)
                for reference in override.get("evidence", []):
                    checked_reference(reference)
            completed = bool(old and old[1].get("is_complete"))
            contract_path = Path(str(source) + ".contract.yaml")
            scoring_path = Path(str(source) + ".scoring.yaml")
            contract = {
                "schema_version": "1.0.0", "AuthorityEffect": "None", "artifact": artifact,
                "status": "source_reviewed" if assessment else "review_incomplete",
                "formal_specification": assessment["formal_specification"] if assessment else None,
                "operations": {name: ({k: v for k, v in item.items() if k != "body"}
                                      if isinstance(item, dict) else {"obligation": item})
                               for name, item in assessment["symbol_map"].items()} if assessment else {},
                "invariants": assessment["invariant_argument"] if assessment else [],
                "failure_paths": assessment["failure_paths"] if assessment else {},
                "trust_boundary": assessment["trust_boundary"] if assessment else None,
                "assurance_limits": assessment["assurance_limits"] if assessment else [
                    "This source has not received a complete symbol-level contract and five-gate review.",
                    "No production safety, semantic theorem or completed score is inferred from this file's existence."],
                "review_evidence": [pin(old[0])] if assessment else [],
                "open_obligations": [] if assessment else [
                    "Specify actual domains, results, error priority, invariants and operational bounds for every entry point.",
                    "Review callers and providers; obtain independent semantic, negative, mutation and complexity evidence."]}
            if override:
                contract.update(override["contract"])
                contract["review_evidence"].extend(override.get("evidence", []))
            if contract_path.exists() and not args.check:
                current = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
                # Preserve independently authored contracts, including earlier PFP companions.
                if current.get("schema_id"):
                    if current.get("source_sha256") != artifact["sha256"]:
                        raise ValueError("Stale existing contract: " + str(contract_path))
                    contract = current
            elif contract_path.exists() and args.check:
                current = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
                if current.get("schema_id"):
                    if current.get("source_sha256") != artifact["sha256"]:
                        raise ValueError("Stale existing contract: " + str(contract_path))
                    contract = current
            if not contract.get("schema_id"):
                if args.check:
                    if not contract_path.exists() or contract_path.read_text(encoding="utf-8") != encoded(contract):
                        failures.append(str(contract_path))
                else:
                    contract_path.write_text(encoded(contract), encoding="utf-8", newline="\n")
            if not contract_path.exists():
                failures.append(str(contract_path))
                continue
            level = old[1].get("level", old[1].get("capability_level")) if old else None
            if override and "level" in override:
                level = override["level"]
            gates = old[1].get("gates") if completed else {f"G{i}": None for i in range(1, 6)}
            scoring = {
                "schema_version": "2.0.0", "AuthorityEffect": "None", "artifact": artifact,
                "rubric": pin(ROOT / "SCORING.md"), "architecture_target": "L4", "engineering_target": "A",
                "level": level, "gates": gates,
                "composite_grade": old[1]["composite_grade"] if completed else None,
                "score_token": old[1]["score_token"] if completed else None,
                "is_complete": completed,
                "assessment_status": "existing_source_review_referenced" if completed else "incomplete",
                "assessment_source": pin(old[0]) if old else None, "contract": pin(contract_path),
                "assessment_note": "Capability describes delivered code. Existing L1/L2/L3/L5 levels are preserved; neither a sidecar nor the L4 architecture target upgrades them.",
                "open_obligations": [] if completed else ["Complete each missing sovereign gate; no completed token until all five have adequate evidence."]}
            if override and not completed:
                scoring["known_findings"] = override.get("known_findings", [])
                scoring["partial_evidence"] = override.get("evidence", [])
            if relative in measurements:
                measurement = measurements[relative]
                if measurement["source_sha256"] != artifact["sha256"]:
                    raise ValueError("Stale structural measurement: " + relative)
                for reference in measurement["evidence"]:
                    checked_reference(reference)
                scoring["structural_measurement"] = measurement
            if args.check:
                if not scoring_path.exists() or scoring_path.read_text(encoding="utf-8") != encoded(scoring):
                    failures.append(str(scoring_path))
            else:
                scoring_path.write_text(encoded(scoring), encoding="utf-8", newline="\n")
            rows.append({"source": relative, "source_sha256": artifact["sha256"],
                         "scoring": pin(scoring_path) if scoring_path.exists() else None,
                         "contract": pin(contract_path), "score_token": scoring["score_token"],
                         "is_complete": completed, "contract_status": contract.get("status", "existing_scoped_contract")})
    summary = {"AuthorityEffect": "None", "goal_complete": False, "modules": list(MODULES),
               "total_files": len(rows), "completed_assessments": sum(row["is_complete"] for row in rows),
               "incomplete_assessments": sum(not row["is_complete"] for row in rows), "files": rows}
    ledger = HERE / "progress.json"
    if args.check:
        if not ledger.exists() or ledger.read_text(encoding="utf-8") != encoded(summary):
            failures.append(str(ledger))
    else:
        ledger.write_text(encoded(summary), encoding="utf-8", newline="\n")
    if failures:
        raise SystemExit("Stale companions:\n" + "\n".join(failures))
    print(("Verified" if args.check else "Wrote"), len(rows), "source-bound companion pairs;",
          summary["completed_assessments"], "existing completed assessments;",
          summary["incomplete_assessments"], "incomplete; goal remains open.")


if __name__ == "__main__":
    main()
