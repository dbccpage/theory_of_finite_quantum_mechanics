"""Outcome Value Object and dictionary mapping for Prompt Civilization.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Self

from .outcome_type import OperatorDecisionOutcome, OutcomeType, ReviewOutcome


@dataclass(frozen=True, slots=True)
class Outcome:
    """Outcome Value Object representing a deterministic review or decision outcome."""

    outcome_type: OutcomeType
    value: str

    @classmethod
    def review(cls, outcome: str | ReviewOutcome) -> Self:
        val = outcome.value if isinstance(outcome, ReviewOutcome) else str(outcome)
        return cls(outcome_type=OutcomeType.REVIEW, value=val)

    @classmethod
    def decision(cls, outcome: str | OperatorDecisionOutcome) -> Self:
        val = outcome.value if isinstance(outcome, OperatorDecisionOutcome) else str(outcome)
        return cls(outcome_type=OutcomeType.DECISION, value=val)

    def to_dict(self) -> dict[str, str]:
        return {
            "outcome_type": self.outcome_type.value,
            "value": self.value,
        }

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, str]) -> Self:
        return cls(
            outcome_type=OutcomeType(data["outcome_type"]),
            value=str(data["value"]),
        )
