from fractions import Fraction as Q
from pathlib import Path
import importlib, sys, types, unittest

pkg = types.ModuleType('staged_qm')
pkg.__path__ = [str(Path(__file__).resolve().parents[1] / 'src/qm')]
sys.modules[pkg.__name__] = pkg
m = importlib.import_module('staged_qm.qc_self_obstruction')


class ConstantOverheadTests(unittest.TestCase):
    def test_closed_form_and_literal_values(self):
        # c = 4, p0 = 1/10: r = 2/5, p_k = (2/5)^(2^k) / 4
        self.assertEqual([m.conc(4, Q(1, 10), k) for k in range(4)],
                         [Q(1, 10), Q(1, 25), Q(4, 625), Q(64, 390625)])
        for k in range(8):
            self.assertTrue(m.conc_closed_holds(4, Q(1, 10), k))
            self.assertTrue(m.conc_closed_holds(Q(3, 2), Q(-1, 7), k))   # no sign assumption

    def test_three_regimes(self):
        self.assertEqual(m.classify(4, Q(1, 10)), 'below')
        self.assertEqual(m.classify(4, Q(1, 4)), 'fixed')
        self.assertEqual(m.classify(4, Q(3, 10)), 'above')
        self.assertEqual(m.threshold(4), Q(1, 4))
        # fixed point: constant 1/c
        self.assertTrue(all(m.conc(4, Q(1, 4), k) == Q(1, 4) for k in range(10)))
        # below: strictly decreasing, doubly exponential, tends below any epsilon
        seq = [m.conc(4, Q(1, 10), k) for k in range(8)]
        self.assertTrue(all(b < a for a, b in zip(seq, seq[1:])))
        self.assertEqual(m.first_level_below(4, Q(1, 10), Q(1, 10 ** 9)), 5)
        # above: strictly increasing and leaves any bound
        up = [m.conc(4, Q(3, 10), k) for k in range(6)]
        self.assertTrue(all(b > a for a, b in zip(up, up[1:])))
        self.assertEqual(m.first_level_above(4, Q(3, 10), 1), 3)
        self.assertIsNotNone(m.first_level_above(4, Q(3, 10), 10 ** 30))

    def test_half_bound(self):
        for k in range(8):
            self.assertTrue(m.half_bound_holds(4, Q(1, 8), k))
        with self.assertRaises(ValueError):
            m.half_bound_holds(4, Q(1, 4), 1)

    def test_exactly_at_threshold_boundary_pair(self):
        # one rational step either side of 1/c separates the regimes
        eps = Q(1, 10 ** 6)
        self.assertEqual(m.classify(7, Q(1, 7) - eps), 'below')
        self.assertEqual(m.classify(7, Q(1, 7) + eps), 'above')

    def test_unrepaired_union_bound_never_contracts(self):
        for a in (1, 2, 5):
            vals = [m.linear_level(a, Q(1, 100), k) for k in range(6)]
            self.assertTrue(all(v >= Q(1, 100) for v in vals))

    def test_pair_count_and_threshold_drop(self):
        self.assertEqual([m.pair_count(a) for a in (2, 3, 4, 10)], [1, 3, 6, 45])
        self.assertTrue(m.threshold(m.pair_count(10)) < m.threshold(m.pair_count(4)))

    def test_refusals(self):
        for bad in (0.5, True, 'x'):
            with self.assertRaises(ValueError):
                m.conc(bad, 1, 1)
        with self.assertRaises(ValueError):
            m.classify(0, 1)
        with self.assertRaises(ValueError):
            m.conc(1, 1, -1)


