"""Read-only scanner that resolves `lean4/...::Decl` and `path.lean` references in `dag/`, `papers/`, and `problem_sets/`.

AuthorityEffect: None. Read-only inventory and resolution check against files on disk.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import posixpath
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DECL_RE = re.compile(
    r"^(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|partial|unsafe)\s+)*"
    r"(theorem|lemma|def|structure|inductive|class|abbrev|instance|axiom|opaque)\s+([^\s:({\[]+)"
)
REF_RE = re.compile(
    r"(?<![A-Za-z0-9_./:-])([A-Za-z0-9_./-]*lean4/[A-Za-z0-9_./-]+\.lean|[A-Za-z0-9_.]+/[A-Za-z0-9_./-]+\.lean)(?:::([A-Za-z0-9_.']+))?"
)
EXTERNAL_PREFIXES = ("omega_engine_atlas/", "omega_engine/", "omega_engine_education/")
RECOVERED_BUNDLE_PATHS = {"lean4/genx/lakefile.lean", "po023/lean4/lakefile.lean"}


def index_lean_files(root: Path) -> tuple[dict[str, str], dict[str, set[str]], dict[str, set[str]]]:
    lean_files: dict[str, str] = {}
    decl_to_files: dict[str, set[str]] = {}
    file_decls: dict[str, set[str]] = {}

    for p in sorted((root / "lean4").rglob("*.lean")):
        rel = p.relative_to(root).as_posix()
        lean_files[p.name] = rel
        decls: set[str] = set()
        stack: list[tuple[str, str]] = []
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            s = line.strip()
            m_ns = re.match(r"namespace\s+(\S+)", s)
            m_sec = re.match(r"section(?:\s+(\S+))?\s*$", s)
            m_end = re.match(r"end(?:\s+(\S+))?\s*$", s)
            if m_ns:
                ns_name = m_ns.group(1)
                stack.append(("ns", ns_name))
                decls.add(ns_name)
            elif m_sec:
                stack.append(("sec", m_sec.group(1) or ""))
            elif m_end and stack:
                stack.pop()
            m = DECL_RE.match(line)
            if m and line[:1] not in (" ", "\t", "-"):
                name = m.group(2)
                prefix = ".".join(n for k, n in stack if k == "ns")
                full = name[len("_root_."):] if name.startswith("_root_.") else (prefix + "." + name if prefix else name)
                for cand in {name, full, name.split(".")[-1]}:
                    decls.add(cand)
                    decl_to_files.setdefault(cand, set()).add(rel)
        file_decls[rel] = decls
    return lean_files, decl_to_files, file_decls


def load_custody_and_pins(root: Path) -> tuple[set[str], set[str]]:
    custody_doc = json.loads((root / "dag/pfp/filename_custody.json").read_text(encoding="utf-8"))
    custody_sealed = {row["path"] for row in custody_doc.get("prompts", [])} | {
        row["path"] for row in custody_doc.get("papers", [])
    }
    pinned_papers: set[str] = set()
    for p in sorted((root / "dag/operads").glob("*.yaml")):
        in_pins = False
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip() == "paper_source_pins:":
                in_pins = True
                continue
            if in_pins:
                item = re.match(r"^\s*- path: (dag/derivations/\S+\.md)\s*$", line)
                if item:
                    pinned_papers.add(item.group(1))
                elif not re.match(r"^\s+(sha256: \S+)?$", line):
                    in_pins = False
    return custody_sealed, pinned_papers


def classify_reference(
    root: Path,
    file_rel: str,
    path_str: str,
    decl: str | None,
    lean_files: dict[str, str],
    decl_to_files: dict[str, set[str]],
    file_decls: dict[str, set[str]],
) -> tuple[str, str | None]:
    file_path = root / file_rel
    if path_str.startswith("../"):
        cand = (file_path.parent / path_str).resolve()
        try:
            rel_cand = cand.relative_to(root.resolve()).as_posix()
        except ValueError:
            rel_cand = None
        if rel_cand and (root / rel_cand).is_file():
            if not decl or decl in file_decls.get(rel_cand, set()) or decl.split(".")[-1] in file_decls.get(rel_cand, set()):
                return "RESOLVED", None
    else:
        if (root / path_str).is_file():
            if not decl or decl in file_decls.get(path_str, set()) or decl.split(".")[-1] in file_decls.get(path_str, set()):
                return "RESOLVED", None

    clean_path = re.sub(r"^(?:\.\./)+", "", path_str)
    if clean_path.startswith(EXTERNAL_PREFIXES):
        return "UNRESOLVED_EXTERNAL_REPO", None
    if clean_path in RECOVERED_BUNDLE_PATHS:
        return "UNRESOLVED_RECOVERED_BUNDLE", None

    basename = Path(clean_path).name
    flat_cand = lean_files.get(basename)
    if not decl:
        if flat_cand:
            target = posixpath.relpath(flat_cand, posixpath.dirname(file_rel)) if path_str.startswith("../") else flat_cand
            return "REMAPPABLE_PATH_MOVED", target
        return "UNRESOLVED_MISSING_FILE", None

    if flat_cand and (decl in file_decls.get(flat_cand, set()) or decl.split(".")[-1] in file_decls.get(flat_cand, set())):
        target_path = posixpath.relpath(flat_cand, posixpath.dirname(file_rel)) if path_str.startswith("../") else flat_cand
        return "REMAPPABLE_FILE_MOVED_SAME_DECL", f"{target_path}::{decl}"

    cands = decl_to_files.get(decl, set()) or decl_to_files.get(decl.split(".")[-1], set())
    if len(cands) == 1:
        new_file = next(iter(cands))
        target_path = posixpath.relpath(new_file, posixpath.dirname(file_rel)) if path_str.startswith("../") else new_file
        return "REMAPPABLE_DECL_MOVED_UNIQUE", f"{target_path}::{decl}"
    if len(cands) > 1:
        return "UNRESOLVED_AMBIGUOUS_DECL", ",".join(sorted(cands))
    if (root / clean_path).is_file():
        return "UNRESOLVED_MISSING_DECL_IN_EXISTING_FILE", None
    return "UNRESOLVED_MISSING_FILE_AND_DECL", None


def scan(root: Path = ROOT) -> dict[str, Any]:
    lean_files, decl_to_files, file_decls = index_lean_files(root)
    custody_sealed, pinned_papers = load_custody_and_pins(root)

    summary = Counter()
    editable_broken: list[dict[str, Any]] = []
    pinned_broken_counts = Counter()

    for folder in ("dag", "papers", "problem_sets"):
        base = root / folder
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.suffix not in (".md", ".yaml", ".yml"):
                continue
            rel = p.relative_to(root).as_posix()
            if rel.startswith("dag/results/"):
                continue
            is_pinned = (
                rel in custody_sealed
                or rel in pinned_papers
                or rel.startswith(("dag/operads/", "dag/prompts/"))
            )
            text = p.read_text(encoding="utf-8", errors="replace")
            for m in REF_RE.finditer(text):
                path_str, decl = m.group(1), m.group(2)
                status, target = classify_reference(
                    root, rel, path_str, decl, lean_files, decl_to_files, file_decls
                )
                scope = "pinned_or_custody" if is_pinned else "editable"
                summary[f"{scope}:{status}"] += 1
                if status != "RESOLVED":
                    if is_pinned:
                        pinned_broken_counts[status] += 1
                    else:
                        editable_broken.append(
                            {
                                "file": rel,
                                "reference": m.group(0),
                                "status": status,
                                "target": target,
                            }
                        )
    return {
        "indexed_lean_files": len(file_decls),
        "indexed_declarations": len(decl_to_files),
        "summary": dict(sorted(summary.items())),
        "editable_remappable_remaining": sum(
            1 for r in editable_broken if r["status"].startswith("REMAPPABLE_")
        ),
        "editable_unresolved_remaining": sum(
            1 for r in editable_broken if not r["status"].startswith("REMAPPABLE_")
        ),
        "pinned_or_custody_broken_by_status": dict(sorted(pinned_broken_counts.items())),
        "editable_broken": editable_broken,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--details", action="store_true", help="include full editable_broken list")
    args = parser.parse_args()
    result = scan(args.root)
    if not args.details:
        result = {k: v for k, v in result.items() if k != "editable_broken"}
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
