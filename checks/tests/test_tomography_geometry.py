"""Independent rotation, equatorial and symbolic-tomography controls."""
from __future__ import annotations

from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
from pathlib import Path
import sys
from typing import TypeVar, cast
import unittest
from unittest.mock import patch

from hypothesis import assume, given, settings, strategies as st
import sympy as sp

CHECKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHECKS)); sys.path.insert(0, str(Path(__file__).parent))
import test_inert_prime_geometry as fixture
from checker_support.boundary import evaluate
from checker_support.equatorial_ray_geometry import EquatorialRayGeometry as E, NORTH
from checker_support.gaussian_rational import GaussianRational as G
from checker_support.gaussian_vector3 import GaussianVector3 as V
from checker_support.hermitian_tomography import HermitianTomography as H
from checker_support.orthogonal_gaussian_pair import OrthogonalGaussianPair as P
from checker_support.outcome import Outcome

T = TypeVar('T')
PROPERTY = settings(max_examples=40, derandomize=True, deadline=None, database=None)


def projector(vector: V) -> sp.Matrix:
    values = fixture.symbolic(vector)
    return values*values.conjugate().T/(values.conjugate().T*values)[0]


def kernel_fixtures() -> tuple[tuple[V, tuple[Q, ...]], ...]:
    return (
        (V(((1, 0), (1, 0), (1, 0))), tuple(Q(x, 3) for x in (1, 1, 1, -2, 0, -2, 0, -2, 0))),
        (V(((1, 0), (2, 0), (1, 1))), tuple(Q(x, 7) for x in (3, 2, 4, -4, 0, -2, -2, -4, -4))),
        (V(((1, 0), (3, 0), (1, 0))), tuple(Q(x, 11) for x in (3, -3, 3, -6, 0, -2, 0, -6, 0))))


