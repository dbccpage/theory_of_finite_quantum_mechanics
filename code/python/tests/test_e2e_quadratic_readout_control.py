"""Exact tests for the QM-208 finite map: quadratic readout, Sorkin selection, interference.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases import holonomy_bridge_control as hbc
from finite_qm.use_cases import quadratic_readout_control as qrc

N = 12


@pytest.fixture(scope="module")
def control() -> dict:
    return qrc.evaluate_quadratic_readout_control(conductor=N)


def test_phase_blind_monomials_are_exactly_the_diagonal(control: dict) -> None:
    census = control["monomial_census"]
    assert census["monomials_examined"] == 14
    assert [tuple(m) for m in census["phase_blind"]] == [(1, 1), (2, 2)]
    assert census["blind_are_exactly_diagonal"]
    assert len(census["phase_sensitive"]) == 12


def test_sorkin_i3_selects_beta_zero_on_the_grid(control: dict) -> None:
    sel = control["sorkin_selection"]
    assert sel["selection_is_exactly_beta_zero"]
    assert len(sel["rows"]) == 16
    assert all(Fraction(str(b)) == 0 for _, b in sel["selected"])
    assert len(sel["selected"]) == 4
    assert control["quartic_i3_on_unit_triple_is_36"]
    assert str(control["quartic_i3_on_unit_triple"]) == "36"
    assert control["quadratic_i3_on_unit_triple_is_zero"]


def test_quartic_term_breaks_sorkin_on_the_unit_triple() -> None:
    one = hbc.root_of_unity(N, 0)
    rows = qrc.sorkin_selection(N, [(Fraction(1), Fraction(1))], [[one, one, one]])["rows"]
    assert rows[0]["i3_zero_on_all_triples"] is False
    assert str(rows[0]["i3_values"][0]) == "36"
    quadratic = qrc.sorkin_selection(N, [(Fraction(1), Fraction(0))], [[one, one, one]])["rows"]
    assert quadratic[0]["i3_zero_on_all_triples"] is True


def test_two_report_interference_is_born_weight_times_holonomy(control: dict) -> None:
    two = control["two_report_interference"]
    assert str(two["i2"]) == "1"
    assert two["holonomy_exponent"] == 10
    assert two["i2_equals_born_weight_times_two_re_holonomy"]
    assert two["i2_gauge_invariant"]
    assert two["holonomy_factorizes_through_cycle_invariants"]
    assert control["three_report_interference"]["quadratic_i3_zero"]


def test_quadratic_interferes_where_l1_is_additive(control: dict) -> None:
    inter = control["interference"]
    assert inter["quadratic_has_some_interference"]
    assert inter["l1_additive_on_all_pairs"]
    assert [str(r["i2_quadratic"]) for r in inter["rows"]][:3] == ["2", "-2", "0"]
    assert all(str(r["i2_l1"]) == "0" for r in inter["rows"])
    assert all(r["i2_equals_two_re_cross_term"] for r in inter["rows"])


def test_amplitudes_live_in_finite_extensions(control: dict) -> None:
    ext = control["amplitude_extensions"]
    assert ext["sqrt3_squared_is_3"]
    assert ext["weight_3_over_4_has_amplitude_in_q_zeta12"]
    assert ext["every_extension_is_finite"]
    assert [r["extension"] for r in ext["rows"]] == ["Q", "Q", "Q(sqrt(2))", "Q(sqrt(3/4))", "Q"]
    assert qrc.rational_square_root(Fraction(9, 16)) == Fraction(3, 4)
    assert qrc.rational_square_root(Fraction(2)) is None
    assert qrc.rational_square_root(Fraction(0)) == Fraction(0)


def test_ledger_has_three_layers(control: dict) -> None:
    ledger = control["residual_import_ledger"]
    assert [row["layer"] for row in ledger] == ["finite invariant", "completion", "residual import"]
    assert [row["status"] for row in ledger] == ["COMPUTED", "none needed", "IMPORTED"]
    assert "add-then-square" in ledger[2]["statement"]


def test_refusals() -> None:
    with pytest.raises(qrc.ReadoutControlRefusal):
        qrc.monomial_readout(0, 0, N)
    with pytest.raises(qrc.ReadoutControlRefusal):
        qrc.phase_blind_monomial_census(N, N)
    with pytest.raises(qrc.ReadoutControlRefusal):
        qrc.evaluate_quadratic_readout_control(conductor=10)
