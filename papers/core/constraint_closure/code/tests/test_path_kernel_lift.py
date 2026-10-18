"""Unique-path L1 vs many-path kernel vs χ=1. Stdlib. AuthorityEffect: None."""

from __future__ import annotations

import ast
import math
from pathlib import Path

from path_kernel_lift import (
    bond_growth_lower,
    bond_growth_window,
    compose_under_g1g2g3,
    declared_face_two_site_fixture,
    delta_eval,
    diamond_composition,
    g3_fail_local_green_global_red,
    hex_shell_paths,
    hex_shortest_path_count,
    join_report,
    local_green_global_red_hex,
    many_path_kernel,
    one_local_stays_chi1,
    path_kernel,
    two_site_forces_chi,
    unique_path_l1,
)

ILLEGAL = (
    "numpy",
    "scipy",
    "sympy",
    "universe_anomalonica",
    "omega_engine",
)


def test_no_illegal_imports() -> None:
    src = Path(__file__).resolve().parents[1] / "path_kernel_lift.py"
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
    assert names <= {"__future__", "math", "typing", "regge_alpha_wall"}


def test_unique_path_l1_is_unity() -> None:
    u = unique_path_l1(2000)
    assert u["g1_unique_decomposition"] is True
    assert u["n_paths_per_shell"] == 1
    assert u["kernel_is_a_sum"] is False
    assert abs(u["sum_w"] - 1.0) < 1e-3
    assert abs(u["w_1"] - 0.5) < 1e-12
    assert abs(u["w_2"] - 1.0 / 6.0) < 1e-12
    assert u["foc012_refuses_born"] is True
    assert u["born_requires_additional_structure"] is True
    assert u["born_derived_here"] is False
    assert u["sum_born_limit"] > 1.0
    assert u["is_qed"] is False


def test_many_path_kernel_is_a_sum() -> None:
    m = many_path_kernel(2, 2.0, beta=0.0)
    assert m["n_paths"] == 2
    assert m["kernel_is_a_sum"] is True
    assert m["z_many"] == 2.0
    assert m["z_unique"] == 1.0
    assert m["ratio"] == 2.0
    assert m["born_derived_here"] is False
    assert m["foc012_refuses_born"] is True
    z_beta = many_path_kernel(3, 1.0, beta=1.0)
    assert abs(z_beta["z_many"] - 3.0 * math.exp(-1.0)) < 1e-12


def test_g1g2g3_diamond_composes() -> None:
    d = diamond_composition(0.0)
    assert d["n_paths"] == 2
    assert d["z_direct_two_paths"] == 2.0
    assert d["g1g2g3_holds_on_cut"] is True
    assert compose_under_g1g2g3(1.0, 1.0) == 1.0
    assert path_kernel(0, 1.0, 0.0) == 0.0


def test_g3_fail_is_local_green_global_red() -> None:
    g = g3_fail_local_green_global_red()
    assert g["delta_eval"] == -1
    assert g["local_green_global_red"] is True
    assert g["g3_holds"] is False
    assert g["false_green_if_eg_defined_as_product"] is True
    assert delta_eval(1, 0, 0) == 0
    assert delta_eval(0, 1, 1) == 1


def test_hex_axes_are_unique_off_axis_are_many() -> None:
    assert hex_shortest_path_count(0, 0) == 1
    assert hex_shortest_path_count(3, 0) == 1
    assert hex_shortest_path_count(0, -3) == 1
    assert hex_shortest_path_count(1, 1) == 2
    assert hex_shortest_path_count(2, 1) == 3
    s1 = hex_shell_paths(1)
    assert s1["n_cells"] == 6
    assert s1["n_axial"] == 6
    assert s1["n_off_axis"] == 0
    assert s1["total_geodesics"] == 6
    s2 = hex_shell_paths(2)
    assert s2["n_cells"] == 12
    assert s2["n_axial"] == 6
    assert s2["n_off_axis"] == 6
    assert s2["total_geodesics"] == 6 * 1 + 6 * 2
    assert s2["kernel_is_a_sum"] is True


def test_one_local_stays_product_two_site_forces_chi() -> None:
    one = one_local_stays_chi1()
    assert one["chi"] == 1
    assert one["n_e"] == 0
    assert one["forces_chi_gt_1"] is False
    two = two_site_forces_chi(1.0)
    assert two["chi_lower_bound"] == 2
    assert two["chi_exact"] is None
    assert two["forces_chi_gt_1"] is True
    stay = two_site_forces_chi(0.0)
    assert stay["chi_lower_bound"] == 1
    assert stay["chi_exact"] == 1
    assert stay["forces_chi_gt_1"] is False


def test_bond_growth_lower_bound_positive_in_window() -> None:
    nu, g = 1.0, 1.0
    tmax = bond_growth_window(nu, g)
    assert abs(tmax - 1.0 / 48.0) < 1e-12
    t = 0.01
    assert t < tmax
    lo = bond_growth_lower(nu, g, t)
    assert lo > 0
    assert abs(lo - (0.01 - 24.0 * 0.0001)) < 1e-12
    assert bond_growth_lower(nu, g, 0.0) == 0.0


def test_face_two_site_mapping_is_admitted_not_derived() -> None:
    f = declared_face_two_site_fixture()
    assert f["hollow_chi"] == 1
    assert f["filled_chi_lower_bound"] == 2
    assert f["filled_chi_exact"] is None
    assert f["hollow_n_e"] == 0
    assert f["filled_n_e"] == 1.0
    assert f["face_two_site_mapping_admitted"] is True
    assert f["face_two_site_mapping_derived"] is False
    assert f["physical_identifications_proved"] is False
    assert f["po011_lemma_53"] is True


def test_hex_wall_local_green_global_red() -> None:
    r0 = local_green_global_red_hex(0)
    assert r0["trivial_interior"] is True
    assert r0["E_g_is_alpha"] == 0
    r2 = local_green_global_red_hex(2)
    assert r2["trivial_interior"] is False
    assert r2["interior_not_k6"] == 0
    assert r2["interior_k6_green"] > 0
    assert r2["E_local_product"] == 1
    assert r2["E_g_is_alpha"] == 0
    assert r2["global_evaluator_declared"] is True
    assert r2["qed_observable_constructed"] is False
    assert r2["delta_eval"] == -1
    assert r2["local_green_global_red"] is True
    assert r2["is_qed"] is False
    assert r2["false_green_if_eg_is_local_product"] is False


def test_join_report_wires_the_grammar() -> None:
    j = join_report()
    assert abs(j["unique_path_sum_w"] - 1.0) < 1e-3
    assert j["many_path_ratio"] == 2.0
    assert j["diamond_g1g2g3"] is True
    assert j["delta_eval_counterexample"] == -1
    assert j["hollow_chi"] == 1
    assert j["filled_chi_lower_bound"] == 2
    assert j["face_two_site_mapping_derived"] is False
    assert j["hex_R2_local_green_global_red"] is True
    assert j["hex_R2_axial_unique"] == 6
    assert j["bond_growth_lower_at_t"] > 0
    assert j["foc012_refuses_born"] is True
    assert j["born_derived_here"] is False
    assert j["is_qed"] is False
