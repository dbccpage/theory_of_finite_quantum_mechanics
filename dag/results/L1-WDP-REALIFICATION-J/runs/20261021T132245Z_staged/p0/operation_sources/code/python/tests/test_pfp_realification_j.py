"""Exact controls for the realification / declared-J certificate (PFP batch 01, L1-WDP-REALIFICATION-J)."""
import importlib.util
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_realification_j.py'
_SPEC = importlib.util.spec_from_file_location('pfp_realification_j', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)

G = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(1), F(1))]


def mats(rows, cols, pool):
    for flat in product(pool, repeat=rows * cols):
        yield [list(flat[i * cols:(i + 1) * cols]) for i in range(rows)]


class RealificationJ(unittest.TestCase):
    def test_multiplicativity_and_intertwining_exhaustive_on_small_2x2(self):
        pool = G[:3]
        count = 0
        for A in mats(2, 2, pool):
            RA = m.realify(A)
            self.assertEqual(m.rmatmul(m.jmat(2), RA), m.rmatmul(RA, m.jmat(2)))
            self.assertEqual(m.realify(m.imul(A)), m.rmatmul(m.jmat(2), RA))
            self.assertEqual(m.realify(m.star(A)), m.transpose(RA))
            for B in mats(2, 2, G[1:3]):
                self.assertEqual(m.realify(m.cmatmul(A, B)), m.rmatmul(RA, m.realify(B)))
                count += 1
        self.assertEqual(count, 81 * 16)

    def test_injective_and_additive_on_a_box(self):
        seen = {}
        for A in mats(1, 2, G):
            key = tuple(map(tuple, m.realify(A)))
            self.assertNotIn(key, seen)
            seen[key] = A
        a, b = [[G[3], G[1]]], [[G[2], G[3]]]
        s = [[(a[0][j][0] + b[0][j][0], a[0][j][1] + b[0][j][1]) for j in range(2)]]
        sumR = [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(m.realify(a), m.realify(b))]
        self.assertEqual(m.realify(s), sumR)

    def test_image_equals_commutant_of_J(self):
        # Theorem 2 exhaustively on: all 2 x 2 over {-1,0,1}; all 2 x 4 over {0,1}; 4 x 4 over {0,1} with zero lower rows;
        # and on every R(A) with A in {0,1,i,1+i}^{2x2} (all of which commute).
        def decide(M):
            rows, cols = len(M), len(M[0])
            comm = m.rmatmul(m.jmat(rows // 2), M) == m.rmatmul(M, m.jmat(cols // 2))
            self.assertEqual(comm, m.realify(m.recover(M)) == M)
            return comm

        pm = (F(-1), F(0), F(1))
        self.assertEqual(sum(decide([list(f[:2]), list(f[2:])]) for f in product(pm, repeat=4)), 9)  # [[a,-b],[b,a]] with a, b in {-1,0,1}
        bits = (F(0), F(1))
        n24 = sum(decide([list(f[:4]), list(f[4:])]) for f in product(bits, repeat=8))
        self.assertEqual(n24, 4)  # rows (p1,p2,-q1,-q2) and (q1,q2,p1,p2) with entries in {0,1} force q = 0, p free: 4
        n44 = sum(decide([list(f[:4]), list(f[4:]), [F(0)] * 4, [F(0)] * 4]) for f in product(bits, repeat=8))
        self.assertEqual(n44, 1)  # zero lower rows (Q, P) force P = Q = 0
        for A in mats(2, 2, G):
            self.assertTrue(decide(m.realify(A)))

    def test_trace_is_twice_the_real_part_not_twice_the_complex_trace(self):
        A = [[(F(1), F(1))]]
        self.assertEqual(sum(m.realify(A)[i][i] for i in range(2)), 2)
        r = m.record_prod(1, 1, 1, ['1:1'], ['1:0'])
        self.assertEqual((r['trace_real'], r['trace_complex'], r['trace_identity'], r['trace_twice_complex']), ('2', '1:1', '1', '0'))
        for A in mats(2, 2, G):
            tr = sum(A[i][i][0] for i in range(2))
            self.assertEqual(sum(m.realify(A)[i][i] for i in range(4)), 2 * tr)

    def test_unrestricted_real_matrices_and_odd_dimensions_are_refused(self):
        d = lambda *v: [str(x) for i in range(len(v)) for x in [v[i] if i == j else 0 for j in range(len(v))]]
        self.assertEqual(m.record_img(4, 4, d(1, 0, 0, 0))['status'], 'noncommuting')
        self.assertEqual(m.record_img(4, 4, d(1, 1, -1, -1))['anticommutes'], '1')
        self.assertEqual(m.record_img(2, 2, d(1, -1))['anticommutes'], '1')
        self.assertEqual(m.record_img(3, 3, d(1, 1, 1))['status'], 'odd_dim')
        sym = m.record_img(4, 4, d(1, 2, 3, 4))
        self.assertEqual((sym['symmetric'], sym['status']), ('1', 'noncommuting'))
        self.assertEqual(m.record_img(2, 2, ['2', '3', '-3', '2'])['recovered'], ['2:-3'])  # the other sign convention is R(conj z)

    def test_square_roots_of_minus_one_census_matches_brute_force_and_only_pm_J_commutes(self):
        for B in range(1, 6):
            brute = [X for X in product(range(-B, B + 1), repeat=4) if m.mul2(X, X) == (-1, 0, 0, -1)]
            self.assertEqual(sorted(m.census(B)), sorted(brute))
            rec = m.record_jcensus(B)
            self.assertEqual((rec['total'], rec['commuting_J'], rec['pm_J']), (len(brute), 2, 2))
        other = m.record_jstruct(1, -1, 2, -1)
        self.assertEqual((other['sq_neg_id'], other['pm_J'], other['commutes_J']), (True, False, False))

    def test_positivity_is_preserved_and_reflected_on_all_small_hermitian_2x2(self):
        pool = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(1), F(1)), (F(-1), F(1))]
        count = 0
        for a, d in product((-1, 0, 1, 2), repeat=2):
            for b in pool:
                toks = ['%d:0' % a, '%s:%s' % b, '%s:%s' % (b[0], -b[1]), '%d:0' % d]
                rec = m.record_psd(2, toks)
                direct = a >= 0 and d >= 0 and a * d - (b[0] ** 2 + b[1] ** 2) >= 0
                self.assertEqual((rec['complex_psd'], rec['real_psd'], rec['agree']), (m.bit(direct), m.bit(direct), '1'), toks)
                count += 1
        self.assertEqual(count, 80)
        self.assertEqual(m.record_psd(2, ['1:0', '0:1', '0:1', '1:0'])['hermitian'], '0')

    def test_interleaved_ordering_is_a_different_matrix_and_a_different_J(self):
        one = m.record_prod(1, 1, 1, ['1:1'], ['2:-3'])
        self.assertEqual((one['RA_interleaved'], one['interleaved_commutes_block_J']), (['1', '-1', '1', '1'], True))
        two = m.record_prod(2, 2, 2, ['1:1', '2:0', '0:-1', '3:0'], ['1:0', '0:0', '0:0', '1:0'])
        self.assertNotEqual(two['RA_interleaved'], m.flat(m.realify(m.gparse(two['input'][4], 2, 2))))
        self.assertFalse(two['interleaved_commutes_block_J'])
        A = m.gparse(['1:1', '2:0', '0:-1', '3:0'], 2, 2)
        self.assertEqual(two['RAstar'], m.flat(m.realify(m.star(A))))
        self.assertNotEqual(two['RAstar'], m.flat(m.realify([list(r) for r in zip(*A)])))

    def test_wire_format_has_one_line_per_case_and_no_empty_field(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        for line in lines:
            self.assertTrue(all(line.split('\t')) and line == line.strip())
        self.assertEqual(lines[0], 'prod\t1\t1\t1\t5,1,-1,5\t1,1,-1,1\t1,-1,1,1\t1\t1\t1\t1\t1\t1\t0\t0\t2\t1:1\t1\t0')
        self.assertEqual(len(m.public_tsv().splitlines()), len(m.CASES))


if __name__ == '__main__':
    unittest.main()
