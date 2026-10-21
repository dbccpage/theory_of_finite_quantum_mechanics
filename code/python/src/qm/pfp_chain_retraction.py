"""Chain retractions over Q: homology of a subcomplex inclusion and the existence of a retraction.

Producer for PFP batch 01, node PG-CHAIN-RETRACTION.  A case is a finite free chain complex D over Q (basis
sizes per degree and integer boundary matrices d_k : D_k -> D_{k-1}, columns = D_k basis) and a set of basis
vectors per degree spanning a candidate subcomplex C with the inclusion i.  For every case the producer computes

* whether C is closed under d (a subcomplex) and, if so, the dimensions, Betti numbers b_k(C), b_k(D);
* rank H_k(i) as dim(Z_k(C) + B_k(D)) - dim B_k(D), with Z_k(C) from an explicit nullspace;
* the linear system "r_k restricted to C_k is the identity and d r = r d" for r : D -> C, its rank and augmented rank
  (consistent iff a retraction exists), and, when consistent, the canonical solution (free unknowns set to 0) as data.

Exact Fractions only.  Scope: finite free complexes over Q listed in CASES; nothing about Z, torsion or infinite
complexes.  AuthorityEffect: None.
"""
from fractions import Fraction


def simplicial(vertices, edges, faces=(), solids=()):
    """Matrices d1, d2, d3 of an oriented simplicial complex given by vertex count and index tuples."""
    d1 = [[0] * len(edges) for _ in range(vertices)]
    for j, (a, b) in enumerate(edges):
        d1[a][j] -= 1
        d1[b][j] += 1
    index = {e: j for j, e in enumerate(edges)}
    d2 = [[0] * len(faces) for _ in edges]
    for j, (a, b, c) in enumerate(faces):
        d2[index[(b, c)]][j] += 1
        d2[index[(a, c)]][j] -= 1
        d2[index[(a, b)]][j] += 1
    findex = {f: j for j, f in enumerate(faces)}
    d3 = [[0] * len(solids) for _ in faces]
    for j, (a, b, c, d) in enumerate(solids):
        d3[findex[(b, c, d)]][j] += 1
        d3[findex[(a, c, d)]][j] -= 1
        d3[findex[(a, b, d)]][j] += 1
        d3[findex[(a, b, c)]][j] -= 1
    return d1, d2, d3


def encode(name, vertices, edges, faces, solids, sub):
    d1, d2, d3 = simplicial(vertices, edges, faces, solids)
    dims = [vertices, len(edges)] + ([len(faces)] if faces else []) + ([len(solids)] if solids else [])
    mats = [d1] + ([d2] if faces else []) + ([d3] if solids else [])
    mat_s = ';'.join('/'.join(','.join(str(x) for x in row) for row in m) for m in mats)
    sub_s = ';'.join('.'.join(str(i) for i in s) if s else '-' for s in sub)
    return ['cx', name, ','.join(str(x) for x in dims), mat_s, sub_s]


TRI_E = [(0, 1), (1, 2), (0, 2)]
TET_E = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
TET_F = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
CASES = [
    encode('two_isolated_points_in_edge', 2, [(0, 1)], [], [], [[0, 1], []]),
    encode('triangle_boundary_in_filled_triangle', 3, TRI_E, [(0, 1, 2)], [], [[0, 1, 2], [0, 1, 2], []]),
    encode('point_in_edge', 2, [(0, 1)], [], [], [[0], []]),
    encode('edge_in_filled_triangle', 3, TRI_E, [(0, 1, 2)], [], [[0, 1], [0], []]),
    encode('triangle_boundary_with_pendant_edge', 4, TRI_E + [(0, 3)], [], [], [[0, 1, 2], [0, 1, 2]]),
    encode('triangle_in_two_triangles_sharing_an_edge', 4, TRI_E + [(1, 3), (0, 3)], [], [], [[0, 1, 2], [0, 1, 2]]),
    encode('identity_inclusion', 3, TRI_E, [(0, 1, 2)], [], [[0, 1, 2], [0, 1, 2], [0]]),
    encode('zero_subcomplex', 3, TRI_E, [(0, 1, 2)], [], [[], [], []]),
    encode('path_closing_to_a_cycle', 3, TRI_E, [], [], [[0, 1, 2], [0, 1]]),
    encode('hollow_tetrahedron_in_solid_tetrahedron', 4, TET_E, TET_F, [(0, 1, 2, 3)], [[0, 1, 2, 3], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3], []]),
    encode('tetrahedron_1_skeleton_in_2_skeleton', 4, TET_E, TET_F, [], [[0, 1, 2, 3], [0, 1, 2, 3, 4, 5], []]),
    encode('filled_face_in_solid_tetrahedron', 4, TET_E, TET_F, [(0, 1, 2, 3)], [[0, 1, 2], [0, 1, 3], [0], []]),
    encode('edge_without_its_endpoint_is_not_a_subcomplex', 3, TRI_E, [(0, 1, 2)], [], [[0], [0], []]),
]


