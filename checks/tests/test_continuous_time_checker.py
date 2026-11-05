"""Independent finite-map roots, Gaussian matrices and branch witnesses. AuthorityEffect: None."""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
from itertools import product
import io
import json
from pathlib import Path
import runpy
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from hypothesis import given, settings, strategies as st
import sympy as sp

CHECKS = Path(__file__).resolve().parents[1]
APP = CHECKS/"independent/ds-continuous-time-exp-generator.py"
sys.path.insert(0, str(CHECKS))
from checker_support.boundary import Violation, evaluate
from checker_support.cases import Cases
from checker_support.domains import Failure
from checker_support.gaussian_rational import GaussianRational as G
from checker_support.rational_matrix import RationalMatrix

PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)
TABLE = st.lists(st.integers(0, 3), min_size=4, max_size=4)
PAIRS = st.lists(st.tuples(st.integers(-6, 6), st.integers(-6, 6)), min_size=4, max_size=4)


def load() -> SimpleNamespace:
    return SimpleNamespace(**runpy.run_path(str(APP)))


def _operator(images: tuple[int, ...]) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(len(images), len(images), lambda row, column: int(row == images[column]))


def _matrix(values: tuple[tuple[int, int], ...] | list[tuple[int, int]]) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(2, 2, [real+sp.I*imaginary for real, imaginary in values])


