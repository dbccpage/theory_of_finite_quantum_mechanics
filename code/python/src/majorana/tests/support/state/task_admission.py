from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/task_admission.rs``.

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


TASK_PACKET_SCHEMA_VERSION: Any = None


TASK_ENVELOPE_SCHEMA_VERSION: Any = None


TASK_COMPILATION_SCHEMA_VERSION: Any = None


TASK_LEASE_SCHEMA_VERSION: Any = None


TASK_RECEIPT_SCHEMA_VERSION: Any = None


S03_001_FROZEN_BASE: Any = None


S03_001_PACKET_ID: Any = None


S03_001_GOAL_ID: Any = None


S03_001_OBSERVER_DOMAIN: Any = None


S03_001_STATE_DOMAIN: Any = None


S03_001_EVIDENCE_CEILING: Any = None


S03_001_GOAL_DECLARATION: Any = None


S03_001_HOST_ID: Any = None


S03_001_PRODUCER_ID: Any = None


S03_001_EVALUATOR_ID: Any = None


S03_001_AUTHORITY_WITNESS_ID: Any = None


S03_001_LEASE_ID: Any = None


S03_001_UPSTREAM_REFERENCE_ID: Any = None


S03_001_UPSTREAM_PACKET_ID: Any = None


S03_001_UPSTREAM_SCHEMA_VERSION: Any = None


S03_001_UPSTREAM_PACKET_SHA256: Any = None


S03_001_LEGACY_LEASE_REFERENCE_ID: Any = None


S03_001_LEGACY_LEASE_PATH: Any = None


S03_001_LEGACY_LEASE_SCHEMA_VERSION: Any = None


S03_001_LEGACY_LEASE_SHA256: Any = None


S03_001_LEGACY_SCHEMA_REFERENCE_ID: Any = None


S03_001_LEGACY_SCHEMA_PATH: Any = None


S03_001_LEGACY_SCHEMA_VERSION: Any = None


S03_001_LEGACY_SCHEMA_SHA256: Any = None


S03_001_PACKET_SHA256: Any = None


S03_001_OBSERVER_SHA256: Any = None


S03_001_BUNDLE_SHA256: Any = None


