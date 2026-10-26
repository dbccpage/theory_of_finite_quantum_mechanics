"""Typed evidence records for PO-000.

These records describe exact finite certificates, counterexamples, premise
checks, and numerical replays. They never return ``PROVEN`` and never mint
authority. Independent review must be emitted by a different process.

2026-08-31: rewritten from pydantic models to frozen stdlib dataclasses so
the deposit depends on stdlib+numpy+pytest only.  The record shapes, the
recomputed-aggregate validation, and the JSON output layout are unchanged.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

SCHEMA_VERSION: Literal["po000.mechanization_run.v4"] = "po000.mechanization_run.v4"

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CLAIM_LEDGER_PATH = PACKAGE_ROOT / "projection_obstruction_claim_ledger.md"

# Proof-packet rows (P001-*) are a separate index, not paper claims.
_LEDGER_ROW = re.compile(r"^\|\s*`?([A-Z](?:\d+[A-Za-z0-9\-]*|-[A-Z][A-Z0-9\-]*))`?\s*\|", re.MULTILINE)


def load_required_claim_ids(ledger_path: Path = CLAIM_LEDGER_PATH) -> tuple[str, ...]:
    """Read the claim universe from the markdown ledger, which is authoritative.

    2026-09-03: this was a hand-maintained tuple of 47 ids whose ``H`` group
    stopped at ``H7``.  The ledger carried 51 -- ``E4-second``,
    ``E4-commutator``, ``H8`` and ``H9`` were missing -- so
    ``claim_disposition_complete`` could report True while four paper claims
    had never been considered at all.  Deriving the universe from the ledger
    means the two cannot drift apart again.

    Fails closed: a missing or unparseable ledger raises rather than yielding
    a short universe that would silently understate what must be dispositioned.
    """

    if not ledger_path.is_file():
        raise FileNotFoundError(
            f"claim ledger is required to determine the claim universe: {ledger_path}"
        )
    text = ledger_path.read_text(encoding="utf-8")
    ids = [cid for cid in dict.fromkeys(_LEDGER_ROW.findall(text))
           if not cid.startswith("P001-")]
    if not ids:
        raise ValueError(f"no claim rows parsed from {ledger_path}")
    return tuple(ids)


# Preserve the historical index without extending the retired ledger files.
# Current written theorem groups receive explicit non-executable dispositions.
REQUIRED_CLAIM_IDS = (
    *load_required_claim_ids(),
    "V68-CANCELLATION", "V68-LOCAL-ZERO", "V68-PHYSICAL",
    "V69-JORDAN", "V69-SELECTOR",
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


def _jsonable(value: Any) -> Any:
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


@dataclass(frozen=True)
class ClaimEvidence:
    """One claim-scoped replay or certificate result."""

    claim_ids: tuple[str, ...]
    title: str
    evidence_kind: EvidenceKind
    verdict: ReplayVerdict
    statement_scope: str
    algorithm: str
    witness: dict[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()
    authority_effect: Literal["None"] = "None"

    def __post_init__(self) -> None:
        object.__setattr__(self, "claim_ids", tuple(self.claim_ids))
        object.__setattr__(self, "limitations", tuple(self.limitations))
        object.__setattr__(self, "evidence_kind", EvidenceKind(self.evidence_kind))
        object.__setattr__(self, "verdict", ReplayVerdict(self.verdict))
        if not self.claim_ids or not all(isinstance(item, str) for item in self.claim_ids):
            raise ValueError("claim_ids must be a nonempty tuple of strings")
        if self.authority_effect != "None":
            raise ValueError("authority_effect must be the literal string None")
        if not isinstance(self.witness, dict):
            raise ValueError("witness must be a dict")

    def model_dump(self, mode: str = "python") -> dict[str, Any]:
        return {
            "claim_ids": _jsonable(self.claim_ids),
            "title": self.title,
            "evidence_kind": self.evidence_kind.value,
            "verdict": self.verdict.value,
            "statement_scope": self.statement_scope,
            "algorithm": self.algorithm,
            "witness": _jsonable(self.witness),
            "limitations": _jsonable(self.limitations),
            "authority_effect": self.authority_effect,
        }


@dataclass(frozen=True)
class MechanizationRun:
    """Deterministic aggregate emitted by ``po000-replay``."""

    paper_version: str
    python_package_version: str
    results: tuple[ClaimEvidence, ...]
    unresolved_claim_ids: tuple[str, ...]
    execution_completed: bool
    executable_checks_passed: bool
    open_obligations_present: bool
    refusals_present: bool
    claim_disposition_complete: bool
    promotion_eligible: Literal[False]
    schema_version: Literal["po000.mechanization_run.v4"] = SCHEMA_VERSION
    paper_id: Literal["PO-000"] = "PO-000"
    source_hashes: dict[str, str] = field(default_factory=dict)
    publication_hashes: dict[str, str] = field(default_factory=dict)
    finite_certificates: dict[str, Any] = field(default_factory=dict)
    authority_effect: Literal["None"] = "None"

    def __post_init__(self) -> None:
        object.__setattr__(self, "results", tuple(self.results))
        object.__setattr__(self, "unresolved_claim_ids", tuple(self.unresolved_claim_ids))
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("unexpected schema_version")
        if self.paper_id != "PO-000":
            raise ValueError("unexpected paper_id")
        if self.promotion_eligible is not False:
            raise ValueError("promotion_eligible must be false")
        if self.authority_effect != "None":
            raise ValueError("authority_effect must be the literal string None")
        self._aggregate_status_is_recomputed()

    def _aggregate_status_is_recomputed(self) -> None:
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

    def model_dump(self, mode: str = "python") -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "paper_id": self.paper_id,
            "paper_version": self.paper_version,
            "python_package_version": self.python_package_version,
            "results": [result.model_dump(mode=mode) for result in self.results],
            "unresolved_claim_ids": list(self.unresolved_claim_ids),
            "source_hashes": dict(self.source_hashes),
            "publication_hashes": dict(self.publication_hashes),
            "finite_certificates": _jsonable(self.finite_certificates),
            "execution_completed": self.execution_completed,
            "executable_checks_passed": self.executable_checks_passed,
            "open_obligations_present": self.open_obligations_present,
            "refusals_present": self.refusals_present,
            "claim_disposition_complete": self.claim_disposition_complete,
            "promotion_eligible": self.promotion_eligible,
            "authority_effect": self.authority_effect,
        }

    def model_dump_json(self, indent: int | None = None) -> str:
        return json.dumps(self.model_dump(mode="json"), indent=indent)

    @property
    def passes(self) -> bool:
        """Executable check verdict indicator."""

        return (
            self.execution_completed
            and self.executable_checks_passed
            and all(result.verdict != ReplayVerdict.FAIL for result in self.results)
        )
