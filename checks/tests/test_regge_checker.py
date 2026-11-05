"""Independent exact cosine-formula and supplied-block verification. AuthorityEffect: None."""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
import io
import json
from pathlib import Path
import runpy
import subprocess
import sys
from types import SimpleNamespace
from typing import Any
import unittest
from unittest.mock import patch

from hypothesis import given, settings, strategies as st
import sympy as sp

CHECKS = Path(__file__).resolve().parents[1]
APP = CHECKS/"independent/dfm-regge-gravity-fence.py"
sys.path.insert(0, str(CHECKS))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import Failure

PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)
RATIONAL = st.fractions(-5, 5, max_denominator=12)


def load() -> SimpleNamespace:
    return SimpleNamespace(**runpy.run_path(str(APP)))


def _block(beta: Q) -> Any:
    parameter = sp.Rational(beta.numerator, beta.denominator)
    generator = sp.ImmutableMatrix([[0, 1], [1, 0]])
    cayley = (sp.eye(2)+parameter*generator)*(sp.eye(2)-parameter*generator).inv()
    return sp.diag(cayley, sp.eye(2))


class ReggeCheckerTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object, kind: str = "input") -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("refusal lacks error")
        self.assertEqual(result.error.kind, kind)
        return result.error

    def test_oracle_and_import_lifecycle(self) -> None:
        self.assertEqual(_block(Q(0)), sp.eye(4))
        self.assertEqual(_block(Q(1, 2)), sp.ImmutableMatrix([[sp.Rational(5, 3), sp.Rational(4, 3), 0, 0],
                                                            [sp.Rational(4, 3), sp.Rational(5, 3), 0, 0],
                                                            [0, 0, 1, 0], [0, 0, 0, 1]]))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            load()
        self.assertEqual(output.getvalue(), "")
        with self.assertRaises(AssertionError):
            self.refused(lambda: None)

    @PROPERTY
    @given(RATIONAL, RATIONAL, RATIONAL)
    def test_cosine_formulas_against_gram_and_polynomial_oracles(self, a: Q, b: Q, c: Q) -> None:
        module = load()
        gram = sp.ImmutableMatrix([[b*b, (b*b+c*c-a*a)/2], [(b*b+c*c-a*a)/2, c*c]])
        self.assertEqual(module.cos_num(a, b, c), Q(2*gram[0, 1]))
        total = module.cos_num(a, b, c)+module.cos_num(b, a, c)+module.cos_num(c, a, b)
        self.assertEqual(total, Q(sp.ImmutableMatrix([a, b, c]).dot(sp.ImmutableMatrix([a, b, c]))))
        if b*c:
            self.assertEqual(module.cos_law(a, b, c), Q(gram[0, 1]/(b*c)))
        else:
            self.refused(module.cos_law, a, b, c)

    @PROPERTY
    @given(RATIONAL.filter(lambda value: value not in (-1, 1)))
    def test_cayley_matrix_trace_and_metric(self, beta: Q) -> None:
        module = load()
        block = module.CayleyBlock(beta)
        actual = block.matrix()
        self.assertTrue(actual.ok)
        expected = _block(beta)
        matrix = sp.ImmutableMatrix(actual.value.rows)
        self.assertEqual(matrix, expected)
        self.assertEqual(block.trace().value, Q(expected.trace()))
        self.assertEqual(module.block_trace(beta), Q(expected.trace()))
        self.assertEqual(module.gamma(beta), Q(expected[0, 0]))
        metric = sp.diag(1, -1, -1, -1)
        self.assertEqual(matrix.T*metric*matrix, metric)
        self.assertEqual(matrix.det(), 1)

    @PROPERTY
    @given(st.integers(2, 12), st.integers(0, 100), st.fractions(Q(1, 8), 4, max_denominator=8))
    def test_right_triangles_against_coordinate_projections(self, u: int, selector: int, scale: Q) -> None:
        module = load()
        v = 1+selector % (u-1)
        horizontal, vertical, hypotenuse = scale*(u*u-v*v), scale*2*u*v, scale*(u*u+v*v)
        self.assertEqual(horizontal*horizontal+vertical*vertical, hypotenuse*hypotenuse)
        self.assertEqual(module.cos_law(hypotenuse, horizontal, vertical), 0)
        self.assertEqual(module.cos_law(horizontal, vertical, hypotenuse), vertical/hypotenuse)
        self.assertEqual(module.cos_law(vertical, horizontal, hypotenuse), horizontal/hypotenuse)

    def test_fixed_values_signed_domain_and_parameter_separation(self) -> None:
        module = load()
        self.assertEqual(tuple(module.cos_num(*row) for row in ((5, 3, 4), (3, 4, 5), (4, 3, 5))), (0, 32, 18))
        self.assertEqual(tuple(module.cos_law(*row) for row in ((5, 3, 4), (3, 4, 5), (4, 3, 5))), (0, Q(4, 5), Q(3, 5)))
        self.assertEqual(module.cos_law(5, 1, 1), Q(-23, 2))
        self.assertEqual(module.cos_law(-2, -3, 4), Q(-7, 8))
        for beta in (Q(0), Q(1, 2), Q(-1, 2), Q(2), Q(-2)):
            block = module.CayleyBlock(beta)
            self.assertEqual(sp.ImmutableMatrix(block.matrix().value.rows), _block(beta))
            self.assertEqual(block.trace().value, Q(_block(beta).trace()))
        self.assertEqual(module.gamma(Q(1, 2)), Q(5, 3))
        self.assertEqual(module.block_trace(Q(1, 2)), Q(16, 3))
        self.assertNotEqual(module.block_trace(Q(1, 2)), Q(7, 5))

    def test_invalid_domains_and_poles(self) -> None:
        module = load()
        for bad in (True, 1.0, "1", None, complex(1)):
            for operation in (module.exact, module.CayleyBlock, module.gamma, module.block_trace):
                self.refused(operation, bad)
            for args in ((bad, 3, 4), (5, bad, 4), (5, 3, bad)):
                self.refused(module.cos_num, *args)
                self.refused(module.cos_law, *args)
        for pole in (-1, 1, Q(-1), Q(1)):
            for operation in (module.CayleyBlock, module.gamma, module.block_trace):
                self.refused(operation, pole)
        for args in ((1, 0, 1), (1, 1, 0), (0, 0, 0)):
            self.refused(module.cos_law, *args)
        self.assertEqual(module.cos_num(0, 0, 0), 0)

    def test_component_square_and_prefix_budgets(self) -> None:
        module = load()
        self.assertEqual(module.exact(2**4095), 2**4095)
        self.refused(module.exact, 2**4096, kind="resource")
        self.refused(module.exact, Q(1, 2**4096), kind="resource")
        self.refused(module.cos_num, 2**2048, 1, 1, kind="resource")
        self.refused(module.cos_num, 1, 2**2048, 1, kind="resource")
        self.refused(module.cos_num, 1, 1, 2**2048, kind="resource")
        large = 2**2048-1
        self.refused(module.cos_num, large, large, large, kind="resource")
        self.refused(module.cos_law, 0, 2**2047, 2**2048, kind="resource")
        self.refused(module.cos_law, 2**2048, 0, 1)
        self.refused(module.CayleyBlock, 2**2048, kind="resource")
        near_pole = module.CayleyBlock(Q(large, large-1))
        self.assertEqual(near_pole.matrix().error.kind, "resource")
        self.assertEqual(near_pole.trace().error.kind, "resource")
        wide = module.CayleyBlock(large-1)
        self.assertTrue(wide.matrix().ok)
        self.assertEqual(wide.trace().error.kind, "resource")

    def test_owned_parameter_and_railway_paths(self) -> None:
        module = load()
        value = module.CayleyBlock(Q(1, 2))
        self.assertEqual((value.parameter, value.square, value.denominator), (Q(1, 2), Q(1, 4), Q(3, 4)))
        with self.assertRaises(FrozenInstanceError):
            value.parameter = Q(0)
        matrix = value.matrix().value
        with self.assertRaises(FrozenInstanceError):
            matrix.rows = ()
        self.assertEqual(value.trace().value, Q(16, 3))

    def test_denominator_budget_before_exact_cancellation(self) -> None:
        module = load()
        b, c = Q(2**2048-49, 5), Q(2**2048-5, 5)
        numerator, denominator = b*b+c*c, 2*b*c
        quotient = numerator/denominator
        self.assertEqual(numerator.numerator.bit_length(), 4093)
        self.assertEqual(denominator.numerator.bit_length(), 4097)
        self.assertEqual((quotient.numerator.bit_length(), quotient.denominator.bit_length()), (4096, 4096))
        self.refused(module.cos_law, 0, b, c, kind="resource")

    def test_actual_trace_accumulation_and_fault_propagation(self) -> None:
        module = load()
        block = module.CayleyBlock(Q(1, 2))
        from checker_support.rational_matrix import RationalMatrix
        probe = RationalMatrix(((1, 0, 0, 0), (0, 2, 0, 0), (0, 0, 3, 0), (0, 0, 0, 4)))
        with patch.object(module.CayleyBlock, "_matrix", return_value=probe):
            self.assertEqual(block.trace().value, 10)
        for error in (RuntimeError("bug"), KeyboardInterrupt()):
            with patch.object(module.CayleyBlock, "_matrix", side_effect=error):
                with self.assertRaises(type(error)):
                    block.trace()

    def test_counts_guards_and_counterexample(self) -> None:
        module = load()
        run = Cases()
        module.check_numerator_identity(run)
        self.assertEqual(run.checks, 5)
        total = module.check_lengths(run)
        self.assertEqual(total, Q(7, 5))
        self.assertEqual(run.checks, 13)
        module.check_block(total, run)
        self.assertEqual(run.checks, 19)
        self.refused(module.check_numerator_identity, None)
        self.refused(module.check_lengths, None)
        self.refused(module.check_block, Q(7, 5), None)
        self.refused(module.check_block, True, Cases())
        self.refused(module.check_block, Q(16, 3), Cases(), kind="check")
        with patch.object(sp, "expand", return_value=sp.Integer(1)):
            self.refused(module.check_numerator_identity, Cases(), kind="check")
        for _ in range(2):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                module.main()
            self.assertEqual(json.loads(output.getvalue())["checks"], 19)

    def test_executable_cli_and_failure_exit(self) -> None:
        flags = [] if __debug__ else ["-O"]
        result = subprocess.run([sys.executable, "-I", "-B", *flags, "-X", "utf8", str(APP)], capture_output=True,
                                text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        receipt = json.loads(result.stdout)
        self.assertEqual((receipt["status"], receipt["checks"]), ("passed", 19))
        with patch.object(Cases, "require", side_effect=Violation("check", "injected")), contextlib.redirect_stderr(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as failure:
                runpy.run_path(str(APP), run_name="__main__")
        self.assertEqual(failure.exception.code, 1)
        self.assertEqual(json.loads(output.getvalue())["kind"], "check")
        module = load()
        with patch.object(sp, "expand", side_effect=RuntimeError("bug")):
            with self.assertRaises(RuntimeError):
                cli(module.main)


if __name__ == "__main__":
    unittest.main(verbosity=2)
