"""Reducer Operator Contract & Implementation (os:reducer).

Doctrine:
- A ReducerOperator is a deterministic, stateless, unary, same-carrier structural canonicalization operator (S -> S).
- Removes declared redundancy or normalizes representation.
- Idempotent: R(R(s)) == R(s).
- κ non-expanding: κ(R(s)) <= κ(s).
- Inherits root Operator law: Phi(R(s)) <= Phi(s).
"""

from __future__ import annotations
from typing import Any, Dict, Final, Optional

from omega_engine.crates.operator.base.operator_base import (
    OperatorBase,
    OperatorFailure,
    OperatorResult,
)

CONTRACT_ID: Final[str] = "os:reducer"


class ReducerOperator(OperatorBase):
    """Base class for Reducer Operators (idempotent, kappa non-expanding, Phi non-increasing)."""

    contract_id: Final[str] = CONTRACT_ID
    idempotent_required: Final[bool] = True
    kappa_nonincrease_required: Final[bool] = True

    def __init__(
        self,
        operator_id: str,
        domain: str,
        reduction_measure_name: str = "kappa",
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            operator_id=operator_id,
            domain=domain,
            codomain=domain,
            config=config,
        )
        self.reduction_measure_name = reduction_measure_name


__all__ = [
    "ReducerOperator",
    "CONTRACT_ID",
]
