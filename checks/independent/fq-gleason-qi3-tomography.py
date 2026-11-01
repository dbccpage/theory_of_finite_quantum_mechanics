"""Exact symbolic and arithmetic controls for the nine-ray Q(i)^3 reduction and 3-adic residual.

No repository code is imported. This checks reconstruction signs, uniqueness,
quadratic expansion, a generic matrix inverse identity used in the paper
proof, the rational rescaling bounds, and the global bounded zero-weight
3-adic residual frame function s3 (plus exoticQi3 = (1 + s3) / 3).
"""

from __future__ import annotations

from fractions import Fraction
import json

import sympy as sp


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def zero(expression: sp.Expr) -> bool:
    return sp.expand(expression) == 0


def v3_int(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 0
    k = 0
    while n % 3 == 0:
        n //= 3
        k += 1
    return k


def p3_part_int(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 0
    while n % 3 == 0:
        n //= 3
    return n


def v3_rat(q: Fraction) -> int:
    if q <= 0:
        return 0
    return v3_int(q.numerator) - v3_int(q.denominator)


def u3_rat(q: Fraction) -> Fraction:
    if q <= 0:
        return Fraction(0)
    rem = (p3_part_int(q.numerator) * p3_part_int(q.denominator)) % 3
    return Fraction(1) if rem == 1 else Fraction(-1)


def is_lead3_coord(c_norm: Fraction, vec_norm: Fraction) -> bool:
    return c_norm > 0 and v3_rat(c_norm) < v3_rat(vec_norm)


def coord_sign3(c_norm: Fraction, vec_norm: Fraction) -> Fraction:
    return u3_rat(c_norm) * u3_rat(vec_norm)


GVec = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction], tuple[Fraction, Fraction]]


def g_norm_sq(z: tuple[Fraction, Fraction]) -> Fraction:
    return z[0] * z[0] + z[1] * z[1]


def vec_norm_sq(u: GVec) -> Fraction:
    return g_norm_sq(u[0]) + g_norm_sq(u[1]) + g_norm_sq(u[2])


def g_inner(u: GVec, v: GVec) -> tuple[Fraction, Fraction]:
    re = sum(a[0] * b[0] + a[1] * b[1] for a, b in zip(u, v))
    im = sum(a[0] * b[1] - a[1] * b[0] for a, b in zip(u, v))
    return (re, im)


