from __future__ import annotations
# SPDX-License-Identifier: Apache-2.0


from dataclasses import dataclass
from typing import Any, Literal

from omega_engine.crates.majorana.carriers.parity_carrier import MajoranaParityCarrier
from omega_engine.crates.majorana.core.gf2_diagnostic import tetron_native

Topology = Literal["disk", "cylinder", "torus"]

TOPOLOGIES: tuple[str, ...] = ("disk", "cylinder", "torus")

EXPECTED_DIM_H1: dict[str, int] = {"disk": 0, "cylinder": 1, "torus": 2}

HARDWARE_READING: dict[str, str] = {
    "disk": "open tetron array; no protected logical parity error",
    "cylinder": "tetron ring / H-junction ladder; one logical parity class",
    "torus": "periodic tetron array; two independent logical parity classes",
}


@dataclass(frozen=True)
class CarrierReport:
    """Measured structure of a tetron-array carrier.

    ``dim_h1``, ``rank_d0``, ``rank_d1``, and ``graph_b1`` are the native
    ``majorana_gf2_diagnostic`` operation ``tetron``. Cell counts are the
    carrier layout. ``expected_dim_h1`` is the design prediction, kept
    alongside so a mismatch is visible rather than silent.
    """

    topology: str
    rows: int
    cols: int
    num_mzm: int
    num_channels: int
    num_islands: int
    euler_characteristic: int
    rank_d0: int
    rank_d1: int
    graph_b1: int
    dim_h1: int
    expected_dim_h1: int
    hardware_reading: str
    horizontal_channels: dict[tuple[int, int], int]
    vertical_channels: dict[tuple[int, int], int]
    column_slots: int
    row_slots: int
    authority_effect: str = "None"

    @property
    def homology_matches_prediction(self) -> bool:
        return self.dim_h1 == self.expected_dim_h1

    def summary(self) -> dict[str, Any]:
        """Certificate-safe view; drops the channel index maps."""
        return {
            "topology": self.topology,
            "rows": self.rows,
            "cols": self.cols,
            "num_mzm": self.num_mzm,
            "num_channels": self.num_channels,
            "num_islands": self.num_islands,
            "euler_characteristic": self.euler_characteristic,
            "rank_d0": self.rank_d0,
            "rank_d1": self.rank_d1,
            "graph_b1": self.graph_b1,
            "dim_h1": self.dim_h1,
            "expected_dim_h1": self.expected_dim_h1,
            "homology_matches_prediction": self.homology_matches_prediction,
            "hardware_reading": self.hardware_reading,
            "authority_effect": self.authority_effect,
        }


def _validate_extent(rows: int, cols: int, topology: str) -> None:
    if topology not in TOPOLOGIES:
        raise ValueError(
            f"unknown topology {topology!r}; expected one of {TOPOLOGIES}"
        )
    if rows < 1 or cols < 1:
        raise ValueError("rows and cols must be >= 1")
    if topology in ("torus", "cylinder") and cols < 2:
        raise ValueError(
            f"{topology} is periodic in columns; cols must be >= 2 (got {cols})"
        )
    if topology == "torus" and rows < 2:
        raise ValueError(f"torus is periodic in rows; rows must be >= 2 (got {rows})")


def _lattice_shape(rows: int, cols: int, topology: str) -> tuple[int, int, bool, bool]:
    """Return (vertex_rows, vertex_cols, wrap_rows, wrap_cols)."""
    if topology == "torus":
        return rows, cols, True, True
    if topology == "cylinder":
        return rows + 1, cols, False, True
    return rows + 1, cols + 1, False, False


