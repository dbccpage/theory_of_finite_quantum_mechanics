"""
Adversarial Stress Test Suite: Root W Relational Schema & Boundary Sign Inversion
AuthorityEffect: None

Tests that view_boundary_sign_inversion strictly eliminates Cartesian cross-terms
and enforces boundary sign inversion d_1(sigma(e)) = -d_1(e) with net_sum == 0 across:
1. Multi-edge paths with shared hub vertices (e.g. c -> a -> b and d -> a -> e).
2. Ultra-high degree star hubs (50 in-edges, 75 out-edges).
3. Complete bipartite graphs (K_10,10 with 100 directed edges).
4. Antiparallel self-cancelling directed cycles (a -> b and b -> a).
5. 100 randomized directed graph topologies.
6. Irreflexivity check constraint enforcement (rejection of self-loops).
7. Foreign key constraint enforcement.
"""

import random
import sqlite3
from pathlib import Path

import pytest

_schema_path = (
    Path(__file__).resolve().parent.parent / "code" / "queries" / "root_w_relational_schema.sql"
)


def _init_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    with open(_schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    return conn


def test_specified_multi_edge_paths():
    """Validates multi-edge paths (c -> a -> b, d -> a -> e) with degree-4 hub."""
    conn = _init_db()

    for v in ["a", "b", "c", "d", "e"]:
        conn.execute(
            "INSERT INTO carrier_elements (element_id, admitted_step) VALUES (?, 1);", (v,)
        )

    edges = [("c", "a"), ("a", "b"), ("d", "a"), ("a", "e")]
    for u, v in edges:
        conn.execute(
            "INSERT INTO difference_relations (src, dst, admitted_step) VALUES (?, ?, 2);", (u, v)
        )

    rows = conn.execute(
        "SELECT vertex, orig_weight, trans_weight, net_sum FROM view_boundary_sign_inversion ORDER BY vertex;"
    ).fetchall()

    assert len(rows) == 5, f"Expected exactly 5 rows (1 per vertex), got {len(rows)}"

    for vertex, orig_w, trans_w, net_sum in rows:
        assert net_sum == 0, f"Vertex {vertex} failed boundary cancellation: net_sum={net_sum}"
        assert trans_w == -orig_w, (
            f"Vertex {vertex} failed sign flip: orig={orig_w}, trans={trans_w}"
        )

    row_a = [r for r in rows if r[0] == "a"][0]
    assert row_a[1] == 0 and row_a[2] == 0 and row_a[3] == 0, (
        "Hub vertex 'a' must have net 0 boundary weight"
    )
    conn.close()


def test_high_degree_hub_cartesian_elimination():
    """Validates that a hub vertex with 50 incoming and 75 outgoing edges does NOT produce Cartesian explosion."""
    conn = _init_db()

    conn.execute(
        "INSERT INTO carrier_elements (element_id, admitted_step) VALUES (?, 1);", ("hub",)
    )
    for i in range(50):
        v = f"in_{i}"
        conn.execute(
            "INSERT INTO carrier_elements (element_id, admitted_step) VALUES (?, 1);", (v,)
        )
        conn.execute(
            "INSERT INTO difference_relations (src, dst, admitted_step) VALUES (?, ?, 1);",
            (v, "hub"),
        )

    for j in range(75):
        v = f"out_{j}"
        conn.execute(
            "INSERT INTO carrier_elements (element_id, admitted_step) VALUES (?, 1);", (v,)
        )
        conn.execute(
            "INSERT INTO difference_relations (src, dst, admitted_step) VALUES (?, ?, 1);",
            ("hub", v),
        )

    rows = conn.execute(
        "SELECT vertex, orig_weight, trans_weight, net_sum FROM view_boundary_sign_inversion;"
    ).fetchall()

    # Invariant: exactly 1 row per active vertex (1 + 50 + 75 = 126 rows)
    assert len(rows) == 126, (
        f"Expected 126 unique vertex rows, got {len(rows)} (Cartesian cross-term leak!)"
    )

    for vertex, orig_w, trans_w, net_sum in rows:
        assert net_sum == 0
        assert trans_w == -orig_w

    row_hub = [r for r in rows if r[0] == "hub"][0]
    assert row_hub[1] == (50 - 75) == -25
    assert row_hub[2] == 25
    assert row_hub[3] == 0
    conn.close()


def test_dense_bipartite_graph_complete_cancellation():
    """Validates complete bipartite graph K_10,10 (100 edges) across 20 vertices."""
    conn = _init_db()

    left = [f"L_{i}" for i in range(10)]
    right = [f"R_{j}" for j in range(10)]
    for v in left + right:
        conn.execute(
            "INSERT INTO carrier_elements (element_id, admitted_step) VALUES (?, 1);", (v,)
        )

    for u in left:
        for w in right:
            conn.execute(
                "INSERT INTO difference_relations (src, dst, admitted_step) VALUES (?, ?, 1);",
                (u, w),
            )

    rows = conn.execute(
        "SELECT vertex, orig_weight, trans_weight, net_sum FROM view_boundary_sign_inversion;"
    ).fetchall()

    assert len(rows) == 20
    for vertex, orig_w, trans_w, net_sum in rows:
        assert net_sum == 0
        assert trans_w == -orig_w
        if vertex.startswith("L_"):
            assert orig_w == -10 and trans_w == 10
        else:
            assert orig_w == 10 and trans_w == -10
    conn.close()


def test_antiparallel_bidirectional_edges():
    """Validates antiparallel edge pair a -> b and b -> a."""
    conn = _init_db()

    for v in ["a", "b"]:
        conn.execute(
            "INSERT INTO carrier_elements (element_id, admitted_step) VALUES (?, 1);", (v,)
        )

    conn.execute(
        "INSERT INTO difference_relations (src, dst, admitted_step) VALUES (?, ?, 1);", ("a", "b")
    )
    conn.execute(
        "INSERT INTO difference_relations (src, dst, admitted_step) VALUES (?, ?, 1);", ("b", "a")
    )

    rows = conn.execute(
        "SELECT vertex, orig_weight, trans_weight, net_sum FROM view_boundary_sign_inversion;"
    ).fetchall()

    assert len(rows) == 2
    for vertex, orig_w, trans_w, net_sum in rows:
        assert orig_w == 0 and trans_w == 0 and net_sum == 0
    conn.close()


def test_100_random_directed_graphs_sign_inversion():
    """Stress-test 100 randomized directed topologies with arbitrary degree distributions."""
    rng = random.Random(42)

    for g in range(100):
        conn = _init_db()
        num_v = rng.randint(4, 25)
        v_ids = [f"v_{i}" for i in range(num_v)]
        for v in v_ids:
            conn.execute(
                "INSERT INTO carrier_elements (element_id, admitted_step) VALUES (?, 1);", (v,)
            )

        num_e = rng.randint(3, 40)
        e_set = set()
        for _ in range(num_e):
            u, w = rng.sample(v_ids, 2)
            if (u, w) not in e_set:
                e_set.add((u, w))
                conn.execute(
                    "INSERT INTO difference_relations (src, dst, admitted_step) VALUES (?, ?, 1);",
                    (u, w),
                )

        rows = conn.execute(
            "SELECT vertex, orig_weight, trans_weight, net_sum FROM view_boundary_sign_inversion;"
        ).fetchall()

        active_verts = set(u for u, w in e_set) | set(w for u, w in e_set)
        assert len(rows) == len(active_verts), f"Row count mismatch on graph {g}"

        for vertex, orig_w, trans_w, net_sum in rows:
            assert net_sum == 0, f"Graph {g}, vertex {vertex} net_sum != 0"
            assert trans_w == -orig_w
        conn.close()


def test_negative_control_irreflexivity_rejection():
    """Negative control: self-loops (a -> a) must be rejected by chk_irreflexive."""
    conn = _init_db()
    conn.execute("INSERT INTO carrier_elements (element_id, admitted_step) VALUES (?, 1);", ("a",))

    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO difference_relations (src, dst, admitted_step) VALUES (?, ?, 1);",
            ("a", "a"),
        )
    conn.close()


def test_negative_control_foreign_key_rejection():
    """Negative control: inserting edge with unadmitted vertex fails foreign key constraint."""
    conn = _init_db()
    conn.execute("INSERT INTO carrier_elements (element_id, admitted_step) VALUES (?, 1);", ("a",))

    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO difference_relations (src, dst, admitted_step) VALUES (?, ?, 1);",
            ("a", "ghost"),
        )
    conn.close()
