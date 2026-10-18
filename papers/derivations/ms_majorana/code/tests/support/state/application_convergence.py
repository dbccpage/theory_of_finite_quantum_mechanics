from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/application_convergence.rs``.

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


APPLICATION_CONVERGENCE_PACKET_SCHEMA_V1: Any = None


APPLICATION_CONVERGENCE_RECEIPT_SCHEMA_V1: Any = None


APPLICATION_CONVERGENCE_VERIFICATION_SCHEMA_V1: Any = None


ApplicationLaneV1 = Enum(
    "ApplicationLaneV1",
    {
        "PromptPackets": "PromptPackets",
        "Api": "Api",
        "BusinessPlanAnalyzer": "BusinessPlanAnalyzer",
        "Sweeper": "Sweeper",
        "RipPapers": "RipPapers",
        "Corrigibility": "Corrigibility",
        "SymbolGame": "SymbolGame",
        "Mub": "Mub",
        "ResidualFamilies": "ResidualFamilies",
        "CertifierLoop": "CertifierLoop",
        "FiniteLambdaLedger": "FiniteLambdaLedger",
    },
    type=str,
)
ApplicationLaneV1.__doc__ = "Structural mirror of Rust ``ApplicationLaneV1`` variants."


ALL: Any = None


fn: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class LaneConvergenceReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``LaneConvergenceReceiptV1``."""

    lane: Any = None
    packet_path: Any = None
    packet_sha256: Any = None
    evidence_manifest_sha256: Any = None
    owner_paths: Any = None
    adapter_paths: Any = None
    focused_receipt_sha256: Any = None
    terminal: Any = None
    residual_ids: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "lane",
            "packet_path",
            "packet_sha256",
            "evidence_manifest_sha256",
            "owner_paths",
            "adapter_paths",
            "focused_receipt_sha256",
            "terminal",
            "residual_ids",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "LaneConvergenceReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ResidualUnionEntryV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ResidualUnionEntryV1``."""

    residual_id: Any = None
    owner: Any = None
    source_lanes: Any = None
    terminal: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("residual_id", "owner", "source_lanes", "terminal")
        if len(args) > len(names):
            raise TypeError(
                "ResidualUnionEntryV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ConvergenceWitnessPlanV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ConvergenceWitnessPlanV1``."""

    producer_identity_id: Any = None
    independent_evaluator_identity_id: Any = None
    authority_witness_identity_id: Any = None
    deterministic_gate_identity_id: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "producer_identity_id",
            "independent_evaluator_identity_id",
            "authority_witness_identity_id",
            "deterministic_gate_identity_id",
        )
        if len(args) > len(names):
            raise TypeError(
                "ConvergenceWitnessPlanV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ApplicationConvergencePacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ApplicationConvergencePacketV1``."""

    schema_version: Any = None
    packet_id: Any = None
    frozen_base: Any = None
    lanes: Any = None
    residual_union: Any = None
    witnesses: Any = None
    evidence_ceiling: Any = None
    product_terminal_is_authority: Any = None
    promotion_permission: Any = None
    gate_activated: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "frozen_base",
            "lanes",
            "residual_union",
            "witnesses",
            "evidence_ceiling",
            "product_terminal_is_authority",
            "promotion_permission",
            "gate_activated",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "ApplicationConvergencePacketV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


ConvergenceReceiptKindV1 = Enum(
    "ConvergenceReceiptKindV1",
    {
        "LaneBundle": "LaneBundle",
        "IndependentEvaluation": "IndependentEvaluation",
        "AuthorityWitness": "AuthorityWitness",
        "DeterministicGate": "DeterministicGate",
    },
    type=str,
)
ConvergenceReceiptKindV1.__doc__ = (
    "Structural mirror of Rust ``ConvergenceReceiptKindV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ConvergenceReceiptParentV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ConvergenceReceiptParentV1``."""

    receipt_id: Any = None
    receipt_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("receipt_id", "receipt_sha256")
        if len(args) > len(names):
            raise TypeError(
                "ConvergenceReceiptParentV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ConvergenceReceiptMaterialV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ConvergenceReceiptMaterialV1``."""

    schema_version: Any = None
    receipt_id: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    kind: Any = None
    graph_rank: Any = None
    issuer_identity_id: Any = None
    parents: Any = None
    evidence_hashes: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "receipt_id",
            "packet_id",
            "packet_sha256",
            "kind",
            "graph_rank",
            "issuer_identity_id",
            "parents",
            "evidence_hashes",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "ConvergenceReceiptMaterialV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ConvergenceReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ConvergenceReceiptV1``."""

    material: Any = None
    receipt_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("material", "receipt_sha256")
        if len(args) > len(names):
            raise TypeError(
                "ConvergenceReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


HostileFaultV1 = Enum(
    "HostileFaultV1",
    {
        "MalformedPacket": "MalformedPacket",
        "PacketHashTamper": "PacketHashTamper",
        "UnknownResidualFamily": "UnknownResidualFamily",
        "RawTextCanary": "RawTextCanary",
        "StaleOracle": "StaleOracle",
        "EvidenceCycle": "EvidenceCycle",
        "RetryExhaustion": "RetryExhaustion",
        "BrokenLambdaLedger": "BrokenLambdaLedger",
        "WitnessIdentityCollision": "WitnessIdentityCollision",
        "ToolTimeout": "ToolTimeout",
        "PolicyDrift": "PolicyDrift",
        "CommitFailure": "CommitFailure",
        "CrashReplay": "CrashReplay",
        "AuthorityBypass": "AuthorityBypass",
    },
    type=str,
)
HostileFaultV1.__doc__ = "Structural mirror of Rust ``HostileFaultV1`` variants."


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class HostileFaultOutcomeV1(_RustSurfaceObject):
    """Structural mirror of Rust ``HostileFaultOutcomeV1``."""

    fault: Any = None
    terminal: Any = None
    detector_live: Any = None
    append_only_receipts_preserved: Any = None
    promotion_ready_commit_created: Any = None
    replay_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "fault",
            "terminal",
            "detector_live",
            "append_only_receipts_preserved",
            "promotion_ready_commit_created",
            "replay_sha256",
        )
        if len(args) > len(names):
            raise TypeError(
                "HostileFaultOutcomeV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class HostileFaultMatrixV1(_RustSurfaceObject):
    """Structural mirror of Rust ``HostileFaultMatrixV1``."""

    outcomes: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("outcomes", "authority_effect")
        if len(args) > len(names):
            raise TypeError(
                "HostileFaultMatrixV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


HumanDecisionStateV1 = Enum(
    "HumanDecisionStateV1", {"PendingHumanPromotion": "PendingHumanPromotion"}, type=str
)
HumanDecisionStateV1.__doc__ = (
    "Structural mirror of Rust ``HumanDecisionStateV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ApplicationConvergenceVerificationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ApplicationConvergenceVerificationV1``."""

    schema_version: Any = None
    packet_sha256: Any = None
    receipt_dag_sha256: Any = None
    lane_count: Any = None
    residual_count: Any = None
    hostile_fault_count: Any = None
    receipt_count: Any = None
    receipt_dag_acyclic: Any = None
    receipt_dag_rank_ordered: Any = None
    residual_union_complete: Any = None
    human_decision_state: Any = None
    human_decision_recorded: Any = None
    promotion_constructor_called: Any = None
    authorized_local_result_created: Any = None
    gate_activated: Any = None
    terminal: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_sha256",
            "receipt_dag_sha256",
            "lane_count",
            "residual_count",
            "hostile_fault_count",
            "receipt_count",
            "receipt_dag_acyclic",
            "receipt_dag_rank_ordered",
            "residual_union_complete",
            "human_decision_state",
            "human_decision_recorded",
            "promotion_constructor_called",
            "authorized_local_result_created",
            "gate_activated",
            "terminal",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "ApplicationConvergenceVerificationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


ApplicationConvergenceError = Enum(
    "ApplicationConvergenceError",
    {
        "InvalidText": "InvalidText",
        "InvalidHash": "InvalidHash",
        "LaneSetChanged": "LaneSetChanged",
        "LaneCollectionChanged": "LaneCollectionChanged",
        "LaneTerminalChanged": "LaneTerminalChanged",
        "ResidualUnionChanged": "ResidualUnionChanged",
        "WitnessIdentityCollision": "WitnessIdentityCollision",
        "AuthorityExpansion": "AuthorityExpansion",
        "PromotionBoundaryChanged": "PromotionBoundaryChanged",
        "ReceiptDagInvalid": "ReceiptDagInvalid",
        "ReceiptHashMismatch": "ReceiptHashMismatch",
        "FaultMatrixChanged": "FaultMatrixChanged",
        "Json": "Json",
    },
    type=str,
)
ApplicationConvergenceError.__doc__ = (
    "Structural mirror of Rust ``ApplicationConvergenceError`` variants."
)


def validate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/application_convergence.rs::validate"
    )


def application_convergence_packet_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``application_convergence_packet_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/application_convergence.rs::application_convergence_packet_sha256_v1"
    )


def canonical_hostile_fault_matrix_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``canonical_hostile_fault_matrix_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/application_convergence.rs::canonical_hostile_fault_matrix_v1"
    )


def build_application_convergence_receipt_dag_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``build_application_convergence_receipt_dag_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/application_convergence.rs::build_application_convergence_receipt_dag_v1"
    )


def validate_application_convergence_receipt_dag_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate_application_convergence_receipt_dag_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/application_convergence.rs::validate_application_convergence_receipt_dag_v1"
    )


def verify_application_convergence_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``verify_application_convergence_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/application_convergence.rs::verify_application_convergence_v1"
    )




