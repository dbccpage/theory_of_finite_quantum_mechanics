"""Exact rational Gate E check for one default point of the periodic U=t Meron chain.

Evaluates G^{(2)}_{4,1} on the 16-dimensional CAR Fock space. The default call is
L=4, M=1, r=1/10. That receipt records eigenvalue -1/706440, test vector
(-1, -1, -1, -1, +1, +1, +1, +1), and v^T G v = -1/88305. It does not record
a scaling on (0, 1/192].

AuthorityEffect: None.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def compute_gate_e_counterexample(r_rational: sp.Rational = sp.Rational(1, 10)) -> dict[str, object]:
    dim = 16

    def get_bit(s: int, x: int) -> int:
        return (s >> x) & 1

    def set_bit(s: int, x: int, val: int) -> int:
        return (s | (1 << x)) if val else (s & ~(1 << x))

    c = [sp.zeros(dim, dim) for _ in range(4)]
    c_dag = [sp.zeros(dim, dim) for _ in range(4)]
    n = [sp.zeros(dim, dim) for _ in range(4)]

    for x in range(4):
        for s in range(dim):
            nx = get_bit(s, x)
            sign = 1
            for y in range(x):
                if get_bit(s, y) == 1:
                    sign = -sign
            if nx == 1:
                c[x][set_bit(s, x, 0), s] = sign
            if nx == 0:
                c_dag[x][set_bit(s, x, 1), s] = sign
        n[x] = c_dag[x] * c[x]

    a = [((-1) ** x) * (n[x] - sp.Rational(1, 2) * sp.eye(dim)) for x in range(4)]
    P = [sp.zeros(dim, dim) for _ in range(4)]
    for x in range(4):
        y = (x + 1) % 4
        hop = c_dag[x] * c[y] + c_dag[y] * c[x]
        dens = n[x] + n[y] - 2 * (n[x] * n[y])
        P[x] = sp.Rational(1, 2) * (dens + hop)

    r = r_rational
    q = 1 + r
    T0 = (sp.eye(dim) + r * P[0]) * (sp.eye(dim) + r * P[2])
    T1 = (sp.eye(dim) + r * P[1]) * (sp.eye(dim) + r * P[3])
    W = T1 * T0
    X0 = (1 / q) * W.trace()

    dX = [sp.Rational(0)] * 8
    for x in range(4):
        dX[x] = sp.Rational(1, 2) * (1 / q) * (T1 * T0 * a[x]).trace()
        dX[4 + x] = sp.Rational(1, 2) * (1 / q) * (T1 * a[x] * T0).trace()

    d2X = sp.zeros(8, 8)
    for x in range(4):
        for y in range(4):
            d2X[x, y] = sp.Rational(1, 4) * (1 / q) * (T1 * T0 * a[x] * a[y]).trace()
            d2X[4 + x, 4 + y] = sp.Rational(1, 4) * (1 / q) * (T1 * a[x] * a[y] * T0).trace()
            d2X[x, 4 + y] = sp.Rational(1, 4) * (1 / q) * (T1 * a[y] * T0 * a[x]).trace()
            d2X[4 + x, y] = sp.Rational(1, 4) * (1 / q) * (T1 * a[x] * T0 * a[y]).trace()

    G = sp.zeros(8, 8)
    for i in range(8):
        for j in range(8):
            G[i, j] = 4 * (d2X[i, j] / X0 - (dX[i] * dX[j]) / (X0**2))

    lam = sp.Symbol("lam")
    cp = G.charpoly(lam)
    roots = sp.roots(cp)
    multiplicity = sum(int(item) for item in roots.values())
    is_positive_semidefinite = multiplicity == G.rows and all(
        root >= 0 for root in roots
    )

    v = sp.Matrix([-1, -1, -1, -1, 1, 1, 1, 1])
    quad_form = (v.T * G * v)[0, 0]

    return {
        "r": str(r),
        "q": str(q),
        "X0": str(X0),
        "eigenvalues_exact": {str(k): int(v_mult) for k, v_mult in roots.items()},
        "negative_eigenvalue": str(min(roots.keys())),
        "test_vector": [int(x) for x in v],
        "quadratic_form_exact": str(quad_form),
        "quadratic_form_float": float(quad_form),
        "is_positive_semidefinite": bool(is_positive_semidefinite),
    }


def main() -> int:
    print("Running exact rational Gate E counterexample for r = 1/10...")
    result = compute_gate_e_counterexample(sp.Rational(1, 10))
    print(json.dumps(result, indent=2))

    out_file = Path(__file__).parent / "gate_e_exact_counterexample_receipt.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Saved receipt to {out_file}")
    return 0


if __name__ == "__main__":
    main()
