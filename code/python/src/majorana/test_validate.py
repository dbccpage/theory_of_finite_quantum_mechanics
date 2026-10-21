"""Negative controls for omega_contract_core.validate.

Mirrors the Rust suite in `omega_engine/crates/omega_contract_core/src/validate.rs`
(`constitution_tests`, `descriptor_tests`). `validate.py` is 487 lines of authority
firewall that no test imported before 2026-07-28; role validators reachable from
concrete product descriptors are exercised on the Rust side by
`omega_contracts::descriptors::product_spine`, so what is pinned here is what neither
covered: the constitutional block, the lift-license authority boundary, registry
duplicate-id, and the Terminalizer deprecation gate.

`omega_engine_py/omega_contract_core` carries no MIRROR_MANIFEST, so Rust<->Python
agreement here is a claim, not a guarantee. These tests assert the same error strings
as the Rust suite, which is what makes a divergence visible.
"""

import pytest

from omega_engine_governance.contracts import (
    AuthorityEffect,
    ComponentRole,
    ContractCategory,
    ContractStatus,
)
from omega_engine_governance.contracts.kinds import Capability, CapabilityPolicy
from omega_engine_governance.contracts.schema import (
    ArtifactFamily,
    AuthorityLayer,
    ConstitutionalBlock,
    ContractDescriptor,
    ReplayBlock,
    WitnessesBlock,
)
from omega_engine_governance.contracts.descriptor_validation import (
    expected_layer_for_family,
    validate_registry,
)




def valid_constitution(
    emits: ArtifactFamily, layer: AuthorityLayer
) -> ConstitutionalBlock:
    """Satisfies every clause. Each test breaks exactly one thing."""
    return ConstitutionalBlock(
        emits=emits,
        authority_layer=layer,
        contract_dependencies=["anomalon.some.dependency"],
        law_refs=[],
        forbidden_later_layers=[],
        replay_certificates=["schema_hash"],
    )


def bare(role: ComponentRole, authority_effect: AuthorityEffect) -> ContractDescriptor:
    return ContractDescriptor(
        id="anomalon.test.subject",
        name="test subject",
        category=ContractCategory.Lifts,
        role=role,
        status=ContractStatus.Canonical,
        authority_effect=authority_effect,
    )


def valid_lift_license() -> ContractDescriptor:
    d = bare(ComponentRole.LiftLicense, AuthorityEffect.AuthorizesTransition)
    d.constitution = valid_constitution(
        ArtifactFamily.ActionLicense, AuthorityLayer.Action
    )
    d.constraints.scope_bound = True
    d.constraints.non_transferable = True
    d.constraints.authority_does_not_exceed_evidence = True
    d.constraints.mutation_forbidden = True
    d.replay = ReplayBlock(required=["schema_hash"])
    d.witnesses = WitnessesBlock(required=["operator_signature"])
    d.capabilities = CapabilityPolicy(
        forbidden=[Capability.ExecuteStateTransition, Capability.RuntimeMutation]
    )
    return d


EXPECTED_FAMILY_LAYERS = [
    (ArtifactFamily.StructureArtifact, AuthorityLayer.Structure),
    (ArtifactFamily.EvidenceEnvelope, AuthorityLayer.Evidence),
    (ArtifactFamily.FactEnvelope, AuthorityLayer.Fact),
    (ArtifactFamily.DecisionEnvelope, AuthorityLayer.Judgment),
    (ArtifactFamily.ActionLicense, AuthorityLayer.Action),
    (ArtifactFamily.Action, AuthorityLayer.Action),
    (ArtifactFamily.Record, AuthorityLayer.Record),
]




def test_baseline_constitution_validates():
    assert (
        valid_constitution(
            ArtifactFamily.EvidenceEnvelope, AuthorityLayer.Evidence
        ).validate()
        is None
    )


def test_constitution_forbidding_its_own_authority_layer_rejected():
    c = valid_constitution(ArtifactFamily.EvidenceEnvelope, AuthorityLayer.Evidence)
    c.forbidden_later_layers = [AuthorityLayer.Evidence]
    with pytest.raises(
        ValueError, match="constitution cannot forbid its own authority layer"
    ):
        c.validate()


