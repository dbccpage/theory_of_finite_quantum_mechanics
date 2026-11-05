"""Exact constants of the thermodynamic-limit proof (all Fractions).

Each function returns the constant and asserts, in exact arithmetic, the
inequality the proof uses it for. The transcendental inputs enter only through
two rational bounds: e < 3, and e^x - 1 <= x / (1 - x) for 0 <= x < 1.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

E_UPPER = Fraction(3)


def expm1_upper(x: Fraction) -> Fraction:
    """Rational upper bound x/(1-x) for e^x - 1 on 0 <= x < 1."""
    if not 0 <= x < 1:
        raise ValueError("need 0 <= x < 1")
    return x / (1 - x)


def polymer_sum(label_norm: Fraction, degree: int) -> Fraction:
    """Rooted polymer majorant S = e t / (1 - 4 Delta e t), t = e^{label_norm} - 1.

    Requires 4 Delta e t < 1 and returns S after checking the
    Kotecky-Preiss condition (Delta + 1) S < 1.
    """
    et = E_UPPER * expm1_upper(label_norm)
    if not 4 * degree * et < 1:
        raise ArithmeticError("connected-set series diverges")
    s = et / (1 - 4 * degree * et)
    if not (degree + 1) * s < 1:
        raise ArithmeticError("Kotecky-Preiss condition fails")
    return s


@dataclass(frozen=True)
class Constants:
    s1: Fraction          # two-point gas majorant, label norm 1/128, degree 7
    m1: Fraction          # |C^L_{0y}| bound on |theta| <= 1/96
    s_f: Fraction         # one-source gas for F = <h_0>
    m_f: Fraction         # |F - theta/4| <= m_f (96 theta)^2
    s_g: Fraction         # B_0 / a_y gas, label norm 1/192, degree 11
    m_g: Fraction         # |<B_0(u) a_y>| bound on |theta| <= 1/144
    g_const: Fraction     # |g - 1/2| <= g_const * 288 |theta|
    theta_star: Fraction  # strict positivity window
    zero_mode_radius: Fraction  # k > 0 pointwise for theta below this


def compute() -> Constants:
    # Two-point gas: bonds (3/4)|theta| <= 1/128, sources |z|,|w| <= 1/64 (norm 1/2).
    assert Fraction(3, 4) * Fraction(1, 96) == Fraction(1, 128)
    assert Fraction(1, 64) * Fraction(1, 2) == Fraction(1, 128)
    s1 = polymer_sum(Fraction(1, 128), 7)
    assert s1 == Fraction(3, 43)
    m1 = 2 * s1 * 64 * 64
    assert m1 == Fraction(24576, 43)
    # F = <h_0>: one source s h_0, |s| <= 1/128, ||h_0|| = 1.
    s_f = polymer_sum(Fraction(1, 128), 7)
    f_bound = s_f * 128
    assert f_bound == Fraction(384, 43)
    m_f = f_bound + Fraction(1, 96) / 4
    # g: sources z B_0 (||B_0|| <= 3, |z| <= 1/576) and w a_y (|w| <= 1/96),
    # bonds (3/4)|theta| <= 1/192, so |theta| <= 1/144.
    assert 3 * Fraction(1, 576) == Fraction(1, 192)
    assert Fraction(1, 96) * Fraction(1, 2) == Fraction(1, 192)
    assert Fraction(3, 4) * Fraction(1, 144) == Fraction(1, 192)
    s_g = polymer_sum(Fraction(1, 192), 11)
    assert s_g == Fraction(3, 59)
    m_g = 2 * s_g * 576 * 96
    assert m_g == Fraction(331776, 59)
    # sum over y on |theta| <= 1/288 (ratio 144|theta| <= 1/2): 4 + 2 * 1 terms.
    g_const = 6 * m_g + Fraction(1, 2)
    theta_star = 1 / (4 * (18432 * m_f + 288 * g_const))
    zero_mode_radius = 1 / (768 * (3 * m1 + Fraction(1, 4)))
    return Constants(s1, m1, s_f, m_f, s_g, m_g, g_const, theta_star, zero_mode_radius)


def lift_error_bound(length: int, theta: Fraction) -> Fraction:
    """eps_L(theta) = 4 M_1 L (128 |theta|)^L, valid for |theta| < 1/128."""
    if not abs(theta) < Fraction(1, 128):
        raise ValueError("lift bound needs |theta| < 1/128")
    c = compute()
    # wrap sum: sum over n == y mod L of (3/4)^{|n|} <= 2/(1-(3/4)^4) = 512/175 < 3
    assert 2 / (1 - Fraction(3, 4) ** 4) == Fraction(512, 175)
    assert 1 + Fraction(512, 175) < 4
    return 4 * c.m1 * length * (128 * abs(theta)) ** length


def tail_bound(theta: Fraction, ratio_e_mu: Fraction) -> Fraction:
    """sup_{L,u} sum_y e^{mu d}|C| <= M_1 (1+q)/(1-q), q = 96|theta| e^mu < 1.

    ``ratio_e_mu`` is a rational upper bound for e^mu.
    """
    q = 96 * abs(theta) * ratio_e_mu
    if not q < 1:
        raise ValueError("need 96 |theta| e^mu < 1")
    return compute().m1 * (1 + q) / (1 - q)


def embedding_lift_factor() -> Fraction:
    """(128^2 theta / 96)^{1/2} squared at theta = 1/192: 128^2/(96*192) = 8/9.

    In TL-7 the lift error at a window site is e^{mu|n|}|D_n| <= 4M_1 (128 theta)^L e^{mu L/2}
    = 4M_1 q^{L/2} (128^2 theta/96)^{L/2} <= 4M_1 q^{L/2} (8/9)^{L/2} on 0 <= theta <= 1/192.
    """
    return Fraction(128 * 128, 96 * 192)


def embedding_bound(length: int, theta: Fraction, ratio_e_mu: Fraction) -> Fraction:
    """||E_L - C^infty||_mu <= M_1 q^{L/2} (4L + 4/(1 - q)), q = 96|theta| e^mu.

    Valid for |theta| <= 1/192, e^mu >= 1, q < 1 and even L >= 4. Three parts:
    the lift error at the L window sites (at most 4M_1 q^{L/2} each, by
    ``embedding_lift_factor``), the wrapped images (each m outside the window once,
    e^{mu|n|}|C_{0m}| <= M_1 q^{|m|} since |n| <= |m|), and the tail outside the window.
    The last two are each at most 2 M_1 q^{L/2}/(1 - q).
    """
    if not (abs(theta) <= Fraction(1, 192) and length >= 4 and length % 2 == 0):
        raise ValueError("embedding bound needs |theta| <= 1/192 and even L >= 4")
    if ratio_e_mu < 1:
        raise ValueError("need e^mu >= 1")
    q = 96 * abs(theta) * ratio_e_mu
    if not q < 1:
        raise ValueError("need 96 |theta| e^mu < 1")
    return compute().m1 * q ** (length // 2) * (4 * length + 4 / (1 - q))


def as_json() -> dict[str, str]:
    c = compute()
    return {k: f"{v.numerator}/{v.denominator}" for k, v in c.__dict__.items()}
