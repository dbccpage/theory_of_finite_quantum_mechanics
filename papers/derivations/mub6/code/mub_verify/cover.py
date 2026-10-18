"""Gauge-fixed 5-torus geometry, branch-and-bound covering, and coverage validation.

AuthorityEffect: None.
stated region only; mints no authority.

Parametrization:
- Coordinate 0: v_0 is gauge-fixed real-positive at 1/sqrt6:
  x_0 in [4082/10000, 4083/10000], y_0 = 0.
- Coordinates 1..5: v_k on the circle of radius 1/sqrt6:
  x_k, y_k in [-41/100, 41/100].
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, NamedTuple, Optional, Sequence, Tuple

from .interval import (
    RationalInterval,
    VectorBox,
    box_volume,
    boxes_overlap_interior,
)
from .masses import EnclosedTriple
from .mub_triples import D


def circle_box() -> RationalInterval:
    """Bounding interval for circle of radius 1/sqrt6: [-41/100, 41/100]."""
    return RationalInterval(Fraction(-41, 100), Fraction(41, 100))


def r_bracket() -> RationalInterval:
    """Tight rational bracket of 1/sqrt6: [4082/10000, 4083/10000]."""
    return RationalInterval(Fraction(4082, 10000), Fraction(4083, 10000))


def gauge_fixed_torus_region() -> VectorBox:
    """Gauge-fixed 5-torus candidate domain in 12 real coordinates."""
    coords: List[RationalInterval] = [circle_box() for _ in range(12)]
    coords[0] = r_bracket()
    coords[1] = RationalInterval.point(Fraction(0, 1))
    return tuple(coords)


def narrow_torus_cell() -> VectorBox:
    """Narrow torus cell: [26/100, 30/100] across all 12 coordinates."""
    lo = Fraction(26, 100)
    hi = Fraction(30, 100)
    iv = RationalInterval(lo, hi)
    return tuple(iv for _ in range(12))


def wide_torus_cell() -> VectorBox:
    """Wide torus cell: [10/100, 46/100] across all 12 coordinates."""
    lo = Fraction(10, 100)
    hi = Fraction(46, 100)
    iv = RationalInterval(lo, hi)
    return tuple(iv for _ in range(12))


def box_touches_torus(vbox: VectorBox) -> bool:
    """True iff vbox can contain a vector mutually unbiased to B1.

    For every coordinate k in 0..5, |v_k|^2 = x_k^2 + y_k^2 must bracket 1/6.
    If any coordinate fails, the box holds no B1-unbiased vector and is off-torus.
    """
    sixth = Fraction(1, 6)
    for k in range(D):
        x = vbox[2 * k]
        y = vbox[2 * k + 1]
        mod_sq = x.sq().add(y.sq())
        if mod_sq.lo > sixth or mod_sq.hi < sixth:
            return False
    return True


def split_widest(vbox: VectorBox) -> Tuple[VectorBox, VectorBox]:
    """Bisect vbox along its coordinate of maximal width.

    Ties broken by selecting the lowest coordinate index.
    """
    wi = 0
    max_w = vbox[0].width()
    for i in range(1, len(vbox)):
        w = vbox[i].width()
        if w > max_w:
            max_w = w
            wi = i

    mid = (vbox[wi].lo + vbox[wi].hi) * Fraction(1, 2)

    box_a = list(vbox)
    box_b = list(vbox)
    box_a[wi] = RationalInterval(vbox[wi].lo, mid)
    box_b[wi] = RationalInterval(mid, vbox[wi].hi)

    return (tuple(box_a), tuple(box_b))


def presplit_region(region: VectorBox, depth: int) -> List[VectorBox]:
    """Decompose region into 2^depth independent sub-regions by repeated bisection."""
    chunks = [region]
    for _ in range(depth):
        next_chunks: List[VectorBox] = []
        for c in chunks:
            a, b = split_widest(c)
            next_chunks.append(a)
            next_chunks.append(b)
        chunks = next_chunks
    return chunks


class CertifiedBox(NamedTuple):
    box: VectorBox
    gap: Fraction
    depth: int


class CoverReport(NamedTuple):
    certified_boxes: List[CertifiedBox]
    off_torus_boxes: List[Tuple[VectorBox, int]]
    uncertified_boxes: List[Tuple[VectorBox, int]]
    min_gap: Optional[Fraction]
    max_depth_used: int

    @property
    def certified_count(self) -> int:
        return len(self.certified_boxes)

    @property
    def off_torus_count(self) -> int:
        return len(self.off_torus_boxes)

    @property
    def uncertified_count(self) -> int:
        return len(self.uncertified_boxes)

    @property
    def is_complete(self) -> bool:
        return len(self.uncertified_boxes) == 0


def cover_region(
    enc: EnclosedTriple,
    region: VectorBox,
    max_depth: int,
    store_all_boxes: bool = True,
) -> CoverReport:
    """Cover region by branch-and-bound subdivision.

    1. Discard if not box_touches_torus (off-torus).
    2. Try to certify with enc (positive f_gap).
    3. If depth >= max_depth, record uncertified.
    4. Else split widest coordinate and recurse.
    """
    stack: List[Tuple[VectorBox, int]] = [(region, 0)]
    certified_boxes: List[CertifiedBox] = []
    off_torus_boxes: List[Tuple[VectorBox, int]] = []
    uncertified_boxes: List[Tuple[VectorBox, int]] = []
    min_gap: Optional[Fraction] = None
    max_depth_used = 0

    while stack:
        vbox, depth = stack.pop()
        if depth > max_depth_used:
            max_depth_used = depth

        if not box_touches_torus(vbox):
            if store_all_boxes:
                off_torus_boxes.append((vbox, depth))
            continue

        gap = enc.certify_vector_box(vbox)
        if gap is not None:
            if store_all_boxes:
                certified_boxes.append(CertifiedBox(vbox, gap, depth))
            if min_gap is None or gap < min_gap:
                min_gap = gap
            continue

        if depth >= max_depth:
            uncertified_boxes.append((vbox, depth))
        else:
            a, b = split_widest(vbox)
            stack.append((a, depth + 1))
            stack.append((b, depth + 1))

    return CoverReport(
        certified_boxes=certified_boxes,
        off_torus_boxes=off_torus_boxes,
        uncertified_boxes=uncertified_boxes,
        min_gap=min_gap,
        max_depth_used=max_depth_used,
    )


def active_box_volume(box: VectorBox, active_coords: Sequence[int]) -> Fraction:
    """Exact volume of box along active (non-degenerate) coordinates."""
    vol = Fraction(1, 1)
    for k in active_coords:
        vol *= box[k].width()
    return vol


def verify_full_coverage(
    domain: VectorBox,
    certified_boxes: Sequence[VectorBox],
    off_torus_boxes: Sequence[VectorBox],
) -> Tuple[bool, str]:
    """Verify that union of certified and off-torus boxes equals domain with zero gaps and no overlap.

    Returns (success, message).
    """
    all_leaves = list(certified_boxes) + list(off_torus_boxes)
    if not all_leaves:
        return False, "Empty leaf collection"

    active_coords = [k for k in range(len(domain)) if domain[k].width() > 0]
    if not active_coords:
        return False, "Domain has zero volume in all coordinates (degenerate domain)"

    domain_vol = active_box_volume(domain, active_coords)
    total_leaf_vol = Fraction(0, 1)

    for i, leaf in enumerate(all_leaves):
        for k in range(len(domain)):
            if leaf[k].lo < domain[k].lo or leaf[k].hi > domain[k].hi:
                return False, f"Leaf {i} exceeds domain bounds on coordinate {k}"
            if domain[k].width() == 0 and (leaf[k].lo != domain[k].lo or leaf[k].hi != domain[k].hi):
                return False, f"Leaf {i} violates fixed coordinate {k}"
        total_leaf_vol += active_box_volume(leaf, active_coords)

    if total_leaf_vol != domain_vol:
        return (
            False,
            f"Volume mismatch: sum of leaves = {total_leaf_vol}, domain = {domain_vol}, diff = {total_leaf_vol - domain_vol}",
        )

    n = len(all_leaves)
    for i in range(n):
        for j in range(i + 1, n):
            overlap = True
            for k in active_coords:
                if not all_leaves[i][k].overlaps_interior(all_leaves[j][k]):
                    overlap = False
                    break
            if overlap:
                return False, f"Leaves {i} and {j} overlap in interior"

    return True, f"Full coverage verified: {len(all_leaves)} leaves ({len(certified_boxes)} certified, {len(off_torus_boxes)} off-torus), exact volume match {domain_vol}, zero gaps, zero double-counting."
