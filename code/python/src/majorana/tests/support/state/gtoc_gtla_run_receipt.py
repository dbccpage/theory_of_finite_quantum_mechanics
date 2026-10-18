from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


# BEGIN GENERATED RUST SURFACE
# Rust source: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs
# Rust sha256: cb3012dfcfc3ef6e16179bbed45795c88e46375234547a65bd4a4d1aa6a0e806
# Structural parity only; no behavioral or authority claim.
from pydantic.dataclasses import dataclass
from enum import Enum
from typing import Any, TypeAlias


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
RUN_PACKET_SCHEMA_VERSION: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
RUN_RECEIPT_SCHEMA_VERSION: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
RUN_NODE_SCHEMA_VERSION: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
RUN_VERIFICATION_SCHEMA_VERSION: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
RUN_RENDER_SCHEMA_VERSION: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S06_001_FROZEN_BASE: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S06_001_PACKET_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S06_001_GOAL_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S06_001_OBSERVER_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S06_001_RENDERER_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S06_001_EVIDENCE_CEILING: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
SOURCE_RECEIPT_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
DDA_RECEIPT_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
DEFECT_RECEIPT_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
RENDER_RECEIPT_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
TERMINAL_RECEIPT_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S06_001_WRITE_SURFACE: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S06_001_SOURCE_MANIFEST: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S06_001_INPUT_ARTIFACTS: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class FrozenRunSourceV1(_RustSurfaceObject):
    """Structural mirror of Rust ``FrozenRunSourceV1``."""

    path: Any = None
    sha256: Any = None
    bytes: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("path", "sha256", "bytes")
        if len(args) > len(names):
            raise TypeError("FrozenRunSourceV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class RunArtifactBindingV1(_RustSurfaceObject):
    """Structural mirror of Rust ``RunArtifactBindingV1``."""

    path: Any = None
    sha256: Any = None
    bytes: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("path", "sha256", "bytes")
        if len(args) > len(names):
            raise TypeError(
                "RunArtifactBindingV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class RunBudgetsV1(_RustSurfaceObject):
    """Structural mirror of Rust ``RunBudgetsV1``."""

    attempt_budget: Any = None
    repair_budget: Any = None
    successor_budget: Any = None
    time_budget_seconds: Any = None
    process_budget: Any = None
    token_budget: Any = None
    receipt_node_budget: Any = None
    defect_budget: Any = None
    transition_budget: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "attempt_budget",
            "repair_budget",
            "successor_budget",
            "time_budget_seconds",
            "process_budget",
            "token_budget",
            "receipt_node_budget",
            "defect_budget",
            "transition_budget",
        )
        if len(args) > len(names):
            raise TypeError("RunBudgetsV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class FrozenRunObserverV1(_RustSurfaceObject):
    """Structural mirror of Rust ``FrozenRunObserverV1``."""

    observer_id: Any = None
    source_manifest_sha256: Any = None
    visible_artifact_sha256: Any = None
    hidden_context_classes: Any = None
    model_context_available: Any = None
    promotion_constructor_available: Any = None
    authorized_local_result_constructor_available: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "observer_id",
            "source_manifest_sha256",
            "visible_artifact_sha256",
            "hidden_context_classes",
            "model_context_available",
            "promotion_constructor_available",
            "authorized_local_result_constructor_available",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "FrozenRunObserverV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class GtocGtlaRunPacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``GtocGtlaRunPacketV1``."""

    schema_version: Any = None
    packet_id: Any = None
    goal_id: Any = None
    frozen_base: Any = None
    observer: Any = None
    observer_sha256: Any = None
    source_manifest: Any = None
    input_artifacts: Any = None
    initial_residual_ids: Any = None
    licensed_operations: Any = None
    legal_terminals: Any = None
    budgets: Any = None
    evidence_ceiling: Any = None
    exact_write_surface: Any = None
    promotion_constructor_available: Any = None
    authorized_local_result_constructor_available: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "goal_id",
            "frozen_base",
            "observer",
            "observer_sha256",
            "source_manifest",
            "input_artifacts",
            "initial_residual_ids",
            "licensed_operations",
            "legal_terminals",
            "budgets",
            "evidence_ceiling",
            "exact_write_surface",
            "promotion_constructor_available",
            "authorized_local_result_constructor_available",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "GtocGtlaRunPacketV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


RunStepOutcomeV1 = Enum(
    "RunStepOutcomeV1",
    {"Executed": "Executed", "RefusedToExecute": "RefusedToExecute"},
    type=str,
)
RunStepOutcomeV1.__doc__ = "Structural mirror of Rust ``RunStepOutcomeV1`` variants."


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class DdaTransitionReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``DdaTransitionReceiptV1``."""

    sequence: Any = None
    op: Any = None
    before_residual_ids: Any = None
    after_residual_ids: Any = None
    outcome: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "sequence",
            "op",
            "before_residual_ids",
            "after_residual_ids",
            "outcome",
        )
        if len(args) > len(names):
            raise TypeError(
                "DdaTransitionReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ExternalImportV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ExternalImportV1``."""

    import_id: Any = None
    description: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("import_id", "description")
        if len(args) > len(names):
            raise TypeError("ExternalImportV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


RunReceiptKindV1 = Enum(
    "RunReceiptKindV1",
    {
        "Source": "Source",
        "DdaTrace": "DdaTrace",
        "DefectDispositions": "DefectDispositions",
        "CanonicalRender": "CanonicalRender",
        "Terminal": "Terminal",
    },
    type=str,
)
RunReceiptKindV1.__doc__ = "Structural mirror of Rust ``RunReceiptKindV1`` variants."


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class RunReceiptParentV1(_RustSurfaceObject):
    """Structural mirror of Rust ``RunReceiptParentV1``."""

    receipt_id: Any = None
    receipt_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("receipt_id", "receipt_sha256")
        if len(args) > len(names):
            raise TypeError("RunReceiptParentV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class DefectDispositionV1(_RustSurfaceObject):
    """Structural mirror of Rust ``DefectDispositionV1``."""

    defect_id: Any = None
    terminal: Any = None
    evidence_sequences: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("defect_id", "terminal", "evidence_sequences")
        if len(args) > len(names):
            raise TypeError(
                "DefectDispositionV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


RunReceiptPayloadV1 = Enum(
    "RunReceiptPayloadV1",
    {
        "Source": "Source",
        "DdaTrace": "DdaTrace",
        "DefectDispositions": "DefectDispositions",
        "CanonicalRender": "CanonicalRender",
        "Terminal": "Terminal",
    },
    type=str,
)
RunReceiptPayloadV1.__doc__ = (
    "Structural mirror of Rust ``RunReceiptPayloadV1`` variants."
)


def kind(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``kind``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::kind"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class RunReceiptNodeMaterialV1(_RustSurfaceObject):
    """Structural mirror of Rust ``RunReceiptNodeMaterialV1``."""

    schema_version: Any = None
    receipt_id: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    graph_rank: Any = None
    parents: Any = None
    payload: Any = None
    evidence_ceiling: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "receipt_id",
            "packet_id",
            "packet_sha256",
            "graph_rank",
            "parents",
            "payload",
            "evidence_ceiling",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "RunReceiptNodeMaterialV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class RunReceiptNodeV1(_RustSurfaceObject):
    """Structural mirror of Rust ``RunReceiptNodeV1``."""

    material: Any = None
    receipt_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("material", "receipt_sha256")
        if len(args) > len(names):
            raise TypeError("RunReceiptNodeV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class GtocGtlaRunReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``GtocGtlaRunReceiptV1``."""

    schema_version: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    nodes: Any = None
    terminal_receipt_id: Any = None
    claimed_terminal: Any = None
    promotion_requested: Any = None
    promotion_constructor_called: Any = None
    authorized_local_result_created: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "packet_sha256",
            "nodes",
            "terminal_receipt_id",
            "claimed_terminal",
            "promotion_requested",
            "promotion_constructor_called",
            "authorized_local_result_created",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "GtocGtlaRunReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class CanonicalRunRenderV1(_RustSurfaceObject):
    """Structural mirror of Rust ``CanonicalRunRenderV1``."""

    schema_version: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    renderer_id: Any = None
    transitions: Any = None
    dispositions: Any = None
    terminal: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "packet_sha256",
            "renderer_id",
            "transitions",
            "dispositions",
            "terminal",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "CanonicalRunRenderV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class GtocGtlaRunVerificationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``GtocGtlaRunVerificationV1``."""

    schema_version: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    run_receipt_sha256: Any = None
    artifact_closure_sha256: Any = None
    receipt_dag_sha256: Any = None
    dda_trace_sha256: Any = None
    defect_disposition_sha256: Any = None
    canonical_render_sha256: Any = None
    cochain_boundary_sha256: Any = None
    node_count: Any = None
    defect_count: Any = None
    d1_d0_zero: Any = None
    terminal: Any = None
    promotion_requested: Any = None
    promotion_constructor_called: Any = None
    authorized_local_result_created: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "packet_sha256",
            "run_receipt_sha256",
            "artifact_closure_sha256",
            "receipt_dag_sha256",
            "dda_trace_sha256",
            "defect_disposition_sha256",
            "canonical_render_sha256",
            "cochain_boundary_sha256",
            "node_count",
            "defect_count",
            "d1_d0_zero",
            "terminal",
            "promotion_requested",
            "promotion_constructor_called",
            "authorized_local_result_created",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "GtocGtlaRunVerificationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


RunArtifactBytesV1: TypeAlias = Any


def canonical_s06_001_packet_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``canonical_s06_001_packet_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::canonical_s06_001_packet_v1"
    )


def canonical_s06_001_render_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``canonical_s06_001_render_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::canonical_s06_001_render_v1"
    )


def canonical_s06_001_render_bytes_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``canonical_s06_001_render_bytes_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::canonical_s06_001_render_bytes_v1"
    )


def canonical_s06_001_run_receipt_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``canonical_s06_001_run_receipt_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::canonical_s06_001_run_receipt_v1"
    )


def run_packet_canonical_bytes_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``run_packet_canonical_bytes_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::run_packet_canonical_bytes_v1"
    )


def run_packet_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``run_packet_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::run_packet_sha256_v1"
    )


def run_receipt_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``run_receipt_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::run_receipt_sha256_v1"
    )


