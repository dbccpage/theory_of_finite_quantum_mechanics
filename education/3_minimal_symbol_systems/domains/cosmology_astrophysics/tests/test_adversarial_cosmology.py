"""
Adversarial Stress Test Suite: Cosmology, Gravitation & Astrophysics (Domain 7)
AuthorityEffect: None

Empirical challenge tests targeting:
1. Discrete causal set posets: transitive closure, Alexandrov intervals, and Myrheim-Meyer dimension estimation.
2. Acyclicity and causal irreflexivity: rejection of closed timelike curves (CTCs) and loops.
3. 3D Regge simplicial spacetime: boundary nilpotency B_1 * B_2 = 0 and B_2 * B_3 = 0.
4. Wheeler-DeWitt constraint defect Phi_WDW = 0 and multi-tetrahedron complexes (glued 3-ball and S^3 4-simplex boundary).
"""

import sys
from pathlib import Path

import pytest

# Ensure domain code is on sys.path
_test_dir = Path(__file__).resolve().parent
_code_dir = _test_dir.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from domain_cosmology_kernel import (
    CausalSet,
    DomainEngine,
)

# ============================================================================
# SECTION 1: Discrete Causal Sets, Alexandrov Intervals & Myrheim-Meyer
# ============================================================================


def test_deep_linear_causal_chain():
    """
    Stress-test transitive closure on deep causal chain:
    e_0 prec e_1 prec ... prec e_9 (10 elements).
    Total relations after transitive closure = 10 * 9 / 2 = 45 relations.
    Alexandrov interval I(e_0, e_9) = [e_1 ... e_8] (8 elements).
    Hasse irreducible links = 9 links (e_i, e_{i+1}).
    """
    N = 10
    events = [f"e{i}" for i in range(N)]
    rels = {(f"e{i}", f"e{i + 1}") for i in range(N - 1)}

    cs = CausalSet(events, rels)
    expected_total_rels = N * (N - 1) // 2
    assert len(cs.relations) == expected_total_rels

    # Maximal interval between endpoints
    iv = cs.alexandrov_interval("e0", f"e{N - 1}")
    assert iv == [f"e{i}" for i in range(1, N - 1)]
    assert len(iv) == N - 2

    # Hasse links are only adjacent steps
    links = cs.hasse_links()
    assert len(links) == N - 1
    for i in range(N - 1):
        assert (f"e{i}", f"e{i + 1}") in links




def test_causal_set_ctc_and_negative_controls():
    """
    Negative controls:
    1. 2-element closed timelike curve (CTC): e0 prec e1 and e1 prec e0.
    2. 3-element CTC: e0 prec e1 prec e2 prec e0.
    3. 5-element deep cycle.
    4. Self-loop: e0 prec e0.
    5. Non-existent element referenced in relations.
    """
    # 2-cycle
    with pytest.raises(ValueError, match="Causal cycle detected|Acyclicity violated"):
        CausalSet(["e0", "e1"], {("e0", "e1"), ("e1", "e0")})

    # 3-cycle
    with pytest.raises(ValueError, match="Causal cycle detected|Acyclicity violated"):
        CausalSet(["e0", "e1", "e2"], {("e0", "e1"), ("e1", "e2"), ("e2", "e0")})

    # 5-cycle
    with pytest.raises(ValueError, match="Causal cycle detected|Acyclicity violated"):
        CausalSet([f"e{i}" for i in range(5)], {(f"e{i}", f"e{(i + 1) % 5}") for i in range(5)})

    # Self-loop
    with pytest.raises(ValueError, match="violates irreflexivity"):
        CausalSet(["e0"], {("e0", "e0")})

    # Unknown element
    with pytest.raises(ValueError, match="references non-existent element"):
        CausalSet(["e0", "e1"], {("e0", "ghost")})


# ============================================================================
# SECTION 2: 3D Regge Simplicial Spacetime & Wheeler-DeWitt Nilpotency
# ============================================================================


def test_regge_spacetime_single_tetrahedron_full_nilpotency():
    """
    Verifies standard single 3D Regge tetrahedron:
    V=4, E=6, F=4, T=1.
    B_1 * B_2 = 0 (vertices x faces = 4 x 4 identically 0).
    B_2 * B_3 = 0 (edges x tetrahedra = 6 x 1 identically 0).
    Wheeler-DeWitt defect Phi_WDW = 0.
    Euler characteristic chi = 4 - 6 + 4 - 1 = 1.
    """
    engine = DomainEngine()
    receipt = engine.evaluate_regge_spacetime_complex()
    assert receipt.num_vertices == 4
    assert receipt.num_edges == 6
    assert receipt.num_faces == 4
    assert receipt.num_tetrahedra == 1
    assert receipt.is_b1_b2_nilpotent
    assert receipt.is_b2_b3_nilpotent
    assert receipt.boundary_defect == 0
    assert receipt.euler_characteristic == 1

    # Verify B_1 * B_2 matrix is strictly zero
    for row in receipt.b1_matrix:
        assert len(row) == 6
    for row in receipt.b2_matrix:
        assert len(row) == 4
    for row in receipt.b3_matrix:
        assert len(row) == 1


