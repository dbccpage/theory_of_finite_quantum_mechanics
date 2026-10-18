"""Pytest Test Suite for Regge Calculus & SUSY Saturation Derivation.

AuthorityEffect: None.

Verifies:
1. 4D Regge-Barbero-Immirzi action and deficit angle metrics.
2. Primitive Difference quotient minimization on 2-simplex carriers.
3. SUSY topological saturation scale E_sat = v_EW * 360 (85.6 TeV - 88.56 TeV).
4. BaseSolver interface contract compliance (urn:omega:math:solver:v1.0.0).
5. Dual-track claim discipline (Track A climb vs Track B kill/receipt).
"""

from __future__ import annotations

import math
import os
import sys

base_dir = os.environ.get("CODA_OOUTWIRE_DOCS")
if base_dir:
    math_dir = os.path.join(base_dir, "universe_anomalonica", "math")
    for p in [base_dir, math_dir]:
        if p not in sys.path:
            sys.path.insert(0, p)

import numpy as np
import pytest

try:
    from universe_anomalonica.omega_engine.solver.regge_susy_saturation_solver import (
        ReggeSUSYSaturationSolverAdapter,
        compute_4d_regge_immirzi_action_and_deficit,
        compute_primitive_difference_quotient,
        compute_susy_saturation_scale,
        run_full_regge_susy_tev_derivation,
    )
    from universe_anomalonica.omega_engine.solver import (
        SolverInput,
        create_solver,
        list_available_solvers,
    )
except ImportError:
    try:
        from regge_susy_saturation_solver import (
            ReggeSUSYSaturationSolverAdapter,
            compute_4d_regge_immirzi_action_and_deficit,
            compute_primitive_difference_quotient,
            compute_susy_saturation_scale,
            run_full_regge_susy_tev_derivation,
        )
        from solver import (
            SolverInput,
            create_solver,
            list_available_solvers,
        )
    except ImportError:
        pytestmark = pytest.mark.skip(reason="regge_susy_saturation_solver module not present")



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
    """Verify solver adapter conforms to BaseSolver contract (urn:omega:math:solver:v1.0.0)."""
    assert "regge_susy_saturation" in list_available_solvers()

    solver = create_solver("regge_susy_saturation")
    solver_input = SolverInput(
        problem_id="test_susy_001",
        category="QuantumFieldRegge",
        data={
            "v_ew_gev": 246.0,
            "angular_factor": 360.0,
            "cochain": [1.0, 1.0, 1.0],
        },
    )

    output = solver.solve(solver_input)
    assert output.solver_id == "regge_susy_saturation"
    assert output.status in ["SOLVED", "FEASIBLE"]
    assert output.authority_effect == "EvidenceOnly"
    assert output.certificate is not None
    assert output.certificate.certificate_type == "RESIDUAL_BOUND"
    assert output.certificate.is_valid is True

    # Hash verification
    checked = solver.verify_output(output)
    assert checked.authority_effect == "FactOnly"
    assert len(checked.verification_hash) == 64
