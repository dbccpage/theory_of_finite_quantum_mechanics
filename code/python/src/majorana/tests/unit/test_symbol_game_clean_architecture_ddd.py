"""Comprehensive Unit Test Suite for Symbol Game Clean Architecture & DDD implementation."""

from __future__ import annotations

import tempfile
from fractions import Fraction
from pathlib import Path
import pytest

from omega_engine_pfp.domain import (
    AuthorityEffect,
    BudgetExhaustedError,
    BytePayload,
    CandidateBudget,
    CandidateId,
    CanonicalizationError,
    CandidateProposal,
    CarrierId,
    CoboundaryScoreResult,
    Code,
    ContentDigest,
    DEFAULT_REQUIRED_FIELDS,
    DemandId,
    DemandItemV1,
    Description,
    Disposition,
    DispositionState,
    DualWitnessRequiredError,
    EliminationReceiptV1,
    FieldName,
    ForbiddenAuthorityError,
    FrozenCorpus,
    GateReceiptV1,
    Identifier,
    IllegalPathAccessError,
    InvariantViolationError,
    KILL_CONDITION_MAP,
    KillConditionInfo,
    Kind,
    LlmTurnContentArtifactV1,
    LlmTurnPayloadV1,
    LlmTurnRunRootV1,
    MAX_CANDIDATE_BUDGET,
    MAX_DESCRIPTION_LENGTH,
    MAX_OBJECTIVE_LENGTH,
    MAX_OPERATION_BUDGET,
    MAX_PAYLOAD_BYTES,
    MAX_STRING_LENGTH,
    MAX_SUMMARY_LENGTH,
    ObjectiveTypedV1,
    ObstructionFamily,
    ObstructionFamilyKind,
    ObstructionHintV1,
    ObstructionId,
    ObstructionLedgerEvent,
    OperationBudget,
    OwnedPath,
    PacketEnvelopeV2,
    PathManifest,
    PayloadSizeLimitExceededError,
    PolicyScore,
    ProcessEvent,
    ProducerId,
    PromptArtifactId,
    PromptArtifactV1,
    ProtectedPath,
    ReceiptId,
    RefusalCode,
    REGISTERED_KILL_CONDITIONS,
    Regime,
    RegimeKind,
    RequiredReplyFields,
    ResidualColour,
    ResidualDropV1,
    Role,
    RoleKind,
    RoutingHypothesis,
    RunRootId,
    SchemaVersion,
    SecurityPathViolationError,
    SourceArtifactV1,
    SourceIntakeBundleV1,
    StepBudget,
    Summary,
    TaskId,
    TaskObjective,
    TurnKind,
    TurnModality,
    TurnRole,
    TurnType,
    TurnTypeKind,
    WireKey,
)
from omega_engine_pfp.use_cases import (
    CompilePromptUseCase,
    CreateCodeChangeProposalUseCase,
    CreateTurnUseCase,
    EliminateObstructionUseCase,
    EvaluateCandidateUseCase,
    EvaluateCecMetricUseCase,
    EvaluateCoboundaryScoreUseCase,
    EvaluatePatchGatesUseCase,
    EvaluatePolicyUseCase,
    FreezeCorpusUseCase,
    IntakeResearchSourcesUseCase,
    ParseMachineBlockUseCase,
    SubmitCandidateUseCase,
    SubmitPatchCandidateUseCase,
    ValidateReplyResidualUseCase,
    VerifyResearchClaimUseCase,
)
from omega_engine_pfp.infrastructure import (
    CecBridgeAdapter,
    FilePromptRepository,
    InMemoryDbContext,
    MemoryPromptRepository,
    MemoryTurnRepository,
    ObstructionLedgerAdapter,
    OesosEvidenceAdapter,
    SymbolGameDbContext,
    deserialize_envelope_v2,
    deserialize_prompt_artifact,
    serialize_envelope_v2,
    serialize_prompt_artifact,
)
from omega_engine_pfp.controllers import (
    CodeChangeController,
    PromptController,
    TurnController,
)


def test_byte_payload_value_object_guards_and_digests() -> None:
    """BytePayload enforces size invariants, prevents 10GB memory bombs, and computes ContentDigest."""
    # Valid payload
    payload = BytePayload.from_str("hello omega engine")
    assert payload.as_str() == "hello omega engine"
    assert len(payload) == 18
    assert payload.digest.hex_digest is not None
    assert len(payload.digest.hex_digest) == 64

    # Enforce maximum single payload ceiling (16MB)
    with pytest.raises(PayloadSizeLimitExceededError):
        # Oversized bytes
        BytePayload(b"x" * (MAX_PAYLOAD_BYTES + 1))


def test_wire_key_enum_exhaustion() -> None:
    """WireKey enum replaces magic strings across wire boundaries."""
    assert WireKey.SCHEMA_VERSION.value == "schema_version"
    assert WireKey.PROMPT_ARTIFACT_ID.value == "prompt_artifact_id"
    assert WireKey.AUTHORITY_EFFECT.value == "authority_effect"
    assert WireKey.OPEN_OBSTRUCTIONS.value == "open_obstructions"


