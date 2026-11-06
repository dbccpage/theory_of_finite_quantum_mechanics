"""Genesis Primitives Category 10: Attachment Ladder & Lawful Skeletal Filtration.

Selected educational models related to 19L57G1 (lean4/Derivation/Attachment.lean, LadderGeneral.lean).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

Lawful attachment policies without clamping, checked attachments, the exact
UpFamily one-edge grammar, and occurrence tokens vs position indices.
"""

from __future__ import annotations

from typing import Any, Callable, Sequence

from .primitive_passage import PS, PEvent, preplay

Policy = Callable[[int], int]


def lawful_to(pi: Policy, rounds: int) -> bool:
    """Lawfulness certificate: every attachment chooses an already-represented parent."""
    if type(rounds) is not int or rounds < 0:
        return False
    for k in range(rounds + 1):
        parent = pi(k + 1)
        if type(parent) is not int or not 0 <= parent <= k:
            return False
    return True


def par(pi: Policy, k: int) -> int:
    """The chosen parent of child k + 1."""
    return pi(k + 1)


def fresh_tok(s: PS) -> int:
    """Canonical fresh token: one past the maximum occurrence token."""
    return max(s.occ) + 1 if s.occ else 0


def up_block(s: PS, p: int) -> list[PEvent]:
    """Single Up block attaching a new node to represented parent p."""
    tok = fresh_tok(s)
    child_pos = len(s.occ)
    return [
        ("admitOcc", tok),
        ("assertWit", p, child_pos),
        ("admitWit", p, child_pos),
        ("protect", p, child_pos),
    ]


def up_family(s: PS) -> list[list[PEvent]]:
    """Complete Up family: all legal attachments across all represented positions."""
    return [up_block(s, p) for p in range(len(s.occ))]


def attach_checked(s: PS, p: int) -> dict[str, Any]:
    """Checked attachment: extend at parent p on a live state, or return typed refusal."""
    if type(p) is int and 0 <= p < len(s.occ) and not s.halted:
        t = preplay(up_block(s, p), s)
        return {
            "outcome": "attached",
            "occ_len": len(t.occ),
            "wit_len": len(t.wit),
            "post_state": t,
        }
    return {
        "outcome": "refusedParent",
        "parent": p,
        "bound": len(s.occ),
    }


def shell_guard(dim: int, cell_boundary: Sequence[int]) -> bool:
    """Ascent condition: a (k+1)-cell is admissible only over an unfilled boundary of strictly ascending indices."""
    if type(dim) is not int or dim < 0 or len(cell_boundary) != dim + 1:
        return False
    if any(type(index) is not int or index < 0 for index in cell_boundary):
        return False
    return all(cell_boundary[i] < cell_boundary[i + 1] for i in range(len(cell_boundary) - 1))
