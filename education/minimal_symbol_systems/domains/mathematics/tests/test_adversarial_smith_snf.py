"""
Adversarial Stress Test Suite: Smith Normal Form, Simplicial Manifolds & Homology Invariants
AuthorityEffect: None

Tests exact algebraic invariants of SmithNormalForm on RP^2 and Klein Bottle under:
1. Permutations of triangle ordering (shuffling 2-simplex basis).
2. Cyclic vertex permutations (even permutations preserving triangle orientation).
3. Transposition vertex swaps (odd permutations reversing triangle orientation).
4. Vertex isomorphism relabelings (S_n action on 0-simplices).
5. Exact Bareiss divisibility, unimodularity (det(P) = +/-1, det(Q) = +/-1), and Stokes nilpotency d1 * d2 = 0.
"""

import random
import sys
from pathlib import Path
from typing import List, Tuple

_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from smith_normal_form import (
    SmithNormalForm,
    _mat_mul,
    build_klein_bottle_complex,
    build_rp2_complex,
)


def _rebuild_complex_from_triangles(
    triangles: List[Tuple[int, int, int]], num_verts: int = None
) -> Tuple[List[int], List[List[int]], List[List[int]]]:
    """Helper to reconstruct canonical simplicial boundary matrices d1 and d2 from triangle list."""
    verts = sorted(list(set(v for t in triangles for v in t)))
    n_v = num_verts if num_verts is not None else len(verts)
    vert_map = {v: i for i, v in enumerate(verts)}

    edges = sorted(
        list(
            set(
                (min(vert_map[u], vert_map[v]), max(vert_map[u], vert_map[v]))
                for u, v, w in triangles
                for (u, v) in [(u, v), (u, w), (v, w)]
            )
        )
    )
    edge_map = {e: i for i, e in enumerate(edges)}

    d1 = [[0] * len(edges) for _ in range(n_v)]
    for j, (u, v) in enumerate(edges):
        d1[v][j] += 1
        d1[u][j] -= 1

    d2 = [[0] * len(triangles) for _ in range(len(edges))]
    for j, (u, v, w) in enumerate(triangles):
        iu, iv, iw = vert_map[u], vert_map[v], vert_map[w]
        for a, b in [(iv, iw), (iw, iu), (iu, iv)]:
            e = (min(a, b), max(a, b))
            sgn = 1 if a < b else -1
            d2[edge_map[e]][j] += sgn

    return [n_v, len(edges), len(triangles)], d1, d2


def test_rp2_exact_invariants():
    """Validates baseline RP^2 complex: d1 * d2 = 0, H_0 = Z, H_1 = Z/2Z, H_2 = 0, chi = 1."""
    f, d1, d2 = build_rp2_complex()
    assert f == [6, 15, 10]

    prod = _mat_mul(d1, d2)
    assert all(all(x == 0 for x in row) for row in prod), "RP2 must satisfy d1 * d2 = 0 identically"

    h0 = SmithNormalForm.compute_homology(None, d1, f[0], dim=0)
    h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
    h2 = SmithNormalForm.compute_homology(d2, None, f[2], dim=2)

    assert h0.betti_number == 1 and h0.torsion_coefficients == [] and h0.homology_group_str == "Z"
    assert (
        h1.betti_number == 0 and h1.torsion_coefficients == [2] and h1.homology_group_str == "Z/2Z"
    )
    assert h2.betti_number == 0 and h2.torsion_coefficients == [] and h2.homology_group_str == "0"
    assert f[0] - f[1] + f[2] == 1


def test_klein_bottle_exact_invariants():
    """Validates baseline Klein bottle complex: d1 * d2 = 0, H_0 = Z, H_1 = Z (+) Z/2Z, H_2 = 0, chi = 0."""
    f, d1, d2 = build_klein_bottle_complex()
    assert f == [12, 36, 24]

    prod = _mat_mul(d1, d2)
    assert all(all(x == 0 for x in row) for row in prod), (
        "Klein bottle must satisfy d1 * d2 = 0 identically"
    )

    h0 = SmithNormalForm.compute_homology(None, d1, f[0], dim=0)
    h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
    h2 = SmithNormalForm.compute_homology(d2, None, f[2], dim=2)

    assert h0.betti_number == 1 and h0.torsion_coefficients == [] and h0.homology_group_str == "Z"
    assert (
        h1.betti_number == 1
        and h1.torsion_coefficients == [2]
        and h1.homology_group_str == "Z (+) Z/2Z"
    )
    assert h2.betti_number == 0 and h2.torsion_coefficients == [] and h2.homology_group_str == "0"
    assert f[0] - f[1] + f[2] == 0


def test_rp2_adversarial_triangle_shuffles():
    """Stress-test RP^2 with 50 random permutations of the triangle list order."""
    rp2_triangles = [
        (0, 1, 2),
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 0),
        (4, 0, 1),
        (0, 2, 5),
        (2, 4, 5),
        (4, 1, 5),
        (1, 3, 5),
        (3, 0, 5),
    ]
    rng = random.Random(42)
    for _ in range(50):
        shuffled = rp2_triangles[:]
        rng.shuffle(shuffled)
        f, d1, d2 = _rebuild_complex_from_triangles(shuffled, num_verts=6)
        prod = _mat_mul(d1, d2)
        assert all(all(x == 0 for x in row) for row in prod), (
            "Nilpotency broken under triangle shuffling"
        )
        h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
        h2 = SmithNormalForm.compute_homology(d2, None, f[2], dim=2)
        assert h1.betti_number == 0 and h1.torsion_coefficients == [2]
        assert h2.betti_number == 0 and h2.torsion_coefficients == []


