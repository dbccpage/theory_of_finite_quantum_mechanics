"""Exact finite meron-cluster fixture, evaluated with SQLite and exact rationals.

Vendored subset of two repository files at commit
52cb5457f6c485ba548cfd292f6012a941ed22cf:

- omega_engine_projects/fsp/code/sign_sql/exact_models.py
  (SHA-256 a0b3301af1a38618d59a16a92a462f026a40263f0726d32e3e7ea910588bbaa1)
- omega_engine_projects/fsp/databases/meron_hubbard.sql
  (SHA-256 2e772cb9eccd510aed828b5f71438dddef7ead99a26bd99f3009039888b07c49)

Only the meron functions were copied, from ``rational`` to
``meron_transfer_trace`` inclusive. The schema is read from the sibling file
``meron_schema.sql``, which holds the meron tables and views of the second file.
The import block and the schema path are the only other changes; no arithmetic
function and no SQL statement was edited. The only SQL arithmetic extensions are
scalar rational operations, a stepwise rational sum, and integer popcount.
"""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from fractions import Fraction
from pathlib import Path

SCHEMA = Path(__file__).resolve().with_name("meron_schema.sql")


def rational(value: object) -> Fraction:
    """Reject approximate numbers, including integral floats and booleans."""
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise TypeError("exact integer, fraction, or rational string required")
    if isinstance(value, str) and any(c in value.lower() for c in ".e"):
        raise ValueError("decimal/exponent syntax is not an exact rational input")
    return Fraction(value)


class RationalSum:
    def __init__(self) -> None:
        self.total = Fraction(0)

    def step(self, value: str) -> None:
        self.total += rational(value)

    def finalize(self) -> str:
        return str(self.total)


def connection() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys=ON")
    con.create_function("qadd", 2, lambda a, b: str(rational(a) + rational(b)))
    con.create_function("qmul", 2, lambda a, b: str(rational(a) * rational(b)))
    con.create_function("qdiv", 2, lambda a, b: str(rational(a) / rational(b)))
    con.create_function("qabs", 1, lambda a: str(abs(rational(a))))
    con.create_function("qsign", 1, lambda a: (rational(a) > 0) - (rational(a) < 0))
    con.create_function("qpow", 2, lambda a, n: str(rational(a) ** n))
    con.create_function("popcount", 1, int.bit_count)
    con.create_aggregate("qsum", 1, RationalSum)
    con.executescript(SCHEMA.read_text(encoding="utf-8"))
    return con


def save_parameters(con: sqlite3.Connection, parameters: dict) -> None:
    con.execute("INSERT INTO experiment_metadata VALUES('parameters',?)",(json.dumps(parameters,sort_keys=True),))


def parameters(con: sqlite3.Connection) -> dict:
    row=con.execute("SELECT value FROM experiment_metadata WHERE key='parameters'").fetchone()
    return json.loads(row[0]) if row else {}


def hop_sign(state: int, source: int, target: int) -> int:
    lo, hi = sorted((source, target))
    occupied_between = (state >> (lo + 1)) & ((1 << (hi - lo - 1)) - 1)
    return -1 if occupied_between.bit_count() % 2 else 1


def meron_database(sites: int = 4, repetitions: int = 2, q: object = "3") -> sqlite3.Connection:
    """U=t periodic even chain; q=exp(epsilon*t), scalar exp(-epsilon*t/4) removed.

    SQL constructs all breakup graphs, loop components and occupations. CAR
    signs are calculated from the reconstructed hopping configurations in SQL.
    """
    if type(sites) is not int or sites < 4 or sites % 2 or sites > 6:
        raise ValueError("finite checkerboard fixture requires 4 or 6 sites")
    if type(repetitions) is not int or repetitions < 1 or sites * repetitions > 12:
        raise ValueError("at most 12 interaction plaquettes are supported")
    qvalue = rational(q)
    if qvalue < 1:
        raise ValueError("q=exp(epsilon*t) must be at least one")
    con = connection()
    times = 2 * repetitions
    save_parameters(con,{"model":"spinless U=t meron Hamiltonian","sites":sites,"repetitions":repetitions,
                         "q":str(qvalue),"boundary":"periodic even chain","epsilon_t":"log(q)",
                         "removed_positive_scalar":f"q^(-{Fraction(sites*repetitions,4)})"})
    con.execute("INSERT INTO meron_parameter VALUES(?,?,?,?)", (sites, times, sites * repetitions, str((qvalue - 1) / 2)))
    con.executemany("INSERT INTO meron_node VALUES(?,?,?)", ((t * sites + x, t, x) for t in range(times) for x in range(sites)))
    plaquettes = []
    for t in range(times):
        for x in range(t % 2, sites, 2):
            y = (x + 1) % sites
            plaquettes.append((len(plaquettes), t, x, y, t * sites + x, t * sites + y, ((t + 1) % times) * sites + x, ((t + 1) % times) * sites + y))
    con.executemany("INSERT INTO meron_plaquette VALUES(?,?,?,?,?,?,?,?)", plaquettes)
    con.executescript(MERON_BUILD)
    return con


