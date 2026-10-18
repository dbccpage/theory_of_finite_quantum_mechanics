from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/software_change_profile.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


# BEGIN GENERATED RUST SURFACE
# Rust source: omega_engine/crates/omega_state/src/software_change_profile.rs
# Rust sha256: edbd32a5ee993290f042f2cc5f703bb5db17478334e206cd9890d9b8851a45f5
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
SOFTWARE_PROFILE_SCHEMA_V1: Any = None


SoftwareProfileKindV1 = Enum(
    "SoftwareProfileKindV1",
    {
        "Rust": "Rust",
        "Python": "Python",
        "GeneratedArtifact": "GeneratedArtifact",
        "ManualEdit": "ManualEdit",
    },
    type=str,
)
SoftwareProfileKindV1.__doc__ = (
    "Structural mirror of Rust ``SoftwareProfileKindV1`` variants."
)


# The Rust value is intentionally not guessed by the structural mirror.
ALL: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SoftwareCommandV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SoftwareCommandV1``."""

    program: Any = None
    arguments: Any = None
    affected_paths: Any = None
    timeout_seconds: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("program", "arguments", "affected_paths", "timeout_seconds")
        if len(args) > len(names):
            raise TypeError("SoftwareCommandV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SoftwareProfileV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SoftwareProfileV1``."""

    schema_version: Any = None
    kind: Any = None
    stages: Any = None
    commands: Any = None
    witness_fields: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "kind",
            "stages",
            "commands",
            "witness_fields",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError("SoftwareProfileV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def validate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/software_change_profile.rs::validate"
    )


def compile_software_profile_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``compile_software_profile_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/software_change_profile.rs::compile_software_profile_v1"
    )


ChangeActorV1 = Enum("ChangeActorV1", {"Agent": "Agent", "Manual": "Manual"}, type=str)
ChangeActorV1.__doc__ = "Structural mirror of Rust ``ChangeActorV1`` variants."


ChangeDiagnosticLevelV1 = Enum(
    "ChangeDiagnosticLevelV1", {"Warning": "Warning", "Error": "Error"}, type=str
)
ChangeDiagnosticLevelV1.__doc__ = (
    "Structural mirror of Rust ``ChangeDiagnosticLevelV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ChangeDiagnosticV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ChangeDiagnosticV1``."""

    level: Any = None
    message: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("level", "message")
        if len(args) > len(names):
            raise TypeError("ChangeDiagnosticV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ChangeWitnessV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ChangeWitnessV1``."""

    producer_id: Any = None
    independent_evaluator_id: Any = None
    authority_witness_id: Any = None
    packet_sha256: Any = None
    diff_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "producer_id",
            "independent_evaluator_id",
            "authority_witness_id",
            "packet_sha256",
            "diff_sha256",
        )
        if len(args) > len(names):
            raise TypeError("ChangeWitnessV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SoftwareChangeAttemptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SoftwareChangeAttemptV1``."""

    profile: Any = None
    actor: Any = None
    admitted: Any = None
    direct_unpacketized_write: Any = None
    declared_write_surface: Any = None
    changed_paths: Any = None
    expected_diff_sha256: Any = None
    observed_diff_sha256: Any = None
    tests_configured: Any = None
    required_tool_available: Any = None
    diagnostics: Any = None
    witness: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "profile",
            "actor",
            "admitted",
            "direct_unpacketized_write",
            "declared_write_surface",
            "changed_paths",
            "expected_diff_sha256",
            "observed_diff_sha256",
            "tests_configured",
            "required_tool_available",
            "diagnostics",
            "witness",
        )
        if len(args) > len(names):
            raise TypeError(
                "SoftwareChangeAttemptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SoftwareChangeReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SoftwareChangeReceiptV1``."""

    profile: Any = None
    actor: Any = None
    affected_paths: Any = None
    witness: Any = None
    terminal: Any = None
    authority_effect: Any = None
    approved: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "profile",
            "actor",
            "affected_paths",
            "witness",
            "terminal",
            "authority_effect",
            "approved",
        )
        if len(args) > len(names):
            raise TypeError(
                "SoftwareChangeReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def evaluate_software_change_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``evaluate_software_change_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/software_change_profile.rs::evaluate_software_change_v1"
    )


SoftwareChangeError = Enum(
    "SoftwareChangeError",
    {
        "SchemaVersion": "SchemaVersion",
        "ProfileDrift": "ProfileDrift",
        "WitnessShapeChanged": "WitnessShapeChanged",
        "AuthorityExpansion": "AuthorityExpansion",
        "UnboundedCommand": "UnboundedCommand",
        "DirectWrite": "DirectWrite",
        "MissingTool": "MissingTool",
        "MissingTestConfiguration": "MissingTestConfiguration",
        "WriteSurfaceViolation": "WriteSurfaceViolation",
        "DiffTampered": "DiffTampered",
        "WitnessConflict": "WitnessConflict",
        "InvalidDiagnostic": "InvalidDiagnostic",
        "GateDiagnostic": "GateDiagnostic",
    },
    type=str,
)
SoftwareChangeError.__doc__ = (
    "Structural mirror of Rust ``SoftwareChangeError`` variants."
)


# The Rust value is intentionally not guessed by the structural mirror.
fn: Any = None


# END GENERATED RUST SURFACE


