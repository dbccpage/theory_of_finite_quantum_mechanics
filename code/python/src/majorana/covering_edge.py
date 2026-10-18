from __future__ import annotations
"""Exact finite covering-edge Banach-diagram certificates for PO-000 §2."""


from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import TypeAlias

from sympy import Abs, Basic, Matrix, Max, simplify
from sympy.matrices.matrixbase import MatrixBase

from omega_engine.crates.linear_algebra_theory.exact import (
    ExactInput,
    as_rational,
    exact_column,
    exact_equal,
    exact_matrix_from_matrix,
    l1_norm,
)

NodeId: TypeAlias = str
EdgeId: TypeAlias = str


@dataclass
class CoveringEdge:
    """A contractive map from the upper fiber to the lower fiber."""

    edge_id: EdgeId
    lower: NodeId
    upper: NodeId
    restriction: Matrix

    def __post_init__(self) -> None:
        object.__setattr__(self, "restriction", exact_matrix_from_matrix(self.restriction))


@dataclass
class CoboundaryBoundCertificate:
    """Exact witness for ``||Delta(s)||_1 <= 2 |E| ||s||_infinity``."""

    coboundary_norm: Basic
    section_sup_norm: Basic
    bound: Basic
    holds: bool


def l1_operator_norm(matrix: MatrixBase) -> Basic:
    r"""Exact induced :math:`\ell^1` operator norm (maximum column sum)."""

    if matrix.cols == 0:
        return simplify(0)
    column_sums = [
        sum(Abs(matrix[row, col]) for row in range(matrix.rows)) for col in range(matrix.cols)
    ]
    return simplify(Max(*column_sums))


class CoveringEdgeDiagram:
    """Finite vector-space realization of the paper's covering-edge diagram."""

    def __init__(self, fiber_dimensions: Mapping[NodeId, int], edges: Sequence[CoveringEdge]):
        if not fiber_dimensions:
            raise ValueError("a covering-edge diagram needs at least one fiber")
        if any(dim <= 0 for dim in fiber_dimensions.values()):
            raise ValueError("fiber dimensions must be positive")
        if len({edge.edge_id for edge in edges}) != len(edges):
            raise ValueError("edge identifiers must be unique")

        self.fiber_dimensions = dict(fiber_dimensions)
        self.edges = tuple(edges)
        for edge in self.edges:
            if edge.lower not in self.fiber_dimensions or edge.upper not in self.fiber_dimensions:
                raise ValueError(f"edge {edge.edge_id!r} references an unknown node")
            expected = (
                self.fiber_dimensions[edge.lower],
                self.fiber_dimensions[edge.upper],
            )
            if edge.restriction.shape != expected:
                raise ValueError(
                    f"edge {edge.edge_id!r} has shape {edge.restriction.shape}, expected {expected}"
                )
            if l1_operator_norm(edge.restriction) > 1:
                raise ValueError(f"edge {edge.edge_id!r} is not l1-contractive")

    def normalize_section(
        self, section: Mapping[NodeId, Sequence[ExactInput] | MatrixBase]
    ) -> dict[NodeId, Matrix]:
        """Validate a total section and return exact column vectors."""

        missing = set(self.fiber_dimensions) - set(section)
        extra = set(section) - set(self.fiber_dimensions)
        if missing or extra:
            raise ValueError(
                f"section domain mismatch; missing={sorted(missing)}, extra={sorted(extra)}"
            )

        normalized: dict[NodeId, Matrix] = {}
        for node, dim in self.fiber_dimensions.items():
            value = section[node]
            vector = (
                exact_matrix_from_matrix(value)
                if isinstance(value, MatrixBase)
                else exact_column(value)
            )
            if vector.shape != (dim, 1):
                raise ValueError(
                    f"section value at {node!r} has shape {vector.shape}, expected {(dim, 1)}"
                )
            normalized[node] = vector
        return normalized

    def coboundary(
        self, section: Mapping[NodeId, Sequence[ExactInput] | MatrixBase]
    ) -> dict[EdgeId, Matrix]:
        """Compute ``Delta(s)_e = r_(b,a) s(b) - s(a)`` exactly."""

        values = self.normalize_section(section)
        return {
            edge.edge_id: edge.restriction * values[edge.upper] - values[edge.lower]
            for edge in self.edges
        }

    def inconsistency(self, section: Mapping[NodeId, Sequence[ExactInput] | MatrixBase]) -> Basic:
        """Compute the exact raw edge tally ``I(s)``."""

        defects = self.coboundary(section)
        return simplify(sum(l1_norm(defects[edge.edge_id]) for edge in self.edges))

    def coboundary_bound_certificate(
        self, section: Mapping[NodeId, Sequence[ExactInput] | MatrixBase]
    ) -> CoboundaryBoundCertificate:
        """Recompute both sides of the §2.2 bound on one exact finite carrier."""

        values = self.normalize_section(section)
        section_sup = Max(*(l1_norm(value) for value in values.values()))
        coboundary_norm = self.inconsistency(values)
        bound = simplify(as_rational(2) * len(self.edges) * section_sup)
        return CoboundaryBoundCertificate(
            coboundary_norm=coboundary_norm,
            section_sup_norm=section_sup,
            bound=bound,
            holds=bool(simplify(bound - coboundary_norm) >= 0),
        )

    def is_descended(self, section: Mapping[NodeId, Sequence[ExactInput] | MatrixBase]) -> bool:
        """Return true exactly when every covering-edge defect vanishes."""

        return all(
            exact_equal(defect, Matrix.zeros(defect.rows, 1))
            for defect in self.coboundary(section).values()
        )





