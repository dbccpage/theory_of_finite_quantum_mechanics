"""Regression: dict-path d1 (curl) must agree with the matrix path (build_face_boundary).

The master fixture stores the cyclic edge (2, 0) while the face (0, 1, 2)
traverses (0, 1), (1, 2), (2, 0). A 1-cochain is alternating -- h(v, u) = -h(u, v)
-- so a reversed-key read must flip sign, exactly as the incidence matrix does.
Before the repair the dict path read a reversed stored edge as absent: d1h = 1.5
against the matrix path's 0.7 on the same declared carrier, and d1(d0 f) != 0.
Two implementations on the same declared carrier must agree (falsifiability
criterion, 002_finite_obstruction_calculus / 000_primitive_axiomatics).

The engine surface moved since the original repair (PR #1879): the letter
classes (AR carrier, AT.f91 dict d1, AV.f95 matrix d1) were de-lettered into
``code/network_residual.py`` as ``Network``, ``curl``, and
``build_face_boundary``. Same theorem, current names.
"""
import numpy as np
import pytest

from omega_engine.crates.residuals.network_residual import (
    Network,
    build_face_boundary,
    curl,
    gradient,
)

MASTER = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (2, 0)], faces=[(0, 1, 2)])
MASTER_H1 = {(0, 1): 1.0, (1, 2): 0.5, (2, 0): -0.8}

MIXED = Network(
    nodes=[0, 1, 2, 3],
    edges=[(0, 1), (2, 1), (2, 0), (1, 3), (3, 2)],
    faces=[(0, 1, 2), (1, 3, 2)],
)


def _matrix_d1(c, h_1):
    """Coboundary via the incidence matrix: (d1 h)_f = (B^T h)_f, B = face boundary."""
    boundary = build_face_boundary(c)
    h_vec = np.zeros(len(c.edges))
    for idx, e in enumerate(c.edges):
        h_vec[idx] = h_1.get(e, 0.0)
    image = boundary.T @ h_vec
    return {f: float(image[j]) for j, f in enumerate(c.faces)}


def test_dict_d1_matches_matrix_d1_on_master_fixture():
    dict_d1 = curl(MASTER, MASTER_H1)
    matrix_d1 = _matrix_d1(MASTER, MASTER_H1)
    assert set(dict_d1) == set(matrix_d1)
    for face in matrix_d1:
        assert dict_d1[face] == pytest.approx(matrix_d1[face])
    assert dict_d1[(0, 1, 2)] == pytest.approx(0.7)


def test_dict_d1_matches_matrix_d1_on_mixed_orientation_carrier():
    h_1 = {(0, 1): 0.25, (2, 1): -1.5, (2, 0): 2.0, (1, 3): 0.75, (3, 2): -0.5}
    dict_d1 = curl(MIXED, h_1)
    matrix_d1 = _matrix_d1(MIXED, h_1)
    assert set(dict_d1) == set(matrix_d1)
    for face in matrix_d1:
        assert dict_d1[face] == pytest.approx(matrix_d1[face])


def test_reversed_key_reads_as_negated_value():
    dict_d1 = curl(MASTER, {(2, 0): -0.8})
    assert dict_d1[(0, 1, 2)] == pytest.approx(-0.8)


def test_d1_after_d0_vanishes_on_mixed_orientation_carrier():
    """d1(d0 f) = 0 even when stored edge orientations disagree with face traversal."""
    potentials = {0: 0.3, 1: -1.2, 2: 2.0, 3: 0.7}
    grad = gradient(MIXED, potentials)
    for _face, value in curl(MIXED, grad).items():
        assert value == pytest.approx(0.0, abs=1e-12)


