from __future__ import annotations
from omega_engine.crates.type.symgame import TerminalStatus, Obstruction, ProjectionReceipt, DetectorCase, SolverManifest, SolverProposal

from dataclasses import replace
from typing import Any

import pytest

from omega_engine_pfp.infrastructure.serialization import (
    domain_digest,
    freeze,
)
from omega_engine.crates.operator.projector.proj_symbol_game import (
    DetectorCase,
    IdentityAdapter,
    Obstruction,
    ProjectionReceipt,
    RuntimeProblem,
    SolverManifest,
    SolverProposal,
    TerminalStatus,
)
from omega_engine_pfp.fixtures import (
    ExhaustiveCspSolver,
    NamedVariableRetraction,
    NoOpClaimingSolver,
    build_demo_problem,
)
from omega_engine_pfp.fixtures.finite_csp import (
    normalize_state,
)
from omega_engine.crates.engine.eng_symbol_game import OesosLab
from omega_engine_pfp.domain import (
    CandidateArtifactV1,
    PacketEnvelopeV2,
)


def test_candidate_claim_cannot_bypass_projection_or_obstruction_ledger() -> None:
    problem = build_demo_problem()
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(problem)

    assert run.terminal_status is TerminalStatus.LAB_EXACT_CANDIDATE
    assert run.locally_resolved
    assert len(run.attempts) == 2
    assert run.attempts[0].claimed_terminal == "Exact"
    assert not run.attempts[0].accepted
    assert run.attempts[0].reason == "repeated-state"
    assert run.attempts[1].accepted
    assert run.active_obstructions == ()
    opened = {
        event.obstruction_id
        for event in run.obstruction_events
        if event.disposition == "OPENED"
    }
    discharged = {
        event.obstruction_id
        for event in run.obstruction_events
        if event.disposition == "DISCHARGED"
    }
    assert opened == discharged == set(problem.envelope.constraints)


def test_packet_commitment_refuses_native_state_substitution() -> None:
    problem = build_demo_problem()
    substituted = replace(
        problem,
        native_initial_state=(("x", 1), ("y", 1)),
    )

    run = OesosLab((ExhaustiveCspSolver(),)).solve(substituted)

    assert run.terminal_status is TerminalStatus.INVALID_PACKET
    assert "INITIAL_STATE_PACKET_MISMATCH" in run.stop_reasons
    assert not run.locally_resolved

    type_substituted = replace(
        problem,
        native_initial_state=list(problem.native_initial_state),
    )
    type_run = OesosLab((ExhaustiveCspSolver(),)).solve(type_substituted)
    assert "INITIAL_STATE_PACKET_MISMATCH" in type_run.stop_reasons


@pytest.mark.parametrize(
    "envelope_change",
    (
        {"payload": {"different_problem": True}},
        {"constraints": ("unrelated:constraint",)},
    ),
)
def test_packet_contract_must_match_projector_runtime_semantics(
    envelope_change: dict[str, Any],
) -> None:
    problem = build_demo_problem()
    mismatched = replace(
        problem,
        envelope=replace(problem.envelope, **envelope_change),
    )

    run = OesosLab((ExhaustiveCspSolver(),)).solve(mismatched)

    assert run.terminal_status is TerminalStatus.INVALID_PACKET
    assert "PACKET_RUNTIME_SEMANTICS_MISMATCH" in run.stop_reasons
    assert not run.locally_resolved


class ExactStateAttackSolver:
    manifest = SolverManifest(
        solver_id="finite-exhaustive-retraction",
        families=("finite_csp",),
    )

    def __init__(self, mode: str) -> None:
        self.mode = mode

    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal:
        exact = (("x", 1), ("y", 1))
        kwargs: dict[str, Any] = {
            "packet_id": problem.envelope.packet_id,
            "producer_id": self.manifest.solver_id,
            "payload": exact,
            "witness": "attacker-witness",
        }
        if self.mode == "payload":
            kwargs["payload"] = {"decoy": "not-executed"}
        elif self.mode == "witness":
            kwargs["witness"] = ""
        elif self.mode == "authority":
            kwargs["authority_effect"] = "Promote"
        elif self.mode == "producer":
            kwargs["producer_id"] = "different-producer"
        return SolverProposal(
            state=exact,
            candidate=CandidateArtifactV1(**kwargs),
            next_carrier_id=problem.adapter.target_carrier_id,
        )


