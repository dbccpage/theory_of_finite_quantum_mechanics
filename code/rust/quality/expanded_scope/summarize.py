"""Bind coverage to authored reviews; companion existence is not a passing grade."""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "evidence/quality/expanded_scope"


def pin(path):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", default="evidence/quality/expanded_scope/inventory-current.json")
    parser.add_argument("--output", default="evidence/quality/expanded_scope/coverage.json")
    args = parser.parse_args()
    inventory_path = ROOT / args.inventory
    inventory = json.loads(inventory_path.read_text())
    partial = json.loads((BASE / "review-progress.json").read_text())
    complete = json.loads((BASE / "simplex-assessment.json").read_text())
    assessed = {complete["source"]["path"]: complete}
    if (BASE / "batch2-assessments.json").is_file():
        assessed.update(json.loads((BASE / "batch2-assessments.json").read_text())["files"])
    if (BASE / "batch3-assessments.json").is_file():
        assessed.update(json.loads((BASE / "batch3-assessments.json").read_text())["files"])
    if (BASE / "batch4-assessments.json").is_file():
        assessed.update(json.loads((BASE / "batch4-assessments.json").read_text())["files"])
    below_target = {}
    if (BASE / "batch5-assessments.json").is_file():
        fifth = json.loads((BASE / "batch5-assessments.json").read_text())
        assessed.update(fifth["files"])
        below_target.update(fifth["below_target_assets"])
    batch_partial = {}
    if (BASE / "batch6-assessments.json").is_file():
        sixth = json.loads((BASE / "batch6-assessments.json").read_text())
        assessed.update(sixth["files"])
        batch_partial = {item["source"]["path"]: item for item in sixth["ancillary_partial_reviews"]}
    summaries = {}
    for name, row in inventory["subjects"].items():
        current_pin = pin(ROOT / name)
        assert current_pin["sha256"] == row["sha256"], "Regenerate inventory: " + name
        result = {"artifact": current_pin, "companion": row["companion"],
                  "review_status": "NOT_REVIEWED", "score_token": None, "target_achieved": False}
        if name in partial["files"]:
            result.update({"review_status": "PARTIAL", "basis": partial["files"][name]})
        if name in batch_partial:
            assessment = batch_partial[name]
            assert assessment["source"] == current_pin
            companion = ROOT / row["companion"]
            doc = json.loads(companion.read_text())
            score = next(record["record"] for record in doc["scoring_history"] if record["sha256"] == doc["current_scoring"])
            assert score["artifact"] == current_pin and not score["is_complete"] and score["score_token"] is None
            result.update({"review_status": "PARTIAL", "companion_pin": pin(companion), "basis": "Explicitly partial companion review; no full source grade."})
        if name in below_target:
            assessment = below_target[name]
            assert assessment["source"] == current_pin
            companion = ROOT / row["companion"]
            doc = json.loads(companion.read_text())
            score = next(record["record"] for record in doc["scoring_history"] if record["sha256"] == doc["current_scoring"])
            assert score["artifact"] == current_pin and score["is_complete"] and not score["target_achieved"]
            assert score["score_token"] == assessment["score_token"]
            result.update({"review_status": "COMPLETE_BELOW_TARGET", "score_token": score["score_token"], "companion_pin": pin(companion)})
        if name in assessed:
            assessment = assessed[name]
            assert assessment["source"] == current_pin
            companion = ROOT / row["companion"]
            doc = json.loads(companion.read_text())
            score = next(record["record"] for record in doc["scoring_history"] if record["sha256"] == doc["current_scoring"])
            assert score["artifact"] == current_pin and score["is_complete"] and score["score_token"] == assessment["score_token"]
            assert score["level"] in ("L4", "L5") and score["composite_grade"] in ("E", "D", "C", "B", "A", "A+")
            result.update({"review_status": "COMPLETE_SOURCE_REVIEW", "score_token": score["score_token"], "target_achieved": True,
                           "companion_pin": pin(companion)})
            result.pop("basis", None)  # Historical partial data stays in history, not the current score view.
        summaries[name] = result
    counts = Counter(row["review_status"] for row in summaries.values())
    result = {"AuthorityEffect": "None", "minimum_target": "L4E or higher",
        "target_confirmation": "User explicitly confirmed: Get everything to L4E or higher.",
        "full_scope_target_achieved": False, "inventory": pin(inventory_path),
        "directories": len(inventory["requested_directories"]), "subjects": len(summaries),
        "review_counts": dict(counts), "complete_at_target": sum(row["target_achieved"] for row in summaries.values()),
        "missing_companions": inventory["missing_companions"], "name_collisions": inventory["companion_name_collisions"],
        "scope_caveat": "Only authored source-bound complete assessments count. Neither migrated legacy labels nor existing companions, syntax checks or a package test pass are automatically individual L4 certification.",
        "files": summaries}
    (ROOT / args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "files"}, indent=2))


if __name__ == "__main__":
    main()
