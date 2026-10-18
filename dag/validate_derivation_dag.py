"""Validator for derivation_dag.json (AuthorityEffect: None).

Checks structure only: schema, reference resolution, acyclicity, vocabulary,
that cited repository paths exist, and that cited Lean/Rust symbols occur in the
cited file. It does not check that any statement is true.

References beginning with "pr:" or "external:" name pull requests or files outside
this checkout and are not resolved.

Usage: python validate_derivation_dag.py [--repo-root DIR] [--no-files]
Exit status 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DAG = HERE / "derivation_dag.json"

STAGES = (
    "PREGENESIS", "GENESIS", "MSSN_SN", "WDP", "L1_EMERGENCE", "L1_TO_L2",
    "FINITE_QM_CORE", "FINITE_QM_DYNAMICS", "FINITE_QM_STRUCTURE", "IMPLEMENTATION",
)
STATUSES = (
    "ADMITTED_PRIMITIVE", "DEFINITION", "PROVED_PROSE", "PROVED_LEAN",
    "COMPUTATIONALLY_CHECKED", "CONDITIONAL", "IMPORTED_ASSUMPTION", "OPEN", "REFUTED",
)
ROUTE_STATUSES = (
    "DERIVED_PROSE", "DERIVED_LEAN", "COMPUTED", "CONDITIONAL_ON_IMPORT", "GAP_NO_DERIVATION",
)
NODE_KEYS = {
    "id", "stage", "status", "source_status", "statement", "source", "lean", "rust",
    "imported_structure", "bottleneck", "tags", "see_also",
}
FORBIDDEN = (
    "proves", "guarantees", "mathematically verifies", "fundamentally", "true intelligence",
    "impossible", "universal", "flawless", "perfectly", "clearly", "obviously", "simply",
    "merely", "weaponized",
)


def repo_root_from(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "omega_engine").is_dir() and (parent / "omega_engine_atlas").is_dir():
            return parent
    raise SystemExit("repo root not found; pass --repo-root")


def split_ref(ref: str) -> tuple[str, str | None]:
    path, _, tail = ref.partition("::")
    return path, tail or None


EXTERNAL_PREFIXES = ("pr:", "external:")


def is_external(ref: str) -> bool:
    """References to pull requests or files outside this checkout are not resolved."""
    return ref.startswith(EXTERNAL_PREFIXES)


def line_ref_path(ref: str) -> str:
    path = ref.split("#", 1)[0]
    m = re.match(r"^(.*?):(\d+)(?:[-,]\d+)*$", path)
    return m.group(1) if m else path


def _walk_strings(value) -> list[str]:
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, list):
        for item in value:
            out.extend(_walk_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            out.extend(_walk_strings(item))
    return out


def _id_mentioned(text: str, node_id: str) -> bool:
    return re.search(
        r"(?<![A-Za-z0-9-])" + re.escape(node_id) + r"(?![A-Za-z0-9-])",
        text,
    ) is not None


def _check_bottlenecks(node_id: str, nodes: list[dict]) -> bool:
    for other in nodes:
        if other.get("id") == node_id:
            continue
        bottleneck = str(other.get("bottleneck") or "")
        if "open in lean" in bottleneck.lower() and _id_mentioned(bottleneck, node_id):
            return True
    return False


def _node_conflict_reason(node: dict, blocking_notes: list[str], nodes: list[dict]) -> str | None:
    node_id = str(node.get("id") or "")
    tags = node.get("tags") or []
    if "unwritten" in tags:
        return "tagged unwritten"
    if "proposed-pr-open" in tags:
        return "tagged proposed-pr-open"
    if any(_id_mentioned(note, node_id) for note in blocking_notes):
        return "a segment note says that id is OPEN or that no proof or Lean was checked"
    if _check_bottlenecks(node_id, nodes):
        return "another bottleneck says it is open in Lean"
    return None


def proved_lean_record_conflicts(dag: dict) -> dict[str, str]:
    """PROVED_LEAN ids the file itself still marks unwritten or unchecked.

    A tag, a segment note, or another node's bottleneck is enough. The
    statement text is not consulted.
    """
    nodes = dag.get("nodes") or []
    blocking_notes = [
        note
        for note in _walk_strings(dag.get("segment_notes"))
        if "no proof or lean was checked" in note.lower() or "status open" in note.lower()
    ]
    conflicts: dict[str, str] = {}
    for node in nodes:
        if node.get("status") != "PROVED_LEAN":
            continue
        node_id = str(node.get("id") or "")
        reason = _node_conflict_reason(node, blocking_notes, nodes)
        if reason:
            conflicts[node_id] = reason
    return conflicts


def _validate_node_schema(n: dict) -> list[str]:
    errs: list[str] = []
    extra = set(n) - NODE_KEYS
    if extra:
        errs.append(f"node {n.get('id')}: unknown keys {sorted(extra)}")
    for k in ("id", "stage", "status", "source_status", "statement", "bottleneck"):
        if not isinstance(n.get(k), str) or not n.get(k):
            errs.append(f"node {n.get('id')}: missing string field {k}")
    for k in ("source", "lean", "rust", "imported_structure", "tags", "see_also"):
        if k in ("tags", "see_also") and k not in n:
            continue
        if not isinstance(n.get(k), list) or not all(isinstance(x, str) for x in n.get(k, [])):
            errs.append(f"node {n.get('id')}: field {k} must be a list of strings")
    return errs


def _validate_node_semantic(n: dict, conflicts: dict[str, str]) -> list[str]:
    errs: list[str] = []
    if n.get("stage") not in STAGES:
        errs.append(f"node {n.get('id')}: bad stage {n.get('stage')}")
    if n.get("status") not in STATUSES:
        errs.append(f"node {n.get('id')}: bad status {n.get('status')}")
    if n.get("status") == "PROVED_LEAN" and not n.get("lean"):
        errs.append(f"node {n.get('id')}: PROVED_LEAN without a lean reference")
    if n.get("status") == "PROVED_LEAN":
        statement = str(n.get("statement") or "").lower()
        for phrase in (
            "not yet proved",
            "not yet written or checked",
            "no lean proof",
            "recorded open",
            "is open in the",
        ):
            if phrase in statement:
                errs.append(f"node {n.get('id')}: PROVED_LEAN but statement says {phrase!r}")
        reason = conflicts.get(str(n.get("id") or ""))
        if reason:
            errs.append(f"node {n.get('id')}: PROVED_LEAN but {reason}")
    if n.get("status") not in ("ADMITTED_PRIMITIVE", "OPEN") and not n.get("source"):
        errs.append(f"node {n.get('id')}: no source reference")
    return errs


def _check_nodes(nodes: list[dict], conflicts: dict[str, str]) -> tuple[list[str], dict[str, dict]]:
    errs: list[str] = []
    ids: dict[str, dict] = {}
    for n in nodes:
        errs.extend(_validate_node_schema(n))
        node_id = str(n.get("id") or "")
        if node_id in ids:
            errs.append(f"duplicate node id {node_id}")
        ids[node_id] = n
        errs.extend(_validate_node_semantic(n, conflicts))
    return errs, ids


def _check_routes(routes: list[dict], ids: dict[str, dict]) -> tuple[list[str], dict[str, list[dict]]]:
    errs: list[str] = []
    rids: set[str] = set()
    incoming: dict[str, list[dict]] = defaultdict(list)
    for r in routes:
        rid = r.get("id")
        if rid in rids:
            errs.append(f"duplicate route id {rid}")
        rids.add(rid)
        if r.get("status") not in ROUTE_STATUSES:
            errs.append(f"route {rid}: bad status {r.get('status')}")
        if r.get("output") not in ids:
            errs.append(f"route {rid}: unknown output {r.get('output')}")
        for i in r.get("inputs", []):
            if i not in ids:
                errs.append(f"route {rid}: unknown input {i}")
        if not r.get("inputs"):
            errs.append(f"route {rid}: no inputs")
        if r.get("status") != "GAP_NO_DERIVATION" and not r.get("source"):
            errs.append(f"route {rid}: derived route without source")
        if r.get("output") in r.get("inputs", []):
            errs.append(f"route {rid}: output among its inputs")
        incoming[r.get("output", "")].append(r)
    return errs, incoming


def _check_acyclicity(routes: list[dict], ids: dict[str, dict]) -> list[str]:
    succ: dict[str, set[str]] = defaultdict(set)
    indeg: dict[str, int] = {i: 0 for i in ids}
    for r in routes:
        for i in r.get("inputs", []):
            if i in ids and r.get("output") in ids and r["output"] not in succ[i]:
                succ[i].add(r["output"])
                indeg[r["output"]] += 1
    queue = [i for i, d in indeg.items() if d == 0]
    seen = 0
    while queue:
        x = queue.pop()
        seen += 1
        for y in succ[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                queue.append(y)
    if seen != len(ids):
        cyc = sorted(i for i, d in indeg.items() if d > 0)
        return [f"cycle among nodes: {cyc[:12]}"]
    return []


def _check_incoming_routes(ids: dict[str, dict], incoming: dict[str, list[dict]]) -> list[str]:
    errs: list[str] = []
    for i, n in ids.items():
        if n["status"] in ("PROVED_PROSE", "PROVED_LEAN", "COMPUTATIONALLY_CHECKED", "CONDITIONAL", "REFUTED") and not incoming.get(i):
            errs.append(f"node {i}: status {n['status']} but no incoming route")
        if n["status"] in ("PROVED_PROSE", "PROVED_LEAN") and incoming.get(i) and all(
            r["status"] == "GAP_NO_DERIVATION" for r in incoming[i]
        ):
            errs.append(f"node {i}: {n['status']} but every incoming route is a gap")
    return errs


def _check_forbidden_words(dag: dict) -> list[str]:
    errs: list[str] = []
    blob = json.dumps(dag).lower()
    for w in FORBIDDEN:
        if re.search(r"\b" + re.escape(w) + r"\b", blob):
            errs.append(f"forbidden word in file: {w}")
    return errs


def _check_file_refs(nodes: list[dict], routes: list[dict], root: Path) -> list[str]:
    errs: list[str] = []

    def exists(rel: str) -> bool:
        return (root / rel).exists()

    for n in nodes:
        for ref in n.get("source", []):
            if not is_external(ref) and not exists(line_ref_path(ref)):
                errs.append(f"node {n['id']}: source path missing: {ref}")
        for field in ("lean", "rust"):
            for ref in n.get(field, []):
                if is_external(ref):
                    continue
                p, sym = split_ref(ref)
                if not exists(p):
                    errs.append(f"node {n['id']}: {field} path missing: {p}")
                elif sym and (root / p).is_file():
                    text = (root / p).read_text(encoding="utf-8", errors="replace")
                    leaf = sym.split("::")[-1].split(".")[-1]
                    if leaf not in text:
                        errs.append(f"node {n['id']}: symbol {sym} not in {p}")
    for r in routes:
        for ref in r.get("source", []):
            if not is_external(ref) and not exists(line_ref_path(ref)):
                errs.append(f"route {r['id']}: source path missing: {ref}")
    return errs


def check(dag: dict, root: Path | None) -> list[str]:
    conflicts = proved_lean_record_conflicts(dag)
    node_errs, ids = _check_nodes(dag.get("nodes", []), conflicts)
    route_errs, incoming = _check_routes(dag.get("routes", []), ids)
    cyc_errs = _check_acyclicity(dag.get("routes", []), ids)
    inc_errs = _check_incoming_routes(ids, incoming)
    forbid_errs = _check_forbidden_words(dag)
    file_errs = _check_file_refs(dag.get("nodes", []), dag.get("routes", []), root) if root is not None else []
    return node_errs + route_errs + cyc_errs + inc_errs + forbid_errs + file_errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path)
    ap.add_argument("--no-files", action="store_true", help="skip path/symbol resolution")
    ap.add_argument("--dag", type=Path, default=DAG)
    args = ap.parse_args(argv)
    dag = json.loads(args.dag.read_text(encoding="utf-8"))
    root = None if args.no_files else (args.repo_root or repo_root_from(HERE))
    errs = check(dag, root)
    for e in errs:
        print("FAIL", e)
    print(f"nodes={len(dag['nodes'])} routes={len(dag['routes'])} failures={len(errs)}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
