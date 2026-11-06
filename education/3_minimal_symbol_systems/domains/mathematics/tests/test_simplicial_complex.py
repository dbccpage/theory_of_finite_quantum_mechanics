"""
Comprehensive Tests & Negative Controls for Simplicial Complex & Boundary Nilpotency
AuthorityEffect: None
"""

import numpy as np
import pytest
from domain_mathematics_kernel import (
    DomainEngine,
    Simplex0,
    Simplex1,
    Simplex2,
    SimplicialComplex,
)


def test_simplex0_validity():
    """Vertex validity: non-empty vertex ID accepted, empty string rejected."""
    v = Simplex0("v1")
    assert v.id == "v1"

    with pytest.raises(ValueError, match="Vertex id cannot be empty"):
        Simplex0("")


def test_simplex1_irrefl_and_reversal():
    """1-simplex irreflexivity and transposition boundary sign inversion."""
    e = Simplex1(src="u", dst="v")
    assert e.src == "u" and e.dst == "v"

    # Transposition / reversal
    e_rev = e.reversal()
    assert e_rev.src == "v" and e_rev.dst == "u"

    b_orig = e.boundary()
    b_rev = e_rev.boundary()
    assert b_orig == {"v": 1, "u": -1}
    assert b_rev == {"u": 1, "v": -1}

    # Verify sign inversion: partial_1(sigma(e)) == -partial_1(e)
    for pt in ["u", "v"]:
        assert b_rev[pt] == -b_orig[pt]

    # Negative control: self-loop rejected by irreflexivity
    with pytest.raises(ValueError, match="Degenerate 1-simplex rejected"):
        Simplex1(src="x", dst="x")


def test_simplex2_alternating_sum():
    """2-simplex oriented boundary edges."""
    t = Simplex2(v0="a", v1="b", v2="c")
    b_edges = t.boundary_edges()
    expected = [(1, ("b", "c")), (-1, ("a", "c")), (1, ("a", "b"))]
    assert b_edges == expected

    # Negative control: non-distinct vertices rejected
    with pytest.raises(ValueError, match="Degenerate 2-simplex rejected"):
        Simplex2(v0="a", v1="a", v2="b")

    with pytest.raises(ValueError, match="Degenerate 2-simplex rejected"):
        Simplex2(v0="a", v1="b", v2="a")


def test_boundary_nilpotency_triangle():
    """Single 2-simplex boundary closure: B_1 * B_2 = 0."""
    sc = SimplicialComplex()
    sc.add_triangle("a", "b", "c")

    b1 = sc.boundary_matrix_d1()
    b2 = sc.boundary_matrix_d2()
    assert len(b1) == 3  # 3 vertices
    assert len(b1[0]) == 3  # 3 edges
    assert len(b2) == 3  # 3 edges
    assert len(b2[0]) == 1  # 1 triangle

    is_nilpotent, product = sc.compute_boundary_nilpotency()
    assert is_nilpotent is True
    assert np.all(np.array(product) == 0)


def test_boundary_nilpotency_tetrahedron_shell():
    """Tetrahedron boundary shell (2-sphere S^2): 4 vertices, 6 edges, 4 triangles."""
    sc = SimplicialComplex()
    # 4 faces of a tetrahedron
    sc.add_triangle("v0", "v1", "v2")
    sc.add_triangle("v0", "v1", "v3")
    sc.add_triangle("v1", "v2", "v3")
    sc.add_triangle("v0", "v2", "v3")

    assert len(sc.vertices) == 4
    assert len(sc.edges) == 6
    assert len(sc.triangles) == 4

    is_nilpotent, product = sc.compute_boundary_nilpotency()
    assert is_nilpotent is True
    assert np.all(np.array(product) == 0)
    assert sc.euler_characteristic() == 4 - 6 + 4  # chi = 2 for S^2


def test_boundary_nilpotency_shared_edge_mesh():
    """Planar mesh with shared edge: 4 vertices, 5 edges, 2 triangles."""
    sc = SimplicialComplex()
    sc.add_triangle("v0", "v1", "v2")
    sc.add_triangle("v1", "v2", "v3")

    assert len(sc.vertices) == 4
    assert len(sc.edges) == 5
    assert len(sc.triangles) == 2

    is_nilpotent, product = sc.compute_boundary_nilpotency()
    assert is_nilpotent is True
    assert np.all(np.array(product) == 0)
    assert sc.euler_characteristic() == 4 - 5 + 2  # chi = 1 (topological disk)


def test_euler_characteristic_invariants():
    """Topological Euler characteristic invariants: chi = n0 - n1 + n2."""
    # Single triangle: 3 vertices, 3 edges, 1 face -> chi = 1
    sc1 = SimplicialComplex()
    sc1.add_triangle("a", "b", "c")
    assert sc1.euler_characteristic() == 1

    # 1-cycle (boundary of triangle, no face): 3 vertices, 3 edges, 0 faces -> chi = 0
    sc2 = SimplicialComplex()
    sc2.add_edge("a", "b")
    sc2.add_edge("b", "c")
    sc2.add_edge("c", "a")
    assert sc2.euler_characteristic() == 0

    # Tetrahedron shell (S^2): chi = 2
    sc3 = SimplicialComplex()
    sc3.add_triangle("v0", "v1", "v2")
    sc3.add_triangle("v0", "v1", "v3")
    sc3.add_triangle("v1", "v2", "v3")
    sc3.add_triangle("v0", "v2", "v3")
    assert sc3.euler_characteristic() == 2


def test_tampered_boundary_operator_negative_control():
    """Negative Control: Tampered non-alternating signs violate nilpotency."""
    sc = SimplicialComplex()
    sc.add_triangle("v0", "v1", "v2")

    b1 = np.array(sc.boundary_matrix_d1(), dtype=np.int64)
    # Deliberately malformed B2 with all +1 signs (no alternating cancellation)
    malformed_b2 = np.array([[1], [1], [1]], dtype=np.int64)

    tampered_prod = np.dot(b1, malformed_b2)
    assert not np.all(tampered_prod == 0), "Tampered non-alternating boundary must fail nilpotency"
    assert np.any(tampered_prod != 0), "Non-zero residual must be present"


def test_degenerate_simplices_negative_control():
    """Negative Control: Degenerate self-loops and non-distinct vertices are rejected."""
    sc = SimplicialComplex()
    with pytest.raises(ValueError, match="Self-loop edge"):
        sc.add_edge("a", "a")

    with pytest.raises(ValueError, match="pairwise distinct"):
        sc.add_triangle("a", "b", "a")


def test_domain_engine_boundary_closure():
    """DomainEngine boundary closure evaluation using exact matrix multiplication."""
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_alpha", "pt_beta")
    engine.step_03_enforce_irrefl()

    # Automatic canonical 2-simplex synthesis
    assert engine.evaluate_boundary_closure() is True
    assert engine.state.invariants["boundary_nilpotence"] is True

    # Custom multi-triangle complex evaluation
    custom_sc = SimplicialComplex()
    custom_sc.add_triangle("v0", "v1", "v2")
    custom_sc.add_triangle("v1", "v2", "v3")
    assert engine.evaluate_boundary_closure(custom_complex=custom_sc) is True
