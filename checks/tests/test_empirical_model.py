"""Independent finite assignment and distribution tests. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import sys
from typing import TypeVar, cast
import unittest
from unittest.mock import MagicMock, patch

from hypothesis import given, settings, strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import evaluate
from checker_support.empirical_model import EmpiricalModel
from checker_support.measurement_scenario import MeasurementScenario, assignment, cochain, sections
from checker_support.outcome import Outcome

T = TypeVar("T")
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)


def binary_digits(number: int, size: int) -> tuple[int, ...]:
    return tuple((number >> index) & 1 for index in reversed(range(size)))


def parity(target: int) -> dict[tuple[int, ...], Q]:
    return {binary_digits(value, 2): Q(int((value//2+value % 2) % 2 == target), 2) for value in range(4)}


class EmpiricalModelTests(unittest.TestCase):
    def accepted(self, result: Outcome[T]) -> T:
        if result.error is not None:
            self.fail(str(result.error))
        return cast(T, result.value)

    def test_oracles_and_fixed_contextual_descent(self) -> None:
        self.assertEqual(binary_digits(5, 3), (1, 0, 1))
        self.assertEqual(binary_digits(6, 3), (1, 1, 0))
        self.assertEqual(parity(1), {(0, 0): Q(0), (0, 1): Q(1, 2), (1, 0): Q(1, 2), (1, 1): Q(0)})
        scenario = MeasurementScenario(4, ((0, 2), (0, 3), (1, 2), (1, 3)))
        pr = EmpiricalModel(scenario, [parity(value) for value in (0, 0, 0, 1)])
        uniform = EmpiricalModel(scenario, [{key: Q(1, 4) for key in parity(0)}]*4)
        self.assertEqual(self.accepted(pr.support_globals()), ())
        self.assertEqual(self.accepted(pr.matching_families(scenario.contexts)), (0, 0, 0, 0))
        self.assertEqual(self.accepted(uniform.matching_families(scenario.contexts)), (16, 16, 0, 0))
        globals_ = ((0, 0, 0, 0), (1, 0, 0, 1))
        tables = [{key: Q(sum(tuple(value[p] for p in context) == key for value in globals_), 2)
                   for key in sections(2)} for context in scenario.contexts]
        mixture = EmpiricalModel(scenario, tables)
        self.assertEqual(self.accepted(mixture.support_globals()), globals_)
        self.assertEqual(self.accepted(mixture.matching_families(((0, 1, 2), (1, 2, 3)))), (4, 2, 0, 2))

    @PROPERTY
    @given(st.lists(st.integers(0, 8), min_size=8, max_size=8), st.lists(st.integers(0, 8), min_size=8, max_size=8))
    def test_generated_marginals_incidence_and_mixtures(self, left: list[int], right: list[int]) -> None:
        scenario = MeasurementScenario(3, ((0, 1), (1, 2)))
        left[0] += 1
        right[0] += 1
        def tables(weights: list[int]) -> list[dict[tuple[int, ...], Q]]:
            total = sum(weights)
            return [{local: Q(sum(weight for index, weight in enumerate(weights)
                                 if tuple(binary_digits(index, 3)[p] for p in context) == local), total)
                     for local in sections(len(context))} for context in scenario.contexts]
        first, second = EmpiricalModel(scenario, tables(left)), EmpiricalModel(scenario, tables(right))
        mixture = self.accepted(first.mixture(second))
        for got, a, b in zip(mixture.stacked(), first.stacked(), second.stacked()):
            self.assertEqual(got, (a+b)/2)
        incidence = self.accepted(scenario.incidence())
        for row, (index, local) in zip(incidence, scenario.rows()):
            expected = tuple(Q(int(tuple(binary_digits(number, 3)[p] for p in scenario.contexts[index]) == local)) for number in range(8))
            self.assertEqual(row, expected)
        full = {binary_digits(number, 3): Q(weight, sum(left)) for number, weight in enumerate(left)}
        direct = self.accepted(scenario.marginal(full, (0, 1, 2), (1,)))
        middle = self.accepted(scenario.marginal(full, (0, 1, 2), (2, 1)))
        self.assertEqual(self.accepted(scenario.marginal(middle, (2, 1), (1,))), direct)
        self.assertEqual(self.accepted(scenario.marginal(full, (0, 1, 2), ())), {(): Q(1)})

    def test_all_small_parity_cycles_and_assignment_projection(self) -> None:
        for size in (3, 4, 5):
            contexts = tuple(tuple(sorted((i, (i+1) % size))) for i in range(size))
            scenario = MeasurementScenario(size, contexts)
            for target in product((0, 1), repeat=size):
                model = EmpiricalModel(scenario, [parity(bit) for bit in target])
                expected = tuple(binary_digits(number, size) for number in range(1 << size)
                                 if all((binary_digits(number, size)[i]+binary_digits(number, size)[(i+1) % size]) % 2 == bit for i, bit in enumerate(target)))
                self.assertEqual(self.accepted(model.support_globals()), expected)
                count = 2 if sum(target) % 2 == 0 else 0
                self.assertEqual(self.accepted(model.matching_families((tuple(range(size-1)), tuple(range(1, size))))), (2, count, 0, 2-count))
            for value in scenario.globals:
                self.assertEqual(self.accepted(scenario.restrict(value, (size-1, 0))), (value[-1], value[0]))

    def test_scenario_exact_domains_and_context_invariants(self) -> None:
        for size in (True, 1.0, "1", None, 0, -1, 7, 64):
            self.assertFalse(evaluate(MeasurementScenario, size, ((0,),)).ok)
        for contexts in ((), ((),), ((0, 0),), ((True,),), ((1.0,),), ((2,),), ((0,),), ((1, 0),), ((0, 1), (0, 1))):
            self.assertFalse(evaluate(MeasurementScenario, 2, contexts).ok)
        scenario = MeasurementScenario(2, ((0, 1),))
        for value in ((True, 0), (0, 2), (0,), "00", None):
            self.assertFalse(scenario.restrict(value, (0,)).ok)
        for positions in ((-1,), (2,), (True,), (0, 0), "0", None):
            self.assertFalse(scenario.sections(positions).ok)
            self.assertFalse(scenario.restrict((0, 0), positions).ok)
        self.assertEqual(self.accepted(scenario.sections(())), ((),))
        self.assertFalse(evaluate(sections, 7).ok)
        self.assertFalse(evaluate(assignment, (True,), 1).ok)

    def test_cochain_whole_shape_and_probability_refusals(self) -> None:
        scenario = MeasurementScenario(2, ((0,), (1,)))
        table = {(0,): Q(1), (1,): Q(0)}
        for value in ({}, {(0,): 1}, {(False,): 1, (1,): 0}, {(0,): 1, (1,): 0, (2,): 0}, {(0,): 1.0, (1,): 0}, {(0,): True, (1,): 0}, (), None):
            self.assertFalse(evaluate(cochain, value, 1).ok)
            self.assertFalse(scenario.marginal(value, (0,), ()).ok)
        for tables in ((), (table,), (table, table, table), ({(0,): Q(2), (1,): Q(-1)}, table), ({(0,): Q(0), (1,): Q(0)}, table)):
            self.assertFalse(evaluate(EmpiricalModel, scenario, tables).ok)
        self.assertFalse(evaluate(EmpiricalModel, None, (table,)).ok)
        model = EmpiricalModel(scenario, (table, table))
        self.assertFalse(model.mixture(None).ok)
        other = EmpiricalModel(MeasurementScenario(1, ((0,),)), (table,))
        self.assertFalse(model.mixture(other).ok)
        self.assertFalse(scenario.marginal(table, (0,), (1,)).ok)
        # Signed cochains are admitted independently of probability models.
        signed = {(0,): Q(-2), (1,): Q(3)}
        self.assertEqual(self.accepted(scenario.marginal(signed, (0,), ())), {(): Q(1)})

    def test_snapshot_ownership_and_detached_exports(self) -> None:
        context = [0]
        scenario = MeasurementScenario(1, [context])
        context.clear()
        table = {(0,): Q(1, 3), (1,): Q(2, 3)}
        model = EmpiricalModel(scenario, [table])
        table.clear()
        export = model.distributions()
        export[0].clear()
        self.assertEqual(model.weights, ((Q(1, 3), Q(2, 3)),))
        self.assertEqual(scenario.contexts, ((0,),))
        with self.assertRaises(FrozenInstanceError):
            scenario.n = 6  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            model.weights = ()  # type: ignore[misc]
        self.assertEqual(self.accepted(model.support_globals()), ((0,), (1,)))

    def test_incidence_family_and_rational_resource_boundaries(self) -> None:
        full = MeasurementScenario(6, (tuple(range(6)),))
        incidence = self.accepted(full.incidence())
        self.assertEqual(len(incidence), 64)
        self.assertEqual(incidence, tuple(tuple(Q(int(i == j)) for j in range(64)) for i in range(64)))
        excessive = MeasurementScenario(6, tuple(combinations(range(6), 3))[:16])
        with patch("checker_support.measurement_scenario.sections", side_effect=RuntimeError("must not enumerate")):
            self.assertEqual(excessive.incidence().error.kind, "resource")  # type: ignore[union-attr]
        scenario = MeasurementScenario(6, tuple((i,) for i in range(6)))
        model = EmpiricalModel(scenario, [{(0,): Q(1, 2), (1,): Q(1, 2)}]*6)
        failing = MagicMock(side_effect=RuntimeError("must not form candidates"))
        with patch("checker_support.empirical_model.product", failing):
            refusal = model.matching_families(tuple(combinations(range(6), 2)))
            self.assertEqual(refusal.error.kind if refusal.error else None, "resource")
        failing.assert_not_called()
        small = MeasurementScenario(2, ((0, 1),))
        large = Q(2**4095)
        values = dict(zip(sections(2), (large, large, -large, -large)))
        refused = small.marginal(values, (0, 1), ())
        self.assertEqual(refused.error.kind if refused.error else None, "resource")
        self.assertFalse(evaluate(cochain, {(0,): Q(1, 2**4096), (1,): Q(0)}, 1).ok)

    def test_cover_preflight_and_runtime_error_propagation(self) -> None:
        scenario = MeasurementScenario(2, ((0,), (1,)))
        model = EmpiricalModel(scenario, [{(0,): Q(1), (1,): Q(0)}]*2)
        with patch.object(EmpiricalModel, "_supports", side_effect=RuntimeError("must not inspect supports")):
            for cover in ((), ((),), ((0,),), ((0, 1), (1, 0)), ((0,), (2,)), "cover"):
                self.assertFalse(model.matching_families(cover).ok)
        with patch.object(EmpiricalModel, "_supports", side_effect=RuntimeError("bug")):
            with self.assertRaises(RuntimeError):
                model.support_globals()
        with patch.object(EmpiricalModel, "_supports", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                model.matching_families(((0,), (1,)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
