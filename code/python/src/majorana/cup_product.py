from __future__ import annotations
"""Cup product shell."""

from dataclasses import field
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class SparseCochain:
    degree: int
    terms: List[Tuple[int, float]] = field(default_factory=list)


@dataclass
class CupProduct:
    left_degree: int
    right_degree: int
    result: SparseCochain

    @classmethod
    def of(cls, a: SparseCochain, b: SparseCochain) -> "CupProduct":
        terms: List[Tuple[int, float]] = []
        if len(a.terms) == 1 and len(b.terms) == 1:
            ia, ca = a.terms[0]
            ib, cb = b.terms[0]
            terms.append((ia * 1_000_003 + ib, ca * cb))
        return cls(a.degree, b.degree, SparseCochain(a.degree + b.degree, terms))



