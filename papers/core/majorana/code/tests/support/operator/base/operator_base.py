"""Root Operator Contract & Implementation (admitted -> admitted).

Doctrine:
- An Operator is a deterministic, stateless, single-step typed transformation over admitted BaseTypes.
- Root law: Every admitted Operator satisfies Phi(output) <= Phi(input) established externally.
- Operator implementations NEVER compute Phi (no Phi1, no Gamma2, no Xi math).
- Single-step only: repetition and sequencing belong to Pipeline/Runner orchestration.
- Operator composition cannot mint authority (AuthorityEffect: None).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Final, Optional

CONTRACT_ID: Final[str] = "os:operator"


@dataclass(frozen=True, slots=True)
class OperatorResult:
    """Immutable typed result of an Operator execution step."""
    output: Any
    is_success: bool
    operator_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class OperatorFailure:
    """Typed failure produced by an Operator execution step."""
    failure_reason: str
    failure_details: Dict[str, Any] = field(default_factory=dict)


class OperatorBase(ABC):
    """Base class for all pure, admitted Operators (admitted -> admitted)."""

    contract_id: Final[str] = CONTRACT_ID
    authority_effect: Final[str] = "None"
    phi_nonincrease_required: Final[bool] = True

    def __init__(
        self,
        operator_id: str,
        domain: str,
        codomain: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.operator_id = operator_id
        self.domain = domain
        self.codomain = codomain
        self.config = config or {}

    def apply(self, input_data: Any) -> OperatorResult | OperatorFailure:
        """Purity execution envelope: validates admitted input, executes 1 step, validates result."""
        if input_data is None:
            return OperatorFailure(
                failure_reason="NullInputError",
                failure_details={"msg": "Operator input cannot be None"},
            )
        try:
            res = self._apply_once(input_data)
            if isinstance(res, OperatorFailure):
                return res
            return OperatorResult(
                output=res,
                is_success=True,
                operator_id=self.operator_id,
                metadata={
                    "domain": self.domain,
                    "codomain": self.codomain,
                },
            )
        except Exception as exc:
            return OperatorFailure(
                failure_reason="OperatorExecutionError",
                failure_details={"error": str(exc)},
            )

    @abstractmethod
    def _apply_once(self, input_data: Any) -> Any | OperatorFailure:
        """Internal single-step transformation method implemented by concrete Operators."""


__all__ = [
    "OperatorBase",
    "OperatorResult",
    "OperatorFailure",
    "CONTRACT_ID",
]