def test_prompt_artifact_aggregate_invariants_and_authority_firewall() -> None:
    """PromptArtifactV1 refuses non-None authority and Exact without a dual witness.

    The refusals are asserted by their **code**, not by exception type. The
    aggregate validates in `__post_init__` and raises `CanonicalizationError`
    carrying a refusal code; the previously expected `ForbiddenAuthorityError`
    and `DualWitnessRequiredError` live in `domain/invariants.py`, which no
    production module imports. Asserting the code is also the stronger check --
    a type alone cannot distinguish these two refusals from any other.
    """
    dummy_digest = "a" * 64
    obj = ObjectiveTypedV1(kind="test", summary="test objective")

    def _artifact(**overrides: object) -> PromptArtifactV1:
        fields = dict(
            regime_id=dummy_digest,
            regime_kind=RegimeKind.SYMBOL_ONLY.value,
            admitted_constructors=("c1", "c2"),
            open_obstructions=(),
            demand_set=(),
            kill_conditions=("F-01_inherited_meaning",),
            required_reply_fields=("status",),
            objective_typed=obj,
            residual_colour=ResidualColour.OPEN.value,
            dual_witness_required=False,
            dual_witness_ref=None,
            prompt_body_sha256=dummy_digest,
            prompt_body_byte_count=128,
            explicit_artifact_id="art_001",
        )
        fields.update(overrides)
        return PromptArtifactV1(**fields)

    # The permitted case. Without it, a constructor that refused everything
    # would satisfy both refusal assertions below.
    art = _artifact()
    assert art.authority_effect == "None"
    assert art.residual_colour == ResidualColour.OPEN.value

    with pytest.raises(CanonicalizationError, match="AUTHORITY_EFFECT_NON_NONE"):
        _artifact(authority_effect="Authoritative")

    with pytest.raises(CanonicalizationError, match="EXACT_WITHOUT_DUAL_WITNESS"):
        _artifact(
            residual_colour=ResidualColour.EXACT.value,
            dual_witness_required=True,
            dual_witness_ref=None,
        )

def test_use_case_compile_prompt_and_validate_residual() -> None:
    """CompilePromptUseCase and ValidateReplyResidualUseCase operate contractively."""
    compile_uc = CompilePromptUseCase()
    validate_uc = ValidateReplyResidualUseCase()

    # `create` takes no free-text `description`: an obstruction is identified by
    # id and family, and a demand by id and kind, with prose confined to `note`.
    obs = ObstructionHintV1.create(
        obstruction_id="obs_1",
        family=ObstructionFamilyKind.CONTINUUM_FROM_FINITE.value,
    )
    dem = DemandItemV1.create(
        demand_id="dem_1",
        kind="repair",
        note="add comma",
    )

    art = compile_uc.execute(
        prompt_artifact_id="art_test_100",
        regime_kind=RegimeKind.SYMBOL_ONLY.value,
        prompt_body="Task instructions for symbol game",
        open_obstructions=(obs,),
        demand_set=(dem,),
        required_reply_fields=("status", "step_claims"),
    )

    assert str(art.explicit_artifact_id) == "art_test_100"
    assert len(art.open_obstructions) == 1
    assert len(art.demand_set) == 1

    # The validator takes the reply *text* and returns a bool: it checks that
    # every required field name appears in the reply. It does not parse, and it
    # returns no message -- an earlier signature returning `(bool, str)` over a
    # dict is what this test was written against.
    valid_reply = (
        '{"status": "PASS", "step_claims": ["claim_1"], '
        '"residual_colour": "Open", "authority_effect": "None"}'
    )
    assert validate_uc.execute(artifact=art, reply_content=valid_reply) is True

    # A reply missing a declared required field is refused. `step_claims` is in
    # `required_reply_fields`; without this negative case a validator that
    # always returned True would pass the assertion above.
    invalid_reply = '{"status": "PASS"}'
    assert validate_uc.execute(artifact=art, reply_content=invalid_reply) is False


