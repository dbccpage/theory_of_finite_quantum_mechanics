"""Sparse exact open Kitaev wire in Majorana coefficient convention.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

MAX_WIRE_SITES: int = 65_536


class KitaevWireError(Exception):
    pass


@dataclass(frozen=True)
class MajoranaBilinear:
    a: int  # 1-indexed, a < b
    b: int

    def __post_init__(self) -> None:
        if self.a < 1 or self.a >= self.b:
            raise KitaevWireError(f"Bilinear requires 1 <= a < b, got ({self.a}, {self.b})")

    def mode_a(self) -> int:
        return self.a

    def mode_b(self) -> int:
        return self.b

    def generator_on_mode(self, mode: int) -> Optional[tuple[int, int]]:
        """Real coefficient and target in i [i gamma_a gamma_b, gamma_mode]."""
        if mode == self.a:
            return (2, self.b)
        elif mode == self.b:
            return (-2, self.a)
        return None


class SparseKitaevWire:
    def __init__(self, sites: int, t: Fraction, delta: Fraction, mu: Fraction) -> None:
        if sites < 2 or sites > MAX_WIRE_SITES:
            raise KitaevWireError(f"sites {sites} outside 2..={MAX_WIRE_SITES}")
        self._sites = sites
        self._t = t
        self._delta = delta
        self._mu = mu
        self._terms: dict[MajoranaBilinear, Fraction] = {}
        self._build_hamiltonian()

    def _build_hamiltonian(self) -> None:
        # H = -N mu/2 I + sum_(a<b) h_ab i gamma_a gamma_b
        # On-site chemical potential:
        # h_(2j-1, 2j) = -mu / 2
        for j in range(1, self._sites + 1):
            g_odd = 2 * j - 1
            g_even = 2 * j
            self._terms[MajoranaBilinear(g_odd, g_even)] = -self._mu / 2

        # Hopping and pairing between site j and j+1:
        # h_(2j, 2j+1) = -(t + delta) / 2
        # h_(2j-1, 2j+2) = (t - delta) / 2
        for j in range(1, self._sites):
            g_even_j = 2 * j
            g_odd_next = 2 * j + 1
            self._terms[MajoranaBilinear(g_even_j, g_odd_next)] = -(self._t + self._delta) / 2

            g_odd_j = 2 * j - 1
            g_even_next = 2 * j + 2
            self._terms[MajoranaBilinear(g_odd_j, g_even_next)] = (self._t - self._delta) / 2

        # Filter out 0 terms
        self._terms = {k: v for k, v in self._terms.items() if v != 0}

    def sites(self) -> int:
        return self._sites

    def mode_count(self) -> int:
        return 2 * self._sites

    def hamiltonian_terms(self) -> dict[MajoranaBilinear, Fraction]:
        return dict(self._terms)

    def commutator_with_generator(self, mode: int) -> dict[int, Fraction]:
        """Compute [H, gamma_mode] = sum_k c_k gamma_k."""
        if mode < 1 or mode > self.mode_count():
            raise KitaevWireError(f"mode {mode} outside 1..={self.mode_count()}")
        result: dict[int, Fraction] = {}
        for bilinear, coeff in self._terms.items():
            action = bilinear.generator_on_mode(mode)
            if action is not None:
                scale, target_mode = action
                val = coeff * scale
                result[target_mode] = result.get(target_mode, Fraction(0)) + val
                if result[target_mode] == 0:
                    del result[target_mode]
        return result

    def isolated_majoranas(self) -> list[int]:
        """Modes whose commutator with H is identically zero."""
        isolated = []
        for m in range(1, self.mode_count() + 1):
            comm = self.commutator_with_generator(m)
            if len(comm) == 0:
                isolated.append(m)
        return isolated
