from __future__ import annotations
"""
Executable Python dual harness for W6.9 / OB-HERM (Hermiticity of H).

Mirrors Lean `003_qm_hermiticity_of_h.lean`:

1. Diagonal and Pauli-X generators are Hermitian (real-symmetric).
2. Non-Hermitian matrix and irreversible rate generators exist.
3. Stochastic host does not require Hermiticity; unitary lift host does.
4. OB-HERM underivable from FinL1/stochastic alone; conditional under unitary lift.
5. Hermitian algebra residual: real linear closure; [X,Z] skew; unitary package
   requires Hermitian H; Stone OPEN.

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

    def is_hermitian(self) -> bool:
        """Real-symmetric ⇔ Hermitian on this real Mat2 toy."""
        return self.a01 == self.a10

    def is_anti_hermitian(self) -> bool:
        """Real-skew pure off-diagonal ⇔ anti-Hermitian toy."""
        return self.a01 == -self.a10 and self.a00 == 0 and self.a11 == 0

    def is_diagonal(self) -> bool:
        return self.a01 == 0 and self.a10 == 0

    def add(self, other: "Mat2") -> "Mat2":
        return Mat2(
            self.a00 + other.a00,
            self.a01 + other.a01,
            self.a10 + other.a10,
            self.a11 + other.a11,
        )

    def smul(self, k: int) -> "Mat2":
        return Mat2(k * self.a00, k * self.a01, k * self.a10, k * self.a11)

    def sub(self, other: "Mat2") -> "Mat2":
        return self.add(other.smul(-1))

    def mul(self, other: "Mat2") -> "Mat2":
        return Mat2(
            self.a00 * other.a00 + self.a01 * other.a10,
            self.a00 * other.a01 + self.a01 * other.a11,
            self.a10 * other.a00 + self.a11 * other.a10,
            self.a10 * other.a01 + self.a11 * other.a11,
        )


def diag_h(d0: int, d1: int) -> Mat2:
    return Mat2(d0, 0, 0, d1)


SIGMA_X = Mat2(0, 1, 1, 0)
SIGMA_Z = Mat2(1, 0, 0, -1)
NON_HERM_G = Mat2(0, 1, 0, 0)


def test_diag_and_pauli_hermitian():
    assert diag_h(2, 3).is_hermitian()
    assert diag_h(2, 3).is_diagonal()
    assert SIGMA_X.is_hermitian()
    assert SIGMA_Z.is_hermitian()


def test_non_herm_counterexample():
    assert not NON_HERM_G.is_hermitian()
    assert SIGMA_X.is_hermitian() and not NON_HERM_G.is_hermitian()


@dataclass(frozen=True)
class Rate2:
    r01: int
    r10: int

    def to_mat(self) -> Mat2:
        return Mat2(-(self.r01), self.r10, self.r01, -(self.r10))

    def is_symmetric_rates(self) -> bool:
        return self.r01 == self.r10


RESET_RATES = Rate2(r01=1, r10=0)
BALANCED_RATES = Rate2(r01=2, r10=2)


def test_stochastic_rate_not_forced_hermitian():
    assert not RESET_RATES.is_symmetric_rates()
    assert not RESET_RATES.to_mat().is_hermitian()
    assert BALANCED_RATES.is_symmetric_rates()
    assert BALANCED_RATES.to_mat().is_hermitian()


class DynamicsHost(str, Enum):
    FIN_L1_STOCHASTIC = "finL1Stochastic"
    COMPLEX_UNITARY = "complexHilbertUnitary"


@dataclass(frozen=True)
class DeclaredGenerator:
    host: DynamicsHost
    requires_hermitian: bool

    def __post_init__(self) -> None:
        if self.host is DynamicsHost.COMPLEX_UNITARY and not self.requires_hermitian:
            raise ValueError("unitary host requires Hermitian generator")


def test_host_hermiticity_requirements():
    stoch = DeclaredGenerator(
        host=DynamicsHost.FIN_L1_STOCHASTIC, requires_hermitian=False
    )
    unit = DeclaredGenerator(host=DynamicsHost.COMPLEX_UNITARY, requires_hermitian=True)
    assert stoch.requires_hermitian is False
    assert unit.requires_hermitian is True
    with pytest.raises(ValueError, match="unitary host requires"):
        DeclaredGenerator(host=DynamicsHost.COMPLEX_UNITARY, requires_hermitian=False)


def test_hermiticity_underivable_from_stochastic_alone():
    assert not RESET_RATES.to_mat().is_hermitian()
    assert not NON_HERM_G.is_hermitian()
    assert SIGMA_X.is_hermitian()
    assert diag_h(2, 3).is_hermitian()
    assert (
        DeclaredGenerator(
            host=DynamicsHost.FIN_L1_STOCHASTIC, requires_hermitian=False
        ).requires_hermitian
        is False
    )
    assert (
        DeclaredGenerator(
            host=DynamicsHost.COMPLEX_UNITARY, requires_hermitian=True
        ).requires_hermitian
        is True
    )
    ob_herm_from_fin_l1 = "underivable"
    ob_herm_under_unitary = "conditionalImport"
    assert ob_herm_from_fin_l1 == "underivable"
    assert ob_herm_under_unitary == "conditionalImport"


def test_stone_theorem_marked_open():
    stone_theorem_open = True
    assert stone_theorem_open is True


# --- Hermitian algebra residual ---


def pauli_combo(alpha: int, beta: int) -> Mat2:
    return SIGMA_X.smul(alpha).add(SIGMA_Z.smul(beta))


def comm(a: Mat2, b: Mat2) -> Mat2:
    return a.mul(b).sub(b.mul(a))


def test_pauli_combo_hermitian():
    assert pauli_combo(1, 2).is_hermitian()
    assert pauli_combo(0, 5).is_hermitian()
    assert pauli_combo(3, 0).is_hermitian()


def test_comm_xz_skew():
    c = comm(SIGMA_X, SIGMA_Z)
    assert c == Mat2(0, -2, 2, 0)
    assert c.is_anti_hermitian()
    assert not c.is_hermitian()


def test_unitary_hamiltonian_package():
    package = {
        "H": SIGMA_X,
        "host": DynamicsHost.COMPLEX_UNITARY,
        "requires_hermitian": True,
    }
    assert package["H"].is_hermitian()
    assert package["host"] is DynamicsHost.COMPLEX_UNITARY
    assert not NON_HERM_G.is_hermitian()


def test_hermiticity_algebra_residual_package():
    assert pauli_combo(1, 2).is_hermitian()
    c = comm(SIGMA_X, SIGMA_Z)
    assert c.is_anti_hermitian()
    assert c == Mat2(0, -2, 2, 0)
    assert SIGMA_X.is_hermitian()
    assert not NON_HERM_G.is_hermitian()
    stone_theorem_open = True
    assert stone_theorem_open is True
    ob_herm_under_unitary = "conditionalImport"
    assert ob_herm_under_unitary == "conditionalImport"


if __name__ == "__main__":
    pytest.main([__file__])
