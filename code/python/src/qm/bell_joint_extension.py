"""Exact CHSH certificate for one normalized joint law on four binary variables.

Bit order is A0, A1, B0, B1 (least significant first); a set bit means +1.
Origin: FQ-BELL-CLASSICAL-JOINT-EXTENSION. AuthorityEffect: None.
The supplied joint law is an assumption, not a reconstruction of quantum data.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence


@dataclass(frozen=True)
class JointBellCertificate:
    correlators: tuple[Fraction, Fraction, Fraction, Fraction]
    chsh: Fraction
    positive_score_mass: Fraction
    negative_score_mass: Fraction
    lower_slack: Fraction
    upper_slack: Fraction


def certify_joint_law(weights: Sequence[Fraction | int]) -> JointBellCertificate:
    """Require 16 nonnegative exact weights of total one; certify -2 <= S <= 2.

Correlator order is E00, E01, E10, E11. The independently accumulated
score masses certify S = 2(P+ - P-), 2+S = 4P+, and 2-S = 4P-.
"""
    if len(weights) != 16:
        raise ValueError("the joint law must have exactly 16 weights")
    if any(type(w) not in (int, Fraction) for w in weights):
        raise TypeError("weights must be exact integers or Fractions")
    probabilities = tuple(Fraction(w) for w in weights)
    if any(w < 0 for w in probabilities):
        raise ValueError("joint weights must be nonnegative")
    if sum(probabilities, Fraction(0)) != 1:
        raise ValueError("joint weights must sum to one")
    correlators = [Fraction(0) for _ in range(4)]
    plus = minus = Fraction(0)
    for mask, weight in enumerate(probabilities):
        a0, a1, b0, b1 = (1 if mask & (1 << j) else -1 for j in range(4))
        for j, product in enumerate((a0*b0, a0*b1, a1*b0, a1*b1)):
            correlators[j] += weight * product
        # Factored route, separate from the four correlator accumulations.
        score = a0 * (b0 + b1) + a1 * (b0 - b1)
        if score == 2:
            plus += weight
        else:
            minus += weight
    e00, e01, e10, e11 = correlators
    chsh = e00 + e01 + e10 - e11
    return JointBellCertificate(
        (e00, e01, e10, e11), chsh, plus, minus, 2 + chsh, 2 - chsh
    )


def response_products() -> tuple[tuple[int, int, int, int], ...]:
    """Nullary generator: the ordered product table on the fixed carrier."""
    rows = []
    for mask in range(16):
        a0, a1, b0, b1 = (1 if mask & (1 << j) else -1 for j in range(4))
        rows.append((a0*b0, a0*b1, a1*b0, a1*b1))
    return tuple(rows)


def _exact_vector(values, size):
    if len(values) != size:
        raise ValueError(f"expected {size} exact coordinates")
    if any(type(x) not in (int, Fraction) for x in values):
        raise TypeError("coordinates must be exact integers or Fractions")
    return tuple(Fraction(x) for x in values)


def _joint_weights(weights):
    result = _exact_vector(weights, 16)
    if any(x < 0 for x in result):
        raise ValueError("joint weights must be nonnegative")
    if sum(result, Fraction(0)) != 1:
        raise ValueError("joint weights must sum to one")
    return result


def joint_expectation(weights, responses) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Binary generator (JointLaw, ResponseMap4) -> Q^4, using one law.

    The response table may be arbitrary exact rational four-vectors. The CHSH
    bound requires the specific response_products table, not an arbitrary table.
    """
    probabilities = _joint_weights(weights)
    if len(responses) != 16:
        raise ValueError("the response map must have exactly 16 rows")
    table = tuple(_exact_vector(row, 4) for row in responses)
    return tuple(sum((p * row[j] for p, row in zip(probabilities, table)), Fraction(0)) for j in range(4))


def chsh_linear(correlators) -> Fraction:
    """Unary generator on Q^4; a scalar value alone is not a Bell certificate."""
    a, b, c, d = _exact_vector(correlators, 4)
    return a + b + c - d


def verify_joint_certificate(weights, certificate: JointBellCertificate) -> None:
    """Reject a false certificate by recomputing every component independently.

    Does not call certify_joint_law or accept its verdict. This direct-product
    route is distinct from the producer's factored score partition.
    """
    probabilities = _joint_weights(weights)
    if type(certificate) is not JointBellCertificate:
        raise TypeError("expected a JointBellCertificate")
    fields = (certificate.chsh, certificate.positive_score_mass, certificate.negative_score_mass,
              certificate.lower_slack, certificate.upper_slack)
    _exact_vector(certificate.correlators, 4)
    _exact_vector(fields, 5)
    products = response_products()
    e = tuple(sum((probabilities[m] * products[m][j] for m in range(16)), Fraction(0)) for j in range(4))
    scores = tuple(row[0] + row[1] + row[2] - row[3] for row in products)
    plus = sum((p for p, s in zip(probabilities, scores) if s == 2), Fraction(0))
    minus = sum((p for p, s in zip(probabilities, scores) if s == -2), Fraction(0))
    s = e[0] + e[1] + e[2] - e[3]
    if certificate != JointBellCertificate(e, s, plus, minus, 2+s, 2-s):
        raise ValueError("certificate does not match the supplied joint law")
