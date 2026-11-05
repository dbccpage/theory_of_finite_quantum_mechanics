"""Trotter cochain response matrices and characteristic polynomials; AuthorityEffect: None.

This module constructs exact rational response matrices G^{(2)}_{4,M} for the
L=4 staggered Trotter cochain formulation, extracts the exact roots of their
characteristic polynomials for M in {1, 2, 3}, evaluates the exact closed-form
staggered Rayleigh quotients for M=1 and M=2, and tests whether the zero-mode
dimension obeys dim ker G^{(2)}_{4,M} = 4M - 1 up to M=4.

Scope boundaries:
- Evaluated on finite CAR Fock space of dimension 2^4 = 16.
- Physical continuum claims are not asserted from this finite model.
"""

from typing import Any

import sympy as sp
from fractions import Fraction


def exact_rational(value):
    if type(value) not in (int, Fraction) and not isinstance(value, sp.Rational):
        raise ValueError("an exact rational coupling is required")
    return sp.Rational(value)



def _exact_expression(value):
    if isinstance(value, sp.Expr) and value.is_commutative and not value.has(sp.Float):
        return value
    return exact_rational(value)


def get_fock_car_operators() -> tuple[int, list[sp.Matrix], list[sp.Matrix], list[sp.Matrix], list[sp.Matrix], list[sp.Matrix]]:
    """Construct standard fermionic CAR creation, annihilation, and density operators on L=4."""
    dim = 16

    def get_bit(s: int, x: int) -> int:
        return (s >> x) & 1

    def set_bit(s: int, x: int, val: int) -> int:
        return (s | (1 << x)) if val else (s & ~(1 << x))

    c: list[sp.Matrix] = [sp.zeros(dim, dim) for _ in range(4)]
    c_dag: list[sp.Matrix] = [sp.zeros(dim, dim) for _ in range(4)]
    n: list[sp.Matrix] = [sp.zeros(dim, dim) for _ in range(4)]

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

    a: list[sp.Matrix] = [((-1) ** x) * (n[x] - sp.Rational(1, 2) * sp.eye(dim)) for x in range(4)]
    P: list[sp.Matrix] = [sp.zeros(dim, dim) for _ in range(4)]
    for x in range(4):
        y = (x + 1) % 4
        hop = c_dag[x] * c[y] + c_dag[y] * c[x]
        dens = n[x] + n[y] - 2 * (n[x] * n[y])
        P[x] = sp.Rational(1, 2) * (dens + hop)

    return dim, c, c_dag, n, a, P


def closed_form_lambda_stag_m1(r: Any) -> Any:
    """Exact closed rational form for lambda_stag(r, M=1).

    Formula: -r^4 / [ 4 * (r + 2) * (r^2 + 4r + 8) ]
    """
    r = _exact_expression(r)
    if r == -2:
        raise ValueError("singular rational expression")
    return - (r ** 4) / (4 * (r + 2) * (r ** 2 + 4 * r + 8))


def closed_form_lambda_stag_m2(r: Any) -> Any:
    """Exact closed rational form for lambda_stag(r, M=2).

    Formula: -r^4 * (r^3 + 8r^2 + 32r + 32) / [ 4 * (r^6 + 16r^5 + 128r^4 + 512r^3 + 1280r^2 + 2048r + 2048) ]
    """
    r = _exact_expression(r)
    num = (r ** 4) * (r ** 3 + 8 * r ** 2 + 32 * r + 32)
    den = 4 * (r ** 6 + 16 * r ** 5 + 128 * r ** 4 + 512 * r ** 3 + 1280 * r ** 2 + 2048 * r + 2048)
    if den == 0:
        raise ValueError("singular rational expression")
    return - num / den


