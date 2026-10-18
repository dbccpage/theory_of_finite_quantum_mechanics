from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/gtoc3_lift_license.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


# BEGIN GENERATED RUST SURFACE
# Rust source: omega_engine/crates/omega_state/src/gtoc3_lift_license.rs
# Rust sha256: 11cbcd541f8ef89796d02cfdf4382de8a7a4c3a688569ebff5dd1103e2a3ec79
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
GTOC3_PACKET_SCHEMA_VERSION: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
GTOC3_ADMISSION_SCHEMA_VERSION: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
GTOC3_CLASSIFICATION_SCHEMA_VERSION: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
GTOC3_RECEIPT_SCHEMA_VERSION: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_FROZEN_BASE: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_TARGET: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_OPERATOR_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_SEMANTIC_CONTRACT_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_license_ID: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_OBSERVER_DOMAIN: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_STATE_DOMAIN: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_EVIDENCE_CEILING: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_SOURCE_CARRIER_SHA256: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_TARGET_CARRIER_SHA256: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_OBSTRUCTION_SUMMARY: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_OBSTRUCTION_SHA256: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_MAX_COST_UNITS: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_MAX_NEW_DIMENSIONS: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_SOURCE_MANIFEST: Any = None


# The Rust value is intentionally not guessed by the structural mirror.
S02_002_WRITE_SURFACE: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc3PacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc3PacketV1``."""

    schema_version: Any = None
    packet_id: Any = None
    frozen_base: Any = None
    target_sprint: Any = None
    source_manifest: Any = None
    budgets: Any = None
    evidence_ceiling: Any = None
    observer: Any = None
    producer_id: Any = None
    evaluator_id: Any = None
    authority_witness_id: Any = None
    prior_work_ledger: Any = None
    operator_manifest: Any = None
    trigger: Any = None
    candidate: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "frozen_base",
            "target_sprint",
            "source_manifest",
            "budgets",
            "evidence_ceiling",
            "observer",
            "producer_id",
            "evaluator_id",
            "authority_witness_id",
            "prior_work_ledger",
            "operator_manifest",
            "trigger",
            "candidate",
        )
        if len(args) > len(names):
            raise TypeError("Gtoc3PacketV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def validate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc3_lift_license.rs::validate"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc3AdmissionV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc3AdmissionV1``."""

    schema_version: Any = None
    packet: Any = None
    packet_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("schema_version", "packet", "packet_sha256")
        if len(args) > len(names):
            raise TypeError("Gtoc3AdmissionV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


Gtoc3SurvivorRouteV1 = Enum(
    "Gtoc3SurvivorRouteV1",
    {
        "ProofObligation": "ProofObligation",
        "OracleNeeded": "OracleNeeded",
        "LiftLicenseNeeded": "LiftLicenseNeeded",
        "Refused": "Refused",
        "InvalidEvidence": "InvalidEvidence",
        "InfrastructureFailure": "InfrastructureFailure",
    },
    type=str,
)
Gtoc3SurvivorRouteV1.__doc__ = (
    "Structural mirror of Rust ``Gtoc3SurvivorRouteV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc3ClassificationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc3ClassificationV1``."""

    schema_version: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    observer_sha256: Any = None
    operator_manifest_sha256: Any = None
    trigger_sha256: Any = None
    candidate_sha256: Any = None
    evaluation_sha256: Any = None
    structural_trigger_not_license: Any = None
    complete_for_licensing: Any = None
    license_issued: Any = None
    lift_executed: Any = None
    terminal_proposal: Any = None
    survivor_routes: Any = None
    residual_ids: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "packet_sha256",
            "observer_sha256",
            "operator_manifest_sha256",
            "trigger_sha256",
            "candidate_sha256",
            "evaluation_sha256",
            "structural_trigger_not_license",
            "complete_for_licensing",
            "license_issued",
            "lift_executed",
            "terminal_proposal",
            "survivor_routes",
            "residual_ids",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc3ClassificationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc3ProducerReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc3ProducerReceiptV1``."""

    schema_version: Any = None
    producer_id: Any = None
    packet_sha256: Any = None
    operator_manifest_sha256: Any = None
    trigger_sha256: Any = None
    candidate_sha256: Any = None
    evaluation: Any = None
    evaluation_sha256: Any = None
    license_issued: Any = None
    lift_executed: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "producer_id",
            "packet_sha256",
            "operator_manifest_sha256",
            "trigger_sha256",
            "candidate_sha256",
            "evaluation",
            "evaluation_sha256",
            "license_issued",
            "lift_executed",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc3ProducerReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc3EvaluationReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc3EvaluationReceiptV1``."""

    schema_version: Any = None
    evaluator_id: Any = None
    producer_id: Any = None
    algorithm: Any = None
    independently_recomputed_sha256: Any = None
    exact_match: Any = None
    trigger_not_treated_as_license: Any = None
    operator_license_binding_checked: Any = None
    policy_budget_checked: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "evaluator_id",
            "producer_id",
            "algorithm",
            "independently_recomputed_sha256",
            "exact_match",
            "trigger_not_treated_as_license",
            "operator_license_binding_checked",
            "policy_budget_checked",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc3EvaluationReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc3AuthorityWitnessV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc3AuthorityWitnessV1``."""

    schema_version: Any = None
    authority_witness_id: Any = None
    identities_distinct: Any = None
    human_promotion_performed: Any = None
    license_issued: Any = None
    lift_executed: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "authority_witness_id",
            "identities_distinct",
            "human_promotion_performed",
            "license_issued",
            "lift_executed",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc3AuthorityWitnessV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc3ReplayReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc3ReplayReceiptV1``."""

    schema_version: Any = None
    packet_sha256: Any = None
    first_producer_sha256: Any = None
    replay_producer_sha256: Any = None
    deterministic: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_sha256",
            "first_producer_sha256",
            "replay_producer_sha256",
            "deterministic",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc3ReplayReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc3TerminalReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc3TerminalReceiptV1``."""

    schema_version: Any = None
    packet_id: Any = None
    terminal_proposal: Any = None
    survivor_routes: Any = None
    residual_ids: Any = None
    human_promotion_performed: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "terminal_proposal",
            "survivor_routes",
            "residual_ids",
            "human_promotion_performed",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc3TerminalReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc3ReceiptBundleV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc3ReceiptBundleV1``."""

    schema_version: Any = None
    producer: Any = None
    evaluation: Any = None
    authority_witness: Any = None
    replay: Any = None
    terminal: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "producer",
            "evaluation",
            "authority_witness",
            "replay",
            "terminal",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc3ReceiptBundleV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc3ExecutionV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc3ExecutionV1``."""

    classification: Any = None
    receipts: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("classification", "receipts")
        if len(args) > len(names):
            raise TypeError("Gtoc3ExecutionV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def evaluate_gtoc3_lift_candidate_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``evaluate_gtoc3_lift_candidate_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc3_lift_license.rs::evaluate_gtoc3_lift_candidate_v1"
    )


def independently_evaluate_claimed_gtoc3_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``independently_evaluate_claimed_gtoc3_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc3_lift_license.rs::independently_evaluate_claimed_gtoc3_v1"
    )


def gtoc3_observer_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``gtoc3_observer_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc3_lift_license.rs::gtoc3_observer_sha256_v1"
    )


def gtoc3_packet_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``gtoc3_packet_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc3_lift_license.rs::gtoc3_packet_sha256_v1"
    )


def gtoc3_sha256_json_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``gtoc3_sha256_json_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc3_lift_license.rs::gtoc3_sha256_json_v1"
    )


Gtoc3Error = Enum(
    "Gtoc3Error",
    {
        "Contract": "Contract",
        "Lift": "Lift",
        "SchemaMismatch": "SchemaMismatch",
        "EmptyField": "EmptyField",
        "InvalidSha256": "InvalidSha256",
        "NonCanonicalList": "NonCanonicalList",
        "FrozenBaseMismatch": "FrozenBaseMismatch",
        "ScopeExpansion": "ScopeExpansion",
        "SourceManifestMismatch": "SourceManifestMismatch",
        "BudgetOutsideAdmission": "BudgetOutsideAdmission",
        "EvidenceCeilingChanged": "EvidenceCeilingChanged",
        "IdentityCollision": "IdentityCollision",
        "ObserverInvalid": "ObserverInvalid",
        "ObserverContextMismatch": "ObserverContextMismatch",
        "ObserverHashMismatch": "ObserverHashMismatch",
        "PacketHashMismatch": "PacketHashMismatch",
        "OperatorManifestMismatch": "OperatorManifestMismatch",
        "TriggerManifestMismatch": "TriggerManifestMismatch",
        "TriggerCarrierMismatch": "TriggerCarrierMismatch",
        "TerminalizerMismatch": "TerminalizerMismatch",
        "MissingLicenseCandidate": "MissingLicenseCandidate",
        "LicenseNotRegistered": "LicenseNotRegistered",
        "PolicyBudgetExceeded": "PolicyBudgetExceeded",
        "ProducerReceiptMismatch": "ProducerReceiptMismatch",
        "ClassificationInvariant": "ClassificationInvariant",
        "ReplayMismatch": "ReplayMismatch",
        "Json": "Json",
    },
    type=str,
)
Gtoc3Error.__doc__ = "Structural mirror of Rust ``Gtoc3Error`` variants."


# The Rust value is intentionally not guessed by the structural mirror.
fn: Any = None


# END GENERATED RUST SURFACE


