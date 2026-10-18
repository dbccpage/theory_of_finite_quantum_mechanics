from __future__ import annotations
"""M1 — Witness dominance + budget-free trichotomy (gtla.md SVIII; Inspector OD-1).

THEORETICAL MINIMUM
  INVARIANT  Witnessed (Phi1, Gamma2) masses alone decide the cohomological
             class; a budget flag can never replace or reroute a witnessed
             classification to BudgetUnknown (SVIII witness dominance).
  BREAK      The pre-repair OD-1 behavior: budget tested on the boundary
             BEFORE the trichotomy, so (1,1,budget) -> BudgetUnknown with
             Gamma2 > 0 witnessed (the SVIII falsifier verbatim).
  WITNESS    verdict.cohomological / verdict.routing on every (phi,gamma)
             cell with budget_exhausted=True + a valid DebtRecord.
  MUTATION   In foc_terminalizer.classify_phi_gamma, consult budget_exhausted
             before classify_trichotomy and return a BudgetUnknown-routed
             verdict -> every dominance row here goes red.

AuthorityEffect: None throughout.
"""


import inspect

import pytest

from omega_engine.crates.type.runtime_axes import (
    CohomologicalStatus,
    RoutingTerminal,
)
from omega_engine.crates.type.terminalizers import (
    DEBT_GROUND_PRECOMMITTED_BUDGET,
    DebtRecord,
    TerminalizerRefusal,
    classify_phi_gamma,
)
from omega_engine.crates.type.terminalizers.termz_finite_obstruction_calculus import classify_trichotomy


def _debt() -> DebtRecord:
    return DebtRecord(
        ground=DEBT_GROUND_PRECOMMITTED_BUDGET,
        stopped_family="shadow_family_rabbit",
        bound_or_obligation="budget=12 shadow evaluations committed pre-run",
        resume_condition="rerun with budget >= 13 shadow evaluations",
    )


class TestWitnessDominanceHeadline:
    """The SVIII falsifier cells, one by one (Landau class 2)."""

    def test_gamma_positive_with_budget_is_active_closure_failure_never_budget_unknown(
        self,
    ) -> None:
        verdict = classify_phi_gamma(1, 1, budget_exhausted=True, debt=_debt())
        assert verdict.cohomological is CohomologicalStatus.ActiveClosureFailure
        assert verdict.routing is RoutingTerminal.Repair
        assert verdict.routing is not RoutingTerminal.BudgetUnknown

    def test_closed_survivor_with_budget_is_preserved(self) -> None:
        verdict = classify_phi_gamma(2, 0, budget_exhausted=True, debt=_debt())
        assert verdict.cohomological is CohomologicalStatus.ClosedSurvivor
        assert verdict.routing is RoutingTerminal.RequiresLift
        assert verdict.routing is not RoutingTerminal.BudgetUnknown

    def test_exact_repair_with_budget_stays_exact_repair_check_passed(self) -> None:
        verdict = classify_phi_gamma(0, 0, budget_exhausted=True, debt=_debt())
        assert verdict.cohomological is CohomologicalStatus.ExactRepair
        assert verdict.routing is RoutingTerminal.CheckPassed
        assert verdict.routing is not RoutingTerminal.BudgetUnknown


class TestBudgetFlagIsInertOnBothAxes:
    """Full matrix: budget flag changes NEITHER axis on any witnessed cell."""

    @pytest.mark.parametrize(
        ("phi1", "gamma2", "expected_coh", "expected_routing"),
        [
            (0, 0, CohomologicalStatus.ExactRepair, RoutingTerminal.CheckPassed),
            (1, 0, CohomologicalStatus.ClosedSurvivor, RoutingTerminal.RequiresLift),
            (
                "1/3",
                0,
                CohomologicalStatus.ClosedSurvivor,
                RoutingTerminal.RequiresLift,
            ),
            (1, 1, CohomologicalStatus.ActiveClosureFailure, RoutingTerminal.Repair),
            (
                "2/7",
                "1/9",
                CohomologicalStatus.ActiveClosureFailure,
                RoutingTerminal.Repair,
            ),
        ],
    )
    def test_budget_flag_never_changes_either_witnessed_axis(
        self, phi1, gamma2, expected_coh, expected_routing
    ) -> None:
        free = classify_phi_gamma(phi1, gamma2)
        flagged = classify_phi_gamma(phi1, gamma2, budget_exhausted=True, debt=_debt())
        assert free.cohomological is expected_coh
        assert flagged.cohomological is expected_coh
        assert free.routing is expected_routing
        assert flagged.routing is expected_routing
        assert classify_trichotomy(phi1, gamma2) is expected_coh

    def test_budget_debt_is_recorded_as_trace_event_not_terminal(self) -> None:
        debt = _debt()
        verdict = classify_phi_gamma(1, 1, budget_exhausted=True, debt=debt)
        assert verdict.trace_events == (debt.as_trace_event(),)
        assert verdict.cohomological is CohomologicalStatus.ActiveClosureFailure

    def test_budget_flag_without_debt_record_refuses_typed(self) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="BUDGET_FLAG_WITHOUT_DEBT_RECORD"
        ) as excinfo:
            classify_phi_gamma(1, 1, budget_exhausted=True)
        assert excinfo.value.token == "BUDGET_FLAG_WITHOUT_DEBT_RECORD"

    def test_debt_kwarg_of_wrong_type_refuses_typed(self) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="DEBT_RECORD_REQUIRED"
        ) as excinfo:
            classify_phi_gamma(1, 0, debt="not a debt record")
        assert excinfo.value.token == "DEBT_RECORD_REQUIRED"


class TestTrichotomyIsBudgetFreeByConstruction:
    def test_classify_trichotomy_signature_admits_masses_only(self) -> None:
        params = list(inspect.signature(classify_trichotomy).parameters)
        assert params == ["phi1", "gamma2"]

    def test_verdict_authority_effect_is_none_on_every_cell(self) -> None:
        for phi1, gamma2 in [(0, 0), (1, 0), (1, 1)]:
            verdict = classify_phi_gamma(
                phi1, gamma2, budget_exhausted=True, debt=_debt()
            )
            assert verdict.authority_effect == "None"


