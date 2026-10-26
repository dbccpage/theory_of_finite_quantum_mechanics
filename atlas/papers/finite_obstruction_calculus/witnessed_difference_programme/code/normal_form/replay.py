"""PLAN-ODM-5: finite text-set SQL reconstruction control.

The schema is R(A,B,C), A -> B, decomposed as AB and AC. The reusable FD
implication/BCNF decision procedure belongs to Rust finite_functional_dependencies;
this paper control independently executes the selected projections and join in
SQLite. It does not cover the historical AutoP/PTIR pipeline or arbitrary schemas.
"""
from __future__ import annotations

import sqlite3


def replay(rows: tuple[tuple[str, str, str], ...]) -> dict:
    if any(len(row) != 3 or any(type(x) is not str for x in row) for row in rows):
        raise ValueError("three exact text attributes required")
    if len(set(rows)) != len(rows):
        raise ValueError("set carrier refuses duplicate rows")
    if any(a == x and b != y for a, b, _ in rows for x, y, _ in rows):
        raise ValueError("declared A -> B dependency violated")
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE r(a TEXT NOT NULL, b TEXT NOT NULL, c TEXT NOT NULL)")
        db.executemany("INSERT INTO r VALUES (?,?,?)", rows)
        db.execute("CREATE VIEW ab AS SELECT DISTINCT a,b FROM r")
        db.execute("CREATE VIEW ac AS SELECT DISTINCT a,c FROM r")
        joined = tuple(db.execute("SELECT ab.a,ab.b,ac.c FROM ab JOIN ac USING(a) ORDER BY 1,2,3"))
    if joined != tuple(sorted(rows)):
        raise ValueError("original-source reconstruction failed")
    return {"rows": joined, "components": ("AB", "AC"),
            "reconstruction_target": "original_source_value", "authority_effect": "None"}