@pytest.mark.parametrize(
    ("mode", "reason"),
    (
        ("payload", "candidate-payload-state-mismatch"),
        ("witness", "candidate-witness-missing"),
        ("authority", "candidate-authority-expansion"),
        ("producer", "candidate-producer-mismatch"),
    ),
)
def test_candidate_artifact_must_bind_the_evaluated_move(
    mode: str,
    reason: str,
) -> None:
    run = OesosLab((ExactStateAttackSolver(mode),)).solve(build_demo_problem())

    assert not run.locally_resolved
    assert run.attempts[0].reason == reason
    assert run.evidence_valid()
    assert len(run.candidate_artifacts) == 1
    assert run.candidate_artifacts[0].candidate_id == run.attempts[0].candidate_id


@pytest.mark.parametrize(
    "mutator",
    (
        lambda run: replace(
            run,
            prime000=replace(run.prime000, declarations=("forged",)),
        ),
        lambda run: replace(
            run,
            adapter=replace(run.adapter, adapter_id="forged-adapter"),
        ),
        lambda run: replace(
            run,
            adapter=replace(run.adapter, detail="forged-detail"),
        ),
        lambda run: replace(
            run,
            detector=replace(run.detector, projector_id="forged-projector"),
        ),
        lambda run: replace(
            run,
            detector=replace(run.detector, cases_checked=0),
        ),
        lambda run: replace(run, final_native_state={"forged": True}),
        lambda run: replace(
            run,
            final_projection=replace(
                run.final_projection,
                projector_id="forged-projector",
            ),
        ),
        lambda run: replace(
            run,
            final_projection=replace(run.final_projection, witness="forged-witness"),
        ),
    ),
    ids=(
        "prime000",
        "adapter-id",
        "adapter-detail",
        "detector-id",
        "detector-count",
        "final-native-state",
        "projection-id",
        "projection-witness",
    ),
)
def test_green_receipt_binds_every_admission_gate(mutator: Any) -> None:
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(
        build_demo_problem()
    )

    forged = mutator(run)

    assert run.locally_resolved
    assert not forged.evidence_valid()
    assert not forged.locally_resolved
    with pytest.raises(ValueError, match="committed evidence"):
        forged.to_wire_receipt()


def test_green_receipt_binds_candidate_artifact_set_and_content() -> None:
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(
        build_demo_problem()
    )
    assert run.locally_resolved
    assert len(run.candidate_artifacts) == 2

    dropped = replace(run, candidate_artifacts=run.candidate_artifacts[:-1])
    replacement = replace(run.candidate_artifacts[-1], witness="forged-witness")
    replaced = replace(
        run,
        candidate_artifacts=(*run.candidate_artifacts[:-1], replacement),
    )

    for forged in (dropped, replaced):
        assert not forged.evidence_valid()
        assert not forged.locally_resolved


class ReceiptTupleSubclass(tuple):
    """Carries uncommitted state while comparing like an ordinary tuple."""

    authority_effect = "Promote"


