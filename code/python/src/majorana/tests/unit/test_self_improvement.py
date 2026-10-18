from __future__ import annotations
from omega_engine.crates.type.symgame import TerminalStatus, ProjectionReceipt, SolverManifest, SolverProposal

from typing import Any

import pytest

from omega_engine_pfp.fixtures import (
    ExhaustiveCspSolver,
    NoOpClaimingSolver,
    build_demo_problem,
)
from omega_engine_pfp.domain.aggregates.learning_policy import (
    FrozenCorpus,
    evaluate_policy,
    propose_routing_update,
)
from omega_engine.crates.engine.eng_symbol_game import OesosLab
from omega_engine.crates.operator.projector.proj_symbol_game import (
    ProjectionReceipt,
    RuntimeProblem,
    SolverManifest,
    SolverProposal,
    TerminalStatus,
)
from omega_engine_pfp.domain import CandidateArtifactV1


def _corpora() -> tuple[FrozenCorpus, FrozenCorpus]:
    exact = TerminalStatus.LAB_EXACT_CANDIDATE.value
    training = FrozenCorpus(
        "training-v1",
        (
            build_demo_problem(task_id="train-0"),
            build_demo_problem(task_id="train-1", initial=(("x", 1), ("y", 0))),
        ),
        (exact, exact),
    )
    held_out = FrozenCorpus(
        "held-out-v1",
        (
            build_demo_problem(task_id="held-0", initial=(("x", 0), ("y", 1))),
            build_demo_problem(task_id="held-1", initial=(("x", 0), ("y", 0))),
        ),
        (exact, exact),
    )
    return training, held_out


def test_engine_runs_its_policy_through_its_own_packet_machinery() -> None:
    solvers = (NoOpClaimingSolver(), ExhaustiveCspSolver())
    engine = OesosLab(solvers)
    baseline_policy = engine.policy
    training, held_out = _corpora()

    receipt = propose_routing_update(engine, training, held_out)

    assert receipt.policy_packet_run.locally_resolved
    assert receipt.non_regression_passed
    assert receipt.strict_improvement
    assert receipt.proposed_policy == tuple(reversed(baseline_policy))
    assert (
        receipt.training_proposed.total_attempts
        < receipt.training_baseline.total_attempts
    )
    assert (
        receipt.held_out_proposed.total_attempts
        < receipt.held_out_baseline.total_attempts
    )
    assert (
        receipt.held_out_proposed.correct_terminal_count
        == receipt.held_out_baseline.correct_terminal_count
    )
    assert not receipt.applied_locally
    assert engine.policy == baseline_policy


def test_local_promotion_refuses_without_isolation_attestation() -> None:
    engine = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver()))
    baseline_policy = engine.policy
    training, held_out = _corpora()

    assert not engine.promotion_isolation_attested
    with pytest.raises(ValueError, match="promotion isolation is not attested"):
        propose_routing_update(engine, training, held_out, apply=True)

    assert engine.policy == baseline_policy


def test_direct_policy_mutation_is_not_a_public_admission_surface() -> None:
    engine = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver()))

    assert not hasattr(engine, "apply_local_policy")


def test_no_policy_is_applied_without_strict_training_improvement() -> None:
    engine = OesosLab((ExhaustiveCspSolver(), NoOpClaimingSolver()))
    training, held_out = _corpora()

    receipt = propose_routing_update(engine, training, held_out, apply=False)

    assert not receipt.strict_improvement
    assert not receipt.applied_locally
    assert engine.policy == receipt.baseline_policy


def test_training_and_held_out_packet_ids_must_be_disjoint() -> None:
    engine = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver()))
    training, _ = _corpora()

    with pytest.raises(ValueError, match="disjoint"):
        propose_routing_update(engine, training, training)


class StatefulSnapshotSolver:
    manifest = SolverManifest(
        solver_id="finite-exhaustive-retraction",
        families=("finite_csp",),
    )

    def __init__(self) -> None:
        self.calls = 0

    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        self.calls += 1
        if self.calls != 1:
            return None
        exact = (("x", 1), ("y", 1))
        return SolverProposal(
            state=exact,
            candidate=CandidateArtifactV1(
                packet_id=problem.envelope.packet_id,
                producer_id=self.manifest.solver_id,
                payload=exact,
                witness="fresh-snapshot-control",
            ),
            next_carrier_id=problem.adapter.target_carrier_id,
        )


