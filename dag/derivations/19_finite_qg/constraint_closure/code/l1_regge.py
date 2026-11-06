r"""
Regge Calculus Component Module (GR-002 / PO-012).
2D, 3D, and 4D Regge-Barbero-Immirzi Action Minimization & Curvature Deficits.
AuthorityEffect: None.
"""

import math
from typing import Dict, Any, List
import numpy as np
from scipy.optimize import linprog


def compute_regge_valency_deficit(valency: int = 5) -> Dict[str, Any]:
    r"""
    Computes Regge deficit angle from minimal 2-simplex vertex valency defect.
    Flat 2D triangular lattice has valency 6 (6 * pi/3 = 2*pi).
    A defect drops valency to 5 (5 * pi/3 = 5*pi/3).
    Deficit angle \Delta \theta = 2*pi - 5*pi/3 = pi/3.
    """
    flat_valency = 6
    angle_per_triangle = math.pi / 3.0
    deficit_angle = 2.0 * math.pi - valency * angle_per_triangle
    exact_fraction = (flat_valency - valency) / flat_valency

    return {
        "valency": valency,
        "flat_valency": flat_valency,
        "deficit_angle_exact": "pi/3" if valency == 5 else f"{(flat_valency - valency)}*pi/3",
        "deficit_angle_radians": deficit_angle,
        "fractional_curvature": exact_fraction,
        "interpretation": "Point-like Regge curvature from discrete 2-simplex valency defect."
    }


def compute_3d_regge_action_minimization(
    hinge_valencies: List[int] = None,
    hinge_areas: List[float] = None
) -> Dict[str, Any]:
    r"""
    Evaluates 3D simplicial block valency deficits under Regge action minimization:
    \min_{\Lambda} S_{\text{Regge}} = \sum_i \epsilon_i(\Lambda) A_i
    where \epsilon_i = 2\pi - k_i \theta_{\text{dihedral}} is the deficit angle at hinge i,
    and \theta_{\text{dihedral}} = \arccos(1/3) \approx 1.230959 rad for regular tetrahedra.
    """
    if hinge_valencies is None:
        hinge_valencies = [5, 4, 6, 5]
    if hinge_areas is None:
        hinge_areas = [1.0, 1.0, 1.0, 1.0]

    theta_dihedral = math.acos(1.0 / 3.0)
    flat_hinge_valency = 2.0 * math.pi / theta_dihedral

    epsilon_list = [2.0 * math.pi - k * theta_dihedral for k in hinge_valencies]
    total_regge_action = float(sum(eps * area for eps, area in zip(epsilon_list, hinge_areas)))

    c = np.array(hinge_areas)
    A_eq = np.eye(len(hinge_valencies))
    b_eq = np.abs(epsilon_list)
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, method='highs')

    minimized_action = float(res.fun) if res.success else total_regge_action
    total_area = float(sum(hinge_areas))
    boundary_curvature_scaling = total_regge_action / max(1e-12, total_area)

    return {
        "dihedral_angle_rad": theta_dihedral,
        "flat_hinge_valency": flat_hinge_valency,
        "hinge_valencies": hinge_valencies,
        "deficit_angles_rad": epsilon_list,
        "total_regge_action": total_regge_action,
        "minimized_regge_action": minimized_action,
        "boundary_curvature_scaling": boundary_curvature_scaling,
        "lp_solver_success": res.success,
        "authority": "None"
    }


def compute_4d_barbero_immirzi_regge_action(
    hinge_valencies_4d: List[int] = None,
    triangle_areas: List[float] = None,
    immirzi_gamma: float = 0.274066
) -> Dict[str, Any]:
    r"""
    Evaluates 4D spacetime 2-simplex triangle hinge valencies under Regge-Barbero-Immirzi action constraints:
    S_{\text{4D}} = \sum_i A_i \left( \epsilon_i^{(4D)} + \frac{1}{\gamma} \epsilon_i^{\text{dual}} \right)
    """
    if hinge_valencies_4d is None:
        hinge_valencies_4d = [5, 4, 5, 4]
    if triangle_areas is None:
        triangle_areas = [1.0, 1.0, 1.0, 1.0]

    theta_hyper = math.acos(1.0 / 4.0)
    flat_4d_valency = 2.0 * math.pi / theta_hyper

    epsilon_4d = [2.0 * math.pi - N * theta_hyper for N in hinge_valencies_4d]
    epsilon_dual = [math.sin(eps) for eps in epsilon_4d]

    action_4d_terms = [
        area * (eps + (1.0 / max(1e-6, immirzi_gamma)) * eps_d)
        for area, eps, eps_d in zip(triangle_areas, epsilon_4d, epsilon_dual)
    ]
    total_4d_action = float(sum(action_4d_terms))
    total_area = float(sum(triangle_areas))
    boundary_4d_curvature_density = total_4d_action / max(1e-12, total_area)

    return {
        "hyper_dihedral_angle_rad": theta_hyper,
        "flat_4d_hinge_valency": flat_4d_valency,
        "hinge_valencies_4d": hinge_valencies_4d,
        "epsilon_4d_rad": epsilon_4d,
        "epsilon_dual": epsilon_dual,
        "immirzi_gamma": immirzi_gamma,
        "total_4d_action": total_4d_action,
        "boundary_4d_curvature_density": boundary_4d_curvature_density,
        "authority": "None"
    }
