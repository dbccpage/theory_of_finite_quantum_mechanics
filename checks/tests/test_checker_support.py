"""Contract, property and independent-oracle tests for checker infrastructure.

AuthorityEffect: None. Dynamic invocation deliberately exercises invalid public
inputs; production sources remain strictly typed. Runs unchanged under -O.
"""
from __future__ import annotations

from collections.abc import Callable
from contextlib import redirect_stderr
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
from io import StringIO
from itertools import product
import json
from pathlib import Path
import sys
import unittest
from typing import Never
from unittest.mock import patch

from hypothesis import example, given, settings, strategies as st
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli, evaluate, require
from checker_support.cases import Cases
from checker_support import domains as d
from checker_support.domains import Failure
from checker_support.gaussian_matrix2 import GaussianMatrix2 as M
from checker_support.gaussian_rational import GaussianRational as G
from checker_support.outcome import Outcome
from checker_support.mutation_case import MutationCase
from checker_support.cases import Cases as CheckRun
from checker_support.boundary import Violation
from checker_support.wilson_operator import direct_wilson_determinant
from checker_support import wilson_operator as w
from checker_support.domains import hole

settings.register_profile("checker_contract", max_examples=80, deadline=None,
                          derandomize=True, database=None)
settings.load_profile("checker_contract")
RATIONAL = st.fractions(min_value=-8, max_value=8, max_denominator=12)


def raises(error: BaseException) -> Never:
    """An explicit error injection, including uncaught cancellation signals."""
    raise error


