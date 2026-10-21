"""Torsion of the rational unit circle (unit Gaussian rationals) and what finite phase carriers can select.

Producer for PFP batch 01, node L1-U1-SELECTOR-OTHER-SEGMENT (a pointer node: the selection of C and U(1) from
finite carriers is owned by another segment and is NOT established here). Exact Fractions and integers only.
Four record kinds:
  half   the exhaustive list of rational circle points with 2x an integer (2x = k, |k| <= 2): x = k/2, y^2 = 1 - x^2,
         the rational y (if any) and the exact order of each point; x = +-1/2 is refused because 3/4 is no rational square;
  point  the rational circle point with Cayley parameters (m, n): x = (n^2 - m^2)/(n^2 + m^2), y = 2mn/(n^2 + m^2),
         whether 2x is an integer, the smallest prime p dividing den(2x), the p-adic valuations of 2 Re z^k for k = 1..6
         (the recurrence 2 Re z^(k+1) = 2x (2 Re z^k) - 2 Re z^(k-1) predicts -k v_p(den 2x)), and the exact order
         (smallest n <= 12 with z^n = 1, or 0). Real parts and imaginary parts are iterated with the three-term recurrence.
  census   all Cayley points with |m|, |n| <= B (B = 3, 6): how many distinct circle points, how many of them are in mu_4 (order <= 12),
           whether (-1, 0) is reached (it is: n = 0), and that every point outside mu_4 has 2x not an integer;
  ffcircle the unit circle x^2 + y^2 = 1 over the finite field F_p (a finite carrier proper): it has p - 1 points if p = 1 mod 4,
           p + 1 if p = 3 mod 4 (p if p = 2), is cyclic, and so carries phases of orders other than 1, 2, 4 (native table only).
Not a statement about completion, continuity, the compact group U(1), the complex field, or physics. AuthorityEffect: None.
"""
from fractions import Fraction
from math import isqrt

CASES = [
    ['half', -2], ['half', -1], ['half', 0], ['half', 1], ['half', 2],
    ['point', 0, 1], ['point', 1, 0], ['point', 1, 1], ['point', -1, 1],
    ['point', 1, 2], ['point', 2, 1], ['point', 1, 3], ['point', 2, 3], ['point', 3, 2], ['point', 1, 4],
    ['point', 3, 4], ['point', 1, 8], ['point', 4, 7], ['point', 5, 12], ['point', 2, 5],
    ['census', 3], ['census', 6],
    ['ffcircle', 2], ['ffcircle', 3], ['ffcircle', 5], ['ffcircle', 7], ['ffcircle', 11], ['ffcircle', 13], ['ffcircle', 17], ['ffcircle', 19],
    ['ffcircle', 23], ['ffcircle', 29], ['ffcircle', 31], ['ffcircle', 41], ['ffcircle', 43],
]

ORDER_BOUND = 12
POWERS = 6


def rational_sqrt(q):
    """The nonnegative rational square root of q, or None."""
    if q < 0:
        return None
    a, b = isqrt(q.numerator), isqrt(q.denominator)
    return Fraction(a, b) if a * a == q.numerator and b * b == q.denominator else None


def power_sequences(x, y):
    """(Re z^k, Im z^k) for k = 0..ORDER_BOUND by the recurrence z^(k+2) = 2x z^(k+1) - z^k (valid when x^2 + y^2 = 1)."""
    re, im = [Fraction(1), x], [Fraction(0), y]
    for k in range(ORDER_BOUND - 1):
        re.append(2 * x * re[-1] - re[-2])
        im.append(2 * x * im[-1] - im[-2])
    return re, im


def exact_order(x, y):
    re, im = power_sequences(x, y)
    for n in range(1, ORDER_BOUND + 1):
        if re[n] == 1 and im[n] == 0:
            return n
    return 0


def smallest_prime_factor(n):
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n


def valuation(q, p):
    """p-adic valuation of a nonzero rational."""
    def v(n):
        count = 0
        while n % p == 0:
            n //= p
            count += 1
        return count
    return v(q.numerator) - v(q.denominator)


def record_half(k):
    x = Fraction(k, 2)
    y2 = 1 - x * x
    y = rational_sqrt(y2)
    if y is None:
        return {'kind': 'half', 'input': ['half', k], 'x': str(x), 'y_squared': str(y2), 'y_values': [], 'orders': [], 'status': 'refused_irrational_y'}
    ys = sorted({y, -y})
    return {'kind': 'half', 'input': ['half', k], 'x': str(x), 'y_squared': str(y2), 'y_values': [str(v) for v in ys],
            'orders': [exact_order(x, v) for v in ys], 'status': 'unit_points'}


