"""Majorana zero modes, Clifford algebra anticommutation, and braid actions.

Exact GF(2) and rational representation of Majorana modes and Kitaev chains.
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Set, Tuple


class MajoranaError(Exception):
    pass


@dataclass(frozen=True)
class MajoranaMonomial:
    """A product of distinct Majorana modes gamma_{i_1} ... gamma_{i_k} with i_1 < ... < i_k."""
    modes: Tuple[int, ...]  # sorted indices of gamma operators

    @classmethod
    def identity(cls) -> MajoranaMonomial:
        return cls(())

    @classmethod
    def single(cls, i: int) -> MajoranaMonomial:
        return cls((i,))

    def multiply(self, other: MajoranaMonomial) -> Tuple[Fraction, MajoranaMonomial]:
        """Multiply two Majorana monomials using {gamma_i, gamma_j} = 2 delta_{ij}."""
        # Merge sort while tracking sign flips
        all_modes = list(self.modes) + list(other.modes)
        sign = Fraction(1)
        # Bubble sort adjacent modes: gamma_i gamma_j = -gamma_j gamma_i for i != j
        n = len(all_modes)
        for i in range(n):
            for j in range(n - 1 - i):
                if all_modes[j] > all_modes[j + 1]:
                    all_modes[j], all_modes[j + 1] = all_modes[j + 1], all_modes[j]
                    sign = -sign

        # Cancel duplicates: gamma_i^2 = 1
        merged: List[int] = []
        k = 0
        while k < len(all_modes):
            if k + 1 < len(all_modes) and all_modes[k] == all_modes[k + 1]:
                # gamma_i^2 = 1
                k += 2
            else:
                merged.append(all_modes[k])
                k += 1

        return sign, MajoranaMonomial(tuple(merged))


@dataclass
class MajoranaOperator:
    """Linear combination of Majorana monomials with exact rational coefficients."""
    terms: Dict[MajoranaMonomial, Fraction] = field(default_factory=dict)

    @classmethod
    def zero(cls) -> MajoranaOperator:
        return cls({})

    @classmethod
    def identity(cls) -> MajoranaOperator:
        return cls({MajoranaMonomial.identity(): Fraction(1)})

    @classmethod
    def mode(cls, i: int) -> MajoranaOperator:
        return cls({MajoranaMonomial.single(i): Fraction(1)})

    def add(self, other: MajoranaOperator) -> MajoranaOperator:
        res = dict(self.terms)
        for mon, coef in other.terms.items():
            res[mon] = res.get(mon, Fraction(0)) + coef
            if res[mon] == 0:
                del res[mon]
        return MajoranaOperator(res)

    def multiply(self, other: MajoranaOperator) -> MajoranaOperator:
        res: Dict[MajoranaMonomial, Fraction] = {}
        for mon1, coef1 in self.terms.items():
            for mon2, coef2 in other.terms.items():
                sign, prod_mon = mon1.multiply(mon2)
                val = coef1 * coef2 * sign
                res[prod_mon] = res.get(prod_mon, Fraction(0)) + val
                if res[prod_mon] == 0:
                    del res[prod_mon]
        return MajoranaOperator(res)

    def is_zero(self) -> bool:
        return len(self.terms) == 0

    def is_scalar(self) -> bool:
        return len(self.terms) == 0 or (
            len(self.terms) == 1 and MajoranaMonomial.identity() in self.terms
        )

    def scalar_value(self) -> Fraction:
        return self.terms.get(MajoranaMonomial.identity(), Fraction(0))


def anticommutator(op1: MajoranaOperator, op2: MajoranaOperator) -> MajoranaOperator:
    """{A, B} = AB + BA."""
    return op1.multiply(op2).add(op2.multiply(op1))


def commutator(op1: MajoranaOperator, op2: MajoranaOperator) -> MajoranaOperator:
    """[A, B] = AB - BA."""
    neg_op2 = MajoranaOperator({mon: -c for mon, c in op2.terms.items()})
    return op1.multiply(op2).add(neg_op2.multiply(op1))


def kitaev_chain_parity(num_sites: usize) -> MajoranaOperator:
    """Total fermion parity operator P = prod_{j=1}^N ( -i gamma_{2j-1} gamma_{2j} )."""
    p = MajoranaOperator.identity()
    for j in range(num_sites):
        g_odd = MajoranaOperator.mode(2 * j)
        g_even = MajoranaOperator.mode(2 * j + 1)
        # Pair density proxy
        p = p.multiply(g_odd).multiply(g_even)
    return p
