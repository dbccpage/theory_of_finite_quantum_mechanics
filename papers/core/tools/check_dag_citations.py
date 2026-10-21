#!/usr/bin/env python3
"""Check that every DAG-style id cited in papers/core/finite_quantum_mechanics.md
resolves to a node in dag/derivation_dag.json or a record in dag/theory_of_finite_qm.jsonl.

Id families checked: FQ-, DS-, L1-, GP-, IMPL-, PG-, PGW-, TFQ-.

Usage (from anywhere):
    python -I -X utf8 papers/core/tools/check_dag_citations.py [--paper PATH ...] [--list]

Exit status 0 when every cited id resolves, 1 otherwise. Machine-written rows in
the "DAG results audit" section are checked like any other text, so the
generator and the checker cannot drift apart silently.
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DAG = REPO / "dag" / "derivation_dag.json"
JSONL = REPO / "dag" / "theory_of_finite_qm.jsonl"
DEFAULT_PAPERS = [REPO / "papers" / "core" / "finite_quantum_mechanics.md"]

ID_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:FQ|DS|L1|GP|IMPL|PG|PGW|TFQ)-[A-Z0-9]+(?:-[A-Z0-9]+)*"
)


def known_ids():
    ids = {}
    dag = json.loads(DAG.read_text(encoding="utf-8"))
    for n in dag["nodes"]:
        ids[n["id"]] = "dag-node"
    with JSONL.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            ids.setdefault(rec["id"], "jsonl-record")
    return ids


def cited(path):
    out = {}
    for lineno, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        for m in ID_RE.finditer(line):
            out.setdefault(m.group(0), []).append(lineno)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--paper", action="append", type=Path)
    ap.add_argument("--list", action="store_true", help="print every resolved id too")
    args = ap.parse_args(argv)
    papers = args.paper or DEFAULT_PAPERS
    ids = known_ids()
    bad = 0
    for paper in papers:
        refs = cited(paper)
        missing = {k: v for k, v in refs.items() if k not in ids}
        print(f"{paper.name}: {len(refs)} distinct DAG-style ids cited, "
              f"{len(refs) - len(missing)} resolve, {len(missing)} do not")
        if args.list:
            for k in sorted(refs):
                print(f"  {'ok ' if k in ids else 'BAD'} {k} ({ids.get(k, 'unresolved')})")
        for k in sorted(missing):
            print(f"  UNRESOLVED {k}  (lines {', '.join(map(str, missing[k][:8]))})")
        bad += len(missing)
    print("FAIL" if bad else "OK")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
