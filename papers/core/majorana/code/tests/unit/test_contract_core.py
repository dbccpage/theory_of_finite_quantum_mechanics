import pytest
import os
import tempfile
import yaml  # type: ignore[import-untyped]
from omega_engine_governance.contracts import AuthorityEffect
from omega_engine_governance.contracts.kinds import Capability, CapabilityPolicy
from omega_engine_governance.contracts.schema import (
    ProofObligationRef,
    TerminalPolicy,
    RefusalPolicy,
    OperatorClassPolicy,
)
from omega_engine.crates.contract_core.registry.v1_types import from_dict
from omega_engine.crates.contract_core.registry.v1_validate import validate_v1, is_well_formed_po
from omega_engine.crates.contract_core.registry.v1_loader import load_v1_dir, intra_file_consistency


# kinds tests
def test_authority_effect_helpers_partition_layers():
    assert AuthorityEffect.StateTransition.is_execution()
    assert not AuthorityEffect.AuthorizesTransition.is_execution()

    assert AuthorityEffect.AuthorizesTransition.is_license()
    assert not AuthorityEffect.RequestsDecision.is_license()

    assert AuthorityEffect.RequiresEvaluator.is_decision()
    assert AuthorityEffect.RequestsDecision.is_decision()
    assert not AuthorityEffect.FactOnly.is_decision()

    assert AuthorityEffect.None_.is_evidence_layer()
    assert AuthorityEffect.EvidenceOnly.is_evidence_layer()
    assert AuthorityEffect.FactOnly.is_evidence_layer()
    assert not AuthorityEffect.StateTransition.is_evidence_layer()


def test_capability_policy_helpers_report_membership():
    policy = CapabilityPolicy(
        forbidden=[Capability.RawPayloadExposure, Capability.SelfCertification],
        required=[Capability.ActionLicensing],
    )
    assert policy.forbids(Capability.RawPayloadExposure)
    assert policy.forbids(Capability.SelfCertification)
    assert not policy.forbids(Capability.ComputePhi)
    assert policy.requires(Capability.ActionLicensing)
    assert not policy.requires(Capability.ExecuteStateTransition)


# v1 types tests
def test_policy_types_default_empty():
    assert len(TerminalPolicy().may_emit) == 0
    assert len(TerminalPolicy().may_support) == 0
    assert len(RefusalPolicy().may_emit) == 0
    oc = OperatorClassPolicy()
    assert len(oc.may_support) == 0
    assert not oc.must_not_self_assign


def test_proof_obligation_ref_is_transparent_string():
    p = ProofObligationRef("PO-D3")
    assert p.as_str() == "PO-D3"
    assert p == "PO-D3"


def test_rust_binding_renames_crate_field():
    # Test from_dict renames 'crate' to 'krate' in RustBinding
    y_str = """
schema_version: "omega.contract.v1"
contract_id: "urn:omega:math:demo:v0.1.0"
title: "Demo"
kind: "math_contract"
status: "mathematical_wip"
descriptor:
  authority_effect: "none"
  evidence_ceiling: "ShapeOnly"
rust_binding:
  crate: "omega_core"
  module: "trichotomy"
"""
    c = from_dict(yaml.safe_load(y_str))
    assert c.rust_binding.krate == "omega_core"
    assert c.rust_binding.module == "trichotomy"


GOOD_YAML = """
schema_version: "omega.contract.v1"
contract_id: "urn:omega:math:demo:v0.1.0"
title: "Demo"
kind: "math_contract"
status: "mathematical_wip"
descriptor:
  authority_effect: "none"
  evidence_ceiling: "ShapeOnly"
  runtime_enforcement: false
  customer_claim_allowed: false
  dependencies: { contracts: [], proof_obligations: ["PO-D3", "PO-AUTH-NC"] }
  terminals: { may_emit: [], may_support: ["ExactRepair"] }
  refusals: { may_emit: ["Invalid"] }
  operator_classes: { may_support: [], must_not_self_assign: true }
"""


def parse(y: str):
    return from_dict(yaml.safe_load(y))


def test_good_contract_validates():
    validate_v1(parse(GOOD_YAML))


def test_nonmath_missing_role_fails():
    y = """
schema_version: "omega.contract.v1"
contract_id: "urn:omega:obstruction:demo:v0.1.0"
title: "Demo"
kind: "obstruction_contract"
status: "mathematical_wip"
descriptor:
  authority_effect: "evidence_only"
  evidence_ceiling: "LocalReplay"
"""
    with pytest.raises(ValueError) as exc:
        validate_v1(parse(y))
    assert any("role required" in f for f in exc.value.args[0])


