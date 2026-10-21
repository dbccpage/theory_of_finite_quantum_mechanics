#!/usr/bin/env python3
"""Regenerate the DAG-derived blocks of papers/core from dag/derivation_dag.json.

Three generated blocks, each fenced by BEGIN/END comment markers that must
already exist in the target file:

  dag-census            papers/core/finite_quantum_mechanics.md  (section 13.8.8)
  dag-results-audit     papers/core/finite_quantum_mechanics.md  (DAG results audit)
  pfp-ledger            papers/core/finite_quantum_mechanics_claim_ledger.md (SRC-PFP)
  ledger-distribution   papers/core/finite_quantum_mechanics_claim_ledger.md (Distribution)

Source of the reviewed rows: the `pfp_review` object on each node of
dag/derivation_dag.json (written by dag/sync_pfp_results.py). This script only
reads the DAG; it never edits anything under dag/.

Usage (from anywhere):
    python -I -X utf8 papers/core/tools/build_results_audit_table.py            # print blocks
    python -I -X utf8 papers/core/tools/build_results_audit_table.py --write    # update files
    python -I -X utf8 papers/core/tools/build_results_audit_table.py --check    # exit 1 if stale
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DAG = REPO / "dag" / "derivation_dag.json"
PAPER = REPO / "papers" / "core" / "finite_quantum_mechanics.md"
LEDGER = REPO / "papers" / "core" / "finite_quantum_mechanics_claim_ledger.md"

NODE_STATUS_ORDER = [
    "ADMITTED_PRIMITIVE", "DEFINITION", "PROVED_PROSE", "PROVED_LEAN",
    "COMPUTATIONALLY_CHECKED", "CONDITIONAL", "IMPORTED_ASSUMPTION", "OPEN",
    "REFUTED", "SOURCE_RECORD",
]
ROUTE_STATUS_ORDER = [
    "DERIVED_PROSE", "DERIVED_LEAN", "COMPUTED", "CONDITIONAL_ON_IMPORT",
    "GAP_NO_DERIVATION", "RECORD_PARENT",
]
SCOPE_ORDER = ["consistent", "caveat_added", "statement_narrowed", "status_lowered"]

# DAG node status -> claim-ledger Type vocabulary.
LEDGER_TYPE = {
    "PROVED_LEAN": "PROVED_LEAN",
    "COMPUTATIONALLY_CHECKED": "FINITE COMPUTATION",
    "CONDITIONAL": "CONDITIONAL",
    "IMPORTED_ASSUMPTION": "DECLARED",
    "ADMITTED_PRIMITIVE": "DECLARED",
    "DEFINITION": "DEFINITION",
    "OPEN": "OPEN",
    "PROVED_PROSE": "ASSERTED",
    "REFUTED": "REFUTED BY AUDIT",
    "SOURCE_RECORD": "UNTYPED",
}


def marker(name, end=False):
    return f"<!-- {'END' if end else 'BEGIN'} GENERATED {name} (papers/core/tools/build_results_audit_table.py) -->"


def cell(text):
    """One-line, pipe-safe markdown table cell."""
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    return text.replace("|", "\\|")


def load():
    return json.loads(DAG.read_text(encoding="utf-8"))


def reviewed(dag):
    return [n for n in dag["nodes"] if "pfp_review" in n]


def status_cell(node):
    p = node["pfp_review"]
    if p["scope_effect"] == "status_lowered":
        return f"`{node['status']}` (was `{p['prior_status']}`)"
    return f"`{node['status']}`"


def census_block(dag):
    nodes, routes = dag["nodes"], dag["routes"]
    rev = reviewed(dag)
    ncount = collections.Counter(n["status"] for n in nodes)
    rcount = collections.Counter(n["status"] for n in rev)
    scount = collections.Counter(r["status"] for r in routes)
    unknown = set(ncount) - set(NODE_STATUS_ORDER)
    if unknown:
        raise SystemExit(f"unknown node status {unknown}")
    both = sum(1 for n in nodes if len(n.get("lean") or []) >= 2 and len(n.get("rust") or []) >= 2)
    no_lean = sum(1 for n in nodes if not n.get("lean"))
    no_rust = sum(1 for n in nodes if not n.get("rust"))
    stages = len({n["stage"] for n in nodes})
    sc = collections.Counter(n["pfp_review"]["scope_effect"] for n in rev)
    out = []
    out.append(
        f"The derivation DAG (`dag/derivation_dag.json`, schema `{dag['schema_version']}`) now has "
        f"{len(nodes)} nodes in {stages} stages and {len(routes)} routes. "
        f"The tables below are generated from that file by "
        f"`papers/core/tools/build_results_audit_table.py`; they replace the earlier "
        f"177-node, 172-route partition."
    )
    out.append("")
    out.append("| Node status | Nodes | PFP-reviewed |")
    out.append("| --- | ---: | ---: |")
    for s in NODE_STATUS_ORDER:
        if ncount.get(s):
            out.append(f"| `{s}` | {ncount[s]} | {rcount.get(s, 0)} |")
    out.append(f"| **Total** | **{len(nodes)}** | **{len(rev)}** |")
    out.append("")
    out.append("| Route status | Routes |")
    out.append("| --- | ---: |")
    for s in ROUTE_STATUS_ORDER:
        if scount.get(s):
            out.append(f"| `{s}` | {scount[s]} |")
    out.append(f"| **Total** | **{len(routes)}** |")
    out.append("")
    out.append(
        f"Of the {len(rev)} reviewed nodes, "
        + ", ".join(f"{sc.get(k, 0)} are `{k}`" for k in SCOPE_ORDER)
        + ". "
        f"Only {both} of the {len(nodes)} nodes cite two or more Lean declarations and two or more Rust "
        f"witnesses; {no_lean} cite no Lean declaration and {no_rust} cite no Rust witness. "
        f"A node's status is a label on its statement; it does not say that the statement is "
        f"mechanized in both languages."
    )
    return "\n".join(out)


def audit_block(dag):
    rev = reviewed(dag)
    out = []
    out.append(
        f"The table has one row for each of the {len(rev)} DAG nodes that carry a `pfp_review` object, "
        f"in DAG order. *DAG status* is the status the node holds now; where the review lowered it, "
        f"the earlier status is shown. *scope_effect* is `consistent` (statement kept), `caveat_added`, "
        f"`statement_narrowed` (the statement was rewritten down to the narrowest claim) or "
        f"`status_lowered`. *Narrowest claim* and *Does not support* are copied from the review."
    )
    out.append("")
    out.append("| Node | DAG status | scope_effect | Narrowest claim | Does not support |")
    out.append("| --- | --- | --- | --- | --- |")
    for n in rev:
        p = n["pfp_review"]
        out.append(
            f"| `{n['id']}` | {status_cell(n)} | `{p['scope_effect']}` | "
            f"{cell(p['narrowest_claim'])} | {cell(p['does_not_support'])} |"
        )
    return "\n".join(out)


def pfp_ledger_block(dag):
    rev = reviewed(dag)
    out = []
    out.append("| ID | Claim | Type | Evidence | DAG status |")
    out.append("| --- | --- | --- | --- | --- |")
    for n in rev:
        p = n["pfp_review"]
        typ = LEDGER_TYPE[n["status"]]
        status = n["status"]
        if p["scope_effect"] == "status_lowered":
            status += f" (was {p['prior_status']}; status_lowered)"
        else:
            status += f" ({p['scope_effect']})"
        out.append(
            f"| {n['id']} | {cell(p['narrowest_claim'])} | {typ} | `{p['review']}` | {status} |"
        )
    return "\n".join(out)


def count_ledger_types(text):
    """Count rows per Type over every table whose header starts '| ID | Claim | Type'."""
    counts = collections.Counter()
    in_table = False
    for line in text.split("\n"):
        if line.startswith("| ID | Claim | Type"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                in_table = False
                continue
            if line.startswith("| ---"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
            if len(cells) >= 3:
                counts[cells[2]] += 1
    return counts


def distribution_block(ledger_text, meanings):
    counts = count_ledger_types(ledger_text)
    out = ["| Type | Count | Meaning |", "| --- | ---: | --- |"]
    seen = set()
    for typ, meaning in meanings:
        out.append(f"| {typ} | {counts.get(typ, 0)} | {meaning} |")
        seen.add(typ)
    extra = set(counts) - seen
    if extra:
        raise SystemExit(f"ledger rows use types missing from the taxonomy: {sorted(extra)}")
    out.append(f"| **Total** | **{sum(counts.values())}** | |")
    return "\n".join(out)


# Taxonomy (order and meanings). PROVED_LEAN is defined here; it is the type of the
# FQM-U1-C1..C7 rows and of the DAG-keyed rows whose node status is PROVED_LEAN.
TAXONOMY = [
    ("ASSERTED", "Source proposal without admitted mechanical support for this claim."),
    ("SCOPE FENCE", "A scope boundary or non-claim."),
    ("OPEN", "An unresolved claim or conjecture."),
    ("DEFINITION", "A declared definition."),
    ("UNTYPED", "Historical source status still requires triage."),
    ("CONDITIONAL", "A statement with explicit antecedents and imported structure."),
    ("REFUTED BY AUDIT", "Historical audit refuted the source claim; do not cite it as true."),
    ("REFUTED BY COMPUTATION", "A named countermodel refutes the source claim; the corrected boundary is in the statement."),
    ("LEAN PROVED (RECEIPTED)", "Historical receipted source classification; receipt applicability remains subject to GAP-FQM-020."),
    ("PROVED_LEAN", "Added 2026-10-21. The row's statement, at the scope written in the row, is stated by the Lean 4 declarations named in its evidence, as recorded by a sealed run. The row's own scope limits its use; it says nothing about a parent DAG node, and it is not a physical claim. For DAG-keyed rows the scope is the review's narrowest claim."),
    ("FINITE COMPUTATION", "Named finite computations with the domains and limits stated in each evidence field; not a general proof."),
    ("EXACT FINITE ALGEBRA", "An exact algebraic result or finite decision at the declared scope."),
    ("FINITE FIXTURE", "A declared regression fixture, not a general theorem."),
    ("DECLARED", "An imported or supplied input."),
    ("REFUSAL", "A typed refusal."),
    ("PARTIAL", "A bounded result with the remaining obligation explicitly retained."),
]


def splice(text, name, body):
    b, e = marker(name), marker(name, end=True)
    i, j = text.find(b), text.find(e)
    if i < 0 or j < 0 or j < i:
        raise SystemExit(f"markers for {name!r} not found")
    return text[: i + len(b)] + "\n\n" + body + "\n\n" + text[j:]


def build(paper_text, ledger_text, dag):
    paper_text = splice(paper_text, "dag-census", census_block(dag))
    paper_text = splice(paper_text, "dag-results-audit", audit_block(dag))
    ledger_text = splice(ledger_text, "pfp-ledger", pfp_ledger_block(dag))
    # Distribution counts rows, so it is computed after the other ledger blocks are in place.
    ledger_text = splice(ledger_text, "ledger-distribution", distribution_block(ledger_text, TAXONOMY))
    return paper_text, ledger_text


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--write", action="store_true", help="update the files in place")
    g.add_argument("--check", action="store_true", help="exit 1 if a generated block is stale")
    args = ap.parse_args(argv)
    dag = load()
    paper_old = PAPER.read_text(encoding="utf-8")
    ledger_old = LEDGER.read_text(encoding="utf-8")
    paper_new, ledger_new = build(paper_old, ledger_old, dag)
    if args.write:
        for path, old, new in ((PAPER, paper_old, paper_new), (LEDGER, ledger_old, ledger_new)):
            if old != new:
                with open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(new)
            print(f"{path.name}: {'updated' if old != new else 'already current'}")
        return 0
    if args.check:
        stale = [p.name for p, o, n in ((PAPER, paper_old, paper_new), (LEDGER, ledger_old, ledger_new)) if o != n]
        print("stale: " + ", ".join(stale) if stale else "generated blocks are current")
        return 1 if stale else 0
    print(census_block(dag))
    print()
    print(audit_block(dag)[:1500] + "\n...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
