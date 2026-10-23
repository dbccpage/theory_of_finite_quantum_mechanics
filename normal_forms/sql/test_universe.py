"""Tests for normal_forms/sql/universe.sql and load_universe.py.

Run from the repository root:

    pytest normal_forms/sql/test_universe.py

(a) lossless join   : every node, route, record, review and replay result is rebuilt from the
                      tables and compared with the source JSON, field by field.
(b) keys and counts : integrity, foreign keys, source row counts (read from the sources, never
                      hard-coded) and declared column widths.
(c) normal forms    : candidate keys named in the DDL comments match the constraints, and no
                      attribute is functionally dependent on a proper subset of a composite key.
(d) portability     : the DDL contains no non-ANSI keywords, types or quoting.

Authority effect: None.  These tests check a database layout against files in this repository.
"""

from __future__ import annotations

import collections
import copy
import itertools
import json
import pathlib
import re
import sqlite3

import pytest

import load_universe as lu

REPO = lu.REPO
SQL_TEXT = lu.SCHEMA_SQL.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# fixtures
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def sources():
    return lu.read_sources(REPO)


@pytest.fixture(scope="module")
def db(sources):
    conn = lu.build(":memory:", REPO, sources)
    yield conn
    conn.close()


@pytest.fixture(scope="module")
def dag(sources):
    return sources["dag"]


@pytest.fixture(scope="module")
def em(sources):
    return sources["evidence_map"]


def ordered_lists(conn, table, owner_col, value_col):
    out = collections.defaultdict(list)
    sql = f"SELECT {owner_col}, {value_col} FROM {table} ORDER BY {owner_col}, ordinal"
    for owner, value in conn.execute(sql):
        out[owner].append(value)
    return out


def pairs(conn, sql):
    return {k: v for k, v in conn.execute(sql)}


def user_tables(conn):
    return [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]


# --------------------------------------------------------------------------
# (a) lossless join
# --------------------------------------------------------------------------

def reconstruct_nodes(conn):
    source = ordered_lists(conn, "node_source_ref", "node_id", "source_ref")
    lean = ordered_lists(conn, "node_lean_ref", "node_id", "lean_ref")
    rust = ordered_lists(conn, "node_rust_ref", "node_id", "rust_ref")
    python = ordered_lists(conn, "node_python_ref", "node_id", "python_ref")
    imported = ordered_lists(conn, "node_imported_structure", "node_id", "structure_text")
    tags = ordered_lists(conn, "node_tag", "node_id", "tag_text")
    see_also = ordered_lists(conn, "node_see_also", "node_id", "see_also_node_id")
    reviews = reconstruct_reviews(conn)
    out = {}
    query = ("SELECT node_id, stage_name, status_code, source_status_text, statement_text, bottleneck_text "
             "FROM node_core")
    for nid, stage, status, source_status, statement, bottleneck in conn.execute(query):
        node = {
            "stage": stage, "status": status, "source_status": source_status,
            "statement": statement, "bottleneck": bottleneck,
            "source": source.get(nid, []), "lean": lean.get(nid, []), "rust": rust.get(nid, []),
            "imported_structure": imported.get(nid, []), "tags": tags.get(nid, []),
        }
        if nid in see_also:
            node["see_also"] = see_also[nid]
        if nid in python:
            node["python"] = python[nid]
        if nid in reviews:
            node["pfp_review"] = reviews[nid]
        out[nid] = node
    return out


def reconstruct_reviews(conn):
    refs = ordered_lists(conn, "pfp_review_ref", "node_id", "review_ref")
    superseded = ordered_lists(conn, "pfp_review_superseded_by", "node_id", "superseded_by")
    prior_routes = collections.defaultdict(dict)
    for nid, rid, status in conn.execute(
            "SELECT node_id, route_id, prior_status_code FROM pfp_review_prior_route_status"):
        prior_routes[nid][rid] = status
    query = """
      SELECT node_id, review_path, review_sha256, verdict, scope_effect, reason_text,
             narrowest_claim_text, does_not_support_text, next_test_text,
             prior_status_code, prior_statement_text, prior_bottleneck_text
      FROM pfp_review
      NATURAL JOIN pfp_review_claim
      NATURAL JOIN pfp_review_prior
      NATURAL JOIN pfp_review_file"""
    out = {}
    for (nid, path, sha, verdict, scope, reason, narrowest, dns, next_test,
         prior_status, prior_statement, prior_bottleneck) in conn.execute(query):
        review = {
            "review": path, "review_sha256": sha, "review_refs": refs.get(nid, []),
            "verdict": verdict, "narrowest_claim": narrowest, "does_not_support": dns,
            "next_test": next_test, "scope_effect": scope, "reason": reason,
            "prior_status": prior_status, "prior_statement": prior_statement,
            "prior_bottleneck": prior_bottleneck, "superseded_by": superseded.get(nid, []),
        }
        if nid in prior_routes:
            review["prior_route_status"] = prior_routes[nid]
        out[nid] = review
    return out


