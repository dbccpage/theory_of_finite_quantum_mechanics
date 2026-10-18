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
