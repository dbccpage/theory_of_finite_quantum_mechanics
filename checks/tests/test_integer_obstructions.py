"""Independent factorization and finite-census checks for integer obstructions.

AuthorityEffect: None. These tests do not supply continuum or physical claims.
"""
from __future__ import annotations

import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
import importlib.util
import io
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from typing import TypeVar, cast
import unittest
from unittest.mock import patch

from hypothesis import assume, given, settings, strategies as st
import sympy as sp

CHECKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHECKS))
from checker_support.boundary import Violation, evaluate
from checker_support.cases import Cases
from checker_support.integer_quadratic_equation import IntegerQuadraticEquation as Equation
from checker_support.outcome import Outcome

T = TypeVar('T')
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)
COEFFICIENTS = st.tuples(*(st.integers(-50, 50) for _ in range(3)))
APP = CHECKS/'independent/fq-gap-continuum-hilbert-lift.py'


def load() -> ModuleType:
    name = 'reviewed_integer_obstruction_controls'
    spec = importlib.util.spec_from_file_location(name, APP)
    if spec is None or spec.loader is None:
        raise Violation('resource', 'integer obstruction import specification unavailable')
    module = importlib.util.module_from_spec(spec); previous = sys.modules.get(name)
    try:
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous


def reference_roots(coefficients: tuple[int, int, int]) -> tuple[Q, ...]:
    a, b, c = coefficients; x = sp.Symbol('x')
    factors = sp.Poly(a*x*x+b*x+c, x, domain=sp.QQ).ground_roots()
    return tuple(sorted(Q(root) for root in factors))


