# -*- coding: utf-8 -*-
"""
Layer 4: CODA-CS-Q (Continuum Shadow to Continuum Bridge).

Checks equality of supplied finite section vectors and reports their smallest
nonzero coordinate distance. It does not prove image factorization, the
decoder 2*eps bound, or metric separation for arbitrary spaces.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Optional, Tuple

from coda_application.domain.l1_quotient import FunctionalEvaluator, _no_tick
from coda_application.domain.entities import LayerExecutionRecord
from coda_application.domain.intake import IntakeData, intake
from coda_application.domain.value_objects import ExactRational, LayerId


def _data(problem: Any) -> IntakeData:
    return problem if isinstance(problem, IntakeData) else intake(problem)


def _er(value: Fraction) -> ExactRational:
    return ExactRational(value.numerator, value.denominator)


class Layer4CSQ:
    """Evaluates Layer 4: Continuum Shadow to Continuum Bridge."""

    @staticmethod
    def evaluate(problem: Any, *, evaluator: FunctionalEvaluator, tick=_no_tick) -> Tuple[LayerExecutionRecord, ExactRational]:
        """
        Executes a finite section-vector collision check.
        Returns LayerExecutionRecord and the minimum nonzero separation.

        Two distinct sections at distance 0 that the data does not declare as glued (a
        compatible overlap, where agreement is required by Layer 2) fail this declared label-separation policy: their supplied vectors agree.
        This is a finite label check, not a proof of an ambient metric axiom.
        """
        data = _data(problem)
        sections = list(data.sections)
        glued = {frozenset(pair) for pair, compatible in data.overlaps if compatible}
        collisions = []
        min_sep: Optional[Fraction] = None
        for i in range(len(sections)):
            for j in range(i + 1, len(sections)):
                (la, a), (lb, b) = sections[i], sections[j]
                if len(a) != len(b):
                    continue
                diff = evaluator.mass(tuple(x - y for x, y in zip(a, b)), tick=tick)
                if diff == 0:
                    if frozenset((la, lb)) not in glued:
                        collisions.append((la, lb))
                elif min_sep is None or diff < min_sep:
                    min_sep = diff
        sep = min_sep if min_sep is not None else Fraction(0)
        succeeded = not collisions
        if collisions:
            msg = f"Metric separation failure: colliding sections {collisions}"
        elif min_sep is None:
            msg = "Single section or no comparable pair; metric separation holds trivially"
        else:
            msg = f"Metric separation verified; min nonzero distance={sep}"
        record = LayerExecutionRecord(
            layer_id=LayerId.CS_Q,
            succeeded=succeeded,
            diagnostic_message=msg,
            defect_mass=_er(sep),
            metadata={"min_separation": _er(sep).to_tuple(), "collisions": tuple(collisions)},
        )
        return record, _er(sep)
