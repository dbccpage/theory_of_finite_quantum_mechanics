# -*- coding: utf-8 -*-
"""
Layer 5: CODA-Q (The Continuum).

Continuum representations via completion and enclosure.
Checks ordering and diameter of a supplied rational interval. It does not
construct a metric completion or verify that an unknown state lies inside.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Tuple

from coda_application.domain.entities import LayerExecutionRecord
from coda_application.domain.intake import IntakeData, exact, intake
from coda_application.domain.value_objects import ExactRational, LayerId


def _data(problem: Any) -> IntakeData:
    return problem if isinstance(problem, IntakeData) else intake(problem)


def _er(value: Fraction) -> ExactRational:
    return ExactRational(value.numerator, value.denominator)


class Layer5Q:
    """Evaluates a finite rational enclosure supplied for Layer 5."""

    @staticmethod
    def evaluate(problem: Any) -> Tuple[LayerExecutionRecord, ExactRational]:
        """
        Executes Layer 5 interval enclosure evaluation.
        Returns LayerExecutionRecord and interval diameter.
        """
        if isinstance(problem, IntakeData):
            lo, hi = problem.enclosure
        else:
            lo_raw, hi_raw = problem.enclosure_interval
            lo, hi = exact(lo_raw, "enclosure lo"), exact(hi_raw, "enclosure hi")
        if hi < lo:
            diameter, succeeded = Fraction(0), False
            msg = f"Inverted interval enclosure [{lo}, {hi}]"
        else:
            diameter, succeeded = hi - lo, True
            msg = f"Enclosure verified: [{lo}, {hi}] with diameter {diameter}; midpoint is not exact state"
        record = LayerExecutionRecord(
            layer_id=LayerId.Q,
            succeeded=succeeded,
            diagnostic_message=msg,
            defect_mass=_er(diameter),
            metadata={
                "interval_lo": (lo.numerator, lo.denominator),
                "interval_hi": (hi.numerator, hi.denominator),
                "diameter": _er(diameter).to_tuple(),
            },
        )
        return record, _er(diameter)
