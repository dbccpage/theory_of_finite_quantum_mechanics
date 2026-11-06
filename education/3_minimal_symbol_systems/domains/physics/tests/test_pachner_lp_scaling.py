"""Tests of retained finite calculations and declared fixtures.
Physical recovery and removed certificate wrappers are outside this test scope.
"""

import random
import sys
from pathlib import Path

import pytest
import yaml

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from pachner_lp_scaling import (
    PachnerLpScalingEvaluator,
    Simplicial4DComplex,
)




def test_seed_complex_topology():
    """Validates the seed 4-sphere complex (boundary of 5-simplex)."""
    c = Simplicial4DComplex()
    assert c.num_vertices == 6
    assert c.num_edges == 15
    assert c.num_triangles == 20
    assert c.num_tetrahedra == 15
    assert c.num_four_simplices == 6
    # chi = 6 - 15 + 20 - 15 + 6 = 2
    assert c.euler_characteristic == 2


def test_pachner_2_to_4_move_cell_counts_and_euler_invariance():
    """Validates that a 2->4 bistellar move increments N4 by 2, adds 1 edge, and conserves chi."""
    c = Simplicial4DComplex()
    # Apply 1->5 move first so that opposing vertices across shared tetrahedra do not already form an edge
    v_new, added_simplices = c.apply_1_to_5_move()
    assert c.num_four_simplices == 10
    assert c.euler_characteristic == 2

    candidates = c.find_viable_2_to_4_moves()
    assert len(candidates) > 0, "Expected viable 2->4 candidates after 1->5 subdivision"

    t, s1, s2, v0, v1 = candidates[0]
    n0_before = c.num_vertices
    n1_before = c.num_edges
    n2_before = c.num_triangles
    n3_before = c.num_tetrahedra
    n4_before = c.num_four_simplices
    chi_before = c.euler_characteristic

    applied = c.apply_2_to_4_move((t, s1, s2, v0, v1))
    assert applied is True

    assert c.num_four_simplices == n4_before + 2
    assert c.num_edges == n1_before + 1
    assert c.num_triangles == n2_before + 4
    assert c.num_tetrahedra == n3_before + 5
    assert c.num_vertices == n0_before
    assert c.euler_characteristic == chi_before == 2
    assert tuple(sorted((v0, v1))) in c.edges


def test_pachner_3_to_3_flip_cell_counts_and_euler_invariance():
    """Validates that a 3->3 bistellar flip maintains N4 invariant and conserves chi."""
    c = Simplicial4DComplex()
    c.grow_to_size(18, rng=random.Random(101))
    assert c.euler_characteristic == 2

    candidates = c.find_viable_3_to_3_moves()
    assert len(candidates) > 0, "Expected viable 3->3 candidates in grown complex"

    cand = candidates[0]
    tri, slist, dual_tri = cand

    n0_before = c.num_vertices
    n1_before = c.num_edges
    n2_before = c.num_triangles
    n3_before = c.num_tetrahedra
    n4_before = c.num_four_simplices
    chi_before = c.euler_characteristic

    applied = c.apply_3_to_3_move(cand)
    assert applied is True

    # 3->3 flip preserves all cell counts
    assert c.num_four_simplices == n4_before
    assert c.num_tetrahedra == n3_before
    assert c.num_triangles == n2_before
    assert c.num_edges == n1_before
    assert c.num_vertices == n0_before
    assert c.euler_characteristic == chi_before == 2
    assert dual_tri in c.triangles


def test_euler_characteristic_conservation_trajectory():
    """Validates exact chi = 2 conservation along a sequence of mixed Pachner moves."""
    c = Simplicial4DComplex()
    rng = random.Random(2026)

    for step in range(25):
        # Attempt 3->3 flip with probability 0.4
        if rng.random() < 0.4:
            flips = c.randomize_triangulation(num_flips=1, rng=rng)
            if flips == 0:
                candidates = c.find_viable_2_to_4_moves()
                if candidates:
                    c.apply_2_to_4_move(rng.choice(candidates))
                else:
                    c.apply_1_to_5_move()
        else:
            candidates = c.find_viable_2_to_4_moves()
            if candidates:
                c.apply_2_to_4_move(rng.choice(candidates))
            else:
                c.apply_1_to_5_move()

        assert c.euler_characteristic == 2, (
            f"Euler characteristic drift at step {step}: chi = {c.euler_characteristic}"
        )

    assert c.num_four_simplices > 20


