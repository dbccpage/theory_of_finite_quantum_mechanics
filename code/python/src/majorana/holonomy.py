"""Discrete holonomy residual on a declared face.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .complexes import ChainComplexGf2
from .gf2_terminalizer import (
    Cyclotomic16Element,
    GF2Matrix,
    GF2ScheduleStatus,
    Gf2CocycleClassifier,
)

HOLONOMY_RECEIPT_TAG = "omega.majorana-holonomy-receipt.v1"
AUTHORITY_FENCE = "AuthorityEffect None; declared carrier + monoid only; diagnostic receipt."


@dataclass
class HolonomyReceiptGf2:
    certificate_tag: str
    complex_name: str
    connection: list[int]
    face_residuals: list[int]
    flat: bool
    residual_weight: int
    boundary_valid: bool
    authority_effect: str = "None"
    notes: str = ""


@dataclass
class HolonomyReceiptCyclotomic:
    certificate_tag: str
    face_index: int
    edge_walk: list[int]
    product_coeffs: list[int]
    flat: bool
    authority_effect: str = "None"
    notes: str = ""


def face_edge_support(d1: GF2Matrix, face_idx: int) -> list[int]:
    if face_idx >= d1.rows:
        raise ValueError(f"Face index {face_idx} out of range {d1.rows}")
    return [c for c in range(d1.cols) if d1.data[face_idx][c] == 1]


def face_holonomy_residual_gf2(
    d1: GF2Matrix, face_idx: int, connection: Sequence[int]
) -> int:
    supp = face_edge_support(d1, face_idx)
    return sum(connection[e] % 2 for e in supp) % 2


def gauge_transform_gf2(
    d0: GF2Matrix, connection: Sequence[int], vertex_gauge: Sequence[int]
) -> list[int]:
    delta = d0.multiply_vector(vertex_gauge)
    return [(c ^ d) & 1 for c, d in zip(connection, delta)]


def holonomy_receipt_gf2(
    complex: ChainComplexGf2, connection: Sequence[int]
) -> HolonomyReceiptGf2:
    if len(connection) != complex.num_edges:
        raise ValueError("Connection length does not match complex edges")
    boundary_valid = complex.verify_boundary()
    face_residuals = complex.d1.multiply_vector(connection)
    flat = all(r == 0 for r in face_residuals)
    res_wt = sum(face_residuals)
    return HolonomyReceiptGf2(
        certificate_tag=HOLONOMY_RECEIPT_TAG,
        complex_name=complex.name,
        connection=list(connection),
        face_residuals=face_residuals,
        flat=flat,
        residual_weight=res_wt,
        boundary_valid=boundary_valid,
        notes="flat holonomy" if flat else "non-flat holonomy residual present",
    )


def holonomy_receipt_cyclotomic_face0(
    complex: ChainComplexGf2,
    edge_cyclotomic_coeffs: Sequence[Sequence[int]],
) -> HolonomyReceiptCyclotomic:
    if complex.num_faces == 0:
        raise ValueError("Complex has no faces")
    walk = face_edge_support(complex.d1, 0)
    prod = Cyclotomic16Element.one()
    for e in walk:
        elem = Cyclotomic16Element(tuple(edge_cyclotomic_coeffs[e]))
        prod = prod.multiply(elem)
    flat = (prod == Cyclotomic16Element.one())
    return HolonomyReceiptCyclotomic(
        certificate_tag=HOLONOMY_RECEIPT_TAG,
        face_index=0,
        edge_walk=walk,
        product_coeffs=list(prod.coeffs),
        flat=flat,
        notes="cyclotomic face holonomy computed",
    )


def connect_to_schedule_class(
    complex: ChainComplexGf2, connection: Sequence[int]
) -> GF2ScheduleStatus:
    receipt = Gf2CocycleClassifier.classify(complex.d0, complex.d1, connection)
    return receipt.schedule_status
