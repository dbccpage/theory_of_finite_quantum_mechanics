"""Exact checks for the finite signed-history identity.

The ordered CAR trace and the original occupation-history sum are evaluated
separately. One fixture lies in the declared disk by the rational bound
log(1+x) < x. Another repeats the outside L=4, M=1, q=3 control. Neither
fixture samples a measure or runs an infinite schedule.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path


def repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        marker = parent / ".git"
        if marker.is_file() or marker.is_dir():
            return parent
    raise SystemExit("repository root not found")


ROOT = repo_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from omega_engine_projects.fsp.meron_sign_problem.code.meron_exact_model import (  # noqa: E402
    hop_sign,
    meron_database,
    meron_summary,
    meron_transfer_trace,
    rational,
)


class ClaimRefused(Exception):
    pass


def exact_rational(value: object, name: str) -> Fraction:
    if isinstance(value, bool) or isinstance(value, float) or type(value) not in (int, Fraction):
        raise SystemExit("non-exact " + name)
    return Fraction(value)


def a_x(state: int, site: int) -> Fraction:
    """a_x = (-1)^x (n_x - 1/2), low bit = site 0."""
    occupied = (state >> site) & 1
    sign = 1 if site % 2 == 0 else -1
    return sign * Fraction(2 * occupied - 1, 2)


def layer_transfer(sites: int, q: Fraction, parity: int, *, signed: bool) -> list[list[Fraction]]:
    """One checkerboard layer, bonds in increasing order, original CAR hop sign."""
    dimension = 1 << sites
    matrix = [
        [Fraction(1) if row == col else Fraction(0) for col in range(dimension)]
        for row in range(dimension)
    ]
    for site in range(parity, sites, 2):
        neighbor = (site + 1) % sites
        updated = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
        for state in range(dimension):
            mixed = ((state >> site) ^ (state >> neighbor)) & 1
            diagonal = (q + 1) / 2 if mixed else Fraction(1)
            hop = None
            other = 0
            if mixed:
                other = state ^ (1 << site) ^ (1 << neighbor)
                sign = hop_sign(state, site, neighbor) if signed else 1
                hop = (q - 1) / 2 * sign
            for origin in range(dimension):
                value = matrix[state][origin]
                if value == 0:
                    continue
                updated[state][origin] += diagonal * value
                if hop is not None:
                    updated[other][origin] += hop * value
        matrix = updated
    return matrix


def insertion_diagonal(sites: int, rates: tuple[Fraction, ...]) -> list[Fraction]:
    """exp(sum_x z_x a_x/(2M)) when exp(z_x/(4M)) = rates[x]."""
    if len(rates) != sites:
        raise SystemExit("one rate per site required")
    checked = tuple(exact_rational(rate, "insertion rate") for rate in rates)
    if any(rate <= 0 for rate in checked):
        raise SystemExit("insertion rate must be positive")
    dimension = 1 << sites
    diagonal = []
    for state in range(dimension):
        weight = Fraction(1)
        for site, rate in enumerate(checked):
            twice = 2 * a_x(state, site)
            if twice == 1:
                weight *= rate
            elif twice == -1:
                weight *= Fraction(1) / rate
            else:
                raise SystemExit("a_x is not half-integral")
        diagonal.append(weight)
    return diagonal


def observable_diagonal(sites: int, site: int) -> list[Fraction]:
    return [a_x(state, site) for state in range(1 << sites)]


def apply_matrix(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    image = []
    for row in matrix:
        total = Fraction(0)
        for entry, component in zip(row, vector, strict=True):
            if entry != 0 and component != 0:
                total += entry * component
        image.append(total)
    return image


def scalar_for(sites: int, repetitions: int, q: Fraction) -> Fraction:
    """q^{-LM/4} when that power is an integer. Otherwise the comparisons stay unscaled."""
    exponent = sites * repetitions
    if exponent % 4 != 0:
        return Fraction(1)
    return q ** (-(exponent // 4))


def ordered_product_trace(
    layers: list[list[list[Fraction]]],
    diagonals: list[list[Fraction]],
    scalar: Fraction,
    observables: list[list[Fraction] | None] | None = None,
) -> Fraction:
    """Trace of T_{K-1} D_{K-1} ... T_0 D_0, optional diagonal factors in the D slots."""
    dimension = len(diagonals[0])
    total = Fraction(0)
    for start in range(dimension):
        vector = [Fraction(0) for _ in range(dimension)]
        vector[start] = Fraction(1)
        for step, layer in enumerate(layers):
            vector = [diagonals[step][index] * vector[index] for index in range(dimension)]
            if observables is not None and observables[step] is not None:
                factor = observables[step]
                vector = [factor[index] * vector[index] for index in range(dimension)]
            vector = apply_matrix(layer, vector)
        total += vector[start]
    return total * scalar


def history_numerator(
    layers: list[list[list[Fraction]]],
    diagonals: list[list[Fraction]],
    scalar: Fraction,
    observables: list[list[Fraction] | None] | None = None,
) -> Fraction:
    """Sum over occupation tuples of layer matrix elements times the same diagonals."""
    dimension = len(diagonals[0])
    steps = len(layers)
    total = Fraction(0)

    def walk(step: int, first: int, current: int, weight: Fraction) -> None:
        nonlocal total
        if step == steps:
            if current == first:
                total += weight
            return
        extra = Fraction(1)
        if observables is not None and observables[step] is not None:
            extra = observables[step][current]
        if extra == 0:
            return
        incoming = diagonals[step][current] * extra
        if incoming == 0:
            return
        row_weights = weight * incoming
        for nxt in range(dimension):
            amplitude = layers[step][nxt][current]
            if amplitude == 0:
                continue
            walk(step + 1, first, nxt, row_weights * amplitude)

    for start in range(dimension):
        walk(0, start, start, Fraction(1))
    return total * scalar


def accept_claim(claimed: Fraction, actual: Fraction) -> bool:
    if type(claimed) is not Fraction or type(actual) is not Fraction or claimed != actual:
        raise ClaimRefused
    return True


def control_rejects(claimed: Fraction, actual: Fraction) -> bool:
    try:
        accept_claim(claimed, actual)
    except ClaimRefused:
        return True
    return False


def require_disk(q: Fraction, rows: tuple[tuple[Fraction, ...], ...], repetitions: int) -> None:
    """Sufficient rational certificate that theta < 1/192 and every |z_x| < 1/64.

    For x>0, log(1+x) = integral_0^x dt/(1+t) < x. Thus M log q < M(q-1)
    and 4M |log rate| is strictly below the compared rational.
    """
    if q < 1 or repetitions < 1:
        raise SystemExit("disk certificate requires q>=1 and M>=1")
    if repetitions * (q - 1) > Fraction(1, 192):
        raise SystemExit("temperature certificate missed the disk")
    for row in rows:
        for rate in row:
            if rate <= 0:
                raise SystemExit("insertion rate must be positive")
            if rate >= 1:
                slack = rate - 1
            else:
                slack = Fraction(1, rate) - 1
            if 4 * repetitions * slack > Fraction(1, 64):
                raise SystemExit("source certificate missed the disk")


def build_layers(sites: int, q: Fraction, repetitions: int, *, signed: bool) -> list[list[list[Fraction]]]:
    layers = []
    for time in range(2 * repetitions):
        layers.append(layer_transfer(sites, q, time % 2, signed=signed))
    return layers


def require_identity(
    layers: list[list[list[Fraction]]],
    diagonals: list[list[Fraction]],
    scalar: Fraction,
    observables: list[list[Fraction] | None] | None = None,
) -> Fraction:
    traced = ordered_product_trace(layers, diagonals, scalar, observables)
    counted = history_numerator(layers, diagonals, scalar, observables)
    if control_rejects(counted, traced):
        raise SystemExit("protected identity refused: history " + str(counted) + " trace " + str(traced))
    return traced


def zero_diagonals(sites: int, steps: int) -> list[list[Fraction]]:
    ones = insertion_diagonal(sites, tuple(Fraction(1) for _ in range(sites)))
    return [list(ones) for _ in range(steps)]


def require_zero_source_pin(sites: int, repetitions: int, q: Fraction) -> Fraction:
    layers = build_layers(sites, q, repetitions, signed=True)
    diagonals = zero_diagonals(sites, 2 * repetitions)
    unscaled = require_identity(layers, diagonals, Fraction(1))
    transfer = rational(meron_transfer_trace(sites, repetitions, q))
    if unscaled != transfer:
        raise SystemExit("zero-source trace missed meron_transfer_trace")
    if sites in (4, 6) and sites * repetitions <= 12:
        summary = meron_summary(meron_database(sites, repetitions, q))
        sql_partition = rational(summary["signed_partition"])
        if not summary["reconstruction"] or sql_partition != transfer:
            raise SystemExit("zero-source signed partition is not the original ensemble")
    return unscaled


def outside_disk_control() -> None:
    sites = 4
    repetitions = 1
    q = Fraction(3)
    outside_zero = require_zero_source_pin(sites, repetitions, q)
    layers = build_layers(sites, q, repetitions, signed=True)
    old_rates = (
        (Fraction(2), Fraction(1), Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(3), Fraction(1), Fraction(1)),
    )
    new_rates = (
        (Fraction(2), Fraction(1), Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(1), Fraction(5)),
    )
    if old_rates == new_rates or old_rates[0] == old_rates[1] or new_rates[0] == new_rates[1]:
        raise SystemExit("time-dependent source was not altered")
    scalar = scalar_for(sites, repetitions, q)
    old_diagonals = [insertion_diagonal(sites, row) for row in old_rates]
    new_diagonals = [insertion_diagonal(sites, row) for row in new_rates]
    old_trace = require_identity(layers, old_diagonals, scalar)
    new_trace = require_identity(layers, new_diagonals, scalar)
    unsigned = build_layers(sites, q, repetitions, signed=False)
    substitute = require_identity(unsigned, old_diagonals, scalar)
    changed_source_caught = control_rejects(old_trace, new_trace)
    wrong_numerator_caught = control_rejects(substitute, old_trace)
    print("outside_zero_unscaled=" + str(outside_zero))
    print("outside_protected=" + str(old_trace))
    print("outside_changed=" + str(new_trace))
    print("outside_substitute=" + str(substitute))
    print("outside_changed_source_caught=" + str(changed_source_caught).lower())
    print("outside_wrong_numerator_caught=" + str(wrong_numerator_caught).lower())
    if not changed_source_caught or not wrong_numerator_caught:
        raise SystemExit("outside-disk controls did not fire")


def inside_disk_control() -> None:
    sites = 4
    repetitions = 1
    q = Fraction(193, 192)
    old_rates = (
        (Fraction(257, 256), Fraction(1), Fraction(1), Fraction(256, 257)),
        (Fraction(1), Fraction(257, 256), Fraction(256, 257), Fraction(1)),
    )
    new_rates = (
        old_rates[0],
        (Fraction(1), Fraction(1), Fraction(256, 257), Fraction(257, 256)),
    )
    require_disk(q, old_rates, repetitions)
    require_disk(q, new_rates, repetitions)
    if old_rates[1] == new_rates[1]:
        raise SystemExit("in-disk source was not altered")
    inside_zero = require_zero_source_pin(sites, repetitions, q)
    layers = build_layers(sites, q, repetitions, signed=True)
    scalar = scalar_for(sites, repetitions, q)
    if scalar != Fraction(192, 193):
        raise SystemExit("q^{-LM/4} was not the rational 192/193")
    old_diagonals = [insertion_diagonal(sites, row) for row in old_rates]
    new_diagonals = [insertion_diagonal(sites, row) for row in new_rates]
    protected = require_identity(layers, old_diagonals, scalar)
    changed = require_identity(layers, new_diagonals, scalar)
    unsigned = build_layers(sites, q, repetitions, signed=False)
    substitute = require_identity(unsigned, old_diagonals, scalar)
    if not control_rejects(protected, changed) or not control_rejects(substitute, protected):
        raise SystemExit("in-disk controls did not fire")
    ones = zero_diagonals(sites, 2)
    first = observable_diagonal(sites, 0)
    second = observable_diagonal(sites, 1)
    distinct = [first, second]
    same_site = [first, first]
    mixed = require_identity(layers, ones, scalar, distinct)
    same_site_value = require_identity(layers, ones, scalar, same_site)
    if mixed == same_site_value:
        raise SystemExit("distinct-site numerator equals the same-site control")
    wide_scalar = scalar_for(6, 1, q)
    if wide_scalar != 1:
        raise SystemExit("L=6 comparison must stay unscaled")
    wide_zero = require_zero_source_pin(6, 1, q)
    small_scalar = scalar_for(2, 1, q)
    if small_scalar != 1:
        raise SystemExit("L=2 comparison must stay unscaled")
    small_zero = require_zero_source_pin(2, 1, q)
    print("inside_q=" + str(q))
    print("inside_zero_unscaled=" + str(inside_zero))
    print("wide_zero_unscaled=" + str(wide_zero))
    print("small_zero_unscaled=" + str(small_zero))
    print("inside_scalar=" + str(scalar))
    print("inside_protected=" + str(protected))
    print("inside_changed=" + str(changed))
    print("inside_substitute=" + str(substitute))
    print("inside_mixed=" + str(mixed))
    print("inside_same_site=" + str(same_site_value))


def main() -> int:
    outside_disk_control()
    inside_disk_control()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