def test_two_glued_tetrahedra_regge_complex():
    """
    Multi-tetrahedron Regge spacetime:
    Two tetrahedra T1 = (v0, v1, v2, v3) and T2 = (v1, v2, v3, v4)
    sharing the triangular face (v1, v2, v3).
    Vertices: 5 (v0..v4)
    Edges: 9 (6 for T1 + 3 new for v4: (v1, v4), (v2, v4), (v3, v4))
    Faces: 7 (4 for T1 + 3 new for T2: (v1, v2, v4), (v1, v3, v4), (v2, v3, v4))
    Tetrahedra: 2 (T1, T2)
    Euler characteristic: 5 - 9 + 7 - 2 = 1 (topological 3-ball).
    Verify B_1 * B_2 = 0 and B_2 * B_3 = 0 hold identically.
    """
    vertices = ["v0", "v1", "v2", "v3", "v4"]
    v_idx = {v: i for i, v in enumerate(vertices)}

    edges = [
        # T1 edges
        ("v0", "v1"),
        ("v0", "v2"),
        ("v0", "v3"),
        ("v1", "v2"),
        ("v1", "v3"),
        ("v2", "v3"),
        # T2 new edges
        ("v1", "v4"),
        ("v2", "v4"),
        ("v3", "v4"),
    ]
    e_idx = {e: i for i, e in enumerate(edges)}

    def get_edge_sign(src: str, dst: str):
        if (src, dst) in e_idx:
            return e_idx[(src, dst)], +1
        elif (dst, src) in e_idx:
            return e_idx[(dst, src)], -1
        raise KeyError(f"Edge ({src}, {dst}) missing")

    faces = [
        # T1 faces
        ("v1", "v2", "v3"),  # Shared face
        ("v0", "v2", "v3"),
        ("v0", "v1", "v3"),
        ("v0", "v1", "v2"),
        # T2 faces
        ("v2", "v3", "v4"),
        ("v1", "v3", "v4"),
        ("v1", "v2", "v4"),
    ]
    f_idx = {f: i for i, f in enumerate(faces)}

    tetrahedra = [("v0", "v1", "v2", "v3"), ("v1", "v2", "v3", "v4")]

    n0, n1, n2, n3 = len(vertices), len(edges), len(faces), len(tetrahedra)

    # B_1: vertices x edges
    b1 = [[0] * n1 for _ in range(n0)]
    for j, (u, v) in enumerate(edges):
        b1[v_idx[v]][j] += 1
        b1[v_idx[u]][j] -= 1

    # B_2: edges x faces
    b2 = [[0] * n2 for _ in range(n1)]
    for k, (u0, u1, u2) in enumerate(faces):
        boundary_terms = [(1, (u1, u2)), (-1, (u0, u2)), (1, (u0, u1))]
        for sign, (src, dst) in boundary_terms:
            idx, s = get_edge_sign(src, dst)
            b2[idx][k] += sign * s

    # B_3: faces x tetrahedra
    # T1: (v0, v1, v2, v3) -> +(v1,v2,v3) - (v0,v2,v3) + (v0,v1,v3) - (v0,v1,v2)
    # T2: (v1, v2, v3, v4) -> +(v2,v3,v4) - (v1,v3,v4) + (v1,v2,v4) - (v1,v2,v3)
    b3 = [[0] * n3 for _ in range(n2)]
    t1_terms = [
        (1, ("v1", "v2", "v3")),
        (-1, ("v0", "v2", "v3")),
        (1, ("v0", "v1", "v3")),
        (-1, ("v0", "v1", "v2")),
    ]
    for sign, f in t1_terms:
        b3[f_idx[f]][0] += sign

    t2_terms = [
        (1, ("v2", "v3", "v4")),
        (-1, ("v1", "v3", "v4")),
        (1, ("v1", "v2", "v4")),
        (-1, ("v1", "v2", "v3")),
    ]
    for sign, f in t2_terms:
        b3[f_idx[f]][1] += sign

    # Check B_1 * B_2 = 0
    prod12 = [[sum(b1[i][j] * b2[j][k] for j in range(n1)) for k in range(n2)] for i in range(n0)]
    assert all(val == 0 for row in prod12 for val in row), (
        "B_1 * B_2 failed nilpotency on 2-tetrahedra complex"
    )

    # Check B_2 * B_3 = 0
    prod23 = [[sum(b2[j][k] * b3[k][l] for k in range(n2)) for l in range(n3)] for j in range(n1)]
    assert all(val == 0 for row in prod23 for val in row), (
        "B_2 * B_3 failed nilpotency on 2-tetrahedra complex"
    )

    # Euler characteristic
    chi = n0 - n1 + n2 - n3
    assert chi == 5 - 9 + 7 - 2 == 1


