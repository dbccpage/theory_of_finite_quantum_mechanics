"""Exact exhaustive tests for finite Boolean cochain algebra laws."""

import pytest

from omega_engine.crates.solver.solv_finite_cochain_law import (
    FINITE_COHCHAIN_LAW_SCHEMA,
    FiniteCochainLawError,
    solve_finite_boolean_cochain_laws,
)


D0 = ((-1, 1, 0), (0, -1, 1), (-1, 0, 1))
D1 = ((1, 1, -1),)


def test_exhaustive_boolean_carriers_discharge_displayed_finite_laws():
    receipt = solve_finite_boolean_cochain_laws((3, 3, 1), D0, D1)
    assert receipt.schema == FINITE_COHCHAIN_LAW_SCHEMA
    assert receipt.conformant is True
    assert receipt.coefficient_group_laws is True
    assert receipt.cochain_group_laws == (True, True, True)
    assert receipt.d0_homomorphism is True
    assert receipt.d1_homomorphism is True
    assert receipt.delta1_delta0_zero is True
    assert receipt.state_counts == (8, 8, 2)
    assert receipt.ordered_pairs_checked == (64, 64, 4)
    assert receipt.authority_effect == "None"
    assert len(receipt.evidence_sha256) == 64


def test_homomorphism_laws_do_not_hide_a_bad_chain_composite():
    receipt = solve_finite_boolean_cochain_laws((3, 3, 1), D0, ((1, 0, 0),))
    assert receipt.d0_homomorphism is True
    assert receipt.d1_homomorphism is True
    assert receipt.delta1_delta0_zero is False
    assert receipt.conformant is False


def test_mod_two_receipt_is_orientation_independent():
    flipped = tuple(tuple(-value for value in row) for row in D0)
    original = solve_finite_boolean_cochain_laws((3, 3, 1), D0, D1)
    reoriented = solve_finite_boolean_cochain_laws((3, 3, 1), flipped, D1)
    assert reoriented.canonical_payload() == original.canonical_payload()
    assert reoriented.evidence_sha256 == original.evidence_sha256


def test_resource_and_shape_limits_fail_closed():
    with pytest.raises(FiniteCochainLawError, match="max_states"):
        solve_finite_boolean_cochain_laws((4, 1, 0), ((0, 0, 0, 0),), (), max_states=8)
    with pytest.raises(FiniteCochainLawError, match="shape"):
        solve_finite_boolean_cochain_laws((2, 2, 1), ((1, 0),), ((1, 1),))


