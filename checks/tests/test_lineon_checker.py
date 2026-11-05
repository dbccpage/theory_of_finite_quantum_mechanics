"""Path ownership, exact holonomy and finite receipt contracts for TFQ-1219.

AuthorityEffect: None. These tests do not establish a physical sign-free model.
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
from test_review_repairs import load, _collision_free
from checker_support.boundary import cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import Failure

STEM = "check_tfq_1219_fsp_hinge_lineon_sign_claim"
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)
HOPS = st.lists(st.tuples(st.integers(-1, 1), st.integers(-1, 1)), max_size=25)


class LineonCheckerTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object) -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        if result.error is None:
            self.fail("refusal has no typed failure")
        return result.error

    def test_refusal_helper_rejects_success(self) -> None:
        with self.assertRaises(AssertionError):
            self.refused(lambda: 0)

    @PROPERTY
    @given(first=st.integers(-100, 100), gap=st.integers(-3, 20), hops=HOPS)
    def test_path_order_against_site_and_edge_oracle(self, first: int, gap: int, hops: list[tuple[int, int]]) -> None:
        module = load(STEM)
        second = first + gap
        expected = gap > 0 and _collision_free(first, second, tuple(hops))
        path = module.LineonPath(first, second, hops)
        self.assertIs(path.preserves_order(), expected)
        self.assertIs(module.verify_1d_lineon_collision_avoidance(first, second, hops), expected)
        self.assertIs(module.verify_1d_lineon_collision_avoidance(first + 123, second + 123, hops), expected)
        if expected:
            self.assertEqual(module.compute_lineon_permutation_parity(first, second, hops), 0)
        else:
            self.assertEqual(self.refused(module.compute_lineon_permutation_parity, first, second, hops).kind, "input")

    def test_snapshot_ownership_and_validation_use_the_same_data(self) -> None:
        module = load(STEM)
        hops = [[1, 0], [0, -1]]
        path = module.LineonPath(0, 2, hops)
        hops[0][0] = -1
        hops.clear()
        self.assertEqual(path.hops, ((1, 0), (0, -1)))
        self.assertFalse(path.preserves_order())
        with self.assertRaises(FrozenInstanceError):
            path.first = 999
        trajectory = [0, 1, 1, 0]
        snapshot = module.validate_unit_trajectory(trajectory)
        trajectory.clear()
        self.assertEqual(snapshot, (0, 1, 1, 0))
        original_sequence = module.sequence
        colliding = [(1, -1)]
        def clear_after_snapshot(value: object, *args: object, **kwargs: object) -> object:
            result: object = original_sequence(value, *args, **kwargs)
            if value is colliding:
                colliding.clear()
            return result
        with patch.object(module, "sequence", side_effect=clear_after_snapshot):
            self.assertFalse(module.verify_1d_lineon_collision_avoidance(0, 1, colliding))
        left, right = [0, 1], [1, 0]
        def clear_trajectories(value: object, *args: object, **kwargs: object) -> object:
            result: object = original_sequence(value, *args, **kwargs)
            if value is left:
                left.clear()
            elif value is right:
                right.clear()
            return result
        with patch.object(module, "sequence", side_effect=clear_trajectories):
            self.assertEqual(module.verify_discrete_ivt_collision_site(0, 1, left, right), (True, 0))

    def test_path_domains_and_resource_extremes(self) -> None:
        module = load(STEM)
        for first, second, hops in ((True, 1, []), (0, 1.0, []), (0, 1, [(2, 0)]), (0, 1, [(0, -2)]),
                                    (0, 1, [(True, 0)]), (0, 1, [(0.5, 0)]), (0, 1, [(1,)]),
                                    (0, 1, [(1, 0, 0)]), (0, 1, "hops"), (0, 1, [None])):
            self.refused(module.LineonPath, first, second, hops)
        for initial in (2**4096, -(2**4096)):
            with patch.object(module, "sequence", side_effect=AssertionError("collection before position admission")):
                self.assertEqual(self.refused(module.verify_1d_lineon_collision_avoidance, initial, 1, []).kind, "resource")
        self.assertEqual(self.refused(module.LineonPath, 0, 1, [(0, 0)]*4097).kind, "resource")
        self.assertTrue(module.LineonPath(0, 1, [(0, 0)]*4096).preserves_order())
        maximum = 2**4096-1
        self.assertTrue(module.LineonPath(maximum-1, maximum, [(1, 1)]).preserves_order())
        self.assertTrue(module.LineonPath(-maximum, -maximum+1, []).preserves_order())
        # Validation precedes the mathematical false result for unordered input.
        self.refused(module.verify_1d_lineon_collision_avoidance, 2, 1, [(4, 0)])

    def test_unit_trajectory_and_ivt_input_refusals(self) -> None:
        module = load(STEM)
        for trajectory in ([0, 2], [0, -2], [True], [0.0], [2**4096], [0]*4097, "0,1"):
            self.refused(module.validate_unit_trajectory, trajectory)
        self.assertEqual(module.validate_unit_trajectory([]), ())
        for args in ((0, 1, [], []), (0, 1, [0], [1, 0]), (True, 1, [0, 1], [1, 0]),
                     (0, 2, [0, 2], [2, 0]), (0, 1, [0, 1], [1.0, 0]), (2**4096, 1, [0], [1])):
            self.refused(module.verify_discrete_ivt_collision_site, *args)

    def test_ivt_site_edge_and_nonexchange_witness_semantics(self) -> None:
        module = load(STEM)
        cases = [
            ((0, 2, [0, 1, 2], [2, 1, 0]), (True, 1)),
            ((0, 1, [0, 1], [1, 0]), (True, 0)),
            ((0, 1, [0, 1, 0, 1], [1, 0, 0, 0]), (True, 2)),
            ((0, 1, [0, 1, 0, 1], [1, 0, 1, 0]), (True, 0)),
            ((0, 1, [0, 0], [1, 1]), (False, -1)),
            ((1, 0, [1, 0], [0, 1]), (False, -1)),
            ((0, 0, [0], [0]), (False, -1)),
            ((0, 1, [1, 1], [0, 0]), (False, -1)),
            ((0, 2, [0, 1, 1], [2, 1, 1]), (False, -1)),
            ((0, 2, [1, 1, 2], [2, 1, 0]), (False, -1)),
            ((2, 0, [2, 1, 0], [0, 1, 2]), (False, -1)),
        ]
        for args, expected in cases:
            self.assertEqual(module.verify_discrete_ivt_collision_site(*args), expected)

    @PROPERTY
    @given(first=st.integers(-20, 20), gap=st.integers(1, 5), hops=HOPS)
    def test_ivt_generated_swaps_have_a_valid_witness(self, first: int, gap: int, hops: list[tuple[int, int]]) -> None:
        module = load(STEM)
        second = first+gap
        left, right = [first], [second]
        for a, b in hops:
            left.append(left[-1]+a)
            right.append(right[-1]+b)
        found, index = module.verify_discrete_ivt_collision_site(first, second, left, right)
        swapped = left[-1] == second and right[-1] == first
        self.assertIs(found, swapped)
        if found:
            self.assertGreaterEqual(index, 0)
            self.assertLess(index, len(left))
            site = left[index] == right[index]
            edge = index+1 < len(left) and (left[index]-right[index])*(left[index+1]-right[index+1]) < 0
            self.assertTrue(site or edge)
        else:
            self.assertEqual(index, -1)

    @PROPERTY
    @given(a=st.integers(-5, 5), b=st.integers(-5, 5), c=st.integers(-5, 5), d=st.integers(-5, 5))
    def test_commutator_against_symbolic_matrix_oracle(self, a: int, b: int, c: int, d: int) -> None:
        module = load(STEM)
        g, matrix = module.ComplexRat, module.Mat2x2
        u, v = g(Q(a, 5), Q(b, 7)), g(Q(c, 5), Q(d, 7))
        left, right = matrix(g(1), u, g(0), g(1)), matrix(g(1), g(0), v, g(1))
        actual = module.compute_commutator_holonomy_trace(left, right)
        su, sv = sp.Rational(a, 5)+sp.I*sp.Rational(b, 7), sp.Rational(c, 5)+sp.I*sp.Rational(d, 7)
        first, second = sp.Matrix([[1, su], [0, 1]]), sp.Matrix([[1, 0], [sv, 1]])
        expected = sp.expand(sp.trace(first*second*first.inv()*second.inv()))
        self.assertEqual(sp.Rational(actual.re.numerator, actual.re.denominator), sp.re(expected))
        self.assertEqual(sp.Rational(actual.im.numerator, actual.im.denominator), sp.im(expected))

    def test_matrix_boundaries_and_singular_inverse(self) -> None:
        module = load(STEM)
        eye = module.Mat2x2.eye()
        for invalid in (None, 1, [], object()):
            self.assertEqual(self.refused(module.compute_commutator_holonomy_trace, invalid, eye).kind, "input")
            self.assertEqual(self.refused(module.compute_commutator_holonomy_trace, eye, invalid).kind, "input")
        zero = module.ComplexRat(0)
        singular = module.Mat2x2(zero, zero, zero, zero)
        self.refused(module.compute_commutator_holonomy_trace, singular, eye)
        self.refused(module.compute_commutator_holonomy_trace, eye, singular)

    @PROPERTY
    @given(numerator=st.integers(-1000, 1000), denominator=st.integers(1, 40), corner=st.booleans(), nonabelian=st.booleans())
    def test_projection_mass_and_routing_are_literal_toy_rules(self, numerator: int, denominator: int, corner: bool, nonabelian: bool) -> None:
        module = load(STEM)
        trace = Q(numerator, denominator)
        actual = module.evaluate_foliated_projected_trace(corner, trace)
        self.assertEqual(actual, trace if corner else Q(numerator*numerator, denominator*denominator))
        self.assertIs(type(actual), Q)
        self.assertEqual(module.compute_defect_mass_phi1(trace), 2 if numerator < 0 else 0)
        table = {(False, False): "EXACT_REPAIR", (True, False): "OPEN_SIGN_OBSTRUCTION",
                 (False, True): "OPEN_SIGN_OBSTRUCTION", (True, True): "OPEN_SIGN_OBSTRUCTION"}
        self.assertEqual(module.evaluate_terminal_routing(corner, nonabelian), table[(corner, nonabelian)])

    def test_trace_and_flag_refusals_precede_branching(self) -> None:
        module = load(STEM)
        for bad in (0, 1, None, "yes", [], object()):
            self.refused(module.evaluate_foliated_projected_trace, bad, Q(1))
            self.refused(module.evaluate_terminal_routing, bad, False)
            self.refused(module.evaluate_terminal_routing, True, bad)
        for bad in (True, False, 0.1, "1", None, 2**4096):
            self.refused(module.compute_defect_mass_phi1, bad)
            self.refused(module.compute_curvature_gamma2, bad)
            self.refused(module.evaluate_foliated_projected_trace, True, bad)
            self.refused(module.evaluate_foliated_projected_trace, False, bad)
        for outside in (Q(-201, 100), Q(201, 100)):
            self.refused(module.compute_curvature_gamma2, outside)
        for value, expected in ((-2, sp.pi), (-1, 2*sp.pi/3), (0, sp.pi/2), (1, sp.pi/3), (2, sp.Integer(0))):
            self.assertEqual(module.compute_curvature_gamma2(Q(value)), expected)

    @PROPERTY
    @given(numerator=st.integers(-200, 200))
    def test_curvature_is_exact_bounded_symbolic_construction(self, numerator: int) -> None:
        module = load(STEM)
        value = Q(numerator, 100)
        result = module.compute_curvature_gamma2(value)
        self.assertFalse(result.has(sp.Float))
        if value.denominator == 1:
            expected = {-2: sp.pi, -1: 2*sp.pi/3, 0: sp.pi/2, 1: sp.pi/3, 2: sp.Integer(0)}
            self.assertEqual(result, expected[value.numerator])
        else:
            self.assertIs(result.func, sp.acos)
            self.assertEqual(result.args, (sp.Rational(value.numerator, 2*value.denominator),))
        with patch.object(module.sp, "acos", wraps=sp.acos) as operation:
            module.compute_curvature_gamma2(Q(1, 3))
            operation.assert_called_once_with(sp.Rational(1, 6), evaluate=False)

    @PROPERTY
    @given(statuses=st.lists(st.booleans(), max_size=20))
    def test_generated_case_accounting(self, statuses: list[bool]) -> None:
        module = load(STEM)
        def supplied(cases: Cases) -> None:
            for index, status in enumerate(statuses):
                cases.append((f"generated-{index}", status))
        with patch.object(module, "check_lineon_paths", supplied):
            result = module.run_checks()
        failures = [f"generated-{index}" for index, status in enumerate(statuses) if not status]
        self.assertEqual(result["total_checks"], 25+len(statuses))
        self.assertEqual(result["failed_checks"], len(failures))
        self.assertEqual(result["failures"], failures)
        self.assertIs(result["all_passed"], not failures)

    def test_default_receipt_and_sections_have_unique_exact_statuses(self) -> None:
        module = load(STEM)
        expected = {"record_id": "TFQ-1219", "dag_node": "FSP-HINGE-LINEON-SIGN-CLAIM", "authority_effect": "None",
                    "total_checks": 77, "failed_checks": 0, "failures": [], "all_passed": True}
        self.assertEqual(module.run_checks(), expected)
        self.assertEqual(module.run_checks(), expected)
        cases = Cases()
        module.check_lineon_paths(cases)
        self.assertEqual(len(cases), 52)
        positive, negative = module.check_holonomy_examples(cases)
        self.assertEqual(len(cases), 66)
        module.check_toy_projection_and_routing(cases, positive, negative)
        self.assertEqual(len(cases), 75)
        module.check_y_junction_convention(cases, positive)
        self.assertEqual(len(cases), 77)
        self.assertEqual(len({name for name, _ in cases}), 77)
        self.assertTrue(all(type(status) is bool and status for _, status in cases))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(cli(module.main), 0)
        self.assertEqual(json.loads(output.getvalue()), expected)

    def test_faults_fail_cli_and_preserve_cancellation(self) -> None:
        module = load(STEM)
        def failed(cases: Cases) -> None:
            cases.append(("injected", False))
        with patch.object(module, "check_lineon_paths", failed):
            result = module.run_checks()
            self.assertEqual(result["failures"], ["injected"])
            self.assertEqual(result["failed_checks"], 1)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli(module.main), 1)
        def duplicates(cases: Cases) -> None:
            cases.append(("same", True))
            cases.append(("same", False))
        with patch.object(module, "check_lineon_paths", duplicates):
            self.assertEqual(self.refused(module.run_checks).kind, "duplicate")
        with patch.object(module, "check_lineon_paths", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                cli(module.main)
        errors = io.StringIO()
        with patch.object(module, "check_lineon_paths", side_effect=OSError("injected")):
            with contextlib.redirect_stderr(errors):
                self.assertEqual(cli(module.main), 1)
        self.assertEqual(json.loads(errors.getvalue())["kind"], "resource")
        self.assertTrue(module.run_checks()["all_passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
