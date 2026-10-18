"""Two-ground debt records and the legality gate for the ``BudgetUnknown`` terminal.

Owner surface for gtla.md SVIII "Budget Honesty and Witness Dominance"
(Inspector finding OD-4/M2). ``BudgetUnknown`` is a **resource** terminal on
the RoutingTerminal axis; it is not an obstruction class. Its legality law:

    It may be emitted only when classification did not complete at the
    declared claim and scope, on exactly one of two grounds:
      (a) exhaustion of a *precommitted* budget; or
      (b) an undischarged *exhaustiveness / cofinality* obligation on a
          declared search family (the canonical CODA-A use, coda_a.md
          SS2.5/SS11.6).
    In both cases the terminal carries a **debt record**: what was not
    evaluated, under which committed budget or which unproven obligation,
    and what re-run would resolve it.

Witness dominance (same section): if witnessed Phi1/Gamma2 masses exist, the
classification COMPLETED and the trichotomy classifier decides — budget can
never retire a witness. That case is refused here and belongs to
``omega_terminalizers.classify_phi_gamma``.

AuthorityEffect: None throughout.
"""

from __future__ import annotations
from pydantic.dataclasses import dataclass
from typing import Any, Optional, Tuple

from .termz_refusals import TerminalizerRefusal

DEBT_GROUND_PRECOMMITTED_BUDGET = "precommitted_budget_exhausted"
DEBT_GROUND_COFINALITY = "undischarged_cofinality_obligation"

DEBT_GROUNDS: Tuple[str, str] = (
    DEBT_GROUND_PRECOMMITTED_BUDGET,
    DEBT_GROUND_COFINALITY,
)


@dataclass(frozen=True)
class DebtRecord:
    """Debt record carried by a legal ``BudgetUnknown`` terminal.

    Law (gtla.md SVIII): the record must say what was not evaluated
    (``stopped_family``), under which committed budget or which unproven
    obligation (``bound_or_obligation``), and what re-run would resolve it
    (``resume_condition``). ``ground`` must be exactly one member of
    :data:`DEBT_GROUNDS`.

    Typed refusals (all :class:`TerminalizerRefusal`):
      * ``DEBT_GROUND_INVALID`` — ground not exactly one of the two grounds;
      * ``DEBT_FIELD_EMPTY`` — any required field missing/blank/non-string;
      * ``DEBT_AUTHORITY_WIDENING_REFUSED`` — authority_effect != "None".

    Budget changes are trace events, never retroactive excuses: a
    ``DebtRecord`` records the committed bound, it does not amend it.
    AuthorityEffect: None.
    """

    ground: str
    stopped_family: str
    bound_or_obligation: str
    resume_condition: str
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        if self.ground not in DEBT_GROUNDS:
            raise TerminalizerRefusal(
                "DEBT_GROUND_INVALID",
                f"ground must be exactly one of {DEBT_GROUNDS}, got {self.ground!r}",
            )
        for field_name in ("stopped_family", "bound_or_obligation", "resume_condition"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise TerminalizerRefusal(
                    "DEBT_FIELD_EMPTY",
                    f"{field_name} must be a non-empty string "
                    f"(the debt must be replayable), got {value!r}",
                )
        if self.authority_effect != "None":
            raise TerminalizerRefusal(
                "DEBT_AUTHORITY_WIDENING_REFUSED",
                "a debt record carries AuthorityEffect None only",
            )

    def as_trace_event(self) -> str:
        """Render the debt as a single deterministic trace-event string."""
        return (
            f"debt[{self.ground}]: stopped_family={self.stopped_family}; "
            f"bound_or_obligation={self.bound_or_obligation}; "
            f"resume_condition={self.resume_condition}"
        )


@dataclass(frozen=True)
class BudgetUnknownTerminal:
    """The legal ``BudgetUnknown`` terminal (routing axis) with its debt.

    ``diagnostic`` is ``DiagnosticClass.NotComputed`` by construction:
    classification did not complete, so no obstruction class exists. This
    type never carries a witnessed trichotomy class — that would violate
    witness dominance. AuthorityEffect: None.

    ``__post_init__`` closes the DIRECT-construction bypass (the sole
    intended constructor is :func:`emit_budget_unknown`, but a dataclass's
    fields remain publicly settable): ``debt`` must be a real
    :class:`DebtRecord` — a legal ``BudgetUnknown`` always carries a
    replayable debt, never a bare string or dict — and ``authority_effect``
    must be exactly ``'None'``. Both laws are already enforced by
    :func:`emit_budget_unknown` before it builds this record; the checks
    here are defense in depth against constructing the dataclass directly.
    """

    debt: DebtRecord
    diagnostic: Any
    routing: Any
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        if not isinstance(self.debt, DebtRecord):
            raise TerminalizerRefusal(
                "DEBT_RECORD_REQUIRED",
                "BudgetUnknownTerminal.debt must be a DebtRecord (got "
                f"{type(self.debt).__name__}); direct construction with a "
                "forged or malformed debt is refused — use "
                "emit_budget_unknown()",
            )
        if self.authority_effect != "None":
            raise TerminalizerRefusal(
                "DEBT_AUTHORITY_WIDENING_REFUSED",
                "BudgetUnknownTerminal carries AuthorityEffect None only "
                f"(got {self.authority_effect!r})",
            )


def emit_budget_unknown(
    debt: DebtRecord,
    *,
    witnessed_phi1: Optional[Any] = None,
    witnessed_gamma2: Optional[Any] = None,
) -> BudgetUnknownTerminal:
    """Sole constructor for a legal ``BudgetUnknown`` terminal.

    Law (gtla.md SVIII legality table, row 4): ``BudgetUnknown`` is legal
    ONLY when classification did not complete — no witnessed Phi1/Gamma2 —
    AND a valid :class:`DebtRecord` with exactly one ground is supplied.

    Typed refusals (:class:`TerminalizerRefusal`):
      * ``WITNESS_DOMINANCE_REFUSAL`` — witnessed masses were supplied;
        classification completed (or must run). Budget exhaustion may stop
        further search; it may not retire a witness already found. Route
        the witnessed masses through ``classify_phi_gamma`` and attach the
        debt as a trace event there.
      * ``DEBT_RECORD_REQUIRED`` — ``debt`` is not a ``DebtRecord``.

    AuthorityEffect: None.
    """
    if witnessed_phi1 is not None or witnessed_gamma2 is not None:
        raise TerminalizerRefusal(
            "WITNESS_DOMINANCE_REFUSAL",
            "witnessed Phi1/Gamma2 were supplied, so classification completed "
            "at this claim and scope; BudgetUnknown may not replace a witnessed "
            "classification (SVIII falsifier). Use classify_phi_gamma and "
            "attach the DebtRecord as a trace event.",
        )
    if not isinstance(debt, DebtRecord):
        raise TerminalizerRefusal(
            "DEBT_RECORD_REQUIRED",
            "BudgetUnknown is legal only with a valid two-ground DebtRecord "
            f"(got {type(debt).__name__})",
        )
    from omega_engine.crates.type.runtime_axes import (
        DiagnosticClass,
        RoutingTerminal,
    )

    return BudgetUnknownTerminal(
        debt=debt,
        diagnostic=DiagnosticClass.NotComputed,
        routing=RoutingTerminal.BudgetUnknown,
    )


__all__ = [
    "DEBT_GROUNDS",
    "DEBT_GROUND_PRECOMMITTED_BUDGET",
    "DEBT_GROUND_COFINALITY",
    "DebtRecord",
    "BudgetUnknownTerminal",
    "emit_budget_unknown",
]