def record_point(m, n):
    c = n * n + m * m
    x, y = Fraction(n * n - m * m, c), Fraction(2 * m * n, c)
    assert x * x + y * y == 1
    twice = 2 * x
    integral = twice.denominator == 1
    p = 0 if integral else smallest_prime_factor(twice.denominator)
    re, _ = power_sequences(x, y)
    vals = [] if integral else [valuation(2 * re[k], p) for k in range(1, POWERS + 1)]
    order = exact_order(x, y)
    return {'kind': 'point', 'input': ['point', m, n], 'x': str(x), 'y': str(y), 'twice_x_integral': integral, 'prime': p,
            'valuations': vals, 'order': order, 'mu4': order in (1, 2, 4)}


def circle_point(m, n):
    c = n * n + m * m
    return Fraction(n * n - m * m, c), Fraction(2 * m * n, c)


def record_census(bound):
    pts = {circle_point(m, n) for m in range(-bound, bound + 1) for n in range(-bound, bound + 1) if (m, n) != (0, 0)}
    mu4 = [p for p in pts if exact_order(*p) in (1, 2, 4)]
    other = [p for p in pts if p not in mu4]
    return {'kind': 'census', 'input': ['census', bound], 'points': len(pts), 'mu4_points': len(mu4), 'other_points': len(other),
            'reaches_minus_one': (Fraction(-1), Fraction(0)) in pts,
            'other_points_have_nonintegral_2x': all((2 * x).denominator != 1 for x, _ in other)}


def record_ffcircle(p):
    # count by the Euler criterion (-1 is a square mod p iff p = 1 mod 4); the group is then searched for an element of full order
    count = 2 if p == 2 else (p - 1 if p % 4 == 1 else p + 1)
    pts = [(x, y) for x in range(p) for y in range(p) if (x * x + y * y - 1) % p == 0]
    assert len(pts) == count
    best = 0
    for (x, y) in pts:
        a, b, k = x, y, 1
        while (a, b) != (1, 0):
            a, b = (a * x - b * y) % p, (a * y + b * x) % p
            k += 1
        best = max(best, k)
    divisors = [d for d in range(1, count + 1) if count % d == 0]
    return {'kind': 'ffcircle', 'input': ['ffcircle', p], 'count': count, 'max_element_order': best, 'cyclic': best == count,
            'divisible_by_four': count % 4 == 0, 'orders_beyond_four': any(d not in (1, 2, 4) for d in divisors)}


def record(case):
    if case[0] == 'half':
        return record_half(case[1])
    if case[0] == 'census':
        return record_census(case[1])
    if case[0] == 'ffcircle':
        return record_ffcircle(case[1])
    return record_point(case[1], case[2])


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def wire_lines(data):
    out = []
    for r in data['records']:
        i = r['input']
        if r['kind'] == 'census':
            out.append('\t'.join(['census', str(i[1]), str(r['points']), str(r['mu4_points']), str(r['other_points']),
                                  str(int(r['reaches_minus_one'])), str(int(r['other_points_have_nonintegral_2x']))]))
        elif r['kind'] == 'ffcircle':
            out.append('\t'.join(['ffcircle', str(i[1]), str(r['count']), str(r['max_element_order']), str(int(r['cyclic'])),
                                  str(int(r['divisible_by_four'])), str(int(r['orders_beyond_four']))]))
        elif r['kind'] == 'half':
            out.append('\t'.join(['half', str(i[1]), r['x'], r['y_squared'], ','.join(r['y_values']) or '-',
                                  ','.join(str(o) for o in r['orders']) or '-', r['status']]))
        else:
            out.append('\t'.join(['point', str(i[1]), str(i[2]), r['x'], r['y'], str(int(r['twice_x_integral'])), str(r['prime']),
                                  ','.join(str(v) for v in r['valuations']) or '-', str(r['order']), str(int(r['mu4']))]))
    return out


def public_tsv(cases=CASES):
    return ''.join('point\t%d\t%d\n' % (c[1], c[2]) if c[0] == 'point' else '%s\t%d\n' % (c[0], c[1]) for c in cases)
