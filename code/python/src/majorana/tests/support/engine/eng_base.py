"""Engine Execution Contract Implementation (strict base).

Conforms to:
    urn:omega:execution:engine:v1.0.0

Doctrine (base frozen — do not weaken):
- Engine executes only licensed carrier transitions.
- Engine does not measure, solve, evaluate, compute Φ/Γ, certify, license, or terminalize.
- Residual geometry lives in functional/; domain math in math crates / dual-home packages.
"""

from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Final

from omega_engine.crates.type.engine_io import (
    CheckedEngineOutput,
    EngineAction,
    EngineInput,
    EngineOutput,
    LicensedTransitionInput,
    RefusedEngineOutput,
)

CONTRACT_ID: Final[str] = "urn:omega:execution:engine:v1.0.0"
SCHEMA_VERSION: Final[str] = "omega.contract.v1"

# Engine v1 forbids residual geometry computation in this module.
_FORBIDDEN_ENGINE_MATH = frozenset({"phi1", "gamma2", "compute_phi", "compute_gamma"})


class Engine(ABC):
    """Licensed transition executor (Engine v1). Not a DomainWorker."""

    implements: Final[tuple[str, ...]] = (CONTRACT_ID,)

    def __init__(
        self,
        engine_id: str = "omega_prime_engine",
        engine_version: str = "v1.0.0",
    ) -> None:
        self.engine_id = engine_id
        self.engine_version = engine_version
        self.schema_hash = self.compute_schema_hash()

    def compute_schema_hash(self) -> str:
        raw = f"{CONTRACT_ID}:{SCHEMA_VERSION}:{self.engine_id}:{self.engine_version}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @abstractmethod
    def execute_licensed_transition(
        self, input_data: LicensedTransitionInput
    ) -> EngineAction | RefusedEngineOutput:
        """Execute one licensed state transition or refuse."""

    def execute_step(self, input_data: EngineInput) -> EngineOutput:
        """Refuse cochain/residual work on Engine v1.

        Historical smoke used execute_step for residual mass. That is DomainWorker
        territory. Engine must not compute Φ₁ here.
        """
        del input_data  # unused; refuse path
        raise PermissionError(
            "Engine v1 refuses residual/cochain execute_step; "
            "use DomainWorker (urn:omega:execution:domain_worker:v1.0.0) "
            "and functional residual geometry."
        )

    def verify_output(
        self, output: EngineOutput
    ) -> CheckedEngineOutput | RefusedEngineOutput:
        """Structural hash check only — no residual geometry recomputation."""
        data_bytes = json.dumps(
            {
                "vec": output.residual_vector,
                "status": output.status,
                "task_id": output.task_id,
            },
            sort_keys=True,
        ).encode("utf-8")
        expected_hash = hashlib.sha256(data_bytes).hexdigest()

        if output.output_hash != expected_hash:
            return RefusedEngineOutput(
                output=output,
                refusal_reason=(
                    f"Output hash mismatch: expected {expected_hash}, got {output.output_hash}"
                ),
            )

        # Engine does not recompute phi1_mass; DomainWorker/functional owns that invariant.
        v_hash = hashlib.sha256(
            f"verify:{output.output_hash}".encode("utf-8")
        ).hexdigest()
        return CheckedEngineOutput(
            output=output,
            verification_hash=v_hash,
            authority_effect="FactOnly",
        )


class LicensedEngine(Engine):
    """Compatibility Engine fenced from admitted transitions until P3-07E."""

    def execute_licensed_transition(
        self, input_data: LicensedTransitionInput
    ) -> EngineAction | RefusedEngineOutput:
        if not input_data.license_ref or not str(input_data.license_ref).strip():
            refused = EngineOutput(
                task_id="engine_refuse",
                status="REFUSED",
                residual_vector=[],
                phi1_mass=0.0,
                output_hash="",
                authority_effect="Refused",
            )
            return RefusedEngineOutput(
                output=refused,
                refusal_reason="engine_requires_action_license",
            )

        refused = EngineOutput(
            task_id="engine_refuse",
            status="REFUSED",
            residual_vector=[],
            phi1_mass=0.0,
            output_hash="",
            authority_effect="Refused",
        )
        return RefusedEngineOutput(
            output=refused,
            refusal_reason="engine_admitted_transition_fenced_until_p3_07e",
        )


def verify_engine_contract(engine: Engine) -> Dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "engine_id": engine.engine_id,
        "schema_hash": engine.schema_hash,
        "implements": list(engine.implements),
        "authority_effect": "None",
        "declared_contract_authority_effect": "StateTransition",
        "admissible": False,
        "execution_fence": "P3-07E",
        "forbids": sorted(_FORBIDDEN_ENGINE_MATH),
    }


__all__ = [
    "Engine",
    "LicensedEngine",
    "EngineInput",
    "EngineOutput",
    "CheckedEngineOutput",
    "RefusedEngineOutput",
    "LicensedTransitionInput",
    "EngineAction",
    "verify_engine_contract",
    "CONTRACT_ID",
    "SCHEMA_VERSION",
]
