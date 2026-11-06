"""Genesis Primitives Category 14: Controller Category & Variable Event Grammars.

Selected educational models related to 19L57G1 (lean4/Derivation/ControllerCategory.lean, code/derivation/controller_category.py).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

The 1024-member class of variable event grammars, controlled interpreters,
response-liveness predicates, and controlled execution orbits.
"""

from __future__ import annotations

from itertools import product
from typing import Sequence

from .primitive_passage import PS, PEvent, pstep

KIND_NAMES: tuple[str, ...] = (
    "admitOcc",
    "admitWit",
    "protect",
    "declareObs",
    "refineCol",
    "addCol",
    "refuse",
    "setBudget",
    "setLicense",
    "halt",
)

_KIND_INDEX: dict[str, int] = {k: i for i, k in enumerate(KIND_NAMES)}

KindDesc = tuple[bool, ...]
FULL_K: KindDesc = (True,) * 10


def _validate_descriptor(d: KindDesc) -> None:
    if (
        type(d) is not tuple
        or len(d) != len(KIND_NAMES)
        or any(type(flag) is not bool for flag in d)
    ):
        raise ValueError("REFUSED_SHAPE: controller needs ten exact Boolean toggles")


def all_kinds() -> list[KindDesc]:
    """The complete 1024-member enumeration of event-grammar configurations."""
    return [tuple(bits) for bits in product((False, True), repeat=10)]


def full_without(name: str) -> KindDesc:
    """The all-on controller with exactly one event kind disabled."""
    if name not in _KIND_INDEX:
        raise ValueError(f"unknown event kind: {name!r}")
    return tuple(k != name for k in KIND_NAMES)


def enabled(d: KindDesc, e: PEvent) -> bool:
    """Checks whether the controller enables event e."""
    _validate_descriptor(d)
    if type(e) is not tuple or not e:
        raise ValueError("REFUSED_SHAPE: event must be a nonempty immutable tuple")
    kind = e[0]
    if kind == "assertWit":
        return True  # Supply-side grammar is universally enabled
    if not isinstance(kind, str) or kind not in _KIND_INDEX:
        raise ValueError(f"unknown event kind: {kind!r}")
    return d[_KIND_INDEX[kind]]


def interp_k(d: KindDesc, s: PS, e: PEvent) -> PS:
    """Controlled interpreter: executes step if enabled, else inert."""
    return pstep(s, e) if enabled(d, e) else s


def replay_k(d: KindDesc, h: Sequence[PEvent], s: PS) -> PS:
    """Replays history h under controller d starting from state s."""
    for e in h:
        s = interp_k(d, s, e)
    return s


def response_live(d: KindDesc) -> bool:
    """Syntactic two-rule support: both response executors and funding enabled."""
    _validate_descriptor(d)
    return d[_KIND_INDEX["refineCol"]] and d[_KIND_INDEX["addCol"]] and d[_KIND_INDEX["setBudget"]]
