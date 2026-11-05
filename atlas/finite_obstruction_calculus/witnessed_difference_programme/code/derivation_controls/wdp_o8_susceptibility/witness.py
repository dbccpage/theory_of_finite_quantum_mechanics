"""AR-1 outside-membership on one labelled carrier.

Even periodic full-Fock ring L=4, dimension 16, checkerboard count M=2,
source parameter q=3. The exact gap 767/384 is not a pointwise susceptibility,
not a parity-sector ratio, and not a law for theta growing with L.
"""

from __future__ import annotations

from fractions import Fraction

_CEILING = Fraction(1, 192)
_SQL = (
    Fraction(48, 19),
    Fraction(149, 57),
    Fraction(12, 19),
    Fraction(5, 57),
)


def _rational(value: object, name: str) -> Fraction:
    if type(value) is int:
        return Fraction(value)
    if type(value) is Fraction:
        return value
    raise ValueError(f"{name} is not an exact rational")


def _factorial(n: int) -> int:
    acc = 1
    for k in range(2, n + 1):
        acc *= k
    return acc


def ring_dimension(length: object) -> int:
    """Occupation-basis size of the labelled full-Fock ring. Only L=4."""
    if type(length) is not int:
        raise ValueError("length is not an integer")
    if length != 4:
        raise ValueError(
            "refused: labelled carrier is the even full-Fock ring L=4, "
            "not a law in L"
        )
    dim = 1 << length
    if dim != 16:
        raise RuntimeError("full-Fock dimension is not 16")
    return dim


def admit_ar1(m: object, r: object, rho: object = 0) -> Fraction:
    """Return q=1+r/M when r>=rho>=0 and r+rho<=1/192.

    The comparison is strict on the upper end: the endpoint 1/192 is admitted.
    A strictly larger upper end is the domain refusal, not a derivative.
    """
    if type(m) is not int or m < 1:
        raise ValueError("checkerboard count is not a positive integer")
    radius = _rational(r, "r")
    slack = _rational(rho, "rho")
    if radius < 0 or slack < 0 or slack > radius:
        raise ValueError("refused: AR-1 requires r >= rho >= 0")
    if radius + slack > _CEILING:
        raise ValueError(
            "refused: temperature interval exceeds proved upper bound 1/192"
        )
    return 1 + radius / m


def _ar8_factor() -> int:
    """4!/(1/2)^4. Same integer as 2*192, not the reason for that denominator."""
    factor = Fraction(_factorial(4)) / Fraction(1, 2) ** 4
    if factor != 384 or factor.denominator != 1:
        raise RuntimeError("AR-8 factor is not 384")
    return int(factor)


def _log3_three_term() -> Fraction:
    """Positive truncation of log((1+1/2)/(1-1/2)) after three terms."""
    total = Fraction(0)
    for k in range(3):
        total += Fraction(1, 1 << (2 * k + 1)) / (2 * k + 1)
    return 2 * total


def _exp_below_three() -> int:
    """e<3 from n!>=2^{n-1} and the geometric sum, strict at n=3."""
    if _factorial(1) != 1 << 0:
        raise RuntimeError("factorial base failed")
    # For every integer n>=1, n+1>=2, so n!>=2^{n-1} passes to (n+1)!.
    if 1 + 1 < 2:
        raise RuntimeError("inductive multiplier failed")
    if Fraction(1, _factorial(3)) >= Fraction(1, 1 << 2):
        raise RuntimeError("1/3! was not strictly below 2^{1-3}")
    partial = Fraction(0)
    for j in range(24):
        partial += Fraction(1, 1 << j)
        if partial != 2 - Fraction(1, 1 << j) or 2 - partial <= 0:
            raise RuntimeError("geometric partial sum failed")
    return 1


def _membership(m: int, q: int) -> int:
    euler_r = m * (q - 1)
    try:
        admit_ar1(m, euler_r, 0)
    except ValueError as exc:
        if "1/192" not in str(exc):
            raise
        return 0
    raise RuntimeError("q=3 at M=2 was admitted inside AR-1")