MERON_BUILD = """
INSERT INTO meron_graph
WITH RECURSIVE graphs(depth,gid,weight) AS (
 SELECT 0,0,'1' UNION ALL
 SELECT depth+1,gid | (b.bit << depth),qmul(weight,CASE b.bit WHEN 0 THEN '1' ELSE horizontal END)
 FROM graphs CROSS JOIN bit b CROSS JOIN meron_parameter WHERE depth < plaquettes
) SELECT gid,weight FROM graphs,meron_parameter WHERE depth=plaquettes;

INSERT INTO meron_edge
SELECT g.gid,p.a,CASE WHEN (g.gid >> p.pid)&1 THEN p.b ELSE p.c END FROM meron_graph g CROSS JOIN meron_plaquette p
UNION ALL SELECT g.gid,p.d,CASE WHEN (g.gid >> p.pid)&1 THEN p.c ELSE p.b END FROM meron_graph g CROSS JOIN meron_plaquette p;
INSERT INTO meron_edge SELECT gid,target,source FROM meron_edge;

INSERT INTO meron_component
WITH RECURSIVE reach(gid,root,node) AS (
 SELECT gid,node,node FROM meron_graph CROSS JOIN meron_node UNION
 SELECT r.gid,r.root,e.target FROM reach r JOIN meron_edge e ON e.gid=r.gid AND e.source=r.node
), roots AS (SELECT gid,node,MIN(root) root FROM reach GROUP BY gid,node)
SELECT gid,node,root,DENSE_RANK() OVER(PARTITION BY gid ORDER BY root)-1 FROM roots;

INSERT INTO meron_orientation
WITH RECURSIVE counts AS (SELECT gid,MAX(cluster)+1 k FROM meron_component GROUP BY gid),
orient(gid,k,mask) AS (SELECT gid,k,0 FROM counts UNION ALL SELECT gid,k,mask+1 FROM orient WHERE mask+1 < (1 << k))
SELECT gid,mask,k FROM orient;

INSERT INTO meron_state
SELECT o.gid,o.mask,n.time,SUM((((1-(n.site%2)) + ((o.mask >> c.cluster)&1))%2) << n.site)
FROM meron_orientation o JOIN meron_component c ON c.gid=o.gid JOIN meron_node n ON n.node=c.node
GROUP BY o.gid,o.mask,n.time;

INSERT INTO meron_configuration
SELECT s.gid,s.mask,
 CASE WHEN SUM(CASE WHEN ((s.state >> p.x)&1) != ((after.state >> p.x)&1)
 THEN popcount((s.state >> (MIN(p.x,p.y)+1)) & ((1 << (ABS(p.x-p.y)-1))-1)) ELSE 0 END)%2=0 THEN 1 ELSE -1 END,
 g.weight
FROM meron_state s JOIN meron_parameter par JOIN meron_state after
 ON after.gid=s.gid AND after.mask=s.mask AND after.time=(s.time+1)%par.times
JOIN meron_plaquette p ON p.time=s.time JOIN meron_graph g ON g.gid=s.gid
GROUP BY s.gid,s.mask;
"""


