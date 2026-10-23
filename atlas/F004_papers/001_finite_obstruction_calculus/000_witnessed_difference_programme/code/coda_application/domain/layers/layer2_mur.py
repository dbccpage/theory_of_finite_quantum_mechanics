# -*- coding: utf-8 -*-
"""
Layer 2: CODA-MUR (Meta & Universal Re-Presentation).

Checks declared finite section overlaps for compatibility, shape agreement,
and exact coordinate loss. It does not compute the general MUR commutation
defect, comparison spans, holonomy, or transport certificates.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Tuple

from coda_application.domain.l1_quotient import FunctionalEvaluator, _no_tick
from coda_application.domain.entities import LayerExecutionRecord
from coda_application.domain.intake import IntakeData, intake
from coda_application.domain.value_objects import ExactRational, LayerId


def _data(problem: Any) -> IntakeData:
    return problem if isinstance(problem, IntakeData) else intake(problem)


def _er(value: Fraction) -> ExactRational:
    return ExactRational(value.numerator, value.denominator)


class Layer2MUR:
    """Evaluates Layer 2: Meta & Universal Re-Presentation."""

    @staticmethod
    def evaluate(problem: Any, *, evaluator: FunctionalEvaluator, tick=_no_tick) -> Tuple[LayerExecutionRecord, ExactRational]:
        """
        Checks declared overlap compatibility and returns coordinate loss.

        A declared-incompatible overlap, an overlap naming a missing section, sections of
        unequal length, or any measured loss on a declared-compatible overlap fails the
        layer (catalog G4: transport loss must equal 0).
        """
        data = _data(problem)
        loss_coordinates = []
        incompatible, missing, mismatched = [], [], []
        for (u, v), compatible in data.overlaps:
            if not compatible:
                incompatible.append((u, v))
                loss_coordinates.append(Fraction(1))
                continue
            su, sv = data.section(u), data.section(v)
            if su is None or sv is None:
                missing.append((u, v))
                continue
            if len(su) != len(sv):
                mismatched.append((u, v))
                continue
            loss_coordinates.extend(a - b for a, b in zip(su, sv))
        loss = evaluator.mass(loss_coordinates, tick=tick)
        succeeded = not incompatible and not missing and not mismatched and loss == 0
        msg = (
            f"Transport loss={loss}; incompatible overlaps={len(incompatible)}, "
            f"overlaps naming a missing section={len(missing)}, length mismatches={len(mismatched)}"
        )
        record = LayerExecutionRecord(
            layer_id=LayerId.MUR,
            succeeded=succeeded,
            diagnostic_message=("Transport verified: " if succeeded else "Transport failure: ") + msg,
            defect_mass=_er(loss),
            metadata={
                "incompatible_overlaps": len(incompatible),
                "missing_section_overlaps": tuple(missing),
                "length_mismatches": tuple(mismatched),
                "loss_defect": _er(loss).to_tuple(),
            },
        )
        return record, _er(loss)
