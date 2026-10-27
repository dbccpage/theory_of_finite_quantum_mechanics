"""Exhaustive checks of the small propositions in papers/complexity/p_vs_np_and_eth_from_genesis.md.

Standard library only, exact integer arithmetic, fixed seeds. Each check prints one line and
the script exits 1 if any check fails. These are checks on finite instances, not proofs.

Usage (from the repository root):
    python -I papers/complexity/checks/complexity_checks.py
"""

from __future__ import annotations

import itertools
import random
import sys

Edge = tuple[int, int]


def random_graph(rng: random.Random, n: int, p: float) -> list[Edge]:
    return [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]


# --- Section 3: tags and colourings ----------------------------------------------------------


def tag_exists(n: int, conflicts: list[Edge], bits: int) -> bool:
    """Is there t : V -> {0,1}^bits with t(u) != t(v) on every conflicting pair?"""
    return any(all(t[u] != t[v] for u, v in conflicts) for t in itertools.product(range(2**bits), repeat=n))


def chromatic_number(n: int, edges: list[Edge]) -> int:
    for k in range(1, n + 1):
        if any(all(c[u] != c[v] for u, v in edges) for c in itertools.product(range(k), repeat=n)):
            return k
    return n


def bipartite(n: int, edges: list[Edge]) -> bool:
    """Breadth-first two-colouring: the polynomial-time test for one-bit tags."""
    colour: dict[int, int] = {}
    adj: dict[int, list[int]] = {v: [] for v in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    for s in range(n):
        if s in colour:
            continue
        colour[s], queue = 0, [s]
        while queue:
            u = queue.pop()
            for v in adj[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]
                    queue.append(v)
                elif colour[v] == colour[u]:
                    return False
    return True


def check_tags(rng: random.Random) -> bool:
    for _ in range(150):
        n = rng.randint(1, 6)
        e = random_graph(rng, n, rng.random())
        chi = chromatic_number(n, e)
        if tag_exists(n, e, 1) != (chi <= 2) or tag_exists(n, e, 1) != bipartite(n, e):
            return False
        if tag_exists(n, e, 2) != (chi <= 4):
            return False
    return True


# --- Section 4: the sign, switching and the frustration index --------------------------------


def frustration_index(n: int, edges: list[Edge], neg: list[int]) -> int:
    """Phi_1 over F_2 with unit weights: min over switchings s of the number of negative edges."""
    return min(sum((x + s[u] + s[v]) % 2 for (u, v), x in zip(edges, neg)) for s in itertools.product((0, 1), repeat=n))


def max_cut(n: int, edges: list[Edge]) -> int:
    return max(sum(s[u] != s[v] for u, v in edges) for s in itertools.product((0, 1), repeat=n))


def check_frustration_maxcut(rng: random.Random) -> bool:
    for _ in range(200):
        n = rng.randint(1, 7)
        e = random_graph(rng, n, rng.random())
        if frustration_index(n, e, [1] * len(e)) != len(e) - max_cut(n, e):
            return False
    return True


def check_balance_by_chords(rng: random.Random) -> bool:
    """A signing switches to all-positive iff every fundamental cycle of a spanning forest is positive."""
    for _ in range(200):
        n = rng.randint(1, 7)
        e = random_graph(rng, n, rng.random())
        neg = [rng.randint(0, 1) for _ in e]
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                x = parent[x]
            return x

        # Spanning forest by union-find; potentials along the forest; chord parities decide.
        forest: dict[int, list[tuple[int, int]]] = {v: [] for v in range(n)}
        chords: list[int] = []
        for i, (u, v) in enumerate(e):
            ru, rv = find(u), find(v)
            if ru == rv:
                chords.append(i)
            else:
                parent[ru] = rv
                forest[u].append((v, neg[i]))
                forest[v].append((u, neg[i]))
        pot: dict[int, int] = {}
        for s in range(n):
            if s in pot:
                continue
            pot[s], stack = 0, [s]
            while stack:
                u = stack.pop()
                for v, x in forest[u]:
                    if v not in pot:
                        pot[v] = (pot[u] + x) % 2
                        stack.append(v)
        by_chords = all((neg[i] + pot[e[i][0]] + pot[e[i][1]]) % 2 == 0 for i in chords)
        if by_chords != (frustration_index(n, e, neg) == 0):
            return False
    return True


def integer_phi1_and_dual(n: int, edges: list[Edge], c: list[int], box: int = 3) -> tuple[int, int]:
    """Unit-weight Phi_1 over Z by search over integer potentials in a box, and the best integer
    dual circulation y in {-1,0,1}^E. Weak duality gives dual <= LP value <= primal; equality pins
    the rational optimum to the integer one on this instance."""
    vs = range(-box, box + 1)
    primal = min(sum(abs(ce - (g[v] - g[u])) for (u, v), ce in zip(edges, c)) for g in itertools.product(vs, repeat=n))
    dual = -(10**9)
    for y in itertools.product((-1, 0, 1), repeat=len(edges)):
        flow = [0] * n
        for (u, v), ye in zip(edges, y):
            flow[u] -= ye
            flow[v] += ye
        if all(f == 0 for f in flow):
            dual = max(dual, sum(ye * ce for ye, ce in zip(y, c)))
    return primal, dual


def check_integer_phi1_is_lp(rng: random.Random) -> bool:
    for _ in range(60):
        n = rng.randint(2, 5)
        e = random_graph(rng, n, 0.8)
        if not e or len(e) > 8:
            continue
        c = [rng.randint(-2, 2) for _ in e]
        primal, dual = integer_phi1_and_dual(n, e, c)
        if primal != dual:
            return False
    return True


# --- Section 5: signed sums of F_2 polynomials as model counts --------------------------------

Monomial = tuple[int, ...]


def sign_sum(n: int, monos: list[Monomial]) -> int:
    return sum((-1) ** (sum(all(x[i] for i in m) for m in monos) % 2) for x in itertools.product((0, 1), repeat=n))


def cnf_for_zero_set(n: int, monos: list[Monomial]) -> tuple[int, list[list[int]]]:
    """Parsimonious CNF (literals are +-(index+1)) whose models are in bijection with {x : p(x) = 0}.
    Variables: x_0..x_{n-1}, then y_j (= monomial j) and z_j (= y_0 xor ... xor y_j)."""
    clauses: list[list[int]] = []
    y = [n + j + 1 for j in range(len(monos))]
    z = [n + len(monos) + j + 1 for j in range(len(monos))]
    for j, m in enumerate(monos):
        lits = [i + 1 for i in m]
        clauses += [[-y[j], a] for a in lits]
        clauses.append([y[j]] + [-a for a in lits])
    for j in range(len(monos)):
        if j == 0:
            clauses += [[-z[0], y[0]], [z[0], -y[0]]]
        else:
            a, b, out = z[j - 1], y[j], z[j]
            clauses += [[-out, a, b], [-out, -a, -b], [out, -a, b], [out, a, -b]]
    if monos:
        clauses.append([-z[-1]])
    return n + 2 * len(monos), clauses


def count_models(nvars: int, clauses: list[list[int]]) -> int:
    def sat(a: tuple[int, ...]) -> bool:
        return all(any((a[abs(l) - 1] == 1) == (l > 0) for l in cl) for cl in clauses)

    return sum(sat(a) for a in itertools.product((0, 1), repeat=nvars))


def check_sign_sum_reduction(rng: random.Random) -> bool:
    for _ in range(80):
        n = rng.randint(1, 4)
        k = rng.randint(0, 3)
        monos = [tuple(sorted(rng.sample(range(n), rng.randint(1, min(3, n))))) for _ in range(k)]
        nvars, clauses = cnf_for_zero_set(n, monos)
        if max((len(cl) for cl in clauses), default=0) > 4:
            return False
        if sign_sum(n, monos) != 2 * count_models(nvars, clauses) - 2**n:
            return False
    return True


# --- Section 4: one-dimensional characters of S_n ---------------------------------------------


def check_sn_characters() -> bool:
    """For n = 2..5 the commutator subgroup of S_n is the alternating group, of index 2, so S_n has
    exactly two homomorphisms to an abelian group of order 2 or to C^*: the trivial one and the sign."""

    def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(p[q[i]] for i in range(len(q)))

    def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
        inv = [0] * len(p)
        for i, pi in enumerate(p):
            inv[pi] = i
        return tuple(inv)

    def parity(p: tuple[int, ...]) -> int:
        return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2

    for n in range(2, 6):
        group = list(itertools.permutations(range(n)))
        sub = {compose(compose(a, b), compose(inverse(a), inverse(b))) for a in group for b in group}
        while True:
            closed = sub | {compose(a, b) for a in sub for b in sub}
            if closed == sub:
                break
            sub = closed
        if sub != {p for p in group if parity(p) == 0}:
            return False
    return True


def main() -> int:
    rng = random.Random(20261027)
    checks = [
        ("one-bit tag iff bipartite, two-bit tag iff 4-colourable", lambda: check_tags(rng)),
        ("frustration index of the all-negative signing = |E| - maxcut", lambda: check_frustration_maxcut(rng)),
        ("balance decided by chord parities of a spanning forest", lambda: check_balance_by_chords(rng)),
        ("integer Phi_1 on graphs equals an integer dual certificate", lambda: check_integer_phi1_is_lp(rng)),
        ("sum (-1)^p(x) = 2 #models - 2^n for the width-4 CNF", lambda: check_sign_sum_reduction(rng)),
        ("commutator subgroup of S_n is A_n (n = 2..5)", check_sn_characters),
    ]
    ok = True
    for name, fn in checks:
        res = fn()
        ok &= res
        print(("PASS " if res else "FAIL ") + name)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
