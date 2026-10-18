from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/gtoc1_classifier.rs``.

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


GTOC1_ADMISSION_SCHEMA_VERSION: Any = None


GTOC1_PACKET_SCHEMA_VERSION: Any = None


GTOC1_CLASSIFICATION_SCHEMA_VERSION: Any = None


GTOC1_RECEIPT_SCHEMA_VERSION: Any = None


GTOC1_OBSERVER_DOMAIN: Any = None


GTOC1_STATE_DOMAIN: Any = None


GTOC1_EVIDENCE_CEILING: Any = None


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SourceHashV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SourceHashV1``."""

    path: Any = None
    sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("path", "sha256")
        if len(args) > len(names):
            raise TypeError("SourceHashV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1BudgetsV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1BudgetsV1``."""

    attempt_budget: Any = None
    repair_budget: Any = None
    successor_budget: Any = None
    time_budget_seconds: Any = None
    process_budget: Any = None
    token_budget: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "attempt_budget",
            "repair_budget",
            "successor_budget",
            "time_budget_seconds",
            "process_budget",
            "token_budget",
        )
        if len(args) > len(names):
            raise TypeError("Gtoc1BudgetsV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class RetainedCarrierV1(_RustSurfaceObject):
    """Structural mirror of Rust ``RetainedCarrierV1``."""

    carrier_id: Any = None
    retained_edge_count: Any = None
    retention_witness_ids: Any = None
    recomparison_witness_ids: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "carrier_id",
            "retained_edge_count",
            "retention_witness_ids",
            "recomparison_witness_ids",
        )
        if len(args) > len(names):
            raise TypeError("RetainedCarrierV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class RationalV1(_RustSurfaceObject):
    """Structural mirror of Rust ``RationalV1``."""

    numerator: Any = None
    denominator: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("numerator", "denominator")
        if len(args) > len(names):
            raise TypeError("RationalV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def integer(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``integer``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc1_classifier.rs::integer"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class RationalMatrixV1(_RustSurfaceObject):
    """Structural mirror of Rust ``RationalMatrixV1``."""

    rows: Any = None
    cols: Any = None
    row_major: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("rows", "cols", "row_major")
        if len(args) > len(names):
            raise TypeError("RationalMatrixV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class DeclaredCochainWindowV1(_RustSurfaceObject):
    """Structural mirror of Rust ``DeclaredCochainWindowV1``."""

    window_id: Any = None
    zero_relation_id: Any = None
    rule_id: Any = None
    residual_id: Any = None
    d0: Any = None
    d1: Any = None
    residual: Any = None
    stabilization_witness_id: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "window_id",
            "zero_relation_id",
            "rule_id",
            "residual_id",
            "d0",
            "d1",
            "residual",
            "stabilization_witness_id",
        )
        if len(args) > len(names):
            raise TypeError(
                "DeclaredCochainWindowV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


NoRuleReasonV1 = Enum(
    "NoRuleReasonV1",
    {
        "ClosureWindowUndeclared": "ClosureWindowUndeclared",
        "SourceEvidenceUnavailable": "SourceEvidenceUnavailable",
        "RuleOutsideFrozenCarrier": "RuleOutsideFrozenCarrier",
    },
    type=str,
)
NoRuleReasonV1.__doc__ = "Structural mirror of Rust ``NoRuleReasonV1`` variants."


NoRuleDispositionV1 = Enum(
    "NoRuleDispositionV1",
    {"RequestSource": "RequestSource", "Refuse": "Refuse"},
    type=str,
)
NoRuleDispositionV1.__doc__ = (
    "Structural mirror of Rust ``NoRuleDispositionV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class UnavailableRuleV1(_RustSurfaceObject):
    """Structural mirror of Rust ``UnavailableRuleV1``."""

    rule_request_id: Any = None
    reason: Any = None
    disposition: Any = None
    basis: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("rule_request_id", "reason", "disposition", "basis")
        if len(args) > len(names):
            raise TypeError("UnavailableRuleV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


WindowRuleV1 = Enum(
    "WindowRuleV1", {"Declared": "Declared", "Unavailable": "Unavailable"}, type=str
)
WindowRuleV1.__doc__ = "Structural mirror of Rust ``WindowRuleV1`` variants."


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1PacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1PacketV1``."""

    schema_version: Any = None
    packet_id: Any = None
    frozen_base: Any = None
    target_rows: Any = None
    source_manifest: Any = None
    budgets: Any = None
    evidence_ceiling: Any = None
    observer: Any = None
    producer_id: Any = None
    evaluator_id: Any = None
    authority_witness_id: Any = None
    prior_work_ledger: Any = None
    carrier: Any = None
    rule: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "frozen_base",
            "target_rows",
            "source_manifest",
            "budgets",
            "evidence_ceiling",
            "observer",
            "producer_id",
            "evaluator_id",
            "authority_witness_id",
            "prior_work_ledger",
            "carrier",
            "rule",
        )
        if len(args) > len(names):
            raise TypeError("Gtoc1PacketV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def validate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc1_classifier.rs::validate"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1AdmissionV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1AdmissionV1``."""

    schema_version: Any = None
    packet: Any = None
    packet_sha256: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("schema_version", "packet", "packet_sha256")
        if len(args) > len(names):
            raise TypeError("Gtoc1AdmissionV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


Gtoc1RouteV1 = Enum(
    "Gtoc1RouteV1",
    {
        "ExactRepair": "ExactRepair",
        "ClosedResidual": "ClosedResidual",
        "ActiveClosureFailure": "ActiveClosureFailure",
        "NoRule": "NoRule",
    },
    type=str,
)
Gtoc1RouteV1.__doc__ = "Structural mirror of Rust ``Gtoc1RouteV1`` variants."


ALL: Any = None


DiagnosticSupportV1 = Enum(
    "DiagnosticSupportV1",
    {"Zero": "Zero", "NonZero": "NonZero", "NotPopulated": "NotPopulated"},
    type=str,
)
DiagnosticSupportV1.__doc__ = (
    "Structural mirror of Rust ``DiagnosticSupportV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1ClassificationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1ClassificationV1``."""

    schema_version: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    observer_sha256: Any = None
    phi1_support: Any = None
    gamma2_support: Any = None
    route: Any = None
    terminal_proposal: Any = None
    residual_ids: Any = None
    evidence_ceiling: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "packet_sha256",
            "observer_sha256",
            "phi1_support",
            "gamma2_support",
            "route",
            "terminal_proposal",
            "residual_ids",
            "evidence_ceiling",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc1ClassificationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1RouteStatusRowV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1RouteStatusRowV1``."""

    route: Any = None
    phi1_support: Any = None
    gamma2_support: Any = None
    legal_terminals: Any = None
    requirement: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "route",
            "phi1_support",
            "gamma2_support",
            "legal_terminals",
            "requirement",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc1RouteStatusRowV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def gtoc1_route_status_matrix_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``gtoc1_route_status_matrix_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc1_classifier.rs::gtoc1_route_status_matrix_v1"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1ProducerReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1ProducerReceiptV1``."""

    schema_version: Any = None
    packet_id: Any = None
    packet_sha256: Any = None
    observer_sha256: Any = None
    producer_id: Any = None
    source_manifest_sha256: Any = None
    classifier_input_sha256: Any = None
    classification_sha256: Any = None
    route: Any = None
    terminal_proposal: Any = None
    residual_ids: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "packet_sha256",
            "observer_sha256",
            "producer_id",
            "source_manifest_sha256",
            "classifier_input_sha256",
            "classification_sha256",
            "route",
            "terminal_proposal",
            "residual_ids",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc1ProducerReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1EvaluationReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1EvaluationReceiptV1``."""

    schema_version: Any = None
    evaluator_id: Any = None
    producer_id: Any = None
    algorithm: Any = None
    replay_classification_sha256: Any = None
    producer_classification_sha256: Any = None
    exact_match: Any = None
    route: Any = None
    terminal_proposal: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "evaluator_id",
            "producer_id",
            "algorithm",
            "replay_classification_sha256",
            "producer_classification_sha256",
            "exact_match",
            "route",
            "terminal_proposal",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc1EvaluationReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1AuthorityWitnessAttestationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1AuthorityWitnessAttestationV1``."""

    schema_version: Any = None
    authority_witness_id: Any = None
    producer_evaluator_witness_distinct: Any = None
    evidence_ceiling_preserved: Any = None
    promotion_performed: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "authority_witness_id",
            "producer_evaluator_witness_distinct",
            "evidence_ceiling_preserved",
            "promotion_performed",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc1AuthorityWitnessAttestationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1ReplayReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1ReplayReceiptV1``."""

    schema_version: Any = None
    packet_sha256: Any = None
    classification_sha256: Any = None
    replay_sha256: Any = None
    deterministic: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_sha256",
            "classification_sha256",
            "replay_sha256",
            "deterministic",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc1ReplayReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


Gtoc1HumanDecisionV1 = Enum(
    "Gtoc1HumanDecisionV1", {"PendingHumanPromotion": "PendingHumanPromotion"}, type=str
)
Gtoc1HumanDecisionV1.__doc__ = (
    "Structural mirror of Rust ``Gtoc1HumanDecisionV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1TerminalReceiptV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1TerminalReceiptV1``."""

    schema_version: Any = None
    packet_id: Any = None
    route: Any = None
    terminal_proposal: Any = None
    residual_ids: Any = None
    human_decision: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "packet_id",
            "route",
            "terminal_proposal",
            "residual_ids",
            "human_decision",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc1TerminalReceiptV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1ReceiptBundleV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1ReceiptBundleV1``."""

    schema_version: Any = None
    producer: Any = None
    evaluation: Any = None
    authority_witness: Any = None
    replay: Any = None
    terminal: Any = None
    target_status_matrix: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "producer",
            "evaluation",
            "authority_witness",
            "replay",
            "terminal",
            "target_status_matrix",
        )
        if len(args) > len(names):
            raise TypeError(
                "Gtoc1ReceiptBundleV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class Gtoc1ExecutionV1(_RustSurfaceObject):
    """Structural mirror of Rust ``Gtoc1ExecutionV1``."""

    classification: Any = None
    receipts: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("classification", "receipts")
        if len(args) > len(names):
            raise TypeError("Gtoc1ExecutionV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def classify_gtoc1_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``classify_gtoc1_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc1_classifier.rs::classify_gtoc1_v1"
    )


def execute_and_evaluate_gtoc1_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``execute_and_evaluate_gtoc1_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc1_classifier.rs::execute_and_evaluate_gtoc1_v1"
    )


def evaluate_gtoc1_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``evaluate_gtoc1_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc1_classifier.rs::evaluate_gtoc1_v1"
    )


def observer_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``observer_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc1_classifier.rs::observer_sha256_v1"
    )


def packet_sha256_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``packet_sha256_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc1_classifier.rs::packet_sha256_v1"
    )


def sha256_json_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``sha256_json_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc1_classifier.rs::sha256_json_v1"
    )


def sha256_bytes_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``sha256_bytes_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/gtoc1_classifier.rs::sha256_bytes_v1"
    )


Gtoc1Error = Enum(
    "Gtoc1Error",
    {
        "SchemaMismatch": "SchemaMismatch",
        "EmptyField": "EmptyField",
        "InvalidSha256": "InvalidSha256",
        "InvalidGitCommit": "InvalidGitCommit",
        "NonCanonicalList": "NonCanonicalList",
        "InvalidWritePath": "InvalidWritePath",
        "ScopeExpansion": "ScopeExpansion",
        "BudgetOutsideAdmission": "BudgetOutsideAdmission",
        "EvidenceCeilingChanged": "EvidenceCeilingChanged",
        "IdentityCollision": "IdentityCollision",
        "CarrierNotRetained": "CarrierNotRetained",
        "ObserverContextMismatch": "ObserverContextMismatch",
        "ObserverSourceManifestMismatch": "ObserverSourceManifestMismatch",
        "ObserverInvalid": "ObserverInvalid",
        "ObserverHashMismatch": "ObserverHashMismatch",
        "PacketHashMismatch": "PacketHashMismatch",
        "RationalOutsideFiniteDomain": "RationalOutsideFiniteDomain",
        "NonCanonicalRational": "NonCanonicalRational",
        "MatrixDimensionOutsideFiniteDomain": "MatrixDimensionOutsideFiniteDomain",
        "MatrixShape": "MatrixShape",
        "MatrixEncoding": "MatrixEncoding",
        "ResidualDimension": "ResidualDimension",
        "InvalidCochainComposition": "InvalidCochainComposition",
        "Homological": "Homological",
        "ClassificationInvariant": "ClassificationInvariant",
        "AuthorityExpanded": "AuthorityExpanded",
        "ProducerReceiptMismatch": "ProducerReceiptMismatch",
        "ReplayMismatch": "ReplayMismatch",
        "Json": "Json",
    },
    type=str,
)
Gtoc1Error.__doc__ = "Structural mirror of Rust ``Gtoc1Error`` variants."


fn: Any = None




