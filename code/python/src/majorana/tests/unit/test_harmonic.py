from __future__ import annotations
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jeremy H. Carroll

"""Invariants for the GF(2) l1 harmonic projection.

Phi_1([r]) = min over alpha of weight(r + d0 alpha) is the minimum-weight
representative of a cohomology class. Two things must hold or the number is
meaningless: it must be a *class* invariant, and it must be the true minimum.
Both are checked against an independent brute force.
"""


import itertools
import random

import pytest

from omega_engine.crates.majorana.carriers.surface_carrier import (
    build_tetron_array,
    logical_class_representative,
)
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix
from omega_engine.crates.majorana.engines.harmonic import (
    L1HarmonicProjection,
    class_coordinates,
    code_distance,
    h1_basis,
    l1_harmonic_projection,
)


def _brute_force_min_weight(d0_rows: list[list[int]], residual: list[int]) -> int:
    """Independent oracle: enumerate every alpha in C^0, not a basis of im d0."""
    d0 = GF2Matrix(d0_rows)
    best = sum(residual)
    for bits in itertools.product((0, 1), repeat=d0.cols):
        image = d0.mat_vec_mul(list(bits))
        best = min(best, sum((a ^ b) for a, b in zip(residual, image)))
    return best


# --- agreement with an independent oracle -------------------------------------


@pytest.mark.parametrize("topology", ["disk", "cylinder", "torus"])
def test_matches_brute_force_over_all_alpha(topology: str) -> None:
    carrier, report = build_tetron_array(2, 2, topology)
    rng = random.Random(20260805)
    for _ in range(8):
        residual = [rng.randint(0, 1) for _ in range(report.num_channels)]
        projection = l1_harmonic_projection(carrier.D0, residual)
        assert projection.exact
        assert projection.weight == _brute_force_min_weight(carrier.D0, residual)


# --- the representative really is in the coset --------------------------------


@pytest.mark.parametrize("topology", ["cylinder", "torus"])
def test_representative_lies_in_the_coset(topology: str) -> None:
    carrier, report = build_tetron_array(3, 3, topology)
    d0 = GF2Matrix(carrier.D0)
    rng = random.Random(7)
    for _ in range(6):
        residual = [rng.randint(0, 1) for _ in range(report.num_channels)]
        projection = l1_harmonic_projection(carrier.D0, residual)

        # weight is the weight of the representative it reports
        assert projection.weight == sum(projection.representative)
        # representative = residual + d0 alpha, with the alpha it reports
        image = d0.mat_vec_mul(projection.alpha)
        assert [a ^ b for a, b in zip(residual, image)] == projection.representative
        # and the difference is genuinely a coboundary
        assert d0.solve(
            [a ^ b for a, b in zip(residual, projection.representative)]
        ) is not None


# --- Phi_1 is a class invariant ------------------------------------------------


@pytest.mark.parametrize("topology", ["disk", "cylinder", "torus"])
def test_phi1_is_constant_on_a_cohomology_class(topology: str) -> None:
    carrier, report = build_tetron_array(3, 3, topology)
    d0 = GF2Matrix(carrier.D0)
    rng = random.Random(99)
    residual = [rng.randint(0, 1) for _ in range(report.num_channels)]
    baseline = l1_harmonic_projection(carrier.D0, residual)

    for _ in range(6):
        alpha = [rng.randint(0, 1) for _ in range(report.num_mzm)]
        shifted = [
            a ^ b for a, b in zip(residual, d0.mat_vec_mul(alpha))
        ]
        moved = l1_harmonic_projection(carrier.D0, shifted)
        assert moved.weight == baseline.weight
        # canonical representative, so the witness is identical too
        assert moved.representative == baseline.representative


def test_exact_residual_has_zero_phi1() -> None:
    carrier, report = build_tetron_array(3, 3, "torus")
    d0 = GF2Matrix(carrier.D0)
    alpha = [0] * report.num_mzm
    alpha[2] = 1
    alpha[5] = 1
    residual = d0.mat_vec_mul(alpha)
    projection = l1_harmonic_projection(carrier.D0, residual)
    assert projection.weight == 0
    assert projection.representative == [0] * report.num_channels


# --- budget honesty ------------------------------------------------------------


def test_budget_exhaustion_reports_an_upper_bound_not_a_lie() -> None:
    carrier, report = build_tetron_array(3, 3, "torus")
    residual = logical_class_representative(report, axis="column", index=0)

    full = l1_harmonic_projection(carrier.D0, residual)
    assert full.exact

    capped = l1_harmonic_projection(carrier.D0, residual, budget=8)
    assert not capped.exact
    assert capped.searched <= 8
    assert capped.weight >= full.weight, "a capped search must never undercut the truth"
    assert capped.weight == sum(capped.representative)


def test_budget_is_recorded_against_the_coset_size() -> None:
    carrier, _ = build_tetron_array(3, 3, "torus")
    projection = l1_harmonic_projection(carrier.D0, [0] * carrier.C1_dim)
    assert projection.coset_size == 2 ** 8  # rank d0 = V - 1 = 8
    assert projection.searched == projection.coset_size
    assert projection.authority_effect == "None"


# --- minimum weights are the topological ones ---------------------------------


@pytest.mark.parametrize("rows,cols", [(2, 3), (3, 3), (3, 4), (4, 3)])
def test_column_class_minimum_weight_is_the_row_count(rows: int, cols: int) -> None:
    """A logical string must cross every lattice row, so its weight is >= rows."""
    carrier, report = build_tetron_array(rows, cols, "torus")
    residual = logical_class_representative(report, axis="column", index=0)
    assert l1_harmonic_projection(carrier.D0, residual).weight == rows


