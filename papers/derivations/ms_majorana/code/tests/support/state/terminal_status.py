from __future__ import annotations
from pydantic import ConfigDict
"""Structural Python mirror for ``omega_engine/crates/omega_state/src/terminal_status.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


from pydantic.dataclasses import dataclass
from enum import Enum
from typing import Any


class _RustSurfaceMeta(type):
    def __getattr__(cls, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {cls.__name__}.{name} is not ported"
            )

        return unavailable


class _RustSurfaceObject(metaclass=_RustSurfaceMeta):
    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {type(self).__name__}.{name} is not ported"
            )

        return unavailable


TerminationCondition = Enum(
    "TerminationCondition",
    {
        "Converged": "Converged",
        "Irreducible": "Irreducible",
        "BudgetExhausted": "BudgetExhausted",
        "ExternalAbort": "ExternalAbort",
        "Suspended": "Suspended",
        "ConstraintViolation": "ConstraintViolation",
    },
    type=str,
)
TerminationCondition.__doc__ = (
    "Structural mirror of Rust ``TerminationCondition`` variants."
)


TerminalStatus = Enum(
    "TerminalStatus",
    {
        "ExactRuleDerived": "ExactRuleDerived",
        "UniqueOutputDerived": "UniqueOutputDerived",
        "NoRuleInSearchClass": "NoRuleInSearchClass",
        "NonUniqueOutput": "NonUniqueOutput",
        "EnumeratorFailure": "EnumeratorFailure",
        "Refused": "Refused",
        "LabelConflictsWithDerivation": "LabelConflictsWithDerivation",
        "BudgetUnknown": "BudgetUnknown",
        "InvalidProposal": "InvalidProposal",
        "OperatorConflict": "OperatorConflict",
        "UnknownSector": "UnknownSector",
        "NoDescentYet": "NoDescentYet",
        "LabelOnlyUncertified": "LabelOnlyUncertified",
        "LiftRequired": "LiftRequired",
        "ParseRefused": "ParseRefused",
        "ReplayMismatch": "ReplayMismatch",
        "PolicyAmbiguous": "PolicyAmbiguous",
        "NoPacket": "NoPacket",
        "VerifierDisabled": "VerifierDisabled",
        "SearchIncomplete": "SearchIncomplete",
        "PolicyUnderspecified": "PolicyUnderspecified",
    },
    type=str,
)
TerminalStatus.__doc__ = "Structural mirror of Rust ``TerminalStatus`` variants."


ALL_TERMINAL_STATUSES: Any = None


ResidualClass = Enum(
    "ResidualClass",
    {
        "Exact": "Exact",
        "ClosedSurvivor": "ClosedSurvivor",
        "Open": "Open",
        "Refused": "Refused",
    },
    type=str,
)
ResidualClass.__doc__ = "Structural mirror of Rust ``ResidualClass`` variants."


@dataclass(init=False, config=ConfigDict(arbitrary_types_allowed=True))
class FiberAgreement(_RustSurfaceObject):
    """Structural mirror of Rust ``FiberAgreement``."""

    coherent_transport_verified: Any = None
    replay_equivalence_verified: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("coherent_transport_verified", "replay_equivalence_verified")
        if len(args) > len(names):
            raise TypeError("FiberAgreement received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


TerminalClassificationError = Enum(
    "TerminalClassificationError",
    {
        "InvalidFiberCounts": "InvalidFiberCounts",
        "InvalidFiberState": "InvalidFiberState",
    },
    type=str,
)
TerminalClassificationError.__doc__ = (
    "Structural mirror of Rust ``TerminalClassificationError`` variants."
)


def authority_level(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``authority_level``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/terminal_status.rs::authority_level"
    )


def residual_class(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``residual_class``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/terminal_status.rs::residual_class"
    )


def can_teach(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``can_teach``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/terminal_status.rs::can_teach"
    )


def authority_terminal(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``authority_terminal``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/terminal_status.rs::authority_terminal"
    )


def terminal_from_fiber(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``terminal_from_fiber``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/terminal_status.rs::terminal_from_fiber"
    )




