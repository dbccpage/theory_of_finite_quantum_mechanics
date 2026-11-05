"""Independent finite-clock action and packed-matrix verification. AuthorityEffect: None."""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
from itertools import permutations
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
APP = CHECKS/"independent/dfm-relational-time-fence.py"
sys.path.insert(0, str(CHECKS))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import Failure
from checker_support.rational_matrix import RationalMatrix

Perm = tuple[int, int, int]
UNIT: Perm = (0, 1, 2)
PERMS: tuple[Perm, ...] = tuple((a, b, c) for a, b, c in permutations(range(3)))
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)


def load() -> SimpleNamespace:
    return SimpleNamespace(**runpy.run_path(str(APP)))


def _inverse(value: Perm) -> Perm:
    table = {image: source for source, image in enumerate(value)}
    return table[0], table[1], table[2]


def _frames(links: list[Perm]) -> tuple[Perm, ...]:
    images = [0, 1, 2]
    result = [UNIT]
    for link in links:
        images = [link[state] for state in images]
        result.append((images[0], images[1], images[2]))
    return tuple(result)


class RelationalTimeTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object, kind: str = "input") -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("refusal lacks error")
        self.assertEqual(result.error.kind, kind)
        return result.error

    def test_oracles_and_import_lifecycle(self) -> None:
        self.assertEqual(_inverse((1, 2, 0)), (2, 0, 1))
        self.assertEqual(_frames([(1, 0, 2), (0, 2, 1)]), (UNIT, (1, 0, 2), (2, 0, 1)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            load()
        self.assertEqual(output.getvalue(), "")
        with self.assertRaises(AssertionError):
            self.refused(lambda: None)

    def test_full_s3_census_and_exact_domains(self) -> None:
        module = load()
        for first in PERMS:
            self.assertEqual(module.inverse(first), _inverse(first))
            for second in PERMS:
                expected = tuple(first[state] for state in second)
                self.assertEqual(module.compose(first, second), expected)
        for bad in ((0, 1), (0, 1, 2, 3), (0, 0, 2), (True, 0, 2), (0, 1.0, 2), "012", None):
            self.refused(module.inverse, bad)
            self.refused(module.compose, bad, UNIT)
            self.refused(module.compose, UNIT, bad)
            self.refused(module.PermutationSchedule, (bad,))

    @PROPERTY
    @given(st.lists(st.sampled_from(PERMS), max_size=8))
    def test_frames_seams_closure_and_histories(self, links: list[Perm]) -> None:
        module = load()
        schedule = module.PermutationSchedule(links)
        expected = _frames(links)
        self.assertEqual(schedule.frame_values, expected)
        self.assertEqual(module.frames(links), expected)
        for initial in range(3):
            self.assertEqual(schedule.history(initial).value, tuple(frame[initial] for frame in expected))
            self.assertTrue(schedule.evolves(schedule.history(initial).value).value)
        if not links:
            self.assertEqual(schedule.closed().error.message, "emptyPeriod")
            self.assertEqual(schedule.blocks().error.message, "emptyPeriod")
            self.assertEqual(module.closure(links), "emptyPeriod")
            return
        self.assertEqual(schedule.blocks().value, (UNIT,)*(len(links)-1)+(expected[-1],))
        tag = "ok" if expected[-1] == UNIT else "nontrivialHolonomy"
        self.assertEqual(module.closure(links), tag)
        result = schedule.closed()
        self.assertEqual(result.ok, expected[-1] == UNIT)
        if result.ok:
            self.assertIs(result.value, schedule)
        else:
            self.assertEqual(result.error.message, "nontrivialHolonomy")

    @PROPERTY
    @given(st.lists(st.sampled_from(PERMS), max_size=8),
           st.lists(st.sampled_from(PERMS), min_size=9, max_size=9),
           st.lists(st.integers(0, 2), min_size=9, max_size=9))
    def test_endpoint_gauges_preserve_arbitrary_history_evolution(self, links: list[Perm], supplied_gauges: list[Perm], supplied_states: list[int]) -> None:
        module = load()
        schedule = module.PermutationSchedule(links)
        gauges, history = supplied_gauges[:len(links)+1], supplied_states[:len(links)+1]
        expected_links = [tuple(_inverse(gauges[t+1])[link[gauges[t][state]]] for state in range(3)) for t, link in enumerate(links)]
        changed = schedule.changed(gauges)
        self.assertTrue(changed.ok)
        self.assertEqual(changed.value.links, tuple(expected_links))
        coords = schedule.coordinates(history, gauges)
        self.assertTrue(coords.ok)
        self.assertEqual(coords.value, tuple(_inverse(gauge)[state] for gauge, state in zip(gauges, history)))
        self.assertEqual(tuple(gauge[state] for gauge, state in zip(gauges, coords.value)), tuple(history))
        evolves = all(history[t+1] == link[history[t]] for t, link in enumerate(links))
        self.assertEqual(schedule.evolves(history).value, evolves)
        self.assertEqual(changed.value.evolves(coords.value).value, evolves)
        stationary = schedule.coordinates(history, schedule.frame_values).value
        self.assertEqual(all(a == b for a, b in zip(stationary, stationary[1:])), evolves)

    def test_noninvolutive_endpoint_fixture(self) -> None:
        module = load()
        links = [(1, 2, 0), (1, 0, 2)]
        gauges = [(2, 0, 1), (0, 2, 1), (1, 2, 0)]
        schedule = module.PermutationSchedule(links)
        changed = schedule.changed(gauges).value
        for t, frame in enumerate(_frames(links)):
            expected = tuple(_inverse(gauges[t])[frame[gauges[0][state]]] for state in range(3))
            self.assertEqual(changed.frame_values[t], expected)
        self.assertEqual(schedule.blocks().value[-1], (0, 2, 1))
        self.assertEqual(schedule.closed().error.message, "nontrivialHolonomy")
        run = Cases()
        module.gauge_regression(links, gauges, run)
        self.assertEqual(run.checks, 15)

    def test_noninvolutive_evolution_direction(self) -> None:
        module = load()
        schedule = module.PermutationSchedule(((1, 2, 0),))
        for initial in range(3):
            self.assertTrue(schedule.evolves((initial, (initial+1) % 3)).value)
            self.assertFalse(schedule.evolves((initial, (initial+2) % 3)).value)
        self.assertEqual(schedule.blocks().value, ((1, 2, 0),))

    def test_snapshot_ownership_and_all_railway_refusals(self) -> None:
        module = load()
        link = [1, 0, 2]
        links = [link]
        schedule = module.PermutationSchedule(links)
        link[0] = 0
        links.clear()
        self.assertEqual(schedule.links, ((1, 0, 2),))
        self.assertEqual(schedule.frame_values, (UNIT, (1, 0, 2)))
        with self.assertRaises(FrozenInstanceError):
            schedule.links = ()
        for initial in (True, False, -1, 3, 1.0, None):
            outcome = schedule.history(initial)
            self.assertFalse(outcome.ok)
            self.assertEqual(outcome.error.kind, "input")
        for history in ((), (0,), (0, 1, 2), (True, 1), (0, 3), "01"):
            self.assertFalse(schedule.evolves(history).ok)
            self.assertFalse(schedule.coordinates(history, (UNIT, UNIT)).ok)
        for gauges in ((), (UNIT,), (UNIT, UNIT, UNIT), ((0, 0, 2), UNIT), "gauges"):
            self.assertFalse(schedule.changed(gauges).ok)
            self.assertFalse(schedule.coordinates((0, 1), gauges).ok)
        self.assertFalse(schedule.evolves((0, 0)).value)
        self.assertTrue(schedule.evolves((0, 1)).value)
        self.assertTrue(module.PermutationSchedule((UNIT,)).closed().ok)

    def test_empty_boundary_and_full_period_budget(self) -> None:
        module = load()
        empty = module.PermutationSchedule(())
        self.assertEqual(empty.frame_values, (UNIT,))
        self.assertEqual(empty.history(2).value, (2,))
        self.assertTrue(empty.evolves((2,)).value)
        self.assertTrue(empty.changed((UNIT,)).ok)
        self.assertFalse(empty.closed().ok)
        self.assertFalse(empty.blocks().ok)
        self.refused(module.cycle_regression, (), Cases())
        self.refused(module.gauge_regression, (), (UNIT,), Cases())
        full = module.PermutationSchedule((UNIT,)*64)
        self.assertEqual(len(full.frame_values), 65)
        self.assertEqual(full.blocks().value, (UNIT,)*64)
        self.assertTrue(full.closed().ok)
        self.assertEqual(full.history(1).value, (1,)*65)
        self.assertTrue(full.changed((UNIT,)*65).ok)
        self.assertEqual(full.coordinates((1,)*65, (UNIT,)*65).value, (1,)*65)
        self.refused(module.PermutationSchedule, (UNIT,)*65, kind="resource")
        self.assertEqual(full.changed((UNIT,)*66).error.kind, "resource")
        self.assertEqual(full.evolves((1,)*66).error.kind, "resource")

    def test_matrix_vector_operations_against_symbolic_oracle(self) -> None:
        module = load()
        left = ((Q(1, 2), -2, 3), (4, 0, Q(1, 3)))
        right = ((1, 2), (-1, 3), (2, 0))
        vector = (Q(2, 3), -1, 2)
        expected = sp.ImmutableMatrix(left)*sp.ImmutableMatrix(right)
        self.assertEqual(sp.ImmutableMatrix(module.mul(left, right)), expected)
        self.assertEqual(sp.ImmutableMatrix(module.transp(left)), sp.ImmutableMatrix(left).T)
        self.assertEqual(sp.ImmutableMatrix(module.apply(left, vector)), sp.ImmutableMatrix(left)*sp.ImmutableMatrix(vector))
        rows = [list(row) for row in left]
        snapshot = module.mat(rows)
        rows[0][0] = Q(9)
        self.assertEqual(snapshot, tuple(tuple(row) for row in left))
        self.assertEqual(snapshot[0][0], Q(1, 2))
        for bad in ((), ((1, 0), (1,)), ((True,),), ((1.0,),), "matrix"):
            self.refused(module.mat, bad)
            self.refused(module.mul, bad, ((1,),))
            self.refused(module.transp, bad)
        for invalid_vector in ((), (True, -1, 2), (1.0, -1, 2), (1, 2), "123"):
            self.refused(module.apply, left, invalid_vector)
        self.refused(module.mul, left, ((1,),))
        self.refused(module.apply, ((2**4095,),), (2,), kind="resource")
        self.refused(module.mat, ((1,),)*65, kind="resource")

    def test_packed_clock_and_fixed_control_counts(self) -> None:
        module = load()
        identity = module.mat(((1, 0), (0, 1)))
        step = module.mat(((0, -1), (1, 0)))
        symbolic = sp.ImmutableMatrix(step)
        powers = tuple(module.mat(tuple(tuple(Q(value) for value in row) for row in (symbolic**t).tolist())) for t in range(5))
        packed, shift = module._packed_product(powers, step, identity)
        clock = sp.zeros(4)
        for t in range(4):
            clock[(t+1) % 4, t] = 1
        expected = sp.kronecker_product(clock, sp.eye(2))
        self.assertEqual(sp.ImmutableMatrix(packed), expected)
        self.assertEqual(sp.ImmutableMatrix(shift), expected)
        run = Cases()
        module.matrix_regression(run)
        self.assertEqual(run.checks, 15)
        module.fault_regression(run)
        self.assertEqual(run.checks, 19)
        for length in range(1, 5):
            section = Cases()
            module.cycle_regression((UNIT,)*length, section)
            self.assertEqual(section.checks, 16*length+163)

    def test_guard_faults_and_cancellation(self) -> None:
        module = load()
        self.refused(module.matrix_regression, None)
        self.refused(module.cycle_regression, (UNIT,), None)
        self.refused(module.gauge_regression, (UNIT,), (UNIT, UNIT), None)
        self.refused(module.fault_regression, None)
        with patch.object(RationalMatrix, "mul", return_value=RationalMatrix.eye(2)):
            self.refused(module.matrix_regression, Cases(), kind="check")
        with patch.object(RationalMatrix, "mul", side_effect=RuntimeError("bug")):
            with self.assertRaises(RuntimeError):
                cli(module.main)
        with patch.object(RationalMatrix, "mul", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                cli(module.main)

    def test_full_enumeration_and_executable_failure_exit(self) -> None:
        flags = [] if __debug__ else ["-O"]
        result = subprocess.run([sys.executable, "-I", "-B", *flags, "-X", "utf8", str(APP)], capture_output=True,
                                text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        receipt = json.loads(result.stdout)
        self.assertEqual((receipt["status"], receipt["checks"]), ("passed", 347936))
        self.assertEqual((receipt["schedules"], receipt["closed"], receipt["nonclosing"]), (1554, 259, 1295))
        with patch.object(Cases, "require", side_effect=Violation("check", "injected")), contextlib.redirect_stderr(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as failure:
                runpy.run_path(str(APP), run_name="__main__")
        self.assertEqual(failure.exception.code, 1)
        self.assertEqual(json.loads(output.getvalue())["kind"], "check")


if __name__ == "__main__":
    unittest.main(verbosity=2)
