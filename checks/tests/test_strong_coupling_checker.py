"""Exact arithmetic, resource and receipt contracts for the finite TFQ-1052 checker.

AuthorityEffect: None. Supplied group tables remain conditional data.
"""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
import io
import json
from math import factorial
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from hypothesis import given, settings, strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_review_repairs import load
from checker_support.boundary import cli, evaluate
from checker_support.domains import Failure

STEM = "check_tfq_1052_fqcd_strong_coupling_area_law"
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)


class StrongCouplingCheckerTests(unittest.TestCase):
    def refused(self, operation: Callable[..., object], *args: object) -> Failure:
        result = evaluate(lambda: operation(*args))
        self.assertFalse(result.ok)
        if result.error is None:
            self.fail("refusal has no typed error")
        return result.error

    def test_refusal_assertion_requires_actual_failure(self) -> None:
        with self.assertRaises(AssertionError):
            self.refused(lambda: 1)

    @PROPERTY
    @given(n=st.integers(2, 24), d=st.integers(2, 12), left=st.integers(1, 30), top=st.integers(1, 30))
    def test_geometry_and_thresholds(self, n: int, d: int, left: int, top: int) -> None:
        module = load(STEM)
        directions = [(a, b, sign) for a in range(d) for b in range(d) if a != b for sign in (-1, 1)]
        self.assertEqual(module.delta_coordination(d), len(directions))
        self.assertEqual(module.spanning_area(left, top), sum(left for _ in range(top)))
        self.assertEqual(module.perimeter(left, top), sum((left, top, left, top)))
        lower, upper = module.beta0_rational_bounds(n, d)
        # Independent factorial series encloses e more tightly than the fixture bounds.
        e_low = sum((Q(1, factorial(k)) for k in range(13)), Q(0))
        e_high = e_low + Q(1, 12 * factorial(12))
        factor = 40 * len(directions) * (n - 1)
        self.assertLess(lower, 1 / (factor * e_high))
        self.assertLess(1 / (factor * e_low), upper)
        self.assertEqual(module.beta0_rational_midpoint(n, d), (lower + upper) / 2)
        self.assertEqual(module.normal_directions(d + 1), len([1 for _ in range(d - 1) for _ in (-1, 1)]))

    @PROPERTY
    @given(numerator=st.integers(0, 19), area=st.integers(1, 20))
    def test_cluster_series_recurrence_and_partial_sums(self, numerator: int, area: int) -> None:
        module = load(STEM)
        mu = Q(numerator, 20)
        tail = module.cluster_sum_rational(mu, area)
        self.assertIs(type(tail), Q)
        self.assertEqual(tail, mu ** area + mu * tail)
        partial = sum((mu ** k for k in range(area, area + 12)), Q(0))
        self.assertLessEqual(partial, tail)
        self.assertEqual(module.area_law_bound_rational(area), Q(1, 4) ** area)
        self.assertLessEqual(module.cluster_sum_rational(Q(1, 5), area), module.area_law_bound_rational(area))

    @PROPERTY
    @given(dim=st.integers(1, 12), numerator=st.integers(-10, 10), area=st.integers(1, 12))
    def test_decimation_and_collar_products(self, dim: int, numerator: int, area: int) -> None:
        module = load(STEM)
        activity = Q(numerator, 13)
        expected = activity
        for _ in range(area - 1):
            expected = expected * activity / dim
        self.assertEqual(module.twod_decimation_rational(dim, activity, area), expected)
        contraction = Q(1)
        for _ in range(area):
            contraction /= dim
        self.assertEqual(module.general_collar_contraction_rational(dim, area), contraction)
        self.assertEqual(module.collar_contraction_rational(area), Q(1, 2) ** area)
        self.assertEqual(module.general_collar_contraction_rational(dim, 0), 1)
        self.assertEqual(module.collar_contraction_rational(0), 1)

    @PROPERTY
    @given(perimeter=st.integers(1, 6), width=st.integers(1, 4), dim=st.integers(2, 7), numerator=st.integers(1, 5))
    def test_multi_plaquette_bound_from_repeated_factors(self, perimeter: int, width: int, dim: int, numerator: int) -> None:
        module = load(STEM)
        beta = Q(numerator, 11)
        expected = Q(1)
        for _ in range(perimeter):
            expected *= 4
            for _ in range(width):
                expected *= beta * beta * beta / (dim * dim)
        self.assertEqual(module.d4_multi_plaquette_collar_bound(perimeter, width, dim, beta), expected)

    @PROPERTY
    @given(t=st.integers(-20, 20), charge=st.integers(-25, 25))
    def test_theta_phase_against_linear_complex_products(self, t: int, charge: int) -> None:
        module = load(STEM)
        c, s = Q(1-t*t, 1+t*t), Q(2*t, 1+t*t)
        re, im = Q(1), Q(0)
        sign = -1 if charge >= 0 else 1
        for _ in range(abs(charge)):
            re, im = re*c-im*sign*s, re*sign*s+im*c
        actual = module.theta_phase(c, s, charge)
        self.assertEqual(actual, (re, im))
        self.assertTrue(all(type(value) is Q for value in actual))
        self.assertEqual(actual[0]**2 + actual[1]**2, 1)
        self.assertEqual(module.theta_phase(c, s, -charge), (re, -im))

    @PROPERTY
    @given(a=st.integers(-10, 10).filter(lambda value: value != 0), c=st.integers(-9, 9), b=st.integers(-9, 9))
    def test_modified_chirality_square_for_nonunit_inputs(self, a: int, c: int, b: int) -> None:
        module = load(STEM)
        radius_squared = Q(c*c, 25) + Q(b*b, 49)
        self.assertEqual(module.direct_modified_chirality_square(Q(a, 3), Q(c, 5), Q(b, 7)),
                         [[radius_squared, 0], [0, radius_squared]])

    def test_all_arithmetic_input_boundaries(self) -> None:
        module = load(STEM)
        calls: list[tuple[str, tuple[object, ...]]] = [
            ("delta_coordination", (1,)), ("delta_coordination", (True,)), ("delta_coordination", (4097,)),
            ("beta0_rational_bounds", (1, 2)), ("beta0_rational_bounds", (2, False)),
            ("beta0_rational_midpoint", (2, 4097)), ("spanning_area", (0, 1)), ("perimeter", (1, 1.0)),
            ("cluster_sum_rational", (-1, 1)), ("cluster_sum_rational", (1, 1)),
            ("cluster_sum_rational", (Q(1, 2), 0)), ("cluster_sum_rational", (0.1, 2)),
            ("area_law_bound_rational", (True,)), ("area_law_bound_rational", (4097,)),
            ("collar_contraction_rational", (-1,)), ("general_collar_contraction_rational", (0, 1)),
            ("general_collar_contraction_rational", (2, 4097)), ("twod_decimation_rational", (0, Q(1), 1)),
            ("twod_decimation_rational", (2, Q(1), 0)), ("twod_decimation_rational", (2, 0.1, 2)),
            ("normal_directions", (2,)), ("normal_directions", (4097,)),
            ("d4_multi_plaquette_collar_bound", (0, 1, 2, Q(1))),
            ("d4_multi_plaquette_collar_bound", (1, 0, 2, Q(1))),
            ("d4_multi_plaquette_collar_bound", (1, 1, 1, Q(1))),
            ("d4_multi_plaquette_collar_bound", (1, 1, 2, 0)),
            ("d4_multi_plaquette_collar_bound", (1, 1, 2, -1)),
            ("theta_phase", (1, 1, 2)), ("theta_phase", (1, 0, True)), ("theta_phase", (1, 0, -4097)),
            ("theta_phase", (1, 0, 4097)), ("theta_phase", (0.0, 1, 1)),
            ("direct_modified_chirality_square", (0, 1, 0)), ("direct_modified_chirality_square", (False, 1, 0)),
            ("direct_modified_chirality_square", (0.1, 1, 0)), ("direct_modified_chirality_square", (1, 1.0, 0)),
        ]
        for name, args in calls:
            with self.subTest(name=name, args=args):
                self.refused(getattr(module, name), *args)
        with patch.object(Q, "__pow__", side_effect=AssertionError("unit ratio reached arithmetic")):
            self.assertEqual(self.refused(module.cluster_sum_rational, 1, 1).kind, "input")
        self.assertEqual(module.delta_coordination(4096), 33546240)
        self.assertEqual(module.theta_phase(0, 1, 4096), (1, 0))
        self.assertEqual(module.theta_phase(0, 1, -4096), (1, 0))
        self.assertEqual(module.cluster_sum_rational(0, 4096), 0)
        self.assertEqual(module.twod_decimation_rational(1, -1, 4096), 1)
        self.assertEqual(module.perimeter(4096, 4096), 16384)

    def test_combined_power_budget_precedes_arithmetic(self) -> None:
        module = load(STEM)
        self.assertIsNone(module._power_budget(65536))
        self.assertEqual(self.refused(module._power_budget, 65537).kind, "resource")
        calls = ((module.cluster_sum_rational, (Q(1, 2**100), 4096)),
                 (module.twod_decimation_rational, (4096, Q(1, 2**100), 4096)),
                 (module.d4_multi_plaquette_collar_bound, (4096, 4096, 4096, Q(1, 2**100))))
        with patch.object(Q, "__pow__", side_effect=AssertionError("power executed before budget")):
            for operation, args in calls:
                self.assertEqual(self.refused(operation, *args).kind, "resource")
        t = 2**100
        with patch.object(module, "_complex_power", side_effect=AssertionError("complex power before budget")):
            self.assertEqual(self.refused(module.theta_phase, Q(1-t*t, 1+t*t), Q(2*t, 1+t*t), 4096).kind, "resource")

    @PROPERTY
    @given(values=st.lists(st.integers(0, 100), min_size=1, max_size=12))
    def test_invariant_table_snapshots_and_accessor_separation(self, values: list[int]) -> None:
        module = load(STEM)
        scalars: list[list[object]] = [[str(index), value] for index, value in enumerate(values)]
        intervals: list[list[object]] = [["interval", [Q(1, 3), Q(2, 3)]]]
        table = module.SubgroupInvariantTable(scalars, intervals)
        scalars[0][1] = -999
        intervals.clear()
        for index, value in enumerate(values):
            self.assertEqual(table.value(str(index)), value)
            self.assertIs(type(table.value(str(index))), Q)
        self.assertEqual(table.bounds("interval"), (Q(1, 3), Q(2, 3)))
        self.refused(table.value, "interval")
        self.refused(table.bounds, "0")
        with self.assertRaises(FrozenInstanceError):
            table.scalars = ()

    def test_invariant_table_refusals(self) -> None:
        module = load(STEM)
        cases: list[tuple[object, object]] = [
            ((), ()), ((("x", -1),), ()), ((("x", 0.5),), ()), (((False, 1),), ()),
            ((("", 1),), ()), ((("x"*129, 1),), ()), ((("x", 1, 2),), ()),
            ((("x", 1), ("x", 2)), ()), ((("x", 1),), (("x", (0, 1)),)),
            ((), (("x", (1, 1)),)), ((), (("x", (2, 1)),)), ((), (("x", (-1, 1)),)),
            ((), (("x", (0, True)),)), ((), (("x", (0, 1, 2)),)),
            (tuple((str(i), 1) for i in range(33)), ()), ("x", ()), ((), "x"),
        ]
        for scalars, intervals in cases:
            self.refused(module.SubgroupInvariantTable, scalars, intervals)
        table = module.SubgroupInvariantTable((("x", 1),), ())
        self.refused(table.value, None)
        self.refused(table.bounds, None)
        for scalars, intervals in (((('x', 1), ('x', 2)), ()), ((("x", 1),), (("x", (0, 1)),))):
            self.assertEqual(self.refused(module.SubgroupInvariantTable, scalars, intervals).kind, "duplicate")

    def test_supplied_tables_keep_exact_known_values(self) -> None:
        module = load(STEM)
        expected = {
            "s4_cubic_invariants_rational": {"3": 1, "3_prime": 1, "2": 1, "sgn": 0},
            "a5_cubic_invariants_rational": {"3_a": 1, "3_b": 1, "4": 1, "5": 2},
            "binary_icosahedral_2i_invariants_rational": {"2_s": 0, "2_s_prime": 0, "4_s": 0, "6_s": 0, "3_a": 1, "3_b": 1, "4_t": 1, "5_t": 2},
            "valentiner_sigma1080_invariants_rational": {"I11_3a": 1, "I2_3a": 0, "I3_3a": 1, "I3_5a": 1, "I3_8a": 2, "I3_10": 2},
        }
        for name, values in expected.items():
            actual = getattr(module, name)()
            self.assertEqual(actual, values)
            self.assertTrue(all(type(value) is Q for value in actual.values()))
        su2, su3 = module.su2_ade_binary_polyhedral_tower_rational(), module.su3_subgroup_tower_and_freezing_scales_rational()
        self.assertEqual((len(su2.scalars), len(su2.intervals), len(su3.scalars), len(su3.intervals)), (6, 2, 7, 2))
        self.assertEqual(dict(su2.scalars), {"I3_2T_2s": 0, "I3_2T_3t": 2, "I3_2O_2s": 0,
                                          "I3_2O_3": 1, "delta_min_Q8": 1, "delta_min_2T": Q(1, 2)})
        self.assertEqual(dict(su3.scalars), {"I3_Delta27_3": 3, "I3_Delta54_3_1": 1, "I3_Delta54_3_2": 2,
                                          "delta_min_Delta27": 1, "delta_min_Delta54": Q(5, 6),
                                          "beta_freeze_proxy_Delta27": 1, "beta_freeze_proxy_Delta54": Q(6, 5)})
        self.assertEqual(su2.bounds("delta_min_2I_bounds"), (Q(3, 16), Q(1, 5)))
        self.assertEqual(su3.bounds("delta_min_Sigma1080_bounds"), (Q(11, 24), Q(7, 15)))
        low, high = su3.bounds("beta_freeze_proxy_Sigma1080_bounds")
        self.assertEqual((low, high), (Q(15, 7), Q(24, 11)))

    @PROPERTY
    @given(statuses=st.lists(st.booleans(), max_size=12))
    def test_receipt_counts_every_generated_case(self, statuses: list[bool]) -> None:
        module = load(STEM)
        def supplied(record: Callable[[bool, str], None]) -> None:
            for index, status in enumerate(statuses):
                record(status, f"generated-{index}")
        with patch.object(module, "check_coordination", supplied):
            result = module.run_checks()
        failed = [f"generated-{i}" for i, status in enumerate(statuses) if not status]
        self.assertEqual(result["total_checks"], 241 + len(statuses))
        self.assertEqual(result["failures"], failed)
        self.assertEqual(result["failed_checks"], len(failed))
        self.assertIs(result["all_passed"], not failed)

    def test_default_receipt_cli_and_direct_oracle_faults(self) -> None:
        module = load(STEM)
        expected = {"record_id": "TFQ-1052", "dag_node": "FQCD-STRONG-COUPLING-AREA-LAW", "authority_effect": "None",
                    "total_checks": 250, "failed_checks": 0, "failures": [], "all_passed": True}
        self.assertEqual(module.run_checks(), expected)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(cli(module.main), 0)
        self.assertEqual(json.loads(output.getvalue()), expected)
        with patch.object(module, "direct_wilson_determinant", return_value=Q(987654321)):
            receipt = module.run_checks()
            self.assertEqual(receipt["total_checks"], 250)
            self.assertEqual(receipt["failed_checks"], 31)
            self.assertFalse(receipt["all_passed"])
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli(module.main), 1)

    def test_railway_faults_and_recorder_errors_are_not_swallowed(self) -> None:
        module = load(STEM)
        def duplicates(record: Callable[[bool, str], None]) -> None:
            record(True, "same")
            record(False, "same")
        with patch.object(module, "check_coordination", duplicates):
            self.assertEqual(self.refused(module.run_checks).kind, "duplicate")
        def malformed(record: Callable[..., None]) -> None:
            record(1, "truthy")
        with patch.object(module, "check_coordination", malformed):
            self.assertEqual(self.refused(module.run_checks).kind, "input")
        def broken_recorder(condition: bool, description: str) -> None:
            if description == "delta_coordination(1) refused":
                raise ValueError("recorder error")
        with self.assertRaisesRegex(ValueError, "recorder error"):
            module.check_coordination(broken_recorder)
        original_coordination = module.delta_coordination
        def rejects_failed_check(condition: bool, description: str) -> None:
            if not condition:
                raise ValueError("failed-check recorder error")
        with patch.object(module, "delta_coordination", side_effect=lambda d: 2 if d == 1 else original_coordination(d)):
            with self.assertRaisesRegex(ValueError, "failed-check recorder error"):
                module.check_coordination(rejects_failed_check)
        with patch.object(module, "check_theta_fixture", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                cli(module.main)
        errors = io.StringIO()
        with patch.object(module, "check_theta_fixture", side_effect=OSError("injected")):
            with contextlib.redirect_stderr(errors):
                self.assertEqual(cli(module.main), 1)
        self.assertEqual(json.loads(errors.getvalue())["kind"], "resource")
        self.assertTrue(module.run_checks()["all_passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
