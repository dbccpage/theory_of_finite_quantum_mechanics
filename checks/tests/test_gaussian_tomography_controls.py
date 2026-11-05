"""Composition, source custody and retained-population controls for tomography.

AuthorityEffect: None. Archived conditions establish review custody, not proof
of a general rigidity or continuity theorem. Arithmetic oracles are separate.
"""
from __future__ import annotations

import ast
import contextlib
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from typing import TypeVar, cast
import unittest
from unittest.mock import patch


CHECKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHECKS)); sys.path.insert(0, str(Path(__file__).parent))
import test_inert_prime_geometry as fixture
from checker_support.boundary import Violation, evaluate
from checker_support.cases import Cases
from checker_support.gaussian_vector3 import GaussianVector3 as V
from checker_support.hermitian_tomography import HermitianTomography as H
from checker_support.inert_prime_residual import InertPrimeResidual as R
from checker_support.orthogonal_gaussian_pair import OrthogonalGaussianPair as P
from checker_support.outcome import Outcome

APP = CHECKS/'independent/fq-gleason-qi3-tomography.py'
REVIEW = CHECKS.parent/'reviews/repository_file_review'
T = TypeVar('T')


def load() -> ModuleType:
    name = 'reviewed_gaussian_tomography_controls'
    spec = importlib.util.spec_from_file_location(name, APP)
    if spec is None or spec.loader is None:
        raise Violation('resource', 'tomography import specification is unavailable')
    module = importlib.util.module_from_spec(spec); previous = sys.modules.get(name)
    try:
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous


