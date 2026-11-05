"""Independent finite Gaussian rephasing and counting verification.

AuthorityEffect: None. No unitary mixing matrix or measured phase is inferred.
"""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from hypothesis import given, settings, strategies as st
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_review_repairs import load
from checker_support.boundary import cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import Failure
from checker_support.gaussian_rational import GaussianRational as GR

STEM = "dfm-ckm-physics-fence"
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)
FRACTIONS = st.fractions(-5, 5, max_denominator=6)
LABELS: st.SearchStrategy[tuple[Q, Q]] = st.tuples(FRACTIONS, FRACTIONS).filter(lambda value: value != (Q(0), Q(0)))


def _complex(value: GR) -> sp.Expr:
    return sp.Rational(value.re.numerator, value.re.denominator)+sp.I*sp.Rational(value.im.numerator, value.im.denominator)


def _components(value: sp.Expr) -> tuple[Q, Q]:
    re, im = sp.expand_complex(value).as_real_imag()
    return Q(int(re.p), int(re.q)), Q(int(im.p), int(im.q))


def _related(left: tuple[tuple[GR, ...], ...], right: tuple[tuple[GR, ...], ...]) -> bool:
    """Solve row0=1, then every column and row, then verify all edge equations."""
    cols = [sp.cancel(_complex(a)/_complex(b)) for a, b in zip(left[0], right[0])]
    rows = [sp.cancel(_complex(b[0])*cols[0]/_complex(a[0])) for a, b in zip(left, right)]
    return all(sp.cancel(rows[i]*_complex(value)-cols[j]*_complex(right[i][j])) == 0
               for i, row in enumerate(left) for j, value in enumerate(row))


class CkmCheckerTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object, kind: str = "input") -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("refusal lacks an error")
        self.assertEqual(result.error.kind, kind)
        return result.error

    def test_oracles_and_refusal_helper(self) -> None:
        self.assertEqual(_components(_complex(GR(Q(2, 3), Q(-4, 7)))), (Q(2, 3), Q(-4, 7)))
        one, two = GR(1), GR(2)
        self.assertTrue(_related(((one,),), ((two,),)))
        self.assertFalse(_related(((one, one), (one, one)), ((one, one), (one, two))))
        with self.assertRaises(AssertionError):
            self.refused(lambda: None)

    @PROPERTY
    @given(FRACTIONS)
    def test_counting_against_polynomial_oracles(self, n: Q) -> None:
        module = load(STEM)
        self.assertEqual(module.cycle_count(n), n*n-2*n+1)
        self.assertEqual(module.constraint_count(n), (n*n-n)/2)
        self.assertEqual(module.cp_count(n), (n*n-3*n+2)/2)
        self.assertEqual(module.cycle_count(n)-module.constraint_count(n), module.cp_count(n))

    @PROPERTY
    @given(st.lists(st.tuples(FRACTIONS, FRACTIONS), min_size=4, max_size=4))
    def test_quartets_against_complex_oracle(self, parts: list[tuple[Q, Q]]) -> None:
        module = load(STEM)
        labels = [GR(*pair) for pair in parts]
        a, b, c, d = [_complex(value) for value in labels]
        expected = _components(a*b*sp.conjugate(c)*sp.conjugate(d))
        value = module.quartet(*labels)
        self.assertEqual((value.re, value.im), expected)

    def test_scalar_and_quartet_boundaries(self) -> None:
        module = load(STEM)
        for operation in (module.exact_rational, module.cycle_count, module.constraint_count, module.cp_count):
            for value in (True, 0.5, "1", None):
                self.refused(operation, value)
            self.refused(operation, 1 << 4096, kind="resource")
        for operation in (module.cycle_count, module.constraint_count, module.cp_count):
            self.refused(operation, 1 << 4095, kind="resource")
        for index in range(4):
            for invalid in (None, 1, True, 0.5, (1, 2)):
                labels: list[object] = [GR(1)]*4
                labels[index] = invalid
                self.refused(module.quartet, *labels)
        self.assertEqual(module.quartet(GR(0), GR(1), GR(1), GR(1)), GR(0))
        self.refused(module.quartet, GR(1 << 4095), GR(2), GR(1), GR(1), kind="resource")

    @PROPERTY
    @given(st.lists(LABELS, min_size=10, max_size=10))
    def test_gaussian_table_action_and_normalization_oracle(self, parts: list[tuple[Q, Q]]) -> None:
        module = load(STEM)
        values = tuple(GR(*pair) for pair in parts)
        table = (values[:3], values[3:6])
        rows, cols = values[6:8], (values[8], values[9], GR(1))
        owned = module.GaussianRephasingTable(table)
        action = owned.act(rows, cols)
        self.assertTrue(action.ok)
        other = action.value.cells
        expected = tuple(tuple(GR(*_components(_complex(rows[i])*_complex(value)/_complex(cols[j])))
                               for j, value in enumerate(row)) for i, row in enumerate(table))
        self.assertEqual(other, expected)
        self.assertEqual(module.act(table, rows, cols), expected)
        normalized = owned.normalized()
        self.assertTrue(normalized.ok)
        norm = normalized.value.cells
        expected_norm = tuple(tuple(GR(*_components(_complex(value)*_complex(table[0][0])/
                                                  (_complex(row[0])*_complex(table[0][j]))))
                                   for j, value in enumerate(row)) for row in table)
        self.assertEqual(norm, expected_norm)
        self.assertEqual(module.normalize(table), norm)
        self.assertEqual(module.normalize(other), norm)
        self.assertEqual(module.normalize(norm), norm)
        self.assertEqual(norm[0], (GR(1),)*3)
        self.assertEqual(tuple(row[0] for row in norm), (GR(1),)*2)

    @PROPERTY
    @given(st.lists(LABELS, min_size=8, max_size=8))
    def test_witness_against_independent_gauge_equations(self, parts: list[tuple[Q, Q]]) -> None:
        module = load(STEM)
        values = tuple(GR(*pair) for pair in parts)
        left = (values[:2], values[2:4])
        right = (values[4:6], values[6:8])
        decision = _related(left, right)
        witness = module.witness(left, right)
        self.assertEqual(witness is not None, decision)
        if witness is not None:
            self.assertEqual(module.act(left, *witness), right)
        rows, cols = values[4:6], values[6:8]
        changed = module.act(left, rows, cols)
        self.assertTrue(_related(left, changed))
        result = module.GaussianRephasingTable(left).witness(module.GaussianRephasingTable(changed))
        self.assertTrue(result.ok)
        self.assertIsNotNone(result.value)
        self.assertEqual(module.act(left, *result.value), changed)
        separated = (changed[0], (changed[1][0], changed[1][1].mul(GR(2))))
        no_match = module.GaussianRephasingTable(left).witness(module.GaussianRephasingTable(separated))
        self.assertTrue(no_match.ok)
        self.assertIsNone(no_match.value)
        self.assertFalse(_related(left, separated))

    def test_table_snapshots_singletons_and_maximum(self) -> None:
        module = load(STEM)
        matrix = [[GR(1), GR(2)], [GR(3), GR(4)]]
        owned = module.GaussianRephasingTable(matrix)
        matrix[0][0] = GR(0)
        matrix[1].clear()
        matrix.clear()
        self.assertEqual(owned.cells, ((GR(1), GR(2)), (GR(3), GR(4))))
        with self.assertRaises(FrozenInstanceError):
            owned.cells = ()
        full = tuple((GR(1),)*64 for _ in range(64))
        self.assertEqual(module.shape(full), (64, 64))
        for table in (((GR(2),),), ((GR(2), GR(3)),), ((GR(2),), (GR(3),))):
            self.assertTrue(all(value == GR(1) for row in module.normalize(table) for value in row))
            self.assertIsNotNone(module.witness(table, module.normalize(table)))

    def test_nonreal_fixed_normalization_action_and_witness(self) -> None:
        module = load(STEM)
        table = ((GR(1, 1), GR(2, -1), GR(3, 2)), (GR(2, 3), GR(4, -1), GR(-1, 2)))
        rows, cols = (GR(2, -1), GR(-1, 3)), (GR(1, 2), GR(2, 1), GR(-3, 2))
        expected = tuple(tuple(GR(*_components(_complex(rows[i])*_complex(value)/_complex(cols[j])))
                               for j, value in enumerate(row)) for i, row in enumerate(table))
        norm = tuple(tuple(GR(*_components(_complex(value)*_complex(table[0][0])/
                                         (_complex(row[0])*_complex(table[0][j]))))
                          for j, value in enumerate(row)) for row in table)
        self.assertEqual(module.normalize(table), norm)
        self.assertEqual(module.act(table, rows, cols), expected)
        certificate = module.witness(table, expected)
        self.assertIsNotNone(certificate)
        self.assertEqual(module.act(table, *certificate), expected)
        self.assertTrue(_related(table, expected))
        separated = (expected[0], (expected[1][0], expected[1][1].mul(GR(2)), expected[1][2]))
        self.assertIsNone(module.witness(table, separated))
        self.assertFalse(_related(table, separated))

    def test_table_gauge_and_witness_domains(self) -> None:
        module = load(STEM)
        valid = ((GR(1),),)
        for table in (None, "", (), ((),), ((GR(1),), (GR(1), GR(1))), ((GR(0),),), ((1,),), ((True,),)):
            for operation in (module.shape, module.normalize):
                self.refused(operation, table)
            self.refused(module.act, table, (GR(1),), (GR(1),))
            self.refused(module.witness, valid, table)
            self.refused(module.witness, table, valid)
        for oversized_table in ((valid[0],)*65, ((GR(1),)*65,)):
            self.refused(module.shape, oversized_table, kind="resource")
        for gauge in (None, "", (), (GR(1), GR(1)), (GR(0),), (True,), (1,)):
            self.refused(module.act, valid, gauge, (GR(1),))
            self.refused(module.act, valid, (GR(1),), gauge)
        self.refused(module.witness, valid, ((GR(1), GR(1)),))
        owned = module.GaussianRephasingTable(valid)
        for right in (None, valid, module.GaussianRephasingTable(((GR(1), GR(1)),))):
            result = owned.witness(right)
            self.assertFalse(result.ok)
            self.assertEqual(result.error.kind, "input")

    def test_table_arithmetic_resource_failure(self) -> None:
        module = load(STEM)
        huge = GR(1 << 4095)
        owned = module.GaussianRephasingTable(((huge,),))
        # Conservative operation budgets may refuse even a final cancellable identity.
        self.assertEqual(owned.normalized().error.kind, "resource")
        self.assertEqual(owned.act((GR(2),), (GR(1),)).error.kind, "resource")
        self.assertEqual(owned.witness(owned).error.kind, "resource")
        self.refused(module.normalize, ((huge,),), kind="resource")
        self.refused(module.act, ((huge,),), (GR(2),), (GR(1),), kind="resource")

    def test_sign_census_and_enumeration_preflight(self) -> None:
        module = load(STEM)
        for height, width in ((1, 1), (1, 6), (2, 3), (3, 2), (6, 1)):
            tables = module.sign_tables(height, width)
            self.assertEqual(len(tables), 2**(height*width))
            self.assertEqual(len(set(tables)), len(tables))
            self.assertTrue(all(module.shape(table) == (height, width) for table in tables))
        for dimensions in ((0, 1), (True, 1), (1, 0), (1, False)):
            self.refused(module.sign_tables, *dimensions)
        for dimensions in ((7, 1), (1, 7), (3, 3)):
            self.refused(module.sign_tables, *dimensions, kind="resource")
        self.refused(module.check_sign_actions, ((GR(1),),), 1, 2)
        self.refused(module.check_sign_actions, ((GR(1 << 4095),),), 1, 2)
        with patch.object(module, "product", side_effect=AssertionError("enumeration started")):
            self.refused(module.check_sign_actions, ((GR(1),),), 10**9, 1, kind="resource")
        self.assertEqual(module.check_sign_actions(((GR(1),),), 1, 1), 4)

    def test_failed_refusal_is_a_failed_check(self) -> None:
        module = load(STEM)
        with patch.object(module, "exact_rational", return_value=Q(1)):
            self.refused(module.check_invalid_inputs, kind="check")
        cases = Cases()
        module.check_invalid_inputs(cases)
        self.assertEqual(cases.checks, 11)
        errors = io.StringIO()
        with patch.object(module, "exact_rational", return_value=Q(1)):
            with contextlib.redirect_stderr(errors):
                self.assertEqual(cli(module.check_invalid_inputs), 1)
        self.assertEqual(json.loads(errors.getvalue())["kind"], "check")

    def test_default_counts_and_fixed_faults(self) -> None:
        module = load(STEM)
        cases = Cases()
        with contextlib.redirect_stdout(io.StringIO()):
            module.check_counting_examples(cases)
            self.assertEqual(cases.checks, 28)
            module.check_quartet_examples(cases)
            self.assertEqual(cases.checks, 31)
            module.check_rephasing(cases)
            self.assertEqual(cases.checks, 11370)
            module.check_invalid_inputs(cases)
        self.assertEqual(cases.checks, 11381)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(cli(module.main), 0)
        self.assertIn("2376 sign actions, 4388 pair decisions; orbits [1, 1, 1, 2, 4]", output.getvalue())
        receipt = json.loads(output.getvalue()[output.getvalue().index("{"):])
        self.assertEqual(receipt["checks"], 11381)
        with patch.object(module, "cp_count", return_value=Q(99)):
            self.refused(module.check_counting_examples, kind="check")
        with patch.object(module, "quartet", return_value=GR(0)):
            self.refused(module.check_quartet_examples, kind="check")
        with patch.object(module, "witness", return_value=None):
            self.refused(module.check_nonreal, kind="check")

    def test_recorders_failure_and_cancellation(self) -> None:
        module = load(STEM)
        for check in (module.check_rephasing, module.check_invalid_inputs, module.check_counting_examples,
                      module.check_quartet_examples, module.check_nonreal):
            self.refused(check, object())
        one = ((GR(1),),)
        for operation, args in ((module.check_canonical, (one,)), (module.check_pair, (one, one)),
                                (module.check_sign_actions, (one, 1, 1))):
            self.refused(operation, *args, object())
        owned = module.GaussianRephasingTable(one)
        for method, operation, call_args in (("_normalized", owned.normalized, ()), ("_act", owned.act, ((GR(1),), (GR(1),))),
                                        ("_witness", owned.witness, (owned,))):
            with patch.object(module.GaussianRephasingTable, method, side_effect=OSError("injected")):
                self.assertEqual(operation(*call_args).error.kind, "resource")
            with patch.object(module.GaussianRephasingTable, method, side_effect=KeyboardInterrupt):
                with self.assertRaises(KeyboardInterrupt):
                    operation(*call_args)
        errors = io.StringIO()
        with patch.object(module, "check_counting_examples", side_effect=OSError("injected")):
            with contextlib.redirect_stderr(errors):
                self.assertEqual(cli(module.main), 1)
        self.assertEqual(json.loads(errors.getvalue())["kind"], "resource")


if __name__ == "__main__":
    unittest.main(verbosity=2)
