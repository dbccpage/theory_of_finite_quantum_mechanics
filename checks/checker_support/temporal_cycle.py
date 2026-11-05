"""Owned finite three-color temporal cycle. AuthorityEffect: None.

An even cycle has 2, 4 or 6 sites, immutable SU(3) links in Q(i),
and an antiperiodic closing link. This is a finite matrix representation.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
import sympy as sp

from .boundary import Violation, evaluate
from .domains import sequence
from .gaussian_expression import _decode
from .gaussian_matrix import GaussianMatrix as M
from .gaussian_rational import GaussianRational as G
from .outcome import Outcome


def _link(value: object) -> M:
    if type(value) is M:
        return value.require_shape(3, 3)
    return M.from_sympy(value).require_shape(3, 3)


def _transport(links: tuple[M, ...]) -> M:
    size = 3*len(links)
    rows = [[G(0) for _ in range(size)] for _ in range(size)]
    for site, link in enumerate(links):
        target = (site+1) % len(links)
        sign = G(-1) if site == len(links)-1 else G(1)
        for i in range(3):
            for j in range(3):
                rows[3*site+i][3*target+j] = link.rows[i][j].mul(sign)
    return M(rows)


@dataclass(frozen=True, slots=True, init=False)
class TemporalCycle:
    """Owns admitted links and cached transport; each query returns detached exports."""
    _links: tuple[M, ...]
    _forward: M

    def __init__(self, links: object) -> None:
        if type(links) is not tuple:
            raise Violation("input", "temporal links require an immutable tuple")
        entries = sequence(links, "temporal links", maximum=6)
        if len(entries) not in (2, 4, 6):
            raise Violation("input", "temporal cycle needs 2, 4 or 6 sites")
        owned = tuple(_link(value) for value in entries)
        identity = M.eye(3)
        for link in owned:
            if link.adjoint().mul(link) != identity:
                raise Violation("input", "temporal link is not unitary")
            if link.determinant() != G(1):
                raise Violation("input", "temporal link determinant is not one")
        forward = _transport(owned)
        object.__setattr__(self, "_links", owned)
        object.__setattr__(self, "_forward", forward)

    @property
    def sites(self) -> int:
        return len(self._links)

    @property
    def links(self) -> tuple[sp.ImmutableMatrix, ...]:
        return tuple(link.to_sympy() for link in self._links)

    def transport(self) -> sp.ImmutableMatrix:
        """Legacy exact immutable export; no caller can mutate cached transport."""
        return self._forward.to_sympy()

    def transport_result(self) -> Outcome[M]:
        return evaluate(lambda: self._forward)

    def _dirac(self, mass: object, fugacity: object) -> M:
        admitted_mass = _decode(mass)
        activity = _decode(fugacity)
        if admitted_mass.im != 0:
            raise Violation("input", "temporal mass must be real")
        if activity == G(0):
            raise Violation("input", "zero fugacity has no inverse")
        forward = self._forward.scale(activity)
        backward = self._forward.adjoint().scale(activity.inv())
        hopping = forward.add(backward.neg()).scale(Q(1, 2))
        return M.eye(3*self.sites).scale(admitted_mass).add(hopping)

    def dirac(self, mass: object, fugacity: object) -> sp.ImmutableMatrix:
        """Legacy exact export; admits nonunit activity for explicit counterexamples."""
        return self._dirac(mass, fugacity).to_sympy()

    def dirac_result(self, mass: object, fugacity: object) -> Outcome[M]:
        return evaluate(self._dirac, mass, fugacity)
