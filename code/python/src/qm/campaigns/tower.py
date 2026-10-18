"""A refinement tower of partitions. Indices multiply to the number of atoms.

Origin: code/python/src/qm/campaigns/tower.py
Claim: {{0,1,2,3}} refined by halves and then by singletons has index product 4.
AuthorityEffect: None.
"""
from fractions import Fraction


class TowerError(Exception):
    """A level was not a refinement of the previous level."""


def _index(coarse, fine) -> int:
    for block in fine:
        hosts = [parent for parent in coarse if block <= parent]
        if len(hosts) != 1:
            raise TowerError(f"block {block} is not inside exactly one coarser block")
    return len(fine) // len(coarse) if len(coarse) and len(fine) % len(coarse) == 0 else None


def tower_degree() -> int:
    levels = (
        (frozenset({0, 1, 2, 3}),),
        (frozenset({0, 1}), frozenset({2, 3})),
        tuple(frozenset({atom}) for atom in range(4)),
    )
    degree = 1
    for coarse, fine in zip(levels, levels[1:]):
        step = _index(coarse, fine)
        if step is None:
            raise TowerError("refinement index is not an integer")
        degree *= step
    atoms = len(levels[-1])
    if degree != atoms:
        raise TowerError(f"tower degree {degree} is not the atom count {atoms}")
    return degree
