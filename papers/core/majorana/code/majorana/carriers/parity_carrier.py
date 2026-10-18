from __future__ import annotations
# SPDX-License-Identifier: Apache-2.0


from dataclasses import field
from dataclasses import dataclass
from typing import Any, Literal

from omega_engine.crates.majorana.core.gf2_schema import (
    normalize_matrix,
    normalize_vector,
)


@dataclass(frozen=True)
class MajoranaParityCarrier:
    """Finite GF(2) parity/coherence carrier.

    No informal prose claim is executable. The terminalizer only accepts this
    finite carrier shape.
    """

    carrier_kind: Literal["majorana_parity_gf2"]
    coefficient_field: Literal["GF2"]
    D0: list[list[int]]
    D1: list[list[int]]
    residual: list[int]
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def C0_dim(self) -> int:
        return len(self.D0[0]) if self.D0 else 0

    @property
    def C1_dim(self) -> int:
        return len(self.D0)

    @property
    def C2_dim(self) -> int:
        return len(self.D1)

    def normalized(self) -> "MajoranaParityCarrier":
        return MajoranaParityCarrier(
            carrier_kind="majorana_parity_gf2",
            coefficient_field="GF2",
            D0=normalize_matrix(self.D0),
            D1=normalize_matrix(self.D1),
            residual=normalize_vector(self.residual),
            metadata=dict(self.metadata),
        )

    def validate_shape(self) -> None:
        if self.carrier_kind != "majorana_parity_gf2":
            raise ValueError("carrier_kind must be majorana_parity_gf2")
        if self.coefficient_field != "GF2":
            raise ValueError("coefficient_field must be GF2")
        if not self.D0:
            raise ValueError("D0 must be non-empty")
        d0_cols = len(self.D0[0])
        if d0_cols == 0:
            raise ValueError("D0 must have at least one column")
        if any(len(row) != d0_cols for row in self.D0):
            raise ValueError("D0 rows must have equal length")
        d1_cols = len(self.D1[0]) if self.D1 else len(self.D0)
        if d1_cols != len(self.D0):
            raise ValueError("D1 column count must equal D0 row count")
        if self.D1 and any(len(row) != d1_cols for row in self.D1):
            raise ValueError("D1 rows must have equal length")
        if len(self.residual) != len(self.D0):
            raise ValueError("residual length must equal C1 dimension")






