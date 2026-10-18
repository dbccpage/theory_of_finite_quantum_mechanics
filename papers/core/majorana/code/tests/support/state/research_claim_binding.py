from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/research_claim_binding.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


# BEGIN GENERATED RUST SURFACE
# Rust source: omega_engine/crates/omega_state/src/research_claim_binding.rs
# Rust sha256: 7ba6d5df75858dccb508cbe8620960c603b8e1b59ce93ef059519f2f2a191f60
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
CLAIM_BINDING_PACKET_SCHEMA_V1: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
CLAIM_BINDING_VERIFICATION_SCHEMA_V1: Any = None


ClaimSourceKindV1 = Enum(
    "ClaimSourceKindV1",
    {
        "PaperSection": "PaperSection",
        "ClaimLedger": "ClaimLedger",
        "ProofLedger": "ProofLedger",
        "BasementTheoremLedger": "BasementTheoremLedger",
    },
    type=str,
)
ClaimSourceKindV1.__doc__ = "Structural mirror of Rust ``ClaimSourceKindV1`` variants."


# The Rust value is intentionally not guessed by the structural mirror.
ALL: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ClaimSourceBindingV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ClaimSourceBindingV1``."""

    kind: Any = None
    path: Any = None
    anchor: Any = None
    sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("kind", "path", "anchor", "sha256")
        if len(args) > len(names):
            raise TypeError(
                "ClaimSourceBindingV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class RustClaimWitnessV1(_RustSurfaceObject):
    """Structural mirror of Rust ``RustClaimWitnessV1``."""

    crate_name: Any = None
    symbol: Any = None
    test_target: Any = None
    test_name: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("crate_name", "symbol", "test_target", "test_name")
        if len(args) > len(names):
            raise TypeError("RustClaimWitnessV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class LeanClaimWitnessV1(_RustSurfaceObject):
    """Structural mirror of Rust ``LeanClaimWitnessV1``."""

    source_path: Any = None
    module: Any = None
    theorem: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("source_path", "module", "theorem")
        if len(args) > len(names):
            raise TypeError("LeanClaimWitnessV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ClaimWitnessPlanV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ClaimWitnessPlanV1``."""

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
            raise TypeError("ClaimWitnessPlanV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ResearchClaimBindingPacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ResearchClaimBindingPacketV1``."""

    schema_version: Any = None
    packet_id: Any = None
    frozen_base: Any = None
    claim_id: Any = None
    obligation_id: Any = None
    claim_sources: Any = None
    rust_witness: Any = None
    lean_witness: Any = None
    exact_write_surfaces: Any = None
    witnesses: Any = None
    evidence_ceiling: Any = None
    publication_permission: Any = None
    promotion_permission: Any = None
    gate_activated: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "frozen_base",
            "claim_id",
            "obligation_id",
            "claim_sources",
            "rust_witness",
            "lean_witness",
            "exact_write_surfaces",
            "witnesses",
            "evidence_ceiling",
            "publication_permission",
            "promotion_permission",
            "gate_activated",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "ResearchClaimBindingPacketV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ClaimBindingObservationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ClaimBindingObservationV1``."""

    observed_source_hashes: Any = None
    rust_symbol_resolved: Any = None
    rust_test_passed: Any = None
    lean_target_built: Any = None
    lean_theorem_axiom_free: Any = None
    citations_resolved: Any = None
    independent_review_accepted: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "observed_source_hashes",
            "rust_symbol_resolved",
            "rust_test_passed",
            "lean_target_built",
            "lean_theorem_axiom_free",
            "citations_resolved",
            "independent_review_accepted",
        )
        if len(args) > len(names):
            raise TypeError(
                "ClaimBindingObservationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class ClaimBindingVerificationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``ClaimBindingVerificationV1``."""

    schema_version: Any = None
    packet_sha256: Any = None
    claim_id: Any = None
    obligation_id: Any = None
    source_count: Any = None
    all_sources_frozen: Any = None
    rust_witness_resolved: Any = None
    lean_witness_resolved: Any = None
    citations_resolved: Any = None
    independent_review_accepted: Any = None
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
            "claim_id",
            "obligation_id",
            "source_count",
            "all_sources_frozen",
            "rust_witness_resolved",
            "lean_witness_resolved",
            "citations_resolved",
            "independent_review_accepted",
            "human_decision_recorded",
            "publication_performed",
            "promotion_constructor_called",
            "gate_activated",
            "terminal",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "ClaimBindingVerificationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


ResearchClaimBindingError = Enum(
    "ResearchClaimBindingError",
    {
        "InvalidText": "InvalidText",
        "InvalidHash": "InvalidHash",
        "SourceSetChanged": "SourceSetChanged",
        "WriteSurfaceChanged": "WriteSurfaceChanged",
        "WitnessIdentityCollision": "WitnessIdentityCollision",
        "AuthorityExpansion": "AuthorityExpansion",
        "SourceHashMismatch": "SourceHashMismatch",
        "RustWitnessFailed": "RustWitnessFailed",
        "LeanWitnessFailed": "LeanWitnessFailed",
        "CitationWitnessFailed": "CitationWitnessFailed",
        "IndependentReviewMissing": "IndependentReviewMissing",
        "Json": "Json",
    },
    type=str,
)
ResearchClaimBindingError.__doc__ = (
    "Structural mirror of Rust ``ResearchClaimBindingError`` variants."
)


def validate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/research_claim_binding.rs::validate"
    )


def claim_binding_packet_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``claim_binding_packet_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/research_claim_binding.rs::claim_binding_packet_sha256_v1"
    )


def verify_research_claim_binding_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``verify_research_claim_binding_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/research_claim_binding.rs::verify_research_claim_binding_v1"
    )


# END GENERATED RUST SURFACE


