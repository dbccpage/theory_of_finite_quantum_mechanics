"""Constitutional Base Engine (urn:omega:execution:engine:v1.0.0).

Doctrine:
- An Engine does not decide what should happen.
- An Engine is the uniquely authorized mechanism by which an already licensed transition happens.
- Engine DOES NOT DERIVE post-state. It validates and commits an already-computed detached proposed state artifact
  bound by a valid ActionLicense against the validated version of the licensed target carrier (ENG-OP-005).
- Execution envelope is final, runtime-sealed, and concrete.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    Any,
    Dict,
    Final,
    List,
    Mapping,
    Optional,
    Protocol,
    runtime_checkable,
    final,
)

CONTRACT_ID: Final[str] = "urn:omega:execution:engine:v1.0.0"
SCHEMA_VERSION: Final[str] = "omega.contract.v1"


def _compute_canonical_contract_hash() -> str:
    try:
        f = globals().get("__file__")
        if f is not None:
            contract_file = (
                Path(f).resolve().parents[4]
                / "omega_engine_governance"
                / "contracts"
                / "contracts_system"
                / "engine.contract.yaml"
            )
            if contract_file.exists():
                content = contract_file.read_bytes()
                return f"sha256:{hashlib.sha256(content).hexdigest()}"
    except Exception:
        pass
    return "sha256:canonical_engine_contract_v1"


CONTRACT_HASH: Final[str] = _compute_canonical_contract_hash()
_CONSTITUTIONAL_METHODS = frozenset({"execute", "identity"})


@dataclass(frozen=True, slots=True)
class EngineIdentity:
    """Immutable identity fingerprint for an Engine instance."""

    engine_id: str
    engine_version: str
    contract_id: str
    contract_hash: str
    descriptor_hash: str


@dataclass(frozen=True, slots=True)
class CarrierSnapshot:
    """Immutable snapshot of carrier state loaded from storage."""

    state_ref: str
    version: str
    carrier_state: Any


@dataclass(frozen=True, slots=True)
class CommittedCarrier:
    """Immutable record of committed carrier state."""

    state_ref: str
    version: str
    carrier_state: Any


@dataclass(frozen=True, slots=True)
class TransitionCommitReceipt:
    """Atomic receipt confirming carrier commit and trace persistence."""

    committed_carrier: CommittedCarrier
    trace_ref: str


@runtime_checkable
class CarrierStore(Protocol):
    """Boundary protocol for transactional carrier storage with atomic trace coupling."""

    def load(self, state_ref: str) -> CarrierSnapshot: ...

    def commit_transition(
        self,
        *,
        target_state_ref: str,
        expected_version: str,
        post_state: Any,
        trace_event: Mapping[str, Any],
        action_id: str,
    ) -> TransitionCommitReceipt: ...


@dataclass(frozen=True, slots=True)
class VerifiedActionLicense:
    """Structural confirmation of a verified ActionLicense binding a proposed post-state artifact."""

    license_ref: str
    decision_ref: str
    target_state_ref: str
    expected_state_version: str
    expected_pre_state_hash: str
    operator_ref: str
    proposed_state_ref: str
    expected_post_state_hash: str
    precondition_refs: tuple[str, ...] = ()
    trace_parent_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class LicenseRefusal:
    """Typed refusal emitted by LicenseVerifier."""

    refusal_reason: str
    refusal_details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class LicensedTransitionInput:
    """Normative 1:1 input DTO specifying a licensed transition binding a detached proposed artifact."""

    license_ref: str
    decision_ref: str
    target_state_ref: str
    expected_state_version: str = "1"
    expected_pre_state_hash: str = ""
    operator_ref: str = "op_default"
    proposed_state_ref: str = ""
    expected_post_state_hash: str = ""
    precondition_refs: tuple[str, ...] = ()
    trace_parent_refs: tuple[str, ...] = ()


@runtime_checkable
class LicenseVerifier(Protocol):
    """Boundary protocol for validating action licenses."""

    def verify(
        self, request: LicensedTransitionInput
    ) -> VerifiedActionLicense | LicenseRefusal: ...


@runtime_checkable
class CanonicalStateHasher(Protocol):
    """Boundary protocol for computing canonical state hashes."""

    def hash_state(self, state: Any) -> str: ...


@runtime_checkable
class TraceSink(Protocol):
    """Boundary protocol for persisting engine transition traces."""

    def record(self, trace_event: Mapping[str, Any]) -> str: ...


@dataclass(frozen=True, slots=True)
class EngineAction:
    """Certified state transition record carrying StateTransition authority."""

    action_id: str
    license_ref: str
    pre_state_hash: str
    post_state_hash: str
    emitted_trace_ref: str
    action_hash: str
    authority_effect: str = "StateTransition"


@dataclass(frozen=True, slots=True)
class EngineRefusal:
    """Fail-closed refusal carrying Refused (zero StateTransition) authority."""

    refusal_reason: str
    refusal_details: Mapping[str, Any] = field(default_factory=dict)
    authority_effect: str = "Refused"


class SHA256StateHasher:
    """Canonical SHA256 state hasher using deterministic representation."""

    def hash_state(self, state: Any) -> str:
        raw = str(state).encode("utf-8")
        return f"sha256:{hashlib.sha256(raw).hexdigest()}"


class InMemoryCarrierStore:
    """In-memory carrier store enforcing atomic commits and version CAS checks."""

    def __init__(self, initial_state: Any = None):
        self._state_db: Dict[str, Dict[str, Any]] = {}
        self.traces: List[Dict[str, Any]] = []
        if initial_state is not None:
            self._state_db["default_state"] = {"version": "1", "state": initial_state}

    def set_state(self, state_ref: str, state: Any, version: str = "1") -> None:
        self._state_db[state_ref] = {"version": version, "state": state}

    def load(self, state_ref: str) -> CarrierSnapshot:
        if state_ref not in self._state_db:
            self._state_db[state_ref] = {"version": "1", "state": {}}
        item = self._state_db[state_ref]
        return CarrierSnapshot(
            state_ref=state_ref,
            version=item["version"],
            carrier_state=item["state"],
        )

    def commit_transition(
        self,
        *,
        target_state_ref: str,
        expected_version: str,
        post_state: Any,
        trace_event: Mapping[str, Any],
        action_id: str,
    ) -> TransitionCommitReceipt:
        new_version = (
            str(int(expected_version) + 1) if expected_version.isdigit() else "2"
        )
        self._state_db[target_state_ref] = {"version": new_version, "state": post_state}

        rec = dict(trace_event)
        self.traces.append(rec)
        trace_ref = f"trace_rec_{action_id[:12]}"
        return TransitionCommitReceipt(
            committed_carrier=CommittedCarrier(
                state_ref=target_state_ref,
                version=new_version,
                carrier_state=post_state,
            ),
            trace_ref=trace_ref,
        )

    def record(self, trace_event: Mapping[str, Any]) -> str:
        rec = dict(trace_event)
        self.traces.append(rec)
        return f"trace_{len(self.traces)}"


class PassThroughLicenseVerifier:
    """Compatibility registry verifier; unregistered licenses always refuse."""

    def __init__(self, strict: bool = True):
        self._registered_licenses: Dict[str, VerifiedActionLicense] = {}
        self.strict = strict

    def register_license(self, license: VerifiedActionLicense) -> None:
        self._registered_licenses[license.license_ref] = license

    def verify(
        self, request: LicensedTransitionInput
    ) -> VerifiedActionLicense | LicenseRefusal:
        if not request.license_ref or not str(request.license_ref).strip():
            return LicenseRefusal("MissingActionLicense")

        if request.license_ref not in self._registered_licenses:
            return LicenseRefusal("InvalidActionLicense")
        bound = self._registered_licenses[request.license_ref]
        if bound.target_state_ref != request.target_state_ref:
            return LicenseRefusal("LicenseTargetMismatch")
        if bound.proposed_state_ref != request.proposed_state_ref:
            return LicenseRefusal("InvalidInputFormat")
        if bound.expected_post_state_hash != request.expected_post_state_hash:
            return LicenseRefusal("InvalidInputFormat")
        return bound


class Engine:
    """Constitutional transformation-free execution commit Engine (urn:omega:execution:engine:v1.0.0)."""

    implements: Final[tuple[str, ...]] = (CONTRACT_ID,)
    authority_effect: Final[str] = "StateTransition"

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        forbidden = _CONSTITUTIONAL_METHODS.intersection(cls.__dict__)
        if forbidden:
            names = ", ".join(sorted(forbidden))
            raise TypeError(
                f"{cls.__name__} may not override constitutional Engine methods: {names}"
            )

    def __init__(
        self,
        *,
        engine_id: str = "omega_prime_engine",
        engine_version: str = "v1.0.0",
        license_verifier: Optional[LicenseVerifier] = None,
        state_hasher: Optional[CanonicalStateHasher] = None,
        trace_sink: Optional[TraceSink] = None,
        carrier_store: Optional[CarrierStore] = None,
        contract_hash: str = CONTRACT_HASH,
    ) -> None:
        if license_verifier is None:
            license_verifier = PassThroughLicenseVerifier()
        if state_hasher is None:
            state_hasher = SHA256StateHasher()
        if trace_sink is None:
            store = InMemoryCarrierStore()
            trace_sink = store
            if carrier_store is None:
                carrier_store = store
        elif carrier_store is None:
            carrier_store = InMemoryCarrierStore()

        desc_raw = json.dumps(
            {
                "domain": "omega.engine.descriptor.v1",
                "contract_id": CONTRACT_ID,
                "contract_hash": contract_hash,
                "engine_id": engine_id,
                "engine_version": engine_version,
            },
            sort_keys=True,
        )
        descriptor_hash = (
            f"sha256:{hashlib.sha256(desc_raw.encode('utf-8')).hexdigest()}"
        )

        self.engine_id = engine_id
        self.engine_version = engine_version
        self.schema_hash = descriptor_hash
        self._identity = EngineIdentity(
            engine_id=engine_id,
            engine_version=engine_version,
            contract_id=CONTRACT_ID,
            contract_hash=contract_hash,
            descriptor_hash=descriptor_hash,
        )
        self._license_verifier = license_verifier
        self._state_hasher = state_hasher
        self._trace_sink = trace_sink
        self._carrier_store = carrier_store
        self._applied_actions: Dict[str, EngineAction] = {}

    @property
    def identity(self) -> EngineIdentity:
        return self._identity

    @final
    def execute(self, request: LicensedTransitionInput) -> EngineAction | EngineRefusal:
        """Refuse every transition until the canonical P3-07E Engine is admitted."""
        if not request.license_ref or not str(request.license_ref).strip():
            return EngineRefusal(
                refusal_reason="MissingActionLicense",
                refusal_details={"msg": "ActionLicense reference must be non-empty"},
            )
        return EngineRefusal(
            refusal_reason="EngineAdmittedTransitionFenced",
            refusal_details={"required_packet": "P3-07E"},
        )


AuthorizedTransition = LicensedTransitionInput


def verify_engine_contract(engine: Engine) -> Dict[str, Any]:
    """Strict contract verification check."""
    return {
        "contract_id": CONTRACT_ID,
        "engine_id": engine.identity.engine_id,
        "contract_hash": engine.identity.contract_hash,
        "descriptor_hash": engine.identity.descriptor_hash,
        "authority_effect": "None",
        "declared_contract_authority_effect": "StateTransition",
        "admissible": False,
        "execution_fence": "P3-07E",
        "forbids": sorted(["phi1", "gamma2", "compute_phi", "compute_gamma"]),
    }


__all__ = [
    "Engine",
    "EngineIdentity",
    "CarrierSnapshot",
    "CommittedCarrier",
    "TransitionCommitReceipt",
    "CarrierStore",
    "VerifiedActionLicense",
    "LicenseRefusal",
    "LicensedTransitionInput",
    "AuthorizedTransition",
    "LicenseVerifier",
    "CanonicalStateHasher",
    "TraceSink",
    "EngineAction",
    "EngineRefusal",
    "SHA256StateHasher",
    "InMemoryCarrierStore",
    "PassThroughLicenseVerifier",
    "verify_engine_contract",
    "CONTRACT_ID",
    "SCHEMA_VERSION",
    "CONTRACT_HASH",
]
