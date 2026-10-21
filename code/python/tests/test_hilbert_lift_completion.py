from fractions import Fraction as Q
from pathlib import Path
import importlib, sys, types, unittest
pkg = types.ModuleType('staged_qm')
pkg.__path__ = [str(Path(__file__).resolve().parents[1] / 'src/qm')]
sys.modules[pkg.__name__] = pkg
m = importlib.import_module('staged_qm.hilbert_lift_completion')

X = m.fin_vector([1, Q(1, 2), -3])
Y = m.fin_vector([2, 0, Q(1, 3)])
F = m.seq({0: 1, 2: Q(-1, 2), 5: 3})
G = m.seq({1: Q(2, 7), 2: 1, 9: -1})
H = m.seq({0: -2, 5: Q(1, 3)})


class TowerTests(unittest.TestCase):
    def test_padding_isometric_and_cocone(self):
        for mm in (3, 4, 7):
            self.assertTrue(m.padding_is_isometric(X, Y, mm))
        with self.assertRaises(ValueError):
            m.pad(X, 2)

    def test_pad_trans_and_refl(self):
        self.assertEqual(m.pad(m.pad(X, 4), 6), m.pad(X, 6))
        self.assertEqual(m.pad(X, 3), X)

    def test_restriction_identity(self):
        self.assertTrue(m.restriction_identity(X, Y))
        self.assertEqual(m.fin_inner(X, Y), Q(1))

    def test_exhaustion_and_truncation(self):
        for f in (F, G, H, m.seq({})):
            n, x = m.exhaustion(f)
            self.assertEqual(m.of_fin(x), f)
            self.assertEqual(m.trunc(n, m.of_fin(x)), x)
        self.assertEqual(m.exhaustion(m.seq({}))[0], 0)

    def test_bessel_truncation(self):
        for n in range(0, 12):
            self.assertTrue(m.bessel_truncation_holds(n, F))
        self.assertEqual(m.fin_inner(m.trunc(6, F), m.trunc(6, F)), m.qinner(F, F))

    def test_bilinearity_symmetry_positivity(self):
        self.assertEqual(m.qinner(F, G), m.qinner(G, F))
        self.assertEqual(m.qinner(m.add(F, G), H), m.qinner(F, H) + m.qinner(G, H))
        self.assertEqual(m.qinner(m.smul(Q(-3, 4), F), G), Q(-3, 4) * m.qinner(F, G))
        self.assertGreaterEqual(m.qinner(F, F), 0)
        self.assertEqual(m.qinner(m.seq({}), m.seq({})), 0)


class UniformityTests(unittest.TestCase):
    def test_cauchy_schwarz_and_doubling_triangle(self):
        for f, g in ((F, G), (G, H), (F, F), (m.seq({}), G)):
            self.assertTrue(m.cauchy_schwarz_holds(f, g))
        self.assertTrue(m.doubling_triangle_holds(F, G, H))
        self.assertTrue(m.l1_dominates_l2(F, G))
        self.assertEqual(m.sqdist(F, G), m.sqdist(G, F))
        self.assertEqual(m.sqdist(F, F), 0)

    def test_sup_below_l2_below_l1(self):
        self.assertLessEqual(m.supdist(F, G) ** 2, m.sqdist(F, G))
        self.assertLessEqual(m.sqdist(F, G), m.l1dist(F, G) ** 2)


class HarmonicTests(unittest.TestCase):
    def test_telescoping_and_sqdist_bounds(self):
        for n in range(1, 9):
            for mm in range(n, 20):
                self.assertTrue(m.telescoping_bound_holds(n, mm))
                self.assertTrue(m.harmonic_sqdist_bound_holds(n, mm))

    def test_explicit_modulus(self):
        for k in range(0, 6):
            self.assertTrue(m.modulus_holds(m.harmonic, m.harmonic_modulus, k, m.harmonic_modulus(k) + 12))
        point = m.CauchyPoint(m.harmonic, m.harmonic_modulus)
        self.assertEqual(point.approximant(2), m.harmonic(3))
        self.assertTrue(point.check(3, 15))

    def test_not_l1_cauchy(self):
        for n in range(1, 10):
            self.assertTrue(m.harmonic_l1_lower_bound_holds(n))
        pairs = [(2 * n, n) for n in range(1, 10)]
        self.assertEqual(m.l1_cauchy_fails(m.harmonic, Q(1, 2), pairs), pairs)

    def test_no_exact_limit(self):
        for f in (F, G, H, m.seq({})):
            M = m.support_bound(f)
            for N in range(M + 1, M + 8):
                self.assertTrue(m.harmonic_nonconvergence_bound_holds(f, N))
        with self.assertRaises(ValueError):
            m.harmonic_nonconvergence_bound_holds(F, 3)

    def test_inner_fluctuation_bound(self):
        for mm in range(1, 8):
            for n in range(mm, 12):
                self.assertTrue(m.inner_fluctuation_holds(m.harmonic(mm), m.harmonic(n), m.harmonic(mm + 1), m.harmonic(n + 2)))
                self.assertTrue(m.inner_fluctuation_holds(m.harmonic(mm), m.harmonic(n), F, G))


