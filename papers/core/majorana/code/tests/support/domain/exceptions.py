"""Domain exceptions and error hierarchy for omega_engine crates."""

from __future__ import annotations


class DomainError(Exception):
    """Base exception for all domain errors."""


class InvariantViolationError(DomainError):
    """Raised when a core domain invariant is violated."""


class ForbiddenAuthorityError(InvariantViolationError):
    """Raised when non-None authority is claimed or detected."""


class BudgetExhaustedError(DomainError):
    """Raised when an operation, candidate, or step budget is exceeded."""


class DigestFormatError(InvariantViolationError):
    """Raised when a content digest format is invalid."""


class SecurityPathViolationError(InvariantViolationError):
    """Raised when a path violates traversal or access boundaries."""


class PayloadSizeLimitExceededError(InvariantViolationError):
    """Raised when a payload exceeds maximum allowed size (e.g. 16MB)."""


class DualWitnessRequiredError(InvariantViolationError):
    """Raised when Exact residual is claimed without a verified dual witness reference."""


class CanonicalizationError(ValueError, DomainError):
    """Raised when canonical wire serialization or parsing fails."""


class RefusalError(DomainError):
    """Raised when a candidate turn or proposal violates a required gate or fence."""


__all__ = [
    "BudgetExhaustedError",
    "CanonicalizationError",
    "DigestFormatError",
    "DomainError",
    "DualWitnessRequiredError",
    "ForbiddenAuthorityError",
    "InvariantViolationError",
    "PayloadSizeLimitExceededError",
    "RefusalError",
    "SecurityPathViolationError",
]
