"""End-to-end residual classifier: residual -> terminal + receipt.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence

from .gf2_terminalizer import (
    GF2Matrix,
    GF2ScheduleStatus,
    Gf2CocycleClassifier,
)
from .harmonic import (
    DEFAULT_BUDGET,
    H1Basis,
    h1_basis,
    l1_harmonic_projection,
)

CLASSIFIED_RECEIPT_TAG = "omega.majorana-tetron-classified.v1"


class Terminal(str, Enum):
    Exact = "Exact"
    OpenObstruction = "OpenObstruction"
    ClosedResidual = "ClosedResidual"
    TypedHarmonic = "TypedHarmonic"
    RepresentationInvalid = "RepresentationInvalid"

    def reading(self) -> str:
        readings = {
            Terminal.Exact: "pure gauge: an MZM reference-frame relabelling; no defect",
            Terminal.OpenObstruction: (
                "an island parity constraint is violated; a localized violated "
                "declared island parity relation, named by the coherence witness; "
                "physical cause UNDETERMINED"
            ),
            Terminal.ClosedResidual: (
                "consistent with every island constraint but not gauge: a logical "
                "parity error whose minimum weight was not certified"
            ),
            Terminal.TypedHarmonic: (
                "a logical parity error, identified in the H^1 basis, with a "
                "certified minimum-weight witness"
            ),
            Terminal.RepresentationInvalid: "the declared carrier is not a cochain complex",
        }
        return readings[self]


@dataclass
class ClassifiedReceipt:
    certificate_tag: str
    terminal: Terminal
    terminal_reading: str
    boundary_valid: bool
    num_edges: int
    residual: list[int]
    face_syndrome: list[int]
    dim_h1: Optional[int]
    class_id: Optional[int]
    class_coordinates: Optional[list[int]]
    phi1_min_weight: Optional[int]
    phi1_representative: Optional[list[int]]
    phi1_certified: bool
    authority_effect: str = "None"


def classify(
    d0: GF2Matrix, d1: GF2Matrix, residual: Sequence[int], budget: int = DEFAULT_BUDGET
) -> ClassifiedReceipt:
    num_edges = len(residual)
    if d0.rows != num_edges or d1.cols != num_edges or not Gf2CocycleClassifier.verify_boundary(d0, d1):
        term = Terminal.RepresentationInvalid
        return ClassifiedReceipt(
            certificate_tag=CLASSIFIED_RECEIPT_TAG,
            terminal=term,
            terminal_reading=term.reading(),
            boundary_valid=False,
            num_edges=num_edges,
            residual=list(residual),
            face_syndrome=[],
            dim_h1=None,
            class_id=None,
            class_coordinates=None,
            phi1_min_weight=None,
            phi1_representative=None,
            phi1_certified=False,
        )

    syndrome = d1.multiply_vector(residual)
    if any(s != 0 for s in syndrome):
        term = Terminal.OpenObstruction
        return ClassifiedReceipt(
            certificate_tag=CLASSIFIED_RECEIPT_TAG,
            terminal=term,
            terminal_reading=term.reading(),
            boundary_valid=True,
            num_edges=num_edges,
            residual=list(residual),
            face_syndrome=syndrome,
            dim_h1=None,
            class_id=None,
            class_coordinates=None,
            phi1_min_weight=None,
            phi1_representative=None,
            phi1_certified=False,
        )

    # Closed residual: check if exact
    if Gf2CocycleClassifier.solve_coboundary(d0, residual) is not None:
        term = Terminal.Exact
        return ClassifiedReceipt(
            certificate_tag=CLASSIFIED_RECEIPT_TAG,
            terminal=term,
            terminal_reading=term.reading(),
            boundary_valid=True,
            num_edges=num_edges,
            residual=list(residual),
            face_syndrome=syndrome,
            dim_h1=None,
            class_id=None,
            class_coordinates=None,
            phi1_min_weight=0,
            phi1_representative=[0] * num_edges,
            phi1_certified=True,
        )

    # Closed and non-exact: classify in H^1
    basis = h1_basis(d0, d1)
    if basis.dim_h1 == 0:
        term = Terminal.ClosedResidual
        return ClassifiedReceipt(
            certificate_tag=CLASSIFIED_RECEIPT_TAG,
            terminal=term,
            terminal_reading=term.reading(),
            boundary_valid=True,
            num_edges=num_edges,
            residual=list(residual),
            face_syndrome=syndrome,
            dim_h1=0,
            class_id=None,
            class_coordinates=None,
            phi1_min_weight=None,
            phi1_representative=None,
            phi1_certified=False,
        )

    proj = l1_harmonic_projection(d0, d1, basis, residual, budget)
    if proj.exact_within_budget:
        term = Terminal.TypedHarmonic
        return ClassifiedReceipt(
            certificate_tag=CLASSIFIED_RECEIPT_TAG,
            terminal=term,
            terminal_reading=term.reading(),
            boundary_valid=True,
            num_edges=num_edges,
            residual=list(residual),
            face_syndrome=syndrome,
            dim_h1=basis.dim_h1,
            class_id=proj.class_id,
            class_coordinates=proj.class_coordinates,
            phi1_min_weight=proj.phi1_min_weight,
            phi1_representative=proj.representative,
            phi1_certified=True,
        )
    else:
        term = Terminal.ClosedResidual
        return ClassifiedReceipt(
            certificate_tag=CLASSIFIED_RECEIPT_TAG,
            terminal=term,
            terminal_reading=term.reading(),
            boundary_valid=True,
            num_edges=num_edges,
            residual=list(residual),
            face_syndrome=syndrome,
            dim_h1=basis.dim_h1,
            class_id=proj.class_id,
            class_coordinates=proj.class_coordinates,
            phi1_min_weight=proj.phi1_min_weight,
            phi1_representative=proj.representative,
            phi1_certified=False,
        )


def classify_default(d0: GF2Matrix, d1: GF2Matrix, residual: Sequence[int]) -> ClassifiedReceipt:
    return classify(d0, d1, residual, DEFAULT_BUDGET)


def classify_with_diagnostics(
    d0: GF2Matrix, d1: GF2Matrix, residual: Sequence[int], budget: int = DEFAULT_BUDGET
) -> ClassifiedReceipt:
    return classify(d0, d1, residual, budget)
