"""Genesis Primitives Category 16: Stable Content, Relational Inertia & Quiescence.

Selected educational models related to 19L57G1 (lean4/Derivation/StableContent.lean, Inertia.lean, code/derivation/stable_content.py).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

Protected separation, sufficient conditions for trace stability, quiescent states,
and relational inertia (resistance of relational structures to environmental perturbation).
"""

from __future__ import annotations

from typing import Sequence

from .primitive_passage import PS, obst_p, sep_p


def prot_sep(s: PS, i: int, j: int) -> bool:
    """Protected separation: protected AND separated by the declared observation."""
    if s.obs is None:
        return False
    return (i, j) in s.prot and sep_p(s.obs, i, j)


def quiescent_p(s: PS, n: int) -> bool:
    """Quiescence: no pair below n is actively obstructed."""
    return all(not obst_p(s, i, j) for i in range(n) for j in range(n))


def has_relational_inertia(s: PS, i: int, j: int, post_states: Sequence[PS]) -> bool:
    """Relational inertia: a protected separation persists across an entire family of perturbed post-states."""
    if not prot_sep(s, i, j):
        return False
    return all(prot_sep(s_next, i, j) for s_next in post_states)
