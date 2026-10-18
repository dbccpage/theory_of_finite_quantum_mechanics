"""Lambda Operator Contract & Implementation (os:lambda).

Doctrine:
- A LambdaOperator is a deterministic, stateless, unary internal-descent morphism over admitted BaseTypes.
- Maps S -> T without carrier enlargement.
- Requires an external LambdaWitness carrying measurement and evaluation references.
- Does NOT compute canonical functionals and does NOT evaluate numbers internally.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Final, Optional

from omega_engine.crates.operator.base.operator_base import (
    OperatorBase,
    OperatorFailure,
    OperatorResult,
)

CONTRACT_ID: Final[str] = "os:lambda"


@dataclass(frozen=True, slots=True)
class LambdaWitness:
    """Immutable external witness carrying functional measurement and evaluation evidence references."""

    witness_id: str
    functional_ref: str
    before_measurement_ref: str
    after_measurement_ref: str
    evaluation_ref: str
    comparison: str = "NonIncreasing"
    is_valid: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class LambdaOperator(OperatorBase):
    """Base class for Lambda Operators requiring external Phi-witness."""

    contract_id: Final[str] = CONTRACT_ID

    def __init__(
        self,
        operator_id: str,
        domain: str,
        codomain: str,
        witness: Optional[LambdaWitness] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            operator_id=operator_id,
            domain=domain,
            codomain=codomain,
            config=config,
        )
        self.witness = witness

    def apply_with_witness(
        self, input_data: Any, witness: LambdaWitness
    ) -> OperatorResult | OperatorFailure:
        """Executes Lambda step requiring valid external witness."""
        if not witness or not witness.is_valid:
            return OperatorFailure(
                failure_reason="InvalidLambdaWitness",
                failure_details={"msg": "Valid external LambdaWitness is required for Lambda admission"},
            )
        res = self.apply(input_data)
        if isinstance(res, OperatorResult):
            metadata = dict(res.metadata)
            metadata["witness_id"] = witness.witness_id
            metadata["functional_ref"] = witness.functional_ref
            metadata["before_measurement_ref"] = witness.before_measurement_ref
            metadata["after_measurement_ref"] = witness.after_measurement_ref
            metadata["evaluation_ref"] = witness.evaluation_ref
            metadata["comparison"] = witness.comparison
            return OperatorResult(
                output=res.output,
                is_success=res.is_success,
                operator_id=res.operator_id,
                metadata=metadata,
            )
        return res


__all__ = [
    "LambdaOperator",
    "LambdaWitness",
    "CONTRACT_ID",
]
