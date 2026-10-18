"""Exact E2E tests for QM-212: dressed graph polynomials (DFM) and rational QED g-2 enclosure.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases import dressed_qed_g2_control as dqc
from finite_qm.use_cases import holonomy_bridge_control as hbc


@pytest.fixture(scope="module")
def control() -> dict:
    return dqc.evaluate_dressed_qed_g2_control(conductor=12)


def test_symanzik_u_matches_kirchhoff_dual_cofactor_on_diamond_and_triangle(
    control: dict,
) -> None:
    s = control["dfm_symanzik"]
    assert s["diamond_spanning_tree_count"] == 8
    assert s["diamond_first_betti_number"] == 2
    assert s["u_diamond_unit"] == "8"
    assert s["u_diamond_prime_weights"] == "101"
    assert s["kirchhoff_identity_holds_on_diamond"]
    assert s["kirchhoff_identity_holds_on_triangle"]


def test_ravera_dfm_tree_dressing_is_idempotent_and_gauge_invariant(
    control: dict,
) -> None:
    s = control["dfm_symanzik"]
    assert s["dfm_retraction_idempotent"]
    assert s["dfm_retraction_gauge_invariant"]
    assert s["dfm_every_spanning_tree_neutralizes_its_tree_edges"]
    assert s["dressed_symanzik_gauge_invariant"]
    assert s["all_trees_unimodular_basis_change"]


def test_changing_cotree_holonomy_changes_dressed_symanzik_value() -> None:
    diamond = hbc.FiniteCarrierGraph(4, ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)))
    z = lambda k: hbc.root_of_unity(12, k)  # noqa: E731
    c1 = hbc.U1Cochain(diamond, (z(1), z(0), z(2), z(5), z(7)))
    c2 = hbc.U1Cochain(diamond, (z(1), z(0), z(2), z(8), z(7)))
    tree = diamond.spanning_tree()
    d1 = dqc.dress_cochain_on_tree(c1, tree)
    d2 = dqc.dress_cochain_on_tree(c2, tree)
    alphas1 = [Fraction(1 + hbc.root_exponent(v)) for v in d1.values]
    alphas2 = [Fraction(1 + hbc.root_exponent(v)) for v in d2.values]
    assert dqc.symanzik_u_polynomial(diamond, alphas1) != dqc.symanzik_u_polynomial(
        diamond, alphas2
    )


def test_rational_period_intervals_enclose_known_convergent_values() -> None:
    coeffs = dqc.qed_loop_coefficients()
    assert coeffs["pi"].width < Fraction(1, 10**25)
    coarse_pi = dqc.RationalInterval(
        Fraction(3141592653589793, 10**15),
        Fraction(3141592653589794, 10**15),
    )
    assert coarse_pi.contains(coeffs["pi"])
    assert coeffs["ln2"].width < Fraction(1, 10**15)
    assert coeffs["zeta3"].width < Fraction(1, 10**14)
    assert coeffs["zeta5"].width < Fraction(1, 10**12)


def test_qed_c1_c2_c3_and_ae_enclosure_to_twelve_decimals(control: dict) -> None:
    q = control["qed_g2"]
    assert q["c1_exact"] == "1/2"
    assert q["c2_width_lt_1e14"]
    assert q["c2_decimal_12"] == "-0.328478965579"
    assert q["c3_width_lt_1e12"]
    assert q["c3_decimal_12"] == "1.181241456587"
    assert q["ae_1_to_3_width_lt_1e15"]
    assert q["ae_1_to_3_12_digits_agree"]
    assert q["ae_1_to_3_decimal_12"] == "0.001159652231"
    assert q["ae_1_to_4_width_lt_1e12"]
    assert q["ae_1_to_4_12_digits_agree"]
    assert q["ae_1_to_4_decimal_12"] == "0.001159652175"
    assert q["ae_1_to_4_12_digits_enclose_115965217"]


def test_nonpositive_edge_weight_or_inverted_interval_is_refused() -> None:
    diamond = hbc.FiniteCarrierGraph(4, ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)))
    with pytest.raises(dqc.DressedQedControlRefusal):
        dqc.symanzik_u_polynomial(diamond, [Fraction(1), Fraction(0), Fraction(1), Fraction(1), Fraction(1)])
    with pytest.raises(dqc.DressedQedControlRefusal):
        dqc.RationalInterval(Fraction(2), Fraction(1))
    with pytest.raises(dqc.DressedQedControlRefusal):
        dqc.RationalInterval(Fraction(-1), Fraction(1)).reciprocal()


def test_non_spanning_edge_subset_is_refused_by_dressing() -> None:
    diamond = hbc.FiniteCarrierGraph(4, ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)))
    z = lambda k: hbc.root_of_unity(12, k)  # noqa: E731
    cochain = hbc.U1Cochain(diamond, (z(1), z(0), z(2), z(5), z(7)))
    # Edges (0, 1), (0, 2), (1, 2) form a triangle on {0,1,2} and isolate locus 3
    with pytest.raises(dqc.DressedQedControlRefusal):
        dqc.dress_cochain_on_tree(cochain, (0, 1, 4))


def test_residual_import_ledger_names_three_layers(control: dict) -> None:
    ledger = control["residual_import_ledger"]
    assert [row["layer"] for row in ledger] == [
        "finite invariant",
        "completion",
        "residual import",
    ]
    assert ledger[0]["status"] == "COMPUTED"
    assert ledger[2]["status"] == "IMPORTED"
