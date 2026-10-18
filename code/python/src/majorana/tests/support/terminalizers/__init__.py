"""Omega Terminalizers package.

Provides terminalization classifiers, spine terminal mappings, and public certificates.
"""

from __future__ import annotations
from .termz_refusals import TerminalizerRefusal as TerminalizerRefusal
from .termz_debt import (
    DEBT_GROUNDS as DEBT_GROUNDS,
    DEBT_GROUND_PRECOMMITTED_BUDGET as DEBT_GROUND_PRECOMMITTED_BUDGET,
    DEBT_GROUND_COFINALITY as DEBT_GROUND_COFINALITY,
    DebtRecord as DebtRecord,
    BudgetUnknownTerminal as BudgetUnknownTerminal,
    emit_budget_unknown as emit_budget_unknown,
)
from .termz_finite_obstruction_calculus import (
    classify_phi_gamma as classify_phi_gamma,
    TerminalizerVerdict as TerminalizerVerdict,
)
from .termz_pointed_classifier import (
    ObstructionStatus,
    PointedObstructionClassifier,
    terminalize,
)
from .termz_boundary_closure import (
    BoundaryClosureTerminalGate,
    TerminalBranchResult,
    TerminalBranchVerdict,
)

__all__ = [
    "TerminalizerRefusal",
    "DEBT_GROUNDS",
    "DEBT_GROUND_PRECOMMITTED_BUDGET",
    "DEBT_GROUND_COFINALITY",
    "DebtRecord",
    "BudgetUnknownTerminal",
    "emit_budget_unknown",
    "classify_phi_gamma",
    "TerminalizerVerdict",
    "Terminal",
    "TerminalOutcome",
    "ValidatorReport",
    "ObstructionStatus",
    "PointedObstructionClassifier",
    "terminalize",
    "BoundaryClosureTerminalGate",
    "TerminalBranchResult",
    "TerminalBranchVerdict",
]
