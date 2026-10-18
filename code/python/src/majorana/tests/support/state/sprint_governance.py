from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/sprint_governance.rs``.

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


SPRINT_GOVERNANCE_SCHEMA_VERSION: Any = None


SPRINT_RETROSPECTIVE_SCHEMA_VERSION: Any = None


SprintLifecycleV1 = Enum(
    "SprintLifecycleV1",
    {
        "Planned": "Planned",
        "Ready": "Ready",
        "Active": "Active",
        "Blocked": "Blocked",
        "Completed": "Completed",
    },
    type=str,
)
SprintLifecycleV1.__doc__ = "Structural mirror of Rust ``SprintLifecycleV1`` variants."


SprintAuthorityStatusV1 = Enum(
    "SprintAuthorityStatusV1",
    {
        "None": "None",
        "PendingHumanPromotion": "PendingHumanPromotion",
        "AuthorizedLocalResult": "AuthorizedLocalResult",
        "HumanRejected": "HumanRejected",
    },
    type=str,
)
SprintAuthorityStatusV1.__doc__ = (
    "Structural mirror of Rust ``SprintAuthorityStatusV1`` variants."
)


ProcessProfileKindV1 = Enum(
    "ProcessProfileKindV1",
    {
        "RustDevelopment": "RustDevelopment",
        "PythonDevelopment": "PythonDevelopment",
        "LeanMathematics": "LeanMathematics",
        "ResearchPaper": "ResearchPaper",
        "ManualEdit": "ManualEdit",
        "Mixed": "Mixed",
    },
    type=str,
)
ProcessProfileKindV1.__doc__ = (
    "Structural mirror of Rust ``ProcessProfileKindV1`` variants."
)


ALL: Any = None


ProfileOperationV1 = Enum(
    "ProfileOperationV1",
    {
        "EditRust": "EditRust",
        "EditPython": "EditPython",
        "EditLean": "EditLean",
        "EditResearchPaper": "EditResearchPaper",
        "ApplyExactManualDiff": "ApplyExactManualDiff",
        "EditMixedCarrier": "EditMixedCarrier",
        "UpdateClaimLedger": "UpdateClaimLedger",
        "UpdateCitations": "UpdateCitations",
        "RunFocusedGate": "RunFocusedGate",
    },
    type=str,
)
ProfileOperationV1.__doc__ = (
    "Structural mirror of Rust ``ProfileOperationV1`` variants."
)


DeterministicGateV1 = Enum(
    "DeterministicGateV1",
    {
        "ExactDiffReview": "ExactDiffReview",
        "IndependentWitness": "IndependentWitness",
        "AuthorityBoundary": "AuthorityBoundary",
        "RustFormat": "RustFormat",
        "RustCheck": "RustCheck",
        "RustClippy": "RustClippy",
        "RustFocusedTests": "RustFocusedTests",
        "PythonLint": "PythonLint",
        "PythonTypeCheck": "PythonTypeCheck",
        "PythonImportCheck": "PythonImportCheck",
        "PythonFocusedTests": "PythonFocusedTests",
        "LeanTargetBuild": "LeanTargetBuild",
        "LeanPlaceholderScan": "LeanPlaceholderScan",
        "LeanAxiomAudit": "LeanAxiomAudit",
        "PaperClaimBinding": "PaperClaimBinding",
        "CitationAudit": "CitationAudit",
        "ArtifactBuild": "ArtifactBuild",
        "EvidenceCeilingAudit": "EvidenceCeilingAudit",
    },
    type=str,
)
DeterministicGateV1.__doc__ = (
    "Structural mirror of Rust ``DeterministicGateV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class CompiledProcessProfileV1(_RustSurfaceObject):
    """Structural mirror of Rust ``CompiledProcessProfileV1``."""

    profile: Any = None
    stages: Any = None
    allowed_operations: Any = None
    required_gates: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "profile",
            "stages",
            "allowed_operations",
            "required_gates",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "CompiledProcessProfileV1 received too many positional arguments"
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
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/sprint_governance.rs::validate"
    )


