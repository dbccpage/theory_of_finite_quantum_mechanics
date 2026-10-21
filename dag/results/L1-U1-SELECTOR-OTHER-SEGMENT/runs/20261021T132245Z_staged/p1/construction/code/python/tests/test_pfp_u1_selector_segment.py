"""Exact controls for the rational unit-circle torsion certificate (PFP batch 01, L1-U1-SELECTOR-OTHER-SEGMENT)."""
import importlib.util
import unittest
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_u1_selector_segment.py'
_SPEC = importlib.util.spec_from_file_location('pfp_u1_selector_segment', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def circle_points(max_den):
    """All rational circle points whose x and y have denominators dividing some c <= max_den, by brute force over a^2 + b^2 = c^2."""
    pts = set()
    for c in range(1, max_den + 1):
        for a in range(-c, c + 1):
            rest = c * c - a * a
            b = isqrt(rest)
            if b * b == rest:
                pts.add((F(a, c), F(b, c)))
                pts.add((F(a, c), F(-b, c)))
    return pts


def gpow(a, b, n):
    re, im = 1, 0
    for _ in range(n):
        re, im = re * a - im * b, re * b + im * a
    return re, im


class U1SelectorSegment(unittest.TestCase):
    def test_torsion_of_the_rational_circle_is_mu4_on_every_point_of_denominator_up_to_200(self):
        pts = circle_points(200)
        self.assertGreater(len(pts), 100)
        torsion = set()
        for x, y in pts:
            d = x.denominator * y.denominator // gcd(x.denominator, y.denominator)
            a, b = int(x * d), int(y * d)
            for n in range(1, 25):
                if gpow(a, b, n) == (d ** n, 0):
                    torsion.add((x, y))
                    break
        self.assertEqual(torsion, {(F(1), F(0)), (F(-1), F(0)), (F(0), F(1)), (F(0), F(-1))})

    def test_valuation_law_at_every_prime_dividing_den_of_twice_x(self):
        for x, y in circle_points(60):
            t = 2 * x
            if t.denominator == 1:
                continue
            d = x.denominator * y.denominator // gcd(x.denominator, y.denominator)
            a, b = int(x * d), int(y * d)
            for p in range(2, t.denominator + 1):
                if t.denominator % p or any(p % q == 0 for q in range(2, p)):
                    continue
                dv = 0
                n = t.denominator
                while n % p == 0:
                    n //= p
                    dv += 1
                for k in range(1, 9):
                    re = gpow(a, b, k)[0] * 2
                    v = 0
                    while re % p == 0:
                        re //= p
                        v += 1
                    vd = 0
                    nd = d
                    while nd % p == 0:
                        nd //= p
                        vd += 1
                    self.assertEqual(v - k * vd, -k * dv, (x, y, p, k))

    def test_half_integer_x_has_no_rational_y_and_the_unit_points_have_the_right_orders(self):
        for r in range(-300, 301):
            for s in range(1, 41):
                self.assertNotEqual(F(r, s) ** 2, F(3, 4))
        recs = {k: m.record_half(k) for k in range(-2, 3)}
        self.assertEqual([recs[k]['status'] for k in range(-2, 3)], ['unit_points', 'refused_irrational_y', 'unit_points', 'refused_irrational_y', 'unit_points'])
        self.assertEqual((recs[-2]['orders'], recs[0]['orders'], recs[2]['orders']), ([2], [4, 4], [1]))

    def test_cayley_map_reaches_every_point_except_the_south_pole(self):
        for x, y in circle_points(40):
            if x == -1:
                continue
            mm, nn = y, 1 + x  # the inverse Cayley parameters used in the kernel
            c = nn * nn + mm * mm
            self.assertEqual(((nn * nn - mm * mm) / c, 2 * mm * nn / c), (x, y))
        for (mm, nn) in [(0, 1), (1, 1), (1, 2), (3, 4), (5, 12)]:
            r = m.record_point(mm, nn)
            self.assertEqual(F(r['x']) ** 2 + F(r['y']) ** 2, 1)

    def test_records_match_the_known_instances(self):
        r = m.record_point(1, 2)
        self.assertEqual((r['x'], r['y'], r['prime'], r['valuations'], r['order'], r['mu4']), ('3/5', '4/5', 5, [-1, -2, -3, -4, -5, -6], 0, False))
        self.assertEqual(m.record_point(1, 1)['order'], 4)
        self.assertEqual(m.record_point(0, 1)['order'], 1)
        self.assertEqual(m.record_point(1, 0)['order'], 2)
        self.assertEqual(m.record_point(3, 4)['valuations'], [-2, -4, -6, -8, -10, -12])

    def test_census_cayley_points_include_mu4_and_the_south_pole(self):
        for b in (1, 2, 3, 4, 6):
            r = m.record_census(b)
            self.assertEqual((r['mu4_points'], r['reaches_minus_one'], r['other_points_have_nonintegral_2x']), (4, True, True))
            self.assertEqual(r['points'], r['mu4_points'] + r['other_points'])
        self.assertEqual((m.record_census(3)['points'], m.record_census(6)['points']), (16, 48))

    def test_unit_circle_over_finite_fields_has_p_minus_or_plus_one_points_and_is_cyclic(self):
        for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53):
            pts = [(x, y) for x in range(p) for y in range(p) if (x * x + y * y) % p == 1 % p]
            r = m.record_ffcircle(p)
            self.assertEqual(r['count'], len(pts))
            self.assertTrue(r['cyclic'])
            self.assertEqual(r['count'], p if p == 2 else p - 1 if p % 4 == 1 else p + 1)
            self.assertEqual(r['orders_beyond_four'], len(pts) not in (1, 2, 4))
        self.assertFalse(m.record_ffcircle(3)['orders_beyond_four'])
        self.assertTrue(m.record_ffcircle(7)['orders_beyond_four'])

    def test_wire_format_has_one_line_per_case_and_no_empty_field(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        for line in lines:
            self.assertTrue(all(line.split('\t')) and line == line.strip())
        self.assertEqual(lines[1], 'half\t-1\t-1/2\t3/4\t-\t-\trefused_irrational_y')
        self.assertEqual(lines[9], 'point\t1\t2\t3/5\t4/5\t0\t5\t-1,-2,-3,-4,-5,-6\t0\t0')
        self.assertEqual(len(m.public_tsv().splitlines()), len(m.CASES))


if __name__ == '__main__':
    unittest.main()
