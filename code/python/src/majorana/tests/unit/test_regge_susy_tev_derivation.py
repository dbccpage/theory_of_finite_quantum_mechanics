from __future__ import annotations
"""Pytest Test Suite for Regge Calculus & SUSY Saturation Derivation.

AuthorityEffect: None.

Verifies:
1. 4D Regge-Barbero-Immirzi action and deficit angle metrics.
2. Primitive Difference quotient minimization on 2-simplex carriers.
3. SUSY topological saturation scale E_sat = v_EW * 360 (85.6 TeV - 88.56 TeV).
4. Optional BaseSolver adapter compliance with SolverKernel v1.2 evidence.
5. Dual-track claim discipline (Track A climb vs Track B kill/receipt).
"""


import math
import os
import sys

# Ensure anomalon root is on sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for p in [
    base_dir,
    os.path.join(base_dir, "coda"),
    os.path.join(base_dir, "codaq"),
    os.path.join(base_dir, "math"),
]:
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np
import pytest

from omega_engine.crates.solver.solv_regge_susy_saturation import (
    ReggeSUSYSaturationSolverAdapter,
    compute_4d_regge_immirzi_action_and_deficit,
    compute_primitive_difference_quotient,
    compute_susy_saturation_scale,
    solve_regge_susy_saturation,
)
from omega_engine.crates.solver.base.solver_base import BaseSolver
from omega_engine.crates.type.solver_kernel import SolverKernel, SolverResult



def test_4d_regge_immirzi_action_and_deficit():
    """Verify 4D Regge-Barbero-Immirzi action and hyper-dihedral deficit calculations."""
    res = compute_4d_regge_immirzi_action_and_deficit(
        hinge_valencies_4d=[5, 4, 5, 4],
        triangle_areas=[1.0, 1.0, 1.0, 1.0],
        immirzi_gamma=0.274066,
    )
    assert abs(res["hyper_dihedral_angle_rad"] - math.acos(0.25)) < 1e-6
    assert len(res["epsilon_4d_rad"]) == 4
    assert res["total_4d_action"] != 0.0
    assert res["authority_effect"] == "None"


def test_primitive_difference_quotient_on_triangle():
    """Verify L1 repair distance and dual witness on 2-simplex."""
    d0 = np.array([[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0], [1.0, 0.0, -1.0]])

    # 1. Exact coboundary omega_exact = d0 * [1, 2, 0]^T = [1, -2, 1]^T -> Phi1 = 0
    cochain_exact = [1.0, -2.0, 1.0]
    res_exact = compute_primitive_difference_quotient(cochain_exact, d0)
    assert res_exact["solved"] is True
    assert abs(res_exact["min_l1"]) < 1e-6

    # 2. Non-zero residual class / circulation loop omega_loop = [1, 1, 1]^T -> Phi1 = 3.0
    cochain_loop = [1.0, 1.0, 1.0]
    res_loop = compute_primitive_difference_quotient(cochain_loop, d0)
    assert res_loop["solved"] is True
    assert abs(res_loop["min_l1"] - 3.0) < 1e-6



def test_susy_saturation_scale_derivation():
    """Verify SUSY saturation scale calculation (85.6 TeV - 88.56 TeV)."""
    res = compute_susy_saturation_scale(v_ew=246.0, angular_factor=360.0)

    # 246.0 * 360 = 88560 GeV = 88.56 TeV
    assert abs(res["e_sat_gev"] - 88560.0) < 1e-6
    assert abs(res["e_sat_tev"] - 88.56) < 1e-6

    # Baseline 237.8 * 360 = 85608 GeV = 85.608 TeV
    assert abs(res["e_sat_alt_tev"] - 85.608) < 1e-3
    assert "85.6 TeV - 88.56 TeV" in res["target_band_tev"]
    assert res["authority_effect"] == "None"


def test_regge_susy_solver_adapter_contract():
    """The adapter emits unverified evidence and never self-certifies."""
    problem = {
        "v_ew_gev": 246.0,
        "angular_factor": 360.0,
        "cochain": [1.0, 1.0, 1.0],
    }
    solver = ReggeSUSYSaturationSolverAdapter()
    output = solver.solve(problem)

    assert isinstance(solver, BaseSolver)
    assert isinstance(solver, SolverKernel)
    assert isinstance(output, SolverResult)
    assert output.evidence_class == "EvidenceOnly"
    assert output.authority_effect == "None"
    assert output.diagnostics == {
        "lp_completed": True,
        "arithmetic_profile": "binary64_scipy_highs",
        "verification_status": "Unverified",
    }
    assert output.residual["mass"] == pytest.approx(3.0)
    assert output.payload["susy"]["e_sat_tev"] == pytest.approx(88.56)
    assert output.proof_artifact_candidates == ()


def test_function_form_kernel_matches_adapter_payload():
    problem = {"cochain": [1.0, -2.0, 1.0]}
    direct = solve_regge_susy_saturation(problem)
    adapted = ReggeSUSYSaturationSolverAdapter().solve(problem)

    assert direct == adapted
    assert direct.residual["mass"] == pytest.approx(0.0, abs=1e-8)



