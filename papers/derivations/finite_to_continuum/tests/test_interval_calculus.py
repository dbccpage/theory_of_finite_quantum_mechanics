"""Unit tests for Step 1: Certified Rational Interval Arithmetic."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

CODE_DIR = str(Path(__file__).resolve().parents[1] / "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from interval_calculus import (
    RationalInterval,
    certified_pi_enclosure,
    exp_interval,
    ln_interval_around_one,
    rational_heron_sqrt_bounds,
    sqrt_interval,
)


class TestRationalIntervalCalculus(unittest.TestCase):
    def test_float_and_bool_strict_refusal(self) -> None:
        """Floats and booleans in scalar position must raise TypeError."""
        with self.assertRaises(TypeError):
            RationalInterval(0.5, 1.0)
        with self.assertRaises(TypeError):
            RationalInterval(Fraction(1, 2), 1.0)
        with self.assertRaises(TypeError):
            RationalInterval(True, Fraction(1))
        with self.assertRaises(TypeError):
            RationalInterval(Fraction(0), False)

    def test_invariant_lo_le_hi(self) -> None:
        """lo > hi must raise ValueError."""
        with self.assertRaises(ValueError):
            RationalInterval(Fraction(2), Fraction(1))

    def test_interval_arithmetic(self) -> None:
        a = RationalInterval(Fraction(1, 2), Fraction(3, 2))
        b = RationalInterval(Fraction(2), Fraction(3))

        c = a + b
        self.assertEqual(c.lo, Fraction(5, 2))
        self.assertEqual(c.hi, Fraction(9, 2))

        d = a - b
        self.assertEqual(d.lo, Fraction(-5, 2))
        self.assertEqual(d.hi, Fraction(-1, 2))

        m = a * b
        self.assertEqual(m.lo, Fraction(1))
        self.assertEqual(m.hi, Fraction(9, 2))

        div = a / b
        self.assertEqual(div.lo, Fraction(1, 6))
        self.assertEqual(div.hi, Fraction(3, 4))

    def test_division_by_zero_interval(self) -> None:
        a = RationalInterval(Fraction(1), Fraction(2))
        zero_straddle = RationalInterval(Fraction(-1), Fraction(1))
        with self.assertRaises(ZeroDivisionError):
            _ = a / zero_straddle

    def test_abs_and_powers(self) -> None:
        straddle = RationalInterval(Fraction(-2), Fraction(3))
        abs_s = abs(straddle)
        self.assertEqual(abs_s.lo, Fraction(0))
        self.assertEqual(abs_s.hi, Fraction(3))

        sq = straddle ** 2
        self.assertEqual(sq.lo, Fraction(0))
        self.assertEqual(sq.hi, Fraction(9))

        cube = straddle ** 3
        self.assertEqual(cube.lo, Fraction(-8))
        self.assertEqual(cube.hi, Fraction(27))

    def test_heron_sqrt_bounds(self) -> None:
        lo, hi = rational_heron_sqrt_bounds(Fraction(4), steps=5)
        self.assertTrue(lo <= Fraction(2) <= hi)
        self.assertTrue(hi - lo < Fraction(1, 1000))

        lo2, hi2 = rational_heron_sqrt_bounds(Fraction(2), steps=8)
        self.assertTrue(lo2 * lo2 <= Fraction(2) <= hi2 * hi2)
        self.assertTrue(hi2 - lo2 < Fraction(1, 10**8))

    def test_sqrt_interval(self) -> None:
        i = RationalInterval(Fraction(1), Fraction(4))
        sq = sqrt_interval(i, steps=10)
        self.assertTrue(sq.lo <= Fraction(1))
        self.assertTrue(sq.hi >= Fraction(2))

    def test_exp_interval(self) -> None:
        e0 = exp_interval(RationalInterval(Fraction(0), Fraction(0)), order=5)
        self.assertEqual(e0.lo, Fraction(1))
        self.assertEqual(e0.hi, Fraction(1))

        e1 = exp_interval(RationalInterval(Fraction(1), Fraction(1)), order=15)
        self.assertTrue(Fraction(271828, 100000) <= e1.lo <= e1.hi <= Fraction(271829, 100000))
        self.assertTrue(e1.width < Fraction(1, 10**6))

    def test_certified_pi_enclosure(self) -> None:
        pi = certified_pi_enclosure(terms=8)
        self.assertTrue(Fraction(314159, 100000) <= pi.lo <= pi.hi <= Fraction(314160, 100000))
        self.assertTrue(pi.width < Fraction(1, 10**18))


if __name__ == "__main__":
    unittest.main()
