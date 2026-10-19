"""Homology-correct tetron-array carriers on a surface.

A tetron is a 2-cell: one superconducting island, four MZMs on its
boundary, total fermion parity pinned by charging energy. An R x C array
of tetrons therefore tiles a surface, and the array's cohomology is the
surface's.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .complexes import ChainComplexGf2
from .gf2_terminalizer import GF2Matrix, Gf2CocycleClassifier


class Topology(str, Enum):
    Disk = "Disk"
    Cylinder = "Cylinder"
    Torus = "Torus"

    def wraps(self) -> tuple[bool, bool]:
        return {
            Topology.Disk: (False, False),
            Topology.Cylinder: (False, True),
            Topology.Torus: (True, True),
        }[self]

    def expected_dim_h1(self) -> int:
        return {Topology.Disk: 0, Topology.Cylinder: 1, Topology.Torus: 2}[self]

    def name(self) -> str:
        return {
            Topology.Disk: "tetron_disk",
            Topology.Cylinder: "tetron_cylinder",
            Topology.Torus: "tetron_torus",
        }[self]


class Axis(str, Enum):
    Row = "Row"
    Column = "Column"
    # Aliases
    X = "Column"
    Z = "Row"


@dataclass
class TetronReport:
    topology: Topology
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
    horizontal: list[list[int]]
    vertical: list[list[int]]
    authority_effect: str = "None"
    code_distance: Optional[int] = None

    def homology_matches_prediction(self) -> bool:
        return self.dim_h1 == self.expected_dim_h1


def build_tetron_array(
    rows: int, cols: int, topology: Topology
) -> tuple[ChainComplexGf2, TetronReport]:
    if rows == 0 or cols == 0:
        raise ValueError("rows and cols must be >= 1")
    wrap_r, wrap_c = topology.wraps()
    if wrap_c and cols < 2:
        raise ValueError(f"{topology} is periodic in columns; cols must be >= 2")
    if wrap_r and rows < 2:
        raise ValueError(f"{topology} is periodic in rows; rows must be >= 2")

    vrows = rows if wrap_r else rows + 1
    vcols = cols if wrap_c else cols + 1
    num_mzm = vrows * vcols

    def mzm(i: int, j: int) -> int:
        return (i % vrows) * vcols + (j % vcols)

    d0_rows: list[list[int]] = []

    def add_channel(u: int, v: int) -> int:
        row = [0] * num_mzm
        row[u] ^= 1
        row[v] ^= 1
        d0_rows.append(row)
        return len(d0_rows) - 1

    # Horizontal channels H(i, j) joins MZM (i, j) to (i, j+1)
    h_span = vcols if wrap_c else vcols - 1
    horizontal = [[-1] * h_span for _ in range(vrows)]
    for i in range(vrows):
        for j in range(h_span):
            horizontal[i][j] = add_channel(mzm(i, j), mzm(i, j + 1))

    # Vertical channels V(i, j) joins MZM (i, j) to (i+1, j)
    v_span = vrows if wrap_r else vrows - 1
    vertical = [[-1] * vcols for _ in range(v_span)]
    for i in range(v_span):
        for j in range(vcols):
            vertical[i][j] = add_channel(mzm(i, j), mzm(i + 1, j))

    num_channels = len(d0_rows)

    # Island 2-cells: island (i, j) bounded by H(i, j), V(i, j+1), H(i+1, j), V(i, j)
    d1_rows: list[list[int]] = []
    for i in range(rows):
        for j in range(cols):
            row = [0] * num_channels
            j_next = (j + 1) % vcols if wrap_c else j + 1
            i_next = (i + 1) % vrows if wrap_r else i + 1
            row[horizontal[i][j]] ^= 1
            row[vertical[i][j_next]] ^= 1
            row[horizontal[i_next][j]] ^= 1
            row[vertical[i][j]] ^= 1
            d1_rows.append(row)

    num_islands = len(d1_rows)

    d0 = GF2Matrix.from_data(d0_rows)
    d1 = GF2Matrix.from_data(d1_rows)
    rank_d0 = d0.rank()
    rank_d1 = d1.rank()
    dim_h1 = (num_channels - rank_d1) - rank_d0

    complex = ChainComplexGf2(
        name=topology.name(),
        d0=d0,
        d1=d1,
        num_vertices=num_mzm,
        num_edges=num_channels,
        num_faces=num_islands,
    )
    if not Gf2CocycleClassifier.verify_boundary(complex.d0, complex.d1):
        raise ValueError("constructed carrier violates d1 * d0 = 0")

    # Code distance if applicable
    d_val = None
    if dim_h1 > 0 and num_channels <= 16:
        from .repair_limit import homology_distance
        d_val = homology_distance(complex)
    elif topology == Topology.Torus:
        d_val = min(rows, cols)

    report = TetronReport(
        topology=topology,
        rows=rows,
        cols=cols,
        num_mzm=num_mzm,
        num_channels=num_channels,
        num_islands=num_islands,
        euler_characteristic=num_mzm - num_channels + num_islands,
        rank_d0=rank_d0,
        rank_d1=rank_d1,
        graph_b1=num_channels - rank_d0,
        dim_h1=dim_h1,
        expected_dim_h1=topology.expected_dim_h1(),
        horizontal=horizontal,
        vertical=vertical,
        authority_effect="None",
        code_distance=d_val,
    )
    return complex, report


def logical_class_representative(
    report_or_rows: TetronReport | int,
    axis: Axis = Axis.Column,
    index: int = 0,
) -> list[int]:
    """Generates an explicit closed 1-cochain generating a logical parity class."""
    if isinstance(report_or_rows, int):
        rows = report_or_rows
        cols = int(axis) if isinstance(axis, int) else rows
        actual_axis = index if isinstance(index, Axis) else Axis.Column
        _, rep = build_tetron_array(rows, cols, Topology.Torus)
        return logical_class_representative(rep, actual_axis, 0)

    report = report_or_rows
    residual = [0] * report.num_channels
    if axis in (Axis.Column, Axis.X):
        slot = index % len(report.horizontal[0])
        for row in report.horizontal:
            residual[row[slot]] = 1
    elif axis in (Axis.Row, Axis.Z):
        slot = index % len(report.vertical)
        for col_idx in report.vertical[slot]:
            residual[col_idx] = 1
    return residual


@dataclass(frozen=True)
class TetronScalingRow:
    """2D Tetron cochain complex scaling row over F_2 matching Rust TetronScalingRow."""
    topology: Topology
    rows: int
    cols: int
    num_mzm: int
    num_channels: int
    num_islands: int
    rank_d0: int
    rank_d1: int
    dim_h1: int
    expected_dim_h1: int
    boundary_exact: bool
    euler_agrees: bool
    generators_closed: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topology": self.topology.value,
            "rows": self.rows,
            "cols": self.cols,
            "num_mzm": self.num_mzm,
            "num_channels": self.num_channels,
            "num_islands": self.num_islands,
            "rank_d0": self.rank_d0,
            "rank_d1": self.rank_d1,
            "dim_h1": self.dim_h1,
            "expected_dim_h1": self.expected_dim_h1,
            "boundary_exact": self.boundary_exact,
            "euler_agrees": self.euler_agrees,
            "generators_closed": self.generators_closed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TetronScalingRow":
        return cls(
            topology=Topology(str(data["topology"])),
            rows=int(data["rows"]),
            cols=int(data["cols"]),
            num_mzm=int(data["num_mzm"]),
            num_channels=int(data["num_channels"]),
            num_islands=int(data["num_islands"]),
            rank_d0=int(data["rank_d0"]),
            rank_d1=int(data["rank_d1"]),
            dim_h1=int(data["dim_h1"]),
            expected_dim_h1=int(data["expected_dim_h1"]),
            boundary_exact=bool(data["boundary_exact"]),
            euler_agrees=bool(data["euler_agrees"]),
            generators_closed=bool(data["generators_closed"]),
        )


def benchmark_tetron_lattice_scaling(
    sizes: Sequence[Tuple[int, int]],
    topologies: Sequence[Topology],
) -> List[TetronScalingRow]:
    """Finite lattice scaling benchmark for 2D Tetron cochain complexes across declared
    (rows, cols) grid dimensions and topologies (Disk, Cylinder, Torus).
    Matches Rust tfqm_majorana::benchmark_tetron_lattice_scaling bit-for-bit.
    """
    if not sizes or not topologies:
        raise ValueError("sizes and topologies must be non-empty")

    from .repair_limit import apply_d1

    rows_out: List[TetronScalingRow] = []
    for topology in topologies:
        for rows, cols in sizes:
            complex_gf2, report = build_tetron_array(rows, cols, topology)
            boundary_exact = bool(complex_gf2.verify_boundary())
            closed_surface = topology == Topology.Torus
            predicted_h1 = (2 if closed_surface else 1) - report.euler_characteristic
            euler_agrees = report.dim_h1 == predicted_h1

            generators_closed = True
            for axis in (Axis.Column, Axis.Row):
                rep = logical_class_representative(report, axis, 0)
                syn = apply_d1(complex_gf2.d1, rep)
                if any(b != 0 for b in syn):
                    generators_closed = False

            rows_out.append(
                TetronScalingRow(
                    topology=topology,
                    rows=rows,
                    cols=cols,
                    num_mzm=report.num_mzm,
                    num_channels=report.num_channels,
                    num_islands=report.num_islands,
                    rank_d0=report.rank_d0,
                    rank_d1=report.rank_d1,
                    dim_h1=report.dim_h1,
                    expected_dim_h1=report.expected_dim_h1,
                    boundary_exact=boundary_exact,
                    euler_agrees=euler_agrees,
                    generators_closed=generators_closed,
                )
            )
    return rows_out


def tetron_scaling_to_canonical_json(rows: Sequence[TetronScalingRow]) -> str:
    """Serialize TetronScalingRow list to canonical 2-space pretty JSON with LF line endings."""
    return json.dumps([row.to_dict() for row in rows], indent=2)


def tetron_scaling_from_canonical_json(json_str: str) -> List[TetronScalingRow]:
    """Deserialize TetronScalingRow list from canonical JSON string."""
    raw = json.loads(json_str)
    return [TetronScalingRow.from_dict(item) for item in raw]