@pytest.mark.parametrize(
    "mutator",
    (
        lambda run: replace(
            run,
            stop_reasons=ReceiptTupleSubclass(run.stop_reasons),
        ),
        lambda run: replace(run, attempts=ReceiptTupleSubclass(run.attempts)),
        lambda run: replace(
            run,
            candidate_artifacts=ReceiptTupleSubclass(run.candidate_artifacts),
        ),
        lambda run: replace(
            run,
            obstruction_events=ReceiptTupleSubclass(run.obstruction_events),
        ),
        lambda run: replace(
            run,
            active_obstructions=ReceiptTupleSubclass(run.active_obstructions),
        ),
        lambda run: replace(
            run,
            process_events=ReceiptTupleSubclass(run.process_events),
        ),
        lambda run: replace(
            run,
            prime000=replace(
                run.prime000,
                declarations=ReceiptTupleSubclass(run.prime000.declarations),
            ),
        ),
        lambda run: replace(
            run,
            adapter=replace(
                run.adapter,
                loss_ledger=ReceiptTupleSubclass(run.adapter.loss_ledger),
            ),
        ),
        lambda run: replace(
            run,
            detector=replace(
                run.detector,
                failures=ReceiptTupleSubclass(run.detector.failures),
            ),
        ),
        lambda run: replace(
            run,
            final_projection=replace(
                run.final_projection,
                obstructions=ReceiptTupleSubclass(
                    run.final_projection.obstructions,
                ),
            ),
        ),
        lambda run: replace(
            run,
            attempts=(
                *run.attempts[:-1],
                replace(
                    run.attempts[-1],
                    before_measure=ReceiptTupleSubclass(
                        run.attempts[-1].before_measure
                    ),
                ),
            ),
        ),
    ),
    ids=(
        "stop-reasons",
        "attempts",
        "artifacts",
        "obstruction-events",
        "active-obstructions",
        "process-events",
        "prime-declarations",
        "adapter-loss-ledger",
        "detector-failures",
        "projection-obstructions",
        "attempt-measure",
    ),
)
def test_receipt_refuses_tuple_substitution_even_when_contents_match(
    mutator: Any,
) -> None:
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(
        build_demo_problem()
    )

    forged = mutator(run)

    assert not forged.evidence_valid()
    with pytest.raises(ValueError, match="committed evidence"):
        forged.to_wire_receipt()


@pytest.mark.parametrize(
    "mutator",
    (
        lambda run: replace(run, prime000=None),
        lambda run: replace(run, adapter=object()),
        lambda run: replace(run, detector="wrong-type"),
        lambda run: replace(run, final_projection=object()),
        lambda run: replace(run, obstruction_events=(object(),)),
        lambda run: replace(run, process_events=(object(),)),
        lambda run: replace(run, packet_id=7),
    ),
    ids=(
        "prime000",
        "adapter",
        "detector",
        "projection",
        "obstruction-event",
        "process-event",
        "scalar-hash",
    ),
)
def test_evidence_validator_is_total_on_malformed_nested_types(mutator: Any) -> None:
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(
        build_demo_problem()
    )

    forged = mutator(run)

    assert forged.evidence_valid() is False
    assert forged.locally_resolved is False
    with pytest.raises(ValueError, match="committed evidence"):
        forged.to_wire_receipt()


class MutableMeaningAdapter:
    adapter_id = "mutable-meaning-adapter-v1"
    source_carrier_id = "finite-csp-v1"
    target_carrier_id = "finite-csp-v1"

    @property
    def config_digest(self) -> str:
        return domain_digest(
            "omega.oesos.adapter-config.v1",
            {
                "adapter_id": self.adapter_id,
                "source_carrier_id": self.source_carrier_id,
                "target_carrier_id": self.target_carrier_id,
            },
        )

    def adapt(self, state: Any) -> Any:
        return state

    def descend(self, state: Any) -> Any:
        return state

    def native_meaning(self, state: Any) -> Any:
        return normalize_state(state)

    def packet_meaning(self, state: Any) -> Any:
        return normalize_state(state)

    def loss_ledger(self, state: Any) -> tuple[str, ...]:
        return ()


