"""Finite repair-capacity wall demo (QM_102 shadow; CODE_DEMO only).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from .complexes import ChainComplexGf2, surface_grid_2x2_torus, torus_logical_x_example
from .gf2_terminalizer import (
    GF2Matrix,
    GF2ScheduleStatus,
    Gf2CocycleClassifier,
)
from .repair_capacity import repair_capacity_from_distance

AUTHORITY_FENCE = (
    "AuthorityEffect None; finite homology distance bounds unique correction capacity; "
    "LGGR on declared torus only; not a no-go for quantum computing."
)


def hamming_weight(v: Sequence[int]) -> int:
    return sum(b % 2 for b in v)


def apply_d1(d1: GF2Matrix, omega: Sequence[int]) -> list[int]:
    return d1.multiply_vector(omega)


def face_syndrome(d1: GF2Matrix, e: Sequence[int]) -> list[int]:
    return apply_d1(d1, e)


def syndrome_is_zero(d1: GF2Matrix, e: Sequence[int]) -> bool:
    return all(s == 0 for s in face_syndrome(d1, e))


def apply_d0(d0: GF2Matrix, alpha: Sequence[int]) -> list[int]:
    return d0.multiply_vector(alpha)


def in_image_d0(d0: GF2Matrix, omega: Sequence[int]) -> bool:
    return Gf2CocycleClassifier.solve_coboundary(d0, omega) is not None


def solve_d0(d0: GF2Matrix, omega: Sequence[int]) -> Optional[list[int]]:
    return Gf2CocycleClassifier.solve_coboundary(d0, omega)


def is_closed(d1: GF2Matrix, omega: Sequence[int]) -> bool:
    return syndrome_is_zero(d1, omega)


def gf2_add(a: Sequence[int], b: Sequence[int]) -> list[int]:
    if len(a) != len(b):
        raise ValueError(f"gf2_add length mismatch: {len(a)} != {len(b)}")
    return [(x ^ y) & 1 for x, y in zip(a, b)]


def homology_distance(complex: ChainComplexGf2) -> Optional[int]:
    """Exhaustive search for d = min { wt(c) : d1 c = 0, c not in im d0 }."""
    if complex.num_edges > 16:
        raise ValueError("Exhaustive homology distance capped at 16 edges")
    min_wt: Optional[int] = None
    for bitmask in range(1, 1 << complex.num_edges):
        v = [(bitmask >> i) & 1 for i in range(complex.num_edges)]
        if not is_closed(complex.d1, v):
            continue
        if in_image_d0(complex.d0, v):
            continue
        wt = hamming_weight(v)
        if min_wt is None or wt < min_wt:
            min_wt = wt
            if min_wt == 1:
                break
    return min_wt


def repair_capacity_bound(d: int) -> int:
    return repair_capacity_from_distance(d)


def repair_capacity_t(complex: ChainComplexGf2) -> Optional[int]:
    d = homology_distance(complex)
    return repair_capacity_bound(d) if d is not None else None


@dataclass
class RepairCapacityReceipt:
    complex_name: str
    num_edges: int
    homology_distance: Optional[int]
    repair_capacity_t: Optional[int]
    authority_effect: str = "None"
    fence: str = AUTHORITY_FENCE


@dataclass
class HomologyDistanceReport:
    complex_name: str
    d: Optional[int]
    t: Optional[int]
    min_weight_representative: Optional[list[int]]
    q1_dimension: Optional[int] = None
    notes: str = ""

@dataclass
class CosetDecodeDemo:
    complex_name: str
    weight: int
    within_capacity: bool
    unique_repair: bool
    notes: str


@dataclass
class LggrDemoReport:
    complex_name: str
    omega: list[int]
    local_green: bool
    global_red: bool
    is_lggr: bool
    notes: str


def audit_repair_capacity(complex: ChainComplexGf2) -> RepairCapacityReceipt:
    d = homology_distance(complex)
    t = repair_capacity_bound(d) if d is not None else None
    return RepairCapacityReceipt(complex.name, complex.num_edges, d, t)


def coset_decode_demo(complex: ChainComplexGf2, error: Sequence[int]) -> CosetDecodeDemo:
    wt = hamming_weight(error)
    t = repair_capacity_t(complex)
    if t is None:
        return CosetDecodeDemo(complex.name, wt, False, False, "no non-zero homology distance")
    within = (wt <= t)
    return CosetDecodeDemo(complex.name, wt, within, within, "unique decode guaranteed iff wt <= t")


def lggr_demo_torus() -> LggrDemoReport:
    c = surface_grid_2x2_torus()
    omega = torus_logical_x_example()
    return lggr_demo_on(c, omega)


def lggr_demo_on(complex: ChainComplexGf2, omega: Sequence[int]) -> LggrDemoReport:
    closed = is_closed(complex.d1, omega)
    exact = in_image_d0(complex.d0, omega)
    lggr = closed and not exact
    return LggrDemoReport(
        complex.name,
        list(omega),
        local_green=closed,
        global_red=not exact,
        is_lggr=lggr,
        notes="LGGR demonstrated" if lggr else "Not LGGR",
    )
