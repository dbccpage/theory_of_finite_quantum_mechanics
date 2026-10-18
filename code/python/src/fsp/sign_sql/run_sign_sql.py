"""run_sign_sql.py -- stdlib sqlite3 runner for the sign-problem walk database.

Creates a fresh in-memory database, applies schema.sql and seed.sql, runs
every query in queries.sql (split on '-- @query <id> <title>' markers), and
prints deterministic results (every query carries its own ORDER BY; no
timestamps, no environment data).

AuthorityEffect: None.  Honesty fences: the toy instance ILLUSTRATES the
structure of the sign problem; it does not simulate physics.  The
Wheeler-DeWitt row is a declared boundary object citing the house DeWitt
case study (PP/021).  Hardness statements (Cook-Levin, Troyer-Wiese) are
external literature; nothing here derives them.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent

QUERY_MARKER = "-- @query "


def load_queries(text: str) -> list[tuple[str, str, str]]:
    """Split queries.sql into (query_id, title, sql) triples on marker lines."""
    queries: list[tuple[str, str, str]] = []
    qid: str | None = None
    title = ""
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith(QUERY_MARKER):
            if qid is not None:
                queries.append((qid, title, "\n".join(buf)))
            rest = line[len(QUERY_MARKER):].strip()
            parts = rest.split(" ", 1)
            qid = parts[0]
            title = parts[1] if len(parts) > 1 else ""
            buf = []
        else:
            buf.append(line)
    if qid is not None:
        queries.append((qid, title, "\n".join(buf)))
    return queries


def build_db() -> sqlite3.Connection:
    """Create a fresh in-memory database and apply schema + seed."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript((BASE / "schema.sql").read_text(encoding="utf-8"))
    conn.executescript((BASE / "seed.sql").read_text(encoding="utf-8"))
    return conn


def run_query(conn: sqlite3.Connection, sql: str) -> tuple[list[str], list[tuple[object, ...]]]:
    """Execute one query; return (column names, rows)."""
    cur = conn.execute(sql)
    cols = [d[0] for d in cur.description]
    return cols, cur.fetchall()


def main() -> None:
    conn = build_db()
    text = (BASE / "queries.sql").read_text(encoding="utf-8")
    for qid, title, sql in load_queries(text):
        print(f"=== {qid} :: {title}")
        cols, rows = run_query(conn, sql)
        print(" | ".join(cols))
        for row in rows:
            print(" | ".join(str(v) for v in row))
        print(f"({len(rows)} rows)")
        print()
    conn.close()


if __name__ == "__main__":
    main()
