"""Independent finite SL2 transport, ownership and dependency verification.

AuthorityEffect: None. No continuum statement follows from these finite tests.
"""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from dataclasses import FrozenInstanceError
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

STEM = "dfm-continuum-interface"
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)
WORD = st.lists(st.tuples(st.sampled_from(("x", "y")), st.sampled_from((-1, 1))), max_size=8)


def _shears(a: int, b: int) -> sp.Matrix:
    return sp.ImmutableMatrix([[1, a], [0, 1]])*sp.ImmutableMatrix([[1, 0], [b, 1]])


def _oracle(labels: dict[str, sp.Matrix], path: tuple[tuple[str, int], ...]) -> sp.Matrix:
    """Right-multiply reversed factors with independent symbolic inversion."""
    factors = [labels[edge]**sign for edge, sign in path]
    result = sp.eye(2)
    for factor in reversed(factors):
        result = result*factor
    return result


class ContinuumInterfaceTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object, kind: str = "input") -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("refusal lacks an error")
        self.assertEqual(result.error.kind, kind)
        return result.error

    def test_oracle_and_refusal_helper(self) -> None:
        x, y = _shears(1, 0), _shears(0, 1)
        self.assertEqual(_oracle({"x": x, "y": y}, (("x", 1), ("y", 1))), sp.Matrix([[1, 1], [1, 2]]))
        self.assertEqual(_oracle({"x": x}, (("x", -1),)), sp.Matrix([[1, -1], [0, 1]]))
        self.assertEqual(_oracle({}, ()), sp.eye(2))
        with self.assertRaises(AssertionError):
            self.refused(lambda: None)

    @PROPERTY
    @given(st.integers(-8, 8), st.integers(-8, 8), WORD, WORD)
    def test_signed_transport_group_and_footprint_oracle(self, a: int, b: int, first: list[tuple[str, int]], second: list[tuple[str, int]]) -> None:
        module = load(STEM)
        labels = {"x": _shears(a, b), "y": _shears(b, a), "outside": sp.eye(2)}
        path, tail = tuple(first), tuple(second)
        expected = _oracle(labels, path)
        self.assertEqual(module.path_transport(labels, path), expected)
        owned = module.SL2Connection(labels)
        result = owned.path(path)
        self.assertTrue(result.ok)
        self.assertEqual(sp.Matrix(result.value.integer_rows()), expected)
        reverse = tuple((edge, -sign) for edge, sign in reversed(path))
        self.assertEqual(module.path_transport(labels, reverse), expected.inv())
        self.assertEqual(module.path_transport(labels, path+tail), _oracle(labels, tail)*expected)
        self.assertEqual(module.footprint(path), {edge for edge, _ in path})
        changed = dict(labels)
        changed["outside"] = _shears(7, 3)
        self.assertEqual(module.path_transport(changed, path), expected)

    @PROPERTY
    @given(st.lists(st.integers(-5, 5), min_size=8, max_size=8))
    def test_fixed_graph_dressing_and_tree_walk_oracle(self, values: list[int]) -> None:
        module = load(STEM)
        matrices = [_shears(values[2*i], values[2*i+1]) for i in range(4)]
        labels = dict(zip(("eRP", "ePA", "eRB", "eAB"), matrices))
        x, y, z, w = matrices
        expected = z.inv()*w*y*x
        self.assertEqual(module.dress(labels, "eAB"), expected)
        self.assertEqual(module.formula(labels), expected)
        owned = module.SL2Connection(labels)
        self.assertEqual(sp.Matrix(owned.dress("eAB").value.integer_rows()), expected)
        for edge in ("eRP", "ePA", "eRB"):
            self.assertEqual(module.dress(labels, edge), sp.eye(2))
        paths = ((), ("eRP",), ("ePA",), ("eRB",), ("eAB",), ("eRP", "ePA"), ("ePA", "eAB"), ("eRP", "ePA", "eAB"))
        for path in paths:
            expected_path = _oracle(labels, tuple((edge, 1) for edge in path))
            self.assertEqual(module.transport(labels, path), expected_path)
            self.assertEqual(sp.Matrix(owned.tree(path).value.integer_rows()), expected_path)

    @PROPERTY
    @given(st.lists(st.integers(-1000, 1000), min_size=4, max_size=4))
    def test_additive_specialization(self, values: list[int]) -> None:
        module = load(STEM)
        rp, pa, rb, ab = values
        self.assertEqual(module.additive_dress(*values), sum((rp, pa, ab))-rb)
        labels = dict(zip(("eRP", "ePA", "eRB", "eAB"), (_shears(value, 0) for value in values)))
        self.assertEqual(module.dress(labels, "eAB"), _shears(rp+pa-rb+ab, 0))

    def test_matrix_and_scalar_domains(self) -> None:
        module = load(STEM)
        invalid_rows: tuple[object, ...] = (None, (), ((1, 0),), ((1, 0, 0), (0, 1, 0)),
            ((True, 0), (0, 1)), ((1.0, 0), (0, 1)), ((sp.Integer(1), 0), (0, 1)),
            ((2, 0), (0, 1)), ((-1, 0), (0, 1)), ((0, 0), (0, 0)))
        for rows in invalid_rows:
            self.refused(module.mat, rows)
        self.refused(module.mat, ((1, 1 << 4096), (0, 1)), kind="resource")
        self.assertIsInstance(module.mat([[1, -7], [0, 1]]), sp.ImmutableMatrix)
        self.assertIsInstance(module.eye(), sp.ImmutableMatrix)
        for index in range(4):
            for value in (True, 1.0, None, "1"):
                labels: list[object] = [0]*4
                labels[index] = value
                self.refused(module.additive_dress, *labels)
        self.refused(module.additive_dress, 1 << 4096, 0, 0, 0, kind="resource")
        self.refused(module.additive_dress, 1 << 4095, 1 << 4095, 0, 0, kind="resource")

    def test_label_admission_and_unused_matrices(self) -> None:
        module = load(STEM)
        invalid_matrices = (None, [[1, 0], [0, 1]], sp.eye(3), sp.zeros(2), sp.Matrix([[2, 0], [0, 1]]),
                            sp.Matrix([[1.0, 0], [0, 1]]), sp.Matrix([[1, sp.Rational(1, 2)], [0, 1]]),
                            sp.Matrix([[1, sp.Symbol("x")], [0, 1]]))
        for matrix in invalid_matrices:
            self.refused(module.path_transport, {"unused": matrix}, ())
        for labels in (None, (), {None: sp.eye(2)}, {True: sp.eye(2)}, {"": sp.eye(2)}, {" ": sp.eye(2)}):
            self.refused(module.validated_labels, labels)
        self.refused(module.validated_labels, {"x"*65: sp.eye(2)}, kind="resource")
        self.refused(module.validated_labels, {"x": sp.Matrix([[1, 1 << 4096], [0, 1]])}, kind="resource")
        self.refused(module.validated_labels, {str(i): sp.eye(2) for i in range(4097)}, kind="resource")
        self.assertEqual(module.path_transport({}, ()), sp.eye(2))

    def test_connection_and_export_snapshot_ownership(self) -> None:
        module = load(STEM)
        matrix = sp.Matrix([[1, 2], [0, 1]])
        labels = {"x": matrix}
        owned = module.SL2Connection(labels)
        exported = module.validated_labels(labels)
        matrix[0, 1] = 99
        labels.clear()
        self.assertEqual(sp.Matrix(owned.path((("x", 1),)).value.integer_rows()), sp.Matrix([[1, 2], [0, 1]]))
        self.assertEqual(exported["x"], sp.Matrix([[1, 2], [0, 1]]))
        exported.clear()
        self.assertEqual(tuple(owned.labels), ("x",))
        with self.assertRaises(TypeError):
            owned.labels["x"] = None
        with self.assertRaises(FrozenInstanceError):
            owned.labels = {}
        with self.assertRaises(TypeError):
            module.EDGES["bad"] = ("a", "a")
        with self.assertRaises(TypeError):
            module.TREE_PATH["a"] = ()

    def test_signed_path_and_footprint_refusals(self) -> None:
        module = load(STEM)
        malformed: tuple[object, ...] = (None, "x", (None,), (("x",),), (("x", 1, 2),),
            ((None, 1),), (("", 1),), (("x", 0),), (("x", True),), (("x", 1.0),), (("x", 2),))
        for path in malformed:
            self.refused(module.footprint, path)
            self.refused(module.path_transport, {"x": sp.eye(2)}, path)
        self.refused(module.path_transport, {}, (("missing", 1),))
        self.refused(module.footprint, (("x"*65, 1),), kind="resource")
        self.refused(module.footprint, (("x", 1),)*4097, kind="resource")
        self.assertEqual(module.footprint((("x", 1), ("x", -1), ("y", 1))), {"x", "y"})

    def test_fixed_graph_admission_and_whole_word_preflight(self) -> None:
        module = load(STEM)
        labels = {name: sp.eye(2) for name in module.EDGES}
        for path in (None, ("missing",), ("ePA", "eRP"), ("eRP", "eRB"), (True,)):
            self.refused(module.transport, labels, path)
        self.refused(module.transport, {}, ("eRP",))
        for edge in (None, "missing", True):
            self.refused(module.incident, edge)
            self.refused(module.dress, labels, edge)
        for name in labels:
            incomplete = {edge: matrix for edge, matrix in labels.items() if edge != name}
            self.refused(module.dress, incomplete, "eAB")
            self.refused(module.formula, incomplete)
        huge = sp.Matrix([[1, 1 << 4095], [0, 1]])
        # Unknown final edge must be found before the prefix exceeds arithmetic budget.
        self.refused(module.path_transport, {"x": huge}, (("x", 1), ("x", 1), ("missing", 1)))
        self.assertFalse(module.incident("eRP"))
        self.assertTrue(all(module.incident(edge) for edge in ("ePA", "eRB", "eAB")))

    def test_resource_boundaries_and_conservative_arithmetic(self) -> None:
        module = load(STEM)
        labels = {str(i): sp.eye(2) for i in range(4096)}
        self.assertEqual(len(module.SL2Connection(labels).labels), 4096)
        word = (("x", 1),)*4096
        self.assertEqual(module.path_transport({"x": sp.eye(2)}, word), sp.eye(2))
        self.refused(module.path_transport, {"x": sp.eye(2)}, word+(("x", 1),), kind="resource")
        huge = sp.Matrix([[1, 1 << 4095], [0, 1]])
        self.refused(module.path_transport, {"x": huge}, (("x", 1), ("x", 1)), kind="resource")
        big = 1 << 2048
        # det is exactly1, but individual determinant products exceed the budget.
        self.refused(module.validated_labels, {"x": sp.Matrix([[big, big-1], [big+1, big]])}, kind="resource")

    def test_fixture_scope_and_guard_types(self) -> None:
        module = load(STEM)
        labels = {"x": sp.eye(2), "y": sp.eye(2), "outside": sp.eye(2)}
        module.check_path_laws((), labels)
        self.refused(module.check_path_laws, (("outside", 1),), labels)
        self.refused(module.check_path_laws, (), {"x": sp.eye(2)})
        self.refused(module.check_path_laws, (("x", 1),)*4096, labels, kind="resource")
        with patch.object(module.SL2Connection, "_path", side_effect=AssertionError("transport began before prefix admission")):
            self.refused(module.check_path_laws, (("x", 1),)*4096, labels, kind="resource")
        self.refused(module.require, 1, "truthy is not bool")
        self.refused(module.require, False, "false obligation", kind="check")

    def test_default_counts_and_fixed_fault_detection(self) -> None:
        module = load(STEM)
        cases = Cases()
        counts = []
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            for check in (module.check_general_dependencies, module.check_additive, module.check_identity_matrices,
                          module.check_noncommutative_order, module.check_star_enumeration):
                check(cases)
                counts.append(cases.checks)
        self.assertEqual(counts, [488, 491, 500, 509, 511])
        self.assertIn("85 loop words, 255 append cases", output.getvalue())
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(cli(module.main), 0)
        receipt = json.loads(output.getvalue()[output.getvalue().rindex('{'):])
        self.assertEqual(receipt["checks"], 511)
        for operation, check, wrong in (("additive_dress", module.check_additive, 0),
                                        ("dress", module.check_noncommutative_order, sp.eye(2)),
                                        ("incident", module.check_star_enumeration, True)):
            with patch.object(module, operation, return_value=wrong), contextlib.redirect_stdout(io.StringIO()):
                self.refused(check, kind="check")

    def test_recorders_railway_and_cancellation(self) -> None:
        module = load(STEM)
        for check in (module.check_general_dependencies, module.check_additive, module.check_identity_matrices,
                      module.check_noncommutative_order, module.check_star_enumeration):
            self.refused(check, object())
        self.refused(module.check_path_laws, (), {}, object())
        owned = module.SL2Connection({})
        for method, operation, argument in (("_path", owned.path, ()), ("_tree", owned.tree, ()), ("_dress", owned.dress, "eAB")):
            with patch.object(module.SL2Connection, method, side_effect=OSError("injected")):
                self.assertEqual(operation(argument).error.kind, "resource")
            with patch.object(module.SL2Connection, method, side_effect=KeyboardInterrupt):
                with self.assertRaises(KeyboardInterrupt):
                    operation(argument)
        errors = io.StringIO()
        with patch.object(module, "check_general_dependencies", side_effect=OSError("injected")):
            with contextlib.redirect_stderr(errors):
                self.assertEqual(cli(module.main), 1)
        self.assertEqual(json.loads(errors.getvalue())["kind"], "resource")


if __name__ == "__main__":
    unittest.main(verbosity=2)
