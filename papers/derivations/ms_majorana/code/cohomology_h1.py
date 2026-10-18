from __future__ import annotations
"""Exact first cohomology H^1 = ker d1 / im d0 (spine S1.5 L2035).

Faithful to the spine's exact-arithmetic requirement: dimensions and membership
are decided over the rationals (``Fraction`` via :class:`QMatrix`), NOT float.
This realizes the closed-Survivor sector the audit found ABSENT (A3).

Shape convention (matching ``omega_functional/gamma2.py``):
    d0 : C^0 -> C^1   shape (E, V)   -- coboundary of 0-cochains
    d1 : C^1 -> C^2   shape (F, E)   -- coboundary of 1-cochains

The quotient H^1 = Z^1 / B^1 with Z^1 = ker d1, B^1 = im d0 is well defined
only when the cochain law d1 . d0 = 0 holds (so B^1 subseteq Z^1). We REFUSE
(typed) on shape mismatch and on d1.d0 != 0 rather than returning a wrong number.

DIAGNOSTIC ONLY. Mints no authority.
"""


from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence

from .qmatrix import QMatrix
from .errors import DimensionMismatch, CoboundaryLawViolation


def _to_qmatrix(M, rows: int, cols: int) -> QMatrix:
    """Coerce a nested sequence / QMatrix into an exact QMatrix of given shape."""
    if isinstance(M, QMatrix):
        if M.shape != (rows, cols):
            raise DimensionMismatch(f"expected shape ({rows}, {cols}), got {M.shape}")
        return M
    flat: List[Fraction] = []
    for r in M:
        row = list(r)
        if len(row) != cols:
            raise DimensionMismatch(f"row has {len(row)} entries, expected {cols}")
        flat.extend(Fraction(x) for x in row)
    if len(flat) != rows * cols:
        raise DimensionMismatch(
            f"expected {rows * cols} entries for ({rows}, {cols}), got {len(flat)}"
        )
    return QMatrix.from_row_major(rows, cols, flat)


@dataclass(frozen=True)
class H1Result:
    """Exact H^1 dimension data. Diagnostic; mints no authority."""

    num_edges: int  
    rank_d0: int  
    rank_d1: int  
    dim_z1: int  
    dim_b1: int  
    dim_h1: int  

    def as_dict(self) -> dict:
        return {
            "num_edges": self.num_edges,
            "rank_d0": self.rank_d0,
            "rank_d1": self.rank_d1,
            "dim_z1": self.dim_z1,
            "dim_b1": self.dim_b1,
            "dim_h1": self.dim_h1,
        }


class CohomologyH1:
    """Exact H^1 = ker d1 / im d0 over the rationals."""

    def __init__(self, d0, d1, num_edges: int, num_vertices: int, num_faces: int):
        self.num_edges = num_edges
        self.num_vertices = num_vertices
        self.num_faces = num_faces
        self.d0 = _to_qmatrix(d0, num_edges, num_vertices)  
        self.d1 = _to_qmatrix(d1, num_faces, num_edges)  
        if self.d0.rows != self.d1.cols:
            raise DimensionMismatch(
                f"d0 produces {self.d0.rows} edges but d1 expects {self.d1.cols}"
            )
        comp = self.d1.matmul(self.d0)  
        if not comp.is_zero():
            raise CoboundaryLawViolation(
                "d1 . d0 != 0 exactly; H^1 = ker d1 / im d0 is not well defined"
            )

    @classmethod
    def from_dims(cls, d0, d1) -> "CohomologyH1":
        """Build inferring (E, V, F) from the matrix shapes.

        ``d0`` is (E, V), ``d1`` is (F, E).
        """
        d0m = d0 if isinstance(d0, QMatrix) else _infer(d0)
        d1m = d1 if isinstance(d1, QMatrix) else _infer(d1)
        E, V = d0m.shape
        F, E2 = d1m.shape
        if E != E2:
            raise DimensionMismatch(
                f"d0 has {E} edges (rows) but d1 has {E2} edges (cols)"
            )
        return cls(d0m, d1m, num_edges=E, num_vertices=V, num_faces=F)

    def result(self) -> H1Result:
        rank_d0 = self.d0.rank()  
        rank_d1 = self.d1.rank()
        dim_z1 = self.num_edges - rank_d1  
        dim_b1 = rank_d0
        dim_h1 = dim_z1 - dim_b1
        return H1Result(
            num_edges=self.num_edges,
            rank_d0=rank_d0,
            rank_d1=rank_d1,
            dim_z1=dim_z1,
            dim_b1=dim_b1,
            dim_h1=dim_h1,
        )

    def dim_h1(self) -> int:
        return self.result().dim_h1

    def d0_as_float(self) -> List[List[float]]:
        """Float view of d0 (E, V) for handing to the float LP solver."""
        return [[float(v) for v in row] for row in self.d0.data]

    def is_closed(self, x: Sequence) -> bool:
        """Exact: x in Z^1 (ker d1), i.e. d1 . x = 0 over the rationals."""
        xq = _column(x, self.num_edges)
        return self.d1.matmul(xq).is_zero()

    def gamma2(self, x: Sequence) -> Fraction:
        """Exact Gamma2 = ||d1 x||_1 over the rationals (closure defect)."""
        xq = _column(x, self.num_edges)
        prod = self.d1.matmul(xq)
        return sum((abs(row[0]) for row in prod.data), Fraction(0))

    def is_exact(self, x: Sequence) -> bool:
        """Exact: x in B^1 = im d0, i.e. x = d0 alpha for some alpha.

        Decided by rank augmentation: x in col-space(d0) iff
        rank([d0 | x]) == rank(d0). Pure exact arithmetic, no float lstsq.
        """
        xq = _column(x, self.num_edges)
        base_rank = self.d0.rank()
        aug = _augment(self.d0, xq)
        return aug.rank() == base_rank

    def class_dimension_contribution(self, x: Sequence) -> str:
        """Diagnostic label for where x sits: 'exact' (in B^1),
        'closed_nonexact' (in Z^1 \\ B^1, a nonzero H^1 class), or 'open'
        (not closed). Mints no authority."""
        if not self.is_closed(x):
            return "open"
        if self.is_exact(x):
            return "exact"
        return "closed_nonexact"


def _infer(M) -> QMatrix:
    rows = list(M)
    nrows = len(rows)
    ncols = len(rows[0]) if nrows else 0
    flat: List[Fraction] = []
    for r in rows:
        rl = list(r)
        if len(rl) != ncols:
            raise DimensionMismatch("ragged matrix")
        flat.extend(Fraction(x) for x in rl)
    return QMatrix.from_row_major(nrows, ncols, flat)


def _column(x: Sequence, n: int) -> QMatrix:
    xl = list(x)
    if len(xl) != n:
        raise DimensionMismatch(f"cochain has {len(xl)} entries, expected {n} edges")
    return QMatrix(n, 1, [[Fraction(v)] for v in xl])


def _augment(M: QMatrix, col: QMatrix) -> QMatrix:
    if M.rows != col.rows:
        raise DimensionMismatch("augmentation row mismatch")
    data = [M.data[r][:] + [col.data[r][0]] for r in range(M.rows)]
    return QMatrix(M.rows, M.cols + 1, data)


def h1_dimension(d0, d1) -> int:
    """Convenience: exact dim H^1 from (d0:(E,V), d1:(F,E))."""
    return CohomologyH1.from_dims(d0, d1).dim_h1()


