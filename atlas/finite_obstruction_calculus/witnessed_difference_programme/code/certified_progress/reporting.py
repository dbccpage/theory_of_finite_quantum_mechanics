"""Reporting precedence after an actual certificate check."""

from fractions import Fraction

from .checker import check_certificate
from .model import compile_model, rational


def report_termination(model, certificate, budget, *, task_admits_impossibility=False):
    if type(task_admits_impossibility) is not bool:
        raise ValueError("task reporting policy must be an explicit boolean")
    available = rational(budget)
    receipt = check_certificate(model, certificate)
    if not receipt["accepted"]:
        return {"termination": "RefusedCertificate", "receipt": receipt}
    arena = compile_model(model)
    if receipt["claim"] == "LOSS":
        if not arena.moves(arena.initial):
            termination = "Stalled"
        else:
            termination = "Impossible" if task_admits_impossibility else "LosingInDeclaredArena"
    elif Fraction(receipt["initial_value"]) <= available:
        termination = "ResolvedWithinBudget"
    elif receipt["claim"] == "WIN_OPTIMAL":
        termination = "Exhausted"
    else:
        termination = "UndeterminedBudget"
    return {"termination": termination, "receipt": receipt,
            "task_admits_impossibility": task_admits_impossibility,
            "authority_effect": "None"}
