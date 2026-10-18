"""Certified curvature masses Psi^sq and Phi^sq in exact rational interval arithmetic.

AuthorityEffect: None.
stated region only; mints no authority.

Mathematical definitions:
- Vector mass: Phi^sq(T, v) = sum_{i=0}^{17} (|<e_i, v>|^2 - 1/6)^2
- Basis mass:  Psi^sq(T, U) = sum_{j=0}^5 sum_{i=0}^{17} (|<e_i, U_j>|^2 - 1/6)^2
                            = sum_{j=0}^5 Phi^sq(T, U_j)
- Invariant-Systems functional: f(v) = 1 - (6/5) * Phi^sq(T, v)
  => 1 - f(v) = (6/5) * Phi^sq(T, v) >= f_gap = (6/5) * Phi^sq_lower.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Sequence, Tuple

from .cyclotomic import (
    Cyc24,
    SqrtBox,
    cyc24_interval_enclosure,
)
from .interval import (
    BasisBox,
    RationalInterval,
    VectorBox,
)
from .mub_triples import D, ExactVec


class EnclosedVector:
    """Pre-enclosed fixed vector where conj(e[k]) = (A_k, B_k) are RationalIntervals."""

    __slots__ = ("components",)

    def __init__(self, components: Sequence[Tuple[RationalInterval, RationalInterval]]) -> None:
        self.components = tuple(components)

    @classmethod
    def from_exact_vec(cls, e: ExactVec, sb: SqrtBox) -> EnclosedVector:
        comps = []
        for k in range(D):
            re_iv, im_iv = cyc24_interval_enclosure(e[k].conj(), sb)
            comps.append((re_iv, im_iv))
        return cls(comps)

    def widened(self, delta: Fraction) -> EnclosedVector:
        """Widen each component interval by [-delta, delta]."""
        d = RationalInterval(-delta, delta)
        new_comps = []
        for re_iv, im_iv in self.components:
            new_comps.append((re_iv.add(d), im_iv.add(d)))
        return EnclosedVector(new_comps)

    def residual_sq_lower(self, vbox: VectorBox) -> Fraction:
        """Certified lower bound on (| <e, v> |^2 - 1/6)^2 over vbox."""
        re = RationalInterval.point(Fraction(0, 1))
        im = RationalInterval.point(Fraction(0, 1))

        for k in range(D):
            a, b = self.components[k]
            x = vbox[2 * k]
            y = vbox[2 * k + 1]
            re = re.add(a.mul(x).sub(b.mul(y)))
            im = im.add(a.mul(y).add(b.mul(x)))

        mod_sq = re.sq().add(im.sq())
        sixth = RationalInterval.point(Fraction(1, 6))
        omega = mod_sq.sub(sixth)
        return omega.sq().lo


class EnclosedTriple:
    """An exact MUB triple pre-enclosed into RationalIntervals for fast box evaluation."""

    __slots__ = ("vectors",)

    def __init__(self, vectors: Sequence[EnclosedVector]) -> None:
        self.vectors = tuple(vectors)

    @classmethod
    def from_columns(cls, columns: Sequence[ExactVec], sb: SqrtBox | None = None) -> EnclosedTriple:
        if sb is None:
            sb = SqrtBox.standard()
        vecs = [EnclosedVector.from_exact_vec(col, sb) for col in columns]
        return cls(vecs)

    @classmethod
    def widened_from_columns(
        cls,
        columns: Sequence[ExactVec],
        delta: Fraction,
        sb: SqrtBox | None = None,
    ) -> EnclosedTriple:
        """Widen B2 and B3 (columns 6..17) by +/- delta, keeping B1 (columns 0..5) exact."""
        if sb is None:
            sb = SqrtBox.standard()
        vecs = []
        for i, col in enumerate(columns):
            base = EnclosedVector.from_exact_vec(col, sb)
            if i >= D:
                vecs.append(base.widened(delta))
            else:
                vecs.append(base)
        return cls(vecs)

    def phi_sq_lower(self, vbox: VectorBox) -> Fraction:
        """Certified lower bound on Phi^sq(T, v) = sum_{i=0}^{17} omega_i(v)^2 over vbox."""
        total = Fraction(0, 1)
        for ev in self.vectors:
            total += ev.residual_sq_lower(vbox)
        return total

    def f_gap(self, vbox: VectorBox) -> Fraction:
        """Certified lower bound on 1 - f(v) = (6/5) * Phi^sq(T, v)."""
        return Fraction(6, 5) * self.phi_sq_lower(vbox)

    def psi_sq_lower(self, bbox: BasisBox) -> Fraction:
        """Certified lower bound on Psi^sq(T, U) = sum_{j=0}^5 Phi^sq(T, U_j)."""
        total = Fraction(0, 1)
        for col_box in bbox:
            total += self.phi_sq_lower(col_box)
        return total

    def certify_vector_box(self, vbox: VectorBox) -> Fraction | None:
        """Return certified f_gap if strictly positive, else None."""
        gap = self.f_gap(vbox)
        if gap > Fraction(0, 1):
            return gap
        return None

    def certify_basis_box(self, bbox: BasisBox) -> Fraction | None:
        """Return certified psi_gap if strictly positive, else None."""
        psi = self.psi_sq_lower(bbox)
        if psi > Fraction(0, 1):
            return psi
        return None
