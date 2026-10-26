"""Finite L=4, M=1, r=0 cumulants. Not a spacetime Gaussian field.

TD-2a identity layers and the TD-6 scaling of Phi on the 16-state
periodic occupation basis. Constant and alternating profiles are
evaluated by that trace. No continuum limit is computed.
"""

from __future__ import annotations

from fractions import Fraction

_L = 4
_M = 1
_R = Fraction(0)
_R_MAX = Fraction(1, 192)
_FOCK = 1 << _L
_HALF = 2 * _M
_CHI0 = Fraction(1, 4)
_ONE_SITE_KAPPA_2 = Fraction(1, 16)

Profile = tuple[tuple[Fraction, ...], tuple[Fraction, ...]]


def _factorial(n: int) -> int:
    value = 1
    for factor in range(2, n + 1):
        value *= factor
    return value


def _binom(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    value = 1
    for i in range(k):
        value = value * (n - i) // (i + 1)
    return value


def _sqrt_l() -> int:
    root = 2
    if root * root != _L:
        raise RuntimeError("L=4 does not have integer square root 2")
    return root


def _scale() -> int:
    scale = 2 * _M * _sqrt_l()
    if scale != 4:
        raise RuntimeError("TD-6 denominator is not 4")
    return scale


def _a(state: int, site: int) -> Fraction:
    if not 0 <= state < _FOCK or not 0 <= site < _L:
        raise RuntimeError("index left the occupation basis")
    occupation = (state >> site) & 1
    sign = 1 if site % 2 == 0 else -1
    return Fraction(sign) * (Fraction(occupation) - Fraction(1, 2))


def _layer(out_state: int, in_state: int) -> int:
    """TD-2a at r=0: every layer is the identity."""
    if out_state == in_state:
        return 1
    return 0


def _history_weight(s0: int, s1: int) -> int:
    # Periodic product <s1|T_0|s0><s0|T_1|s1> with both layers the identity.
    return _layer(s1, s0) * _layer(s0, s1)


def _zero_source_factor() -> int:
    q = Fraction(1) + _R / _M
    if q != 1:
        raise RuntimeError("decoupled control is not q=1")
    if _L * _M != 4:
        raise RuntimeError("LM/4 is not 1")
    return 1


def _constant() -> Profile:
    row = tuple(Fraction(1) for _ in range(_L))
    return (row, row)


def _alternating() -> Profile:
    plus = tuple(Fraction(1) for _ in range(_L))
    minus = tuple(Fraction(-1) for _ in range(_L))
    return (plus, minus)


def _one_site() -> Profile:
    row = tuple(Fraction(1) if site == 0 else Fraction(0) for site in range(_L))
    return (row, row)


def _phi(profile: Profile, s0: int, s1: int) -> Fraction:
    states = (s0, s1)
    total = Fraction(0)
    for step, state in enumerate(states):
        for site in range(_L):
            total += profile[step][site] * _a(state, site)
    return total / _scale()


def _sigma(profile: Profile, site: int) -> Fraction:
    acc = profile[0][site] + profile[1][site]
    return acc / (4 * _M * _sqrt_l())


def _log_cosh_derivatives() -> tuple[Fraction, Fraction]:
    """Second and fourth derivatives of log cosh at 0, degree 4 exact."""
    w2 = Fraction(1, 2)
    w4 = Fraction(1, 24)
    a2 = w2
    a4 = w4 - (w2 * w2) / 2
    second = a2 * _factorial(2)
    fourth = a4 * _factorial(4)
    expected = (Fraction(1, 2), Fraction(-1, 12), Fraction(1), Fraction(-2))
    if (a2, a4, second, fourth) != expected:
        raise RuntimeError("log cosh derivatives at 0 are not 1 and -2")
    return second, fourth


def _cumulants_from_moments(moments: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    if moments[0] != 1:
        raise RuntimeError("raw moment mu_0 is not 1")
    order = len(moments) - 1
    kappa = [Fraction(0) for _ in range(order + 1)]
    kappa[1] = moments[1]
    for n in range(2, order + 1):
        correction = Fraction(0)
        for m in range(1, n):
            correction += Fraction(_binom(n - 1, m - 1)) * kappa[m] * moments[n - m]
        kappa[n] = moments[n] - correction
    return tuple(kappa[1:])


def _fock_moments(profile: Profile, order: int = 4) -> tuple[Fraction, ...]:
    values: list[Fraction] = []
    weighted = 0
    for s0 in range(_FOCK):
        for s1 in range(_FOCK):
            weight = _history_weight(s0, s1)
            if weight == 0:
                continue
            if weight != 1:
                raise RuntimeError("identity-layer weight is not 1")
            values.append(_phi(profile, s0, s1))
            weighted += 1
    if weighted != _FOCK or len(values) != _FOCK:
        raise RuntimeError("weighted histories are not the 16 occupation states")
    moments = [Fraction(1)]
    for n in range(1, order + 1):
        total = Fraction(0)
        for value in values:
            total += value ** n
        moments.append(total / Fraction(weighted))
    return tuple(moments)


def _sigma_cumulants(profile: Profile) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    second, fourth = _log_cosh_derivatives()
    sum2 = Fraction(0)
    sum4 = Fraction(0)
    for site in range(_L):
        item = _sigma(profile, site)
        sum2 += item * item
        sum4 += item ** 4
    return (Fraction(0), second * sum2, Fraction(0), fourth * sum4)


def _evaluate(profile: Profile) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    moments = _fock_moments(profile)
    got = _cumulants_from_moments(moments)
    predicted = _sigma_cumulants(profile)
    if got != predicted:
        raise RuntimeError("Fock cumulants disagree with the TD-2a logarithm")
    return got, moments


def _check_basis() -> None:
    if _FOCK != 16 or _HALF != 2:
        raise RuntimeError("carrier is not 16 Fock states and 2 half-steps")
    if not 0 <= _R <= _R_MAX:
        raise RuntimeError("r left 0<=r<=1/192")
    if _a(0, 0) != Fraction(-1, 2) or _a(1, 0) != Fraction(1, 2):
        raise RuntimeError("a_0 is not n_0-1/2 on the occupation basis")
    for state in range(_FOCK):
        for site in range(_L):
            if _a(state, site) ** 2 != Fraction(1, 4):
                raise RuntimeError("a_x squared is not 1/4")
        complement = state ^ (_FOCK - 1)
        if _phi(_constant(), state, state) + _phi(_constant(), complement, complement) != 0:
            raise RuntimeError("particle-hole did not reverse the constant profile")
    for site in range(_L):
        empty = sum(1 for state in range(_FOCK) if ((state >> site) & 1) == 0)
        if empty != 8:
            raise RuntimeError("occupation basis is not balanced")


def _check_profiles() -> None:
    constant = _constant()
    alternating = _alternating()
    for s0 in range(_FOCK):
        for s1 in range(_FOCK):
            direct_constant = Fraction(0)
            direct_alternating = Fraction(0)
            for site in range(_L):
                direct_constant += _a(s0, site) + _a(s1, site)
                direct_alternating += _a(s0, site) - _a(s1, site)
            if _phi(constant, s0, s1) != direct_constant / 4:
                raise RuntimeError("constant Phi left the TD-6 formula")
            if _phi(alternating, s0, s1) != direct_alternating / 4:
                raise RuntimeError("alternating Phi left the TD-6 formula")
    if tuple(_sigma(constant, site) for site in range(_L)) != (Fraction(1, 4),) * _L:
        raise RuntimeError("constant sigma is not 1/4 at every site")
    if tuple(_sigma(alternating, site) for site in range(_L)) != (Fraction(0),) * _L:
        raise RuntimeError("alternating sigma is not 0")


def _trace_counts() -> tuple[int, int, int]:
    weighted = 0
    off = 0
    for s0 in range(_FOCK):
        for s1 in range(_FOCK):
            if _history_weight(s0, s1):
                weighted += 1
            else:
                off += 1
    trace = _zero_source_factor() * weighted
    if trace != 16 or weighted != 16 or off != 240:
        raise RuntimeError("zero-source trace is not 16 on 256 histories")
    return trace, weighted, off


def _alternating_support() -> tuple[int, Fraction, int, int, Fraction]:
    profile = _alternating()
    zero_supported = 0
    phi_sum = Fraction(0)
    nonzero_off = 0
    zero_off = 0
    for s0 in range(_FOCK):
        for s1 in range(_FOCK):
            value = _phi(profile, s0, s1)
            if _history_weight(s0, s1):
                phi_sum += value
                if value != 0:
                    raise RuntimeError("alternating Phi is nonzero on a weighted history")
                zero_supported += 1
            elif value == 0:
                zero_off += 1
            else:
                nonzero_off += 1
    example = _phi(profile, 0, 1)
    if _history_weight(0, 1) != 0:
        raise RuntimeError("history (0,1) is not off support")
    if zero_supported != 16 or phi_sum != 0:
        raise RuntimeError("alternating support is not identically zero")
    return zero_supported, phi_sum, nonzero_off, zero_off, example


def _sup(profile: Profile) -> Fraction:
    values = [abs(profile[step][site]) for step in range(_HALF) for site in range(_L)]
    return max(values)


def _time_independent(profile: Profile) -> int:
    if all(profile[0][site] == profile[1][site] for site in range(_L)):
        return 1
    return 0


def _schedule() -> tuple[int, int, int]:
    target = _L // 4
    k = 1
    while k ** 4 < target:
        k += 1
        if k > _L:
            raise RuntimeError("schedule root exceeded L")
    if 4 * (k ** 4) != _L:
        raise RuntimeError("L is not 4k^4")
    required_m = _L * _L
    matched = 1 if _M == required_m else 0
    return matched, k, required_m


def _printed_second_majorant(norm: Fraction) -> Fraction:
    if norm != 1:
        raise RuntimeError("selected sup norm is not 1")
    # Printed TD-7 at n=2, R=1/64, C_0=1/19, L^{0}=1. Not a polymer re-proof.
    bound = Fraction(2, 19) * _factorial(2) * (64 ** 2)
    if bound != Fraction(16384, 19):
        raise RuntimeError("printed second majorant is not 16384/19")
    return bound


def _inside(value: Fraction, bound: Fraction) -> int:
    if -bound < value < bound and value != bound and value != -bound:
        return 1
    return 0


def _static_member(profile: Profile, on_schedule: int) -> int:
    if _time_independent(profile) != 1 or on_schedule != 1:
        return 0
    raise RuntimeError('a finite label array is not the H^{-s}(T) law')


def witness() -> dict[str, int | Fraction]:
    _check_basis()
    _check_profiles()
    trace, weighted, off = _trace_counts()
    supported, phi_sum, nonzero_off, zero_off, example = _alternating_support()
    constant_k, constant_m = _evaluate(_constant())
    alternating_k, alternating_m = _evaluate(_alternating())
    one_site_k, _one_site_m = _evaluate(_one_site())
    if one_site_k[1] == constant_k[1]:
        raise RuntimeError("one-site cumulant was copied onto the four-site profile")
    on_schedule, schedule_k, schedule_m = _schedule()
    bound = _printed_second_majorant(_sup(_constant()))
    if _sup(_alternating()) != 1:
        raise RuntimeError("alternating sup norm is not 1")
    constant_in = _inside(constant_k[1], bound)
    alternating_in = _inside(alternating_k[1], bound)
    if constant_in != 1 or alternating_in != 1:
        raise RuntimeError("exact second cumulant left the printed majorant")
    if bound == constant_k[1] or bound == alternating_k[1]:
        raise RuntimeError("majorant equals a cumulant")
    if alternating_k != (Fraction(0), Fraction(0), Fraction(0), Fraction(0)):
        raise RuntimeError("alternating cumulants through order 4 did not vanish")
    if phi_sum != 0 or supported != weighted:
        raise RuntimeError("vanishing cumulants were not the zero observable")
    alternating_time = _time_independent(_alternating())
    constant_time = _time_independent(_constant())
    alternating_member = _static_member(_alternating(), on_schedule)
    if alternating_time != 0 or alternating_member != 0 or on_schedule != 0:
        raise RuntimeError("alternating profile entered the static input class")
    if constant_k[1] == alternating_k[1]:
        raise RuntimeError("constant and alternating second cumulants coincide")
    chi_equals_constant = 1 if constant_k[1] == _CHI0 else 0
    chi_equals_alternating = 1 if alternating_k[1] == _CHI0 else 0
    gaussian_fourth = Fraction(0)
    fourth_is_gaussian = 1 if constant_k[3] == gaussian_fourth else 0
    return {
        "L": _L,
        "M": _M,
        "r": _R,
        "r_max": _R_MAX,
        "r_inside_disk": 1,
        "fock": _FOCK,
        "half_steps": _HALF,
        "sites": _L,
        "labels": _HALF * _L,
        "sqrt_L": _sqrt_l(),
        "scale_denominator": _scale(),
        "zero_source_trace": trace,
        "weighted_histories": weighted,
        "off_support_histories": off,
        "layers_identity": 1,
        "constant_kappa_1": constant_k[0],
        "constant_kappa_2": constant_k[1],
        "constant_kappa_3": constant_k[2],
        "constant_kappa_4": constant_k[3],
        "constant_mu_2": constant_m[2],
        "constant_mu_4": constant_m[4],
        "one_site_kappa_2": one_site_k[1],
        "one_site_kappa_4": one_site_k[3],
        "carrier_kappa_is_one_site": 0,
        "alternating_supported_zero_count": supported,
        "alternating_supported_phi_sum": phi_sum,
        "alternating_kappa_1": alternating_k[0],
        "alternating_kappa_2": alternating_k[1],
        "alternating_kappa_3": alternating_k[2],
        "alternating_kappa_4": alternating_k[3],
        "alternating_mu_2": alternating_m[2],
        "alternating_every_cumulant_zero": 1,
        "alternating_off_support_nonzero": nonzero_off,
        "alternating_off_support_zero": zero_off,
        "alternating_off_support_phi": example,
        "alternating_off_support_weight": 0,
        "chi_0": _CHI0,
        "chi_equals_constant_kappa_2": chi_equals_constant,
        "chi_equals_alternating_kappa_2": chi_equals_alternating,
        "constant_fourth_is_gaussian": fourth_is_gaussian,
        "gaussian_fourth": gaussian_fourth,
        "constant_time_independent": constant_time,
        "alternating_time_independent": alternating_time,
        "schedule_k": schedule_k,
        "schedule_L": 4 * (schedule_k ** 4),
        "schedule_M": schedule_m,
        "on_static_schedule": on_schedule,
        "alternating_in_static_class": alternating_member,
        "majorant_kappa_2": bound,
        "constant_inside_majorant": constant_in,
        "alternating_inside_majorant": alternating_in,
        "majorant_equals_constant_kappa_2": 1 if bound == constant_k[1] else 0,
        "majorant_equals_alternating_kappa_2": 1 if bound == alternating_k[1] else 0,
        "joint_spacetime_field_limit": 0,
        "continuum_limit": 0,
    }


def refuse_joint_spacetime_field() -> None:
    raise ValueError(
        "refused: static Gaussian and bounded time-labelled cumulant results "
        "are not a joint spacetime field limit"
    )


def refuse_continuum() -> None:
    raise ValueError("refused: a finite model does not establish a continuum limit")


def refuse_static_membership(profile_name: object) -> None:
    if type(profile_name) is not str:
        raise ValueError("profile name is not a string")
    if profile_name == "alternating":
        raise ValueError(
            "refused: the static Gaussian input class does not contain the "
            "alternating 8-label profile"
        )
    if profile_name == "constant":
        raise ValueError(
            "refused: (L,M)=(4,1) is not the schedule M=L^2 and kappa_4=-1/32 "
            "is not a Gaussian field"
        )
    raise ValueError("refused: profile is outside the selected scope")


def refuse_higher_dimensional_sum(dimension: object, term: object) -> None:
    if type(dimension) is not int:
        raise ValueError("dimension is not an integer")
    if type(term) is int:
        term = Fraction(term)
    if type(term) is not Fraction:
        raise ValueError("term is not an exact rational")
    if dimension != 1:
        raise ValueError("do not copy a 1D constant into a higher-dimensional sum")
    if term != _ONE_SITE_KAPPA_2:
        raise ValueError("term is not the one-site second cumulant")


def refuse_outside_temperature(r: object) -> None:
    if type(r) is int:
        r = Fraction(r)
    if type(r) is not Fraction:
        raise ValueError("r is not an exact rational")
    if r < 0 or r > _R_MAX:
        raise ValueError(
            "refused: r lies outside 0<=r<=1/192 and is not an in-disk field limit"
        )