def test_mutable_final_output_is_detached_and_mutation_breaks_evidence() -> None:
    base = build_demo_problem()
    native_state = {"x": 1, "y": 1}
    normalized = normalize_state(native_state)
    projector = base.projector
    payload = {
        "domains": projector.domains,
        "constraints": tuple(
            {
                "constraint_id": item.constraint_id,
                "coefficients": item.coefficients,
                "rhs": item.rhs,
                "closure_failure": item.closure_failure,
            }
            for item in projector.constraints
        ),
        "initial_state": normalized,
    }
    envelope = replace(
        base.envelope,
        payload=payload,
        initial_state_hash=domain_digest(
            "omega.oesos.native-state.v1",
            native_state,
        ),
        source_digest=domain_digest("omega.oesos.fixture-source.v1", payload),
    )
    problem = replace(
        base,
        envelope=envelope,
        native_initial_state=native_state,
        adapter=MutableMeaningAdapter(),
    )
    run = OesosLab((ExhaustiveCspSolver(),)).solve(problem)

    assert run.locally_resolved
    assert run.final_native_state is not problem.native_initial_state
    run.final_native_state["x"] = 0

    assert problem.native_initial_state["x"] == 1
    assert not run.evidence_valid()
    assert not run.locally_resolved


class UnknownRetractionSolver(ExactStateAttackSolver):
    manifest = SolverManifest(
        solver_id="unknown-retraction",
        families=("finite_csp",),
    )


def test_candidate_cannot_self_certify_a_retraction() -> None:
    run = OesosLab((UnknownRetractionSolver("valid"),)).solve(build_demo_problem())

    assert not run.locally_resolved
    assert run.attempts[0].reason == "host-retraction-law-failed"


class ManifestAttackSolver(ExactStateAttackSolver):
    def __init__(self, *, authority: str = "None", deterministic: bool = True) -> None:
        super().__init__("valid")
        self.manifest = SolverManifest(
            solver_id="finite-exhaustive-retraction",
            families=("finite_csp",),
            authority_effect=authority,
            deterministic=deterministic,
        )


@pytest.mark.parametrize(
    ("solver", "blocker"),
    (
        (ManifestAttackSolver(authority="Promote"), "SOLVER_AUTHORITY_EXPANSION"),
        (ManifestAttackSolver(deterministic=False), "NONDETERMINISTIC_SOLVER"),
    ),
)
def test_solver_manifest_cannot_expand_authority_or_disable_replay(
    solver: ManifestAttackSolver,
    blocker: str,
) -> None:
    run = OesosLab((solver,)).solve(build_demo_problem())

    assert run.terminal_status is TerminalStatus.INVALID_PACKET
    assert any(reason.startswith(blocker) for reason in run.stop_reasons)
    assert not run.attempts


class ManifestMutatingSolver(ExactStateAttackSolver):
    def __init__(self) -> None:
        super().__init__("valid")
        self.manifest = SolverManifest(
            solver_id="finite-exhaustive-retraction",
            families=("finite_csp",),
        )

    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal:
        self.manifest = replace(self.manifest, authority_effect="Promote")
        return super().propose(problem, packet_state, projection)


def test_solver_manifest_is_rechecked_after_proposal() -> None:
    run = OesosLab((ManifestMutatingSolver(),)).solve(build_demo_problem())

    assert not run.locally_resolved
    assert run.attempts[0].reason == "solver-manifest-drift"


class DroppingKeyAdapter:
    adapter_id = "lossy-drop-y"
    source_carrier_id = "finite-csp-v1"
    target_carrier_id = "finite-csp-v1"

    @property
    def config_digest(self) -> str:
        return domain_digest("test.adapter-config", self.adapter_id)

    def adapt(self, native_state: Any) -> Any:
        return tuple((name, value) for name, value in native_state if name != "y")

    def descend(self, packet_state: Any) -> Any:
        return tuple(packet_state)

    def native_meaning(self, native_state: Any) -> Any:
        return tuple(native_state)

    def packet_meaning(self, packet_state: Any) -> Any:
        return tuple(packet_state)

    def loss_ledger(self, native_state: Any) -> tuple[str, ...]:
        return ("protected:y",)


def test_prime001_refuses_loss_of_a_protected_distinction() -> None:
    problem = replace(build_demo_problem(), adapter=DroppingKeyAdapter())
    run = OesosLab((ExhaustiveCspSolver(),)).solve(problem)

    assert run.terminal_status is TerminalStatus.ADAPTER_FAILURE
    assert not run.adapter.sound
    assert run.adapter.loss_ledger == ("protected:y",)
    assert run.attempts == ()


