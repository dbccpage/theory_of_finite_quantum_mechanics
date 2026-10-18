"""FOC residual terminalizer: Phi1 / Gamma2 -> cohomological class + routing.

Owner of the Python trichotomy rail (gtla.md SVIII "Budget Honesty and
Witness Dominance"; Rust reference:
``omega_atlas_reconciliation::terminalize``; Lean reference:
``PaperER003`` ``domainPolicy`` after the 2026-07-28 repair).

Laws enforced here (Inspector finding OD-1, the SVIII falsifier):

* The trichotomy classifier :func:`classify_trichotomy` takes ``(phi1,
  gamma2)`` ONLY and is budget-free by construction — there is no budget
  parameter to test before the trichotomy.
* Witness dominance: at a fixed claim and scope, witnessed masses decide the
  cohomological class. ``Gamma2 > 0`` witnessed -> ``ActiveClosureFailure``
  whatever any flag says; ``(Phi1 > 0, Gamma2 = 0)`` -> ``ClosedSurvivor``;
  ``Phi1 = 0`` -> ``ExactRepair``. No meta flag (budget, no_rule, refused)
  can flip a witnessed cohomological classification; flags may only reroute
  the ROUTING axis or refuse.
* Budget exhaustion with witnessed masses NEVER yields ``BudgetUnknown``:
  classification completed, so the verdict classifies and the budget debt is
  recorded as a trace event (see ``omega_terminalizers.debt`` for the only
  legal ``BudgetUnknown`` constructor, gated on classification NOT having
  completed).

AuthorityEffect: None throughout.
"""

from __future__ import annotations
import re
from pydantic.dataclasses import dataclass
from fractions import Fraction
from typing import Any, Optional, Tuple, Union

from .termz_debt import DebtRecord
from .termz_refusals import TerminalizerRefusal

#: Exact-mass input domain. ``float`` is deliberately NOT a member: this is
#: the exact rail (FiniteCochainComplex discipline — "floating point is
#: forbidden"). The legacy alias ``Number`` is kept for importers but no
#: longer admits floats at runtime.
ExactMass = Union[int, str, Fraction]
Number = ExactMass

#: Scientific-notation exponent, matched at the end of a candidate mass
#: string (mirrors the ``E`` group of ``fractions._RATIONAL_FORMAT``).
_SCI_EXPONENT_RE = re.compile(r"[eE]\s*([+-]?\d+)\s*\Z")

#: Bound on ``abs(exponent)`` for a scientific-notation mass literal.
#: ``Fraction`` builds the numerator/denominator via ``10 ** abs(exponent)``
#: (a power, not a digit-string-to-int conversion), so Python's
#: ``sys.int_max_str_digits`` guard (default 4300) does NOT fire on this
#: path — ``Fraction("1e-2000000")`` parses in ~1s while materializing a
#: ~2,000,000-digit denominator. 10**4 gives ten thousand digits of
#: precision, comfortably beyond any exact mass literal that arises in this
#: domain, while keeping worst-case construction cost bounded and in the
#: same order of magnitude as the digit-literal guard's own ceiling.
_MAX_ABS_MASS_EXPONENT = 10**4


@dataclass(frozen=True)
class TerminalizerVerdict:
    """Four-axis-aligned verdict. ``extension`` is the ExtensionStatus axis
    (``None`` only for verdicts constructed outside the classifier)."""

    phi1: Fraction
    gamma2: Fraction
    cohomological: Any
    routing: Any
    extension: Any = None
    authority_effect: str = "None"
    trace_events: Tuple[str, ...] = ()