def test_forbidding_a_different_layer_is_permitted():
    c = valid_constitution(ArtifactFamily.EvidenceEnvelope, AuthorityLayer.Evidence)
    c.forbidden_later_layers = [AuthorityLayer.Action]
    assert c.validate() is None


def test_every_artifact_family_validates_at_its_expected_layer():
    """Class 1: pins all seven arms of the family -> layer map in one law."""
    assert len(EXPECTED_FAMILY_LAYERS) == 7, "ArtifactFamily changed; extend the map"
    for family, layer in EXPECTED_FAMILY_LAYERS:
        assert valid_constitution(family, layer).validate() is None, (
            f"{family} at {layer}"
        )


def test_expected_layer_for_family_agrees_with_the_map():
    for family, layer in EXPECTED_FAMILY_LAYERS:
        assert expected_layer_for_family(family) == layer


def test_no_artifact_family_validates_at_the_runtime_layer():
    """Class 1 dual: Runtime is never an expected layer, so it is wrong for every family."""
    for family, expected in EXPECTED_FAMILY_LAYERS:
        c = valid_constitution(family, AuthorityLayer.Runtime)
        with pytest.raises(
            ValueError, match=f"{family.name} must use {expected.name} authority layer"
        ):
            c.validate()


def test_structure_layer_without_dependency_or_law_ref_rejected():
    c = valid_constitution(ArtifactFamily.StructureArtifact, AuthorityLayer.Structure)
    c.contract_dependencies = []
    c.law_refs = []
    with pytest.raises(
        ValueError, match="Structure and Fact layers require at least one"
    ):
        c.validate()


def test_fact_layer_without_dependency_or_law_ref_rejected():
    c = valid_constitution(ArtifactFamily.FactEnvelope, AuthorityLayer.Fact)
    c.contract_dependencies = []
    c.law_refs = []
    with pytest.raises(
        ValueError, match="Structure and Fact layers require at least one"
    ):
        c.validate()


def test_law_ref_alone_grounds_a_fact_layer():
    c = valid_constitution(ArtifactFamily.FactEnvelope, AuthorityLayer.Fact)
    c.contract_dependencies = []
    c.law_refs = ["anomalon.law.some_law"]
    assert c.validate() is None


def test_evidence_layer_needs_no_dependency_or_law_ref():
    c = valid_constitution(ArtifactFamily.EvidenceEnvelope, AuthorityLayer.Evidence)
    c.contract_dependencies = []
    c.law_refs = []
    assert c.validate() is None


def test_constitution_without_schema_hash_certificate_rejected():
    c = valid_constitution(ArtifactFamily.EvidenceEnvelope, AuthorityLayer.Evidence)
    c.replay_certificates = ["policy_hash"]
    with pytest.raises(
        ValueError, match="constitution must require 'schema_hash' certificate"
    ):
        c.validate()


def test_empty_replay_certificates_rejected():
    c = valid_constitution(ArtifactFamily.EvidenceEnvelope, AuthorityLayer.Evidence)
    c.replay_certificates = []
    with pytest.raises(
        ValueError, match="constitution must require 'schema_hash' certificate"
    ):
        c.validate()




def test_valid_lift_license_accepted():
    assert valid_lift_license().validate() is None


def test_lift_license_without_constitution_rejected():
    d = valid_lift_license()
    d.constitution = None
    with pytest.raises(ValueError, match="contract requires constitution block"):
        d.validate()


def test_lift_license_emitting_wrong_family_rejected():
    d = valid_lift_license()
    d.constitution.emits = ArtifactFamily.Action
    with pytest.raises(ValueError, match="contract must emit ActionLicense"):
        d.validate()


def test_lift_license_with_wrong_authority_effect_rejected():
    d = valid_lift_license()
    d.authority_effect = AuthorityEffect.EvidenceOnly
    with pytest.raises(
        ValueError,
        match="lift license must have authority_effect = AuthorizesTransition",
    ):
        d.validate()


def test_lift_license_without_scope_bound_rejected():
    d = valid_lift_license()
    d.constraints.scope_bound = None
    with pytest.raises(ValueError, match="lift license must be scope bound"):
        d.validate()


