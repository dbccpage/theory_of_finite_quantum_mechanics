"""
Adversarial Stress Test Suite: Simplicial Complexes & Boundary Nilpotency (B_1 * B_2 = 0)
AuthorityEffect: None

Tests boundary nilpotency B_1 * B_2 = 0 and input rejection invariants across:
1. Standard 2D triangulations (disks, cylinders, spheres, tori, Klein bottles, RP^2, random planar Delaunay).
2. Degenerate triangulations (pinched vertices, self-edges, inverted triangles, non-manifold books, isolated simplices).
3. Permutation & ordering invariance (arbitrary shuffling of vertices, edges, triangles, and edge basis reversals).
4. Cross-kernel equivalence between Domain 2 (Pure Math) and Domain 1 (Theoretical Physics).
"""

import random
import sys
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pytest
from scipy.spatial import Delaunay

# Ensure both math and physics code are on sys.path
_test_dir = Path(__file__).resolve().parent
_tower_root = _test_dir.parents[1]
_math_code = _tower_root / "mathematics" / "code"
_phys_code = _tower_root / "physics" / "code"

for p in [str(_math_code), str(_phys_code)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import domain_mathematics_kernel as dmk
import domain_physics_kernel as dpk

# ==============================================================================
# 1. TRIANGULATION GENERATORS
# ==============================================================================


def generate_disk_fan(
    num_perimeter: int = 6,
) -> Tuple[List[str], List[Tuple[str, str]], List[Tuple[str, str, str]]]:
    """Triangulated 2D disk with 1 central vertex and N perimeter vertices."""
    center = "v_center"
    perimeter = [f"v_perim_{i}" for i in range(num_perimeter)]
    vertices = [center] + perimeter
    faces = []
    edges_set = set()

    for i in range(num_perimeter):
        v1 = perimeter[i]
        v2 = perimeter[(i + 1) % num_perimeter]
        faces.append((center, v1, v2))
        edges_set.add((center, v1))
        edges_set.add((center, v2))
        edges_set.add((v1, v2))

    return vertices, list(edges_set), faces


def generate_cylinder(
    num_circ: int = 6, num_height: int = 3
) -> Tuple[List[str], List[Tuple[str, str]], List[Tuple[str, str, str]]]:
    """Triangulated topological cylinder S^1 x [0, 1]."""
    vertices = [f"v_{h}_{c}" for h in range(num_height) for c in range(num_circ)]
    faces = []
    edges_set = set()

    for h in range(num_height - 1):
        for c in range(num_circ):
            c_next = (c + 1) % num_circ
            v00 = f"v_{h}_{c}"
            v01 = f"v_{h}_{c_next}"
            v10 = f"v_{h + 1}_{c}"
            v11 = f"v_{h + 1}_{c_next}"

            # Two triangles per quad cell
            faces.append((v00, v01, v11))
            faces.append((v00, v11, v10))

            for u, v in [(v00, v01), (v01, v11), (v00, v11), (v11, v10), (v00, v10)]:
                edges_set.add((u, v) if (v, u) not in edges_set else (v, u))

    return vertices, list(edges_set), faces


def generate_sphere_tetrahedron() -> Tuple[
    List[str], List[Tuple[str, str]], List[Tuple[str, str, str]]
]:
    """Tetrahedron shell (boundary of 3-simplex, S^2)."""
    vertices = ["v0", "v1", "v2", "v3"]
    faces = [("v0", "v1", "v2"), ("v0", "v2", "v3"), ("v0", "v3", "v1"), ("v1", "v3", "v2")]
    edges_set = set()
    for v0, v1, v2 in faces:
        for u, v in [(v1, v2), (v0, v2), (v0, v1)]:
            if (v, u) not in edges_set:
                edges_set.add((u, v))
    return vertices, list(edges_set), faces


def generate_sphere_octahedron() -> Tuple[
    List[str], List[Tuple[str, str]], List[Tuple[str, str, str]]
]:
    """Regular octahedron shell (S^2)."""
    vertices = ["top", "bottom", "p0", "p1", "p2", "p3"]
    faces = [
        ("top", "p0", "p1"),
        ("top", "p1", "p2"),
        ("top", "p2", "p3"),
        ("top", "p3", "p0"),
        ("bottom", "p1", "p0"),
        ("bottom", "p2", "p1"),
        ("bottom", "p3", "p2"),
        ("bottom", "p0", "p3"),
    ]
    edges_set = set()
    for v0, v1, v2 in faces:
        for u, v in [(v1, v2), (v0, v2), (v0, v1)]:
            if (v, u) not in edges_set:
                edges_set.add((u, v))
    return vertices, list(edges_set), faces


def generate_sphere_icosahedron() -> Tuple[
    List[str], List[Tuple[str, str]], List[Tuple[str, str, str]]
]:
    """Regular icosahedron shell (S^2, 12 vertices, 30 edges, 20 faces)."""
    (1.0 + np.sqrt(5.0)) / 2.0
    vertices = [f"ico_{i}" for i in range(12)]
    faces_idx = [
        (0, 11, 5),
        (0, 5, 1),
        (0, 1, 7),
        (0, 7, 10),
        (0, 10, 11),
        (1, 5, 9),
        (5, 11, 4),
        (11, 10, 2),
        (10, 7, 6),
        (7, 1, 8),
        (3, 9, 4),
        (3, 4, 2),
        (3, 2, 6),
        (3, 6, 8),
        (3, 8, 9),
        (4, 9, 5),
        (2, 4, 11),
        (6, 2, 10),
        (8, 6, 7),
        (9, 8, 1),
    ]
    faces = [(f"ico_{a}", f"ico_{b}", f"ico_{c}") for a, b, c in faces_idx]
    edges_set = set()
    for v0, v1, v2 in faces:
        for u, v in [(v1, v2), (v0, v2), (v0, v1)]:
            if (v, u) not in edges_set:
                edges_set.add((u, v))
    return vertices, list(edges_set), faces


def generate_torus(
    nx: int = 4, ny: int = 4
) -> Tuple[List[str], List[Tuple[str, str]], List[Tuple[str, str, str]]]:
    """Triangulated flat torus T^2 (periodic boundary conditions, chi = 0)."""
    vertices = [f"t_{x}_{y}" for x in range(nx) for y in range(ny)]
    faces = []
    edges_set = set()

    for x in range(nx):
        for y in range(ny):
            x_next = (x + 1) % nx
            y_next = (y + 1) % ny
            v00 = f"t_{x}_{y}"
            v10 = f"t_{x_next}_{y}"
            v01 = f"t_{x}_{y_next}"
            v11 = f"t_{x_next}_{y_next}"

            faces.append((v00, v10, v11))
            faces.append((v00, v11, v01))

            for u, v in [(v00, v10), (v10, v11), (v00, v11), (v11, v01), (v00, v01)]:
                if (v, u) not in edges_set:
                    edges_set.add((u, v))

    return vertices, list(edges_set), faces


def generate_mobius_strip(
    num_segments: int = 6,
) -> Tuple[List[str], List[Tuple[str, str]], List[Tuple[str, str, str]]]:
    """Triangulated Mobius strip with half-twist identification at endpoints."""
    # Top vertices: t_0 ... t_{N-1}, Bottom vertices: b_0 ... b_{N-1}
    # Twist: t_N -> b_0, b_N -> t_0
    vertices = [f"t_{i}" for i in range(num_segments)] + [f"b_{i}" for i in range(num_segments)]
    faces = []
    edges_set = set()

    for i in range(num_segments):
        t_curr = f"t_{i}"
        b_curr = f"b_{i}"
        if i < num_segments - 1:
            t_next = f"t_{i + 1}"
            b_next = f"b_{i + 1}"
        else:
            # Half-twist: top connects to bottom, bottom connects to top
            t_next = "b_0"
            b_next = "t_0"

        faces.append((b_curr, t_curr, t_next))
        faces.append((b_curr, t_next, b_next))

        for u, v in [
            (b_curr, t_curr),
            (t_curr, t_next),
            (b_curr, t_next),
            (t_next, b_next),
            (b_curr, b_next),
        ]:
            if (v, u) not in edges_set:
                edges_set.add((u, v))

    return vertices, list(edges_set), faces


def generate_projective_plane_rp2() -> Tuple[
    List[str], List[Tuple[str, str]], List[Tuple[str, str, str]]
]:
    """Minimal 6-vertex triangulation of the Real Projective Plane RP^2 (10 faces, 15 edges)."""
    vertices = [f"rp_{i}" for i in range(1, 7)]
    # Standard 6-vertex RP^2 (Boy-Apéry minimal embedding):
    faces = [
        ("rp_1", "rp_2", "rp_4"),
        ("rp_2", "rp_3", "rp_5"),
        ("rp_3", "rp_1", "rp_6"),
        ("rp_1", "rp_5", "rp_6"),
        ("rp_2", "rp_6", "rp_4"),
        ("rp_3", "rp_4", "rp_5"),
        ("rp_4", "rp_6", "rp_5"),
        ("rp_1", "rp_4", "rp_5"),
        ("rp_2", "rp_5", "rp_6"),
        ("rp_3", "rp_6", "rp_4"),
    ]
    edges_set = set()
    for v0, v1, v2 in faces:
        for u, v in [(v1, v2), (v0, v2), (v0, v1)]:
            if (v, u) not in edges_set:
                edges_set.add((u, v))
    return vertices, list(edges_set), faces


def generate_random_planar_delaunay(
    num_points: int = 25, seed: int = 42
) -> Tuple[List[str], List[Tuple[str, str]], List[Tuple[str, str, str]]]:
    """Generates random 2D Delaunay triangulation."""
    rng = np.random.default_rng(seed)
    points = rng.uniform(-1.0, 1.0, size=(num_points, 2))
    tri = Delaunay(points)

    vertices = [f"d_{i}" for i in range(num_points)]
    faces = [(f"d_{a}", f"d_{b}", f"d_{c}") for a, b, c in tri.simplices]

    edges_set = set()
    for v0, v1, v2 in faces:
        for u, v in [(v1, v2), (v0, v2), (v0, v1)]:
            if (v, u) not in edges_set:
                edges_set.add((u, v))

    return vertices, list(edges_set), faces


# ==============================================================================
# 2. ADVERSARIAL STRESS TESTS: ARBITRARY 2D TOPOLOGICAL TRIANGULATIONS
# ==============================================================================


@pytest.mark.parametrize(
    "generator, name",
    [
        (lambda: generate_disk_fan(8), "Disk Fan N=8"),
        (lambda: generate_disk_fan(24), "Disk Fan N=24"),
        (lambda: generate_cylinder(6, 4), "Cylinder 6x4"),
        (lambda: generate_cylinder(12, 3), "Cylinder 12x3"),
        (generate_sphere_tetrahedron, "Sphere Tetrahedron"),
        (generate_sphere_octahedron, "Sphere Octahedron"),
        (generate_sphere_icosahedron, "Sphere Icosahedron"),
        (lambda: generate_torus(4, 4), "Torus 4x4"),
        (lambda: generate_torus(6, 6), "Torus 6x6"),
        (lambda: generate_mobius_strip(8), "Mobius Strip N=8"),
        (generate_projective_plane_rp2, "Projective Plane RP^2"),
        (lambda: generate_random_planar_delaunay(20, seed=101), "Delaunay N=20"),
        (lambda: generate_random_planar_delaunay(50, seed=202), "Delaunay N=50"),
        (lambda: generate_random_planar_delaunay(100, seed=303), "Delaunay N=100"),
    ],
)
def test_arbitrary_2d_triangulations_nilpotency(generator, name):
    """
    Stress-tests B_1 * B_2 = 0 on arbitrary 2D triangulations across both
    Pure Mathematics SimplicialComplex and Physics DomainEngine.
    """
    vertices, edges, faces = generator()

    # 1. Test Domain 2 (Pure Math) SimplicialComplex
    complex_math = dmk.SimplicialComplex()
    for v in vertices:
        complex_math.add_vertex(v)
    for u, v in edges:
        complex_math.add_edge(u, v)
    for v0, v1, v2 in faces:
        complex_math.add_triangle(v0, v1, v2)

    is_nilpotent_math, prod_math = complex_math.compute_boundary_nilpotency()
    assert is_nilpotent_math is True, f"Boundary nilpotency failed in Math kernel on {name}"
    prod_math_np = np.array(prod_math, dtype=np.int64)
    assert np.all(prod_math_np == 0), f"Non-zero entry in Math kernel B_1*B_2 on {name}"

    # 2. Test Domain 1 (Physics) DomainEngine
    engine_phys = dpk.DomainEngine()
    receipt = engine_phys.evaluate_simplicial_boundary_matrices(vertices, edges, faces)
    assert receipt.is_nilpotent is True, f"Boundary nilpotency failed in Physics kernel on {name}"
    assert np.all(np.array(receipt.product_matrix) == 0), (
        f"Non-zero entry in Physics kernel B_1*B_2 on {name}"
    )
    assert receipt.authority_effect == "None"


# ==============================================================================
# 3. ADVERSARIAL STRESS TESTS: DEGENERATE & EDGE CASE TRIANGULATIONS
# ==============================================================================


def test_pinched_topological_singularities():
    """
    Pinched singularities:
    1. Bowtie: Two triangles sharing exactly one vertex (v_pinch).
    2. Wedge of two spheres (S^2 v S^2) sharing a single vertex.
    Verifies that topological singularities do not break homological nilpotency B_1*B_2 = 0.
    """
    # 1. Bowtie
    complex_bowtie = dmk.SimplicialComplex()
    complex_bowtie.add_triangle("p", "a1", "a2")
    complex_bowtie.add_triangle("p", "b1", "b2")
    is_nil, prod = complex_bowtie.compute_boundary_nilpotency()
    assert is_nil is True
    assert np.all(np.array(prod) == 0)

    # 2. Wedge of two octahedron spheres glued at "pinch"
    v_s1, e_s1, f_s1 = generate_sphere_octahedron()
    v_s2, e_s2, f_s2 = generate_sphere_octahedron()

    # Rename s1 and s2 vertices, identifying "top" as "pinch"
    def rename_v(v, prefix):
        return "pinch" if v == "top" else f"{prefix}_{v}"

    wedge_vertices = (
        ["pinch"]
        + [f"s1_{v}" for v in v_s1 if v != "top"]
        + [f"s2_{v}" for v in v_s2 if v != "top"]
    )
    wedge_faces = [
        (rename_v(a, "s1"), rename_v(b, "s1"), rename_v(c, "s1")) for a, b, c in f_s1
    ] + [(rename_v(a, "s2"), rename_v(b, "s2"), rename_v(c, "s2")) for a, b, c in f_s2]
    wedge_edges = set()
    for a, b, c in wedge_faces:
        for u, v in [(b, c), (a, c), (a, b)]:
            if (v, u) not in wedge_edges:
                wedge_edges.add((u, v))

    engine_phys = dpk.DomainEngine()
    receipt = engine_phys.evaluate_simplicial_boundary_matrices(
        wedge_vertices, list(wedge_edges), wedge_faces
    )
    assert receipt.is_nilpotent is True
    assert np.all(np.array(receipt.product_matrix) == 0)


def test_non_manifold_book_of_triangles():
    """
    Non-manifold complex: K triangles sharing a single common spine edge (spine_a, spine_b).
    Verifies B_1 * B_2 = 0 holds even when the space fails to be a manifold.
    """
    k_pages = 7
    complex_book = dmk.SimplicialComplex()
    for i in range(k_pages):
        complex_book.add_triangle("spine_a", "spine_b", f"page_{i}")

    is_nil, prod = complex_book.compute_boundary_nilpotency()
    assert is_nil is True
    assert np.all(np.array(prod) == 0)


def test_inverted_triangles_and_all_permutation_orientations():
    """
    Tests that B_1 * B_2 = 0 holds regardless of triangle orientation:
    - 3 cyclic (even) permutations: (0, 1, 2), (1, 2, 0), (2, 0, 1)
    - 3 acyclic (odd) permutations: (1, 0, 2), (0, 2, 1), (2, 1, 0)
    All 6 orientations must satisfy exact nilpotency.
    """
    perms = [
        ("x0", "x1", "x2"),
        ("x1", "x2", "x0"),
        ("x2", "x0", "x1"),
        ("x1", "x0", "x2"),
        ("x0", "x2", "x1"),
        ("x2", "x1", "x0"),
    ]
    for perm in perms:
        comp = dmk.SimplicialComplex()
        comp.add_triangle(*perm)
        is_nil, prod = comp.compute_boundary_nilpotency()
        assert is_nil is True, f"Failed on triangle orientation: {perm}"
        assert np.all(np.array(prod) == 0)


def test_disconnected_and_isolated_simplices():
    """
    Tests complexes containing disconnected components, isolated vertices,
    and isolated edges without attached faces.
    """
    comp = dmk.SimplicialComplex()
    # 5 isolated vertices
    for i in range(5):
        comp.add_vertex(f"iso_v_{i}")
    # 3 isolated edges
    comp.add_edge("e1_a", "e1_b")
    comp.add_edge("e2_a", "e2_b")
    comp.add_edge("e3_a", "e3_b")
    # 2 disjoint triangles
    comp.add_triangle("t1_0", "t1_1", "t1_2")
    comp.add_triangle("t2_0", "t2_1", "t2_2")

    is_nil, prod = comp.compute_boundary_nilpotency()
    assert is_nil is True
    assert np.all(np.array(prod) == 0)


def test_degenerate_simplex_rejections():
    """
    Verifies that degenerate and illegal inputs are rejected with explicit exceptions:
    1. Simplex0 with empty ID.
    2. Simplex1 with self-loop edge.
    3. Simplex2 with non-distinct vertices.
    4. SimplicialComplex.add_edge with self-loop.
    5. SimplicialComplex.add_triangle with non-distinct vertices.
    6. Physics evaluate_simplicial_boundary_matrices with missing face boundary edge.
    """
    # 1. Empty vertex id
    with pytest.raises(ValueError, match="Vertex id cannot be empty"):
        dmk.Simplex0(id="")

    # 2. Self-loop edge in Simplex1
    with pytest.raises(ValueError, match="Degenerate 1-simplex rejected"):
        dmk.Simplex1(src="node_a", dst="node_a")

    # 3. Duplicate vertices in Simplex2
    with pytest.raises(ValueError, match="Degenerate 2-simplex rejected"):
        dmk.Simplex2(v0="a", v1="a", v2="b")
    with pytest.raises(ValueError, match="Degenerate 2-simplex rejected"):
        dmk.Simplex2(v0="a", v1="b", v2="a")
    with pytest.raises(ValueError, match="Degenerate 2-simplex rejected"):
        dmk.Simplex2(v0="a", v1="a", v2="a")

    # 4. Self-loop in complex
    comp = dmk.SimplicialComplex()
    with pytest.raises(ValueError, match="Self-loop edge"):
        comp.add_edge("a", "a")

    # 5. Degenerate triangle in complex
    with pytest.raises(ValueError, match="Triangle vertices must be pairwise distinct"):
        comp.add_triangle("x", "x", "y")
    with pytest.raises(ValueError, match="Triangle vertices must be pairwise distinct"):
        comp.add_triangle("x", "y", "y")

    # 6. Missing face boundary edge in physics engine
    engine = dpk.DomainEngine()
    with pytest.raises(KeyError, match="Face boundary edge .* missing"):
        engine.evaluate_simplicial_boundary_matrices(
            vertices=["a", "b", "c"],
            edges=[("a", "b")],  # Missing ("b", "c") and ("a", "c")
            faces=[("a", "b", "c")],
        )


# ==============================================================================
# 4. ADVERSARIAL STRESS TESTS: PERMUTATION & ORDERING INVARIANCE
# ==============================================================================


@pytest.mark.parametrize("trial", range(15))
def test_full_permutation_and_basis_reversal_invariance(trial):
    """
    Adversarial stress test: B_1 * B_2 = 0 must be 100% invariant under:
    1. Arbitrary shuffling of vertex ordering.
    2. Arbitrary shuffling of edge ordering.
    3. Arbitrary shuffling of face ordering.
    4. Arbitrary flipping of basis edge orientations (u, v) -> (v, u).
    """
    rng = random.Random(42000 + trial)
    vertices, edges, faces = generate_sphere_icosahedron()

    # 1. Invert random edge orientations in the basis
    transformed_edges = []
    for u, v in edges:
        if rng.random() > 0.5:
            transformed_edges.append((v, u))
        else:
            transformed_edges.append((u, v))

    # 2. Shuffle vertices, edges, faces independently
    rng.shuffle(vertices)
    rng.shuffle(transformed_edges)
    rng.shuffle(faces)

    # Verify Domain 1 (Physics)
    engine_phys = dpk.DomainEngine()
    receipt = engine_phys.evaluate_simplicial_boundary_matrices(vertices, transformed_edges, faces)
    assert receipt.is_nilpotent is True, f"Physics kernel nilpotency failed on trial {trial}"
    assert np.all(np.array(receipt.product_matrix) == 0)

    # Verify Domain 2 (Pure Math)
    complex_math = dmk.SimplicialComplex()
    for v in vertices:
        complex_math.add_vertex(v)
    for u, v in transformed_edges:
        complex_math.add_edge(u, v)
    for v0, v1, v2 in faces:
        complex_math.add_triangle(v0, v1, v2)

    is_nil_math, prod_math = complex_math.compute_boundary_nilpotency()
    assert is_nil_math is True, f"Math kernel nilpotency failed on trial {trial}"
    assert np.all(np.array(prod_math) == 0)


# ==============================================================================
# 5. SCALE & STRESS BENCHMARK
# ==============================================================================


def test_large_scale_triangulation_boundary_nilpotency():
    """
    Large-scale stress test: Delaunay triangulation with 300 points,
    yielding ~900 edges and ~600 faces.
    Verifies that exact integer matrix multiplication scales and remains identically zero.
    """
    vertices, edges, faces = generate_random_planar_delaunay(num_points=300, seed=999)

    engine_phys = dpk.DomainEngine()
    receipt = engine_phys.evaluate_simplicial_boundary_matrices(vertices, edges, faces)
    assert receipt.is_nilpotent is True
    assert len(receipt.vertices) == 300
    assert len(receipt.faces) > 500
    assert np.all(np.array(receipt.product_matrix) == 0)
    assert receipt.euler_characteristic == 1  # Topological disk chi = 1


# ==============================================================================
# 6. ADVERSARIAL VULNERABILITIES & FAILURE MODES (EMPIRICAL CHALLENGER FINDINGS)
# ==============================================================================


def test_mathematics_antiparallel_edge_deduplication_preserves_chi():
    comp = dmk.SimplicialComplex()
    comp.add_triangle("a", "b", "c")  # Boundary edges: (b, c), (a, c), (a, b)
    comp.add_triangle("c", "b", "d")  # Boundary edges: (b, d), (c, d), (c, b)

    assert len(comp.vertices) == 4
    assert len(comp.triangles) == 2

    # Verified deduplication: 5 basis edges instead of 6
    assert len(comp.edges) == 5
    assert ("b", "c") in comp.edges
    assert ("c", "b") not in comp.edges

    # Topological disk chi = |V| - |E| + |F| = 4 - 5 + 2 = 1
    assert comp.euler_characteristic() == 1

    # Boundary nilpotency B_1 * B_2 = 0 remains exact integer zero
    is_nil, prod = comp.compute_boundary_nilpotency()
    assert is_nil is True
    assert np.all(np.array(prod) == 0)


def test_physics_missing_vertex_raises_key_error():
    engine = dpk.DomainEngine()
    vertices = ["a", "b"]  # Vertex 'c' missing!
    edges = [("a", "b"), ("b", "c"), ("a", "c")]
    faces = [("a", "b", "c")]

    with pytest.raises(KeyError, match="Edge vertex 'c' missing from vertices list"):
        engine.evaluate_simplicial_boundary_matrices(vertices, edges, faces)


def test_physics_self_loop_silent_acceptance():
    """
    VULNERABILITY FINDING 3:
    In DomainEngine.evaluate_simplicial_boundary_matrices (domain_physics_kernel.py),
    self-loops in `edges` (e.g. ('a', 'a')) are not validated or rejected.
    b1[v_idx['a']][j] += 1 followed by -= 1 nets to 0, creating a zero column in B_1.
    If the caller supplies self-loops, the function silently accepts them instead of
    raising a ValueError as Simplex1 and SimplicialComplex do.
    """
    engine = dpk.DomainEngine()
    vertices = ["a", "b", "c"]
    edges = [("a", "a"), ("a", "b"), ("b", "c"), ("a", "c")]  # Contains self-loop ('a', 'a')
    faces = [("a", "b", "c")]

    # Silently accepted without ValueError
    receipt = engine.evaluate_simplicial_boundary_matrices(vertices, edges, faces)
    assert receipt.is_nilpotent is True
    # Column 0 of B_1 corresponds to self-loop and is identically zero
    assert [row[0] for row in receipt.b1_matrix] == [0, 0, 0]
