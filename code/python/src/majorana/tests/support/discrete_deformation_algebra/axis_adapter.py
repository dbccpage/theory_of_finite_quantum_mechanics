"""ADAPT-01 owner: total, axis-typed adapter from paper terminal spellings
onto the live four-axis registry enums (Inspector finding OD-5/M3).

The GTLA paper family spells some terminals in layer vocabulary while the
runtime owns registry tokens (``types.py``). The declared alias table
(gtla/docs/support/coda_authority_boundary_matrix.yaml, ADAPT-01/ADAPT-02)
is mechanized here as a TOTAL mapping:

* ``LiftRequired``  <-> ``RoutingTerminal.RequiresLift``
* ``Refused``       <-> ``RoutingTerminal.Refusal``
* ``RefusedClosure`` -> ``RoutingTerminal.Refusal`` (closure-scoped)
* ``Survivor`` / ``StabilizedSurvivor`` <-> trichotomy
  ``CohomologicalStatus.ClosedSurvivor``; ``Survivor`` also reads
  ``DiagnosticClass.ClosedResidual`` on the diagnostic axis
* ``Open`` / ``OpenResidual`` / ``OpenObstruction`` <-> the
  ``ActiveClosureFailure`` reading on BOTH the diagnostic axis and the
  trichotomy axis
* ``Exact`` -> ``DiagnosticClass.ExactClass`` (diagnostic axis) /
  ``CohomologicalStatus.ExactRepair`` (trichotomy axis) — axis named,
  never guessed

Laws:

* **Axis-typed lookup.** ``resolve_alias(token, axis)`` returns a member of
  ``axis`` or raises a typed :class:`AliasAdapterRefusal`. Asking one axis
  for another axis's token (e.g. asking ``DiagnosticClass`` for
  ``"RequiresLift"``) refuses with ``AXIS_MISMATCH_REFUSED`` — the adapter
  NEVER coerces across axes.
* **Fail-closed totality.** A token outside the declared table refuses with
  ``UNKNOWN_TERMINAL_TOKEN_REFUSED``; there is no default row.
* The table is exported (:func:`alias_table`) so tests can check totality
  over the paper's alias declarations without re-deriving it.

No new enums are introduced: every target is a member of the live token
sets in ``omega_discrete_deformation_algebra.types``.

AuthorityEffect: None — mapping a spelling never changes a terminal's
meaning, promotes a terminal, or mints authority.
"""

from __future__ import annotations
import enum
from typing import Dict, Mapping, Tuple, Type

from omega_engine.crates.type.runtime_axes import (
    CohomologicalStatus,
    DiagnosticClass,
    ExtensionStatus,
    RoutingTerminal,
)


class AliasAdapterRefusal(ValueError):
    """Typed refusal raised by the ADAPT-01 adapter.

    Attributes:
        token: machine-readable refusal token (stable; tests bind to it).
    """

    def __init__(self, token: str, detail: str = "") -> None:
        self.token = token
        super().__init__(f"{token}: {detail}" if detail else token)


#: The four supported target axes (live registry enums; no duplicates).
SUPPORTED_AXES: Tuple[Type[enum.Enum], ...] = (
    DiagnosticClass,
    RoutingTerminal,
    ExtensionStatus,
    CohomologicalStatus,
)

# Declared alias rows per axis (paper spelling -> registry member). Native
# registry spellings resolve as identity rows and are NOT repeated here.
_ALIAS_ROWS: Dict[Type[enum.Enum], Dict[str, enum.Enum]] = {
    RoutingTerminal: {
        "LiftRequired": RoutingTerminal.RequiresLift,
        "Refused": RoutingTerminal.Refusal,
        "RefusedClosure": RoutingTerminal.Refusal,
    },
    DiagnosticClass: {
        "Exact": DiagnosticClass.ExactClass,
        "Open": DiagnosticClass.ActiveClosureFailure,
        "OpenResidual": DiagnosticClass.ActiveClosureFailure,
        "OpenObstruction": DiagnosticClass.ActiveClosureFailure,
        "Survivor": DiagnosticClass.ClosedResidual,
    },
    CohomologicalStatus: {
        "Exact": CohomologicalStatus.ExactRepair,
        "StabilizedSurvivor": CohomologicalStatus.ClosedSurvivor,
        "Survivor": CohomologicalStatus.ClosedSurvivor,
        "Open": CohomologicalStatus.ActiveClosureFailure,
        "OpenResidual": CohomologicalStatus.ActiveClosureFailure,
        "OpenObstruction": CohomologicalStatus.ActiveClosureFailure,
    },
    ExtensionStatus: {},  # identity-only: the paper uses registry spellings
}


