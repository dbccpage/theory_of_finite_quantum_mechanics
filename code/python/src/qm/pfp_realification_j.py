"""Realification R(A) = [[P, -Q], [Q, P]] of exact Gaussian-rational matrices and the declared complex structure J.

Producer for PFP batch 01, node L1-WDP-REALIFICATION-J. Fractions only. Five record kinds:
  prod     (also R(A*) and the INTERLEAVED coordinate ordering (re_1, im_1, re_2, ...), which is a different J)  R(AB) for composable Gaussian-rational A (m x n), B (n x k) and the checked identities
           R(A)R(B) = R(AB), J_m R(A) = R(A) J_n, R(iA) = J_m R(A), R(A*) = R(A)^T, recovery of A from R(A),
           Hermitian <-> symmetric, and (square case) Tr R(A) = 2 Re Tr A, which is NOT 2 Tr A when Im Tr A != 0;
  img      a real 2m x 2n matrix M: is J_m M = M J_n (then M = R(A) for the A read from the blocks) or not;
  psd      a Hermitian A (n x n): is A positive semidefinite, is the real symmetric R(A) positive semidefinite (instances of
           preservation and reflection of positivity, NOT a theorem; PSD decided by all principal minors >= 0);
  jstruct  an integer 2 x 2 matrix X: X^2 = -I, X = +-J, X commutes with J (J is declared, not selected);
  jcensus  the number of integer 2 x 2 square roots of -I with entries in [-B, B], and how many commute with J.
Not a statement about states R(rho)/2, positivity, instruments, or any selection of J. AuthorityEffect: None.
"""
from fractions import Fraction as F

