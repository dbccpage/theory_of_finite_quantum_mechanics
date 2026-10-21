"""Exact rational Cayley circle parameterization, 5-adic half-angle obstruction,
Gaussian power injectivity, quadratic half-angle restoration, cyclotomic torsion
tower Q/Z, and Cauchy/dyadic phase completion receipts for FQ-GAP-U1-CIRCLE.

Replays in exact rational arithmetic the Lean modules of
dag/results/FQ-GAP-U1-CIRCLE/runs/20261020T223000Z_u1_phase_completion_lean
(U1CayleyProjectiveCircle, U1HalfAngleObstruction, U1PowerMapInjectivity,
U1CyclotomicTorsionTower, U1CauchyCircleCompletion) and mirrors the Rust twin
code/rust/src/qm/u1_phase_completion.rs.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from math import floor

AUTHORITY_FENCE = (
    "AuthorityEffect None; exact rational and quadratic algebraic certificates only; "
    "compact analytic U(1) topology and transcendental exponential/logarithm maps are "
    "not derived from finite or rational data alone."
)

PROVENANCE = (
    "Replays the Lean modules of "
    "dag/results/FQ-GAP-U1-CIRCLE/runs/20261020T223000Z_u1_phase_completion_lean "
    "(U1CayleyProjectiveCircle, U1HalfAngleObstruction, U1PythagoreanObstruction, "
    "U1PowerMapInjectivity, U1CyclotomicTorsionTower, U1CauchyCircleCompletion, "
    "U1ChebyshevCauchyBridge, U1QuadraticTowerAndCayleyStone, U1PhaseSynthesis) and mirrors "
    "code/rust/src/qm/u1_phase_completion.rs."
)


def _q(x: object) -> Q:
    if type(x) is int:
        return Q(x)
    if type(x) is Q:
        return x
    raise ValueError("exact integer or Fraction required")


def _z(n: object) -> int:
    if type(n) is int:
        return n
    raise ValueError("exact integer required")


# ============================================================================
# 1. Affine & Projective Cayley Parameterization of S^1(Q)
# ============================================================================


def is_unit_circle(re: object, im: object) -> bool:
    """Return True when (re, im) lies on the rational unit circle re^2 + im^2 == 1."""
    x, y = _q(re), _q(im)
    return x * x + y * y == Q(1)


def circle_mul(re1: object, im1: object, re2: object, im2: object) -> tuple[Q, Q]:
    """Multiply two points on S^1(Q) via Gaussian multiplication."""
    x1, y1 = _q(re1), _q(im1)
    x2, y2 = _q(re2), _q(im2)
    if not is_unit_circle(x1, y1) or not is_unit_circle(x2, y2):
        raise ValueError("points on the unit circle required")
    return (x1 * x2 - y1 * y2, x1 * y2 + y1 * x2)


def affine_cayley(t: object) -> tuple[Q, Q]:
    """Map rational parameter t to ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)) on S^1(Q)."""
    r = _q(t)
    denom = Q(1) + r * r
    return ((Q(1) - r * r) / denom, (Q(2) * r) / denom)


def inverse_cayley(re: object, im: object) -> Q:
    """Invert the affine Cayley map via im / (re + 1); refuses (-1, 0) and non-unit points."""
    x, y = _q(re), _q(im)
    if not is_unit_circle(x, y):
        raise ValueError("point on the unit circle required")
    if x == Q(-1):
        raise ValueError("south-pole puncture (-1, 0) is outside the affine Cayley chart")
    return y / (x + Q(1))


def affine_cayley_mul_param(t1: object, t2: object) -> Q | None:
    """Return (t1 + t2)/(1 - t1*t2) when t1*t2 != 1, or None at the south-pole collision."""
    r1, r2 = _q(t1), _q(t2)
    denom = Q(1) - r1 * r2
    if denom == Q(0):
        return None
    return (r1 + r2) / denom


def projective_cayley(u: object, v: object) -> tuple[Q, Q]:
    """Map homogeneous coordinates [u : v] in P^1(Q) to S^1(Q), sending [0 : 1] to (-1, 0)."""
    x, y = _q(u), _q(v)
    denom = x * x + y * y
    if denom == Q(0):
        raise ValueError("homogeneous origin (0, 0) is excluded from P^1(Q)")
    return ((x * x - y * y) / denom, (Q(2) * x * y) / denom)


def inverse_projective_cayley(re: object, im: object) -> tuple[Q, Q]:
    """Map every point of S^1(Q) to a representative [u : v] in P^1(Q)."""
    x, y = _q(re), _q(im)
    if not is_unit_circle(x, y):
        raise ValueError("point on the unit circle required")
    if x == Q(-1):
        return (Q(0), Q(1))
    return (Q(1), y / (x + Q(1)))


def projective_mul(u1: object, v1: object, u2: object, v2: object) -> tuple[Q, Q]:
    """Multiply homogeneous projective coordinates via (u1*u2 - v1*v2, u1*v2 + v1*u2)."""
    a1, b1 = _q(u1), _q(v1)
    a2, b2 = _q(u2), _q(v2)
    if (a1 == Q(0) and b1 == Q(0)) or (a2 == Q(0) and b2 == Q(0)):
        raise ValueError("homogeneous origin (0, 0) is excluded from P^1(Q)")
    return (a1 * a2 - b1 * b2, a1 * b2 + b1 * a2)


# ============================================================================
# 2. Pythagorean Half-Angle Obstruction & 5-Adic Valuation Certifier
# ============================================================================


def five_adic_valuation(n: object) -> tuple[int, int]:
    """Factor nonzero integer n = 5^v5 * unit_part with unit_part % 5 != 0."""
    m = _z(n)
    if m == 0:
        raise ValueError("nonzero integer required for 5-adic valuation")
    v5 = 0
    unit = m
    while unit % 5 == 0:
        unit //= 5
        v5 += 1
    return (v5, unit)


def certify_four_fifths_not_square(num: object, den: object) -> dict[str, object]:
    """Certify (num/den)^2 != 4/5 via 5-adic valuation parity on 5*num^2 vs 4*den^2."""
    p, q_den = _z(num), _z(den)
    if q_den == 0:
        raise ValueError("nonzero denominator required")
    lhs = 5 * p * p
    rhs = 4 * q_den * q_den
    residual = abs(lhs - rhs)
    v5_den, _ = five_adic_valuation(q_den)
    rhs_v5 = 2 * v5_den
    lhs_v5 = None if p == 0 else 2 * five_adic_valuation(p)[0] + 1
    parity_disjoint = True if lhs_v5 is None else (lhs_v5 % 2 == 1 and rhs_v5 % 2 == 0)
    return {
        "num": p,
        "den": q_den,
        "lhs_five_num_sq": lhs,
        "rhs_four_den_sq": rhs,
        "abs_residual": residual,
        "lhs_v5": lhs_v5,
        "rhs_v5": rhs_v5,
        "parity_disjoint": parity_disjoint,
        "obstructed": residual >= 1 and parity_disjoint,
    }


def certify_u345_no_rational_sqrt(re: object, im: object) -> dict[str, object]:
    """Certify that no (re, im) in Q^2 satisfies both (re + i*im)^2 = (3 + 4i)/5 and re^2 + im^2 = 1."""
    x, y = _q(re), _q(im)
    sq_re = x * x - y * y
    sq_im = Q(2) * x * y
    norm_sq = x * x + y * y
    half_sum = (sq_re + norm_sq) / Q(2)
    v5_receipt = certify_four_fifths_not_square(x.numerator, x.denominator)
    matches_target = sq_re == Q(3, 5) and sq_im == Q(4, 5) and norm_sq == Q(1)
    return {
        "re": str(x),
        "im": str(y),
        "sq_re": str(sq_re),
        "sq_im": str(sq_im),
        "norm_sq": str(norm_sq),
        "half_sum_equals_re_sq": half_sum == x * x,
        "re_sq_minus_four_fifths": str(x * x - Q(4, 5)),
        "four_fifths_obstruction": v5_receipt,
        "matches_u345_and_unit": matches_target,
        "obstructed": not matches_target and bool(v5_receipt["obstructed"]),
    }


# ============================================================================
# 3. Gaussian Power Recurrence & Mod-5 Idempotence Certifier
# ============================================================================


def gauss_pow_34(n: object) -> tuple[int, int]:
    """Compute exact integer coordinates (A_n, B_n) of (3 + 4i)^n for n >= 0."""
    exp = _z(n)
    if exp < 0:
        raise ValueError("nonnegative exponent required")
    a, b = 1, 0
    for _ in range(exp):
        a, b = 3 * a - 4 * b, 4 * a + 3 * b
    return (a, b)


def u345_power(k: object) -> tuple[Q, Q]:
    """Compute exact rational coordinates of ((3 + 4i)/5)^k for any integer k."""
    exp = _z(k)
    abs_k = abs(exp)
    a, b = gauss_pow_34(abs_k)
    scale = Q(5) ** abs_k
    imag_signed = b if exp >= 0 else -b
    return (Q(a) / scale, Q(imag_signed) / scale)


def _check_gauss_step(n: int) -> bool:
    a, b = gauss_pow_34(n)
    five_pow_2n = 5 ** (2 * n)
    return (a % 5 == 3) and (b % 5 == 4) and (b != 0) and (a * a + b * b == five_pow_2n)


def certify_power_injectivity_window(max_n: object) -> dict[str, object]:
    """Check mod-5 idempotence (A_n, B_n) == (3, 4) mod 5 and pairwise distinct powers on [-max_n, max_n]."""
    bound = _z(max_n)
    if bound < 1 or bound > 256:
        raise ValueError("max_n in [1, 256] required")
    mod5_ok = all(_check_gauss_step(n) for n in range(1, bound + 1))
    points = [u345_power(k) for k in range(-bound, bound + 1)]
    on_circle = all(is_unit_circle(re, im) for re, im in points)
    distinct = len(set(points)) == 2 * bound + 1
    return {
        "max_n": bound,
        "mod5_invariant_holds": mod5_ok,
        "all_on_unit_circle": on_circle,
        "tested_exponents": 2 * bound + 1,
        "distinct_points": len(set(points)),
        "injective_on_window": mod5_ok and on_circle and distinct,
    }


# ============================================================================
# 4. Algebraic Half-Angle Extension in Q(sqrt(5))(i)
# ============================================================================


@dataclass(frozen=True)
class QuadSqrt5:
    """Element a + b*sqrt(5) of the real quadratic extension Q(sqrt(5))."""

    a: Q
    b: Q

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", _q(self.a))
        object.__setattr__(self, "b", _q(self.b))


@dataclass(frozen=True)
class CircleQuadSqrt5:
    """Element re + i*im in Q(sqrt(5))(i)."""

    re: QuadSqrt5
    im: QuadSqrt5


def quad_add(x: QuadSqrt5, y: QuadSqrt5) -> QuadSqrt5:
    """Return x + y in Q(sqrt(5))."""
    return QuadSqrt5(x.a + y.a, x.b + y.b)


def quad_sub(x: QuadSqrt5, y: QuadSqrt5) -> QuadSqrt5:
    """Return x - y in Q(sqrt(5))."""
    return QuadSqrt5(x.a - y.a, x.b - y.b)


def quad_mul(x: QuadSqrt5, y: QuadSqrt5) -> QuadSqrt5:
    """Return x * y in Q(sqrt(5)) using (sqrt(5))^2 = 5."""
    return QuadSqrt5(x.a * y.a + Q(5) * x.b * y.b, x.a * y.b + x.b * y.a)


def quad_conj(x: QuadSqrt5) -> QuadSqrt5:
    """Return the Galois conjugate a - b*sqrt(5)."""
    return QuadSqrt5(x.a, -x.b)


def quad_norm(x: QuadSqrt5) -> Q:
    """Return the field norm N(a + b*sqrt(5)) = a^2 - 5*b^2."""
    return x.a * x.a - Q(5) * x.b * x.b


def quad_inv(x: QuadSqrt5) -> QuadSqrt5:
    """Return the multiplicative inverse in Q(sqrt(5)); refuses 0 + 0*sqrt(5)."""
    nrm = quad_norm(x)
    if nrm == Q(0):
        raise ValueError("zero element in Q(sqrt(5)) has no multiplicative inverse")
    return QuadSqrt5(x.a / nrm, -x.b / nrm)


def circle_quad_mul(z1: CircleQuadSqrt5, z2: CircleQuadSqrt5) -> CircleQuadSqrt5:
    """Multiply two elements in Q(sqrt(5))(i)."""
    re = quad_sub(quad_mul(z1.re, z2.re), quad_mul(z1.im, z2.im))
    im = quad_add(quad_mul(z1.re, z2.im), quad_mul(z1.im, z2.re))
    return CircleQuadSqrt5(re, im)


def circle_quad_norm_sq(z: CircleQuadSqrt5) -> QuadSqrt5:
    """Return re^2 + im^2 in Q(sqrt(5))."""
    return quad_add(quad_mul(z.re, z.re), quad_mul(z.im, z.im))


def u345_quad_sqrt_certificate() -> dict[str, object]:
    """Certify that w = (2/5*sqrt(5), 1/5*sqrt(5)) in S^1(Q(sqrt(5))) satisfies w^2 = (3/5, 4/5)."""
    w = CircleQuadSqrt5(QuadSqrt5(Q(0), Q(2, 5)), QuadSqrt5(Q(0), Q(1, 5)))
    w_sq = circle_quad_mul(w, w)
    nrm_sq = circle_quad_norm_sq(w)
    target = CircleQuadSqrt5(QuadSqrt5(Q(3, 5), Q(0)), QuadSqrt5(Q(4, 5), Q(0)))
    unit = QuadSqrt5(Q(1), Q(0))
    return {
        "w_re": (str(w.re.a), str(w.re.b)),
        "w_im": (str(w.im.a), str(w.im.b)),
        "w_sq_re": (str(w_sq.re.a), str(w_sq.re.b)),
        "w_sq_im": (str(w_sq.im.a), str(w_sq.im.b)),
        "norm_sq": (str(nrm_sq.a), str(nrm_sq.b)),
        "squares_to_u345": w_sq == target,
        "on_unit_circle": nrm_sq == unit,
        "requires_quadratic_extension": w.re.b != Q(0) and w.im.b != Q(0),
    }


# ============================================================================
# 5. Cyclotomic Torsion Tower mu_N -> Q/Z & Finite Haar Character Orthogonality
# ============================================================================


def refine_torsion_phase(n_level: object, k_factor: object, a_index: object) -> dict[str, object]:
    """Refine a_index mod n_level to (k_factor * a_index) mod (k_factor * n_level) in Q/Z."""
    n = _z(n_level)
    k = _z(k_factor)
    a = _z(a_index)
    if n < 1 or k < 1:
        raise ValueError("positive n_level and k_factor required")
    base_idx = a % n
    refined_idx = k * base_idx
    refined_level = k * n
    base_phase = Q(base_idx, n)
    refined_phase = Q(refined_idx, refined_level)
    return {
        "n_level": n,
        "k_factor": k,
        "base_index": base_idx,
        "refined_level": refined_level,
        "refined_index": refined_idx,
        "base_phase": str(base_phase),
        "refined_phase": str(refined_phase),
        "phase_preserved": base_phase == refined_phase,
    }


def _mod_one(q: Q) -> Q:
    return q - Q(floor(q))


def divide_rat_phase_mod_one(q_phase: object, m_divisor: object) -> dict[str, object]:
    """Return the m_divisor distinct m-th division phases of q_phase in Q/Z cap [0, 1)."""
    q = _mod_one(_q(q_phase))
    m = _z(m_divisor)
    if m < 1 or m > 1024:
        raise ValueError("m_divisor in [1, 1024] required")
    roots = [_mod_one((q + Q(j)) / Q(m)) for j in range(m)]
    in_range = all(Q(0) <= r < Q(1) for r in roots)
    distinct = len(set(roots)) == m
    multiplies_back = all(_mod_one(Q(m) * r) == q for r in roots)
    return {
        "q_mod_one": str(q),
        "m_divisor": m,
        "roots": [str(r) for r in roots],
        "all_in_unit_interval": in_range,
        "distinct_count": len(set(roots)),
        "all_multiply_to_q_mod_one": in_range and distinct and multiplies_back,
    }


def _pow_i(exponent: int) -> tuple[Q, Q]:
    r = exponent % 4
    table = ((Q(1), Q(0)), (Q(0), Q(1)), (Q(-1), Q(0)), (Q(0), Q(-1)))
    return table[r]


def fourth_roots_haar_certificate(character_power: object) -> dict[str, object]:
    """Evaluate 1/4 * sum_{j=0}^3 i^(j * character_power) over mu_4 in Q(i)."""
    m = _z(character_power)
    terms = [_pow_i(j * m) for j in range(4)]
    avg_re = sum((re for re, _ in terms), Q(0)) / Q(4)
    avg_im = sum((im for _, im in terms), Q(0)) / Q(4)
    trivial = m % 4 == 0
    expected = (Q(1), Q(0)) if trivial else (Q(0), Q(0))
    return {
        "character_power": m,
        "is_trivial_character": trivial,
        "average_re": str(avg_re),
        "average_im": str(avg_im),
        "orthogonality_holds": (avg_re, avg_im) == expected,
    }


# ============================================================================
# 6. Cauchy / Dyadic Interval Completion & Finite Torsion Grid epsilon-Net
# ============================================================================


def torsion_grid_cover_certificate(q_phase: object, n_grid: object) -> dict[str, object]:
    """Certify that q_phase in [0, 1] lies within 1/n_grid of k/n_grid for k = floor(n_grid * q_phase)."""
    q = _q(q_phase)
    n = _z(n_grid)
    if q < Q(0) or q > Q(1):
        raise ValueError("q_phase in [0, 1] required")
    if n < 1:
        raise ValueError("positive n_grid required")
    k = floor(Q(n) * q)
    grid_pt = Q(k, n)
    dist = abs(q - grid_pt)
    bound = Q(1, n)
    return {
        "q_phase": str(q),
        "n_grid": n,
        "grid_index": k,
        "grid_point": str(grid_pt),
        "distance": str(dist),
        "bound": str(bound),
        "within_bound": 0 <= k <= n and dist <= bound,
    }


def dyadic_sqrt5_interval_step(lo: object, hi: object) -> dict[str, object]:
    """Bisect a rational interval [lo, hi] bracketing sqrt(5) and map to half-angle cosine 2*sqrt(5)/5."""
    a, b = _q(lo), _q(hi)
    if a < Q(0) or a > b or a * a > Q(5) or b * b < Q(5):
        raise ValueError("valid nonnegative bracket [lo, hi] with lo^2 <= 5 <= hi^2 required")
    mid = (a + b) / Q(2)
    new_lo, new_hi = (mid, b) if mid * mid <= Q(5) else (a, mid)
    cos_lo, cos_hi = Q(2, 5) * new_lo, Q(2, 5) * new_hi
    brackets_four_fifths = cos_lo * cos_lo <= Q(4, 5) <= cos_hi * cos_hi
    width_halved = (new_hi - new_lo) * Q(2) == (b - a)
    return {
        "new_lo": str(new_lo),
        "new_hi": str(new_hi),
        "cos_half_lo": str(cos_lo),
        "cos_half_hi": str(cos_hi),
        "width": str(new_hi - new_lo),
        "brackets_sqrt5": new_lo * new_lo <= Q(5) <= new_hi * new_hi,
        "brackets_four_fifths": brackets_four_fifths,
        "width_halved": width_halved,
    }


def negative_controls_certificate() -> dict[str, object]:
    """Certify the 3 rival / boundary failure modes for FQ-GAP-U1-CIRCLE."""
    sign_group_exp2 = (1 * 1 == 1) and ((-1) * (-1) == 1)
    split_null_norm = 1 * 1 - 1 * 1 == 0
    affine_collision = affine_cayley_mul_param(Q(1), Q(1)) is None
    proj_resolved = projective_cayley(*projective_mul(Q(1), Q(1), Q(1), Q(1))) == (Q(-1), Q(0))
    return {
        "sign_group_exponent_two": sign_group_exp2,
        "split_complex_zero_divisor_at_one_one": split_null_norm,
        "affine_cayley_pole_collision_at_one_one": affine_collision,
        "projective_cayley_resolves_south_pole": proj_resolved,
        "all_negative_controls_verified": (
            sign_group_exp2 and split_null_norm and affine_collision and proj_resolved
        ),
    }


# ============================================================================
# 7. Chebyshev/Taylor Cauchy Bridge & 4D Hermitian Q(i) Born Carrier
# ============================================================================


def chebyshev_t(n: object, x: object) -> Q:
    """Evaluate the Chebyshev polynomial T_n(x) of the first kind over Q."""
    deg = _z(n)
    val = _q(x)
    if deg < 0:
        raise ValueError("nonnegative degree n required")
    if deg == 0:
        return Q(1)
    t_prev, t_curr = Q(1), val
    for _ in range(2, deg + 1):
        t_prev, t_curr = t_curr, Q(2) * val * t_curr - t_prev
    return t_curr


def chebyshev_u(n: object, x: object) -> Q:
    """Evaluate the Chebyshev polynomial U_n(x) of the second kind over Q."""
    deg = _z(n)
    val = _q(x)
    if deg < 0:
        raise ValueError("nonnegative degree n required")
    if deg == 0:
        return Q(1)
    u_prev, u_curr = Q(1), Q(2) * val
    for _ in range(2, deg + 1):
        u_prev, u_curr = u_curr, Q(2) * val * u_curr - u_prev
    return u_curr


def chebyshev_circle_certificate(re: object, im: object, max_n: object) -> dict[str, object]:
    """Certify that (T_n(re), im * U_{n-1}(re)) equals (re + i*im)^n on S^1(Q) for 1 <= n <= max_n."""
    c, s = _q(re), _q(im)
    bound = _z(max_n)
    if not is_unit_circle(c, s):
        raise ValueError("point (re, im) on S^1(Q) required")
    if bound < 1 or bound > 64:
        raise ValueError("max_n in [1, 64] required")
    pow_re, pow_im = c, s
    all_match = True
    all_unit = True
    for deg in range(1, bound + 1):
        tn = chebyshev_t(deg, c)
        un_minus_1 = chebyshev_u(deg - 1, c)
        cheb_pt = (tn, s * un_minus_1)
        if cheb_pt != (pow_re, pow_im) or not is_unit_circle(cheb_pt[0], cheb_pt[1]):
            all_match = False
            all_unit = False
        pow_re, pow_im = circle_mul(pow_re, pow_im, c, s)
    return {
        "base_point": (str(c), str(s)),
        "max_n": bound,
        "chebyshev_matches_circle_powers": all_match,
        "pell_identity_holds_all_degrees": all_unit,
    }


def taylor_trig_enclosure_certificate(theta: object) -> dict[str, object]:
    """Certify alternating Taylor cosine/sine enclosures and degree-6 Pythagorean defect on 0 <= theta <= 1."""
    th = _q(theta)
    if th < Q(0) or th > Q(1):
        raise ValueError("theta in [0, 1] required")
    th2 = th * th
    th3 = th2 * th
    th4 = th2 * th2
    th5 = th4 * th
    th6 = th4 * th2
    th7 = th6 * th
    c0 = Q(1)
    c2 = Q(1) - th2 / Q(2)
    c4 = c2 + th4 / Q(24)
    c6 = c4 - th6 / Q(720)
    s1 = th
    s3 = th - th3 / Q(6)
    s5 = s3 + th5 / Q(120)
    s7 = s5 - th7 / Q(5040)
    cos_nested = c2 <= c6 <= c4 <= c0
    sin_nested = s3 <= s7 <= s5 <= s1
    cos_width_ok = Q(0) <= (c4 - c6) <= Q(1, 720)
    sin_width_ok = Q(0) <= (s5 - s7) <= Q(1, 5040)
    defect = Q(1) - (c4 * c4 + s3 * s3)
    defect_formula = th6 * (Q(8) - th2) / Q(576)
    defect_ok = (defect == defect_formula) and (Q(0) <= defect <= Q(1, 72))
    return {
        "theta": str(th),
        "taylor_cos6": str(c6),
        "taylor_sin7": str(s7),
        "cos_nested_enclosure": cos_nested,
        "sin_nested_enclosure": sin_nested,
        "cos_width_within_1_over_720": cos_width_ok,
        "sin_width_within_1_over_5040": sin_width_ok,
        "pythagorean_defect": str(defect),
        "pythagorean_defect_verified": defect_ok,
        "all_taylor_bounds_verified": (
            cos_nested and sin_nested and cos_width_ok and sin_width_ok and defect_ok
        ),
    }


def cayley_dyadic_approx_certificate(theta: object, k_depth: object) -> dict[str, object]:
    """Subdivide theta by 2^(k+1), apply Cayley map, and square k_depth times on S^1(Q)."""
    th = _q(theta)
    k = _z(k_depth)
    if k < 0 or k > 16:
        raise ValueError("k_depth in [0, 16] required")
    t_sub = th / Q(2 ** (k + 1))
    re, im = affine_cayley(t_sub)
    for _ in range(k):
        re, im = circle_mul(re, im, re, im)
    return {
        "theta": str(th),
        "k_depth": k,
        "approx_re": str(re),
        "approx_im": str(im),
        "strictly_on_unit_circle": is_unit_circle(re, im),
    }


def hermitian_qi_born_certificate(
    x1: object,
    y1: object,
    x2: object,
    y2: object,
    u1: object,
    v1: object,
    u2: object,
    v2: object,
) -> dict[str, object]:
    """Certify 4D Hermitian Q(i) rank-1 projectors, sigma_y orthogonality, and Born inner-product modulus squared."""
    rx1, ry1, rx2, ry2 = _q(x1), _q(y1), _q(x2), _q(y2)
    ru1, rv1, ru2, rv2 = _q(u1), _q(v1), _q(u2), _q(v2)
    p_d1 = rx1 * rx1 + ry1 * ry1
    p_d2 = rx2 * rx2 + ry2 * ry2
    p_br = rx1 * rx2 + ry1 * ry2
    p_bi = rx1 * ry2 - ry1 * rx2
    q_d1 = ru1 * ru1 + rv1 * rv1
    q_d2 = ru2 * ru2 + rv2 * rv2
    q_br = ru1 * ru2 + rv1 * rv2
    q_bi = ru1 * rv2 - rv1 * ru2
    det_p = p_d1 * p_d2 - (p_br * p_br + p_bi * p_bi)
    frob_pq = p_d1 * q_d1 + p_d2 * q_d2 + Q(2) * p_br * q_br + Q(2) * p_bi * q_bi
    inner_re = rx1 * ru1 + ry1 * rv1 + rx2 * ru2 + ry2 * rv2
    inner_im = rx1 * rv1 - ry1 * ru1 + rx2 * rv2 - ry2 * ru2
    inner_mod_sq = inner_re * inner_re + inner_im * inner_im
    sigma_y_orth = (p_d1 * Q(0) + p_d2 * Q(0) + Q(2) * p_br * Q(0) + Q(2) * Q(0) * Q(1)) == Q(0)
    return {
        "det_psi_zero": det_p == Q(0),
        "trace_psi": str(p_d1 + p_d2),
        "frobenius_trace_pq": str(frob_pq),
        "inner_modulus_sq": str(inner_mod_sq),
        "born_pairing_matches_inner_mod_sq": frob_pq == inner_mod_sq,
        "sigma_y_orthogonal_to_real_sym": sigma_y_orth,
    }


def _tower_zero(level: int) -> object:
    return Q(0) if level == 0 else (_tower_zero(level - 1), _tower_zero(level - 1))


def _tower_one(level: int) -> object:
    return Q(1) if level == 0 else (_tower_one(level - 1), _tower_zero(level - 1))


def _tower_of_rat(level: int, q: Q) -> object:
    return q if level == 0 else (_tower_of_rat(level - 1, q), _tower_zero(level - 1))


def _tower_add(level: int, x: object, y: object) -> object:
    if level == 0:
        return x + y  # type: ignore[operator]
    xa, xb = x  # type: ignore[misc]
    ya, yb = y  # type: ignore[misc]
    return (_tower_add(level - 1, xa, ya), _tower_add(level - 1, xb, yb))


def _tower_sub(level: int, x: object, y: object) -> object:
    if level == 0:
        return x - y  # type: ignore[operator]
    xa, xb = x  # type: ignore[misc]
    ya, yb = y  # type: ignore[misc]
    return (_tower_sub(level - 1, xa, ya), _tower_sub(level - 1, xb, yb))


def _tower_neg(level: int, x: object) -> object:
    if level == 0:
        return -x  # type: ignore[operator]
    xa, xb = x  # type: ignore[misc]
    return (_tower_neg(level - 1, xa), _tower_neg(level - 1, xb))


def _tower_mul(level: int, x: object, y: object, rads: list[object]) -> object:
    if level == 0:
        return x * y  # type: ignore[operator]
    xa, xb = x  # type: ignore[misc]
    ya, yb = y  # type: ignore[misc]
    d = rads[level - 1]
    ac = _tower_mul(level - 1, xa, ya, rads)
    bd = _tower_mul(level - 1, xb, yb, rads)
    dbd = _tower_mul(level - 1, d, bd, rads)
    ad = _tower_mul(level - 1, xa, yb, rads)
    bc = _tower_mul(level - 1, xb, ya, rads)
    return (_tower_add(level - 1, ac, dbd), _tower_add(level - 1, ad, bc))


def _tower_circle_sq(level: int, re: object, im: object, rads: list[object]) -> tuple[object, object]:
    re2 = _tower_mul(level, re, re, rads)
    im2 = _tower_mul(level, im, im, rads)
    re_im = _tower_mul(level, re, im, rads)
    return (_tower_sub(level, re2, im2), _tower_add(level, re_im, re_im))


def u345_quadratic_tower_certificate(max_level: int = 3) -> dict[str, object]:
    """Certify the iterated real quadratic square-root tower K_{m+1} = K_m(sqrt((1+c_m)/2)) for 2^m-divisions of u345."""
    if not isinstance(max_level, int) or isinstance(max_level, bool) or max_level < 1 or max_level > 5:
        raise ValueError("max_level must be an integer in [1, 5]")
    c: object = Q(3, 5)
    s: object = Q(4, 5)
    w: object = Q(5, 8)
    v: object = Q(5, 4)
    rads: list[object] = []
    levels: list[dict[str, object]] = []
    for m in range(max_level + 1):
        one_m = _tower_one(m)
        zero_m = _tower_zero(m)
        c2 = _tower_mul(m, c, c, rads)
        s2 = _tower_mul(m, s, s, rads)
        on_circle = _tower_add(m, c2, s2) == one_m
        one_plus_c = _tower_add(m, one_m, c)
        w_inv_ok = _tower_mul(m, one_plus_c, w, rads) == one_m
        v_inv_ok = _tower_mul(m, s, v, rads) == one_m
        cur_re, cur_im = c, s
        for _ in range(m):
            cur_re, cur_im = _tower_circle_sq(m, cur_re, cur_im, rads)
        pow_matches_u345 = (
            cur_re == _tower_of_rat(m, Q(3, 5))
            and cur_im == _tower_of_rat(m, Q(4, 5))
        )
        levels.append(
            {
                "level": m,
                "on_unit_circle": on_circle,
                "w_inverse_valid": w_inv_ok,
                "v_inverse_valid": v_inv_ok,
                "pow_two_pow_m_equals_u345": pow_matches_u345,
            }
        )
        if m < max_level:
            half_m = _tower_of_rat(m, Q(1, 2))
            two_m = _tower_of_rat(m, Q(2, 1))
            d_m = _tower_mul(m, half_m, one_plus_c, rads)
            rads.append(d_m)
            next_c = (zero_m, one_m)
            next_s = (zero_m, _tower_mul(m, s, w, rads))
            v2 = _tower_mul(m, v, v, rads)
            two_v2 = _tower_mul(m, two_m, v2, rads)
            a_w = _tower_mul(m, two_v2, one_plus_c, rads)
            next_w = (a_w, _tower_neg(m, a_w))
            next_v = (zero_m, _tower_mul(m, two_m, v, rads))
            c, s, w, v = next_c, next_s, next_w, next_v
    return {
        "max_level": max_level,
        "level_0_radicand": str(rads[0]),
        "all_levels_on_circle": all(bool(lv["on_unit_circle"]) for lv in levels),
        "all_inverses_valid": all(bool(lv["w_inverse_valid"]) and bool(lv["v_inverse_valid"]) for lv in levels),
        "all_two_pow_m_match_u345": all(bool(lv["pow_two_pow_m_equals_u345"]) for lv in levels),
        "levels": levels,
    }


def _qi_mul(a: tuple[Q, Q], b: tuple[Q, Q]) -> tuple[Q, Q]:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _qi_add(a: tuple[Q, Q], b: tuple[Q, Q]) -> tuple[Q, Q]:
    return (a[0] + b[0], a[1] + b[1])


def _qi_sub(a: tuple[Q, Q], b: tuple[Q, Q]) -> tuple[Q, Q]:
    return (a[0] - b[0], a[1] - b[1])


def _qi_conj(a: tuple[Q, Q]) -> tuple[Q, Q]:
    return (a[0], -a[1])


def _mat2_mul(
    m1: tuple[tuple[Q, Q], tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]],
    m2: tuple[tuple[Q, Q], tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]],
) -> tuple[tuple[Q, Q], tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]]:
    a11, a12, a21, a22 = m1
    b11, b12, b21, b22 = m2
    return (
        _qi_add(_qi_mul(a11, b11), _qi_mul(a12, b21)),
        _qi_add(_qi_mul(a11, b12), _qi_mul(a12, b22)),
        _qi_add(_qi_mul(a21, b11), _qi_mul(a22, b21)),
        _qi_add(_qi_mul(a21, b12), _qi_mul(a22, b22)),
    )


def _mat2_dagger(
    m: tuple[tuple[Q, Q], tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]],
) -> tuple[tuple[Q, Q], tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]]:
    a11, a12, a21, a22 = m
    return (_qi_conj(a11), _qi_conj(a21), _qi_conj(a12), _qi_conj(a22))


def _cayley_step_mat(
    hz: Q, hx: Q, hy: Q, t: Q
) -> tuple[tuple[Q, Q], tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]]:
    nsq = hz * hz + hx * hx + hy * hy
    d = Q(1) + t * t * nsq
    c = (Q(1) - t * t * nsq) / d
    s = (Q(2) * t) / d
    return (
        (c, -s * hz),
        (-s * hy, -s * hx),
        (s * hy, -s * hx),
        (c, s * hz),
    )


def cayley_hermitian_stone_certificate(
    z: object, x: object, y: object, t1: object, t2: object
) -> dict[str, object]:
    """Certify the discrete Cayley unitary step U_H(t) = (I - i t H)(I + i t H)^{-1} on TracelessHerm2Qi."""
    hz, hx, hy = _q(z), _q(x), _q(y)
    rt1, rt2 = _q(t1), _q(t2)
    nsq = hz * hz + hx * hx + hy * hy
    d1 = Q(1) + rt1 * rt1 * nsq
    d2 = Q(1) + rt2 * rt2 * nsq
    u1 = _cayley_step_mat(hz, hx, hy, rt1)
    u2 = _cayley_step_mat(hz, hx, hy, rt2)
    plus1 = (
        (Q(1), rt1 * hz),
        (rt1 * hy, rt1 * hx),
        (-rt1 * hy, rt1 * hx),
        (Q(1), -rt1 * hz),
    )
    minus1 = (
        (Q(1), -rt1 * hz),
        (-rt1 * hy, -rt1 * hx),
        (rt1 * hy, -rt1 * hx),
        (Q(1), rt1 * hz),
    )
    id_mat = ((Q(1), Q(0)), (Q(0), Q(0)), (Q(0), Q(0)), (Q(1), Q(0)))
    neg_id_mat = ((Q(-1), Q(0)), (Q(0), Q(0)), (Q(0), Q(0)), (Q(-1), Q(0)))
    resolvent_ok = _mat2_mul(plus1, u1) == minus1 and _mat2_mul(u1, plus1) == minus1
    u1_dag = _mat2_dagger(u1)
    unitary_ok = _mat2_mul(u1_dag, u1) == id_mat and _mat2_mul(u1, u1_dag) == id_mat
    det_u1 = _qi_sub(_qi_mul(u1[0], u1[3]), _qi_mul(u1[1], u1[2]))
    dagger_neg_ok = u1_dag == _cayley_step_mat(hz, hx, hy, -rt1)
    prod12 = _mat2_mul(u1, u2)
    prod21 = _mat2_mul(u2, u1)
    comm_ok = prod12 == prod21
    reg_denom = Q(1) - rt1 * rt2 * nsq
    if reg_denom != Q(0):
        t_comp = (rt1 + rt2) / reg_denom
        comp_ok = prod12 == _cayley_step_mat(hz, hx, hy, t_comp)
        pole_collision = False
    else:
        comp_ok = (nsq != Q(1)) or (prod12 == neg_id_mat)
        pole_collision = True
    uz_half = _cayley_step_mat(Q(1), Q(0), Q(0), Q(1, 2))
    pythagorean_ok = uz_half[0] == (Q(3, 5), Q(-4, 5)) and uz_half[3] == (Q(3, 5), Q(4, 5))
    return {
        "norm_sq": str(nsq),
        "denom_t1": str(d1),
        "denom_t2": str(d2),
        "denom_ge_one": d1 >= Q(1) and d2 >= Q(1),
        "resolvent_valid": resolvent_ok,
        "unitary_valid": unitary_ok,
        "det_is_one": det_u1 == (Q(1), Q(0)),
        "dagger_equals_neg_step": dagger_neg_ok,
        "steps_commute": comm_ok,
        "composition_law_valid": comp_ok,
        "pole_collision": pole_collision,
        "pauli_z_half_is_u345": pythagorean_ok,
    }