def _root_index(size: int) -> dict[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    found: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for images in product(range(size), repeat=size):
        squared = _operator(images)**2
        target = tuple(next(row for row in range(size) if squared[row, column] == 1) for column in range(size))
        found.setdefault(target, []).append(images)
    return {target: tuple(values) for target, values in found.items()}


class ContinuousTimeCheckerTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object, kind: str = "input") -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("refusal lacks error")
        self.assertEqual(result.error.kind, kind)
        return result.error

    def test_oracles_and_pure_import(self) -> None:
        self.assertEqual(_operator((1, 1)), sp.ImmutableMatrix(((0, 0), (1, 1))))
        self.assertEqual(_matrix([(1, 2), (3, 4), (5, 6), (7, 8)])[1, 0], 5+6*sp.I)
        self.assertEqual(_root_index(1), {(0,): ((0,),)})
        self.assertEqual(_root_index(2)[(0, 1)], ((0, 1), (1, 0)))
        self.assertNotIn((1, 0), _root_index(2))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            module = load()
        self.assertEqual(output.getvalue(), "")
        self.assertNotIn("checks", vars(module))

    def test_complete_small_root_censuses_and_four_state_witness(self) -> None:
        module = load()
        for size in range(1, 4):
            reference = _root_index(size)
            for images in product(range(size), repeat=size):
                result = module.FiniteEndomap(images).square_roots()
                self.assertTrue(result.ok)
                self.assertEqual(tuple(root.images for root in result.value), reference.get(images, ()))
        self.assertEqual(tuple(value.images for value in module.maps()), ((0, 0), (0, 1), (1, 0), (1, 1)))
        roots = module.FiniteEndomap((1, 0, 3, 2)).square_roots().value
        self.assertEqual(tuple(root.images for root in roots), ((2, 3, 1, 0), (3, 2, 0, 1)))
        self.assertEqual(module.FiniteEndomap((1, 2, 3, 0)).square_roots().value, ())

    def test_composition_refuses_carrier_loss(self) -> None:
        module = load()
        for left_size, right_size in product(range(1, 5), repeat=2):
            left = module.FiniteEndomap((0,)*left_size)
            right = module.FiniteEndomap((0,)*right_size)
            result = left.compose(right)
            self.assertEqual(result.ok, left_size == right_size)
            if left_size != right_size:
                self.assertEqual(result.error.kind, "input")

    @PROPERTY
    @given(TABLE, TABLE, st.integers(0, 30))
    def test_generated_composition_action_and_power(self, first: list[int], second: list[int], exponent: int) -> None:
        module = load()
        a, b = module.FiniteEndomap(first), module.FiniteEndomap(second)
        composed = a.compose(b)
        self.assertTrue(composed.ok)
        self.assertEqual(_operator(composed.value.images), _operator(tuple(first))*_operator(tuple(second)))
        power = a.power(exponent)
        self.assertTrue(power.ok)
        self.assertEqual(_operator(power.value.images), _operator(tuple(first))**exponent)
        for state in range(4):
            self.assertEqual(a.apply(state).value, first[state])

    def test_finite_map_ownership_domains_and_full_power_budget(self) -> None:
        module = load()
        images = [1, 2, 0]
        value = module.FiniteEndomap(images)
        images.clear()
        self.assertEqual(value.images, (1, 2, 0))
        with self.assertRaises(FrozenInstanceError):
            value.images = (0, 1, 2)
        for invalid in ((), (True, 0), (0, 1.0), (-1, 0), (0, 2), "01", None):
            self.refused(module.FiniteEndomap, invalid)
        self.refused(module.FiniteEndomap, (0,)*5, kind="resource")
        for invalid_state in (True, False, -1, 3, 1.0, None):
            self.assertEqual(value.apply(invalid_state).error.kind, "input")
        for exponent in (True, -1, 1.0, None):
            self.assertEqual(value.power(exponent).error.kind, "input")
        self.assertEqual(value.power(4097).error.kind, "resource")
        self.assertEqual(value.power(4096).value.images, (1, 2, 0))
        self.assertEqual(value.power(0).value.images, (0, 1, 2))
        self.assertEqual(value.compose(module.FiniteEndomap((0, 1))).error.kind, "input")
        self.assertEqual(value.compose((1, 2, 0)).error.kind, "input")
        self.assertIs(module.toggle(False), True)
        self.assertIs(module.toggle(True), False)
        for invalid_boolean in (0, 1, "false", None):
            self.refused(module.toggle, invalid_boolean)

    @PROPERTY
    @given(PAIRS, PAIRS)
    def test_gaussian_products_against_symbolic_oracle(self, left: list[tuple[int, int]], right: list[tuple[int, int]]) -> None:
        module = load()
        expected = (_matrix(left)*_matrix(right)).applyfunc(sp.expand)
        self.assertEqual(_matrix(module.mmul(left, right)), expected)
        addition = module.gadd(left[0], right[0])
        multiply = module.gmul(left[0], right[0])
        first, second = left[0][0]+sp.I*left[0][1], right[0][0]+sp.I*right[0][1]
        self.assertEqual(addition[0]+sp.I*addition[1], first+second)
        self.assertEqual(multiply[0]+sp.I*multiply[1], sp.expand(first*second))

    def test_scaled_roots_are_distinct_unitary_half_steps(self) -> None:
        module = load()
        swap = sp.ImmutableMatrix(((0, 1), (1, 0)))
        for raw in (module.SCALED, module.NEGATIVE):
            half = _matrix(raw)/2
            self.assertEqual((half*half).applyfunc(sp.expand), swap)
            self.assertEqual((half.conjugate().T*half).applyfunc(sp.expand), sp.eye(2))
            self.assertEqual(_matrix(module.mmul(raw, raw)), 4*swap)
        self.assertNotEqual(module.SCALED, module.NEGATIVE)
        values = [list(pair) for pair in module.SCALED]
        snapshot = module.mmul(values, module.SCALED)
        values[0][0] = 9
        self.assertEqual(snapshot, module.FOUR_SWAP)

    def test_exact_gaussian_domains_and_preflight(self) -> None:
        module = load()
        for bad in ((), (1,), (1, 2, 3), (True, 0), (1.0, 0), (Q(1), 0), "12", None):
            self.refused(module.gadd, bad, (0, 0))
            self.refused(module.gmul, (0, 0), bad)
        for bad_matrix in ((), (module.SCALED[0],)*3, ((True, 0),)*4, "matrix", None):
            self.refused(module.mmul, module.SCALED, bad_matrix)
        with patch.object(G, "__mul__", side_effect=RuntimeError("must not multiply")):
            self.refused(module.mmul, module.SCALED, ((True, 0),)*4)
        self.refused(module.gmul, (2**4095, 0), (2, 0), kind="resource")
        self.refused(module.gadd, (2**4095, 0), (2**4095, 0), kind="resource")

    @PROPERTY
    @given(st.integers(-1000, 1000), st.integers(-1000, 1000))
    def test_cayley_and_odd_branch_oracles(self, parameter: int, branch: int) -> None:
        module = load()
        phase = (1+sp.I*parameter)/(1-sp.I*parameter)
        self.assertEqual(sp.simplify(phase*sp.conjugate(phase)), 1)
        self.assertTrue(module.cayley(parameter))
        result = module.energy(branch)
        self.assertEqual((result-1)//2, branch)
        self.assertEqual(result % 2, 1)
        self.assertEqual(module.energy(branch+1)-result, 2)

    def test_integer_domains_and_polynomial_resource_boundaries(self) -> None:
        module = load()
        for value in (True, 1.0, Q(1), "1", None):
            self.refused(module.energy, value)
            self.refused(module.cayley, value)
            self.refused(module.nilpotent, value, 1, 1, -1)
        self.refused(module.energy, 2**4095, kind="resource")
        self.assertEqual(module.energy(-(2**4095)), -(2**4096)+1)
        self.refused(module.energy, 2**4096, kind="resource")
        self.assertTrue(module.cayley(2**1023))
        self.refused(module.cayley, 2**1024, kind="resource")
        self.refused(module.cayley, 2**2048, kind="resource")
        self.refused(module.nilpotent, 2**4096-1, 0, 0, 0, kind="resource")
        self.refused(module.nilpotent, 0, 0, 2**4096, 0, kind="resource")

    def test_nilpotent_forced_candidate_against_matrix_oracle(self) -> None:
        module = load()
        swap = sp.ImmutableMatrix(((0, 1), (1, 0)))
        candidate = swap-sp.eye(2)
        self.assertEqual(candidate**2, sp.ImmutableMatrix(((2, -2), (-2, 2))))
        for entries in product((-1, 0, 1), repeat=4):
            matrix = sp.ImmutableMatrix(2, 2, entries)
            expected = matrix+sp.eye(2) == swap and matrix**2 == sp.zeros(2)
            self.assertEqual(module.nilpotent(*entries), expected)
        self.assertFalse(module.nilpotent(-1, 1, 1, -1))

    def test_reentrant_counts_faults_and_cancellation(self) -> None:
        module = load()
        for _ in range(2):
            cases = Cases()
            module.verify(cases)
            self.assertEqual(cases.checks, 355)
        self.refused(module.verify, None)
        with patch.object(G, "__mul__", return_value=G(0)):
            self.refused(module.verify, Cases(), kind="check")
        value = module.FiniteEndomap((1, 0))
        with patch.object(module.FiniteEndomap, "_compose", side_effect=RuntimeError("bug")):
            with self.assertRaises(RuntimeError):
                value.power(2)
        with patch.object(module.FiniteEndomap, "_compose", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                value.square_roots()

    @PROPERTY
    @given(st.lists(st.integers(-8, 8), min_size=4, max_size=4), st.lists(st.integers(-8, 8), min_size=4, max_size=4))
    def test_integer_matrix_product_against_symbolic_oracle(self, left: list[int], right: list[int]) -> None:
        module = load()
        self.assertEqual(sp.ImmutableMatrix(2, 2, module.mm(left, right)), sp.ImmutableMatrix(2, 2, left)*sp.ImmutableMatrix(2, 2, right))

    @PROPERTY
    @given(st.integers(0, 4096))
    def test_quarter_turn_powers_against_matrix_and_cycle(self, exponent: int) -> None:
        module = load()
        matrix = sp.ImmutableMatrix(((0, -1), (1, 0)))
        self.assertEqual(sp.ImmutableMatrix(2, 2, module.powj(exponent)), matrix**exponent)
        cycle = module.FiniteEndomap((1, 2, 3, 0)).power(exponent).value
        orbit = ((1, 0), (0, 1), (-1, 0), (0, -1))
        self.assertEqual(tuple(matrix**exponent*sp.ImmutableMatrix((1, 0))), orbit[cycle.images[0]])
        self.assertEqual(module.powj(exponent), module.REPS[exponent % 4])

    def test_fixed_nonsymmetric_integer_products_and_snapshots(self) -> None:
        module = load()
        left, right = [1, 2, 3, 4], [2, -1, 1, 3]
        result = module.mm(left, right)
        self.assertEqual(result, (4, 5, 10, 9))
        self.assertTrue(all(type(entry) is int for entry in result))
        self.assertEqual(module.mm(right, left), (-1, 0, 10, 14))
        left.clear()
        right[0] = 9
        self.assertEqual(result, (4, 5, 10, 9))
        self.assertEqual(tuple(module.powj(exponent) for exponent in range(5)), (module.EYE, module.JAY, module.JAY2, module.JAY3, module.EYE))
        self.assertEqual(module.powj(4096), module.EYE)

    def test_residue_exact_domains_and_resource_limits(self) -> None:
        module = load()
        for exponent in (True, False, -1, 1.0, Q(1), "1", None):
            self.refused(module.powj, exponent)
        self.refused(module.powj, 4097, kind="resource")
        for bad in ((), (1, 2, 3), (1, 2, 3, 4, 5), (True, 0, 0, 1), (1.0, 0, 0, 1), (Q(1), 0, 0, 1), "1234", None):
            self.refused(module.mm, bad, module.EYE)
            self.refused(module.mm, module.EYE, bad)
        self.refused(module.mm, (2**4096, 0, 0, 1), module.EYE, kind="resource")
        self.refused(module.mm, (2**4095, 0, 0, 1), (2, 0, 0, 1), kind="resource")
        self.refused(module._real_flat, RationalMatrix.eye(3))
        self.refused(module._real_flat, RationalMatrix(((Q(1, 2), 0), (0, 1))))

    def test_residue_preflight_before_multiplication(self) -> None:
        module = load()
        with patch.object(RationalMatrix, "mul", side_effect=RuntimeError("must not multiply")):
            self.refused(module.powj, -1)
            self.refused(module.powj, True)
            self.refused(module.mm, module.EYE, (True, 0, 0, 1))
        with patch.object(RationalMatrix, "mul", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                module.powj(2)

    def test_residue_control_counts_and_injected_fault(self) -> None:
        module = load()
        for _ in range(2):
            cases = Cases()
            module.verify_residues(cases)
            self.assertEqual(cases.checks, 257)
        self.refused(module.verify_residues, None)
        with patch.object(RationalMatrix, "mul", return_value=RationalMatrix.eye(2)):
            self.refused(module.verify_residues, Cases(), kind="check")

    def test_executable_receipt_and_failure_exit(self) -> None:
        flags = [] if __debug__ else ["-O"]
        result = subprocess.run([sys.executable, "-I", "-B", *flags, "-X", "utf8", str(APP)],
                                capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        receipt = json.loads(result.stdout)
        self.assertEqual((receipt["status"], receipt["checks"], receipt["Boolean_maps"]), ("passed", 612, 4))
        self.assertEqual((receipt["root_and_branch"], receipt["residues"]), (355, 257))
        with patch.object(Cases, "require", side_effect=Violation("check", "injected")), contextlib.redirect_stderr(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as failure:
                runpy.run_path(str(APP), run_name="__main__")
        self.assertEqual(failure.exception.code, 1)
        self.assertEqual(json.loads(output.getvalue())["kind"], "check")


if __name__ == "__main__":
    unittest.main(verbosity=2)
