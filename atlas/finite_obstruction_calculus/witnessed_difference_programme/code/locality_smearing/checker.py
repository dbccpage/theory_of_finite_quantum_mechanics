"""Independent witness checker. Does not import the witness producers."""

from __future__ import annotations

from fractions import Fraction as Q

from witnessed_difference.exact_linear import CongruenceCertificate, ExactField, verify_congruence
from witnessed_difference.outcomes import Accepted

from hermitianization.model import rational

from .finite import admit_syndrome, syndrome, xor


def _check_recovery(rows, errors, repairs, certificate):
    admit_syndrome(rows, errors, repairs)
    if certificate.get("kind") == "collision" and set(certificate) == {"kind", "left", "right"}:
        x, y = tuple(certificate["left"]), tuple(certificate["right"])
        return (
            x in errors
            and y in errors
            and syndrome(rows, x) == syndrome(rows, y)
            and xor(x, y) not in repairs
        )
    if certificate.get("kind") != "decoder" or set(certificate) != {"kind", "rows"}:
        return False
    mapping = {}
    for item in certificate["rows"]:
        if set(item) != {"syndrome", "repair"}:
            return False
        s, r = tuple(item["syndrome"]), tuple(item["repair"])
        if s in mapping or len(r) != len(errors[0]):
            return False
        mapping[s] = r
    return set(mapping) == {syndrome(rows, e) for e in errors} and all(
        xor(e, mapping[syndrome(rows, e)]) in repairs for e in errors
    )


def check_recovery(rows, errors, repairs, certificate):
    try:
        return _check_recovery(rows, errors, repairs, certificate)
    except (TypeError, ValueError, KeyError, AttributeError):
        return False


def check_congruence(matrix, certificate):
    """The matrix is supplied separately by the host; a candidate cannot replace it."""
    try:
        if set(certificate) != {"basis", "diagonal"}:
            return False
        entries = (
            [x for row in matrix for x in row]
            + [x for row in certificate["basis"] for x in row]
            + certificate["diagonal"]
        )
        if any(type(x) is not str or str(Q(x)) != x for x in entries):
            return False
        c = CongruenceCertificate(
            ExactField.RATIONAL,
            tuple(tuple(Q(x) for x in row) for row in matrix),
            tuple(tuple(Q(x) for x in row) for row in certificate["basis"]),
            tuple(Q(x) for x in certificate["diagonal"]),
        )
        return isinstance(verify_congruence(c), Accepted)
    except (ValueError, TypeError, ZeroDivisionError):
        return False


def _check_alternating(samples, derivative_bound, submitted_average):
    n = len(samples)
    if not n or n % 2 or not samples[0] or any(len(r) != len(samples[0]) for r in samples):
        return False
    d = rational(derivative_bound)
    if d < 0:
        return False
    data = [[rational(x) for x in row] for row in samples]
    # This checks the finite adjacent-pair premise, not C1 regularity of a physical field.
    if any(
        abs(data[j][x] - data[j + 1][x]) > d / n
        for j in range(0, n, 2)
        for x in range(len(data[0]))
    ):
        return False
    average = sum((-1) ** j * x for j, row in enumerate(data) for x in row) / (n * len(data[0]))
    return average == rational(submitted_average) and abs(average) <= d / (2 * n)


def _check_subdivision(original, k, fine):
    if type(k) is not int or k < 1 or not original or len(fine) != k * len(original):
        return False
    x, y = tuple(map(rational, original)), tuple(map(rational, fine))
    return all(y[j * k + i] == x[j] / k for j in range(len(x)) for i in range(k)) and (
        sum(x) == sum(y) and sum(t * t for t in x) == k * sum(t * t for t in y)
    )


def check_alternating(samples, derivative_bound, submitted_average):
    try:
        return _check_alternating(samples, derivative_bound, submitted_average)
    except (ValueError, TypeError, ZeroDivisionError):
        return False


def check_subdivision(original, k, fine):
    try:
        return _check_subdivision(original, k, fine)
    except (ValueError, TypeError, ZeroDivisionError):
        return False
