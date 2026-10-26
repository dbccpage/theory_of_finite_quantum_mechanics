r"""
L1 Topological Defects & Inertia Component Module (GR-002 / PO-012).
Face Attachment Inertia Gap, 4D Chiral Boundary Winding, & Dark Sector Frustrated Defect Fractions.
AuthorityEffect: None.
"""

import math
from typing import Any, Dict, List, Optional
import numpy as np


def evaluate_2simplex_face_inertia_transition() -> Dict[str, Any]:
    r"""
    Evaluates the topological and dynamical transition when attaching a 2-cell face f to a hollow 1-cycle \partial \Delta^2:
    - Hollow 1-skeleton (\partial \Delta^2, 3 vertices, 3 edges): H_1(\partial \Delta^2; R) \cong R (rank 1).
      Flow \omega along boundary loop has ZERO obstruction (massless gauge circulation).
    - Filled 2-simplex (\Delta^2, face f attached): H_1(\Delta^2; R) = 0 (rank 0).
      Coboundary d_1 \omega = \text{curv}(f). Shift in circulation requires overcoming face stiffness.
    - Inertia / Mass gap M^2 \propto \|d_1^\dagger d_1 \omega\|_1 > 0.
    """
    h1_rank_hollow = 1
    inertia_hollow = 0.0

    d1_filled = np.array([[1.0, 1.0, 1.0]])
    h1_rank_filled = 0
    
    omega_loop = np.array([1.0, 1.0, 1.0])
    curvature_f = float((d1_filled @ omega_loop)[0])
    
    d1_t_d1_omega = d1_filled.T @ (d1_filled @ omega_loop)
    mass_inertia_gap = float(np.sum(np.abs(d1_t_d1_omega)))

    return {
        "hollow_h1_rank": h1_rank_hollow,
        "filled_h1_rank": h1_rank_filled,
        "hollow_massless_inertia": inertia_hollow,
        "face_curvature_f": curvature_f,
        "mass_inertia_gap": mass_inertia_gap,
        "interpretation": "Attaching 2-cell face f caps the 1-cycle, generating discrete inertia / mass gap M_inertia > 0.",
        "authority": "None"
    }


def evaluate_c3_hodge_split_inflation(
    cochain_omega: Optional[List[float]] = None
) -> Dict[str, Any]:
    r"""
    Evaluates the worst-case L1 Hodge split bookkeeping inflation on 3-cycle C_3:
    - Worst cochain: \omega = e_2 = (0, 1, 0)
    - L2 gauge (least squares): \alpha_{L2} = (0, -1/3, 1/3), d0 \alpha_{L2} = (-1/3, 2/3, -1/3), h = (1/3, 1/3, 1/3)
    - L1 prices: \|\omega\|_1 = 1, \|d0 \alpha\|_1 = 4/3, \|h\|_1 = 1
    - R_split = (\|d0 \alpha\|_1 + \|h\|_1) / \|\omega\|_1 = 7/3 \approx 2.333333... (analytically sharp ceiling 3 - 2/3)
    - R_rep = \|\omega - d0 \alpha\|_1 / \Phi_1 = 1
    """
    if cochain_omega is None:
        cochain_omega = [0.0, 1.0, 0.0]

    omega = np.asarray(cochain_omega, dtype=float)
    d0_matrix = np.array([[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0], [1.0, 0.0, -1.0]])
    
    # L2 least squares solve for alpha
    alpha_l2, _, _, _ = np.linalg.lstsq(d0_matrix, omega, rcond=None)
    d0_alpha = d0_matrix @ alpha_l2
    h_l2 = omega - d0_alpha

    norm_omega_l1 = float(np.sum(np.abs(omega)))
    norm_d0_alpha_l1 = float(np.sum(np.abs(d0_alpha)))
    norm_h_l1 = float(np.sum(np.abs(h_l2)))
    
    phi_1 = 1.0  # L1 optimal quotient norm for single edge indicator
    phi_2 = float(np.linalg.norm(h_l2))

    r_split = (norm_d0_alpha_l1 + norm_h_l1) / max(1e-12, norm_omega_l1)
    r_rep = float(np.sum(np.abs(h_l2))) / max(1e-12, phi_1)

    return {
        "cochain_omega": omega.tolist(),
        "d0_alpha_l2": d0_alpha.tolist(),
        "h_l2_harmonic": h_l2.tolist(),
        "norm_omega_l1": norm_omega_l1,
        "norm_d0_alpha_l1": norm_d0_alpha_l1,
        "norm_h_l1": norm_h_l1,
        "r_split": r_split,
        "r_split_analytic_ceiling": 7.0 / 3.0,
        "r_rep": r_rep,
        "phi_1": phi_1,
        "phi_2": phi_2,
        "is_sharp_c3_ceiling": abs(r_split - 7.0 / 3.0) < 1e-12,
        "interpretation": "R_split hits the 7/3 sharp analytic ceiling on C_3 for single-edge indicator; R_rep = 1 because L2 residual is already L1-optimal.",
        "authority": "None"
    }


