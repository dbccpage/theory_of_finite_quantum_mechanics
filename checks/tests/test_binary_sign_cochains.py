"""Independent Boolean cochain oracle and finite enumeration. AuthorityEffect: None."""
from __future__ import annotations

import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction
import importlib.util
import io
from itertools import product
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from typing import TypeVar
import unittest
from unittest.mock import patch

from hypothesis import given, settings, strategies as st

CHECKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHECKS))
from checker_support.binary_sign_cochain import BinarySignCochain as Cochain
from checker_support.boundary import Violation, evaluate
from checker_support.cases import Cases
from checker_support.outcome import Outcome

APP = CHECKS/"independent/fsp-bf-2group-sign-claim.py"
PROPERTY = settings(max_examples=80, derandomize=True, deadline=None, database=None)
SIGNS = st.lists(st.sampled_from((-1, 1)), min_size=8, max_size=8)
T = TypeVar("T")


def load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("reviewed_sign_cocycle_controls", APP)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load sign controls")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


def exponent_table(phases: tuple[int, ...], degree: int) -> dict[tuple[int, ...], int]:
    return dict(zip(product((0, 1), repeat=degree), (int(value == -1) for value in phases)))


def boundary_bits(phases: tuple[int, ...]) -> tuple[int, ...]:
    beta = exponent_table(phases, 2)
    return tuple((beta[b, c]+beta[(a+b) % 2, c]+beta[a, (b+c) % 2]+beta[a, b]) % 2
                 for a, b, c in product((0, 1), repeat=3))


def pentagon_bits(phases: tuple[int, ...]) -> tuple[int, ...]:
    omega = exponent_table(phases, 3)
    return tuple((omega[b, c, d]+omega[(a+b) % 2, c, d]+omega[a, (b+c) % 2, d]
                  +omega[a, b, (c+d) % 2]+omega[a, b, c]) % 2
                 for a, b, c, d in product((0, 1), repeat=4))


