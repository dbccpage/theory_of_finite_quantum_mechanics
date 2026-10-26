"""Tests of retained finite calculations and declared fixtures.
Physical recovery and removed certificate wrappers are outside this test scope.
"""

from __future__ import annotations

import math

import pytest
from regge_wdw_evaluator import ReggeWdwEvaluator


@pytest.fixture
def evaluator():
    ev = ReggeWdwEvaluator(in_memory=True)
    yield ev
    ev.close()


class TestFiniteGeometryAndAlgebraFixtures:
    """Numerical examples only; these tests do not reproduce a complete physics paper."""

    def test_finding_1_triangle_loop_strong_lp_duality(self, evaluator: ReggeWdwEvaluator):
        """Finding 1: Pure gauge Phi=0, cycle Phi=3, dual witness w*=[1,1,1]^T, duality gap zero."""
        res = evaluator.evaluate_triangle_cycle_strong_duality()
        assert res["all_certified"] is True

        # Pure gauge case
        pg = res["pure_gauge"]
        assert abs(pg["primal"] - 0.0) < 1e-12
        assert abs(pg["dual"] - 0.0) < 1e-12
        assert pg["gap"] < 1e-12
        assert pg["status"] == "CERTIFIED_STRONG_DUALITY"

        # Cycle obstruction case
        cyc = res["cycle_obstruction"]
        assert abs(cyc["primal"] - 3.0) < 1e-12
        assert abs(cyc["dual"] - 3.0) < 1e-12
        assert cyc["gap"] < 1e-12
        assert cyc["status"] == "CERTIFIED_STRONG_DUALITY"
        w_star = cyc["dual_witness"]
        for wi in w_star:
            assert abs(wi - 1.0) < 1e-12

    def test_finding_2_carroll_s4_bianchi_holonomy(self, evaluator: ReggeWdwEvaluator):
        """Finding 2: Regular S4 has ||d_2 eps||_1 = 0; perturbed S4 has ||d_2 eps||_1 ~ 1.9565652080."""
        res = evaluator.evaluate_carroll_s4_bianchi_perturbation()

        # Regular S4
        reg = res["regular"]
        assert reg["d2_eps_l1"] < 1e-12
        assert reg["d2_eps_linf"] < 1e-12
        assert reg["status"] == "ABELIAN_BIANCHI_SATISFIED"

        # Carroll perturbed S4 (l_{01} = 1.1)
        pert = res["perturbed"]
        assert abs(pert["d2_eps_l1"] - 1.9565652080) < 1e-6
        assert abs(pert["d2_eps_linf"] - 0.2445706510) < 1e-6
        assert abs(pert["val_0234"] - (-0.2445706510)) < 1e-6
        assert pert["status"] == "NONZERO_ABELIAN_BOUNDARY"



    def test_finding_5_hodge_dirac_laplacian_witten_index(self, evaluator: ReggeWdwEvaluator):
        """Finding 5: Single 2-simplex Delta_1 = 3*I_3, W = 1; glued triangles spectrum {2, 2, 4, 4, 4}."""
        res = evaluator.evaluate_hodge_dirac_laplacian_witten_index()

        s = res["single_2simplex"]
        assert s["is_3I"] is True
        assert s["trace"] == 9.0
        assert s["witten_index"] == 1

        g = res["double_triangle"]
        assert g["trace"] == 16.0
        assert g["witten_index"] == 1
        expected_eigvals = [2.0, 2.0, 4.0, 4.0, 4.0]
        for actual, exp in zip(g["eigvals"], expected_eigvals):
            assert abs(actual - exp) < 1e-4

    def test_finding_6_fixed_carrier_homogeneity_vs_double_well(self, evaluator: ReggeWdwEvaluator):
        """Finding 6: R2 linear = 1.000000 vs R2 quartic = 0.985563, unique minimum at origin."""
        res = evaluator.evaluate_fixed_carrier_homogeneity_vs_double_well()

        assert abs(res["r2_linear"] - 1.0) < 1e-6
        assert abs(res["r2_quartic"] - 0.985563) < 1e-5
        assert res["origin_minimum"] is True
        assert res["is_absolute_value_fixture"] is True