def test_policy_evaluation_uses_a_fresh_solver_snapshot_per_run() -> None:
    solver = StatefulSnapshotSolver()
    problem = build_demo_problem(task_id="stateful-snapshot")
    corpus = FrozenCorpus(
        "stateful-snapshot-corpus",
        (problem,),
        (TerminalStatus.LAB_EXACT_CANDIDATE.value,),
    )
    policy = (solver.manifest.solver_id,)

    first = evaluate_policy((solver,), policy, corpus)
    second = evaluate_policy((solver,), policy, corpus)

    assert first == second
    assert first.correct_terminal_count == 1
    assert solver.calls == 0


class GlobalToggleSolver(StatefulSnapshotSolver):
    global_calls = 0

    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        type(self).global_calls += 1
        if type(self).global_calls % 2 == 0:
            return None
        self.calls = 0
        return super().propose(problem, packet_state, projection)


def test_duplicate_replay_refuses_hidden_global_nondeterminism() -> None:
    GlobalToggleSolver.global_calls = 0
    solver = GlobalToggleSolver()
    problem = build_demo_problem(task_id="global-toggle")
    corpus = FrozenCorpus(
        "global-toggle-corpus",
        (problem,),
        (TerminalStatus.LAB_EXACT_CANDIDATE.value,),
    )

    with pytest.raises(
        ValueError,
        match="determinism replay mismatch|solver factory environment drift",
    ):
        evaluate_policy((solver,), (solver.manifest.solver_id,), corpus)


class PairStableGlobalToggleSolver(StatefulSnapshotSolver):
    _global_calls = 0

    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        type(self)._global_calls += 1
        evaluation_pair = (type(self)._global_calls - 1) // 2
        if evaluation_pair % 2:
            return None
        self.calls = 0
        return super().propose(problem, packet_state, projection)


def test_promotion_refuses_pair_stable_class_global_execution_state() -> None:
    PairStableGlobalToggleSolver._global_calls = 0
    solver = PairStableGlobalToggleSolver()
    engine = OesosLab((NoOpClaimingSolver(), solver))
    baseline_policy = engine.policy
    exact = TerminalStatus.LAB_EXACT_CANDIDATE.value
    training = FrozenCorpus(
        "pair-stable-training",
        (build_demo_problem(task_id="pair-stable-train"),),
        (exact,),
    )
    held_out = FrozenCorpus(
        "pair-stable-held-out",
        (build_demo_problem(task_id="pair-stable-held"),),
        (exact,),
    )

    assert any(
        finding.endswith("PairStableGlobalToggleSolver._global_calls")
        for finding in engine.promotion_isolation_findings
    )

    with pytest.raises(ValueError, match="promotion isolation"):
        propose_routing_update(engine, training, held_out, apply=True)

    assert engine.policy == baseline_policy


class ReflectiveGlobalSolver(StatefulSnapshotSolver):
    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        globals()
        return super().propose(problem, packet_state, projection)


def test_promotion_refuses_reflective_global_access() -> None:
    engine = OesosLab((NoOpClaimingSolver(), ReflectiveGlobalSolver()))
    training, held_out = _corpora()

    with pytest.raises(ValueError, match="ambient-reflective-builtin:.*globals"):
        propose_routing_update(engine, training, held_out, apply=True)


_TRANSITIVE_HELPER_PAIR_CALLS = 0


def _pair_stable_ambient_helper(
    solver: StatefulSnapshotSolver,
    problem: RuntimeProblem,
    packet_state: Any,
    projection: ProjectionReceipt,
) -> SolverProposal | None:
    global _TRANSITIVE_HELPER_PAIR_CALLS
    file_capability = open
    assert file_capability is not None
    _TRANSITIVE_HELPER_PAIR_CALLS += 1
    evaluation_pair = (_TRANSITIVE_HELPER_PAIR_CALLS - 1) // 2
    if evaluation_pair % 2:
        return None
    solver.calls = 0
    return StatefulSnapshotSolver.propose(
        solver,
        problem,
        packet_state,
        projection,
    )


