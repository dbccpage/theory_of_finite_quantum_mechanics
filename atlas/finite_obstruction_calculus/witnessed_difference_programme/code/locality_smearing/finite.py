"""Exact finite syndrome, cochain and filtering operations (no physical bindings)."""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations

from hermitianization.model import rational


def xor(x, y):
    if len(x) != len(y) or any(type(a) is not int or a not in (0, 1) for a in (*x, *y)):
        raise ValueError("equal length binary vectors required")
    return tuple(a ^ b for a, b in zip(x, y, strict=True))


def syndrome(rows, x):
    if any(len(r) != len(x) for r in rows):
        raise ValueError("syndrome shape mismatch")
    if any(type(a) is not int or a not in (0, 1) for a in (*x, *(a for r in rows for a in r))):
        raise ValueError("binary entries required")
    return tuple(sum(a * b for a, b in zip(r, x, strict=True)) % 2 for r in rows)


def admit_syndrome(rows, errors, repairs):
    if not errors or len(set(errors)) != len(errors) or len(set(repairs)) != len(repairs):
        raise ValueError(
            "nonempty distinct admitted errors and a distinct repair subgroup required"
        )
    width = len(errors[0])
    if any(len(e) != width for e in (*errors, *repairs)):
        raise ValueError("carrier mismatch")
    zero = (0,) * width
    b = set(repairs)
    if zero not in b or any(xor(x, y) not in b for x in b for y in b):
        raise ValueError("repairs must be a binary subspace")
    if any(any(syndrome(rows, x)) for x in b):
        raise ValueError("repair outside syndrome kernel")
    for x in errors:
        syndrome(rows, x)


def recovery(rows, errors, repairs):
    admit_syndrome(rows, errors, repairs)
    representatives = {}
    for e in errors:
        s = syndrome(rows, e)
        if s in representatives and xor(e, representatives[s]) not in repairs:
            return {"kind": "collision", "left": list(representatives[s]), "right": list(e)}
        representatives.setdefault(s, e)
    return {
        "kind": "decoder",
        "rows": [
            {"syndrome": list(s), "repair": list(e)} for s, e in sorted(representatives.items())
        ],
    }


def observation_completion(rows, errors, repairs):
    """Minimum extra binary rows, with exhaustive finite lower coverage."""
    admit_syndrome(rows, errors, repairs)
    width = len(errors[0])
    available = [tuple((i >> j) & 1 for j in range(width)) for i in range(1, 2**width)]
    for size in range(len(available) + 1):
        for selected in combinations(available, size):
            # Added observations must respect the same declared repair equivalence.
            if any(any(syndrome(selected, b)) for b in repairs):
                continue
            witness = recovery((*rows, *selected), errors, repairs)
            if witness["kind"] == "decoder":
                return {
                    "extra_rows": [list(r) for r in selected],
                    "decoder": witness,
                    "minimum": size,
                }
    raise AssertionError("a quotient-separating finite row family must exist")


def differences(values):
    x = tuple(map(rational, values))
    if not x:
        raise ValueError("nonempty periodic cycle required")
    return tuple(x[(j + 1) % len(x)] - x[j] for j in range(len(x)))


def primitive(values):
    """A submitted exact cycle cochain is a coboundary iff its period is zero."""
    x = tuple(map(rational, values))
    if not x or sum(x) != 0:
        raise ValueError("nonzero period or empty carrier")
    potential = [Q(0)]
    for value in x[:-1]:
        potential.append(potential[-1] + value)
    return tuple(potential)


def harmonic(values):
    x = tuple(map(rational, values))
    if not x:
        raise ValueError("nonempty carrier required")
    return (sum(x) / len(x),) * len(x)


def subdivide(values, k):
    if type(k) is not int or k < 1:
        raise ValueError("positive integral subdivision required")
    return tuple(rational(x) / k for x in values for _ in range(k))


def alternating_average(samples):
    """samples[j][x]; even temporal count and a fixed nonempty spatial carrier."""
    n = len(samples)
    if not n or n % 2 or not samples[0] or any(len(r) != len(samples[0]) for r in samples):
        raise ValueError("rectangular samples and positive even temporal count required")
    return sum((-1) ** j * rational(x) for j, row in enumerate(samples) for x in row) / (
        n * len(samples[0])
    )


def exponential_envelope(theta, multiple):
    """exp(multiple*theta) <= (1 - multiple*theta/k)^(-k), k=32."""
    theta = rational(theta)
    if not 0 <= theta <= 1 or multiple not in (4, 8, 16):
        raise ValueError("declared compact temperature range required")
    return (1 - Q(multiple) * theta / 32) ** (-32)


def time_consistency_constant(theta, spatial, amplitude, derivative):
    """A/M bound derived in the written fixed-L time-limit theorem."""
    theta, amplitude, derivative = map(rational, (theta, amplitude, derivative))
    if type(spatial) is not int or spatial != 4 or amplitude < 0 or derivative < 0:
        raise ValueError("this CAR binding has L=4 and nonnegative profile bounds")
    e4 = exponential_envelope(theta, 4)
    e16 = exponential_envelope(theta, 16)
    c = 30 * (theta + theta**2) * e16
    k = e16 / 2
    return spatial * (amplitude**2 * c + 2 * theta * e4 * amplitude**2 + k * amplitude * derivative)


def positive_threshold(error_numerator, positive_margin):
    a, margin = rational(error_numerator), rational(positive_margin)
    if a < 0 or margin <= 0:
        raise ValueError("nonnegative envelope and strict positive margin required")
    return max(1, a // margin + 1)
