"""Shared Kernel package for common domain primitives across crates."""

from .authority_effect import AuthorityEffect, validate_authority_effect_none
from .budget import (
    MAX_CANDIDATE_BUDGET,
    MAX_EXECUTION_BUDGET,
    MAX_OPERATION_BUDGET,
    Budget,
    CandidateBudget,
    ExecutionBudget,
    OperationBudget,
    StepBudget,
    TimeBudget,
)
from .byte_payload import (
    MAX_PAYLOAD_BYTES,
    MAX_STRING_LENGTH,
    BytePayload,
)
from .bytes import ByteCount
from .coboundary_score import CandidateProposal, CoboundaryScoreResult
from .code import Code, RefusalCode
from .content_digest import ContentDigest
from .data import DataRecord
from .demand_item import DemandItemV1
from .description import MAX_DESCRIPTION_LENGTH, Description
from .disposition import Disposition, DispositionState
from .field import FieldName
from .gate import GateId
from .hash import ContentHash, Hash, Sha256Hash
from .id import (
    DEFAULT_ID_REGEX,
    CandidateId,
    CarrierId,
    ClaimId,
    ContentArtifactId,
    CorpusId,
    DemandId,
    HypothesisId,
    Identifier,
    IntakeBundleId,
    ObstructionId,
    PacketId,
    PatchArtifactId,
    PolicyId,
    ProducerId,
    PromptArtifactId,
    ReceiptId,
    RunRootId,
    SampleId,
    TaskId,
    EventId,
)
from .key import ContextKey, Key, WireKey as WireKeyVO
from .key_type import CommonWireKeyKind, KeyType, KeyTypeKind
from .kill_condition import (
    KILL_CONDITION_MAP,
    REGISTERED_KILL_CONDITIONS,
    KillConditionInfo,
)
from .kind import Kind, Role, RoleKind
from .llm_payload import LLM_TURN_FAMILY, LLM_TURN_SCHEMA, LlmPayloadV1, LlmTurnPayloadV1
from .media_type import MediaType
from .objective_typed import ObjectiveTypedV1
from .obstruction import ObstructionFamily, ObstructionFamilyKind, ObstructionHintV1
from .patch import MAX_PATCH_BYTES, PatchText
from .path import OwnedPath, ProtectedPath, RelativePath, validate_path_security
from .path_manifest import PathManifest
from .regime import REGIME_KINDS, Regime, RegimeKind
from .required_reply_fields import DEFAULT_REQUIRED_FIELDS, RequiredReplyFields
from .residual_colour import RESIDUAL_COLOURS, ResidualColour
from .residual_drop import ResidualDrop, ResidualDropV1
from .revision import Revision
from .schema import SchemaVersion
from .severity import Severity, SeverityKind
from .summary import MAX_SUMMARY_LENGTH, Summary
from .task_objective import MAX_OBJECTIVE_LENGTH, TaskObjective
from .turn import TurnKind, TurnModality, TurnRole
from .turn_type import TurnType, TurnTypeKind
from .wire_key import WireKey

__all__ = [
    "AuthorityEffect",
    "Budget",
    "ByteCount",
    "BytePayload",
    "CandidateBudget",
    "CandidateId",
    "CandidateProposal",
    "CarrierId",
    "ClaimId",
    "CoboundaryScoreResult",
    "Code",
    "CommonWireKeyKind",
    "ContentArtifactId",
    "ContentDigest",
    "ContentHash",
    "ContextKey",
    "CorpusId",
    "DEFAULT_ID_REGEX",
    "DEFAULT_REQUIRED_FIELDS",
    "DataRecord",
    "DemandId",
    "DemandItemV1",
    "Description",
    "Disposition",
    "DispositionState",
    "EventId",
    "ExecutionBudget",
    "FieldName",
    "GateId",
    "Hash",
    "HypothesisId",
    "Identifier",
    "IntakeBundleId",
    "KILL_CONDITION_MAP",
    "Key",
    "KeyType",
    "KeyTypeKind",
    "KillConditionInfo",
    "Kind",
    "LLM_TURN_FAMILY",
    "LLM_TURN_SCHEMA",
    "LlmPayloadV1",
    "LlmTurnPayloadV1",
    "MAX_CANDIDATE_BUDGET",
    "MAX_DESCRIPTION_LENGTH",
    "MAX_EXECUTION_BUDGET",
    "MAX_OBJECTIVE_LENGTH",
    "MAX_OPERATION_BUDGET",
    "MAX_PATCH_BYTES",
    "MAX_PAYLOAD_BYTES",
    "MAX_STRING_LENGTH",
    "MAX_SUMMARY_LENGTH",
    "MediaType",
    "ObjectiveTypedV1",
    "ObstructionFamily",
    "ObstructionFamilyKind",
    "ObstructionHintV1",
    "ObstructionId",
    "OperationBudget",
    "OwnedPath",
    "PacketId",
    "PatchArtifactId",
    "PatchText",
    "PathManifest",
    "PolicyId",
    "ProducerId",
    "PromptArtifactId",
    "ProtectedPath",
    "REGISTERED_KILL_CONDITIONS",
    "REGIME_KINDS",
    "RESIDUAL_COLOURS",
    "ReceiptId",
    "RefusalCode",
    "Regime",
    "RegimeKind",
    "RelativePath",
    "RequiredReplyFields",
    "ResidualColour",
    "ResidualDrop",
    "ResidualDropV1",
    "Revision",
    "Role",
    "RoleKind",
    "RunRootId",
    "SampleId",
    "SchemaVersion",
    "Severity",
    "SeverityKind",
    "Sha256Hash",
    "StepBudget",
    "Summary",
    "TaskId",
    "TaskObjective",
    "TimeBudget",
    "TurnKind",
    "TurnModality",
    "TurnRole",
    "TurnType",
    "TurnTypeKind",
    "WireKey",
    "WireKeyVO",
    "validate_authority_effect_none",
    "validate_path_security",
]
