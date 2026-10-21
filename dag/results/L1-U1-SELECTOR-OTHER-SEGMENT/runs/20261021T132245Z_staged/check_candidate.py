"""Independent checker for L1-U1-SELECTOR-OTHER-SEGMENT (rational unit-circle torsion).

Recomputes every record without importing the producer and without the three-term recurrence used by it:
a rational circle point is written as a Gaussian integer A = a + b i over a common denominator d (z = A/d,
a^2 + b^2 = d^2, found from the reduced numerators and denominators of x and y), and z^k = A^k / d^k is computed
with exact integer Gaussian multiplication. Orders are read off `A^n == d^n`; p-adic valuations of 2 Re z^k are
v_p(2 Re A^k) - k v_p(d). For the half-integer list a rational y with y^2 = P/Q is decided by the integer square
test on P*Q (the producer tests numerator and denominator separately). The theorem-level prediction (valuation -k v_p(den 2x) when den 2x > 1, so no torsion) is checked
on every point record, not assumed. AuthorityEffect: None.
"""
import sys
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'dag/pfp/prepare_stage.py').is_file())
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'L1-U1-SELECTOR-OTHER-SEGMENT'
KEYS = {'half': {'kind', 'input', 'x', 'y_squared', 'y_values', 'orders', 'status'},
        'point': {'kind', 'input', 'x', 'y', 'twice_x_integral', 'prime', 'valuations', 'order', 'mu4'},
        'census': {'kind', 'input', 'points', 'mu4_points', 'other_points', 'reaches_minus_one', 'other_points_have_nonintegral_2x'},
        'ffcircle': {'kind', 'input', 'count', 'max_element_order', 'cyclic', 'divisible_by_four', 'orders_beyond_four'}}
BOUND = 12
POWERS = 6


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def gmul(u, v):
    return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def gaussian_powers(x, y, upto):
    """z = x + iy on the circle as A/d with Gaussian integer A; returns (d, [A^0 .. A^upto])."""
    d = x.denominator * y.denominator // gcd(x.denominator, y.denominator)
    A = (int(x * d), int(y * d))
    require(A[0] ** 2 + A[1] ** 2 == d * d, 'G3_WITNESS:not_on_circle')
    pw = [(1, 0)]
    for _ in range(upto):
        pw.append(gmul(pw[-1], A))
    return d, pw


def order_of(x, y):
    d, pw = gaussian_powers(x, y, BOUND)
    for n in range(1, BOUND + 1):
        if pw[n] == (d ** n, 0):
            return n
    return 0


def vp_int(n, p):
    require(n != 0, 'G3_WITNESS:valuation_of_zero')
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count


def prime_factors_sorted(n):
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def expected_half(k):
    require(is_int(k) and -2 <= k <= 2, 'G1_SCHEMA:half_input')
    x = F(k, 2)
    y2 = 1 - x * x
    # P/Q (lowest terms) is a rational square iff the integer P*Q is a perfect square; then sqrt = isqrt(P*Q)/Q
    pq = y2.numerator * y2.denominator
    root = isqrt(pq)
    ys = sorted({F(root, y2.denominator), F(-root, y2.denominator)}) if root * root == pq else []
    want = {'x': str(x), 'y_squared': str(y2), 'y_values': [str(v) for v in ys], 'orders': [order_of(x, v) for v in ys],
            'status': 'unit_points' if ys else 'refused_irrational_y'}
    if y2 == F(3, 4):
        require(not ys, 'G3_WITNESS:three_quarters_is_not_a_square')
    require(all(v * v == y2 for v in ys), 'G3_WITNESS:root_is_not_a_root')
    return want


def expected_point(m, n):
    require(is_int(m) and is_int(n) and (m, n) != (0, 0) and abs(m) <= 50 and abs(n) <= 50, 'G1_SCHEMA:point_input')
    c = n * n + m * m
    x, y = F(n * n - m * m, c), F(2 * m * n, c)
    d, pw = gaussian_powers(x, y, BOUND)
    twice = 2 * x
    integral = twice.denominator == 1
    primes = prime_factors_sorted(twice.denominator)
    p = 0 if integral else primes[0]
    order = order_of(x, y)
    vals = []
    if not integral:
        for k in range(1, POWERS + 1):
            vals.append(vp_int(2 * pw[k][0], p) - k * vp_int(d, p))
        # theorem-level prediction: v_p(2 Re z^k) = -k v_p(den 2x) and z has infinite order
        dv = vp_int(twice.denominator, p)
        require(vals == [-k * dv for k in range(1, POWERS + 1)], 'G3_WITNESS:valuation_law')
        require(order == 0, 'G3_WITNESS:torsion_point_with_nonintegral_2x')
    else:
        require(order in (1, 2, 4), 'G3_WITNESS:integral_2x_point_must_be_in_mu4')
    return {'x': str(x), 'y': str(y), 'twice_x_integral': integral, 'prime': p, 'valuations': vals, 'order': order,
            'mu4': order in (1, 2, 4)}


