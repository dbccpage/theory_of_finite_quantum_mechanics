from __future__ import annotations
"""M2 — Two-ground BudgetUnknown legality + DebtRecord refusal battery (SVIII; OD-4).

THEORETICAL MINIMUM
  INVARIANT  BudgetUnknown is constructible ONLY via emit_budget_unknown with
             a valid two-ground DebtRecord and NO witnessed masses; the debt
             record itself refuses malformed grounds/fields/authority.
  BREAK      A bare flag or ad-hoc dict mints a BudgetUnknown; a witnessed
             mass is retired by budget; a third ground slips in.
  WITNESS    TerminalizerRefusal.token per arm, each arm its own distinct
             token (negative-control matrix, Landau class 2).
  MUTATION   Delete the witnessed-mass gate in debt.emit_budget_unknown ->
             the WITNESS_DOMINANCE_REFUSAL rows go red.

AuthorityEffect: None throughout.
"""


import pytest

from omega_engine.crates.type.runtime_axes import DiagnosticClass, RoutingTerminal
from omega_engine.crates.type.terminalizers import (
    DEBT_GROUND_COFINALITY,
    DEBT_GROUND_PRECOMMITTED_BUDGET,
    DEBT_GROUNDS,
    BudgetUnknownTerminal,
    DebtRecord,
    TerminalizerRefusal,
    emit_budget_unknown,
)


def _valid_debt(ground: str = DEBT_GROUND_PRECOMMITTED_BUDGET) -> DebtRecord:
    return DebtRecord(
        ground=ground,
        stopped_family="declared_shadow_family",
        bound_or_obligation="budget=8 committed pre-run",
        resume_condition="rerun with budget >= 9",
    )


class TestGroundRegistry:
    def test_registry_is_exactly_the_two_grounds(self) -> None:
        assert DEBT_GROUNDS == (
            DEBT_GROUND_PRECOMMITTED_BUDGET,
            DEBT_GROUND_COFINALITY,
        )

    @pytest.mark.parametrize("ground", list(DEBT_GROUNDS))
    def test_both_grounds_construct_a_legal_budget_unknown(self, ground: str) -> None:
        debt = _valid_debt(ground)
        terminal = emit_budget_unknown(debt)
        assert isinstance(terminal, BudgetUnknownTerminal)
        assert terminal.debt is debt
        assert terminal.diagnostic is DiagnosticClass.NotComputed
        assert terminal.routing is RoutingTerminal.BudgetUnknown
        assert terminal.authority_effect == "None"


class TestDebtRecordRefusalMatrix:
    """Each arm fails for its own distinct token."""

    def test_third_ground_refused(self) -> None:
        with pytest.raises(TerminalizerRefusal, match="DEBT_GROUND_INVALID") as excinfo:
            DebtRecord(
                ground="ran_out_of_patience",
                stopped_family="f",
                bound_or_obligation="b",
                resume_condition="r",
            )
        assert excinfo.value.token == "DEBT_GROUND_INVALID"

    @pytest.mark.parametrize(
        "field_name", ["stopped_family", "bound_or_obligation", "resume_condition"]
    )
    @pytest.mark.parametrize("bad_value", ["", "   ", None, 7])
    def test_empty_or_nonstring_required_field_refused(
        self, field_name: str, bad_value
    ) -> None:
        kwargs = {
            "ground": DEBT_GROUND_COFINALITY,
            "stopped_family": "f",
            "bound_or_obligation": "b",
            "resume_condition": "r",
        }
        kwargs[field_name] = bad_value
        with pytest.raises(TerminalizerRefusal, match="DEBT_FIELD_EMPTY") as excinfo:
            DebtRecord(**kwargs)
        assert excinfo.value.token == "DEBT_FIELD_EMPTY"

    def test_authority_widening_refused(self) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="DEBT_AUTHORITY_WIDENING_REFUSED"
        ) as excinfo:
            DebtRecord(
                ground=DEBT_GROUND_PRECOMMITTED_BUDGET,
                stopped_family="f",
                bound_or_obligation="b",
                resume_condition="r",
                authority_effect="LocalGreen",
            )
        assert excinfo.value.token == "DEBT_AUTHORITY_WIDENING_REFUSED"

    def test_as_trace_event_is_deterministic_and_replayable(self) -> None:
        event = _valid_debt().as_trace_event()
        assert event == (
            "debt[precommitted_budget_exhausted]: "
            "stopped_family=declared_shadow_family; "
            "bound_or_obligation=budget=8 committed pre-run; "
            "resume_condition=rerun with budget >= 9"
        )


