from __future__ import annotations
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jeremy H. Carroll

"""Invariants for the homology-correct tetron array carrier.

The invariant under test is that ``dim H^1`` is the topology's, not zero.
The carrier this replaces (``carriers.tetron_carrier``) satisfies every other
property here and fails exactly this one, at every array size.
"""


import pytest

from omega_engine.crates.majorana.carriers.surface_carrier import (
    TOPOLOGIES,
    build_tetron_array,
    logical_class_representative,
)
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix
from omega_engine.crates.majorana.engines.terminalizer import terminalize, validate_complex


# --- d1 . d0 = 0 --------------------------------------------------------------


@pytest.mark.parametrize("topology", TOPOLOGIES)
@pytest.mark.parametrize("rows,cols", [(2, 2), (2, 3), (3, 3), (3, 2)])
def test_cochain_relation_holds(topology: str, rows: int, cols: int) -> None:
    carrier, _ = build_tetron_array(rows, cols, topology)
    d0 = GF2Matrix(carrier.D0)
    d1 = GF2Matrix(carrier.D1, cols=d0.rows)
    assert validate_complex(d0, d1), f"d1 . d0 != 0 for {topology} {rows}x{cols}"


# --- the cell counts are the ones the design predicts --------------------------


@pytest.mark.parametrize(
    "topology,rows,cols,exp_v,exp_e,exp_f",
    [
        ("disk", 2, 3, 3 * 4, 2 * 4 + 3 * 3, 6),
        ("cylinder", 2, 3, 3 * 3, 2 * 3 + 3 * 3, 6),
        ("torus", 2, 3, 2 * 3, 2 * 2 * 3, 6),
    ],
)
def test_cell_counts(
    topology: str, rows: int, cols: int, exp_v: int, exp_e: int, exp_f: int
) -> None:
    _, report = build_tetron_array(rows, cols, topology)
    assert (report.num_mzm, report.num_channels, report.num_islands) == (
        exp_v,
        exp_e,
        exp_f,
    )


# --- THE invariant: dim H^1 is 0 / 1 / 2 by topology --------------------------


@pytest.mark.parametrize("rows,cols", [(2, 2), (2, 3), (3, 3), (3, 4), (4, 4)])
@pytest.mark.parametrize(
    "topology,expected_b1", [("disk", 0), ("cylinder", 1), ("torus", 2)]
)
def test_dim_h1_matches_topology(
    rows: int, cols: int, topology: str, expected_b1: int
) -> None:
    _, report = build_tetron_array(rows, cols, topology)
    assert report.dim_h1 == expected_b1, (
        f"{topology} {rows}x{cols}: dim H^1 = {report.dim_h1}, expected {expected_b1}"
    )


@pytest.mark.parametrize("topology", TOPOLOGIES)
@pytest.mark.parametrize("rows,cols", [(2, 2), (3, 3), (3, 4)])
def test_dim_h1_agrees_with_euler_characteristic(
    topology: str, rows: int, cols: int
) -> None:
    """dim H^1 = 1 - chi (bounded surfaces) or 2 - chi (closed)."""
    _, report = build_tetron_array(rows, cols, topology)
    closed = topology == "torus"
    predicted = (2 if closed else 1) - report.euler_characteristic
    assert report.dim_h1 == predicted


def test_the_old_carrier_is_homologically_trivial() -> None:
    """Pins the defect this module exists to fix.

    If ``tetron_carrier`` ever grows real homology this test fails loudly and
    the two builders must be reconciled rather than silently diverge.
    """
    from omega_engine.crates.majorana.carriers.tetron_carrier import build_tetron_array_carrier

    for num_tetrons in (1, 2, 3, 4):
        carrier = build_tetron_array_carrier(num_tetrons)
        d0 = GF2Matrix(carrier.D0)
        d1 = GF2Matrix(carrier.D1, cols=d0.rows)
        rank_d0 = len(d0.rref()[1])
        rank_d1 = len(d1.rref()[1]) if d1.rows else 0
        dim_h1 = (d0.rows - rank_d1) - rank_d0
        assert dim_h1 == 0, "tetron_carrier grew homology; reconcile the builders"