def test_turn_controller_full_lifecycle_and_budget_enforcement() -> None:
    """TurnController manages LLM turn runs and enforces candidate budgets."""
    repo = MemoryTurnRepository()
    controller = TurnController(repository=repo)

    run_root = controller.create_turn(
        task_id="task_turn_001",
        objective="Resolve obstruction obs_1",
        candidate_budget=2,
    )

    # `LlmTurnRunRootV1.task_id` is declared `-> str`. Wrapping it in a
    # `TaskId` compares a string against a value object and never matches.
    assert run_root.task_id == "task_turn_001"
    assert len(run_root.candidate_ids) == 0
    loaded_root = repo.get_run_root(str(run_root.run_root_id))
    assert loaded_root is not None
    assert loaded_root.to_dict() == run_root.to_dict()

    # Submit candidate 1
    reply_1 = '```json\n{"status": "PASS", "step_claims": ["c1"], "obstruction_receipts": [], "residual_colour": "Open", "AUTHORITY_EFFECT": "None"}\n```'
    run_root, cand_1, cont_1 = controller.submit_candidate(
        run_root=run_root,
        candidate_id="cand_001",
        producer_id="agent_alpha",
        reply_text=reply_1,
    )
    assert len(run_root.candidate_ids) == 1

    # Evaluate candidate 1
    eval_res = controller.evaluate_candidate(
        run_root=run_root,
        candidate=cand_1,
        content=cont_1,
    )
    assert eval_res["disposition"] == "ACCEPTED"

    # Submit candidate 2
    reply_2 = '```json\n{"status": "PASS", "step_claims": ["c2"], "obstruction_receipts": [], "residual_colour": "Open", "AUTHORITY_EFFECT": "None"}\n```'
    run_root, cand_2, cont_2 = controller.submit_candidate(
        run_root=run_root,
        candidate_id="cand_002",
        producer_id="agent_alpha",
        reply_text=reply_2,
    )
    assert len(run_root.candidate_ids) == 2

    # Submit candidate 3 (exceeds budget 2 -> BudgetExhaustedError)
    with pytest.raises(BudgetExhaustedError):
        controller.submit_candidate(
            run_root=run_root,
            candidate_id="cand_003",
            producer_id="agent_alpha",
            reply_text="overflow candidate",
        )


def test_code_change_controller_and_gate_evaluation() -> None:
    """CodeChangeController enforces path ownership and protected file immutability."""
    controller = CodeChangeController()

    session = controller.create_proposal(
        task_id="code_task_001",
        objective="Fix typo in core module",
        base_revision="main@HEAD",
        owned_paths=("omega_engine/crates/symbol_game/domain",),
        protected_paths=(".canon", "omega_engine/anomalon_councils"),
    )

    # Valid patch within owned paths
    valid_patch = """--- a/omega_engine/crates/symbol_game/domain/sample.py
+++ b/omega_engine/crates/symbol_game/domain/sample.py
@@ -1,1 +1,1 @@
-# old
+# new
"""
    session, bound = controller.submit_patch(
        session=session,
        producer_id="coder_agent",
        patch_text=valid_patch,
    )

    receipts = controller.evaluate_patch_gates(session=session, bound=bound)
    assert all(str(r.disposition) == "PASS" for r in receipts)

    # Patch modifying protected paths
    protected_patch = """--- a/omega_engine/anomalon_councils/rules.yaml
+++ b/omega_engine/anomalon_councils/rules.yaml
@@ -1,1 +1,1 @@
-# old
+# malicious
"""
    session_2, bound_2 = controller.submit_patch(
        session=session,
        producer_id="coder_agent",
        patch_text=protected_patch,
    )
    receipts_2 = controller.evaluate_patch_gates(session=session_2, bound=bound_2)
    failed_gates = [r for r in receipts_2 if str(r.disposition) == "FAIL"]
    assert len(failed_gates) > 0