def declarations(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8')); names = set()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.add(node.name)
        if isinstance(node, ast.ClassDef):
            names.update(node.name+'.'+child.name for child in node.body if isinstance(child, ast.FunctionDef))
    return names


class GaussianTomographyControlTests(unittest.TestCase):
    def accepted(self, result: Outcome[T]) -> T:
        self.assertIsNone(result.error)
        return cast(T, result.value)

    def refused(self, result: Outcome[T], kind: str) -> None:
        self.assertIsNotNone(result.error)
        if result.error is not None:
            self.assertEqual(result.error.kind, kind)

    def test_original_report_values_and_observed_per_run_counter(self) -> None:
        module = load(); original = json.loads((REVIEW/'2026-11-03-tomography-initial-review.json').read_bytes())
        expected = json.loads(original['original_run']['stdout']); expected.pop('scope'); expected.pop('sympy_version')
        observed: list[str] = []; implementation = Cases.require
        def record(cases: Cases, condition: bool, message: str) -> None:
            observed.append(message); implementation(cases, condition, message)
        with patch.object(Cases, 'require', record):
            report = self.accepted(module.verify())
        self.assertEqual({key: report[key] for key in expected}, expected)
        self.assertEqual(report['checks'], len(observed)); self.assertEqual(len(observed), 979)
        self.assertEqual(report['authority_effect'], 'None')
        self.assertIn('finite', report['scope']); self.assertIn('no pointwise-to-uniform', report['scope'])
        self.assertEqual(observed.count('positive sampled oscillation distance'), 33)
        self.assertEqual(observed.count('finite sampled epsilon sandwich'), 18)

    def test_original_sixty_five_obligations_are_bound_to_source_and_symbols(self) -> None:
        mapping = json.loads((CHECKS/'tests/tomography_obligations.json').read_bytes())
        original = (REVIEW/'2026-11-03-tomography-original-fq-gleason-qi3-tomography.py.txt').read_bytes()
        self.assertEqual(hashlib.sha256(original).hexdigest(), mapping['original_source_sha256'])
        calls = sorted((n for n in ast.walk(ast.parse(original)) if isinstance(n, ast.Call)
                        and isinstance(n.func, ast.Name) and n.func.id == 'require'), key=lambda n: n.lineno)
        self.assertEqual(len(calls), 65); self.assertEqual(len(mapping['rows']), 65)
        self.assertEqual(mapping['original_runtime_checks'], 315)
        for index, (node, row) in enumerate(zip(calls, mapping['rows']), 1):
            self.assertEqual((row['obligation_id'], row['line'], row['condition'], row['label']),
                             (index, node.lineno, ast.unparse(node.args[0]), ast.unparse(node.args[1])))
            self.assertIn(row['target_symbol'], declarations(CHECKS.parent/row['target_source']))

    def test_fixed_witnesses_kernels_and_owned_state(self) -> None:
        controls = load().GaussianTomographyControls()
        self.assertEqual(tuple(r.prime for r in controls.residuals), (3, 7, 11))
        self.assertEqual(tuple(v.squared_norm for v in controls.witnesses), (3, 7, 11))
        self.assertEqual(tuple(v.squared_norm for v in controls.equators), (3, 7, 11))
        for index, vector in enumerate(controls.witnesses):
            expected = tuple(Q(int(index == j)) for j in range(3))
            self.assertEqual(tuple(fixture.reference_residual(vector, p) for p in (3, 7, 11)), expected)
            self.assertEqual(controls._kernel_value(index, lambda v: Q(1)), 0)
        with self.assertRaises(FrozenInstanceError):
            controls.witnesses = ()
        report = self.accepted(controls.verify()); report['status'] = 'changed'
        self.assertEqual(self.accepted(controls.verify())['status'], 'PASS')

    def test_six_original_frames_are_executed_and_match_independent_oracle(self) -> None:
        controls = load().GaussianTomographyControls(); pairs: list[P] = []
        implementation = type(controls)._frame
        def record(owner: object, pair: P, cases: Cases) -> None:
            pairs.append(pair); implementation(owner, pair, cases)
        cases = Cases()
        with patch.object(type(controls), '_frame', record):
            controls._frames(cases)
        self.assertEqual(len(pairs), 6); self.assertEqual(cases.checks, 67)
        for pair in pairs:
            u, v = fixture.symbolic(pair.first), fixture.symbolic(pair.second)
            w = u.cross(v).conjugate()
            self.assertEqual((u.conjugate().T*v)[0].expand(), 0)
            self.assertEqual((u.conjugate().T*w)[0].expand(), 0)
            self.assertEqual((v.conjugate().T*w)[0].expand(), 0)
            vectors = (pair.first, pair.second, pair._completion())
            for prime in (3, 7, 11):
                self.assertEqual(sum(fixture.reference_residual(x, prime) for x in vectors), 0)

    def test_retained_oscillation_grid_and_cross_prime_selectivity(self) -> None:
        controls = load().GaussianTomographyControls(); observed: list[tuple[int, int]] = []
        implementation = type(controls)._oscillation
        def record(owner: object, index: int, denominator: int, cases: Cases) -> tuple[V, V]:
            observed.append((index, denominator))
            return cast(tuple[V, V], implementation(owner, index, denominator, cases))
        with patch.object(type(controls), '_oscillation', record):
            controls._oscillations(Cases())
        expected = [(index, multiplier*k) for k in range(1, 8) for index, multiplier in ((0, 3), (1, 7), (0, 21))]
        expected += [(index, 231*k) for k in range(1, 5) for index in range(3)]
        self.assertEqual(observed, expected)
        for index in range(3):
            positive, negative = controls._oscillation(index, 231, Cases())
            for other, prime in enumerate((3, 7, 11)):
                self.assertEqual(fixture.reference_residual(positive, prime), int(index == other))
                self.assertEqual(fixture.reference_residual(negative, prime), -int(index == other))

    def test_radical_extension_and_symmetry_report_values_are_calculated(self) -> None:
        controls = load().GaussianTomographyControls(); cases = Cases()
        self.assertEqual(controls._quadratic_extensions(cases), ((3, 18, 18), (7, 245, 245), (11, 1210, 1210)))
        self.assertEqual(cases.checks, 15)
        self.assertEqual(controls._parallelogram_counterexamples(Cases()), (2, 2, 2))
        self.assertEqual(controls._symmetry_samples(Cases()), (1, 1, 1))
        with patch.object(R, '_residual', return_value=Q(0)):
            self.refused(evaluate(controls._parallelogram_counterexamples, Cases()), 'check')
            self.refused(evaluate(controls._symmetry_samples, Cases()), 'check')

    def test_geometric_sample_populations_and_finite_squeeze(self) -> None:
        controls = load().GaussianTomographyControls(); counts: dict[str, int] = {}
        def recorder(name: str) -> object:
            original = getattr(type(controls), name)
            def recorded(owner: object, *args: object) -> object:
                counts[name] = counts.get(name, 0)+1
                return original(owner, *args)
            return recorded
        names = ('_piron_sample', '_quarter_kelvin', '_tangent_sample', '_sandwich_sample')
        with contextlib.ExitStack() as stack:
            for name in names:
                stack.enter_context(patch.object(type(controls), name, recorder(name)))
            controls._equatorial_controls(Cases())
        self.assertEqual(counts, dict(zip(names, (12, 6, 18, 24))))
        geometry = load().E(controls.equators[0])
        self.assertFalse(controls._squeeze_sample(geometry, 2, Q(1, 100)))
        self.assertTrue(controls._squeeze_sample(geometry, 39, Q(1, 100)))
        with patch.object(type(controls), '_squeeze_sample', return_value=False):
            self.refused(evaluate(controls._equatorial_controls, Cases()), 'check')

    def test_isolated_symbolic_and_arithmetic_failure_guards(self) -> None:
        module = load(); controls = module.GaussianTomographyControls()
        with patch.object(H, '_kernel_relation', return_value=False):
            self.refused(evaluate(controls._kernel_controls, Cases()), 'check')
        with patch.object(H, '_parallelogram', return_value=False):
            self.refused(evaluate(controls._rotation_controls, Cases()), 'check')
        with patch.object(R, '_exotic', return_value=Q(0)):
            self.refused(evaluate(controls._mixture_controls, Cases()), 'check')
        with patch.dict(type(controls)._quadratic_extensions.__globals__, _zero=lambda _: False):
            self.refused(evaluate(controls._quadratic_extensions, Cases()), 'check')
        with patch.object(type(controls), '_kernel_value', return_value=Q(0)):
            self.refused(evaluate(controls._kernel_controls, Cases()), 'check')

    def test_isolated_first_mixture_value_guard(self) -> None:
        controls = load().GaussianTomographyControls(); original = R._exotic
        def isolated(residual: R, value: object) -> Q:
            if value == controls.witnesses[1]:
                return Q(0)
            return original(residual, value)
        with patch.object(R, '_exotic', isolated):
            self.refused(evaluate(controls._mixture_controls, Cases()), 'check')

    def test_railway_cli_failure_and_unexpected_cancellation(self) -> None:
        module = load()
        for kind in ('input', 'check', 'resource'):
            with patch.object(H, '_verify', side_effect=Violation(kind, 'injected failure')):
                self.refused(module.verify(), kind)
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    self.assertEqual(module.main(), 1)
                self.assertEqual(out.getvalue(), ''); self.assertEqual(json.loads(err.getvalue())['kind'], kind)
        for failure in (RuntimeError, KeyboardInterrupt, SystemExit):
            with patch.object(H, '_verify', side_effect=failure), self.assertRaises(failure):
                module.verify()

    def test_quiet_import_restores_module_registration_and_cli_repeats(self) -> None:
        out, err = io.StringIO(), io.StringIO(); previous = ModuleType('previous')
        with patch.dict(sys.modules, reviewed_gaussian_tomography_controls=previous):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                module = load()
            self.assertIs(sys.modules['reviewed_gaussian_tomography_controls'], previous)
        self.assertEqual((out.getvalue(), err.getvalue()), ('', ''))
        reports = []
        for _ in range(2):
            with contextlib.redirect_stdout(out := io.StringIO()):
                self.assertEqual(module.main(), 0)
            reports.append(json.loads(out.getvalue()))
        self.assertEqual(reports[0], reports[1])
        command = [sys.executable, '-I', '-B', '-X', 'utf8']
        if sys.flags.optimize:
            command.append('-O')
        result = subprocess.run(command+[str(APP)], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), reports[0])


if __name__ == '__main__':
    unittest.main()
