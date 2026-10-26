"""Exact finite l1 and import-boundary computations on declared small carriers."""
from fractions import Fraction as Q
import re
from itertools import permutations, product


def _exact(value):
    if type(value) not in (int, Q, str):
        raise TypeError('exact integer, Fraction or rational text required')
    if type(value) is str and (len(value) > 1024 or re.fullmatch(r'[+-]?[0-9]+(?:/[0-9]+)?', value) is None):
        raise ValueError('bounded integer or numerator/denominator text required')
    if type(value) is int and value.bit_length() > 1024:
        raise ValueError('integer exceeds 1024-bit limit')
    q=Q(value)
    if max(q.numerator.bit_length(),q.denominator.bit_length()) > 1024:
        raise ValueError('rational exceeds 1024-bit limit')
    return q


def _chain(x):
    a, b, c, e = x
    d = [b - a, c - b, a - c]
    return [e, 0, -e, *d, sum(d) + e * d[2], int(e == 0)]


def _kkt_valid(weights, capacities, divergence, cost, dual):
    return (
        all(a > 0 for a in weights)
        and all(a >= 0 for a in capacities)
        and not any(divergence)
        and cost == dual
    )


def _kkt(x):
    v, w, h, z = [x[i:i + 3] for i in (0, 3, 6, 9)]
    d = [h[1] - h[0], h[2] - h[1], h[0] - h[2]]
    r = [a - b for a, b in zip(v, d)]
    divergence = [z[2] - z[0], z[0] - z[1], z[1] - z[2]]
    cost = sum(a * abs(b) for a, b in zip(w, r))
    dual = sum(a * b for a, b in zip(z, v))
    slack = [a * abs(b) - c * b for a, b, c in zip(w, r, z)]
    capacities = [a - abs(b) for a, b in zip(w, z)]
    valid = _kkt_valid(w, capacities, divergence, cost, dual)
    return [
        *r, *divergence, *capacities, *slack,
        cost, dual, cost - dual, int(valid),
    ]


def _weighted_pair(x):
    a, b, p, q = x
    norm = p * abs(a) + q * abs(b)
    swapped = p * abs(b) + q * abs(a)
    if min(p, q) < 0:
        raise ValueError('Nonnegative supplied weights required')
    return a, b, p, q, norm, swapped


def _edge(x):
    a, b, p, q, norm, swapped = _weighted_pair(x)
    return [
        p * abs(a), q * abs(b), norm, swapped, swapped - norm,
        abs(a) + abs(b), max(abs(a), abs(b)),
        abs(a) + abs(b) - max(abs(a), abs(b)),
    ]


def _gauge(x):
    a, b, p, q, _, _ = _weighted_pair(x)
    out = []
    for swap, s, t in product((0, 1), (-1, 1), (-1, 1)):
        u, v = (b, a) if swap else (a, b)
        out.append(p * abs(s * u) + q * abs(t * v))
    out.extend([a * a + b * b, b * b + a * a, 3 * p + 4 * q,
                5 * p, 3 * p + 4 * q - 5 * p])
    return out


def _observer(x):
    a, b, p, q, norm, swapped = _weighted_pair(x)
    return [
        norm, p * abs(a) + q * abs(b),
        abs(a) + abs(b) - max(abs(a), abs(b)),
        (2 * a) ** 2 + (2 * b) ** 2 - 2 * (a * a + b * b),
        swapped - norm, p * 0 + q * abs(b),
        p * abs(a) + 0 * abs(b),
    ]


def _weighted_quotient(x, window):
    a, b, c, p, q, t, g0, g1, g2 = x[:9]
    weights = [p, q, t]
    if min(weights) <= 0:
        raise ValueError('Strictly positive weights required')
    if window and x[9] != 0:
        return [0]
    total = sum([a, b, c])
    k = weights.index(min(weights))
    r = [total if i == k else Q(0) for i in range(3)]
    h = [Q(0), a - r[0], a + b - r[0] - r[1]]
    shift = [a + g1 - g0, b + g2 - g1, c + g0 - g2]
    cost = sum(w * abs(z) for w, z in zip(weights, r))
    out = [1, k, *r, *h, cost, *shift, min(weights) * abs(sum(shift))]
    if window:
        out.extend([abs(sum(r)), int(cost != 0),
                    abs(sum(r)) / cost if cost else 0])
    return out


