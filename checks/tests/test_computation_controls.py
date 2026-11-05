"""Finite word-system and six composed computation-control contracts.

AuthorityEffect: None. Finite search and traces do not decide an infinite language.
"""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from dataclasses import FrozenInstanceError
import io
from itertools import product
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from hypothesis import given, settings, strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_review_repairs import load
from checker_support.boundary import cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import Failure

STEM = "comp-finite-model-controls"
Word = tuple[int, ...]
Rule = tuple[Word, Word]
WORDS = st.lists(st.integers(0, 1), max_size=3).map(tuple)
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)


def _context_graph(rules: list[Rule], bound: int) -> set[tuple[Word, Word]]:
    """Independent formal one-hole relation, enumerating contexts rather than scanning sources."""
    words = [word for size in range(bound+1) for word in product((0, 1), repeat=size)]
    edges = set()
    for (left, right), (before, after) in product(product(words, repeat=2), rules):
        source, target = left+before+right, left+after+right
        if max(len(source), len(target)) <= bound:
            edges.add((source, target))
    return edges


def _distances(edges: set[tuple[Word, Word]], source: Word) -> dict[Word, int]:
    """Layer-wise least fixed point; no queue or production predecessor map."""
    distances = {source: 0}
    layer = {source}
    depth = 0
    while layer:
        next_layer = {target for start, target in edges if start in layer and target not in distances}
        depth += 1
        distances.update({word: depth for word in next_layer})
        layer = next_layer
    return distances


class ComputationControlTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object) -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        if result.error is None:
            self.fail("refusal lacks a typed error")
        return result.error

    def test_refusal_helper_requires_a_failure(self) -> None:
        with self.assertRaises(AssertionError):
            self.refused(lambda: None)

    def test_graph_oracles_on_explicit_small_relations(self) -> None:
        self.assertEqual(_context_graph([((0,), (1,))], 1), {((0,), (1,))})
        self.assertEqual(_context_graph([((0,), (1,))], 0), set())
        self.assertEqual(_context_graph([((), (1,))], 1), {((), (1,))})
        edges: set[tuple[Word, Word]] = {((), (0,)), ((0,), (1,)), ((1,), (0,))}
        self.assertEqual(_distances(edges, ()), {(): 0, (0,): 1, (1,): 2})
        self.assertEqual(_distances(set(), (0,)), {(0,): 0})

    @PROPERTY
    @given(rules=st.lists(st.tuples(WORDS, WORDS), max_size=4, unique=True), bound=st.integers(0, 3), source=WORDS, target=WORDS)
    def test_bounded_search_against_context_fixed_point(self, rules: list[Rule], bound: int, source: Word, target: Word) -> None:
        module = load(STEM)
        source = source[:bound]
        model = module.FiniteWordSystem((0, 1), rules, bound)
        edges = _context_graph(rules, bound)
        distances = _distances(edges, source)
        result = model.find_path(source, target)
        self.assertTrue(result.ok)
        if target in distances:
            path = result.value
            self.assertIsNotNone(path)
            self.assertEqual((path[0], path[-1]), (source, target))
            self.assertEqual(len(path)-1, distances[target])
            self.assertTrue(all(edge in edges for edge in zip(path, path[1:])))
            verification = model.verify_trace(path)
            self.assertTrue(verification.ok)
            self.assertEqual(verification.value, path)
        else:
            self.assertIsNone(result.value)

    @PROPERTY
    @given(prefix=WORDS, before=WORDS, after=WORDS, suffix=WORDS)
    def test_one_hole_replacement_uses_exact_context(self, prefix: Word, before: Word, after: Word, suffix: Word) -> None:
        module = load(STEM)
        model = module.FiniteWordSystem((0, 1), ((before, after),), 16)
        source = prefix+before+suffix
        target = prefix+after+suffix
        self.assertEqual(model.apply(source, 0, prefix, suffix), target)
        verification = model.verify_trace((source, target))
        self.assertTrue(verification.ok)
        self.assertEqual(verification.value, (source, target))
        self.refused(model.apply, source+(0,), 0, prefix, suffix)

    def test_search_and_trace_budgets_never_mean_unreachable(self) -> None:
        module = load(STEM)
        model = module.FiniteWordSystem((0, 1, 2), (((0,), (1,)), ((1,), (2,))), 1)
        success = model.find_path((0,), (2,), 3, 8)
        self.assertTrue(success.ok)
        self.assertEqual(success.value, ((0,), (1,), (2,)))
        for result in (model.find_path((0,), (2,), 2, 8), model.find_path((0,), (2,), 3, 7),
                       model.verify_trace(((0,), (1,), (2,)), 7)):
            self.assertFalse(result.ok)
            self.assertIsNone(result.value)
            self.assertEqual(result.error.kind, "resource")
        self.assertTrue(model.verify_trace(((0,), (1,), (2,)), 8).ok)
        self.assertEqual(model.find_path((0,), (0,), 1, 0).value, ((0,),))
        self.assertTrue(model.find_path((0,), (0,), 1, 0).ok)
        with patch.object(module.FiniteWordSystem, "_successors", side_effect=AssertionError("expansion before budget")):
            result = model.find_path((0,), (2,), 3, 0)
            self.assertFalse(result.ok)
            self.assertEqual(result.error.kind, "resource")
        early = module.FiniteWordSystem((0, 1, 2), (((0,), (1,)), ((0,), (2,))), 1)
        self.assertEqual(early.find_path((0,), (1,), 2, 4).value, ((0,), (1,)))
        missing = model.find_path((0,), (), 3, 12)
        self.assertTrue(missing.ok)
        self.assertIsNone(missing.value)

    def test_shortest_route_and_no_path_exhaustion(self) -> None:
        module = load(STEM)
        rules = (((0,), (1,)), ((0,), (2,)), ((2,), (3,)), ((3,), (4,)), ((1,), (4,)))
        model = module.FiniteWordSystem((0, 1, 2, 3, 4), rules, 1)
        route = model.find_path((0,), (4,), 5, 50)
        self.assertTrue(route.ok)
        self.assertEqual(route.value, ((0,), (1,), (4,)))
        exhausted = model.find_path((0,), (), 5, 50)
        self.assertTrue(exhausted.ok)
        self.assertIsNone(exhausted.value)

    def test_empty_rules_cycles_insertion_deletion_and_trace_refusal(self) -> None:
        module = load(STEM)
        empty = module.FiniteWordSystem((0,), (), 1)
        self.assertEqual(empty.find_path((0,), (0,), 1, 0).value, ((0,),))
        self.assertTrue(empty.find_path((0,), (), 1, 0).ok)
        self.assertIsNone(empty.find_path((0,), (), 1, 0).value)
        self.assertEqual(empty.verify_trace(((0,), (0,))).error.kind, "check")
        self.assertEqual(empty.verify_trace(()).error.kind, "input")
        self.assertEqual(empty.verify_trace(((0, 0),)).error.kind, "input")
        self.assertEqual(empty.find_path((0, 0), ()).error.kind, "input")
        self.assertTrue(empty.find_path((), (0, 0), 1, 0).ok)
        self.assertIsNone(empty.find_path((), (0, 0), 1, 0).value)
        cycles = module.FiniteWordSystem((0, 1), (((0,), (1,)), ((1,), (0,))), 1)
        self.assertTrue(cycles.find_path((0,), (), 2, 8).ok)
        self.assertIsNone(cycles.find_path((0,), (), 2, 8).value)
        edits = module.FiniteWordSystem((0, 1), (((), (1,)), ((1,), ())), 2)
        self.assertEqual(edits.apply((0,), 0, (0,), ()), (0, 1))
        self.assertEqual(edits.apply((1, 0), 1, (), (0,)), (0,))
        self.assertTrue(edits.verify_trace(((0,), (0, 1), (0,))).ok)
        self.assertEqual(edits.verify_trace(((0,), (1,))).error.kind, "check")
        bounded_insertion = module.FiniteWordSystem((0, 1), (((), (0,)),), 1)
        exhausted = bounded_insertion.find_path((), (1,), 2, 3)
        self.assertTrue(exhausted.ok)
        self.assertIsNone(exhausted.value)

    def test_model_owns_immutable_snapshots(self) -> None:
        module = load(STEM)
        alphabet = [0, 1]
        before, after = [0], [1]
        rules = [[before, after]]
        model = module.FiniteWordSystem(alphabet, rules, 1)
        alphabet.clear()
        before.clear()
        after.append(0)
        rules.clear()
        self.assertEqual(model.alphabet, frozenset((0, 1)))
        self.assertEqual(model.rules, (((0,), (1,)),))
        self.assertEqual(model.find_path((0,), (1,)).value, ((0,), (1,)))
        with self.assertRaises(FrozenInstanceError):
            model.max_length = 2
        candidate = [[0], [1]]
        result = model.verify_trace(candidate)
        candidate[0].clear()
        self.assertEqual(result.value, ((0,), (1,)))

    def test_model_schema_and_word_boundaries(self) -> None:
        module = load(STEM)
        malformed: list[tuple[object, object, object]] = [
            ((), (), 1), ((0, 0), (), 1), ((True,), (), 1), ((-1,), (), 1), ((4096,), (), 1),
            (tuple(range(33)), (), 1), ((0,), (), True), ((0,), (), -1), ((0,), (), 65),
            ((0,), "rules", 1), ((0,), (((),),), 1), ((0,), (((), (1,)),), 1),
            ((0,), (((0,)*65, ()),), 1), ((0,), (((0,), ()), ((0,), ())), 1),
        ]
        for alphabet, rules, bound in malformed:
            self.refused(module.FiniteWordSystem, alphabet, rules, bound)
        oversized_rules = tuple(((0,)*size, (1,)) for size in range(33))
        self.assertEqual(self.refused(module.FiniteWordSystem, (0, 1), oversized_rules, 1).kind, "resource")
        model = module.FiniteWordSystem((0, 1), (((0,), (1,)),), 64)
        for word in ((True,), (0.0,), (-1,), (4096,), (2,), (0,)*65, "0"):
            self.refused(model.admit_word, word)
        self.assertEqual(model.admit_word((0,)*64), (0,)*64)
        for index in (-1, True, 1, 2**4096):
            self.refused(model.apply, (0,), index, (), ())
        self.assertEqual(model.verify_trace(((0,),)*4097).error.kind, "resource")
        identity = module.FiniteWordSystem((0,), (((0,), (0,)),), 1)
        self.assertTrue(identity.verify_trace(((0,),)*4096).ok)

    def test_search_parameter_refusals(self) -> None:
        module = load(STEM)
        model = module.FiniteWordSystem((0,), (), 1)
        for states, trials in ((0, 0), (True, 0), (4097, 0), (1, -1), (1, True), (1, 65537)):
            result = model.find_path((0,), (0,), states, trials)
            self.assertFalse(result.ok)
            self.assertIsNone(result.value)
        for value in (True, -1, 65537):
            self.assertFalse(model.verify_trace(((0,),), value).ok)
        self.assertFalse(model.find_path((False,), (0,)).ok)
        self.assertFalse(model.find_path((0,), (False,)).ok)

    @PROPERTY
    @given(value=st.integers(0, 2**128), argument=st.integers(0, 2**128), current=st.integers(0, 2**128), halted=st.booleans())
    def test_constant_writer_halt_persistence_and_natural_merge(self, value: int, argument: int, current: int, halted: bool) -> None:
        module = load(STEM)
        self.assertEqual(module.write_halt(value, halted, current), (True, current if halted else value))
        self.assertEqual(module.eval_const(value, argument), value)
        self.assertEqual(module.merge01(value), 0 if value == 1 else value)
        self.assertEqual(module.merge01(module.merge01(value)), module.merge01(value))

    @PROPERTY
    @given(code=st.integers(0, 4095), word=st.lists(st.integers(0, 4095), max_size=63))
    def test_encoding_and_blank_extension(self, code: int, word: list[int]) -> None:
        module = load(STEM)
        self.assertEqual(module.start_word(code), (code, 0))
        self.assertIs(module.word_pred(module.start_word(code)), code == 1)
        snapshot = word[:]
        result = module.append_blank(word)
        self.assertEqual(result[:-1], snapshot)
        self.assertEqual(result[-1], 0)
        self.assertEqual(word, snapshot)
        word.clear()
        self.assertEqual(result, snapshot+[0])

    def test_literal_helper_domains(self) -> None:
        module = load(STEM)
        bad: object
        for bad in (-1, True, False, 0.0, None, 2**4096):
            self.refused(module.merge01, bad)
            self.refused(module.eval_const, bad, 0)
            self.refused(module.eval_const, 0, bad)
            self.refused(module.write_halt, bad, True, 0)
            self.refused(module.write_halt, 0, False, bad)
        for bad in (0, 1, None, "halted"):
            self.refused(module.write_halt, 1, bad, 0)
        for bad in (-1, True, 4096):
            self.refused(module.start_word, bad)
        for bad in ((), (1,), (1, 0, 0), (True, 0), (1, 0.0), (4096, 0), "10"):
            self.refused(module.word_pred, bad)
        for bad in ([0]*64, [True], [-1], [4096], None):
            self.refused(module.append_blank, bad)
        maximum = 2**4096-1
        self.assertEqual(module.eval_const(maximum, maximum), maximum)
        self.assertEqual(module.write_halt(0, True, maximum), (True, maximum))
        self.assertEqual(module.append_blank([]), [0])
        self.assertEqual(module.append_blank([1]*63), [1]*63+[0])

    def test_six_original_controls_and_cli(self) -> None:
        module = load(STEM)
        expected = {"scope": "six finite computation controls", "authority_effect": "None", "total_checks": 50,
                    "failed_checks": 0, "failures": [], "all_passed": True}
        self.assertEqual(module.run_checks(), expected)
        cases = Cases()
        for operation, total in ((module.check_word_moves, 5), (module.check_no_rule_bound, 10),
                                 (module.check_constant_writer, 35), (module.check_predicate_composition, 41),
                                 (module.check_fixed_target, 43), (module.check_marked_tape, 50)):
            operation(cases)
            self.assertEqual(len(cases), total)
        self.assertTrue(all(type(status) is bool and status for _, status in cases))
        self.assertEqual(len({name for name, _ in cases}), 50)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(cli(module.main), 0)
        self.assertEqual(json.loads(output.getvalue()), expected)

    @PROPERTY
    @given(statuses=st.lists(st.booleans(), max_size=20))
    def test_generated_receipt_accounting(self, statuses: list[bool]) -> None:
        module = load(STEM)
        def supplied(cases: Cases) -> None:
            for index, status in enumerate(statuses):
                cases.append((f"generated-{index}", status))
        with patch.object(module, "check_word_moves", supplied):
            result = module.run_checks()
        failed = [f"generated-{i}" for i, status in enumerate(statuses) if not status]
        self.assertEqual(result["total_checks"], 45+len(statuses))
        self.assertEqual(result["failures"], failed)
        self.assertEqual(result["failed_checks"], len(failed))
        self.assertIs(result["all_passed"], not failed)

    def test_expected_failures_cancellation_and_repeated_invocations(self) -> None:
        module = load(STEM)
        def failed(cases: Cases) -> None:
            cases.append(("injected", False))
        with patch.object(module, "check_marked_tape", failed):
            self.assertEqual(module.run_checks()["failures"], ["injected"])
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli(module.main), 1)
        errors = io.StringIO()
        with patch.object(module, "check_marked_tape", side_effect=OSError("injected")):
            with contextlib.redirect_stderr(errors):
                self.assertEqual(cli(module.main), 1)
        self.assertEqual(json.loads(errors.getvalue())["kind"], "resource")
        with patch.object(module, "check_marked_tape", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                cli(module.main)
        self.assertTrue(module.run_checks()["all_passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
