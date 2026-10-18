"""Rank calculation and numerical rank verification for linear operators.

Companion to ``omega_engine/crates_rs/omega_linear_algebra/src/linear_algebra/rank.rs``.

RELATIONSHIP TO THE RUST SOURCE, restated. This module previously declared
"The Rust module is the behavioral specification. Generated symbols fail closed
where behavior has not been implemented.", and inherited a fail-closed base that
raised NotImplementedError for anything unimplemented. That declaration was
dropped when the NumPy implementation landed, while the Rust source and 163
sibling files kept the same pattern.

The implementation below is real, so failing closed is no longer right -- but
the specification relationship still holds and is restated here rather than left
implicit. RESIDUAL: no test compares this implementation against the Rust one,
so the two can disagree about the rank of a matrix with nothing detecting it.
That matters because rank decides cohomology dimensions elsewhere in this
package. Prefer the exact rational rank in
``omega_engine.crates.homology_theory.qmatrix.QMatrix.rank`` when the input is
exact data rather than a noisy measurement; the SVD path here is for the
genuinely numerical case, and its default tolerance scales as
``max(rows, cols) * sigma_max * eps``.

AuthorityEffect: None.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Sequence, Tuple
import numpy as np


NumericalRankError = Enum(
    "NumericalRankError",
    {
        "InvalidTolerance": "InvalidTolerance",
        "NonFiniteEntry": "NonFiniteEntry",
        "NonFiniteSingularValue": "NonFiniteSingularValue",
    },
    type=str,
)
NumericalRankError.__doc__ = (
    "Error variants, mirroring Rust ``NumericalRankError``."
)


@dataclass
class NumericalRankReport:
    """Report of numerical rank and singular value spectrum."""

    rank: int
    tolerance: float
    rows: int
    cols: int
    singular_values: List[float]

    @property
    def smallest_counted_singular_value(self) -> float:
        if self.rank > 0 and self.rank <= len(self.singular_values):
            return float(self.singular_values[self.rank - 1])
        return 0.0

    @property
    def largest_rejected_singular_value(self) -> float:
        if self.rank < len(self.singular_values):
            return float(self.singular_values[self.rank])
        return 0.0

    @property
    def threshold_margin(self) -> float:
        return self.smallest_counted_singular_value - self.largest_rejected_singular_value


def compute_numerical_rank(matrix: Any, tol: Optional[float] = None) -> NumericalRankReport:
    """Computes the numerical rank and singular value profile of a matrix via SVD."""
    mat = np.asarray(matrix, dtype=float)
    if mat.ndim != 2:
        raise ValueError(f"Expected 2D matrix, got shape {mat.shape}")
    if not np.all(np.isfinite(mat)):
        raise ValueError("Matrix contains non-finite entries")
    rows, cols = mat.shape
    if rows == 0 or cols == 0:
        return NumericalRankReport(rank=0, tolerance=0.0, rows=rows, cols=cols, singular_values=[])

    s = np.linalg.svd(mat, compute_uv=False)
    s_list = [float(v) for v in s]

    if tol is None:
        eps = np.finfo(float).eps
        tol = float(max(rows, cols) * s_list[0] * eps) if s_list else 1e-12

    if tol < 0:
        raise ValueError("Tolerance must be non-negative")

    r = int(np.sum(s > tol))
    return NumericalRankReport(
        rank=r,
        tolerance=float(tol),
        rows=rows,
        cols=cols,
        singular_values=s_list,
    )


def rank(matrix: Any, tol: Optional[float] = None) -> int:
    """Returns the numerical rank of a matrix."""
    return compute_numerical_rank(matrix, tol).rank


def tolerance(matrix: Any) -> float:
    """Returns default singular value threshold tolerance."""
    return compute_numerical_rank(matrix).tolerance


def shape(matrix: Any) -> Tuple[int, int]:
    """Returns matrix shape (rows, cols)."""
    rep = compute_numerical_rank(matrix)
    return (rep.rows, rep.cols)


def singular_values(matrix: Any) -> List[float]:
    """Returns singular values in descending order."""
    return compute_numerical_rank(matrix).singular_values


def smallest_counted_singular_value(matrix: Any, tol: Optional[float] = None) -> float:
    """Returns the smallest counted singular value."""
    return compute_numerical_rank(matrix, tol).smallest_counted_singular_value


def largest_rejected_singular_value(matrix: Any, tol: Optional[float] = None) -> float:
    """Returns the largest rejected singular value."""
    return compute_numerical_rank(matrix, tol).largest_rejected_singular_value


def threshold_margin(matrix: Any, tol: Optional[float] = None) -> float:
    """Returns gap between smallest counted and largest rejected singular value."""
    return compute_numerical_rank(matrix, tol).threshold_margin


__all__ = [
    "NumericalRankError",
    "NumericalRankReport",
    "compute_numerical_rank",
    "rank",
    "tolerance",
    "shape",
    "singular_values",
    "smallest_counted_singular_value",
    "largest_rejected_singular_value",
    "threshold_margin",
]