class FailingFinalDescentAdapter:
    adapter_id = "fails-only-on-final-descent"
    source_carrier_id = "finite-csp-v1"
    target_carrier_id = "finite-csp-v1"

    def __init__(self) -> None:
        self.descents = 0

    @property
    def config_digest(self) -> str:
        return domain_digest("test.adapter-config", self.adapter_id)

    def adapt(self, native_state: Any) -> Any:
        return native_state

    def descend(self, packet_state: Any) -> Any:
        self.descents += 1
        if self.descents >= 3:
            raise RuntimeError("final descent refused")
        return packet_state

    def native_meaning(self, native_state: Any) -> Any:
        return native_state

    def packet_meaning(self, packet_state: Any) -> Any:
        return packet_state

    def loss_ledger(self, native_state: Any) -> tuple[str, ...]:
        return ()


def test_final_descent_failure_cannot_retain_a_local_exact_candidate() -> None:
    problem = replace(build_demo_problem(), adapter=FailingFinalDescentAdapter())
    run = OesosLab((ExhaustiveCspSolver(),)).solve(problem)

    assert run.terminal_status is TerminalStatus.ADAPTER_FAILURE
    assert run.final_native_state is None
    assert any("FINAL_DESCENT_FAILURE" in reason for reason in run.stop_reasons)
    assert not run.locally_resolved


class ConstantGreenProjector:
    projector_id = "constant-green-attack"

    def __init__(self, delegate: Any) -> None:
        self.delegate = delegate

    @property
    def config_digest(self) -> str:
        return domain_digest("test.projector-config", self.projector_id)

    def meaning(self, state: Any) -> Any:
        return self.delegate.meaning(state)

    def skeleton(self, state: Any) -> Any:
        return self.delegate.skeleton(state)

    def validate_packet(
        self,
        envelope: PacketEnvelopeV2,
        native_initial_state: Any,
    ) -> bool:
        return self.delegate.validate_packet(envelope, native_initial_state)

    def project(self, state: Any) -> ProjectionReceipt:
        return ProjectionReceipt(
            projector_id=self.projector_id,
            state_hash=domain_digest("omega.oesos.state.v1", self.meaning(state)),
            obstructions=(),
            witness="constant-detector-attack",
        )

    def verify_retraction(
        self,
        solver_id: str,
        before_state: Any,
        after_state: Any,
    ) -> bool:
        return False


def test_detector_adequacy_runs_the_negative_control() -> None:
    base = build_demo_problem()
    projector = ConstantGreenProjector(base.projector)
    problem = replace(base, projector=projector, observer_id=projector.projector_id)
    run = OesosLab((ExhaustiveCspSolver(),)).solve(problem)

    assert run.terminal_status is TerminalStatus.DETECTOR_INADEQUATE
    assert not run.detector.adequate
    assert any("known-obstructed" in failure for failure in run.detector.failures)


def test_prime002_stops_at_budget_with_obstruction_still_open() -> None:
    problem = build_demo_problem(step_budget=1)
    engine = OesosLab(
        (NamedVariableRetraction("x", 1), NamedVariableRetraction("y", 1))
    )
    run = engine.solve(problem)

    assert run.terminal_status is TerminalStatus.BUDGET_EXHAUSTED
    assert run.accepted_steps == 1
    assert run.active_obstructions
    assert "BUDGET_EXHAUSTED" in run.stop_reasons
    assert any(
        event.disposition == "UPDATED" and event.obstruction_id == "closure:x+y"
        for event in run.obstruction_events
    )