def compute_exact_response_matrix(M: int, r_rat: sp.Rational) -> dict[str, Any]:
    """Compute the exact rational G^{(2)}_{4,M} matrix, eigenvalues, and zero-mode count.

    Parameters:
        M: Number of Trotter step repetitions (temporal dimension 2M).
        r_rat: Exact rational coupling r.

    Returns:
        Dictionary containing dimension, partition trace X0, eigenvalues,
        zero-mode count, negative eigenvalues, and staggered Rayleigh quotient.
    """
    if type(M) is not int or M < 1:
        raise ValueError("M must be a positive integer")
    r_rat = exact_rational(r_rat)
    if r_rat == -M:
        raise ValueError("singular Trotter normalization")
    dim, _, _, _, a, P = get_fock_car_operators()
    r_M = r_rat / M
    q = 1 + r_M

    # Two alternating layer transfer operators
    T0 = (sp.eye(dim) + r_M * P[0]) * (sp.eye(dim) + r_M * P[2])
    T1 = (sp.eye(dim) + r_M * P[1]) * (sp.eye(dim) + r_M * P[3])

    T: list[sp.Matrix] = []
    for _ in range(M):
        T.append(T0)
        T.append(T1)

    K = 2 * M
    total_sources = K * 4
    norm_factor = q ** (-M)

    # Base partition trace
    W0 = sp.eye(dim)
    for j in range(K - 1, -1, -1):
        W0 = W0 * T[j]
    X0 = norm_factor * W0.trace()
    if X0 == 0:
        raise ValueError("zero partition trace")

    # First derivatives
    dX = [sp.Rational(0)] * total_sources
    for j in range(K):
        for x in range(4):
            idx = j * 4 + x
            prod = sp.eye(dim)
            for k in range(K - 1, -1, -1):
                prod = prod * T[k]
                if k == j:
                    prod = prod * (a[x] / (2 * M))
            dX[idx] = norm_factor * prod.trace()

    # Second derivatives
    d2X = sp.zeros(total_sources, total_sources)
    for j1 in range(K):
        for x1 in range(4):
            idx1 = j1 * 4 + x1
            for j2 in range(K):
                for x2 in range(4):
                    idx2 = j2 * 4 + x2
                    prod = sp.eye(dim)
                    for k in range(K - 1, -1, -1):
                        prod = prod * T[k]
                        if k == j1 and k == j2:
                            prod = prod * (a[x1] * a[x2] / (4 * M ** 2))
                        elif k == j1:
                            prod = prod * (a[x1] / (2 * M))
                        elif k == j2:
                            prod = prod * (a[x2] / (2 * M))
                    d2X[idx1, idx2] = norm_factor * prod.trace()

    d2X = sp.Rational(1, 2) * (d2X + d2X.T)

    # G = (2M)^2 * [ d2X / X0 - (dX * dX^T) / X0^2 ]
    G = sp.zeros(total_sources, total_sources)
    for i in range(total_sources):
        for j in range(total_sources):
            G[i, j] = (2 * M) ** 2 * (d2X[i, j] / X0 - (dX[i] * dX[j]) / (X0 ** 2))

    # Characteristic polynomial roots
    lam = sp.Symbol('lam')
    cp = G.charpoly(lam)
    roots = sp.roots(cp)

    if sum(roots.values()) != total_sources:
        raise ValueError("unresolved spectrum: symbolic roots are incomplete")
    if any(root.is_negative is None for root in roots):
        raise ValueError("unresolved spectrum: an eigenvalue sign is undecided")
    eigenvalues_dict = {str(k): int(v_mult) for k, v_mult in roots.items()}
    zero_mode_count = eigenvalues_dict.get('0', 0)
    negative_eigs = [k for k in roots if k.is_negative]

    # Staggered Rayleigh quotient
    v = sp.Matrix([(-1) ** (idx // 4) for idx in range(total_sources)])
    v_norm_sq = (v.T * v)[0, 0]
    quad_form = (v.T * G * v)[0, 0]
    rayleigh = quad_form / v_norm_sq

    return {
        'M': M,
        'r': str(r_rat),
        'X0': str(X0),
        'dim_G': total_sources,
        'eigenvalues': eigenvalues_dict,
        'zero_modes': zero_mode_count,
        'negative_eigenvalues': [str(k) for k in negative_eigs],
        'negative_count': sum(int(roots[k]) for k in negative_eigs),
        'v_norm_sq': int(v_norm_sq),
        'quad_form_stag': str(quad_form),
        'rayleigh_stag': str(rayleigh),
        'matrix': G,
    }