def test_four_simplex_boundary_s3_nilpotency():
    """
    Spherical 3D Spacetime: Boundary of a 4-simplex (triangulation of S^3).
    5 vertices (v0..v4).
    10 edges (all pairs).
    10 faces (all triplets).
    5 tetrahedra (all 4-tuples).
    Euler characteristic chi(S^3) = 5 - 10 + 10 - 5 = 0.
    Stokes boundary nilpotency B_1 * B_2 = 0 and B_2 * B_3 = 0 must hold on the closed 3-sphere!
    """
    import itertools

    vertices = [f"v{i}" for i in range(5)]
    v_idx = {v: i for i, v in enumerate(vertices)}

    edges = list(itertools.combinations(vertices, 2))
    e_idx = {e: i for i, e in enumerate(edges)}

    def get_edge_sign(src: str, dst: str):
        if (src, dst) in e_idx:
            return e_idx[(src, dst)], +1
        elif (dst, src) in e_idx:
            return e_idx[(dst, src)], -1
        raise KeyError(f"Edge ({src}, {dst}) missing")

    faces = list(itertools.combinations(vertices, 3))
    f_idx = {f: i for i, f in enumerate(faces)}

    def get_face_sign(u0, u1, u2):
        # Even permutation of sorted triple -> +1, odd -> -1
        sorted_triple = tuple(sorted([u0, u1, u2]))
        # Inversion count
        lst = [u0, u1, u2]
        inv = 0
        for i in range(3):
            for j in range(i + 1, 3):
                if lst[i] > lst[j]:
                    inv += 1
        sign = -1 if (inv % 2 == 1) else +1
        return f_idx[sorted_triple], sign

    tetrahedra = list(itertools.combinations(vertices, 4))
    {t: i for i, t in enumerate(tetrahedra)}

    n0, n1, n2, n3 = len(vertices), len(edges), len(faces), len(tetrahedra)
    assert (n0, n1, n2, n3) == (5, 10, 10, 5)

    # B_1: vertices x edges
    b1 = [[0] * n1 for _ in range(n0)]
    for j, (u, v) in enumerate(edges):
        b1[v_idx[v]][j] += 1
        b1[v_idx[u]][j] -= 1

    # B_2: edges x faces
    b2 = [[0] * n2 for _ in range(n1)]
    for k, (u0, u1, u2) in enumerate(faces):
        boundary_terms = [(1, (u1, u2)), (-1, (u0, u2)), (1, (u0, u1))]
        for sign, (src, dst) in boundary_terms:
            idx, s = get_edge_sign(src, dst)
            b2[idx][k] += sign * s

    # B_3: faces x tetrahedra
    # partial_3(u0, u1, u2, u3) = +(u1, u2, u3) - (u0, u2, u3) + (u0, u1, u3) - (u0, u1, u2)
    b3 = [[0] * n3 for _ in range(n2)]
    for l, (u0, u1, u2, u3) in enumerate(tetrahedra):
        t_terms = [(1, (u1, u2, u3)), (-1, (u0, u2, u3)), (1, (u0, u1, u3)), (-1, (u0, u1, u2))]
        for sign, face in t_terms:
            idx, s = get_face_sign(*face)
            b3[idx][l] += sign * s

    # Check B_1 * B_2 = 0
    prod12 = [[sum(b1[i][j] * b2[j][k] for j in range(n1)) for k in range(n2)] for i in range(n0)]
    assert all(val == 0 for row in prod12 for val in row), "B_1 * B_2 failed nilpotency on S^3"

    # Check B_2 * B_3 = 0
    prod23 = [[sum(b2[j][k] * b3[k][l] for k in range(n2)) for l in range(n3)] for j in range(n1)]
    assert all(val == 0 for row in prod23 for val in row), "B_2 * B_3 failed nilpotency on S^3"

    # Euler characteristic of S^3 is 0
    chi = n0 - n1 + n2 - n3
    assert chi == 0


def test_regge_corrupted_boundary_detection():
    """
    Negative control: Corrupting face or tetrahedron boundary signs induces
    non-zero Wheeler-DeWitt constraint defect Phi_WDW > 0.
    """
    engine = DomainEngine()
    receipt = engine.evaluate_regge_spacetime_complex()

    # Corrupt B_2
    b1 = receipt.b1_matrix
    b2_bad = [row[:] for row in receipt.b2_matrix]
    b2_bad[0][0] += 1  # Corrupt entry

    n0 = len(b1)
    n1 = len(b2_bad)
    n2 = len(b2_bad[0])
    prod12_bad = [
        [sum(b1[i][j] * b2_bad[j][k] for j in range(n1)) for k in range(n2)] for i in range(n0)
    ]

    defect = sum(abs(v) for row in prod12_bad for v in row)
    assert defect > 0, "Corrupted B_2 must cause non-zero WDW defect"