S03_001_WRITE_SURFACE: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class FrozenTaskArtifactV1(_RustSurfaceObject):
    """Structural mirror of Rust ``FrozenTaskArtifactV1``."""

    artifact_id: Any = None
    path: Any = None
    kind: Any = None
    role: Any = None
    sha256: Any = None
    byte_len: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("artifact_id", "path", "kind", "role", "sha256", "byte_len")
        if len(args) > len(names):
            raise TypeError(
                "FrozenTaskArtifactV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


S03_001_SOURCE_MANIFEST: Any = None


TaskArtifactKindV1 = Enum(
    "TaskArtifactKindV1",
    {
        "Markdown": "Markdown",
        "Rust": "Rust",
        "Lean": "Lean",
        "Json": "Json",
        "Yaml": "Yaml",
        "Toml": "Toml",
        "Python": "Python",
        "Text": "Text",
    },
    type=str,
)
TaskArtifactKindV1.__doc__ = (
    "Structural mirror of Rust ``TaskArtifactKindV1`` variants."
)


TaskArtifactRoleV1 = Enum(
    "TaskArtifactRoleV1",
    {
        "Plan": "Plan",
        "Protocol": "Protocol",
        "Policy": "Policy",
        "Test": "Test",
        "LegacyProtocol": "LegacyProtocol",
    },
    type=str,
)
TaskArtifactRoleV1.__doc__ = (
    "Structural mirror of Rust ``TaskArtifactRoleV1`` variants."
)


TaskOperationV1 = Enum(
    "TaskOperationV1",
    {
        "CanonicalizePacket": "CanonicalizePacket",
        "HashArtifacts": "HashArtifacts",
        "ValidateBundle": "ValidateBundle",
        "CheckLease": "CheckLease",
        "IssueLease": "IssueLease",
    },
    type=str,
)
TaskOperationV1.__doc__ = "Structural mirror of Rust ``TaskOperationV1`` variants."


TaskAdmissionPermissionV1 = Enum(
    "TaskAdmissionPermissionV1",
    {
        "ReadFrozenArtifacts": "ReadFrozenArtifacts",
        "CompilePacket": "CompilePacket",
        "ValidatePacket": "ValidatePacket",
        "CheckLeases": "CheckLeases",
        "IssueLease": "IssueLease",
    },
    type=str,
)
TaskAdmissionPermissionV1.__doc__ = (
    "Structural mirror of Rust ``TaskAdmissionPermissionV1`` variants."
)


TaskFreezeStatusV1 = Enum(
    "TaskFreezeStatusV1", {"Unfrozen": "Unfrozen", "Frozen": "Frozen"}, type=str
)
TaskFreezeStatusV1.__doc__ = (
    "Structural mirror of Rust ``TaskFreezeStatusV1`` variants."
)


LegacyReadPolicyV1 = Enum(
    "LegacyReadPolicyV1",
    {"Refuse": "Refuse", "ExplicitReadOnly": "ExplicitReadOnly"},
    type=str,
)
LegacyReadPolicyV1.__doc__ = (
    "Structural mirror of Rust ``LegacyReadPolicyV1`` variants."
)


OraclePolicyV1 = Enum(
    "OraclePolicyV1", {"Route": "Route", "Refuse": "Refuse"}, type=str
)
OraclePolicyV1.__doc__ = "Structural mirror of Rust ``OraclePolicyV1`` variants."


CarrierChangePolicyV1 = Enum(
    "CarrierChangePolicyV1",
    {"RequireLiftLicense": "RequireLiftLicense", "AllowImplicit": "AllowImplicit"},
    type=str,
)
CarrierChangePolicyV1.__doc__ = (
    "Structural mirror of Rust ``CarrierChangePolicyV1`` variants."
)


TaskLeaseModeV1 = Enum("TaskLeaseModeV1", {"Write": "Write"}, type=str)
TaskLeaseModeV1.__doc__ = "Structural mirror of Rust ``TaskLeaseModeV1`` variants."


TaskAdmissionStatusV1 = Enum(
    "TaskAdmissionStatusV1",
    {"CompiledForHostLease": "CompiledForHostLease", "Admitted": "Admitted"},
    type=str,
)
TaskAdmissionStatusV1.__doc__ = (
    "Structural mirror of Rust ``TaskAdmissionStatusV1`` variants."
)


TaskAdmissionSurvivorV1 = Enum(
    "TaskAdmissionSurvivorV1",
    {
        "MissingArtifact": "MissingArtifact",
        "LeaseConflict": "LeaseConflict",
        "LiftLicenseNeeded": "LiftLicenseNeeded",
        "Refused": "Refused",
        "InvalidEvidence": "InvalidEvidence",
        "InfrastructureFailure": "InfrastructureFailure",
    },
    type=str,
)
TaskAdmissionSurvivorV1.__doc__ = (
    "Structural mirror of Rust ``TaskAdmissionSurvivorV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TaskArtifactV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TaskArtifactV1``."""

    artifact_id: Any = None
    path: Any = None
    kind: Any = None
    role: Any = None
    sha256: Any = None
    byte_len: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("artifact_id", "path", "kind", "role", "sha256", "byte_len")
        if len(args) > len(names):
            raise TypeError("TaskArtifactV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ResolvedTaskArtifactV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ResolvedTaskArtifactV1``."""

    artifact_id: Any = None
    path: Any = None
    sha256: Any = None
    byte_len: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("artifact_id", "path", "sha256", "byte_len")
        if len(args) > len(names):
            raise TypeError(
                "ResolvedTaskArtifactV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TaskPacketReferenceV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TaskPacketReferenceV1``."""

    reference_id: Any = None
    packet_id: Any = None
    schema_version: Any = None
    packet_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("reference_id", "packet_id", "schema_version", "packet_sha256")
        if len(args) > len(names):
            raise TypeError(
                "TaskPacketReferenceV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class LegacyPacketReferenceV1(_RustSurfaceObject):
    """Structural mirror of Rust ``LegacyPacketReferenceV1``."""

    reference_id: Any = None
    path: Any = None
    schema_version: Any = None
    sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("reference_id", "path", "schema_version", "sha256")
        if len(args) > len(names):
            raise TypeError(
                "LegacyPacketReferenceV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TaskAdmissionBudgetsV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TaskAdmissionBudgetsV1``."""

    attempt_budget: Any = None
    repair_budget: Any = None
    successor_budget: Any = None
    time_budget_seconds: Any = None
    process_budget: Any = None
    token_budget: Any = None
    max_changed_files: Any = None
    max_diff_bytes: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "attempt_budget",
            "repair_budget",
            "successor_budget",
            "time_budget_seconds",
            "process_budget",
            "token_budget",
            "max_changed_files",
            "max_diff_bytes",
        )
        if len(args) > len(names):
            raise TypeError(
                "TaskAdmissionBudgetsV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TaskAdmissionPolicyV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TaskAdmissionPolicyV1``."""

    legacy_read_policy: Any = None
    oracle_policy: Any = None
    carrier_change_policy: Any = None
    imports_require_packet_reference: Any = None
    exact_write_surface: Any = None
    public_hashes_declared_artifacts_only: Any = None
    model_delegation_allowed: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "legacy_read_policy",
            "oracle_policy",
            "carrier_change_policy",
            "imports_require_packet_reference",
            "exact_write_surface",
            "public_hashes_declared_artifacts_only",
            "model_delegation_allowed",
        )
        if len(args) > len(names):
            raise TypeError(
                "TaskAdmissionPolicyV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TaskSuccessorPolicyV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TaskSuccessorPolicyV1``."""

    host_only: Any = None
    max_successors: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("host_only", "max_successors")
        if len(args) > len(names):
            raise TypeError(
                "TaskSuccessorPolicyV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TaskLeaseRequestV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TaskLeaseRequestV1``."""

    lease_id: Any = None
    owner_id: Any = None
    mode: Any = None
    canonical_paths: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("lease_id", "owner_id", "mode", "canonical_paths")
        if len(args) > len(names):
            raise TypeError("TaskLeaseRequestV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class FrozenTaskObserverV1(_RustSurfaceObject):
    """Structural mirror of Rust ``FrozenTaskObserverV1``."""

    observer_id: Any = None
    observer_domain: Any = None
    state_domain: Any = None
    frozen_base: Any = None
    visible_artifact_hashes: Any = None
    hidden_artifact_classes: Any = None
    tool_permissions: Any = None
    write_surface: Any = None
    evidence_ceiling: Any = None
    model_delegation_allowed: Any = None
    observer_hash: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "observer_id",
            "observer_domain",
            "state_domain",
            "frozen_base",
            "visible_artifact_hashes",
            "hidden_artifact_classes",
            "tool_permissions",
            "write_surface",
            "evidence_ceiling",
            "model_delegation_allowed",
            "observer_hash",
        )
        if len(args) > len(names):
            raise TypeError(
                "FrozenTaskObserverV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class MixedCarrierTaskPacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``MixedCarrierTaskPacketV1``."""

    schema_version: Any = None
    packet_id: Any = None
    goal_id: Any = None
    goal_declaration: Any = None
    freeze_status: Any = None
    frozen_base: Any = None
    artifacts: Any = None
    packet_references: Any = None
    legacy_inputs: Any = None
    allowed_operations: Any = None
    policy: Any = None
    budgets: Any = None
    write_surface: Any = None
    lease_request: Any = None
    successor_policy: Any = None
    nonclaims: Any = None
    evidence_ceiling: Any = None
    admission_host_id: Any = None
    producer_id: Any = None
    evaluator_id: Any = None
    authority_witness_id: Any = None
    observer: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "goal_id",
            "goal_declaration",
            "freeze_status",
            "frozen_base",
            "artifacts",
            "packet_references",
            "legacy_inputs",
            "allowed_operations",
            "policy",
            "budgets",
            "write_surface",
            "lease_request",
            "successor_policy",
            "nonclaims",
            "evidence_ceiling",
            "admission_host_id",
            "producer_id",
            "evaluator_id",
            "authority_witness_id",
            "observer",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "MixedCarrierTaskPacketV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TaskAdmissionEnvelopeV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TaskAdmissionEnvelopeV1``."""

    schema_version: Any = None
    packet: Any = None
    packet_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("schema_version", "packet", "packet_sha256")
        if len(args) > len(names):
            raise TypeError(
                "TaskAdmissionEnvelopeV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class CompiledTaskPacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``CompiledTaskPacketV1``."""

    schema_version: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    bundle_sha256: Any = None
    observer_sha256: Any = None
    frozen_base: Any = None
    admission_host_id: Any = None
    lease_request: Any = None
    write_surface: Any = None
    evidence_ceiling: Any = None
    status: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "packet_sha256",
            "bundle_sha256",
            "observer_sha256",
            "frozen_base",
            "admission_host_id",
            "lease_request",
            "write_surface",
            "evidence_ceiling",
            "status",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "CompiledTaskPacketV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ActiveTaskLeaseV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ActiveTaskLeaseV1``."""

    schema_version: Any = None
    lease_id: Any = None
    owner_id: Any = None
    packet_sha256: Any = None
    mode: Any = None
    canonical_paths: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "lease_id",
            "owner_id",
            "packet_sha256",
            "mode",
            "canonical_paths",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError("ActiveTaskLeaseV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class TaskAdmissionReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``TaskAdmissionReceiptV1``."""

    schema_version: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    bundle_sha256: Any = None
    observer_sha256: Any = None
    frozen_base: Any = None
    lease: Any = None
    schema_checked: Any = None
    canonical_bytes_checked: Any = None
    bundle_checked: Any = None
    paths_checked: Any = None
    budgets_checked: Any = None
    policy_checked: Any = None
    lease_checked: Any = None
    status: Any = None
    terminal: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "packet_sha256",
            "bundle_sha256",
            "observer_sha256",
            "frozen_base",
            "lease",
            "schema_checked",
            "canonical_bytes_checked",
            "bundle_checked",
            "paths_checked",
            "budgets_checked",
            "policy_checked",
            "lease_checked",
            "status",
            "terminal",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "TaskAdmissionReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class HostLeaseRegistryV1(_RustSurfaceObject):
    """Structural mirror of Rust ``HostLeaseRegistryV1``."""

    active: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("active",)
        if len(args) > len(names):
            raise TypeError(
                "HostLeaseRegistryV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def expected_source_manifest_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``expected_source_manifest_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::expected_source_manifest_v1"
    )


def resolve_task_artifact_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``resolve_task_artifact_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::resolve_task_artifact_v1"
    )


def artifact_id(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``artifact_id``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::artifact_id"
    )


def path(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``path``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::path"
    )


def sha256(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``sha256``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::sha256"
    )


fn: Any = None


def validate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::validate"
    )


def task_observer_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``task_observer_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::task_observer_sha256_v1"
    )


def task_packet_canonical_bytes_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``task_packet_canonical_bytes_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::task_packet_canonical_bytes_v1"
    )


def task_packet_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``task_packet_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::task_packet_sha256_v1"
    )


def task_bundle_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``task_bundle_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::task_bundle_sha256_v1"
    )


def compile_task_packet_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``compile_task_packet_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::compile_task_packet_v1"
    )


def from_active(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``from_active``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::from_active"
    )


def active_leases(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``active_leases``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::active_leases"
    )


def issue(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``issue``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::issue"
    )


def replay_task_admission_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``replay_task_admission_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/task_admission.rs::replay_task_admission_v1"
    )


TaskAdmissionError = Enum(
    "TaskAdmissionError",
    {
        "SchemaMismatch": "SchemaMismatch",
        "EmptyField": "EmptyField",
        "InvalidSha256": "InvalidSha256",
        "InvalidGitCommit": "InvalidGitCommit",
        "NonCanonicalPath": "NonCanonicalPath",
        "NonCanonicalList": "NonCanonicalList",
        "EmptyArtifact": "EmptyArtifact",
        "ArtifactKindMismatch": "ArtifactKindMismatch",
        "UnfrozenPacket": "UnfrozenPacket",
        "FrozenBaseMismatch": "FrozenBaseMismatch",
        "StaleBase": "StaleBase",
        "ScopeExpansion": "ScopeExpansion",
        "SourceManifestMismatch": "SourceManifestMismatch",
        "ImplicitLegacyRead": "ImplicitLegacyRead",
        "PacketReferenceSetChanged": "PacketReferenceSetChanged",
        "OperationSetChanged": "OperationSetChanged",
        "PolicyExpansion": "PolicyExpansion",
        "CarrierChangeUnlicensed": "CarrierChangeUnlicensed",
        "BudgetOutsideAdmission": "BudgetOutsideAdmission",
        "WriteSurfaceChanged": "WriteSurfaceChanged",
        "LeaseRequestMismatch": "LeaseRequestMismatch",
        "SuccessorPolicyChanged": "SuccessorPolicyChanged",
        "NonclaimSetChanged": "NonclaimSetChanged",
        "EvidenceCeilingChanged": "EvidenceCeilingChanged",
        "IdentityCollision": "IdentityCollision",
        "IdentitySetChanged": "IdentitySetChanged",
        "AuthorityExpansion": "AuthorityExpansion",
        "ObserverContextMismatch": "ObserverContextMismatch",
        "ObserverHashMismatch": "ObserverHashMismatch",
        "PacketHashMismatch": "PacketHashMismatch",
        "MissingArtifact": "MissingArtifact",
        "BundleMemberMismatch": "BundleMemberMismatch",
        "ArtifactHashMismatch": "ArtifactHashMismatch",
        "CompilationInvariant": "CompilationInvariant",
        "HostIssuerMismatch": "HostIssuerMismatch",
        "LeaseIdCollision": "LeaseIdCollision",
        "LeaseConflict": "LeaseConflict",
        "ReceiptInvariant": "ReceiptInvariant",
        "ReplayMismatch": "ReplayMismatch",
        "Json": "Json",
    },
    type=str,
)
TaskAdmissionError.__doc__ = (
    "Structural mirror of Rust ``TaskAdmissionError`` variants."
)




