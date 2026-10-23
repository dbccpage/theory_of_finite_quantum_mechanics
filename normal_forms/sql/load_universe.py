#!/usr/bin/env python3
"""Load the repository's facts into the relational schema in universe.sql.

Usage (from the repository root):

    python -I -X utf8 normal_forms/sql/load_universe.py            # writes universe.sqlite
    python -I -X utf8 normal_forms/sql/load_universe.py --db other.sqlite
    python -I -X utf8 normal_forms/sql/load_universe.py --check    # in memory, then run the tests

Sources read (nothing is written back to them):

    dag/derivation_dag.json
    dag/evidence/evidence_map.json
    dag/research/*lean_replay*.json
    normal_forms/contracts/PROVENANCE.json and the copied contract YAML files

SQLite is used only as an execution engine for the ANSI DDL.  The loader
turns on PRAGMA foreign_keys and stops at the first key, uniqueness,
check or foreign-key violation; it never skips or repairs a row.

Authority effect: None.  Loading restates existing files as rows and
grants no status to any claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sqlite3
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEMA_SQL = HERE / "universe.sql"
DEFAULT_DB = HERE / "universe.sqlite"
TEST_FILE = HERE / "test_universe.py"


class LoadError(RuntimeError):
    """Raised when a source file cannot be loaded without losing or inventing a fact."""


# --------------------------------------------------------------------------
# connection and schema
# --------------------------------------------------------------------------

def connect(path: str | pathlib.Path = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA foreign_keys = ON")
    if conn.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        raise LoadError("this SQLite build cannot enforce foreign keys")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))


def insert(conn: sqlite3.Connection, table: str, columns: tuple[str, ...], rows) -> int:
    """Insert rows one at a time so a violation names the table and the row."""
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' * len(columns))})"
    count = 0
    for row in rows:
        try:
            conn.execute(sql, row)
        except sqlite3.Error as exc:
            raise LoadError(f"{table}: {exc}; row = {row!r}") from exc
        count += 1
    return count


def insert_list(conn: sqlite3.Connection, table: str, key_col: str, value_col: str, owners) -> int:
    """owners yields (key, list_of_values); one row per element, ordinal from 0."""
    rows = ((key, i, value) for key, values in owners for i, value in enumerate(values))
    return insert(conn, table, (key_col, "ordinal", value_col), rows)


def sha256_of(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --------------------------------------------------------------------------
# derivation_dag.json
# --------------------------------------------------------------------------

def load_dag(conn: sqlite3.Connection, dag: dict) -> None:
    nodes, routes, records = dag["nodes"], dag["routes"], dag["records"]

    insert(conn, "stage", ("stage_name", "stage_ordinal"),
           ((s, i) for i, s in enumerate(dag["stages"])))
    insert(conn, "node_status_code", ("status_code", "meaning"), dag["status_legend"].items())
    insert(conn, "route_status_code", ("status_code",),
           ((s,) for s in sorted({r["status"] for r in routes})))
    insert(conn, "record_status_code", ("status_code",),
           ((s,) for s in sorted({r["record_status"] for r in records})))

    # nodes
    insert(conn, "node", ("node_id",), ((n["id"],) for n in nodes))
    insert(conn, "node_stage", ("node_id", "stage_name"), ((n["id"], n["stage"]) for n in nodes))
    insert(conn, "node_status", ("node_id", "status_code"), ((n["id"], n["status"]) for n in nodes))
    insert(conn, "node_source_status", ("node_id", "source_status_text"),
           ((n["id"], n["source_status"]) for n in nodes))
    insert(conn, "node_statement", ("node_id", "statement_text"),
           ((n["id"], n["statement"]) for n in nodes))
    insert(conn, "node_bottleneck", ("node_id", "bottleneck_text"),
           ((n["id"], n["bottleneck"]) for n in nodes))
    for table, field, column in (
        ("node_source_ref", "source", "source_ref"),
        ("node_lean_ref", "lean", "lean_ref"),
        ("node_rust_ref", "rust", "rust_ref"),
        ("node_python_ref", "python", "python_ref"),
        ("node_imported_structure", "imported_structure", "structure_text"),
        ("node_tag", "tags", "tag_text"),
        ("node_see_also", "see_also", "see_also_node_id"),
    ):
        insert_list(conn, table, "node_id", column, ((n["id"], n.get(field, [])) for n in nodes))

    # pfp_review: file, core, claim, prior, lists, prior route status
    reviews = [(n["id"], n["pfp_review"]) for n in nodes if "pfp_review" in n]
    digests: dict[str, str] = {}
    for _, review in reviews:
        previous = digests.setdefault(review["review"], review["review_sha256"])
        if previous != review["review_sha256"]:
            raise LoadError(f"review file {review['review']} has two digests")
    insert(conn, "pfp_review_file", ("review_path", "review_sha256"), digests.items())
    insert(conn, "pfp_review", ("node_id", "review_path", "verdict", "scope_effect", "reason_text"),
           ((nid, r["review"], r["verdict"], r["scope_effect"], r["reason"]) for nid, r in reviews))
    insert(conn, "pfp_review_claim",
           ("node_id", "narrowest_claim_text", "does_not_support_text", "next_test_text"),
           ((nid, r["narrowest_claim"], r["does_not_support"], r["next_test"]) for nid, r in reviews))
    insert(conn, "pfp_review_prior",
           ("node_id", "prior_status_code", "prior_statement_text", "prior_bottleneck_text"),
           ((nid, r["prior_status"], r["prior_statement"], r["prior_bottleneck"]) for nid, r in reviews))
    insert_list(conn, "pfp_review_ref", "node_id", "review_ref",
                ((nid, r["review_refs"]) for nid, r in reviews))
    insert_list(conn, "pfp_review_superseded_by", "node_id", "superseded_by",
                ((nid, r["superseded_by"]) for nid, r in reviews))

    # routes
    insert(conn, "route", ("route_id",), ((r["id"],) for r in routes))
    insert(conn, "route_status", ("route_id", "status_code"), ((r["id"], r["status"]) for r in routes))
    insert_list(conn, "route_input", "route_id", "node_id", ((r["id"], r["inputs"]) for r in routes))
    insert(conn, "route_output", ("route_id", "output_node_id"), ((r["id"], r["output"]) for r in routes))
    insert_list(conn, "route_source_ref", "route_id", "source_ref",
                ((r["id"], r.get("source", [])) for r in routes))
    insert(conn, "route_mechanism", ("route_id", "mechanism_text"),
           ((r["id"], r["mechanism"]) for r in routes if "mechanism" in r))
    insert(conn, "route_note", ("route_id", "note_text"),
           ((r["id"], r["note"]) for r in routes if "note" in r))

    # prior route statuses are written after routes exist
    insert(conn, "pfp_review_prior_route_status", ("node_id", "route_id", "prior_status_code"),
           ((nid, rid, status) for nid, r in reviews
            for rid, status in r.get("prior_route_status", {}).items()))

    # records
    insert(conn, "record", ("record_id", "record_uuid", "local_id"),
           ((r["id"], r["uuid"], r["local_id"]) for r in records))
    insert(conn, "record_name", ("record_id", "record_name"), ((r["id"], r["name"]) for r in records))
    insert(conn, "record_summary", ("record_id", "summary_text"), ((r["id"], r["summary"]) for r in records))
    insert(conn, "record_obligation", ("record_id", "obligation_text"),
           ((r["id"], r["obligation"]) for r in records))
    insert(conn, "record_stage", ("record_id", "stage_name"), ((r["id"], r["stage"]) for r in records))
    insert(conn, "record_status", ("record_id", "status_code"),
           ((r["id"], r["record_status"]) for r in records))
    insert(conn, "record_source_slice", ("record_id", "source_slice"),
           ((r["id"], r["source_slice"]) for r in records))
    insert(conn, "record_parent", ("record_id", "parent_record_id"),
           ((r["id"], r["parent_id"]) for r in records if r["parent_id"] is not None))
    for table, field, column in (
        ("record_coda_atlas_id", "coda_atlas_ids", "coda_atlas_id"),
        ("record_coda_atlas_path", "coda_atlas_paths", "coda_atlas_path"),
        ("record_dag_id", "existing_derivation_dag_ids", "existing_dag_id"),
        ("record_f004_ref", "f004_refs", "f004_ref"),
        ("record_lean4_ref", "lean4", "lean4_ref"),
        ("record_python_ref", "python", "python_ref"),
        ("record_rust_ref", "rust", "rust_ref"),
        ("record_pfp_review_ref", "pfp_review_refs", "pfp_review_ref"),
    ):
        insert_list(conn, table, "record_id", column, ((r["id"], r.get(field, [])) for r in records))


# --------------------------------------------------------------------------
# evidence_map.json and the lean replay files
# --------------------------------------------------------------------------

RECEIPT_ID = re.compile(r"^(?P<file>.+)#(?P<index>\d+):(?P<module>.+)$")


def replay_module_results(data: dict, rel: str) -> list:
    """Module results that itemise axioms.

    Older receipts nest that list at lean_replay.results.
    campaign_pgw-presentation-not-expressive-lift_lean_replay.json puts the
    same list at the top level. A file with neither shape is an error: its
    declarations are not dropped.
    """
    envelope = data.get("lean_replay")
    if isinstance(envelope, dict) and isinstance(envelope.get("results"), list):
        return envelope["results"]
    if isinstance(data.get("results"), list):
        return data["results"]
    raise LoadError(rel + ": no lean_replay.results and no top-level results list")


def _consistent(store: dict, key, value, what: str) -> None:
    previous = store.setdefault(key, value)
    if previous != value:
        raise LoadError(f"{what} for {key!r} has two values: {previous!r} and {value!r}")


def load_evidence(conn: sqlite3.Connection, em: dict, replay_files: dict[str, dict]) -> None:
    """replay_files maps a repo-relative path to its parsed JSON."""
    grade_codes = list(em["grades"])
    if set(grade_codes) != set(em["grade_rules"]):
        raise LoadError("evidence_map grades and grade_rules disagree")
    insert(conn, "evidence_grade_code", ("grade_code", "rule_text"),
           ((g, em["grade_rules"][g]) for g in grade_codes))
    insert(conn, "evidence_grade", ("node_id", "grade_code"), ((n["id"], n["grade"]) for n in em["nodes"]))
    insert(conn, "evidence_fact", ("node_id", "fact_name", "fact_count"),
           ((n["id"], name, count) for n in em["nodes"] for name, count in n["facts"].items()))
    insert(conn, "evidence_file", ("evidence_path", "sha256", "sha256_basis", "size_bytes"),
           ((path, f["sha256"], f["sha256_basis"], f["size"]) for path, f in em["files"].items()))

    # lean files and declarations, from every lean_decl citation on every node
    resolution: dict[str, str] = {}
    replay: dict[str, str] = {}
    declarations: dict[tuple[str, str], dict] = {}
    for node in em["nodes"]:
        for item in node["items"]:
            if item["kind"] != "lean_decl":
                continue
            path = item["path"]
            _consistent(resolution, path, item["resolution"], "lean_file.resolution")
            _consistent(replay, path, item["replay"], "lean_file_replay.replay_status")
            if item["resolution"] == "present" and not item["file_exists"]:
                raise LoadError(f"{path}: resolution 'present' with file_exists false")
            if item["resolution"] != "present" and item["file_exists"]:
                raise LoadError(f"{path}: resolution {item['resolution']!r} with file_exists true")
            if item["symbol"] is None:
                continue
            record = {
                "symbol_declared": item["symbol_declared"],
                "symbol_exists": item["symbol_exists"],
                "decl_listed": item["decl_listed"],
                "decl_ambiguous": item["decl_ambiguous"],
            }
            _consistent(declarations, (path, item["symbol"]), record, "lean_declaration facts")
    insert(conn, "lean_file", ("lean_path", "resolution"), sorted(resolution.items()))
    insert(conn, "lean_file_replay", ("lean_path", "replay_status"), sorted(replay.items()))
    insert(conn, "lean_declaration", ("lean_path", "symbol"), sorted(declarations))
    scan_rows = []
    for (path, symbol), facts in sorted(declarations.items()):
        declared, exists = facts["symbol_declared"], facts["symbol_exists"]
        if (declared is None) != (exists is None):
            raise LoadError(f"{path}::{symbol}: symbol_declared and symbol_exists are not both null")
        if declared is not None:
            scan_rows.append((path, symbol, declared, exists))
    insert(conn, "lean_declaration_scan", ("lean_path", "symbol", "symbol_declared", "symbol_exists"),
           scan_rows)
    insert(conn, "lean_declaration_listing", ("lean_path", "symbol", "decl_listed", "decl_ambiguous"),
           ((p, s, f["decl_listed"], f["decl_ambiguous"]) for (p, s), f in sorted(declarations.items())))

    # replay receipts: files, modules, per-module results
    receipt_files: dict[str, dict] = {}
    module_paths: dict[str, str] = {}
    module_nodes: dict[str, str] = {}
    for rec in em["receipts"]:
        _consistent(receipt_files, rec["receipt_file"], {
            "receipt_file_sha256": rec["receipt_file_sha256"],
            "checked_at": rec["checked_at"],
            "lean_version": rec["lean_version"],
            "mathlib_source_sha": rec["mathlib_source_sha"],
        }, "replay_receipt")
        _consistent(module_paths, rec["module"], rec["path"], "lean_module.lean_path")
        if rec["dag_node"]:
            _consistent(module_nodes, rec["module"], rec["dag_node"], "lean_module_node.node_id")
    insert(conn, "replay_receipt",
           ("receipt_file", "receipt_file_sha256", "checked_at", "lean_version", "mathlib_source_sha"),
           ((f, v["receipt_file_sha256"], v["checked_at"], v["lean_version"], v["mathlib_source_sha"])
            for f, v in sorted(receipt_files.items())))
    insert(conn, "lean_module", ("lean_module_name", "lean_path"), sorted(module_paths.items()))
    insert(conn, "lean_module_node", ("lean_module_name", "node_id"), sorted(module_nodes.items()))

    module_rows, audit_rows = [], []
    for rec in em["receipts"]:
        match = RECEIPT_ID.match(rec["id"])
        if not match or match["file"] != rec["receipt_file"] or match["module"] != rec["module"]:
            raise LoadError(f"receipt id {rec['id']!r} does not match its file and module")
        module_rows.append((rec["receipt_file"], rec["module"], int(match["index"]),
                            rec["recorded_sha256"], rec["exit_code"], rec["decl_count"]))
        audit_rows.append((rec["receipt_file"], rec["module"], rec["admission_scan_passed"],
                           rec["axiom_audit_passed"], rec["axioms_itemised"], rec["axioms_standard"]))
    insert(conn, "receipt_module",
           ("receipt_file", "lean_module_name", "file_index", "recorded_sha256", "exit_code", "decl_count"),
           module_rows)
    insert(conn, "receipt_module_build", ("receipt_file", "lean_module_name", "built_successfully"),
           ((r["receipt_file"], r["module"], r["built_successfully"])
            for r in em["receipts"] if r["built_successfully"] is not None))
    insert(conn, "receipt_module_source_unchanged",
           ("receipt_file", "lean_module_name", "source_unchanged_during_build"),
           ((r["receipt_file"], r["module"], r["source_unchanged_during_build"])
            for r in em["receipts"] if r["source_unchanged_during_build"] is not None))
    insert(conn, "receipt_module_audit",
           ("receipt_file", "lean_module_name", "admission_scan_passed", "axiom_audit_passed",
            "axioms_itemised", "axioms_standard"), audit_rows)

    # axioms: the allowed set plus anything a replay file actually reports
    allowed = list(em["allowed_axioms"])
    seen = set(allowed)
    declaration_rows, axiom_rows = [], []
    for rel in sorted(replay_files):
        for result in replay_module_results(replay_files[rel], rel):
            module = result.get("module")
            axioms_map = result.get("axioms")
            if not isinstance(module, str) or not isinstance(axioms_map, dict):
                raise LoadError(rel + ": a module result lacks module or axioms")
            for declaration, axioms in axioms_map.items():
                declaration_rows.append((rel, module, declaration))
                for axiom in axioms:
                    seen.add(axiom)
                    axiom_rows.append((rel, module, declaration, axiom))
    insert(conn, "lean_axiom", ("axiom_name",), ((a,) for a in sorted(seen)))
    insert(conn, "lean_axiom_allowed", ("axiom_name",), ((a,) for a in sorted(allowed)))
    insert(conn, "receipt_declaration", ("receipt_file", "lean_module_name", "declaration"), declaration_rows)
    insert(conn, "receipt_axiom", ("receipt_file", "lean_module_name", "declaration", "axiom_name"),
           axiom_rows)


# --------------------------------------------------------------------------
# normal-form contracts
# --------------------------------------------------------------------------

def contract_category(contract: dict, domain_entry: dict | None) -> str:
    quad = (contract.get("definition") or {}).get("quadrilateral") or {}
    if quad.get("qualifies_as_true_normal_form") is True:
        return "true_normal_form"
    if quad.get("qualifies_as_extended_form") is True:
        return "extended_form_contract"
    if domain_entry is not None and domain_entry.get("form_category") == "Extended Form Contract":
        return "extended_form_contract"
    if quad.get("qualifies_as_true_normal_form") is False:
        return "not_true_normal_form"
    return "unstated"


def load_contracts(conn: sqlite3.Connection, contracts_dir: pathlib.Path) -> None:
    provenance = json.loads((contracts_dir / "PROVENANCE.json").read_text(encoding="utf-8"))
    domain = yaml.safe_load((contracts_dir / "nf_domain_index.yaml").read_text(encoding="utf-8"))
    domain_by_id = {c["nf_id"]: c for c in domain["contracts"]}

    contract_rows, status_rows, verification_rows, theory_rows = [], [], [], []
    citation_rows, label_rows, non_claim_owners, source_rows = [], [], [], []
    works: dict[str, tuple] = {}
    for entry in provenance["copied"]:
        if entry["kind"] != "contract":
            continue
        path = contracts_dir / pathlib.PurePosixPath(entry["copied_to"]).name
        if sha256_of(path) != entry["sha256"]:
            raise LoadError(f"{path.name}: bytes differ from the sha256 recorded in PROVENANCE.json")
        contract = yaml.safe_load(path.read_text(encoding="utf-8"))
        ident, purpose = contract["identity"], contract["purpose"]
        nf_id = ident["id"]
        if nf_id != entry["contract_id"]:
            raise LoadError(f"{path.name}: identity.id {nf_id!r} differs from PROVENANCE {entry['contract_id']!r}")
        contract_rows.append((
            nf_id, ident["name"], ident["short_name"], ident["family"],
            contract_category(contract, domain_by_id.get(nf_id)),
            contract["classification"]["hierarchy_level"], entry["index_status"],
            purpose["excludes_anomaly"], purpose["preserves_invariant"]))
        if ident.get("contract_status") is not None:
            status_rows.append((nf_id, ident["contract_status"]))
        if ident.get("verification_status") is not None:
            verification_rows.append((nf_id, ident["verification_status"]))
        if ident.get("theory_status") is not None:
            theory_rows.append((nf_id, ident["theory_status"]))
        citation = (contract.get("definition") or {}).get("citation")
        if citation is not None:
            if set(citation) == {"label"}:
                label_rows.append((nf_id, citation["label"]))
            else:
                authors = citation.get("authors", citation.get("author"))
                if authors is None or "year" not in citation or "work" not in citation:
                    raise LoadError(f"{path.name}: citation has unexpected keys {sorted(citation)}")
                _consistent(works, citation["work"], (authors, citation["year"]), "nf_work")
                citation_rows.append((nf_id, citation["work"]))
        non_claim_owners.append((nf_id, purpose["non_claims"]))
        source_rows.append((nf_id, entry["source_path_relative"], entry["sha256"], entry["size_bytes"]))

    insert(conn, "nf_contract",
           ("nf_id", "name", "short_name", "family", "category", "hierarchy_level", "index_status",
            "excludes_anomaly", "preserves_invariant"), contract_rows)
    insert(conn, "nf_contract_status", ("nf_id", "contract_status"), status_rows)
    insert(conn, "nf_verification_status", ("nf_id", "verification_status"), verification_rows)
    insert(conn, "nf_theory_status", ("nf_id", "theory_status"), theory_rows)
    insert(conn, "nf_work", ("citation_work", "citation_authors", "citation_year"),
           ((work, authors, year) for work, (authors, year) in sorted(works.items())))
    insert(conn, "nf_citation", ("nf_id", "citation_work"), citation_rows)
    insert(conn, "nf_citation_label", ("nf_id", "citation_label"), label_rows)
    insert_list(conn, "nf_non_claim", "nf_id", "non_claim_text", non_claim_owners)
    insert(conn, "nf_source_file", ("nf_id", "source_relative_path", "sha256", "size_bytes"), source_rows)


# --------------------------------------------------------------------------
# top level
# --------------------------------------------------------------------------

def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_sources(repo: pathlib.Path) -> dict:
    replay = {
        f"dag/research/{p.name}": read_json(p)
        for p in sorted((repo / "dag" / "research").glob("*lean_replay*.json"))
    }
    if not replay:
        raise LoadError("no dag/research/*lean_replay*.json files found")
    return {
        "dag": read_json(repo / "dag" / "derivation_dag.json"),
        "evidence_map": read_json(repo / "dag" / "evidence" / "evidence_map.json"),
        "replay_files": replay,
        "contracts_dir": repo / "normal_forms" / "contracts",
    }


def build(db_path: str | pathlib.Path = ":memory:", repo: pathlib.Path = REPO,
          sources: dict | None = None) -> sqlite3.Connection:
    """Create the schema and load every source.  Raises LoadError on any violation."""
    sources = sources or read_sources(repo)
    if str(db_path) != ":memory:" and pathlib.Path(db_path).exists():
        pathlib.Path(db_path).unlink()
    conn = connect(db_path)
    create_schema(conn)
    load_dag(conn, sources["dag"])
    load_evidence(conn, sources["evidence_map"], sources["replay_files"])
    load_contracts(conn, sources["contracts_dir"])
    conn.commit()
    violations = conn.execute("PRAGMA foreign_key_check").fetchall()
    if violations:
        raise LoadError(f"foreign_key_check reported {len(violations)} violations, first: {violations[0]!r}")
    return conn


def table_counts(conn: sqlite3.Connection) -> dict[str, int]:
    names = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    return {n: conn.execute(f"SELECT COUNT(*) FROM {n}").fetchone()[0] for n in names}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite file to (re)create")
    parser.add_argument("--repo-root", default=str(REPO), help="repository root")
    parser.add_argument("--check", action="store_true",
                        help="build in memory, then run test_universe.py with pytest")
    args = parser.parse_args(argv)
    repo = pathlib.Path(args.repo_root).resolve()

    try:
        conn = build(":memory:" if args.check else args.db, repo)
    except LoadError as exc:
        print(f"load_universe: FAILED: {exc}", file=sys.stderr)
        return 1
    counts = table_counts(conn)
    total = sum(counts.values())
    conn.close()
    target = "in memory" if args.check else args.db
    print(f"load_universe: loaded {len(counts)} tables, {total} rows ({target})")
    if not args.check:
        for name, n in counts.items():
            print(f"  {name:36s} {n:7d}")
        return 0

    try:
        import pytest
    except ImportError:
        print("load_universe: --check needs pytest to run test_universe.py", file=sys.stderr)
        return 1
    return int(pytest.main(["-q", "-p", "no:cacheprovider", str(TEST_FILE)]))


if __name__ == "__main__":
    sys.exit(main())