class CheckerSupportTests(unittest.TestCase):
    def refused(self, action: Callable[..., object], *args: object,
                kind: str = "input", **kwargs: object) -> Failure:
        result = evaluate(action, *args, **kwargs)
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("refusal must include its typed cause")
        self.assertEqual(result.error.kind, kind)
        return result.error

    def test_failure_value_and_exception_bridge(self) -> None:
        for kind in ("input", "resource", "check", "duplicate"):
            failure = evaluate(Failure, kind, "cause").value
            if failure is None:
                self.fail("valid failure was refused")
            record = failure.to_record()
            self.assertEqual(record, {"kind": kind, "message": "cause"})
            record["message"] = "changed"
            self.assertEqual(failure.message, "cause")
            with self.assertRaises(FrozenInstanceError):
                setattr(failure, "kind", "check")
        for invalid_kind, message in (("unknown", "x"), (1, "x"), ("input", ""),
                              ("input", "  "), ("input", 3)):
            self.refused(Failure, invalid_kind, message)
            self.refused(Violation, invalid_kind, message)
        error = Violation("check", "evidence mismatch")
        self.assertEqual(str(error), "evidence mismatch")
        self.assertEqual(evaluate(raises, error).error, error.failure)

    def test_outcome_construction_and_nullable_success(self) -> None:
        failure = Failure("input", "no")
        for args, kwargs in (((), {}), ((None,), {"error": failure}),
                             ((1,), {"error": failure}), ((), {"error": "wrong"})):
            self.refused(Outcome, *args, **kwargs)
        empty: Outcome[None] = Outcome(value=None)
        self.assertTrue(empty.ok)
        self.assertIsNone(empty.value_or(None))
        self.assertEqual(empty.map(lambda _: 7).value, 7)
        failed: Outcome[int] = Outcome(error=failure)
        self.assertEqual(failed.value_or(8), 8)
        self.assertEqual(failed.bind(lambda _: self.fail("must short circuit")).error, failure)
        with self.assertRaises(FrozenInstanceError):
            setattr(empty, "error", failure)

    def test_outcome_transitions_preserve_errors(self) -> None:
        start = Outcome(value=4)
        self.assertEqual(start.map(lambda x: x + 3).value, 7)
        self.assertEqual(start.value_or(0), 4)
        invalid: Callable[..., Outcome[object]] = start.bind
        self.assertFalse(invalid(3).ok)
        self.assertFalse(invalid(lambda _: 3).ok)
        for error in (ValueError(), TypeError("type"), ZeroDivisionError("zero"),
                      Violation("resource", "budget"), OSError("unavailable")):
            def fail_transition(_: int) -> Outcome[int]:
                raise error
            result = start.bind(fail_transition)
            self.assertFalse(result.ok)
            self.assertIsNotNone(result.error)
        with self.assertRaises(RuntimeError):
            start.map(lambda _: raises(RuntimeError("programmer error")))

    @given(st.integers(), st.integers(), st.integers())
    def test_railway_associativity(self, value: int, a: int, b: int) -> None:
        def first(x: int) -> Outcome[int]:
            return Outcome(value=x + a) if x >= 0 else Outcome(error=Failure("input", "negative"))
        def second(x: int) -> Outcome[int]:
            return Outcome(value=x * b)
        start = Outcome(value=value)
        self.assertEqual(start.bind(first).bind(second), start.bind(lambda x: first(x).bind(second)))

    def test_boundary_errors_cancellation_and_required_boolean(self) -> None:
        dynamic: Callable[..., Outcome[object]] = evaluate
        self.assertFalse(dynamic(3).ok)
        for error in (ValueError(), TypeError(), ZeroDivisionError()):
            result = evaluate(raises, error)
            self.assertEqual(result.error, Failure("input", type(error).__name__))
        self.assertEqual(evaluate(raises, OSError()).error, Failure("resource", "OSError"))
        for uncaught in (RuntimeError(), KeyboardInterrupt(), SystemExit(2)):
            with self.assertRaises(type(uncaught)):
                evaluate(raises, uncaught)
        require(True, "valid obligation")
        self.refused(require, False, "false obligation", kind="check")
        for condition in (0, 1, "true", None, [], object()):
            self.refused(require, condition, "not a bool")
        for message in ("", " ", None, 1):
            self.refused(require, True, message)

    def test_cli_exit_domain_and_failure_wire_format(self) -> None:
        for status in (None, 0, 1, 255):
            stream = StringIO()
            with redirect_stderr(stream):
                actual = cli(lambda: status)
            self.assertEqual(actual, 0 if status is None else status)
            self.assertEqual(stream.getvalue(), "")
        for invalid_status in (True, False, -1, 256, "0", Q(0)):
            action: Callable[..., int] = cli
            stream = StringIO()
            with redirect_stderr(stream):
                self.assertEqual(action(lambda: invalid_status), 1)
            self.assertEqual(json.loads(stream.getvalue())["kind"], "input")
        stream = StringIO()
        with redirect_stderr(stream):
            self.assertEqual(cli(lambda: raises(Violation("check", "failed"))), 1)
        self.assertEqual(json.loads(stream.getvalue()),
                         {"status": "failed", "kind": "check", "message": "failed"})
        stream.close()
        with redirect_stderr(stream):
            self.assertEqual(cli(lambda: raises(OSError("resource failure"))), 1)

    def test_integer_boundaries(self) -> None:
        for value in (True, False, Q(1), 1.0, "1", None):
            self.refused(d.integer, value)
        for kwargs in ({"minimum": True}, {"maximum": 1.0}, {"minimum": 2, "maximum": 1}):
            self.refused(d.integer, 1, **kwargs)
        self.refused(d.integer, -1, minimum=0)
        self.refused(d.integer, 2, minimum=2, maximum=1)
        self.refused(d.integer, 2, maximum=1, kind="resource")
        self.assertEqual(d.integer(-1, minimum=-1, maximum=-1), -1)
        self.assertEqual(d.integer(1 << 200), 1 << 200)

    def test_rational_boundaries_and_resource_budget(self) -> None:
        for value in (True, 0.5, "1/2", None):
            self.refused(d.rational, value)
        self.refused(d.rational, 1, strictly_positive=1)
        self.refused(d.rational, 1, minimum=True)
        self.refused(d.rational, -1, minimum=0)
        for value in (0, -1):
            self.refused(d.rational, value, strictly_positive=True)
        for oversized in (1 << 4096, Q(1, 1 << 4096)):
            self.refused(d.rational, oversized, kind="resource")
        self.assertEqual(d.rational((1 << 4096) - 1), (1 << 4096) - 1)
        self.assertEqual(d.rational(Q(1, 3), minimum=Q(1, 3), strictly_positive=True), Q(1, 3))

    def test_collection_admission_and_snapshot_ownership(self) -> None:
        value: object
        for value in (None, {}, range(3), "abc"):
            self.refused(d.sequence, value)
        for kwargs in ({"maximum": -1}, {"maximum": True}, {"size": -1},
                       {"size": True}, {"size": 2}):
            self.refused(d.sequence, [1], **kwargs)
        self.refused(d.sequence, [], maximum=4097, kind="resource")
        self.refused(d.sequence, [1], maximum=0, kind="resource")
        self.refused(d.sequence, [], size=2, maximum=1, kind="resource")
        source = [1, 2]
        frozen = d.sequence(source, size=2)
        source[0] = 9
        self.assertEqual(frozen, (1, 2))
        self.assertEqual(d.sequence([], size=0, maximum=0), ())
        self.assertEqual(len(d.sequence([0]*4096)), 4096)

    def test_matrix_word_and_permutation_domains(self) -> None:
        matrix: object
        for matrix in ([], [[]], [[1], []], [[True]], [[1.0]]):
            self.refused(d.integer_matrix, matrix)
        self.refused(d.integer_matrix, [[0]*65]*65, kind="resource")
        self.refused(d.integer_matrix, [[1]], rows=2)
        self.refused(d.integer_matrix, [[1]], cols=2)
        self.assertEqual(d.integer_matrix([[1, 2], [3, 4]], rows=2, cols=2), ((1, 2), (3, 4)))
        self.assertEqual(d.flat_matrix2([1, 2, 3, Q(1, 4)]), (Q(1), Q(2), Q(3), Q(1, 4)))
        for value in ([1, 2, 3], [1, 2, 3, 4.0]):
            self.refused(d.flat_matrix2, value)
        self.assertEqual(d.binary_word([True, False]), (True, False))
        self.refused(d.binary_word, [1])
        self.refused(d.binary_word, [False]*65, kind="resource")
        self.assertEqual(d.permutation3([2, 0, 1]), (2, 0, 1))
        for value in ([0, 1], [0, 0, 2], [False, 1, 2], [0, 1, 3]):
            self.refused(d.permutation3, value)

    def test_cases_transactional_admission_and_iteration(self) -> None:
        cases = Cases()
        for row in (("", True), ("  ", True), (1, True), ("a", 1), ("x",), ["x", True]):
            self.refused(cases.append, row)
        self.assertTrue(cases.record("x", True).ok)
        snapshot = iter(cases)
        self.assertFalse(cases.record("x", False).ok)
        self.assertTrue(cases.record("y", False).ok)
        self.assertEqual(tuple(snapshot), (("x", True),))
        self.assertEqual(tuple(cases), (("x", True), ("y", False)))
        self.assertEqual(len(cases), 2)
        self.assertEqual(cases.checks, 2)
        self.assertEqual(len(Cases()), 0)
        self.refused(cases.append, ("a"*1025, True), kind="resource")
        with patch("checker_support.cases.MAX_CASES", 2):
            self.refused(cases.append, ("z", True), kind="resource")
        self.assertEqual(len(cases), 2)
        self.assertEqual(cases.checks, 2)
        self.assertTrue(cases.record("a"*1024, True).ok)
        self.assertEqual(cases.checks, 3)
        self.refused(cases.require, False, "counted failure", kind="check")
        self.assertEqual(cases.checks, 4)
        self.assertEqual(len(cases), 3)

    def test_counter_is_invocation_owned_and_counts_failed_obligations(self) -> None:
        counter = CheckRun()
        self.assertEqual(counter.checks, 0)
        counter.require(True, "first")
        self.refused(counter.require, False, "second", kind="check")
        self.assertEqual(counter.checks, 2)
        self.assertEqual(CheckRun().checks, 0)
        with self.assertRaises(AttributeError):
            setattr(counter, "checks", 0)

    def test_mutation_request_admission_and_exact_replacement(self) -> None:
        valid = MutationCase("test-fault", "domains.py", "old", "new", ("test_integer_boundaries",))
        self.assertEqual(valid.apply("prefix old suffix"), "prefix new suffix")
        self.refused(valid.apply, "old old")
        self.refused(valid.apply, "absent")
        self.refused(valid.apply, 3)
        fields: list[object] = [valid.identity, valid.source, valid.before, valid.after, valid.tests]
        invalid: tuple[tuple[int, object], ...] = ((0, ""), (0, "../escape"), (0, 1),
            (1, "../domains.py"), (1, "x.txt"), (2, ""), (2, 1), (2, "a"*8193),
            (3, "old"), (4, []), (4, ()), (4, ("wrong",)), (4, (1,)),
            (4, ("test_x",)*33))
        for index, replacement in invalid:
            changed = fields.copy()
            changed[index] = replacement
            self.refused(MutationCase, *changed)
        self.refused(MutationCase, "a", "b.py", "x", "y", ("test_x", "test_x"), kind="duplicate")
        with self.assertRaises(FrozenInstanceError):
            setattr(valid, "after", "changed")

    def test_gaussian_invalid_components_operands_and_immutability(self) -> None:
        for value in (True, 0.5, "1", None):
            self.refused(G, value)
            self.refused(G, 0, value)
            for operation in (G(1).__add__, G(1).__sub__, G(1).__mul__, G(1).div):
                self.refused(operation, value)
        self.refused(G(0).inv)
        with self.assertRaises(FrozenInstanceError):
            setattr(G(1), "re", Q(2))
        self.assertEqual(G(2, 3).conj(), G(2, -3))
        self.assertEqual(G(2, 3).norm_sq(), Q(13))
        self.assertEqual(G(2, 3).mul(G(1)), G(2, 3))

    @given(RATIONAL, RATIONAL, RATIONAL, RATIONAL)
    def test_gaussian_field_against_symbolic_complex_arithmetic(self, a: Q, b: Q, c: Q, e: Q) -> None:
        left, right = G(a, b), G(c, e)
        symbolic_left, symbolic_right = sp.Rational(a) + sp.I*sp.Rational(b), sp.Rational(c) + sp.I*sp.Rational(e)
        for actual, expected in ((left+right, symbolic_left+symbolic_right),
                                 (left-right, symbolic_left-symbolic_right),
                                 (left*right, symbolic_left*symbolic_right)):
            self.assertEqual(actual.re, sp.re(sp.expand(expected)))
            self.assertEqual(actual.im, sp.im(sp.expand(expected)))
        if right != G(0):
            quotient = left.div(right)
            self.assertEqual(quotient*right, left)
            self.assertEqual(right.inv()*right, G(1))
        self.assertEqual((left*right).conj(), left.conj()*right.conj())

    def test_gaussian_matrix_invariants(self) -> None:
        self.refused(M, 1, G(0), G(0), G(1))
        self.refused(M.eye().mul, 1)
        self.refused(M(G(1), G(2), G(2), G(4)).inv)
        with self.assertRaises(FrozenInstanceError):
            setattr(M.eye(), "a11", G(2))
        self.assertEqual(M.eye().trace(), G(2))
        self.assertEqual(M.pauli_x().det(), G(-1))
        self.assertEqual(M.pauli_x().mul(M.pauli_x()), M.eye())
        self.assertEqual(M.pauli_z().mul(M.pauli_z()), M.eye())
        self.assertTrue(M.pauli_x().is_unitary())
        self.assertFalse(M(G(2), G(0), G(0), G(1)).is_unitary())
        matrix = M(G(1, 2), G(2), G(0, 3), G(4, -1))
        self.assertEqual(matrix.mul(matrix.inv()), M.eye())
        self.assertEqual(matrix.adjoint().adjoint(), matrix)
        self.assertEqual(matrix.adjoint(), M(G(1,-2), G(0,-3), G(2), G(4,1)))

    @given(st.lists(st.integers(-4, 4), max_size=8), st.lists(st.integers(-4, 4), max_size=8),
           st.lists(st.integers(-4, 4), max_size=8), st.lists(st.integers(-4, 4), max_size=8))
    def test_word_replacement_preserves_context(self, left: list[int], before: list[int],
                                               after: list[int], right: list[int]) -> None:
        original = left+before+right
        result = hole(original, left, before, after, right)
        self.assertEqual(result, left+after+right)
        self.assertEqual(hole(result, left, after, before, right), original)
        self.assertIsNot(result, original)

    def test_word_replacement_refusals(self) -> None:
        self.refused(hole, [9], [], [1], [2], [])
        self.refused(hole, [True], [], [True], [2], [])
        self.refused(hole, [0]*4096, [0]*4096, [], [1], [], kind="resource")

    def test_stabilizer_admission_and_cache_snapshot(self) -> None:
        from checker_support import happy_boundary as h
        gens = h.build_boundary_gens_20()
        self.assertEqual(h.validate_generators(gens), tuple(gens))
        gens[0] = 0
        self.refused(h.validate_generators, gens)
        self.refused(h.validate_generators, [1])
        # Independent but noncommuting: X_0 and Z_0 among 20 single Pauli bits.
        self.refused(h.validate_generators, [1 << i for i in range(20)])
        self.refused(h.validate_generators, [True]*20)
        for args in ((20, 0, 0), (0, 2, 0), (0, 0, -1)):
            self.refused(h.set_xz, *args, kind="resource" if 20 in args or 2 in args else "input")
        self.refused(h.encode_local_gen, 5, [(0, 0)]*4, kind="resource")
        self.refused(h.encode_local_gen, 0, [(0, 0)]*3)
        self.refused(h.encode_central_gen, [(0, 0)]*4)
        self.refused(h.commutes_20, -1, 0)
        self.refused(h.commutes_20, 0, 1 << 40, kind="resource")
        self.refused(h.gf2_rank, [-1])
        self.refused(h.region_entropy, h.BOUNDARY_GENS_20, [0, 0])
        self.refused(h.region_mutual_information, h.BOUNDARY_GENS_20, [1], [1])
        self.assertEqual(h.interval_entropy(h.BOUNDARY_GENS_20, 0, 0), 0)
        self.assertEqual(h.interval_entropy(h.BOUNDARY_GENS_20, 0, 20), 0)
        self.assertEqual(h.encode_local_gen(0, [(1,0),(0,1),(0,1),(1,0)]), 105)
        self.assertEqual(h.encode_central_gen([(1,0)]+[(0,0)]*4), 26)
        self.assertEqual(h.encode_central_gen([(0,1)]+[(0,0)]*4), 145)
        self.assertFalse(h.commutes_20(1, 2))
        self.assertTrue(h.commutes_20(1, 4))

    def test_stabilizer_mincut_independent_assignments(self) -> None:
        from checker_support import happy_boundary as h
        for start, length in product(range(20), range(21)):
            region = {(start+i)%20 for i in range(length)}
            costs = []
            for central, *outer in product((0, 1), repeat=6):
                costs.append(sum(central != side for side in outer) +
                             sum(outer[q//4] != int(q in region) for q in range(20)))
            self.assertEqual(h.interval_mincut(start, length), min(costs))
            expected_mask = sum(3 << (2*q) for q in region)
            self.assertEqual(h.interval_bitmask_40(start, length), expected_mask)

    def test_stabilizer_entropy_for_product_and_bell_states(self) -> None:
        from checker_support import happy_boundary as h
        product_state = [1 << (2*q+1) for q in range(20)]
        bell_state = [5, 10] + product_state[2:]
        for region in ([], [0], [1,2,3], list(range(20))):
            self.assertEqual(h.region_entropy(product_state, region), 0)
        self.assertEqual(h.region_entropy(bell_state, [0]), 1)
        self.assertEqual(h.region_entropy(bell_state, [1]), 1)
        self.assertEqual(h.region_entropy(bell_state, [0,1]), 0)
        self.assertEqual(h.region_mutual_information(bell_state, [0], [1]), 2)
        self.assertEqual(h.region_mutual_information(bell_state, [0], [2]), 0)

    @given(st.lists(st.integers(0, 255), max_size=9))
    def test_rank_against_explicit_vector_span(self, rows: list[int]) -> None:
        from checker_support import happy_boundary as h
        span = {0}
        for row in rows:
            span |= {value ^ row for value in tuple(span)}
        self.assertEqual(1 << h.gf2_rank(rows), len(span))

    def test_wilson_shapes_and_chirality_boundaries(self) -> None:
        self.assertTrue(w.clifford_relations(w.gamma_matrices()))
        self.assertTrue(w.assembled_operator_checks())
        for matrix in ([], [[G(0)]], [[0]*16]*16):
            self.refused(w.gamma5_hermitian, matrix)
        self.refused(w.clifford_relations, [])
        self.refused(w.clifford_relations, w.gamma_matrices(), [1, 1, 0, -1])
        self.refused(w.clifford_relations, w.gamma_matrices(), [True]*4)
        self.refused(w.assembled_operator, 0.5)
        self.refused(w.color_link, 4, 0, kind="resource")
        self.refused(w.spin_color_index, 0, 4, 0, kind="resource")
        self.assertEqual({w.spin_color_index(*x) for x in product(range(2), range(4), range(2))}, set(range(16)))
        for mu, site in product(range(4), range(2)):
            link = w.color_link(mu, site)
            self.assertTrue(M(*link[0], *link[1]).is_unitary())
        bad = w.gamma_matrices()
        bad[0][0][0] = G(0, 1)
        self.assertFalse(w.clifford_relations(bad))
        bad = w.gamma_matrices()
        bad[0][0][2] = G(2)
        bad[0][2][0] = G(2)
        self.assertFalse(w.clifford_relations(bad))
        with patch.object(w, "gamma_matrices", return_value=bad):
            self.assertFalse(w.assembled_operator_checks())
        self.assertFalse(w.clifford_relations(w.gamma_matrices(), (1, 1, 1, 1)))
        # A nonunitary similarity preserves Clifford/chirality relations but
        # destroys Hermiticity, isolating that independent admission invariant.
        scale = (G(2), G(1), G(1), G(1))
        similar = [[[scale[i]*entry*scale[j].inv() for j, entry in enumerate(row)]
                    for i, row in enumerate(matrix)] for matrix in w.gamma_matrices()]
        self.assertFalse(w.clifford_relations(similar))
        operator = w.assembled_operator(Q(1, 2))
        operator[0][1] = operator[0][1] + G(1)
        self.assertFalse(w.gamma5_hermitian(operator))

    def test_wilson_operator_independent_block_construction(self) -> None:
        identity, zero = sp.eye(2), sp.zeros(2)
        pauli = (sp.Matrix([[0,1],[1,0]]), sp.Matrix([[0,-sp.I],[sp.I,0]]), sp.diag(1,-1))
        gamma = [sp.BlockMatrix([[zero, identity], [identity, zero]]).as_explicit()]
        gamma.extend(sp.BlockMatrix([[zero,-sp.I*sigma],[sp.I*sigma,zero]]).as_explicit()
                     for sigma in pauli)
        def link(mu: int, site: int) -> sp.Matrix:
            cosine, sine = (sp.Rational(3,5), sp.Rational(4,5)) if (mu+site)%2 else (sp.Rational(5,13), sp.Rational(12,13))
            phase = sp.Rational(3,5)+sp.I*sp.Rational(4,5) if site else 1
            return phase*sp.Matrix([[cosine,-sine],[sine,cosine]])
        for wilson in (Q(0), Q(1,2), Q(3,2)):
            blocks = [[(-1+4*wilson)*sp.eye(8) if s == t else sp.zeros(8)
                       for t in range(2)] for s in range(2)]
            for site, mu in product(range(2), range(4)):
                target = (site+1)%2 if mu == 0 else site
                blocks[site][target] += sp.kronecker_product((-wilson*sp.eye(4)+gamma[mu])/2, link(mu,site))
                blocks[site][target] += sp.kronecker_product((-wilson*sp.eye(4)-gamma[mu])/2, link(mu,target).H)
            expected = sp.BlockMatrix(blocks).as_explicit().applyfunc(sp.expand)
            actual = sp.Matrix([[sp.Rational(z.re)+sp.I*sp.Rational(z.im)
                                 for z in row] for row in w.assembled_operator(wilson)])
            self.assertEqual(actual, expected)

    @given(RATIONAL, RATIONAL)
    @settings(max_examples=25)
    @example(mass=Q(0), wilson=Q(0))
    @example(mass=Q(-2), wilson=Q(1))
    @example(mass=Q(-1), wilson=Q(1))
    @example(mass=Q(-3), wilson=Q(1))
    @example(mass=Q(-1), wilson=Q(0))
    @example(mass=Q(-2), wilson=Q(3))
    def test_wilson_determinant_independent_symbolic_elimination(self, mass: Q, wilson: Q) -> None:
        s, r = mass+2*wilson, wilson
        matrix = sp.Matrix([[s,0,-r,0,-r,0,0,0],[0,s,0,-r,0,-r,0,0],
                            [-r,0,s,0,0,0,0,1],[0,-r,0,s,0,0,1,0],
                            [-r,0,0,0,s,0,0,1],[0,-r,0,0,0,s,-1,0],
                            [0,0,0,-1,0,1,s,0],[0,0,-1,0,-1,0,0,s]])
        self.assertEqual(direct_wilson_determinant(mass, wilson), matrix.det(method="bareiss"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
