"""Regge climb tests. Stdlib. No illegal imports. AuthorityEffect: None."""

from __future__ import annotations

import ast
from pathlib import Path

from regge_climb import (
    Q2,
    Q,
    SuperPair,
    climb_report,
    count_admissible_tetras,
    d0,
    d1_d0_zero,
    q_squares_to_laplacian,
    regge_deficit_2d,
    su2_tetra_admissible,
    su3_extras_needed,
    u1_holonomy_from_deficit,
    vertex_laplacian,
)

ILLEGAL = (
    "numpy",
    "scipy",
    "sympy",
    "universe_anomalonica",
    "omega_engine",
    "torch",
    "tensorflow",
)


def _imported(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def test_regge_climb_has_no_illegal_imports() -> None:
    src = Path(__file__).resolve().parents[1] / "regge_climb.py"
    names = _imported(src)
    for banned in ILLEGAL:
        assert banned not in names


def test_regge_deficit_flat_and_k5() -> None:
    assert regge_deficit_2d(6) == (0, 3)
    assert regge_deficit_2d(5) == (1, 3)


def test_ponzano_regge_su2_on_tetrahedron() -> None:
    assert su2_tetra_admissible((2, 2, 2, 2, 2, 2))
    assert su2_tetra_admissible((2, 2, 2, 2, 2, 0))
    assert not su2_tetra_admissible((3, 0, 0, 0, 0, 0))
    assert not su2_tetra_admissible((4, 1, 1, 0, 0, 0))
    ok, total = count_admissible_tetras(1)
    assert total == 2**6
    assert 0 < ok < total


def test_u1_holonomy_from_deficit() -> None:
    assert u1_holonomy_from_deficit(0) == 0
    assert u1_holonomy_from_deficit(1) == 1
    assert u1_holonomy_from_deficit(6) == 0
    assert u1_holonomy_from_deficit(7) == 1
    try:
        u1_holonomy_from_deficit(1, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("nonpositive periods must be refused")


def test_su3_is_available_only_after_extras() -> None:
    extras = su3_extras_needed()
    assert extras["hermitian_form"] is True
    assert extras["unit_determinant"] is True
    assert extras["adjoint_eight_from_vertex_count"] is False


def test_d_squared_zero_on_filled_triangle() -> None:
    assert d1_d0_zero((1, 2, 3))
    assert d1_d0_zero((0, 0, 0))
    assert d0((1, 1, 1)) == (0, 0, 0)


def test_witten_q_squares_to_laplacian() -> None:
    for even in ((1, 0, 0), (1, -1, 0), (2, 3, -5)):
        for odd in ((0, 0, 0), (1, 1, -2), (4, -1, 0)):
            pair = SuperPair(even, odd)
            assert q_squares_to_laplacian(pair)
            twice = Q2(pair)
            assert twice.even == vertex_laplacian(even)


def test_q_is_not_zero_and_is_odd() -> None:
    pair = SuperPair((1, 0, 0), (0, 0, 0))
    once = Q(pair)
    assert once.odd == d0((1, 0, 0))
    assert once.odd != (0, 0, 0)
    assert once.even == (0, 0, 0)


def test_climb_report_does_not_claim_mssm_or_forced_su3() -> None:
    r = climb_report()
    assert r["is_mssm"] is False
    assert r["is_su3_forced"] is False
    assert r["su2_label_fixture_admissible"] is True
    assert r["cyclic_phase_from_deficit"] is True
    assert r["u1_embedding_constructed"] is False
    assert r["graph_supercharge_identity"] is True
    assert r["physical_susy_identification"] is False
    assert r["q2_is_laplacian"] is True
    assert r["su2_regular_tetra"] is True
    assert r["authority_effect"] == "None"