def reconstruct_routes(conn):
    inputs = ordered_lists(conn, "route_input", "route_id", "node_id")
    sources = ordered_lists(conn, "route_source_ref", "route_id", "source_ref")
    mechanism = pairs(conn, "SELECT route_id, mechanism_text FROM route_mechanism")
    note = pairs(conn, "SELECT route_id, note_text FROM route_note")
    out = {}
    for rid, status, output in conn.execute("SELECT route_id, status_code, output_node_id FROM route_core"):
        route = {"inputs": inputs.get(rid, []), "output": output, "status": status}
        if rid in sources:
            route["source"] = sources[rid]
        if rid in mechanism:
            route["mechanism"] = mechanism[rid]
        if rid in note:
            route["note"] = note[rid]
        out[rid] = route
    return out


RECORD_LISTS = (
    ("record_coda_atlas_id", "coda_atlas_id", "coda_atlas_ids"),
    ("record_coda_atlas_path", "coda_atlas_path", "coda_atlas_paths"),
    ("record_dag_id", "existing_dag_id", "existing_derivation_dag_ids"),
    ("record_f004_ref", "f004_ref", "f004_refs"),
    ("record_lean4_ref", "lean4_ref", "lean4"),
    ("record_python_ref", "python_ref", "python"),
    ("record_rust_ref", "rust_ref", "rust"),
    ("record_pfp_review_ref", "pfp_review_ref", "pfp_review_refs"),
)
RECORD_OPTIONAL_LISTS = {"pfp_review_refs"}


def reconstruct_records(conn):
    lists = {field: ordered_lists(conn, table, "record_id", column) for table, column, field in RECORD_LISTS}
    parent = pairs(conn, "SELECT record_id, parent_record_id FROM record_parent")
    out = {}
    query = ("SELECT record_id, record_uuid, local_id, record_name, summary_text, obligation_text, "
             "stage_name, status_code, source_slice FROM record_core")
    for rid, uuid, local_id, name, summary, obligation, stage, status, slice_ in conn.execute(query):
        record = {"uuid": uuid, "local_id": local_id, "name": name, "summary": summary,
                  "obligation": obligation, "stage": stage, "record_status": status,
                  "source_slice": slice_, "parent_id": parent.get(rid)}
        for _, _, field in RECORD_LISTS:
            if field in RECORD_OPTIONAL_LISTS and rid not in lists[field]:
                continue
            record[field] = lists[field].get(rid, [])
        out[rid] = record
    return out


def keyed(items, key="id"):
    out = {}
    for item in items:
        if item[key] in out:
            raise AssertionError(f"duplicate {key} {item[key]!r} in source")
        out[item[key]] = {k: v for k, v in item.items() if k != key}
    return out


def test_lossless_nodes(db, dag):
    """Natural join of the node relations returns every node exactly (all 13 source fields)."""
    expected = keyed(dag["nodes"])
    # An explicit empty see_also list and an absent one are both zero rows; report the difference.
    explicit_empty = [nid for nid, n in expected.items() if n.get("see_also") == []]
    for nid in explicit_empty:
        del expected[nid]["see_also"]
    assert reconstruct_nodes(db) == expected
    assert len(explicit_empty) == sum(1 for n in dag["nodes"] if n.get("see_also") == [])


def test_lossless_node_fields_cover_the_source(dag):
    """The decomposition covers every key the source nodes, routes and records use."""
    node_keys = {k for n in dag["nodes"] for k in n}
    route_keys = {k for r in dag["routes"] for k in r}
    record_keys = {k for r in dag["records"] for k in r}
    assert node_keys == {"id", "stage", "status", "source_status", "statement", "source", "lean", "rust",
                         "imported_structure", "bottleneck", "tags", "pfp_review", "see_also"}
    assert route_keys == {"id", "inputs", "output", "status", "source", "mechanism", "note"}
    assert record_keys == {"id", "uuid", "local_id", "name", "summary", "obligation", "stage",
                           "record_status", "source_slice", "parent_id", "coda_atlas_ids",
                           "coda_atlas_paths", "existing_derivation_dag_ids", "f004_refs", "lean4",
                           "python", "rust", "pfp_review_refs"}
    review_keys = {k for n in dag["nodes"] if "pfp_review" in n for k in n["pfp_review"]}
    assert review_keys == {"review", "review_sha256", "review_refs", "verdict", "narrowest_claim",
                           "does_not_support", "next_test", "scope_effect", "reason", "prior_status",
                           "prior_statement", "prior_bottleneck", "superseded_by", "prior_route_status"}


def test_lossless_routes(db, dag):
    """Same join for routes.  An empty source list and an absent one are both zero rows."""
    expected = keyed(dag["routes"])
    for route in expected.values():
        if route.get("source") == []:
            del route["source"]
    assert reconstruct_routes(db) == expected


def test_lossless_records(db, dag):
    assert reconstruct_records(db) == keyed(dag["records"])


def test_lossless_vocabularies(db, dag):
    stages = [r[0] for r in db.execute("SELECT stage_name FROM stage ORDER BY stage_ordinal")]
    assert stages == dag["stages"]
    assert pairs(db, "SELECT status_code, meaning FROM node_status_code") == dag["status_legend"]
    assert {r[0] for r in db.execute("SELECT status_code FROM route_status_code")} == \
        {r["status"] for r in dag["routes"]}
    assert {r[0] for r in db.execute("SELECT status_code FROM record_status_code")} == \
        {r["record_status"] for r in dag["records"]}


