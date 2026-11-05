"""Exact bounded Hubbard transfer matrices. AuthorityEffect: None.

1..4 sites, 1..4 slices, lexical forward/reverse bond schedule. Exact positive
r, h and fugacity; all stored values and arithmetic admissions use 4096 bits.
"""
from dataclasses import dataclass
from fractions import Fraction as Q

from .bond_graph import BondGraph
from .boundary import Violation, evaluate
from .domains import integer, rational
from .hubbard_determinants import HubbardDeterminants
from .outcome import Outcome
from .rational_determinant import _determinant
from .rational_matrix import RationalMatrix


def _kinetic(graph: BondGraph, r: Q) -> RationalMatrix:
    inverse = rational(1/r, "inverse hopping")
    cosine = rational(rational(r+inverse, "hopping sum")/2, "bond diagonal")
    sine = rational(rational(r-inverse, "hopping difference")/2, "bond off diagonal")
    result = RationalMatrix.eye(graph.sites)
    for left, right in graph.bonds+tuple(reversed(graph.bonds)):
        rows = [list(row) for row in RationalMatrix.eye(graph.sites).rows]
        rows[left][left] = rows[right][right] = cosine
        rows[left][right] = rows[right][left] = sine
        result = RationalMatrix(rows).mul(result)
    return result


def _power(base: Q, exponent: int) -> Q:
    factor = rational(1/base) if exponent < 0 else base
    result = Q(1)
    for _ in range(abs(exponent)):
        result = rational(result*factor, "field prefactor power")
    return result


def _potential(sites: int, mask: int, offset: int, h: Q, fugacity: Q,
               reverse: bool) -> RationalMatrix:
    signs = tuple(2*((mask >> (offset+i)) & 1)-1 for i in range(sites))
    diagonal = tuple(rational(fugacity*_power(h, -s if reverse else s), "potential") for s in signs)
    return RationalMatrix(tuple(tuple(diagonal[i] if i == j else Q(0) for j in range(sites))
                                for i in range(sites)))


@dataclass(frozen=True, slots=True, init=False)
class HubbardTransfer:
    """Owns graph, parameters and cached kinetic matrix; field queries are reentrant."""
    graph: BondGraph
    slices: int
    r: Q
    hs: Q
    fugacity: Q
    attractive: bool
    kinetic: RationalMatrix

    def __init__(self, graph: object, slices: object, r: object, hs: object,
                 fugacity: object, attractive: object = False) -> None:
        if type(graph) is not BondGraph:
            raise Violation("input", "transfer requires an owned BondGraph")
        times = integer(slices, "Hubbard slices", 1, 4)
        hopping = rational(r, "hopping parameter", strictly_positive=True)
        coupling = rational(hs, "field coupling", strictly_positive=True)
        activity = rational(fugacity, "fugacity", strictly_positive=True)
        if type(attractive) is not bool:
            raise Violation("input", "attractive channel must be bool")
        kinetic = _kinetic(graph, hopping)
        for name, value in (("graph", graph), ("slices", times), ("r", hopping), ("hs", coupling),
                            ("fugacity", activity), ("attractive", attractive), ("kinetic", kinetic)):
            object.__setattr__(self, name, value)

    @property
    def field_count(self) -> int:
        return 1 << (self.graph.sites*self.slices)

    def _determinants(self, mask: object) -> HubbardDeterminants:
        field = integer(mask, "field mask", 0, self.field_count-1)
        sites = self.graph.sites
        identity = RationalMatrix.eye(sites)
        up = down = identity
        for time in range(self.slices):
            up_potential = _potential(sites, field, time*sites, self.hs, self.fugacity, False)
            down_potential = _potential(sites, field, time*sites, self.hs, self.fugacity, not self.attractive)
            up = self.kinetic.mul(up_potential).mul(up)
            down = self.kinetic.mul(down_potential).mul(down)
        total_s = 2*field.bit_count()-sites*self.slices
        prefactor = _power(self.hs, -total_s) if self.attractive else Q(1)
        return HubbardDeterminants(_determinant(identity.add(up)), _determinant(identity.add(down)),
                                   prefactor, total_s)

    def determinants(self, mask: object) -> Outcome[HubbardDeterminants]:
        return evaluate(self._determinants, mask)