class IntegerObstructionTests(unittest.TestCase):
    def accepted(self, result: Outcome[T]) -> T:
        self.assertIsNone(result.error)
        return cast(T, result.value)

    def refused(self, result: Outcome[T], kind: str) -> None:
        self.assertIsNotNone(result.error)
        if result.error is not None:
            self.assertEqual(result.error.kind, kind)

    def test_all_small_polynomials_against_independent_factorization(self) -> None:
        for coefficients in product(range(-3, 4), repeat=3):
            if coefficients == (0, 0, 0):
                continue
            equation = Equation(coefficients); expected = reference_roots(cast(tuple[int, int, int], coefficients))
            self.assertEqual(self.accepted(equation.rational_roots()), expected, coefficients)
            integers = tuple(q.numerator for q in expected if q.denominator == 1)
            self.assertEqual(self.accepted(equation.integer_roots()), integers, coefficients)
            a, b, c = coefficients
            self.assertEqual(self.accepted(equation.discriminant()), b*b-4*a*c)

    @PROPERTY
    @given(COEFFICIENTS, st.integers(-30, 30), st.integers(1, 13), st.integers(-30, 30))
    def test_generated_evaluation_and_homogenization(self, coefficients: tuple[int, int, int],
                                                    numerator: int, denominator: int, y: int) -> None:
        assume(coefficients != (0, 0, 0)); equation = Equation(coefficients)
        a, b, c = coefficients; x = Q(numerator, denominator)
        self.assertEqual(self.accepted(equation.evaluate(x)), a*x*x+b*x+c)
        homogeneous = self.accepted(equation.homogeneous_value((numerator, y)))
        self.assertEqual(homogeneous, a*numerator*numerator+b*numerator*y+c*y*y)
        expected = reference_roots(coefficients)
        self.assertEqual(self.accepted(equation.rational_roots()), expected)

    @PROPERTY
    @given(st.integers(-20, 20), st.integers(-20, 20), st.integers(1, 13),
           st.integers(1, 13), st.integers(-10, 10))
    def test_generated_factored_roots_are_complete_sorted_and_distinct(self, first: int, second: int,
                                                                     d1: int, d2: int, scale: int) -> None:
        assume(scale != 0)
        coefficients = (scale*d1*d2, -scale*(first*d2+second*d1), scale*first*second)
        equation = Equation(coefficients)
        self.assertEqual(self.accepted(equation.rational_roots()), tuple(sorted({Q(first, d1), Q(second, d2)})))

    def test_square_root_boundary_and_independent_square_census(self) -> None:
        squares = {n*n: n for n in range(33)}
        for number in range(-10, 1025):
            self.assertEqual(self.accepted(Equation.square_root(number)), squares.get(number))
        base = (1 << 2047)+3
        self.assertEqual(self.accepted(Equation.square_root(base*base)), base)
        self.assertIsNone(self.accepted(Equation.square_root(base*base+1)))
        self.refused(Equation.square_root(1 << 4096), 'resource')
        for value in (True, 4.0, Q(4), None, '4'):
            self.refused(Equation.square_root(value), 'input')

    def test_exact_domains_constant_linear_and_repeated_roots(self) -> None:
        invalid: object
        for invalid in (None, (), (1, 2), (1, 2, 3, 4), (0, 0, 0), (True, 1, 1), (1.0, 1, 1), (Q(1), 1, 1)):
            self.refused(evaluate(Equation, invalid), 'input')
        for coefficients, rational, integer in (((0, 0, 2), (), ()), ((0, 2, -1), (Q(1, 2),), ()),
                                                ((0, -2, 4), (Q(2),), (2,)), ((1, -4, 4), (Q(2),), (2,)),
                                                ((-1, 0, 1), (Q(-1), Q(1)), (-1, 1))):
            equation = Equation(coefficients)
            self.assertEqual(self.accepted(equation.rational_roots()), rational)
            self.assertEqual(self.accepted(equation.integer_roots()), integer)
        equation = Equation((1, -1, -1))
        for invalid in (None, True, 1.0, '1', (1,)):
            self.refused(equation.evaluate(invalid), 'input')
        for invalid in (None, (1,), (1, 2, 3), (True, 0), (1.0, 0), (Q(1), 0)):
            self.refused(equation.homogeneous_value(invalid), 'input')

    def test_owned_coefficients_and_immutable_reentrant_results(self) -> None:
        coefficients = [1, -3, 2]; equation = Equation(coefficients); coefficients[0] = 7
        self.assertEqual(equation.coefficients, (1, -3, 2))
        with self.assertRaises(FrozenInstanceError):
            equation.constant = 0  # type: ignore[misc]
        self.assertEqual(self.accepted(equation.rational_roots()), (Q(1), Q(2)))
        self.assertEqual(self.accepted(equation.rational_roots()), (Q(1), Q(2)))

    def test_resource_boundaries_cover_products_prefixes_and_arguments(self) -> None:
        maximum = (1 << 4096)-1
        self.assertEqual(Equation((0, 0, maximum)).constant, maximum)
        self.refused(evaluate(Equation, (0, 0, 1 << 4096)), 'resource')
        square = Equation((1, 0, 0))
        self.assertEqual(self.accepted(square.evaluate(1 << 2047)), Q(1 << 4094))
        self.refused(square.evaluate(1 << 2048), 'resource')
        self.refused(square.evaluate(Q(1, 1 << 4096)), 'resource')
        self.refused(square.homogeneous_value((1 << 2048, 0)), 'resource')
        self.refused(Equation((1, 1 << 2048, 1)).discriminant(), 'resource')
        self.refused(Equation((1 << 4095, 0, 0)).discriminant(), 'resource')
        self.refused(Equation((-(1 << 2046), (1 << 2048)-1, 1 << 2046)).discriminant(), 'resource')
        self.refused(Equation((1, 1 << 2048, 1)).rational_roots(), 'resource')
        self.refused(Equation((1, 1 << 2048, 1)).integer_roots(), 'resource')

    def test_root_replay_guards_and_unexpected_failures(self) -> None:
        equation = Equation((1, -3, 2))
        with patch.object(Equation, '_evaluate', return_value=Q(1)):
            self.refused(equation.rational_roots(), 'check')
        for exception in (RuntimeError, KeyboardInterrupt, SystemExit):
            with patch.object(Equation, '_discriminant', side_effect=exception), self.assertRaises(exception):
                equation.rational_roots()

    def test_original_sample_populations_and_actual_per_run_counter(self) -> None:
        module = load(); observed: list[str] = []; implementation = Cases.require
        def record(cases: Cases, condition: bool, message: str) -> None:
            observed.append(message); implementation(cases, condition, message)
        with patch.object(Cases, 'require', record):
            result = self.accepted(module.verify())
        self.assertEqual(result['checks'], len(observed)); self.assertEqual(len(observed), 18949)
        self.assertEqual((result['hilbert_points'], result['pair_points'], result['positive_denominators'], result['box_points']),
                         (65, 961, 2000, 15625))
        self.assertEqual(result['box_hits'], [[0, 0, 0]]); self.assertEqual(result['natural_hits'], 0)
        self.assertEqual(result['square_residues_mod5'], [0, 1, 4, 4, 1])
        self.assertEqual(observed.count('discriminant identity sample'), 65)
        self.assertEqual(observed.count('left descent scaling sample'), 6)
        self.assertEqual(observed.count('right descent scaling sample'), 6)
        self.assertEqual(observed.count('cleared integer box census'), 15625)
        self.assertIn('no scalar-field selection', result['scope'])

    @settings(max_examples=30, derandomize=True, deadline=None, database=None)
    @given(st.integers(0, 8), st.integers(0, 8), st.integers(0, 40), st.integers(0, 4))
    def test_generated_census_policies_against_direct_enumeration(self, radius: int, pair: int, natural: int, box: int) -> None:
        controls = load().IntegerObstructionControls(radius, pair, natural, box)
        result = self.accepted(controls.verify())
        pairs = [(a, b) for a, b in product(range(pair+1), repeat=2) if Q(a*a, 4) == Q(b*b, 5)]
        self.assertEqual(pairs, [(0, 0)]); self.assertEqual(result['pair_points'], (pair+1)**2)
        hits = [(a, b, d) for a, b, d in product(range(-box, box+1), repeat=3)
                if Q(a*a-b*b, 3) == Q(d*d, 5) and a*a+b*b == d*d]
        self.assertEqual(result['box_hits'], [list(p) for p in hits])
        natural_hits = sum(5*a*a == 4*b*b for b in range(1, natural+1) for a in range(b+1))
        self.assertEqual(result['natural_hits'], natural_hits)
        self.assertEqual(result['hilbert_points'], len(list(range(-radius, radius+1))))

    def test_policy_bounds_zero_pair_admission_and_ownership(self) -> None:
        cls = load().IntegerObstructionControls
        for index, maximum in enumerate((64, 64, 10000, 16)):
            for invalid in (-1, True, 1.0, Q(1), None, maximum+1):
                values: list[object] = [0, 0, 0, 0]; values[index] = invalid
                self.refused(evaluate(cls, *values), 'resource' if invalid == maximum+1 else 'input')
        maximum_report = self.accepted(cls(64, 64, 10000, 16).verify())
        self.assertEqual(maximum_report['checks'], 50845)
        controls = cls(0, 0, 0, 0); self.assertEqual(self.accepted(controls.verify())['checks'], 45)
        with self.assertRaises(FrozenInstanceError):
            controls.box_radius = 2
        for invalid_pair in (None, (), (1, 1), (-1, 0), (0.0, 0.0), (False, False), (Q(0), 0)):
            self.refused(controls.zero_pair(invalid_pair), 'input')
        self.refused(controls.zero_pair((1 << 4096, 0)), 'resource')
        self.assertEqual(self.accepted(controls.zero_pair((0, 0))), (0, 0))
        with patch.object(Equation, '_homogeneous_value', return_value=0):
            self.refused(controls.zero_pair((1, 1)), 'check')

    def test_composition_refuses_helper_failures_without_suppressing_them(self) -> None:
        module = load(); controls = module.IntegerObstructionControls(0, 0, 5, 0)
        with patch.dict(type(controls)._positive_denominators.__globals__, _square_root=lambda _: 2):
            self.refused(controls.verify(), 'check')
        def refusal(_: object) -> int:
            raise Violation('resource', 'injected square-root budget')
        with patch.dict(type(controls)._positive_denominators.__globals__, _square_root=refusal):
            self.refused(controls.verify(), 'resource')
        with patch.object(Equation, '_rational_roots', return_value=()):
            self.refused(controls.verify(), 'check')

    def test_quiet_import_cli_and_per_run_failure_state(self) -> None:
        output = io.StringIO(); previous = ModuleType('previous')
        with patch.dict(sys.modules, reviewed_integer_obstruction_controls=previous):
            with contextlib.redirect_stdout(output):
                module = load()
            self.assertIs(sys.modules['reviewed_integer_obstruction_controls'], previous)
        self.assertEqual(output.getvalue(), '')
        with patch.object(Equation, '_rational_roots', side_effect=Violation('check', 'injected')):
            self.refused(module.verify(), 'check')
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                self.assertEqual(module.main(), 1)
            self.assertEqual(out.getvalue(), ''); self.assertEqual(json.loads(err.getvalue())['kind'], 'check')
        reports = []
        for _ in range(2):
            with contextlib.redirect_stdout(output := io.StringIO()):
                self.assertEqual(module.main(), 0)
            reports.append(json.loads(output.getvalue()))
        self.assertEqual(reports[0], reports[1]); self.assertEqual(reports[0]['failures'], 0)
        process = subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8', str(APP)], capture_output=True, text=True, timeout=30)
        self.assertEqual(process.returncode, 0, process.stderr); self.assertEqual(json.loads(process.stdout), reports[0])

    def test_isolated_arithmetic_prefix_budgets(self) -> None:
        maximum = (1 << 4096)-1
        # The Horner prefix overflows before multiplication by one half shrinks it.
        self.refused(Equation((2, maximum, 0)).evaluate(Q(1, 2)), 'resource')
        # Both partial terms fit; only the final homogeneous sum overflows.
        self.refused(Equation((0, maximum, 1)).homogeneous_value((1, 1)), 'resource')

    def test_isolated_admission_and_first_failure(self) -> None:
        controls = load().IntegerObstructionControls(0, 0, 10, 0)
        with patch.object(Equation, '_homogeneous_value', side_effect=AssertionError('arithmetic before natural admission')):
            self.refused(controls.zero_pair((-1, 0)), 'input')
        calls: list[int] = []
        def bad_square(value: int) -> int:
            if calls:
                raise AssertionError('work continued after a rejected square-root result')
            calls.append(value)
            return 2
        with patch.dict(type(controls)._positive_denominators.__globals__, _square_root=bad_square):
            self.refused(evaluate(controls._positive_denominators, Cases()), 'check')
        self.assertEqual(calls, [20])
        original = Equation._rational_roots
        def roots(equation: Equation) -> tuple[Q, ...]:
            if equation.coefficients == (0, 2, -1):
                return ()
            return original(equation)
        with patch.object(Equation, '_rational_roots', roots):
            self.refused(controls.verify(), 'check')

    def test_application_unexpected_errors_and_cancellation_propagate(self) -> None:
        controls = load().IntegerObstructionControls(0, 0, 0, 0)
        for exception in (RuntimeError, KeyboardInterrupt, SystemExit):
            with patch.object(Equation, '_rational_roots', side_effect=exception), self.assertRaises(exception):
                controls.verify()


if __name__ == '__main__':
    unittest.main()
