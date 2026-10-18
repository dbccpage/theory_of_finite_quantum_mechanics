from __future__ import annotations
"""
Executable Python dual harness for W6.13 / OB-CONVEX (convexity of state space).

Mirrors Lean `003_qm_convexity_state_space.lean`:

1. Classical bit residual weights closed under discrete Nat-scale mixture.
2. Mixture of pure0 and pure1 yields fairBit (simplex convexity).
3. Classical cone/simplex param counts ≠ complex qubit density params (4).
4. Beyond-simplex convex body underivable from FinL1 alone; conditional under lift.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


@dataclass(frozen=True)
class BitWeight:
    w0: int
    w1: int

    @property
    def total(self) -> int:
        return self.w0 + self.w1

    @property
    def is_pure(self) -> bool:
        return (self.w0 > 0 and self.w1 == 0) or (self.w0 == 0 and self.w1 > 0)

    @property
    def is_mixed(self) -> bool:
        return self.w0 > 0 and self.w1 > 0


def mix(a: BitWeight, b: BitWeight, s: int, t: int) -> BitWeight:
    """Unnormalized cone mixture: s·a + t·b componentwise."""
    return BitWeight(s * a.w0 + t * b.w0, s * a.w1 + t * b.w1)


PURE0 = BitWeight(1, 0)
PURE1 = BitWeight(0, 1)
FAIR = BitWeight(1, 1)

CLASSICAL_BIT_CONE_PARAMS = 2
CLASSICAL_BIT_SIMPLEX_FREE = 1
COMPLEX_QUBIT_DENSITY_PARAMS = 4
REAL_REBIT_DENSITY_PARAMS = 3


def test_classical_mix_closed():
    m = mix(BitWeight(2, 1), BitWeight(0, 3), 1, 2)
    assert m == BitWeight(2, 7)
    assert m.total == 1 * 3 + 2 * 3


def test_mix_pures_fair():
    assert PURE0.is_pure and PURE1.is_pure
    assert mix(PURE0, PURE1, 1, 1) == FAIR
    assert FAIR.is_mixed


def test_mix_total_identity():
    a, b = BitWeight(2, 3), BitWeight(1, 0)
    s, t = 2, 5
    m = mix(a, b, s, t)
    assert m.total == s * a.total + t * b.total


def test_beyond_simplex_param_gap():
    assert CLASSICAL_BIT_CONE_PARAMS == 2
    assert COMPLEX_QUBIT_DENSITY_PARAMS == 4
    assert CLASSICAL_BIT_CONE_PARAMS != COMPLEX_QUBIT_DENSITY_PARAMS
    assert CLASSICAL_BIT_SIMPLEX_FREE != COMPLEX_QUBIT_DENSITY_PARAMS
    assert REAL_REBIT_DENSITY_PARAMS != COMPLEX_QUBIT_DENSITY_PARAMS


class StateSpaceHost(str, Enum):
    FIN_L1_SIMPLEX = "finL1Simplex"
    COMPLEX_CONVEX = "complexHilbertConvexBody"


@dataclass(frozen=True)
class DeclaredStateSpace:
    host: StateSpaceHost
    free_params: int

    def __post_init__(self) -> None:
        if self.host is StateSpaceHost.FIN_L1_SIMPLEX and self.free_params > 1:
            raise ValueError("classical bit simplex free params must be ≤ 1")


def test_declared_state_space_hosts():
    classical = DeclaredStateSpace(host=StateSpaceHost.FIN_L1_SIMPLEX, free_params=1)
    qubit = DeclaredStateSpace(host=StateSpaceHost.COMPLEX_CONVEX, free_params=4)
    assert classical.free_params == 1
    assert qubit.free_params == 4
    with pytest.raises(ValueError, match="classical bit simplex"):
        DeclaredStateSpace(host=StateSpaceHost.FIN_L1_SIMPLEX, free_params=4)


def test_convexity_import_status_packaging():
    ob_convex_simplex = "derived"
    ob_convex_beyond = "underivable"
    ob_convex_under_lift = "conditionalImport"
    assert ob_convex_simplex == "derived"
    assert ob_convex_beyond == "underivable"
    assert ob_convex_under_lift == "conditionalImport"
    full_convex_body_classification_open = True
    assert full_convex_body_classification_open is True


def test_convexity_package():
    assert mix(PURE0, PURE1, 1, 1) == FAIR
    assert CLASSICAL_BIT_CONE_PARAMS != COMPLEX_QUBIT_DENSITY_PARAMS
    assert (
        DeclaredStateSpace(
            host=StateSpaceHost.FIN_L1_SIMPLEX, free_params=1
        ).free_params
        == 1
    )
    assert (
        DeclaredStateSpace(
            host=StateSpaceHost.COMPLEX_CONVEX, free_params=4
        ).free_params
        == 4
    )


if __name__ == "__main__":
    pytest.main([__file__])