def test_lossless_evidence_grades(db, em):
    assert pairs(db, "SELECT node_id, grade_code FROM evidence_grade") == {n["id"]: n["grade"] for n in em["nodes"]}
    facts = collections.defaultdict(dict)
    for nid, name, count in db.execute("SELECT node_id, fact_name, fact_count FROM evidence_fact"):
        facts[nid][name] = count
    assert dict(facts) == {n["id"]: n["facts"] for n in em["nodes"]}
    assert pairs(db, "SELECT grade_code, rule_text FROM evidence_grade_code") == em["grade_rules"]
    files = {p: {"sha256": s, "sha256_basis": b, "size": z}
             for p, s, b, z in db.execute("SELECT evidence_path, sha256, sha256_basis, size_bytes FROM evidence_file")}
    assert files == em["files"]


def test_lossless_lean_declarations(db, em):
    expected_files, expected_decls = {}, {}
    for node in em["nodes"]:
        for item in node["items"]:
            if item["kind"] != "lean_decl":
                continue
            expected_files[item["path"]] = (item["resolution"], item["replay"])
            if item["symbol"] is not None:
                expected_decls[(item["path"], item["symbol"])] = (
                    item["symbol_declared"], item["symbol_exists"], item["decl_listed"], item["decl_ambiguous"])
    actual_files = {p: (r, s) for p, r, s in db.execute(
        "SELECT lean_path, resolution, replay_status FROM lean_file NATURAL JOIN lean_file_replay")}
    assert actual_files == expected_files
    # scan facts are optional rows: null in the source means no row.
    scan = {(p, s): (d, e) for p, s, d, e in db.execute(
        "SELECT lean_path, symbol, symbol_declared, symbol_exists FROM lean_declaration_scan")}
    listing = {(p, s): (l, a) for p, s, l, a in db.execute(
        "SELECT lean_path, symbol, decl_listed, decl_ambiguous FROM lean_declaration_listing")}
    actual = {}
    for key in listing:
        declared, exists = scan.get(key, (None, None))
        actual[key] = (None if declared is None else bool(declared), None if exists is None else bool(exists),
                       bool(listing[key][0]), bool(listing[key][1]))
    assert actual == expected_decls
    # an in-repo file means the file exists; the dropped file_exists column is recoverable
    for node in em["nodes"]:
        for item in node["items"]:
            if item["kind"] == "lean_decl":
                assert item["file_exists"] == (item["resolution"] == "present")


def test_lossless_receipts_and_axioms(db, em, sources):
    expected = {}
    for rec in em["receipts"]:
        match = lu.RECEIPT_ID.match(rec["id"])
        expected[(rec["receipt_file"], rec["module"])] = rec
        assert match["file"] == rec["receipt_file"] and match["module"] == rec["module"]
    query = """
      SELECT receipt_file, lean_module_name, file_index, recorded_sha256, exit_code, decl_count, lean_path,
             admission_scan_passed, axiom_audit_passed, axioms_itemised, axioms_standard,
             receipt_file_sha256, checked_at, lean_version, mathlib_source_sha
      FROM receipt_module
      NATURAL JOIN receipt_module_audit
      NATURAL JOIN lean_module
      NATURAL JOIN replay_receipt"""
    seen = set()
    build = {(f, m): bool(b) for f, m, b in db.execute(
        "SELECT receipt_file, lean_module_name, built_successfully FROM receipt_module_build")}
    unchanged = {(f, m): bool(v) for f, m, v in db.execute(
        "SELECT receipt_file, lean_module_name, source_unchanged_during_build FROM receipt_module_source_unchanged")}
    for (rfile, module, index, rsha, exit_code, decl_count, path, b, c, d, e,
         file_sha, checked_at, lean_version, mathlib) in db.execute(query):
        rec = expected[(rfile, module)]
        seen.add((rfile, module))
        assert rec["id"] == f"{rfile}#{index}:{module}"
        assert (rec["recorded_sha256"], rec["exit_code"], rec["decl_count"], rec["path"]) == \
            (rsha, exit_code, decl_count, path)
        assert unchanged.get((rfile, module)) == rec["source_unchanged_during_build"]
        assert (rec["admission_scan_passed"], rec["axiom_audit_passed"],
                rec["axioms_itemised"], rec["axioms_standard"]) == (bool(b), bool(c), bool(d), bool(e))
        assert (rec["receipt_file_sha256"], rec["checked_at"], rec["lean_version"], rec["mathlib_source_sha"]) == \
            (file_sha, checked_at, lean_version, mathlib)
        # toolchain is the numeric part of lean_version and is not stored; built_successfully is
        # recorded for some receipts only, so it has its own optional-row table
        assert rec["toolchain"] in rec["lean_version"]
        assert build.get((rfile, module)) == rec["built_successfully"]
        if rec["built_successfully"] is not None:
            assert rec["built_successfully"] == (exit_code == 0)
    assert seen == set(expected)
    nodes = pairs(db, "SELECT lean_module_name, node_id FROM lean_module_node")
    for rec in em["receipts"]:
        assert nodes.get(rec["module"]) == (rec["dag_node"] or None)

    # declaration x axiom, rebuilt per module result and compared with the replay files
    axioms = collections.defaultdict(lambda: collections.defaultdict(set))
    declared = collections.defaultdict(set)
    for rfile, module, decl in db.execute("SELECT receipt_file, lean_module_name, declaration FROM receipt_declaration"):
        declared[(rfile, module)].add(decl)
    for rfile, module, decl, axiom in db.execute(
            "SELECT receipt_file, lean_module_name, declaration, axiom_name FROM receipt_axiom"):
        axioms[(rfile, module)][decl].add(axiom)
    for rel, data in sources["replay_files"].items():
        for result in lu.replay_module_results(data, rel):
            key = (rel, result["module"])
            assert declared[key] == set(result["axioms"])
            assert {d: set(a) for d, a in axioms[key].items()} == \
                {d: set(a) for d, a in result["axioms"].items() if a}
            rec = expected[key]
            if rec["axioms_itemised"]:
                assert rec["decl_count"] == len(result["axioms"])
                assert set(rec["axioms_union"]) == {a for s in axioms[key].values() for a in s}
    allowed = {r[0] for r in db.execute("SELECT axiom_name FROM lean_axiom_allowed")}
    assert allowed == set(em["allowed_axioms"])


