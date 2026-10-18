"""Constructor Base Contract & Implementation (raw -> admitted).

Doctrine:
- A Constructor is an admission-boundary builder.
- Maps raw, unvalidated, or external input S_raw -> S_admitted.
- Does NOT inherit OperatorBase (Constructors are admission boundaries, not pure Operators).
- Does NOT compute canonical functionals (Phi1, Gamma2, Xi).
- Does NOT execute Operators.
- Does NOT carry licensing or authority minting.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Final, Optional

CONTRACT_ID: Final[str] = "urn:omega:execution:constructor:v1.0.0"


@dataclass(frozen=True, slots=True)
class AdmittedResult:
    """Immutable result of a Constructor admission step."""
    admitted_object: Any
    is_admitted: bool
    carrier_family: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ConstructorRefusal:
    """Fail-closed refusal produced by a Constructor when raw input is inadmissible."""
    refusal_reason: str
    refusal_details: Dict[str, Any] = field(default_factory=dict)


class ConstructorBase(ABC):
    """Base class for all admission-boundary Constructors (raw -> admitted)."""

    implements: Final[tuple[str, ...]] = (CONTRACT_ID,)

    def __init__(self, constructor_id: str, carrier_family: str) -> None:
        self.constructor_id = constructor_id
        self.carrier_family = carrier_family

    def construct(self, raw_input: Any) -> AdmittedResult | ConstructorRefusal:
        """Admission envelope: validates raw input and builds an admitted object."""
        if raw_input is None:
            return ConstructorRefusal(
                refusal_reason="NullRawInput",
                refusal_details={"msg": "Raw input cannot be None"},
            )
        try:
            res = self._construct_admitted(raw_input)
            if isinstance(res, ConstructorRefusal):
                return res
            return AdmittedResult(
                admitted_object=res,
                is_admitted=True,
                carrier_family=self.carrier_family,
                metadata={"constructor_id": self.constructor_id},
            )
        except Exception as exc:
            return ConstructorRefusal(
                refusal_reason="ConstructionFailure",
                refusal_details={"error": str(exc)},
            )

    @abstractmethod
    def _construct_admitted(self, raw_input: Any) -> Any | ConstructorRefusal:
        """Internal construction method implemented by concrete Constructors."""


__all__ = [
    "ConstructorBase",
    "AdmittedResult",
    "ConstructorRefusal",
    "CONTRACT_ID",
]
