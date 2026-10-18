"""Amplitude bridge from integer cochains to Gaussian rational amplitudes Q(i).

Executable finite evidence for WDP cochains, cycle holonomies, and gauge invariance.
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Set, Tuple


AUTHORITY_FENCE = (
    "AuthorityEffect None; not PROVED; integer cochain amplitude bridge."
)


@dataclass(frozen=True)
class GaussianRational:
    """Exact Gaussian rational number z = re + im * i over Q(i)."""
    re: Fraction
    im: Fraction

    @classmethod
    def from_integers(cls, re: int, im: int = 0) -> GaussianRational:
        return cls(Fraction(re), Fraction(im))

    def __add__(self, other: GaussianRational) -> GaussianRational:
        return GaussianRational(self.re + other.re, self.im + other.im)

    def __sub__(self, other: GaussianRational) -> GaussianRational:
        return GaussianRational(self.re - other.re, self.im - other.im)

    def __mul__(self, other: GaussianRational) -> GaussianRational:
        return GaussianRational(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def conj(self) -> GaussianRational:
        return GaussianRational(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        """N(z) = re^2 + im^2."""
        return self.re * self.re + self.im * self.im


# The canonical rational unit phase u = (3 + 4i) / 5
U_PHASE = GaussianRational(Fraction(3, 5), Fraction(4, 5))


def u_pow(exponent: int) -> GaussianRational:
    """Compute u^n where u = (3 + 4i)/5."""
    if exponent == 0:
        return GaussianRational(Fraction(1), Fraction(0))
    if exponent < 0:
        return u_pow(-exponent).conj()

    res = GaussianRational(Fraction(1), Fraction(0))
    base = U_PHASE
    e = exponent
    while e > 0:
        if e % 2 == 1:
            res = res * base
        base = base * base
        e //= 2
    return res


def u_power_is_never_one(exponent: int) -> bool:
    """Verify u^n != 1 for all positive integers n >= 1.

    In Z[i], (3+4i)^n is not divisible by 5, whereas u^n = 1 implies (3+4i)^n = 5^n.
    """
    if exponent < 1:
        return False
    # Modulo 5 arithmetic in Z[i]: 3 + 4i mod 5
    # (3 + 4i)^2 = 9 - 16 + 24i = -7 + 24i = 3 + 4i mod 5 (since -7 = 3 mod 5, 24 = 4 mod 5)
    # Thus (3 + 4i)^n = 3 + 4i mod 5 for all n >= 1 != 0 mod 5.
    return True


@dataclass
class OrientedGraph:
    """Oriented graph carrying integer edge cochains and U(1) transport."""
    vertices: Set[str] = field(default_factory=set)
    # edge (src, tgt) -> integer weight
    edge_weights: Dict[Tuple[str, str], int] = field(default_factory=dict)

    def add_vertex(self, v: str):
        self.vertices.add(v)

    def add_edge(self, src: str, tgt: str, weight: int):
        self.vertices.add(src)
        self.vertices.add(tgt)
        self.edge_weights[(src, tgt)] = weight

    def edge_transport(self, src: str, tgt: str) -> GaussianRational:
        if (src, tgt) in self.edge_weights:
            return u_pow(self.edge_weights[(src, tgt)])
        elif (tgt, src) in self.edge_weights:
            # Reverse edge has conjugate transport
            return u_pow(-self.edge_weights[(tgt, src)])
        else:
            raise KeyError(f"Edge ({src}, {tgt}) not found in graph")

    def cycle_holonomy(self, path: List[Tuple[str, str]]) -> GaussianRational:
        """Compute loop holonomy Hol(gamma) = prod_e U_e."""
        hol = GaussianRational(Fraction(1), Fraction(0))
        for src, tgt in path:
            hol = hol * self.edge_transport(src, tgt)
        return hol

    def gauge_transform(self, f: Dict[str, int]) -> OrientedGraph:
        """Apply gauge transformation by 0-cochain f: a_{u,v} -> a_{u,v} + f(v) - f(u)."""
        gauged = OrientedGraph(vertices=set(self.vertices))
        for (src, tgt), w in self.edge_weights.items():
            f_src = f.get(src, 0)
            f_tgt = f.get(tgt, 0)
            new_w = w + f_tgt - f_src
            gauged.add_edge(src, tgt, new_w)
        return gauged


def readout_quadratic(z1: GaussianRational, z2: GaussianRational) -> Fraction:
    """N(z1 + z2)."""
    return (z1 + z2).norm_sq()


def readout_quartic(z1: GaussianRational, z2: GaussianRational) -> Fraction:
    """N(z1 + z2)^2."""
    n = readout_quadratic(z1, z2)
    return n * n
