from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/witness_receipt_dag.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


from pydantic.dataclasses import dataclass
from enum import Enum
from typing import Any


class _RustSurfaceMeta(type):
    def __getattr__(cls, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {cls.__name__}.{name} is not ported"
            )

        return unavailable


class _RustSurfaceObject(metaclass=_RustSurfaceMeta):
    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {type(self).__name__}.{name} is not ported"
            )

        return unavailable


WITNESS_PACKET_SCHEMA_VERSION: Any = None


WITNESS_RECEIPT_SCHEMA_VERSION: Any = None


WITNESS_BUNDLE_SCHEMA_VERSION: Any = None


WITNESS_VERIFICATION_SCHEMA_VERSION: Any = None


S04_001_FROZEN_BASE: Any = None


S04_001_PACKET_ID: Any = None


S04_001_GOAL_ID: Any = None


S04_001_HOST_ID: Any = None


S04_001_HUMAN_ID: Any = None


S04_001_OBSERVER_DOMAIN: Any = None


S04_001_STATE_DOMAIN: Any = None


S04_001_EVIDENCE_CEILING: Any = None


S04_001_UPSTREAM_PACKET_ID: Any = None


S04_001_UPSTREAM_PACKET_SHA256: Any = None


S04_001_UPSTREAM_RECEIPT_ARTIFACT_SHA256: Any = None