def build_tetron_array(
    rows: int = 3,
    cols: int = 3,
    topology: Topology = "torus",
    residual: list[int] | None = None,
) -> tuple[MajoranaParityCarrier, CarrierReport]:
    """Build an ``rows x cols`` tetron array on ``topology``.

    Returns the GF(2) carrier and a report whose ``dim_h1`` is the native
    ``majorana_gf2_diagnostic`` operation ``tetron`` field, not a Python rank.
    """
    _validate_extent(rows, cols, topology)
    vrows, vcols, wrap_r, wrap_c = _lattice_shape(rows, cols, topology)

    def mzm(i: int, j: int) -> int:
        return (i % vrows) * vcols + (j % vcols)

    num_mzm = vrows * vcols

    h_index: dict[tuple[int, int], int] = {}
    v_index: dict[tuple[int, int], int] = {}
    d0_rows: list[list[int]] = []

    def add_channel(u: int, v: int) -> int:
        row = [0] * num_mzm
        row[u] ^= 1
        row[v] ^= 1
        d0_rows.append(row)
        return len(d0_rows) - 1

    h_span = vcols if wrap_c else vcols - 1
    for i in range(vrows):
        for j in range(h_span):
            h_index[(i, j)] = add_channel(mzm(i, j), mzm(i, j + 1))

    v_span = vrows if wrap_r else vrows - 1
    for i in range(v_span):
        for j in range(vcols):
            v_index[(i, j)] = add_channel(mzm(i, j), mzm(i + 1, j))

    num_channels = len(d0_rows)

    d1_rows: list[list[int]] = []
    for i in range(rows):
        for j in range(cols):
            row = [0] * num_channels
            for key, table in (
                ((i, j), h_index),
                ((i, (j + 1) % vcols if wrap_c else j + 1), v_index),
                (((i + 1) % vrows if wrap_r else i + 1, j), h_index),
                ((i, j), v_index),
            ):
                if table is h_index:
                    row[h_index[key]] ^= 1
                else:
                    row[v_index[key]] ^= 1
            d1_rows.append(row)

    num_islands = len(d1_rows)

    measured = tetron_native(rows, cols, topology)
    rank_d0 = measured["rank_d0"]
    rank_d1 = measured["rank_d1"]
    dim_h1 = measured["dim_h1"]

    report = CarrierReport(
        topology=topology,
        rows=rows,
        cols=cols,
        num_mzm=num_mzm,
        num_channels=num_channels,
        num_islands=num_islands,
        euler_characteristic=num_mzm - num_channels + num_islands,
        rank_d0=rank_d0,
        rank_d1=rank_d1,
        graph_b1=measured["graph_b1"],
        dim_h1=dim_h1,
        expected_dim_h1=EXPECTED_DIM_H1[topology],
        hardware_reading=HARDWARE_READING[topology],
        horizontal_channels=dict(h_index),
        vertical_channels=dict(v_index),
        column_slots=h_span,
        row_slots=v_span,
    )

    if residual is None:
        residual_vec = [0] * num_channels
    else:
        if len(residual) != num_channels:
            raise ValueError(
                f"residual length ({len(residual)}) must equal the channel count "
                f"({num_channels})"
            )
        residual_vec = [x % 2 for x in residual]

    carrier = MajoranaParityCarrier(
        carrier_kind="majorana_parity_gf2",
        coefficient_field="GF2",
        D0=d0_rows,
        D1=d1_rows,
        residual=residual_vec,
        metadata=report.summary(),
    )
    carrier.validate_shape()
    return carrier, report


def logical_class_representative(
    report: CarrierReport,
    axis: Literal["row", "column"] = "column",
    index: int = 0,
) -> list[int]:
    """An explicit closed 1-cochain that generates a logical parity class.

    ``axis="column"``: every horizontal channel in column slot ``index``. It is
    closed because island ``(i, index)`` contains exactly ``H(i, index)`` and
    ``H(i+1, index)``. On a torus and a cylinder it is *not* a coboundary.

    ``axis="row"``: every vertical channel in row slot ``index``. Closed by the
    same argument. Non-exact on a torus only -- on a cylinder it equals
    ``d0 alpha`` for ``alpha = 1`` on lattice rows ``<= index``.

    Physically: a string of faulty channels crossing the array. Its weight is
    the number of channels that must be wrong to realize the logical error.
    """
    residual = [0] * report.num_channels
    if axis == "column":
        slot = index % report.column_slots
        for (_i, j), channel in report.horizontal_channels.items():
            if j == slot:
                residual[channel] = 1
    elif axis == "row":
        slot = index % report.row_slots
        for (i, _j), channel in report.vertical_channels.items():
            if i == slot:
                residual[channel] = 1
    else:
        raise ValueError(f"axis must be 'row' or 'column', got {axis!r}")
    return residual





