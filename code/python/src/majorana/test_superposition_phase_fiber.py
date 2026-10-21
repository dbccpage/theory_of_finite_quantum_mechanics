"""
Executable Python Property Test Suite for W4.1 / Rung 5 (PL-QM043-1):
Superposition as the Quotient Fiber & Non-L1 Interference Cross-Term Resource.

Tests:
1. Phase-blind L1 quotient invariance: Superposition states sharing diagonal L1 weights
   w1, w2 have identical classical L1 mass laws under d_0 phase-blind primitive difference.
2. Non-L1 interference cross-term: Adding phase delta_int introduces a non-zero residual
   mass R_int = delta_int that is quotient-invisible on diagonal readout but active under mixing.
3. LGGR Non-Factorization Invariant: Local Green (w1 >= 0, w2 >= 0) with non-zero phase
   interference (delta_int != 0) fails global L1 factorization (LGGR defect != 0).
"""

import pytest
from dataclasses import dataclass


@dataclass(frozen=True)
class SuperpositionState:
    w1: int
    w2: int
    delta_int: int

    @property
    def is_local_green(self) -> bool:
        """Local Green condition: diagonal components are non-negative L1 masses."""
        return self.w1 >= 0 and self.w2 >= 0

    @property
    def classical_l1_mass(self) -> int:
        """Diagonal L1 weight sum without phase interference."""
        return self.w1 + self.w2

    @property
    def superposed_mass(self) -> int:
        """Superposed mass carrying non-L1 phase interference cross-term."""
        return self.w1 + self.w2 + self.delta_int

    @property
    def interference_residual(self) -> int:
        """Interference residual R_int = superposed_mass - classical_l1_mass."""
        return self.superposed_mass - self.classical_l1_mass


def test_phase_blind_l1_quotient_invariance():
    """Superposition states with identical w1, w2 but different phase delta_int share the same classical L1 mass."""
    s1 = SuperpositionState(w1=3, w2=4, delta_int=2)
    s2 = SuperpositionState(w1=3, w2=4, delta_int=-1)
    assert s1.classical_l1_mass == 7
    assert s2.classical_l1_mass == 7
    assert s1.classical_l1_mass == s2.classical_l1_mass


def test_non_l1_interference_cross_term():
    """Interference residual equals delta_int and measures non-L1 cross-term surplus."""
    s = SuperpositionState(w1=5, w2=2, delta_int=4)
    assert s.interference_residual == 4
    assert s.superposed_mass == 11
    assert s.superposed_mass != s.classical_l1_mass


def test_lggr_non_factorization_invariant():
    """Local Green (w1, w2 >= 0) with delta_int != 0 exhibits non-zero interference residual (Local Green != Global Red)."""
    s = SuperpositionState(w1=4, w2=4, delta_int=-3)
    assert s.is_local_green is True
    assert s.interference_residual != 0
    assert s.interference_residual == -3


if __name__ == "__main__":
    pytest.main([__file__])
