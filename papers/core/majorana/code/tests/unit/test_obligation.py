from __future__ import annotations
"""INTAKE-S7: Non-vacuous assertion proof obligation tracker.

Replaces legacy mock-only test obligations with explicit, evidence-bound assertion laws.
AuthorityEffect: None.
"""


from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class TestObligationStatus(str, Enum):
    __test__ = False
    PROPOSED = "PROPOSED"
    VERIFIED_NON_VACUOUS = "VERIFIED_NON_VACUOUS"
    REFUSED_TAUTOLOGY = "REFUSED_TAUTOLOGY"
    REWRITE_REQUIRED = "REWRITE_REQUIRED"


class TestObligationRefuse(Exception):
    __test__ = False

    def __init__(self, refuse_class: str, message: str, **detail: Any) -> None:
        super().__init__(message)
        self.refuse_class = refuse_class
        self.detail = detail


@dataclass
class TestObligation:
    __test__ = False
    obligation_id: str
    target_symbol: str
    assertion_expr: str
    status: TestObligationStatus = TestObligationStatus.PROPOSED
    evidence_path: Optional[str] = None
    authority_effect: str = "None"
    note: str = ""

    def __post_init__(self) -> None:
        if not self.obligation_id.strip():
            raise TestObligationRefuse("EMPTY_ID", "empty obligation_id")
        if not self.target_symbol.strip():
            raise TestObligationRefuse("EMPTY_SYMBOL", "empty target_symbol")
        if self.authority_effect != "None":
            raise TestObligationRefuse(
                "AUTHORITY_LAUNDER",
                f"authority_effect must be None (got {self.authority_effect})",
            )
        # Verify non-vacuous assertion expression rule
        expr_clean = self.assertion_expr.strip().lower()
        if expr_clean in (
            "assert true",
            "assert 1 == 1",
            "assert true is true",
            "pass",
        ):
            self.status = TestObligationStatus.REFUSED_TAUTOLOGY
            self.note = "refused: tautology assertion detected"

    def verify_evidence(self, path: str) -> TestObligationStatus:
        if self.status == TestObligationStatus.REFUSED_TAUTOLOGY:
            raise TestObligationRefuse(
                "TAUTOLOGY_CANNOT_VERIFY",
                "tautology assertions cannot achieve VERIFIED_NON_VACUOUS status",
            )
        if not path or not path.strip():
            self.status = TestObligationStatus.REWRITE_REQUIRED
            return self.status
        self.evidence_path = path
        self.status = TestObligationStatus.VERIFIED_NON_VACUOUS
        return self.status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "obligation_id": self.obligation_id,
            "target_symbol": self.target_symbol,
            "assertion_expr": self.assertion_expr,
            "status": self.status.value,
            "evidence_path": self.evidence_path,
            "authority_effect": self.authority_effect,
            "note": self.note,
        }
