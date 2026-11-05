"""Contract, generated-property and failure tests for the four AdS checkers.

AuthorityEffect: None. Exact algebra and a supplied finite fixture are tested;
no continuum duality or physical identification follows from this evidence.
"""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from fractions import Fraction as Q
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from hypothesis import given, settings, strategies as st
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_review_repairs as regression
from test_review_repairs import load
from checker_support.boundary import cli, evaluate, Violation
from checker_support.cases import Cases
from checker_support.domains import Failure

FAMILY = ("ads-cft-duality-import", "ads-happy-toy-not-duality-gap",
          "ads-regge-area-rt-gap", "ads-rt-formula-import")
RATIONALS = st.fractions(min_value=-50, max_value=50, max_denominator=30)
NONNEGATIVE = st.fractions(min_value=0, max_value=50, max_denominator=30)
POSITIVE = st.fractions(min_value=Q(1, 50), max_value=50, max_denominator=50)
PROPERTIES = settings(max_examples=80, derandomize=True, deadline=None, database=None)


class AdsCheckerTests(unittest.TestCase):
    def refused(self, function: Callable[..., object], *args: object, kind: str = "input") -> None:
        result = evaluate(function, *args)
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("refusal lost its typed failure")
        self.assertEqual(result.error.kind, kind)

    def test_scalar_admission_every_parameter(self) -> None:
        cft, happy, regge, rt = (load(stem) for stem in FAMILY)
        functions = [
            (cft.gkpw_mass_sq, 2), (cft.shadow_dimension, 2), (cft.gkpw_discriminant, 2),
            (cft.bf_bound, 1), (cft.gkpw_root_plus, 2), (cft.gkpw_root_minus, 2),
            (happy.cft_renyi_factor, 1), (happy.stabilizer_renyi_factor, 1),
            (happy.renyi_spectrum_defect, 2), (regge.uniform_defect_regge_action, 2),
            (rt.rt_leading_entropy, 2), (rt.brown_henneaux_central_charge, 2),
            (rt.ads3_geodesic_length, 2), (rt.calabrese_cardy_coefficient, 1),
            (rt.cayley_menger_triangle_area_sq, 3), (rt.has_rational_square_root, 1),
        ]
        for function, arity in functions:
            for position in range(arity):
                for invalid in (True, False, 0.5, "1", None, complex(1)):
                    values: list[object] = [Q(1)] * arity
                    values[position] = invalid
                    with self.subTest(function=function.__name__, position=position, invalid=invalid):
                        self.refused(function, *values)
                values = [Q(1)] * arity
                values[position] = 1 << 4096
                self.refused(function, *values, kind="resource")
            result = function(*([1] * arity))
            self.assertIs(type(result), bool if function is rt.has_rational_square_root else Q)

    def test_positive_and_nonnegative_boundaries(self) -> None:
        happy, rt = load(FAMILY[1]), load(FAMILY[3])
        for value in (Q(0), Q(-1)):
            for function in (happy.cft_renyi_factor, happy.stabilizer_renyi_factor):
                self.refused(function, value)
            self.refused(happy.renyi_spectrum_defect, value, Q(1))
            self.refused(rt.rt_leading_entropy, Q(1), value)
            self.refused(rt.brown_henneaux_central_charge, value, Q(1))
            self.refused(rt.brown_henneaux_central_charge, Q(1), value)
            self.refused(rt.ads3_geodesic_length, value, Q(1))
        self.refused(happy.renyi_spectrum_defect, Q(2), Q(-1))
        self.refused(rt.rt_leading_entropy, Q(-1), Q(1))
        self.refused(rt.ads3_geodesic_length, Q(1), Q(-1))
        self.refused(rt.calabrese_cardy_coefficient, Q(-1))
        self.refused(rt.has_rational_square_root, Q(-1))
        self.assertEqual(rt.rt_leading_entropy(0, 1), 0)
        self.assertEqual(rt.ads3_geodesic_length(1, 0), 0)
        self.assertEqual(rt.calabrese_cardy_coefficient(0), 0)
        self.assertEqual(happy.renyi_spectrum_defect(2, 0), 0)

    @PROPERTIES
    @given(d=RATIONALS, delta=RATIONALS, signed_root=RATIONALS)
    def test_gkpw_exact_polynomial_and_signed_roots(self, d: Q, delta: Q, signed_root: Q) -> None:
        module = load(FAMILY[0])
        mass = module.gkpw_mass_sq(d, delta)
        # Independent completed-square representation, including negative d and s.
        self.assertEqual(mass, (delta - d/2)**2 - d*d/4)
        self.assertEqual(module.shadow_dimension(d, delta), d-delta)
        self.assertEqual(module.bf_bound(d), -(d/2)**2)
        self.assertEqual(module.gkpw_discriminant(d, mass), (2*delta-d)**2)
        plus = module.gkpw_root_plus(d, signed_root)
        minus = module.gkpw_root_minus(d, signed_root)
        self.assertEqual(plus+minus, d)
        self.assertEqual(plus-minus, signed_root)
        expected_mass = (signed_root*signed_root-d*d)/4
        self.assertEqual(module.gkpw_mass_sq(d, plus), expected_mass)
        self.assertEqual(module.gkpw_mass_sq(d, minus), expected_mass)

    @PROPERTIES
    @given(order=POSITIVE, entropy=NONNEGATIVE)
    def test_renyi_signed_defect(self, order: Q, entropy: Q) -> None:
        module = load(FAMILY[1])
        self.assertEqual(module.cft_renyi_factor(order)*2*order, order+1)
        self.assertEqual(module.stabilizer_renyi_factor(order), 1)
        self.assertEqual(module.renyi_spectrum_defect(order, entropy), (order-1)*entropy/(2*order))
        self.assertEqual(module.renyi_spectrum_defect(order, Q(0)), 0)

    @PROPERTIES
    @given(area=NONNEGATIVE, subdivisions=st.integers(min_value=1, max_value=128), curvature=RATIONALS)
    def test_subdivision_and_regge_action(self, area: Q, subdivisions: int, curvature: Q) -> None:
        module = load(FAMILY[2])
        pieces = [area/subdivisions for _ in range(subdivisions)]
        self.assertEqual(module.linear_area_subdivision_sum(area, subdivisions), sum(pieces, Q(0)))
        square_sum = sum((piece*piece for piece in pieces), Q(0))
        self.assertEqual(module.sq_area_subdivision_sum(area, subdivisions), square_sum)
        self.assertEqual(module.sq_area_subdivision_defect(area, subdivisions), area*area-square_sum)
        self.assertEqual(module.uniform_defect_regge_action(area*area, curvature), area*area*curvature)
        # The algebraic action admits signed coefficients, like the formal definition.
        self.assertEqual(module.uniform_defect_regge_action(-area, curvature), -area*curvature)

    def test_subdivision_rejects_invalid_domain_and_budget(self) -> None:
        module = load(FAMILY[2])
        for function in (module.linear_area_subdivision_sum, module.sq_area_subdivision_sum,
                         module.sq_area_subdivision_defect):
            unadmitted = MagicMock()
            unadmitted.__mul__.side_effect = RuntimeError("arithmetic before admission")
            self.refused(function, unadmitted, 2)
            unadmitted.__mul__.assert_not_called()
            for invalid in (True, 0.5, "1", Q(-1), None):
                self.refused(function, invalid, 2)
            for invalid in (True, 0.5, "1", 0, -1, Q(2), None):
                self.refused(function, Q(1), invalid)
            self.refused(function, 1 << 4096, 2, kind="resource")
            self.refused(function, Q(1), 1 << 4096, kind="resource")
            self.assertIs(type(function(1, 2)), Q)
        self.assertEqual(module.linear_area_subdivision_sum(1, 1 << 4095), 1)
        self.assertEqual(module.sq_area_subdivision_sum(1, 1 << 4095), Q(1, 1 << 4095))

    @PROPERTIES
    @given(radius=POSITIVE, newton=POSITIVE, log_factor=NONNEGATIVE, area=NONNEGATIVE)
    def test_rt_coupling_properties(self, radius: Q, newton: Q, log_factor: Q, area: Q) -> None:
        module = load(FAMILY[3])
        central = module.brown_henneaux_central_charge(radius, newton)
        geodesic = module.ads3_geodesic_length(radius, log_factor)
        self.assertEqual(central*2*newton, 3*radius)
        self.assertEqual(geodesic, 2*radius*log_factor)
        self.assertEqual(module.rt_leading_entropy(geodesic, newton), central*log_factor/3)
        self.assertEqual(module.calabrese_cardy_coefficient(central), central/3)
        self.assertEqual(module.rt_leading_entropy(area, newton)*4*newton, area)

    @settings(max_examples=35, derandomize=True, deadline=None, database=None)
    @given(a=RATIONALS, b=RATIONALS, c=RATIONALS)
    def test_cayley_menger_against_determinant(self, a: Q, b: Q, c: Q) -> None:
        module = load(FAMILY[3])
        determinant = sp.Matrix([[0, 1, 1, 1], [1, 0, a, b], [1, a, 0, c], [1, b, c, 0]]).det()
        self.assertEqual(module.cayley_menger_triangle_area_sq(a, b, c), -determinant/16)
        # Signed non-geometric squared distances are polynomial inputs, not geometry certificates.
        self.assertEqual(module.cayley_menger_triangle_area_sq(0, 0, 1), Q(-1, 16))
        self.assertEqual(module.cayley_menger_triangle_area_sq(1, 1, 2), Q(1, 4))

    @PROPERTIES
    @given(numerator=st.integers(min_value=0, max_value=1000), denominator=st.integers(min_value=1, max_value=1000))
    def test_square_certificate(self, numerator: int, denominator: int) -> None:
        module = load(FAMILY[3])
        square = Q(numerator, denominator)**2
        self.assertTrue(module.has_rational_square_root(square))
        if numerator:
            self.assertFalse(module.has_rational_square_root(2*square))
        self.assertFalse(module.has_rational_square_root(Q(3, 4)))
        self.assertFalse(module.has_rational_square_root(Q(1, 2)))

    def test_runtime_counts_and_repeatable_reports(self) -> None:
        original = Cases.require
        for stem, expected in zip(FAMILY, (829, 499, 553, 528)):
            module = load(stem)
            outputs = []
            for _ in range(2):
                observed: list[str] = []
                def counted(run: Cases, condition: bool, message: str) -> None:
                    observed.append(message)
                    original(run, condition, message)
                output = io.StringIO()
                with patch.object(Cases, "require", counted), contextlib.redirect_stdout(output):
                    self.assertEqual(module.main(), 0)
                self.assertEqual(len(observed), expected, stem)
                self.assertIn(f"checks={len(observed)} ", output.getvalue())
                outputs.append(output.getvalue())
            self.assertEqual(outputs[0], outputs[1])

    def test_failed_obligation_is_a_nonzero_railway_cli(self) -> None:
        for stem in FAMILY:
            module = load(stem)
            output, errors = io.StringIO(), io.StringIO()
            with patch.object(Cases, "require", side_effect=Violation("check", "injected obligation")):
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                    self.assertEqual(cli(module.main), 1)
            self.assertEqual(output.getvalue(), "")
            self.assertEqual(json.loads(errors.getvalue())["kind"], "check")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(module.main(), 0)

    def test_fixture_mismatch_refusals(self) -> None:
        module = load(FAMILY[1])
        with patch.object(module, "interval_mincut", return_value=0):
            self.refused(module.check_interval_census, Cases(), kind="check")
        self.refused(module.check_mutual_information_and_codimension, Cases(), [], kind="input")
        module = load(FAMILY[2])
        with patch.object(module, "interval_mincut", return_value=9):
            self.refused(module.check_supplied_carrier_counts, Cases(), kind="check")
        self.refused(module.check_defect_weighting, True, Cases())
        self.refused(module.check_defect_weighting, 1 << 4096, Cases(), kind="resource")
        self.refused(module.check_defect_weighting, Q(1), Cases(), kind="check")
        module = load(FAMILY[3])
        with patch.object(module, "interval_entropy", return_value=0):
            self.refused(module.check_scaling_and_complements, Cases(), kind="check")
        for start, length, kind in ((True, 1, "input"), (-1, 1, "input"),
                                    (20, 1, "resource"), (0, -1, "input"), (0, 21, "resource")):
            self.refused(module.interval_entropy, start, length, kind=kind)

    def test_loader_restores_modules_on_success_failure_and_cancellation(self) -> None:
        stem = FAMILY[0]
        name = "reviewed_"+stem.replace("-", "_")
        marker = ModuleType(name)
        def inspect_registration(loader: importlib.machinery.SourceFileLoader, module: ModuleType) -> None:
            self.assertIs(sys.modules[module.__name__], module)
        with patch.dict(sys.modules):
            sys.modules.pop(name, None)
            with patch.object(importlib.machinery.SourceFileLoader, "exec_module", inspect_registration):
                self.assertEqual(load(stem).__name__, name)
            self.assertNotIn(name, sys.modules)
            with patch.object(importlib.machinery.SourceFileLoader, "exec_module", side_effect=OSError("unreadable")):
                with self.assertRaises(OSError):
                    load(stem)
            self.assertNotIn(name, sys.modules)
        with patch.dict(sys.modules, {name: marker}):
            self.assertIsNot(load(stem), marker)
            self.assertIs(sys.modules[name], marker)
            for error in (OSError("unreadable"), RuntimeError("broken import"), KeyboardInterrupt()):
                with patch.object(importlib.machinery.SourceFileLoader, "exec_module", side_effect=error):
                    with self.assertRaises(type(error)):
                        load(stem)
                self.assertIs(sys.modules[name], marker)
        for invalid in ("../escape", "", "missing", True):
            self.refused(load, invalid)
        with patch.object(importlib.util, "spec_from_file_location", return_value=None):
            self.refused(load, stem, kind="resource")
        empty_spec = importlib.machinery.ModuleSpec(name, None)
        with patch.object(importlib.util, "spec_from_file_location", return_value=empty_spec):
            self.refused(load, stem, kind="resource")

    def test_silent_preserves_result_and_propagates_error(self) -> None:
        def operation(value: int, *, offset: int = 0) -> int:
            print("captured")
            print("also captured", file=sys.stderr)
            return value+offset
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(regression.silent(operation, 2, offset=3), 5)
            with self.assertRaises(ZeroDivisionError):
                regression.silent(lambda: 1/0)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")

    def test_refusal_helpers_cannot_accept_success_or_wrong_failure(self) -> None:
        with self.assertRaises(AssertionError):
            self.refused(lambda: 3)
        with self.assertRaises(AssertionError):
            self.refused(lambda: 1/0, kind="resource")
        original_suite = regression.ReviewedCheckerRegressionTests()
        with self.assertRaises(AssertionError):
            original_suite.refused(lambda: 3)
        failure = original_suite.refused(lambda: 1/0)
        self.assertEqual(failure.kind, "input")
        inconsistent = SimpleNamespace(ok=True, value=None, error=Failure("input", "inconsistent success"))
        with patch(__name__+".evaluate", return_value=inconsistent):
            with self.assertRaises(AssertionError):
                self.refused(lambda: None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
