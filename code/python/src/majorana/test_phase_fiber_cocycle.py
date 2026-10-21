"""
Executable Python dual for W4.3 (QMREG 52 / TOY-MECH):
Discrete 2-cocycle stand-in over transport monoid.

Honest residual: full H^2 classification and continuous U(1) coefficients
remain OPEN. This suite checks:

* additive σ(t1,t2)=t1*t2 on Int is a 2-cocycle and not identically 0
* Bool XOR monoid with σ=AND is a nontrivial Z/2 cocycle (not zero, not coboundary)

Matches Lean `003_qm_phase_fiber_cocycle.lean`.

AuthorityEffect: None. No Wave-4 exit claim.
"""

import pytest
import math
import cmath
from dataclasses import dataclass
from itertools import product
from typing import Callable


@dataclass(frozen=True)
class ProjectivePhaseCocycle:
    cocycle_fn: Callable[[int, int], complex]

    def evaluate_2_cocycle_identity(
        self, t1: int, t2: int, t3: int, mult_fn: Callable[[int, int], int]
    ) -> bool:
        """
        Verify 2-cocycle identity:
        sigma(t1, t2) * sigma(mult(t1, t2), t3) == sigma(t2, t3) * sigma(t1, mult(t2, t3))
        """
        lhs = self.cocycle_fn(t1, t2) * self.cocycle_fn(mult_fn(t1, t2), t3)
        rhs = self.cocycle_fn(t2, t3) * self.cocycle_fn(t1, mult_fn(t2, t3))
        return math.isclose(abs(lhs - rhs), 0.0, abs_tol=1e-12)


def mult_add(a: int, b: int) -> int:
    return a + b


def additive_sigma(t1: int, t2: int) -> int:
    """Lean additiveCocycle.phase_shift: σ(t1,t2) = t1 * t2."""
    return t1 * t2


def additive_is_cocycle(t1: int, t2: int, t3: int) -> bool:
    """Lean IsCocycle on Int: σ(t1,t2)+σ(t1+t2,t3) = σ(t2,t3)+σ(t1,t2+t3)."""
    lhs = additive_sigma(t1, t2) + additive_sigma(t1 + t2, t3)
    rhs = additive_sigma(t2, t3) + additive_sigma(t1, t2 + t3)
    return lhs == rhs


def phase_mul(a: bool, b: bool) -> bool:
    """Lean phaseMul: Bool XOR monoid."""
    return a != b


def and_cocycle(g: bool, h: bool) -> bool:
    """Lean andCocycle: σ = AND."""
    return g and h


def zero_cocycle(_g: bool, _h: bool) -> bool:
    return False


def bool_is_cocycle(
    sigma: Callable[[bool, bool], bool], g: bool, h: bool, k: bool
) -> bool:
    """Lean IsBoolCocycle identity."""
    lhs = phase_mul(sigma(g, h), sigma(phase_mul(g, h), k))
    rhs = phase_mul(sigma(h, k), sigma(g, phase_mul(h, k)))
    return lhs is rhs


def coboundary(f: Callable[[bool], bool], g: bool, h: bool) -> bool:
    """Lean coboundary: f(g) xor f(h) xor f(g xor h)."""
    return phase_mul(phase_mul(f(g), f(h)), f(phase_mul(g, h)))


def test_trivial_cocycle_identity():
    """Trivial cocycle sigma(t1, t2) = 1 + 0j obeys 2-cocycle identity."""
    cocycle = ProjectivePhaseCocycle(lambda t1, t2: complex(1.0, 0.0))
    assert cocycle.evaluate_2_cocycle_identity(1, 2, 3, mult_add) is True


def test_exponential_phase_cocycle_identity():
    """Phase factor sigma(t1, t2) = exp(i * alpha * t1 * t2) obeys 2-cocycle identity."""
    alpha = 0.45
    fn = lambda t1, t2: cmath.exp(1j * alpha * t1 * t2)
    cocycle = ProjectivePhaseCocycle(fn)
    assert cocycle.evaluate_2_cocycle_identity(2, 3, 4, mult_add) is True


def test_u1_gauge_phase_cocycle():
    """U(1) coboundary sigma(t1, t2) = f(t1) f(t2) / f(t1 + t2) is a valid 2-cocycle."""
    f = lambda t: cmath.exp(1j * 0.3 * t)
    fn = lambda t1, t2: (f(t1) * f(t2)) / f(t1 + t2)
    cocycle = ProjectivePhaseCocycle(fn)
    assert cocycle.evaluate_2_cocycle_identity(1, 5, 10, mult_add) is True


def test_additive_cocycle_holds():
    """Lean additive_cocycle_holds / additiveCocycle_is_cocycle on Int samples."""
    samples = [
        (0, 0, 0),
        (1, 1, 1),
        (2, 3, 4),
        (-1, 5, 2),
        (7, -3, -2),
        (1, 0, -1),
    ]
    for t1, t2, t3 in samples:
        assert additive_is_cocycle(t1, t2, t3) is True


def test_additive_cocycle_not_identically_zero():
    """Lean additive_cocycle_not_identically_zero: σ(1,1)=1 ≠ 0."""
    assert additive_sigma(1, 1) == 1
    assert additive_sigma(1, 1) != 0
    assert additive_sigma(2, 3) == 6
    assert additive_sigma(0, 5) == 0


def test_and_cocycle_is_cocycle():
    """Lean andCocycle_is_cocycle: exhaustive on Bool^3."""
    for g, h, k in product([False, True], repeat=3):
        assert bool_is_cocycle(and_cocycle, g, h, k) is True
    for g, h, k in product([False, True], repeat=3):
        assert bool_is_cocycle(zero_cocycle, g, h, k) is True


def test_and_cocycle_not_zero():
    """Lean andCocycle_not_zero / andCocycle_not_identically_zero."""
    assert and_cocycle(True, True) is True
    assert and_cocycle(True, True) is not zero_cocycle(True, True)
    assert and_cocycle(False, False) is False
    assert and_cocycle(True, False) is False


def test_and_cocycle_not_coboundary():
    """Lean andCocycle_not_coboundary: AND is not δf for any f : Bool → Bool."""
    for f_false, f_true in product([False, True], repeat=2):
        f = lambda b, ff=f_false, ft=f_true: ft if b else ff
        matches_all = all(
            and_cocycle(g, h) is coboundary(f, g, h)
            for g, h in product([False, True], repeat=2)
        )
        assert matches_all is False


def test_and_cocycle_nontrivial_package():
    """Lean andCocycle_nontrivial packaging: cocycle + not zero + not coboundary."""
    assert and_cocycle(True, True) is True
    assert bool_is_cocycle(and_cocycle, True, True, True) is True
    table = {
        (False, False): False,
        (False, True): False,
        (True, False): False,
        (True, True): True,
    }
    for (g, h), expected in table.items():
        assert and_cocycle(g, h) is expected


if __name__ == "__main__":
    pytest.main([__file__])