def test_persistence_symbol_game_db_context() -> None:
    """SymbolGameDbContext executes atomic disk operations and FilePromptRepository round-trips."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SymbolGameDbContext(tmpdir)
        repo = FilePromptRepository(db)

        dummy_digest = "b" * 64
        # `PromptArtifactV1` constructs from `explicit_artifact_id`, `regime_id`
        # and `objective_typed`; `prompt_artifact_id` survives only as a derived
        # read property. The old kwargs named an earlier generation of the
        # aggregate and never reached it.
        art = PromptArtifactV1(
            schema_version="omega.symbol-game.prompt-artifact.v1",
            regime_kind=RegimeKind.SYMBOL_ONLY.value,
            regime_id=dummy_digest,
            prompt_body_sha256=dummy_digest,
            prompt_body_byte_count=len(b"prompt body"),
            admitted_constructors=(),
            open_obstructions=(),
            demand_set=(),
            # Both must be non-empty and canonically sorted; the aggregate
            # refuses `REFUSAL_ARRAY_NOT_SORTED` on an empty tuple. These are the
            # values `TurnController.create_turn` itself defaults to.
            kill_conditions=("F-01_inherited_meaning",),
            required_reply_fields=("obstruction_receipts", "status", "step_claims"),
            objective_typed=ObjectiveTypedV1(kind="disk_test", summary="summary"),
            residual_colour=ResidualColour.OPEN.value,
            dual_witness_required=False,
            dual_witness_ref=None,
        )

        # `prompt_artifact_id` is content-addressed: the aggregate computes it
        # from its own fields and the round-trip refuses a wire id that does not
        # match. Supplying one was the old contract; deriving it is the current
        # one, and it makes the round-trip assert something real.
        artifact_id = str(art.prompt_artifact_id)
        assert len(artifact_id) == 64

        repo.save_prompt_artifact(art)
        loaded = repo.get_prompt_artifact(artifact_id)
        assert loaded is not None
        assert str(loaded.prompt_artifact_id) == artifact_id
        assert str(loaded.regime_id) == dummy_digest


def test_discrete_coboundary_scoring_use_case() -> None:
    """EvaluateCoboundaryScoreUseCase scores a proposal by its residual drop.

    This test named an API generation that no longer exists: it constructed
    `CandidateProposal` with `target_obstruction_ids`, `eliminated_demand_ids`,
    `patch_bytes_digest` and `dual_witness_digest` -- the real field is
    `repaired_obstruction_ids`, and the other three have no counterpart -- and
    then read `phi1`, `gamma2`, `xi`, `is_exact` and `residual_colour` off a
    `CoboundaryScoreResult` that carries none of them. It raised `TypeError` at
    the first constructor, so the five bogus reads were never reached either.

    Rewritten against the surface the use case actually computes: a rational
    residual norm before and after, the drop between them, and exactness gated
    on a dual witness.
    """
    uc = EvaluateCoboundaryScoreUseCase()

    # Repairs 2 of 5 open obstructions and claims no dual witness.
    proposal_open = CandidateProposal(
        proposal_id="prop_001",
        repaired_obstruction_ids=("obs_1", "obs_2"),
        structural_cost=1.0,
        dual_witness_ref=None,
    )
    res_open = uc.execute(proposal_open, total_open_obstructions=5)
    assert res_open.proposal_id == "prop_001"
    assert res_open.prior_residual_norm == Fraction(5)
    assert res_open.post_residual_norm == Fraction(3)  # 5 - 2
    assert res_open.residual_drop == Fraction(2)
    assert res_open.is_exact_candidate is False
    assert res_open.dual_witness_ref is None
    assert res_open.normalized_efficiency == pytest.approx(2.0 / (1.0 + 1.0))

    # Repairs all 3 and carries a dual witness -> exact.
    proposal_exact = CandidateProposal(
        proposal_id="prop_002",
        repaired_obstruction_ids=("obs_1", "obs_2", "obs_3"),
        structural_cost=0.0,
        dual_witness_ref="d" * 64,  # a dual witness ref is a content digest
    )
    res_exact = uc.execute(proposal_exact, total_open_obstructions=3)
    assert res_exact.post_residual_norm == Fraction(0)
    assert res_exact.residual_drop == Fraction(3)
    assert res_exact.is_exact_candidate is True

    # The governance half of the same branch: a zero residual is not exact on
    # its own. Without this, dropping the `dual_witness_ref` conjunct from
    # `is_exact` would leave both assertions above still passing.
    proposal_unwitnessed = CandidateProposal(
        proposal_id="prop_003",
        repaired_obstruction_ids=("obs_1", "obs_2", "obs_3"),
        structural_cost=0.0,
        dual_witness_ref=None,
    )
    res_unwitnessed = uc.execute(proposal_unwitnessed, total_open_obstructions=3)
    assert res_unwitnessed.post_residual_norm == Fraction(0)
    assert res_unwitnessed.is_exact_candidate is False

    # An overclaim -- three claimed repairs against one open obstruction.
    # `post_residual_norm` was always clamped at zero here, but the drop and
    # the efficiency were computed from the raw claim, so this fixture scored
    # drop 3 and efficiency 3.0 while the honest single-repair proposal below
    # scored 1 and 1.0: claiming more than exists outranked being right.
    res_overclaim = uc.execute(proposal_exact, total_open_obstructions=1)
    assert res_overclaim.post_residual_norm == Fraction(0)
    # The invariant the phrase "the drop between them" actually names.
    assert res_overclaim.residual_drop == (
        res_overclaim.prior_residual_norm - res_overclaim.post_residual_norm
    )

    # The ranking consequence, stated directly: an overclaim may not beat an
    # honest proposal that repairs everything actually open.
    proposal_honest = CandidateProposal(
        proposal_id="prop_004",
        repaired_obstruction_ids=("obs_1",),
        structural_cost=0.0,
        dual_witness_ref="d" * 64,
    )
    res_honest = uc.execute(proposal_honest, total_open_obstructions=1)
    assert res_honest.residual_drop == res_overclaim.residual_drop
    assert res_honest.normalized_efficiency == res_overclaim.normalized_efficiency

    # Clamping the count is not enough on its own: repeating one id was another
    # way to manufacture a full drop. Three copies of `obs_1` against three
    # open obstructions reported drop 3, residual 0 and is_exact_candidate True
    # after repairing exactly one obstruction. The ids are a claim about which
    # obstructions close, so they are a set, and the malformed claim is refused
    # at the entity rather than merely absorbed by scoring.
    with pytest.raises(CanonicalizationError):
        CandidateProposal(
            proposal_id="prop_005",
            repaired_obstruction_ids=("obs_1", "obs_1", "obs_1"),
            structural_cost=0.0,
            dual_witness_ref="d" * 64,
        )

    # Defence in depth: scoring counts distinct ids even if a duplicate tuple
    # reaches it past the entity guard, because scoring is what turns a count
    # into an exactness verdict.
    smuggled = CandidateProposal(
        proposal_id="prop_006",
        repaired_obstruction_ids=("obs_1",),
        structural_cost=0.0,
        dual_witness_ref="d" * 64,
    )
    object.__setattr__(
        smuggled, "repaired_obstruction_ids", ("obs_1", "obs_1", "obs_1")
    )
    res_smuggled = uc.execute(smuggled, total_open_obstructions=3)
    assert res_smuggled.residual_drop == Fraction(1)
    assert res_smuggled.post_residual_norm == Fraction(2)
    assert res_smuggled.is_exact_candidate is False


def test_decomposed_value_objects_invariants_and_behaviors() -> None:
    """Comprehensive test validating each decomposed Value Object in domain/value_objects."""
    # 1. TaskId
    tid = TaskId("task_abc-123.test")
    assert str(tid) == "task_abc-123.test"
    with pytest.raises(InvariantViolationError):
        TaskId("")
    with pytest.raises(InvariantViolationError):
        TaskId("invalid task id with spaces")

    # 2. Budgets
    cb = CandidateBudget(8)
    assert int(cb) == 8
    cb.check_capacity(5)
    with pytest.raises(BudgetExhaustedError):
        cb.check_capacity(8)
    with pytest.raises(InvariantViolationError):
        CandidateBudget(0)
    # Two different quantities share the name `MAX_CANDIDATE_BUDGET`.
    # `CandidateBudget.MAX_VALUE` (1024, in the shared kernel's `budget.py`)
    # caps how large a budget may be *declared*; the run-root aggregates'
    # `MAX_CANDIDATE_BUDGET` (32) caps how many candidate ids a run root may
    # *hold*. This constructs a `CandidateBudget`, so the value object's own
    # ceiling governs it -- asserting against the aggregate bound claimed a
    # coupling the domain does not have, and the check silently never fired.
    with pytest.raises(InvariantViolationError):
        CandidateBudget(CandidateBudget.MAX_VALUE + 1)
    # Recorded rather than assumed: the two bounds are not equal, so a budget
    # may be declared far larger than any run root could record against it.
    assert MAX_CANDIDATE_BUDGET < CandidateBudget.MAX_VALUE

    ob = OperationBudget(32)
    assert int(ob) == 32
    with pytest.raises(InvariantViolationError):
        OperationBudget(0)

    sb = StepBudget(2)
    assert int(sb) == 2

    # 3. Roles and TurnKinds
    role = TurnRole.assistant()
    assert str(role) == "assistant"
    kind = TurnKind.symbol_game()
    assert str(kind) == "symbol_game_turn"

    # 4. TaskObjective
    obj = TaskObjective("Solve discrete obstruction on lattice")
    assert str(obj) == "Solve discrete obstruction on lattice"
    with pytest.raises(InvariantViolationError):
        TaskObjective("   ")

    # 5. RequiredReplyFields
    rrf = RequiredReplyFields.from_sequence(
        ["step_claims", "status", "step_claims", "obstruction_receipts"]
    )
    assert rrf.as_tuple() == ("obstruction_receipts", "status", "step_claims")
    ok, err = rrf.validate_reply(
        ["status", "step_claims", "obstruction_receipts", "extra"]
    )
    assert ok is True
    ok, err = rrf.validate_reply(["status"])
    assert ok is False

    # 6. Disposition
    disp_open = Disposition.open_state()
    assert str(disp_open) == "OPEN"
    assert disp_open.is_terminal() is False
    disp_acc = Disposition.accepted()
    assert disp_acc.is_terminal() is True

    # 7. Identifiers (DRY Shared Kernel subclasses)
    obs_id = ObstructionId("obs_001")
    pid = PromptArtifactId("prompt_art_001")
    cid = CandidateId("cand_001")
    rid = ReceiptId("rcpt_001")
    rrid = RunRootId("run_root_001")
    prid = ProducerId("agent_beta")
    carr_id = CarrierId("carrier_001")
    assert isinstance(obs_id, Identifier)
    assert isinstance(pid, Identifier)
    assert isinstance(cid, Identifier)
    assert isinstance(rid, Identifier)
    assert isinstance(rrid, Identifier)
    assert isinstance(prid, Identifier)
    assert isinstance(carr_id, Identifier)
    assert str(obs_id) == "obs_001"
    assert str(pid) == "prompt_art_001"
    assert str(cid) == "cand_001"
    assert str(rid) == "rcpt_001"
    assert str(rrid) == "run_root_001"
    assert str(prid) == "agent_beta"
    assert str(carr_id) == "carrier_001"
    assert repr(obs_id) == "ObstructionId(value='obs_001')"

    # 8. PathManifest and Security
    manifest = PathManifest.create(
        owned=["omega_engine/crates/symbol_game", "omega_engine/domain"],
        protected=[".canon", "omega_engine/anomalon_councils"],
    )
    assert len(manifest.owned_paths) == 2
    assert len(manifest.protected_paths) == 2

    with pytest.raises(SecurityPathViolationError):
        OwnedPath("../traversal/bad")
    with pytest.raises(SecurityPathViolationError):
        ProtectedPath("C:\\windows\\bad")
    with pytest.raises(SecurityPathViolationError):
        OwnedPath("/absolute/bad")
    with pytest.raises(SecurityPathViolationError):
        OwnedPath("safe/file.py:alternate-stream")
    with pytest.raises(SecurityPathViolationError):
        OwnedPath("safe/trailing-space ")
    with pytest.raises(SecurityPathViolationError):
        OwnedPath("safe/control\x00name")

    # 9. LlmTurnPayloadV1 Composite Value Object
    payload = LlmTurnPayloadV1.create(
        task_id="task_turn_42",
        objective="Execute symbol game turn",
        role="assistant",
        turn_kind="symbol_game_turn",
        candidate_budget=3,
        operation_budget=10,
    )
    assert isinstance(payload.task_id, TaskId)
    assert isinstance(payload.objective, TaskObjective)
    assert isinstance(payload.role, TurnRole)
    assert isinstance(payload.turn_kind, TurnKind)
    assert isinstance(payload.candidate_budget, CandidateBudget)
    assert isinstance(payload.operation_budget, OperationBudget)
    assert isinstance(payload.required_reply_fields, RequiredReplyFields)
    dict_repr = payload.to_dict()
    assert dict_repr["task_id"] == "task_turn_42"
    assert dict_repr["candidate_budget"] == 3

    # 10. Direct import from omega_engine_pfp.domain.shared_kernel.id
    from omega_engine_pfp.domain.shared_kernel.id import (
        CandidateId as SKCandidateId,
        CarrierId as SKCarrierId,
        DemandId as SKDemandId,
        Identifier as SKIdentifier,
        ObstructionId as SKObstructionId,
        ProducerId as SKProducerId,
        PromptArtifactId as SKPromptArtifactId,
        ReceiptId as SKReceiptId,
        RunRootId as SKRunRootId,
        TaskId as SKTaskId,
    )

    assert SKTaskId("t1") == TaskId("t1")
    assert SKObstructionId("o1") == ObstructionId("o1")
    assert SKDemandId("d1") == DemandId("d1")
    assert issubclass(SKTaskId, SKIdentifier)
    assert issubclass(SKDemandId, SKIdentifier)

    # 11. Shared Kernel value objects: Description, Summary, SchemaVersion, Code, RefusalCode, Kind, FieldName, ObstructionFamily
    desc = Description("Detailed obstruction description")
    assert str(desc) == "Detailed obstruction description"
    with pytest.raises(InvariantViolationError):
        Description("")
    with pytest.raises(InvariantViolationError):
        Description("x" * (MAX_DESCRIPTION_LENGTH + 1))

    summ = Summary("Short summary of objective")
    assert str(summ) == "Short summary of objective"
    with pytest.raises(InvariantViolationError):
        Summary("")
    with pytest.raises(InvariantViolationError):
        Summary("x" * (MAX_SUMMARY_LENGTH + 1))

    schema = SchemaVersion("omega.symbol-game.prompt-artifact.v1")
    assert str(schema) == "omega.symbol-game.prompt-artifact.v1"
    with pytest.raises(InvariantViolationError):
        SchemaVersion("invalid_schema_format")

    code_vo = Code("F-01_inherited_meaning")
    assert str(code_vo) == "F-01_inherited_meaning"
    refusal_vo = RefusalCode("REFUSAL_INHERITED_MEANING")
    assert str(refusal_vo) == "REFUSAL_INHERITED_MEANING"

    kind_vo = Kind("prompt_turn")
    assert str(kind_vo) == "prompt_turn"
    field_vo = FieldName("status")
    assert str(field_vo) == "status"
    obs_fam = ObstructionFamily("ontology_smuggling")
    assert str(obs_fam) == "ontology_smuggling"

    # 12. DemandItemV1 and ObstructionHintV1 using Shared Kernel types
    #
    # Both calls named fields these types no longer carry. `DemandItemV1` had
    # `description` and `target_obstruction_id`; it now carries `kind` and an
    # optional `note`. `ObstructionHintV1` had `description`; it now carries
    # `residual_colour`, `magnitude`, `demand_id` and `prior_report_digests`.
    # Both raised `TypeError` inside `create`, so the `isinstance` assertions
    # beneath them -- the point of this section -- never ran.
    dem = DemandItemV1.create(
        demand_id="dem_001",
        kind="type_annotation",
        note="Add missing type annotations",
    )
    assert isinstance(dem.demand_id, DemandId)
    assert isinstance(dem.kind, Kind)
    assert dem.to_dict()["demand_id"] == "dem_001"

    obs_hint = ObstructionHintV1.create(
        obstruction_id="obs_001",
        family="ontology_smuggling",
        residual_colour=ResidualColour.OPEN.value,
        demand_id="dem_001",
    )
    assert isinstance(obs_hint.obstruction_id, ObstructionId)
    assert isinstance(obs_hint.family, ObstructionFamily)
    assert isinstance(obs_hint.demand_id, DemandId)
    assert obs_hint.to_dict()["obstruction_id"] == "obs_001"

    # 13. KillConditionInfo using Shared Kernel types
    kc_info = KillConditionInfo.create(
        code="F-01_inherited_meaning",
        description="Proposal re-introduces informal prose",
        severity="CRITICAL",
        refusal_code="REFUSAL_INHERITED_MEANING",
    )
    assert isinstance(kc_info.code, Code)
    assert isinstance(kc_info.description, Description)
    assert isinstance(kc_info.refusal_code, RefusalCode)
    assert kc_info.to_dict()["code"] == "F-01_inherited_meaning"

    # 14. Shared Kernel: Severity, DataRecord, ResidualDropV1, Budget variations
    from omega_engine_pfp.domain.shared_kernel import (
        Budget,
        DataRecord,
        ExecutionBudget,
        ResidualDropV1 as SKResidualDrop,
        Severity,
        SeverityKind,
        TimeBudget,
    )

    sev_crit = Severity.critical()
    assert str(sev_crit) == "CRITICAL"
    assert sev_crit.is_blocking_or_higher() is True
    with pytest.raises(InvariantViolationError):
        Severity("UNKNOWN_SEVERITY")

    data_rec = DataRecord({"key": "val", "num": 123})
    assert data_rec["key"] == "val"
    assert "num" in data_rec
    assert data_rec.to_dict() == {"key": "val", "num": 123}
    with pytest.raises(InvariantViolationError, match="keys must be exact strings"):
        DataRecord({1: "integer key", "1": "string key"})
    with pytest.raises(InvariantViolationError, match="unordered set"):
        DataRecord({"unstable": {"b", "a"}})

    res_drop = SKResidualDrop.create(delta_phi1=1.5, delta_gamma2=0.0, delta_xi=0.5)
    assert res_drop.is_strictly_contractive() is True
    assert res_drop.to_dict()["delta_phi1"] == 1.5

    exec_b = ExecutionBudget(50)
    assert int(exec_b) == 50
    assert issubclass(ExecutionBudget, Budget)

    time_b = TimeBudget(120)
    assert int(time_b) == 120
    assert issubclass(TimeBudget, Budget)

    # 15. Shared Kernel: Role, RoleKind, TurnRole, TurnKind, TurnType, Regime from crates.domain.shared_kernel
    assert issubclass(Role, Kind)
    assert issubclass(TurnRole, Role)
    assert issubclass(TurnRole, Kind)
    assert issubclass(TurnKind, Kind)

    r_user = TurnRole.user()
    assert str(r_user) == "user"
    assert TurnRole.from_str(RoleKind.ASSISTANT) == TurnRole.assistant()
    assert Role.from_str(RoleKind.OPERATOR) == Role.operator()

    k_sym = TurnKind.symbol_game()
    assert str(k_sym) == "symbol_game_turn"
    assert TurnKind.from_str(TurnModality.PROSE) == TurnKind.prose()

    tt = TurnType.from_str(TurnTypeKind.PROMPT)
    assert str(tt) == "prompt"

    reg = Regime.from_str(RegimeKind.FENCE_ONLY)
    assert str(reg) == "fence_only"
    assert Regime.symbol_only() == Regime(RegimeKind.SYMBOL_ONLY.value)

    # 16. Shared Kernel: Direct imports of moved modules from omega_engine_pfp.domain.shared_kernel
    from omega_engine_pfp.domain.shared_kernel import (
        ContentDigest as SKContentDigest,
        FieldName as SKFieldName,
        ObstructionFamily as SKObstructionFamily,
        ObstructionFamilyKind,
        ResidualColour as SKResidualColour,
        ResidualDropV1 as SKResidualDropV1,
    )

    assert issubclass(SKObstructionFamily, Kind)
    of_smug = SKObstructionFamily.from_str(ObstructionFamilyKind.ONTOLOGY_SMUGGLING)
    assert str(of_smug) == "ontology_smuggling"

    fn = SKFieldName("valid_field.key")
    assert str(fn) == "valid_field.key"

    digest = SKContentDigest.from_string("test string")
    assert len(str(digest)) == 64

    assert SKResidualColour.OPEN.value == "Open"
    assert SKResidualColour.EXACT.value == "Exact"

    # 17. Shared Kernel: Hash & Sha256Hash and LearningPolicy Aggregate Decomposition
    from omega_engine_pfp.domain.shared_kernel.hash import Hash, Sha256Hash
    from omega_engine_pfp.domain.aggregates.learning_policy import (
        FrozenCorpus,
        PolicyScore,
        RoutingHypothesis,
    )

    h = Sha256Hash.from_string("eval corpus data")
    assert len(str(h)) == 64
    assert isinstance(h, Hash)
    assert str(h) == h.hex_digest
    assert h == Sha256Hash(h.hex_digest)

    corpus = FrozenCorpus.create(
        corpus_id="corpus_001",
        corpus_sha256=str(h),
        sample_ids=["sample_1", "sample_2"],
    )
    assert str(corpus.corpus_id) == "corpus_001"
    assert str(corpus.corpus_sha256) == str(h)
    assert len(corpus.sample_ids) == 2
    assert str(corpus.sample_ids[0]) == "sample_1"
    assert corpus.to_dict()["corpus_id"] == "corpus_001"

    score = PolicyScore.create(
        policy_id="policy_opt_01",
        corpus_id="corpus_001",
        success_rate=0.95,
        average_residual_drop=0.42,
        efficiency=0.88,
    )
    assert str(score.policy_id) == "policy_opt_01"
    assert score.to_dict()["success_rate"] == 0.95

    hyp = RoutingHypothesis.create(
        hypothesis_id="hyp_route_001",
        target_regime="coda_l1",
        routing_weights={"w1": 0.5, "w2": 0.5},
        predicted_efficiency=0.91,
    )
    assert str(hyp.hypothesis_id) == "hyp_route_001"
    assert str(hyp.target_regime) == "coda_l1"
    assert hyp.to_dict()["predicted_efficiency"] == 0.91

    # 18. Shared Kernel: Combined obstruction.py and ObjectiveTypedV1 typed IDs
    from omega_engine_pfp.domain.shared_kernel.obstruction import (
        ObstructionFamily as SKObstructionFam,
        ObstructionFamilyKind as SKObstructionFamKind,
        ObstructionHintV1 as SKObstructionHintV1,
    )

    hint = SKObstructionHintV1.create(
        obstruction_id="obs_combined_001",
        family=SKObstructionFamKind.ONTOLOGY_SMUGGLING,
        description="Smuggled ontology in proof term",
    )
    assert isinstance(hint.obstruction_id, ObstructionId)
    assert isinstance(hint.family, SKObstructionFam)
    assert hint.to_dict()["obstruction_id"] == "obs_combined_001"

    # `create` converts to value objects; it does not sort. `__post_init__`
    # refuses `ARRAY_NOT_CANONICALLY_SORTED` rather than reordering, which is
    # the same house rule the run-root tuples follow. This block passed
    # `["obs_combined_001", "obs_002"]` and asserted the result came back
    # sorted -- the old contract -- so it raised before any assertion ran.
    obj_typed = ObjectiveTypedV1.create(
        kind="prompt_turn",
        summary="Refactor prompt turn with typed IDs",
        target_obstruction_ids=["obs_002", "obs_combined_001"],
        target_demand_ids=["dem_001", "dem_002"],
    )
    assert len(obj_typed.target_obstruction_ids) == 2
    assert isinstance(obj_typed.target_obstruction_ids[0], ObstructionId)
    assert len(obj_typed.target_demand_ids) == 2
    assert isinstance(obj_typed.target_demand_ids[0], DemandId)
    assert str(obj_typed.target_obstruction_ids[0]) == "obs_002"
    assert obj_typed.to_dict()["target_obstruction_ids"] == [
        "obs_002",
        "obs_combined_001",
    ]

    # The invariant the old assertion assumed away: unsorted input is refused,
    # not quietly reordered. Without this the block above only shows that
    # already-sorted input survives.
    with pytest.raises(CanonicalizationError):
        ObjectiveTypedV1.create(
            kind="prompt_turn",
            summary="Unsorted target ids",
            target_obstruction_ids=["obs_combined_001", "obs_002"],
        )
    assert obj_typed.to_dict()["target_demand_ids"] == ["dem_001", "dem_002"]

    # 19. Shared Kernel: Key and KeyType
    from omega_engine_pfp.domain.shared_kernel import (
        CommonWireKeyKind,
        ContextKey,
        Key,
        KeyType,
        WireKeyVO,
    )

    k = Key("task_id")
    assert str(k) == "task_id"
    assert k == Key("task_id")
    assert k == Key(CommonWireKeyKind.TASK_ID.value)

    wk = WireKeyVO("schema_version")
    assert wk.key_type == KeyType.WIRE
    assert wk == WireKeyVO("schema_version")
    assert wk == WireKeyVO(CommonWireKeyKind.SCHEMA_VERSION.value)

    ck = ContextKey("model_id")
    assert ck.key_type == KeyType.CONTEXT
    assert ck == ContextKey("model_id")

    # 20. Shared Kernel: LlmPayloadV1, TaskObjective, and PathManifest
    from omega_engine_pfp.domain.shared_kernel import (
        LlmPayloadV1 as SKLlmPayloadV1,
        LlmTurnPayloadV1 as SKLlmTurnPayloadV1,
        PathManifest as SKPathManifest,
        TaskObjective as SKTaskObjective,
    )

    t_obj = SKTaskObjective("Formulate contractive coboundary")
    assert str(t_obj) == "Formulate contractive coboundary"

    manifest = SKPathManifest.create(
        owned=["src/core.py", "src/models.py"],
        protected=["src/config.py"],
    )
    assert len(manifest.owned_paths) == 2
    assert len(manifest.protected_paths) == 1

    llm_p = SKLlmPayloadV1.create(
        task_id="task_turn_001",
        objective="Run LLM turn",
        prompt_artifact_id="prompt_art_001",
        prompt_body_sha256="a" * 64,
        prompt_body_bytes_len=1024,
    )
    assert isinstance(llm_p, SKLlmTurnPayloadV1)
    assert isinstance(llm_p.schema_version, SchemaVersion)
    assert str(llm_p.schema_version) == "omega.symbol-game.llm-turn.v1"
    assert str(llm_p.task_id) == "task_turn_001"
    assert llm_p.to_dict()["task_id"] == "task_turn_001"
