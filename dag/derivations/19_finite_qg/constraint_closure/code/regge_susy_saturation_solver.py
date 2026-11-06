"""Regge Calculus & Primitive Difference SUSY Saturation Solver Subsystem.

Conforms strictly to contract specification:
    urn:omega:math:solver:v1.0.0

AuthorityEffect: None.

Evaluates 3D & 4D simplicial Regge-Barbero-Immirzi deficit angles, primitive difference
quotients, and the topological saturation scale prediction E_sat = v_EW * 360 (85.6 TeV - 88.56 TeV).
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple
import numpy as np

try:
    from universe_anomalonica.omega_engine.solver.solver import (
        BaseSolver,
        SolverCertificate,
        SolverInput,
        SolverOutput,
    )
except ImportError:
    try:
        from .solver import (
            BaseSolver,
            SolverCertificate,
            SolverInput,
            SolverOutput,
        )
    except (ImportError, ValueError):
        from solver import (
            BaseSolver,
            SolverCertificate,
            SolverInput,
            SolverOutput,
        )


def compute_primitive_difference_quotient(
    cochain: Sequence[float],
    d0_matrix: np.ndarray,
) -> Dict[str, Any]:
    r"""Compute Primitive Difference quotient mass Phi1([omega]) = min_alpha ||omega - d0 alpha||_1."""
    import scipy.optimize as opt

    cochain_vec = np.asarray(cochain, dtype=float)
    n_e, n_v = d0_matrix.shape

    c = np.concatenate([np.zeros(n_v), np.ones(n_e)])
    i_e = np.eye(n_e)
    a_ub = np.vstack([np.hstack([d0_matrix, -i_e]), np.hstack([-d0_matrix, -i_e])])
    b_ub = np.concatenate([cochain_vec, -cochain_vec])
    bounds = [(None, None)] * n_v + [(0, None)] * n_e

    res = opt.linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if res.success:
        min_l1 = float(res.fun)
        alpha_opt = res.x[:n_v]
        residual_vec = cochain_vec - d0_matrix @ alpha_opt
    else:
        min_l1 = float(np.sum(np.abs(cochain_vec)))
        alpha_opt = np.zeros(n_v)
        residual_vec = cochain_vec

    return {
        "min_l1": min_l1,
        "alpha_opt": alpha_opt.tolist(),
        "residual_vector": residual_vec.tolist(),
        "solved": bool(res.success),
        "authority_effect": "None",
    }


def compute_4d_regge_immirzi_action_and_deficit(
    hinge_valencies_4d: Optional[List[int]] = None,
    triangle_areas: Optional[List[float]] = None,
    immirzi_gamma: float = 0.274066,
) -> Dict[str, Any]:
    r"""Evaluates 4D Regge-Barbero-Immirzi discrete action over 2-simplex triangle hinges.

    S_{4D} = sum_i A_i * ( epsilon_i^{(4D)} + (1 / gamma) * sin(epsilon_i^{(4D)}) )
    where theta_{hyper} = arccos(1/4) ~ 1.318116 rad.
    """
    if hinge_valencies_4d is None:
        hinge_valencies_4d = [5, 4, 5, 4]
    if triangle_areas is None:
        triangle_areas = [1.0, 1.0, 1.0, 1.0]

    theta_hyper = math.acos(1.0 / 4.0)
    flat_4d_valency = 2.0 * math.pi / theta_hyper

    epsilon_4d = [2.0 * math.pi - N * theta_hyper for N in hinge_valencies_4d]
    epsilon_dual = [math.sin(eps) for eps in epsilon_4d]

    action_terms = [
        area * (eps + (1.0 / max(1e-6, immirzi_gamma)) * eps_d)
        for area, eps, eps_d in zip(triangle_areas, epsilon_4d, epsilon_dual)
    ]
    total_4d_action = float(sum(action_terms))
    total_area = float(sum(triangle_areas))
    boundary_density = total_4d_action / max(1e-12, total_area)

    return {
        "hyper_dihedral_angle_rad": theta_hyper,
        "flat_4d_hinge_valency": flat_4d_valency,
        "hinge_valencies_4d": hinge_valencies_4d,
        "epsilon_4d_rad": epsilon_4d,
        "epsilon_dual": epsilon_dual,
        "immirzi_gamma": immirzi_gamma,
        "total_4d_action": total_4d_action,
        "boundary_4d_curvature_density": boundary_density,
        "authority_effect": "None",
    }


def compute_susy_saturation_scale(
    v_ew: float = 246.0,
    angular_factor: float = 360.0,
) -> Dict[str, Any]:
    r"""Computes topological saturation scale E_sat = v_EW * 360 (GeV -> TeV).

    Track A (Climb / Motif): Full 360-degree angular inflation over 2-simplex face/edge modes.
    Track B (Kill / Receipt): 360 is angular motif, v_EW is phenomenological input.
    """
    e_sat_gev = v_ew * angular_factor
    e_sat_tev = e_sat_gev / 1000.0

    v_ew_alt = 237.8
    e_sat_gev_alt = v_ew_alt * angular_factor
    e_sat_tev_alt = e_sat_gev_alt / 1000.0

    return {
        "v_ew_gev": v_ew,
        "angular_factor_degrees": angular_factor,
        "e_sat_gev": e_sat_gev,
        "e_sat_tev": e_sat_tev,
        "v_ew_alt_gev": v_ew_alt,
        "e_sat_alt_tev": e_sat_tev_alt,
        "target_band_tev": "85.6 TeV - 88.56 TeV",
        "track_a_classification": "Class B motif / Topological saturation scale",
        "track_b_receipt": "v_EW hardcoded as input; 360 is full angular manifold factor.",
        "authority_effect": "None",
    }


class ReggeSUSYSaturationSolverAdapter(BaseSolver):
    """Adapter wrapping Regge-Barbero-Immirzi & SUSY Saturation derivation logic."""

    def __init__(self, solver_id: str = "regge_susy_saturation"):
        super().__init__(
            solver_id=solver_id,
            category="QuantumFieldRegge",
            solver_version="v1.0.0",
        )

    def solve(self, solver_input: SolverInput) -> SolverOutput:
        data = solver_input.data or solver_input.parameters or {}
        v_ew = float(data.get("v_ew_gev", 246.0))
        angular_factor = float(data.get("angular_factor", 360.0))
        hinge_valencies_4d = data.get("hinge_valencies_4d", [5, 4, 5, 4])
        triangle_areas = data.get("triangle_areas", [1.0, 1.0, 1.0, 1.0])
        immirzi_gamma = float(data.get("immirzi_gamma", 0.274066))

        regge_res = compute_4d_regge_immirzi_action_and_deficit(
            hinge_valencies_4d=hinge_valencies_4d,
            triangle_areas=triangle_areas,
            immirzi_gamma=immirzi_gamma,
        )

        susy_res = compute_susy_saturation_scale(
            v_ew=v_ew,
            angular_factor=angular_factor,
        )

        d0 = np.array([[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0], [1.0, 0.0, -1.0]])
        cochain = data.get("cochain", [1.0, 1.0, 1.0])
        pd_res = compute_primitive_difference_quotient(cochain, d0)

        witness_data = {
            "regge": regge_res,
            "susy": susy_res,
            "primitive_difference": pd_res,
        }

        cert_bytes = json.dumps(witness_data, sort_keys=True, default=str).encode("utf-8")
        cert_hash = hashlib.sha256(cert_bytes).hexdigest()

        status = "SOLVED" if pd_res.get("solved") else "OBSTRUCTED"

        output = SolverOutput(
            problem_id=solver_input.problem_id,
            solver_id=self.solver_id,
            status=status,
            residual_mass=float(pd_res.get("min_l1", 0.0)),
            residual_vector=[float(x) for x in pd_res.get("residual_vector", [])],
            certificate=SolverCertificate(
                certificate_type="RESIDUAL_BOUND",
                witness_data=witness_data,
                is_valid=True,
                certificate_hash=cert_hash,
            ),
            metadata={"authority_effect": "None"},
            authority_effect="EvidenceOnly",
        )
        return output


__all__ = [
    "compute_primitive_difference_quotient",
    "compute_4d_regge_immirzi_action_and_deficit",
    "compute_susy_saturation_scale",
    "ReggeSUSYSaturationSolverAdapter",
]