S04_001_WRITE_SURFACE: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class FrozenWitnessSourceV1(_RustSurfaceObject):
    """Structural mirror of Rust ``FrozenWitnessSourceV1``."""

    path: Any = None
    sha256: Any = None
    byte_len: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("path", "sha256", "byte_len")
        if len(args) > len(names):
            raise TypeError(
                "FrozenWitnessSourceV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


S04_001_SOURCE_MANIFEST: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class WitnessBudgetsV1(_RustSurfaceObject):
    """Structural mirror of Rust ``WitnessBudgetsV1``."""

    attempt_budget: Any = None
    repair_budget: Any = None
    successor_budget: Any = None
    time_budget_seconds: Any = None
    process_budget: Any = None
    token_budget: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "attempt_budget",
            "repair_budget",
            "successor_budget",
            "time_budget_seconds",
            "process_budget",
            "token_budget",
        )
        if len(args) > len(names):
            raise TypeError("WitnessBudgetsV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


WitnessRoleV1 = Enum(
    "WitnessRoleV1",
    {
        "Host": "Host",
        "Producer": "Producer",
        "IndependentEvaluator": "IndependentEvaluator",
        "AuthorityWitness": "AuthorityWitness",
        "DeterministicGate": "DeterministicGate",
        "HumanAuthority": "HumanAuthority",
    },
    type=str,
)
WitnessRoleV1.__doc__ = "Structural mirror of Rust ``WitnessRoleV1`` variants."


ALL: Any = None


fn: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class FrozenRoleIdentityV1(_RustSurfaceObject):
    """Structural mirror of Rust ``FrozenRoleIdentityV1``."""

    role: Any = None
    identity_id: Any = None
    session_id: Any = None
    context_sha256: Any = None
    visibility_class: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "role",
            "identity_id",
            "session_id",
            "context_sha256",
            "visibility_class",
        )
        if len(args) > len(names):
            raise TypeError(
                "FrozenRoleIdentityV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


WitnessPermissionV1 = Enum(
    "WitnessPermissionV1",
    {
        "ReadFrozenSources": "ReadFrozenSources",
        "VerifyReceipts": "VerifyReceipts",
        "RecordHumanDecision": "RecordHumanDecision",
    },
    type=str,
)
WitnessPermissionV1.__doc__ = (
    "Structural mirror of Rust ``WitnessPermissionV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class FrozenWitnessObserverV1(_RustSurfaceObject):
    """Structural mirror of Rust ``FrozenWitnessObserverV1``."""

    observer_id: Any = None
    observer_domain: Any = None
    state_domain: Any = None
    frozen_base: Any = None
    observer_hash: Any = None
    visible_artifact_hashes: Any = None
    hidden_artifact_classes: Any = None
    tool_permissions: Any = None
    write_surface: Any = None
    evidence_ceiling: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "observer_id",
            "observer_domain",
            "state_domain",
            "frozen_base",
            "observer_hash",
            "visible_artifact_hashes",
            "hidden_artifact_classes",
            "tool_permissions",
            "write_surface",
            "evidence_ceiling",
        )
        if len(args) > len(names):
            raise TypeError(
                "FrozenWitnessObserverV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class UpstreamAdmissionReferenceV1(_RustSurfaceObject):
    """Structural mirror of Rust ``UpstreamAdmissionReferenceV1``."""

    goal_id: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    receipt_artifact_sha256: Any = None
    terminal: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "goal_id",
            "packet_id",
            "packet_sha256",
            "receipt_artifact_sha256",
            "terminal",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "UpstreamAdmissionReferenceV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class WitnessTowerPacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``WitnessTowerPacketV1``."""

    schema_version: Any = None
    packet_id: Any = None
    goal_id: Any = None
    frozen_base: Any = None
    source_manifest: Any = None
    upstream: Any = None
    budgets: Any = None
    role_plan: Any = None
    observer: Any = None
    write_surface: Any = None
    evidence_ceiling: Any = None
    authority_effect: Any = None
    promotion_constructor_available: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "goal_id",
            "frozen_base",
            "source_manifest",
            "upstream",
            "budgets",
            "role_plan",
            "observer",
            "write_surface",
            "evidence_ceiling",
            "authority_effect",
            "promotion_constructor_available",
        )
        if len(args) > len(names):
            raise TypeError(
                "WitnessTowerPacketV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def validate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::validate"
    )


WitnessReceiptKindV1 = Enum(
    "WitnessReceiptKindV1",
    {
        "Producer": "Producer",
        "IndependentEvaluation": "IndependentEvaluation",
        "AuthorityWitness": "AuthorityWitness",
        "DeterministicGate": "DeterministicGate",
        "HumanDecision": "HumanDecision",
    },
    type=str,
)
WitnessReceiptKindV1.__doc__ = (
    "Structural mirror of Rust ``WitnessReceiptKindV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class WitnessReceiptParentV1(_RustSurfaceObject):
    """Structural mirror of Rust ``WitnessReceiptParentV1``."""

    receipt_id: Any = None
    receipt_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("receipt_id", "receipt_sha256")
        if len(args) > len(names):
            raise TypeError(
                "WitnessReceiptParentV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


HumanDecisionOutcomeV1 = Enum(
    "HumanDecisionOutcomeV1",
    {
        "PendingHumanPromotion": "PendingHumanPromotion",
        "PromotionRequested": "PromotionRequested",
        "Rejected": "Rejected",
    },
    type=str,
)
HumanDecisionOutcomeV1.__doc__ = (
    "Structural mirror of Rust ``HumanDecisionOutcomeV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class HumanDecisionV1(_RustSurfaceObject):
    """Structural mirror of Rust ``HumanDecisionV1``."""

    decision_id: Any = None
    recorded_by_host_id: Any = None
    human_actor_id: Any = None
    outcome: Any = None
    basis: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "decision_id",
            "recorded_by_host_id",
            "human_actor_id",
            "outcome",
            "basis",
        )
        if len(args) > len(names):
            raise TypeError("HumanDecisionV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class WitnessReceiptMaterialV1(_RustSurfaceObject):
    """Structural mirror of Rust ``WitnessReceiptMaterialV1``."""

    schema_version: Any = None
    receipt_id: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    kind: Any = None
    issuer_identity_id: Any = None
    issuer_session_id: Any = None
    issuer_context_sha256: Any = None
    graph_rank: Any = None
    parents: Any = None
    evidence_hashes: Any = None
    evidence_ceiling: Any = None
    human_decision: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "receipt_id",
            "packet_id",
            "packet_sha256",
            "kind",
            "issuer_identity_id",
            "issuer_session_id",
            "issuer_context_sha256",
            "graph_rank",
            "parents",
            "evidence_hashes",
            "evidence_ceiling",
            "human_decision",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "WitnessReceiptMaterialV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class WitnessReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``WitnessReceiptV1``."""

    material: Any = None
    receipt_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("material", "receipt_sha256")
        if len(args) > len(names):
            raise TypeError("WitnessReceiptV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class JointAuthorityBoundaryV1(_RustSurfaceObject):
    """Structural mirror of Rust ``JointAuthorityBoundaryV1``."""

    identity_separated: Any = None
    session_separated: Any = None
    context_separated: Any = None
    receipt_dag_acyclic: Any = None
    rank_ordered: Any = None
    deterministic_gate_present: Any = None
    human_decision_recorded: Any = None
    promotion_requested: Any = None
    promotion_constructor_called: Any = None
    authorized_local_result_created: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "identity_separated",
            "session_separated",
            "context_separated",
            "receipt_dag_acyclic",
            "rank_ordered",
            "deterministic_gate_present",
            "human_decision_recorded",
            "promotion_requested",
            "promotion_constructor_called",
            "authorized_local_result_created",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "JointAuthorityBoundaryV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class WitnessTowerVerificationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``WitnessTowerVerificationV1``."""

    schema_version: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    role_plan_sha256: Any = None
    receipt_dag_sha256: Any = None
    human_decision: Any = None
    boundary: Any = None
    terminal: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "packet_sha256",
            "role_plan_sha256",
            "receipt_dag_sha256",
            "human_decision",
            "boundary",
            "terminal",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "WitnessTowerVerificationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class WitnessTowerReceiptBundleV1(_RustSurfaceObject):
    """Structural mirror of Rust ``WitnessTowerReceiptBundleV1``."""

    schema_version: Any = None
    packet_sha256: Any = None
    receipts: Any = None
    verification: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("schema_version", "packet_sha256", "receipts", "verification")
        if len(args) > len(names):
            raise TypeError(
                "WitnessTowerReceiptBundleV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def canonical_s04_001_packet_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``canonical_s04_001_packet_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::canonical_s04_001_packet_v1"
    )


def witness_packet_canonical_bytes_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``witness_packet_canonical_bytes_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::witness_packet_canonical_bytes_v1"
    )


def witness_packet_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``witness_packet_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::witness_packet_sha256_v1"
    )


def witness_receipt_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``witness_receipt_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::witness_receipt_sha256_v1"
    )


def canonical_s04_001_receipt_bundle_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``canonical_s04_001_receipt_bundle_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::canonical_s04_001_receipt_bundle_v1"
    )


def record_human_decision_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``record_human_decision_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::record_human_decision_v1"
    )