def _exact_mass(x: ExactMass, name: str) -> Fraction:
    """Exact-rail conversion of one witnessed mass.

    Law: masses are exact rationals. Accepted: ``int``, ``Fraction``, and
    strings parsed exactly by ``Fraction`` (e.g. ``"1/3"``). Refused with a
    typed :class:`TerminalizerRefusal`:

      * ``FLOAT_MASS_REFUSED`` — ``float``/``bool``: floating point is
        forbidden on the exact rail (a ``1e-30`` float must never round to
        zero mass; there is NO ``limit_denominator`` rounding here);
      * ``MASS_EXPONENT_OUT_OF_RANGE_REFUSED`` — a scientific-notation
        string whose exponent magnitude exceeds
        :data:`_MAX_ABS_MASS_EXPONENT`; refused BEFORE calling
        ``Fraction()``, which would otherwise materialize an
        astronomically large numerator/denominator (e.g.
        ``Fraction("1e-2000000")`` parses in ~1s and builds a
        ~2,000,000-digit denominator — a resource-exhaustion vector
        Python's ``sys.int_max_str_digits`` does not guard);
      * ``MASS_PARSE_REFUSED`` — string that ``Fraction`` cannot parse;
      * ``MASS_TYPE_REFUSED`` — any other type;
      * ``NEGATIVE_MASS_REFUSED`` — negative value (Phi1/Gamma2 are norms).
    """
    if isinstance(x, bool) or isinstance(x, float):
        raise TerminalizerRefusal(
            "FLOAT_MASS_REFUSED",
            f"{name}: use integers, strings, or Fraction; floating point is "
            f"forbidden on the exact rail (got {x!r})",
        )
    if isinstance(x, Fraction):
        value = x
    elif isinstance(x, int):
        value = Fraction(x)
    elif isinstance(x, str):
        exponent_match = _SCI_EXPONENT_RE.search(x)
        if exponent_match is not None and (
            abs(int(exponent_match.group(1))) > _MAX_ABS_MASS_EXPONENT
        ):
            raise TerminalizerRefusal(
                "MASS_EXPONENT_OUT_OF_RANGE_REFUSED",
                f"{name}: scientific-notation exponent magnitude must be "
                f"<= {_MAX_ABS_MASS_EXPONENT} (got "
                f"{exponent_match.group(1)} in {x!r}); refusing before "
                f"Fraction() would materialize an astronomically large "
                f"numerator/denominator",
            )
        try:
            value = Fraction(x)
        except (ValueError, ZeroDivisionError) as exc:
            raise TerminalizerRefusal(
                "MASS_PARSE_REFUSED",
                f"{name}: {x!r} is not an exact rational literal",
            ) from exc
    else:
        raise TerminalizerRefusal(
            "MASS_TYPE_REFUSED",
            f"{name}: use integers, strings, or Fraction (got {type(x).__name__})",
        )
    if value < 0:
        raise TerminalizerRefusal(
            "NEGATIVE_MASS_REFUSED",
            f"{name}: witnessed masses are norms and must be nonnegative (got {value})",
        )
    return value


def classify_trichotomy(phi1: ExactMass, gamma2: ExactMass) -> Any:
    """Budget-free trichotomy core. Takes ``(phi1, gamma2)`` ONLY.

    Mirrors the Rust rail ``omega_atlas_reconciliation::terminalize``
    (``Phi=0 -> ExactRepair | Gamma=0 -> StabilizedSurvivor | else ->
    OpenObstruction``): total and mutually exclusive over witnessed
    consistent nonnegative masses. By construction no budget, licensing, or
    routing flag can reach this function.

    Well-formedness (Inspector OD-3/M4): ``Gamma2`` is the norm of a
    boundary of the same cochain, so ``Gamma2 > 0 => Phi1 > 0``. A witness
    pair ``(0, gamma>0)`` is inconsistent and refuses with token
    ``INCONSISTENT_WITNESS`` — it must never classify as ``ExactRepair``.
    Input refusals are inherited from :func:`_exact_mass` (exact rail; no
    floats, no rounding, no negatives). AuthorityEffect: None.
    """
    from omega_engine.crates.type.runtime_axes import CohomologicalStatus

    p = _exact_mass(phi1, "phi1")
    g = _exact_mass(gamma2, "gamma2")
    if p == 0 and g > 0:
        raise TerminalizerRefusal(
            "INCONSISTENT_WITNESS",
            f"Gamma2 > 0 implies Phi1 > 0 (Gamma2 is a norm of a boundary of "
            f"the same cochain); got (phi1=0, gamma2={g}). Refusing to emit "
            f"ExactRepair over an inconsistent witness.",
        )
    if p == 0:
        return CohomologicalStatus.ExactRepair
    if g == 0:
        return CohomologicalStatus.ClosedSurvivor
    return CohomologicalStatus.ActiveClosureFailure


