from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


# BEGIN GENERATED RUST SURFACE
# Rust source: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs
# Rust sha256: da57f9f89dd396cbd1bca72880d024c81a4d3238bd6f78af9add06572c3f160f
# Structural parity only; no behavioral or authority claim.
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


# The Rust value is intentionally not guessed by the structural mirror.
PROTOCOL_SCHEMA_VERSION: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
LEGACY_PACKET_SCHEMA_VERSION: Any = None


GtocGtlaStage = Enum(
    "GtocGtlaStage",
    {
        "Carrier": "Carrier",
        "PrimitiveDifference": "PrimitiveDifference",
        "ZeroRelation": "ZeroRelation",
        "CochainRealization": "CochainRealization",
        "Quotient": "Quotient",
        "ResidualSeparation": "ResidualSeparation",
        "Observer": "Observer",
        "Witnesses": "Witnesses",
        "LicensedTransformation": "LicensedTransformation",
        "SurvivorRouting": "SurvivorRouting",
        "TerminalProposal": "TerminalProposal",
        "PriorWorkLedger": "PriorWorkLedger",
    },
    type=str,
)
GtocGtlaStage.__doc__ = "Structural mirror of Rust ``GtocGtlaStage`` variants."


# The Rust value is intentionally not guessed by the structural mirror.
ALL: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
fn: Any = None


GtocTerminal = Enum(
    "GtocTerminal",
    {
        "ExactRepair": "ExactRepair",
        "StabilizedSurvivor": "StabilizedSurvivor",
        "OpenObstruction": "OpenObstruction",
        "OracleNeeded": "OracleNeeded",
        "LiftLicenseNeeded": "LiftLicenseNeeded",
        "Refused": "Refused",
        "Invalid": "Invalid",
        "InfrastructureFailure": "InfrastructureFailure",
    },
    type=str,
)
GtocTerminal.__doc__ = "Structural mirror of Rust ``GtocTerminal`` variants."


CochainRealizationKind = Enum(
    "CochainRealizationKind",
    {"Exact": "Exact", "Structural": "Structural", "Unresolved": "Unresolved"},
    type=str,
)
CochainRealizationKind.__doc__ = (
    "Structural mirror of Rust ``CochainRealizationKind`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class FrozenObserverContextV1(_RustSurfaceObject):
    """Structural mirror of Rust ``FrozenObserverContextV1``."""

    observer_id: Any = None
    observer_domain: Any = None
    state_domain: Any = None
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
            "observer_hash",
            "visible_artifact_hashes",
            "hidden_artifact_classes",
            "tool_permissions",
            "write_surface",
            "evidence_ceiling",
        )
        if len(args) > len(names):
            raise TypeError(
                "FrozenObserverContextV1 received too many positional arguments"
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
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::validate"
    )


LegacyPacketFieldV1 = Enum(
    "LegacyPacketFieldV1",
    {
        "Carrier": "Carrier",
        "C0": "C0",
        "D0": "D0",
        "C1": "C1",
        "ZeroRel": "ZeroRel",
        "Q1": "Q1",
        "D1": "D1",
        "Gamma2": "Gamma2",
        "Phi1": "Phi1",
        "Classification": "Classification",
        "LicensedLift": "LicensedLift",
        "DdaExecution": "DdaExecution",
        "Terminalization": "Terminalization",
    },
    type=str,
)
LegacyPacketFieldV1.__doc__ = (
    "Structural mirror of Rust ``LegacyPacketFieldV1`` variants."
)


CompileContextFieldV1 = Enum(
    "CompileContextFieldV1",
    {
        "PrimitiveDifference": "PrimitiveDifference",
        "C2": "C2",
        "D1D0Witness": "D1D0Witness",
        "Observer": "Observer",
        "Witnesses": "Witnesses",
        "PriorWorkLedger": "PriorWorkLedger",
    },
    type=str,
)
CompileContextFieldV1.__doc__ = (
    "Structural mirror of Rust ``CompileContextFieldV1`` variants."
)


ProtocolSourceV1 = Enum(
    "ProtocolSourceV1", {"Legacy": "Legacy", "Context": "Context"}, type=str
)
ProtocolSourceV1.__doc__ = "Structural mirror of Rust ``ProtocolSourceV1`` variants."