class BinaryCochainTests(unittest.TestCase):
    def refused(self, result: Outcome[T], kind: str = "input") -> None:
        self.assertIsNotNone(result.error)
        if result.error is None:
            self.fail("Expected a typed refusal")
        self.assertEqual(result.error.kind, kind)

    def test_all_degree_two_boundaries_against_boolean_oracle(self) -> None:
        image = set()
        normalized = []
        for phases in product((-1, 1), repeat=4):
            cochain = Cochain(2, phases)
            self.assertEqual(cochain.is_normalized(), phases[:3] == (1, 1, 1))
            result = cochain.coboundary()
            self.assertIsNone(result.error)
            self.assertIsNotNone(result.value)
            if result.value is None:
                self.fail("Missing boundary value")
            expected = tuple(1-2*bit for bit in boundary_bits(phases))
            self.assertEqual(result.value.phases, expected)
            self.assertTrue(all(value == 0 for value in pentagon_bits(result.value.phases)))
            image.add(result.value.phases)
            if cochain.is_normalized():
                normalized.append(cochain)
                self.assertEqual(result.value.at((1, 1, 1)).value, 1)
        self.assertEqual(len(normalized), 2)
        self.assertEqual(len(image), 4)
        self.assertNotIn(Cochain.generator().phases, image)

    def test_all_degree_three_cochains_and_pentagon_points(self) -> None:
        closed = 0
        normalized = 0
        points = tuple(product((0, 1), repeat=4))
        for phases in product((-1, 1), repeat=8):
            cochain = Cochain(3, phases)
            self.assertEqual(cochain.is_normalized(), phases[:7] == (1,)*7)
            expected = pentagon_bits(phases)
            actual = tuple(cochain.pentagon(point).value for point in points)
            self.assertEqual(actual, tuple(1-2*bit for bit in expected))
            closed += all(value == 0 for value in expected)
            normalized += cochain.is_normalized()
        self.assertEqual((closed, normalized), (8, 2))

    @PROPERTY
    @given(st.sampled_from((2, 3)), SIGNS, SIGNS, SIGNS)
    def test_generated_point_order_products_and_owned_snapshots(self, degree: int, first: list[int],
                                                               second: list[int], third: list[int]) -> None:
        phases = first[:2**degree]
        cochain = Cochain(degree, phases)
        reference = dict(zip(product((0, 1), repeat=degree), phases))
        phases[0] *= -1
        for point, value in reference.items():
            self.assertEqual(cochain.at(point).value, value)
        other, last = Cochain(degree, second[:2**degree]), Cochain(degree, third[:2**degree])
        result = cochain.multiply(other)
        self.assertIsNone(result.error)
        if result.value is None:
            self.fail("Missing product value")
        expected = tuple(1-2*((int(a == -1)+int(b == -1)) % 2)
                         for a, b in zip(cochain.phases, other.phases))
        self.assertEqual(result.value.phases, expected)
        self.assertEqual(result.value.multiply(last).value, cochain._multiply(other._multiply(last)))
        self.assertEqual(cochain.multiply(cochain).value, Cochain(degree, (1,)*(2**degree)))
        with self.assertRaises(FrozenInstanceError):
            cochain.degree = 3  # type: ignore[misc]

    def test_exact_degrees_signs_and_shapes(self) -> None:
        for degree in (True, 2.0, Fraction(2), "2", None, 0, 1):
            self.refused(evaluate(Cochain, degree, (1,)*4))
        for oversized_degree in (4, 1 << 4096):
            self.refused(evaluate(Cochain, oversized_degree, (1,)*4), "resource")
        for phases in (None, (), (1,)*3, (1,)*5, (True, 1, 1, 1),
                       (1.0, 1, 1, 1), (Fraction(1), 1, 1, 1), (0, 1, 1, 1), (2, 1, 1, 1)):
            self.refused(evaluate(Cochain, 2, phases))
        for degree in (2, 3):
            cochain = Cochain(degree, (1,)*(2**degree))
            for bad in (None, (), (0,)*(degree-1), (True,)*(degree),
                        (0.0,)*degree, (Fraction(0),)*degree, (-1,)*degree):
                self.refused(cochain.at(bad))
            self.refused(cochain.at((2,)*degree), "resource")
            self.refused(cochain.at((0,)*(degree+1)), "resource" if degree==3 else "input")
        self.refused(evaluate(Cochain, 2, [1]*9), "resource")

    def test_operation_degree_and_operand_refusals(self) -> None:
        two, three = Cochain(2, (1,)*4), Cochain.generator()
        self.refused(three.coboundary())
        self.refused(two.pentagon((0, 0, 0, 0)))
        for bad in (None, object(), 1, two):
            self.refused(three.multiply(bad))
        for bad in (None, (), (0,)*3, (False,)*4, (0.0,)*4):
            self.refused(three.pentagon(bad))
        for oversized_point in ((0,)*5, (2,)*4):
            self.refused(three.pentagon(oversized_point), "resource")

    def test_rephasing_and_generator_sign_for_all_two_cochains(self) -> None:
        omega = Cochain.generator()
        self.assertEqual(omega.phases, (1, 1, 1, 1, 1, 1, 1, -1))
        for phases in product((-1, 1), repeat=4):
            beta = Cochain(2, phases)
            boundary = beta._coboundary()
            result = omega.multiply(boundary)
            self.assertIsNone(result.error)
            if result.value is None:
                self.fail("Missing rephasing value")
            expected = tuple(1-2*((int(a == -1)+b) % 2) for a, b in zip(omega.phases, boundary_bits(phases)))
            self.assertEqual(result.value.phases, expected)
            if beta.is_normalized():
                self.assertEqual(result.value.at((1, 1, 1)).value, -1)

    def test_all_candidates_and_actual_case_count(self) -> None:
        module = load()
        accepted = []
        for phases in product((-1, 1), repeat=8):
            result = module.SignCocycleControls(Cochain(3, phases)).verify()
            if result.ok:
                accepted.append(phases)
            else:
                self.refused(result, "check")
        self.assertEqual(accepted, [Cochain.generator().phases])
        observed: list[str] = []
        original = Cases.require
        def record(cases: Cases, condition: bool, label: str) -> None:
            observed.append(label)
            original(cases, condition, label)
        controls = module.SignCocycleControls()
        with patch.object(Cases, "require", record):
            report = controls.verify().value
        self.assertEqual(report["checks"], len(observed))
        self.assertEqual(report["checks"], 26)
        self.assertEqual((report["pentagon_cases"], report["cochains"], report["normalized_cochains"]), (16, 16, 2))
        self.assertEqual(report, controls.verify().value)
        for invalid in (False, [], object(), Cochain(2, (1,)*4)):
            self.refused(evaluate(module.SignCocycleControls, invalid))
        with self.assertRaises(FrozenInstanceError):
            controls.cocycle = Cochain.generator()

    def test_admission_precedes_dependent_operations(self) -> None:
        with self.assertRaises(AssertionError):
            self.refused(evaluate(Cochain, 2, (1,)*4))
        with patch.dict(Cochain.__init__.__globals__, sequence=unittest.mock.Mock(side_effect=RuntimeError("must not admit"))):
            self.refused(evaluate(Cochain, 4, (1,)*4), "resource")
            self.refused(evaluate(Cochain, True, (1,)*4))
        with patch.dict(Cochain.__init__.__globals__, _sign=unittest.mock.Mock(side_effect=RuntimeError("must not map"))):
            self.refused(evaluate(Cochain, 2, (1,)*3))

    def test_failure_translation_and_unexpected_exceptions(self) -> None:
        module = load()
        with patch.object(Cochain, "_pentagon", side_effect=Violation("check", "injected")):
            self.assertEqual(module.SignCocycleControls().verify().error.kind, "check")
            with contextlib.redirect_stderr(io.StringIO()) as output:
                self.assertEqual(module.main(), 1)
            self.assertIn("injected", output.getvalue())
        for exception in (RuntimeError, KeyboardInterrupt, SystemExit):
            with patch.object(Cochain, "_at", side_effect=exception):
                with self.assertRaises(exception):
                    Cochain.generator().at((1, 1, 1))
            with patch.object(Cochain, "_pentagon", side_effect=exception):
                with self.assertRaises(exception):
                    module.SignCocycleControls().verify()

    def test_quiet_import_and_original_cli(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as output:
            module = load()
        self.assertEqual(output.getvalue(), "")
        for _ in range(2):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(module.main(), 0)
            self.assertEqual(output.getvalue(), "pentagon_cases=16 cochains=16 normalized_cochains=2 generator_phase=-1 failures=0\n")
        result = subprocess.run([sys.executable, "-I", "-B", str(APP)], capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, output.getvalue())


if __name__ == "__main__":
    unittest.main()
