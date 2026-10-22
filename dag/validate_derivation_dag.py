"""Origin: dag/validate_derivation_dag.py
Claim: derivation_dag.json is a finite acyclic record whose node, route and TFQ record fields match the declared vocabulary, whose records and nodes name each other, whose cited paths resolve and whose JSONL and Markdown views match the renderer
AuthorityEffect: None
Scope Fence: this file does not claim that any recorded statement is true
Level: L5
MutationKillCount: 10

Checks structure only: schema, reference resolution, acyclicity, vocabulary,
that cited repository paths exist, and that cited Lean/Rust symbols occur in the
cited file. It does not check that any statement is true. A pfp_review object on a
node is checked for shape, for a status that is not above its prior_status, and (when
files are checked) for an existing review file whose sha256 matches.

derivation_dag.json (schema derivation_dag.v2) is the single source of the derivation
graph. A document that declares a schema_version, or carries records, must be v2 and
carry the top-level keys of DAG_REQUIRED_KEYS. Its TFQ records (top-level key records)
are checked for their fields, unique ids, a parent_id that names another record (null
only for a root) without a parent cycle, at least one existing_derivation_dag_ids entry
that is a node, and every node being named by at least one record; when files are
checked, every record must have a derivation paper dag/derivations/*/tfq_NNNN_*.md.
The views theory_of_finite_qm.jsonl and theory_of_finite_qm.md next to the DAG file must
be byte-identical to what dag/render_dag_views.py renders (skip with --no-views).

References beginning with "pr:" or "external:" name pull requests or files outside
this checkout and are not resolved.

Usage: python validate_derivation_dag.py [--repo-root DIR] [--no-files] [--no-views]
Exit status 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import hashlib
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
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import render_dag_views  # noqa: E402

SCHEMA_VERSION = "derivation_dag.v2"
# Top-level keys of derivation_dag.json; a document declaring a schema_version must carry the required ones.
DAG_REQUIRED_KEYS = ("schema_version", "stages", "nodes", "routes", "records", "index_document")
DAG_KEYS = set(DAG_REQUIRED_KEYS) | {
    "title",
    "authority_effect",
    "source_commit",
    "model_dag",
    "scope",
    "status_legend",
    "edge_semantics",
    "non_discharge_notes",
    "segment_notes",
    "schema_notes",
}
INDEX_DOCUMENT_KEYS = (
    "header_markdown",
    "record_count_note",
    "stage_index",
    "application_stages",
    "coda_atlas_packages",
    "source_corpus_restatements",
)
CODA_PACKAGE_KEYS = ("floor", "shelf", "package", "path")
RESTATEMENT_KEYS = ("source_id", "corpus", "alias_of")
# A TFQ record, as one line of theory_of_finite_qm.jsonl renders it.
RECORD_STRING_FIELDS = ("id", "local_id", "name", "obligation", "record_status", "source_slice", "stage", "summary", "uuid")
RECORD_LIST_FIELDS = (
    "coda_atlas_ids",
    "coda_atlas_paths",
    "existing_derivation_dag_ids",
    "f004_refs",
    "lean4",
    "python",
    "rust",
)
RECORD_KEYS = set(RECORD_STRING_FIELDS) | set(RECORD_LIST_FIELDS) | {"parent_id"}
RECORD_OPTIONAL_KEYS = ("pfp_review_refs",)
RECORD_ID = re.compile(r"TFQ-\d{4}")
RECORD_STATUS = re.compile(r"[A-Z][A-Z0-9_]*")

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
    "TENSOR_COMPOSITION",
    # TFQ tree stages that gained nodes when the DAG and the JSONL were joined (sync_unified_dag.py).
    "FINITE_OBSTRUCTION",
    "AUTHORIZATION",
    "FINITE_HILBERT",
    "FINITE_QM_INFORMATION",
    "FINITE_GAUGE",
    "FINITE_QED",
    "FINITE_ELECTROWEAK",
    "FINITE_QCD",
    "FINITE_TOPOLOGICAL",
    "FINITE_QG",
    "CONTINUUM_INTERFACE",
    "IMPLEMENTATION_CORE",
    "IMPLEMENTATION_SIBLING",
    "ENGINE_CUSTODY",
    "MAJORANA",
    "COMPUTATION",
    # Frontier branches (sync_frontier_branches.py).
    "CONSTRUCTOR_THEORY",
    "CAUSAL_QFT",
    "ADS_CFT",
    "LOOP_QUANTUM_GRAVITY",
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
    "SOURCE_RECORD",
)
ROUTE_STATUSES = (
    "DERIVED_PROSE",
    "DERIVED_LEAN",
    "COMPUTED",
    "CONDITIONAL_ON_IMPORT",
    "GAP_NO_DERIVATION",
    "RECORD_PARENT",
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
    "pfp_review",
}
# The pfp_review object that sync_pfp_results.py writes onto a node whose PFP result folder was reviewed.
PFP_REVIEW_KEYS = (
    "review",
    "review_sha256",
    "review_refs",
    "verdict",
    "narrowest_claim",
    "does_not_support",
    "next_test",
    "scope_effect",
    "reason",
    "prior_status",
    "prior_statement",
    "prior_bottleneck",
    "superseded_by",
)
PFP_REVIEW_OPTIONAL_KEYS = ("prior_route_status",)
PFP_SCOPE_EFFECTS = ("consistent", "caveat_added", "statement_narrowed", "status_lowered")
# Weakest to strongest; a reviewed node may keep or lower its prior status, never raise it.
PFP_STATUS_RANK = {
    "OPEN": 0,
    "SOURCE_RECORD": 0,
    "IMPORTED_ASSUMPTION": 1,
    "ADMITTED_PRIMITIVE": 1,
    "CONDITIONAL": 2,
    "DEFINITION": 2,
    "COMPUTATIONALLY_CHECKED": 3,
    "PROVED_PROSE": 4,
    "PROVED_LEAN": 5,
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


def symbol_leaf(symbol: str) -> str:
    """The last name component of a cited symbol: the part that must occur in the cited file."""
    return symbol.split("::")[-1].split(".")[-1]


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


def _pfp_text_errors(node_id: object, review: dict[str, object]) -> list[str]:
    errs: list[str] = []
    for key in PFP_REVIEW_KEYS:
        if key in ("review_refs", "superseded_by"):
            continue
        value = review.get(key)
        if not isinstance(value, str) or not value:
            errs.append(f"node {node_id}: pfp_review.{key} must be a non-empty string")
    sha = review.get("review_sha256")
    if isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha) is None:
        errs.append(f"node {node_id}: pfp_review.review_sha256 is not a sha256 hex digest")
    return errs


def _pfp_list_errors(node_id: object, review: dict[str, object]) -> list[str]:
    errs: list[str] = []
    refs = _string_list(review.get("review_refs"))
    if not refs:
        errs.append(f"node {node_id}: pfp_review.review_refs must be a non-empty list of strings")
    elif refs[-1] != review.get("review"):
        errs.append(f"node {node_id}: pfp_review.review_refs must end with the review path")
    if _string_list(review.get("superseded_by")) is None:
        errs.append(f"node {node_id}: pfp_review.superseded_by must be a list of strings")
    return errs


def _pfp_status_errors(node: dict[str, object], review: dict[str, object]) -> list[str]:
    errs: list[str] = []
    node_id = node.get("id")
    status = _text(node, "status")
    prior = review.get("prior_status")
    if review.get("scope_effect") not in PFP_SCOPE_EFFECTS:
        errs.append(f"node {node_id}: pfp_review.scope_effect {review.get('scope_effect')!r} is not in the vocabulary")
    if prior not in PFP_STATUS_RANK or status not in PFP_STATUS_RANK:
        if status != prior:
            errs.append(f"node {node_id}: pfp_review.prior_status {prior!r} cannot be compared with {status!r}")
        return errs
    if PFP_STATUS_RANK[status] > PFP_STATUS_RANK[prior]:
        errs.append(f"node {node_id}: status {status} is above pfp_review.prior_status {prior}")
    if (status != prior) != (review.get("scope_effect") == "status_lowered"):
        errs.append(f"node {node_id}: pfp_review.scope_effect must be status_lowered exactly when the status changed")
    if review.get("scope_effect") == "statement_narrowed" and _text(node, "statement") == review.get("prior_statement"):
        errs.append(f"node {node_id}: pfp_review says statement_narrowed but the statement is the prior statement")
    return errs


def _pfp_review_errors(node: dict[str, object]) -> list[str]:
    if "pfp_review" not in node:
        return []
    node_id = node.get("id")
    review = _mapping(node.get("pfp_review"))
    if review is None:
        return [f"node {node_id}: pfp_review must be an object"]
    errs: list[str] = []
    missing = [key for key in PFP_REVIEW_KEYS if key not in review]
    extra = sorted(set(review) - set(PFP_REVIEW_KEYS) - set(PFP_REVIEW_OPTIONAL_KEYS))
    if missing:
        errs.append(f"node {node_id}: pfp_review is missing {missing}")
    if extra:
        errs.append(f"node {node_id}: pfp_review has unknown keys {extra}")
    if missing:
        return errs
    errs.extend(_pfp_text_errors(node_id, review))
    errs.extend(_pfp_list_errors(node_id, review))
    errs.extend(_pfp_status_errors(node, review))
    return errs


def _validate_node_schema(node: dict[str, object]) -> list[str]:
    errs: list[str] = []
    extra = set(node) - NODE_KEYS
    if extra:
        errs.append(f"node {node.get('id')}: unknown keys {sorted(extra)}")
    errs.extend(_missing_strings(node))
    errs.extend(_bad_lists(node))
    errs.extend(_pfp_review_errors(node))
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
    leaf = symbol_leaf(symbol)
    if leaf not in text:
        return [f"node {node_id}: symbol {symbol} not in {path}"]
    return []


def pfp_review_sha256(data: bytes) -> str:
    """Newline-normalized, so a CRLF checkout of a review file hashes like the committed bytes."""
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def _pfp_file_errors(node: dict[str, object], root: Path) -> list[str]:
    review = _mapping(node.get("pfp_review"))
    if review is None:
        return []
    node_id = node.get("id")
    errs: list[str] = []
    for ref in _string_list(review.get("review_refs")) or []:
        if not _path_exists(root, ref):
            errs.append(f"node {node_id}: pfp_review file missing: {ref}")
    path = review.get("review")
    if isinstance(path, str) and _path_exists(root, path):
        if pfp_review_sha256((root / path).read_bytes()) != review.get("review_sha256"):
            errs.append(f"node {node_id}: pfp_review.review_sha256 does not match {path}")
    return errs


def _node_ref_errors(node: dict[str, object], root: Path) -> list[str]:
    errs: list[str] = _pfp_file_errors(node, root)
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


# ---------------------------------------------------------------------------------------------
# derivation_dag.v2: top-level keys, the index document, the TFQ records and the rendered views.


def _string_rows_errors(where: str, value: object) -> list[str]:
    rows = _string_list(value)
    if rows is None:
        return [f"{where} must be a list of strings"]
    bad = [row for row in rows if row not in STAGES]
    return [f"{where}: unknown stage {row}" for row in bad]


def _index_document_errors(doc: object) -> list[str]:
    mapped = _mapping(doc)
    if mapped is None:
        return ["index_document must be an object"]
    errs: list[str] = []
    if sorted(mapped) != sorted(INDEX_DOCUMENT_KEYS):
        errs.append(f"index_document keys {sorted(mapped)} are not {sorted(INDEX_DOCUMENT_KEYS)}")
    for key in ("header_markdown", "record_count_note"):
        if not isinstance(mapped.get(key), str) or not mapped.get(key):
            errs.append(f"index_document.{key} must be a non-empty string")
    for key in ("stage_index", "application_stages"):
        errs.extend(_string_rows_errors(f"index_document.{key}", mapped.get(key)))
    coda = _mapping(mapped.get("coda_atlas_packages"))
    if coda is None or not isinstance(coda.get("heading"), str) or not isinstance(coda.get("rows"), list):
        errs.append("index_document.coda_atlas_packages must have a heading string and a rows list")
    else:
        for row in _maps(coda.get("rows")):
            if sorted(row) != sorted(CODA_PACKAGE_KEYS) or not all(isinstance(row[k], str) for k in row):
                errs.append(f"index_document.coda_atlas_packages row {row} must have string fields {CODA_PACKAGE_KEYS}")
    for row in _maps(mapped.get("source_corpus_restatements")):
        if not all(isinstance(row.get(k), str) and row.get(k) for k in RESTATEMENT_KEYS):
            errs.append(f"index_document.source_corpus_restatements row {row} must have string fields {RESTATEMENT_KEYS}")
    return errs


def _check_top_level(dag: dict[str, object]) -> list[str]:
    if "schema_version" not in dag and "records" not in dag:
        return []  # a bare node/route graph (unit tests); the packaged file always declares its schema
    errs: list[str] = []
    if dag.get("schema_version") != SCHEMA_VERSION:
        errs.append(f"schema_version {dag.get('schema_version')!r} is not {SCHEMA_VERSION}")
    missing = [key for key in DAG_REQUIRED_KEYS if key not in dag]
    if missing:
        errs.append(f"derivation_dag.json is missing top-level keys {missing}")
    extra = sorted(set(dag) - DAG_KEYS)
    if extra:
        errs.append(f"derivation_dag.json has unknown top-level keys {extra}")
    if "index_document" in dag:
        errs.extend(_index_document_errors(dag.get("index_document")))
    if "records" in dag and not isinstance(dag.get("records"), list):
        errs.append("records must be a list")
    return errs


def _record_schema_errors(record: dict[str, object]) -> list[str]:
    rid = record.get("id")
    errs: list[str] = []
    missing = sorted(RECORD_KEYS - set(record))
    extra = sorted(set(record) - RECORD_KEYS - set(RECORD_OPTIONAL_KEYS))
    if missing:
        errs.append(f"record {rid}: missing keys {missing}")
    if extra:
        errs.append(f"record {rid}: unknown keys {extra}")
    for key in RECORD_STRING_FIELDS:
        if key in record and (not isinstance(record[key], str) or not record[key]):
            errs.append(f"record {rid}: field {key} must be a non-empty string")
    for key in (*RECORD_LIST_FIELDS, *RECORD_OPTIONAL_KEYS):
        if key in record and _string_list(record[key]) is None:
            errs.append(f"record {rid}: field {key} must be a list of strings")
    if "parent_id" in record and record["parent_id"] is not None and not isinstance(record["parent_id"], str):
        errs.append(f"record {rid}: parent_id must be a record id or null")
    if isinstance(rid, str) and RECORD_ID.fullmatch(rid) is None:
        errs.append(f"record {rid}: id is not TFQ-NNNN")
    if isinstance(record.get("stage"), str) and record["stage"] not in STAGES:
        errs.append(f"record {rid}: bad stage {record['stage']}")
    status = record.get("record_status")
    if isinstance(status, str) and RECORD_STATUS.fullmatch(status) is None:
        errs.append(f"record {rid}: record_status {status!r} is not an upper-case label")
    return errs


def _parent_cycle_errors(parent: dict[str, object]) -> list[str]:
    errs: list[str] = []
    done: set[str] = set()
    for start in parent:
        path: list[str] = []
        cur: object = start
        while isinstance(cur, str) and cur in parent and cur not in done:
            if cur in path:
                errs.append(f"record {cur}: parent_id chain is a cycle")
                break
            path.append(cur)
            cur = parent[cur]
        done.update(path)
    return errs


def _check_records(records: list[dict[str, object]], ids: dict[str, dict[str, object]]) -> list[str]:
    errs: list[str] = []
    seen_records: dict[str, dict[str, object]] = {}
    for record in records:
        errs.extend(_record_schema_errors(record))
        rid = _text(record, "id")
        if rid in seen_records:
            errs.append(f"duplicate record id {rid}")
        seen_records[rid] = record
    parent: dict[str, object] = {}
    named: set[str] = set()
    for rid, record in seen_records.items():
        pid = record.get("parent_id")
        parent[rid] = pid
        if pid is not None and (pid not in seen_records or pid == rid):
            errs.append(f"record {rid}: parent_id {pid} is not another record")
        dag_ids = _string_list(record.get("existing_derivation_dag_ids")) or []
        named.update(dag_ids)
        if not any(x in ids for x in dag_ids):
            errs.append(f"record {rid}: names no DAG node in existing_derivation_dag_ids")
    errs.extend(_parent_cycle_errors(parent))
    for node_id in ids:
        if node_id not in named:
            errs.append(f"node {node_id}: named by no record")
    return errs


def _record_paper_errors(records: list[dict[str, object]], root: Path) -> list[str]:
    papers: set[str] = set()
    for path in (root / "dag" / "derivations").rglob("tfq_*.md"):
        match = re.match(r"tfq_(\d{4})_", path.name)
        if match:
            papers.add("TFQ-" + match.group(1))
    return [f"record {_text(r, 'id')}: no derivation paper dag/derivations/*/tfq_{_text(r, 'id')[4:]}_*.md"
            for r in records if _text(r, "id") not in papers]


def view_errors(dag: dict[str, object], views_dir: Path) -> list[str]:
    """The JSONL and Markdown views next to the DAG file must be what the renderer makes of it."""
    try:
        rendered = {
            "theory_of_finite_qm.jsonl": render_dag_views.render_jsonl(dag),
            "theory_of_finite_qm.md": render_dag_views.render_md(dag),
        }
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        return [f"views cannot be rendered from derivation_dag.json: {error!r}"]
    errs: list[str] = []
    for name, text in rendered.items():
        path = views_dir / name
        if not path.is_file() or path.read_bytes() != text.encode("utf-8"):
            errs.append(f"view {name} differs from derivation_dag.json; run dag/render_dag_views.py --write")
    return errs


def check(dag: dict[str, object], root: Path | None, views_dir: Path | None = None) -> list[str]:
    conflicts = proved_lean_record_conflicts(dag)
    nodes = _maps(dag.get("nodes"))
    routes = _maps(dag.get("routes"))
    top_errs = _check_top_level(dag)
    node_errs, ids = _check_nodes(nodes, conflicts)
    route_errs, incoming = _check_routes(routes, ids)
    cyc_errs = _check_acyclicity(routes, ids)
    inc_errs = _check_incoming_routes(ids, incoming)
    records = _maps(dag.get("records"))
    record_errs = _check_records(records, ids) if "records" in dag else []
    forbid_errs = _check_forbidden_words(dag)
    file_errs: list[str] = []
    if root is not None:
        file_errs = _check_file_refs(nodes, routes, root)
        if "records" in dag:
            file_errs += _record_paper_errors(records, root)
    view_errs: list[str] = []
    if views_dir is not None and not top_errs:
        view_errs = view_errors(dag, views_dir)
    return top_errs + node_errs + route_errs + cyc_errs + inc_errs + record_errs + forbid_errs + file_errs + view_errs


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
    records = _maps(dag.get("records"))
    print(f"nodes={len(nodes)} routes={len(routes)} records={len(records)} failures={len(errs)}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--no-files", action="store_true", help="skip path/symbol resolution")
    parser.add_argument("--dag", type=Path, default=DAG)
    parser.add_argument("--no-views", action="store_true", help="skip the JSONL and Markdown view comparison")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        dag = _load_dag(args.dag)
        root = _selected_root(bool(args.no_files), args.repo_root)
    except DagContractError as error:
        print("FAIL", error.detail)
        return 1
    views_dir = None if args.no_views else args.dag.resolve().parent
    errs = check(dag, root, views_dir)
    _print_report(dag, errs)
    if errs:
        return exact_int(1)
    return exact_int(0)


if __name__ == "__main__":
    sys.exit(main())