def test_lossless_contracts(db):
    """Contract rows rebuild the fields they were taken from, read straight from the copied YAML."""
    import yaml
    contracts = REPO / "normal_forms" / "contracts"
    provenance = json.loads((contracts / "PROVENANCE.json").read_text(encoding="utf-8"))
    works = {w: (a, y) for w, a, y in db.execute(
        "SELECT citation_work, citation_authors, citation_year FROM nf_work")}
    cited = pairs(db, "SELECT nf_id, citation_work FROM nf_citation")
    labels = pairs(db, "SELECT nf_id, citation_label FROM nf_citation_label")
    claims = ordered_lists(db, "nf_non_claim", "nf_id", "non_claim_text")
    statuses = pairs(db, "SELECT nf_id, contract_status FROM nf_contract_status")
    verification = pairs(db, "SELECT nf_id, verification_status FROM nf_verification_status")
    theory = pairs(db, "SELECT nf_id, theory_status FROM nf_theory_status")
    rows = {r[0]: r for r in db.execute(
        "SELECT nf_id, name, short_name, family, hierarchy_level, excludes_anomaly, preserves_invariant "
        "FROM nf_contract")}
    for entry in provenance["copied"]:
        if entry["kind"] != "contract":
            continue
        doc = yaml.safe_load((contracts / pathlib.PurePosixPath(entry["copied_to"]).name).read_text(encoding="utf-8"))
        ident, purpose = doc["identity"], doc["purpose"]
        nf_id = ident["id"]
        assert rows[nf_id][1:] == (ident["name"], ident["short_name"], ident["family"],
                                   doc["classification"]["hierarchy_level"],
                                   purpose["excludes_anomaly"], purpose["preserves_invariant"])
        assert claims.get(nf_id, []) == purpose["non_claims"]
        assert statuses.get(nf_id) == ident.get("contract_status")
        assert verification.get(nf_id) == ident.get("verification_status")
        assert theory.get(nf_id) == ident.get("theory_status")
        citation = (doc.get("definition") or {}).get("citation")
        if citation is None:
            assert nf_id not in cited and nf_id not in labels
        elif set(citation) == {"label"}:
            assert labels[nf_id] == citation["label"] and nf_id not in cited
        else:
            assert works[cited[nf_id]] == (citation.get("authors", citation.get("author")), citation["year"])
            assert cited[nf_id] == citation["work"]


def test_node_python_table_matches_source(db, dag):
    """No node carries a python key today, so the table is empty; it must track the source if that changes."""
    expected = sum(len(n.get("python", [])) for n in dag["nodes"])
    assert db.execute("SELECT COUNT(*) FROM node_python_ref").fetchone()[0] == expected


# --------------------------------------------------------------------------
# (b) keys, foreign keys, counts, widths
# --------------------------------------------------------------------------

def count(conn, table):
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def test_foreign_keys_are_enforced_and_hold(db):
    assert db.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    assert db.execute("PRAGMA foreign_key_check").fetchall() == []
    assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"


def test_constraints_reject_bad_rows(db):
    """The constraints bite: a duplicate key, a dangling reference and a bad value all fail loudly."""
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO stage VALUES ('PREGENESIS', 99)")
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO node_stage VALUES ('NO-SUCH-NODE', 'PREGENESIS')")
    with pytest.raises(sqlite3.IntegrityError):
        node = db.execute("SELECT node_id FROM node").fetchone()[0]
        db.execute("INSERT INTO node_status VALUES (?, 'NOT_A_STATUS')", (node,))
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO evidence_file VALUES ('x', 'y', 'rot13', 1)")
    db.rollback()


