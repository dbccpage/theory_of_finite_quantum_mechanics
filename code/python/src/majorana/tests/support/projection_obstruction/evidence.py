"""Typed evidence records for PO-000.

These records describe exact finite certificates, counterexamples, premise
checks, and numerical replays. They never return ``PROVEN`` and never mint
authority. Independent review must be emitted by a different process.
"""

from __future__ import annotations
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION: Literal["po000.mechanization_run.v3"] = "po000.mechanization_run.v3"
REQUIRED_CLAIM_IDS = tuple(
    [f"A{i}" for i in range(1, 8)]
    + [f"B{i}" for i in range(1, 5)]
    + [f"C{i}" for i in range(1, 5)]
    + [f"D{i}" for i in range(1, 9)] + ["D8a"]
    + [f"E{i}" for i in range(1, 10)]
    + [f"F{i}" for i in range(1, 4)]
    + [f"G{i}" for i in range(1, 5)]
    + [f"H{i}" for i in range(1, 8)]
)


class EvidenceKind(StrEnum):
    """The strongest evidence class the Python package can honestly emit."""

    EXACT_FINITE = "exact_finite"
    EXACT_SYMBOLIC_INSTANCE = "exact_symbolic_instance"
    FINITE_EXHAUSTIVE = "finite_exhaustive"
    NUMERICAL_REPLAY = "numerical_replay"
    COUNTEREXAMPLE = "counterexample"
    PREMISE_CHECK = "premise_check"
    STATIC_SCOPE_FENCE = "static_scope_fence"
    NOT_EXECUTABLE = "not_executable"


class ReplayVerdict(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    REFUSED = "refused"
    OPEN = "open"


class ClaimEvidence(BaseModel):
    """One claim-scoped replay or certificate result."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    claim_ids: tuple[str, ...]
    title: str
    evidence_kind: EvidenceKind
    verdict: ReplayVerdict
    statement_scope: str
    algorithm: str
    witness: dict[str, Any] = Field(default_factory=dict)
    limitations: tuple[str, ...] = ()
    authority_effect: Literal["None"] = "None"


class MechanizationRun(BaseModel):
    """Deterministic aggregate emitted by ``po000-replay``."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal["po000.mechanization_run.v3"] = SCHEMA_VERSION
    paper_id: Literal["PO-000"] = "PO-000"
    paper_version: str
    python_package_version: str
    results: tuple[ClaimEvidence, ...]
    unresolved_claim_ids: tuple[str, ...]
    source_hashes: dict[str, str] = Field(default_factory=dict)
    publication_hashes: dict[str, str] = Field(default_factory=dict)

    execution_completed: bool
    executable_checks_passed: bool
    open_obligations_present: bool
    refusals_present: bool
    claim_disposition_complete: bool
    promotion_eligible: Literal[False]
    authority_effect: Literal["None"] = "None"

    @model_validator(mode="after")
    def _aggregate_status_is_recomputed(self) -> MechanizationRun:
        """Reject self-inconsistent aggregate status fields."""

        claim_ids = tuple(claim_id for result in self.results for claim_id in result.claim_ids)
        if len(set(claim_ids)) != len(claim_ids):
            raise ValueError("claim_disposition_complete cannot be computed with duplicate claims")
        expected_executable = all(result.verdict != ReplayVerdict.FAIL for result in self.results)
        expected_refusals = any(result.verdict == ReplayVerdict.REFUSED for result in self.results)
        expected_open = bool(self.unresolved_claim_ids) or any(
            result.verdict == ReplayVerdict.OPEN for result in self.results
        )
        expected_complete = set(claim_ids) == set(REQUIRED_CLAIM_IDS)
        if self.execution_completed is not True:
            raise ValueError("execution_completed must be true")
        if self.executable_checks_passed is not expected_executable:
            raise ValueError("executable_checks_passed is inconsistent with result verdicts")
        if self.refusals_present is not expected_refusals:
            raise ValueError("refusals_present is inconsistent with result verdicts")
        if self.open_obligations_present is not expected_open:
            raise ValueError("open_obligations_present is inconsistent with unresolved/open claims")
        if self.claim_disposition_complete is not expected_complete:
            raise ValueError(
                "claim_disposition_complete is inconsistent with required claim coverage"
            )
        return self

    @property
    def passes(self) -> bool:
        """Executable check verdict indicator."""

        return (
            self.execution_completed
            and self.executable_checks_passed
            and all(result.verdict != ReplayVerdict.FAIL for result in self.results)
        )



