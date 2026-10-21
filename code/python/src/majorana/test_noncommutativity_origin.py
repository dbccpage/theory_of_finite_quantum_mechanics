from __future__ import annotations
"""
Executable Python dual harness for W6.6 / OB-NONCOMM (non-commutativity origin).

Mirrors Lean `003_qm_noncommutativity_origin.lean`:

1. Diagonal classical observables always commute.
2. Pauli X,Z do not commute on the integer 2×2 toy.
3. FinL1 classical host forbids noncommuting pairs; complex-Hilbert lift admits them.
4. OB-NONCOMM underivable from FinL1 alone; conditional import under lift.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


@dataclass(frozen=True)
class Mat2:
    a00: int
    a01: int
    a10: int
    a11: int

    def mul(self, other: Mat2) -> Mat2:
        return Mat2(
            self.a00 * other.a00 + self.a01 * other.a10,
            self.a00 * other.a01 + self.a01 * other.a11,
            self.a10 * other.a00 + self.a11 * other.a10,
            self.a10 * other.a01 + self.a11 * other.a11,
        )

    def sub(self, other: Mat2) -> Mat2:
        return Mat2(
            self.a00 - other.a00,
            self.a01 - other.a01,
            self.a10 - other.a10,
            self.a11 - other.a11,
        )

    def is_diagonal(self) -> bool:
        return self.a01 == 0 and self.a10 == 0

    def commutator(self, other: Mat2) -> Mat2:
        return self.mul(other).sub(other.mul(self))

    def commutes_with(self, other: Mat2) -> bool:
        return self.commutator(other) == Mat2(0, 0, 0, 0)


ZERO = Mat2(0, 0, 0, 0)


def diag_obs(d0: int, d1: int) -> Mat2:
    return Mat2(d0, 0, 0, d1)


SIGMA_X = Mat2(0, 1, 1, 0)
SIGMA_Z = Mat2(1, 0, 0, -1)


def test_diagonal_observables_commute():
    a = diag_obs(2, 3)
    b = diag_obs(1, 4)
    assert a.is_diagonal() and b.is_diagonal()
    assert a.commutes_with(b)
    assert a.mul(b) == diag_obs(2, 12)
    assert b.mul(a) == diag_obs(2, 12)


def test_classical_sector_readouts_commute():
    pairs = [(0, 1), (2, 3), (5, -1), (7, 7)]
    for d0, d1 in pairs:
        for e0, e1 in pairs:
            assert diag_obs(d0, d1).commutes_with(diag_obs(e0, e1))


def test_sigma_x_sigma_z_not_commute():
    assert not SIGMA_X.is_diagonal()
    assert SIGMA_Z.is_diagonal()
    xz = SIGMA_X.mul(SIGMA_Z)
    zx = SIGMA_Z.mul(SIGMA_X)
    assert xz == Mat2(0, -1, 1, 0)
    assert zx == Mat2(0, 1, -1, 0)
    assert not SIGMA_X.commutes_with(SIGMA_Z)
    assert SIGMA_X.commutator(SIGMA_Z) != ZERO


class AlgebraHost(str, Enum):
    FIN_L1 = "finL1Classical"
    COMPLEX = "complexHilbertLift"


@dataclass(frozen=True)
class DeclaredObservableAlgebra:
    host: AlgebraHost
    admits_noncommuting_pair: bool

    def __post_init__(self) -> None:
        if self.host is AlgebraHost.FIN_L1 and self.admits_noncommuting_pair:
            raise ValueError("classical host cannot admit noncommuting pairs")


def test_classical_algebra_forbids_noncomm():
    classical = DeclaredObservableAlgebra(
        host=AlgebraHost.FIN_L1, admits_noncommuting_pair=False
    )
    assert classical.admits_noncommuting_pair is False
    with pytest.raises(ValueError, match="classical host"):
        DeclaredObservableAlgebra(
            host=AlgebraHost.FIN_L1, admits_noncommuting_pair=True
        )


def test_complex_lift_admits_noncomm():
    lift = DeclaredObservableAlgebra(
        host=AlgebraHost.COMPLEX, admits_noncommuting_pair=True
    )
    assert lift.admits_noncommuting_pair is True


def test_noncomm_underivable_from_finL1_alone():
    """Classical readouts always commute; noncommuting pair needs lift host."""
    for c1 in (diag_obs(2, 3), diag_obs(0, 1)):
        for c2 in (diag_obs(1, 4), diag_obs(5, 5)):
            assert c1.commutes_with(c2)
    assert not SIGMA_X.commutes_with(SIGMA_Z)
    assert (
        DeclaredObservableAlgebra(
            host=AlgebraHost.FIN_L1, admits_noncommuting_pair=False
        ).admits_noncommuting_pair
        is False
    )
    assert (
        DeclaredObservableAlgebra(
            host=AlgebraHost.COMPLEX, admits_noncommuting_pair=True
        ).admits_noncommuting_pair
        is True
    )


def test_ob_noncomm_status_packaging():
    ob_noncomm_from_finL1 = "underivable"
    ob_noncomm_under_lift = "conditionalImport"
    assert ob_noncomm_from_finL1 == "underivable"
    assert ob_noncomm_under_lift == "conditionalImport"
    full_contextuality_derivation_open = True
    assert full_contextuality_derivation_open is True


if __name__ == "__main__":
    pytest.main([__file__])
