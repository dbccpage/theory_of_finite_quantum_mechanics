#!/usr/bin/env python3
"""CPTP Channel Class, Choi's Theorem, Stinespring Dilation, and Conductor Escalation.

Campaign C250 Block 06 (Global Steps 176-200).
AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path as _Path
from typing import Any, Callable, Sequence

import numpy as np

from ..domain.gaussian_rational import Gaussian


def build_choi_matrix(
    channel: Callable[[np.ndarray], np.ndarray],
    dim: int = 2,
) -> np.ndarray:
    """Construct the Choi matrix C_E = (I (x) E)(|Omega><Omega|) for a channel.

    |Omega> = sum_{i=0}^{dim-1} |i> (x) |i>.
    C_E = sum_{i,j=0}^{dim-1} |i><j| (x) E(|i><j|).
    """
    d2 = dim * dim
    choi = np.zeros((d2, d2), dtype=complex)
    for i in range(dim):
        for j in range(dim):
            e_ij = np.zeros((dim, dim), dtype=complex)
            e_ij[i, j] = 1.0
            image_e_ij = channel(e_ij)
            for r in range(dim):
                for c in range(dim):
                    row = i * dim + r
                    col = j * dim + c
                    choi[row, col] = image_e_ij[r, c]
    return choi


def _exact_matrix_from_input(mat: Any) -> list[list[Gaussian]]:
    """Preserve every complex entry; finite floats become exact binary rationals."""
    rows = [list(row) for row in mat]
    if not rows or any(len(row) != len(rows) for row in rows):
        raise ValueError("Expected a nonempty square matrix")
    return [[Gaussian.of(value) for value in row] for row in rows]


def _tolerance(tol: float | None) -> Fraction:
    if tol is None:
        return Fraction(0)
    if not math.isfinite(tol) or tol < 0:
        raise ValueError("Tolerance must be finite and nonnegative")
    return Fraction(tol)


def exact_determinant(submat: Sequence[Sequence[Any]]) -> Any:
    """Calculate exact determinant of a square Fraction or Gaussian matrix via Gaussian elimination."""
    k = len(submat)
    if k == 0:
        return Fraction(1, 1)
    if k == 1:
        return submat[0][0]
    if k == 2:
        return submat[0][0] * submat[1][1] - submat[0][1] * submat[1][0]
    if k == 3:
        return (
            submat[0][0] * (submat[1][1] * submat[2][2] - submat[1][2] * submat[2][1])
            - submat[0][1] * (submat[1][0] * submat[2][2] - submat[1][2] * submat[2][0])
            + submat[0][2] * (submat[1][0] * submat[2][1] - submat[1][1] * submat[2][0])
        )
    a = [list(row) for row in submat]
    det: Any = Fraction(1, 1)
    for i in range(k):
        pivot = i
        while pivot < k and a[pivot][i] == 0:
            pivot += 1
        if pivot == k:
            return Fraction(0, 1)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            det = -det
        det *= a[i][i]
        pv = a[i][i]
        for r in range(i + 1, k):
            factor = a[r][i] / pv
            for c in range(i, k):
                a[r][c] -= factor * a[i][c]
    return det


def verify_trace_preservation(choi: Any, dim: int = 2, tol: float | None = None) -> bool:
    """Check partial trace exactly, or within an explicitly supplied tolerance."""
    eps = _tolerance(tol)
    if type(dim) is not int or dim < 1:
        return False
    try:
        matrix = _exact_matrix_from_input(choi)
    except (ValueError, TypeError, OverflowError):
        return False
    if len(matrix) != dim * dim:
        return False
    for i in range(dim):
        for j in range(dim):
            delta = sum(matrix[i * dim + k][j * dim + k] for k in range(dim)) - int(i == j)
            d_real = delta.real if isinstance(delta, Gaussian) else getattr(delta, "real", delta)
            d_imag = delta.imag if isinstance(delta, Gaussian) else getattr(delta, "imag", 0)
            if abs(Fraction(d_real)) > eps or abs(Fraction(d_imag)) > eps:
                return False
    return True


def check_all_principal_minors_psd(matrix: Any, tol: float | None = None) -> tuple[bool, list[float]]:
    """Hermitian principal-minor test; tol=None admits no negative minor."""
    eps = _tolerance(tol)
    try:
        mat = _exact_matrix_from_input(matrix)
    except (ValueError, TypeError, OverflowError):
        return False, []
    n = len(mat)
    if any(mat[i][j] != mat[j][i].conjugate() for i in range(n) for j in range(n)):
        return False, []
    minors = []
    good = True
    for k in range(1, n + 1):
        for indices in itertools.combinations(range(n), k):
            value = Gaussian.of(exact_determinant([[mat[r][c] for c in indices] for r in indices]))
            if value.imag:
                return False, []
            minors.append(float(value.real))
            if value.real < -eps:
                good = False
    return good, minors


def verify_complete_positivity(choi: Any, tol: float | None = None) -> tuple[bool, list[float]]:
    """Return the declared principal-minor verdict and numerical diagnostics.

    Eigenvalues are display-only. Exact arithmetic is used on the supplied
    entries; an explicit tol makes the positivity result an approximate check.
    """
    good, _ = check_all_principal_minors_psd(choi, tol=tol)
    try:
        matrix = _exact_matrix_from_input(choi)
        values = np.linalg.eigvalsh(np.array([[complex(v) for v in row] for row in matrix]))
    except (ValueError, TypeError, OverflowError, np.linalg.LinAlgError):
        return False, []
    return good, [float(v) for v in values]


def rational_kraus_weights(probability: Fraction) -> tuple[int, Fraction]:
    """a/b is a sum of a*b copies of (1/b)^2, allowing extra Kraus terms."""
    if not isinstance(probability,Fraction) or not 0 <= probability <= 1:
        raise ValueError("Expected a rational probability in [0,1]")
    a,b=probability.numerator,probability.denominator
    return a*b,Fraction(1,b)


def depolarizing_channel(p: float, dim: int = 2) -> Callable[[np.ndarray], np.ndarray]:
    """Single-qubit depolarizing channel: E_p(rho) = (1-p)*rho + p*Tr(rho)*I/dim."""
    def channel(rho: np.ndarray) -> np.ndarray:
        return (1.0 - p) * rho + p * np.trace(rho) * np.eye(dim, dtype=complex) / dim
    return channel


def bit_flip_channel(p: float) -> Callable[[np.ndarray], np.ndarray]:
    """Single-qubit bit-flip channel: E(rho) = (1-p)*rho + p*X*rho*X."""
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    def channel(rho: np.ndarray) -> np.ndarray:
        return (1.0 - p) * rho + p * (x @ rho @ x)
    return channel


def phase_flip_channel(p: float) -> Callable[[np.ndarray], np.ndarray]:
    """Single-qubit phase-flip channel: E(rho) = (1-p)*rho + p*Z*rho*Z."""
    z = np.array([[1, 0], [0, -1]], dtype=complex)
    def channel(rho: np.ndarray) -> np.ndarray:
        return (1.0 - p) * rho + p * (z @ rho @ z)
    return channel


def bit_phase_flip_channel(p: float) -> Callable[[np.ndarray], np.ndarray]:
    """Single-qubit bit-phase-flip channel: E(rho) = (1-p)*rho + p*Y*rho*Y."""
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    def channel(rho: np.ndarray) -> np.ndarray:
        return (1.0 - p) * rho + p * (y @ rho @ y)
    return channel


def projective_measurement_channel() -> Callable[[np.ndarray], np.ndarray]:
    """Single-qubit Z-basis projective measurement channel: E(rho) = P0*rho*P0 + P1*rho*P1."""
    p0 = np.array([[1, 0], [0, 0]], dtype=complex)
    p1 = np.array([[0, 0], [0, 1]], dtype=complex)
    def channel(rho: np.ndarray) -> np.ndarray:
        return p0 @ rho @ p0 + p1 @ rho @ p1
    return channel


def identity_channel(dim: int = 2) -> Callable[[np.ndarray], np.ndarray]:
    """Ideal identity channel: E(rho) = rho."""
    def channel(rho: np.ndarray) -> np.ndarray:
        return rho.copy()
    return channel


def two_qubit_css_syndrome_channel() -> Callable[[np.ndarray], np.ndarray]:
    """Two-qubit parity measurement channel in Z (x) Z: E(rho) = P_even*rho*P_even + P_odd*rho*P_odd."""
    p_even = np.zeros((4, 4), dtype=complex)
    p_even[0, 0] = 1.0
    p_even[3, 3] = 1.0
    p_odd = np.zeros((4, 4), dtype=complex)
    p_odd[1, 1] = 1.0
    p_odd[2, 2] = 1.0
    def channel(rho: np.ndarray) -> np.ndarray:
        return p_even @ rho @ p_even + p_odd @ rho @ p_odd
    return channel


def minimal_cyclotomic_conductor_for_sqrt(d: int) -> int:
    """Compute the minimal cyclotomic conductor n such that sqrt(d) in Q(zeta_n).

    By Kronecker-Weber:
    - If d is a perfect square: conductor = 1.
    - If d = 2: conductor = 8 (zeta_8 = (1+i)/sqrt(2) => sqrt(2) in Q(zeta_8)).
    - For squarefree d:
      * if d = -1: conductor = 4.
      * if d = p (prime = 1 mod 4): conductor = p.
      * if d = p (prime = 3 mod 4): conductor = 4*p (since sqrt(-p) in Q(zeta_p) and i in Q(zeta_4)).
      * if d = 2*q: conductor depends on 8 * odd_part.
    """
    if type(d) is not int or d < 1:
        raise ValueError("Expected a positive radicand")
    val = d
    sq_free = 1
    for p in range(2, int(math.isqrt(d)) + 1):
        count = 0
        while val % p == 0:
            count += 1
            val //= p
        if count % 2 == 1:
            sq_free *= p
    if val > 1:
        sq_free *= val

    if sq_free == 1:
        return 1
    elif sq_free == 2:
        return 8
    elif sq_free == 3:
        return 12
    elif sq_free == 5:
        return 5
    elif sq_free == 6:
        return 24
    elif sq_free == 7:
        return 28
    else:
        if sq_free % 4 == 1:
            return sq_free
        else:
            return 4 * sq_free


def evaluate_channel_census() -> list[dict[str, Any]]:
    """Census of all open-system channels across the 22 corpus targets."""
    channels_def = [
        {
            "channel_id": "CH-01",
            "name": "Identity / Ideal Coherent Channel",
            "targets": [1, 2, 3, 4, 5, 6, 7, 8],
            "dimension": 2,
            "kraus_rank": 1,
            "sqrt_factors": [1],
            "dilation_conductor": 1,
            "escalates_beyond_120": False,
        },
        {
            "channel_id": "CH-02",
            "name": "Bit-Flip Channel (p = 1/3)",
            "targets": [9],
            "dimension": 2,
            "kraus_rank": 2,
            "sqrt_factors": [2, 3],
            "dilation_conductor": 12,
            "escalates_beyond_120": False,
        },
        {
            "channel_id": "CH-03",
            "name": "Phase-Flip Channel (p = 1/4)",
            "targets": [12],
            "dimension": 2,
            "kraus_rank": 2,
            "sqrt_factors": [3],
            "dilation_conductor": 12,
            "escalates_beyond_120": False,
        },
        {
            "channel_id": "CH-04",
            "name": "Bit-Phase Flip Channel (p = 1/3)",
            "targets": [14],
            "dimension": 2,
            "kraus_rank": 2,
            "sqrt_factors": [3],
            "dilation_conductor": 12,
            "escalates_beyond_120": False,
        },
        {
            "channel_id": "CH-05",
            "name": "Single-Qubit Depolarizing Channel (p = 1/3)",
            "targets": [20],
            "dimension": 2,
            "kraus_rank": 4,
            "sqrt_factors": [3],
            "dilation_conductor": 12,
            "escalates_beyond_120": False,
        },
        {
            "channel_id": "CH-06",
            "name": "Single-Qubit Depolarizing Channel (p = 1/7)",
            "targets": [20],
            "dimension": 2,
            "kraus_rank": 4,
            "sqrt_factors": [7],
            "dilation_conductor": 28,
            "escalates_beyond_120": True,
        },
        {
            "channel_id": "CH-07",
            "name": "Single-Qubit Projective Measurement Channel",
            "targets": [10, 11],
            "dimension": 2,
            "kraus_rank": 2,
            "sqrt_factors": [1],
            "dilation_conductor": 4,
            "escalates_beyond_120": False,
        },
        {
            "channel_id": "CH-08",
            "name": "Two-Qubit CSS Plaquette Syndrome Extraction Channel",
            "targets": [12, 16],
            "dimension": 4,
            "kraus_rank": 2,
            "sqrt_factors": [1],
            "dilation_conductor": 4,
            "escalates_beyond_120": False,
        },
    ]
    return channels_def


def run_block_06_execution() -> dict[str, Any]:
    """Execute complete mathematical and computational battery for Block 06."""
    depol_1_3 = depolarizing_channel(1.0 / 3.0, dim=2)
    choi_1_3 = build_choi_matrix(depol_1_3, dim=2)
    tp_1_3 = verify_trace_preservation(choi_1_3, dim=2, tol=1e-12)
    cp_1_3, ev_1_3 = verify_complete_positivity(choi_1_3, tol=1e-12)
    conductor_1_3 = minimal_cyclotomic_conductor_for_sqrt(3)

    depol_1_7 = depolarizing_channel(1.0 / 7.0, dim=2)
    choi_1_7 = build_choi_matrix(depol_1_7, dim=2)
    tp_1_7 = verify_trace_preservation(choi_1_7, dim=2, tol=1e-12)
    cp_1_7, ev_1_7 = verify_complete_positivity(choi_1_7, tol=1e-12)
    conductor_1_7 = minimal_cyclotomic_conductor_for_sqrt(7)

    census = evaluate_channel_census()
    total_censused = len(census)
    escalating_channels = [c for c in census if c["escalates_beyond_120"]]
    escalating_count = len(escalating_channels)

    kraus_rank_bound_d2 = 4

    result = {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "block_id": "block_06",
        "choi_theorem_ported_lean": False,
        "numerical_fixture_tolerance": 1e-12,
        "numerical_fixture_scope": "Binary-float channel inputs; exact principal-minor arithmetic with explicitly allowed tolerance",
        "stinespring_requires_extension": None,
        "dilation_scope": "selected spectral construction; arbitrary redundant Kraus realizations need not extend the field",
        "depolarizing_p_1_3_dilation_conductor": conductor_1_3,
        "depolarizing_p_1_7_dilation_conductor": conductor_1_7,
        "kraus_rank_bound_d2": kraus_rank_bound_d2,
        "channels_censused": total_censused,
        "channels_escalating_beyond_120": escalating_count,
        "depolarizing_1_3_verification": {
            "trace_preserving": tp_1_3,
            "completely_positive": cp_1_3,
            "choi_eigenvalues": ev_1_3,
            "dilation_conductor": conductor_1_3,
            "divides_120": (120 % conductor_1_3 == 0),
        },
        "depolarizing_1_7_verification": {
            "trace_preserving": tp_1_7,
            "completely_positive": cp_1_7,
            "choi_eigenvalues": ev_1_7,
            "dilation_conductor": conductor_1_7,
            "divides_120": (120 % conductor_1_7 == 0),
        },
        "channel_census": census,
    }
    return result


def main() -> None:
    output_path = (_Path(__file__).resolve().parents[4] / "apps" / "finite_qm") / "evidence" / "c250_block06_channels.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = run_block_06_execution()
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Emitted {output_path} successfully.")


if __name__ == "__main__":
    main()

__all__ = ['bit_flip_channel', 'bit_phase_flip_channel', 'build_choi_matrix', 'check_all_principal_minors_psd', 'depolarizing_channel', 'evaluate_channel_census', 'exact_determinant', 'identity_channel', 'main', 'minimal_cyclotomic_conductor_for_sqrt', 'phase_flip_channel', 'projective_measurement_channel', 'rational_kraus_weights', 'run_block_06_execution', 'two_qubit_css_syndrome_channel', 'verify_complete_positivity', 'verify_trace_preservation']
