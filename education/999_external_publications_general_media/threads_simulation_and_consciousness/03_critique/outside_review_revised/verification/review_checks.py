"""Finite checks for the holographic-brain review.

Run: python verification/review_checks.py
Optional: --json PATH; --failure-fixture (deliberately exits nonzero).
These checks do not reproduce the paper's lattice simulation.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import re
import sys
import unittest

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
KB_EV_K = 8.617333262145e-5
HC_EV_NM = 1239.8419843320026
YEAR_S = 365.25 * 24 * 3600
METRICS = {}


def trace_norm(a):
    """Singular-value definition, also valid for non-Hermitian inputs."""
    return float(np.linalg.svd(a, compute_uv=False).sum())


def marginals(rho, dim_a=2, dim_b=2):
    r = rho.reshape(dim_a, dim_b, dim_a, dim_b)
    return np.einsum("abcb->ac", r), np.einsum("abad->bd", r)


def quoted_posts(path):
    posts, lines = [], []
    for line in path.read_text(encoding="utf-8").splitlines() + [""]:
        if line.startswith("> "):
            lines.append(line[2:])
        elif lines:
            posts.append("\n".join(lines))
            lines = []
    return posts


def validate_post(post):
    if not post or len(post) > 500:
        raise ValueError("A post must contain 1 to 500 characters.")


class EquationChecks(unittest.TestCase):
    def test_E01_temporal_transverse_gauss_constraint(self):
        t, e, c = sp.symbols("t e c", real=True, nonzero=True)
        n = sp.Function("n")(t)
        # Zero temporal potential and zero vector divergence give zero Gauss LHS.
        constraint = -e * n + c
        self.assertEqual(sp.solve(constraint, n), [c / e])
        self.assertEqual(sp.diff(constraint, t), -e * sp.diff(n, t))
        self.assertEqual(sp.solve(constraint.subs(c, 0), n), [0])

    def test_E03_full_matter_gauss_residual(self):
        x, y = sp.symbols("x y")
        e, m, mass2, gamma, v = sp.symbols("e m mass2 gamma v")
        n, a, b, E1, E2, A0, p, q = [
            sp.Function(s)(x, y)
            for s in ("n", "a", "b", "E1", "E2", "A0", "p", "q")
        ]
        s1 = -mass2 * a - gamma * (E1 + sp.diff(A0, x)) + v * p
        s2 = -mass2 * b - gamma * (E2 + sp.diff(A0, y)) + v * q
        E1dot = sp.diff(a, y, 2) - sp.diff(b, x, y) - e**2 * n * a / m + s1
        E2dot = sp.diff(b, x, 2) - sp.diff(a, x, y) - e**2 * n * b / m + s2
        rhodot = -e**2 / m * (sp.diff(n * a, x) + sp.diff(n * b, y))
        residual = sp.diff(E1dot, x) + sp.diff(E2dot, y) - rhodot
        self.assertEqual(sp.simplify(residual - sp.diff(s1, x) - sp.diff(s2, y)), 0)

    def test_E04_wrong_charge_coefficient_leaves_residual(self):
        e, m, div_nA = sp.symbols("e m div_nA", nonzero=True)
        wrong = -e * div_nA / m - (-e**2 * div_nA / m)
        self.assertEqual(sp.factor(wrong), e * (e - 1) * div_nA / m)
        self.assertNotEqual(wrong.subs({e: sp.Rational(3, 10), m: 1, div_nA: 1}), 0)

    def test_E04_madelung_real_and_imaginary_parts(self):
        R, Rt, Rx, Rxx, bt, bx, bxx, A, Ax, A0, e, m = sp.symbols(
            "R Rt Rx Rxx bt bx bxx A Ax A0 e m", real=True, nonzero=True
        )
        # (d_x - i e A)^2(R exp(i beta)) / exp(i beta), with independent jets.
        B = bx - e * A
        D2 = Rxx + 2 * sp.I * Rx * B + sp.I * R * (bxx - e * Ax) - R * B**2
        equation = sp.I * Rt - R * bt + e * A0 * R + D2 / (2 * m)
        solution = sp.solve(sp.re(equation), A0)[0]
        correct = bt / e - Rxx / (2 * m * e * R) + e * (A - bx / e)**2 / (2 * m)
        self.assertEqual(sp.simplify(solution - correct), 0)
        printed = bt / e - Rxx / (2 * m * e * R) - e * (A - bx / e)**2 / (2 * m)
        self.assertNotEqual(sp.simplify(solution - printed), 0)
        rtdot = sp.solve(sp.im(equation), Rt)[0]
        continuity = e / m * (2 * R * Rx * (A - bx / e) + R**2 * (Ax - bxx / e))
        self.assertEqual(sp.simplify(2 * R * rtdot - continuity), 0)

    def test_E04_inverse_controller_general_substitution(self):
        x, y, mass2, v = sp.symbols("x y mass2 v", nonzero=True)
        u1, u2, next1, next2 = [sp.Function(s)(x, y) for s in ("u1", "u2", "next1", "next2")]
        prev1 = (-sp.diff(u1, y, 2) + sp.diff(u2, x, y) + mass2 * u1) / v - next1
        prev2 = (-sp.diff(u2, x, 2) + sp.diff(u1, x, y) + mass2 * u2) / v - next2
        residual1 = sp.diff(u1, y, 2) - sp.diff(u2, x, y) - mass2 * u1 + v * (prev1 + next1)
        residual2 = sp.diff(u2, x, 2) - sp.diff(u1, x, y) - mass2 * u2 + v * (prev2 + next2)
        self.assertEqual(sp.simplify(residual1), 0)
        self.assertEqual(sp.simplify(residual2), 0)

    def test_E04_printed_inverse_fails_nonconstant_target(self):
        x, y = sp.symbols("x y")
        # One layer, M^2=2, v=1, no following layer, no matter term.
        u1, u2 = sp.sin(x), sp.sin(y)
        printed1 = -sp.diff(u1, x, 2) + sp.diff(u2, x, y) + 2 * u1
        printed2 = -sp.diff(u2, y, 2) + sp.diff(u1, x, y) + 2 * u2
        res1 = sp.diff(u1, y, 2) - sp.diff(u2, x, y) - 2 * u1 + printed1
        res2 = sp.diff(u2, x, 2) - sp.diff(u1, x, y) - 2 * u2 + printed2
        self.assertEqual(sp.simplify(res1), sp.sin(x))
        self.assertEqual(sp.simplify(res2), sp.sin(y))

    def test_E04_inverse_recurrence_not_leading_power(self):
        last, current = Fraction(0), Fraction(1, 10)
        for _ in range(4):
            last, current = current, Fraction(5, 2) * current - last
        self.assertEqual(current, Fraction(341, 160))
        self.assertNotEqual(current, Fraction(1, 10) * Fraction(5, 2)**4)
        METRICS["corrected_separated_target_input"] = float(current)

    def test_E05_resonance_requires_squared_frequency(self):
        omega, plasma_squared = Fraction(1, 10), Fraction(1, 25)
        self.assertGreaterEqual(omega, plasma_squared)  # printed comparison passes
        self.assertLess(omega**2 - plasma_squared, 0)   # no real carrier wavevector
        # Natural units: [n]=E^3, [m]=E, [e]=1, [Omega]=E.
        self.assertEqual(3 - 1, 2)  # e^2 n/m is a squared energy
        self.assertNotEqual(3 - 1, 1)

    def test_A31_correct_coupling_preserves_population(self):
        c, a, b = sp.symbols("c a b", real=True)
        correct = 2 * a * c * b + 2 * b * (-c * a)
        printed = 2 * a * c * b + 2 * b * (-c * b)
        self.assertEqual(sp.expand(correct), 0)
        self.assertNotEqual(printed.subs({c: 1, a: sp.Rational(3, 5), b: sp.Rational(4, 5)}), 0)

    def test_S01_sech_reduced_solution(self):
        t, tau, shift = sp.symbols("t tau shift", real=True, nonzero=True)
        theta = 2 * sp.atan(sp.exp((t - shift) / tau))
        self.assertEqual(sp.simplify(sp.diff(theta, t) - sp.sin(theta) / tau), 0)
        envelope = 1 / sp.cosh((t - shift) / tau)
        z = sp.symbols("z", positive=True)
        half_angle = sp.expand_trig(sp.sin(2 * sp.atan(z)))
        self.assertEqual(sp.simplify(half_angle - 2 * z / (1 + z**2)), 0)
        self.assertEqual(sp.simplify(half_angle.subs(z, sp.exp((t - shift) / tau))
                                     - envelope.rewrite(sp.exp)), 0)

    def test_four_transverse_tensor_can_be_spatially_longitudinal(self):
        omega, k = sp.symbols("omega k", nonzero=True)
        wave_covector = sp.Matrix([[omega, 0, 0, -k]])
        b = sp.Matrix([k, 0, 0, omega])
        response = b * b.T
        self.assertEqual(wave_covector * response, sp.zeros(1, 4))
        self.assertEqual(response[3, 3], omega**2)


class NumericalChecks(unittest.TestCase):
    def test_O01_capacity_and_units(self):
        bits_per_mm2 = 4 * 1.3 * 2 / (500e-6)**3
        total_bytes = bits_per_mm2 * 2500 * 100 / 8
        self.assertTrue(math.isclose(bits_per_mm2, 8.32e10, rel_tol=1e-13))
        self.assertTrue(math.isclose(total_bytes, 2.6e15, rel_tol=1e-13))
        self.assertEqual(250e12 / 8 / 1e12, 31.25)
        METRICS.update(capacity_decimal_PB=total_bytes / 1e15, synaptic_decimal_TB=31.25)

    def test_O03_screening_contrast_and_uniform_control(self):
        transmission = lambda n: 1 / (1 + 0.045 * n)
        change = transmission(0.79) - transmission(1)
        self.assertAlmostEqual(change, float(Fraction(37800, 4328599)), places=12)
        self.assertNotAlmostEqual(change, 0.045, places=3)
        uniform = np.full(32, transmission(1))
        self.assertLess(float(np.abs(np.fft.fft(uniform)[1:]).max()), 1e-12)
        METRICS["field_transmission_difference"] = change

    def test_R01_thermal_and_photon_scales(self):
        kT = KB_EV_K * 310
        energy = HC_EV_NM / 500
        occupation = 1 / math.expm1(energy / kT)
        self.assertAlmostEqual(energy, 2.479683968664, places=11)
        self.assertTrue(4e-41 < occupation < 6e-41)
        METRICS.update(kBT_eV=kT, landauer_full_bit_eV=kT * math.log(2),
                       photon_500nm_eV=energy, thermal_photon_occupation=occupation)

    def test_R02_mean_lifetime_and_reliability_are_different(self):
        kT = KB_EV_K * 310
        p = 0.01
        values = []
        for attempt in (1e-12, 1.0):
            mean_barrier = kT * math.log(YEAR_S / attempt)
            reliable_barrier = kT * math.log(YEAR_S / (attempt * -math.log1p(-p)))
            tau = attempt * math.exp(reliable_barrier / kT)
            actual_failure = -math.expm1(-YEAR_S / tau)
            self.assertAlmostEqual(actual_failure, p, places=13)
            self.assertGreater(reliable_barrier, mean_barrier)
            values.append(dict(attempt_s=attempt, mean_barrier_eV=mean_barrier,
                               one_percent_barrier_eV=reliable_barrier))
        self.assertAlmostEqual(-math.expm1(-1), 0.6321205588285577)
        METRICS["one_year_retention"] = values

    def test_Q02_separable_state_has_correlation_defect(self):
        rho = np.diag([0.5, 0, 0, 0.5])
        a, b = marginals(rho)
        self.assertAlmostEqual(trace_norm(rho - np.kron(a, b)), 1.0)

    def test_Q01_first_moments_do_not_determine_marginals(self):
        annihilator = np.diag(np.sqrt(np.arange(1, 3)), 1)
        one, zero = np.diag([0, 1, 0]), np.diag([1, 0, 0])
        self.assertEqual(float(np.trace(one @ annihilator)), 0)
        self.assertEqual(float(np.trace(zero @ annihilator)), 0)
        rho = np.kron(one, zero)
        a, b = marginals(rho, 3, 3)
        self.assertTrue(np.array_equal(np.kron(a, b), rho))
        self.assertAlmostEqual(trace_norm(rho - np.kron(zero, zero)), 2.0)

    def test_product_transfer_bound_finite_samples(self):
        rng = np.random.default_rng(515518)
        def density(d):
            z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
            z = z @ z.conj().T
            return z / np.trace(z)
        for _ in range(20):
            rho = density(4)
            a, b = marginals(rho)
            product = np.kron(density(2), density(2))
            defect = trace_norm(rho - np.kron(a, b))
            self.assertLessEqual(defect, 3 * trace_norm(rho - product) + 1e-12)

    def test_projection_lower_bound_with_full_incident_norm(self):
        X = np.array([[0, 1], [1, 0]], complex)
        Z = np.diag([1, -1]).astype(complex)
        I = np.eye(2)
        H = 1.2 * np.kron(Z, I) + 0.7 * np.kron(I, X) + 0.3 * np.kron(X, X)
        rho0 = np.diag([1, 0, 0, 0]).astype(complex)
        a0, b0 = marginals(rho0)
        drho = -1j * (H @ rho0 - rho0 @ H)
        da, db = marginals(drho)
        normal = drho - np.kron(da, b0) - np.kron(a0, db)
        nu = trace_norm(normal)
        g_inc = max(1.2 + 0.3, 0.7 + 0.3)
        window = nu / (48 * g_inc**2)
        energies, vectors = np.linalg.eigh(H)
        self.assertAlmostEqual(nu, 0.6)
        for fraction in (0.1, 0.5, 1.0):
            t = fraction * window
            U = (vectors * np.exp(-1j * energies * t)) @ vectors.conj().T
            rho = U @ rho0 @ U.conj().T
            a, b = marginals(rho)
            defect = trace_norm(rho - np.kron(a, b))
            self.assertGreaterEqual(defect + 1e-12, nu * t - 24 * g_inc**2 * t**2)
            self.assertGreaterEqual(defect + 1e-12, nu * t / 2)
        METRICS["two_qubit_projection_example"] = dict(nu=nu, g_inc=g_inc, half_slope_window=window)


class ObservationChecks(unittest.TestCase):
    def test_phase_gradient_changes_density_future(self):
        x, epsilon, m = sp.symbols("x epsilon m", nonzero=True)
        beta = epsilon * sp.cos(x)
        ndot = -sp.diff(beta, x, 2) / m
        self.assertEqual(ndot, epsilon * sp.cos(x) / m)
        self.assertNotEqual(ndot, 0)

    def test_gauge_transformation_preserves_velocity(self):
        A, beta_x, alpha_x, e = sp.symbols("A beta_x alpha_x e", nonzero=True)
        before = A - beta_x / e
        after = A + alpha_x / e - (beta_x + alpha_x) / e
        self.assertEqual(sp.simplify(after - before), 0)

    def test_P01_blind_spot_is_channel_relative(self):
        q = {0: 0, 1: 0, 2: 1}
        other = {0: 0, 1: 1, 2: 0}
        self.assertEqual(q[0], q[1])
        for evaluator in itertools.product((False, True), repeat=2):
            self.assertEqual(evaluator[q[0]], evaluator[q[1]])
        self.assertNotEqual(other[0], other[1])

    def test_P02_pigeonhole_needs_cardinality_condition(self):
        maps_3_to_2 = itertools.product(range(2), repeat=3)
        self.assertTrue(all(len(set(q)) < 3 for q in maps_3_to_2))
        self.assertEqual(sum(len(set(q)) == 2 for q in itertools.product(range(2), repeat=2)), 2)

    def test_P04_equal_marginals_different_joint_likelihood(self):
        independent = {(a, b): Fraction(1, 4) for a, b in itertools.product((0, 1), repeat=2)}
        copied = {(0, 0): Fraction(1, 2), (1, 1): Fraction(1, 2),
                  (0, 1): Fraction(0), (1, 0): Fraction(0)}
        for coordinate in (0, 1):
            self.assertEqual(sum(p for x, p in independent.items() if x[coordinate] == 0),
                             sum(p for x, p in copied.items() if x[coordinate] == 0))
        self.assertEqual(copied[(0, 0)] / independent[(0, 0)], 2)

    def test_P03_equal_positive_likelihood_preserves_odds(self):
        prior1, prior2, likelihood = Fraction(1, 5), Fraction(4, 5), Fraction(3, 7)
        self.assertEqual((prior1 * likelihood) / (prior2 * likelihood), prior1 / prior2)

    def test_R01_reversible_copy_and_clear_with_retained_copy(self):
        states = set(itertools.product((0, 1), repeat=2))
        transform = lambda x, y: (x, y ^ x)
        self.assertEqual({transform(*s) for s in states}, states)
        for bit in (0, 1):
            self.assertEqual(transform(bit, 0), (bit, bit))
            self.assertEqual(transform(bit, bit), (bit, 0))


class PackageChecks(unittest.TestCase):
    def test_source_files_match_recorded_hashes(self):
        expected = json.loads((ROOT / "verification/source_hashes.json").read_text())
        self.assertEqual(set(expected), {"ijms-25-02399.pdf", "ijms-25-02399.md"})
        for name, digest in expected.items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)

    def test_public_posts_are_present_and_within_limit(self):
        lengths = {}
        for name in ("public_replies.md", "public_reply_variants.md"):
            posts = quoted_posts(ROOT / name)
            self.assertEqual(len(posts), 4, name)
            for post in posts:
                validate_post(post)
            lengths[name] = [len(p) for p in posts]
        METRICS["public_reply_characters"] = lengths

    def test_length_validator_rejects_overflow_and_empty_text(self):
        validate_post("x" * 500)
        with self.assertRaises(ValueError):
            validate_post("x" * 501)
        with self.assertRaises(ValueError):
            validate_post("")

    def test_relative_document_links_resolve(self):
        for path in ROOT.glob("*.md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
                if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                self.assertTrue((path.parent / target.split("#")[0]).is_file(), f"{path.name}: {target}")


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"test": test.id(), "status": "passed"})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append({"test": test.id(), "status": "failed",
                             "detail": self._exc_info_to_string(err, test)})

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append({"test": test.id(), "status": "error",
                             "detail": self._exc_info_to_string(err, test)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--failure-fixture", action="store_true")
    args = parser.parse_args()
    suite = unittest.TestSuite()
    for case in (EquationChecks, NumericalChecks, ObservationChecks, PackageChecks):
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(case))
    if args.failure_fixture:
        class ExpectedFailureFixture(unittest.TestCase):
            def test_deliberate_failure(self):
                self.fail("Intentional negative control: this run must exit nonzero.")
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ExpectedFailureFixture))
    result = unittest.TextTestRunner(verbosity=2, resultclass=RecordingResult).run(suite)
    if args.json:
        payload = {
            "scope": "Symbolic identities, finite examples and package checks; no full lattice reproduction.",
            "python": platform.python_version(), "numpy": np.__version__, "sympy": sp.__version__,
            "passed": result.wasSuccessful(), "tests_run": result.testsRun,
            "failures": len(result.failures), "errors": len(result.errors),
            "negative_control": args.failure_fixture, "tests": result.records, "metrics": METRICS,
        }
        args.json.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
