"""Evidence-only evaluation of projection and endomorphism obstructions."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any

import numpy as np

from omega_engine.crates.operator.lambda_op.lamb_chain_obstruction import (
    compute_po_015_projection_obstruction,
)
from omega_engine.crates.type.solver_kernel import (
    AUTHORITY_EFFECT_NONE,
    EVIDENCE_ONLY,
)


@dataclass(frozen=True)
class ProjectionObstructionReceipt:
    po_015_norm: float
    endomorphism_class: str
    presentation_axis: int
    is_non_retractable: bool
    evidence_sha256: str = ""
    evidence_class: str = field(default=EVIDENCE_ONLY, init=False)
    authority_effect: str = field(default=AUTHORITY_EFFECT_NONE, init=False)

    def __post_init__(self) -> None:
        if self.presentation_axis not in range(1, 6):
            raise ValueError("presentation_axis must be in range 1..5")
        if not self.evidence_sha256:
            payload = {
                "authority_effect": self.authority_effect,
                "endomorphism_class": self.endomorphism_class,
                "is_non_retractable": self.is_non_retractable,
                "po_015_norm": self.po_015_norm,
                "presentation_axis": self.presentation_axis,
            }
            encoded = json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
            object.__setattr__(self, "evidence_sha256", sha256(encoded).hexdigest())


def evaluate_endomorphism_cohomology(
    differential: Sequence[Sequence[Any]],
    endomorphism: Sequence[Sequence[Any]],
    *,
    tolerance: float = 1e-12,
) -> str:
    """Classify a finite float-profile endomorphism candidate."""

    differential_array = np.asarray(differential, dtype=float)
    endomorphism_array = np.asarray(endomorphism, dtype=float)
    if differential_array.shape != endomorphism_array.shape:
        raise ValueError("differential and endomorphism shapes must match")
    if not np.isfinite(differential_array).all() or not np.isfinite(
        endomorphism_array
    ).all():
        raise ValueError("endomorphism inputs must be finite")

    commutator = (
        differential_array @ endomorphism_array
        - endomorphism_array @ differential_array
    )
    if float(np.linalg.norm(commutator)) > tolerance:
        return "P_NONCLOSED"
    if float(np.linalg.norm(endomorphism_array)) <= tolerance:
        return "P_EXACT"
    return "P_CLOSED_NONEXACT"


def build_projection_obstruction_receipt(
    differential: Sequence[Sequence[Any]],
    projection: Sequence[Sequence[Any]],
    endomorphism: Sequence[Sequence[Any]],
    *,
    presentation_axis: int = 1,
    tolerance: float = 1e-12,
) -> ProjectionObstructionReceipt:
    is_subcomplex, obstruction_norm = compute_po_015_projection_obstruction(
        differential,
        projection,
        tolerance=tolerance,
    )
    endomorphism_class = evaluate_endomorphism_cohomology(
        differential,
        endomorphism,
        tolerance=tolerance,
    )
    return ProjectionObstructionReceipt(
        po_015_norm=obstruction_norm,
        endomorphism_class=endomorphism_class,
        presentation_axis=presentation_axis,
        is_non_retractable=(
            not is_subcomplex or endomorphism_class != "P_EXACT"
        ),
    )


__all__ = [
    "ProjectionObstructionReceipt",
    "build_projection_obstruction_receipt",
    "evaluate_endomorphism_cohomology",
]
