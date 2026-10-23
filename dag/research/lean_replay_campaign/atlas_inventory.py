"""Inventory every reference from this repository into the sibling `the_symbol_game` tree.

AuthorityEffect: None. Read-only on the sibling tree. Scans the text files of this checkout for path
strings that start with a top-level folder of the sibling tree (omega_engine*, omega_simplex*, `.claude/`
inside it) or that name `the_symbol_game`, resolves each distinct path there, and writes
docs/maintenance/atlas_dependency_inventory.json and .md.

    python -I -X utf8 atlas_inventory.py --repo R --atlas C:\\...\\the_symbol_game --out-dir R/docs/maintenance
"""
from __future__ import annotations

import argparse
import collections
import datetime
import json
import os
import re
from pathlib import Path

TEXT_EXT = {".py", ".rs", ".toml", ".md", ".json", ".jsonl", ".yaml", ".yml", ".ps1", ".sh", ".lean", ".txt",
            ".tex", ".cfg", ".ini", ".csv", ".html", ".bib", ".rst", ".ebnf", ".lock"}
SKIP_DIRS = {".git", "__pycache__", "target", ".lake", "node_modules", ".pytest_cache", ".mypy_cache"}
# provenance headers and the campaign's own tools name the atlas on purpose
SKIP_PREFIX = ("lean4/b/", "lean4/.lake/", "lean4/Imported/", "docs/maintenance/atlas_dependency_inventory",
               "dag/research/lean_replay_campaign/")
PATH_SIMPLE = re.compile(
    r"(?<![\w/.\\-])(?:the_symbol_game[/\\]+)?((?:omega_engine[a-z_]*|omega_simplex[a-z_]*)(?:[/\\][A-Za-z0-9_.@+~-]+)+)")
# Only a `.claude/` path written as a path INTO the sibling tree counts. A bare `.claude/...` in this repository
# (skills, agents, worktrees) is this repository's own and is not an atlas dependency.
DOT_CLAUDE = re.compile(r"(?<![\w.\\-])the_symbol_game[/\\]+(\.claude/[A-Za-z0-9_./@+-]+\.(?:md|json|yaml|yml|txt))")
ABS = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\s\"'`]*the_symbol_game[\\/]+([A-Za-z0-9_./\\@+-]*)")
PY_IMPORT = re.compile(r"^\s*(?:from|import)\s+(omega_engine[a-z_]*|omega_simplex[a-z_]*)(?:[.\s]|$)", re.M)
NEEDLES = (b"omega_engine", b"omega_simplex", b"the_symbol_game", b".claude/")

PROVENANCE_LOC = "dag provenance strings (history)"
PROVENANCE_KEYS = ("f004_refs", "coda_atlas_paths", "coda_atlas_ids")
LIVE = ("dag nodes/records/routes (derivation_dag.json)", "dag fragments (sync inputs)", "code/**", "papers/**",
        "scripts/**", "lean4/**", "docs/**", "problem_sets/**", "dag other (operads, research, pfp, tools)", "other")
GENERATED = ("dag generated views and derivation papers",)
SEALED = ("dag/results (sealed run artifacts)",)


def classify_location(rel: str) -> str:
    if rel == "dag/derivation_dag.json":
        return "dag nodes/records/routes (derivation_dag.json)"
    if rel.startswith("dag/fragments/"):
        return "dag fragments (sync inputs)"
    if rel.startswith("dag/derivations/") or rel.startswith("dag/theory_of_finite_qm"):
        return "dag generated views and derivation papers"
    if rel.startswith("dag/results/"):
        return "dag/results (sealed run artifacts)"
    if rel.startswith("dag/"):
        return "dag other (operads, research, pfp, tools)"
    for top in ("papers", "code", "scripts", "lean4", "docs", "problem_sets"):
        if rel.startswith(top + "/"):
            return top + "/**"
    return "other"


