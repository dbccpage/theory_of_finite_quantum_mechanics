"""Canonical Functional Base Contract & Implementation (functional_base.py).

Doctrine:
- Functional computes measurements over admitted states.
- Functional DOES NOT evaluate, judge admissibility, choose operators, or emit state transitions.
- Solver calls from Functional are permitted ONLY when the measurement definition itself requires solving an optimization problem.
- Functional MAY NOT select among solvers at runtime or interpret convergence as admissibility.
- FunctionalOutput always carries AuthorityEffect: EvidenceOnly.
"""

from __future__ import annotations
import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Final, Optional, Tuple

from omega_engine.crates.trace.base.trace_signal import TraceSignal, TraceSignalKind

CONTRACT_ID: Final[str] = "urn:omega:measurement:functional:v1.0.0"


@dataclass(frozen=True, slots=True)
class FunctionalIdentity:
    """Immutable identity descriptor for a Functional instance."""
    functional_id: str
    functional_version: str
    contract_id: str = CONTRACT_ID
    schema_hash: str = ""


@dataclass(frozen=True, slots=True)
class FunctionalConfig:
    """Immutable configuration envelope for a Functional instance."""
    config_id: str
    params: Dict[str, Any] = field(default_factory=dict)
    config_hash: str = field(default_factory=str)

    def __post_init__(self) -> None:
        if not self.config_hash:
            raw = json.dumps({"config_id": self.config_id, "params": self.params}, sort_keys=True).encode("utf-8")
            object.__setattr__(self, "config_hash", f"sha256:{hashlib.sha256(raw).hexdigest()}")


@dataclass(frozen=True, slots=True)
class FunctionalOutput:
    """Immutable evidence envelope produced by a Functional measurement."""

    functional_id: str
    functional_version: str
    input_ref: str
    input_hash: str
    config_hash: str
    output_hash: str
    values: Dict[str, Any]
    observable_refs: Tuple[str, ...] = ()
    solver_refs: Tuple[str, ...] = ()
    witness_refs: Tuple[str, ...] = ()
    candidate_certificate_refs: Tuple[str, ...] = ()
    range_behavior: str = "NonNegativeReal"
    authority_effect: str = "EvidenceOnly"
    trace_signal: Optional[TraceSignal] = None

    def compute_hash(self) -> str:
        raw = json.dumps(
            {
                "functional_id": self.functional_id,
                "functional_version": self.functional_version,
                "input_hash": self.input_hash,
                "config_hash": self.config_hash,
                "values": self.values,
                "authority_effect": self.authority_effect,
            },
            sort_keys=True,
        ).encode("utf-8")
        return f"sha256:{hashlib.sha256(raw).hexdigest()}"


class FunctionalBase(ABC):
    """Canonical sealed Functional measuring admitted states without judgment or control."""

    contract_id: Final[str] = CONTRACT_ID
    authority_effect: Final[str] = "EvidenceOnly"

    def __init__(
        self,
        functional_id: str = "functional_001",
        functional_version: str = "v1.0.0",
        config: Optional[FunctionalConfig] = None,
    ) -> None:
        self.functional_id = functional_id
        self.functional_version = functional_version
        self.config = config or FunctionalConfig(config_id="default_config")
        self._identity = FunctionalIdentity(
            functional_id=functional_id,
            functional_version=functional_version,
            contract_id=CONTRACT_ID,
        )

    @property
    def identity(self) -> FunctionalIdentity:
        return self._identity

    def compute(self, state: Any, input_ref: str = "state_ref_001") -> FunctionalOutput:
        """Final execution envelope for functional measurement."""
        state_raw = str(state).encode("utf-8")
        input_hash = f"sha256:{hashlib.sha256(state_raw).hexdigest()}"

        values, solver_refs, candidate_cert_refs = self._compute_values(state)

        signal = TraceSignal(
            source_ref=f"functional:{self.functional_id}",
            source_contract_ref=CONTRACT_ID,
            event_kind=TraceSignalKind.FUNCTIONAL_MEASURED.value,
            payload={
                "functional_id": self.functional_id,
                "values": values,
                "input_hash": input_hash,
            },
            authority_effect="None",
        )

        unhashed = FunctionalOutput(
            functional_id=self.functional_id,
            functional_version=self.functional_version,
            input_ref=input_ref,
            input_hash=input_hash,
            config_hash=self.config.config_hash,
            output_hash="",
            values=values,
            solver_refs=solver_refs,
            candidate_certificate_refs=candidate_cert_refs,
            authority_effect="EvidenceOnly",
            trace_signal=signal,
        )

        return FunctionalOutput(
            functional_id=unhashed.functional_id,
            functional_version=unhashed.functional_version,
            input_ref=unhashed.input_ref,
            input_hash=unhashed.input_hash,
            config_hash=unhashed.config_hash,
            output_hash=unhashed.compute_hash(),
            values=unhashed.values,
            solver_refs=unhashed.solver_refs,
            candidate_certificate_refs=unhashed.candidate_certificate_refs,
            authority_effect=unhashed.authority_effect,
            trace_signal=signal,
        )

    @abstractmethod
    def _compute_values(
        self, state: Any
    ) -> Tuple[Dict[str, Any], Tuple[str, ...], Tuple[str, ...]]:
        """Internal measurement logic returning (values_dict, solver_refs, candidate_certificate_refs)."""


__all__ = [
    "FunctionalBase",
    "FunctionalIdentity",
    "FunctionalConfig",
    "FunctionalOutput",
    "CONTRACT_ID",
]
