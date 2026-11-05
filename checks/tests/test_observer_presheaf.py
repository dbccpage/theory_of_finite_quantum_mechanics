"""Finite observer checker integration and independent oracles. AuthorityEffect: None."""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from fractions import Fraction as Q
from itertools import combinations, product
import io
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
APP = CHECKS/"independent/foc035_observer_presheaf.py"
sys.path.insert(0, str(CHECKS))
from checker_support.boundary import Violation, evaluate
from checker_support.cases import Cases

PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)


def load() -> SimpleNamespace:
    return SimpleNamespace(**runpy.run_path(str(APP)))


def is_forest(edges: tuple[tuple[int, int], ...], size: int) -> bool:
    components = [{index} for index in range(size)]
    for first, second in edges:
        left = next(component for component in components if first in component)
        right = next(component for component in components if second in component)
        if left is right:
            return False
        components.remove(left)
        components.remove(right)
        components.append(left | right)
    return True


class ObserverPresheafTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object) -> None:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)

    def test_import_oracles_and_per_run_recorder(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as output:
            module = load()
        self.assertEqual(output.getvalue(), "")
        self.assertNotIn("CHECKED", vars(module))
        self.assertTrue(is_forest(((0, 1), (1, 2)), 3))
        self.assertFalse(is_forest(((0, 1), (1, 2), (0, 2)), 3))
        first, second = Cases(), Cases()
        with contextlib.redirect_stdout(io.StringIO()):
            module._ok(first, "first", True)
            module._ok(second, "second", True)
        self.assertEqual((first.checks, second.checks), (1, 1))
        self.refused(module._ok, None, "bad", True)
        self.refused(module._ok, Cases(), "bad", 1)

    def test_legacy_lp_adapter_and_probability_input_refusals(self) -> None:
        module = load()
        self.assertEqual(module.verify_lp((Q(1, 2),), ((1,),), (1,), (1,), (Q(1, 2),)), Q(1, 2))
        self.assertEqual(module.simplex_min((1,), ((1,),), (2,)), ([Q(2)], [Q(1)]))
        self.assertIsNone(module.simplex_min((1,), ((0,),), (1,)))
        self.refused(module.simplex_min, (-1,), ((0,),), (0,))
        for value in (True, 0.1, "0", None, -1, 2):
            self.refused(module.noisy_pr, value)
        for value in (True, 1.0, -1, 2, "0", None):
            self.refused(module.parity_dist, value)
        self.refused(module.simplex_min, (0.1,), ((1,),), (1,))
        self.refused(module.verify_lp, (1,), ((1,),), (1,), (0,), (0,))
        self.refused(module.mixture, module.pr_box(), module.pr_box()[:1])
        self.refused(module.point_mass, module.BELL, (0, 0, True, 0))
        self.refused(module.point_mass, None, (0,))

    def test_bell_ncf_distance_and_signed_section_oracles(self) -> None:
        module = load()
        for noise, fraction, distance in ((Q(0), Q(0), Q(2)), (Q(1, 4), Q(1, 2), Q(1)), (Q(1, 2), Q(1), Q(0)), (Q(1), Q(1), Q(0))):
            model = module.noisy_pr(noise)
            self.assertEqual(module.ncf(module.BELL, model), fraction)
            self.assertEqual(module.l1_defect(module.BELL, model), distance)
        model = module.EmpiricalModel(module.BELL, module.pr_box())
        signed = module._signed_section(model)
        matrix = sp.ImmutableMatrix(module.BELL._incidence())
        self.assertEqual(matrix*sp.ImmutableMatrix(signed), sp.ImmutableMatrix(model.stacked()))
        self.assertEqual(sum(signed), 1)
        self.assertLess(min(signed), 0)
        self.assertTrue(module.check_functoriality())

    @PROPERTY
    @given(st.lists(st.integers(0, 8), min_size=4, max_size=4))
    def test_generated_single_context_models_are_noncontextual(self, weights: list[int]) -> None:
        module = load()
        weights[0] += 1
        distribution = dict(zip(product((0, 1), repeat=2), (Q(value, sum(weights)) for value in weights)))
        scenario = module.Scenario(2, ((0, 1),))
        self.assertEqual(module.ncf(scenario, [distribution]), 1)
        self.assertEqual(module.l1_defect(scenario, [distribution]), 0)

    def test_gyo_exhaustive_graph_oracle_and_domains(self) -> None:
        module = load()
        all_edges = tuple(combinations(range(4), 2))
        for mask in range(1 << len(all_edges)):
            edges = tuple(edge for index, edge in enumerate(all_edges) if mask & (1 << index))
            self.assertEqual(module.gyo(edges), is_forest(edges, 4))
        self.assertTrue(module.gyo([{"a", "b"}, {"b", "c"}]))
        self.assertTrue(module.gyo([(), (0, 1), (0, 1)]))
        for malformed_edges in (None, "edges", ((True,),), ((1.0,),), ((-1,),), ((64,),), (("",),), (("a"*65,),), ((0, 0),), ((None,),)):
            self.refused(module.gyo, malformed_edges)
        self.refused(module.gyo, [(index,) for index in range(17)])
        self.refused(module.gyo, [set(range(17))])

    @PROPERTY
    @given(st.lists(st.integers(0, 8), min_size=8, max_size=8))
    def test_path_gluing_against_independent_marginals(self, weights: list[int]) -> None:
        module = load()
        weights[0] += 1
        assignments = tuple(product((0, 1), repeat=3))
        total = sum(weights)
        first = {(a, b): Q(sum(weight for key, weight in zip(assignments, weights) if key[:2] == (a, b)), total) for a, b in product((0, 1), repeat=2)}
        second = {(b, c): Q(sum(weight for key, weight in zip(assignments, weights) if key[1:] == (b, c)), total) for b, c in product((0, 1), repeat=2)}
        joint = module._glue_pair(first, second)
        self.assertEqual(sum(joint.values()), 1)
        self.assertGreaterEqual(min(joint.values()), 0)
        for key, expected in first.items():
            self.assertEqual(sum(value for assignment, value in joint.items() if assignment[:2] == key), expected)
        for key, expected in second.items():
            self.assertEqual(sum(value for assignment, value in joint.items() if assignment[1:] == key), expected)

    def test_gluing_zero_overlap_mismatch_and_lp_size_preflight(self) -> None:
        module = load()
        left = {(0, 0): Q(1), (0, 1): Q(0), (1, 0): Q(0), (1, 1): Q(0)}
        right = {(0, 0): Q(0), (0, 1): Q(1), (1, 0): Q(0), (1, 1): Q(0)}
        joint = module._glue_pair(left, right)
        self.assertEqual(joint[(0, 0, 1)], 1)
        self.assertEqual(sum(joint.values()), 1)
        incompatible = {(0, 0): Q(0), (0, 1): Q(0), (1, 0): Q(1), (1, 1): Q(0)}
        self.refused(module._glue_pair, left, incompatible)
        scenario = module.Scenario(6, tuple((i,) for i in range(6)))
        distributions = [{(0,): Q(1, 2), (1,): Q(1, 2)}]*6
        with patch.object(module.Scenario, "_incidence", side_effect=RuntimeError("must not allocate")):
            self.refused(module.ncf, scenario, distributions)
            self.refused(module.l1_defect, scenario, distributions)
            self.refused(module._signed_section, module.EmpiricalModel(scenario, distributions))

    def test_executable_groups_and_failure_exit(self) -> None:
        flags = [] if __debug__ else ["-O"]
        result = subprocess.run([sys.executable, "-I", "-B", *flags, "-X", "utf8", str(APP)], capture_output=True, text=True, encoding="utf-8", timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(sum(line.startswith("ok  ") for line in result.stdout.splitlines()), 50)
        self.assertTrue(result.stdout.endswith("50 checks passed\n"))
        with patch.object(Cases, "require", side_effect=Violation("check", "injected")), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as failure:
                runpy.run_path(str(APP), run_name="__main__")
        self.assertEqual(failure.exception.code, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