class TransitiveHelperAttackSolver(StatefulSnapshotSolver):
    def _hidden_helper(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        return _pair_stable_ambient_helper(
            self,
            problem,
            packet_state,
            projection,
        )

    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        return self._hidden_helper(problem, packet_state, projection)


def test_promotion_refuses_transitive_helper_false_promotion() -> None:
    global _TRANSITIVE_HELPER_PAIR_CALLS
    _TRANSITIVE_HELPER_PAIR_CALLS = 0
    engine = OesosLab((NoOpClaimingSolver(), TransitiveHelperAttackSolver()))
    baseline_policy = engine.policy
    training, held_out = _corpora()

    assert any(
        "_pair_stable_ambient_helper" in finding
        and "_TRANSITIVE_HELPER_PAIR_CALLS" in finding
        for finding in engine.promotion_isolation_findings
    )
    assert any(
        "_pair_stable_ambient_helper" in finding and "open" in finding
        for finding in engine.promotion_isolation_findings
    )
    with pytest.raises(ValueError, match="promotion isolation"):
        propose_routing_update(engine, training, held_out, apply=True)

    assert _TRANSITIVE_HELPER_PAIR_CALLS == 0
    assert engine.policy == baseline_policy


class AliasedTransitiveHelperAttackSolver(TransitiveHelperAttackSolver):
    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        helper = self._hidden_helper
        return helper(problem, packet_state, projection)


def test_promotion_refuses_aliased_self_helper_false_promotion() -> None:
    global _TRANSITIVE_HELPER_PAIR_CALLS
    _TRANSITIVE_HELPER_PAIR_CALLS = 0
    engine = OesosLab((NoOpClaimingSolver(), AliasedTransitiveHelperAttackSolver()))
    baseline_policy = engine.policy
    training, held_out = _corpora()

    assert any(
        "_pair_stable_ambient_helper" in finding
        and "_TRANSITIVE_HELPER_PAIR_CALLS" in finding
        for finding in engine.promotion_isolation_findings
    )
    assert any(
        "_pair_stable_ambient_helper" in finding and "open" in finding
        for finding in engine.promotion_isolation_findings
    )
    with pytest.raises(ValueError, match="promotion isolation"):
        propose_routing_update(engine, training, held_out, apply=True)

    assert _TRANSITIVE_HELPER_PAIR_CALLS == 0
    assert engine.policy == baseline_policy


class NestedExecutableAttackSolver(StatefulSnapshotSolver):
    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        def hidden() -> None:
            open("never-executed")

        assert hidden is not None
        return None


class RuntimeImportAttackSolver(StatefulSnapshotSolver):
    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        import random

        assert random is not None
        return None


class ReflectiveOwnerAttackSolver(StatefulSnapshotSolver):
    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        class_namespace = type(self).__dict__
        assert class_namespace
        return None


class MutableDefaultAttackSolver(StatefulSnapshotSolver):
    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
        hidden_state: list[int] = [],
    ) -> SolverProposal | None:
        hidden_state.append(1)
        return None


def _make_closure_helper() -> Any:
    hidden_state = [0]

    def helper(
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        hidden_state[0] += 1
        return None

    return helper


_CLOSURE_HELPER = _make_closure_helper()


class ClosureHelperAttackSolver(StatefulSnapshotSolver):
    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        return _CLOSURE_HELPER(problem, packet_state, projection)


@pytest.mark.parametrize(
    ("solver", "finding"),
    (
        (NestedExecutableAttackSolver(), "nested-executable-code"),
        (RuntimeImportAttackSolver(), "runtime-import-edge"),
        (ReflectiveOwnerAttackSolver(), "reflective-owner-access"),
        (MutableDefaultAttackSolver(), "mutable-callable-default"),
        (ClosureHelperAttackSolver(), "unisolated-closure-binding"),
    ),
)
def test_promotion_refuses_unisolated_callable_edges(
    solver: StatefulSnapshotSolver,
    finding: str,
) -> None:
    engine = OesosLab((NoOpClaimingSolver(), solver))

    assert not engine.promotion_isolation_attested
    assert any(item.startswith(finding) for item in engine.promotion_isolation_findings)