def split_provenance(text: str):
    """(text without the provenance keys, text of only those values) for a DAG-shaped JSON document."""
    import json
    try:
        data = json.loads(text)
    except ValueError:
        return text, ""
    kept: list = []

    def walk(o):
        if isinstance(o, dict):
            out = {}
            for k, v in o.items():
                if k in PROVENANCE_KEYS:
                    kept.append(v)
                else:
                    out[k] = walk(v)
            return out
        if isinstance(o, list):
            return [walk(x) for x in o]
        return o
    rest = walk(data)
    return json.dumps(rest, ensure_ascii=False), json.dumps(kept, ensure_ascii=False)


def kind_of(path: str) -> str:
    low = path.lower()
    ext = os.path.splitext(low)[1]
    if ext == ".lean":
        return "Lean"
    if ext == ".rs" or low.endswith("cargo.toml") or low.endswith("cargo.lock"):
        return "Rust"
    if ext == ".py":
        return "Python"
    if ext in (".yaml", ".yml"):
        return "yaml claim register" if re.search(r"claim|register|ledger|contract", low) else "yaml (other)"
    if ext in (".md", ".txt", ".tex", ".rst", ".bib", ".ebnf"):
        return "paper / document"
    if ext in (".json", ".jsonl", ".csv"):
        return "data (json/jsonl/csv)"
    if ext == "":
        return "directory or extensionless"
    return "other"


def clean(p: str) -> str:
    p = p.replace("\\", "/")
    p = re.sub(r"::.*$", "", p)
    p = re.sub(r"#.*$", "", p)
    p = re.sub(r":\d+(?:[-,]\d+)*$", "", p)
    p = re.sub(r"/{2,}", "/", p)
    return p.rstrip(".,;:)").rstrip("/")


def group_of(path: str) -> str:
    parts = path.split("/")
    if parts[0] == "omega_engine_atlas":
        if len(parts) >= 5 and parts[2] == "F004_papers":
            return "/".join(parts[:5]) if parts[3][:1].isdigit() and len(parts) > 5 else "/".join(parts[:4])
        return "/".join(parts[:3])
    if parts[0] == "omega_engine_education" and len(parts) >= 3:
        return "/".join(parts[:3])
    return parts[0]


def scan(repo: Path):
    refs: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    examples: dict[str, list] = collections.defaultdict(list)
    py_imports: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    abs_hits: collections.Counter = collections.Counter()
    scanned = mentioning = 0
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not (d == ".claude" and Path(dirpath) == repo)]
        for fn in filenames:
            full = Path(dirpath) / fn
            rel = full.relative_to(repo).as_posix()
            if any(rel.startswith(s) for s in SKIP_PREFIX):
                continue
            if full.suffix.lower() not in TEXT_EXT:
                continue
            try:
                raw = full.read_bytes()
            except OSError:
                continue
            scanned += 1
            if not any(n in raw for n in NEEDLES):
                continue
            mentioning += 1
            text = raw.decode("utf-8", errors="replace")
            loc = classify_location(rel)
            parts = [(text, loc)]
            if rel == "dag/derivation_dag.json" or (rel.startswith("dag/fragments/") and rel.endswith(".json")):
                rest, prov = split_provenance(text)
                parts = [(rest, loc), (prov, PROVENANCE_LOC)]
            for part, ploc in parts:
                found = {clean(m.group(1)) for m in PATH_SIMPLE.finditer(part)}
                found |= {clean(m.group(1)) for m in DOT_CLAUDE.finditer(part)}
                for m in ABS.finditer(part):
                    abs_hits[rel] += 1
                    tail = clean(m.group(1))
                    if tail:
                        found.add(tail)
                for p in found:
                    if not p:
                        continue
                    refs[p][ploc] += 1
                    if len(examples[p]) < 3 and rel not in examples[p]:
                        examples[p].append(rel)
            if full.suffix == ".py":
                for m in PY_IMPORT.finditer(text):
                    py_imports[m.group(1)][rel] += 1
    return refs, examples, py_imports, abs_hits, scanned, mentioning