CASES = [
    ['prod', 1, 1, 1, ['1:1'], ['2:-3']],
    ['prod', 2, 2, 2, ['1:1', '2:0', '0:-1', '3:0'], ['0:0', '1:-1', '1:0', '0:1']],
    ['prod', 3, 3, 3, ['1/2:1/3', '0:1', '2:0', '1:-1', '1/4:0', '0:-2', '3:1', '0:0', '-1:1/2'],
     ['1:0', '0:1', '1:1', '0:-1', '2:0', '1/3:0', '0:0', '1:-2', '5:0']],
    ['prod', 2, 3, 1, ['1:2', '0:1', '3:-1', '-1:0', '2:2', '0:0'], ['1:0', '0:1', '2:-1']],
    ['prod', 3, 2, 2, ['1:0', '0:1', '2:1', '1:-1', '0:0', '3:0'], ['0:1', '1:0', '-1:1', '2:0']],
    ['prod', 2, 2, 2, ['2:0', '1:-1', '1:1', '3:0'], ['1:0', '0:0', '0:0', '1:0']],
    ['prod', 2, 2, 2, ['0:0', '0:0', '0:0', '0:0'], ['1:2', '3:4', '5:6', '7:8']],
    ['prod', 3, 3, 3, ['1:0', '0:0', '0:0', '0:0', '1:0', '0:0', '0:0', '0:0', '1:0'],
     ['1:1', '2:0', '0:3', '0:0', '1:-1', '4:0', '1/2:0', '0:1', '2:2']],
    ['prod', 2, 2, 2, ['0:1', '0:0', '0:0', '0:1'], ['1:2', '3:0', '0:-1', '1:1']],
    ['img', 4, 4, ['1', '3', '-2', '0', '0', '0', '0', '1', '2', '0', '1', '3', '0', '-1', '0', '0']],
    ['img', 4, 4, ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']],
    ['img', 4, 4, ['-1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1']],
    ['img', 4, 4, ['1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '-1', '0', '0', '0', '0', '-1']],
    ['img', 3, 3, ['1', '0', '0', '0', '1', '0', '0', '0', '1']],
    ['img', 2, 2, ['2', '-3', '3', '2']],
    ['img', 2, 2, ['2', '3', '-3', '2']],
    ['img', 2, 4, ['1', '3', '-2', '1', '2', '-1', '1', '3']],
    ['img', 2, 4, ['1', '0', '0', '0', '0', '1', '0', '0']],
    ['img', 4, 4, ['2', '1', '0', '1', '1', '3', '-1', '0', '0', '-1', '2', '1', '1', '0', '1', '3']],
    ['img', 2, 2, ['1', '0', '0', '-1']],
    ['img', 4, 4, ['1', '0', '0', '0', '0', '2', '0', '0', '0', '0', '3', '0', '0', '0', '0', '4']],
    ['img', 4, 4, ['1/2', '0', '0', '0', '0', '1/2', '0', '0', '0', '0', '1/2', '0', '0', '0', '0', '1/2']],
    ['psd', 2, ['2:0', '1:-1', '1:1', '1:0']],
    ['psd', 2, ['1:0', '2:0', '2:0', '1:0']],
    ['psd', 2, ['2:0', '1:-1', '1:1', '3:0']],
    ['psd', 2, ['1:0', '0:1', '0:1', '1:0']],
    ['psd', 3, ['2:0', '0:1', '0:0', '0:-1', '2:0', '1:0', '0:0', '1:0', '1:0']],
    ['psd', 3, ['1:0', '0:-1', '1:0', '0:1', '1:0', '0:1', '1:0', '0:-1', '1:0']],
    ['psd', 1, ['-1:0']],
    ['psd', 2, ['1:0', '0:0', '0:0', '0:0']],
    ['psd', 2, ['0:0', '1:0', '1:0', '0:0']],
    ['jstruct', 0, -1, 1, 0],
    ['jstruct', 0, 1, -1, 0],
    ['jstruct', 1, -1, 2, -1],
    ['jstruct', 2, -5, 1, -2],
    ['jstruct', 1, 0, 0, -1],
    ['jstruct', 0, 1, 1, 0],
    ['jstruct', 1, 1, 1, 1],
    ['jstruct', 0, 0, 0, 0],
    ['jcensus', 1],
    ['jcensus', 2],
    ['jcensus', 3],
    ['jcensus', 5],
    ['jcensus', 7],
]


def fq(x):
    return str(F(x))


def gtok(z):
    return '%s:%s' % (fq(z[0]), fq(z[1]))


def gparse(tokens, rows, cols):
    vals = []
    for t in tokens:
        a, b = t.split(':')
        vals.append((F(a), F(b)))
    return [vals[i * cols:(i + 1) * cols] for i in range(rows)]


def cmatmul(A, B):
    m, n, k = len(A), len(B), len(B[0])
    out = [[(F(0), F(0)) for _ in range(k)] for _ in range(m)]
    for i in range(m):
        for j in range(k):
            re = sum(A[i][t][0] * B[t][j][0] - A[i][t][1] * B[t][j][1] for t in range(n))
            im = sum(A[i][t][0] * B[t][j][1] + A[i][t][1] * B[t][j][0] for t in range(n))
            out[i][j] = (re, im)
    return out


def realify(A):
    m, n = len(A), len(A[0])
    R = [[F(0)] * (2 * n) for _ in range(2 * m)]
    for i in range(m):
        for j in range(n):
            P, Q = A[i][j]
            R[i][j] = P
            R[i][n + j] = -Q
            R[m + i][j] = Q
            R[m + i][n + j] = P
    return R


def rmatmul(X, Y):
    return [[sum(X[i][t] * Y[t][j] for t in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]


def transpose(X):
    return [list(r) for r in zip(*X)]


def jmat(m):
    J = [[F(0)] * (2 * m) for _ in range(2 * m)]
    for i in range(m):
        J[i][m + i] = F(-1)
        J[m + i][i] = F(1)
    return J


def star(A):
    return [[(A[i][j][0], -A[i][j][1]) for i in range(len(A))] for j in range(len(A[0]))]


def imul(A):
    return [[(-z[1], z[0]) for z in row] for row in A]


def recover(M):
    m, n = len(M) // 2, len(M[0]) // 2
    return [[(M[i][j], -M[i][n + j]) for j in range(n)] for i in range(m)]


def interleave(M, m, n):
    """Real matrix in the interleaved coordinate order (re_1, im_1, re_2, im_2, ...): R'[2i+a][2j+b] = R[i + a m][j + b n]."""
    out = [[F(0)] * (2 * n) for _ in range(2 * m)]
    for i in range(m):
        for j in range(n):
            for a in range(2):
                for b in range(2):
                    out[2 * i + a][2 * j + b] = M[i + a * m][j + b * n]
    return out


def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    total = F(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += (-1) ** j * M[0][j] * det(minor)
    return total


def cdet(A):
    """Determinant of a small complex matrix of (re, im) Fractions by Laplace expansion."""
    n = len(A)
    if n == 1:
        return A[0][0]
    re, im = F(0), F(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in A[1:]]
        d = cdet(minor)
        z = A[0][j]
        sign = (-1) ** j
        re += sign * (z[0] * d[0] - z[1] * d[1])
        im += sign * (z[0] * d[1] + z[1] * d[0])
    return (re, im)


def subsets(n):
    for mask in range(1, 1 << n):
        yield [i for i in range(n) if mask >> i & 1]


def complex_psd(A):
    """Hermitian A is positive semidefinite iff every principal minor is >= 0 (the minors are real)."""
    for idx in subsets(len(A)):
        d = cdet([[A[i][j] for j in idx] for i in idx])
        assert d[1] == 0
        if d[0] < 0:
            return False
    return True


def real_psd(M):
    return all(det([[M[i][j] for j in idx] for i in idx]) >= 0 for idx in subsets(len(M)))


def flat(M):
    return [fq(x) for row in M for x in row]


def bit(b):
    return '1' if b else '0'


def record_prod(m, n, k, atok, btok):
    A, B = gparse(atok, m, n), gparse(btok, n, k)
    AB = cmatmul(A, B)
    RA, RB, RAB = realify(A), realify(B), realify(AB)
    tr = {'hermitian': '-', 'symmetric_RA': '-', 'trace_real': '-', 'trace_complex': '-', 'trace_identity': '-', 'trace_twice_complex': '-'}
    if m == n:
        trc = (sum(A[i][i][0] for i in range(n)), sum(A[i][i][1] for i in range(n)))
        trr = sum(RA[i][i] for i in range(2 * n))
        tr = {'hermitian': bit(star(A) == A), 'symmetric_RA': bit(transpose(RA) == RA), 'trace_real': fq(trr),
              'trace_complex': gtok(trc), 'trace_identity': bit(trr == 2 * trc[0]),
              'trace_twice_complex': bit(trr == 2 * trc[0] and 2 * trc[1] == 0)}
    ras = interleave(RA, m, n)
    rec = {'kind': 'prod', 'input': ['prod', m, n, k, list(atok), list(btok)], 'RAB': flat(RAB), 'RAstar': flat(realify(star(A))),
           'RA_interleaved': flat(ras), 'interleaved_commutes_block_J': rmatmul(jmat(m), ras) == rmatmul(ras, jmat(n)),
           'mult_ok': rmatmul(RA, RB) == RAB, 'intertwine_ok': rmatmul(jmat(m), RA) == rmatmul(RA, jmat(n)),
           'imul_ok': realify(imul(A)) == rmatmul(jmat(m), RA), 'star_ok': realify(star(A)) == transpose(RA),
           'roundtrip_ok': recover(RA) == A}
    rec.update(tr)
    return rec


def record_img(rows, cols, toks):
    M = [[F(toks[i * cols + j]) for j in range(cols)] for i in range(rows)]
    rec = {'kind': 'img', 'input': ['img', rows, cols, list(toks)]}
    if rows % 2 or cols % 2:
        rec.update({'status': 'odd_dim', 'commutes': '-', 'anticommutes': '-', 'symmetric': '-', 'hermitian': '-', 'recovered': []})
        return rec
    m, n = rows // 2, cols // 2
    JM, MJ = rmatmul(jmat(m), M), rmatmul(M, jmat(n))
    commutes = JM == MJ
    anti = JM == [[-x for x in r] for r in MJ]
    A = recover(M) if commutes else None
    rec.update({'status': 'ok' if commutes else 'noncommuting', 'commutes': bit(commutes), 'anticommutes': bit(anti),
                'symmetric': bit(transpose(M) == M) if rows == cols else '-',
                'hermitian': bit(star(A) == A) if (commutes and m == n) else '-',
                'recovered': [gtok(z) for row in A for z in row] if commutes else []})
    return rec


def record_psd(n, atok):
    A = gparse(atok, n, n)
    herm = star(A) == A
    rec = {'kind': 'psd', 'input': ['psd', n, list(atok)], 'hermitian': bit(herm), 'complex_psd': '-', 'real_psd': '-', 'agree': '-'}
    if herm:
        cp, rp = complex_psd(A), real_psd(realify(A))
        rec.update({'complex_psd': bit(cp), 'real_psd': bit(rp), 'agree': bit(cp == rp)})
    return rec


def mul2(X, Y):
    return (X[0] * Y[0] + X[1] * Y[2], X[0] * Y[1] + X[1] * Y[3], X[2] * Y[0] + X[3] * Y[2], X[2] * Y[1] + X[3] * Y[3])


J2 = (0, -1, 1, 0)


def record_jstruct(a, b, c, d):
    X = (a, b, c, d)
    return {'kind': 'jstruct', 'input': ['jstruct', a, b, c, d], 'sq_neg_id': mul2(X, X) == (-1, 0, 0, -1),
            'pm_J': X in (J2, (0, 1, -1, 0)), 'commutes_J': mul2(X, J2) == mul2(J2, X)}


def census(B):
    """Integer 2x2 matrices with entries in [-B, B] and X^2 = -I, from the trace-zero parametrization d = -a, bc = -(1 + a^2)."""
    found = []
    for a in range(-B, B + 1):
        N = 1 + a * a
        for b in range(-B, B + 1):
            if b != 0 and N % b == 0:
                c = -N // b
                if abs(c) <= B:
                    found.append((a, b, c, -a))
    return found


def record_jcensus(B):
    found = census(B)
    return {'kind': 'jcensus', 'input': ['jcensus', B], 'total': len(found),
            'commuting_J': sum(1 for X in found if mul2(X, J2) == mul2(J2, X)),
            'pm_J': sum(1 for X in found if X in (J2, (0, 1, -1, 0)))}


def record(case):
    kind = case[0]
    if kind == 'prod':
        return record_prod(*case[1:])
    if kind == 'img':
        return record_img(*case[1:])
    if kind == 'psd':
        return record_psd(*case[1:])
    if kind == 'jstruct':
        return record_jstruct(*case[1:])
    if kind == 'jcensus':
        return record_jcensus(*case[1:])
    raise ValueError('unknown kind')


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def wire_lines(data):
    out = []
    for r in data['records']:
        i = r['input']
        if r['kind'] == 'prod':
            out.append('\t'.join(['prod', str(i[1]), str(i[2]), str(i[3]), ','.join(r['RAB']), ','.join(r['RAstar']), ','.join(r['RA_interleaved']),
                                  bit(r['interleaved_commutes_block_J']), bit(r['mult_ok']), bit(r['intertwine_ok']),
                                  bit(r['imul_ok']), bit(r['star_ok']), bit(r['roundtrip_ok']), r['hermitian'], r['symmetric_RA'],
                                  r['trace_real'], r['trace_complex'], r['trace_identity'], r['trace_twice_complex']]))
        elif r['kind'] == 'img':
            out.append('\t'.join(['img', str(i[1]), str(i[2]), r['status'], r['commutes'], r['anticommutes'], r['symmetric'], r['hermitian'],
                                  ';'.join(r['recovered']) or '-']))
        elif r['kind'] == 'psd':
            out.append('\t'.join(['psd', str(i[1]), r['hermitian'], r['complex_psd'], r['real_psd'], r['agree']]))
        elif r['kind'] == 'jstruct':
            out.append('\t'.join(['jstruct', str(i[1]), str(i[2]), str(i[3]), str(i[4]), bit(r['sq_neg_id']), bit(r['pm_J']), bit(r['commutes_J'])]))
        else:
            out.append('\t'.join(['jcensus', str(i[1]), str(r['total']), str(r['commuting_J']), str(r['pm_J'])]))
    return out


def public_tsv(cases=CASES):
    out = []
    for c in cases:
        if c[0] == 'prod':
            out.append('prod\t%d\t%d\t%d\t%s\t%s\n' % (c[1], c[2], c[3], ';'.join(c[4]), ';'.join(c[5])))
        elif c[0] == 'img':
            out.append('img\t%d\t%d\t%s\n' % (c[1], c[2], ';'.join(c[3])))
        elif c[0] == 'psd':
            out.append('psd\t%d\t%s\n' % (c[1], ';'.join(c[2])))
        elif c[0] == 'jstruct':
            out.append('jstruct\t%d\t%d\t%d\t%d\n' % tuple(c[1:5]))
        else:
            out.append('jcensus\t%d\n' % c[1])
    return ''.join(out)
