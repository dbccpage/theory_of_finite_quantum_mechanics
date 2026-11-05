# -*- coding: utf-8 -*-
"""
Layer 3: CODA-CS (Continuum Shadow).

Checks a total map from a finite set of fine profile labels to coarse labels.
No protected-answer map or transport certificate is supplied, so this check
alone establishes neither fiber constancy of an answer nor a continuum limit.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Tuple

from coda_application.domain.entities import LayerExecutionRecord
from coda_application.domain.intake import IntakeData, intake
from coda_application.domain.value_objects import ExactRational, LayerId


def _data(problem: Any) -> IntakeData:
    return problem if isinstance(problem, IntakeData) else intake(problem)


def _er(value: Fraction) -> ExactRational:
    return ExactRational(value.numerator, value.denominator)


class Layer3CS:
    """Evaluates Layer 3: Continuum Shadow."""

    @staticmethod
    def evaluate(problem: Any) -> Tuple[LayerExecutionRecord, bool]:
        """
        Checks the declared finite projection domain and codomain.
        Returns LayerExecutionRecord and boolean indicating refinement consistency.
        """
        data = _data(problem)
        proj = dict(data.projection)
        fine, coarse = set(data.fine), set(data.coarse)
        missing = fine - set(proj)
        extra = set(proj) - fine
        invalid = {f for f, c in proj.items() if c not in coarse}
        inconsistent = len(missing | extra | invalid)
        consistent = inconsistent == 0
        msg = ("Total finite profile map verified; no protected-answer claim is checked"
               if consistent else f"Projection is not a total map between the declared profiles: {inconsistent} invalid coordinates")
        record = LayerExecutionRecord(
            layer_id=LayerId.CS,
            succeeded=consistent,
            diagnostic_message=msg,
            defect_mass=ExactRational(inconsistent, 1),
            metadata={"coarse_profile": data.coarse, "fine_profile": data.fine, "invalid_projection_coordinates": inconsistent},
        )
        return record, consistent