def test_row_counts_equal_source_counts(db, dag, em):
    nodes, routes, records = dag["nodes"], dag["routes"], dag["records"]
    assert count(db, "node") == len(nodes)
    for table in ("node_stage", "node_status", "node_source_status", "node_statement", "node_bottleneck"):
        assert count(db, table) == len(nodes), table
    list_fields = {"node_source_ref": "source", "node_lean_ref": "lean", "node_rust_ref": "rust",
                   "node_python_ref": "python", "node_imported_structure": "imported_structure",
                   "node_tag": "tags", "node_see_also": "see_also"}
    for table, field in list_fields.items():
        assert count(db, table) == sum(len(n.get(field, [])) for n in nodes), table

    assert count(db, "route") == len(routes)
    for table in ("route_status", "route_output"):
        assert count(db, table) == len(routes), table
    assert count(db, "route_input") == sum(len(r["inputs"]) for r in routes)
    assert count(db, "route_source_ref") == sum(len(r.get("source", [])) for r in routes)
    assert count(db, "route_mechanism") == sum("mechanism" in r for r in routes)
    assert count(db, "route_note") == sum("note" in r for r in routes)

    assert count(db, "record") == len(records)
    for table in ("record_name", "record_summary", "record_obligation", "record_stage", "record_status",
                  "record_source_slice"):
        assert count(db, table) == len(records), table
    assert count(db, "record_parent") == sum(r["parent_id"] is not None for r in records)
    for table, _, field in RECORD_LISTS:
        assert count(db, table) == sum(len(r.get(field, [])) for r in records), table

    reviews = [n["pfp_review"] for n in nodes if "pfp_review" in n]
    assert count(db, "pfp_review") == len(reviews)
    assert count(db, "pfp_review_file") == len({r["review"] for r in reviews})
    assert count(db, "pfp_review_ref") == sum(len(r["review_refs"]) for r in reviews)
    assert count(db, "pfp_review_superseded_by") == sum(len(r["superseded_by"]) for r in reviews)
    assert count(db, "pfp_review_prior_route_status") == sum(len(r.get("prior_route_status", {})) for r in reviews)

    assert count(db, "evidence_grade") == len(em["nodes"]) == len(nodes)
    assert count(db, "evidence_fact") == sum(len(n["facts"]) for n in em["nodes"])
    assert count(db, "evidence_file") == len(em["files"])
    assert count(db, "receipt_module") == len(em["receipts"])
    assert count(db, "receipt_module_audit") == len(em["receipts"])
    assert count(db, "receipt_module_build") == sum(r["built_successfully"] is not None for r in em["receipts"])
    assert count(db, "receipt_module_source_unchanged") == sum(
        r["source_unchanged_during_build"] is not None for r in em["receipts"])
    assert count(db, "replay_receipt") == len({r["receipt_file"] for r in em["receipts"]})
    assert count(db, "lean_module") == len({r["module"] for r in em["receipts"]})


def test_receipt_axiom_rows_equal_declaration_axiom_pairs(db, sources):
    pairs_in_files = 0
    declarations = 0
    for rel, data in sources["replay_files"].items():
        for res in lu.replay_module_results(data, rel):
            declarations += len(res["axioms"])
            pairs_in_files += sum(len(a) for a in res["axioms"].values())
    assert count(db, "receipt_axiom") == pairs_in_files
    assert count(db, "receipt_declaration") == declarations
    # one row per declaration x axiom: no declaration lists an axiom twice
    assert db.execute("""SELECT COUNT(*) FROM (
        SELECT receipt_file, lean_module_name, declaration, axiom_name
        FROM receipt_axiom GROUP BY 1, 2, 3, 4 HAVING COUNT(*) > 1) AS d""").fetchone()[0] == 0


def test_node_count_matches_documented_headline_counts(db, dag):
    """Guard against the loader silently dropping rows: counts come from the file itself."""
    assert count(db, "node") == len(dag["nodes"]) > 0
    assert count(db, "route") == len(dag["routes"]) > 0
    assert count(db, "record") == len(dag["records"]) > 0


def test_contract_counts_and_bytes(db):
    contracts = REPO / "normal_forms" / "contracts"
    provenance = json.loads((contracts / "PROVENANCE.json").read_text(encoding="utf-8"))
    for entry in provenance["copied"]:
        path = contracts / pathlib.PurePosixPath(entry["copied_to"]).name
        assert lu.sha256_of(path) == entry["sha256"], path.name
        assert path.stat().st_size == entry["size_bytes"], path.name
    kinds = collections.Counter((e["kind"], e["index_status"]) for e in provenance["copied"])
    assert count(db, "nf_contract") == sum(n for (k, _), n in kinds.items() if k == "contract")
    assert db.execute("SELECT COUNT(*) FROM nf_contract WHERE index_status = 'active'").fetchone()[0] == \
        kinds[("contract", "active")]
    # every id the copied index.yaml calls active is loaded
    import yaml
    index = yaml.safe_load((contracts / "index.yaml").read_text(encoding="utf-8"))["contracts"]
    loaded = {r[0] for r in db.execute("SELECT nf_id FROM nf_contract")}
    assert set(index["active"]) <= loaded
    assert provenance["index_ids_without_a_file_found"] == []