class TradeoffProjector:
    projector_id = "tradeoff-projector"

    @property
    def config_digest(self) -> str:
        return domain_digest("test.projector-config", self.projector_id)

    def meaning(self, state: Any) -> Any:
        return str(state)

    def skeleton(self, state: Any) -> Any:
        return "fixed-skeleton"

    def validate_packet(
        self,
        envelope: PacketEnvelopeV2,
        native_initial_state: Any,
    ) -> bool:
        payload = {"initial_state": "before", "carrier": "fixed-skeleton"}
        return (
            native_initial_state == "before"
            and envelope.constraints == ("A", "B")
            and envelope.payload == freeze(payload)
            and envelope.source_digest == domain_digest("test.tradeoff-source", payload)
        )

    def project(self, state: Any) -> ProjectionReceipt:
        obstruction_map = {
            "before": (
                Obstruction("A", 10.0, "A residual"),
                Obstruction("B", 1.0, "B residual"),
            ),
            "worsen": (Obstruction("A", 11.0, "A residual"),),
            "introduce": (
                Obstruction("A", 9.0, "A residual"),
                Obstruction("C", 0.5, "new residual"),
            ),
            "exact": (),
        }
        return ProjectionReceipt(
            projector_id=self.projector_id,
            state_hash=domain_digest("omega.oesos.state.v1", self.meaning(state)),
            obstructions=obstruction_map[str(state)],
            witness="independent-tradeoff-control",
        )

    def verify_retraction(
        self,
        solver_id: str,
        before_state: Any,
        after_state: Any,
    ) -> bool:
        return solver_id == "tradeoff-producer" and before_state != after_state


class TradeoffSolver:
    manifest = SolverManifest(
        solver_id="tradeoff-producer",
        families=("tradeoff",),
    )

    def __init__(self, target: str) -> None:
        self.target = target

    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal:
        return SolverProposal(
            state=self.target,
            candidate=CandidateArtifactV1(
                packet_id=problem.envelope.packet_id,
                producer_id=self.manifest.solver_id,
                payload=self.target,
                witness="adversarial-obstruction-tradeoff",
            ),
            next_carrier_id=problem.adapter.target_carrier_id,
        )


def _tradeoff_problem() -> RuntimeProblem:
    projector = TradeoffProjector()
    before_projection = projector.project("before")
    exact_projection = projector.project("exact")
    payload = {"initial_state": "before", "carrier": "fixed-skeleton"}
    envelope = PacketEnvelopeV2(
        task_id="tradeoff-control",
        packet_family="tradeoff",
        carrier_id="tradeoff-v1",
        initial_state_hash=domain_digest("omega.oesos.native-state.v1", "before"),
        payload=payload,
        constraints=("A", "B"),
        protected_boundaries=("A", "B"),
        step_budget=1,
        source_digest=domain_digest("test.tradeoff-source", payload),
    )
    return RuntimeProblem(
        envelope=envelope,
        native_initial_state="before",
        projector=projector,
        adapter=IdentityAdapter("tradeoff-v1", "tradeoff-v1"),
        detector_cases=(
            DetectorCase(
                "exact-control",
                "exact",
                (),
                exact_projection.control_digest,
            ),
            DetectorCase(
                "red-control",
                "before",
                before_projection.active_ids,
                before_projection.control_digest,
            ),
        ),
        primitive_difference="named obstruction magnitude",
        zero_relation="no named obstruction remains",
        observer_id=projector.projector_id,
        witness_certificate="tradeoff-controls-v1",
        protected_obstruction_ids=("A", "B"),
    )


@pytest.mark.parametrize("target", ("worsen", "introduce"))
def test_obstruction_tradeoffs_and_new_ids_are_not_descent(target: str) -> None:
    run = OesosLab((TradeoffSolver(target),)).solve(_tradeoff_problem())

    assert not run.locally_resolved
    assert run.attempts[0].reason == "no-strict-residual-descent"


def test_stuck_solver_returns_typed_active_obstruction() -> None:
    run = OesosLab((NoOpClaimingSolver(),)).solve(build_demo_problem())

    assert run.terminal_status is TerminalStatus.LAB_ACTIVE_CLOSURE_FAILURE_CANDIDATE
    assert run.stop_reasons == ("STUCK_CORPUS",)
    assert set(run.active_obstructions) == {
        "fixed:x",
        "fixed:y",
        "closure:x+y",
    }