class TestEmitBudgetUnknownLegalityGate:
    @pytest.mark.parametrize(
        ("witnessed_phi1", "witnessed_gamma2"),
        [(1, None), (None, 1), (1, 1), (0, None), (None, 0), (0, 0)],
    )
    def test_any_witnessed_mass_refuses_even_zero(
        self, witnessed_phi1, witnessed_gamma2
    ) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="WITNESS_DOMINANCE_REFUSAL"
        ) as excinfo:
            emit_budget_unknown(
                _valid_debt(),
                witnessed_phi1=witnessed_phi1,
                witnessed_gamma2=witnessed_gamma2,
            )
        assert excinfo.value.token == "WITNESS_DOMINANCE_REFUSAL"

    @pytest.mark.parametrize("bad_debt", [None, "debt", {"ground": "x"}, 3])
    def test_non_debt_record_refused(self, bad_debt) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="DEBT_RECORD_REQUIRED"
        ) as excinfo:
            emit_budget_unknown(bad_debt)
        assert excinfo.value.token == "DEBT_RECORD_REQUIRED"


class TestBudgetUnknownTerminalDirectConstructionBypass:
    """P2 repair: BudgetUnknownTerminal(...) had no __post_init__, so a bare
    dataclass call bypassed emit_budget_unknown()'s legality gate entirely.
    ``BudgetUnknownTerminal(debt="garbage", diagnostic="X", routing="Y")``
    used to construct without complaint.
    """

    def test_garbage_debt_direct_construction_refused(self) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="DEBT_RECORD_REQUIRED"
        ) as excinfo:
            BudgetUnknownTerminal(debt="garbage", diagnostic="X", routing="Y")
        assert excinfo.value.token == "DEBT_RECORD_REQUIRED"

    @pytest.mark.parametrize(
        "bad_debt", [None, {"ground": "x"}, 3, ["not", "a", "record"]]
    )
    def test_other_non_debt_record_types_direct_construction_refused(
        self, bad_debt
    ) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="DEBT_RECORD_REQUIRED"
        ) as excinfo:
            BudgetUnknownTerminal(debt=bad_debt, diagnostic="X", routing="Y")
        assert excinfo.value.token == "DEBT_RECORD_REQUIRED"

    def test_authority_widening_direct_construction_refused(self) -> None:
        with pytest.raises(
            TerminalizerRefusal, match="DEBT_AUTHORITY_WIDENING_REFUSED"
        ) as excinfo:
            BudgetUnknownTerminal(
                debt=_valid_debt(),
                diagnostic="X",
                routing="Y",
                authority_effect="LocalGreen",
            )
        assert excinfo.value.token == "DEBT_AUTHORITY_WIDENING_REFUSED"

    def test_legitimate_construction_via_emit_budget_unknown_still_works(self) -> None:
        terminal = emit_budget_unknown(_valid_debt())
        assert isinstance(terminal, BudgetUnknownTerminal)
        assert terminal.authority_effect == "None"

    def test_direct_construction_with_a_real_debt_record_still_works(self) -> None:
        terminal = BudgetUnknownTerminal(
            debt=_valid_debt(),
            diagnostic=DiagnosticClass.NotComputed,
            routing=RoutingTerminal.BudgetUnknown,
        )
        assert terminal.debt.ground == DEBT_GROUND_PRECOMMITTED_BUDGET