def declared_widths(conn):
    widths = []
    for table in user_tables(conn):
        for _, col, ctype, *_ in conn.execute(f"PRAGMA table_info({table})"):
            m = re.fullmatch(r"CHARACTER VARYING\((\d+)\)", ctype)
            if m:
                widths.append((table, col, int(m.group(1))))
    return widths


def test_loaded_values_fit_declared_widths(db):
    """SQLite ignores CHARACTER VARYING(n); this check stands in for a database that enforces it."""
    assert declared_widths(db)
    for table, col, width in declared_widths(db):
        longest = db.execute(f"SELECT MAX(LENGTH({col})) FROM {table}").fetchone()[0] or 0
        assert longest <= width, f"{table}.{col}: longest value {longest} exceeds declared width {width}"


def test_loader_fails_loudly(sources):
    """A key or foreign-key violation in a source raises LoadError instead of being skipped."""
    bad = copy.deepcopy(sources["dag"])
    bad["nodes"][0]["stage"] = "NOT_A_STAGE"
    with pytest.raises(lu.LoadError, match="node_stage"):
        lu.build(":memory:", REPO, {**sources, "dag": bad})

    dup = copy.deepcopy(sources["dag"])
    dup["nodes"].append(copy.deepcopy(dup["nodes"][0]))
    with pytest.raises(lu.LoadError, match="node"):
        lu.build(":memory:", REPO, {**sources, "dag": dup})

    dangling = copy.deepcopy(sources["dag"])
    dangling["routes"][0]["inputs"].append("NO-SUCH-NODE")
    with pytest.raises(lu.LoadError, match="route_input"):
        lu.build(":memory:", REPO, {**sources, "dag": dangling})


# --------------------------------------------------------------------------
# (c) normal-form sanity
# --------------------------------------------------------------------------

COMMENT_BLOCK = re.compile(r"((?:^--[^\n]*\n)+)CREATE TABLE (\w+) \(", re.MULTILINE)


def declared_table_comments():
    out = {}
    for block, table in COMMENT_BLOCK.findall(SQL_TEXT):
        m_nf = re.search(r"Normal form\s*:\s*(.+)", block)
        m_keys = re.search(r"Candidate keys:\s*(.+)", block)
        out[table] = (m_nf.group(1).strip() if m_nf else None, m_keys.group(1).strip() if m_keys else None)
    return out


def parse_candidate_keys(text):
    return {frozenset(c.strip() for c in group.split(",")) for group in re.findall(r"\(([^)]*)\)", text)}


def actual_unique_keys(conn, table):
    keys = set()
    for _, name, unique, origin, _ in conn.execute(f"PRAGMA index_list({table})"):
        if unique and origin in ("pk", "u"):
            keys.add(frozenset(r[2] for r in conn.execute(f"PRAGMA index_info({name})")))
    return keys


def primary_key(conn, table):
    cols = sorted(((pk, name) for _, name, _, _, _, pk in conn.execute(f"PRAGMA table_info({table})") if pk))
    return [name for _, name in cols]


def test_every_table_documents_its_normal_form_and_keys(db):
    comments = declared_table_comments()
    assert set(comments) == set(user_tables(db))
    for table, (normal_form, keys) in comments.items():
        assert normal_form and re.match(r"(BCNF|6NF-style)", normal_form), f"{table}: normal form comment"
        assert keys, f"{table}: candidate keys comment"


def test_declared_candidate_keys_match_the_constraints(db):
    for table, (_, keys) in declared_table_comments().items():
        assert parse_candidate_keys(keys) == actual_unique_keys(db, table), table


def test_tables_have_primary_keys_and_no_nullable_columns(db):
    """Optional facts are optional rows, so every column is NOT NULL."""
    for table in user_tables(db):
        assert primary_key(db, table), f"{table} has no primary key"
        for _, col, _, notnull, _, pk in db.execute(f"PRAGMA table_info({table})"):
            assert notnull or pk, f"{table}.{col} is nullable"


def nonkey_columns(conn, table):
    key = set(primary_key(conn, table))
    return [name for _, name, *_ in conn.execute(f"PRAGMA table_info({table})") if name not in key]


def holds_on_data(conn, table, determinant, dependent):
    """True when determinant -> dependent holds on the data and the test is not vacuous.

    Not vacuous means the dependent column is not constant and some determinant value occurs in at
    least two rows, so that agreement is evidence.
    """
    det = ", ".join(determinant)
    if conn.execute(f"SELECT COUNT(DISTINCT {dependent}) FROM {table}").fetchone()[0] < 2:
        return False  # a constant column depends on everything; that says nothing about the design
    exercised = conn.execute(
        f"SELECT COUNT(*) FROM (SELECT {det} FROM {table} GROUP BY {det} HAVING COUNT(*) > 1) AS g").fetchone()[0]
    if not exercised:
        return False
    broken = conn.execute(
        f"SELECT COUNT(*) FROM (SELECT {det} FROM {table} GROUP BY {det} "
        f"HAVING COUNT(DISTINCT {dependent}) > 1) AS g").fetchone()[0]
    return broken == 0