def test_lift_license_without_non_transferable_rejected():
    d = valid_lift_license()
    d.constraints.non_transferable = False
    with pytest.raises(ValueError, match="lift license must be non-transferable"):
        d.validate()


def test_lift_license_with_authority_exceeding_evidence_rejected():
    d = valid_lift_license()
    d.constraints.authority_does_not_exceed_evidence = None
    with pytest.raises(
        ValueError, match="lift license authority must not exceed evidence"
    ):
        d.validate()


def test_lift_license_without_mutation_forbidden_rejected():
    d = valid_lift_license()
    d.constraints.mutation_forbidden = None
    with pytest.raises(ValueError, match="lift license must forbid mutation"):
        d.validate()


def test_lift_license_without_replay_block_rejected():
    d = valid_lift_license()
    d.replay = None
    with pytest.raises(ValueError, match="lift license must declare replay block"):
        d.validate()


def test_lift_license_with_empty_replay_required_rejected():
    d = valid_lift_license()
    d.replay = ReplayBlock(required=[])
    with pytest.raises(ValueError, match="lift license must declare replay block"):
        d.validate()


def test_lift_license_without_witnesses_rejected():
    d = valid_lift_license()
    d.witnesses = None
    with pytest.raises(
        ValueError, match="lift license must declare witness requirements"
    ):
        d.validate()


def test_lift_license_with_empty_witnesses_rejected():
    d = valid_lift_license()
    d.witnesses = WitnessesBlock(required=[])
    with pytest.raises(
        ValueError, match="lift license must declare witness requirements"
    ):
        d.validate()


def test_lift_license_permitting_state_transition_rejected():
    d = valid_lift_license()
    d.capabilities.forbidden = [Capability.RuntimeMutation]
    with pytest.raises(
        ValueError, match="lift license must not execute state transitions"
    ):
        d.validate()


def test_lift_license_permitting_runtime_mutation_rejected():
    d = valid_lift_license()
    d.capabilities.forbidden = [Capability.ExecuteStateTransition]
    with pytest.raises(ValueError, match="lift license must not mutate runtime"):
        d.validate()




def registry_member(contract_id: str) -> ContractDescriptor:
    """Policy is the no-op arm unless id == 'anomalon.policy', isolating registry
    behaviour from role behaviour."""
    d = bare(ComponentRole.Policy, AuthorityEffect.None_)
    d.id = contract_id
    return d


def test_validate_registry_accepts_distinct_ids():
    assert (
        validate_registry(
            [registry_member("anomalon.a"), registry_member("anomalon.b")]
        )
        is None
    )


def test_validate_registry_rejects_duplicate_ids():
    members = [
        registry_member("anomalon.a"),
        registry_member("anomalon.b"),
        registry_member("anomalon.a"),
    ]
    with pytest.raises(ValueError, match="duplicate contract id: anomalon.a"):
        validate_registry(members)


def test_validate_registry_reports_the_failing_member_by_id():
    bad = registry_member("anomalon.broken")
    bad.name = "  "
    with pytest.raises(
        ValueError, match="contract 'anomalon.broken' failed validation"
    ):
        validate_registry([bad])




def test_canonical_terminalizer_rejected():
    d = bare(ComponentRole.Terminalizer, AuthorityEffect.None_)
    with pytest.raises(
        ValueError, match="Terminalizer is deprecated; use TerminalMapper"
    ):
        d.validate()


def test_deprecated_terminalizer_accepted():
    d = bare(ComponentRole.Terminalizer, AuthorityEffect.None_)
    d.status = ContractStatus.Deprecated
    assert d.validate() is None




def test_unknown_family_raises_rather_than_defaulting():
    """Rust's `expected_layer_for_family` is an exhaustive `match`, so an unknown
    family cannot exist. Python dispatches on value and needs a live guard. This
    branch has no Rust counterpart by construction -- pinned so a future port that
    silently returns a default layer instead of raising is caught here."""

    class NotAFamily:
        name = "NotAFamily"
        value = "NotAFamily"

    with pytest.raises(ValueError, match="Unknown family"):
        expected_layer_for_family(NotAFamily())