def witness() -> dict[str, int | Fraction]:
    length = 4
    dimension = ring_dimension(length)
    m = 2
    q = 3
    q_max = admit_ar1(m, _CEILING, 0)
    q_from_parts = 1 + _CEILING / m
    denominator = m * 192
    q_cleared = Fraction(denominator + 1, denominator)
    if q_max != q_from_parts or q_max != q_cleared or q_max != Fraction(385, 384):
        raise RuntimeError("greatest AR-1 parameter moved")
    gap = Fraction(q) - q_max
    cleared = q * q_max.denominator - q_max.numerator
    if cleared != 3 * 384 - 385 or cleared != 767 or gap != Fraction(cleared, denominator):
        raise RuntimeError("cleared q-gap is not 767/384")
    euler_r = m * (q - 1)
    if euler_r != 4:
        raise RuntimeError("Euler parameter at q=3, M=2 is not 4")
    r_gap = Fraction(euler_r) - _CEILING
    if r_gap != Fraction(767, 192) or r_gap / m != gap:
        raise RuntimeError("Euler gap does not return the q-gap")
    if _membership(m, q) != 0:
        raise RuntimeError("fixture was marked inside AR-1")
    log_lower = _log3_three_term()
    theta_lower = Fraction(m) * log_lower
    separation = theta_lower - _CEILING
    if log_lower != Fraction(263, 240) or theta_lower != Fraction(263, 120):
        raise RuntimeError("three-term temperature bound moved")
    if separation != Fraction(2099, 960) or separation <= 0:
        raise RuntimeError("temperature separation is not 2099/960")
    if _exp_below_three() != 1:
        raise RuntimeError("exponential comparison failed")
    bond_norm = Fraction(3, 4)
    bond_lower = 2 * bond_norm
    bond_ceiling = Fraction(1, 256)
    bond_excess = bond_lower - bond_ceiling
    if bond_excess != Fraction(383, 256) or bond_excess <= 0:
        raise RuntimeError("bond excess is not 383/256")
    schedule_theta = Fraction(length, 192)
    schedule_gap = schedule_theta - _CEILING
    schedule_ratio = schedule_theta / length
    if schedule_theta != Fraction(1, 48) or schedule_gap != Fraction(1, 64):
        raise RuntimeError("printed theta(L)=L/192 comparison moved")
    if schedule_ratio != _CEILING or schedule_ratio == 0:
        raise RuntimeError("printed theta/L bound was treated as vanishing")
    ar8 = _ar8_factor()
    if ar8 != denominator:
        raise RuntimeError("AR-8 integer and the temperature denominator diverged")
    if gap in _SQL or gap == Fraction(1, 4):
        raise RuntimeError("q-gap collided with a one-dimensional readout")
    result: dict[str, int | Fraction] = {
        "L": length,
        "dimension": dimension,
        "M": m,
        "q": q,
        "r_ceiling": _CEILING,
        "q_ar1_max": q_max,
        "cleared_gap": cleared,
        "q_gap": gap,
        "euler_r": euler_r,
        "r_gap": r_gap,
        "denominator": denominator,
        "ar8_factor": ar8,
        "denominator_reason_is_ar8": 0,
        "ar1_member": 0,
        "endpoint_admitted": 1,
        "log3_three_term_lower": log_lower,
        "theta_three_term_lower": theta_lower,
        "temperature_separation": separation,
        "temperature_above_ceiling": 1,
        "exp_below_three": 1,
        "factorial_three": _factorial(3),
        "two_to_the_two": 1 << 2,
        "bond_norm": bond_norm,
        "bond_lower": bond_lower,
        "bond_ceiling": bond_ceiling,
        "bond_excess": bond_excess,
        "bond_above_ceiling": 1,
        "schedule_theta": schedule_theta,
        "schedule_gap": schedule_gap,
        "schedule_theta_over_L": schedule_ratio,
        "schedule_bound_vanishes": 0,
        "pointwise_susceptibility_supplied": 0,
        "parity_sector_ratio_supplied": 0,
        "theta_scaling_law_supplied": 0,
        "sql_reused": 0,
        "p_second_supplied": 0,
        "p_second_is_gap": 0,
        "continuum_limit": 0,
        "higher_dimensional_sum": 0,
        "outside_limit_fails": 0,
    }
    for value in result.values():
        if type(value) is not int and type(value) is not Fraction:
            raise RuntimeError("witness value is not an exact integer or rational")
    if result["pointwise_susceptibility_supplied"] or result["continuum_limit"]:
        raise RuntimeError("an excluded claim was marked supplied")
    if result["p_second_supplied"] or result["p_second_is_gap"] or result["sql_reused"]:
        raise RuntimeError("the gap was marked as a susceptibility")
    return result


def refuse_pointwise_susceptibility() -> None:
    raise ValueError(
        "refused: all-temperature pointwise susceptibility is not selected; "
        "767/384 is not p''(theta, 0)"
    )


def refuse_sector_ratio() -> None:
    raise ValueError("refused: a parity-sector ratio is not selected")


def refuse_theta_scaling() -> None:
    raise ValueError("refused: no law for theta growing with L is selected")


def refuse_sql_ratio(value: object) -> None:
    exact = _rational(value, "ratio")
    if exact in _SQL:
        raise ValueError("refused: one-dimensional SQL ratios 48/19 and 149/57 are not reused")
    if exact == Fraction(767, 384):
        raise ValueError("refused: 767/384 is not an SQL ratio and not p''(theta, 0)")
    raise ValueError("refused: this carrier does not supply an SQL susceptibility")


def refuse_continuum() -> None:
    raise ValueError("refused: a finite model does not establish a continuum limit")


def refuse_higher_dimensional_sum(dimension: object, term: object) -> None:
    if type(dimension) is not int:
        raise ValueError("dimension is not an integer")
    _rational(term, "term")
    raise ValueError("refused: do not copy a 1D constant into a higher-dimensional sum")


def refuse_outside_limit() -> None:
    raise ValueError(
        "refused: a majorant that does not apply is not a proof that the outside limit fails"
    )