# A partial dependency found here would mean a table is not in 2NF on the loaded data.  The entries
# below are agreements in the current data that the design does not rely on: each fact is a fact of
# the whole key, and the repeated component happens to carry the same value wherever it recurs.
_SYMBOL_NOTE = ("the same symbol name recurs under several paths and its scan/listing facts agree "
                "there; the facts belong to the (lean_path, symbol) pair, and a path where they "
                "differed would be legal")
_MODULE_NOTE = ("the same module is replayed in several receipt files with an unchanged source, so "
                "its recorded digest and declaration count agree; both are facts of one replay, and "
                "a replay of an edited module would differ")
PARTIAL_DEPENDENCY_COINCIDENCES: dict[tuple[str, tuple[str, ...], str], str] = {
    ("lean_declaration_listing", ("symbol",), "decl_listed"): _SYMBOL_NOTE,
    ("lean_declaration_scan", ("symbol",), "symbol_declared"): _SYMBOL_NOTE,
    ("lean_declaration_scan", ("symbol",), "symbol_exists"): _SYMBOL_NOTE,
    ("receipt_module", ("lean_module_name",), "recorded_sha256"): _MODULE_NOTE,
    ("receipt_module", ("lean_module_name",), "decl_count"): _MODULE_NOTE,
}


def test_no_attribute_depends_on_a_proper_subset_of_a_composite_key(db):
    findings = []
    for table in user_tables(db):
        key = primary_key(db, table)
        if len(key) < 2:
            continue
        for size in range(1, len(key)):
            for subset in itertools.combinations(key, size):
                for attr in nonkey_columns(db, table):
                    if holds_on_data(db, table, subset, attr):
                        findings.append((table, subset, attr))
    unexplained = [f for f in findings if f not in PARTIAL_DEPENDENCY_COINCIDENCES]
    assert unexplained == [], f"partial dependencies on the loaded data: {unexplained}"


def test_ordered_list_tables_are_keyed_by_owner_and_ordinal(db):
    """Every *_ref/_tag list table has the same shape, so the value depends on the whole key."""
    for table in user_tables(db):
        cols = [r[1] for r in db.execute(f"PRAGMA table_info({table})")]
        if "ordinal" in cols:
            assert primary_key(db, table)[-1] == "ordinal", table
            assert len(cols) == 3, table


def test_no_undeclared_functional_dependency_among_low_cardinality_attributes(db):
    """Probe pairs of non-key attributes of single-key tables for a non-key determinant.

    A hit would suggest a transitive dependency (not BCNF).  Only determinants that repeat in the data
    are tested, and the table must have a free-text-free pair, so unique text columns cannot trigger it.
    """
    findings = []
    for table in user_tables(db):
        key = primary_key(db, table)
        if len(key) != 1:
            continue
        attrs = [(name, ctype) for _, name, ctype, *_ in db.execute(f"PRAGMA table_info({table})")
                 if name not in key]
        for (a, a_type), (b, _) in itertools.permutations(attrs, 2):
            width = re.fullmatch(r"CHARACTER VARYING\((\d+)\)", a_type)
            if width and int(width.group(1)) >= 1024:
                continue  # prose columns: agreement would be an accident of uniqueness
            if holds_on_data(db, table, (a,), b):
                findings.append((table, a, b))
    assert findings == [] or all(f in ACKNOWLEDGED_NONKEY_DEPENDENCIES for f in findings), findings


# A determinant that repeats and always agrees on the dependent in the current data.  Each is a coincidence
# of a small table, and the reason is recorded; none is a design dependency.
ACKNOWLEDGED_NONKEY_DEPENDENCIES: dict[tuple[str, str, str], str] = {
    ("replay_receipt", "checked_at", "lean_version"):
        "receipts that share a checked_at date in this checkout also share one Lean version string; "
        "the version is a fact of the receipt file, and a second toolchain on that date would be a different value",
}


# --------------------------------------------------------------------------
# (d) DDL portability
# --------------------------------------------------------------------------

def strip_comments(sql):
    return "\n".join(line.split("--", 1)[0] for line in sql.splitlines())


DENYLIST = {
    "AUTOINCREMENT": r"\bAUTOINCREMENT\b",
    "AUTO_INCREMENT": r"\bAUTO_INCREMENT\b",
    "TEXT as a type": r"\bTEXT\b",
    "IF NOT EXISTS": r"\bIF\s+NOT\s+EXISTS\b",
    "IF EXISTS": r"\bIF\s+EXISTS\b",
    "backtick quoting": r"`",
    "square-bracket quoting": r"\[[A-Za-z_]",
    "double-quoted identifier": r'"',
    "LIMIT": r"\bLIMIT\b",
    "OFFSET": r"\bOFFSET\b",
    "PRAGMA": r"\bPRAGMA\b",
    "WITHOUT ROWID": r"\bWITHOUT\s+ROWID\b",
    "STRICT tables": r"\)\s*STRICT\b",
    "ROWID": r"\bROWID\b",
    "SERIAL": r"\b(BIG|SMALL)?SERIAL\b",
    "VARCHAR": r"\bVARCHAR2?\b",
    "NVARCHAR": r"\bNVARCHAR\b",
    "UNSIGNED": r"\bUNSIGNED\b",
    "BLOB": r"\bBLOB\b",
    "JSON/JSONB": r"\bJSONB?\b",
    "ENGINE=": r"\bENGINE\s*=",
    "ON CONFLICT": r"\bON\s+CONFLICT\b",
    "INSERT OR": r"\bINSERT\s+OR\b",
    "REPLACE INTO": r"\bREPLACE\s+INTO\b",
    "ILIKE": r"\bILIKE\b",
    "GLOB": r"\bGLOB\b",
    "Postgres cast ::": r"::",
    "NUMBER": r"\bNUMBER\b",
    "DATETIME": r"\bDATETIME\b",
    "TINYINT": r"\bTINYINT\b",
    "MEDIUMTEXT/LONGTEXT": r"\b(MEDIUM|LONG)TEXT\b",
    "COLLATE": r"\bCOLLATE\b",
    "GENERATED ALWAYS": r"\bGENERATED\s+ALWAYS\b",
    "TEMP/TEMPORARY": r"\bTEMP(ORARY)?\b",
    "VIRTUAL": r"\bVIRTUAL\b",
    "UNLOGGED": r"\bUNLOGGED\b",
}

