r"""
Finite-Regime Quantum Mechanics Engine (`finite_qm_engine`).

Decomposes finite quantum mechanics across the 6-rung ingredient ladder (QM_121)
and 5-group obligation register (QM_211).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass(frozen=True)
class Rung1BornRedundancy:
    """Rung 1: P = w / sum w. Complex amplitude square ||c||^2 / sum ||c||^2 is redundant."""
    weights: np.ndarray
    probabilities: np.ndarray
    amplitude_probabilities: Optional[np.ndarray]
    redundancy_verified: bool


@dataclass(frozen=True)
class Rung2DensityPurity:
    """Rung 2: Density matrix rho = diag(p), trace=1, PSD, purity sum p^2 in (0, 1]."""
    rho_diag: np.ndarray
    trace: float
    is_psd: bool
    purity: float
    mixedness: float
    off_diagonal_mass: float


@dataclass(frozen=True)
class Rung3CPTPShadow:
    """Rung 3: CPTP channel to stochastic population shadow kernel K(y|x)."""
    stochastic_kernel: np.ndarray
    is_column_stochastic: bool
    trace_preserving: bool


@dataclass(frozen=True)
class Rung4PathSum:
    """Rung 4: Finite path sum M^(m+n) = M^m M^n (Chapman-Kolmogorov)."""
    step_matrix: np.ndarray
    power_matrix: np.ndarray
    chapman_kolmogorov_holds: bool


@dataclass(frozen=True)
class Rung5SuperpositionFiber:
    """Rung 5: Quotient fiber U(1)^(|E_w|-1) over nonzero support E_w."""
    nonzero_support_size: int
    fiber_dimension: int
    global_phase_invisible: bool
    relative_phase_visible: bool


@dataclass(frozen=True)
class Rung6InterferenceCrossTerm:
    """Rung 6: Non-l1 cross-term 2 Re(c_i c_j*) and QC buildability set S."""
    l1_sum: float
    l2_interfered_mass: float
    cross_term: float
    is_non_l1_computable: bool


class FiniteQMEngine:
    """Core engine evaluating the 6-rung ingredient ladder for finite-regime QM."""

    @staticmethod
    def rung_1_born_redundancy(
        weights: np.ndarray,
        amplitudes: Optional[np.ndarray] = None
    ) -> Rung1BornRedundancy:
        """Evaluates Rung 1: classical l1 probability normalization."""
        weights = np.asarray(weights, dtype=float)
        w_sum = np.sum(weights)
        if w_sum <= 0:
            probs = np.zeros_like(weights)
        else:
            probs = weights / w_sum

        amp_probs = None
        redundancy_verified = True
        if amplitudes is not None:
            amps = np.asarray(amplitudes, dtype=complex)
            amp_sq = np.abs(amps) ** 2
            amp_sum = np.sum(amp_sq)
            if amp_sum > 0:
                amp_probs = amp_sq / amp_sum
                redundancy_verified = bool(np.allclose(probs, amp_probs))
            else:
                amp_probs = np.zeros_like(amp_sq)

        return Rung1BornRedundancy(
            weights=weights,
            probabilities=probs,
            amplitude_probabilities=amp_probs,
            redundancy_verified=redundancy_verified,
        )

    @staticmethod
    def rung_2_density_purity(weights: np.ndarray) -> Rung2DensityPurity:
        """Evaluates Rung 2: diagonal density embedding rho = diag(p)."""
        r1 = FiniteQMEngine.rung_1_born_redundancy(weights)
        p = r1.probabilities
        rho = np.diag(p)
        tr = float(np.trace(rho))
        evals = np.linalg.eigvalsh(rho)
        is_psd = bool(np.all(evals >= -1e-12))
        pur = float(np.sum(p ** 2))
        mix = float(1.0 - pur)
        off_diag = 0.0

        return Rung2DensityPurity(
            rho_diag=rho,
            trace=tr,
            is_psd=is_psd,
            purity=pur,
            mixedness=mix,
            off_diagonal_mass=off_diag,
        )

    @staticmethod
    def rung_3_cptp_shadow(kraus_ops: List[np.ndarray]) -> Rung3CPTPShadow:
        """Evaluates Rung 3: CPTP channel population shadow kernel K(y|x)."""
        dim = kraus_ops[0].shape[0]
        completeness = np.sum([A.conj().T @ A for A in kraus_ops], axis=0)
        trace_preserving = bool(np.allclose(completeness, np.eye(dim)))

        kernel = np.zeros((dim, dim), dtype=float)
        for x in range(dim):
            for y in range(dim):
                kernel[y, x] = np.sum([np.abs(A[y, x]) ** 2 for A in kraus_ops])

        col_sums = np.sum(kernel, axis=0)
        is_col_stoch = bool(np.allclose(col_sums, np.ones(dim)))

        return Rung3CPTPShadow(
            stochastic_kernel=kernel,
            is_column_stochastic=is_col_stoch,
            trace_preserving=trace_preserving,
        )

    @staticmethod
    def rung_4_path_sum(step_matrix: np.ndarray, steps: int) -> Rung4PathSum:
        """Evaluates Rung 4: Chapman-Kolmogorov path sum matrix power M^n."""
        M = np.asarray(step_matrix, dtype=float)
        Mn = np.linalg.matrix_power(M, steps)

        a = steps // 2
        b = steps - a
        Ma = np.linalg.matrix_power(M, a)
        Mb = np.linalg.matrix_power(M, b)
        ck_holds = bool(np.allclose(Mn, Ma @ Mb))

        return Rung4PathSum(
            step_matrix=M,
            power_matrix=Mn,
            chapman_kolmogorov_holds=ck_holds,
        )

    @staticmethod
    def rung_5_superposition_fiber(amplitudes: np.ndarray) -> Rung5SuperpositionFiber:
        """Evaluates Rung 5: quotient fiber U(1)^(|E_w|-1) over nonzero support."""
        amps = np.asarray(amplitudes, dtype=complex)
        nonzero_mask = np.abs(amps) > 1e-12
        nz_count = int(np.sum(nonzero_mask))
        fiber_dim = max(0, nz_count - 1)

        return Rung5SuperpositionFiber(
            nonzero_support_size=nz_count,
            fiber_dimension=fiber_dim,
            global_phase_invisible=True,
            relative_phase_visible=(fiber_dim > 0),
        )

    @staticmethod
    def rung_6_interference_cross_term(amplitudes: np.ndarray) -> Rung6InterferenceCrossTerm:
        """Evaluates Rung 6: non-l1 cross-term 2 Re(c_i c_j*)."""
        amps = np.asarray(amplitudes, dtype=complex)
        l1_sum = float(np.sum(np.abs(amps) ** 2))
        total_amp = np.sum(amps)
        l2_interfered = float(np.abs(total_amp) ** 2)
        cross = float(l2_interfered - l1_sum)

        return Rung6InterferenceCrossTerm(
            l1_sum=l1_sum,
            l2_interfered_mass=l2_interfered,
            cross_term=cross,
            is_non_l1_computable=bool(np.abs(cross) > 1e-12),
        )


def evaluate_6rung_ladder(
    weights: np.ndarray,
    amplitudes: np.ndarray,
    kraus_ops: List[np.ndarray],
    step_matrix: np.ndarray,
    steps: int = 3,
) -> Dict[str, Any]:
    """Computes full 6-rung ladder metrics with nonclaim box and AuthorityEffect: None."""
    r1 = FiniteQMEngine.rung_1_born_redundancy(weights, amplitudes)
    r2 = FiniteQMEngine.rung_2_density_purity(weights)
    r3 = FiniteQMEngine.rung_3_cptp_shadow(kraus_ops)
    r4 = FiniteQMEngine.rung_4_path_sum(step_matrix, steps)
    r5 = FiniteQMEngine.rung_5_superposition_fiber(amplitudes)
    r6 = FiniteQMEngine.rung_6_interference_cross_term(amplitudes)

    return {
        "authority_effect": "None",
        "nonclaim_box": {
            "supports": "6-rung ingredient ladder decomposition of finite-regime QM",
            "does_not_support": "Derivation of Born rule or C/U(1) phase carrier without structural imports",
            "narrowest_defensible_claim": "QM decomposes into classical l1 base (Rungs 1-4), phase fiber (Rung 5), interference cross-term (Rung 6), and 8 explicit recovery imports",
            "next_test_needed": "Drop-one failure verification across all 8 B8 recovery slots",
        },
        "rung_1_born": {
            "probabilities": r1.probabilities.tolist(),
            "redundancy_verified": r1.redundancy_verified,
        },
        "rung_2_density": {
            "purity": r2.purity,
            "mixedness": r2.mixedness,
            "is_psd": r2.is_psd,
            "off_diagonal_mass": r2.off_diagonal_mass,
        },
        "rung_3_cptp_shadow": {
            "stochastic_kernel": r3.stochastic_kernel.tolist(),
            "is_column_stochastic": r3.is_column_stochastic,
            "trace_preserving": r3.trace_preserving,
        },
        "rung_4_path_sum": {
            "power_matrix": r4.power_matrix.tolist(),
            "chapman_kolmogorov_holds": r4.chapman_kolmogorov_holds,
        },
        "rung_5_phase_fiber": {
            "nonzero_support_size": r5.nonzero_support_size,
            "fiber_dimension": r5.fiber_dimension,
        },
        "rung_6_interference": {
            "l1_sum": r6.l1_sum,
            "l2_interfered_mass": r6.l2_interfered_mass,
            "cross_term": r6.cross_term,
            "is_non_l1_computable": r6.is_non_l1_computable,
        },
    }

def _matmul(left, right):
    size = len(left)
    return tuple(
        tuple(
            sum((left[row][k] * right[k][col] for k in range(size)), Fraction(0))
            for col in range(size)
        )
        for row in range(size)
    )


def exact_ladder_cross_term() -> Fraction:
    """Chapman–Kolmogorov defect of a rational permutation, then the cross term.

    The step matrix is the 3-cycle. M^2 M is compared with M^3. The returned
    value is the interference cross term of amplitudes (1, -1), which is -2,
    after that defect has been checked.
    """
    step = (
        (Fraction(0), Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
    )
    square = _matmul(step, step)
    cube_by_square = _matmul(square, step)
    cube_by_power = _matmul(step, square)
    defect = Fraction(0)
    for row in range(3):
        for col in range(3):
            defect += abs(cube_by_square[row][col] - cube_by_power[row][col])
    if defect != 0:
        raise ValueError(f"Chapman-Kolmogorov defect is {defect}")
    amplitudes = (Fraction(1), Fraction(-1))
    born = amplitudes[0] ** 2 + amplitudes[1] ** 2
    interfered = (amplitudes[0] + amplitudes[1]) ** 2
    return interfered - born


__all__ = ['FiniteQMEngine', 'Rung1BornRedundancy', 'Rung2DensityPurity', 'Rung3CPTPShadow', 'Rung4PathSum', 'Rung5SuperpositionFiber', 'Rung6InterferenceCrossTerm', 'evaluate_6rung_ladder', 'exact_ladder_cross_term']
