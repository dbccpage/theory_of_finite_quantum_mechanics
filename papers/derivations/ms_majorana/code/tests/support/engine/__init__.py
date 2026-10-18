"""Engine Subsystem Package conforming to urn:omega:engine:v1.0.0.

Provides base state-transition commit boundaries, engine invariants, and domain engines.
"""

from .eng_base import (
    CONTRACT_ID as ENGINE_CONTRACT_ID,
    CheckedEngineOutput,
    Engine,
    EngineAction,
    EngineInput,
    EngineOutput,
    LicensedEngine,
    LicensedTransitionInput,
    RefusedEngineOutput,
    verify_engine_contract,
)
from .eng_invariants import (
    EngineDecision,
    EngineError,
    EngineRuntimeState,
    EngineTraceStep,
    EscalationRoute,
    EvaluationAudit,
    EvaluationVerdict,
    RunSummary,
    RuntimeFailure,
    TerminationCondition,
    TerminationViolation,
    Tolerances,
    assert_candidate_accounting,
    assert_meta_escalation_resolution,
    assert_search_endpoint_invariance,
    assert_stagnation_resolves,
    assert_trace_integrity,
)

from .eng_prompt_intake import (
    CotRecord,
    PromptGeometry,
    PromptIntakeEngine,
    PromptRecord,
    fallback_id_for,
    normalize_text,
    parse_csv_fields,
    perceive,
)

from .eng_operator_algebra import (
    AlgebraicState,
    CStarAlgebra,
    DimensionMismatch,
    DoubleCommutantDiagnostic,
    EmptyGenerators,
    FiniteVonNeumannAlgebra,
    GnsConstruction,
    InvalidObservable,
    MatrixCStarAlgebra,
    ModularFlow,
    NonDiagonalState,
    NonFaithfulState,
    NonPositiveState,
    NonSquareMatrix,
    NonUnitalState,
    OperatorAlgebraError,
    ZeroDimension,
)

from .eng_obstruction import (
    BestScoreSelector,
    Candidate,
    CandidateGenerator,
    CandidateSelector,
    DefaultObstructionEvaluator,
    EvaluatedCandidate,
    ObstructionEvaluator,
    ObstructionFunctional,
    ObstructionMetrics,
    ObstructionThresholds,
    ObstructionVerdict,
    OperatorId,
    Provenance,
    ScoreWeights,
    obstruction_score,
)

from .eng_stream import StreamingEngine
from .eng_omega_algo_prime_0 import AlgoPrimeDdaEngine, PhaseReceipt

__all__ = [
    "Engine",
    "LicensedEngine",
    "EngineInput",
    "EngineOutput",
    "CheckedEngineOutput",
    "RefusedEngineOutput",
    "LicensedTransitionInput",
    "EngineAction",
    "verify_engine_contract",
    "ENGINE_CONTRACT_ID",
    "AlgoPrimeDdaEngine",
    "PhaseReceipt",
    "StreamingEngine",
    "CStarAlgebra",
    "PromptIntakeEngine",
]
