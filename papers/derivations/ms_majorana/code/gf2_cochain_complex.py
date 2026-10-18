from __future__ import annotations
"""GF(2) cochain complex dual to GF2ChainComplex.

Authority path: omega_engine.crates.homology_theory.gf2_cochain_complex
(no coda dual-home).
"""

from dataclasses import dataclass
from typing import Sequence

from omega_engine.crates.homology_theory.gf2_matrix import GF2Matrix
from omega_engine.crates.homology_theory.gf2_chain_complex import GF2ChainComplex
from omega_engine.crates.majorana.core.gf2_schema import mod2
from omega_engine.crates.majorana.carriers.parity_carrier import (
    MajoranaParityCarrier,
)


@dataclass
class GF2CochainComplex:
    """GF(2) cochain complex with coboundaries d0: C0->C1 and d1: C1->C2."""

    d0: GF2Matrix
    d1: GF2Matrix
    metadata: dict

    @classmethod
    def from_chain(cls, chain: GF2ChainComplex) -> "GF2CochainComplex":
        boundary_1 = chain.boundary_1()
        boundary_2 = chain.boundary_2()
        d0 = boundary_1.transpose()
        d1 = boundary_2.transpose()
        return cls(
            d0=d0,
            d1=d1,
            metadata={
                "nodes": list(chain.graph.nodes()),
                "edges": list(chain.graph.edges()),
                "faces": [list(face) for face in chain.faces],
                "construction": "cochain_from_directed_graph",
            },
        )

    def validate_cochain(self) -> None:
        """Check d1 d0 = 0."""
        for col_idx in range(self.d0.cols):
            col = [self.d0[row][col_idx] for row in range(self.d0.rows)]
            out = self.d1.mat_vec_mul(col)
            if any(out):
                raise ValueError(
                    f"Invalid cochain complex: d1d0 != 0 at column {col_idx}: {out}"
                )

    def create_carrier(self, residual: Sequence[int]) -> MajoranaParityCarrier:
        self.validate_cochain()
        r = [mod2(x) for x in residual]
        if len(r) != self.d0.rows:
            raise ValueError(
                f"Residual length {len(r)} must equal C^1 dimension {self.d0.rows}"
            )
        return MajoranaParityCarrier(
            carrier_kind="majorana_parity_gf2",
            coefficient_field="GF2",
            D0=self.d0.to_list(),
            D1=self.d1.to_list(),
            residual=r,
            metadata=self.metadata,
        ).normalized()