def _quotient(x):
    return _weighted_quotient(x, False)


def _window(x):
    return _weighted_quotient(x, True)


def _replica(x):
    a, b, n = x
    if n.denominator != 1 or not 0 <= n <= 8:
        raise ValueError('Replica bound')
    copies = [z for _ in range(int(n)) for z in (a, b)]
    return [
        sum(abs(z) for z in copies), sum(z * z for z in copies),
        n * (abs(a) + abs(b)), n * (a * a + b * b),
        (n * a) ** 2 + (n * b) ** 2, n * n * (a * a + b * b),
    ]


def _mass(x):
    if min(x) < 0:
        return [-1]
    mass = sum(x)
    if not mass:
        return [0]
    return [
        1, mass, *(v / mass for v in x), sum(x[:2]) / mass,
        sum(x[2:]) / mass, sum(v / mass for v in x),
    ]


def _circle(x):
    n = int(x[0])
    if x[0] != n or n not in (2, 3, 4):
        raise ValueError('circle order must be 2, 3 or 4')
    return [
        *(int((2 * k) % n == 0) for k in range(n)),
        *((i + j) % n for i in range(n) for j in range(n)),
        int(all((2 * k) % n == 0 for k in range(n))), 4, 0,
    ]


def _gauss(x):
    a, b = x
    norm = a * a + b * b
    if any(z.denominator != 1 for z in x):
        raise ValueError('Gaussian integers required')
    return [
        norm, int(norm == 1), int(norm != 0),
        a / norm if norm else 0, -b / norm if norm else 0,
        *(Q(k * k - 2) for k in range(-3, 4)),
    ]


def _complex(x):
    a, b, c, d = x
    norm = a * a + b * b
    other_norm = c * c + d * d
    u = a * c - b * d
    v = a * d + b * c
    return [
        norm, other_norm, u, v, u * u + v * v, norm * other_norm,
        int(norm != 0), a / norm if norm else 0,
        -b / norm if norm else 0,
    ]


def _gaussian_product(z, w):
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def _gaussian_matrix_product(a, b):
    return [
        tuple(sum(_gaussian_product(a[2 * i + k], b[2 * k + j])[p]
                  for k in range(2)) for p in range(2))
        for i in range(2) for j in range(2)
    ]


def _time(x):
    s = x[0]
    if s not in (-1, 1):
        raise ValueError('time sign must be -1 or 1')
    maps = list(product(range(2), repeat=2))
    squares = [f[f[i]] for f in maps for i in range(2)]
    out = [*squares, sum([f[f[0]], f[f[1]]] == [1, 0] for f in maps)]
    u = [(Q(1, 2), s / 2), (Q(1, 2), -s / 2),
         (Q(1, 2), -s / 2), (Q(1, 2), s / 2)]
    adjoint = [(u[2 * j + i][0], -u[2 * j + i][1])
               for i in range(2) for j in range(2)]
    matrices = u + _gaussian_matrix_product(u, u) + _gaussian_matrix_product(adjoint, u)
    out.extend(v for z in matrices for v in z)
    return out


def _hilbert(x):
    n = int(x[0])
    if x[0] != n or not 0 <= n <= 8:
        raise ValueError('Hilbert truncation must be an integer from 0 to 8')
    u = [Q(1, 2 ** k) for k in range(1, n + 1)]
    return [
        *u, sum(v * v for v in u), Q(1, 3 * 4 ** n),
        Q(1, 4 ** (n + 1)), Q(1, 3), int(Q(1, 3 * 4 ** n) > 0),
    ]