# SQL:2016 reserved words that would be a poor identifier in a portable schema.  Not exhaustive.
RESERVED = {
    "ALL", "AND", "ANY", "AS", "AT", "AVG", "BETWEEN", "BY", "CASE", "CAST", "CHAR", "COUNT", "CREATE",
    "CURRENT", "DATE", "DAY", "DEC", "DEFAULT", "DELETE", "DISTINCT", "DROP", "ELSE", "END", "EXISTS",
    "FALSE", "FROM", "GROUP", "HAVING", "IN", "INSERT", "INT", "INTEGER", "INTERVAL", "INTO", "IS", "JOIN",
    "LANGUAGE", "LEFT", "LIKE", "LOWER", "MAX", "MIN", "MOD", "MODULE", "MONTH", "NATURAL", "NO", "NOT",
    "NULL", "NUMERIC", "OF", "ON", "OR", "ORDER", "OUTER", "POSITION", "PRIMARY", "REAL", "REFERENCES",
    "RIGHT", "ROW", "ROWS", "SELECT", "SET", "SOME", "SUM", "TABLE", "THEN", "TIME", "TIMESTAMP", "TO",
    "TRUE", "UNION", "UNIQUE", "UPDATE", "UPPER", "USER", "USING", "VALUE", "VALUES", "WHEN", "WHERE",
    "WITH", "YEAR", "ZONE",
}

ALLOWED_TYPES = re.compile(r"(CHARACTER VARYING\(\d+\)|INTEGER|BOOLEAN|DATE)")


def test_ddl_has_no_non_ansi_keywords():
    code = strip_comments(SQL_TEXT)
    hits = {name: pattern for name, pattern in DENYLIST.items() if re.search(pattern, code, re.IGNORECASE)}
    assert hits == {}, f"non-ANSI constructs in universe.sql: {sorted(hits)}"


def test_ddl_statements_are_only_create_table_and_create_view():
    code = strip_comments(SQL_TEXT)
    statements = [s.strip() for s in code.split(";") if s.strip()]
    assert statements
    for statement in statements:
        assert re.match(r"CREATE (TABLE|VIEW) \w+", statement), statement[:60]


def test_only_portable_column_types(db):
    for table in user_tables(db):
        for _, col, ctype, *_ in db.execute(f"PRAGMA table_info({table})"):
            assert ALLOWED_TYPES.fullmatch(ctype), f"{table}.{col}: type {ctype!r}"


def test_identifiers_are_not_reserved_words(db):
    for table in user_tables(db):
        assert table.upper() not in RESERVED, table
        for _, col, *_ in db.execute(f"PRAGMA table_info({table})"):
            assert col.upper() not in RESERVED, f"{table}.{col}"
    for (view,) in db.execute("SELECT name FROM sqlite_master WHERE type = 'view'"):
        assert view.upper() not in RESERVED, view


def test_constraints_are_named_and_identifiers_are_short_snake_case(db):
    for table in user_tables(db):
        assert re.fullmatch(r"[a-z][a-z0-9_]*", table) and len(table) <= 40, table
    names = re.findall(r"CONSTRAINT (\w+)", SQL_TEXT)
    assert len(names) == len(set(names)), "constraint names must be unique"
    assert all(len(n) <= 63 for n in names)


def test_ddl_loads_into_a_fresh_database_twice():
    """Idempotence of the build itself: a second build in a new connection gives the same tables."""
    first, second = lu.connect(), lu.connect()
    lu.create_schema(first)
    lu.create_schema(second)
    assert user_tables(first) == user_tables(second)
    first.close()
    second.close()


# --------------------------------------------------------------------------
# README examples run
# --------------------------------------------------------------------------

def test_readme_example_queries_run(db):
    readme = (lu.HERE / "README.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```sql\n(.*?)```", readme, re.DOTALL)
    assert len(blocks) >= 5, "README.md must show at least five example queries"
    for block in blocks:
        assert not re.search(r"\b(LIMIT|PRAGMA|AUTOINCREMENT)\b", block, re.IGNORECASE)
        rows = db.execute(block).fetchall()
        assert rows, f"example query returned no rows:\n{block}"
