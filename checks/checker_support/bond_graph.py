"""Owned simple graph for the bounded Hubbard model. AuthorityEffect: None."""
from dataclasses import dataclass

from .boundary import Violation
from .domains import integer, sequence


def _edge(value: object, sites: int) -> tuple[int, int]:
    left, right = sequence(value, "bond", 2, 2)
    u = integer(left, "bond endpoint", 0, sites-1)
    v = integer(right, "bond endpoint", 0, sites-1)
    if u == v:
        raise Violation("input", "self bonds are excluded")
    return min(u, v), max(u, v)


@dataclass(frozen=True, slots=True, init=False)
class BondGraph:
    """Owns 1..4 sites and at most six unique undirected edges in lexical order."""
    sites: int
    bonds: tuple[tuple[int, int], ...]

    def __init__(self, sites: object, bonds: object) -> None:
        size = integer(sites, "Hubbard sites", 1, 4)
        entries = sequence(bonds, "bonds", maximum=6)
        normalized = tuple(sorted(_edge(edge, size) for edge in entries))
        if len(set(normalized)) != len(normalized):
            raise Violation("duplicate", "undirected bonds must be unique")
        object.__setattr__(self, "sites", size)
        object.__setattr__(self, "bonds", normalized)
