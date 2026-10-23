"""Independent exact recomputation of the numbers in the FOC-035 observer-presheaf nodes.

No repository imports. Everything is restated with fractions.Fraction and plain tuples:
the Bell scenario, the PR box, the noisy PR box, the global-section counts, the exact
noncontextual fraction and l1 defect (each by a two-phase simplex whose answer is then
re-verified by a primal and a dual certificate that do not trust the simplex), the descent
counts on the maximal cover and on the arc cover, the parity cycles for n = 3, 4, 5 and all
2^n targets, the Cech quotient value Phi_1 = 2 on the Bell nerve, delta1 delta0 = 0 on a
nerve with a triple, the Vorob'ev product-formula gluing on a three-context path, and the
size ceilings. It exits 0 and prints each check when every one holds.

    python -I -X utf8 checks/independent/foc035_observer_presheaf.py

AuthorityEffect: None. This restates finite instances; it is not a proof of the general
statements in the nodes, and it does not run the Rust or Python code of the source note.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product

CHECKED: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def ok(label: str, condition: bool) -> None:
    if not condition:
        raise SystemExit("FAILED: " + label)
    CHECKED.append(label)
    print("ok  " + label)


# ---------------------------------------------------------------------------------------------
# Exact LP: minimise c.x subject to A x = b, x >= 0 (b >= 0), two-phase simplex with Bland's rule.
# The caller verifies the returned primal and dual independently of this routine.

def simplex_min(c, A, b):
    m, n = len(A), len(c)
    require(all(v >= 0 for v in b), "invalid exact certificate: all(v >= 0 for v in b)")
    tab = [[F(x) for x in A[i]] + [F(1) if j == i else F(0) for j in range(m)] + [F(b[i])] for i in range(m)]
    basis = [n + i for i in range(m)]
    width = n + m

    def pivot(r, col):
        piv = tab[r][col]
        tab[r] = [x / piv for x in tab[r]]
        for i in range(m):
            if i != r and tab[i][col] != 0:
                f = tab[i][col]
                tab[i] = [x - f * y for x, y in zip(tab[i], tab[r])]
        basis[r] = col

    def reduced(cost):
        return [cost[j] - sum(cost[basis[i]] * tab[i][j] for i in range(m)) for j in range(width)]

    def run(cost, allowed):
        while True:
            red = reduced(cost)
            enter = next((j for j in range(width) if j in allowed and red[j] < 0), None)
            if enter is None:
                return
            rows = [(tab[i][-1] / tab[i][enter], basis[i], i) for i in range(m) if tab[i][enter] > 0]
            if not rows:
                raise SystemExit("unbounded LP")
            r = min(rows)[2]
            pivot(r, enter)

    phase1 = [F(0)] * n + [F(1)] * m
    run(phase1, set(range(width)))
    if sum(tab[i][-1] for i in range(m) if basis[i] >= n) != 0:
        return None
    for i in range(m):  # drive artificial variables out of the basis where possible
        if basis[i] >= n:
            col = next((j for j in range(n) if tab[i][j] != 0), None)
            if col is not None:
                pivot(i, col)
    cost = [F(x) for x in c] + [F(0)] * m
    run(cost, set(range(n)))
    x = [F(0)] * n
    for i in range(m):
        if basis[i] < n:
            x[basis[i]] = tab[i][-1]
    red = reduced(cost)
    y = [-red[n + i] for i in range(m)]
    return x, y


def verify_lp(c, A, b, x, y):
    """x primal feasible, y dual feasible (c_j - y.A_j >= 0), equal objectives."""
    m, n = len(A), len(c)
    require(len(b) == m and len(y) == m and len(x) == n and all(len(row) == n for row in A),
            "certificate dimensions do not match the LP")
    values = list(c) + list(b) + list(x) + list(y) + [v for row in A for v in row]
    require(all(type(v) is int or isinstance(v, F) for v in values), "certificate entries must be exact integers or fractions")
    require(all(v >= 0 for v in x), "invalid exact certificate: all(v >= 0 for v in x)")
    require(all(sum(A[i][j] * x[j] for j in range(n)) == b[i] for i in range(m)), "invalid exact certificate: all(sum(A[i][j] * x[j] for j in range(n)) == b[i] for i in range(m))")
    require(all(c[j] - sum(y[i] * A[i][j] for i in range(m)) >= 0 for j in range(n)), "invalid exact certificate: all(c[j] - sum(y[i] * A[i][j] for i in range(m)) >= 0 for j in range(n))")
    primal = sum(c[j] * x[j] for j in range(n))
    dual = sum(b[i] * y[i] for i in range(m))
    require(primal == dual, "invalid exact certificate: primal == dual")
    return primal


# ---------------------------------------------------------------------------------------------
# Scenarios: measurements 0..M-1 with two outcomes, contexts as sorted tuples.

class Scenario:
    def __init__(self, n, contexts):
        self.n = n
        self.contexts = [tuple(c) for c in contexts]
        self.globals = list(product((0, 1), repeat=n))

    def sections(self, positions):
        return list(product((0, 1), repeat=len(positions)))

    def restrict(self, g, positions):
        return tuple(g[p] for p in positions)

    def rows(self):
        return [(k, s) for k, c in enumerate(self.contexts) for s in self.sections(c)]

    def incidence(self):
        rows = self.rows()
        return [[F(1) if self.restrict(g, self.contexts[k]) == s else F(0) for g in self.globals] for k, s in rows]

    def stacked(self, dists):
        return [dists[k][s] for k, s in self.rows()]

    def support_globals(self, dists):
        return [g for g in self.globals
                if all(dists[k][self.restrict(g, c)] > 0 for k, c in enumerate(self.contexts))]

    def marginal(self, dist, positions, sub):
        idx = [positions.index(p) for p in sub]
        out = {}
        for s, v in dist.items():
            key = tuple(s[i] for i in idx)
            out[key] = out.get(key, F(0)) + v
        return out


def parity_dist(target):
    return {(x, y): (F(1, 2) if (x ^ y) == target else F(0)) for x in (0, 1) for y in (0, 1)}


BELL = Scenario(4, [(0, 2), (0, 3), (1, 2), (1, 3)])  # a=0, a'=1, b=2, b'=3; contexts ab, ab', a'b, a'b'


def pr_box():
    return [parity_dist(t) for t in (0, 0, 0, 1)]


def noisy_pr(lam):
    return [{s: (1 - lam) * v + lam * F(1, 4) for s, v in d.items()} for d in pr_box()]


def point_mass(scen, g):
    return [{s: (F(1) if scen.restrict(g, c) == s else F(0)) for s in scen.sections(c)} for c in scen.contexts]


def mixture(a, b):
    return [{s: (da[s] + db[s]) / 2 for s in da} for da, db in zip(a, b)]


def ncf(scen, dists):
    """Exact noncontextual fraction with verified primal and dual certificates."""
    A = scen.incidence()
    e = scen.stacked(dists)
    m, n = len(A), len(scen.globals)
    Aeq = [row + [F(1) if j == i else F(0) for j in range(m)] for i, row in enumerate(A)]
    c = [F(-1)] * n + [F(0)] * m
    x, y = simplex_min(c, Aeq, e)
    value = verify_lp(c, Aeq, e, x, y)
    return -value


def l1_defect(scen, dists):
    """min ||e - A p||_1 over p in the simplex, certified by an explicit dual witness."""
    A = scen.incidence()
    e = scen.stacked(dists)
    m, n = len(A), len(scen.globals)
    rows = []
    for i in range(m):
        rows.append(A[i] + [F(-1) if j == i else F(0) for j in range(m)] + [F(1) if j == i else F(0) for j in range(m)])
    rows.append([F(1)] * n + [F(0)] * (2 * m))
    b = e + [F(1)]
    c = [F(0)] * n + [F(1)] * (2 * m)
    x, y = simplex_min(c, rows, b)
    value = verify_lp(c, rows, b, x, y)
    p = x[:n]
    resid = [sum(A[i][j] * p[j] for j in range(n)) - e[i] for i in range(m)]
    require(sum(abs(r) for r in resid) == value and sum(p) == 1, "invalid exact certificate: sum(abs(r) for r in resid) == value and sum(p) == 1")
    phi, y0 = y[:m], y[m]
    require(all(abs(v) <= 1 for v in phi), "invalid exact certificate: all(abs(v) <= 1 for v in phi)")
    require(all(sum(phi[i] * A[i][j] for i in range(m)) + y0 <= 0 for j in range(n)), "invalid exact certificate: all(sum(phi[i] * A[i][j] for i in range(m)) + y0 <= 0 for j in range(n))")
    require(sum(phi[i] * e[i] for i in range(m)) + y0 == value, "invalid exact certificate: sum(phi[i] * e[i] for i in range(m)) + y0 == value")
    return value


def matching_families(scen, dists, cover):
    """Matching families over `cover` (position tuples), their gluings in S(M) and the outcome counts."""
    supp = [{s for s, v in d.items() if v > 0} for d in dists]

    def admissible(positions):
        out = []
        for s in scen.sections(positions):
            inside = [k for k, c in enumerate(scen.contexts) if set(c) <= set(positions)]
            if all(tuple(s[positions.index(p)] for p in scen.contexts[k]) in supp[k] for k in inside):
                out.append(s)
        return out

    local = [admissible(tuple(u)) for u in cover]
    glob = set(scen.support_globals(dists))
    unique = ambiguous = none = fams = 0
    for choice in product(*local):
        agree = True
        for i in range(len(cover)):
            for j in range(i + 1, len(cover)):
                common = [p for p in cover[i] if p in cover[j]]
                if tuple(choice[i][cover[i].index(p)] for p in common) != tuple(choice[j][cover[j].index(p)] for p in common):
                    agree = False
        if not agree:
            continue
        fams += 1
        glues = [g for g in glob if all(scen.restrict(g, tuple(cover[i])) == choice[i] for i in range(len(cover)))]
        if len(glues) == 1:
            unique += 1
        elif len(glues) > 1:
            ambiguous += 1
        else:
            none += 1
    return fams, unique, ambiguous, none


# ---------------------------------------------------------------------------------------------
# B1: marginalisation is functorial on the chains inside each maximal context (instances).

def check_functoriality():
    """rho^C_W = rho^V_W o rho^C_V for every chain W <= V <= C, and rho^C_C = id."""
    from itertools import combinations
    for dists in (pr_box(), noisy_pr(F(1, 4)), noisy_pr(F(1, 2))):
        for k, c in enumerate(BELL.contexts):
            d = dists[k]
            if BELL.marginal(d, c, c) != d:
                return False
            for r in range(len(c) + 1):
                for v in combinations(c, r):
                    mid = BELL.marginal(d, c, v)
                    for s in range(len(v) + 1):
                        for w in combinations(v, s):
                            if BELL.marginal(d, c, w) != BELL.marginal(mid, v, w):
                                return False
    return True


def main() -> None:
    # --- fixed models ---
    pr = pr_box()
    ok("PR box rows are distributions", all(sum(d.values()) == 1 and min(d.values()) >= 0 for d in pr))
    ok("B1: restriction is functorial on every chain W <= V <= C (PR, noisy 1/4, noisy 1/2)", check_functoriality())
    overlaps_agree = all(
        BELL.marginal(pr[i], BELL.contexts[i], (p,)) == BELL.marginal(pr[j], BELL.contexts[j], (p,))
        for i in range(4) for j in range(i + 1, 4) for p in set(BELL.contexts[i]) & set(BELL.contexts[j]))
    ok("PR box is no-signalling (all overlap marginals agree)", overlaps_agree)

    # --- B4: strongly contextual, NCF 0, |G| = 0, defect 2 ---
    ok("PR box: |G| = 0", len(BELL.support_globals(pr)) == 0)
    ok("PR box: NCF = 0", ncf(BELL, pr) == 0)
    delta_pr = l1_defect(BELL, pr)
    ok("PR box: l1 defect = 2", delta_pr == 2)

    # --- B5 and B2: noisy PR ---
    for lam in (F(1, 4), F(1, 2)):
        ok(f"noisy PR lambda={lam}: NCF = 2*lambda = {2 * lam}", ncf(BELL, noisy_pr(lam)) == 2 * lam)
    q = noisy_pr(F(1, 4))
    ok("noisy PR lambda=1/4: not strongly contextual (|G| = 16 > 0) and l1 defect positive",
       len(BELL.support_globals(q)) == 16 and l1_defect(BELL, q) > 0)
    h = noisy_pr(F(1, 2))
    ok("noisy PR lambda=1/2: |G| = 16", len(BELL.support_globals(h)) == 16)
    ok("noisy PR lambda=1/2: l1 defect = 0", l1_defect(BELL, h) == 0)

    # --- mixture of two deterministic assignments ---
    g1, g2 = (0, 0, 0, 0), (1, 0, 0, 1)
    mix = mixture(point_mass(BELL, g1), point_mass(BELL, g2))
    ok("mixture of (0,0,0,0) and (1,0,0,1): NCF = 1 and |G| = 2",
       ncf(BELL, mix) == 1 and len(BELL.support_globals(mix)) == 2)

    # --- B3: signed global section of the PR box, found by solving the linear system exactly ---
    A = BELL.incidence()
    e = BELL.stacked(pr)
    rows = [row[:] for row in A] + [[F(1)] * 16]
    rhs = e + [F(1)]
    # Solve A d = e, sum d = 1 by Gauss-Jordan over Fractions; free variables set to zero.
    mat = [rows[i][:16] + [rhs[i]] for i in range(len(rows))]
    piv_cols, r = [], 0
    for col in range(16):
        pr_row = next((i for i in range(r, len(mat)) if mat[i][col] != 0), None)
        if pr_row is None:
            continue
        mat[r], mat[pr_row] = mat[pr_row], mat[r]
        mat[r] = [x / mat[r][col] for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][col] != 0:
                f = mat[i][col]
                mat[i] = [x - f * y for x, y in zip(mat[i], mat[r])]
        piv_cols.append(col)
        r += 1
    consistent = all(row[16] == 0 for row in mat if all(x == 0 for x in row[:16]))
    d = [F(0)] * 16
    for i, col in enumerate(piv_cols):
        d[col] = mat[i][16]
    ok("PR box: a signed global section exists, sums to 1, matches all marginals, and has a negative entry",
       consistent and sum(d) == 1 and all(sum(A[i][j] * d[j] for j in range(16)) == e[i] for i in range(16)) and min(d) < 0)

    # --- B6, B7: descent counts ---
    full = [tuple(c) for c in BELL.contexts]
    ok("maximal cover, PR box: 0 families", matching_families(BELL, pr, full)[0] == 0)
    fams = matching_families(BELL, h, full)
    ok("maximal cover, noisy PR 1/2: 16 families, all Unique, none NoGlobalExtension", fams == (16, 16, 0, 0))
    arcs = [(0, 1, 2), (1, 2, 3)]
    ok("arc cover, mixture of two assignments: 4 families, 2 Unique, 2 NoGlobalExtension",
       matching_families(BELL, mix, arcs) == (4, 2, 0, 2))

    # --- B11: parity cycles ---
    for n in (3, 4, 5):
        ctxs = [tuple(sorted((i, (i + 1) % n))) for i in range(n)]
        scen = Scenario(n, ctxs)
        for bits in range(1 << n):
            t = [(bits >> i) & 1 for i in range(n)]
            dists = []
            for i, c in enumerate(ctxs):
                x, y = c
                # target t_i is the parity of (x_i, x_{i+1}); store on the sorted pair
                dists.append({(u, v): (F(1, 2) if (u ^ v) == t[i] else F(0)) for u in (0, 1) for v in (0, 1)})
            hol = sum(t) % 2
            G = len(scen.support_globals(dists))
            arcs_n = [tuple(range(0, n - 1)), tuple(range(1, n))]
            fams, uni, amb, nge = matching_families(scen, dists, arcs_n)
            frac = ncf(scen, dists)
            good = (G == (0 if hol else 2) and fams == 2 and amb == 0 and nge == (2 if hol else 0)
                    and uni == (0 if hol else 2) and frac == (0 if hol else 1))
            if not good:
                raise SystemExit(f"FAILED parity cycle n={n} targets={t}: G={G} fams={fams} nge={nge} ncf={frac}")
        ok(f"parity cycles n={n}: all {1 << n} target vectors agree with the holonomy statement "
           "(|G| in {0,2}, 2 families, NoGlobalExtension iff holonomy 1, NCF 0 iff holonomy 1)", True)
    ok("n=3 nerve: three contexts, three pairs, no triple intersection",
       all(len(set(a) & set(b)) == 1 for a, b in [((0, 1), (1, 2)), ((1, 2), (0, 2)), ((0, 1), (0, 2))])
       and set((0, 1)) & set((1, 2)) & set((0, 2)) == set())

    # --- B9: Cech coboundary on the Bell nerve, Phi_1 = 2 by matching primal and dual bounds ---
    pairs = [(i, j) for i in range(4) for j in range(i + 1, 4) if set(BELL.contexts[i]) & set(BELL.contexts[j])]
    ok("Bell nerve: exactly four edges (a 4-cycle) and no triple intersection",
       len(pairs) == 4 and not any(set(BELL.contexts[i]) & set(BELL.contexts[j]) & set(BELL.contexts[k])
                                   for i in range(4) for j in range(i + 1, 4) for k in range(j + 1, 4)))
    edge_pos = {p: sorted(set(BELL.contexts[p[0]]) & set(BELL.contexts[p[1]])) for p in pairs}

    def delta0(alpha):
        out = {}
        for (i, j) in pairs:
            pos = edge_pos[(i, j)]
            li = BELL.marginal(alpha[i], BELL.contexts[i], pos)
            lj = BELL.marginal(alpha[j], BELL.contexts[j], pos)
            out[(i, j)] = [li.get(s, F(0)) - lj.get(s, F(0)) for s in BELL.sections(pos)]
        return out

    def norm1(om):
        return sum(abs(x) for v in om.values() for x in v)

    omega = {p: [F(0), F(0)] for p in pairs}
    omega[pairs[0]] = [F(1), F(1)]
    ok("Phi_1 upper bound: alpha = 0 gives ||omega||_1 = 2", norm1(omega) == 2)
    # Dual witness phi with sup norm 1 and phi^T delta0 = 0, found by hand (signs alternate round the
    # 4-cycle so that the terms at every context cancel) and re-checked below on every basis 0-cochain.
    phi = {}
    phi[(0, 1)] = [F(1), F(1)]
    phi[(0, 2)] = [F(-1), F(-1)]
    phi[(1, 3)] = [F(1), F(1)]
    phi[(2, 3)] = [F(-1), F(-1)]
    ok("Bell nerve edges are (0,1), (0,2), (1,3), (2,3)", pairs == [(0, 1), (0, 2), (1, 3), (2, 3)])
    kills_all = True
    for k in range(4):
        for s in BELL.sections(BELL.contexts[k]):
            alpha = [{t: F(0) for t in BELL.sections(c)} for c in BELL.contexts]
            alpha[k][s] = F(1)
            dd = delta0(alpha)
            if sum(a * b for p in pairs for a, b in zip(phi[p], dd[p])) != 0:
                kills_all = False
    ok("Phi_1 dual witness: sup norm 1 and phi annihilates delta0 of every basis 0-cochain", kills_all)
    lower = sum(a * b for p in pairs for a, b in zip(phi[p], omega[p]))
    ok("Phi_1 lower bound: <phi, omega> = 2, so Phi_1 = 2", lower == 2)
    beta = [{t: F(i + k) for k, t in enumerate(BELL.sections(c))} for i, c in enumerate(BELL.contexts)]
    shift = delta0(beta)
    shifted = {p: [a + b for a, b in zip(omega[p], shift[p])] for p in pairs}
    ok("gauge invariance: Phi_1(omega + delta0 beta) is again 2 (lower bound by the same witness, upper bound by alpha = beta)",
       sum(a * b for p in pairs for a, b in zip(phi[p], shifted[p])) == 2)
    sig = [dict(d) for d in h]
    sig[1] = {(0, 0): F(1, 2), (0, 1): F(1, 2), (1, 0): F(0), (1, 1): F(0)}
    dd = delta0(sig)
    ok("signalling example: delta0 e is nonzero at the pair (0,1) with overlap {0} and unequal marginals",
       any(x != 0 for x in dd[(0, 1)]) and edge_pos[(0, 1)] == [0])
    ok("PR box: delta0 e = 0", all(x == 0 for v in delta0(pr).values() for x in v))

    # --- B9: delta1 delta0 = 0 on the cover {0,1},{0,2},{0,3} (one triple) ---
    ctx3 = [(0, 1), (0, 2), (0, 3)]
    pairs3 = [(0, 1), (0, 2), (1, 2)]
    ok("three contexts through measurement 0: pairs (0,1),(0,2),(1,2) and one triple, overlaps {0}",
       all(set(ctx3[i]) & set(ctx3[j]) == {0} for i, j in pairs3) and set(ctx3[0]) & set(ctx3[1]) & set(ctx3[2]) == {0})
    sc3 = Scenario(4, ctx3)
    alpha3 = [{s: F((i * 5 + k * 3) % 7 - 3) for k, s in enumerate(sc3.sections(c))} for i, c in enumerate(ctx3)]
    sections0 = [(0,), (1,)]
    w01 = {}
    for (i, j) in pairs3:
        li = sc3.marginal(alpha3[i], ctx3[i], (0,))
        lj = sc3.marginal(alpha3[j], ctx3[j], (0,))
        w01[(i, j)] = [li[s] - lj[s] for s in sections0]
    curv = [w01[(1, 2)][k] - w01[(0, 2)][k] + w01[(0, 1)][k] for k in range(2)]
    ok("delta1 delta0 alpha = 0 on the triple (0,1,2), with delta0 alpha not zero", curv == [0, 0] and any(x != 0 for v in w01.values() for x in v))
    beta1 = {(0, 1): [F(1), F(0)], (0, 2): [F(0), F(0)], (1, 2): [F(0), F(0)]}
    curv_b = [beta1[(1, 2)][k] - beta1[(0, 2)][k] + beta1[(0, 1)][k] for k in range(2)]
    ok("delta1 of a 1-cochain supported on one pair is [1, 0] (a non-cocycle is detected)", curv_b == [1, 0])

    # --- B13: Vorob'ev product formula on the path {0,1},{1,2},{2,3} with parity targets 0,1,1 ---
    path = Scenario(4, [(0, 1), (1, 2), (2, 3)])
    pd = [parity_dist(t) for t in (0, 1, 1)]
    joint = {}
    for g in path.globals:
        num = F(1)
        for k, c in enumerate(path.contexts):
            num *= pd[k][path.restrict(g, c)]
        den = F(1)
        for pos in (1, 2):
            marg = path.marginal(pd[pos - 1], path.contexts[pos - 1], (pos,))
            den *= marg[(g[pos],)]
        joint[g] = num / den if den != 0 else F(0)
    ok("path cover: product formula gives a distribution with exactly the three given marginals",
       sum(joint.values()) == 1 and min(joint.values()) >= 0 and all(
           path.marginal({g: v for g, v in joint.items()}, tuple(range(4)), c) == pd[k] for k, c in enumerate(path.contexts)))
    ok("path cover: NCF = 1 (the section is a distribution)", ncf(path, pd) == 1)

    def gyo(edges):
        work = [set(x) for x in edges]
        changed = True
        while changed:
            changed = False
            for v in {v for e in work for v in e}:
                holders = [e for e in work if v in e]
                if len(holders) == 1:
                    holders[0].discard(v)
                    changed = True
            for i, e in enumerate(work):
                if any(i != j and e <= f for j, f in enumerate(work)):
                    work.pop(i)
                    changed = True
                    break
            work = [e for e in work if e]
        return not work

    ok("GYO: the three-context path and the two-context path are acyclic, the Bell 4-cycle and a triangle are not",
       gyo([{0, 1}, {1, 2}, {2, 3}]) and gyo([{0, 1}, {1, 2}]) and not gyo([set(c) for c in BELL.contexts])
       and not gyo([{0, 1}, {1, 2}, {0, 2}]))

    # --- B14: the instances of the repaired Test 482 of the source repository (the test itself is not imported) ---
    p_ab = {(0, 0): F(1, 2), (0, 1): F(1, 6), (1, 0): F(1, 12), (1, 1): F(1, 4)}
    p_bc = {(0, 0): F(1, 3), (0, 1): F(1, 4), (1, 0): F(1, 6), (1, 1): F(1, 4)}
    pb_ab = {b: sum(v for (_, bb), v in p_ab.items() if bb == b) for b in (0, 1)}
    pb_bc = {b: sum(v for (bb, _), v in p_bc.items() if bb == b) for b in (0, 1)}
    ok("Test 482 tables: p_ab and p_bc are distributions that agree on the overlap marginal", sum(p_ab.values()) == 1
       and sum(p_bc.values()) == 1 and pb_ab == pb_bc)
    joint482 = {(a, b, c): p_ab[(a, b)] * p_bc[(b, c)] / pb_ab[b] for a in (0, 1) for b in (0, 1) for c in (0, 1)}
    ok("Test 482 tables: the product formula p_ab p_bc / p_b has total mass 1 and reproduces both tables exactly",
       sum(joint482.values()) == 1
       and all(sum(v for (a, b, _), v in joint482.items() if (a, b) == k) == want for k, want in p_ab.items())
       and all(sum(v for (_, b, c), v in joint482.items() if (b, c) == k) == want for k, want in p_bc.items()))
    ok("Test 482 covers: GYO accepts {ab, bc} and rejects {ab, bc, ac}",
       gyo([{"a", "b"}, {"b", "c"}]) and not gyo([{"a", "b"}, {"b", "c"}, {"a", "c"}]))
    compatible = [(a, b, c) for a, b, c in product((0, 1), repeat=3) if (a ^ b) == 0 and (b ^ c) == 0 and (a ^ c) == 1]
    ok("Test 482 triangle: no assignment among the 8 satisfies a = b, b = c and a != c", len(compatible) == 0)

    # --- A2: the table of conditional underdetermination (K row, Adm row, norm and terminal arithmetic) ---
    sub = Scenario(3, [(0, 1), (0, 2)])  # measurements a=0, b=1, b'=2; sub-cover {ab, ab'}
    prsub = [parity_dist(0), parity_dist(0)]
    ok("K row: the PR box on the acyclic sub-cover {ab, ab'} has l1 defect 0 (versus 2 on the Bell cover)",
       l1_defect(sub, prsub) == 0 and delta_pr == 2)
    ok("Adm row: the PR box is no-signalling, so its distance to the no-signalling polytope is 0 (versus 2)",
       overlaps_agree and delta_pr == 2)
    ok("norm row: 2 * (l1 defect 2) = 4", 2 * delta_pr == 4)
    ok("terminal row: the defect 2 is below the threshold 3 of the alternative rule, so ExactRepair differs from OpenObstruction",
       delta_pr < 3 and BELL.support_globals(pr) == [])

    # --- B16: ceilings ---
    ok("ceilings: 2^20 assignments and 2^22 LP entries; 2^64 > 2^20; 2^21 > 2^20; ten singletons 1024 <= 2^20 and 20*1024 <= 2^22",
       2 ** 20 == 1048576 and 2 ** 22 == 4194304 and 2 ** 64 > 2 ** 20 and 2 ** 21 > 2 ** 20
       and 2 ** 10 <= 2 ** 20 and 20 * 1024 <= 2 ** 22)

    # --- C6: the packet (p, p, p) fails pairwise distinctness on three counts ---
    packet = ("p", "p", "p")
    fails = [(i, j) for i in range(3) for j in range(i + 1, 3) if packet[i] == packet[j]]
    ok("self-certification packet (p,p,p): all three role pairs coincide", len(fails) == 3)
    shared = [("id-A", "p1"), ("id-B", "p1"), ("id-A", "p2")]
    ok("shared-principal case: the pair-by-pair rule flags it while the count rule len(principals) < len(identifiers) does not",
       any(a[0] != b[0] and a[1] == b[1] for i, a in enumerate(shared) for b in shared[i + 1:])
       and not (len({s[1] for s in shared}) < len({s[0] for s in shared})))

    same = [("A", "p1"), ("A", "p1"), ("B", "p2")]  # evaluator_also_proposer: identical bindings, a third principal
    ok("evaluator_also_proposer: the count rule misses it too (2 principals, 2 identifiers), the pairwise rule flags it",
       not (len({s[1] for s in same}) < len({s[0] for s in same}))
       and any(a[0] == b[0] for i, a in enumerate(same) for b in same[i + 1:]))

    # --- N3: the countermodel to the wide form of Axis 3 ---
    sigma = {"a": "b", "b": "a"}
    step = {"a": "b", "b": "a"}  # the one transition swaps the two states, so sigma commutes with it
    ok("N3: the renaming sigma commutes with the transition step (hypothesis (i))",
       all(sigma[step[s]] == step[sigma[s]] for s in "ab"))
    charge = {"a": 0, "b": 0}
    ok("N3: the only charge is constant 0 on both states, so it is conserved (hypothesis (ii))",
       all(charge[step[s]] == charge[s] for s in "ab"))

    def verdict(history):
        return history[0] == "a"

    h = ("a",)
    sh = tuple(sigma[s] for s in h)
    ok("N3: V((a)) = True and V(sigma((a))) = V((b)) = False, so V(sigma(H)) != V(H)",
       verdict(h) is True and verdict(sh) is False)

    # --- N4: the unchecked product wrapped to zero ---
    ok("N4: 2^64 assignments wrap to 0 in 64-bit unsigned arithmetic", (2 ** 64) % (2 ** 64) == 0 and 2 ** 64 > 2 ** 20)

    print(f"{len(CHECKED)} checks passed")


if __name__ == "__main__":
    main()
