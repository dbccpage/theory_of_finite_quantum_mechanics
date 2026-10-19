"""Automated verifier for docs/QM_PROBLEM_AND_PROOF_ATLAS.md and the 65-question QM atlas."""
from __future__ import annotations

from pathlib import Path
import re
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "code" / "python") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code" / "python"))

from src.qm.textbook_problems import build_qm_question_atlas, run_textbook_atlas  # noqa: E402

ATLAS_DOC = REPO_ROOT / "docs" / "QM_PROBLEM_AND_PROOF_ATLAS.md"

FORBIDDEN_CLAIM_WORDS: tuple[str, ...] = (
    "proves",
    "guarantees",
    "mathematically verifies",
    "fundamentally",
    "true intelligence",
    "impossible",
    "universal",
    "flawless",
    "perfectly",
    "clearly",
    "obviously",
    "simply",
    "merely",
    "weaponized",
)

LINK_LOC_RE = re.compile(r"\[([^\]]+)\]\(([^)#]+)#L(\d+)(?:-L(\d+))?\)")


def verify_qm_atlas_loc(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Verify all 65 QM question bindings, file line ranges, and claim hygiene in the QM Atlas."""
    atlas_doc = repo_root / "docs" / "QM_PROBLEM_AND_PROOF_ATLAS.md"
    if not atlas_doc.exists():
        raise FileNotFoundError(f"Missing atlas document: {atlas_doc}")

    doc_text = atlas_doc.read_text(encoding="utf-8")

    # 1. Verify all Q01..Q65 rows exist in the markdown document
    missing_q_ids: list[str] = []
    for idx in range(1, 66):
        qid = f"Q{idx:02d}"
        if f"**{qid}**" not in doc_text:
            missing_q_ids.append(qid)

    # 2. Verify all markdown links with #Lstart-Lend ranges
    loc_matches = LINK_LOC_RE.findall(doc_text)
    loc_errors: list[str] = []
    verified_links = 0
    for label, rel_path, start_str, end_str in loc_matches:
        start_line = int(start_str)
        end_line = int(end_str) if end_str else start_line
        if rel_path.startswith("file:///"):
            cleaned = rel_path.replace("file:///", "")
            target_path = Path(cleaned)
        else:
            target_path = (atlas_doc.parent / rel_path).resolve()
            if not target_path.exists():
                target_path = (repo_root / rel_path).resolve()

        if not target_path.exists():
            loc_errors.append(f"{label}: missing file {rel_path}")
            continue

        total_lines = len(target_path.read_text(encoding="utf-8").splitlines())
        if not (1 <= start_line <= end_line <= total_lines):
            loc_errors.append(
                f"{label} ({rel_path}): invalid line range #L{start_line}-L{end_line} (file has {total_lines} lines)"
            )
        else:
            verified_links += 1

    # 3. Verify all 65 entries in build_qm_question_atlas() and run_textbook_atlas()
    atlas_report = run_textbook_atlas()
    questions = build_qm_question_atlas()
    symbol_errors: list[str] = []
    for entry in questions:
        qid = entry["id"]
        for lang, f_key, s_key in (
            ("lean", "lean_file", "lean_symbol"),
            ("rust", "rust_file", "rust_symbol"),
            ("python", "python_file", "python_symbol"),
        ):
            fpath = repo_root / entry[f_key]
            sym = entry[s_key]
            if not fpath.exists():
                symbol_errors.append(f"{qid} ({lang}): missing file {entry[f_key]}")
                continue
            content = fpath.read_text(encoding="utf-8")
            if sym not in content:
                symbol_errors.append(f"{qid} ({lang}): symbol '{sym}' not found in {entry[f_key]}")

    # 4. Verify Claim Hygiene forbidden words in docs/QM_PROBLEM_AND_PROOF_ATLAS.md
    lower_doc = doc_text.lower()
    forbidden_hits: list[str] = []
    for phrase in FORBIDDEN_CLAIM_WORDS:
        pattern = r"\b" + re.escape(phrase.lower()) + r"\b"
        if re.search(pattern, lower_doc):
            forbidden_hits.append(phrase)

    all_passed = (
        len(missing_q_ids) == 0
        and len(loc_errors) == 0
        and len(symbol_errors) == 0
        and len(forbidden_hits) == 0
        and atlas_report["total_questions"] == 65
        and bool(atlas_report["all_textbook_problems_verified"])
        and bool(atlas_report["all_65_verified"])
        and verified_links >= 180
    )

    return {
        "authority_effect": "None",
        "all_passed": all_passed,
        "total_questions": atlas_report["total_questions"],
        "verified_links": verified_links,
        "missing_q_ids": missing_q_ids,
        "loc_errors": loc_errors,
        "symbol_errors": symbol_errors,
        "forbidden_hits": forbidden_hits,
    }


def main() -> int:
    report = verify_qm_atlas_loc()
    print(
        f"QM_ATLAS_LOC_VERIFIER all_passed={report['all_passed']} "
        f"questions={report['total_questions']} verified_links={report['verified_links']}"
    )
    if not report["all_passed"]:
        for key in ("missing_q_ids", "loc_errors", "symbol_errors", "forbidden_hits"):
            if report[key]:
                print(f"  {key}: {report[key]}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
