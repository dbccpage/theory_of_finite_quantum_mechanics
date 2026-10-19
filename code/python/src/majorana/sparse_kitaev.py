"""Sparse exact open Kitaev wire in Majorana coefficient convention.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

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


@dataclass(frozen=True)
class BoundaryIsolation:
    boundary_modes: Tuple[int, int]
    isolated_modes: Set[int]
    left_generator: Dict[int, Fraction]
    right_generator: Dict[int, Fraction]
    is_sweet_spot: bool

    def left_isolated(self) -> bool:
        return len(self.left_generator) == 0

    def right_isolated(self) -> bool:
        return len(self.right_generator) == 0


class SparseKitaevWire:
    def __init__(self, sites: int, t: Fraction, delta: Fraction, mu: Fraction) -> None:
        if sites < 2 or sites > MAX_WIRE_SITES:
            raise KitaevWireError(f"sites {sites} outside 2..={MAX_WIRE_SITES}")
        self._sites = sites
        self._t = Fraction(t)
        self._delta = Fraction(delta)
        self._mu = Fraction(mu)
        self._terms: dict[MajoranaBilinear, Fraction] = {}
        self._incident: dict[int, list[tuple[MajoranaBilinear, Fraction]]] = {}
        self._build_hamiltonian()

    @classmethod
    def new(cls, sites: int, t: Fraction, mu: Fraction, delta: Fraction) -> "SparseKitaevWire":
        """Constructor matching Rust KitaevWire::new(sites, t, mu, delta) parameter order."""
        return cls(sites=sites, t=t, delta=delta, mu=mu)

    def _build_hamiltonian(self) -> None:
        onsite = -self._mu / 2
        bulk = -(self._t + self._delta) / 2
        cross = (self._t - self._delta) / 2

        if onsite != 0:
            for j in range(1, self._sites + 1):
                term = MajoranaBilinear(2 * j - 1, 2 * j)
                self._terms[term] = onsite

        if bulk != 0:
            for j in range(1, self._sites):
                term = MajoranaBilinear(2 * j, 2 * j + 1)
                self._terms[term] = bulk

        if cross != 0:
            for j in range(1, self._sites):
                term = MajoranaBilinear(2 * j - 1, 2 * j + 2)
                self._terms[term] = cross

        for term, coeff in self._terms.items():
            self._incident.setdefault(term.a, []).append((term, coeff))
            self._incident.setdefault(term.b, []).append((term, coeff))

    def sites(self) -> int:
        return self._sites

    def mode_count(self) -> int:
        return 2 * self._sites

    def is_sweet_spot(self) -> bool:
        return self._mu == 0 and self._t == self._delta and self._t > 0

    def boundary_modes(self) -> Tuple[int, int]:
        return (1, self.mode_count())

    def hamiltonian_terms(self) -> dict[MajoranaBilinear, Fraction]:
        return dict(self._terms)

    def terms(self) -> dict[MajoranaBilinear, Fraction]:
        return self._terms

    def active_modes(self) -> set[int]:
        return set(self._incident.keys())

    def isolated_modes(self) -> set[int]:
        active = self.active_modes()
        return {m for m in range(1, self.mode_count() + 1) if m not in active}

    def commutator_with_generator(self, mode: int) -> dict[int, Fraction]:
        """Compute [H, gamma_mode] = sum_k c_k gamma_k in O(degree(mode)) time."""
        if mode < 1 or mode > self.mode_count():
            raise KitaevWireError(f"mode {mode} outside 1..={self.mode_count()}")
        result: dict[int, Fraction] = {}
        for bilinear, coeff in self._incident.get(mode, ()):
            action = bilinear.generator_on_mode(mode)
            if action is not None:
                scale, target_mode = action
                val = coeff * scale
                result[target_mode] = result.get(target_mode, Fraction(0)) + val
                if result[target_mode] == 0:
                    del result[target_mode]
        return result

    def generator_on_mode(self, mode: int) -> dict[int, Fraction]:
        return self.commutator_with_generator(mode)

    def isolated_majoranas(self) -> list[int]:
        """Modes whose commutator with H is identically zero, sorted in ascending order."""
        return sorted(self.isolated_modes())

    def boundary_isolation(self) -> BoundaryIsolation:
        b_left, b_right = self.boundary_modes()
        return BoundaryIsolation(
            boundary_modes=(b_left, b_right),
            isolated_modes=self.isolated_modes(),
            left_generator=self.generator_on_mode(b_left),
            right_generator=self.generator_on_mode(b_right),
            is_sweet_spot=self.is_sweet_spot(),
        )


KitaevWire = SparseKitaevWire


@dataclass(frozen=True)
class KitaevWireScalingReceipt:
    """Sparse 1D Kitaev wire scaling receipt matching Rust KitaevWireScalingReceipt."""
    sites: int
    mode_count: int
    bilinear_terms: int
    boundary_modes: Tuple[int, int]
    isolated_count: int
    endpoints_isolated: bool
    is_sweet_spot: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sites": self.sites,
            "mode_count": self.mode_count,
            "bilinear_terms": self.bilinear_terms,
            "boundary_modes": [self.boundary_modes[0], self.boundary_modes[1]],
            "isolated_count": self.isolated_count,
            "endpoints_isolated": self.endpoints_isolated,
            "is_sweet_spot": self.is_sweet_spot,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KitaevWireScalingReceipt":
        bm = data["boundary_modes"]
        return cls(
            sites=int(data["sites"]),
            mode_count=int(data["mode_count"]),
            bilinear_terms=int(data["bilinear_terms"]),
            boundary_modes=(int(bm[0]), int(bm[1])),
            isolated_count=int(data["isolated_count"]),
            endpoints_isolated=bool(data["endpoints_isolated"]),
            is_sweet_spot=bool(data["is_sweet_spot"]),
        )


def benchmark_sparse_kitaev_scaling(
    site_counts: Sequence[int],
) -> List[KitaevWireScalingReceipt]:
    """Finite lattice scaling benchmark for sparse 1D Kitaev wires across declared site counts
    up to MAX_WIRE_SITES (65,536 sites = 131,072 Majorana modes).
    Matches Rust tfqm_majorana::benchmark_sparse_kitaev_scaling bit-for-bit.
    """
    one = Fraction(1)
    zero = Fraction(0)
    out: List[KitaevWireScalingReceipt] = []
    for sites in site_counts:
        wire = SparseKitaevWire.new(sites, one, zero, one)
        iso = wire.boundary_isolation()
        endpoints_isolated = (
            iso.left_isolated()
            and iso.right_isolated()
            and (1 in iso.isolated_modes)
            and ((2 * sites) in iso.isolated_modes)
        )
        out.append(
            KitaevWireScalingReceipt(
                sites=sites,
                mode_count=wire.mode_count(),
                bilinear_terms=len(wire.terms()),
                boundary_modes=iso.boundary_modes,
                isolated_count=len(iso.isolated_modes),
                endpoints_isolated=endpoints_isolated,
                is_sweet_spot=iso.is_sweet_spot,
            )
        )
    return out


def sparse_kitaev_scaling_to_canonical_json(rows: Sequence[KitaevWireScalingReceipt]) -> str:
    """Serialize KitaevWireScalingReceipt list to canonical 2-space pretty JSON with LF line endings."""
    return json.dumps([row.to_dict() for row in rows], indent=2)


def sparse_kitaev_scaling_from_canonical_json(json_str: str) -> List[KitaevWireScalingReceipt]:
    """Deserialize KitaevWireScalingReceipt list from canonical JSON string."""
    raw = json.loads(json_str)
    return [KitaevWireScalingReceipt.from_dict(item) for item in raw]

