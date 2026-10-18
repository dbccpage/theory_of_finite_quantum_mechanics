"""Exact tests for the QM-209 finite map: context parity and Weyl commutator holonomy.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest
from finite_qm.use_cases import context_parity_control as cpc

N = 12


@pytest.fixture(scope="module")
def control() -> dict:
    return cpc.evaluate_context_parity_control(conductor=N)


def test_peres_mermin_cokernel_is_the_total_parity(control: dict) -> None:
    pm = control["peres_mermin"]
    assert pm["all_contexts_commute"]
    assert pm["context_signs"] == [1, 1, 1, 1, 1, -1]
    assert pm["sign_product"] == -1
    assert pm["incidence_rank_f2"] == 5
    assert pm["cokernel_dimension"] == 1
    assert pm["every_observable_in_two_contexts"]
    assert pm["assignment_exists"] is False
    assert pm["obstruction_class_total_parity"] == 1
    assert pm["even_control_assignment_exists"]
    assert pm["even_control_solution_checks"]


def test_flipping_one_context_sign_removes_the_obstruction(control: dict) -> None:
    pm = control["peres_mermin"]
    rows = [[1 if o in ctx else 0 for o in pm["observables"]] for ctx in pm["contexts"]]
    rhs = [1 if s == -1 else 0 for s in pm["context_signs"]]
    assert cpc.f2_eliminate(rows, rhs)["consistent"] is False
    flipped = list(rhs)
    flipped[0] ^= 1
    solved = cpc.f2_eliminate(rows, flipped)
    assert solved["consistent"] is True
    assert cpc.f2_apply(rows, solved["solution"]) == flipped


def test_f2_elimination_on_a_small_system() -> None:
    rows = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
    odd = cpc.f2_eliminate(rows, [1, 1, 1])
    assert odd["rank"] == 2 and odd["consistent"] is False
    even = cpc.f2_eliminate(rows, [1, 1, 0])
    assert even["consistent"] is True
    assert cpc.f2_apply(rows, even["solution"]) == [1, 1, 0]
    with pytest.raises(cpc.ContextControlRefusal):
        cpc.f2_eliminate([[2, 0]], [0])


def test_weyl_commutator_holonomy_table(control: dict) -> None:
    census = control["weyl_census"]
    assert census[3]["holonomy_exponents_mod_conductor"] == [[0, 0, 0], [0, 8, 4], [0, 4, 8]]
    assert census[4]["holonomy_exponents_mod_conductor"] == [
        [0, 0, 0, 0],
        [0, 9, 6, 3],
        [0, 6, 0, 6],
        [0, 3, 6, 9],
    ]
    for d in (3, 4):
        assert census[d]["dimension"] == d
        assert census[d]["trivial_exactly_when_d_divides_ab"]
        assert census[d]["values_are_dth_roots"]


def test_holonomy_is_conjugation_invariant_and_diagonal_frames_give_none(control: dict) -> None:
    inv = control["conjugation_invariance"]
    assert inv["base_holonomy_exponent"] == 9
    assert inv["invariant_under"] == {"fourier": True, "diagonal_phases": True}
    assert inv["diagonal_pair_has_trivial_holonomy"]
    assert inv["commuting_powers_have_trivial_holonomy"]


def test_ledger_has_three_layers(control: dict) -> None:
    ledger = control["residual_import_ledger"]
    assert [row["layer"] for row in ledger] == ["finite invariant", "completion", "residual import"]
    assert [row["status"] for row in ledger] == ["COMPUTED", "IMPORTED", "IMPORTED"]
    assert "second context" in ledger[2]["statement"]


def test_refuses_conductor_without_mu12() -> None:
    with pytest.raises(cpc.ContextControlRefusal):
        cpc.evaluate_context_parity_control(conductor=10)
