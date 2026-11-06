"""Check the cleaned campaign artifacts without rebuilding or changing them."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MARKDOWN = sorted(HERE.glob("*.md")) + sorted((HERE / "team_summaries").glob("*.md"))
JSON_FILES = sorted(HERE.glob("*.json"))
HYPE_WORDS = (
    "pro" + "ves", "guar" + "antees", "funda" + "mentally",
    "uni" + "versal", "impo" + "ssible", "flaw" + "less", "perf" + "ectly",
)
HYPE = re.compile(r"\b(?:" + "|".join(HYPE_WORDS) + r")\b", re.I)
LINK = re.compile(r"\]\(([^)]+)\)")


def no_float(value, pointer: str) -> None:
    if isinstance(value, float):
        raise AssertionError(f"numeric float at {pointer}")
    if isinstance(value, list):
        for index, child in enumerate(value):
            no_float(child, f"{pointer}/{index}")
    if isinstance(value, dict):
        for key, child in value.items():
            no_float(child, f"{pointer}/{key}")


def main() -> None:
    parsed = {path.name: json.loads(path.read_text(encoding="utf-8-sig")) for path in JSON_FILES}
    all_rows = parsed["proposals_all_500.json"]
    assert len(all_rows) == len({r["proposal_id"] for r in all_rows}) == 500
    assert len(parsed["proposals_by_target_g1.json"]) == 250
    assert len(parsed["proposals_by_target_q.json"]) == 250
    assert Counter(r["classification"] for r in all_rows) == {
        "PROMISING": 41, "INCREMENTAL": 450, "BLOCKED": 9
    }
    assert sum(r["research_priority"] is not None for r in all_rows) == 50
    assert len({r["round2_follow_up"]["source"] for r in all_rows if r["round2_follow_up"]}) == 50
    assert sum(bool(r["round2_follow_up"]) for r in all_rows) == 100
    assert len({r["exact_payload_duplicate_group"] for r in all_rows}) == 160
    assert sum(r["exact_payload_duplicate_count"] > 1 for r in all_rows) == 430
    source_checks = (
        "round1_proposal_digest_matches_manifest",
        "round1_proposal_payload_matches_manifest",
        "round1_dual_witness_digest_matches_manifest",
        "round1_dual_vector_matches_manifest",
        "round1_defect_matches_manifest",
        "round1_prompt_matches_manifest",
        "round1_target_matches_manifest",
    )
    assert all(all(r["provenance"][check] for check in source_checks) for r in all_rows)
    for name, value in parsed.items():
        no_float(value, name)
        if HYPE.search(json.dumps(value, ensure_ascii=False)):
            raise AssertionError(f"hype term in {name}")
    for row in all_rows:
        source = ROOT / row["provenance"]["round1_session_source"]
        assert source.exists()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == row["provenance"]["round1_session_sha256"]
        if row["round2_follow_up"]:
            r2 = ROOT / row["round2_follow_up"]["source"]
            assert r2.exists()
            assert hashlib.sha256(r2.read_bytes()).hexdigest() == row["round2_follow_up"]["source_sha256"]
    link_count = 0
    for path in MARKDOWN:
        body = path.read_text(encoding="utf-8")
        if HYPE.search(body):
            raise AssertionError(f"hype term in {path}")
        for target in LINK.findall(body):
            if "://" in target or target.startswith("#"):
                continue
            local = (path.parent / target.split("#", 1)[0]).resolve()
            if not local.exists():
                raise AssertionError(f"broken link in {path}: {target}")
            link_count += 1
    report = (HERE / "swarm_campaign_report.md").read_text(encoding="utf-8")
    inventory = report.split("<!-- INVENTORY_START -->", 1)[1].split("<!-- INVENTORY_END -->", 1)[0]
    assert len(re.findall(r"^\| \[`PROP_", inventory, re.M)) == 500
    ranked = (HERE / "ranked_proposals.md").read_text(encoding="utf-8")
    assert len(re.findall(r"^\| \d+ \| \[`PROP_", ranked, re.M)) == 50
    graph = parsed["source_graph_audit.json"]
    assert graph["sessions"] == 300
    assert graph["by_round"]["1"]["nonzero_divergence"] == 0
    assert graph["by_round"]["1"]["cut_sections_checked"] == 250
    assert graph["by_round"]["1"]["cut_section_mismatches"] == 0
    assert graph["by_round"]["2"]["nonzero_divergence"] == 50
    assert graph["by_round"]["2"]["proposal_cut_trace_mismatches"] == 50
    print(json.dumps({
        "json_files": len(JSON_FILES),
        "markdown_files": len(MARKDOWN),
        "proposals": len(all_rows),
        "inventory_rows": 500,
        "ranked_rows": 50,
        "resolved_links": link_count,
        "source_hashes": "match",
        "manifest_session_fields": "match",
        "exact_payload_groups": 160,
        "numeric_floats": 0,
        "hype_terms": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
