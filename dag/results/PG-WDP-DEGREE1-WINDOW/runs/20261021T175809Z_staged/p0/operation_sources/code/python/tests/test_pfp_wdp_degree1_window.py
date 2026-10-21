"""Exact controls for the degree-1 window certificate (PFP batch 01, PG-WDP-DEGREE1-WINDOW)."""
import importlib.util
import unittest
from fractions import Fraction
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_wdp_degree1_window.py'
_SPEC = importlib.util.spec_from_file_location('pfp_wdp_degree1_window', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)
CERT = m.certificate()


def lattice_phi(c, radius):
    """Brute force: minimum of the weighted L1 residual over integer potentials in [-radius, radius]^nv."""
    d0 = m.d0_rows(c['nv'], c['edges'])
    best = None
    for x in product(range(-radius, radius + 1), repeat=c['nv']):
        cost = sum(c['w'][i] * abs(c['h'][i] - sum(d0[i][j] * x[j] for j in range(c['nv']))) for i in range(len(d0)))
        if best is None or cost < best:
            best = cost
    return best


class Degree1Window(unittest.TestCase):
    def test_phi1_matches_integer_lattice_search_on_every_case(self):
        for c in m.CASES:
            self.assertEqual(m.phi1(c['nv'], c['edges'], c['w'], c['h']), lattice_phi(c, 5), c['id'])

    def test_phi1_is_a_class_function(self):
        for c in m.CASES:
            d0 = m.d0_rows(c['nv'], c['edges'])
            for x in ([1] * c['nv'], list(range(c['nv'])), [(-1) ** j * 2 for j in range(c['nv'])]):
                shifted = [c['h'][i] + sum(d0[i][j] * x[j] for j in range(c['nv'])) for i in range(len(d0))]
                self.assertEqual(m.phi1(c['nv'], c['edges'], c['w'], shifted), m.phi1(c['nv'], c['edges'], c['w'], c['h']), c['id'])

    def test_kappa_defined_exactly_when_d1_d0_vanishes_on_a_small_universe(self):
        # all 2-vertex-pair windows on 3 vertices with 3 edges and a single d1 row in {-1,0,1}^3
        edges = [[0, 1], [1, 2], [0, 2]]
        d0 = m.d0_rows(3, edges)
        complexes = 0
        for row in product((-1, 0, 1), repeat=3):
            defect = m.cochain_defect(3, edges, [list(row)])
            invariant = True
            for h in product((-1, 0, 1), repeat=3):
                for x in product((-1, 0, 1), repeat=3):
                    moved = [h[i] + sum(d0[i][j] * x[j] for j in range(3)) for i in range(3)]
                    if sum(a * b for a, b in zip(row, moved)) != sum(a * b for a, b in zip(row, h)):
                        invariant = False
            self.assertEqual(defect is None, invariant, row)
            complexes += defect is None
        self.assertEqual(complexes, 3)  # (0,0,0), (1,1,-1), (-1,-1,1)

    def test_every_case_has_exactly_one_class_or_a_refusal(self):
        names = {'ExactClass', 'ClosedResidual', 'ActiveClosureFailure', 'NotAWindow'}
        seen = set()
        for r in CERT['records']:
            self.assertIn(r['diag'], names)
            seen.add(r['diag'])
            if r['complex']:
                phi, gam = Fraction(r['phi1']), Fraction(r['gamma2'])
                flags = [phi == 0, phi > 0 and gam == 0, phi > 0 and gam > 0]
                self.assertEqual(sum(flags), 1, r['id'])
        self.assertEqual(seen, names)

    def test_exact_sequence_dimensions_and_ratio(self):
        for r in CERT['records']:
            if r['complex']:
                self.assertEqual(r['dim_q1'], r['dim_h1'] + r['rank_d1'], r['id'])
                self.assertEqual(r['r_cl'] is None, Fraction(r['phi1']) == 0, r['id'])
                if r['r_cl'] is not None:
                    self.assertEqual(Fraction(r['r_cl']) * Fraction(r['phi1']), Fraction(r['gamma2']))
            else:
                self.assertIsNone(r['dim_h1'])
                self.assertIsNone(r['gamma2'])
                self.assertIsNotNone(r['kappa_witness'])

    def test_named_instances(self):
        by = {r['id']: r for r in CERT['records']}
        self.assertEqual((by['tri_filled_active']['phi1'], by['tri_filled_active']['gamma2'], by['tri_filled_active']['r_cl']), ('2', '2', '1'))
        self.assertEqual(by['tri_heavy_weights']['r_cl'], '1/3')
        self.assertEqual(by['k4_three_faces']['phi1'], '3')
        self.assertEqual(by['violates_d1d0_edge']['kappa_witness'], '0:-1')
        self.assertEqual(by['loop_active']['phi1'], '3')

    def test_unrepaired_sum_is_strictly_larger_on_k4(self):
        c = next(c for c in m.CASES if c['id'] == 'k4_three_faces')
        self.assertEqual(sum(w * abs(x) for w, x in zip(c['w'], c['h'])), 5)
        self.assertEqual(m.phi1(c['nv'], c['edges'], c['w'], c['h']), 3)

    def test_certificates_carry_a_primal_potential_and_a_dual_vector(self):
        by = {c['id']: c for c in m.CASES}
        for r in CERT['records']:
            c = by[r['id']]
            xt, yt = r['witness'][2:].split('|y=')
            x = [Fraction(t) for t in xt.split(',')]
            y = [Fraction(t) for t in yt.split(',')]
            d0 = m.d0_rows(c['nv'], c['edges'])
            self.assertEqual(m.cost(d0, c['w'], c['h'], x), Fraction(r['phi1']), c['id'])
            self.assertEqual(sum(a * b for a, b in zip(y, c['h'])), Fraction(r['phi1']), c['id'])
            self.assertTrue(all(sum(y[e] * d0[e][v] for e in range(len(y))) == 0 for v in range(c['nv'])), c['id'])
            self.assertTrue(all(abs(y[e]) <= c['w'][e] for e in range(len(y))), c['id'])

    def test_gauge_shifted_window_has_the_same_invariants(self):
        by = {r['id']: r for r in CERT['records']}
        a, b = by['tri_filled_active'], by['tri_filled_active_shifted']
        self.assertEqual([a[k] for k in ('phi1', 'gamma2', 'r_cl', 'diag')], [b[k] for k in ('phi1', 'gamma2', 'r_cl', 'diag')])

    def test_wire_format_has_one_line_per_case(self):
        lines = m.wire_lines(CERT)
        self.assertEqual(len(lines), len(m.CASES))
        self.assertTrue(lines[0].startswith('window\ttri_filled_active\t3\t3\t1\t2\t1\t1\t1\t0\t2\t2\t1\tActiveClosureFailure\t-'))
        self.assertEqual(len(m.public_tsv().splitlines()), len(m.CASES))


if __name__ == '__main__':
    unittest.main()