class LevelDependentOverheadTests(unittest.TestCase):
    def test_amp_closed_form(self):
        cs = [Q(2), Q(3), Q(5), Q(7)]
        self.assertEqual([m.amp(cs, k) for k in range(5)], [1, 2, 12, 720, 7 * 720 ** 2])
        for k in range(5):
            self.assertTrue(m.concv_amp_holds(cs, Q(1, 9), k))

    def test_constant_case_reduces(self):
        cs = m.const_family(4, 6)
        for k in range(7):
            self.assertEqual(m.concv(cs, Q(1, 10), k), m.conc(4, Q(1, 10), k))

    def test_bounded_and_exponential_and_polynomial_stay_bounded(self):
        self.assertTrue(m.const_invariant_holds(m.const_family(9, 10), 9))
        self.assertTrue(m.amp_bound_holds(m.const_family(9, 10), 9))
        for A in (1, 2, 5):
            self.assertTrue(m.exp_invariant_holds(A, 10))
            self.assertTrue(m.amp_bound_holds(m.exp_family(A, 10), 4 * A))
            for B in (1, 2, 3, Q(7, 2)):
                self.assertTrue(m.geom_invariant_holds(A, B, 8))
                self.assertTrue(m.amp_bound_holds(m.geom_family(A, B, 8), A * Q(B) ** 2))
        # (k+1)^2 <= 2 * 2^(k+1): covered by A = 2, so M = 8 bounds it
        self.assertTrue(all((k + 1) ** 2 <= 2 * 2 ** (k + 1) for k in range(40)))
        self.assertTrue(m.amp_bound_holds(m.poly_family(10), 8))

    def test_double_exponential_family_escapes_every_bound(self):
        a, b = Q(1), Q(2)
        self.assertTrue(m.dexp_square_identity_holds(a, b, 10))
        self.assertTrue(m.dexp_square_identity_holds(Q(3, 2), Q(5, 4), 9))
        cs = m.dexp_family(a, b, 14)
        # finite refutations of ever larger M: amp_k > M^(2^k) once b^k > M^2 (Lean: dexp_not_ampBounded)
        levels = [m.amp_escape_level(cs, M) for M in (2, 10, 100)]
        self.assertEqual(levels, [3, 7, 14])
        # while the bounded families have no escape level
        self.assertIsNone(m.amp_escape_level(m.exp_family(1, 14), 4))
        self.assertIsNone(m.amp_escape_level(m.poly_family(14), 8))

    def test_dexp_error_leaves_unit_interval_for_positive_p0(self):
        cs = m.dexp_family(Q(1), Q(2), 14)
        for p0, level in ((Q(1, 10), 7), (Q(1, 50), 12)):
            first = next(k for k in range(15) if m.concv(cs, p0, k) >= 1)
            self.assertEqual(first, level)
            self.assertTrue(all(m.concv(cs, p0, k) >= 1 for k in range(level, 15)))

    def test_block_size_growth_below_and_at_the_squaring_ratio(self):
        # N_{k+1} = floor(3/2 N_k): ratio s = 3/2 < 2, overhead 2^(N_k): weighted means stay bounded
        sizes = [8]
        for _ in range(11):
            sizes.append(sizes[-1] * 3 // 2)
        self.assertTrue(all(sizes[k + 1] <= Q(3, 2) * sizes[k] for k in range(11)))
        self.assertTrue(m.block_exp_bound_holds(sizes, Q(3, 2)))
        cs = m.size_family(1, 2, sizes)
        L = 16                                   # ceil(N_0 / (2 - s)) = ceil(8 / (1/2))
        self.assertTrue(m.amp_bound_holds(cs, Q(2) ** L))
        # block size doubling per level (ratio 2): the same overhead escapes each fixed bound
        dbl = [2 ** k for k in range(10)]
        cd = m.size_family(1, 2, dbl)
        self.assertEqual([m.amp_escape_level(cd, Q(2) ** e) for e in (2, 3)], [5, 7])
        with self.assertRaises(ValueError):
            m.block_exp_bound_holds(dbl, 2)

    def test_sandwich_between_constant_overheads(self):
        # a <= c_k <= b gives concv between conc a and conc b
        cs = [Q(2), Q(3), Q(2), Q(3), Q(2), Q(3)]
        for k in range(7):
            self.assertTrue(m.conc(2, Q(1, 10), k) <= m.concv(cs, Q(1, 10), k) <= m.conc(3, Q(1, 10), k))


class RepairBacklogTests(unittest.TestCase):
    def test_equal_and_sufficient_and_insufficient_rates(self):
        # lam = 1, g = 1/2: net rate (1 - g) mu; mu = 2 is exactly enough
        self.assertTrue(m.backlog_bounded_decision(1, Q(1, 2), 2))
        self.assertEqual(m.backlog(1, Q(1, 2), 2, 5, 6), [5] * 7)
        self.assertEqual(m.backlog(1, Q(1, 2), 4, 3, 5), [3, 2, 1, 0, 0, 0])
        self.assertFalse(m.backlog_bounded_decision(1, Q(1, 2), Q(3, 2)))
        self.assertEqual(m.backlog(1, Q(1, 2), Q(3, 2), 0, 4), [0, Q(1, 4), Q(1, 2), Q(3, 4), 1])

    def test_unit_gain_repair_never_bounds(self):
        for mu in (0, 1, 10, 1000):
            self.assertFalse(m.backlog_bounded_decision(Q(1, 100), 1, mu))
            tr = m.backlog(Q(1, 100), 1, mu, 0, 5)
            self.assertEqual(tr, [Q(k, 100) for k in range(6)])

    def test_supply_threshold_and_no_supply(self):
        self.assertEqual(m.supply_threshold(1, Q(1, 2), 1), 2)
        self.assertEqual(m.backlog(1, Q(1, 2), 1 * 0, 0, 3), [0, 1, 2, 3])
        with self.assertRaises(ValueError):
            m.supply_threshold(1, 1, 1)

    def test_budget_bounds_rounds(self):
        self.assertEqual(m.rounds_upper_bound(10, Q(1, 2)), 20)
        with self.assertRaises(ValueError):
            m.rounds_upper_bound(1, 0)


class DepolarizingDecayTests(unittest.TestCase):
    def setUp(self):
        self.Rz = m.rot_z(Q(-7, 25), Q(24, 25))     # 2 phi with cos phi = 3/5, sin phi = 4/5
        self.Rx = m.rot_x(Q(-7, 25), Q(24, 25))
        self.r = [Q(1, 2), Q(1, 3), Q(1, 6)]
        self.s = [Q(-1, 5), Q(2, 5), Q(3, 5)]

    def test_rotations_are_exact_rotations(self):
        self.assertTrue(m.is_rational_rotation(self.Rz))
        self.assertTrue(m.is_rational_rotation(self.Rx))
        with self.assertRaises(ValueError):
            m.rot_z(Q(1, 2), Q(1, 2))

    def test_squared_distance_contracts_exactly(self):
        hist = [(Q(1, 10), self.Rz), (Q(1, 5), self.Rx), (Q(1, 20), self.Rz)]
        self.assertTrue(m.decay_identity_holds(hist, self.r, self.s))
        self.assertEqual(m.contraction_factor_sq(hist), (Q(9, 10) * Q(4, 5) * Q(19, 20)) ** 2)

    def test_uniform_rate_gives_power(self):
        p = Q(1, 10)
        hist = [(p, self.Rz)] * 5
        d0 = m.bloch_sq_dist(self.r, self.s)
        self.assertEqual(m.bloch_sq_dist(m.bloch_run(hist, self.r), m.bloch_run(hist, self.s)),
                         ((1 - p) ** 2) ** 5 * d0)

    def test_matrix_level_agrees_with_bloch_level(self):
        U1 = m.unitary_about('z', Q(3, 5), Q(4, 5))
        U2 = m.unitary_about('x', Q(3, 5), Q(4, 5))
        p = Q(1, 7)
        rho, ref = m.bloch_matrix(self.r), self.r
        for U, R in ((U1, self.Rz), (U2, self.Rx), (U1, self.Rz)):
            rho = m.matrix_step(p, U, rho)
            ref = m.bloch_step(p, R, ref)
            self.assertEqual(m.bloch_of_matrix(rho), ref)

    def test_pauli_part_squares_to_norm(self):
        for v in ([1, 2, 3], [Q(1, 2), 0, Q(-3, 5)], [0, 0, 0]):
            self.assertTrue(m.pauli_part_squares_to_norm(v))

    def test_decay_bound_and_depth(self):
        for p in (Q(1, 10), Q(1, 2), Q(1, 1000)):
            for t in range(0, 40):
                self.assertTrue(m.decay_le_inv_holds(p, t))
        # depth after which at most 1/1000 of the distance remains at rate 1/10
        t = m.depth_until_below(Q(1, 10), Q(1, 1000))
        self.assertEqual(t, 66)
        self.assertTrue((1 - Q(1, 10)) ** t <= Q(1, 1000) < (1 - Q(1, 10)) ** (t - 1))
        # Lean decay_below: t >= (1/delta - 1)/p suffices, here 9990 >= 66
        self.assertGreaterEqual(9990, t)


class AssembledCertificateTests(unittest.TestCase):
    def test_conditions_are_all_needed(self):
        ok = m.viability_report(1, Q(1, 2), 1, 2, 4, Q(1, 10), 10 ** 6, Q(1, 100))
        self.assertTrue(ok['certified'])
        self.assertEqual(ok['level'], m.level_for_failure(4, Q(1, 10), 10 ** 6, Q(1, 100)))
        self.assertFalse(m.viability_report(1, Q(1, 2), 1, Q(19, 10), 4, Q(1, 10), 10 ** 6, Q(1, 100))['certified'])
        self.assertFalse(m.viability_report(1, 1, 1, 100, 4, Q(1, 10), 10 ** 6, Q(1, 100))['certified'])
        self.assertFalse(m.viability_report(1, Q(1, 2), 1, 2, 4, Q(3, 10), 10 ** 6, Q(1, 100))['certified'])

    def test_level_grows_doubly_logarithmically_with_circuit_size(self):
        small = m.level_for_failure(4, Q(1, 10), 10 ** 3, Q(1, 100))
        huge = m.level_for_failure(4, Q(1, 10), 10 ** 60, Q(1, 100))
        self.assertTrue(small < huge)
        self.assertLessEqual(huge - small, 5)

    def test_authority_fence(self):
        self.assertEqual(m.AUTHORITY_EFFECT, 'AuthorityEffect: None')
        self.assertIn('not a proof', m.FENCE)


if __name__ == '__main__':
    unittest.main()
