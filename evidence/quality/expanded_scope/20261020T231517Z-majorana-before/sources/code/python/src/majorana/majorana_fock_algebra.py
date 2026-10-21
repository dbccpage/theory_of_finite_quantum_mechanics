"""Majorana operators on finite fermionic Fock space, over Q(i).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Sequence

from .majorana_modes import (
    MajoranaError,
    MajoranaMonomial,
    MajoranaOperator,
    anticommutator,
    commutator,
    kitaev_chain_parity,
)

AUTHORITY_EFFECT = "AuthorityEffect: None"
MAX_MODES: int = 5


@dataclass(frozen=True)
class GaussianRat:
    re: Fraction
    im: Fraction

    @classmethod
    def from_ints(cls, re: int, im: int = 0) -> GaussianRat:
        return cls(Fraction(re), Fraction(im))

    def __add__(self, other: GaussianRat) -> GaussianRat:
        return GaussianRat(self.re + other.re, self.im + other.im)

    def __sub__(self, other: GaussianRat) -> GaussianRat:
        return GaussianRat(self.re - other.re, self.im - other.im)

    def __mul__(self, other: GaussianRat) -> GaussianRat:
        return GaussianRat(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def is_zero(self) -> bool:
        return self.re == 0 and self.im == 0


def gi(re: int, im: int = 0) -> GaussianRat:
    return GaussianRat.from_ints(re, im)


def first_anticommutation_failure(
    family: Sequence[Sequence[Sequence[GaussianRat]]],
) -> Optional[tuple[int, int]]:
    count = len(family)
    if count == 0:
        return None
    dim = len(family[0])
    for a in range(count):
        for b in range(a, count):
            # Compute {g_a, g_b} = g_a g_b + g_b g_a
            expected_scalar = gi(2 if a == b else 0)
            # Matrix multiply
            for r in range(dim):
                for c in range(dim):
                    acc = gi(0)
                    for k in range(dim):
                        acc = acc + family[a][r][k] * family[b][k][c] + family[b][r][k] * family[a][k][c]
                    target = expected_scalar if r == c else gi(0)
                    if acc != target:
                        return (a + 1, b + 1)
    return None


class FockCarrier:
    def __init__(self, modes: int) -> None:
        if modes < 1 or modes > MAX_MODES:
            raise MajoranaError(f"modes {modes} outside 1..={MAX_MODES}")
        self._modes = modes
        self._dim = 1 << modes

    def modes(self) -> int:
        return self._modes

    def dimension(self) -> int:
        return self._dim

    def majorana_generator(self, a: int) -> list[list[GaussianRat]]:
        if a < 1 or a > 2 * self._modes:
            raise MajoranaError(f"Majorana index {a} outside 1..={2 * self._modes}")
        mode_j = (a - 1) // 2
        is_even = (a % 2 == 0)
        mat = [[gi(0) for _ in range(self._dim)] for _ in range(self._dim)]

        for state in range(self._dim):
            # Jordan-Wigner parity: (-1)^(sum_{k < mode_j} n_k)
            jw_parity = 1
            for k in range(mode_j):
                if (state >> (self._modes - 1 - k)) & 1:
                    jw_parity = -jw_parity

            # Pauli X on mode_j: flips bit
            # Pauli Y on mode_j: flips bit, with phase -i for |0> -> |1>, +i for |1> -> |0>
            bit_mask = 1 << (self._modes - 1 - mode_j)
            next_state = state ^ bit_mask
            val = (state >> (self._modes - 1 - mode_j)) & 1

            if not is_even:
                # X: flips bit with sign jw_parity
                mat[next_state][state] = gi(jw_parity, 0)
            else:
                # Y: flips bit, phase -i if bit was 0, +i if bit was 1
                phase = gi(0, -jw_parity if val == 0 else jw_parity)
                mat[next_state][state] = phase

        return mat

    def lowering_operator(self, j: int) -> list[list[GaussianRat]]:
        # c_j = (gamma_(2j-1) + i gamma_(2j)) / 2
        g_odd = self.majorana_generator(2 * j - 1)
        g_even = self.majorana_generator(2 * j)
        half = GaussianRat(Fraction(1, 2), Fraction(0))
        i_half = GaussianRat(Fraction(0), Fraction(1, 2))
        mat = [[gi(0) for _ in range(self._dim)] for _ in range(self._dim)]
        for r in range(self._dim):
            for c in range(self._dim):
                mat[r][c] = (g_odd[r][c] * half) + (g_even[r][c] * i_half)
        return mat

    def number_operator(self, j: int) -> list[list[GaussianRat]]:
        # c_j^dagger c_j
        mat = [[gi(0) for _ in range(self._dim)] for _ in range(self._dim)]
        bit_mask = 1 << (self._modes - 1 - (j - 1))
        for state in range(self._dim):
            if (state & bit_mask):
                mat[state][state] = gi(1, 0)
        return mat

    def parity_operator(self) -> list[list[GaussianRat]]:
        # P = (-1)^(n_1 + ... + n_L)
        mat = [[gi(0) for _ in range(self._dim)] for _ in range(self._dim)]
        for state in range(self._dim):
            pop = bin(state).count("1")
            mat[state][state] = gi(1 if pop % 2 == 0 else -1, 0)
        return mat

    def braid_unitary(self, a: int) -> list[list[GaussianRat]]:
        # U_a = ((1 + i)/2) * (I + gamma_(a+1) gamma_a)
        if a < 1 or a >= 2 * self._modes:
            raise MajoranaError(f"braid index {a} out of range")
        g_next = self.majorana_generator(a + 1)
        g_curr = self.majorana_generator(a)
        c = GaussianRat(Fraction(1, 2), Fraction(1, 2))
        mat = [[gi(0) for _ in range(self._dim)] for _ in range(self._dim)]
        for r in range(self._dim):
            for col in range(self._dim):
                prod = gi(0)
                for k in range(self._dim):
                    prod = prod + g_next[r][k] * g_curr[k][col]
                ident = gi(1 if r == col else 0)
                mat[r][col] = (ident + prod) * c
        return mat

    def restrict_to_sector(
        self, op: Sequence[Sequence[GaussianRat]], even: bool
    ) -> list[list[GaussianRat]]:
        indices = [
            s for s in range(self._dim)
            if (bin(s).count("1") % 2 == 0) == even
        ]
        sub = []
        for r in indices:
            sub.append([op[r][c] for c in indices])
        return sub
