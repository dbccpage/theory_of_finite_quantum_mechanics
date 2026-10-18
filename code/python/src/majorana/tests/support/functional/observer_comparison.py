"""Structural Python mirror for ``omega_engine/crates/omega_functional/src/observer_comparison.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""

from __future__ import annotations
from dataclasses import dataclass
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


OBSERVER_COMPARISON_AUTHORITY_EFFECT: Any = None


OBSERVER_COMPARISON_EVIDENCE_CEILING: Any = None


OBSERVER_COMPARISON_CUSTOMER_CLAIM_ALLOWED: Any = None


ObserverComparisonStatus = Enum(
    "ObserverComparisonStatus",
    {
        "Agreement": "Agreement",
        "Disagreement": "Disagreement",
        "Incomparable": "Incomparable",
    },
    type=str,
)
ObserverComparisonStatus.__doc__ = (
    "Structural mirror of Rust ``ObserverComparisonStatus`` variants."
)


ObserverComparisonAuthorityRequest = Enum(
    "ObserverComparisonAuthorityRequest",
    {
        "PromoteAgreementToAuthority": "PromoteAgreementToAuthority",
        "PromoteDisagreementToGlobalObstruction": "PromoteDisagreementToGlobalObstruction",
        "RecoverHiddenDistinctions": "RecoverHiddenDistinctions",
        "EmitCustomerClaim": "EmitCustomerClaim",
    },
    type=str,
)
ObserverComparisonAuthorityRequest.__doc__ = (
    "Structural mirror of Rust ``ObserverComparisonAuthorityRequest`` variants."
)


@dataclass(init=False)
class ComparisonLaunderingRefused(_RustSurfaceObject):
    """Structural mirror of Rust ``ComparisonLaunderingRefused``."""

    packet_id: Any = None
    status: Any = None
    requested_promotion: Any = None
    authority_effect: Any = None
    evidence_ceiling: Any = None
    customer_claim_allowed: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "packet_id",
            "status",
            "requested_promotion",
            "authority_effect",
            "evidence_ceiling",
            "customer_claim_allowed",
        )
        if len(args) > len(names):
            raise TypeError(
                "ComparisonLaunderingRefused received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


fn: Any = None


ObserverComparisonResidualKind = Enum(
    "ObserverComparisonResidualKind",
    {
        "NoVisibleDifference": "NoVisibleDifference",
        "ObserverDisagreement": "ObserverDisagreement",
        "IncomparableWithoutTransport": "IncomparableWithoutTransport",
    },
    type=str,
)
ObserverComparisonResidualKind.__doc__ = (
    "Structural mirror of Rust ``ObserverComparisonResidualKind`` variants."
)


@dataclass(init=False)
class ObserverComparisonResidual(_RustSurfaceObject):
    """Structural mirror of Rust ``ObserverComparisonResidual``."""

    packet_id: Any = None
    kind: Any = None
    source_quotient_hash: Any = None
    carrier_hash: Any = None
    comparison_replay_hash: Any = None
    authority_effect: Any = None
    evidence_ceiling: Any = None
    customer_claim_allowed: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "packet_id",
            "kind",
            "source_quotient_hash",
            "carrier_hash",
            "comparison_replay_hash",
            "authority_effect",
            "evidence_ceiling",
            "customer_claim_allowed",
        )
        if len(args) > len(names):
            raise TypeError(
                "ObserverComparisonResidual received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


ObserverComparisonError = Enum(
    "ObserverComparisonError",
    {
        "EmptyPacketId": "EmptyPacketId",
        "EmptyObserverRef": "EmptyObserverRef",
        "ZeroSourceQuotientHash": "ZeroSourceQuotientHash",
        "ZeroEquivalenceRelationHash": "ZeroEquivalenceRelationHash",
        "ZeroReplayHash": "ZeroReplayHash",
        "ZeroCarrierHash": "ZeroCarrierHash",
        "SourceQuotientMismatch": "SourceQuotientMismatch",
        "CarrierMismatch": "CarrierMismatch",
        "IdenticalObserverComparison": "IdenticalObserverComparison",
    },
    type=str,
)
ObserverComparisonError.__doc__ = (
    "Structural mirror of Rust ``ObserverComparisonError`` variants."
)


@dataclass(init=False)
class ObserverComparisonPacket(_RustSurfaceObject):
    """Structural mirror of Rust ``ObserverComparisonPacket``."""

    id: Any = None
    left_observer_ref: Any = None
    right_observer_ref: Any = None
    source_quotient_hash: Any = None
    carrier_hash: Any = None
    left_equivalence_relation_hash: Any = None
    right_equivalence_relation_hash: Any = None
    left_quotient_replay_hash: Any = None
    right_quotient_replay_hash: Any = None
    comparison_replay_hash: Any = None
    status: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "id",
            "left_observer_ref",
            "right_observer_ref",
            "source_quotient_hash",
            "carrier_hash",
            "left_equivalence_relation_hash",
            "right_equivalence_relation_hash",
            "left_quotient_replay_hash",
            "right_quotient_replay_hash",
            "comparison_replay_hash",
            "status",
        )
        if len(args) > len(names):
            raise TypeError(
                "ObserverComparisonPacket received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def new(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``new``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/observer_comparison.rs::new"
    )


def try_from_observer_quotients(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``try_from_observer_quotients``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/observer_comparison.rs::try_from_observer_quotients"
    )


def try_derive_from_equivalence_hashes(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``try_derive_from_equivalence_hashes``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/observer_comparison.rs::try_derive_from_equivalence_hashes"
    )


def residual(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``residual``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/observer_comparison.rs::residual"
    )


def refuse_authority_request(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``refuse_authority_request``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/observer_comparison.rs::refuse_authority_request"
    )




