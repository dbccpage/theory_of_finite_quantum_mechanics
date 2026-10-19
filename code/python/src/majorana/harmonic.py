"""l1 harmonic projection and cohomology-class typing over GF(2).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

from .gf2_terminalizer import GF2Matrix, Gf2CocycleClassifier

DEFAULT_BUDGET: int = 1 << 22
_U64_MAX: int = (1 << 64) - 1


def _high_bit(mask: int) -> Optional[int]:
    if mask <= 0:
        return None
    return mask.bit_length() - 1


def _slice_to_mask(values: Sequence[int]) -> int:
    mask = 0
    for idx, val in enumerate(values):
        if val % 2 == 1:
            mask |= 1 << idx
    return mask


class _Span:
    def __init__(self, width: int) -> None:
        self.pivots: List[Optional[Tuple[int, int]]] = [None] * max(width, 1)

    def reduce(self, mask: int) -> Tuple[int, int]:
        residue = mask
        tag = 0
        while True:
            high = _high_bit(residue)
            if high is None or high >= len(self.pivots):
                break
            slot = self.pivots[high]
            if slot is None:
                break
            pivot_mask, pivot_tag = slot
            residue ^= pivot_mask
            tag ^= pivot_tag
        return residue, tag

    def insert(self, mask: int, tag: int) -> bool:
        residue, accumulated = self.reduce(mask)
        independent = residue != 0
        high = _high_bit(residue)
        if high is not None:
            combined = tag ^ accumulated
            self.pivots[high] = (residue, combined)
        return independent


def _image_basis(d0: GF2Matrix) -> List[Tuple[int, int]]:
    span = _Span(max(d0.rows, 1))
    basis: List[Tuple[int, int]] = []
    for col in range(d0.cols):
        mask = 0
        for row in range(d0.rows):
            if d0.data[row][col] % 2 == 1:
                mask |= 1 << row
        residue, accumulated = span.reduce(mask)
        high = _high_bit(residue)
        if high is not None:
            alpha = (1 << col) ^ accumulated
            span.pivots[high] = (residue, alpha)
            basis.append((residue, alpha))
    return basis


def _kernel_basis(d1: GF2Matrix, num_channels: int) -> List[List[int]]:
    if d1.rows == 0:
        out = []
        for idx in range(num_channels):
            v = [0] * num_channels
            v[idx] = 1
            out.append(v)
        return out
    reduced, _, _ = d1.row_reduce()
    pivot_of_row: List[Tuple[int, int]] = []
    pivot_columns: List[int] = []
    for row in range(reduced.rows):
        col_found = None
        for c in range(reduced.cols):
            if reduced.data[row][c] == 1:
                col_found = c
                break
        if col_found is not None:
            pivot_of_row.append((row, col_found))
            pivot_columns.append(col_found)
    pivot_set = set(pivot_columns)
    basis: List[List[int]] = []
    for free in range(num_channels):
        if free in pivot_set:
            continue
        vec = [0] * num_channels
        vec[free] = 1
        for r, c in pivot_of_row:
            vec[c] = reduced.data[r][free]
        basis.append(vec)
    return basis


@dataclass
class H1Basis:
    dim: int
    generators: List[List[int]]
    num_channels: int
    _span: _Span

    @property
    def dim_h1(self) -> int:
        return self.dim

    def class_coordinates(self, residual: Sequence[int]) -> Optional[List[int]]:
        if len(residual) != self.num_channels:
            return None
        remainder, tag = self._span.reduce(_slice_to_mask(residual))
        if remainder != 0:
            return None
        return [(tag >> idx) & 1 for idx in range(self.dim)]

    def class_representative(self, coordinates: Sequence[int]) -> List[int]:
        vec = [0] * self.num_channels
        for idx in range(min(len(coordinates), self.dim)):
            if coordinates[idx] % 2 == 1:
                gen = self.generators[idx]
                for slot in range(self.num_channels):
                    vec[slot] ^= gen[slot]
        return vec

    @staticmethod
    def class_id(coordinates: Sequence[int]) -> str:
        bits = "".join("1" if (b % 2 == 1) else "0" for b in coordinates)
        return f"h1:{bits}"


def h1_basis(d0: GF2Matrix, d1: GF2Matrix) -> H1Basis:
    num_channels = d0.rows
    span = _Span(max(num_channels, 1))
    generators: List[List[int]] = []

    for channel_mask, _alpha in _image_basis(d0):
        span.insert(channel_mask, 0)

    for vector in _kernel_basis(d1, num_channels):
        mask = _slice_to_mask(vector)
        tag = 1 << len(generators)
        if span.insert(mask, tag):
            generators.append(vector)

    return H1Basis(
        dim=len(generators),
        generators=generators,
        num_channels=num_channels,
        _span=span,
    )


@dataclass
class L1HarmonicProjection:
    weight: int
    representative: List[int]
    alpha: List[int]
    exact: bool
    searched: int
    coset_size: int
    authority_effect: str = "None"

    @property
    def phi1_min_weight(self) -> int:
        return self.weight

    @property
    def exact_within_budget(self) -> bool:
        return self.exact

    @property
    def coset_elements_evaluated(self) -> int:
        return self.searched


def _binary_coset_projection(
    d0: GF2Matrix, residual: Sequence[int], budget: int
) -> L1HarmonicProjection:
    if budget <= 0:
        raise ValueError("budget must be >= 1")
    rows = d0.data
    columns = d0.cols
    if len(rows) != len(residual) or any(len(r) != columns for r in rows):
        raise ValueError("binary coset dimensions differ")

    pivots: List[Optional[Tuple[List[int], List[int]]]] = [None] * len(rows)
    basis: List[Tuple[List[int], List[int]]] = []
    for col in range(columns):
        image = [row[col] % 2 for row in rows]
        source = [0] * columns
        source[col] = 1
        for high in range(len(rows) - 1, -1, -1):
            if image[high] == 0:
                continue
            slot = pivots[high]
            if slot is not None:
                pivot, witness = slot
                for idx in range(len(image)):
                    image[idx] ^= pivot[idx]
                for idx in range(columns):
                    source[idx] ^= witness[idx]
            else:
                pivots[high] = (list(image), list(source))
                basis.append((image, source))
                break

    rank = len(basis)
    coset_size = (1 << rank) if rank < 64 else _U64_MAX
    limit = min(coset_size, budget)

    current = [x % 2 for x in residual]
    alpha = [0] * columns
    best = list(current)
    best_alpha = list(alpha)
    best_weight = sum(1 for x in best if x != 0)

    for step in range(1, limit):
        tz = (step & -step).bit_length() - 1
        image, source = basis[tz]
        for idx in range(len(current)):
            current[idx] ^= image[idx]
        for idx in range(columns):
            alpha[idx] ^= source[idx]
        weight = sum(1 for x in current if x != 0)
        if weight < best_weight or (weight == best_weight and current[::-1] < best[::-1]):
            best_weight = weight
            best = list(current)
            best_alpha = list(alpha)

    return L1HarmonicProjection(
        weight=best_weight,
        representative=best,
        alpha=best_alpha,
        exact=(rank < 64 and coset_size <= budget),
        searched=limit,
        coset_size=coset_size,
        authority_effect="None",
    )


def l1_harmonic_projection(
    d0: GF2Matrix,
    residual_or_d1: Sequence[int] | GF2Matrix,
    budget_or_basis: int | H1Basis = DEFAULT_BUDGET,
    residual: Optional[Sequence[int]] = None,
    budget: int = DEFAULT_BUDGET,
) -> L1HarmonicProjection:
    if isinstance(residual_or_d1, GF2Matrix):
        if residual is None:
            raise ValueError("residual is required when calling 5-argument l1_harmonic_projection")
        return _binary_coset_projection(d0, residual, int(budget))
    return _binary_coset_projection(d0, residual_or_d1, int(budget_or_basis))  # type: ignore[arg-type]


def code_distance(
    d0: GF2Matrix,
    d1: GF2Matrix,
    budget_or_basis: int | H1Basis = DEFAULT_BUDGET,
    budget: int = DEFAULT_BUDGET,
) -> Tuple[Optional[int], bool]:
    if isinstance(budget_or_basis, H1Basis):
        basis = budget_or_basis
        eff_budget = budget
    else:
        basis = h1_basis(d0, d1)
        eff_budget = int(budget_or_basis)

    if basis.dim == 0:
        return None, True
    if basis.dim >= 64:
        raise ValueError("code distance refused: dim H^1 >= 64 does not fit an exact class enumeration")

    best: Optional[int] = None
    all_exact = True
    for code in range(1, 1 << basis.dim):
        coordinates = [(code >> idx) & 1 for idx in range(basis.dim)]
        rep = basis.class_representative(coordinates)
        proj = _binary_coset_projection(d0, rep, eff_budget)
        all_exact = all_exact and proj.exact
        best = proj.weight if best is None else min(best, proj.weight)
    return best, all_exact
