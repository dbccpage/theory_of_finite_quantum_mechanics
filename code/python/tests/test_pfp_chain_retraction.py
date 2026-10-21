"""Exact controls for the chain retraction certificate (PFP batch 01, PG-CHAIN-RETRACTION)."""
import importlib.util
import unittest
from fractions import Fraction
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_chain_retraction.py'
_SPEC = importlib.util.spec_from_file_location('pfp_chain_retraction', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)
CERT = m.certificate()


def rec(name):
    return next(r for r in CERT['records'] if r['name'] == name)


def subsets(n):
    return [[i for i in range(n) if mask >> i & 1] for mask in range(1 << n)]


class ChainRetraction(unittest.TestCase):
    def test_named_non_examples_have_no_retraction_and_kill_a_class(self):
        for name in ('two_isolated_points_in_edge', 'triangle_boundary_in_filled_triangle'):
            r = rec(name)
            self.assertEqual(r['killed'], 1, name)
            self.assertFalse(r['h_injective'], name)
            self.assertFalse(r['retraction_exists'], name)
            self.assertLess(r['system_rank'], r['augmented_rank'], name)
            self.assertEqual(r['retraction'], [], name)

    def test_extensions_that_kill_nothing_admit_an_explicit_verified_retraction(self):
        checked = 0
        for case in m.CASES:
            r = rec(case[1])
            if not r['retraction_exists']:
                continue
            dims, mats, subs = m.parse(*case[2:])
            ret = [[[Fraction(x) for x in row] for row in mat] for mat in r['retraction']]
            n = len(dims) - 1
            for k in range(n + 1):  # r_k . i_k = id
                for c in range(len(subs[k])):
                    for pos, b in enumerate(subs[k]):
                        self.assertEqual(ret[k][c][b], 1 if pos == c else 0)
            for k in range(1, n + 1):  # d^C r_k = r_{k-1} d^D
                for a in range(len(subs[k - 1])):
                    for b in range(dims[k]):
                        left = sum(mats[k - 1][subs[k - 1][a]][subs[k][c]] * ret[k][c][b] for c in range(len(subs[k])))
                        right = sum(ret[k - 1][a][e] * mats[k - 1][e][b] for e in range(dims[k - 1]))
                        self.assertEqual(left, right)
            checked += 1
        self.assertGreaterEqual(checked, 8)

    def test_retraction_implies_injective_homology_on_every_small_complex(self):
        # brute force over every 3-term complex with dims (2, 2, 1), entries in {-1, 0, 1}, and every basis subset
        total = closed = existing = 0
        for d1 in product((-1, 0, 1), repeat=4):
            M1 = [list(d1[0:2]), list(d1[2:4])]
            for d2 in product((-1, 0, 1), repeat=2):
                M2 = [[d2[0]], [d2[1]]]
                if any(sum(M1[i][t] * M2[t][0] for t in range(2)) for i in range(2)):
                    continue
                dims_s, mats_s = '2,2,1', '%s;%s' % ('/'.join(','.join(map(str, row)) for row in M1), '/'.join(str(r[0]) for r in M2))
                for s0 in subsets(2):
                    for s1 in subsets(2):
                        for s2 in subsets(1):
                            sub_s = ';'.join('.'.join(map(str, s)) if s else '-' for s in (s0, s1, s2))
                            r = m.record('x', dims_s, mats_s, sub_s)
                            total += 1
                            if not r['is_subcomplex']:
                                continue
                            closed += 1
                            if r['retraction_exists']:
                                existing += 1
                                self.assertTrue(r['h_injective'], (dims_s, mats_s, sub_s))
                            else:  # observation over Q: the converse also holds on this family
                                self.assertFalse(r['h_injective'], (dims_s, mats_s, sub_s))
        self.assertGreater(closed, 100)
        self.assertGreater(existing, 50)

    def test_betti_numbers_and_rank_of_induced_map_on_known_complexes(self):
        r = rec('triangle_boundary_in_filled_triangle')
        self.assertEqual((r['betti_C'], r['betti_D'], r['rank_hi']), ([1, 1, 0], [1, 0, 0], [1, 0, 0]))
        r = rec('hollow_tetrahedron_in_solid_tetrahedron')
        self.assertEqual((r['betti_C'], r['betti_D'], r['rank_hi'], r['killed']), ([1, 0, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], 1))
        r = rec('tetrahedron_1_skeleton_in_2_skeleton')
        self.assertEqual((r['betti_C'][1], r['betti_D'][1], r['killed']), (3, 0, 3))

    def test_a_set_that_is_not_a_subcomplex_is_refused(self):
        r = rec('edge_without_its_endpoint_is_not_a_subcomplex')
        self.assertFalse(r['is_subcomplex'])
        self.assertEqual((r['killed'], r['retraction_exists'], r['dims_C']), (-1, False, []))

    def test_zero_and_identity_subcomplexes_are_trivial_retracts(self):
        for name in ('zero_subcomplex', 'identity_inclusion'):
            r = rec(name)
            self.assertTrue(r['retraction_exists'] and r['h_injective'], name)

    def test_wire_format_has_one_line_per_case(self):
        lines = m.wire_lines(CERT)
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[0], 'chain\ttwo_isolated_points_in_edge\t1\t2,1\t2,0\t2,0\t1,0\t1,0\t1\t0\t0\t0\t1')
        self.assertEqual(lines[-1], 'chain\tedge_without_its_endpoint_is_not_a_subcomplex\t0\t3,3,1\t-\t-\t-\t-\t-1\t0\t0\t-1\t-1')


if __name__ == '__main__':
    unittest.main()
