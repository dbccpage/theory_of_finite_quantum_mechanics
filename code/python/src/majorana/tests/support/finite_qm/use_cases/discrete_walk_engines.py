"""Phase 1 separating experiment and Phase 2 walk packet engines.

Decomposed from foundations.py monolith. Integrates with omega_engine crates.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Any

import numpy as np
import scipy.linalg
from scipy.linalg import expm

from omega_engine_projects.ms_majorana.code.tests.support.finite_qm.use_cases import cochain

from omega_engine_projects.ms_majorana.code.tests.support.finite_qm.domain.primitives import (
    I2,
    SIGMA_I,
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    HADAMARD_2,
    PHASE_S,
    kron_all,
)
from omega_engine_projects.ms_majorana.code.tests.support.finite_qm.use_cases.rungs import (
    CochainPacket,
    rational_pythagorean_frames_d2,
)


def evaluate_quartic_frame_sum_rational(
    psi: tuple[Fraction, Fraction],
    frame: list[tuple[Fraction, Fraction]]
) -> Fraction:
    """Evaluates the H013 quartic rival readout P_4(u) = (<u, psi>)^4 over an orthonormal frame in Q^2."""
    total = Fraction(0)
    for u in frame:
        dot = u[0] * psi[0] + u[1] * psi[1]
        total += dot ** 4
    return total


def evaluate_quadratic_frame_sum_rational(
    psi: tuple[Fraction, Fraction],
    frame: list[tuple[Fraction, Fraction]]
) -> Fraction:
    """Evaluates the standard quadratic Born readout P_2(u) = (<u, psi>)^2 over an orthonormal frame in Q^2."""
    total = Fraction(0)
    for u in frame:
        dot = u[0] * psi[0] + u[1] * psi[1]
        total += dot ** 2
    return total


def verify_quartic_frame_additivity_failure_exact() -> dict[str, Any]:
    """Executes the Phase 1 separating experiment testing the H013 quartic rival against frame additivity.

    Returns exact rational receipts demonstrating that:
    1. The standard quadratic readout P_2(u) = <u, psi>^2 sums to exactly 1 on all rational frames.
    2. The quartic rival P_4(u) = <u, psi>^4 fails frame additivity on Pythagorean frames,
       exhibiting an exact rational deficit of 288/625 on the (3, 4, 5) frame.
    """
    psi = (Fraction(1), Fraction(0))
    frames = rational_pythagorean_frames_d2()

    p2_sums = [evaluate_quadratic_frame_sum_rational(psi, f) for f in frames]
    p4_sums = [evaluate_quartic_frame_sum_rational(psi, f) for f in frames]
    deficits = [Fraction(1) - s for s in p4_sums]

    assert all(s == Fraction(1) for s in p2_sums), "Quadratic Born rule must sum to 1"

    assert p4_sums[0] == Fraction(1), "Standard basis sum is 1"
    assert p4_sums[1] == Fraction(337, 625), "Pythagorean (3, 4, 5) sum must be 337/625"
    assert deficits[1] == Fraction(288, 625), "Deficit must be exactly 288/625"
    assert p4_sums[2] == Fraction(21361, 28561), "Pythagorean (5, 12, 13) sum must be 21361/28561"

    return {
        "dimension": 2,
        "state": (str(psi[0]), str(psi[1])),
        "frames_tested": len(frames),
        "quadratic_frame_additivity": True,
        "quartic_frame_additivity": False,
        "quartic_sums": [str(s) for s in p4_sums],
        "quartic_deficits": [str(d) for d in deficits],
        "verdict": (
            "The H013 quartic rival fails the frame-additivity / noncontextuality contract on 2D frames. "
            "Under the same contract, only quadratic (degree p=2) readouts preserve frame additivity."
        ),
    }


def quartic_homogeneous_polynomial_reduction() -> dict[str, Any]:
    """Algebraic reduction of general homogeneous quartic polynomials under 2D frame additivity.

    Let P_4(x, y) = c_40 x^4 + c_31 x^3 y + c_22 x^2 y^2 + c_13 x y^3 + c_04 y^4.
    The frame additivity requirement P_4(x, y) + P_4(-y, x) = C for all x^2 + y^2 = 1 forces:
        c_13 = c_31
        c_22 = c_40 + c_04
    Substituting these conditions into P_4 yields:
        P_4(x, y) = (x^2 + y^2) * (c_40 x^2 + c_31 x y + c_04 y^2)
    On the unit circle x^2 + y^2 = 1, this identically reduces to the quadratic form:
        P_4(x, y)|_{S^1} = c_40 x^2 + c_31 x y + c_04 y^2.
    Hence, any frame-additive polynomial on the 2D sphere is identically quadratic (p = 2).
    """
    return {
        "forced_degree": 2,
        "constraint_symmetry": "c_13 == c_31",
        "constraint_trace": "c_22 == c_40 + c_04",
        "reduced_form": "(x^2 + y^2) * (c_40 x^2 + c_31 x y + c_04 y^2)",
        "restriction_on_sphere": "c_40 x^2 + c_31 x y + c_04 y^2",
        "conclusion": "Frame additivity forces all degree-4 polynomials on S^1 to collapse to quadratic form p=2.",
    }



def build_mzi_packet(weights: tuple[float, ...] | None = None) -> CochainPacket:
    """Rung 4: Direct constructor of Mach-Zehnder interferometer cochain packet.

    Vertices:
        0: In
        1: Arm A
        2: Arm B
        3: Out
    Edges:
        0: (0, 1)
        1: (0, 2)
        2: (1, 3)
        3: (2, 3)
    Faces:
        Loop around arms: ((0, 1), (2, 1), (3, -1), (1, -1))
    """
    mzi_complex = cochain.Complex(
        n_vertices=4,
        edges=((0, 1), (0, 2), (1, 3), (2, 3)),
        faces=(((0, 1), (2, 1), (3, -1), (1, -1)),),
        weights=weights,
    )
    return CochainPacket(mzi_complex)


def build_sorkin_3slit_packet(weights: tuple[float, ...] | None = None) -> CochainPacket:
    """Phase 2b: Constructs a 3-slit cochain complex where slit phase shifts are generated by 1-cochains.

    Vertices:
        0: Source / In
        1: Slit A
        2: Slit B
        3: Slit C
        4: Screen / Detector
    Edges (6 directed edges):
        0: (0, 1)  [Source -> Slit A]
        1: (0, 2)  [Source -> Slit B]
        2: (0, 3)  [Source -> Slit C]
        3: (1, 4)  [Slit A -> Detector]
        4: (2, 4)  [Slit B -> Detector]
        5: (3, 4)  [Slit C -> Detector]
    Faces (2-cells enforcing d1 d0 = 0):
        Loop AB: (0, 1) + (1, 4) - (2, 4) - (0, 2) => ((0, 1), (3, 1), (4, -1), (1, -1))
        Loop BC: (0, 2) + (2, 4) - (3, 4) - (0, 3) => ((1, 1), (4, 1), (5, -1), (2, -1))
        Loop CA: (0, 3) + (3, 4) - (1, 4) - (0, 1) => ((2, 1), (5, 1), (3, -1), (0, -1))
    """
    edges = ((0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4))
    faces = (
        ((0, 1), (3, 1), (4, -1), (1, -1)),
        ((1, 1), (4, 1), (5, -1), (2, -1)),
        ((2, 1), (5, 1), (3, -1), (0, -1)),
    )
    return CochainPacket(cochain.Complex(
        n_vertices=5,
        edges=edges,
        faces=faces,
        weights=weights,
    ))


def sorkin_3slit_phases_from_cochain(cochain_1: np.ndarray | Sequence[float]) -> np.ndarray:
    """Computes accumulated phases along slits A, B, C from a 6-edge 1-cochain.

    phi_A = edge_0 + edge_3
    phi_B = edge_1 + edge_4
    phi_C = edge_2 + edge_5
    """
    c = np.asarray(cochain_1, dtype=float)
    if c.shape != (6,):
        raise ValueError(f"1-cochain for 3-slit complex must have 6 edge values, got {c.shape}")
    phi_a = float(c[0] + c[3])
    phi_b = float(c[1] + c[4])
    phi_c = float(c[2] + c[5])
    return np.array([phi_a, phi_b, phi_c], dtype=float)


def sorkin_3slit_amplitudes_from_cochain(cochain_1: np.ndarray | Sequence[float]) -> tuple[complex, complex, complex]:
    """Generates normalized path amplitudes (a1, a2, a3) from 1-cochain phase shifts."""
    phases = sorkin_3slit_phases_from_cochain(cochain_1)
    inv_sqrt3 = 1.0 / math.sqrt(3.0)
    a1 = inv_sqrt3 * np.exp(1j * phases[0])
    a2 = inv_sqrt3 * np.exp(1j * phases[1])
    a3 = inv_sqrt3 * np.exp(1j * phases[2])
    return complex(a1), complex(a2), complex(a3)


def cayley_evolution_from_packet(
    packet: CochainPacket | cochain.Complex,
    tau: float | Fraction,
    steps: int = 1,
    initial_state: np.ndarray | None = None,
    cochain_flow: np.ndarray | None = None,
) -> dict[str, Any]:
    """Phase 2b: Exact rational Cayley evolution driven by 1-cochain flow on the graph.
    
    cay_tau(X) = (I - tau*X)(I + tau*X)^(-1) where X in so(V, Q) is the skew-symmetric
    directed flow generator induced by 1-cochains.
    """
    cx = packet.complex if isinstance(packet, CochainPacket) else packet
    n = cx.n_vertices
    if steps < 0:
        raise ValueError("steps must be non-negative")

    if cochain_flow is not None:
        raw_flow = list(cochain_flow)
        if len(raw_flow) != len(cx.edges):
            raise ValueError(f"cochain_flow shape must match number of edges ({len(cx.edges)})")
        flow = np.array([float(x) for x in raw_flow], dtype=float)
    else:
        raw_flow = [Fraction(x) for x in cx.weight_vector]
        flow = np.array([float(x) for x in raw_flow], dtype=float)

    X = np.zeros((n, n), dtype=float)
    for k, (u, v) in enumerate(cx.edges):
        val = float(flow[k])
        X[v, u] += val
        X[u, v] -= val

    # Verify skew-symmetry
    if not np.allclose(X, -X.T, atol=1e-12):
        raise ValueError("Flow generator must be skew-symmetric")

    # Exact rational Cayley transform when tau is Fraction or int
    is_exact_fraction = isinstance(tau, (Fraction, int))
    rational_u = None
    if is_exact_fraction:
        tau_frac = Fraction(tau)
        X_frac = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for k, (u, v) in enumerate(cx.edges):
            val_frac = Fraction(raw_flow[k])
            X_frac[v][u] += val_frac
            X_frac[u][v] -= val_frac
        I_frac = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        A_frac = [[I_frac[i][j] - tau_frac * X_frac[i][j] for j in range(n)] for i in range(n)]
        B_frac = [[I_frac[i][j] + tau_frac * X_frac[i][j] for j in range(n)] for i in range(n)]
        
        # Invert B_frac over Q via Gauss-Jordan elimination
        aug = [[Fraction(B_frac[i][j]) for j in range(n)] + [Fraction(1 if i == k else 0) for k in range(n)] for i in range(n)]
        for col in range(n):
            pivot_r = None
            for r in range(col, n):
                if aug[r][col] != 0:
                    pivot_r = r
                    break
            if pivot_r is None:
                raise ValueError("Matrix I + tau*X is singular over Q")
            if pivot_r != col:
                aug[col], aug[pivot_r] = aug[pivot_r], aug[col]
            pivot = aug[col][col]
            for c in range(2 * n):
                aug[col][c] /= pivot
            for r in range(n):
                if r != col and aug[r][col] != 0:
                    fac = aug[r][col]
                    for c in range(2 * n):
                        aug[r][c] -= fac * aug[col][c]
        B_inv_frac = [[aug[i][n + j] for j in range(n)] for i in range(n)]
        rational_u = [[sum(A_frac[i][k] * B_inv_frac[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

    tau_fl = float(tau)
    I_fl = np.eye(n, dtype=float)
    u_mat = (I_fl - tau_fl * X) @ np.linalg.inv(I_fl + tau_fl * X)
    is_orthogonal = bool(np.allclose(u_mat.T @ u_mat, I_fl, atol=1e-9))
    det_val = float(np.linalg.det(u_mat))

    # Evolve by steps
    u_evolved = np.linalg.matrix_power(u_mat, steps)
    
    evolved_state = None
    norm_preserved = True
    if initial_state is not None:
        s0 = np.asarray(initial_state, dtype=complex)
        if s0.shape != (n,):
            raise ValueError(f"initial_state shape must match vertex count ({n})")
        evolved_state = u_evolved @ s0
        norm_in = np.linalg.norm(s0)
        norm_out = np.linalg.norm(evolved_state)
        norm_preserved = bool(np.isclose(norm_in, norm_out, atol=1e-9))

    return {
        "dimension": n,
        "generator": X,
        "tau": tau,
        "steps": steps,
        "cayley_operator": u_mat,
        "evolution_operator": u_evolved,
        "rational_cayley": rational_u,
        "is_orthogonal": is_orthogonal,
        "det": det_val,
        "evolved_state": evolved_state,
        "norm_preserved": norm_preserved,
    }


def build_glued_simplex_packet() -> CochainPacket:
    """Constructs the canonical 4-vertex glued 2-simplex diamond cochain complex.

    Two 2-simplices Delta_A = (0, 1, 2) and Delta_B = (3, 2, 1) sharing edge (1, 2).
    """
    edges = ((0, 1), (1, 2), (2, 0), (2, 3), (3, 1))
    faces = (
        ((0, 1), (1, 1), (2, 1)),
        ((3, 1), (4, 1), (1, 1)),
    )
    return CochainPacket(cochain.Complex(n_vertices=4, edges=edges, faces=faces))


CABELLO_18_VECTORS: tuple[tuple[int, int, int, int], ...] = (
    (1, 1, 1, 1),
    (1, 1, 1, -1),
    (1, 1, 0, 0),
    (1, 1, -1, -1),
    (1, 0, 1, 0),
    (1, 0, 0, 1),
    (1, 0, 0, -1),
    (1, 0, -1, 0),
    (1, -1, 1, 1),
    (1, -1, 0, 0),
    (1, -1, -1, 1),
    (1, -1, -1, -1),
    (0, 1, 0, 1),
    (0, 1, 0, 0),
    (0, 1, -1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, -1),
    (0, 0, 0, 1),
)

CABELLO_9_BASES: tuple[tuple[int, int, int, int], ...] = (
    (3, 10, 16, 18),
    (5, 8, 14, 18),
    (6, 7, 14, 16),
    (1, 4, 10, 17),
    (1, 7, 11, 15),
    (2, 6, 12, 15),
    (2, 8, 9, 13),
    (3, 9, 12, 17),
    (4, 5, 11, 13),
)


def cabello_interface_from_packet(packet: CochainPacket | cochain.Complex | None = None) -> dict[str, Any]:
    """Phase 2b: Cabello 18-ray contextuality set and 9 orthogonal tetrads as a cochain measurement configuration.

    Verifies:
      1. All 9 bases are mutually orthogonal in Z^4.
      2. Regular hypergraph: each ray appears in exactly 2 tetrads.
      3. Mod-2 parity refutation: 9 bases != 2k, ruling out non-contextual {0, 1} valuations.
      4. State projector boundary defect vanishing: delta_AB(P_v) = 0 for all 18 pure state projectors.
      5. PSD admission filtering: unconstrained basic feasible vertices (lambda_min = -1/2, delta_AB = 1/2)
         are rejected via explicit positive-semidefinite (PSD) admission check combined with boundary defect vanishing
         (rather than positivity being derived from gluing alone), while all 18 physical rank-1 projectors are preserved without singleton collapse.
    """
    if packet is None:
        pkt = build_glued_simplex_packet()
    else:
        pkt = packet if isinstance(packet, CochainPacket) else CochainPacket(packet)

    assert pkt.verify_d1_d0_nilpotent(), "Packet must satisfy d1 d0 = 0"

    rays = [np.array(v, dtype=float) for v in CABELLO_18_VECTORS]
    n_rays = len(rays)
    n_bases = len(CABELLO_9_BASES)

    all_orthogonal = True
    for b in CABELLO_9_BASES:
        vecs = [rays[idx - 1] for idx in b]
        for i in range(4):
            for j in range(i + 1, 4):
                if not np.isclose(np.dot(vecs[i], vecs[j]), 0.0):
                    all_orthogonal = False
                    break

    degrees = [sum(1 for b in CABELLO_9_BASES if (i + 1) in b) for i in range(n_rays)]
    is_regular_degree_2 = all(d == 2 for d in degrees)

    parity_obstruction = (n_bases % 2 == 1) and is_regular_degree_2

    normal = np.array([1.0, 0.0, 0.0, 0.0], dtype=float)

    def boundary_deficit(rho_mat: np.ndarray) -> float:
        exp_val = float(normal @ rho_mat @ normal)
        return max(0.0, -exp_val)

    def is_psd(rho_mat: np.ndarray, tol: float = 1e-9) -> bool:
        evals = np.linalg.eigvalsh(rho_mat)
        return bool(np.all(evals >= -tol))

    def filter_state(rho_mat: np.ndarray) -> np.ndarray | None:
        if not is_psd(rho_mat):
            return None
        if boundary_deficit(rho_mat) > 1e-9:
            return None
        return rho_mat

    projectors = [np.outer(v, v) / np.dot(v, v) for v in rays]
    projector_deficits = [boundary_deficit(p) for p in projectors]
    all_projectors_defect_free = all(np.isclose(d, 0.0, atol=1e-12) for d in projector_deficits)
    all_projectors_psd = all(is_psd(p) for p in projectors)
    filtered_projectors = [filter_state(p) for p in projectors]
    all_projectors_survive = all(p is not None for p in filtered_projectors)

    distinct_projectors = True
    for i in range(n_rays):
        for j in range(i + 1, n_rays):
            if np.allclose(projectors[i], projectors[j], atol=1e-9):
                distinct_projectors = False
                break

    rho_non_psd_1 = np.array([
        [-0.5, 0.0, 0.0, 0.0],
        [0.0, 0.5, -0.25, 0.25],
        [0.0, -0.25, 0.5, -0.25],
        [0.0, 0.25, -0.25, 0.5],
    ], dtype=float)

    rho_non_psd_2 = np.array([
        [-0.5, 0.0, 0.0, 0.0],
        [0.0, 0.5, 0.25, 0.25],
        [0.0, 0.25, 0.5, 0.25],
        [0.0, 0.25, 0.25, 0.5],
    ], dtype=float)

    non_psd_rejected_1 = filter_state(rho_non_psd_1) is None
    non_psd_rejected_2 = filter_state(rho_non_psd_2) is None
    defect_non_psd_1 = boundary_deficit(rho_non_psd_1)
    defect_non_psd_2 = boundary_deficit(rho_non_psd_2)

    return {
        "num_rays": n_rays,
        "num_bases": n_bases,
        "all_bases_orthogonal": all_orthogonal,
        "is_regular_degree_2": is_regular_degree_2,
        "parity_obstruction": parity_obstruction,
        "all_projectors_defect_free": all_projectors_defect_free,
        "all_projectors_psd": all_projectors_psd,
        "all_projectors_survive": all_projectors_survive,
        "distinct_projectors_count": n_rays if distinct_projectors else -1,
        "non_psd_1_deficit": defect_non_psd_1,
        "non_psd_2_deficit": defect_non_psd_2,
        "non_psd_1_rejected": non_psd_rejected_1,
        "non_psd_2_rejected": non_psd_rejected_2,
    }


def monotone_admission_from_packet(
    packet: CochainPacket | cochain.Complex,
    keep_dim: int,
    cochain_vec: np.ndarray | None = None,
) -> dict[str, Any]:
    """Phase 2b: Signed permutation isometry B_n and monotone projection dissipation Delta_irr > 0.

    Decomposes cochain transformations into:
      1. Hyperoctahedral signed permutations B_n = O(n, Z) = S_n ltimes (Z_2)^n
         preserving l1 and l2 norms exactly.
      2. Monotone projection admissions P_keep dissipating an irreversible residue
         Delta_irr = ||x||_1 - ||P_keep x||_1 > 0 with PSD operator defect Delta_op >= 0.
    """
    cx = packet.complex if isinstance(packet, CochainPacket) else packet
    n = len(cx.edges)
    if keep_dim <= 0 or keep_dim >= n:
        raise ValueError(f"keep_dim must satisfy 0 < keep_dim < {n}, got {keep_dim}")

    if cochain_vec is not None:
        x = np.asarray(cochain_vec, dtype=float)
        if x.shape != (n,):
            raise ValueError(f"cochain_vec shape must match number of edges ({n})")
    else:
        x = np.array([float(cx.weight_vector[i]) * (1.0 if i % 2 == 0 else 2.0) for i in range(n)], dtype=float)

    M = np.zeros((n, n), dtype=float)
    for i in range(n):
        j = (i + 1) % n
        M[i, j] = -1.0 if i == 0 else 1.0

    is_signed_perm = (
        bool(np.allclose(M.T @ M, np.eye(n)))
        and all(val in (-1.0, 0.0, 1.0) for val in M.flat)
    )

    x_iso = M @ x
    l1_orig = float(np.sum(np.abs(x)))
    l1_iso = float(np.sum(np.abs(x_iso)))
    l2_orig = float(np.linalg.norm(x))
    l2_iso = float(np.linalg.norm(x_iso))

    isometry_l1_preserved = bool(np.isclose(l1_orig, l1_iso, atol=1e-12))
    isometry_l2_preserved = bool(np.isclose(l2_orig, l2_iso, atol=1e-12))

    p_keep = np.diag([1.0 if i < keep_dim else 0.0 for i in range(n)])
    x_proj = p_keep @ x
    l1_proj = float(np.sum(np.abs(x_proj)))

    delta_irr = float(l1_orig - l1_proj)
    delta_irr_positive = bool(delta_irr > 1e-12)

    delta_op = np.eye(n) - p_keep.T @ p_keep
    evals_defect = np.linalg.eigvalsh(delta_op)
    operator_defect_psd = bool(np.all(evals_defect >= -1e-12))

    return {
        "dimension": n,
        "keep_dim": keep_dim,
        "is_signed_permutation": is_signed_perm,
        "isometry_l1_preserved": isometry_l1_preserved,
        "isometry_l2_preserved": isometry_l2_preserved,
        "original_l1": l1_orig,
        "projected_l1": l1_proj,
        "delta_irr": delta_irr,
        "delta_irr_positive": delta_irr_positive,
        "operator_defect_psd": operator_defect_psd,
    }

__all__ = ['CABELLO_18_VECTORS', 'CABELLO_9_BASES', 'build_glued_simplex_packet', 'build_mzi_packet', 'build_sorkin_3slit_packet', 'cabello_interface_from_packet', 'cayley_evolution_from_packet', 'evaluate_quadratic_frame_sum_rational', 'evaluate_quartic_frame_sum_rational', 'monotone_admission_from_packet', 'quartic_homogeneous_polynomial_reduction', 'sorkin_3slit_amplitudes_from_cochain', 'sorkin_3slit_phases_from_cochain', 'verify_quartic_frame_additivity_failure_exact']