class TomographyGeometryTests(unittest.TestCase):
    def accepted(self, result: Outcome[T]) -> T:
        self.assertIsNone(result.error)
        return cast(T, result.value)

    def refused(self, result: Outcome[T], kind: str | None = None) -> None:
        self.assertIsNotNone(result.error)
        if kind is not None and result.error is not None:
            self.assertEqual(result.error.kind, kind)

    @PROPERTY
    @given(fixture.VECTOR, fixture.VECTOR, fixture.COORDINATE, fixture.COORDINATE)
    def test_generated_orthogonal_pair_rotation_and_completion(self, first: object, raw: object,
                                                              alpha: object, beta: object) -> None:
        u = V(first); v = self.accepted(u.cross(V(raw)))
        a = G(*cast(tuple[Q, Q], alpha)); b = G(*cast(tuple[Q, Q], beta))
        assume(u.squared_norm > 0 and v.squared_norm > 0 and (a != G(0) or b != G(0)))
        pair = P(u, v); result = self.accepted(pair.rotate(a, b))
        u_sp, v_sp = fixture.symbolic(u), fixture.symbolic(v)
        a_sp, b_sp = a.re+sp.I*a.im, b.re+sp.I*b.im
        self.assertEqual(fixture.symbolic(result.first).applyfunc(sp.expand), (a_sp*u_sp+b_sp*v_sp).applyfunc(sp.expand))
        second = -v.squared_norm*sp.conjugate(b_sp)*u_sp+u.squared_norm*sp.conjugate(a_sp)*v_sp
        self.assertEqual(fixture.symbolic(result.second).applyfunc(sp.expand), second.applyfunc(sp.expand))
        self.assertEqual(self.accepted(result.first.inner(result.second)), G(0))
        self.assertEqual(result.first.squared_norm, a.norm_sq()*u.squared_norm+b.norm_sq()*v.squared_norm)
        self.assertEqual(result.second.squared_norm, u.squared_norm*v.squared_norm*result.first.squared_norm)
        completed = self.accepted(pair.completion())
        self.assertEqual(fixture.symbolic(completed).applyfunc(sp.expand), u_sp.cross(v_sp).conjugate().applyfunc(sp.expand))
        self.assertGreater(completed.squared_norm, 0)

    @PROPERTY
    @given(fixture.COORDINATE, fixture.COORDINATE, fixture.FRACTION, fixture.FRACTION)
    def test_generated_equatorial_tangent_and_two_step_identity(self, y: object, z: object, t: Q, s: Q) -> None:
        vector = V(((0, 0), y, z)); assume(vector.squared_norm > 0); geometry = E(vector)
        quarter = geometry.quarter_turn
        self.assertEqual(E(quarter).quarter_turn, self.accepted(vector.scale((-1, 0))))
        stepped = self.accepted(geometry.tangent(t))
        self.assertEqual(stepped.squared_norm, (1+t*t)*vector.squared_norm)
        composition = self.accepted(E(stepped).tangent(s))
        expected = (1-s*t)*fixture.symbolic(vector)+(s+t)*fixture.symbolic(quarter)
        self.assertEqual(fixture.symbolic(composition).applyfunc(sp.expand), expected.applyfunc(sp.expand))
        cancelled = self.accepted(E(stepped).tangent(-t))
        self.assertEqual(cancelled, self.accepted(vector.scale((1+t*t, 0))))

    @PROPERTY
    @given(fixture.COORDINATE, fixture.COORDINATE, fixture.COORDINATE)
    def test_generated_piron_meridian_and_kelvin(self, y: object, z: object, scalar: object) -> None:
        vector = V(((0, 0), y, z)); factor = G(*cast(tuple[Q, Q], scalar))
        assume(vector.squared_norm > 0 and factor != G(0)); geometry = E(vector)
        pair = self.accepted(geometry.piron(factor)); meridian = self.accepted(geometry.meridian())
        self.assertEqual(self.accepted(pair.first.inner(pair.second)), G(0))
        self.assertEqual(self.accepted(geometry.base.inner(meridian)), G(0))
        self.assertEqual(self.accepted(geometry.quarter_turn.inner(meridian)), G(0))
        step_weight = self.accepted(E.born_weight(pair.first))
        base_weight = self.accepted(E.born_weight(geometry.base))
        self.assertLessEqual(step_weight, base_weight)
        kelvin = self.accepted(geometry.kelvin()); self.assertEqual(kelvin.squared_norm, 1/vector.squared_norm)
        self.assertEqual(self.accepted(meridian.scale((-1/vector.squared_norm, 0))), E(kelvin).base)
        self.assertEqual(self.accepted(E.born_weight(geometry.base))+self.accepted(E.born_weight(E(kelvin).base)), 1)
        self.assertEqual(self.accepted(E.born_weight(pair.first))+self.accepted(E.born_weight(pair.second)),
                         self.accepted(E.born_weight(geometry.base)))

    @PROPERTY
    @given(fixture.COORDINATE, fixture.COORDINATE, st.integers(2, 15))
    def test_generated_pythagorean_sandwich_and_distances(self, y: object, z: object, k: int) -> None:
        vector = V(((0, 0), y, z)); assume(vector.squared_norm > 0); geometry = E(vector)
        rotated = self.accepted(geometry.pythagorean(k))
        inside, outside, tangent = Q(k*k-1, k*k+1), Q(k*k+1, k*k-1), Q(2*k, k*k-1)
        radial_in = self.accepted(vector.scale((inside, 0))); radial_out = self.accepted(vector.scale((outside, 0)))
        self.assertEqual(self.accepted(E(radial_in).tangent(tangent)), rotated)
        self.assertEqual(self.accepted(E(rotated).tangent(-tangent)), radial_out)
        self.assertEqual(rotated.squared_norm, vector.squared_norm)
        outer_weight = self.accepted(E.born_weight(E(radial_out).base))
        rotated_weight = self.accepted(E.born_weight(E(rotated).base))
        inner_weight = self.accepted(E.born_weight(E(radial_in).base))
        self.assertLessEqual(outer_weight, rotated_weight)
        self.assertLessEqual(rotated_weight, inner_weight)
        delta = self.accepted(E(radial_in).base.sub(geometry.base))
        self.assertEqual(delta.squared_norm, (inside-1)**2*vector.squared_norm)

    def test_pair_and_equator_admission_zero_and_ownership(self) -> None:
        zero = V(((0, 0),)*3); e2 = V(((0, 0), (1, 0), (0, 0)))
        for first, second in ((None, e2), (NORTH, None), (zero, e2), (NORTH, zero), (NORTH, NORTH)):
            self.refused(evaluate(P, first, second), 'input')
        pair = P(NORTH, e2)
        for alpha, beta in (((0, 0), (0, 0)), ((True, 0), (1, 0)), (None, (1, 0)), ((1, 0), 1)):
            self.refused(pair.rotate(alpha, beta), 'input')
        for invalid in (None, zero, NORTH, e2.to_pairs()):
            self.refused(evaluate(E, invalid), 'input')
        geometry = E(e2)
        with self.assertRaises(FrozenInstanceError):
            geometry.base = zero  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            pair.first = zero  # type: ignore[misc]
        self.refused(geometry.piron((0, 0)), 'input')
        self.refused(E.born_weight(zero), 'input'); self.refused(E.born_weight(None), 'input')
        self.assertEqual(self.accepted(E.born_weight(e2)), 0)
        self.assertEqual(self.accepted(E.born_weight(NORTH)), 1)

    def test_parameter_and_arithmetic_budgets_and_special_rotations(self) -> None:
        geometry = E(V(((0, 0), (1, 2), (3, -1))))
        for invalid in (True, 1.0, None, (1, 0)):
            self.refused(geometry.tangent(invalid), 'input')
            self.refused(geometry.pythagorean(invalid), 'input')
        self.assertEqual(self.accepted(geometry.pythagorean(1)), geometry.quarter_turn)
        self.assertEqual(self.accepted(geometry.pythagorean(0)), self.accepted(geometry.vector.scale((-1, 0))))
        self.refused(geometry.pythagorean(1 << 2048), 'resource')
        self.refused(geometry.tangent(1 << 4096), 'resource')
        self.refused(P(NORTH, geometry.vector).rotate((1 << 2048, 0), (0, 0)), 'resource')
        # The admitted vector has a bounded norm; its meridian's squared norm does not.
        huge = E(V(((0, 0), (1 << 2047, 0), (0, 0))))
        self.refused(huge.meridian(), 'resource')

    def test_symbolic_tomography_complete_certificate_and_immutability(self) -> None:
        model = H(); self.assertEqual(self.accepted(model.verify()), {'tomography_rank': 9, 'checks': 13})
        self.assertEqual(len(model.rays), 9); self.assertEqual(len(model.values), 9)
        self.assertEqual(len(model.coefficients), 9)
        with self.assertRaises(TypeError):
            model.form[0, 0] = 7
        with self.assertRaises(FrozenInstanceError):
            model.rays = ()  # type: ignore[misc]
        output = self.accepted(model.verify()); output['tomography_rank'] = 0
        self.assertEqual(self.accepted(model.verify())['tomography_rank'], 9)

    @settings(max_examples=25, derandomize=True, deadline=None, database=None)
    @given(fixture.VECTOR, st.lists(st.integers(-5, 5), min_size=9, max_size=9))
    def test_generated_tomography_evaluation_against_numeric_hermitian_form(self, raw: object, coefficients: list[int]) -> None:
        vector = V(raw); assume(vector.squared_norm > 0); model = H()
        d0, d1, d2, a01, a02, a12, b01, b02, b12 = coefficients
        form = sp.Matrix([[d0, a01+sp.I*b01, a02+sp.I*b02],
                          [a01-sp.I*b01, d1, a12+sp.I*b12], [a02-sp.I*b02, a12-sp.I*b12, d2]])
        symbols = sp.symbols('d0 d1 d2 a01 a02 a12 b01 b02 b12', real=True)
        actual = self.accepted(model.evaluate(vector)).subs(dict(zip(symbols, coefficients)))
        values = fixture.symbolic(vector); expected = (values.conjugate().T*form*values)[0]/(values.conjugate().T*values)[0]
        self.assertEqual(sp.simplify(actual-expected), 0)

    def test_kernel_relations_against_operator_matrices_and_wrong_sign(self) -> None:
        model = H()
        for vector, weights in kernel_fixtures():
            residual = projector(vector)
            for weight, ray in zip(weights, model.rays):
                residual += weight*projector(ray)
            self.assertEqual(residual.applyfunc(sp.simplify), sp.zeros(3))
            self.assertTrue(self.accepted(model.kernel_relation(vector, weights)))
            changed = list(weights); changed[0] += 1
            self.assertFalse(self.accepted(model.kernel_relation(vector, changed)))
        vector = V(((1, 0), (0, 1), (0, 0)))
        imaginary = model.coefficients[6]
        self.assertEqual(sp.diff(self.accepted(model.evaluate(vector)), imaginary), -1)

    def test_parallelogram_against_projectors_and_exact_domains(self) -> None:
        model = H(); zero = V(((0, 0),)*3)
        invalid: object
        for vector, _ in kernel_fixtures():
            partner = self.accepted(vector.cross(NORTH)); pair = P(vector, partner)
            self.assertTrue(self.accepted(model.parallelogram(pair)))
            lhs = projector(self.accepted(vector.add(partner)))+projector(self.accepted(vector.sub(partner)))
            total = vector.squared_norm+partner.squared_norm
            rhs = 2*vector.squared_norm/total*projector(vector)+2*partner.squared_norm/total*projector(partner)
            self.assertEqual((lhs-rhs).applyfunc(sp.simplify), sp.zeros(3))
        for invalid in (None, zero, NORTH.to_pairs()):
            self.refused(model.evaluate(invalid), 'input')
        for invalid in (None, (1,)*8, (1.0,)*9, (True,)*9):
            self.refused(model.kernel_relation(NORTH, invalid), 'input')
        self.refused(model.kernel_relation(NORTH, (1 << 4096,)*9), 'resource')
        self.refused(model.parallelogram((NORTH, NORTH)), 'input')

    def test_complex_quarter_turn_and_zero_ray_preflight(self) -> None:
        vector = V(((0, 0), (1, 0), (0, 1))); geometry = E(vector)
        self.assertEqual(geometry.quarter_turn.to_pairs(), ((Q(0), Q(0)), (Q(0), Q(1)), (Q(1), Q(0))))
        values, turned = fixture.symbolic(vector), fixture.symbolic(geometry.quarter_turn)
        self.assertEqual((values.conjugate().T*turned)[0].expand(), 0)
        zero = V(((0, 0),)*3)
        with patch.object(Q, '__truediv__', side_effect=AssertionError('division before ray admission')):
            self.refused(E.born_weight(zero), 'input')

    def test_piron_formula_and_fixed_numeric_hermitian_evaluation(self) -> None:
        geometry = E(V(((0, 0), (1, 1), (2, -1))))
        pair = self.accepted(geometry.piron((2, 1)))
        base, quarter = fixture.symbolic(geometry.base), fixture.symbolic(geometry.quarter_turn)
        self.assertEqual(fixture.symbolic(pair.first).applyfunc(sp.expand), (base+(2+sp.I)*quarter).applyfunc(sp.expand))
        partner = -5*geometry.vector.squared_norm*base+(1+geometry.vector.squared_norm)*(2+sp.I)*quarter
        self.assertEqual(fixture.symbolic(pair.second).applyfunc(sp.expand), partner.applyfunc(sp.expand))
        model = H(); vector = V(((1, 0), (1, 1), (2, -1)))
        form = sp.Matrix([[1, 2+sp.I, 3-2*sp.I], [2-sp.I, 4, -1+3*sp.I], [3+2*sp.I, -1-3*sp.I, 5]])
        variables = sp.symbols('d0 d1 d2 a01 a02 a12 b01 b02 b12', real=True)
        coefficients = (1, 4, 5, 2, 3, -1, 1, -2, 3)
        actual = self.accepted(model.evaluate(vector)).subs(dict(zip(variables, coefficients)))
        values = fixture.symbolic(vector)
        expected = (values.conjugate().T*form*values)[0]/(values.conjugate().T*values)[0]
        self.assertEqual(sp.expand(actual-expected), 0)

    def test_unexpected_failures_propagate_across_composed_queries(self) -> None:
        geometry = E(V(((0, 0), (1, 0), (0, 0)))); model = H()
        for exception in (RuntimeError, KeyboardInterrupt, SystemExit):
            with patch.object(V, '_scale', side_effect=exception), self.assertRaises(exception):
                geometry.piron((1, 0))
            with patch.object(H, '_evaluate', side_effect=exception), self.assertRaises(exception):
                model.kernel_relation(NORTH, (0,)*9)


if __name__ == '__main__':
    unittest.main()
