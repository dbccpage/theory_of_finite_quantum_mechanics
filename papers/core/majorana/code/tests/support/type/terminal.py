from pydantic import ConfigDict
"""Terminal boundaries for Omega execution.

Maintains a strict firewall between derived mathematical structure and terminal
authority. No structure terminal may be coerced into an authority terminal.
"""

from pydantic.dataclasses import dataclass
import re
from typing import Any


class Terminal:
    """Base class for all terminal execution outcomes."""


class AuthorityTerminal(Terminal):
    """Authority-terminal proposal; it is not certified by construction."""

    def __init__(self, token: str, evidence_level: Any) -> None:
        self.token = token
        self.evidence_level = evidence_level

    def __repr__(self) -> str:
        return f"AuthorityTerminal(token={self.token!r}, level={self.evidence_level!r})"


class ScopedNegative(Terminal):
    def __init__(self, formalism: str, reason: str) -> None:
        self.formalism = formalism
        self.reason = reason

    def __repr__(self) -> str:
        return f"ScopedNegative(formalism={self.formalism!r}, reason={self.reason!r})"


class StructureDerived(Terminal):
    """Derived mathematical structure with no authority effect."""

    def __init__(self, formalism: str, certificate: Any) -> None:
        self.formalism = formalism
        self.certificate = certificate

    def __repr__(self) -> str:
        return (
            f"StructureDerived(formalism={self.formalism!r}, cert={self.certificate!r})"
        )


class LiftRequired(Terminal):
    def __init__(self, formalism: str, witness: Any) -> None:
        self.formalism = formalism
        self.witness = witness

    def __repr__(self) -> str:
        return f"LiftRequired(formalism={self.formalism!r}, witness={self.witness!r})"


class RefusedFormalism(Terminal):
    def __init__(self, formalism: str, reason: str) -> None:
        self.formalism = formalism
        self.reason = reason

    def __repr__(self) -> str:
        return f"RefusedFormalism(formalism={self.formalism!r}, reason={self.reason!r})"


@dataclass(config=ConfigDict(arbitrary_types_allowed=True, frozen=True))
class AuthorityDescentState:
    """Explicit state required even to propose an authority transition."""

    replay_hash: str = ""
    deterministic: bool = True
    phi1: Any = 0
    exhaustive: bool = True
    skeleton_aligned: bool = True
    lift_required: bool = False
    has_refusal: bool = False
    human_promoted: bool = False


def is_auth(terminal: Any, descent_state: Any = None) -> bool:
    """Evaluate all guards fail-closed; missing state never passes."""

    if not isinstance(terminal, AuthorityTerminal):
        return False
    if not isinstance(descent_state, AuthorityDescentState):
        return False
    if not terminal.token or terminal.evidence_level is None:
        return False
    if re.fullmatch(r"[0-9a-f]{64}", descent_state.replay_hash) is None:
        return False
    return all(
        (
            descent_state.deterministic,
            descent_state.phi1 == 0,
            descent_state.exhaustive,
            descent_state.skeleton_aligned,
            not descent_state.lift_required,
            not descent_state.has_refusal,
            descent_state.human_promoted,
        )
    )


class Terminalizer:
    """Create terminal proposals; never create certified authority."""

    @staticmethod
    def terminalize_authority(token: str, evidence_level: Any) -> AuthorityTerminal:
        return AuthorityTerminal(token, evidence_level)

    @staticmethod
    def terminalize_structure(formalism: str, certificate: Any) -> StructureDerived:
        return StructureDerived(formalism, certificate)


__all__ = [
    "Terminal",
    "AuthorityTerminal",
    "AuthorityDescentState",
    "ScopedNegative",
    "StructureDerived",
    "LiftRequired",
    "RefusedFormalism",
    "is_auth",
    "Terminalizer",
]


