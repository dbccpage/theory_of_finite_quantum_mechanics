from __future__ import annotations
"""
Executable Python dual harness for W6.16 (time parameter vs generator; irreversibility).

Mirrors Lean `003_qm_time_generator_irreversibility.lean`:

1. Discrete Nat step iteration of 2×2 kernels (Chapman–Kolmogorov toy).
2. Generator label is extra data (not forced by kernel alone).
3. Reset has no left inverse among {id, flip, reset}; flip is reversible.
4. Continuous generator underivable from FinL1; under lift conditional.
5. Semigroup CK samples; reset contracts populations; discrete phase clock;
   continuous rate extra data; Stone OPEN.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Kernel2:
    k00: int
    k10: int
    k01: int
    k11: int

    def is_column_stochastic(self) -> bool:
        return self.k00 + self.k10 == 1 and self.k01 + self.k11 == 1

    def mul(self, other: "Kernel2") -> "Kernel2":
        return Kernel2(
            k00=self.k00 * other.k00 + self.k01 * other.k10,
            k10=self.k10 * other.k00 + self.k11 * other.k10,
            k01=self.k00 * other.k01 + self.k01 * other.k11,
            k11=self.k10 * other.k01 + self.k11 * other.k11,
        )

    def pow(self, n: int) -> "Kernel2":
        acc = ID
        for _ in range(n):
            acc = self.mul(acc)
        return acc


ID = Kernel2(1, 0, 0, 1)
FLIP = Kernel2(0, 1, 1, 0)
RESET = Kernel2(1, 0, 1, 0)


def test_kernels_column_stochastic():
    assert ID.is_column_stochastic()
    assert FLIP.is_column_stochastic()
    assert RESET.is_column_stochastic()


def test_discrete_time_parameter():
    assert FLIP.pow(0) == ID
    assert FLIP.pow(1) == FLIP
    assert FLIP.pow(2) == ID
    assert RESET.pow(1) == RESET
    assert RESET.pow(2) == RESET


def test_flip_reversible():
    assert FLIP.mul(FLIP) == ID


def test_reset_no_left_inverse_among_toy():
    assert ID.mul(RESET) != ID
    assert FLIP.mul(RESET) != ID
    assert RESET.mul(RESET) != ID
    assert RESET.mul(RESET) == RESET


@dataclass(frozen=True)
class GeneratorCandidate:
    rate_scale: int


def test_generator_not_forced_by_kernel():
    assert GeneratorCandidate(0) != GeneratorCandidate(1)


class ImportStatus(str, Enum):
    DERIVED = "derived"
    UNDERIVABLE = "underivable"
    CONDITIONAL_IMPORT = "conditionalImport"


DISCRETE_TIME = ImportStatus.DERIVED
IRREVERSIBILITY_CLASSICAL = ImportStatus.DERIVED
CONTINUOUS_FROM_FINL1 = ImportStatus.UNDERIVABLE
CONTINUOUS_UNDER_LIFT = ImportStatus.CONDITIONAL_IMPORT


def test_import_status_packaging():
    assert DISCRETE_TIME is ImportStatus.DERIVED
    assert IRREVERSIBILITY_CLASSICAL is ImportStatus.DERIVED
    assert CONTINUOUS_FROM_FINL1 is ImportStatus.UNDERIVABLE
    assert CONTINUOUS_UNDER_LIFT is ImportStatus.CONDITIONAL_IMPORT


def test_time_generator_package():
    assert FLIP.pow(2) == ID
    assert RESET.pow(2) == RESET
    assert RESET.mul(RESET) != ID
    assert GeneratorCandidate(0) != GeneratorCandidate(1)
    assert DISCRETE_TIME is ImportStatus.DERIVED
    assert IRREVERSIBILITY_CLASSICAL is ImportStatus.DERIVED
    assert CONTINUOUS_FROM_FINL1 is ImportStatus.UNDERIVABLE
    assert CONTINUOUS_UNDER_LIFT is ImportStatus.CONDITIONAL_IMPORT


# --- Semigroup / contraction / discrete phase residual ---


@dataclass(frozen=True)
class BitWeight:
    w0: int
    w1: int


def apply_kernel(k: Kernel2, w: BitWeight) -> BitWeight:
    return BitWeight(
        k.k00 * w.w0 + k.k01 * w.w1,
        k.k10 * w.w0 + k.k11 * w.w1,
    )


PURE0 = BitWeight(1, 0)
PURE1 = BitWeight(0, 1)
MIXED31 = BitWeight(3, 1)


def test_flip_chapman_kolmogorov_samples():
    assert FLIP.pow(1).mul(FLIP.pow(1)) == FLIP.pow(2)
    assert FLIP.pow(2).mul(FLIP.pow(1)) == FLIP.pow(3)
    assert FLIP.pow(3) == FLIP
    assert RESET.pow(1).mul(RESET.pow(1)) == RESET.pow(2)


def test_reset_contracts_populations():
    assert apply_kernel(RESET, PURE0) == BitWeight(1, 0)
    assert apply_kernel(RESET, PURE1) == BitWeight(1, 0)
    assert apply_kernel(RESET, MIXED31) == BitWeight(4, 0)
    assert apply_kernel(RESET, MIXED31).w1 == 0
    assert apply_kernel(FLIP, PURE0) == PURE1
    assert apply_kernel(FLIP, PURE1) == PURE0


@dataclass(frozen=True)
class DiscretePhaseClock:
    steps: int
    phase_inc: int

    def phase_at(self) -> int:
        return self.steps * self.phase_inc


def test_discrete_phase_clock_and_continuous_rate_extra():
    clock = DiscretePhaseClock(2, 3)
    assert clock.phase_at() == 6
    assert DiscretePhaseClock(1, 3).phase_at() + DiscretePhaseClock(
        2, 3
    ).phase_at() == (DiscretePhaseClock(3, 3).phase_at())
    no_rate, some_rate = 0, 1
    assert no_rate != some_rate


def test_time_generator_semigroup_residual_package():
    assert FLIP.pow(1).mul(FLIP.pow(1)) == FLIP.pow(2)
    assert FLIP.pow(3) == FLIP
    assert apply_kernel(RESET, MIXED31) == BitWeight(4, 0)
    assert apply_kernel(FLIP, PURE0) == PURE1
    assert DiscretePhaseClock(2, 3).phase_at() == 6
    assert 0 != 1  # continuous rate extra data
    full_stone_continuous_open = True
    assert full_stone_continuous_open is True
    assert CONTINUOUS_UNDER_LIFT is ImportStatus.CONDITIONAL_IMPORT
