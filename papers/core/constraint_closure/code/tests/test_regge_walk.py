"""PD → Regge walk tests. Stdlib. No illegal imports. AuthorityEffect: None."""

from __future__ import annotations

import ast
from pathlib import Path

from regge_walk import d0, phi_triangle, run_walk, walk_is_consistent

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


def test_walk_module_imports_are_legal() -> None:
    src = Path(__file__).resolve().parents[1] / "regge_walk.py"
    names = _imported(src)
    for banned in ILLEGAL:
        assert banned not in names
    assert names <= {"__future__", "dataclasses", "typing", "math", "regge_climb"}


def test_walk_has_five_rungs_zero_through_four() -> None:
    w, _ = run_walk()
    assert [r.simplex_dim for r in w.rungs] == [0, 1, 2, 3, 4]
    assert [r.index for r in w.rungs] == [0, 1, 2, 3, 4]


def test_walk_is_consistent_and_has_no_injected_vev() -> None:
    w, _ = run_walk()
    assert walk_is_consistent(w)
    assert w.rungs[0].payload["first_fire"] == 2


def test_each_rung_consumes_the_unit() -> None:
    w, _ = run_walk()
    unit = w.rungs[0].payload["first_fire"]
    assert w.rungs[1].payload["phi_edge"] == unit
    assert w.rungs[2].payload["phi_triangle"] == unit
    assert w.rungs[2].payload["phi_exact"] == 0
    assert w.rungs[3].payload["su2_admissible"] is True
    assert w.rungs[4].payload["lambda_toy"] > 0
    assert phi_triangle(d0((100, -20, 7))) == 0


def test_residuals_are_computed_but_physical_labels_are_refused() -> None:
    _, left = run_walk()
    assert left["inexact_cochain_residual_natural"] == 1
    assert left["exact_cochain_residual"] == 0
    assert left["isolated_edge_residual_raw"] == 2
    assert left["mean_4d_deficit_natural"] > 0
    assert left["physical_identifications_proved"] is False
    assert left["analogy_labels"]["face"] == "Higgs"
    assert "Hermitian SU(3)" in left["next_lifts"]
    assert "continuum Einstein" in left["next_lifts"]
    assert "MSSM superpartners" in left["next_lifts"]


def test_u1_from_deficit_not_from_a_point() -> None:
    w, left = run_walk()
    assert w.rungs[2].payload["u1_holonomy"] == 1
    assert left["deficit_phase_class"] == 1
    assert left["physical_identifications_proved"] is False
    assert "0-simplex" not in w.rungs[2].name or "holonomy" in w.rungs[2].name


def test_graph_cone_does_not_construct_physical_propagation() -> None:
    from regge_walk import lr_reachable

    assert lr_reachable(5, 0, 0) == frozenset({0})
    assert lr_reachable(5, 0, 2) == frozenset({0, 1, 2})
    assert 4 not in lr_reachable(5, 0, 2)
    w, left = run_walk()
    assert left["lr_speed_bound"] == 1
    assert left["propagation_dynamics_constructed"] is False
    assert left["assigned_massless_mode_speed"] == left["lr_speed_bound"]
    assert (
        left["assigned_inertial_mode_speed_num"]
        < left["assigned_inertial_mode_speed_den"]
    )
    assert w.rungs[2].payload["assigned_inertial_mode_per_edge"] > 0


def test_fine_structure_is_a_hunt_not_qed() -> None:
    _, left = run_walk()
    assert left["named_inverse_coupling_lattice"] == 6
    assert 140 < left["named_inverse_coupling_3cycle_4pi"] < 145
    assert left["coupling_identification_proved"] is False
    assert abs(left["named_inverse_coupling_3cycle_4pi"] - 137.035999177) > 1


def test_face_attachment_fact_is_separate_from_particle_analogy() -> None:
    w, left = run_walk()
    r2 = w.rungs[2]
    assert r2.payload["hollow_h1_rank"] == 1
    assert r2.payload["filled_h1_rank"] == 0
    assert r2.payload["face_attachment_increases_loop_stiffness"] is True
    assert r2.payload["physical_identifications_proved"] is False
    assert r2.payload["analogy_labels"]["edges"] == ("W+", "W-", "Z")
    assert r2.payload["loop_inertia_hollow"] == 0
    assert r2.payload["loop_inertia_filled"] > 0
    assert r2.payload["exact_inertia_filled"] == 0
    assert left["physical_identifications_proved"] is False
    assert left["h1_rank_drop"] == (1, 0)
