import pytest
from omega_engine_governance.contracts import (
    SchemaHash,
    ContractCategory,
    ComponentRole,
    AuthorityEffect,
    ContractStatus,
    ContractDescriptor,
    BoundContract,
    audit_contract,
    ContractAuditError,
    NoAuthorityGuard,
    AuthorityTagged,
    AuthorityViolation,
)


def test_descriptor_creation():
    hash_val = SchemaHash(bytes([0] * 32))
    desc = ContractDescriptor(
        id="anomalon.test_contract",
        category=ContractCategory.Math,
        role=ComponentRole.Validator,
        status=ContractStatus.Canonical,
        authority_effect=AuthorityEffect.EvidenceOnly,
        schema_hash=hash_val,
    )
    assert desc.id == "anomalon.test_contract"
    assert desc.category == ContractCategory.Math
    assert desc.role == ComponentRole.Validator
    assert desc.status == ContractStatus.Canonical
    assert desc.authority_effect == AuthorityEffect.EvidenceOnly
    assert desc.schema_hash == hash_val


def test_audit_success():
    hash_val = SchemaHash(bytes([0] * 32))
    desc = ContractDescriptor(
        id="anomalon.test_contract",
        category=ContractCategory.Math,
        role=ComponentRole.Validator,
        status=ContractStatus.Canonical,
        authority_effect=AuthorityEffect.EvidenceOnly,
        schema_hash=hash_val,
    )

    class TestContract(BoundContract):
        DESCRIPTOR = desc
        Input = type(None)
        Output = type(None)
        Subject = type(None)
        RuntimeState = type(None)

    audited = audit_contract(TestContract)
    assert audited is desc


def test_audit_failure_type_mismatch():
    hash_val = SchemaHash(bytes([0] * 32))
    desc = ContractDescriptor(
        id="anomalon.test_contract",
        category=ContractCategory.Math,
        role=ComponentRole.Validator,
        status=ContractStatus.Canonical,
        authority_effect=AuthorityEffect.EvidenceOnly,
        schema_hash=hash_val,
    )

    class TestContract(BoundContract):
        DESCRIPTOR = desc
        Input = int  # Type mismatch (expected type(None))
        Output = type(None)
        Subject = type(None)
        RuntimeState = type(None)

    with pytest.raises(ContractAuditError):
        audit_contract(TestContract)


def test_no_authority_guard():
    class DummyTagged(AuthorityTagged):
        def __init__(self, art_id: str, effect: AuthorityEffect):
            self.art_id = art_id
            self.effect = effect

        def authority_effect(self) -> AuthorityEffect:
            return self.effect

        def artifact_id(self) -> str:
            return self.art_id

    # OK case
    artifact_ok = DummyTagged("id1", AuthorityEffect.None_)
    NoAuthorityGuard.validate(artifact_ok, "test_artifact")

    # Violating case
    artifact_fail = DummyTagged("id2", AuthorityEffect.StateTransition)
    with pytest.raises(AuthorityViolation) as exc_info:
        NoAuthorityGuard.validate(artifact_fail, "test_artifact")
    assert exc_info.value.artifact_id == "id2"
    assert exc_info.value.artifact_name == "test_artifact"
    assert exc_info.value.effect == AuthorityEffect.StateTransition