def test_klein_bottle_adversarial_triangle_shuffles():
    """Stress-test Klein bottle with 50 random permutations of the triangle list order."""
    nx, ny = 3, 4

    def v(x: int, y: int):
        x = x % nx
        if y >= ny:
            return ((nx - (x % nx)) % nx, 0)
        return (x, y % ny)

    kb_triangles = []
    for x in range(nx):
        for y in range(ny):
            kb_triangles.append((v(x, y), v(x + 1, y), v(x + 1, y + 1)))
            kb_triangles.append((v(x, y), v(x + 1, y + 1), v(x, y + 1)))

    rng = random.Random(1337)
    for _ in range(50):
        shuffled = kb_triangles[:]
        rng.shuffle(shuffled)
        f, d1, d2 = _rebuild_complex_from_triangles(shuffled)
        prod = _mat_mul(d1, d2)
        assert all(all(x == 0 for x in row) for row in prod), (
            "Nilpotency broken under KB triangle shuffling"
        )
        h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
        h2 = SmithNormalForm.compute_homology(d2, None, f[2], dim=2)
        assert h1.betti_number == 1 and h1.torsion_coefficients == [2]
        assert h2.betti_number == 0 and h2.torsion_coefficients == []


def test_rp2_cyclic_and_odd_triangle_permutations():
    """Stress-test RP^2 under cyclic (even) and transposition (odd) vertex permutations in triangles."""
    rp2_triangles = [
        (0, 1, 2),
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 0),
        (4, 0, 1),
        (0, 2, 5),
        (2, 4, 5),
        (4, 1, 5),
        (1, 3, 5),
        (3, 0, 5),
    ]

    # Cyclic permutations
    for cycle in [1, 2]:
        permuted = []
        for u, v, w in rp2_triangles:
            permuted.append((v, w, u) if cycle == 1 else (w, u, v))
        f, d1, d2 = _rebuild_complex_from_triangles(permuted, num_verts=6)
        prod = _mat_mul(d1, d2)
        assert all(all(x == 0 for x in row) for row in prod)
        h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
        assert h1.betti_number == 0 and h1.torsion_coefficients == [2]

    # Odd permutations (reversing individual 2-simplex orientations)
    rng = random.Random(777)
    for _ in range(25):
        permuted = []
        for u, v, w in rp2_triangles:
            permuted.append((u, w, v) if rng.random() < 0.5 else (u, v, w))
        f, d1, d2 = _rebuild_complex_from_triangles(permuted, num_verts=6)
        prod = _mat_mul(d1, d2)
        assert all(all(x == 0 for x in row) for row in prod)
        h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
        h2 = SmithNormalForm.compute_homology(d2, None, f[2], dim=2)
        assert h1.betti_number == 0 and h1.torsion_coefficients == [2]
        assert h2.betti_number == 0 and h2.torsion_coefficients == []


def test_rp2_vertex_isomorphisms():
    """Stress-test RP^2 under 50 random vertex relabelings (permutations of {0..5})."""
    rp2_triangles = [
        (0, 1, 2),
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 0),
        (4, 0, 1),
        (0, 2, 5),
        (2, 4, 5),
        (4, 1, 5),
        (1, 3, 5),
        (3, 0, 5),
    ]
    rng = random.Random(999)
    for _ in range(50):
        perm = list(range(6))
        rng.shuffle(perm)
        perm_map = {i: perm[i] for i in range(6)}
        relabeled = [(perm_map[u], perm_map[v], perm_map[w]) for u, v, w in rp2_triangles]
        f, d1, d2 = _rebuild_complex_from_triangles(relabeled, num_verts=6)
        prod = _mat_mul(d1, d2)
        assert all(all(x == 0 for x in row) for row in prod)
        h1 = SmithNormalForm.compute_homology(d1, d2, f[1], dim=1)
        h2 = SmithNormalForm.compute_homology(d2, None, f[2], dim=2)
        assert h1.betti_number == 0 and h1.torsion_coefficients == [2]
        assert h2.betti_number == 0 and h2.torsion_coefficients == []


def test_snf_algebraic_properties_and_divisibility():
    """Validates SNF decomposition properties: S = P*B*Q, unimodular P and Q, divisibility d_i | d_{i+1}."""
    # Diagonal gcd reduction: diag(2, 3) must yield [1, 6]
    M_gcd = [[2, 0], [0, 3]]
    rec_gcd = SmithNormalForm.decompose(M_gcd)
    assert rec_gcd.invariant_factors == [1, 6]
    assert rec_gcd.is_valid_decomposition
    assert abs(rec_gcd.det_P) == 1 and abs(rec_gcd.det_Q) == 1

    # Zero matrices of varied dimensions
    for m, n in [(0, 0), (3, 0), (0, 3), (1, 1), (2, 5), (5, 2)]:
        M_zero = [[0] * n for _ in range(m)]
        rec_zero = SmithNormalForm.decompose(M_zero)
        assert rec_zero.rank == 0
        assert rec_zero.is_valid_decomposition

    # 30 Random matrices
    rng = random.Random(54321)
    for _ in range(30):
        m = rng.randint(1, 5)
        n = rng.randint(1, 5)
        M = [[rng.randint(-12, 12) for _ in range(n)] for _ in range(m)]
        rec = SmithNormalForm.decompose(M)
        assert rec.is_valid_decomposition
        assert rec.divisibility_satisfied
        assert abs(rec.det_P) == 1
        assert abs(rec.det_Q) == 1
        for i in range(len(rec.invariant_factors) - 1):
            assert rec.invariant_factors[i + 1] % rec.invariant_factors[i] == 0
