"""
test_sign_sql.py — Integration Tests for SQL Relational Schemas and Sign Audits
Status: Integration Test Suite
AuthorityEffect: None

Pins and validates:
1. Exact execution of sign_sql walk database (cancellation ratio 1/15 in presentation A, non-negativity in presentation B).
2. Compilation and schema instantiation of databases/fermion_gin_index_schema.sql in SQLite.
3. Verification of SQL CTE views:
   - ViewFspInvolutionSignCancellationAudit
   - ViewAverageSignRecoveryAudit
   - ViewMajoranaZeroModeAudit
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
import pytest

# Add paths
current_dir = Path(__file__).resolve().parent
code_dir = current_dir.parent.parent
sign_sql_dir = code_dir / "sign_sql"
databases_dir = code_dir.parent / "databases"

if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))
if str(sign_sql_dir) not in sys.path:
    sys.path.insert(0, str(sign_sql_dir))

import run_sign_sql


def test_sign_sql_walk_database_integrity():
    """Validates the 5 key pins of the sign_sql walk database."""
    conn = run_sign_sql.build_db()
    try:
        text = (run_sign_sql.BASE / "queries.sql").read_text(encoding="utf-8")
        queries = {qid: sql for qid, _title, sql in run_sign_sql.load_queries(text)}

        # Q1: Net totals agree across presentations
        cols, rows = run_sign_sql.run_query(conn, queries["q1"])
        by_label = {r[cols.index("presentation")]: r for r in rows}
        for label in ("A_frustrated", "B_meron_repaired"):
            row = by_label[label]
            assert row[cols.index("sum_num")] == 1
            assert row[cols.index("common_den")] == 2

        # Q2: Cancellation ratio in A is exactly 1/15
        cols, rows = run_sign_sql.run_query(conn, queries["q2"])
        by_label = {r[cols.index("presentation")]: r for r in rows}
        a = by_label["A_frustrated"]
        assert a[cols.index("ratio_num")] == 1
        assert a[cols.index("ratio_den")] == 15
        assert a[cols.index("l1_num")] == 15

        # Q3: Sign-free presentation B exists
        cols, rows = run_sign_sql.run_query(conn, queries["q3"])
        by_label = {r[cols.index("presentation")]: r for r in rows}
        assert by_label["B_meron_repaired"][cols.index("all_weights_nonnegative")] == 1
        assert by_label["A_frustrated"][cols.index("all_weights_nonnegative")] == 0

        # Q4: Pricing audit row count = 17 (10 licensed, 7 priced)
        cols, rows = run_sign_sql.run_query(conn, queries["q4"])
        assert len(rows) == 17
        priced = [r for r in rows if r[cols.index("priced")] == 1]
        assert len(priced) == 7

        # Q6: Wheeler-DeWitt row is declared boundary
        cols, rows = run_sign_sql.run_query(conn, queries["q6"])
        assert len(rows) == 1
        assert rows[0][cols.index("standing")] == "declared_boundary"
    finally:
        conn.close()


def test_fermion_gin_index_schema_instantiation():
    """Validates that databases/fermion_gin_index_schema.sql instantiates cleanly in SQLite."""
    schema_file = databases_dir / "fermion_gin_index_schema.sql"
    assert schema_file.exists(), f"Schema file not found at {schema_file}"

    conn = sqlite3.connect(":memory:")
    try:
        cur = conn.cursor()
        schema_sql = schema_file.read_text(encoding="utf-8")
        cur.executescript(schema_sql)

        # Check tables and views
        cur.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view');")
        objects = {name: otype for name, otype in cur.fetchall()}

        assert "FermionConfigurations" in objects
        assert "GinModePostingList" in objects
        assert "GinInvolutionPairs" in objects
        assert "GinMajoranaBonds" in objects
        assert "ViewFspInvolutionSignCancellationAudit" in objects
        assert "ViewAverageSignRecoveryAudit" in objects
        assert "ViewMajoranaZeroModeAudit" in objects
    finally:
        conn.close()
