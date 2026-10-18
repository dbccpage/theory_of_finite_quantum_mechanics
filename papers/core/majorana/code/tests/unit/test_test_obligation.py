"""Test suite for TestObligation module (INTAKE-S7)."""

import pytest
from _tests_unit.test_obligation import (
    TestObligation,
    TestObligationStatus,
    TestObligationRefuse,
)


def test_test_obligation_basic():
    ob = TestObligation(
        obligation_id="TO-001",
        target_symbol="try_upgrade_status",
        assertion_expr="assert try_upgrade_status('EXTRACTED', 'PROVED') raises ClaimIrRefuse",
    )
    assert ob.status == TestObligationStatus.PROPOSED
    status = ob.verify_evidence("evidence/contract_preflight.md")
    assert status == TestObligationStatus.VERIFIED_NON_VACUOUS
    assert ob.authority_effect == "None"


def test_test_obligation_tautology_refused():
    ob = TestObligation(
        obligation_id="TO-002",
        target_symbol="dummy_fn",
        assertion_expr="assert True",
    )
    assert ob.status == TestObligationStatus.REFUSED_TAUTOLOGY
    with pytest.raises(TestObligationRefuse):
        ob.verify_evidence("evidence/fake.md")


def test_test_obligation_authority_launder():
    with pytest.raises(TestObligationRefuse):
        TestObligation(
            obligation_id="TO-003",
            target_symbol="dummy_fn",
            assertion_expr="assert x == 5",
            authority_effect="PROMOTED",
        )



