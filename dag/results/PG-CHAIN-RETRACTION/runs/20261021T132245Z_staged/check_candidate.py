"""Independent checker for PG-CHAIN-RETRACTION.

Does not import the producer.  Differences in method:

* rank H_k(i): the producer computes dim(Z_k(C) + B_k(D)) - dim B_k(D) from an explicit nullspace.  This checker uses
  dim ker H_k(i) = rank(d_{k+1}^D) - rank(E_k) - rank(d_{k+1}^C), with E_k the rows of d_{k+1}^D outside the C_k basis
  (cycles of C that are boundaries of D, modulo boundaries of C), and rank H_k(i) = b_k(C) - dim ker; only ranks of
  matrices are used.
* the retraction system is built at the matrix level with linear forms in the unknown entries of r (r_k restricted to
  C_k is the identity; d^C r_k - r_{k-1} d^D = 0), solved by forward elimination and back substitution (producer: per-entry
  equations and reduced row echelon form); the canonical solution sets free unknowns to 0.
* the data retraction, when present, is also verified directly: r_k.i_k = id and the chain-map equation by matrix products.
* data-level consistency: a retraction exists only if H(i) is injective in every degree (the theorem proved in Lean); on
  this family the converse (H(i) injective implies a retraction over Q) is also enforced as an observation.
AuthorityEffect: None.
"""
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-CHAIN-RETRACTION'
KEYS = {'name', 'is_subcomplex', 'dims_D', 'dims_C', 'betti_C', 'betti_D', 'rank_hi', 'killed', 'h_injective',
        'retraction_exists', 'system_rank', 'augmented_rank', 'retraction'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def int_list(x):
    return type(x) is list and all(is_int(v) for v in x)


def forward_rank(matrix, ncols):
    m = [[Fraction(x) for x in row] for row in matrix]
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(r + 1, len(m)):
            if m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


def parse(dims_s, mats_s, sub_s):
    dims = list(map(int, dims_s.split(',')))
    n = len(dims) - 1
    mats = {}
    if n > 0:
        for k, part in enumerate(mats_s.split(';'), start=1):
            rows = [list(map(int, row.split(','))) for row in part.split('/')]
            require(len(rows) == dims[k - 1] and all(len(r) == dims[k] for r in rows), 'G1_SCHEMA:matrix_shape')
            mats[k] = rows
    subs = []
    for k, part in enumerate(sub_s.split(';')):
        s = [] if part == '-' else list(map(int, part.split('.')))
        require(s == sorted(set(s)) and all(0 <= i < dims[k] for i in s), 'G1_SCHEMA:subset')
        subs.append(s)
    require(len(subs) == n + 1, 'G1_SCHEMA:subset_count')
    for k in range(2, n + 1):
        for i in range(dims[k - 2]):
            for j in range(dims[k]):
                require(sum(mats[k - 1][i][t] * mats[k][t][j] for t in range(dims[k - 1])) == 0, 'G1_SCHEMA:d_squared_nonzero')
    return dims, mats, subs


def d(dims, mats, k):
    n = len(dims) - 1
    if 1 <= k <= n:
        return mats[k]
    return [[0] * (dims[k] if 0 <= k <= n else 0) for _ in range(dims[k - 1] if 1 <= k <= n + 1 else 0)]


def rk(dims, mats, k):
    n = len(dims) - 1
    return forward_rank(mats[k], dims[k]) if 1 <= k <= n else 0


def betti(dims, mats):
    n = len(dims) - 1
    return [dims[k] - rk(dims, mats, k) - rk(dims, mats, k + 1) for k in range(n + 1)]


def solve_retraction(dims, mats, subs):
    """Matrix-level linear forms. Returns (system_rank, augmented_rank, r or None)."""
    n = len(dims) - 1
    index = {}
    for k in range(n + 1):
        for c in range(len(subs[k])):
            for b in range(dims[k]):
                if b not in subs[k]:
                    index[(k, c, b)] = len(index)
    nv = len(index)

    def form(k, c, b):  # (coefficients list, constant)
        coef = [Fraction(0)] * nv
        if b in subs[k]:
            return coef, Fraction(1 if subs[k][c] == b else 0)
        coef[index[(k, c, b)]] = Fraction(1)
        return coef, Fraction(0)

    rows = []
    for k in range(1, n + 1):
        dD = mats[k]
        for a in range(len(subs[k - 1])):
            for b in range(dims[k]):
                coef = [Fraction(0)] * nv
                const = Fraction(0)
                # (dC_k r_k)[a][b] = sum over c in C_k of dD[subs[k-1][a]][subs[k][c]] * r_k[c][b]
                for c in range(len(subs[k])):
                    w = dD[subs[k - 1][a]][subs[k][c]]
                    cf, cs = form(k, c, b)
                    coef = [x + w * y for x, y in zip(coef, cf)]
                    const += w * cs
                # (r_{k-1} dD_k)[a][b] = sum over e in D_{k-1} of r_{k-1}[a][e] * dD[e][b]
                for e in range(dims[k - 1]):
                    w = dD[e][b]
                    cf, cs = form(k - 1, a, e)
                    coef = [x - w * y for x, y in zip(coef, cf)]
                    const -= w * cs
                rows.append(coef + [-const])
    plain = forward_rank([r[:nv] for r in rows], nv) if nv else 0
    aug = forward_rank(rows, nv + 1)
    if aug > plain:
        return plain, aug, None
    # back substitution, free unknowns zero
    m = [list(r) for r in rows]
    piv_cols = []
    r = 0
    for c in range(nv):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(r + 1, len(m)):
            if m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv_cols.append(c)
        r += 1
    sol = [Fraction(0)] * nv
    for row_i in range(len(piv_cols) - 1, -1, -1):
        c = piv_cols[row_i]
        total = m[row_i][nv] - sum(m[row_i][j] * sol[j] for j in range(c + 1, nv))
        sol[c] = total / m[row_i][c]
    rmats = []
    for k in range(n + 1):
        rmats.append([[Fraction(1 if subs[k][c] == b else 0) if b in subs[k] else sol[index[(k, c, b)]] for b in range(dims[k])]
                      for c in range(len(subs[k]))])
    return plain, aug, rmats


def verify_retraction(dims, mats, subs, r):
    n = len(dims) - 1
    for k in range(n + 1):
        for c in range(len(subs[k])):
            for pos, b in enumerate(subs[k]):
                if r[k][c][b] != (1 if pos == c else 0):
                    return False
    for k in range(1, n + 1):
        for a in range(len(subs[k - 1])):
            for b in range(dims[k]):
                left = sum(mats[k][subs[k - 1][a]][subs[k][c]] * r[k][c][b] for c in range(len(subs[k])))
                right = sum(r[k - 1][a][e] * mats[k][e][b] for e in range(dims[k - 1]))
                if left != right:
                    return False
    return True


_CACHE = {}


def expected(name, dims_s, mats_s, sub_s):
    key = (name, dims_s, mats_s, sub_s)
    if key in _CACHE:
        return _CACHE[key]
    dims, mats, subs = parse(dims_s, mats_s, sub_s)
    n = len(dims) - 1
    closed = all(mats[k][i][j] == 0 for k in range(1, n + 1) for j in subs[k] for i in range(dims[k - 1]) if i not in subs[k - 1])
    out = {'name': name, 'is_subcomplex': closed, 'dims_D': dims}
    if not closed:
        out.update({'dims_C': [], 'betti_C': [], 'betti_D': [], 'rank_hi': [], 'killed': -1, 'h_injective': False,
                    'retraction_exists': False, 'system_rank': -1, 'augmented_rank': -1, 'retraction': []})
        _CACHE[key] = out
        return out
    dimsC = [len(s) for s in subs]
    matsC = {k: [[mats[k][a][c] for c in subs[k]] for a in subs[k - 1]] for k in range(1, n + 1)}
    bC, bD = betti(dimsC, matsC), betti(dims, mats)
    kernel = []
    for k in range(n + 1):
        if k == n:
            kernel.append(0)
            continue
        rows_out = [row for i, row in enumerate(mats[k + 1]) if i not in subs[k]]
        kernel.append(rk(dims, mats, k + 1) - (forward_rank(rows_out, dims[k + 1]) if rows_out else 0) - rk(dimsC, matsC, k + 1))
    rank_hi = [b - z for b, z in zip(bC, kernel)]
    plain, aug, r = solve_retraction(dims, mats, subs)
    out.update({'dims_C': dimsC, 'betti_C': bC, 'betti_D': bD, 'rank_hi': rank_hi, 'killed': sum(kernel),
                'h_injective': sum(kernel) == 0, 'retraction_exists': r is not None, 'system_rank': plain, 'augmented_rank': aug,
                'retraction': [] if r is None else [[[str(x) for x in row] for row in mat] for mat in r]})
    if r is not None:
        require(verify_retraction(dims, mats, subs, r), 'G3_WITNESS:internal_retraction')
    _CACHE[key] = out
    return out


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = [tuple(c) for c in public['cases']]
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        by_name = {c[1]: c for c in cases}
        seen = []
        for r in records:
            require(type(r) is dict and set(r) == KEYS, 'G1_SCHEMA:record_keys')
            require(type(r['name']) is str and r['name'] in by_name, 'G2_COVERAGE:name')
            seen.append(r['name'])
            want = expected(*by_name[r['name']][1:])
            require(type(r['is_subcomplex']) is bool and type(r['h_injective']) is bool and type(r['retraction_exists']) is bool, 'G1_SCHEMA:bool')
            for key in ('dims_D', 'dims_C', 'betti_C', 'betti_D', 'rank_hi'):
                require(int_list(r[key]), 'G1_SCHEMA:' + key)
            for key in ('killed', 'system_rank', 'augmented_rank'):
                require(is_int(r[key]), 'G1_SCHEMA:' + key)
            ret = r['retraction']
            require(type(ret) is list and all(type(m) is list and all(type(row) is list and all(type(x) is str for x in row) for row in m) for m in ret),
                    'G1_SCHEMA:retraction')
            for key in sorted(KEYS):
                require(r[key] == want[key] and type(r[key]) is type(want[key]), 'G3_WITNESS:' + key)
            # theorem-level consistency
            if r['retraction_exists']:
                require(r['h_injective'] and r['killed'] == 0, 'G3_WITNESS:retraction_forces_injective_homology')
                require(r['system_rank'] == r['augmented_rank'], 'G3_WITNESS:consistent_system')
            elif r['is_subcomplex']:
                require(r['system_rank'] < r['augmented_rank'], 'G3_WITNESS:inconsistent_system')
                require(r['h_injective'] == (r['killed'] == 0), 'G3_WITNESS:killed_iff_not_injective')
            require(r['h_injective'] == r['retraction_exists'] or not r['is_subcomplex'], 'G3_WITNESS:converse_over_Q_on_this_family')
        require(sorted(seen) == sorted(by_name), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ValueError, ZeroDivisionError) as error:
        if isinstance(error, ValueError) and str(error).startswith('G'):
            raise
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