# --- carrier is a valid MajoranaParityCarrier ---------------------------------


@pytest.mark.parametrize("topology", TOPOLOGIES)
def test_carrier_shape_validates(topology: str) -> None:
    carrier, report = build_tetron_array(3, 3, topology)
    carrier.validate_shape()
    assert carrier.C0_dim == report.num_mzm
    assert carrier.C1_dim == report.num_channels
    assert carrier.C2_dim == report.num_islands
    assert carrier.metadata["authority_effect"] == "None"


def test_rejects_degenerate_periodic_sizes() -> None:
    """A periodic direction of extent 1 makes self-loop channels; refuse it."""
    with pytest.raises(ValueError):
        build_tetron_array(1, 1, "torus")
    with pytest.raises(ValueError):
        build_tetron_array(2, 1, "torus")
    with pytest.raises(ValueError):
        build_tetron_array(1, 1, "cylinder")


def test_rejects_unknown_topology() -> None:
    with pytest.raises(ValueError):
        build_tetron_array(2, 2, "klein_bottle")


# --- explicit logical generators are closed and non-exact ---------------------


@pytest.mark.parametrize("rows,cols", [(2, 3), (3, 3), (3, 4)])
def test_column_generator_is_a_nontrivial_class_on_torus(rows: int, cols: int) -> None:
    carrier, report = build_tetron_array(rows, cols, "torus")
    r = logical_class_representative(report, axis="column", index=0)
    result = terminalize(carrier.D0, carrier.D1, r)
    assert result["terminal_status"] == "ClosedResidual"
    assert sum(r) == rows, "column generator should have one channel per lattice row"


@pytest.mark.parametrize("rows,cols", [(2, 3), (3, 3), (3, 4)])
def test_row_generator_is_a_nontrivial_class_on_torus(rows: int, cols: int) -> None:
    carrier, report = build_tetron_array(rows, cols, "torus")
    r = logical_class_representative(report, axis="row", index=0)
    result = terminalize(carrier.D0, carrier.D1, r)
    assert result["terminal_status"] == "ClosedResidual"
    assert sum(r) == cols


def test_row_generator_is_exact_on_cylinder() -> None:
    """The cylinder has only one class; the row generator is the exact one.

    This is not decoration: it is what distinguishes b1=1 from b1=2 and it is
    the reason a cylinder cannot exercise class typing.
    """
    carrier, report = build_tetron_array(3, 4, "cylinder")
    r = logical_class_representative(report, axis="row", index=0)
    assert terminalize(carrier.D0, carrier.D1, r)["terminal_status"] == "Exact"

    c = logical_class_representative(report, axis="column", index=0)
    assert terminalize(carrier.D0, carrier.D1, c)["terminal_status"] == "ClosedResidual"


@pytest.mark.parametrize("axis", ["row", "column"])
def test_both_generators_are_exact_on_disk(axis: str) -> None:
    carrier, report = build_tetron_array(3, 4, "disk")
    r = logical_class_representative(report, axis=axis, index=0)
    assert terminalize(carrier.D0, carrier.D1, r)["terminal_status"] == "Exact"


# --- the three terminals all occur on a torus carrier -------------------------


def test_single_channel_error_is_an_open_obstruction() -> None:
    """One faulty channel violates the parity constraint of its two islands."""
    carrier, report = build_tetron_array(3, 3, "torus")
    r = [0] * report.num_channels
    r[0] = 1
    result = terminalize(carrier.D0, carrier.D1, r)
    assert result["terminal_status"] == "OpenObstruction"
    assert sum(result["coherence_witness"]) == 2, "an edge borders exactly two islands"


def test_gauge_residual_is_exact() -> None:
    carrier, report = build_tetron_array(3, 3, "torus")
    d0 = GF2Matrix(carrier.D0)
    alpha = [0] * report.num_mzm
    alpha[0] = 1
    alpha[4] = 1
    r = d0.mat_vec_mul(alpha)
    assert terminalize(carrier.D0, carrier.D1, r)["terminal_status"] == "Exact"



