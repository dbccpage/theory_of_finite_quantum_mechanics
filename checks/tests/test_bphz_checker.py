"""Independent bounded forest, polynomial and commuting-projector verification.

AuthorityEffect: None. Finite oracles do not assert continuum convergence.
"""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
import io
from itertools import product
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

STEM = "dfm-bphz-continuum-fence"
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)
FRACTIONS = st.fractions(-9, 9, max_denominator=12)


def _flat(matrix: sp.Matrix) -> tuple[Q, Q, Q, Q]:
    a, b, c, d = matrix
    return Q(int(a.p), int(a.q)), Q(int(b.p), int(b.q)), Q(int(c.p), int(c.q)), Q(int(d.p), int(d.q))


class BphzCheckerTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object, kind: str = "input") -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("refusal lacks an error")
        self.assertEqual(result.error.kind, kind)
        return result.error

    def test_oracle_and_refusal_helper(self) -> None:
        self.assertEqual(_flat(sp.Matrix([[1, sp.Rational(2, 3)], [-4, 5]])), (Q(1), Q(2, 3), Q(-4), Q(5)))
        with self.assertRaises(AssertionError):
            self.refused(lambda: None)

    @PROPERTY
    @given(st.lists(st.integers(0, 15), max_size=5))
    def test_forests_against_bitmask_oracle(self, masks: list[int]) -> None:
        module = load(STEM)
        names = tuple(str(index) for index in range(len(masks)))
        edges = {name: frozenset(bit for bit in range(4) if mask & (1 << bit)) for name, mask in zip(names, masks)}
        expected = set()
        for selection in range(1 << len(masks)):
            chosen = [index for index in range(len(masks)) if selection & (1 << index)]
            conflict = any((masks[a] & masks[b]) not in (0, masks[a], masks[b]) for a in chosen for b in chosen)
            if not conflict:
                expected.add(tuple(names[index] for index in chosen))
        self.assertEqual(set(module.forests(names, edges)), expected)
        self.assertEqual(len(list(module.powerset(names))), 1 << len(masks))

    def test_forest_snapshots_and_full_budget(self) -> None:
        module = load(STEM)
        edges = {"a": frozenset({1}), "b": frozenset({1, 2})}
        predicate = module.compatible(edges)
        edges["b"] = frozenset({2})
        edges.clear()
        self.assertTrue(predicate("a", "b"))
        self.refused(predicate, "a", "missing")
        self.refused(predicate, None, "a")
        names = [str(i) for i in range(12)]
        subsets = module.powerset(names)
        names.clear()
        self.assertEqual(len(list(subsets)), 4096)
        full_names = tuple(str(i) for i in range(12))
        self.assertEqual(len(module.forests(full_names, {name: frozenset(range(64)) for name in full_names})), 4096)
        self.assertEqual(module.forests((), {}), [()])

    def test_forest_domains_and_unused_entries(self) -> None:
        module = load(STEM)
        for names in (None, "a", ("a", "a"), (None,), (True,), ("",), (" ",)):
            self.refused(module.powerset, names)
        self.refused(module.powerset, tuple(str(i) for i in range(13)), kind="resource")
        self.refused(module.powerset, ("x"*65,), kind="resource")
        invalid_edges: tuple[object, ...] = (None, [], {"a": set()}, {True: frozenset()}, {"a": frozenset({True})},
                                           {"a": frozenset({-1})}, {"a": frozenset({"1"})})
        for edges in invalid_edges:
            self.refused(module.forests, (), edges)
        for edges in ({"a": frozenset({4096})}, {"a": frozenset(range(65))},
                      {str(i): frozenset() for i in range(13)}):
            self.refused(module.forests, (), edges, kind="resource")
        self.refused(module.forests, ("missing",), {})
        self.refused(module.forests, (), {"unused": None})

    @PROPERTY
    @given(FRACTIONS, FRACTIONS)
    def test_numerator_and_sector_exact_oracles(self, x: Q, y: Q) -> None:
        module = load(STEM)
        a, b = sp.symbols("a b")
        polynomial = 2+3*a+5*b+7*a*b
        expected = polynomial.subs({a: sp.Rational(x.numerator, x.denominator), b: sp.Rational(y.numerator, y.denominator)})
        self.assertEqual(module.N(x, y), Q(int(expected.p), int(expected.q)))
        self.assertEqual(module.six(x, y), 7*x*y)
        self.assertEqual(module.inclusion(x, y), 7*x*y)
        if y not in (0, -1):
            # Partial fractions, independent of the implementation's combined ratio.
            self.assertEqual(module.sector_k(x, y), 1/y+(x-1)/(1+y))

    def test_scalar_domains_and_derived_budgets(self) -> None:
        module = load(STEM)
        for value in (True, 0.5, "1", None):
            for operation in (module.N, module.six, module.inclusion, module.sector_k):
                self.refused(operation, value, 1)
                self.refused(operation, 1, value)
            self.refused(module.exact, value)
        for pole in (0, -1):
            self.refused(module.sector_k, 3, pole)
        self.refused(module.exact, 1 << 4096, kind="resource")
        self.assertEqual(module.exact(Q(1, 1 << 4095)), Q(1, 1 << 4095))
        for operation in (module.N, module.six, module.inclusion):
            self.refused(operation, 1 << 4095, 1, kind="resource")
        self.refused(module.sector_k, 0, Q(1, 1 << 4095), kind="resource")

    @PROPERTY
    @given(st.lists(FRACTIONS, min_size=8, max_size=8))
    def test_matrix_operations_against_symbolic_oracle(self, values: list[Q]) -> None:
        module = load(STEM)
        a, b = values[:4], values[4:]
        self.assertEqual(module.multiply(a, b), _flat(sp.Matrix(2, 2, a)*sp.Matrix(2, 2, b)))
        self.assertEqual(module.residual(a), _flat(sp.eye(2)-sp.Matrix(2, 2, a)))
        self.assertEqual(module.multiply(a, module.IDENTITY), tuple(a))
        self.assertEqual(module.multiply(module.IDENTITY, a), tuple(a))

    @PROPERTY
    @given(st.integers(-5, 5), st.integers(-5, 5), st.lists(st.tuples(st.booleans(), st.booleans()), max_size=8), FRACTIONS, FRACTIONS)
    def test_projector_reduction_and_joint_kernel(self, r: int, s: int, diagonal: list[tuple[bool, bool]], x: Q, y: Q) -> None:
        module = load(STEM)
        basis = sp.Matrix([[1, r], [s, 1+r*s]])
        inverse = basis.inv()
        matrices = [basis*sp.diag(int(a), int(b))*inverse for a, b in diagonal]
        family = tuple(_flat(matrix) for matrix in matrices)
        expected = basis*sp.diag(int(all(not a for a, _ in diagonal)), int(all(not b for _, b in diagonal)))*inverse
        aggregate = module.CommutingProjectorFamily(family)
        reduction = aggregate.reduction()
        self.assertTrue(reduction.ok)
        self.assertEqual(reduction.value.flat2(), _flat(expected))
        self.assertEqual(module.checked_reduce(family), _flat(expected))
        self.assertEqual(module.checked_reduce(family+family), _flat(expected))
        self.assertEqual(module.checked_reduce(tuple(reversed(family))), _flat(expected))
        vector = sp.Matrix([x, y])
        result = aggregate.apply((x, y))
        self.assertTrue(result.ok)
        image = expected*vector
        self.assertEqual(result.value, tuple(Q(int(v.p), int(v.q)) for v in image))
        self.assertEqual(result.value == (x, y), all(matrix*vector == sp.zeros(2, 1) for matrix in matrices))
        module.check_family(family)

    def test_projector_snapshots_maximum_and_empty(self) -> None:
        module = load(STEM)
        row = [Q(1), Q(2, 3), Q(0), Q(0)]
        family = [row]
        aggregate = module.CommutingProjectorFamily(family)
        row[0] = Q(9)
        family.clear()
        self.assertEqual(aggregate.reduction().value.flat2(), (Q(0), Q(-2, 3), Q(0), Q(1)))
        with self.assertRaises(FrozenInstanceError):
            aggregate.projectors = ()
        full = (module.ZERO,)*64
        self.assertEqual(module.checked_reduce(full), module.IDENTITY)
        module.check_family(full)
        self.assertEqual(module.CommutingProjectorFamily(()).apply((2, 3)).value, (Q(2), Q(3)))
        self.refused(module.checked_reduce, full+(module.ZERO,), kind="resource")

    def test_projector_domains_and_conservative_product_budget(self) -> None:
        module = load(STEM)
        for family in (None, "", (None,), ((Q(0),)*3,), ((Q(0),)*5,), ((0, 0, 0, 0),),
                       ((True, Q(0), Q(0), Q(0)),), ((Q(2), Q(0), Q(0), Q(0)),),
                       ((Q(1), Q(0), Q(0), Q(0)), (Q(1), Q(1), Q(0), Q(0)))):
            self.refused(module.checked_reduce, family)
        self.refused(module.checked_reduce, ((Q(1 << 4096), Q(0), Q(0), Q(0)),), kind="resource")
        huge = Q(1 << 2048)
        # This is mathematically idempotent, but products exceed the admitted bit budget.
        self.refused(module.checked_reduce, ((huge, 1-huge, huge, 1-huge),), kind="resource")
        for matrix in (None, (1, 2, 3), (True, 0, 0, 1), (0.5, 0, 0, 1)):
            self.refused(module.multiply, matrix, module.IDENTITY)
            self.refused(module.multiply, module.IDENTITY, matrix)
            self.refused(module.residual, matrix)
        aggregate = module.CommutingProjectorFamily(())
        for vector in (None, (), (1,), (1, 2, 3), (True, 1), (0.5, 1)):
            result = aggregate.apply(vector)
            self.assertFalse(result.ok)
            self.assertEqual(result.error.kind, "input")

    def test_fixture_counts_numerator_challenge_and_cli(self) -> None:
        module = load(STEM)
        cases = Cases()
        counts = []
        with contextlib.redirect_stdout(io.StringIO()):
            for check in (module.check_forest_carriers, module.check_numerator_examples, module.check_sector_example,
                          module.check_projector_api, module.check_invalid_scalars):
                check(cases)
                counts.append(cases.checks)
        self.assertEqual(counts, [5, 131, 133, 570, 575])
        for _ in range(2):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(cli(module.main), 0)
            self.assertIn("12 exact idempotents; 77 compatible lists", output.getvalue())
            receipt = json.loads(output.getvalue()[output.getvalue().index("{"):])
            self.assertEqual(receipt["checks"], 575)
        with patch.object(module, "N", return_value=Q(0)):
            self.refused(module.check_numerator_examples, kind="check")
        with patch.object(module, "six", return_value=Q(99)):
            self.refused(module.check_numerator_examples, kind="check")
        with patch.object(module, "forests", return_value=[]):
            self.refused(module.check_forest_carriers, kind="check")
        with patch.object(module, "sector_k", return_value=Q(0)):
            self.refused(module.check_sector_example, kind="check")

    def test_recorders_railway_and_cancellation(self) -> None:
        module = load(STEM)
        for check in (module.check_forest_carriers, module.check_numerator_examples, module.check_sector_example,
                      module.check_projector_api, module.check_invalid_scalars):
            self.refused(check, object())
        self.refused(module.check_family, (), object())
        aggregate = module.CommutingProjectorFamily(())
        with patch.object(module.CommutingProjectorFamily, "_reduction", side_effect=OSError("injected")):
            self.assertEqual(aggregate.reduction().error.kind, "resource")
            self.assertEqual(aggregate.apply((1, 2)).error.kind, "resource")
        with patch.object(module.CommutingProjectorFamily, "_reduction", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                aggregate.reduction()
        errors = io.StringIO()
        with patch.object(module, "check_forest_carriers", side_effect=OSError("injected")):
            with contextlib.redirect_stderr(errors):
                self.assertEqual(cli(module.main), 1)
        self.assertEqual(json.loads(errors.getvalue())["kind"], "resource")
        with patch.object(module, "check_forest_carriers", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                cli(module.main)


if __name__ == "__main__":
    unittest.main(verbosity=2)
