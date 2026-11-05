"""Exact rational schedule for one constant profile, not an extinction theorem.

Carrier: L=4 periodic CAR, Fock dimension 16, psi_x(tau)=1, theta=1/10, B=1, D=0.
Majorants E_4=(80/79)^32 and E_16=(20/19)^32. Margin m=79^32/(4*80^32).
Numerator A=4*(30*(theta+theta^2)*E_16+2*theta*E_4). Recorded threshold M_0=415.
The one-point Trotter record stays a separate negative verification.
"""

from __future__ import annotations

from fractions import Fraction

_L = 4
_FOCK = 16
_THETA = Fraction(1, 10)
_B = 1
_D = 0
_M0 = 415
_ONE_POINT_EIGENVALUE = Fraction(-1, 706440)
_ONE_POINT_QUADRATIC = Fraction(-1, 88305)
_EDGE_LAMBDA = Fraction(-1, 87426958080)


def _rational(value: object, name: str) -> Fraction:
    if type(value) is int:
        return Fraction(value)
    if type(value) is not Fraction:
        raise ValueError(f"{name} is not an exact rational")
    return value


def _majorants(theta: Fraction) -> tuple[Fraction, Fraction]:
    if not 0 <= theta <= 1:
        raise ValueError("refused: theta is outside the declared compact range")
    e4 = (1 - Fraction(4) * theta / 32) ** (-32)
    e16 = (1 - Fraction(16) * theta / 32) ** (-32)
    return e4, e16


def _one_point() -> tuple[Fraction, Fraction, Fraction]:
    eigenvalue = _ONE_POINT_EIGENVALUE
    quadratic = _ONE_POINT_QUADRATIC
    if 8 * eigenvalue != quadratic or 8 * 88305 != 706440:
        raise RuntimeError("one-point Rayleigh identity failed")
    edge_r = Fraction(1, 192)
    denominator = 4 * (edge_r + 2) * (edge_r ** 2 + 4 * edge_r + 8)
    if denominator != Fraction(455348740, 192 ** 3) or 192 * 455348740 != 87426958080:
        raise RuntimeError("edge denominator identity failed")
    edge = -(edge_r ** 4) / denominator
    if edge != _EDGE_LAMBDA or edge >= 0 or eigenvalue >= 0 or quadratic >= 0:
        raise RuntimeError("one-point record is not the recorded negative verification")
    if not (_THETA > edge_r):
        raise RuntimeError("recorded point is not outside r<=1/192")
    return eigenvalue, quadratic, edge


def schedule(
    theta: object = _THETA,
    sites: object = _L,
    amplitude: object = _B,
    derivative: object = _D,
) -> dict[str, int | Fraction]:
    """Rational A, m, and M_0 on the selected constant profile only."""

    if type(sites) is not int:
        raise ValueError("L is not an exact integer")
    if sites != _L:
        raise ValueError("refused: L is outside the selected scope")
    theta_q = _rational(theta, "theta")
    amplitude_q = _rational(amplitude, "amplitude")
    derivative_q = _rational(derivative, "derivative")
    if theta_q != _THETA or amplitude_q != _B or derivative_q != _D:
        raise ValueError("refused: profile is outside the selected constant schedule")
    e4, e16 = _majorants(theta_q)
    if e4 != Fraction(80, 79) ** 32 or e16 != Fraction(20, 19) ** 32:
        raise RuntimeError("rational majorant does not match the closed form")
    margin = 1 / (4 * e4)
    if margin != Fraction(79 ** 32, 4 * 80 ** 32):
        raise RuntimeError("margin does not match 79^32/(4*80^32)")
    if margin.numerator != 79 ** 32 or margin.denominator != (2 ** 98) * (10 ** 32):
        raise RuntimeError("margin is not the reduced fraction 79^32/(2^98*10^32)")
    if 80 ** 32 != (2 ** 96) * (10 ** 32) or 4 * 80 ** 32 != margin.denominator:
        raise RuntimeError("80^32 denominator identity failed")
    numerator = 4 * (30 * (theta_q + theta_q ** 2) * e16 + 2 * theta_q * e4)
    if type(numerator) is not Fraction or type(margin) is not Fraction:
        raise RuntimeError("schedule left the rationals")
    if numerator <= 0 or margin <= 0:
        raise RuntimeError("numerator and margin must be positive")
    quotient = numerator // margin
    m0 = max(1, quotient + 1)
    if type(quotient) is not int or type(m0) is not int:
        raise RuntimeError("threshold left the integers")
    if m0 != _M0 or quotient != _M0 - 1:
        raise RuntimeError("recorded strict threshold was not reproduced")
    if not (m0 * margin > numerator and (m0 - 1) * margin <= numerator):
        raise RuntimeError("strict margin comparison failed")
    return {
        "theta": theta_q,
        "B": _B,
        "D": _D,
        "E4": e4,
        "E16": e16,
        "margin": margin,
        "numerator": numerator,
        "M0": m0,
        "floor_quotient": quotient,
    }


def witness() -> dict[str, int | Fraction]:
    row = schedule()
    eigenvalue, quadratic, edge = _one_point()
    if eigenvalue == row["margin"] or quadratic == row["margin"] or edge == row["margin"]:
        raise RuntimeError("one-point value was reused as the margin")
    return {
        "L": _L,
        "fock": _FOCK,
        "theta": row["theta"],
        "B": row["B"],
        "D": row["D"],
        "E4": row["E4"],
        "E16": row["E16"],
        "margin": row["margin"],
        "numerator": row["numerator"],
        "M0": row["M0"],
        "floor_quotient": row["floor_quotient"],
        "one_point_eigenvalue": eigenvalue,
        "one_point_quadratic": quadratic,
        "edge_lambda": edge,
        "one_point_psd": 0,
        "one_point_outside_edge": 1,
        "edge_is_positivity_certificate": 0,
        "g_m_positive": 0,
        "field_limit_extinction": 0,
        "beyond_one_point_closed": 0,
        "continuum_limit": 0,
    }


def refuse_extinction_or_positivity(claim: object) -> None:
    """Extinction or positivity beyond the one-point record stays open."""

    if type(claim) is not str or claim == "":
        raise ValueError("claim label is not a nonempty string")
    if claim == "one-point-record":
        raise ValueError(
            "refused: the one-point record is a negative verification at M=1, "
            "not positivity of G_M and not a field-limit extinction theorem"
        )
    raise ValueError(
        "refused: an extinction or positivity claim that is not the one-point "
        "Trotter-response verification record stays open"
    )


def refuse_gate_e_matrix() -> None:
    raise ValueError("refused: the Gate E matrix at M=1 is outside this schedule")


def refuse_higher_dimensional_sum(dimension: object, term: object) -> None:
    """The one-point eigenvalue is one scalar, not a sum over an 8M matrix."""

    if type(dimension) is not int:
        raise ValueError("dimension is not an integer")
    if type(term) is int:
        term = Fraction(term)
    if type(term) is not Fraction:
        raise ValueError("term is not an exact rational")
    if dimension != 1:
        raise ValueError("do not copy a 1D constant into a higher-dimensional sum")
    if term != _ONE_POINT_EIGENVALUE:
        raise ValueError("term is not the one-point eigenvalue")


def refuse_continuum() -> None:
    raise ValueError("refused: a finite carrier does not establish a continuum limit")
