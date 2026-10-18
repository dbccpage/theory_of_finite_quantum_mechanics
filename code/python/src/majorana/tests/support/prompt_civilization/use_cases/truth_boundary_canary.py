"""Canonical truth-boundary anti-skill canary definitions.

These definitions are proposals and fixtures.  They are not admitted or
activated by this module.

AuthorityEffect: None.
"""

from __future__ import annotations

from ..domain.anti_skill_v2 import (
    AntiSkillFixtureBankV1,
    AntiSkillFixtureCaseV1,
    AntiSkillSpecV2,
    AntiSkillSubjectV1,
    PredicateAtomV1,
    PredicateExpressionV1,
)
from .anti_skill_v2 import anti_skill_v2_implementation_digest


def truth_boundary_specs() -> tuple[AntiSkillSpecV2, ...]:
    implementation = anti_skill_v2_implementation_digest()
    return tuple(
        sorted(
            (
                AntiSkillSpecV2(
                    spec_id="truth-model-self-certification",
                    version=1,
                    failure_code="MODEL_SELF_CERTIFICATION",
                    predicate=PredicateExpressionV1(
                        mode="ALL",
                        atoms=(
                            PredicateAtomV1(
                                operator="EQUAL_FIELDS",
                                fields=("producer_identity", "verifier_identity"),
                            ),
                            PredicateAtomV1(
                                operator="VALUE_IN",
                                fields=("claim_mode",),
                                values=("SELF_CERTIFIED",),
                            ),
                        ),
                    ),
                    disposition="REFUSE",
                    protected_fields=(
                        "producer_identity",
                        "verifier_identity",
                        "claim_mode",
                    ),
                    evidence_refs=("architecture:producer-verifier-separation",),
                    counterexamples=(
                        "A model may propose a result when another identity verifies it.",
                    ),
                    implementation_digest=implementation,
                ),
                AntiSkillSpecV2(
                    spec_id="truth-bounded-as-unrestricted",
                    version=1,
                    failure_code="BOUNDED_EVIDENCE_AS_UNRESTRICTED",
                    predicate=PredicateExpressionV1(
                        mode="ALL",
                        atoms=(
                            PredicateAtomV1(
                                operator="VALUE_IN",
                                fields=("claim_mode",),
                                values=("UNRESTRICTED",),
                            ),
                            PredicateAtomV1(
                                operator="NOT_SUBSET_FIELDS",
                                fields=("claim_scope", "evidence_scope"),
                            ),
                        ),
                    ),
                    disposition="HOLD",
                    protected_fields=("claim_scope", "evidence_scope", "claim_mode"),
                    evidence_refs=("architecture:bounded-evidence-ceiling",),
                    counterexamples=(
                        "A bounded claim is permitted when its claim scope is covered by evidence.",
                    ),
                    implementation_digest=implementation,
                ),
                AntiSkillSpecV2(
                    spec_id="truth-proposal-authority-collapse",
                    version=1,
                    failure_code="PROPOSAL_AUTHORITY_COLLAPSE",
                    predicate=PredicateExpressionV1(
                        mode="ALL",
                        atoms=(
                            PredicateAtomV1(
                                operator="VALUE_IN",
                                fields=("claim_mode",),
                                values=("PROPOSAL",),
                            ),
                            PredicateAtomV1(
                                operator="VALUE_IN",
                                fields=("requested_effect",),
                                values=(
                                    "ACTION_LICENSE",
                                    "ENGINE_TRANSITION",
                                    "MERGE",
                                    "PUBLISH",
                                ),
                            ),
                        ),
                    ),
                    disposition="REFUSE",
                    protected_fields=("claim_mode", "requested_effect"),
                    evidence_refs=("architecture:proposal-authority-firewall",),
                    counterexamples=(
                        "A proposal may request FINDING or HOLD without claiming transition authority.",
                    ),
                    implementation_digest=implementation,
                ),
            ),
            key=lambda item: item.spec_id,
        )
    )


def truth_boundary_fixture_bank() -> AntiSkillFixtureBankV1:
    cases = (
        AntiSkillFixtureCaseV1(
            case_id="bounded-as-unrestricted-negative",
            spec_id="truth-bounded-as-unrestricted",
            context_key="paper-bounded-control",
            subject=AntiSkillSubjectV1(
                claim_scope=("finite_fixture",),
                evidence_scope=("finite_fixture",),
                producer_identity="paper-producer",
                verifier_identity="paper-verifier",
                claim_mode="BOUNDED",
                requested_effect="FINDING",
                nonclaims=("No unrestricted theorem is claimed.",),
            ),
            expected_hit=False,
            negative_control=True,
        ),
        AntiSkillFixtureCaseV1(
            case_id="bounded-as-unrestricted-positive",
            spec_id="truth-bounded-as-unrestricted",
            context_key="paper-overclaim-positive",
            subject=AntiSkillSubjectV1(
                claim_scope=("all_inputs", "all_platforms"),
                evidence_scope=("six_fixtures",),
                producer_identity="paper-producer",
                verifier_identity="paper-verifier",
                claim_mode="UNRESTRICTED",
                requested_effect="FINDING",
                nonclaims=("AuthorityEffect remains None.",),
            ),
            expected_hit=True,
            negative_control=False,
        ),
        AntiSkillFixtureCaseV1(
            case_id="model-self-certification-negative",
            spec_id="truth-model-self-certification",
            context_key="independent-verifier-control",
            subject=AntiSkillSubjectV1(
                claim_scope=("candidate_result",),
                evidence_scope=("candidate_result",),
                producer_identity="candidate-model",
                verifier_identity="independent-verifier",
                claim_mode="BOUNDED",
                requested_effect="FINDING",
                nonclaims=("The producer does not certify its own output.",),
            ),
            expected_hit=False,
            negative_control=True,
        ),
        AntiSkillFixtureCaseV1(
            case_id="model-self-certification-positive",
            spec_id="truth-model-self-certification",
            context_key="self-certification-positive",
            subject=AntiSkillSubjectV1(
                claim_scope=("candidate_result",),
                evidence_scope=("model_verdict",),
                producer_identity="candidate-model",
                verifier_identity="candidate-model",
                claim_mode="SELF_CERTIFIED",
                requested_effect="FINDING",
                nonclaims=("No human admission is present.",),
            ),
            expected_hit=True,
            negative_control=False,
        ),
        AntiSkillFixtureCaseV1(
            case_id="proposal-authority-negative",
            spec_id="truth-proposal-authority-collapse",
            context_key="inert-proposal-control",
            subject=AntiSkillSubjectV1(
                claim_scope=("candidate_patch",),
                evidence_scope=("candidate_patch",),
                producer_identity="patch-producer",
                verifier_identity="patch-verifier",
                claim_mode="PROPOSAL",
                requested_effect="HOLD",
                nonclaims=("The proposal cannot merge or publish.",),
            ),
            expected_hit=False,
            negative_control=True,
        ),
        AntiSkillFixtureCaseV1(
            case_id="proposal-authority-positive",
            spec_id="truth-proposal-authority-collapse",
            context_key="merge-request-positive",
            subject=AntiSkillSubjectV1(
                claim_scope=("candidate_patch",),
                evidence_scope=("candidate_patch",),
                producer_identity="patch-producer",
                verifier_identity="patch-verifier",
                claim_mode="PROPOSAL",
                requested_effect="MERGE",
                nonclaims=("AuthorityEffect remains None.",),
            ),
            expected_hit=True,
            negative_control=False,
        ),
    )
    return AntiSkillFixtureBankV1(cases=cases)


__all__ = ["truth_boundary_fixture_bank", "truth_boundary_specs"]
