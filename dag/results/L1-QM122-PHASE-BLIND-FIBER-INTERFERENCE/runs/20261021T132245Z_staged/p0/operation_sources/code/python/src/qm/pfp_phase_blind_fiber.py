"""Phase fibers over Gaussian integers and the unnormalized two-sector Hadamard readout.

Producer for PFP batch 01, node L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE. Exact integers only.
Scope: sector amplitudes in Z[i], the phase-blind weight |z|^2 and the readout (|a+b|^2, |a-b|^2).
Not a statement about complex Hilbert space, normalized or projective states, or physics.
AuthorityEffect: None.
"""
from math import isqrt

CASES = [(1, 1), (1, 2), (2, 5), (5, 5), (25, 1), (3, 3), (0, 5), (5, 0), (0, 0), (4, 9)]


def fiber(weight):
    """All Gaussian integers (x, y) with x^2 + y^2 == weight, found by solving for y at each x."""
    found = []
    r = isqrt(weight)
    for x in range(-r, r + 1):
        rest = weight - x * x
        y = isqrt(rest)
        if y * y == rest:
            found.append((x, y))
            if y:
                found.append((x, -y))
    return sorted(found)


def gadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gsub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def weight(z):
    return z[0] * z[0] + z[1] * z[1]


def readout(a, b):
    """Unnormalized Hadamard mixing: (|a+b|^2, |a-b|^2)."""
    return (weight(gadd(a, b)), weight(gsub(a, b)))


def record(w0, w1):
    f0, f1 = fiber(w0), fiber(w1)
    outs = sorted({readout(a, b) for a in f0 for b in f1})
    total = 2 * (w0 + w1)
    return {
        'input': [w0, w1],
        'fiber_sizes': [len(f0), len(f1)],
        'realizable': bool(f0) and bool(f1),
        'readouts': [list(o) for o in outs],
        'distinct_readouts': len(outs),
        'total_doubled': all(o[0] + o[1] == total for o in outs),
        'descends': len(outs) <= 1,
    }


def certificate(cases=CASES):
    return {'records': [record(w0, w1) for w0, w1 in cases]}


def wire_lines(data):
    out = []
    for r in data['records']:
        reads = ';'.join('%d:%d' % tuple(o) for o in r['readouts']) or '-'
        out.append('\t'.join(['fiber', str(r['input'][0]), str(r['input'][1]), str(r['fiber_sizes'][0]), str(r['fiber_sizes'][1]),
                              str(int(r['realizable'])), str(r['distinct_readouts']), str(int(r['total_doubled'])),
                              str(int(r['descends'])), reads]))
    return out


def public_tsv(cases=CASES):
    return ''.join('fiber\t%d\t%d\n' % c for c in cases)
