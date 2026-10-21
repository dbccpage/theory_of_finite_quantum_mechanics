"""Independent checker for L1-WDP-REALIFICATION-J.

Recomputes every record without importing the producer. R(A) is built by the Kronecker form I2 (x) P + [[0,-1],[1,0]] (x) Q
(the producer places the four blocks explicitly), J_m = [[0,-1],[1,0]] (x) I_m, the real product R(A)R(B) is taken
FIRST and compared with R of the complex product, membership in the image is decided by `R(candidate from the top
blocks) == M` independently of the commutation test and the two must agree (Theorem 2 on the instance), and the
square-root-of-minus-one census is a brute-force scan of all integer 2x2 matrices in the box. AuthorityEffect: None.
"""
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'dag/pfp/prepare_stage.py').is_file())
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'L1-WDP-REALIFICATION-J'
KEYS = {
    'psd': {'kind', 'input', 'hermitian', 'complex_psd', 'real_psd', 'agree'},
    'prod': {'kind', 'input', 'RAB', 'RAstar', 'RA_interleaved', 'interleaved_commutes_block_J', 'mult_ok', 'intertwine_ok', 'imul_ok', 'star_ok', 'roundtrip_ok', 'hermitian', 'symmetric_RA',
             'trace_real', 'trace_complex', 'trace_identity', 'trace_twice_complex'},
    'img': {'kind', 'input', 'status', 'commutes', 'anticommutes', 'symmetric', 'hermitian', 'recovered'},
    'jstruct': {'kind', 'input', 'sq_neg_id', 'pm_J', 'commutes_J'},
    'jcensus': {'kind', 'input', 'total', 'commuting_J', 'pm_J'}}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def canon(s):
    """A canonical rational string: str(Fraction(s)) == s."""
    require(type(s) is str, 'G1_SCHEMA:rational_string')
    try:
        f = F(s)
    except (ValueError, ZeroDivisionError):
        raise ValueError('G1_SCHEMA:rational')
    require(str(f) == s, 'G1_SCHEMA:canonical_rational')
    return f


def gaussian(tok):
    require(type(tok) is str and tok.count(':') == 1, 'G1_SCHEMA:gaussian_token')
    a, b = tok.split(':')
    return canon(a), canon(b)


def zeros(r, c):
    return [[F(0)] * c for _ in range(r)]


def matmul(X, Y):
    return [[sum((X[i][t] * Y[t][j] for t in range(len(Y))), F(0)) for j in range(len(Y[0]))] for i in range(len(X))]


def kron(X, Y):
    return [[X[i][j] * Y[k][l] for j in range(len(X[0])) for l in range(len(Y[0]))] for i in range(len(X)) for k in range(len(Y))]