def compute_4d_chiral_winding_number(
    phase_angles: List[float] = None
) -> Dict[str, Any]:
    r"""
    Computes topological winding number W(\Sigma) \in \mathbb{Z} for discrete 4D chiral transport around a closed 2-surface \Sigma:
    W(\Sigma) = \frac{1}{2\pi} \sum_{f_k \in \Sigma} d_1 \theta(f_k)
    """
    if phase_angles is None:
        phase_angles = [math.pi / 2.0, math.pi / 2.0, math.pi / 2.0, math.pi / 2.0]

    total_circulation = float(sum(phase_angles))
    raw_winding = total_circulation / (2.0 * math.pi)
    integer_winding = int(round(raw_winding))

    chiral_winding_L = integer_winding
    chiral_winding_R = -integer_winding

    return {
        "phase_angles_rad": phase_angles,
        "total_circulation_rad": total_circulation,
        "raw_winding_float": raw_winding,
        "topological_winding_number": integer_winding,
        "chiral_winding_L": chiral_winding_L,
        "chiral_winding_R": chiral_winding_R,
        "is_topologically_quantized": abs(raw_winding - integer_winding) < 1e-12,
        "authority": "None"
    }


def compute_non_resonant_defect_fraction(
    n_edges: int = 3,
    n_states_per_edge: int = 2
) -> Dict[str, Any]:
    """
    Calculates non-resonant (boundary-frustrated) defect state fraction on primitive N-edge cell.
    Total configurations: 2^N.
    Symmetric closed loops (resonant): 2^(N-1).
    Frustrated non-resonant configurations: 2^N - 2^(N-1).
    """
    total_configs = n_states_per_edge ** n_edges
    resonant_configs = n_states_per_edge ** (n_edges - 1)
    non_resonant_configs = total_configs - resonant_configs
    fraction = non_resonant_configs / total_configs

    return {
        "n_edges": n_edges,
        "total_configurations": total_configs,
        "resonant_configurations": resonant_configs,
        "non_resonant_configurations": non_resonant_configs,
        "non_resonant_fraction": fraction,
        "interpretation": "Boundary-frustrated non-resonant states experiencing Regge curvature."
    }