LegacyLiftV1 = Enum(
    "LegacyLiftV1", {"NoneDeclared": "NoneDeclared", "License": "License"}, type=str
)
LegacyLiftV1.__doc__ = "Structural mirror of Rust ``LegacyLiftV1`` variants."


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class LegacyDdaExecutionV1(_RustSurfaceObject):
    """Structural mirror of Rust ``LegacyDdaExecutionV1``."""

    licensed_transformation: Any = None
    survivor_routing: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("licensed_transformation", "survivor_routing")
        if len(args) > len(names):
            raise TypeError(
                "LegacyDdaExecutionV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class LegacyPacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``LegacyPacketV1``."""

    schema_version: Any = None
    carrier: Any = None
    c0: Any = None
    d0: Any = None
    c1: Any = None
    zero_rel: Any = None
    q1: Any = None
    d1: Any = None
    gamma2: Any = None
    phi1: Any = None
    classification: Any = None
    licensed_lift: Any = None
    dda_execution: Any = None
    terminalization: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "carrier",
            "c0",
            "d0",
            "c1",
            "zero_rel",
            "q1",
            "d1",
            "gamma2",
            "phi1",
            "classification",
            "licensed_lift",
            "dda_execution",
            "terminalization",
        )
        if len(args) > len(names):
            raise TypeError("LegacyPacketV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class LegacyCompileContextV1(_RustSurfaceObject):
    """Structural mirror of Rust ``LegacyCompileContextV1``."""

    primitive_difference: Any = None
    realization: Any = None
    c2: Any = None
    d1_d0_witness: Any = None
    observer: Any = None
    witnesses: Any = None
    prior_work_ledger: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "primitive_difference",
            "realization",
            "c2",
            "d1_d0_witness",
            "observer",
            "witnesses",
            "prior_work_ledger",
        )
        if len(args) > len(names):
            raise TypeError(
                "LegacyCompileContextV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class CompiledStageV1(_RustSurfaceObject):
    """Structural mirror of Rust ``CompiledStageV1``."""

    stage: Any = None
    sources: Any = None
    payloads: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("stage", "sources", "payloads")
        if len(args) > len(names):
            raise TypeError("CompiledStageV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class CompiledProtocolV1(_RustSurfaceObject):
    """Structural mirror of Rust ``CompiledProtocolV1``."""

    schema_version: Any = None
    stages: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("schema_version", "stages")
        if len(args) > len(names):
            raise TypeError("CompiledProtocolV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def stage(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``stage``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::stage"
    )


LegacyAdapterLimitationV1 = Enum(
    "LegacyAdapterLimitationV1",
    {
        "PrimitiveDifferenceRequiresContext": "PrimitiveDifferenceRequiresContext",
        "C2AndCompositionWitnessRequireContext": "C2AndCompositionWitnessRequireContext",
        "ObserverRequiresContext": "ObserverRequiresContext",
        "WitnessesRequireContext": "WitnessesRequireContext",
        "PriorWorkLedgerRequiresContext": "PriorWorkLedgerRequiresContext",
        "DdaExecutionSplitsAcrossStagesNineAndTen": "DdaExecutionSplitsAcrossStagesNineAndTen",
        "ClassificationAndTerminalizationMustAgreeAtStageEleven": "ClassificationAndTerminalizationMustAgreeAtStageEleven",
        "StructuralCompilationDoesNotProveMathematicalCochains": "StructuralCompilationDoesNotProveMathematicalCochains",
    },
    type=str,
)
LegacyAdapterLimitationV1.__doc__ = (
    "Structural mirror of Rust ``LegacyAdapterLimitationV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class StageSourceReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``StageSourceReceiptV1``."""

    stage: Any = None
    sources: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("stage", "sources")
        if len(args) > len(names):
            raise TypeError(
                "StageSourceReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class LegacyCompileReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``LegacyCompileReceiptV1``."""

    source_schema_version: Any = None
    target_schema_version: Any = None
    legacy_field_count: Any = None
    stage_sources: Any = None
    limitations: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "source_schema_version",
            "target_schema_version",
            "legacy_field_count",
            "stage_sources",
            "limitations",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "LegacyCompileReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class LegacyCompileOutputV1(_RustSurfaceObject):
    """Structural mirror of Rust ``LegacyCompileOutputV1``."""

    protocol: Any = None
    receipt: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("protocol", "receipt")
        if len(args) > len(names):
            raise TypeError(
                "LegacyCompileOutputV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def compile_legacy_packet_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``compile_legacy_packet_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::compile_legacy_packet_v1"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ProtocolSchemaReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ProtocolSchemaReceiptV1``."""

    schema_version: Any = None
    stages: Any = None
    terminals: Any = None
    legacy_schema_version: Any = None
    legacy_fields: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "stages",
            "terminals",
            "legacy_schema_version",
            "legacy_fields",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "ProtocolSchemaReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def protocol_schema_receipt_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``protocol_schema_receipt_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::protocol_schema_receipt_v1"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ProtocolStateV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ProtocolStateV1``."""

    schema_version: Any = None
    task_id: Any = None
    current_stage: Any = None
    carrier_hash: Any = None
    observer: Any = None
    residual_ids: Any = None
    license_ids: Any = None
    terminal_proposal: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "task_id",
            "current_stage",
            "carrier_hash",
            "observer",
            "residual_ids",
            "license_ids",
            "terminal_proposal",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError("ProtocolStateV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TransitionProposalV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TransitionProposalV1``."""

    to_stage: Any = None
    observer_hash: Any = None
    state_domain: Any = None
    residual_ids: Any = None
    license_ids: Any = None
    terminal_proposal: Any = None
    authority_effect: Any = None
    evidence_refs: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "to_stage",
            "observer_hash",
            "state_domain",
            "residual_ids",
            "license_ids",
            "terminal_proposal",
            "authority_effect",
            "evidence_refs",
        )
        if len(args) > len(names):
            raise TypeError(
                "TransitionProposalV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def preserving(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``preserving``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::preserving"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TransitionReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TransitionReceiptV1``."""

    sequence: Any = None
    from_stage: Any = None
    to_stage: Any = None
    observer_hash: Any = None
    state_domain: Any = None
    residual_ids: Any = None
    license_ids: Any = None
    terminal_proposal: Any = None
    authority_effect: Any = None
    evidence_refs: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "sequence",
            "from_stage",
            "to_stage",
            "observer_hash",
            "state_domain",
            "residual_ids",
            "license_ids",
            "terminal_proposal",
            "authority_effect",
            "evidence_refs",
        )
        if len(args) > len(names):
            raise TypeError(
                "TransitionReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ProtocolTraceV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ProtocolTraceV1``."""

    schema_version: Any = None
    task_id: Any = None
    carrier_hash: Any = None
    observer: Any = None
    initial_residual_ids: Any = None
    license_ids: Any = None
    receipts: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "task_id",
            "carrier_hash",
            "observer",
            "initial_residual_ids",
            "license_ids",
            "receipts",
        )
        if len(args) > len(names):
            raise TypeError("ProtocolTraceV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ProtocolMachineV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ProtocolMachineV1``."""

    state: Any = None
    initial_residual_ids: Any = None
    receipts: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("state", "initial_residual_ids", "receipts")
        if len(args) > len(names):
            raise TypeError("ProtocolMachineV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def new(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``new``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::new"
    )


def state(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``state``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::state"
    )


def is_terminalized(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``is_terminalized``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::is_terminalized"
    )


def advance(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``advance``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::advance"
    )


def into_trace(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``into_trace``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::into_trace"
    )


CompositionFailureKindV1 = Enum(
    "CompositionFailureKindV1",
    {
        "EdgeDiscontinuity": "EdgeDiscontinuity",
        "SkippedStage": "SkippedStage",
        "ObserverChanged": "ObserverChanged",
        "StateDomainChanged": "StateDomainChanged",
        "ResidualLost": "ResidualLost",
        "LicenseSetChanged": "LicenseSetChanged",
        "TerminalChanged": "TerminalChanged",
        "AuthorityExpanded": "AuthorityExpanded",
    },
    type=str,
)
CompositionFailureKindV1.__doc__ = (
    "Structural mirror of Rust ``CompositionFailureKindV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class CompositionFailureV1(_RustSurfaceObject):
    """Structural mirror of Rust ``CompositionFailureV1``."""

    left_sequence: Any = None
    right_sequence: Any = None
    kind: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("left_sequence", "right_sequence", "kind")
        if len(args) > len(names):
            raise TypeError(
                "CompositionFailureV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class StructuralCochainReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``StructuralCochainReceiptV1``."""

    realization: Any = None
    edge_count: Any = None
    composition_count: Any = None
    failures: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("realization", "edge_count", "composition_count", "failures")
        if len(args) > len(names):
            raise TypeError(
                "StructuralCochainReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TraceValidationReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TraceValidationReceiptV1``."""

    schema_version: Any = None
    transition_count: Any = None
    terminal: Any = None
    authority_effect: Any = None
    cochain: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "transition_count",
            "terminal",
            "authority_effect",
            "cochain",
        )
        if len(args) > len(names):
            raise TypeError(
                "TraceValidationReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def structural_d1_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``structural_d1_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::structural_d1_v1"
    )


def structural_cochain_receipt_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``structural_cochain_receipt_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::structural_cochain_receipt_v1"
    )


def validate_protocol_trace_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate_protocol_trace_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::validate_protocol_trace_v1"
    )


ProtocolError = Enum(
    "ProtocolError",
    {
        "SchemaVersion": "SchemaVersion",
        "EmptyField": "EmptyField",
        "InvalidHash": "InvalidHash",
        "StageCount": "StageCount",
        "StageOrder": "StageOrder",
        "LegacyTerminalMismatch": "LegacyTerminalMismatch",
        "SkippedStage": "SkippedStage",
        "ObserverChanged": "ObserverChanged",
        "StateDomainChanged": "StateDomainChanged",
        "ResidualLost": "ResidualLost",
        "LicenseSetChanged": "LicenseSetChanged",
        "EarlyTerminal": "EarlyTerminal",
        "MissingTerminal": "MissingTerminal",
        "TerminalChanged": "TerminalChanged",
        "TerminalResidualMismatch": "TerminalResidualMismatch",
        "AuthorityExpanded": "AuthorityExpanded",
        "AlreadyTerminalized": "AlreadyTerminalized",
        "ReceiptMismatch": "ReceiptMismatch",
        "TraceNotTerminalized": "TraceNotTerminalized",
        "StructuralCompositionFailure": "StructuralCompositionFailure",
    },
    type=str,
)
ProtocolError.__doc__ = "Structural mirror of Rust ``ProtocolError`` variants."


def terminal_route(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``terminal_route``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs::terminal_route"
    )


# END GENERATED RUST SURFACE