def test_nonmath_with_role_ok():
    y = """
schema_version: "omega.contract.v1"
contract_id: "urn:omega:obstruction:demo:v0.1.0"
title: "Demo"
kind: "obstruction_contract"
status: "mathematical_wip"
role: "AnalysisUnit"
descriptor:
  authority_effect: "evidence_only"
  evidence_ceiling: "LocalReplay"
  terminals: { may_emit: [], may_support: [] }
  refusals: { may_emit: [] }
"""
    validate_v1(parse(y))


def test_math_contract_with_authority_fails():
    bad = GOOD_YAML.replace(
        'authority_effect: "none"', 'authority_effect: "requests_decision"'
    )
    with pytest.raises(ValueError) as exc:
        validate_v1(parse(bad))
    assert any(
        "math contract must declare authority_effect: none" in f
        for f in exc.value.args[0]
    )


def test_unknown_terminal_fails():
    bad = GOOD_YAML.replace('may_support: ["ExactRepair"]', 'may_support: ["Bogus"]')
    with pytest.raises(ValueError) as exc:
        validate_v1(parse(bad))
    assert any("unknown terminal: Bogus" in f for f in exc.value.args[0])


def test_unknown_refusal_fails():
    bad = GOOD_YAML.replace('may_emit: ["Invalid"]', 'may_emit: ["Nope"]')
    with pytest.raises(ValueError) as exc:
        validate_v1(parse(bad))
    assert any("unknown refusal: Nope" in f for f in exc.value.args[0])


def test_malformed_proof_obligation_fails():
    bad = GOOD_YAML.replace('"PO-D3", "PO-AUTH-NC"', '"nonsense"')
    with pytest.raises(ValueError) as exc:
        validate_v1(parse(bad))
    assert any("malformed proof obligation" in f for f in exc.value.args[0])


def test_internal_hyphen_proof_obligation_ok():
    assert is_well_formed_po("PO-AUTH-NC")
    assert is_well_formed_po("PO-D3")
    assert not is_well_formed_po("nonsense")
    assert not is_well_formed_po("PO-")


def test_wrong_schema_version_fails():
    bad = GOOD_YAML.replace("omega.contract.v1", "omega.contract.v2")
    with pytest.raises(ValueError) as exc:
        validate_v1(parse(bad))
    assert any(
        "schema_version must be omega.contract.v1" in f for f in exc.value.args[0]
    )


# loader consistency tests
def doc_with_codomain(extra_class: str, extra_outcome: str):
    y = f"""
schema_version: "omega.contract.v1"
contract_id: "urn:omega:math:demo:v0.1.0"
title: "Demo"
kind: "math_contract"
status: "mathematical_wip"
descriptor:
  authority_effect: "none"
  evidence_ceiling: "ShapeOnly"
  terminals: {{ may_emit: [], may_support: ["ExactRepair"] }}
  refusals: {{ may_emit: ["Invalid"] }}
math:
  codomain:
    classes: ["ExactRepair"{extra_class}]
    meta_outcomes: ["Invalid"{extra_outcome}]
"""
    return parse(y)


def test_consistent_codomain_has_no_findings():
    assert len(intra_file_consistency(doc_with_codomain("", ""))) == 0


def test_undeclared_class_is_unknown_terminal():
    findings = intra_file_consistency(doc_with_codomain(', "Bogus"', ""))
    assert any("unknown terminal" in f and "Bogus" in f for f in findings)


def test_undeclared_meta_outcome_is_unknown_refusal():
    findings = intra_file_consistency(doc_with_codomain("", ', "Nope"'))
    assert any("unknown refusal" in f and "Nope" in f for f in findings)


def test_load_v1_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        # write one good contract
        good_path = os.path.join(tmpdir, "demo.contract.yaml")
        with open(good_path, "w", encoding="utf-8") as f:
            f.write(GOOD_YAML)

        # write a non-v1 yaml file (should be skipped silently)
        skip_path = os.path.join(tmpdir, "skip.contract.yaml")
        with open(skip_path, "w", encoding="utf-8") as f:
            f.write("schema_version: omega.contract.v2\ncontract_id: urn:omega:skip\n")

        # write a malformed yaml file (should be skipped silently)
        mal_path = os.path.join(tmpdir, "malformed.contract.yaml")
        with open(mal_path, "w", encoding="utf-8") as f:
            f.write("invalid: yaml: : foo\n")

        report = load_v1_dir(tmpdir)
        assert report.loaded == 1
        assert "urn:omega:math:demo:v0.1.0" in report.contract_ids
        assert len(report.findings) == 0