def herm_cross(u: GVec, v: GVec) -> GVec:
    def g_mul(a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    def g_sub(a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        return (a[0] - b[0], a[1] - b[1])

    def g_conj(a: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        return (a[0], -a[1])

    return (
        g_conj(g_sub(g_mul(u[1], v[2]), g_mul(u[2], v[1]))),
        g_conj(g_sub(g_mul(u[2], v[0]), g_mul(u[0], v[2]))),
        g_conj(g_sub(g_mul(u[0], v[1]), g_mul(u[1], v[0]))),
    )


def s3(u: GVec) -> Fraction:
    vn = vec_norm_sq(u)
    if v3_rat(vn) % 2 == 0:
        return Fraction(0)
    if is_lead3_coord(g_norm_sq(u[0]), vn):
        return coord_sign3(g_norm_sq(u[0]), vn)
    if is_lead3_coord(g_norm_sq(u[1]), vn):
        return coord_sign3(g_norm_sq(u[1]), vn)
    return coord_sign3(g_norm_sq(u[2]), vn)


def exotic_qi3(u: GVec) -> Fraction:
    return (Fraction(1) + s3(u)) / 3


def gv_int(a: int, b: int, c: int, d: int, e: int, g: int) -> GVec:
    return (
        (Fraction(a), Fraction(b)),
        (Fraction(c), Fraction(d)),
        (Fraction(e), Fraction(g)),
    )


def is_one_plus_i_primitive_gvec(u: GVec) -> bool:
    a, b = int(u[0][0]), int(u[0][1])
    c, d = int(u[1][0]), int(u[1][1])
    e, g = int(u[2][0]), int(u[2][1])
    return not ((a + b) % 2 == 0 and (c + d) % 2 == 0 and (e + g) % 2 == 0)


def vp_int(n: int, p: int) -> int:
    n = abs(n)
    if n == 0 or p < 2:
        return 0
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def pp_part_int(n: int, p: int) -> int:
    n = abs(n)
    if n == 0 or p < 2:
        return n
    while n % p == 0:
        n //= p
    return n


def vp_rat(q: Fraction, p: int) -> int:
    if q <= 0:
        return 0
    return vp_int(q.numerator, p) - vp_int(q.denominator, p)


def up_rat_legendre(q: Fraction, p: int) -> Fraction:
    """Legendre symbol (p'-part(q) / p) in {-1, +1} for inert prime p == 3 (mod 4)."""
    if q <= 0:
        return Fraction(0)
    rem = (pp_part_int(q.numerator, p) * pp_part_int(q.denominator, p)) % p
    return Fraction(1) if pow(rem, (p - 1) // 2, p) == 1 else Fraction(-1)


def sp_residual(u: GVec, p: int) -> Fraction:
    vn = vec_norm_sq(u)
    if vp_rat(vn, p) % 2 == 0:
        return Fraction(0)
    nx = g_norm_sq(u[0])
    if nx > 0 and vp_rat(nx, p) < vp_rat(vn, p):
        return up_rat_legendre(nx, p) * up_rat_legendre(vn, p)
    ny = g_norm_sq(u[1])
    if ny > 0 and vp_rat(ny, p) < vp_rat(vn, p):
        return up_rat_legendre(ny, p) * up_rat_legendre(vn, p)
    nz = g_norm_sq(u[2])
    return up_rat_legendre(nz, p) * up_rat_legendre(vn, p)


def main() -> None:
    diagonal = sp.symbols("d0:3", real=True)
    real_part = sp.symbols("a01 a02 a12", real=True)
    imag_part = sp.symbols("b01 b02 b12", real=True)
    pairs = [(0, 1), (0, 2), (1, 2)]
    rho = sp.diag(*diagonal)
    for pair, a, b in zip(pairs, real_part, imag_part):
        j, k = pair
        rho[j, k] = a + sp.I * b
        rho[k, j] = a - sp.I * b
    require(rho == rho.conjugate().T, "candidate is Hermitian")

    basis = [sp.eye(3)[:, j] for j in range(3)]
    rays = basis[:]
    for j, k in pairs:
        rays.extend([basis[j] + basis[k], basis[j] + sp.I * basis[k]])
    values = [sp.expand((v.conjugate().T * rho * v)[0]
                        / (v.conjugate().T * v)[0]) for v in rays]
    expected = list(diagonal)
    for (j, k), a, b in zip(pairs, real_part, imag_part):
        expected.extend([(diagonal[j] + diagonal[k]) / 2 + a,
                         (diagonal[j] + diagonal[k]) / 2 - b])
    require(all(zero(x - y) for x, y in zip(values, expected)),
            "all nine evaluations, including imaginary signs")
    coefficients = list(diagonal) + list(real_part) + list(imag_part)
    tomography = sp.Matrix(values).jacobian(coefficients)
    require(tomography.det() != 0, "tomography has exact rank nine")

    measurements = sp.symbols("m0:9", real=True)
    reconstructed = list(measurements[:3])
    reconstructed_real = []
    reconstructed_imag = []
    for index, (j, k) in enumerate(pairs):
        mean = (measurements[j] + measurements[k]) / 2
        reconstructed_real.append(measurements[3 + 2 * index] - mean)
        reconstructed_imag.append(mean - measurements[4 + 2 * index])
    substitution = dict(zip(coefficients,
                            reconstructed + reconstructed_real + reconstructed_imag))
    require(all(zero(value.subs(substitution) - measurement)
                for value, measurement in zip(values, measurements)),
            "candidate recovers arbitrary rational measurements")

    x = sp.symbols("x0:3", real=True)
    y = sp.symbols("y0:3", real=True)
    v = sp.Matrix([a + sp.I * b for a, b in zip(x, y)])
    numerator = sp.expand((v.conjugate().T * rho * v)[0])
    expansion = sum(diagonal[j] * (x[j] ** 2 + y[j] ** 2) for j in range(3))
    for (j, k), a, b in zip(pairs, real_part, imag_part):
        expansion += 2 * a * (x[j] * x[k] + y[j] * y[k])
        expansion -= 2 * b * (x[j] * y[k] - y[j] * x[k])
    require(zero(numerator - expansion), "generic quadratic expansion")
    require(zero(sp.im(numerator)), "quadratic numerator is rational over Q(i)")

    # Polynomial identity underlying U D^(-1) U* = I when U*U=D.
    # The premise U*U=D and the nonzero determinant are proved in the note;
    # this calculation does not assert those premises for arbitrary matrices.
    entries = sp.symbols("u0:9")
    matrix = sp.Matrix(3, 3, entries)
    identity_residual = matrix * matrix.adjugate() - matrix.det() * sp.eye(3)
    require(all(zero(entry) for entry in identity_residual),
            "generic three by three adjugate identity")

    bound = sp.symbols("B", nonnegative=True)
    epsilon = 1 / (3 * (bound + 1))
    require(sp.cancel(sp.Rational(1, 3) - epsilon * bound - epsilon) == 0,
            "rescaled lower bound")
    require(sp.cancel(sp.Rational(1, 3) + epsilon * bound
                      - (2 * bound + 1) / (3 * (bound + 1))) == 0,
            "rescaled upper bound")
    require(sp.cancel(sp.Rational(2, 3)
                      - (2 * bound + 1) / (3 * (bound + 1)) - epsilon) == 0,
            "upper bound is strictly below two thirds")
    require(epsilon.is_positive is True, "rescaling is positive, including B=0")
    require(epsilon.subs(bound, 0) == sp.Rational(1, 3), "zero-bound control")

    # A wrong sign on an imaginary off-diagonal must fail the same evaluation.
    require(not zero(values[4] - ((diagonal[0] + diagonal[1]) / 2 + imag_part[0])),
            "negative control rejects reversed imaginary sign")

    # Section 5 constructive 7-ray projector kernel relation on (1, 1, 1):
    v111_sp = sp.Matrix([1, 1, 1])
    q_111 = sp.expand((v111_sp.conjugate().T * rho * v111_sp)[0] / 3)
    kernel_comb = (
        q_111
        + sp.Rational(1, 3) * (values[0] + values[1] + values[2])
        - sp.Rational(2, 3) * (values[3] + values[5] + values[7])
    )
    require(zero(kernel_comb),
            "7-ray projector kernel relation vanishes identically for every HermForm3")

    # Section 9D constructive 9-ray projector kernel relation on witness_p7 = (1, 2, 1 + i):
    vp7_sp = sp.Matrix([1, 2, 1 + sp.I])
    q_p7 = sp.expand((vp7_sp.conjugate().T * rho * vp7_sp)[0] / 7)
    kernel_comb_p7 = (
        q_p7
        + sp.Rational(3, 7) * values[0]
        + sp.Rational(2, 7) * values[1]
        + sp.Rational(4, 7) * values[2]
        - sp.Rational(4, 7) * values[3]
        - sp.Rational(2, 7) * values[5]
        - sp.Rational(4, 7) * values[7]
        - sp.Rational(2, 7) * values[6]
        - sp.Rational(4, 7) * values[8]
    )
    require(zero(kernel_comb_p7),
            "9-ray projector kernel relation for witness_p7 vanishes identically for every HermForm3")

    # Section 8: Global bounded zero-weight 3-adic residual s3 and exotic_qi3.
    nine_rays_gvec = [
        gv_int(1, 0, 0, 0, 0, 0),
        gv_int(0, 0, 1, 0, 0, 0),
        gv_int(0, 0, 0, 0, 1, 0),
        gv_int(1, 0, 1, 0, 0, 0),
        gv_int(1, 0, 0, 0, 1, 0),
        gv_int(0, 0, 1, 0, 1, 0),
        gv_int(1, 0, 0, 1, 0, 0),
        gv_int(1, 0, 0, 0, 0, 1),
        gv_int(0, 0, 1, 0, 0, 1),
    ]
    require(all(s3(r) == 0 for r in nine_rays_gvec), "s3 vanishes on all nine tomography rays")
    require(all(exotic_qi3(r) == Fraction(1, 3) for r in nine_rays_gvec),
            "exotic_qi3 equals 1/3 on all nine tomography rays")

    witness_111 = gv_int(1, 0, 1, 0, 1, 0)
    witness_div4 = gv_int(1, 2, 1, 2, 1, 1)
    witness_div8 = gv_int(1, 4, 1, 2, 1, 1)
    require(
        is_one_plus_i_primitive_gvec(witness_111)
        and vec_norm_sq(witness_111) == 3
        and s3(witness_111) == 1,
        "s3(1, 1, 1) == 1 on (1+i)-primitive norm-3 witness",
    )
    require(
        is_one_plus_i_primitive_gvec(witness_div4)
        and vec_norm_sq(witness_div4) == 12
        and s3(witness_div4) == -1,
        "s3 == -1 on (1+i)-primitive norm-12 (4|N) witness",
    )
    require(
        is_one_plus_i_primitive_gvec(witness_div8)
        and vec_norm_sq(witness_div8) == 24
        and s3(witness_div8) == 1,
        "s3 == 1 on (1+i)-primitive norm-24 (8|N) witness",
    )

    # Constructive separation of the 7-ray projector kernel by s3 and exotic_qi3:
    s3_kernel_eval = (
        s3(witness_111)
        + Fraction(1, 3) * (s3(nine_rays_gvec[0]) + s3(nine_rays_gvec[1]) + s3(nine_rays_gvec[2]))
        - Fraction(2, 3) * (s3(nine_rays_gvec[3]) + s3(nine_rays_gvec[4]) + s3(nine_rays_gvec[5]))
    )
    exotic_kernel_eval = (
        exotic_qi3(witness_111)
        + Fraction(1, 3)
        * (exotic_qi3(nine_rays_gvec[0]) + exotic_qi3(nine_rays_gvec[1]) + exotic_qi3(nine_rays_gvec[2]))
        - Fraction(2, 3)
        * (exotic_qi3(nine_rays_gvec[3]) + exotic_qi3(nine_rays_gvec[4]) + exotic_qi3(nine_rays_gvec[5]))
    )
    require(s3_kernel_eval == 1 and exotic_kernel_eval == Fraction(1, 3),
            "s3 and exotic_qi3 constructively separate the 7-ray projector kernel")

    # Check frame additivity across orthogonal frames with odd-v3 rays across shells.
    ortho_pairs = [
        (witness_111, gv_int(1, 0, -1, 0, 0, 0)),
        (witness_111, gv_int(1, 0, 1, 0, -2, 0)),
        (witness_div4, gv_int(1, 0, -1, 0, 0, 0)),
        (witness_div8, gv_int(0, 0, 2, 4, -5, -5)),
    ]
    for u, v in ortho_pairs:
        w = herm_cross(u, v)
        require(g_inner(u, v) == (0, 0) and g_inner(u, w) == (0, 0) and g_inner(v, w) == (0, 0),
                "orthogonal completion via Hermitian cross product")
        require((v3_rat(vec_norm_sq(u)) + v3_rat(vec_norm_sq(v)) + v3_rat(vec_norm_sq(w))) % 2 == 0,
                "sum of 3-adic norm valuations on orthogonal frame is even")
        require(s3(u) + s3(v) + s3(w) == 0, "s3 is a zero-weight frame function")
        require(exotic_qi3(u) + exotic_qi3(v) + exotic_qi3(w) == 1,
                "exotic_qi3 is a weight-1 frame function")

    # Second inert prime p = 7 == 3 (mod 4): s7 is linearly independent of s3.
    witness_p7 = gv_int(1, 0, 2, 0, 1, 1)  # norm 1 + 4 + 2 = 7
    require(
        is_one_plus_i_primitive_gvec(witness_p7)
        and vec_norm_sq(witness_p7) == 7
        and s3(witness_p7) == 0
        and sp_residual(witness_p7, 7) == 1
        and sp_residual(witness_111, 7) == 0,
        "s3 and s7 are linearly independent bounded zero-weight residuals",
    )
    require(all(sp_residual(r, 7) == 0 for r in nine_rays_gvec),
            "s7 vanishes on all nine tomography rays")
    u7, v7 = witness_p7, gv_int(2, 0, -1, 0, 0, 0)
    w7 = herm_cross(u7, v7)
    require(sp_residual(u7, 7) + sp_residual(v7, 7) + sp_residual(w7, 7) == 0,
            "s7 satisfies zero-weight additivity on odd-v7 orthogonal frame")

    # Negative control: flipping the u3 == 2 (mod 3) sign breaks frame additivity.
    u0, v0 = ortho_pairs[0]
    w0 = herm_cross(u0, v0)
    require(abs(s3(u0)) + abs(s3(v0)) + abs(s3(w0)) == 2,
            "negative control: unsigned 3-adic parity fails zero-weight sum")

    # Section 9A: Archimedean discontinuity perturbations near e1 = (1, 0, 0) for p = 3 and p = 7.
    for k in range(1, 8):
        scale3 = Fraction(1, 3 * k)
        pos3_int = gv_int(3 * k, 0, 1, 0, 1, 1)
        neg3_int = gv_int(3 * k, 0, 1, 1, 1, 0)
        pos3_ray = (
            (scale3 * pos3_int[0][0], scale3 * pos3_int[0][1]),
            (scale3 * pos3_int[1][0], scale3 * pos3_int[1][1]),
            (scale3 * pos3_int[2][0], scale3 * pos3_int[2][1]),
        )
        neg3_ray = (
            (scale3 * neg3_int[0][0], scale3 * neg3_int[0][1]),
            (scale3 * neg3_int[1][0], scale3 * neg3_int[1][1]),
            (scale3 * neg3_int[2][0], scale3 * neg3_int[2][1]),
        )
        dist_pos3 = (
            g_norm_sq((pos3_ray[0][0] - 1, pos3_ray[0][1]))
            + g_norm_sq(pos3_ray[1])
            + g_norm_sq(pos3_ray[2])
        )
        dist_neg3 = (
            g_norm_sq((neg3_ray[0][0] - 1, neg3_ray[0][1]))
            + g_norm_sq(neg3_ray[1])
            + g_norm_sq(neg3_ray[2])
        )
        require(
            s3(pos3_int) == 1
            and s3(pos3_ray) == 1
            and exotic_qi3(pos3_ray) == Fraction(2, 3)
            and dist_pos3 == Fraction(1, 3 * k * k),
            "positive 3-adic perturbation ray approaches e1 with s3 == +1",
        )
        require(
            s3(neg3_int) == -1
            and s3(neg3_ray) == -1
            and exotic_qi3(neg3_ray) == Fraction(0)
            and dist_neg3 == Fraction(1, 3 * k * k),
            "negative 3-adic perturbation ray approaches e1 with s3 == -1",
        )

        scale7 = Fraction(1, 7 * k)
        pos7_int = gv_int(7 * k, 0, 1, 1, 2, 1)  # y norm 2 ((2/7)=+1), z norm 5 ((5/7)=-1), total 49k^2+7
        neg7_int = gv_int(7 * k, 0, 2, 1, 1, 1)
        pos7_ray = (
            (scale7 * pos7_int[0][0], scale7 * pos7_int[0][1]),
            (scale7 * pos7_int[1][0], scale7 * pos7_int[1][1]),
            (scale7 * pos7_int[2][0], scale7 * pos7_int[2][1]),
        )
        neg7_ray = (
            (scale7 * neg7_int[0][0], scale7 * neg7_int[0][1]),
            (scale7 * neg7_int[1][0], scale7 * neg7_int[1][1]),
            (scale7 * neg7_int[2][0], scale7 * neg7_int[2][1]),
        )
        dist_pos7 = (
            g_norm_sq((pos7_ray[0][0] - 1, pos7_ray[0][1]))
            + g_norm_sq(pos7_ray[1])
            + g_norm_sq(pos7_ray[2])
        )
        require(
            sp_residual(pos7_ray, 7) == 1
            and sp_residual(neg7_ray, 7) == -1
            and s3(pos7_ray) == 0
            and s3(neg7_ray) == 0
            and dist_pos7 == Fraction(1, 7 * k * k),
            "7-adic perturbation rays approach e1 with s7 == +/-1 and s3 == 0",
        )
        scale3_7k = Fraction(1, 21 * k)
        pos3_7k_int = gv_int(21 * k, 0, 1, 0, 1, 1)
        neg3_7k_int = gv_int(21 * k, 0, 1, 1, 1, 0)
        pos3_7k_ray = (
            (scale3_7k * pos3_7k_int[0][0], scale3_7k * pos3_7k_int[0][1]),
            (scale3_7k * pos3_7k_int[1][0], scale3_7k * pos3_7k_int[1][1]),
            (scale3_7k * pos3_7k_int[2][0], scale3_7k * pos3_7k_int[2][1]),
        )
        neg3_7k_ray = (
            (scale3_7k * neg3_7k_int[0][0], scale3_7k * neg3_7k_int[0][1]),
            (scale3_7k * neg3_7k_int[1][0], scale3_7k * neg3_7k_int[1][1]),
            (scale3_7k * neg3_7k_int[2][0], scale3_7k * neg3_7k_int[2][1]),
        )
        require(
            s3(pos3_7k_ray) == 1
            and s3(neg3_7k_ray) == -1
            and sp_residual(pos3_7k_ray, 7) == 0
            and sp_residual(neg3_7k_ray, 7) == 0,
            "subsequence 3-adic perturbation rays (7*k) have s3 == +/-1 and s7 == 0",
        )

    exotic_qi7 = lambda u: (Fraction(1) + sp_residual(u, 7)) / 3
    exotic_comb_37 = lambda c3, c7, u: (Fraction(1) + c3 * s3(u) + c7 * sp_residual(u, 7)) / 3
    require(
        exotic_qi7(witness_p7) == Fraction(2, 3)
        and exotic_qi7(witness_111) == Fraction(1, 3)
        and exotic_qi7(u7) + exotic_qi7(v7) + exotic_qi7(w7) == Fraction(1)
        and exotic_comb_37(Fraction(2, 5), Fraction(-3, 5), u7)
        + exotic_comb_37(Fraction(2, 5), Fraction(-3, 5), v7)
        + exotic_comb_37(Fraction(2, 5), Fraction(-3, 5), w7)
        == Fraction(1),
        "exoticQi7 and exoticComb37 are weight-1 nonnegative frame functions separating witness_p7 from witness_111",
    )
    kernel_p7_eval = lambda f: (
        f(witness_p7)
        + Fraction(3, 7) * f(nine_rays_gvec[0])
        + Fraction(2, 7) * f(nine_rays_gvec[1])
        + Fraction(4, 7) * f(nine_rays_gvec[2])
        - Fraction(4, 7) * f(nine_rays_gvec[3])
        - Fraction(2, 7) * f(nine_rays_gvec[4])
        - Fraction(4, 7) * f(nine_rays_gvec[5])
        - Fraction(2, 7) * f(nine_rays_gvec[7])
        - Fraction(4, 7) * f(nine_rays_gvec[8])
    )
    require(
        kernel_p7_eval(lambda u: sp_residual(u, 7)) == Fraction(1)
        and kernel_p7_eval(s3) == Fraction(0)
        and kernel_p7_eval(lambda u: Fraction(2, 5) * s3(u) - Fraction(3, 7) * sp_residual(u, 7)) == Fraction(-3, 7),
        "s7_witness_p7_kernel_separation evaluates to 1 on s7, 0 on s3, and c7 on combResidual37 c3 c7",
    )

    # Section 9B: Quadratic field extension Q(i, sqrt(3))^3 and Q(i, sqrt(7))^3 frames
    # breaking even-vp parity and forcing G(witness) == 0.
    sqrt3 = sp.sqrt(3)
    u_s3 = sp.Matrix([1, 1, 1])
    p_s3 = sp.Matrix([1 + sp.I + sqrt3, 1 + sp.I - sqrt3, -2 - 2 * sp.I])
    q_s3 = sp.Matrix([-1 + (1 - sp.I) * sqrt3, -1 - (1 - sp.I) * sqrt3, 2])
    require(
        zero((u_s3.conjugate().T * p_s3)[0])
        and zero((u_s3.conjugate().T * q_s3)[0])
        and zero((p_s3.conjugate().T * q_s3)[0]),
        "Q(i, sqrt(3))^3 frame (witness_111, p_s3, q_s3) is pairwise orthogonal",
    )
    require(
        sp.expand((u_s3.conjugate().T * u_s3)[0]) == 3
        and sp.expand((p_s3.conjugate().T * p_s3)[0]) == 18
        and sp.expand((q_s3.conjugate().T * q_s3)[0]) == 18
        and vp_rat(Fraction(18), 3) == 2
        and vp_rat(Fraction(18), 7) == 0,
        "Q(i, sqrt(3))^3 frame has rational squared norms (3, 18, 18) with even v3 and v7 on partners",
    )

    sqrt7 = sp.sqrt(7)
    u_s7 = sp.Matrix([1, 2, 1 + sp.I])
    v_s7_tilde = sqrt7 * sp.Matrix([2, -1, 0])
    w_s7 = sp.Matrix([1 - sp.I, 2 - 2 * sp.I, -5])
    p_s7 = (1 + sp.I) * v_s7_tilde + (2 + sp.I) * w_s7
    q_s7 = (2 - sp.I) * v_s7_tilde - (1 - sp.I) * w_s7
    require(
        zero((u_s7.conjugate().T * p_s7)[0])
        and zero((u_s7.conjugate().T * q_s7)[0])
        and zero((p_s7.conjugate().T * q_s7)[0]),
        "Q(i, sqrt(7))^3 frame (witness_p7, p_s7, q_s7) is pairwise orthogonal",
    )
    require(
        sp.expand((u_s7.conjugate().T * u_s7)[0]) == 7
        and sp.expand((p_s7.conjugate().T * p_s7)[0]) == 245
        and sp.expand((q_s7.conjugate().T * q_s7)[0]) == 245
        and vp_rat(Fraction(245), 3) == 0
        and vp_rat(Fraction(245), 7) == 2
        and vp_rat(Fraction(245), 11) == 0,
        "Q(i, sqrt(7))^3 frame has rational squared norms (7, 245, 245) with even v3, v7, and v11 on partners",
    )

    # Section 9E: Uniform prime-indexed sp_residual, third inert prime p = 11 == 3 (mod 4),
    # 3x3 Kronecker-delta witness duality, 7-ray witness_p11 projector kernel separation,
    # selective 3-prime oscillation near e1 = (1, 0, 0), and Q(i, sqrt(11))^3 frame completion.
    vp11_sp = sp.Matrix([1, 3, 1])
    q_p11 = sp.expand((vp11_sp.conjugate().T * rho * vp11_sp)[0] / 11)
    kernel_comb_p11 = (
        q_p11
        + sp.Rational(3, 11) * values[0]
        - sp.Rational(3, 11) * values[1]
        + sp.Rational(3, 11) * values[2]
        - sp.Rational(6, 11) * values[3]
        - sp.Rational(2, 11) * values[5]
        - sp.Rational(6, 11) * values[7]
    )
    require(zero(kernel_comb_p11),
            "7-ray projector kernel relation for witness_p11 = (1, 3, 1) vanishes identically for every HermForm3")

    witness_p11 = gv_int(1, 0, 3, 0, 1, 0)  # norm 1 + 9 + 1 = 11
    require(
        is_one_plus_i_primitive_gvec(witness_p11)
        and vec_norm_sq(witness_p11) == 11
        and all(sp_residual(r, 11) == 0 for r in nine_rays_gvec),
        "witness_p11 = (1, 3, 1) is (1+i)-primitive of norm 11 and sp 11 vanishes on all nine tomography rays",
    )
    primes_3_7_11 = (3, 7, 11)
    witnesses_3_7_11 = (witness_111, witness_p7, witness_p11)
    for i_idx, p_i in enumerate(primes_3_7_11):
        for j_idx, w_j in enumerate(witnesses_3_7_11):
            expected_delta = Fraction(1 if i_idx == j_idx else 0)
            require(
                sp_residual(w_j, p_i) == expected_delta,
                f"3x3 Kronecker-delta duality failed at p={p_i}, witness index={j_idx}",
            )

    u11, v11 = witness_p11, gv_int(3, 0, -1, 0, 0, 0)
    w11 = herm_cross(u11, v11)
    require(
        g_inner(u11, v11) == (0, 0)
        and (vp_rat(vec_norm_sq(u11), 11) + vp_rat(vec_norm_sq(v11), 11) + vp_rat(vec_norm_sq(w11), 11)) % 2 == 0
        and sp_residual(u11, 11) + sp_residual(v11, 11) + sp_residual(w11, 11) == 0,
        "sp 11 satisfies zero-weight additivity on odd-v11 orthogonal frame",
    )

    kernel_p11_eval = lambda f: (
        f(witness_p11)
        + Fraction(3, 11) * f(nine_rays_gvec[0])
        - Fraction(3, 11) * f(nine_rays_gvec[1])
        + Fraction(3, 11) * f(nine_rays_gvec[2])
        - Fraction(6, 11) * f(nine_rays_gvec[3])
        - Fraction(2, 11) * f(nine_rays_gvec[4])
        - Fraction(6, 11) * f(nine_rays_gvec[5])
    )
    require(
        kernel_p11_eval(lambda u: sp_residual(u, 11)) == Fraction(1)
        and kernel_p11_eval(lambda u: sp_residual(u, 3)) == Fraction(0)
        and kernel_p11_eval(lambda u: sp_residual(u, 7)) == Fraction(0)
        and kernel_p11_eval(
            lambda u: Fraction(1, 5) * sp_residual(u, 3)
            - Fraction(2, 7) * sp_residual(u, 7)
            + Fraction(4, 11) * sp_residual(u, 11)
        )
        == Fraction(4, 11),
        "sp11_witness_p11_kernel_separation evaluates to 1 on sp 11, 0 on sp 3 and sp 7, and c11 on combResidual3_7_11",
    )

    for k in range(1, 5):
        # Product-scaled selective perturbation rays for p in {3, 7, 11}:
        # p = 3: scale 3 * 77 * k = 231 * k
        s_3 = Fraction(1, 231 * k)
        u3_p = ((Fraction(1), Fraction(0)), (s_3, Fraction(0)), (s_3, s_3))
        u3_n = ((Fraction(1), Fraction(0)), (s_3, s_3), (s_3, Fraction(0)))
        # p = 7: scale 7 * 33 * k = 231 * k
        s_7 = Fraction(1, 231 * k)
        u7_p = ((Fraction(1), Fraction(0)), (s_7, s_7), (2 * s_7, s_7))
        u7_n = ((Fraction(1), Fraction(0)), (2 * s_7, s_7), (s_7, s_7))
        # p = 11: scale 11 * 21 * k = 231 * k, y = 3 (norm 9, (9/11)=+1), z = 1+i (norm 2, (2/11)=-1)
        s_11 = Fraction(1, 231 * k)
        u11_p = ((Fraction(1), Fraction(0)), (3 * s_11, Fraction(0)), (s_11, s_11))
        u11_n = ((Fraction(1), Fraction(0)), (s_11, s_11), (3 * s_11, Fraction(0)))
        selective_rays = [(3, u3_p, u3_n), (7, u7_p, u7_n), (11, u11_p, u11_n)]
        for p_target, r_pos, r_neg in selective_rays:
            for q_prime in primes_3_7_11:
                if q_prime == p_target:
                    require(
                        sp_residual(r_pos, q_prime) == 1 and sp_residual(r_neg, q_prime) == -1,
                        f"selective oscillation diagonal failed at p={p_target}",
                    )
                else:
                    require(
                        sp_residual(r_pos, q_prime) == 0 and sp_residual(r_neg, q_prime) == 0,
                        f"selective oscillation off-diagonal failed at p={p_target}, q={q_prime}",
                    )

    sqrt11 = sp.sqrt(11)
    u_s11 = sp.Matrix([1, 3, 1])
    v_s11_tilde = sqrt11 * sp.Matrix([3, -1, 0])
    w_s11 = sp.Matrix([1, 3, -10])
    p_s11 = 3 * v_s11_tilde + (1 + sp.I) * w_s11
    q_s11 = (1 - sp.I) * v_s11_tilde - 3 * w_s11
    require(
        zero((u_s11.conjugate().T * p_s11)[0])
        and zero((u_s11.conjugate().T * q_s11)[0])
        and zero((p_s11.conjugate().T * q_s11)[0]),
        "Q(i, sqrt(11))^3 frame (witness_p11, p_s11, q_s11) is pairwise orthogonal",
    )
    require(
        sp.expand((u_s11.conjugate().T * u_s11)[0]) == 11
        and sp.expand((p_s11.conjugate().T * p_s11)[0]) == 1210
        and sp.expand((q_s11.conjugate().T * q_s11)[0]) == 1210
        and vp_rat(Fraction(18), 11) == 0
        and vp_rat(Fraction(1210), 3) == 0
        and vp_rat(Fraction(1210), 7) == 0
        and vp_rat(Fraction(1210), 11) == 2,
        "Q(i, sqrt(11))^3 frame has rational squared norms (11, 1210, 1210) with even v3, v7, and v11 on partners",
    )

    # Section 9F: Planar frame-rotation pairs, operator parallelogram law,
    # coordinate-sign symmetry vs. orthogonal parallelogram law, equatorial pole
    # witnesses, and Piron / Pythagorean equatorial rotations on Q(i)^3.
    def g_mul_c(a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    def g_conj_c(a: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        return (a[0], -a[1])

    def g_add_vec(u: GVec, v: GVec) -> GVec:
        return tuple((a[0] + b[0], a[1] + b[1]) for a, b in zip(u, v))  # type: ignore[return-value]

    def g_sub_vec(u: GVec, v: GVec) -> GVec:
        return tuple((a[0] - b[0], a[1] - b[1]) for a, b in zip(u, v))  # type: ignore[return-value]

    def g_smul_vec(c: tuple[Fraction, Fraction], u: GVec) -> GVec:
        return tuple(g_mul_c(c, a) for a in u)  # type: ignore[return-value]

    def rot_pair_u(u: GVec, v: GVec, a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> GVec:
        return g_add_vec(g_smul_vec(a, u), g_smul_vec(b, v))

    def rot_pair_v(u: GVec, v: GVec, a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> GVec:
        nu = (vec_norm_sq(u), Fraction(0))
        nv = (vec_norm_sq(v), Fraction(0))
        c1 = g_mul_c((-nv[0], Fraction(0)), g_conj_c(b))
        c2 = g_mul_c(nu, g_conj_c(a))
        return g_add_vec(g_smul_vec(c1, u), g_smul_vec(c2, v))

    def eq_ortho(y: GVec) -> GVec:
        return ((Fraction(0), Fraction(0)), (-y[2][0], y[2][1]), (y[1][0], -y[1][1]))

    def piron_step(y: GVec, lam: tuple[Fraction, Fraction]) -> GVec:
        return g_add_vec(g_add_vec(nine_rays_gvec[0], y), g_smul_vec(lam, eq_ortho(y)))

    def piron_partner(y: GVec, lam: tuple[Fraction, Fraction]) -> GVec:
        ny = vec_norm_sq(y)
        c1 = (-g_norm_sq(lam) * ny, Fraction(0))
        c2 = g_mul_c((Fraction(1) + ny, Fraction(0)), lam)
        return g_add_vec(
            g_smul_vec(c1, g_add_vec(nine_rays_gvec[0], y)),
            g_smul_vec(c2, eq_ortho(y)),
        )

    def meridian_ortho(y: GVec) -> GVec:
        return g_add_vec(g_smul_vec((-vec_norm_sq(y), Fraction(0)), nine_rays_gvec[0]), y)

    def pythag_eq_rot(y: GVec, k: int) -> GVec:
        kf = Fraction(k)
        c1 = ((kf * kf - 1) / (kf * kf + 1), Fraction(0))
        c2 = ((2 * kf) / (kf * kf + 1), Fraction(0))
        return g_add_vec(g_smul_vec(c1, y), g_smul_vec(c2, eq_ortho(y)))

    def quad_ray_e1(u: GVec) -> Fraction:
        return g_norm_sq(u[0]) / vec_norm_sq(u)

    eq_witness_3 = gv_int(0, 0, 1, 0, 1, 1)
    eq_witness_3_neg = gv_int(0, 0, 1, 1, 1, 0)
    eq_witness_7 = gv_int(0, 0, 1, 1, 2, 1)
    eq_witness_7_neg = gv_int(0, 0, 2, 1, 1, 1)
    eq_witness_11 = gv_int(0, 0, 3, 0, 1, 1)
    eq_witness_11_neg = gv_int(0, 0, 1, 1, 3, 0)
    eq_witness_table = [
        (eq_witness_3, (1, 0, 0)),
        (eq_witness_3_neg, (-1, 0, 0)),
        (eq_witness_7, (0, 1, 0)),
        (eq_witness_7_neg, (0, -1, 0)),
        (eq_witness_11, (0, 0, 1)),
        (eq_witness_11_neg, (0, 0, -1)),
    ]
    for w_vec, (e3, e7, e11) in eq_witness_table:
        require(
            quad_ray_e1(w_vec) == 0
            and sp_residual(w_vec, 3) == e3
            and sp_residual(w_vec, 7) == e7
            and sp_residual(w_vec, 11) == e11,
            "equatorial witness table isolates (sp 3, sp 7, sp 11) with +-1 in e1^perp",
        )

    # Verify failure of orthogonal parallelogram law for s3, s7, sp 11:
    # e1 + (0, 1, 1) = witness_111 (norm 3, s3 = +1),
    # e1 + (0, 2, 1+i) = witness_p7 (norm 7, s7 = +1),
    # e1 + (0, 3, 1) = witness_p11 (norm 11, sp 11 = +1),
    # and by coordinate-sign symmetry sp p (e1 + y) + sp p (e1 - y) = 2 != 0.
    parallelogram_counterexamples = [
        (3, gv_int(0, 0, 1, 0, 1, 0)),
        (7, gv_int(0, 0, 2, 0, 1, 1)),
        (11, gv_int(0, 0, 3, 0, 1, 0)),
    ]
    for p_prime, w_pos in parallelogram_counterexamples:
        u_plus = g_add_vec(nine_rays_gvec[0], w_pos)
        u_minus = g_sub_vec(nine_rays_gvec[0], w_pos)
        require(
            g_inner(nine_rays_gvec[0], w_pos) == (Fraction(0), Fraction(0))
            and sp_residual(u_plus, p_prime) == Fraction(1)
            and sp_residual(u_minus, p_prime) == Fraction(1)
            and sp_residual(u_plus, p_prime) + sp_residual(u_minus, p_prime) == Fraction(2),
            f"sp {p_prime} violates orthogonal parallelogram zero law on (e1, w_pos)",
        )

    # Verify Piron step / partner / meridian identities and Pythagorean equatorial rotations:
    for y_eq in [eq_witness_3, eq_witness_7, eq_witness_11]:
        for k_step in range(1, 5):
            lam_step = (Fraction(1, k_step), Fraction(0))
            u_base = g_add_vec(nine_rays_gvec[0], y_eq)
            v_base = g_smul_vec(lam_step, eq_ortho(y_eq))
            w_mer = meridian_ortho(y_eq)
            p_step = piron_step(y_eq, lam_step)
            p_part = piron_partner(y_eq, lam_step)
            require(
                p_step == rot_pair_u(u_base, v_base, (Fraction(1), Fraction(0)), (Fraction(1), Fraction(0)))
                and p_part == rot_pair_v(u_base, v_base, (Fraction(1), Fraction(0)), (Fraction(1), Fraction(0)))
                and g_inner(u_base, v_base) == (Fraction(0), Fraction(0))
                and g_inner(u_base, w_mer) == (Fraction(0), Fraction(0))
                and g_inner(v_base, w_mer) == (Fraction(0), Fraction(0))
                and g_inner(p_step, p_part) == (Fraction(0), Fraction(0)),
                "Piron base and rotated frames are pairwise orthogonal",
            )
            require(
                quad_ray_e1(p_step) + quad_ray_e1(p_part) == quad_ray_e1(u_base) + quad_ray_e1(v_base)
                and quad_ray_e1(p_step) <= quad_ray_e1(u_base)
                and quad_ray_e1(u_base) + quad_ray_e1(w_mer) == Fraction(1)
                and vec_norm_sq(g_sub_vec(p_step, u_base)) == vec_norm_sq(y_eq) / Fraction(k_step * k_step),
                "Piron frame-rotation sum, monotone descent, meridian complement, and step distance hold",
            )
            y_rot = pythag_eq_rot(y_eq, k_step)
            require(
                y_rot[0] == (Fraction(0), Fraction(0))
                and vec_norm_sq(y_rot) == vec_norm_sq(y_eq)
                and vec_norm_sq(g_add_vec(nine_rays_gvec[0], y_rot)) == vec_norm_sq(u_base)
                and quad_ray_e1(g_add_vec(nine_rays_gvec[0], y_rot)) == quad_ray_e1(u_base),
                "Pythagorean equatorial rotation preserves norm and north-pole Born weight",
            )

    print(json.dumps({"status": "PASS", "sympy_version": sp.__version__,
                      "tomography_rank": tomography.rank(),
                      "s3_witness_111": int(s3(witness_111)),
                      "s3_witness_div4": int(s3(witness_div4)),
                      "s3_witness_div8": int(s3(witness_div8)),
                      "s7_witness_p7": int(sp_residual(witness_p7, 7)),
                      "sp11_witness_p11": int(sp_residual(witness_p11, 11)),
                      "exotic_qi7_witness_p7": str(exotic_qi7(witness_p7)),
                      "sqrt3_frame_norms": [3, 18, 18],
                      "sqrt7_frame_norms": [7, 245, 245],
                      "sqrt11_frame_norms": [11, 1210, 1210],
                      "piron_ortho_parallelogram_sums": [2, 2, 2],
                      "scope": "symbolic algebra controls, uniform sp_residual (p in {3,7,11}), selective oscillation, joint elimination, and Piron/parallelogram/continuity bridge"},
                     sort_keys=True))


if __name__ == "__main__":
    main()

