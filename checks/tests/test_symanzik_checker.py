"""Independent graph, determinant and cotree-boundary verification. AuthorityEffect: None."""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from dataclasses import FrozenInstanceError
import io
import json
import math
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
APP = CHECKS/"independent/dfm-symanzik-qed-ae-fence.py"
sys.path.insert(0, str(CHECKS))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import Failure

Edge = tuple[int, int]
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)
EDGE_LIST = st.lists(st.tuples(st.integers(0, 4), st.integers(0, 4)), max_size=7)


def load() -> SimpleNamespace:
    return SimpleNamespace(**runpy.run_path(str(APP)))


def _components(count: int, edges: list[Edge], mask: int) -> int:
    adjacent: list[set[int]] = [set() for _ in range(count)]
    for index, (first, second) in enumerate(edges):
        if mask & (1 << index):
            adjacent[first].add(second)
            adjacent[second].add(first)
    remaining = set(range(count))
    result = 0
    while remaining:
        pending = [remaining.pop()]
        result += 1
        while pending:
            new = adjacent[pending.pop()] & remaining
            remaining.difference_update(new)
            pending.extend(new)
    return result


def _determinant_sum(count: int, edges: list[Edge], weights: list[int]) -> int:
    incidence = sp.zeros(count, len(edges))
    for index, (first, second) in enumerate(edges):
        incidence[first, index] += 1
        incidence[second, index] -= 1
    reduced = incidence[:-1, :]
    conductance = sp.diag(*(sp.Rational(1, weight) for weight in weights))
    return int(math.prod(weights)*(reduced*conductance*reduced.T).det())


class SymanzikCheckerTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object, kind: str = "input") -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("refusal lacks error")
        self.assertEqual(result.error.kind, kind)
        return result.error

    def test_oracles_and_import_lifecycle(self) -> None:
        self.assertEqual(_components(4, [(0, 1), (2, 3)], 3), 2)
        self.assertEqual(_determinant_sum(2, [(0, 1), (0, 1), (0, 0)], [2, 3, 5]), 25)
        self.assertEqual(_determinant_sum(1, [], []), 1)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            load()
        self.assertEqual(output.getvalue(), "")
        with self.assertRaises(AssertionError):
            self.refused(lambda: None)

    def test_supplied_graph_all_masks_and_individual_products(self) -> None:
        module = load()
        graph = module.CotreeGraph(4, module.EDGES)
        for mask in range(32):
            self.assertEqual(graph.components(mask).value, _components(4, list(module.EDGES), mask))
            self.assertEqual(module.run(mask), _components(4, list(module.EDGES), mask))
            product = math.prod(weight for index, weight in enumerate(module.WEIGHTS) if index not in [i for i in range(5) if mask & (1 << i)])
            self.assertEqual(graph.cotree_product(mask, module.WEIGHTS).value, product)
            self.assertEqual(module.prod(mask, module.WEIGHTS), product)
        self.assertEqual(graph.tree_masks().value, (7, 11, 13, 14, 21, 22, 25, 26))
        self.assertEqual(graph.cotree_sum(module.WEIGHTS).value, 247)
        self.assertEqual(graph.cotree_sum((1,)*5).value, 8)
        self.assertEqual(_determinant_sum(4, list(module.EDGES), list(module.WEIGHTS)), 247)

    @PROPERTY
    @given(st.integers(1, 5), EDGE_LIST)
    def test_generated_connectivity_and_spanning_trees(self, count: int, raw_edges: list[Edge]) -> None:
        module = load()
        edges = [(first % count, second % count) for first, second in raw_edges]
        graph = module.CotreeGraph(count, edges)
        expected = []
        for mask in range(1 << len(edges)):
            components = _components(count, edges, mask)
            self.assertEqual(graph.components(mask).value, components)
            if len([i for i in range(len(edges)) if mask & (1 << i)]) == count-1 and components == 1:
                expected.append(mask)
        self.assertEqual(graph.tree_masks().value, tuple(expected))
        self.assertEqual(graph.cotree_sum((1,)*len(edges)).value, len(expected))

    @PROPERTY
    @given(st.integers(1, 5), EDGE_LIST, st.lists(st.integers(1, 7), min_size=7, max_size=7))
    def test_cotree_polynomial_against_laplacian_determinant(self, count: int, raw_edges: list[Edge], values: list[int]) -> None:
        module = load()
        edges = [(first % count, second % count) for first, second in raw_edges]
        weights = values[:len(edges)]
        result = module.CotreeGraph(count, edges).cotree_sum(weights)
        self.assertTrue(result.ok)
        self.assertEqual(result.value, _determinant_sum(count, edges, weights))

    def test_parallel_edges_loops_zeros_signs_and_empty_products(self) -> None:
        module = load()
        graph = module.CotreeGraph(2, ((0, 1), (1, 0), (0, 0)))
        self.assertEqual(graph.tree_masks().value, (1, 2))
        self.assertEqual(graph.cotree_sum((2, 3, 5)).value, 25)
        self.assertEqual(graph.cotree_sum((-2, 3, -5)).value, -5)
        self.assertEqual(graph.cotree_sum((0, 3, 5)).value, 15)
        self.assertEqual(graph.cotree_sum((2, 3, 0)).value, 0)
        self.assertEqual(graph.cotree_product(7, (2, 3, 5)).value, 1)
        singleton = module.CotreeGraph(1, ())
        self.assertEqual(singleton.components(0).value, 1)
        self.assertEqual(singleton.tree_masks().value, (0,))
        self.assertEqual(singleton.cotree_sum(()).value, 1)
        self.assertEqual(module.CotreeGraph(4, ()).cotree_sum(()).value, 0)
        self.assertEqual(module.CotreeGraph(1, ((0, 0),)).cotree_sum((7,)).value, 7)

    def test_constructor_domains_and_full_size_boundaries(self) -> None:
        module = load()
        for count in (True, False, 0, -1, 1.0, "4", None):
            self.refused(module.CotreeGraph, count, ())
        self.refused(module.CotreeGraph, 17, (), kind="resource")
        for edges in (None, "edges", ((0,),), ((0, 1, 2),), ((True, 1),), ((0, 1.0),), ((-1, 0),), ((0, 4),)):
            self.refused(module.CotreeGraph, 4, edges)
        self.refused(module.CotreeGraph, 2, ((0, 1),)*13, kind="resource")
        full = module.CotreeGraph(16, ((0, 1),)*12)
        self.assertEqual(full.components(4095).value, 15)
        self.assertEqual(full.tree_masks().value, ())
        self.assertEqual(module.CotreeGraph(2, ((0, 1),)*12).tree_masks().value, tuple(1 << i for i in range(12)))
        self.assertEqual(module.CotreeGraph(1, ((0, 0),)*12).cotree_sum((1,)*12).value, 1)

    def test_mask_and_weight_refusals(self) -> None:
        module = load()
        graph = module.CotreeGraph(4, module.EDGES)
        for mask in (True, False, -1, 32, 2**4096, 1.0, None):
            self.assertFalse(graph.components(mask).ok)
            self.assertFalse(graph.cotree_product(mask, module.WEIGHTS).ok)
            self.refused(module.run, mask)
            self.refused(module.prod, mask, module.WEIGHTS)
        for weights in ((), (2, 3), (1,)*6, (True, 3, 5, 7, 11), (2, 3.0, 5, 7, 11), "23571", None):
            self.assertFalse(graph.cotree_product(31, weights).ok)
            self.assertFalse(graph.cotree_sum(weights).ok)
            self.refused(module.prod, 31, weights)
        self.assertEqual(graph.cotree_sum((1,)*13).error.kind, "resource")

    def test_owned_graph_snapshot(self) -> None:
        module = load()
        first = [0, 1]
        edges = [first, [1, 2]]
        graph = module.CotreeGraph(3, edges)
        first[0] = 2
        edges.clear()
        self.assertEqual(graph.edges, ((0, 1), (1, 2)))
        self.assertEqual(graph.tree_masks().value, (3,))
        self.assertEqual(graph.components(1).value, 2)
        with self.assertRaises(FrozenInstanceError):
            graph.vertex_count = 1
        weights = [2, 3]
        result = graph.cotree_product(1, weights)
        weights.clear()
        self.assertEqual(result.value, 3)

    def test_input_product_and_sum_budgets_before_cancellation(self) -> None:
        module = load()
        singleton = module.CotreeGraph(1, ((0, 0),)*3)
        self.assertEqual(singleton.cotree_product(0, (2**4095, 1, 1)).value, 2**4095)
        self.assertEqual(singleton.cotree_product(7, (2**4096, 1, 1)).error.kind, "resource")
        self.assertEqual(singleton.cotree_product(0, (2**4095, 2, 0)).error.kind, "resource")
        self.assertEqual(singleton.cotree_product(0, (-2**4096, 0, 0)).error.kind, "resource")
        graph = module.CotreeGraph(2, ((0, 1),)*4)
        large = 2**1365
        weights = (large, large, -large, -large)
        products = [math.prod(weights[j] for j in range(4) if i != j) for i in range(4)]
        self.assertTrue(all(value.bit_length() == 4096 for value in products))
        self.assertEqual(sum(products), 0)
        self.assertEqual(graph.cotree_sum(weights).error.kind, "resource")

    def test_preflight_admits_every_weight_before_enumeration(self) -> None:
        module = load()
        graph = module.CotreeGraph(4, ((0, 1),))
        with patch.object(module.CotreeGraph, "_trees", side_effect=RuntimeError("must not enumerate")):
            self.assertEqual(graph.cotree_sum((True,)).error.kind, "input")
        with patch.object(module.CotreeGraph, "_product", side_effect=RuntimeError("must not multiply")):
            self.assertEqual(graph.cotree_product(1, (True,)).error.kind, "input")
        self.assertEqual(graph.cotree_sum((0,)).value, 0)

    def test_counts_faults_cancellation_and_programming_errors(self) -> None:
        module = load()
        cases = Cases()
        module.verify(cases)
        self.assertEqual(cases.checks, 22)
        self.refused(module.verify, None)
        with patch.object(module.CotreeGraph, "_components", return_value=4):
            self.refused(module.verify, Cases(), kind="check")
        with patch.object(module.CotreeGraph, "_trees", side_effect=RuntimeError("bug")):
            with self.assertRaises(RuntimeError):
                module.CotreeGraph(1, ()).tree_masks()
        with patch.object(module.CotreeGraph, "_product", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                cli(module.main)

    def test_executable_receipt_and_failure_exit(self) -> None:
        flags = [] if __debug__ else ["-O"]
        result = subprocess.run([sys.executable, "-I", "-B", *flags, "-X", "utf8", str(APP)],
                                capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        receipt = json.loads(result.stdout)
        self.assertEqual((receipt["status"], receipt["checks"], receipt["cotree_sum"], receipt["unit_sum"]), ("passed", 22, 247, 8))
        self.assertEqual(receipt["trees"], [7, 11, 13, 14, 21, 22, 25, 26])
        with patch.object(Cases, "require", side_effect=Violation("check", "injected")), contextlib.redirect_stderr(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as failure:
                runpy.run_path(str(APP), run_name="__main__")
        self.assertEqual(failure.exception.code, 1)
        self.assertEqual(json.loads(output.getvalue())["kind"], "check")


if __name__ == "__main__":
    unittest.main(verbosity=2)
