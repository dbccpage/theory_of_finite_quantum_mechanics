from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/gtoc_corpus_migration.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


# BEGIN GENERATED RUST SURFACE
# Rust source: omega_engine/crates/omega_state/src/gtoc_corpus_migration.rs
# Rust sha256: a720cf8874d2bfc890c67b9c565f1662af556ce06657c2e102b55d475e89d839
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
GTOC_CORPUS_MIGRATION_PACKET_SCHEMA_V1: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
GTOC_CORPUS_MIGRATION_VERIFICATION_SCHEMA_V1: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
GTOC_CORPUS_SOURCE_ROOT_V1: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
GTOC_CORPUS_DESTINATION_ROOT_V1: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
GTOC_CORPUS_SOURCE_FILE_COUNT_V1: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
GTOC_CORPUS_REFERENCE_FILE_COUNT_V1: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class GtocCorpusMigrationPacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``GtocCorpusMigrationPacketV1``."""

    schema_version: Any = None
    packet_id: Any = None
    frozen_base: Any = None
    manifest_path: Any = None
    manifest_sha256: Any = None
    source_root: Any = None
    destination_root: Any = None
    source_file_count: Any = None
    reference_file_count: Any = None
    collision_count: Any = None
    destination_absent: Any = None
    move_executed: Any = None
    exact_write_surfaces: Any = None
    boundary: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "frozen_base",
            "manifest_path",
            "manifest_sha256",
            "source_root",
            "destination_root",
            "source_file_count",
            "reference_file_count",
            "collision_count",
            "destination_absent",
            "move_executed",
            "exact_write_surfaces",
            "boundary",
        )
        if len(args) > len(names):
            raise TypeError(
                "GtocCorpusMigrationPacketV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class GtocCorpusMigrationObservationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``GtocCorpusMigrationObservationV1``."""

    manifest_sha256: Any = None
    source_hashes_replayed: Any = None
    source_tree_present: Any = None
    destination_absent: Any = None
    collision_count: Any = None
    reference_census_replayed: Any = None
    move_executed: Any = None
    independent_review_accepted: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "manifest_sha256",
            "source_hashes_replayed",
            "source_tree_present",
            "destination_absent",
            "collision_count",
            "reference_census_replayed",
            "move_executed",
            "independent_review_accepted",
        )
        if len(args) > len(names):
            raise TypeError(
                "GtocCorpusMigrationObservationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class GtocCorpusMigrationVerificationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``GtocCorpusMigrationVerificationV1``."""

    schema_version: Any = None
    packet_sha256: Any = None
    manifest_sha256: Any = None
    source_file_count: Any = None
    reference_file_count: Any = None
    collision_count: Any = None
    destination_absent: Any = None
    move_executed: Any = None
    residual_obligations: Any = None
    human_decision_recorded: Any = None
    publication_performed: Any = None
    promotion_constructor_called: Any = None
    gate_activated: Any = None
    terminal: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_sha256",
            "manifest_sha256",
            "source_file_count",
            "reference_file_count",
            "collision_count",
            "destination_absent",
            "move_executed",
            "residual_obligations",
            "human_decision_recorded",
            "publication_performed",
            "promotion_constructor_called",
            "gate_activated",
            "terminal",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "GtocCorpusMigrationVerificationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


GtocCorpusMigrationError = Enum(
    "GtocCorpusMigrationError",
    {
        "Common": "Common",
        "PacketChanged": "PacketChanged",
        "InvalidManifestHash": "InvalidManifestHash",
        "ManifestHashMismatch": "ManifestHashMismatch",
        "InventoryReplayFailed": "InventoryReplayFailed",
        "UnexpectedMove": "UnexpectedMove",
        "IndependentReviewMissing": "IndependentReviewMissing",
    },
    type=str,
)
GtocCorpusMigrationError.__doc__ = (
    "Structural mirror of Rust ``GtocCorpusMigrationError`` variants."
)


def validate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_corpus_migration.rs::validate"
    )


def gtoc_corpus_migration_packet_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``gtoc_corpus_migration_packet_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_corpus_migration.rs::gtoc_corpus_migration_packet_sha256_v1"
    )


def verify_gtoc_corpus_migration_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``verify_gtoc_corpus_migration_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc_corpus_migration.rs::verify_gtoc_corpus_migration_v1"
    )


# END GENERATED RUST SURFACE


