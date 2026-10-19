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
LINK_LOC_SYM_RE = re.compile(r"\[([^\]]+)\]\(([^)#]+)#L(\d+)-L(\d+)\)\s*\(`([^`]+)`")
RUST_ATLAS_ROW_RE = re.compile(
    r'\("(Q\d{2})",\s*"[^"]+",\s*"[^"]+",\s*"[^"]+",\s*'
    r'"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"'
)


def _resolve_target_path(repo_root: Path, atlas_doc: Path, rel_path: str) -> Path:
    if rel_path.startswith("file:///"):
        return Path(rel_path.replace("file:///", ""))
    candidate = (atlas_doc.parent / rel_path).resolve()
    if candidate.exists():
        return candidate
    return (repo_root / rel_path).resolve()


def verify_qm_atlas_loc(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Verify all 65 QM question bindings, file line ranges, in-window symbols, and claim hygiene."""
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
        target_path = _resolve_target_path(repo_root, atlas_doc, rel_path)
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

    # 3. Verify that every [label](path#Lstart-Lend) (`symbol`) contains `symbol` inside lines start..end
    window_symbol_errors: list[str] = []
    verified_window_symbols = 0
    for label, rel_path, start_str, end_str, sym in LINK_LOC_SYM_RE.findall(doc_text):
        if sym.startswith("--"):
            continue
        start_line = int(start_str)
        end_line = int(end_str)
        target_path = _resolve_target_path(repo_root, atlas_doc, rel_path)
        if not target_path.exists():
            continue
        flines = target_path.read_text(encoding="utf-8").splitlines()
        window_text = "\n".join(flines[max(0, start_line - 1) : min(len(flines), end_line)])
        if sym not in window_text:
            window_symbol_errors.append(
                f"{label} ({rel_path}#L{start_line}-L{end_line}): symbol '{sym}' not found in line window"
            )
        else:
            verified_window_symbols += 1

    # 4. Verify all 65 entries in build_qm_question_atlas() and Rust/Python parity
    atlas_report = run_textbook_atlas()
    questions = build_qm_question_atlas()
    symbol_errors: list[str] = []
    py_bindings: dict[str, tuple[str, str, str, str, str, str]] = {}
    for entry in questions:
        qid = entry["id"]
        py_bindings[qid] = (
            entry["lean_file"],
            entry["lean_symbol"],
            entry["rust_file"],
            entry["rust_symbol"],
            entry["python_file"],
            entry["python_symbol"],
        )
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

    rust_atlas_file = repo_root / "code" / "rust" / "src" / "qm" / "textbook_problems.rs"
    rust_text = rust_atlas_file.read_text(encoding="utf-8") if rust_atlas_file.exists() else ""
    rust_bindings: dict[str, tuple[str, str, str, str, str, str]] = {
        m[0]: (m[1], m[2], m[3], m[4], m[5], m[6]) for m in RUST_ATLAS_ROW_RE.findall(rust_text)
    }
    rust_python_parity = py_bindings == rust_bindings and len(rust_bindings) == 65

    # 5. Verify Claim Hygiene forbidden words in docs/QM_PROBLEM_AND_PROOF_ATLAS.md
    lower_doc = doc_text.lower()
    forbidden_hits: list[str] = []
    for phrase in FORBIDDEN_CLAIM_WORDS:
        pattern = r"\b" + re.escape(phrase.lower()) + r"\b"
        if re.search(pattern, lower_doc):
            forbidden_hits.append(phrase)

    all_passed = (
        len(missing_q_ids) == 0
        and len(loc_errors) == 0
        and len(window_symbol_errors) == 0
        and len(symbol_errors) == 0
        and len(forbidden_hits) == 0
        and rust_python_parity
        and atlas_report["total_questions"] == 65
        and bool(atlas_report["all_textbook_problems_verified"])
        and bool(atlas_report["all_65_verified"])
        and verified_links >= 180
        and verified_window_symbols >= 190
    )

    return {
        "authority_effect": "None",
        "all_passed": all_passed,
        "total_questions": atlas_report["total_questions"],
        "verified_links": verified_links,
        "verified_window_symbols": verified_window_symbols,
        "rust_python_parity": rust_python_parity,
        "missing_q_ids": missing_q_ids,
        "loc_errors": loc_errors,
        "window_symbol_errors": window_symbol_errors,
        "symbol_errors": symbol_errors,
        "forbidden_hits": forbidden_hits,
    }


def main() -> int:
    report = verify_qm_atlas_loc()
    print(
        f"QM_ATLAS_LOC_VERIFIER all_passed={report['all_passed']} "
        f"questions={report['total_questions']} verified_links={report['verified_links']} "
        f"verified_window_symbols={report['verified_window_symbols']} "
        f"rust_python_parity={report['rust_python_parity']}"
    )
    if not report["all_passed"]:
        for key in (
            "missing_q_ids",
            "loc_errors",
            "window_symbol_errors",
            "symbol_errors",
            "forbidden_hits",
        ):
            if report[key]:
                print(f"  {key}: {report[key]}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