def meron_summary(con: sqlite3.Connection) -> dict:
    model_defects=meron_model_defects(con)
    invalid = con.execute("SELECT COUNT(*) FROM meron_invalid_character").fetchone()[0]
    unequal = con.execute("SELECT COUNT(*) FROM meron_configuration f JOIN meron_graph g ON g.gid=f.gid WHERE qsign(qadd(f.weight,qmul('-1',g.weight)))<>0").fetchone()[0]
    missing = con.execute("""SELECT COUNT(*) FROM (SELECT g.gid FROM meron_graph g
      LEFT JOIN meron_configuration f ON f.gid=g.gid GROUP BY g.gid HAVING COUNT(f.mask)<>
      (1 << (SELECT MAX(cluster)+1 FROM meron_component c WHERE c.gid=g.gid)) OR MIN(f.mask)<0 OR MAX(f.mask)>=
      (1 << (SELECT MAX(cluster)+1 FROM meron_component c WHERE c.gid=g.gid)))""").fetchone()[0]
    key_defects=con.execute("SELECT COUNT(*) FROM (SELECT gid,mask FROM meron_configuration EXCEPT SELECT gid,mask FROM meron_orientation)").fetchone()[0]
    key_defects+=con.execute("SELECT COUNT(*) FROM (SELECT gid,mask FROM meron_orientation EXCEPT SELECT gid,mask FROM meron_configuration)").fetchone()[0]
    rows = con.execute("SELECT * FROM meron_orbit ORDER BY gid").fetchall()
    signed, absolute = con.execute("SELECT qsum(qmul(sign,weight)),qsum(weight) FROM meron_configuration").fetchone()
    reduced = con.execute("SELECT qsum(reduced_weight) FROM meron_orbit").fetchone()[0]
    raw_observable=con.execute("SELECT qsum(qmul(qmul(sign,weight),qmul(observable,observable))) FROM meron_staggered").fetchone()[0]
    reduced_observable=con.execute("SELECT qsum(numerator) FROM meron_squared_orbit").fetchone()[0]
    return {"experiment_parameters":parameters(con),"graphs": len(rows), "configurations": con.execute("SELECT COUNT(*) FROM meron_configuration").fetchone()[0],
            "negative_configurations": con.execute("SELECT COUNT(*) FROM meron_configuration WHERE sign=-1 AND qsign(weight)>0").fetchone()[0],
            "zero_meron_graphs": sum(row[2] == 0 for row in rows), "invalid_characters": invalid,
            "unequal_orbit_weights":unequal,"incomplete_orbits":missing,
            "orientation_key_defects":key_defects,
            "model_relation_defects":model_defects,
            "signed_partition": signed, "absolute_partition": absolute, "reduced_partition": reduced,
            "average_sign": str(rational(signed) / rational(absolute)),
            "staggered_square_numerator":raw_observable,"improved_staggered_square_numerator":reduced_observable,
            "staggered_square_expectation":str(rational(raw_observable)/rational(signed)) if rational(signed) else None,
            "reconstruction": signed == reduced and raw_observable==reduced_observable and invalid == 0 and unequal==0 and missing==0 and key_defects==0 and not model_defects}


def meron_model_defects(con: sqlite3.Connection) -> dict:
    """Replay the declared finite model, so a coherent different ensemble fails.

    This is intentionally priced as a second construction, not a constant-cost
    admission check. Multiset equality includes the full graph domain, declared
    nonnegative breakup weights, physical CAR signs, and every intermediate key.
    """
    declared=parameters(con)
    expected=meron_database(declared["sites"],declared["repetitions"],declared["q"])
    defects={}
    try:
        for table in ("meron_parameter","meron_node","meron_plaquette","meron_graph","meron_edge",
                      "meron_component","meron_orientation","meron_state","meron_configuration"):
            actual_rows=Counter(con.execute(f"SELECT * FROM {table}").fetchall())
            expected_rows=Counter(expected.execute(f"SELECT * FROM {table}").fetchall())
            difference=sum((actual_rows-expected_rows).values())+sum((expected_rows-actual_rows).values())
            if difference:
                defects[table]=difference
    finally:
        expected.close()
    return defects


def meron_transfer_trace(sites: int, repetitions: int, q: object) -> str:
    """Independent occupation-basis transfer multiplication, without clusters."""
    q = rational(q)
    dim = 1 << sites
    matrix = [[Fraction(i == j) for j in range(dim)] for i in range(dim)]
    for time in range(2 * repetitions):
        for x in range(time % 2, sites, 2):
            y = (x + 1) % sites
            updated = [[Fraction(0) for _ in range(dim)] for _ in range(dim)]
            for state in range(dim):
                mixed = ((state >> x) ^ (state >> y)) & 1
                diagonal = (q + 1) / 2 if mixed else Fraction(1)
                for origin in range(dim):
                    updated[state][origin] += diagonal * matrix[state][origin]
                    if mixed:
                        other = state ^ (1 << x) ^ (1 << y)
                        updated[other][origin] += (q - 1) / 2 * hop_sign(state, x, y) * matrix[state][origin]
            matrix = updated
    result = Fraction(0)
    for i in range(dim):
        result += matrix[i][i]
    return str(result)