def _axis_tokens(axis: Type[enum.Enum]) -> Dict[str, enum.Enum]:
    """Full closed lookup for one axis: identity rows + declared aliases."""
    table: Dict[str, enum.Enum] = {member.value: member for member in axis}
    table.update(_ALIAS_ROWS[axis])
    return table


def known_axes_for(token: str) -> Tuple[str, ...]:
    """Names of every supported axis on which ``token`` resolves (may be
    empty). Diagnostic helper for messages and tests; performs no coercion."""
    return tuple(
        axis.__name__ for axis in SUPPORTED_AXES if token in _axis_tokens(axis)
    )


def resolve_alias(token: str, axis: Type[enum.Enum]) -> enum.Enum:
    """Resolve one paper/registry spelling on ONE named axis.

    Law: returns a member of ``axis`` for tokens in the closed table
    (identity rows plus the declared aliases above); everything else is a
    typed refusal — never a coercion, never a default.

    Typed refusals (:class:`AliasAdapterRefusal`):
      * ``UNSUPPORTED_AXIS_REFUSED`` — ``axis`` not one of the four
        registry axes;
      * ``NON_STRING_TOKEN_REFUSED`` — ``token`` is not a string
        (str-valued registry enum members ARE their spelling and pass
        through the same closed table; anything else refuses);
      * ``AXIS_MISMATCH_REFUSED`` — the token is a declared token of a
        DIFFERENT axis (e.g. asking DiagnosticClass for ``"RequiresLift"``);
      * ``UNKNOWN_TERMINAL_TOKEN_REFUSED`` — the token appears on no
        supported axis.

    AuthorityEffect: None.
    """
    if axis not in SUPPORTED_AXES:
        raise AliasAdapterRefusal(
            "UNSUPPORTED_AXIS_REFUSED",
            f"axis must be one of "
            f"{tuple(a.__name__ for a in SUPPORTED_AXES)}, got {axis!r}",
        )
    if not isinstance(token, str):
        raise AliasAdapterRefusal(
            "NON_STRING_TOKEN_REFUSED",
            f"token must be a spelling (str), got {type(token).__name__}; "
            f"str-valued registry enum members pass as their own spelling",
        )
    table = _axis_tokens(axis)
    if token in table:
        return table[token]
    other_axes = known_axes_for(token)
    if other_axes:
        raise AliasAdapterRefusal(
            "AXIS_MISMATCH_REFUSED",
            f"token '{token}' is a {'/'.join(other_axes)} token; asked for "
            f"{axis.__name__}. Declared aliases never coerce across axes.",
        )
    raise AliasAdapterRefusal(
        "UNKNOWN_TERMINAL_TOKEN_REFUSED",
        f"token '{token}' appears on no supported axis "
        f"{tuple(a.__name__ for a in SUPPORTED_AXES)}; the ADAPT-01 table "
        f"is closed and fail-closed",
    )


def alias_table() -> Mapping[str, Mapping[str, str]]:
    """Export the TOTAL closed table for tests: axis name -> {spelling ->
    registry token value}. Identity rows included, so totality over the
    paper's alias declarations is checkable without re-deriving the map."""
    return {
        axis.__name__: {
            spelling: member.value for spelling, member in _axis_tokens(axis).items()
        }
        for axis in SUPPORTED_AXES
    }


__all__ = [
    "AliasAdapterRefusal",
    "SUPPORTED_AXES",
    "resolve_alias",
    "alias_table",
    "known_axes_for",
]



