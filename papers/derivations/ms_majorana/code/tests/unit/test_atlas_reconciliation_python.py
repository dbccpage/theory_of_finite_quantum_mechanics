from omega_engine_governance.contracts import AuthorityEffect
from omega_engine.crates.contract_core.atlas_reconciliation import (
    ReconciliationRow,
    AuthorityBasis,
    AuthClaim,
    TriState,
    validate_row,
    check_governance_strict,
    GovChange,
)


def test_sample_good_row_passes_validation():
    row = ReconciliationRow.sample_good()
    findings = validate_row(row)
    assert not findings, f"Expected no findings, got: {findings}"


def test_invariant_i_violates_when_factors_false_no_class():
    row = ReconciliationRow.sample_good()
    row.primitive_difference.factors_through_quotient = False
    row.primitive_difference.residual_class = ""
    findings = validate_row(row)
    assert any("invariant-I" in f for f in findings)


def test_invariant_ii_violates_on_invalid_cochain():
    row = ReconciliationRow.sample_good()
    row.cochain_validity.d0 = [[1]]
    row.cochain_validity.d1 = [[1]]
    row.cochain_validity.d1_d0_zero = TriState.True_
    findings = validate_row(row)
    assert any("invariant-II" in f for f in findings)


def test_invariant_iii_identity_witness():
    row = ReconciliationRow.sample_good()
    row.identity_witness.identity_loss_risk = True
    findings = validate_row(row)
    assert any("invariant-III" in f for f in findings)


def test_counterfeit_authority_basis_rejected():
    row = ReconciliationRow.sample_good()
    row.authority_basis = [AuthClaim("forged", AuthorityBasis.None_)]
    findings = validate_row(row)
    assert any("counterfeit authority" in f for f in findings)


def test_authority_ceiling_drift_rejected():
    row = ReconciliationRow.sample_good()
    row.declared_authority_effect = AuthorityEffect.StateTransition
    row.role_pinned_ceiling = AuthorityEffect.FactOnly
    findings = validate_row(row)
    assert any("ceiling drift" in f for f in findings)


def test_strict_governance_checks():
    change = GovChange.council_self_certify()
    findings = check_governance_strict(change)
    assert any("self-certification refused" in f for f in findings)

    change2 = GovChange.licensed_lift_full_10_fields()
    findings2 = check_governance_strict(change2)
    assert not findings2