def run_verification_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``run_verification_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::run_verification_sha256_v1"
    )


def run_receipt_node_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``run_receipt_node_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::run_receipt_node_sha256_v1"
    )


def run_observer_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``run_observer_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::run_observer_sha256_v1"
    )


def parse_run_packet_canonical_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``parse_run_packet_canonical_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::parse_run_packet_canonical_v1"
    )


def parse_run_receipt_canonical_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``parse_run_receipt_canonical_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::parse_run_receipt_canonical_v1"
    )


def parse_run_verification_canonical_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``parse_run_verification_canonical_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::parse_run_verification_canonical_v1"
    )


def canonical_json_line_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``canonical_json_line_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::canonical_json_line_v1"
    )


def reseal_run_receipt_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``reseal_run_receipt_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::reseal_run_receipt_v1"
    )


def verify_gtoc_gtla_run_receipt_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``verify_gtoc_gtla_run_receipt_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::verify_gtoc_gtla_run_receipt_v1"
    )


GtocGtlaRunReceiptError = Enum(
    "GtocGtlaRunReceiptError",
    {
        "Decode": "Decode",
        "Encode": "Encode",
        "NonCanonicalJson": "NonCanonicalJson",
        "PacketDrift": "PacketDrift",
        "PacketBoundaryChanged": "PacketBoundaryChanged",
        "RunBindingMismatch": "RunBindingMismatch",
        "AuthorityExpanded": "AuthorityExpanded",
        "NodeCount": "NodeCount",
        "NodeBindingMismatch": "NodeBindingMismatch",
        "NodeHashMismatch": "NodeHashMismatch",
        "DuplicateReceiptId": "DuplicateReceiptId",
        "DuplicateKind": "DuplicateKind",
        "MissingKind": "MissingKind",
        "MissingParent": "MissingParent",
        "ParentHashMismatch": "ParentHashMismatch",
        "ReceiptCycle": "ReceiptCycle",
        "RankOrIdentityMismatch": "RankOrIdentityMismatch",
        "TopologyMismatch": "TopologyMismatch",
        "ArtifactManifestMismatch": "ArtifactManifestMismatch",
        "MissingArtifact": "MissingArtifact",
        "ArtifactSetMismatch": "ArtifactSetMismatch",
        "ArtifactHashMismatch": "ArtifactHashMismatch",
        "InitialResidualMismatch": "InitialResidualMismatch",
        "ImportedEvidence": "ImportedEvidence",
        "TransitionCount": "TransitionCount",
        "TransitionSequence": "TransitionSequence",
        "TransitionEdgeMismatch": "TransitionEdgeMismatch",
        "RefusalMutatedState": "RefusalMutatedState",
        "TransitionAfterTerminal": "TransitionAfterTerminal",
        "UnlicensedOperation": "UnlicensedOperation",
        "LyingExactRepair": "LyingExactRepair",
        "ResidualProjectionChangedState": "ResidualProjectionChangedState",
        "IntegrationChangedState": "IntegrationChangedState",
        "InvalidTerminalize": "InvalidTerminalize",
        "MissingTerminalize": "MissingTerminalize",
        "DefectCount": "DefectCount",
        "DefectSetMismatch": "DefectSetMismatch",
        "DefectEvidenceMismatch": "DefectEvidenceMismatch",
        "DefectTerminalMismatch": "DefectTerminalMismatch",
        "RendererChanged": "RendererChanged",
        "RenderHashMismatch": "RenderHashMismatch",
        "TerminalMismatch": "TerminalMismatch",
        "IllegalTerminal": "IllegalTerminal",
        "EmptyText": "EmptyText",
        "EmptyList": "EmptyList",
        "NotSortedUnique": "NotSortedUnique",
        "InvalidSha256": "InvalidSha256",
    },
    type=str,
)
GtocGtlaRunReceiptError.__doc__ = (
    "Structural mirror of Rust ``GtocGtlaRunReceiptError`` variants."
)


def terminal_route(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``terminal_route``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs::terminal_route"
    )


# END GENERATED RUST SURFACE