def verify_witness_tower_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``verify_witness_tower_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::verify_witness_tower_v1"
    )


def replay_witness_tower_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``replay_witness_tower_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::replay_witness_tower_v1"
    )


def observer_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``observer_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::observer_sha256_v1"
    )


WitnessTowerError = Enum(
    "WitnessTowerError",
    {
        "SchemaMismatch": "SchemaMismatch",
        "EmptyField": "EmptyField",
        "InvalidSha256": "InvalidSha256",
        "InvalidGitCommit": "InvalidGitCommit",
        "NonCanonicalList": "NonCanonicalList",
        "FrozenPacketChanged": "FrozenPacketChanged",
        "SourceManifestChanged": "SourceManifestChanged",
        "SourceUnavailable": "SourceUnavailable",
        "UpstreamReferenceChanged": "UpstreamReferenceChanged",
        "BudgetOutsideAdmission": "BudgetOutsideAdmission",
        "WriteSurfaceChanged": "WriteSurfaceChanged",
        "EvidenceCeilingChanged": "EvidenceCeilingChanged",
        "RolePlanChanged": "RolePlanChanged",
        "IdentityCollision": "IdentityCollision",
        "SessionCollision": "SessionCollision",
        "ContextCollision": "ContextCollision",
        "ObserverChanged": "ObserverChanged",
        "ObserverHashMismatch": "ObserverHashMismatch",
        "AuthorityExpansion": "AuthorityExpansion",
        "PacketHashMismatch": "PacketHashMismatch",
        "ReceiptHashMismatch": "ReceiptHashMismatch",
        "MissingRequiredReceipt": "MissingRequiredReceipt",
        "UnexpectedReceiptSet": "UnexpectedReceiptSet",
        "ReceiptKindChanged": "ReceiptKindChanged",
        "ReceiptRankChanged": "ReceiptRankChanged",
        "ReceiptIssuerChanged": "ReceiptIssuerChanged",
        "ParentReceiptMissing": "ParentReceiptMissing",
        "ParentHashMismatch": "ParentHashMismatch",
        "FutureParent": "FutureParent",
        "ReceiptCycle": "ReceiptCycle",
        "ParentSetChanged": "ParentSetChanged",
        "HumanDecisionMissing": "HumanDecisionMissing",
        "UnexpectedHumanDecision": "UnexpectedHumanDecision",
        "HumanDecisionIdentityChanged": "HumanDecisionIdentityChanged",
        "HostDecisionIssuerMismatch": "HostDecisionIssuerMismatch",
        "HumanActorMismatch": "HumanActorMismatch",
        "ReplayMismatch": "ReplayMismatch",
        "Json": "Json",
    },
    type=str,
)
WitnessTowerError.__doc__ = "Structural mirror of Rust ``WitnessTowerError`` variants."


def terminal_route(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``terminal_route``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/witness_receipt_dag.rs::terminal_route"
    )




