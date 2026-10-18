"""Centralized domain constants, schemas, wire keys, and error tokens for prompt civilization.

AuthorityEffect: None.
"""

from __future__ import annotations

from enum import Enum
import re

AUTHORITY_EFFECT_NONE = "None"
MAX_TEXT_BYTES = 128 * 1024
MAX_ITEMS = 256

DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@-]*$")

# Canonical Schema Identifiers
SCHEMA_APPROVED_PROMPT = "omega.prompt.approved.v1"
SCHEMA_TYPED_PROMPT = "omega.prompt.typed.v1"
SCHEMA_REVIEW_BUNDLE = "omega.prompt.review-bundle.v1"
SCHEMA_REVIEW_RECEIPT = "omega.prompt.review-receipt.v1"
SCHEMA_PROMPT_FINDING = "omega.prompt.finding.v1"
SCHEMA_ANTISKILL_SPEC = "omega.antiskill.spec.v1"
SCHEMA_ANTISKILL_CANDIDATE = "omega.antiskill.candidate.v1"
SCHEMA_CONVERSATION_EPISODE = "omega.antiskill.conversation-episode.v1"
SCHEMA_OPERATOR_DECISION = "omega.prompt.operator-decision.v1"
SCHEMA_ANTISKILL_REGISTRY = "omega.antiskill.registry.v1"


from .outcome_type import OperatorDecisionOutcome, OutcomeType, ReviewOutcome


class CandidateDisciplineLevel(str, Enum):
    """Discipline levels for anti-skill rules."""

    FENCE_ONLY = "fence_only"
    STRUCTURAL_TRANSFORM = "structural_transform"
    REPLAYABLE_ANTIBODY = "replayable_antibody"


# Wire Keys
class ApprovedPromptWireKey(str, Enum):
    PROMPT_ID = "prompt_id"
    REVIEW_RECEIPT_ID = "review_receipt_id"
    APPROVED_BY = "approved_by"
    OBJECTIVE = "objective"
    CLAIM_MODE = "claim_mode"
    RENDERED_PROMPT = "rendered_prompt"
    RENDERED_DIGEST = "rendered_digest"
    CANDIDATE_BUDGET = "candidate_budget"
    OPERATION_BUDGET = "operation_budget"
    REQUESTED_EFFECTS = "requested_effects"
    AUTHORITY_EFFECT = "authority_effect"
    SCHEMA_VERSION = "schema_version"
    APPROVED_PROMPT_ID = "approved_prompt_id"


class TypedPromptWireKey(str, Enum):
    ORIGINAL_TEXT = "original_text"
    SOURCE_DIGEST = "source_digest"
    OBJECTIVE = "objective"
    CLAIM_MODE = "claim_mode"
    IN_SCOPE = "in_scope"
    OUT_OF_SCOPE = "out_of_scope"
    INPUTS = "inputs"
    CONSTRAINTS = "constraints"
    ACCEPTANCE_CRITERIA = "acceptance_criteria"
    EVIDENCE_REQUIREMENTS = "evidence_requirements"
    REQUESTED_EFFECTS = "requested_effects"
    CANDIDATE_BUDGET = "candidate_budget"
    OPERATION_BUDGET = "operation_budget"
    NONCLAIMS = "nonclaims"
    UNRESOLVED_QUESTIONS = "unresolved_questions"
    PROPOSED_PROMPT = "proposed_prompt"
    AUTHORITY_EFFECT = "authority_effect"
    SCHEMA_VERSION = "schema_version"
    PROMPT_ID = "prompt_id"


class PromptReviewReceiptWireKey(str, Enum):
    SOURCE_DIGEST = "source_digest"
    PROMPT_ID = "prompt_id"
    REGISTRY_ID = "registry_id"
    POLICY_DIGEST = "policy_digest"
    IMPLEMENTATION_DIGEST = "implementation_digest"
    FINDING_IDS = "finding_ids"
    OUTCOME = "outcome"
    PROTECTED_FIELDS_OK = "protected_fields_ok"
    AUTHORITY_EFFECT = "authority_effect"
    SCHEMA_VERSION = "schema_version"
    RECEIPT_ID = "receipt_id"


