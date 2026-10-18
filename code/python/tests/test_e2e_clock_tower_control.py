"""Exact tests for the QM-211 finite map: finite spectral theorem and clock towers.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest
from finite_qm.use_cases import clock_tower_control as ctc
from finite_qm.use_cases import holonomy_bridge_control as hbc

N = 24


@pytest.fixture(scope="module")
def control() -> dict:
    return ctc.evaluate_clock_tower_control(conductor=N)


def test_finite_spectral_theorem_on_three_clocks(control: dict) -> None:
    spectral = control["spectral"]
    assert spectral["fourier_d4"]["order"] == 4
    assert spectral["fourier_d4"]["multiplicities"] == [2, 1, 1, 0]
    assert spectral["shift_d4"]["multiplicities"] == [1, 1, 1, 1]
    assert spectral["clock_d3"]["order"] == 3
    assert spectral["clock_d3"]["multiplicities"] == [1, 1, 1]
    for row in spectral.values():
        assert row["projectors_sum_to_identity"]
        assert row["projectors_orthogonal_idempotent"]
        assert row["discrete_steps_u_to_t_match_for_all_t"]
        assert row["multiplicities_sum_to_dimension"]
        assert row["hermitian_exponent_vector_is_class_mod_m"]


def test_square_roots_count_two_to_the_occupied_eigenspaces(control: dict) -> None:
    roots = control["square_roots"]
    assert (
        roots["fourier_d4"]["occupied_eigenspaces"],
        roots["fourier_d4"]["square_root_count"],
    ) == (3, 8)
    assert (roots["shift_d4"]["occupied_eigenspaces"], roots["shift_d4"]["square_root_count"]) == (
        4,
        16,
    )
    assert (roots["clock_d3"]["occupied_eigenspaces"], roots["clock_d3"]["square_root_count"]) == (
        3,
        8,
    )
    for row in roots.values():
        assert row["count_is_two_to_occupied"]
        assert row["all_square_to_u"] and row["all_unitary"] and row["all_distinct"]


def test_clocks_refine_along_divisibility_only(control: dict) -> None:
    tower = control["tower"]
    assert tower["zeta4_refines_zeta3"] is None and tower["zeta3_refines_zeta4"] is None
    assert tower["zeta12_refines_zeta3"] == 4
    assert tower["zeta12_refines_zeta4"] == 3
    assert tower["zeta24_refines_zeta12"] == 2
    assert tower["chain_condition_is_divisibility"]
    existing = control["existing_refinement_tower"]
    assert existing["orders"] == [3, 6, 12]
    assert existing["half_step_squares_to_previous"]


def test_swap_has_a_unitary_root_and_no_real_root(control: dict) -> None:
    sto = control["stochastic_control"]
    assert sto["swap_is_stochastic_and_unitary"]
    assert sto["unitary_root_squares_to_swap"] and sto["unitary_root_is_unitary"]
    assert sto["unitary_root_has_real_entries"] is False
    assert sto["real_root_exists"] is False
    assert sto["stochastic_half_step_exists"] is False
    assert sto["rational_root_exists"] is False
    assert sto["rational_root_candidates"] == ["-1", "-1/2", "-1/4", "1/4", "1/2", "1"]
    assert sto["forced_stochastic_candidate"] == [["0", "1"], ["0", "1"]]


def test_ledger_has_three_layers(control: dict) -> None:
    ledger = control["residual_import_ledger"]
    assert [row["layer"] for row in ledger] == ["finite invariant", "completion", "residual import"]
    assert [row["status"] for row in ledger] == ["COMPUTED", "IMPORTED", "IMPORTED"]
    assert "continuity" in ledger[2]["statement"]


def test_refusals() -> None:
    clock3 = hbc.weyl_clock(3, N)
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.spectral_projectors(clock3, 5)
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.matrix_order(hbc.weyl_shift(4, N), 3)
    two = hbc.root_of_unity(N, 0) + hbc.root_of_unity(N, 0)
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.finite_spectral_theorem(ctc.mat_scale(hbc.identity(2, N), two))
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.clock_square_roots(hbc.weyl_shift(4, 12))
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.refines(5, 3, N)
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.evaluate_clock_tower_control(conductor=12)
