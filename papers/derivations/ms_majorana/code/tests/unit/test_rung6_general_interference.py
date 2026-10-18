"""
Executable Python dual for W4.4 (QMREG 51 / TOY-MECH):
Rung 6 verification at general |E| — interference cross-term is non-L1.

Honest residual: signed / complex continuum estate exit not claimed.
Matches Lean `003_qm_rung6_general_interference.lean`:

* general cross-term expansion identity
* multi-sector Fin-3 ampA=(1,1,1), ampB=(1,1,-1):
  same sum of squares (3), different coherent sum (9 vs 1),
  pairwise cross-term sums (6 vs -2)
* multi_sector_cross_term_non_l1

AuthorityEffect: None. No Wave-4 exit claim.
"""

import pytest
import math
import cmath
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Amplitudes:
    coords: Sequence[complex]

    @property
    def N(self) -> int:
        return len(self.coords)

    @property
    def l1_diagonal_weights(self) -> list[float]:
        """Classical L1 sector weights w_k = |c_k|^2."""
        return [abs(c) ** 2 for c in self.coords]

    @property
    def l1_mass_sum(self) -> float:
        """Classical L1 mass sum sum |c_k|^2."""
        return sum(self.l1_diagonal_weights)

    @property
    def cross_term_sum(self) -> float:
        """Non-L1 interference cross-term sum_{j < k} 2 Re(c_j c_k*)."""
        acc = 0.0
        for j in range(self.N):
            for k in range(j + 1, self.N):
                acc += 2.0 * (self.coords[j] * self.coords[k].conjugate()).real
        return acc

    @property
    def total_readout_probability(self) -> float:
        """Total readout probability |sum c_k|^2."""
        return abs(sum(self.coords)) ** 2


# --- Lean dual: signed Int Fin-3 multi-sector lifts ---


def sum_squares_int(a: Sequence[int]) -> int:
    """Lean sumSquares."""
    return sum(x * x for x in a)


def coherent_sum_sq_int(a: Sequence[int]) -> int:
    """Lean coherentSumSq."""
    s = sum(a)
    return s * s


def pairwise_cross_term_sum_int(a: Sequence[int]) -> int:
    """Lean pairwiseCrossTermSum: 2 * sum_{j<k} a_j a_k."""
    acc = 0
    n = len(a)
    for j in range(n):
        for k in range(j + 1, n):
            acc += a[j] * a[k]
    return 2 * acc


# Lean ampA = (1,1,1), ampB = (1,1,-1)
AMP_A = (1, 1, 1)
AMP_B = (1, 1, -1)


def test_cross_term_expansion_identity():
    """Verify |sum c_k|^2 == sum |c_k|^2 + sum_{j < k} 2 Re(c_j c_k*) for N = 4."""
    amps = Amplitudes(
        [
            cmath.rect(0.5, 0.1),
            cmath.rect(0.5, 0.9),
            cmath.rect(0.5, 2.1),
            cmath.rect(0.5, 3.14),
        ]
    )
    expected = amps.l1_mass_sum + amps.cross_term_sum
    actual = amps.total_readout_probability
    assert math.isclose(actual, expected, abs_tol=1e-12)


def test_non_l1_distinguishability():
    """Two states with identical L1 diagonal weights yield different total readout."""
    state_constructive = Amplitudes(
        [cmath.rect(1 / math.sqrt(2), 0.0), cmath.rect(1 / math.sqrt(2), 0.0)]
    )
    state_destructive = Amplitudes(
        [cmath.rect(1 / math.sqrt(2), 0.0), cmath.rect(1 / math.sqrt(2), math.pi)]
    )

    assert math.isclose(
        state_constructive.l1_mass_sum, state_destructive.l1_mass_sum, abs_tol=1e-12
    )
    assert math.isclose(state_constructive.l1_mass_sum, 1.0, abs_tol=1e-12)

    # Constructive coherent |√2|^2 = 2; destructive = 0
    assert math.isclose(
        state_constructive.total_readout_probability, 2.0, abs_tol=1e-12
    )
    assert math.isclose(state_destructive.total_readout_probability, 0.0, abs_tol=1e-12)


def test_scale_invariance_n8():
    """Verify Rung 6 cross-term expansion identity for N = 8 discrete sectors."""
    coords = [cmath.rect(1.0 / math.sqrt(8), 0.2 * k) for k in range(8)]
    amps = Amplitudes(coords)
    assert math.isclose(amps.l1_mass_sum, 1.0, abs_tol=1e-12)
    assert math.isclose(
        amps.total_readout_probability,
        amps.l1_mass_sum + amps.cross_term_sum,
        abs_tol=1e-12,
    )


def test_fin3_expansion_identity_int():
    """Lean expansion_identity on ampA and ampB."""
    for amp in (AMP_A, AMP_B):
        assert coherent_sum_sq_int(amp) == sum_squares_int(
            amp
        ) + pairwise_cross_term_sum_int(amp)


def test_amp_a_l1_and_cross():
    """Lean ampA_l1 / ampA_cross / ampA_coherent: squares=3, cross=6, coherent=9."""
    assert AMP_A == (1, 1, 1)
    assert sum_squares_int(AMP_A) == 3
    assert pairwise_cross_term_sum_int(AMP_A) == 6
    assert coherent_sum_sq_int(AMP_A) == 9
    assert 3 + 6 == 9


def test_amp_b_l1_and_cross():
    """Lean ampB_l1 / ampB_cross / ampB_coherent: squares=3, cross=-2, coherent=1."""
    assert AMP_B == (1, 1, -1)
    assert sum_squares_int(AMP_B) == 3
    assert pairwise_cross_term_sum_int(AMP_B) == -2
    assert coherent_sum_sq_int(AMP_B) == 1
    assert 3 + (-2) == 1


def test_multi_sector_cross_term_non_l1():
    """Lean multi_sector_cross_term_non_l1: same L1 squares, different total readout."""
    assert sum_squares_int(AMP_A) == 3
    assert sum_squares_int(AMP_B) == 3
    assert sum_squares_int(AMP_A) == sum_squares_int(AMP_B)

    assert pairwise_cross_term_sum_int(AMP_A) == 6
    assert pairwise_cross_term_sum_int(AMP_B) == -2
    assert pairwise_cross_term_sum_int(AMP_A) != pairwise_cross_term_sum_int(AMP_B)

    assert coherent_sum_sq_int(AMP_A) == 9
    assert coherent_sum_sq_int(AMP_B) == 1
    assert coherent_sum_sq_int(AMP_A) != coherent_sum_sq_int(AMP_B)


def test_multi_sector_via_complex_amplitudes():
    """Same Fin-3 lifts through the complex Amplitudes carrier (mutation-sensitive)."""
    a = Amplitudes([1 + 0j, 1 + 0j, 1 + 0j])
    b = Amplitudes([1 + 0j, 1 + 0j, -1 + 0j])
    assert math.isclose(a.l1_mass_sum, 3.0, abs_tol=1e-12)
    assert math.isclose(b.l1_mass_sum, 3.0, abs_tol=1e-12)
    assert math.isclose(a.cross_term_sum, 6.0, abs_tol=1e-12)
    assert math.isclose(b.cross_term_sum, -2.0, abs_tol=1e-12)
    assert math.isclose(a.total_readout_probability, 9.0, abs_tol=1e-12)
    assert math.isclose(b.total_readout_probability, 1.0, abs_tol=1e-12)
    assert a.total_readout_probability != b.total_readout_probability


if __name__ == "__main__":
    pytest.main([__file__])