def test_joint_direct_sum_lp_strong_duality_certification():
    """Validates that joint direct-sum LP solver certifies strong duality with gap <= 1e-9."""
    c = Simplicial4DComplex()
    c.grow_to_size(16, rng=random.Random(303))

    res = PachnerLpScalingEvaluator.solve_joint_direct_sum_lp(c)
    assert res["is_certified"] is True
    assert res["duality_gap"] <= 1e-9
    assert abs(res["primal_obj"] - res["dual_obj"]) <= 1e-9
    assert res["dual_witness_norm_inf"] <= 1.000000001
    assert res["dual_divergence_norm"] <= 1e-9
    assert res["solve_time_ms"] >= 0.0


def test_pachner_lp_scaling_benchmark_and_empirical_exponent():
    """Validates empirical power-law runtime scaling exponent alpha <= 3.5 across size tiers."""
    evaluator = PachnerLpScalingEvaluator(in_memory=True)
    try:
        receipt = evaluator.run_scaling_benchmark(
            run_id="test_run_scaling_tiers",
            target_sizes=[6, 12, 24, 48, 96],
            random_seed=777,
        )

        assert receipt["num_steps"] >= 5
        assert receipt["min_4simplices"] == 6
        assert receipt["max_4simplices"] >= 96
        assert receipt["all_certified"] is True
        assert receipt["max_duality_gap"] <= 1e-9

        # Polynomial scaling bound: alpha <= 3.5
        alpha = receipt["empirical_scaling_exponent"]
        assert alpha <= 3.5, f"Scaling exponent {alpha} exceeds polynomial bound 3.5"

        # Mean solve time per step should be modest (< 500 ms)
        assert receipt["mean_solve_time_ms"] < 500.0
        assert receipt["scaling_audit_status"] == "SAMPLED_SCALING_THRESHOLD_MET"
    finally:
        evaluator.close()


def test_sql_pachner_scaling_audit_view():
    """Validates SQLite execution of Section 14 schema, trajectory insertion, and audit view."""
    evaluator = PachnerLpScalingEvaluator(in_memory=True)
    try:
        evaluator.run_scaling_benchmark(
            run_id="sql_audit_test_run",
            target_sizes=[6, 12, 20],
            random_seed=42,
        )

        cur = evaluator.conn.cursor()

        # Check trajectory count
        cur.execute(
            "SELECT COUNT(*) FROM L1PachnerScalingTrajectory WHERE run_id = 'sql_audit_test_run'"
        )
        count_traj = cur.fetchone()[0]
        assert count_traj >= 3

        # Check summary row
        cur.execute(
            "SELECT min_4simplices, max_4simplices, empirical_scaling_exponent, all_certified FROM L1PachnerScalingSummary WHERE run_id = 'sql_audit_test_run'"
        )
        summary = cur.fetchone()
        assert summary is not None
        assert summary[0] == 6
        assert summary[1] >= 20
        assert summary[3] == 1

        # Check audit view
        cur.execute(
            "SELECT run_id, min_4simplices, max_4simplices, empirical_scaling_exponent, scaling_audit_status FROM ViewL1PachnerScalingAudit WHERE run_id = 'sql_audit_test_run'"
        )
        audit_row = cur.fetchone()
        assert audit_row is not None
        assert audit_row[0] == "sql_audit_test_run"
        assert audit_row[4] == "SAMPLED_SCALING_THRESHOLD_MET"
    finally:
        evaluator.close()


def test_pachner_moves_boundary_conditions():
    """Validates boundary conditions, empty complex checks, and invalid move handling."""
    # Empty complex check
    empty_c = Simplicial4DComplex(four_simplices=set())
    with pytest.raises(ValueError, match="Cannot subdivide empty complex"):
        empty_c.apply_1_to_5_move()

    # Invalid 2->4 move candidate
    c = Simplicial4DComplex()
    assert (
        c.apply_2_to_4_move(((1, 2, 3, 4), (1, 2, 3, 4, 99), (1, 2, 3, 4, 100), 99, 100)) is False
    )

    # Invalid 3->3 move candidate
    assert c.apply_3_to_3_move(((1, 2, 3), [(1, 2, 3, 4, 5)], (6, 7, 8))) is False
