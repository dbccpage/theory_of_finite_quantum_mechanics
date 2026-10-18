"""Kill 3-2-1 uniqueness; measure L1 proximity to SM-gauge and SUSY extras.

Stdlib module under test. No universe_anomalonica, numpy, or omega_engine.
AuthorityEffect: None.
"""

from __future__ import annotations

import ast
from pathlib import Path

from l1_sm_susy_proximity import (
    FINITE_MENU,
    SM_GAUGE_EXTRAS,
    discrete_321_census,
    exact_implies_loop_sum_zero,
    features,
    grading_is_not_susy,
    group_by_name,
    l1,
    min_sm_distance,
    opposite_signs_do_not_cancel,
    phi_triangle,
    proximity_report,
    simplex_shadow,
    sm_distance,
    susy_extra_distance,
    triangle_grading,
    uniqueness_killed,
)

ILLEGAL_IMPORT_PREFIXES = (
    "numpy",
    "scipy",
    "sympy",
    "universe_anomalonica",
    "omega_engine",
    "torch",
    "tensorflow",
)


def test_module_has_no_illegal_imports() -> None:
    src_path = Path(__file__).resolve().parents[1] / "l1_sm_susy_proximity.py"
    tree = ast.parse(src_path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    for banned in ILLEGAL_IMPORT_PREFIXES:
        assert banned not in names, banned


def test_opposite_signs_do_not_cancel() -> None:
    assert opposite_signs_do_not_cancel()
    assert l1((1, -1)) == 2
    assert l1((1, -1)) != 0


def test_phi_vanishes_on_exact_and_not_on_inexact() -> None:
    assert phi_triangle((1, 1, -2)) == 0
    assert phi_triangle((1, 0, 0)) == 1
    assert phi_triangle((-100, 0, 100)) == 0
    assert phi_triangle((100, -40, -59)) == 1
    assert exact_implies_loop_sum_zero()


def test_321_uniqueness_is_false() -> None:
    assert uniqueness_killed()
    rows = discrete_321_census()
    assert len(rows) == len(FINITE_MENU) ** 3
    assert all(d > 0 for _, _, _, d in rows)
    names = {(a, b, c) for a, b, c, _ in rows}
    assert ("Z3", "Z2", "1") in names
    assert ("S3", "Z2", "1") in names
    assert ("Z3", "Z2", "1") != ("S3", "Z2", "1")


def test_named_sm_is_not_in_the_finite_menu() -> None:
    assert not any(g.name == "SU(3)" for g in FINITE_MENU)
    assert not any(g.name == "SU(2)" for g in FINITE_MENU)
    assert not any(g.name == "U(1)" for g in FINITE_MENU)
    min_d, winners = min_sm_distance()
    assert min_d >= 1
    assert SM_GAUGE_EXTRAS[6] == 1
    for a, b, c in winners:
        feat = features(group_by_name(a), group_by_name(b), group_by_name(c))
        assert feat[6] == 0


def test_simplex_shadow_is_close_but_not_sm() -> None:
    g2, g1, g0 = simplex_shadow()
    assert (g2.name, g1.name, g0.name) == ("Z3", "Z2", "1")
    d = sm_distance(features(g2, g1, g0))
    min_d, _ = min_sm_distance()
    assert d > 0
    assert d >= min_d


def test_grading_is_closer_to_susy_extras_but_is_not_susy() -> None:
    gr = triangle_grading()
    assert gr.d_raises_degree
    assert not gr.superbracket
    assert grading_is_not_susy(gr)
    graded = susy_extra_distance(1, 0, int(gr.equal_counting))
    ungraded = susy_extra_distance(0, 0, 0)
    assert graded < ungraded
    assert graded > 0


def test_proximity_report_refuses_derivation() -> None:
    report = proximity_report()
    assert report["authority_effect"] == "None"
    assert report["is_sm"] is False
    assert report["is_susy"] is False
    assert report["sm_l1_zero_exists"] is False
    assert report["uniqueness_killed"] is True
    assert report["min_sm_l1_over_finite_menu"] >= 1
    assert report["simplex_shadow_sm_l1"] >= 1
    assert report["susy_extra_l1_graded"] >= 1
    assert report["graded_closer_than_ungraded"] is True
    assert report["phi_inexact_example"] == 1


def _imported_top_levels(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def test_this_test_file_does_not_import_the_illegal_solver() -> None:
    names = _imported_top_levels(Path(__file__).resolve())
    for banned in ILLEGAL_IMPORT_PREFIXES:
        assert banned not in names
    assert "gauge_higgs_susy_derivation" not in names
