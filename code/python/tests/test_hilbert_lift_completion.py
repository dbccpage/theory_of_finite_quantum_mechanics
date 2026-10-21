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


if __name__ == '__main__':
    unittest.main()