def classify_phi_gamma(
    phi1: Number,
    gamma2: Number,
    *,
    licensed_lift_certificate: bool = False,
    budget_exhausted: bool = False,
    no_rule: bool = False,
    refused: bool = False,
    debt: Optional[DebtRecord] = None,
) -> TerminalizerVerdict:
    """Exact rational classification with witness dominance.

    Cohomological trichotomy (budget-free; computed FIRST, before any meta
    flag is consulted):

      Phi1 = 0             -> ExactRepair
      Phi1 > 0, Gamma2 = 0 -> ClosedSurvivor (StabilizedSurvivor)
      Phi1 > 0, Gamma2 > 0 -> ActiveClosureFailure (OpenObstruction)

    Default routing per gtla.md SVIII front table: ExactRepair ->
    ``CheckPassed``; ClosedSurvivor -> ``RequiresLift``;
    ActiveClosureFailure -> ``Repair``.

    Lift-licensing gate (Inspector OD-2/M14; gtla.md SIII.6.5 Minimal Lift
    Firewall, GTLA-T53): ``licensed_lift_certificate`` is load-bearing on
    the EXTENSION axis of the verdict — the paper's front table pins the
    survivor's ROUTING axis to ``RequiresLift``, so the license
    distinction lives where the registry puts it, on ``ExtensionStatus``:

      * ClosedSurvivor, unlicensed  -> ``extension=ExtensionRequested``
        (lift outstanding; II.5.1: 'LiftRequired requires a concrete
        witness and lift contract' — onward use stays blocked);
      * ClosedSurvivor, licensed    -> ``extension=LicensedLift`` (the
        T53 gate passed; the lift contract may proceed);
      * ActiveClosureFailure, licensed -> ``extension=LicensedLift``
        (coherent: T53 licenses lifts exactly over OPEN obstructions in
        T53's own registry-exhaustion sense, ``LiftLicensed(omega) <=>
        Open_n(w)`` — NOT a claim about the ``OpenObstruction`` /
        ``ActiveClosureFailure`` DiagnosticClass routing token used
        elsewhere in this module; the two happen to agree on this branch
        because ``coh == ActiveClosureFailure`` is exactly the witnessed
        case ``Open_n(w)`` names here), routing stays ``Repair``;
      * ActiveClosureFailure, unlicensed -> ``extension=NoExtensionNeeded``
        (repair at the current level);
      * ExactRepair, licensed -> typed refusal
        ``LIFT_LICENSE_WITHOUT_OPEN_OBSTRUCTION``: GTLA-T53 defines
        ``LiftLicensed(omega) <=> Open_n(w)``; with ``Phi1 = 0`` the
        residual is resolved, no open obstruction exists, and the license
        claim is incoherent — never silently ignored.

    Meta flags override the ROUTING axis only — never the witnessed
    cohomological axis (witness dominance). Priority when several are set:
    ``refused`` > ``no_rule``.

    ``budget_exhausted`` (DEPRECATED, kept for callers of the pre-OD-1
    surface): this flag previously replaced the whole verdict with
    ``BudgetUnknown`` — the exact SVIII falsifier. It now emits the
    corrected dominance behavior: witnessed masses were passed, so the
    verdict classifies exactly as if the flag were absent, and the budget
    debt is recorded on ``trace_events`` — never as a terminal replacement.
    The flag REQUIRES a valid two-ground
    :class:`omega_terminalizers.debt.DebtRecord` via ``debt=``; use
    ``omega_terminalizers.debt.emit_budget_unknown`` instead when
    classification genuinely did not complete.

    Typed refusals (:class:`TerminalizerRefusal`):
      * ``BUDGET_FLAG_WITHOUT_DEBT_RECORD`` — ``budget_exhausted=True``
        without a valid ``DebtRecord`` in ``debt=``;
      * ``INCONSISTENT_WITNESS`` — ``(phi1=0, gamma2>0)``: Gamma2 is a norm
        of a boundary of the same cochain, so ``Gamma2>0 => Phi1>0``; this
        pair must never classify as ``ExactRepair`` (OD-3/M4);
      * ``FLOAT_MASS_REFUSED`` / ``MASS_PARSE_REFUSED`` /
        ``MASS_TYPE_REFUSED`` / ``NEGATIVE_MASS_REFUSED`` — exact-rail
        input discipline (see :func:`_exact_mass`; floats are forbidden and
        there is no rounding, so ``1e-30`` can never classify as zero mass;
        negative masses were previously answered with a Refusal verdict and
        now refuse in type).

    AuthorityEffect: None.
    """
    from omega_engine.crates.type.runtime_axes import (
        CohomologicalStatus,
        ExtensionStatus,
        RoutingTerminal,
    )

    p = _exact_mass(phi1, "phi1")
    g = _exact_mass(gamma2, "gamma2")

    # Witness dominance: the trichotomy is decided FIRST, from the witnessed
    # masses only. No flag consulted before this line.
    coh = classify_trichotomy(p, g)

    trace_events: Tuple[str, ...] = ()
    if budget_exhausted:
        if not isinstance(debt, DebtRecord):
            raise TerminalizerRefusal(
                "BUDGET_FLAG_WITHOUT_DEBT_RECORD",
                "budget_exhausted=True requires a valid two-ground DebtRecord "
                "(debt=...); a bare budget flag can no longer downgrade a "
                "witnessed classification to BudgetUnknown (gtla.md SVIII). "
                "If classification did not complete, use "
                "omega_terminalizers.debt.emit_budget_unknown instead.",
            )
        # Budget exhaustion may stop further search; it may not retire a
        # witness already found. Record the debt; classify by dominance.
        trace_events = trace_events + (debt.as_trace_event(),)
    elif debt is not None:
        if not isinstance(debt, DebtRecord):
            raise TerminalizerRefusal(
                "DEBT_RECORD_REQUIRED",
                f"debt= must be a DebtRecord (got {type(debt).__name__})",
            )
        trace_events = trace_events + (debt.as_trace_event(),)

    # Lift-licensing gate on the extension axis (GTLA-T53; see docstring).
    if coh == CohomologicalStatus.ExactRepair:
        if licensed_lift_certificate:
            raise TerminalizerRefusal(
                "LIFT_LICENSE_WITHOUT_OPEN_OBSTRUCTION",
                "GTLA-T53: LiftLicensed(omega) <=> Open_n(w); Phi1 = 0 means "
                "the residual is resolved, so no open obstruction exists to "
                "license a lift over",
            )
        extension = ExtensionStatus.NoExtensionNeeded
    elif coh == CohomologicalStatus.ClosedSurvivor:
        extension = (
            ExtensionStatus.LicensedLift
            if licensed_lift_certificate
            else ExtensionStatus.ExtensionRequested
        )
    else:
        extension = (
            ExtensionStatus.LicensedLift
            if licensed_lift_certificate
            else ExtensionStatus.NoExtensionNeeded
        )

    # Default routing from the witnessed class (SVIII front table).
    if coh == CohomologicalStatus.ExactRepair:
        routing = RoutingTerminal.CheckPassed
    elif coh == CohomologicalStatus.ClosedSurvivor:
        routing = RoutingTerminal.RequiresLift
    else:
        routing = RoutingTerminal.Repair

    # Meta flags: routing-axis overrides only (never the cohomological axis).
    if refused:
        routing = RoutingTerminal.Refusal
    elif no_rule:
        routing = RoutingTerminal.NoRule

    return TerminalizerVerdict(
        phi1=p,
        gamma2=g,
        cohomological=coh,
        routing=routing,
        extension=extension,
        trace_events=trace_events,
    )