def ident(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def addm(X, Y):
    return [[x + y for x, y in zip(a, b)] for a, b in zip(X, Y)]


J1 = [[F(0), F(-1)], [F(1), F(0)]]
I2 = ident(2)


def real_of(P, Q):
    """R = I2 (x) P + J1 (x) Q for real P, Q (equals [[P,-Q],[Q,P]])."""
    return addm(kron(I2, P), kron(J1, Q))


def parts(A):
    return [[z[0] for z in row] for row in A], [[z[1] for z in row] for row in A]


def gmatrix(tokens, rows, cols):
    require(type(tokens) is list and len(tokens) == rows * cols, 'G1_SCHEMA:matrix_size')
    vals = [gaussian(t) for t in tokens]
    return [vals[i * cols:(i + 1) * cols] for i in range(rows)]


def Jbig(m):
    return kron(J1, ident(m))


def tr(X):
    return sum((X[i][i] for i in range(len(X))), F(0))


def flat(X):
    return [str(x) for row in X for x in row]


def bit(b):
    return '1' if b else '0'


def expected_prod(m, n, k, atok, btok):
    A, B = gmatrix(atok, m, n), gmatrix(btok, n, k)
    P, Q = parts(A)
    S, T = parts(B)
    RA, RB = real_of(P, Q), real_of(S, T)
    real_product = matmul(RA, RB)
    # complex product from real and imaginary parts
    PS, QT, PT, QS = matmul(P, S), matmul(Q, T), matmul(P, T), matmul(Q, S)
    RAB_complex = real_of([[a - b for a, b in zip(r1, r2)] for r1, r2 in zip(PS, QT)], addm(PT, QS))
    Ji = real_of([[-q for q in row] for row in Q], P)  # R(iA): i(P+iQ) = -Q + iP
    ras = addm(kron(P, I2), kron(Q, J1))  # interleaved order (re_1, im_1, re_2, ...): P (x) I2 + Q (x) J1
    Pt, Qt = [list(r) for r in zip(*P)], [list(r) for r in zip(*Q)]
    want = {'RAB': flat(real_product), 'RAstar': flat(real_of(Pt, [[-x for x in row] for row in Qt])), 'RA_interleaved': flat(ras),
            'interleaved_commutes_block_J': matmul(Jbig(m), ras) == matmul(ras, Jbig(n)), 'mult_ok': real_product == RAB_complex,
            'intertwine_ok': matmul(Jbig(m), RA) == matmul(RA, Jbig(n)), 'imul_ok': Ji == matmul(Jbig(m), RA),
            'star_ok': real_of(list(map(list, zip(*P))), [[-x for x in row] for row in zip(*Q)]) == list(map(list, zip(*RA))),
            'roundtrip_ok': [row[:n] for row in RA[:m]] == P and [row[:n] for row in RA[m:]] == Q}
    if m == n:
        herm = [list(r) for r in zip(*P)] == P and [list(r) for r in zip(*Q)] == [[-x for x in row] for row in Q]
        trr, trp, trq = tr(RA), tr(P), tr(Q)
        want.update({'hermitian': bit(herm), 'symmetric_RA': bit([list(r) for r in zip(*RA)] == RA), 'trace_real': str(trr),
                     'trace_complex': '%s:%s' % (trp, trq), 'trace_identity': bit(trr == 2 * trp), 'trace_twice_complex': bit(trr == 2 * trp and trq == 0)})
        require(herm == ([list(r) for r in zip(*RA)] == RA), 'G3_WITNESS:hermitian_iff_symmetric')
    else:
        want.update({'hermitian': '-', 'symmetric_RA': '-', 'trace_real': '-', 'trace_complex': '-', 'trace_identity': '-', 'trace_twice_complex': '-'})
    # theorem-level facts on the instance
    for key in ('mult_ok', 'intertwine_ok', 'imul_ok', 'star_ok', 'roundtrip_ok'):
        require(want[key] is True, 'G3_WITNESS:theorem_1_fails_' + key)
    if m == n:
        require(want['trace_identity'] == '1', 'G3_WITNESS:trace_identity')
    return want


def expected_img(rows, cols, toks):
    require(is_int(rows) and is_int(cols) and rows >= 1 and cols >= 1 and type(toks) is list and len(toks) == rows * cols, 'G1_SCHEMA:img_shape')
    vals = [canon(t) for t in toks]
    M = [vals[i * cols:(i + 1) * cols] for i in range(rows)]
    if rows % 2 or cols % 2:
        return {'status': 'odd_dim', 'commutes': '-', 'anticommutes': '-', 'symmetric': '-', 'hermitian': '-', 'recovered': []}
    m, n = rows // 2, cols // 2
    commutes = matmul(Jbig(m), M) == matmul(M, Jbig(n))
    anti = matmul(Jbig(m), M) == [[-x for x in r] for r in matmul(M, Jbig(n))]
    # image membership decided by the blocks, independently of the commutation test
    U = [row[:n] for row in M[:m]]
    V = [row[n:] for row in M[:m]]
    cand_P, cand_Q = U, [[-x for x in row] for row in V]
    in_image = real_of(cand_P, cand_Q) == M
    require(in_image == commutes, 'G3_WITNESS:theorem_2_image_iff_commutes')
    want = {'status': 'ok' if commutes else 'noncommuting', 'commutes': bit(commutes), 'anticommutes': bit(anti),
            'symmetric': bit([list(r) for r in zip(*M)] == M) if rows == cols else '-', 'hermitian': '-', 'recovered': []}
    if commutes:
        want['recovered'] = ['%s:%s' % (cand_P[i][j], cand_Q[i][j]) for i in range(m) for j in range(n)]
        if m == n:
            herm = [list(r) for r in zip(*cand_P)] == cand_P and [list(r) for r in zip(*cand_Q)] == [[-x for x in row] for row in cand_Q]
            want['hermitian'] = bit(herm)
    return want


def cmul_(u, v):
    return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def hermitian_psd(A):
    """Positive semidefiniteness of a Hermitian matrix of (re, im) Fractions by symmetric elimination (LDL*), exact."""
    A = [list(row) for row in A]
    n = len(A)
    for k in range(n):
        pivot = A[k][k][0]
        if pivot < 0:
            return False
        if pivot == 0:
            if any(A[k][j] != (F(0), F(0)) for j in range(k, n)):
                return False
            continue
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = cmul_(A[i][k], A[k][j])
                A[i][j] = (A[i][j][0] - num[0] / pivot, A[i][j][1] - num[1] / pivot)
    return True


def expected_psd(n, atok):
    require(is_int(n) and 1 <= n <= 4, 'G1_SCHEMA:psd_size')
    A = gmatrix(atok, n, n)
    herm = all(A[i][j] == (A[j][i][0], -A[j][i][1]) for i in range(n) for j in range(n))
    if not herm:
        return {'hermitian': '0', 'complex_psd': '-', 'real_psd': '-', 'agree': '-'}
    P, Q = parts(A)
    R = real_of(P, Q)
    cp = hermitian_psd(A)
    rp = hermitian_psd([[(x, F(0)) for x in row] for row in R])
    require(all(R[i][j] == R[j][i] for i in range(2 * n) for j in range(2 * n)), 'G3_WITNESS:R_of_hermitian_is_symmetric')
    require(cp == rp, 'G3_WITNESS:positivity_not_preserved_and_reflected_on_instance')
    return {'hermitian': '1', 'complex_psd': bit(cp), 'real_psd': bit(rp), 'agree': '1'}


def expected_jstruct(a, b, c, d):
    X = [[F(a), F(b)], [F(c), F(d)]]
    Jm = [[F(0), F(-1)], [F(1), F(0)]]
    return {'sq_neg_id': matmul(X, X) == [[F(-1), F(0)], [F(0), F(-1)]],
            'pm_J': X == Jm or X == [[-x for x in r] for r in Jm], 'commutes_J': matmul(X, Jm) == matmul(Jm, X)}


def mul2i(X, Y):
    return (X[0] * Y[0] + X[1] * Y[2], X[0] * Y[1] + X[1] * Y[3], X[2] * Y[0] + X[3] * Y[2], X[2] * Y[1] + X[3] * Y[3])


def expected_jcensus(B):
    total = commuting = pm = 0
    Jm = (0, -1, 1, 0)
    for X in product(range(-B, B + 1), repeat=4):
        if mul2i(X, X) == (-1, 0, 0, -1):
            total += 1
            commuting += mul2i(X, Jm) == mul2i(Jm, X)
            pm += X == Jm or X == (0, 1, -1, 0)
    require(commuting == pm, 'G3_WITNESS:only_pm_J_commutes_with_J')
    return {'total': total, 'commuting_J': commuting, 'pm_J': pm}


_CACHE = {}


def expected(inp):
    key = repr(inp)
    if key not in _CACHE:
        kind = inp[0]
        if kind == 'prod':
            require(len(inp) == 6 and all(is_int(x) and x >= 1 for x in inp[1:4]) and type(inp[4]) is list and type(inp[5]) is list, 'G1_SCHEMA:prod_input')
            _CACHE[key] = expected_prod(*inp[1:])
        elif kind == 'img':
            require(len(inp) == 4, 'G1_SCHEMA:img_input')
            _CACHE[key] = expected_img(*inp[1:])
        elif kind == 'psd':
            require(len(inp) == 3 and type(inp[2]) is list, 'G1_SCHEMA:psd_input')
            _CACHE[key] = expected_psd(inp[1], inp[2])
        elif kind == 'jstruct':
            require(len(inp) == 5 and all(is_int(x) for x in inp[1:]), 'G1_SCHEMA:jstruct_input')
            _CACHE[key] = expected_jstruct(*inp[1:])
        elif kind == 'jcensus':
            require(len(inp) == 2 and is_int(inp[1]) and 0 <= inp[1] <= 12, 'G1_SCHEMA:jcensus_input')
            _CACHE[key] = expected_jcensus(inp[1])
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
            require(set(r) == {'kind', 'input'} | set(want), 'G1_SCHEMA:unexpected_fields')
        require(sorted(seen) == sorted(repr(c) for c in public['cases']), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ValueError) as error:
        if isinstance(error, ValueError):
            raise
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