class PromptFindingWireKey(str, Enum):
    CODE = "code"
    SEVERITY = "severity"
    FIELD = "field"
    MESSAGE = "message"
    REPAIR_HINT = "repair_hint"
    DETECTOR_REF = "detector_ref"
    AUTHORITY_EFFECT = "authority_effect"
    SCHEMA_VERSION = "schema_version"
    FINDING_ID = "finding_id"


class AntiSkillSpecWireKey(str, Enum):
    SPEC_ID = "spec_id"
    VERSION = "version"
    FAILURE_CODE = "failure_code"
    DETECTOR_KIND = "detector_kind"
    ACTIVATION_FIELDS = "activation_fields"
    REPAIR_KIND = "repair_kind"
    PROTECTED_FIELDS = "protected_fields"
    EPISODE_IDS = "episode_ids"
    CONTEXT_KEYS = "context_keys"
    EVIDENCE_REFS = "evidence_refs"
    COUNTEREXAMPLES = "counterexamples"
    EVALUATION_RECEIPT_REF = "evaluation_receipt_ref"
    COMPOSITION_ORDER = "composition_order"
    COMMUTES_WITH = "commutes_with"
    AUTHORITY_EFFECT = "authority_effect"
    SCHEMA_VERSION = "schema_version"
    SPEC_DIGEST = "spec_digest"


class AntiSkillCandidateWireKey(str, Enum):
    NAME = "name"
    FAILURE_CODE = "failure_code"
    PROPOSED_INVARIANT = "proposed_invariant"
    EPISODE_IDS = "episode_ids"
    CONTEXT_KEYS = "context_keys"
    EVIDENCE_REFS = "evidence_refs"
    COUNTEREXAMPLES = "counterexamples"
    PROTECTED_FIELDS = "protected_fields"
    ACTIVATION_KIND = "activation_kind"
    STATUS = "status"
    AUTHORITY_EFFECT = "authority_effect"
    SCHEMA_VERSION = "schema_version"
    CANDIDATE_ID = "candidate_id"


class ConversationEpisodeWireKey(str, Enum):
    SOURCE_DIGEST = "source_digest"
    SOURCE_FORMAT = "source_format"
    ORDINAL = "ordinal"
    USER_LABEL = "user_label"
    USER_TEXT = "user_text"
    ASSISTANT_LABEL = "assistant_label"
    ASSISTANT_TEXT = "assistant_text"
    SESSION_ID = "session_id"
    TASK_ID = "task_id"
    MODEL_ID = "model_id"
    ANNOTATION = "annotation"
    AUTHORITY_EFFECT = "authority_effect"
    SCHEMA_VERSION = "schema_version"
    EPISODE_ID = "episode_id"


class OperatorDecisionWireKey(str, Enum):
    APPROVED = "approved"
    OPERATOR_ID = "operator_id"
    REVIEW_RECEIPT_ID = "review_receipt_id"


APPROVED_PROMPT_WIRE_FIELDS: frozenset[str] = frozenset(k.value for k in ApprovedPromptWireKey)
TYPED_PROMPT_WIRE_FIELDS: frozenset[str] = frozenset(k.value for k in TypedPromptWireKey)
PROMPT_REVIEW_RECEIPT_WIRE_FIELDS: frozenset[str] = frozenset(k.value for k in PromptReviewReceiptWireKey)
PROMPT_FINDING_WIRE_FIELDS: frozenset[str] = frozenset(k.value for k in PromptFindingWireKey)
ANTISKILL_SPEC_WIRE_FIELDS: frozenset[str] = frozenset(k.value for k in AntiSkillSpecWireKey)
ANTISKILL_CANDIDATE_WIRE_FIELDS: frozenset[str] = frozenset(k.value for k in AntiSkillCandidateWireKey)
CONVERSATION_EPISODE_WIRE_FIELDS: frozenset[str] = frozenset(k.value for k in ConversationEpisodeWireKey)
OPERATOR_DECISION_WIRE_FIELDS: frozenset[str] = frozenset(k.value for k in OperatorDecisionWireKey)
