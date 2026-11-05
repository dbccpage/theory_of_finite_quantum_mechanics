"""Independent symbolic and valuation controls for Gaussian-vector residuals."""
from __future__ import annotations

from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
from math import gcd
from pathlib import Path
import sys
from typing import TypeVar, cast
import unittest
from unittest.mock import patch

from hypothesis import assume, given, settings, strategies as st
import sympy as sp

CHECKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHECKS))
from checker_support.boundary import evaluate
from checker_support.gaussian_rational import GaussianRational as G
from checker_support.gaussian_vector3 import GaussianVector3 as V
from checker_support.inert_prime_residual import InertPrimeResidual as R
from checker_support.outcome import Outcome

T = TypeVar('T')
PROPERTY = settings(max_examples=60, derandomize=True, deadline=None, database=None)
FRACTION = st.builds(Q, st.integers(-8, 8), st.integers(1, 7))
COORDINATE = st.tuples(FRACTION, FRACTION)
VECTOR = st.tuples(COORDINATE, COORDINATE, COORDINATE)
PRIMES = (3, 7, 11, 19, 23, 31)


def symbolic(vector: V) -> sp.Matrix:
    return sp.Matrix([sp.Rational(x.re.numerator, x.re.denominator)
                      + sp.I*sp.Rational(x.im.numerator, x.im.denominator) for x in vector.entries])


def valuation(norm: Q, prime: int) -> int:
    if norm == 0:
        return 0
    return int(sp.factorint(norm.numerator).get(prime, 0)-sp.factorint(norm.denominator).get(prime, 0))


def character(norm: Q, prime: int) -> Q:
    if norm == 0:
        return Q(0)
    exponent = valuation(norm, prime)
    unit = norm / Q(prime)**exponent
    residue = (unit.numerator * pow(unit.denominator, -1, prime)) % prime
    return Q(1 if residue in {i*i % prime for i in range(1, prime)} else -1)


def reference_residual(vector: V, prime: int) -> Q:
    z = symbolic(vector)
    norms = tuple(Q(sp.expand(sp.conjugate(x)*x)) for x in z)
    total = sum(norms, Q(0)); level = valuation(total, prime)
    if level % 2 == 0:
        return Q(0)
    leading = next(norm for norm in norms if norm > 0 and valuation(norm, prime) < level)
    return character(leading, prime)*character(total, prime)