@pytest.mark.parametrize("rows,cols", [(2, 3), (3, 3), (3, 4), (4, 3)])
def test_row_class_minimum_weight_is_the_column_count(rows: int, cols: int) -> None:
    carrier, report = build_tetron_array(rows, cols, "torus")
    residual = logical_class_representative(report, axis="row", index=0)
    assert l1_harmonic_projection(carrier.D0, residual).weight == cols


@pytest.mark.parametrize("rows,cols", [(2, 3), (3, 3), (3, 4), (4, 3)])
def test_torus_code_distance_is_min_of_the_two_extents(rows: int, cols: int) -> None:
    carrier, _ = build_tetron_array(rows, cols, "torus")
    distance, exact = code_distance(carrier.D0, carrier.D1)
    assert exact
    assert distance == min(rows, cols)


@pytest.mark.parametrize("rows,cols", [(2, 3), (3, 3), (2, 4)])
def test_cylinder_code_distance_crosses_the_open_direction(rows: int, cols: int) -> None:
    carrier, _ = build_tetron_array(rows, cols, "cylinder")
    distance, exact = code_distance(carrier.D0, carrier.D1)
    assert exact
    assert distance == rows + 1


def test_disk_has_no_code_distance() -> None:
    """H^1 = 0: there is no nontrivial class, so there is nothing to measure."""
    carrier, _ = build_tetron_array(3, 3, "disk")
    distance, exact = code_distance(carrier.D0, carrier.D1)
    assert distance is None
    assert exact


# --- H^1 basis and class coordinates ------------------------------------------


@pytest.mark.parametrize(
    "topology,expected_dim", [("disk", 0), ("cylinder", 1), ("torus", 2)]
)
def test_h1_basis_has_the_right_dimension(topology: str, expected_dim: int) -> None:
    carrier, _ = build_tetron_array(3, 3, topology)
    basis = h1_basis(carrier.D0, carrier.D1)
    assert basis.dim == expected_dim
    assert len(basis.generators) == expected_dim


def test_generators_are_closed_and_independent() -> None:
    carrier, report = build_tetron_array(3, 3, "torus")
    d0 = GF2Matrix(carrier.D0)
    d1 = GF2Matrix(carrier.D1, cols=report.num_channels)
    basis = h1_basis(carrier.D0, carrier.D1)
    for generator in basis.generators:
        assert not any(d1.mat_vec_mul(generator)), "generator must be closed"
        assert d0.solve(generator) is None, "generator must not be exact"


def test_class_coordinates_are_a_homomorphism() -> None:
    """[r1 + r2] = [r1] + [r2]. Without this the 'type' is not a class label."""
    carrier, report = build_tetron_array(3, 3, "torus")
    basis = h1_basis(carrier.D0, carrier.D1)
    lam1 = logical_class_representative(report, axis="column", index=0)
    lam2 = logical_class_representative(report, axis="row", index=0)
    combined = [a ^ b for a, b in zip(lam1, lam2)]

    c1 = class_coordinates(basis, lam1)
    c2 = class_coordinates(basis, lam2)
    c12 = class_coordinates(basis, combined)
    assert c1 is not None and c2 is not None and c12 is not None
    assert c12 == [a ^ b for a, b in zip(c1, c2)]


def test_the_two_torus_generators_have_distinct_types() -> None:
    carrier, report = build_tetron_array(3, 4, "torus")
    basis = h1_basis(carrier.D0, carrier.D1)
    lam1 = logical_class_representative(report, axis="column", index=0)
    lam2 = logical_class_representative(report, axis="row", index=0)
    c1 = class_coordinates(basis, lam1)
    c2 = class_coordinates(basis, lam2)
    assert c1 != c2
    assert c1 != [0, 0] and c2 != [0, 0]


def test_exact_residual_has_zero_coordinates() -> None:
    carrier, report = build_tetron_array(3, 3, "torus")
    d0 = GF2Matrix(carrier.D0)
    alpha = [0] * report.num_mzm
    alpha[1] = 1
    basis = h1_basis(carrier.D0, carrier.D1)
    assert class_coordinates(basis, d0.mat_vec_mul(alpha)) == [0, 0]


def test_open_residual_has_no_coordinates() -> None:
    """A residual outside ker d1 is not in any cohomology class."""
    carrier, report = build_tetron_array(3, 3, "torus")
    basis = h1_basis(carrier.D0, carrier.D1)
    residual = [0] * report.num_channels
    residual[0] = 1
    assert class_coordinates(basis, residual) is None


def test_class_coordinates_are_constant_on_a_class() -> None:
    carrier, report = build_tetron_array(3, 3, "torus")
    d0 = GF2Matrix(carrier.D0)
    basis = h1_basis(carrier.D0, carrier.D1)
    lam = logical_class_representative(report, axis="column", index=0)
    baseline = class_coordinates(basis, lam)
    rng = random.Random(4242)
    for _ in range(6):
        alpha = [rng.randint(0, 1) for _ in range(report.num_mzm)]
        shifted = [a ^ b for a, b in zip(lam, d0.mat_vec_mul(alpha))]
        assert class_coordinates(basis, shifted) == baseline


def test_projection_dataclass_is_frozen() -> None:
    carrier, _ = build_tetron_array(2, 2, "torus")
    projection = l1_harmonic_projection(carrier.D0, [0] * carrier.C1_dim)
    assert isinstance(projection, L1HarmonicProjection)
    with pytest.raises(Exception):
        projection.weight = 99  # type: ignore[misc]



