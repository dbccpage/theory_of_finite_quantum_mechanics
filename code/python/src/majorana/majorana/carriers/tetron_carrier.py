from __future__ import annotations


from typing import Any, List
from omega_engine.crates.majorana.carriers.parity_carrier import MajoranaParityCarrier


def build_tetron_array_carrier(
    num_tetrons: int = 2,
    residual: List[int] | None = None,
) -> MajoranaParityCarrier:
    """Constructs a MajoranaParityCarrier for a Station Q tetron array topology.

    Each tetron has 4 computational MZMs at the ends of 2 topological wires (top, bottom),
    connected by a central superconducting backbone node.
    Adjacent tetrons are coupled via inter-tetron parity channels forming topological loops (D1 @ D0 = 0).
    """
    if num_tetrons < 1:
        raise ValueError("num_tetrons must be >= 1")

    modes_per_tetron = 6
    total_modes = num_tetrons * modes_per_tetron

    d0_rows: List[List[int]] = []
    d1_rows: List[List[int]] = []

    top_bonds: List[int] = []
    bot_bonds: List[int] = []
    inter_top_bonds: List[int] = []
    inter_top_return_bonds: List[int] = []

    for t in range(num_tetrons):
        offset = t * modes_per_tetron

        r_top = [0] * total_modes
        r_top[offset + 0] = 1
        r_top[offset + 1] = 1
        d0_rows.append(r_top)
        top_bonds.append(len(d0_rows) - 1)

        r_bot = [0] * total_modes
        r_bot[offset + 2] = 1
        r_bot[offset + 3] = 1
        d0_rows.append(r_bot)
        bot_bonds.append(len(d0_rows) - 1)

        r_bb_top = [0] * total_modes
        r_bb_top[offset + 1] = 1
        r_bb_top[offset + 4] = 1
        d0_rows.append(r_bb_top)

        r_bb_bot = [0] * total_modes
        r_bb_bot[offset + 3] = 1
        r_bb_bot[offset + 5] = 1
        d0_rows.append(r_bb_bot)

        if t < num_tetrons - 1:
            next_offset = (t + 1) * modes_per_tetron
            r_it_fwd = [0] * total_modes
            r_it_fwd[offset + 1] = 1
            r_it_fwd[next_offset + 0] = 1
            d0_rows.append(r_it_fwd)
            inter_top_bonds.append(len(d0_rows) - 1)

            r_it_ret = [0] * total_modes
            r_it_ret[next_offset + 1] = 1
            r_it_ret[offset + 0] = 1
            d0_rows.append(r_it_ret)
            inter_top_return_bonds.append(len(d0_rows) - 1)

    num_bonds = len(d0_rows)

    for t in range(num_tetrons - 1):
        row_d1 = [0] * num_bonds
        row_d1[top_bonds[t]] = 1
        row_d1[inter_top_bonds[t]] = 1
        row_d1[top_bonds[t + 1]] = 1
        row_d1[inter_top_return_bonds[t]] = 1
        d1_rows.append(row_d1)

    if residual is None:
        residual_vec = [0] * num_bonds
        if num_bonds > 0:
            residual_vec[0] = 1
    else:
        if len(residual) != num_bonds:
            raise ValueError(f"residual length ({len(residual)}) must equal number of bonds ({num_bonds})")
        residual_vec = list(residual)

    from omega_engine.crates.majorana.core.gf2_diagnostic import classify_native
    from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix

    gf2_d0 = GF2Matrix(d0_rows)
    _, pivots = gf2_d0.rref()
    rank_f2 = len(pivots)
    betti_1_f2 = classify_native(d0_rows, d1_rows, residual_vec, budget=1)["dim_h1"]
    if isinstance(betti_1_f2, bool) or not isinstance(betti_1_f2, int):
        raise ValueError("native classify returned no dim_h1")

    carrier = MajoranaParityCarrier(
        carrier_kind="majorana_parity_gf2",
        coefficient_field="GF2",
        D0=d0_rows,
        D1=d1_rows,
        residual=residual_vec,
        metadata={
            "num_tetrons": num_tetrons,
            "total_modes": total_modes,
            "num_bonds": num_bonds,
            "gf2_rank": rank_f2,
            "betti_1_f2": betti_1_f2,
            "dim_h1": betti_1_f2,
            "authority_effect": "None",
        },
    )
    carrier.validate_shape()
    return carrier




