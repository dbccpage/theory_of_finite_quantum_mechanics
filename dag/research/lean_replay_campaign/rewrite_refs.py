"""Rewrite DAG references to sibling-atlas Lean files so that they name the in-repo copy.

AuthorityEffect: None. Reads lean4/Imported/import_manifest.json and rewrites path strings in
dag/derivation_dag.json and in the sync fragments (dag/fragments/*.json) that own nodes and records.
No node status, statement or route is touched; only the path text of a reference changes. Strings under
`f004_refs`, `coda_atlas_paths` and `coda_atlas_ids` record the F004 atlas provenance of a record and are
left as they were.

    python -I -X utf8 dag/research/lean_replay_campaign/rewrite_refs.py          # dry run, prints counts
    python -I -X utf8 dag/research/lean_replay_campaign/rewrite_refs.py --write  # apply
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "lean4/Imported/import_manifest.json"
SKIP_KEYS = {"f004_refs", "coda_atlas_paths", "coda_atlas_ids"}
TARGETS = ["dag/derivation_dag.json"] + sorted(
    p.relative_to(ROOT).as_posix() for p in (ROOT / "dag/fragments").glob("*.json"))


def header_lines(repo_path: str) -> int:
    """Lines the provenance header adds above the original text of an imported file (0 for a repointed in-repo file)."""
    if not repo_path.startswith("lean4/Imported/"):
        return 0
    for i, line in enumerate((ROOT / repo_path).read_text(encoding="utf-8").split("\n")[:30]):
        if "AuthorityEffect: None. -/" in line:
            return i + 1
    raise SystemExit(f"no provenance header in {repo_path}")


def mapping() -> dict[str, str]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out = {f["original_path"]: f["repo_path"] for f in manifest["files"]
           if not f.get("excluded")}
    out.update(manifest["repointed_instead_of_imported"])
    return out


def shift_lines(spec: str, n: int) -> str:
    """'35-38' -> '44-47'; a single number shifts too."""
    return "-".join(str(int(x) + n) for x in spec.split("-"))


OFFSETS: dict[str, int] = {}
KEPT = "absent notes naming a moved path, left unchanged"


def rewrite(obj, pattern, table, counter, ctx=""):
    if isinstance(obj, dict):
        out = {k: (v if k in SKIP_KEYS else rewrite(v, pattern, table, counter, k)) for k, v in obj.items()}
        # a structured citation {"root": "symbol_game", "path": ...} whose path now names an in-repo file
        # becomes a "local" citation (the sync fragments resolve `local` against this checkout)
        if out.get("root") == "symbol_game" and isinstance(out.get("path"), str)                 and out["path"] in set(table.values()):
            out["root"] = "local"
            counter["root->local"] += 1
            n = OFFSETS.get(out["path"], 0)
            if n and isinstance(out.get("lines"), str):
                out["lines"] = shift_lines(out["lines"], n)
                counter["lines shifted"] += 1
        return out
    if isinstance(obj, list):
        return [rewrite(v, pattern, table, counter, ctx) for v in obj]
    if isinstance(obj, str):
        # "absent: no local lean twin located for <atlas path>" records that the file was NOT found; pointing
        # that sentence at the in-repo copy would make it contradict itself, so the whole note stays as written.
        if ctx == "absent" or obj.lstrip().lower().startswith("absent"):
            if pattern.search(obj):
                counter[KEPT] += 1
            return obj

        def sub(m):
            counter[ctx] += 1
            new = table[m.group("p")]
            if m.group("a"):
                n = OFFSETS.get(new, 0)
                a = int(m.group("a")) + n
                b = f"-{int(m.group('b')) + n}" if m.group("b") else ""
                counter["lines shifted"] += 1
                return f"{new}:{a}{b}"
            return new
        return pattern.sub(sub, obj)
    return obj


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    table = mapping()
    for repo_path in set(table.values()):
        OFFSETS[repo_path] = header_lines(repo_path)
    pattern = re.compile(r"(?<![\w/.\-])(?P<p>" + "|".join(re.escape(p) for p in sorted(table, key=len, reverse=True))
                         + r")(?::(?P<a>\d+)(?:-(?P<b>\d+))?)?(?![\w/])")
    total = 0
    for rel in TARGETS:
        path = ROOT / rel
        data = json.loads(path.read_bytes())
        counter: collections.Counter = collections.Counter()
        new = rewrite(data, pattern, table, counter)
        n = sum(v for k, v in counter.items() if k != KEPT)
        total += n
        print(f"{rel}: {n} path(s) rewritten {dict(counter)}")
        if args.write and n:
            path.write_bytes((json.dumps(new, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print("total", total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
