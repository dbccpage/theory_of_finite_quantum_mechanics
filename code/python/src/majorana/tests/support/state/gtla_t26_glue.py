from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/gtla_t26_glue.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


# BEGIN GENERATED RUST SURFACE
# Rust source: omega_engine/crates/omega_state/src/gtla_t26_glue.rs
# Rust sha256: 7c73aefdce5f12e35d78e895fa8f68e3e5eef0c8f26910bef0e76d82bf9eca4c
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
T26_GLUE_PACKET_SCHEMA_V1: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
T26_GLUE_VERIFICATION_SCHEMA_V1: Any = None


T26HypothesisIdV1 = Enum(
    "T26HypothesisIdV1",
    {
        "H1": "H1",
        "H2": "H2",
        "H3Prime": "H3Prime",
        "H3DoublePrime": "H3DoublePrime",
        "H4": "H4",
        "H5C4": "H5C4",
    },
    type=str,
)
T26HypothesisIdV1.__doc__ = "Structural mirror of Rust ``T26HypothesisIdV1`` variants."


# The Rust value is intentionally not guessed by the structural mirror.
ALL: Any = None


T26HypothesisDispositionV1 = Enum(
    "T26HypothesisDispositionV1",
    {"DeclaredInput": "DeclaredInput", "OpenProofObligation": "OpenProofObligation"},
    type=str,
)
T26HypothesisDispositionV1.__doc__ = (
    "Structural mirror of Rust ``T26HypothesisDispositionV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class T26HypothesisRowV1(_RustSurfaceObject):
    """Structural mirror of Rust ``T26HypothesisRowV1``."""

    hypothesis_id: Any = None
    summary: Any = None
    disposition: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("hypothesis_id", "summary", "disposition", "authority_effect")
        if len(args) > len(names):
            raise TypeError("T26HypothesisRowV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


T26DependentIdV1 = Enum(
    "T26DependentIdV1",
    {"Gtor21": "Gtor21", "Gttc7": "Gttc7", "GtlaT28": "GtlaT28"},
    type=str,
)
T26DependentIdV1.__doc__ = "Structural mirror of Rust ``T26DependentIdV1`` variants."


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class T26DependentRowV1(_RustSurfaceObject):
    """Structural mirror of Rust ``T26DependentRowV1``."""

    dependent_id: Any = None
    required_status: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("dependent_id", "required_status")
        if len(args) > len(names):
            raise TypeError("T26DependentRowV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class T26GluePacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``T26GluePacketV1``."""

    schema_version: Any = None
    packet_id: Any = None
    frozen_base: Any = None
    enc_id: Any = None
    theorem_id: Any = None
    hypotheses: Any = None
    downstream: Any = None
    exact_write_surfaces: Any = None
    boundary: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "frozen_base",
            "enc_id",
            "theorem_id",
            "hypotheses",
            "downstream",
            "exact_write_surfaces",
            "boundary",
        )
        if len(args) > len(names):
            raise TypeError("T26GluePacketV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class T26GlueObservationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``T26GlueObservationV1``."""

    hypothesis_registry_sha256: Any = None
    h3_double_prime_construction_supplied: Any = None
    enc_status: Any = None
    lean_status: Any = None
    downstream_statuses_preserved: Any = None
    independent_review_accepted: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "hypothesis_registry_sha256",
            "h3_double_prime_construction_supplied",
            "enc_status",
            "lean_status",
            "downstream_statuses_preserved",
            "independent_review_accepted",
        )
        if len(args) > len(names):
            raise TypeError(
                "T26GlueObservationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class T26GlueVerificationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``T26GlueVerificationV1``."""

    schema_version: Any = None
    packet_sha256: Any = None
    hypothesis_registry_sha256: Any = None
    hypothesis_count: Any = None
    open_hypotheses: Any = None
    enc_status: Any = None
    lean_status: Any = None
    downstream_statuses_preserved: Any = None
    human_decision_recorded: Any = None
    promotion_constructor_called: Any = None
    gate_activated: Any = None
    terminal: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_sha256",
            "hypothesis_registry_sha256",
            "hypothesis_count",
            "open_hypotheses",
            "enc_status",
            "lean_status",
            "downstream_statuses_preserved",
            "human_decision_recorded",
            "promotion_constructor_called",
            "gate_activated",
            "terminal",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "T26GlueVerificationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


T26GlueError = Enum(
    "T26GlueError",
    {
        "Common": "Common",
        "HypothesisRegistryChanged": "HypothesisRegistryChanged",
        "DownstreamRegistryChanged": "DownstreamRegistryChanged",
        "ObservationHashMismatch": "ObservationHashMismatch",
        "UnsupportedGlueConstruction": "UnsupportedGlueConstruction",
        "StatusInflation": "StatusInflation",
        "DownstreamStatusDrift": "DownstreamStatusDrift",
        "IndependentReviewMissing": "IndependentReviewMissing",
    },
    type=str,
)
T26GlueError.__doc__ = "Structural mirror of Rust ``T26GlueError`` variants."


def canonical_t26_hypotheses_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``canonical_t26_hypotheses_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtla_t26_glue.rs::canonical_t26_hypotheses_v1"
    )


def canonical_t26_dependents_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``canonical_t26_dependents_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtla_t26_glue.rs::canonical_t26_dependents_v1"
    )


def validate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtla_t26_glue.rs::validate"
    )


def t26_hypothesis_registry_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``t26_hypothesis_registry_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtla_t26_glue.rs::t26_hypothesis_registry_sha256_v1"
    )


def t26_glue_packet_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``t26_glue_packet_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtla_t26_glue.rs::t26_glue_packet_sha256_v1"
    )


def verify_t26_glue_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``verify_t26_glue_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtla_t26_glue.rs::verify_t26_glue_v1"
    )


# END GENERATED RUST SURFACE


