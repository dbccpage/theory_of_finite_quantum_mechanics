"""Exact controls for the exact-sequence certificate (PFP batch 01, PG-WDP-QUOTIENT-EXACT-SEQUENCE)."""
import importlib.util
import unittest
from fractions import Fraction
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_wdp_quotient_sequence.py'
_SPEC = importlib.util.spec_from_file_location('pfp_wdp_quotient_sequence', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)

P = 3


def matvec(rows, v):
    return tuple(sum(a * b for a, b in zip(row, v)) % P for row in rows)


def finite_field_counts(c):
    """Brute force over GF(3): |B1|, |Z1|, number of cosets of B1, the fibre sizes of kappa on cosets."""
    nv, edges, d1, mm = c['nv'], c['edges'], c['d1'], len(c['edges'])
    d0 = m.d0_rows(nv, edges)
    vectors = list(product(range(P), repeat=mm))
    image = {tuple(sum(d0[i][j] * x[j] for j in range(nv)) % P for i in range(mm)) for x in product(range(P), repeat=nv)}
    cosets = {}
    for v in vectors:
        key = min(tuple((a + b) % P for a, b in zip(v, b1)) for b1 in image)
        cosets.setdefault(key, v)
    fibres = {}
    for key, v in cosets.items():
        fibres.setdefault(matvec(d1, v) if d1 else (), []).append(key)
    cycles = [v for v in vectors if (not d1) or not any(matvec(d1, v))]
    return len(image), len(cycles), len(cosets), fibres


class QuotientSequence(unittest.TestCase):
    def test_phi1_matches_integer_lattice_search_including_null_weights(self):
        for c in m.CASES:
            d0 = m.d0_rows(c['nv'], c['edges'])
            best = None
            for x in product(range(-5, 6), repeat=c['nv']):
                cost = sum(c['w'][i] * abs(c['h'][i] - sum(d0[i][j] * x[j] for j in range(c['nv']))) for i in range(len(d0)))
                best = cost if best is None or cost < best else best
            self.assertEqual(m.phi1(c['nv'], c['edges'], c['w'], c['h']), best, c['id'])

    def test_exact_sequence_cardinalities_and_section_count_over_gf3(self):
        for r in m.certificate()['records']:
            if not r['complex']:
                continue
            c = next(c for c in m.CASES if c['id'] == r['id'])
            b1, z1, q1, fibres = finite_field_counts(c)
            self.assertEqual(q1, P ** r['dim_q1'], r['id'])          # |Q1| = 3^(m - rank d0)
            self.assertEqual(z1, b1 * P ** r['dim_h1'], r['id'])      # |H1| = |Z1| / |B1|
            self.assertEqual(len(fibres), P ** r['dim_im'], r['id'])  # kappa maps Q1 onto a space of size 3^(rank d1)
            self.assertEqual(q1, P ** r['dim_h1'] * len(fibres), r['id'])
            self.assertTrue(all(len(f) == P ** r['dim_h1'] for f in fibres.values()), r['id'])  # each fibre is a coset of H1
            # lifts of a basis of im d1: (3^dim H1)^(dim im d1) sections
            self.assertEqual((P ** r['dim_h1']) ** r['dim_im'], P ** r['section_dim'], r['id'])
            self.assertEqual(r['canonical_split'], r['section_dim'] == 0)

    def test_exactly_one_class_on_an_exhaustive_range(self):
        for phi, gam in product(range(0, 6), repeat=2):
            flags = [phi == 0, phi > 0 and gam == 0, phi > 0 and gam > 0]
            self.assertEqual(sum(flags), 1)
        for r in m.certificate()['records']:
            self.assertEqual(r['classes_hit'], 1)

    def test_gamma2_le_operator_norm_times_phi1_on_every_triangle_window(self):
        edges = [[0, 1], [1, 2], [0, 2]]
        tested = 0
        for rows in ([], [[1, 1, -1]], [[1, 1, -1], [-2, -2, 2]]):
            for w in product((1, 2, 3), repeat=3):
                on = m.opnorm(rows, list(w))
                for h in product(range(-2, 3), repeat=3):
                    phi = m.phi1(3, edges, list(w), list(h))
                    gam = m.gamma2(rows, list(h))
                    self.assertLessEqual(gam, on * phi, (rows, w, h))
                    self.assertEqual(phi == 0, m.class_zero(3, edges, list(h)), (w, h))
                    tested += 1
        self.assertEqual(tested, 3 * 27 * 125)

    def test_operator_norm_is_the_least_constant_on_a_box(self):
        for c in m.CASES:
            if not c['d1'] or c['id'].startswith('seminorm'):
                continue
            on = m.opnorm(c['d1'], c['w'])
            ok = True
            tight = False
            for v in product(range(-2, 3), repeat=min(len(c['w']), 4)):
                v = list(v) + [0] * (len(c['w']) - len(v))
                j = sum(a * abs(b) for a, b in zip(c['w'], v))
                g = m.gamma2(c['d1'], v)
                ok = ok and g <= on * j
                tight = tight or (j > 0 and g == on * j)
            self.assertTrue(ok and tight, c['id'])

    def test_named_instances(self):
        by = {r['id']: r for r in m.certificate()['records']}
        self.assertEqual((by['loop_three_faces']['opnorm'], by['loop_three_faces']['phi1'], by['loop_three_faces']['gamma2']), ('3', '1', '3'))
        self.assertEqual(by['tri_heavy_weights']['opnorm'], '1/3')
        self.assertFalse(by['violates_d1d0_edge']['bound_holds'])          # the inequality needs d1 d0 = 0
        self.assertFalse(by['seminorm_zero_weight_unfilled']['phi_zero_iff_class_zero'])
        self.assertIsNone(by['seminorm_zero_weight_filled']['opnorm'])
        self.assertTrue(by['k4_all_faces']['canonical_split'] and by['k4_two_faces']['canonical_split'] is False)
        self.assertEqual([r['id'] for r in by.values() if r['canonical_split'] is False], ['two_triangles_mixed', 'k4_two_faces', 'parallel_bigon_active'])

    def test_wire_format_has_one_line_per_case(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertTrue(lines[0].startswith('seq\ttri_filled_active\t1\t3\t2\t1\t1\t0\t1\t1\t0\t1\t0\t1\t2\t2\tActiveClosureFailure\t1\t1\t1\t1'))
        self.assertEqual(len(m.public_tsv().splitlines()), len(m.CASES))


if __name__ == '__main__':
    unittest.main()