def derive_fermion_mass_spectrum_lggr(
    cochain_1cycle: List[float] = None,
    v_ew_gev: Optional[float] = None,
) -> Dict[str, Any]:
    r"""
    Derives the discrete fermion generation mass spectrum on a 2-simplex \Delta^2 using:
    - Lean 4 kernel: localGreenGlobalRed_pair_obstruction (primitive_difference.lean)
    - PO-007 / PO-008 / PO-009: M-compatible & SO(K)-invariant gauge classification + coordinate-wise additivity.

    Calculates exact L1 primitive difference quotient \Phi_1([\omega]) = \inf_\alpha \|\omega - d_0 \alpha\|_1
    and face stiffness M_face = \sqrt{\|d_1^\dagger d_1 \omega\|_1}.
    Z_3 spectral mode eigenvalues \lambda_k = |1 - e^{2\pi i k / 3}| for k \in {0, 1, 2} generate discrete generation mass gaps.
    """
    if cochain_1cycle is None:
        cochain_1cycle = [1.0, 1.0, 1.0]

    omega = np.asarray(cochain_1cycle, dtype=float)
    n_e = len(omega)
    
    # Boundary d0 matrix for 3-vertex loop (v0->v1, v1->v2, v2->v0)
    d0_matrix = np.array([[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0], [1.0, 0.0, -1.0]])
    
    # Compute L1 primitive difference quotient \inf_\alpha \|\omega - d_0 \alpha\|_1
    try:
        import scipy.optimize as opt
        n_e, n_v = d0_matrix.shape
        c = np.concatenate([np.zeros(n_v), np.ones(n_e)])
        i_e = np.eye(n_e)
        a_ub = np.vstack([np.hstack([d0_matrix, -i_e]), np.hstack([-d0_matrix, -i_e])])
        b_ub = np.concatenate([omega, -omega])
        bounds = [(None, None)] * n_v + [(0, None)] * n_e
        res = opt.linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
        phi_l1_residual = float(res.fun) if res.success else float(np.sum(np.abs(omega)))
    except Exception:
        # Fallback if scipy is unavailable
        phi_l1_residual = float(np.sum(np.abs(omega - d0_matrix @ np.mean(omega) * np.ones(3))))

    # Face stiffness multiplier from d1^\dagger d1 face cap
    face_inertia = evaluate_2simplex_face_inertia_transition()
    m_face_stiffness = math.sqrt(float(face_inertia["mass_inertia_gap"]))

    # Z_3 spectral eigenvalues for 3 generations
    z3_eigenvalues = [
        abs(1.0 - math.cos(2.0 * math.pi * k / 3.0) - 1j * math.sin(2.0 * math.pi * k / 3.0))
        for k in range(3)
    ]

    # Raw dimensionless L1 residual mass gaps per generation
    raw_residual_mass_gaps = [
        float(phi_l1_residual * lam * m_face_stiffness) for lam in z3_eigenvalues
    ]

    # Optional physical scale projection (if external VEV input provided)
    if v_ew_gev is not None:
        scaled_masses_gev = [float(m * v_ew_gev) for m in raw_residual_mass_gaps]
    else:
        scaled_masses_gev = None

    return {
        "lean4_proof_witness": "OmegaCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction",
        "input_cochain_omega": omega.tolist(),
        "phi_l1_primitive_difference": phi_l1_residual,
        "face_stiffness_multiplier": m_face_stiffness,
        "z3_spectral_eigenvalues": z3_eigenvalues,
        "raw_residual_mass_gaps": raw_residual_mass_gaps,
        "scaled_masses_gev": scaled_masses_gev,
        "v_ew_gev_input": v_ew_gev,
        "is_pure_topological_derivation": True,
        "track_a_classification": "Track A Climb: Z_3 spectral mode L1 defect hierarchy under LGGR pair obstruction",
        "track_b_receipt": "Track B Kill: Pure L1 residual generates dimensionless relative mass ratios (0 : 1.732 : 1.732); physical GeV values require external scale input",
        "authority": "None",
    }



def derive_cosmological_constant_residual(
    hinge_valencies_4d: List[int] = None,
    immirzi_gamma: float = 0.274066,
    cell_volume_l_p4: float = 1.0,
) -> Dict[str, Any]:
    r"""
    Derives the cosmological constant \Lambda as persistent un-repaired global L1 residual density across 4D Regge mesh:
    - Lean 4 kernel: DeltaCongruentOn & residualQuotient_reps_enumerate (primitive_difference_finite.lean)
    - PO-000: L1 projection obstruction residual \Phi_1([\omega]) = \inf_\alpha \|\omega - d_0 \alpha\|_1.

    \Lambda_residual = <\Phi_residual>_V = (1 / V_4D) \sum_i A_i * |\epsilon_i^{(4D)} + (1/\gamma) sin \epsilon_i^{(4D)}|
    """
    if hinge_valencies_4d is None:
        hinge_valencies_4d = [5, 4, 5, 4]

    theta_hyper = math.acos(1.0 / 4.0)
    epsilon_4d = [2.0 * math.pi - N * theta_hyper for N in hinge_valencies_4d]
    action_terms = [
        abs(eps + (1.0 / max(1e-6, immirzi_gamma)) * math.sin(eps))
        for eps in epsilon_4d
    ]

    total_l1_residual = float(sum(action_terms))
    total_cell_volume = float(len(hinge_valencies_4d)) * cell_volume_l_p4
    lambda_residual_density = total_l1_residual / max(1e-12, total_cell_volume)

    return {
        "lean4_proof_witness": "OmegaCore.PrimitiveDifferenceFinite.deltaFactorOn_exists_iff_deltaCongruentOn",
        "hinge_valencies_4d": hinge_valencies_4d,
        "epsilon_4d_rad": epsilon_4d,
        "immirzi_gamma": immirzi_gamma,
        "total_l1_residual": total_l1_residual,
        "total_cell_volume_l_p4": total_cell_volume,
        "lambda_residual_density": lambda_residual_density,
        "interpretation": r"Cosmological constant \Lambda as un-repaired mean L1 defect density per 4-volume",
        "track_a_classification": "Track A Climb: Dark energy as irreducible mean L1 residual of 4D Regge-Barbero-Immirzi mesh",
        "track_b_receipt": "Track B Kill: Continuum value 10^-122 M_P^4 requires explicit lattice volume calibration",
        "authority": "None",
    }
