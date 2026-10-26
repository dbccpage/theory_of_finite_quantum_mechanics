"""The §23 letter driver: which letters a diagnostic state may propose.

The driver is a policy on top of the step laws. It proposes only letters that
fit the state's FOC class, so it never proposes T on an open or blind state,
E off an exact state, or Λ without a Law 4 trigger. Whether a proposed step is
lawful is still decided by ``automaton.step_violations``.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Dict, Tuple

from automaton import ACTIVE, CLOSED, EXACT, REFUSED, TERMINALIZED, State

INADEQUATE = "DetectorInadequate"

DRIVER_LETTERS: Dict[str, Tuple[str, ...]] = {
    EXACT: ("E", "T", "I"),
    CLOSED: ("R", "Λ", "T", "I"),
    ACTIVE: ("R", "C", "D", "M", "I"),
    INADEQUATE: ("Λ", "M", "C", "I"),
}

# The four §23.2 drivers, as letter tapes.
DRIVERS: Dict[str, str] = {
    "autopoietic": "CREIT",
    "refusal": "CRMT",
    "self_examination": "CRΛIT",
    "allopoietic": "DIT",
}


def driver_class(state: State) -> str:
    return INADEQUATE if not state.adequate else state.cls


def admissible(state: State, control: str) -> Tuple[str, ...]:
    """Letters the driver may propose from ``state`` under ``control``."""
    if control == TERMINALIZED:
        return ()
    letters = DRIVER_LETTERS[driver_class(state)]
    if control == REFUSED:
        return tuple(letter for letter in letters if letter in ("C", "Λ", "T"))
    return letters