class InertPrimeGeometryTests(unittest.TestCase):
    def accepted(self, result: Outcome[T]) -> T:
        self.assertIsNone(result.error)
        return cast(T, result.value)

    def refused(self, result: Outcome[T], kind: str | None = None) -> None:
        self.assertIsNotNone(result.error)
        if kind is not None and result.error is not None:
            self.assertEqual(result.error.kind, kind)

    @PROPERTY
    @given(VECTOR, VECTOR, COORDINATE)
    def test_generated_vector_operations_match_symbolic_geometry(self, left: object, right: object, scalar: object) -> None:
        u, v = V(left), V(right); a = G(*cast(tuple[Q, Q], scalar)); su, sv = symbolic(u), symbolic(v)
        inner = sp.expand((su.conjugate().T*sv)[0]); result = self.accepted(u.inner(v))
        self.assertEqual((result.re, result.im), (Q(sp.re(inner)), Q(sp.im(inner))))
        self.assertEqual(u.squared_norm, Q(sp.expand((su.conjugate().T*su)[0])))
        self.assertEqual(symbolic(self.accepted(u.add(v))), su+sv)
        self.assertEqual(symbolic(self.accepted(u.sub(v))), su-sv)
        self.assertEqual(symbolic(self.accepted(u.scale(a))).applyfunc(sp.expand), ((a.re+sp.I*a.im)*su).applyfunc(sp.expand))
        w = self.accepted(u.cross(v))
        self.assertEqual(symbolic(w).applyfunc(sp.expand), su.cross(sv).conjugate().applyfunc(sp.expand))
        self.assertEqual(self.accepted(u.inner(w)), G(0)); self.assertEqual(self.accepted(v.inner(w)), G(0))

    @PROPERTY
    @given(VECTOR, st.sampled_from(PRIMES))
    def test_generated_residual_matches_factorization_and_residue_oracle(self, values: object, prime: int) -> None:
        vector = V(values); residual = R(prime)
        self.assertEqual(self.accepted(residual.residual(vector)), reference_residual(vector, prime))
        self.assertIn(self.accepted(residual.exotic(vector)), (Q(0), Q(1, 3), Q(2, 3)))

    @PROPERTY
    @given(VECTOR, VECTOR, COORDINATE)
    def test_generated_frames_and_nonzero_complex_scaling(self, first: object, raw: object, scalar: object) -> None:
        u = V(first); v = self.accepted(u.cross(V(raw))); factor = G(*cast(tuple[Q, Q], scalar))
        assume(u.squared_norm > 0 and v.squared_norm > 0 and factor.norm_sq() > 0)
        w = self.accepted(u.cross(v)); scaled = self.accepted(u.scale(factor))
        for prime in PRIMES:
            residual = R(prime)
            values = [self.accepted(residual.residual(x)) for x in (u, v, w)]
            self.assertEqual(sum(values), 0)
            self.assertEqual(sum(self.accepted(residual.exotic(x)) for x in (u, v, w)), 1)
            self.assertEqual(self.accepted(residual.residual(scaled)), values[0])
            self.assertEqual(sum(valuation(x.squared_norm, prime) for x in (u, v, w)) % 2, 0)

    @PROPERTY
    @given(st.sampled_from(PRIMES), st.integers(-12, 12), st.integers(1, 200), st.integers(1, 200))
    def test_generated_valuation_and_unit_character(self, prime: int, exponent: int, numerator: int, denominator: int) -> None:
        assume(gcd(prime, numerator*denominator) == 1)
        norm = Q(numerator, denominator)*Q(prime)**exponent; residual = R(prime)
        self.assertEqual(self.accepted(residual.valuation(norm)), exponent)
        self.assertEqual(self.accepted(residual.unit_character(norm)), character(Q(numerator, denominator), prime))
        n = numerator*prime**abs(exponent)
        self.assertEqual(self.accepted(residual.integer_parts(-n)), (abs(exponent), numerator))

    def test_exact_shape_scalar_domains_and_eager_admission(self) -> None:
        invalid: object
        for invalid in (None, (), [(1, 0)], [(1, 0)]*4, [1, 2, 3], [(True, 0), (0, 0), (0, 0)],
                        [(1.0, 0), (0, 0), (0, 0)], [(1, 0, 0), (0, 0), (0, 0)]):
            self.refused(evaluate(V, invalid), 'input')
        for invalid in ((True, 0, 0, 0, 0, 0), (Q(1), 0, 0, 0, 0, 0), (1.0, 0, 0, 0, 0, 0), (0,)*5):
            self.refused(V.from_integers(invalid), 'input')
        u = self.accepted(V.from_integers((1, 0, 2, 0, 3, 0)))
        for operand in (None, u.to_pairs(), G(1), 1):
            for operation in (u.add, u.sub, u.cross):
                self.refused(operation(operand), 'input')
            self.refused(u.inner(operand), 'input')
        for scalar in (None, 1, True, (1.0, 0), (1,), (1, 0, 0)):
            self.refused(u.scale(scalar), 'input')

    def test_ownership_zero_and_integer_primitivity(self) -> None:
        raw = [[Q(1), Q(0)], [Q(0), Q(0)], [Q(0), Q(0)]]; vector = V(raw)
        raw[0][0] = Q(7); self.assertEqual(vector.entries[0], G(1))
        self.assertEqual(vector.to_pairs(), ((Q(1), Q(0)), (Q(0), Q(0)), (Q(0), Q(0))))
        with self.assertRaises(FrozenInstanceError):
            vector.squared_norm = Q(0)  # type: ignore[misc]
        self.assertTrue(self.accepted(vector.integer_primitive()))
        even = V(((1, 1), (2, 0), (0, 0))); self.assertFalse(self.accepted(even.integer_primitive()))
        fractional = V(((Q(1, 2), 0), (0, 0), (0, 0)))
        self.refused(fractional.integer_primitive(), 'input')
        zero = V(((0, 0),)*3); self.assertFalse(self.accepted(zero.integer_primitive()))
        self.assertEqual(self.accepted(vector.sub(vector)), zero)
        self.assertEqual(self.accepted(R(3).residual(zero)), 0)
        self.assertEqual(self.accepted(R(3).exotic(zero)), Q(1, 3))

    def test_prime_admission_matches_independent_primality(self) -> None:
        for candidate in range(0, 128):
            result = evaluate(R, candidate)
            self.assertEqual(result.ok, candidate % 4 == 3 and bool(sp.isprime(candidate)))
        for invalid in (True, 3.0, Q(3), '3', None):
            self.refused(evaluate(R, invalid), 'input')
        self.refused(evaluate(R, 65539), 'resource')
        largest = max(p for p in range(65000, 65536) if p % 4 == 3 and bool(sp.isprime(p)))
        self.assertEqual(R(largest).prime, largest)
        with self.assertRaises(FrozenInstanceError):
            R(3).prime = 7  # type: ignore[misc]

    def test_norm_and_integer_resource_boundaries(self) -> None:
        moderate = 1 << 2047
        vector = V(((moderate, 0),)*3)
        self.assertEqual(vector.squared_norm, 3*moderate*moderate)
        self.refused(vector.scale((2, 0)), 'resource')
        self.refused(evaluate(V, ((1 << 2048, 0), (0, 0), (0, 0))), 'resource')
        self.refused(evaluate(V, ((G(1 << 4095)), G(0), G(0))), 'resource')
        self.refused(V.from_integers((1 << 4096, 0, 0, 0, 0, 0)), 'resource')
        residual = R(3); maximum = (1 << 4096)-1
        self.accepted(residual.integer_parts(maximum))
        self.refused(residual.integer_parts(1 << 4096), 'resource')
        self.assertEqual(self.accepted(residual.integer_parts(3**2000)), (2000, 1))
        self.assertEqual(self.accepted(residual.valuation(Q(1, 3**2000))), -2000)
        self.refused(residual.valuation(Q(1, 1 << 4096)), 'resource')

    def test_expected_scalar_refusals_and_zero_conventions(self) -> None:
        residual = R(7)
        invalid: object
        self.assertEqual(self.accepted(residual.integer_parts(0)), (0, 0))
        self.assertEqual(self.accepted(residual.valuation(0)), 0)
        self.assertEqual(self.accepted(residual.unit_character(0)), 0)
        for invalid in (True, 7.0, Q(7), None):
            self.refused(residual.integer_parts(invalid), 'input')
        for invalid in (True, 1.0, Q(-1), None):
            self.refused(residual.valuation(invalid), 'input')
            self.refused(residual.unit_character(invalid), 'input')
        for invalid in (None, ((1, 0),)*3, 1):
            self.refused(residual.residual(invalid), 'input')
            self.refused(residual.exotic(invalid), 'input')

    def test_original_witness_values_and_selective_duality(self) -> None:
        witnesses = [V(((1, 0), (1, 0), (1, 0))), V(((1, 0), (2, 0), (1, 1))),
                     V(((1, 0), (3, 0), (1, 0)))]
        for i, prime in enumerate((3, 7, 11)):
            self.assertEqual([self.accepted(R(prime).residual(v)) for v in witnesses], [Q(int(i == j)) for j in range(3)])
        self.assertEqual(self.accepted(R(3).residual(V(((1, 2), (1, 2), (1, 1))))), -1)
        self.assertEqual(self.accepted(R(3).residual(V(((1, 4), (1, 2), (1, 1))))), 1)
        for vector in witnesses:
            self.assertTrue(self.accepted(vector.integer_primitive()))

    def test_accumulated_norm_budget_and_integer_coordinate_order(self) -> None:
        # Each summand fits; their sum alone crosses the storage boundary.
        coordinate = (1 << 2048)-1
        single = V(((coordinate, 0), (0, 0), (0, 0)))
        self.assertEqual(single.squared_norm.numerator.bit_length(), 4096)
        self.refused(evaluate(V, ((coordinate, 0), (coordinate, 0), (0, 0))), 'resource')
        converted = self.accepted(V.from_integers((1, -2, 3, -4, 5, -6)))
        self.assertEqual(converted.to_pairs(), ((Q(1), Q(-2)), (Q(3), Q(-4)), (Q(5), Q(-6))))

    def test_leading_coordinate_character_can_be_negative(self) -> None:
        vector = V(((1, 2), (1, 2), (1, 1)))
        self.assertEqual(fixture_character := character(vector.component_norms[0], 3), -1)
        self.assertEqual(character(vector.squared_norm, 3), 1)
        self.assertEqual(reference_residual(vector, 3), fixture_character)
        self.assertEqual(self.accepted(R(3).residual(vector)), -1)

    def test_internal_algebra_guards_and_unexpected_failure_propagation(self) -> None:
        residual = R(3); zero = V(((0, 0),)*3)
        with patch.object(R, '_valuation', return_value=1):
            self.refused(residual.residual(zero), 'check')
        with patch.dict(R._unit_character.__globals__, pow=lambda *_: 0):
            self.refused(residual.unit_character(1), 'check')
        for exception in (RuntimeError, KeyboardInterrupt, SystemExit):
            with patch.object(G, 'norm_sq', side_effect=exception), self.assertRaises(exception):
                evaluate(V, ((1, 0),)*3)
            with patch.object(R, '_valuation', side_effect=exception), self.assertRaises(exception):
                residual.residual(zero)


if __name__ == '__main__':
    unittest.main()
