"""ASI Regime Contract & Legal Governance Gateway.

Central machine-executable legal governance, constitutional axioms,
mathematical invariants, and fail-closed verification gates for LLMs, ASI,
and sovereign operator oversight.

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path

REGIME_ROOT = Path(__file__).resolve().parent

STRATA = (
    "00_constitution",
    "10_math",
    "20_execution",
    "30_evidence",
    "40_packets",
    "50_os",
)

__all__ = [
    "REGIME_ROOT",
    "STRATA",
]