def parse(dims_s, mats_s, sub_s):
    dims = [int(x) for x in dims_s.split(',')]
    n = len(dims) - 1
    mats = []
    if n > 0:
        parts = mats_s.split(';')
        assert len(parts) == n
        for k, part in enumerate(parts, start=1):
            rows = [[int(x) for x in row.split(',')] for row in part.split('/')]
            assert len(rows) == dims[k - 1] and all(len(r) == dims[k] for r in rows)
            mats.append(rows)
    for k in range(2, n + 1):  # d_{k-1} d_k = 0
        for i in range(dims[k - 2]):
            for j in range(dims[k]):
                assert sum(mats[k - 2][i][t] * mats[k - 1][t][j] for t in range(dims[k - 1])) == 0
    subs = [[] if p == '-' else [int(x) for x in p.split('.')] for p in sub_s.split(';')]
    assert len(subs) == n + 1
    for k, s in enumerate(subs):
        assert s == sorted(set(s)) and all(0 <= i < dims[k] for i in s)
    return dims, mats, subs


def dmat(dims, mats, k):
    """d_k as rows (indexed by D_{k-1}) of columns (D_k); the zero maps outside 1..N."""
    n = len(dims) - 1
    if 1 <= k <= n:
        return mats[k - 1]
    rows = dims[k - 1] if 1 <= k <= n + 1 else 0
    cols = dims[k] if 0 <= k <= n else 0
    return [[0] * cols for _ in range(rows)]


def rref(rows, ncols):
    """Reduced row echelon form of a Fraction matrix; returns (rows, pivot columns)."""
    m = [[Fraction(x) for x in r] for r in rows]
    pivots, r = [], 0
    for c in range(ncols):
        pr = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if pr is None:
            continue
        m[r], m[pr] = m[pr], m[r]
        inv = 1 / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
    return m[:r], pivots


def rank(rows, ncols):
    return len(rref(rows, ncols)[1]) if rows and ncols else 0


def nullspace(rows, ncols):
    red, pivots = rref(rows, ncols) if rows else ([], [])
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for f in free:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for r, p in enumerate(pivots):
            v[p] = -red[r][f]
        basis.append(v)
    return basis


def columns(rows, ncols):
    return [[row[j] for row in rows] for j in range(ncols)]


def betti(dims, mats):
    n = len(dims) - 1
    rk = [rank(dmat(dims, mats, k), dims[k] if k <= n else 0) if 1 <= k <= n else 0 for k in range(n + 2)]
    return [dims[k] - rk[k] - rk[k + 1] for k in range(n + 1)]


def restrict(dims, mats, subs, k):
    return [[dmat(dims, mats, k)[a][c] for c in subs[k]] for a in subs[k - 1]]


def retraction_system(dims, mats, subs):
    """Unknown r_k[c][b] (c in C_k, b in D_k \\ C_k); equations dC_k r_k = r_{k-1} dD_k restricted to C_{k-1} rows."""
    n = len(dims) - 1
    var = {}
    for k in range(n + 1):
        for c in range(len(subs[k])):
            for b in range(dims[k]):
                if b not in subs[k]:
                    var[(k, c, b)] = len(var)

    def entry(k, c, b):
        """Linear form (dict var -> coefficient, constant) for r_k[c][b]."""
        if b in subs[k]:
            return {}, Fraction(1 if subs[k][c] == b else 0)
        return {var[(k, c, b)]: Fraction(1)}, Fraction(0)

    eqs = []
    for k in range(1, n + 1):
        dD = mats[k - 1]
        for a in range(len(subs[k - 1])):
            for b in range(dims[k]):
                coef, const = {}, Fraction(0)
                for ci, c in enumerate(subs[k]):
                    w = dD[subs[k - 1][a]][c]
                    if w:
                        lin, k0 = entry(k, ci, b)
                        for v, x in lin.items():
                            coef[v] = coef.get(v, 0) + w * x
                        const += w * k0
                for e in range(dims[k - 1]):
                    w = dD[e][b]
                    if w:
                        lin, k0 = entry(k - 1, a, e)
                        for v, x in lin.items():
                            coef[v] = coef.get(v, 0) - w * x
                        const -= w * k0
                eqs.append((coef, -const))
    return var, eqs


