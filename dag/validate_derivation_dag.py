"""Origin: dag/validate_derivation_dag.py
Claim: derivation_dag.json is a finite acyclic record whose node and route fields match the declared vocabulary and whose cited paths resolve
AuthorityEffect: None
Scope Fence: this file does not claim that any recorded statement is true
Level: L5
MutationKillCount: 3

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
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

BigRational = Fraction

HERE = Path(__file__).resolve().parent
DAG = HERE / "derivation_dag.json"

STAGES = (
    "PREGENESIS",
    "GENESIS",
    "MSSN_SN",
    "WDP",
    "L1_EMERGENCE",
    "L1_TO_L2",
    "FINITE_QM_CORE",
    "FINITE_QM_DYNAMICS",
    "FINITE_QM_STRUCTURE",
    "IMPLEMENTATION",
    "DRESSING_FIELD",
    "MUTUALLY_UNBIASED_BASES",
    "FERMION_SIGN",
)
STATUSES = (
    "ADMITTED_PRIMITIVE",
    "DEFINITION",
    "PROVED_PROSE",
    "PROVED_LEAN",
    "COMPUTATIONALLY_CHECKED",
    "CONDITIONAL",
    "IMPORTED_ASSUMPTION",
    "OPEN",
    "REFUTED",
)
ROUTE_STATUSES = (
    "DERIVED_PROSE",
    "DERIVED_LEAN",
    "COMPUTED",
    "CONDITIONAL_ON_IMPORT",
    "GAP_NO_DERIVATION",
)
NODE_KEYS = {
    "id",
    "stage",
    "status",
    "source_status",
    "statement",
    "source",
    "lean",
    "rust",
    "imported_structure",
    "bottleneck",
    "tags",
    "see_also",
}
FORBIDDEN = (
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
_PROVED_PHRASES = (
    "not yet proved",
    "not yet written or checked",
    "no lean proof",
    "recorded open",
    "is open in the",
)
_ROUTED_STATUSES = (
    "PROVED_PROSE",
    "PROVED_LEAN",
    "COMPUTATIONALLY_CHECKED",
    "CONDITIONAL",
    "REFUTED",
)
EXTERNAL_PREFIXES = ("pr:", "external:")
_STRING_FIELDS = ("id", "stage", "status", "source_status", "statement", "bottleneck")
_LIST_FIELDS = ("source", "lean", "rust", "imported_structure", "tags", "see_also")


class DagContractError(Exception):
    def __init__(self, invariant: str, detail: str) -> None:
        self.invariant = invariant
        self.detail = detail
        super().__init__(detail)


@dataclass(frozen=True)
class Verification:
    claim: str
    holds: bool
    detail: str


def exact_int(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise DagContractError(
            "exact-integer",
            "Expected exact integer, received boolean or non-integer",
        )
    return value


def big_rational(numer: object, denom: object) -> BigRational:
    den = exact_int(denom)
    if den == 0:
        raise DagContractError("rational-denominator", "rational denominator is nonzero")
    return BigRational(exact_int(numer), den)


def acyclic_ratio(seen: object, total: object) -> BigRational:
    width = exact_int(total)
    if width == 0:
        raise DagContractError("rational-denominator", "rational denominator is nonzero")
    return big_rational(seen, width)


def verify_acyclic_ratio(seen: object, total: object) -> Verification:
    try:
        ratio = acyclic_ratio(seen, total)
    except DagContractError as error:
        return Verification("acyclic-ratio", False, error.detail)
    return Verification("acyclic-ratio", ratio == big_rational(1, 1), str(ratio))


def repo_root_from(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "omega_engine").is_dir() and (parent / "omega_engine_atlas").is_dir():
            return parent
    raise DagContractError("repo-root-resolves", "repo root not found; pass --repo-root")


def split_ref(ref: str) -> tuple[str, str | None]:
    path, _, tail = ref.partition("::")
    return path, tail or None


def is_external(ref: str) -> bool:
    return ref.startswith(EXTERNAL_PREFIXES)


def line_ref_path(ref: str) -> str:
    path = ref.split("#", 1)[0]
    match = re.match(r"^(.*?):(\d+)(?:[-,]\d+)*$", path)
    if match is None:
        return path
    return match.group(1)


def _mapping(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None
    mapped: dict[str, object] = {}
    for key, item in value.items():
        if isinstance(key, str):
            mapped[key] = item
    return mapped


def _maps(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    rows: list[dict[str, object]] = []
    for item in value:
        mapped = _mapping(item)
        if mapped is not None:
            rows.append(mapped)
    return rows


def _text(node: dict[str, object], key: str) -> str:
    value = node.get(key)
    if isinstance(value, str):
        return value
    return ""


def _string_list(value: object) -> list[str] | None:
    if not isinstance(value, list):
        return None
    rows: list[str] = []
    for item in value:
        if not isinstance(item, str):
            return None
        rows.append(item)
    return rows


def _walk_strings(value: object) -> list[str]:
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
        return out
    if isinstance(value, list):
        for item in value:
            out.extend(_walk_strings(item))
        return out
    mapped = _mapping(value)
    if mapped is None:
        return out
    for item in mapped.values():
        out.extend(_walk_strings(item))
    return out


def _id_mentioned(text: str, node_id: str) -> bool:
    return re.search(
        r"(?<![A-Za-z0-9-])" + re.escape(node_id) + r"(?![A-Za-z0-9-])",
        text,
    ) is not None


def _check_bottlenecks(node_id: str, nodes: list[dict[str, object]]) -> bool:
    for other in nodes:
        if _text(other, "id") == node_id:
            continue
        bottleneck = _text(other, "bottleneck")
        if "open in lean" in bottleneck.lower() and _id_mentioned(bottleneck, node_id):
            return True
    return False


def _node_conflict_reason(
    node: dict[str, object],
    blocking_notes: list[str],
    nodes: list[dict[str, object]],
) -> str | None:
    node_id = _text(node, "id")
    tags = _string_list(node.get("tags")) or []
    if "unwritten" in tags:
        return "tagged unwritten"
    if "proposed-pr-open" in tags:
        return "tagged proposed-pr-open"
    if any(_id_mentioned(note, node_id) for note in blocking_notes):
        return "a segment note says that id is OPEN or that no proof or Lean was checked"
    if _check_bottlenecks(node_id, nodes):
        return "another bottleneck says it is open in Lean"
    return None


def proved_lean_record_conflicts(dag: dict[str, object]) -> dict[str, str]:
    nodes = _maps(dag.get("nodes"))
    blocking_notes = [
        note
        for note in _walk_strings(dag.get("segment_notes"))
        if "no proof or lean was checked" in note.lower() or "status open" in note.lower()
    ]
    conflicts: dict[str, str] = {}
    for node in nodes:
        if _text(node, "status") != "PROVED_LEAN":
            continue
        node_id = _text(node, "id")
        reason = _node_conflict_reason(node, blocking_notes, nodes)
        if reason:
            conflicts[node_id] = reason
    return conflicts


def _missing_strings(node: dict[str, object]) -> list[str]:
    errs: list[str] = []
    node_id = node.get("id")
    for key in _STRING_FIELDS:
        value = node.get(key)
        if not isinstance(value, str) or not value:
            errs.append(f"node {node_id}: missing string field {key}")
    return errs


def _bad_lists(node: dict[str, object]) -> list[str]:
    errs: list[str] = []
    node_id = node.get("id")
    for key in _LIST_FIELDS:
        if key in ("tags", "see_also") and key not in node:
            continue
        rows = _string_list(node.get(key))
        if rows is None:
            errs.append(f"node {node_id}: field {key} must be a list of strings")
    return errs


def _validate_node_schema(node: dict[str, object]) -> list[str]:
    errs: list[str] = []
    extra = set(node) - NODE_KEYS
    if extra:
        errs.append(f"node {node.get('id')}: unknown keys {sorted(extra)}")
    errs.extend(_missing_strings(node))
    errs.extend(_bad_lists(node))
    return errs


def _proved_statement_errors(node: dict[str, object]) -> list[str]:
    errs: list[str] = []
    statement = _text(node, "statement").lower()
    for phrase in _PROVED_PHRASES:
        if phrase in statement:
            errs.append(f"node {node.get('id')}: PROVED_LEAN but statement says {phrase!r}")
    return errs


def _validate_node_semantic(node: dict[str, object], conflicts: dict[str, str]) -> list[str]:
    errs: list[str] = []
    node_id = _text(node, "id")
    if _text(node, "stage") not in STAGES:
        errs.append(f"node {node.get('id')}: bad stage {node.get('stage')}")
    if _text(node, "status") not in STATUSES:
        errs.append(f"node {node.get('id')}: bad status {node.get('status')}")
    if _text(node, "status") == "PROVED_LEAN" and not _string_list(node.get("lean")):
        errs.append(f"node {node.get('id')}: PROVED_LEAN without a lean reference")
    if _text(node, "status") == "PROVED_LEAN":
        errs.extend(_proved_statement_errors(node))
        reason = conflicts.get(node_id)
        if reason:
            errs.append(f"node {node.get('id')}: PROVED_LEAN but {reason}")
    if _text(node, "status") not in ("ADMITTED_PRIMITIVE", "OPEN") and not _string_list(node.get("source")):
        errs.append(f"node {node.get('id')}: no source reference")
    return errs


def _check_nodes(
    nodes: list[dict[str, object]],
    conflicts: dict[str, str],
) -> tuple[list[str], dict[str, dict[str, object]]]:
    errs: list[str] = []
    ids: dict[str, dict[str, object]] = {}
    for node in nodes:
        errs.extend(_validate_node_schema(node))
        node_id = _text(node, "id")
        if node_id in ids:
            errs.append(f"duplicate node id {node_id}")
        ids[node_id] = node
        errs.extend(_validate_node_semantic(node, conflicts))
    return errs, ids


def _route_endpoint_errors(route: dict[str, object], ids: dict[str, dict[str, object]]) -> list[str]:
    errs: list[str] = []
    rid = route.get("id")
    output = _text(route, "output")
    inputs = _string_list(route.get("inputs")) or []
    if output not in ids:
        errs.append(f"route {rid}: unknown output {route.get('output')}")
    for item in inputs:
        if item not in ids:
            errs.append(f"route {rid}: unknown input {item}")
    if not inputs:
        errs.append(f"route {rid}: no inputs")
    if output in inputs:
        errs.append(f"route {rid}: output among its inputs")
    return errs


def _route_status_errors(route: dict[str, object]) -> list[str]:
    errs: list[str] = []
    rid = route.get("id")
    status = _text(route, "status")
    if status not in ROUTE_STATUSES:
        errs.append(f"route {rid}: bad status {route.get('status')}")
    sources = _string_list(route.get("source")) or []
    if status != "GAP_NO_DERIVATION" and not sources:
        errs.append(f"route {rid}: derived route without source")
    return errs


def _check_routes(
    routes: list[dict[str, object]],
    ids: dict[str, dict[str, object]],
) -> tuple[list[str], dict[str, list[dict[str, object]]]]:
    errs: list[str] = []
    seen: set[str] = set()
    incoming: dict[str, list[dict[str, object]]] = defaultdict(list)
    for route in routes:
        rid = _text(route, "id")
        if rid in seen:
            errs.append(f"duplicate route id {route.get('id')}")
        seen.add(rid)
        errs.extend(_route_status_errors(route))
        errs.extend(_route_endpoint_errors(route, ids))
        incoming[_text(route, "output")].append(route)
    return errs, incoming


def _route_edges(
    routes: list[dict[str, object]],
    ids: dict[str, dict[str, object]],
) -> tuple[dict[str, set[str]], dict[str, int]]:
    succ: dict[str, set[str]] = defaultdict(set)
    indeg: dict[str, int] = {key: 0 for key in ids}
    for route in routes:
        output = _text(route, "output")
        for item in _string_list(route.get("inputs")) or []:
            if item in ids and output in ids and output not in succ[item]:
                succ[item].add(output)
                indeg[output] = indeg[output] + 1
    return succ, indeg


def _kahn_seen(succ: dict[str, set[str]], indeg: dict[str, int]) -> int:
    queue = [key for key, degree in indeg.items() if degree == 0]
    seen = 0
    while queue:
        current = queue.pop()
        seen = seen + 1
        for nxt in succ[current]:
            indeg[nxt] = indeg[nxt] - 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return seen


def _check_acyclicity(
    routes: list[dict[str, object]],
    ids: dict[str, dict[str, object]],
) -> list[str]:
    succ, indeg = _route_edges(routes, ids)
    seen = _kahn_seen(succ, indeg)
    if len(ids) == 0 or verify_acyclic_ratio(seen, len(ids)).holds:
        return []
    cyc = sorted(key for key, degree in indeg.items() if degree > 0)
    return [f"cycle among nodes: {cyc[:12]}"]


def _gap_only(routes: list[dict[str, object]]) -> bool:
    if not routes:
        return False
    for route in routes:
        if _text(route, "status") != "GAP_NO_DERIVATION":
            return False
    return True


def _check_incoming_routes(
    ids: dict[str, dict[str, object]],
    incoming: dict[str, list[dict[str, object]]],
) -> list[str]:
    errs: list[str] = []
    for key, node in ids.items():
        status = _text(node, "status")
        routes = incoming.get(key) or []
        if status in _ROUTED_STATUSES and not routes:
            errs.append(f"node {key}: status {status} but no incoming route")
        if status in ("PROVED_PROSE", "PROVED_LEAN") and _gap_only(routes):
            errs.append(f"node {key}: {status} but every incoming route is a gap")
    return errs


def _check_forbidden_words(dag: dict[str, object]) -> list[str]:
    errs: list[str] = []
    blob = json.dumps(dag).lower()
    for word in FORBIDDEN:
        if re.search(r"\b" + re.escape(word) + r"\b", blob):
            errs.append(f"forbidden word in file: {word}")
    return errs


def _path_exists(root: Path, ref: str) -> bool:
    return (root / ref).exists()


def _symbol_errors(root: Path, node_id: object, field: str, ref: str) -> list[str]:
    path, symbol = split_ref(ref)
    if not _path_exists(root, path):
        return [f"node {node_id}: {field} path missing: {path}"]
    if not symbol or not (root / path).is_file():
        return []
    text = (root / path).read_text(encoding="utf-8", errors="replace")
    leaf = symbol.split("::")[-1].split(".")[-1]
    if leaf not in text:
        return [f"node {node_id}: symbol {symbol} not in {path}"]
    return []


def _node_ref_errors(node: dict[str, object], root: Path) -> list[str]:
    errs: list[str] = []
    node_id = node.get("id")
    for ref in _string_list(node.get("source")) or []:
        if not is_external(ref) and not _path_exists(root, line_ref_path(ref)):
            errs.append(f"node {node_id}: source path missing: {ref}")
    for field in ("lean", "rust"):
        for ref in _string_list(node.get(field)) or []:
            if is_external(ref):
                continue
            errs.extend(_symbol_errors(root, node_id, field, ref))
    return errs


def _route_ref_errors(route: dict[str, object], root: Path) -> list[str]:
    errs: list[str] = []
    for ref in _string_list(route.get("source")) or []:
        if not is_external(ref) and not _path_exists(root, line_ref_path(ref)):
            errs.append(f"route {route.get('id')}: source path missing: {ref}")
    return errs


def _check_file_refs(
    nodes: list[dict[str, object]],
    routes: list[dict[str, object]],
    root: Path,
) -> list[str]:
    errs: list[str] = []
    for node in nodes:
        errs.extend(_node_ref_errors(node, root))
    for route in routes:
        errs.extend(_route_ref_errors(route, root))
    return errs


def check(dag: dict[str, object], root: Path | None) -> list[str]:
    conflicts = proved_lean_record_conflicts(dag)
    nodes = _maps(dag.get("nodes"))
    routes = _maps(dag.get("routes"))
    node_errs, ids = _check_nodes(nodes, conflicts)
    route_errs, incoming = _check_routes(routes, ids)
    cyc_errs = _check_acyclicity(routes, ids)
    inc_errs = _check_incoming_routes(ids, incoming)
    forbid_errs = _check_forbidden_words(dag)
    file_errs: list[str] = []
    if root is not None:
        file_errs = _check_file_refs(nodes, routes, root)
    return node_errs + route_errs + cyc_errs + inc_errs + forbid_errs + file_errs


def _load_dag(path: Path) -> dict[str, object]:
    try:
        payload: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DagContractError("dag-parses", str(error)) from error
    mapped = _mapping(payload)
    if mapped is None:
        raise DagContractError("dag-is-object", "dag root must be an object")
    return mapped


def _selected_root(skip_files: bool, given: Path | None) -> Path | None:
    if skip_files:
        return None
    if given is not None:
        return given
    return repo_root_from(HERE)


def _print_report(dag: dict[str, object], errs: list[str]) -> None:
    for err in errs:
        print("FAIL", err)
    nodes = _maps(dag.get("nodes"))
    routes = _maps(dag.get("routes"))
    print(f"nodes={len(nodes)} routes={len(routes)} failures={len(errs)}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--no-files", action="store_true", help="skip path/symbol resolution")
    parser.add_argument("--dag", type=Path, default=DAG)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        dag = _load_dag(args.dag)
        root = _selected_root(bool(args.no_files), args.repo_root)
    except DagContractError as error:
        print("FAIL", error.detail)
        return 1
    errs = check(dag, root)
    _print_report(dag, errs)
    if errs:
        return exact_int(1)
    return exact_int(0)


if __name__ == "__main__":
    sys.exit(main())
