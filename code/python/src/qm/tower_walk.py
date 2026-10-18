"""Walk down a tower of binary partitions and multiply the cover degrees.

An 8-element set is split into 4 pairs, then 2 blocks of four pairs-of-pairs,
then one block. Each cover degree is |fine| / |coarse|. The product of the
degrees is compared with the number of atoms.
"""
from fractions import Fraction


class TowerWalkError(Exception):
    """A cover degree was not an integer, or the product missed the atom count."""


def _degree(coarse, fine) -> int:
    if len(fine) % len(coarse) != 0:
        raise TowerWalkError("fine block count does not divide into the coarse count")
    for block in fine:
        containers = [parent for parent in coarse if block <= parent]
        if len(containers) != 1:
            raise TowerWalkError("a fine block is not in exactly one coarse block")
    return len(fine) // len(coarse)


def tower_degree_product() -> int:
    """Return the product of cover degrees from 8 atoms up to one block."""
    atoms = tuple(frozenset([index]) for index in range(8))
    pairs = tuple(frozenset(range(2 * index, 2 * index + 2)) for index in range(4))
    fours = (
        frozenset(range(4)),
        frozenset(range(4, 8)),
    )
    whole = (frozenset(range(8)),)
    degrees = (
        _degree(pairs, atoms),
        _degree(fours, pairs),
        _degree(whole, fours),
    )
    product = 1
    for degree in degrees:
        product *= degree
    if product != len(atoms):
        raise TowerWalkError(f"degree product {product} is not {len(atoms)}")
    if Fraction(product, len(atoms)) != 1:
        raise TowerWalkError("normalized degree is not 1")
    return product
