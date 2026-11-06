"""Regge wall α hunt. Stdlib. No illegal imports. AuthorityEffect: None."""

from __future__ import annotations

import ast
import math
from pathlib import Path

from regge_alpha_wall import (
    QED_ALPHA_INV,
    QED_ALPHA_INV_SOURCE,
    alpha_inv_4pi_over_D,
    alpha_inv_pi_poly,
    eight_pi_cubed,
    hex_wall_deficit_radians,
    hex_wall_deficit_units,
    hex_wall_report,
    l1_unity,
    observer_series_D_over_n_nplus1,
    transform_248_to_137,
    w_obstruction_removal,
)

ILLEGAL = (
    "numpy",
    "scipy",
    "sympy",
    "universe_anomalonica",
    "omega_engine",
)


def test_no_illegal_imports() -> None:
    src = Path(__file__).resolve().parents[1] / "regge_alpha_wall.py"
    tree = ast.parse(src.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    for banned in ILLEGAL:
        assert banned not in names


def test_two_pi_cubed_is_the_245_memory() -> None:
    raw = eight_pi_cubed()
    assert 247 < raw < 249
    t = transform_248_to_137()
    assert t["remembered_as"] == 245
    assert t["is_qed_theorem"] is False


def test_pi_poly_sits_on_137_but_is_not_qed() -> None:
    poly = alpha_inv_pi_poly()
    assert abs(poly - QED_ALPHA_INV) < 5e-4
    assert abs(poly - QED_ALPHA_INV) > 1e-5
    t = transform_248_to_137()
    assert abs(t["alpha_inv_poly"] - poly) < 1e-12
    assert abs(t["half"] + t["triangle_pi_sq_plus_pi"] - poly) < 1e-12
    assert t["formula_selected_post_hoc"] is True
    assert t["wall_selects_formula"] is False
    assert t["qed_alpha_inv_source"] == QED_ALPHA_INV_SOURCE


def test_old_4pi_over_D_overshoots() -> None:
    old = alpha_inv_4pi_over_D()
    assert 142 < old < 143
    assert old - QED_ALPHA_INV > 5


def test_flat_hex_wall_diverges_and_interior_is_zero() -> None:
    rep = hex_wall_report(5)
    assert rep["interior_k6_deficit"] == 0
    assert rep["diverges"] is True
    assert abs(rep["per_R_limit"] - 6 * math.pi) < 1e-12
    r1 = hex_wall_deficit_units(1)
    r2 = hex_wall_deficit_units(2)
    assert r1 == 24
    assert r2 == 42
    assert r2 > r1
    assert abs(hex_wall_deficit_radians(1) - 8 * math.pi) < 1e-9


def test_observer_D_series_sums_to_D_not_alpha() -> None:
    s = observer_series_D_over_n_nplus1(50)
    assert s["equals_alpha"] is False
    assert abs(s["partial"] - s["limit_D"]) < 0.03
    assert s["limit_D"] < 0.1


def test_l1_weights_are_unity() -> None:
    assert abs(w_obstruction_removal(1) - 0.5) < 1e-12
    assert abs(w_obstruction_removal(2) - 1.0 / 6.0) < 1e-12
    u = l1_unity(2000)
    assert abs(u["sum_w_l1"] - 1.0) < 1e-3
    assert u["sum_w_l1_limit"] == 1.0
    assert abs(u["leak_after_l1_unity"] - (1.0 - 9.0 / (math.pi**2))) < 1e-12
    assert u["capacity_ansatz"] == "1/n"
    assert u["capacity_ansatz_derived"] is False
    assert u["born_rule_derived"] is False
    assert u["is_qed"] is False
    assert abs(u["sum_born_limit"] - math.pi**2 / 6.0) < 1e-12
    assert u["sum_born_limit"] > 1.0
