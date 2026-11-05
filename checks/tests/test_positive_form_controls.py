"""Independent exact Gram, event and partition verification. AuthorityEffect: None."""
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
import unittest
from unittest.mock import MagicMock, patch

from hypothesis import given, settings, strategies as st
import sympy as sp

CHECKS = Path(__file__).resolve().parents[1]
APP = CHECKS/"independent/ds-positive-form-controls.py"
sys.path.insert(0, str(CHECKS))
from checker_support.boundary import Violation, evaluate
from checker_support.cases import Cases
from checker_support.domains import Failure

PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)
DATA = st.lists(st.integers(-4, 4), min_size=16, max_size=16)
VECTOR = st.lists(st.integers(-3, 3), min_size=4, max_size=4)


def load() -> SimpleNamespace:
    return SimpleNamespace(**runpy.run_path(str(APP)))


def _rows(values: list[int], rows: int, columns: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(values[row*columns+column] for column in range(columns)) for row in range(rows))


def _partition(labels: list[int], size: int) -> tuple[tuple[int, ...], ...]:
    used = sorted(set(labels[:size]))
    return tuple(tuple(index for index in range(size) if labels[index] == label) for label in used)


def _selector(groups: tuple[tuple[int, ...], ...], size: int) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(size, len(groups), lambda row, column: int(row in groups[column]))


class PositiveFormTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object, kind: str = "input") -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("refusal lacks error")
        self.assertEqual(result.error.kind, kind)
        return result.error

    def test_oracles_and_import_lifecycle(self) -> None:
        self.assertEqual(_rows(list(range(16)), 2, 3), ((0, 1, 2), (3, 4, 5)))
        self.assertEqual(_partition([2, 1, 2, 0], 4), ((3,), (1,), (0, 2)))
        self.assertEqual(_selector(((0, 2), (1,)), 3), sp.ImmutableMatrix(((1, 0), (0, 1), (1, 0))))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            module = load()
        self.assertEqual(output.getvalue(), "")
        self.assertNotIn("checks", vars(module))

    @PROPERTY
    @given(DATA, st.integers(1, 4), st.integers(1, 4), st.integers(0, 5), VECTOR, VECTOR, st.integers(1, 7))
    def test_gram_bilinear_quadratic_and_normalized_weights(self, values: list[int], rows: int, columns: int, scale: int, first: list[int], second: list[int], denominator: int) -> None:
        module = load()
        data = _rows(values, rows, columns)
        form = module.IntegerGramForm(data, scale)
        matrix = sp.ImmutableMatrix(data)
        gram = scale*matrix.T*matrix
        left, right = sp.ImmutableMatrix(first[:columns]), sp.ImmutableMatrix(second[:columns])
        self.assertEqual(sp.ImmutableMatrix(form.gram().value), gram)
        self.assertEqual(form.bilinear(first[:columns], second[:columns]).value, (left.T*gram*right)[0])
        self.assertEqual(form.quadratic(first[:columns]).value, (left.T*gram*left)[0])
        self.assertGreaterEqual(form.quadratic(first[:columns]).value, 0)
        self.assertEqual(form.diagonal_weight(denominator).value, gram.trace()/denominator**2)
        event = tuple(index for index in range(columns) if first[index] >= 0)
        selector = sp.ImmutableMatrix([int(index in event) for index in range(columns)])
        expected = (selector.T*gram*selector)[0]/denominator**2
        self.assertEqual(form.event_weight(event, denominator).value, expected)
        self.assertEqual(form.event_weight(tuple(reversed(event)), denominator).value, expected)

    @PROPERTY
    @given(DATA, st.integers(1, 4), st.integers(1, 4), st.integers(0, 5), VECTOR, VECTOR)
    def test_coarse_graining_against_incidence_matrix(self, values: list[int], rows: int, columns: int, scale: int, labels: list[int], vector: list[int]) -> None:
        module = load()
        data = _rows(values, rows, columns)
        form = module.IntegerGramForm(data, scale)
        groups = _partition(labels, columns)
        selector = _selector(groups, columns)
        result = form.coarse_grained(groups)
        self.assertTrue(result.ok)
        coarse = result.value
        self.assertEqual(sp.ImmutableMatrix(coarse.features), sp.ImmutableMatrix(data)*selector)
        self.assertEqual(coarse.scale, scale)
        self.assertEqual(sp.ImmutableMatrix(coarse.gram().value), selector.T*sp.ImmutableMatrix(form.gram().value)*selector)
        values_coarse = vector[:len(groups)]
        lifted = tuple(int(value) for value in selector*sp.ImmutableMatrix(values_coarse))
        self.assertEqual(coarse.quadratic(values_coarse).value, form.quadratic(lifted).value)
        reversed_groups = tuple(tuple(reversed(group)) for group in groups)
        self.assertEqual(form.coarse_grained(reversed_groups).value.features, coarse.features)

    def test_fixed_nondiagonal_and_multifeature_examples(self) -> None:
        module = load()
        form = module.IntegerGramForm(((1, 2, -1), (3, -2, 4)), 2)
        expected = sp.ImmutableMatrix(((20, -8, 22), (-8, 16, -20), (22, -20, 34)))
        self.assertEqual(sp.ImmutableMatrix(form.gram().value), expected)
        self.assertEqual(form.bilinear((1, 0, 0), (0, 1, 0)).value, -8)
        self.assertTrue(form.bilinear((1, 0, 0), (0, 1, 0)).ok)
        self.assertEqual(form.quadratic((1, -1, 2)).value, 356)
        self.assertEqual(form.coarse_grained(((2, 0), (1,))).value.features, ((0, 2), (7, -2)))
        self.assertEqual(form.event_weight(()).value, 0)
        self.assertEqual(module.IntegerGramForm(((0, 0),), 0).event_weight((0, 1)).value, 0)

    def test_distinct_normalization_witnesses(self) -> None:
        module = load()
        first = module.IntegerGramForm(((1, 1),))
        second = module.IntegerGramForm(((3, 4),))
        self.assertEqual(first.diagonal_weight(2).value, Q(1, 2))
        self.assertEqual(first.event_weight((0, 1), 2).value, 1)
        self.assertEqual(first.event_weight((0,), 2).value, Q(1, 4))
        self.assertEqual(second.diagonal_weight(5).value, 1)
        self.assertEqual(second.event_weight((0, 1), 5).value, Q(49, 25))
        self.assertEqual(second.event_weight((0,), 5).value, Q(9, 25))
        self.assertEqual(second.event_weight((1,), 5).value, Q(16, 25))
        self.assertEqual(second.event_weight((0, 1), 5).value-second.diagonal_weight(5).value, Q(24, 25))
        self.assertEqual(first.coarse_grained(((0, 1),)).value.event_weight((0,), 2).value, 1)

    def test_input_shapes_scalars_and_full_budgets(self) -> None:
        module = load()
        for features in ((), ((),), ((1,), (1, 2)), ((True,),), ((1.0,),), ((Q(1),),), "features", None):
            self.refused(module.IntegerGramForm, features)
        for scale in (-1, True, 1.0, Q(1), "1", None):
            self.refused(module.IntegerGramForm, ((1,),), scale)
        self.refused(module.IntegerGramForm, ((1,),)*17, kind="resource")
        self.refused(module.IntegerGramForm, ((1,)*17,), kind="resource")
        data = tuple(tuple(int(row == column) for column in range(16)) for row in range(16))
        form = module.IntegerGramForm(data)
        self.assertEqual(form.dimension, 16)
        self.assertEqual(form.gram().value, data)
        self.assertEqual(form.quadratic((1,)*16).value, 16)
        self.assertEqual(form.event_weight(tuple(range(16))).value, 16)
        self.assertEqual(form.coarse_grained(tuple((i,) for i in range(16))).value.features, data)

    def test_vectors_events_and_denominator_refusals(self) -> None:
        module = load()
        form = module.IntegerGramForm(((1, -1),))
        for vector in ((), (1,), (1, 2, 3), (True, 0), (1.0, 0), (Q(1), 0), "12", None):
            self.assertEqual(form.quadratic(vector).error.kind, "input")
            self.assertEqual(form.bilinear((1, 0), vector).error.kind, "input")
            self.assertEqual(form.bilinear(vector, (1, 0)).error.kind, "input")
        for event in ((-1,), (2,), (True,), (1.0,), "0", None):
            self.assertEqual(form.event_weight(event).error.kind, "input")
        self.assertEqual(form.event_weight((0, 0)).error.kind, "duplicate")
        self.assertEqual(form.quadratic((1,)*17).error.kind, "resource")
        self.assertEqual(form.event_weight((0,)*17).error.kind, "resource")
        for denominator in (0, -1, True, 1.0, Q(1), "1", None):
            self.assertEqual(form.event_weight((), denominator).error.kind, "input")
            self.assertEqual(form.diagonal_weight(denominator).error.kind, "input")

    def test_partition_refusals_and_canonical_group_order(self) -> None:
        module = load()
        form = module.IntegerGramForm(((2, -1, 3),))
        for partition in ((), ((),), ((), (0, 1, 2)), ((0,),), ((0, 1),), ((0, 1), (3,)), "partition", None):
            self.assertEqual(form.coarse_grained(partition).error.kind, "input")
        for duplicate in (((0, 0), (1, 2)), ((0, 1), (1, 2))):
            self.assertEqual(form.coarse_grained(duplicate).error.kind, "duplicate")
        self.assertEqual(form._event((2, 0, 1)), (0, 1, 2))
        self.assertEqual(form.coarse_grained(((2, 0), (1,))).value.features, ((5, -1),))
        self.assertEqual(form.coarse_grained(((1,), (2, 0))).value.features, ((-1, 5),))

    def test_snapshot_ownership(self) -> None:
        module = load()
        row = [1, 2]
        rows = [row]
        form = module.IntegerGramForm(rows, 2)
        row[0] = 9
        rows.clear()
        self.assertEqual(form.features, ((1, 2),))
        with self.assertRaises(FrozenInstanceError):
            form.scale = 0
        groups = [[1, 0]]
        coarse = form.coarse_grained(groups).value
        groups[0].clear()
        self.assertEqual(coarse.features, ((3,),))
        self.assertEqual(coarse.scale, 2)
        self.assertEqual(form.features, ((1, 2),))

    def test_resource_boundaries_and_later_cancellation(self) -> None:
        module = load()
        self.refused(module.IntegerGramForm, ((2**4096,),), kind="resource")
        self.refused(module.IntegerGramForm, ((1,),), 2**4096, kind="resource")
        large = 2**4095
        form = module.IntegerGramForm(((large, large, -large),))
        self.assertEqual(form.bilinear((1, 1, 1), (0, 0, 0)).error.kind, "resource")
        self.assertEqual(form.bilinear((2, -2, 0), (0, 0, 0)).error.kind, "resource")
        product = module.IntegerGramForm(((-large, large),))
        self.assertEqual(product.bilinear((1, 2), (0, 0)).error.kind, "resource")
        self.assertEqual(form.coarse_grained(((0, 1, 2),)).error.kind, "resource")
        self.assertEqual(form.coarse_grained(((2, 1, 0),)).error.kind, "resource")
        scaled = module.IntegerGramForm(((1,),), large)
        self.assertEqual(scaled.gram().value, ((large,),))
        self.assertEqual(scaled.bilinear((2,), (1,)).error.kind, "resource")
        self.assertEqual(scaled.quadratic((2,)).error.kind, "resource")
        self.assertEqual(scaled.event_weight((), 2**2048).error.kind, "resource")
        norm = module.IntegerGramForm(((2**2047,),)*4, 0)
        self.assertEqual(norm.quadratic((1,)).error.kind, "resource")
        self.assertEqual(norm.diagonal_weight().error.kind, "resource")
        self.assertEqual(module.IntegerGramForm(((2,),), large).gram().error.kind, "resource")
        self.assertEqual(module.IntegerGramForm(((2,),), large).diagonal_weight().error.kind, "resource")

    def test_admission_precedes_dependent_arithmetic(self) -> None:
        module = load()
        form = module.IntegerGramForm(((1, 2),))
        with patch.object(module.IntegerGramForm, "_coordinates", side_effect=RuntimeError("must not project")):
            self.assertEqual(form.bilinear((1, 0), (True, 0)).error.kind, "input")
            self.assertEqual(form.event_weight((), 0).error.kind, "input")
        failing = MagicMock(side_effect=RuntimeError("must not aggregate"))
        with patch.dict(module.IntegerGramForm._coarse_grained.__globals__, {"_dot": failing}):
            self.assertEqual(form.coarse_grained(((0,),)).error.kind, "input")
            self.assertEqual(form.coarse_grained(((0,), (0, 1))).error.kind, "duplicate")
        failing.assert_not_called()

    def test_negative_pairing_and_nonnegative_products(self) -> None:
        module = load()
        vector = sp.ImmutableMatrix((1, -1))
        for scale in range(-8, 13):
            matrix = sp.ImmutableMatrix(((0, scale), (scale, 0)))
            self.assertEqual(module.off_diagonal_pairing(scale), (vector.T*matrix*vector)[0])
        self.assertEqual(module.nonnegative_product(0, 2**4095), 0)
        self.assertEqual(module.nonnegative_product(7, 9), 63)
        for value in (True, 1.0, Q(1), "1", None):
            self.refused(module.off_diagonal_pairing, value)
            self.refused(module.nonnegative_product, 0, value)
        self.refused(module.nonnegative_product, -1, 0)
        self.refused(module.nonnegative_product, 0, -1)
        self.refused(module.nonnegative_product, 0, 2**4096, kind="resource")
        self.refused(module.off_diagonal_pairing, 2**4095, kind="resource")

    def test_counts_faults_and_programming_error_lifecycle(self) -> None:
        module = load()
        for _ in range(2):
            cases = Cases()
            module.verify_positivity(cases)
            self.assertEqual(cases.checks, 619)
            module.verify_decoherence(cases)
            self.assertEqual(cases.checks, 4017)
        self.refused(module.verify_positivity, None)
        self.refused(module.verify_decoherence, None)
        with patch.object(module.IntegerGramForm, "_quadratic", return_value=-1):
            self.refused(module.verify_positivity, Cases(), kind="check")
        form = module.IntegerGramForm(((1,),))
        with patch.object(module.IntegerGramForm, "_coordinates", side_effect=RuntimeError("bug")):
            with self.assertRaises(RuntimeError):
                form.quadratic((1,))
        with patch.object(module.IntegerGramForm, "_gram", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                form.gram()

    def test_executable_receipt_and_failure_exit(self) -> None:
        flags = [] if __debug__ else ["-O"]
        result = subprocess.run([sys.executable, "-I", "-B", *flags, "-X", "utf8", str(APP)], capture_output=True,
                                text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        receipt = json.loads(result.stdout)
        self.assertEqual((receipt["status"], receipt["checks"], receipt["positivity"], receipt["decoherence"], receipt["born_boundary"]), ("passed", 6561, 619, 3398, 2544))
        with patch.object(Cases, "require", side_effect=Violation("check", "injected")), contextlib.redirect_stderr(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as failure:
                runpy.run_path(str(APP), run_name="__main__")
        self.assertEqual(failure.exception.code, 1)
        self.assertEqual(json.loads(output.getvalue())["kind"], "check")


    @PROPERTY
    @given(st.lists(st.integers(-8, 8), min_size=1, max_size=16), st.sampled_from((1, 2, 4)))
    def test_power_shares_against_symbolic_normalization(self, amplitudes: list[int], exponent: int) -> None:
        module = load()
        masses = sp.ImmutableMatrix(amplitudes).applyfunc(lambda value: value**exponent)
        total = sum(masses)
        result = module.power_shares(amplitudes, exponent)
        if total == 0:
            self.assertFalse(result.ok)
            self.assertEqual(result.error.kind, "input")
        else:
            self.assertTrue(result.ok)
            self.assertEqual(result.value, tuple(masses/total))
            self.assertEqual(sum(result.value), 1)
            self.assertTrue(all(type(value) is Q for value in result.value))
        amplitudes.clear()
        self.assertEqual(result.value, None if total == 0 else tuple(masses/total))

    @PROPERTY
    @given(st.integers(-20, 20), st.integers(-20, 20), st.integers(-20, 20), st.integers(-20, 20))
    def test_rotations_against_symbolic_matrix_and_complex_product(self, a: int, b: int, r: int, s: int) -> None:
        module = load()
        values, coefficients = [a, b], [r, s]
        result = module.rotation(values, coefficients)
        expected = sp.ImmutableMatrix(((r, -s), (s, r)))*sp.ImmutableMatrix((a, b))
        self.assertTrue(result.ok)
        self.assertEqual(result.value, tuple(expected))
        real, imaginary = sp.expand((a+sp.I*b)*(r+sp.I*s)).as_real_imag()
        self.assertEqual(result.value, (real, imaginary))
        self.assertEqual(sum(value*value for value in result.value), (a*a+b*b)*(r*r+s*s))
        self.assertTrue(all(type(value) is int for value in result.value))
        values.clear()
        coefficients.clear()
        self.assertEqual(result.value, tuple(expected))

    def test_fixed_shares_and_rotation_orientation(self) -> None:
        module = load()
        self.assertEqual(module.power_shares((3, 4), 1).value, (Q(3, 7), Q(4, 7)))
        self.assertEqual(module.power_shares((3, 4), 2).value, (Q(9, 25), Q(16, 25)))
        self.assertEqual(module.power_shares((3, 4), 4).value, (Q(81, 337), Q(256, 337)))
        self.assertEqual(module.power_shares((-3, 2), 1).value, (Q(3), Q(-2)))
        self.assertEqual(module.power_shares((0, 5), 2).value, (Q(0), Q(1)))
        self.assertEqual(module.power_shares((1,)*16, 4).value, (Q(1, 16),)*16)
        for pair, coefficients, expected in (((3, 4), (3, 4), (-7, 24)), ((2, -3), (-4, 5), (7, 22)), ((7, 9), (0, 0), (0, 0)), ((7, 9), (1, 0), (7, 9))):
            self.assertEqual(module.rotation(pair, coefficients).value, expected)

    def test_born_exact_domains_and_zero_totals(self) -> None:
        module = load()
        for value in (True, 1.0, Q(1), "1", None):
            self.assertEqual(module.power_shares((1, value), 2).error.kind, "input")
            self.assertEqual(module.power_shares((1, 2), value).error.kind, "input")
            self.assertEqual(module.rotation((1, value), (1, 0)).error.kind, "input")
            self.assertEqual(module.rotation((1, 0), (1, value)).error.kind, "input")
        for exponent in (-1, 0, 3, 5, 2**100):
            self.assertEqual(module.power_shares((1, 2), exponent).error.kind, "input")
        for values in ((), "12", None):
            self.assertEqual(module.power_shares(values, 2).error.kind, "input")
        for pair_shape in ((1,), (), "12", None):
            self.assertEqual(module.rotation(pair_shape, (1, 0)).error.kind, "input")
            self.assertEqual(module.rotation((1, 0), pair_shape).error.kind, "input")
        self.assertEqual(module.power_shares((1,)*17, 1).error.kind, "resource")
        self.assertEqual(module.rotation((1, 2, 3), (1, 0)).error.kind, "resource")
        self.assertEqual(module.rotation((1, 0), (1, 2, 3)).error.kind, "resource")
        for exponent in (1, 2, 4):
            self.assertEqual(module.power_shares((0, 0), exponent).error.kind, "input")
        self.assertEqual(module.power_shares((3, -3), 1).error.kind, "input")

    def test_born_full_arithmetic_budgets(self) -> None:
        module = load()
        large = 2**4095
        self.assertEqual(module.power_shares((large,), 1).value, (Q(1),))
        self.assertEqual(module.power_shares((2**2047,), 2).value, (Q(1),))
        self.assertEqual(module.power_shares((2**1023,), 4).value, (Q(1),))
        self.assertEqual(module.rotation((large, 0), (1, 0)).value, (large, 0))
        for amplitudes, exponent in (((2**4096,), 1), ((2**2048,), 2), ((2**1024,), 4), ((large, large, -large), 1), ((2**2047,)*4, 2)):
            self.assertEqual(module.power_shares(amplitudes, exponent).error.kind, "resource")
        self.assertEqual(module.rotation((2**4096, 0), (0, 0)).error.kind, "resource")
        self.assertEqual(module.rotation((0, 0), (2**4096, 0)).error.kind, "resource")
        self.assertEqual(module.rotation((large, large), (2, 2)).error.kind, "resource")
        self.assertEqual(module.rotation((large, large), (1, 1)).error.kind, "resource")

    def test_born_preflight_lifecycle_and_section_counts(self) -> None:
        module = load()
        failing = MagicMock(side_effect=RuntimeError("must not calculate"))
        with patch.dict(module._power_shares.__globals__, {"_masses": failing}):
            self.assertEqual(module.power_shares((1, True), 2).error.kind, "input")
            self.assertEqual(module.power_shares((1, 2), True).error.kind, "input")
            self.assertEqual(module.power_shares((1, 2), 3).error.kind, "input")
            self.assertEqual(module.power_shares((), 2).error.kind, "input")
        with patch.dict(module._rotation.__globals__, {"_dot": failing}):
            self.assertEqual(module.rotation((1, 0), (1, True)).error.kind, "input")
        failing.assert_not_called()
        for _ in range(2):
            cases = Cases()
            module.verify_born_boundary(cases)
            self.assertEqual(cases.checks, 2544)
        self.refused(module.verify_born_boundary, None)
        with patch.dict(module.verify_born_boundary.__globals__, {"_rotation": lambda *_: (0, 0)}):
            self.refused(module.verify_born_boundary, Cases(), kind="check")
        with patch.dict(module._power_shares.__globals__, {"_masses": failing}):
            with self.assertRaises(RuntimeError):
                module.power_shares((1, 2), 2)
        with patch.dict(module._rotation.__globals__, {"_dot": MagicMock(side_effect=KeyboardInterrupt)}):
            with self.assertRaises(KeyboardInterrupt):
                module.rotation((1, 2), (3, 4))


    def test_original_selection_witness_and_actual_guard_correspondence(self) -> None:
        module = load()
        calls: list[str] = []
        implementation = Cases.require
        def record(cases: Cases, condition: bool, label: str) -> None:
            calls.append(label)
            implementation(cases, condition, label)
        with patch.object(Cases, "require", record):
            cases = Cases()
            module.verify_selection_witness(cases)
        self.assertEqual(cases.checks, 11)
        self.assertEqual(len(calls), 11)
        self.assertEqual(len(set(calls)), 11)
        self.assertTrue(all(label.startswith("selection ") for label in calls))
        for amplitudes in ((1, 2), (1, 1)):
            for degree in (2, 4):
                symbolic = sp.ImmutableMatrix(amplitudes).applyfunc(lambda value: value**degree)
                self.assertEqual(module.power_shares(amplitudes, degree).value, tuple(symbolic/sum(symbolic)))
        self.refused(module.verify_selection_witness, None)
        with patch.dict(module.verify_selection_witness.__globals__, _power_shares=lambda *_: (Q(1, 2), Q(1, 2))):
            self.refused(module.verify_selection_witness, Cases(), kind="check")
        with patch.dict(module.verify_selection_witness.__globals__, _masses=MagicMock(side_effect=KeyboardInterrupt)):
            with self.assertRaises(KeyboardInterrupt):
                module.verify_selection_witness(Cases())


if __name__ == "__main__":
    unittest.main(verbosity=2)