def solve_system(nvars, eqs):
    rows = []
    for coef, rhs in eqs:
        row = [Fraction(0)] * (nvars + 1)
        for v, x in coef.items():
            row[v] = Fraction(x)
        row[nvars] = Fraction(rhs)
        rows.append(row)
    a_rank = rank([r[:nvars] for r in rows], nvars) if nvars else 0
    red, pivots = rref(rows, nvars + 1) if rows else ([], [])
    aug_rank = len(pivots)
    if nvars in pivots:
        return a_rank, aug_rank, None
    sol = [Fraction(0)] * nvars
    for r, p in enumerate(pivots):
        sol[p] = red[r][nvars]
    return a_rank, aug_rank, sol


def record(name, dims_s, mats_s, sub_s):
    dims, mats, subs = parse(dims_s, mats_s, sub_s)
    n = len(dims) - 1
    closed = all(mats[k - 1][i][j] == 0 for k in range(1, n + 1) for j in subs[k] for i in range(dims[k - 1]) if i not in subs[k - 1])
    base = {'name': name, 'is_subcomplex': closed, 'dims_D': dims}
    if not closed:
        base.update({'dims_C': [], 'betti_C': [], 'betti_D': [], 'rank_hi': [], 'killed': -1, 'h_injective': False,
                     'retraction_exists': False, 'system_rank': -1, 'augmented_rank': -1, 'retraction': []})
        return base
    dimsC = [len(s) for s in subs]
    matsC = [restrict(dims, mats, subs, k) for k in range(1, n + 1)]
    bC, bD = betti(dimsC, matsC), betti(dims, mats)
    rank_hi = []
    for k in range(n + 1):
        zc = nullspace(dmat(dimsC, matsC, k), dimsC[k]) if k >= 1 else [[Fraction(int(i == j)) for i in range(dimsC[0])] for j in range(dimsC[0])]
        embedded = []
        for v in zc:
            w = [Fraction(0)] * dims[k]
            for pos, idx in enumerate(subs[k]):
                w[idx] = v[pos]
            embedded.append(w)
        bd_cols = columns(dmat(dims, mats, k + 1), dims[k + 1] if k + 1 <= n else 0) if k + 1 <= n else []
        r_b = rank(bd_cols, dims[k]) if bd_cols else 0
        r_all = rank(bd_cols + embedded, dims[k]) if (bd_cols or embedded) else 0
        rank_hi.append(r_all - r_b)
    killed = sum(b - r for b, r in zip(bC, rank_hi))
    var, eqs = retraction_system(dims, mats, subs)
    a_rank, aug_rank, sol = solve_system(len(var), eqs)
    retraction = []
    if sol is not None:
        for k in range(n + 1):
            mat = []
            for c in range(len(subs[k])):
                row = []
                for b in range(dims[k]):
                    row.append(str(Fraction(1 if subs[k][c] == b else 0)) if b in subs[k] else str(sol[var[(k, c, b)]]))
                mat.append(row)
            retraction.append(mat)
    base.update({'dims_C': dimsC, 'betti_C': bC, 'betti_D': bD, 'rank_hi': rank_hi, 'killed': killed,
                 'h_injective': killed == 0, 'retraction_exists': sol is not None, 'system_rank': a_rank,
                 'augmented_rank': aug_rank, 'retraction': retraction})
    return base


def certificate(cases=CASES):
    return {'records': [record(*c[1:]) for c in cases]}


def render(value):
    if isinstance(value, bool):
        return str(int(value))
    if isinstance(value, list):
        return ','.join(str(x) for x in value) or '-'
    return str(value)


FIELDS = ['is_subcomplex', 'dims_D', 'dims_C', 'betti_C', 'betti_D', 'rank_hi', 'killed', 'h_injective', 'retraction_exists',
          'system_rank', 'augmented_rank']


def wire_lines(data):
    return ['\t'.join(['chain', r['name']] + [render(r[f]) for f in FIELDS]) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('\t'.join(c) + '\n' for c in cases)
