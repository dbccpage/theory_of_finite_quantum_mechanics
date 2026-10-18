"""OutcomeType and outcome enumerations for Prompt Civilization.

AuthorityEffect: None.
"""

from __future__ import annotations

from enum import Enum


class OutcomeType(str, Enum):
    """Supported outcome categories."""

    REVIEW = "review"
    DECISION = "decision"


class ReviewOutcome(str, Enum):
    """Supported deterministic review outcomes."""

    READY_FOR_OPERATOR_APPROVAL = "ready_for_operator_approval"
    NEEDS_REPAIR = "needs_repair"
    REJECTED = "rejected"


class OperatorDecisionOutcome(str, Enum):
    """Supported operator decisions."""

    APPROVED = "approved"
    REJECTED = "rejected"