def _dilation(x):
    a, b, d = x
    if not (a + d == 1 and a >= 0 and d >= 0 and a * d >= b * b):
        raise ValueError('positive trace-one input required')
    permutations_found = [p for p in permutations(range(4))
                          if p[0] // 2 == 0 and p[2] // 2 == 0]
    out = [len(permutations_found)]
    for p in permutations_found:
        out.extend([*p, *(p.index(i) for i in range(4))])
    # Choi in (input,output) order for reset to |0><0|, partial trace over output.
    out.extend([*(int(i == j and i in (0, 2))
                  for i in range(4) for j in range(4)),
                1, 0, 0, 1, a + d, 0, 0, 0])
    return out


def _gleason(x):
    a, b = x
    u = (a + b) ** 2
    v = (a - b) ** 2
    z = a * a + b * b
    return [a * a, b * b, z, z, u, v, z, z, u + v, 2 * z,
            u * u + v * v, 2 * z * z, 8 * a * a * b * b]


def _tensor(x):
    a, b, c, d = x
    tensor = [a * c, a * d, b * c, b * d]
    rival = [a * (c + d), 0, b * (c + d), 0]
    return [
        *tensor, *rival, *(v - w for v, w in zip(tensor, rival)),
        (a * a + b * b) * (c * c + d * d), sum(v * v for v in tensor),
    ]


def _lift(x):
    a, b, c, d = x
    first_norm = a * a + b * b
    second_norm = c * c + d * d
    if not first_norm or not second_norm:
        return [0]
    rho = [a * a / first_norm, a * b / first_norm,
           a * b / first_norm, b * b / first_norm]
    sigma = [c * c / second_norm, c * d / second_norm,
             c * d / second_norm, d * d / second_norm]
    overlap = (a * c + b * d) ** 2 / (first_norm * second_norm)
    r = [a * abs(a), b * abs(b)]
    z = [c * abs(c), d * abs(d)]
    saturated = sum(u * v for u, v in zip(r, z)) == sum(abs(u) * abs(v) for u, v in zip(r, z))
    faithful = all(z[i] != 0 for i in range(2) if r[i] != 0)
    return [1, first_norm, second_norm, *rho, *sigma, overlap,
            1 - overlap, int(saturated), int(faithful), int(overlap > 0)]


def _average(x):
    a, b = x
    phases = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    values = [(a * u + b * v) ** 2 + (a * s + b * t) ** 2
              for u, s in phases for v, t in phases]
    correlated = [(a * u + b * u) ** 2 + (a * s + b * s) ** 2
                  for u, s in phases]
    return [*values, *correlated, sum(values) / 16, sum(correlated) / 4,
            a * a + b * b, 2 * a * b]


def _gram(x):
    a, b, c, d = x
    return [a * c + b * d, a * c + 2 * b * d, 2 * a * c + 3 * b * d,
            a * a + b * b, a * a + 2 * b * b, 2 * a * a + 3 * b * b,
            b * d, a * a + 2 * b * b - (a * a + b * b)]


_ARITIES = {
    'chain': 4, 'kkt': 12, 'edge': 4, 'gauge': 4, 'observer': 4,
    'quotient': 9, 'window': 10, 'replica': 3, 'circle': 1, 'gauss': 2,
    'complex': 4, 'time': 1, 'hilbert': 1, 'dilation': 3, 'gleason': 2,
    'tensor': 4, 'lift': 4, 'average': 2, 'gram': 4,
}

_OPERATIONS = {
    'chain': _chain, 'kkt': _kkt, 'edge': _edge, 'gauge': _gauge,
    'observer': _observer, 'quotient': _quotient, 'window': _window,
    'replica': _replica, 'mass': _mass, 'circle': _circle, 'gauss': _gauss,
    'complex': _complex, 'time': _time, 'hilbert': _hilbert,
    'dilation': _dilation, 'gleason': _gleason, 'tensor': _tensor,
    'lift': _lift, 'average': _average, 'gram': _gram,
}


def evaluate(kind, values):
    if type(values) not in (list, tuple) or len(values) > 64:
        raise ValueError('bounded sequence of exact values required')
    if kind == 'mass':
        if not values:
            raise ValueError('nonempty mass vector required')
    elif kind not in _ARITIES or len(values) != _ARITIES[kind]:
        raise ValueError('unknown operation or incorrect input arity')
    x = list(map(_exact, values))
    out = _OPERATIONS[kind](x)
    return [str(Q(v)) for v in out]


def certify(kind, cases):
    return {'records': [{'input': v, 'output': evaluate(kind, v)} for v in cases]}
