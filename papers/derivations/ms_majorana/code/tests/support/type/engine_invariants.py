"""Value types consumed by engine invariant checks."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Tolerances:
    max_drift: float
    threshold: float


class EscalationRoute:
    MetaAnalysis = "MetaAnalysis"
    SolverReview = "SolverReview"
    ManifestRefinement = "ManifestRefinement"


class EvaluationVerdict:
    @classmethod
    def Escalate(cls, route):
        return {"type": "Escalate", "route": route}


class TerminationCondition:
    Irreducible = "Irreducible"
    ContextIrreducible = "ContextIrreducible"


class EngineDecision:
    Lift = "Lift"
    EnterMetaAnalysis = "EnterMetaAnalysis"
    Continue = "Continue"

    @classmethod
    def Terminate(cls, condition):
        return {"type": "Terminate", "condition": condition}


@dataclass
class EngineTraceStep:
    evaluator_verdict: object
    decision: object
    phi: float
    gamma2: float


@dataclass
class EngineRuntimeState:
    trace: list
    step_index: int
    state: object


@dataclass
class EvaluationAudit:
    proposed: int = 0
    evaluated: int = 0
    duplicate_pruned: int = 0
    budget_pruned: int = 0
    already_seen_pruned: int = 0


@dataclass(frozen=True)
class RunSummary:
    final_phi: float
    termination: str
    lift_count: int
    final_mss_level: int


__all__ = ["EngineDecision", "EngineRuntimeState", "EngineTraceStep", "EscalationRoute", "EvaluationAudit", "EvaluationVerdict", "RunSummary", "TerminationCondition", "Tolerances"]
