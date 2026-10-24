"""Independent check for PGW-SN-E08-WEIGHTED-L1-DUALITY.

AuthorityEffect: None.

Run: python -I -X utf8 checks/independent/pgw-sn-e08-weighted-l1-duality.py

This script imports no repository code. For seeded random rational instances (graph
coboundaries and dense random matrices, positive rational weights) it solves, with SymPy's exact
rational simplex (sympy.solvers.simplex), both

  primal: min_x sum_e w_e |h_e - (D x)_e|   (as an LP with slack t_e >= +/-(h_e - (D x)_e))
  dual:   max_y sum_e y_e h_e  s.t.  D^T y = 0,  -w_e <= y_e <= w_e

and checks that the optimal values agree exactly, that the returned optimisers are rational and
feasible, that weak duality holds on random feasible points, and that two altered dual problems
(halved bounds, dropped annihilation) change the value on some instance. It also recomputes the
oriented 3-cycle instance. It exits 0 when every check passes and prints what it checked.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction

from sympy import Rational, symbols
from sympy.solvers.simplex import lpmax, lpmin

FAILURES: list[str] = []
COUNTS: dict[str, int] = {}


def check(name: str, ok: bool) -> None:
    COUNTS[name] = COUNTS.get(name, 0) + 1
    if not ok:
        FAILURES.append(name)


def cost(D, w, h, x):
    return sum(w[e] * abs(h[e] - sum(D[e][v] * x[v] for v in range(len(x)))) for e in range(len(h)))


def solve_primal(D, w, h):
    nE, nV = len(D), len(D[0])
    xs = symbols(f"x0:{nV}")
    ts = symbols(f"t0:{nE}")
    cons = []
    for e in range(nE):
        r = Rational(h[e]) - sum(Rational(D[e][v]) * xs[v] for v in range(nV))
        cons += [ts[e] >= r, ts[e] >= -r, ts[e] >= 0]
    val, sol = lpmin(sum(Rational(w[e]) * ts[e] for e in range(nE)), cons)
    x = [Fraction(str(sol.get(s, 0))) for s in xs]
    return Fraction(str(val)), x


def solve_dual(D, w, h, bound_scale=Fraction(1), annihilate=True):
    nE, nV = len(D), len(D[0])
    ys = symbols(f"y0:{nE}")
    cons = []
    for e in range(nE):
        b = Rational(w[e] * bound_scale)
        cons += [ys[e] <= b, ys[e] >= -b]
    if annihilate:
        for v in range(nV):
            cons.append(sum(Rational(D[e][v]) * ys[e] for e in range(nE)) <= 0)
            cons.append(sum(Rational(D[e][v]) * ys[e] for e in range(nE)) >= 0)
    val, sol = lpmax(sum(Rational(h[e]) * ys[e] for e in range(nE)), cons)
    y = [Fraction(str(sol.get(s, 0))) for s in ys]
    return Fraction(str(val)), y


def feasible(D, w, y):
    nE, nV = len(D), len(D[0])
    return all(sum(y[e] * D[e][v] for e in range(nE)) == 0 for v in range(nV)) and all(
        abs(y[e]) <= w[e] for e in range(nE))


def rand_q(rng, lo=-5, hi=5, den=4):
    return Fraction(rng.randint(lo * den, hi * den), rng.randint(1, den))


def graph_instance(rng):
    nV = rng.randint(2, 5)
    edges = set()
    target = rng.randint(1, nV * (nV - 1) // 2)
    while len(edges) < target:
        a, b = rng.sample(range(nV), 2)
        if (a, b) not in edges and (b, a) not in edges:
            edges.add((a, b))
    D = []
    for (a, b) in sorted(edges):
        row = [Fraction(0)] * nV
        row[a] -= 1
        row[b] += 1
        D.append(row)
    return D


def dense_instance(rng):
    nV, nE = rng.randint(1, 3), rng.randint(1, 5)
    return [[rand_q(rng, -3, 3, 3) for _ in range(nV)] for _ in range(nE)]


def main() -> int:
    rng = random.Random(522)
    changed_half = changed_free = 0
    for trial in range(60):
        D = graph_instance(rng) if trial % 2 == 0 else dense_instance(rng)
        nE = len(D)
        w = [Fraction(rng.randint(1, 12), rng.randint(1, 4)) for _ in range(nE)]
        h = [rand_q(rng) for _ in range(nE)]
        p, x = solve_primal(D, w, h)
        d, y = solve_dual(D, w, h)
        check("strong duality: primal optimum == dual optimum (exact)", p == d)
        check("primal optimiser is rational and attains the value", cost(D, w, h, x) == p)
        check("dual optimiser is rational and feasible", feasible(D, w, y))
        check("dual optimiser attains the value", sum(y[e] * h[e] for e in range(nE)) == d)
        for _ in range(5):
            xr = [rand_q(rng) for _ in range(len(D[0]))]
            check("weak duality: dual optimum <= cost(random x)", d <= cost(D, w, h, xr))
            s = Fraction(rng.randint(0, 10), 10)
            check("scaled dual optimum stays feasible with value <= optimum",
                  feasible(D, w, [s * t for t in y]) and s * d <= p)
        dh, _ = solve_dual(D, w, h, bound_scale=Fraction(1, 2))
        check("halved bounds never exceed the optimum", dh <= d)
        changed_half += dh != d
        df, _ = solve_dual(D, w, h, annihilate=False)
        check("dropping D^T y = 0 never lowers the value", df >= d)
        changed_free += df != d
    check("negative control: halved bounds change the value on some instance", changed_half > 0)
    check("negative control: dropping annihilation changes the value on some instance", changed_free > 0)

    # Oriented 3-cycle, edges 0->1, 1->2, 2->0, unit weights, defect (1, 0, 0).
    D = [[-1, 1, 0], [0, -1, 1], [1, 0, -1]]
    D = [[Fraction(a) for a in row] for row in D]
    w = [Fraction(1)] * 3
    h = [Fraction(1), Fraction(0), Fraction(0)]
    p, _ = solve_primal(D, w, h)
    check("3-cycle optimum is 1", p == 1)
    y = [Fraction(1)] * 3
    check("3-cycle dual (1,1,1) feasible with value 1", feasible(D, w, y) and sum(y[e] * h[e] for e in range(3)) == 1)
    xs = {"x1": [0, 0, 0], "x2": [0, 1, 0], "x3": [0, Fraction(2, 3), Fraction(1, 3)]}
    res = {}
    for k, x in xs.items():
        x = [Fraction(t) for t in x]
        check(f"3-cycle cost({k}) = 1", cost(D, w, h, x) == 1)
        res[k] = [h[e] - sum(D[e][v] * x[v] for v in range(3)) for e in range(3)]
    check("3-cycle residuals (1,0,0) and (0,1,0) differ", res["x1"] == [1, 0, 0] and res["x2"] == [0, 1, 0])
    check("3-cycle harmonic residual (1/3,1/3,1/3) has D^T r = 0",
          res["x3"] == [Fraction(1, 3)] * 3 and all(sum(res["x3"][e] * D[e][v] for e in range(3)) == 0 for v in range(3)))
    check("3-cycle residual (1,0,0) is not harmonic", sum(res["x1"][e] * D[e][0] for e in range(3)) != 0)

    for name in sorted(COUNTS):
        print(f"{COUNTS[name]:5d}  {name}")
    print(f"checks={sum(COUNTS.values())} distinct={len(COUNTS)} failures={len(FAILURES)} "
          f"halved_changed={changed_half} free_changed={changed_free}")
    if FAILURES:
        for name in sorted(set(FAILURES)):
            print("FAILED:", name)
        return 1
    print("OK: weighted l1 strong duality, rational optimisers on these instances, weak duality and the "
          "3-cycle instance recomputed independently.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
