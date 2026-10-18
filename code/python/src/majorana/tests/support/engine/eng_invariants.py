class EngineError(Exception):
    pass


class TerminationViolation(EngineError):
    pass


class RuntimeFailure(EngineError):
    pass


class Tolerances:
    def __init__(self, max_drift: float, threshold: float):
        self.max_drift = max_drift
        self.threshold = threshold


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


class EngineTraceStep:
    def __init__(self, evaluator_verdict, decision, phi: float, gamma2: float):
        self.evaluator_verdict = evaluator_verdict
        self.decision = decision
        self.phi = phi
        self.gamma2 = gamma2


class EngineRuntimeState:
    def __init__(self, trace: list, step_index: int, state):
        self.trace = trace
        self.step_index = step_index
        self.state = state




def assert_trace_integrity(runtime: EngineRuntimeState):
    if len(runtime.trace) != runtime.step_index:
        raise TerminationViolation(
            f"trace length {len(runtime.trace)} != step_index {runtime.step_index}"
        )


def assert_meta_escalation_resolution(trace: list):
    for i in range(len(trace) - 1):
        prev = trace[i]
        nxt = trace[i + 1]

        was_meta_escalation = False
        if (
            isinstance(prev.evaluator_verdict, dict)
            and prev.evaluator_verdict.get("type") == "Escalate"
        ):
            if (
                prev.evaluator_verdict.get("route") == EscalationRoute.MetaAnalysis
                or prev.evaluator_verdict.get("route") == "MetaAnalysis"
            ):
                was_meta_escalation = True

        if not was_meta_escalation:
            continue

        resolved = False
        decision = nxt.decision
        if isinstance(decision, str):
            if decision in [EngineDecision.Lift, EngineDecision.EnterMetaAnalysis]:
                resolved = True
        elif isinstance(decision, dict) and decision.get("type") == "Terminate":
            cond = decision.get("condition")
            if cond in [
                TerminationCondition.Irreducible,
                TerminationCondition.ContextIrreducible,
            ]:
                resolved = True

        if not resolved:
            raise TerminationViolation(
                "Meta escalation was not followed by Lift, Irreducible termination, or MetaAnalysis"
            )


def assert_stagnation_resolves(
    trace: list, stagnation_window: int, tolerances: Tolerances
):
    if len(trace) < stagnation_window:
        return

    recent = trace[-stagnation_window:]

    constant_phi = True
    for i in range(len(recent) - 1):
        if abs(recent[i].phi - recent[i + 1].phi) > tolerances.max_drift:
            constant_phi = False
            break

    last_step = recent[-1]
    phi_positive = last_step.phi > tolerances.threshold
    gamma2_zero = last_step.gamma2 <= tolerances.threshold

    stable_irreducible_candidate = phi_positive and gamma2_zero and constant_phi

    if stable_irreducible_candidate:
        resolved = False
        for t in recent:
            decision = t.decision
            if isinstance(decision, str):
                if decision in [EngineDecision.Lift, EngineDecision.EnterMetaAnalysis]:
                    resolved = True
                    break
            elif isinstance(decision, dict) and decision.get("type") == "Terminate":
                cond = decision.get("condition")
                if cond in [
                    TerminationCondition.Irreducible,
                    TerminationCondition.ContextIrreducible,
                ]:
                    resolved = True
                    break

        if not resolved:
            raise TerminationViolation(
                "Φ₁ > 0, Γ₂ = 0 stagnation silently stalled without Meta escalation or Lift"
            )


class EvaluationAudit:
    def __init__(
        self,
        proposed=0,
        evaluated=0,
        duplicate_pruned=0,
        budget_pruned=0,
        already_seen_pruned=0,
    ):
        self.proposed = proposed
        self.evaluated = evaluated
        self.duplicate_pruned = duplicate_pruned
        self.budget_pruned = budget_pruned
        self.already_seen_pruned = already_seen_pruned


def assert_candidate_accounting(audit: EvaluationAudit):
    accounted = (
        audit.evaluated
        + audit.duplicate_pruned
        + audit.budget_pruned
        + audit.already_seen_pruned
    )
    if accounted != audit.proposed:
        raise RuntimeFailure(
            f"Search proposed {audit.proposed} candidates but only {accounted} were accounted for"
        )


class RunSummary:
    def __init__(
        self, final_phi: float, termination: str, lift_count: int, final_mss_level: int
    ):
        self.final_phi = final_phi
        self.termination = termination
        self.lift_count = lift_count
        self.final_mss_level = final_mss_level


def assert_search_endpoint_invariance(runs: list, tolerances: Tolerances):
    if not runs:
        return

    first = runs[0]
    for run in runs[1:]:
        diff = abs(run.final_phi - first.final_phi)
        scale = max(abs(run.final_phi), abs(first.final_phi), 1.0)
        approx_eq = diff <= tolerances.max_drift * scale

        if (
            not approx_eq
            or run.termination != first.termination
            or run.lift_count != first.lift_count
            or run.final_mss_level != first.final_mss_level
        ):
            raise RuntimeFailure("Search strategy affects ontology: contract violation")

