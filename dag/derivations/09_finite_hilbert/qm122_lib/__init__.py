"""Exported count of reversible Bool report maps from the QM-122 Python dual.

Origin: papers/foundations/finite_ledger.md claim QM-122-C38.
Claim: urn:omega:fqm:qm122:exported-reversible-report-count:v1
AuthorityEffect: None
Mutation-Kills: 3 non-equivalent source mutants, executed by papers/foundations/_code/qm_122/tests/test_qm122_dual.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 3; AST Sonar cognitive complexity max 2; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 3.
Scope Fence: The exported count is the Bool reversible census. It is not Gleason, not M_n(C), and not an authority grant.
"""

from __future__ import annotations

from .qm122_dual import Qm122DualError, qm122_dual_receipt

__all__ = ["Qm122DualError", "exported_reversible_report_count", "qm122_dual_receipt"]


def exported_reversible_report_count() -> int:
    """Return the dual's reversible report count after the named receipt checks."""
    receipt = qm122_dual_receipt()
    count = receipt.reversible_reports
    if type(count) is not int:
        raise Qm122DualError("exported count is not an integer", {"received": type(count).__name__})
    if count != 2:
        raise Qm122DualError("exported reversible report count is not 2", {"count": count})
    return count