def permits(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``permits``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/sprint_governance.rs::permits"
    )


def compile_process_profile_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``compile_process_profile_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/sprint_governance.rs::compile_process_profile_v1"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SprintBudgetsV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SprintBudgetsV1``."""

    attempt_budget: Any = None
    successor_budget: Any = None
    time_budget_seconds: Any = None
    process_budget: Any = None
    token_budget: Any = None
    repair_budget: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "attempt_budget",
            "successor_budget",
            "time_budget_seconds",
            "process_budget",
            "token_budget",
            "repair_budget",
        )
        if len(args) > len(names):
            raise TypeError("SprintBudgetsV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SprintWitnessPlanV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SprintWitnessPlanV1``."""

    producer_id: Any = None
    independent_evaluator_id: Any = None
    authority_witness_id: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("producer_id", "independent_evaluator_id", "authority_witness_id")
        if len(args) > len(names):
            raise TypeError(
                "SprintWitnessPlanV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SprintStoryV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SprintStoryV1``."""

    story_id: Any = None
    lifecycle: Any = None
    producer_id: Any = None
    profile: Any = None
    operations: Any = None
    write_surface: Any = None
    acceptance_criteria: Any = None
    evidence_receipts: Any = None
    survivor_route: Any = None
    nonclaims: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "story_id",
            "lifecycle",
            "producer_id",
            "profile",
            "operations",
            "write_surface",
            "acceptance_criteria",
            "evidence_receipts",
            "survivor_route",
            "nonclaims",
        )
        if len(args) > len(names):
            raise TypeError("SprintStoryV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class StoryDependencyV1(_RustSurfaceObject):
    """Structural mirror of Rust ``StoryDependencyV1``."""

    predecessor: Any = None
    successor: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("predecessor", "successor")
        if len(args) > len(names):
            raise TypeError("StoryDependencyV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SprintGovernancePacketV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SprintGovernancePacketV1``."""

    schema_version: Any = None
    sprint_id: Any = None
    parent_saga_ids: Any = None
    lifecycle: Any = None
    gtoc_terminal: Any = None
    authority_status: Any = None
    authority_effect: Any = None
    frozen_base: Any = None
    packet_sha256: Any = None
    observer_sha256: Any = None
    profiles: Any = None
    stories: Any = None
    dependency_edges: Any = None
    exact_write_surface: Any = None
    budgets: Any = None
    witnesses: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "sprint_id",
            "parent_saga_ids",
            "lifecycle",
            "gtoc_terminal",
            "authority_status",
            "authority_effect",
            "frozen_base",
            "packet_sha256",
            "observer_sha256",
            "profiles",
            "stories",
            "dependency_edges",
            "exact_write_surface",
            "budgets",
            "witnesses",
        )
        if len(args) > len(names):
            raise TypeError(
                "SprintGovernancePacketV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def validate_against_leases(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate_against_leases``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/sprint_governance.rs::validate_against_leases"
    )


def validate_successor_request(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate_successor_request``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/sprint_governance.rs::validate_successor_request"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SprintPathLeaseV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SprintPathLeaseV1``."""

    lease_id: Any = None
    owner: Any = None
    exact_paths: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("lease_id", "owner", "exact_paths")
        if len(args) > len(names):
            raise TypeError("SprintPathLeaseV1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


SprintActorRoleV1 = Enum(
    "SprintActorRoleV1",
    {
        "Host": "Host",
        "Producer": "Producer",
        "IndependentEvaluator": "IndependentEvaluator",
        "AuthorityWitness": "AuthorityWitness",
    },
    type=str,
)
SprintActorRoleV1.__doc__ = "Structural mirror of Rust ``SprintActorRoleV1`` variants."


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SprintSuccessorRequestV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SprintSuccessorRequestV1``."""

    source_sprint_id: Any = None
    requested_by: Any = None
    candidate_ids: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("source_sprint_id", "requested_by", "candidate_ids")
        if len(args) > len(names):
            raise TypeError(
                "SprintSuccessorRequestV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


ImprovementCandidateRouteV1 = Enum(
    "ImprovementCandidateRouteV1",
    {"HostAdmissionRequired": "HostAdmissionRequired"},
    type=str,
)
ImprovementCandidateRouteV1.__doc__ = (
    "Structural mirror of Rust ``ImprovementCandidateRouteV1`` variants."
)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class OperatorImprovementCandidateV1(_RustSurfaceObject):
    """Structural mirror of Rust ``OperatorImprovementCandidateV1``."""

    candidate_id: Any = None
    proposed_change: Any = None
    route: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("candidate_id", "proposed_change", "route")
        if len(args) > len(names):
            raise TypeError(
                "OperatorImprovementCandidateV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SprintRetrospectiveV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SprintRetrospectiveV1``."""

    schema_version: Any = None
    sprint_id: Any = None
    observed_phi1: Any = None
    surviving_gamma2: Any = None
    improvement_candidates: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "sprint_id",
            "observed_phi1",
            "surviving_gamma2",
            "improvement_candidates",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "SprintRetrospectiveV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def validate_against(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate_against``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/sprint_governance.rs::validate_against"
    )


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class SprintGovernanceVerificationV1(_RustSurfaceObject):
    """Structural mirror of Rust ``SprintGovernanceVerificationV1``."""

    schema_version: Any = None
    sprint_id: Any = None
    profile_kinds: Any = None
    stage_count_per_profile: Any = None
    story_count: Any = None
    dependency_edge_count: Any = None
    exact_write_count: Any = None
    authority_effect: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "schema_version",
            "sprint_id",
            "profile_kinds",
            "stage_count_per_profile",
            "story_count",
            "dependency_edge_count",
            "exact_write_count",
            "authority_effect",
        )
        if len(args) > len(names):
            raise TypeError(
                "SprintGovernanceVerificationV1 received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def verify_sprint_governance_v1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``verify_sprint_governance_v1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/sprint_governance.rs::verify_sprint_governance_v1"
    )


SprintGovernanceError = Enum(
    "SprintGovernanceError",
    {
        "SchemaVersion": "SchemaVersion",
        "InvalidIdentifier": "InvalidIdentifier",
        "ParentCount": "ParentCount",
        "UnfrozenAdmission": "UnfrozenAdmission",
        "TerminalDomainConflation": "TerminalDomainConflation",
        "AuthorityConflation": "AuthorityConflation",
        "InvalidBudgets": "InvalidBudgets",
        "WitnessIdentityConflict": "WitnessIdentityConflict",
        "MissingRequiredField": "MissingRequiredField",
        "NotSortedUnique": "NotSortedUnique",
        "DuplicateValue": "DuplicateValue",
        "NonExactPath": "NonExactPath",
        "ProfileStageDrift": "ProfileStageDrift",
        "IncompleteProfile": "IncompleteProfile",
        "UnknownProfile": "UnknownProfile",
        "UnsupportedOperation": "UnsupportedOperation",
        "DuplicateStory": "DuplicateStory",
        "IncompleteStory": "IncompleteStory",
        "StoryWriteOutsideSprint": "StoryWriteOutsideSprint",
        "SharedWriteConflict": "SharedWriteConflict",
        "UnknownDependency": "UnknownDependency",
        "DependencyCycle": "DependencyCycle",
        "LeaseConflict": "LeaseConflict",
        "SuccessorSourceMismatch": "SuccessorSourceMismatch",
        "SuccessorHostOnly": "SuccessorHostOnly",
        "SuccessorBudgetExceeded": "SuccessorBudgetExceeded",
        "RetrospectiveSprintMismatch": "RetrospectiveSprintMismatch",
        "RetrospectiveBeforeTerminal": "RetrospectiveBeforeTerminal",
        "DuplicateImprovementCandidate": "DuplicateImprovementCandidate",
        "RetrospectiveSelfActivation": "RetrospectiveSelfActivation",
    },
    type=str,
)
SprintGovernanceError.__doc__ = (
    "Structural mirror of Rust ``SprintGovernanceError`` variants."
)


fn: Any = None