def expected_census(bound):
    require(is_int(bound) and 1 <= bound <= 12, 'G1_SCHEMA:census_input')
    pts = set()
    for m in range(-bound, bound + 1):
        for n in range(-bound, bound + 1):
            if (m, n) == (0, 0):
                continue
            c = n * n + m * m
            pts.add((F(n * n - m * m, c), F(2 * m * n, c)))
    mu4 = [q for q in pts if q in {(F(1), F(0)), (F(-1), F(0)), (F(0), F(1)), (F(0), F(-1))}]
    other = [q for q in pts if q not in mu4]
    # theorem-level: the points outside mu_4 have no power equal to 1 within the bound and 2x not an integer
    require(all(order_of(x, y) == 0 and (2 * x).denominator != 1 for x, y in other), 'G3_WITNESS:non_mu4_point_with_finite_order_or_integral_2x')
    require(all(order_of(x, y) in (1, 2, 4) for x, y in mu4), 'G3_WITNESS:mu4_orders')
    return {'points': len(pts), 'mu4_points': len(mu4), 'other_points': len(other), 'reaches_minus_one': (F(-1), F(0)) in pts,
            'other_points_have_nonintegral_2x': all((2 * x).denominator != 1 for x, _ in other)}


def expected_ffcircle(p):
    require(is_int(p) and 2 <= p <= 100 and all(p % d for d in range(2, p)), 'G1_SCHEMA:ffcircle_input')
    pts = [(x, y) for x in range(p) for y in range(p) if (x * x + y * y) % p == 1 % p]
    orders = []
    for (x, y) in pts:
        a, b, k = x, y, 1
        while (a, b) != (1 % p, 0):
            a, b = (a * x - b * y) % p, (a * y + b * x) % p
            k += 1
        orders.append(k)
    best = max(orders)
    count = len(pts)
    # a cyclic group of order count has an element of each divisor order
    require(all(any(o == d for o in orders) for d in range(1, count + 1) if count % d == 0), 'G3_WITNESS:circle_group_is_not_cyclic')
    require(all(count % o == 0 for o in orders), 'G3_WITNESS:lagrange')
    return {'count': count, 'max_element_order': best, 'cyclic': best == count, 'divisible_by_four': count % 4 == 0,
            'orders_beyond_four': any(count % d == 0 and d not in (1, 2, 4) for d in range(1, count + 1))}


_CACHE = {}


def expected(inp):
    key = repr(inp)
    if key not in _CACHE:
        require(type(inp) is list and inp, 'G1_SCHEMA:input')
        if inp[0] == 'half':
            require(len(inp) == 2, 'G1_SCHEMA:half_input')
            _CACHE[key] = expected_half(inp[1])
        elif inp[0] == 'census':
            require(len(inp) == 2, 'G1_SCHEMA:census_input')
            _CACHE[key] = expected_census(inp[1])
        elif inp[0] == 'ffcircle':
            require(len(inp) == 2, 'G1_SCHEMA:ffcircle_input')
            _CACHE[key] = expected_ffcircle(inp[1])
        elif inp[0] == 'point':
            require(len(inp) == 3, 'G1_SCHEMA:point_input')
            _CACHE[key] = expected_point(inp[1], inp[2])
        else:
            raise ValueError('G1_SCHEMA:unknown_kind')
    return _CACHE[key]


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        records = data['records']
        require(len(records) == len(public['cases']), 'G2_COVERAGE:record_count')
        seen = []
        for r in records:
            require(type(r) is dict and r.get('kind') in KEYS and set(r) == KEYS[r['kind']], 'G1_SCHEMA:record_keys')
            require(type(r['input']) is list and r['input'][:1] == [r['kind']], 'G1_SCHEMA:input')
            seen.append(repr(r['input']))
            want = expected(r['input'])
            for k, v in want.items():
                require(r[k] == v and type(r[k]) is type(v), 'G3_WITNESS:' + r['kind'] + '_' + k)
                if type(v) is list:
                    require(all(type(a) is type(b) for a, b in zip(r[k], v)), 'G3_WITNESS:type_' + k)
        require(sorted(seen) == sorted(repr(c) for c in public['cases']), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
