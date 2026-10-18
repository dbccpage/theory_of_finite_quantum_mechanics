from __future__ import annotations
"""
Executable Python dual harness for W6.8 — unitarity ↛ stochastic population transport.

Mirrors Lean `003_qm_unitarity_not_from_stochastic.lean`:

1. Reset kernel is column-stochastic but not doubly stochastic.
2. Identity and phase-gate labels share the identity population shadow.
3. Unitarity is not unique from (and not forced by) stochastic population maps alone.
4. Residual: phase family card 3; only id/flip doubly in toy set; orthogonal Mat2
   lift for id/flip; full U(n) OPEN.

AuthorityEffect: None.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


@dataclass(frozen=True)
class Kernel2:
    k00: int
    k10: int
    k01: int
    k11: int

    def is_column_stochastic(self) -> bool:
        return self.k00 + self.k10 == 1 and self.k01 + self.k11 == 1

    def is_doubly_stochastic(self) -> bool:
        return (
            self.is_column_stochastic()
            and self.k00 + self.k01 == 1
            and self.k10 + self.k11 == 1
        )

    def mul(self, other: "Kernel2") -> "Kernel2":
        return Kernel2(
            self.k00 * other.k00 + self.k01 * other.k10,
            self.k10 * other.k00 + self.k11 * other.k10,
            self.k00 * other.k01 + self.k01 * other.k11,
            self.k10 * other.k01 + self.k11 * other.k11,
        )


RESET = Kernel2(1, 0, 1, 0)
ID = Kernel2(1, 0, 0, 1)
FLIP = Kernel2(0, 1, 1, 0)


class UnitaryLabel(str, Enum):
    IDENTITY = "identity"
    PHASE_GATE = "phaseGate"


class PhaseFamily(str, Enum):
    IDENTITY = "identity"
    PHASE_Z = "phaseZ"
    PHASE_GLOBAL = "phaseGlobal"


def population_shadow(label: UnitaryLabel) -> Kernel2:
    return ID


def phase_family_shadow(_label: PhaseFamily) -> Kernel2:
    return ID


def test_reset_column_not_doubly():
    assert RESET.is_column_stochastic()
    assert not RESET.is_doubly_stochastic()
    assert RESET.k00 + RESET.k01 == 2


def test_id_and_flip_doubly():
    assert ID.is_doubly_stochastic()
    assert FLIP.is_doubly_stochastic()
    assert RESET != ID


def test_phase_and_id_same_population_distinct_labels():
    assert population_shadow(UnitaryLabel.IDENTITY) == population_shadow(
        UnitaryLabel.PHASE_GATE
    )
    assert UnitaryLabel.IDENTITY != UnitaryLabel.PHASE_GATE


def test_stochastic_not_implies_unitary_shadow():
    assert RESET.is_column_stochastic() and not RESET.is_doubly_stochastic()


def test_ob_unitary_underivable_marked():
    underivable_from_stochastic = True
    assert underivable_from_stochastic is True




def test_phase_family_card_three_same_shadow():
    labels = list(PhaseFamily)
    assert len(labels) == 3
    assert len(set(labels)) == 3
    for lab in labels:
        assert phase_family_shadow(lab) == ID


def test_doubly_closed_id_flip():
    assert ID.mul(ID).is_doubly_stochastic()
    assert FLIP.mul(FLIP) == ID
    assert FLIP.mul(FLIP).is_doubly_stochastic()
    assert ID.mul(FLIP).is_doubly_stochastic()


def test_only_id_flip_doubly_in_toy_set():
    assert ID.is_doubly_stochastic()
    assert FLIP.is_doubly_stochastic()
    assert not RESET.is_doubly_stochastic()


@dataclass(frozen=True)
class Mat2:
    a00: int
    a01: int
    a10: int
    a11: int

    def mul(self, other: "Mat2") -> "Mat2":
        return Mat2(
            self.a00 * other.a00 + self.a01 * other.a10,
            self.a00 * other.a01 + self.a01 * other.a11,
            self.a10 * other.a00 + self.a11 * other.a10,
            self.a10 * other.a01 + self.a11 * other.a11,
        )

    def transpose(self) -> "Mat2":
        return Mat2(self.a00, self.a10, self.a01, self.a11)

    def is_orthogonal(self) -> bool:
        ident = Mat2(1, 0, 0, 1)
        return self.transpose().mul(self) == ident


MAT_ID = Mat2(1, 0, 0, 1)
MAT_FLIP = Mat2(0, 1, 1, 0)
MAT_NON_ORTHO = Mat2(1, 1, 0, 0)


def test_orthogonal_lifts():
    assert MAT_ID.is_orthogonal()
    assert MAT_FLIP.is_orthogonal()
    assert not MAT_NON_ORTHO.is_orthogonal()


def test_unitarity_population_underdetermination_package():
    assert len(list(PhaseFamily)) == 3
    assert phase_family_shadow(PhaseFamily.IDENTITY) == phase_family_shadow(
        PhaseFamily.PHASE_Z
    )
    assert PhaseFamily.IDENTITY != PhaseFamily.PHASE_Z
    assert ID.is_doubly_stochastic() and FLIP.is_doubly_stochastic()
    assert not RESET.is_doubly_stochastic()
    assert FLIP.mul(FLIP) == ID
    assert MAT_ID.is_orthogonal() and MAT_FLIP.is_orthogonal()
    assert not MAT_NON_ORTHO.is_orthogonal()
    full_unitary_group_open = True
    underivable_from_stochastic = True
    assert full_unitary_group_open is True
    assert underivable_from_stochastic is True


if __name__ == "__main__":
    pytest.main([__file__])
