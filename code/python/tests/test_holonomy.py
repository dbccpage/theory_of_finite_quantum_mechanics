"""Tests for discrete cell complexes, connections, and holonomy."""

import pytest
from fractions import Fraction
from src.holonomy.holonomy_engine import (
    CellComplex,
    RationalMatrix,
    DiscreteConnection,
)


def test_cell_complex_euler_characteristic():
    # Triangle complex: V=3, E=3, F=1 => chi = 1
    cc = CellComplex()
    v0 = cc.add_vertex("A")
    v1 = cc.add_vertex("B")
    v2 = cc.add_vertex("C")
    assert len(cc.vertices) == 3

    e0 = cc.add_edge("A", "B")
    e1 = cc.add_edge("B", "C")
    e2 = cc.add_edge("C", "A")
    assert len(cc.edges) == 3

    f0 = cc.add_face("F0", ["A", "B", "C"])
    assert len(cc.faces) == 1
    assert cc.euler_characteristic == 1


def test_rational_matrix_inverse():
    # 2x2 matrix [[2, 1], [1, 1]]
    m = RationalMatrix.from_ints([[2, 1], [1, 1]])
    inv = m.inverse()
    prod = m.multiply(inv)
    id2 = RationalMatrix.identity(2)
    assert prod.equals(id2)
    assert m.trace() == Fraction(3)


def test_discrete_connection_edge_inversion():
    conn = DiscreteConnection(dim=2)
    # Set transport U(A, B) = [[1, 2], [0, 1]] (shear)
    u_ab = RationalMatrix.from_ints([[1, 2], [0, 1]])
    conn.set_connection("A", "B", u_ab)

    # Retrieval
    assert conn.get_step("A", "B").equals(u_ab)
    # Reverse step must satisfy U(B, A) = U(A, B)^-1
    u_ba = conn.get_step("B", "A")
    assert u_ab.multiply(u_ba).equals(RationalMatrix.identity(2))


def test_flat_and_curved_holonomy():
    cc = CellComplex()
    cc.add_vertex("A")
    cc.add_vertex("B")
    cc.add_vertex("C")
    cc.add_edge("A", "B")
    cc.add_edge("B", "C")
    cc.add_edge("C", "A")
    cc.add_face("triangle", ["A", "B", "C"])

    # Flat connection: all identity
    conn_flat = DiscreteConnection(dim=2)
    id2 = RationalMatrix.identity(2)
    conn_flat.set_connection("A", "B", id2)
    conn_flat.set_connection("B", "C", id2)
    conn_flat.set_connection("C", "A", id2)
    assert conn_flat.is_flat(cc)
    assert conn_flat.face_holonomy(cc.faces[0]).equals(id2)

    # Curved connection: non-commuting shears
    conn_curved = DiscreteConnection(dim=2)
    m1 = RationalMatrix.from_ints([[1, 1], [0, 1]])
    m2 = RationalMatrix.from_ints([[1, 0], [1, 1]])
    m3 = RationalMatrix.identity(2)
    conn_curved.set_connection("A", "B", m1)
    conn_curved.set_connection("B", "C", m2)
    conn_curved.set_connection("C", "A", m3)
    assert not conn_curved.is_flat(cc)
    holo = conn_curved.face_holonomy(cc.faces[0])
    assert not holo.equals(id2)