REMOVAL_COMMIT = "3379759468"  # sibling commit "Remove seven F004 paper families from the atlas tree." (2026-10-22)


def removed_listing(atlas: Path):
    """path -> size of every file the sibling removal commit deleted, read from its parent commit."""
    import subprocess
    r = subprocess.run(["git", "-c", "core.quotepath=off", "-C", str(atlas), "diff-tree", "--no-commit-id", "-r", "--diff-filter=D", "--name-only",
                        REMOVAL_COMMIT], capture_output=True, encoding="utf-8")
    names = [n for n in r.stdout.splitlines() if n]
    if not names:
        return {}
    sizes = subprocess.run(["git", "-c", "core.quotepath=off", "-C", str(atlas), "ls-tree", "-r", "-l", REMOVAL_COMMIT + "^", "--",
                            "omega_engine_atlas/coda_atlas/F004_papers"], capture_output=True, encoding="utf-8")
    out = {}
    for line in sizes.stdout.splitlines():
        meta, _, name = line.partition("	")
        parts = meta.split()
        if len(parts) >= 4:
            out[name] = int(parts[3]) if parts[3].isdigit() else 0
    gone = set(names)
    return {k: v for k, v in out.items() if k in gone}


def resolve(atlas: Path, refs, examples):
    removed = removed_listing(atlas)
    removed_dirs = collections.Counter()
    for k in removed:
        parts = k.split("/")
        for i in range(1, len(parts)):
            removed_dirs["/".join(parts[:i])] += 1
    out = []
    for p in sorted(refs):
        full = atlas / p
        exists = full.exists()
        entry = {"path": p, "group": group_of(p), "exists_in_atlas": exists, "kind": kind_of(p),
                 "referenced_from": dict(sorted(refs[p].items())), "reference_count": sum(refs[p].values()),
                 "example_files": examples[p]}
        if not exists:
            if p in removed:
                entry.update(removed_in_commit=REMOVAL_COMMIT, size_bytes_before_removal=removed[p])
            elif p in removed_dirs:
                entry.update(removed_in_commit=REMOVAL_COMMIT, removed_dir=True, file_count_before_removal=removed_dirs[p])
        if exists:
            if full.is_dir():
                n = size = 0
                for dp, _dn, fns in os.walk(full):
                    n += len(fns)
                    for f in fns:
                        try:
                            size += (Path(dp) / f).stat().st_size
                        except OSError:
                            pass
                entry.update(is_dir=True, size_bytes=size, file_count=n)
            else:
                entry.update(is_dir=False, size_bytes=full.stat().st_size)
        out.append(entry)
    return out


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n / 1:.1f} {unit}"
        n /= 1024
    return str(n)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--atlas", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--json-only", action="store_true")
    a = ap.parse_args()
    repo, atlas, out_dir = Path(a.repo), Path(a.atlas), Path(a.out_dir)
    refs, examples, py_imports, abs_hits, scanned, mentioning = scan(repo)
    paths = resolve(atlas, refs, examples)
    doc = {"schema_version": "atlas_dependency_inventory.v1", "authority_effect": "None",
           "generated": datetime.date.today().isoformat(), "atlas_root": "the_symbol_game (sibling checkout)",
           "files_scanned": scanned, "files_mentioning_atlas": mentioning, "distinct_paths": len(paths),
           "python_imports_of_atlas_packages": {k: dict(v) for k, v in sorted(py_imports.items())},
           "absolute_path_mentions_files": dict(abs_hits), "paths": paths}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "atlas_dependency_inventory.json").write_text(
        json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    print(scanned, "files scanned;", mentioning, "mention the atlas;", len(paths), "distinct paths;",
          sum(1 for e in paths if e["exists_in_atlas"]), "exist in the atlas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