class DensityAndControlTests(unittest.TestCase):
    def test_grid_approximation(self):
        target = m.seq({0: Q(355, 113), 3: Q(-22, 7), 7: Q(1, 1000003)})
        for r in (Q(1), Q(1, 10), Q(1, 1000)):
            q = m.grid_approximation(target, r)
            self.assertLess(m.sqdist(target, q), r ** 2)
        with self.assertRaises(ValueError):
            m.grid_approximation(target, 0)

    def test_mutation_controls(self):
        self.assertTrue(m.unit_vectors_not_cauchy(3, 4))
        self.assertTrue(m.shifted_modulus_fails())
        self.assertFalse(m.harmonic_l1_lower_bound_holds(1) and m.l1dist(m.harmonic(2), m.harmonic(1)) < Q(1, 2))

    def test_shape_refusals(self):
        with self.assertRaises(ValueError):
            m.fin_inner(X, m.fin_vector([1, 2]))
        with self.assertRaises(ValueError):
            m.seq({-1: 1})
        with self.assertRaises(ValueError):
            m.fin_vector([0.5])
        with self.assertRaises(ValueError):
            m.fin_vector([True])
        with self.assertRaises(ValueError):
            m.fin_inner([1.0], [2.0])
        with self.assertRaises(ValueError):
            m.trunc(-1, F)
        with self.assertRaises(ValueError):
            m.harmonic(-1)
        with self.assertRaises(TypeError):
            m.CauchyCandidate(123, lambda k: k)
        point = m.CauchyCandidate(m.harmonic, m.harmonic_modulus)
        with self.assertRaises(ValueError):
            point.approximant(-1)


class OperatorTests(unittest.TestCase):
    def test_shift_and_projection_are_bounded(self):
        samples = [F, G, H, m.harmonic(7), m.seq({})]
        self.assertTrue(m.bounded_operator_holds(m.shift, 1, samples))
        self.assertTrue(m.bounded_operator_holds(lambda f: m.proj(3, f), 1, samples))
        self.assertTrue(m.bounded_operator_holds(lambda f: m.smul(Q(-3, 2), f), Q(9, 4), samples))
        for f, g in ((F, G), (G, H), (m.harmonic(4), m.harmonic(9))):
            self.assertTrue(m.shift_is_isometric(f, g))
            self.assertTrue(m.operator_lipschitz_holds(m.shift, 1, f, g))
            self.assertTrue(m.operator_lipschitz_holds(lambda v: m.proj(3, v), 1, f, g))
        self.assertFalse(m.bounded_operator_holds(lambda f: m.smul(2, f), 1, samples))
        with self.assertRaises(ValueError):
            m.bounded_operator_holds(m.shift, -1, samples)

    def test_transported_modulus(self):
        mu = m.transported_modulus(m.harmonic_modulus, 1)
        for k in range(0, 4):
            self.assertTrue(m.modulus_holds(lambda n: m.shift(m.harmonic(n)), mu, k, mu(k) + 10))
        mu3 = m.transported_modulus(m.harmonic_modulus, Q(5, 2))
        self.assertEqual(mu3(0), m.harmonic_modulus(3))
        self.assertTrue(m.modulus_holds(lambda n: m.smul(Q(3, 2), m.harmonic(n)), mu3, 1, mu3(1) + 10))

    def test_coord_sum_gap_and_bounded_norms(self):
        self.assertEqual(m.coord_sum(F), Q(7, 2))
        self.assertEqual(m.coord_sum(m.add(F, G)), m.coord_sum(F) + m.coord_sum(G))
        for n in range(1, 12):
            self.assertGreaterEqual(m.coord_sum_gap(n), Q(1, 2))
        for N in range(0, 40):
            self.assertTrue(m.harmonic_norm_sq_le_two_holds(N))
        pairs = [(2 * n, n) for n in range(1, 8)]
        self.assertEqual(m.coord_sum_not_cauchy_refutations(pairs), pairs)
        with self.assertRaises(ValueError):
            m.coord_sum_gap(0)

    def test_certificate(self):
        self.assertEqual(m.certify(), Q(1, 2))
        self.assertEqual(m.certify(1), Q(1, 2))
        self.assertEqual(m.certify(Q(1)), Q(1, 2))
        for probe, invariant in ((1.0, 'float refused at the public boundary'), (True, 'boolean refused where a rational was required'), ('text', 'value is not an exact rational')):
            with self.assertRaises(m.HilbertLiftError) as caught:
                m.certify(probe)
            self.assertEqual(caught.exception.invariant, invariant)
        self.assertEqual(m.main(), 0)


if __name__ == '__main__':
    unittest.main()
