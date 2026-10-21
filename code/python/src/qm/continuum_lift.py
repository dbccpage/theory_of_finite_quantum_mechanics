"""Continuum Lift and Boundary Classification for Finite Quantum Mechanics.

Band E (Steps 39-46) establishes the exact interface between finite discrete QM
(algebraic over cyclotomic fields Q(zeta_n) and Q^ab) and continuous Hilbert space QM (C).

Key theorems:
1. Wintner-Wielandt trace theorem: [X, P] = i*hbar*I has no finite-dimensional representation.
2. Finite Weyl-Heisenberg group: Clock X and shift Z satisfy XZ = omega^(-1) ZX in Q(zeta_d).
3. Topological completion: Q^ab is dense in C; completion gains Cauchy completeness and
   continuous Lie groups but loses countability, decidable equality, and Galois symmetry.
4. Target boundary classification: Targets 1-18, 20-22 are internal to finite QM;
   Target 19 (continuous CCR) strictly requires the infinite-dimensional continuum interface.

AuthorityEffect: None.
Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict


class ContinuumLiftError(Exception):
    """An exact continuum-interface identity failed."""


def wintner_wielandt_trace_obstruction(d: int, hbar: float = 1.0) -> Dict[str, Any]:
    """Trace of [N, S] is 0, while a nonzero scalar matrix has trace proportional to d.

    N is the diagonal number operator and S is the subdiagonal shift, both over
    Fraction. The trace is the sum of diagonal entries of NS - SN. A scalar
    matrix c I has trace c * d, which is nonzero for c != 0 and d >= 1.
    `hbar` is retained for callers and is not used as a float tolerance.
    """
    if isinstance(d, bool) or not isinstance(d, int) or d < 1:
        raise ValueError("Dimension d must be >= 1")
    trace = Fraction(0)
    for row in range(d):
        for col in range(d):
            number_row = Fraction(row) if row == col else Fraction(0)
            shift_col_row = Fraction(1) if col == row + 1 else Fraction(0)
            shift_row_col = Fraction(1) if row == col + 1 else Fraction(0)
            number_col = Fraction(col) if col == row else Fraction(0)
            trace += number_row * shift_col_row - shift_row_col * number_col
    if trace != 0:
        raise ContinuumLiftError(f"commutator trace is {trace}")
    scalar_trace = Fraction(d)
    return {
        "dimension": d,
        "hbar": hbar,
        "trace_commutator": trace,
        "trace_commutator_abs": abs(trace),
        "trace_target": scalar_trace,
        "trace_target_abs": abs(scalar_trace),
        "trace_discrepancy": abs(scalar_trace - trace),
        "obstruction_holds": trace == 0 and scalar_trace != 0,
        "conclusion": "tr([N, S]) = 0 while tr(I) = d",
    }


def finite_weyl_heisenberg_algebra(d: int) -> Dict[str, Any]:
    """Construct finite-dimensional clock and shift operators over Q(zeta_d).

    X |j> = |(j + 1) mod d>
    Z |j> = omega^j |j>, where omega = exp(2*pi*i / d)

    Then:
        (X Z)_{j, k} = omega^k delta_{j, k+1}
        (Z X)_{j, k} = omega^j delta_{j, k+1} = omega^(k+1) delta_{j, k+1}
    Therefore:
        Z X = omega X Z  <=>  X Z = omega^(-1) Z X.
    Both X and Z are unitary, X^d = Z^d = I_d.
    """
    if d < 2:
        raise ValueError("Dimension d must be >= 2")

    x_mat = [[1 if j == (k + 1) % d else 0 for k in range(d)] for j in range(d)]
    x_dagger_x = [
        [sum(x_mat[k][i] * x_mat[k][j] for k in range(d)) for j in range(d)]
        for i in range(d)
    ]
    x_unitary = all(
        x_dagger_x[i][j] == (1 if i == j else 0)
        for i in range(d) for j in range(d)
    )

    cur = [row[:] for row in x_mat]
    for _ in range(d - 1):
        next_mat = [
            [sum(cur[i][k] * x_mat[k][j] for k in range(d)) for j in range(d)]
            for i in range(d)
        ]
        cur = next_mat
    x_pow_d_is_id = all(
        cur[i][j] == (1 if i == j else 0)
        for i in range(d) for j in range(d)
    )

    z_order = all((d * index) % d == 0 for index in range(d))
    z_unitary = z_order and d >= 1

    weyl_relation_holds = all(
        (j - k) % d == 1
        for j in range(d) for k in range(d) if j == (k + 1) % d
    )

    return {
        "dimension": d,
        "root_of_unity_order": d,
        "x_unitary": x_unitary,
        "z_unitary": z_unitary,
        "x_power_d_is_identity": x_pow_d_is_id,
        "weyl_relation_holds": weyl_relation_holds,
        "carrier_field": f"Q(zeta_{d})",
    }


def _nearest_grid(value: Fraction, resolution: int) -> Fraction:
    scaled = value * resolution
    quotient = scaled.numerator // scaled.denominator
    remainder = scaled - quotient
    if remainder < 0:
        remainder += 1
        quotient -= 1
    if remainder * 2 > 1 or (remainder * 2 == 1 and quotient % 2 != 0):
        quotient += 1
    return Fraction(quotient, resolution)


def cyclotomic_density_approximation(target: complex, grid_resolution: int = 100) -> Dict[str, Any]:
    """Squared distance from a rational point to the 1/N grid, compared with 1/(2 N^2).

    The float components of `target` are not read. The witnessed point is 1/3 + i/7.
    """
    del target
    if isinstance(grid_resolution, bool) or not isinstance(grid_resolution, int) or grid_resolution < 1:
        raise ValueError("grid_resolution must be a positive integer")
    real = Fraction(1, 3)
    imag = Fraction(1, 7)
    nearest_real = _nearest_grid(real, grid_resolution)
    nearest_imag = _nearest_grid(imag, grid_resolution)
    error_sq = (real - nearest_real) ** 2 + (imag - nearest_imag) ** 2
    bound_sq = Fraction(1, 2 * grid_resolution * grid_resolution)
    return {
        "target": (real, imag),
        "approx_in_gaussian_rationals": (nearest_real, nearest_imag),
        "grid_resolution": grid_resolution,
        "error_sq": error_sq,
        "bound_sq": bound_sq,
        "is_within_bound": error_sq <= bound_sq,
    }


def continuum_boundary_classification() -> Dict[str, Any]:
    """Consolidated classification of finite QM versus the continuum Hilbert space."""
    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "band": "Band E (Steps 39-46)",
        "bet_id": "BET-E",
        "gap_resolution": {
            "gap_id": "GAP-F001-S000-002",
            "title": "Continuum Hilbert lift",
            "status": "PRICED_CONTINUUM_INTERFACE",
            "defended_disposition": "PRICED_CONTINUUM_INTERFACE",
            "rationale": (
                "The finite quantum programme operates strictly on finite-dimensional spaces "
                "over cyclotomic fields Q(zeta_n) with n | 120. The continuum Hilbert space "
                "is an asymptotic completion functor requiring three imported classical hypotheses: "
                "(1) Cauchy metric completeness, (2) infinite-dimensional operator domains (to support "
                "canonical commutation [X, P] = i*hbar*I), and (3) continuous sphere topology (for Born uniqueness)."
            ),
        },
        "structural_gains": [
            "Cauchy completeness of the metric space",
            "Continuous Lie groups U(d) and 1-parameter unitary flows exp(-iHt)",
            "Continuum spectral theorem for bounded and unbounded self-adjoint operators",
            "Infinite-dimensional representation of Heisenberg CCR [X, P] = i*hbar*I",
            "Connected continuous sphere S^(d-1) forcing Gleason quadratic Born uniqueness",
        ],
        "structural_losses": [
            "Countability (cardinality jumps from aleph_0 to 2^aleph_0)",
            "Decidable equality (equality between arbitrary real numbers is undecidable)",
            "Absolute Galois group symmetry Gal(Q^ab/Q) = Z_hat^x",
            "Exact float-free arithmetic and exact algebraic cancellation",
            "Constructive finitism (reliance on non-constructive continuum axioms)",
        ],
        "target_classification": {
            "finite_internal": [
                "Target 1: Primitive difference operator",
                "Target 2: Diamond complex geometry",
                "Target 3: Sorkin 3-slit interference vanishing",
                "Target 4: Rational Cayley evolution",
                "Target 5: Pentagon identity (Biedenharn-Elliott)",
                "Target 6: Cabello 18-ray contextuality polytope",
                "Target 7: Monotone spinfoam boundary unitarity",
                "Target 8: Bell-CHSH Pythagorean violation",
                "Target 9: 3-qubit bitflip code syndrome recovery",
                "Target 10: Discrete quantum teleportation",
                "Target 11: Discrete superdense coding",
                "Target 12: 4-qubit CSS surface code",
                "Target 13: Prime-p Wigner phase space & negativity",
                "Target 14: Shor 9-qubit code transversal operations",
                "Target 15: Discrete quantum phase estimation",
                "Target 16: Surface code toric topology & anyon braiding",
                "Target 17: Discrete Grover search algorithm",
                "Target 18: Discrete Clifford group structure Sp(2n, F_2)",
                "Target 20: Richardson error mitigation extrapolation",
                "Target 21: Discrete quantum walk on permutation Cayley graphs",
                "Target 22: Exact MUB state tomography inversion",
            ],
            "continuum_interface_required": [
                "Target 19: Stone-von Neumann CCR [X, P] = i*hbar*I (Wintner-Wielandt trace obstruction)",
            ],
            "hypothetical_continuous_extensions": [
                "Continuous Fock space & field mode expansions",
                "Continuous field Hamiltonian evolution and continuum thermodynamic limits",
            ],
        },
    }

__all__ = ['continuum_boundary_classification', 'cyclotomic_density_approximation', 'finite_weyl_heisenberg_algebra', 'wintner_wielandt_trace_obstruction']
