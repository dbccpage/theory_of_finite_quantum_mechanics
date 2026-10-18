"""Verifier tests for finite research-model Symbol Game adapters."""

from __future__ import annotations
from omega_engine.crates.type.symgame import TerminalStatus

from dataclasses import replace

import pytest

from omega_engine_pfp.infrastructure.serialization import domain_digest, thaw
from omega_engine.crates.operator.projector.proj_symbol_game import TerminalStatus
from omega_engine.crates.engine.eng_symbol_game import OesosLab
from omega_engine_pfp.infrastructure.adapters.research_solvers import (
    AIRY_OBSTRUCTION_ID,
    AIRY_SOLVER_ID,
    AiryCriticalStateV1,
    AiryNewtonProposalSolver,
    ComplexScalarV1,
    build_airy_problem,
)


PARENT_ID = "1" * 64
SOURCE_DIGEST = "2" * 64


def _problem():
    return build_airy_problem(
        research_parent_event_id=PARENT_ID,
        source_digest=SOURCE_DIGEST,
    )


def test_complex_scalar_roundtrips_only_normalized_finite_float_hex() -> None:
    scalar = ComplexScalarV1.from_complex(complex(-0.0, 1.25))

    assert scalar.real_hex == (-0.0).hex()
    assert scalar.imag_hex == (1.25).hex()
    assert scalar.to_complex() == complex(-0.0, 1.25)

    with pytest.raises(ValueError, match="normalized"):
        ComplexScalarV1(" 0x0.0p+0", (0.0).hex())
    with pytest.raises(ValueError, match="finite"):
        ComplexScalarV1("inf", (0.0).hex())
    with pytest.raises(TypeError, match="exact complex"):
        ComplexScalarV1.from_complex(1.0)  # type: ignore[arg-type]


def test_airy_problem_strictly_binds_source_parent_and_fixed_carrier() -> None:
    problem = _problem()
    envelope = problem.envelope

    assert envelope.parent_event_id == PARENT_ID
    assert envelope.source_digest == SOURCE_DIGEST
    assert envelope.packet_family == "witten_airy_critical"
    assert envelope.allowed_transforms == ("same_carrier_retraction",)
    assert envelope.protected_boundaries == (AIRY_OBSTRUCTION_ID,)
    assert envelope.initial_state_hash == domain_digest(
        "omega.oesos.native-state.v1",
        problem.native_initial_state,
    )
    assert problem.projector.validate_packet(envelope, problem.native_initial_state)
    assert problem.native_initial_state.slot_ids == problem.projector.carrier.slot_ids
    assert len(problem.native_initial_state.slots) == 5

    wrong_parent = replace(envelope, parent_event_id="3" * 64)
    wrong_source = replace(envelope, source_digest="4" * 64)
    assert not problem.projector.validate_packet(
        wrong_parent,
        problem.native_initial_state,
    )
    assert not problem.projector.validate_packet(
        wrong_source,
        problem.native_initial_state,
    )


def test_airy_oesos_run_is_exact_replay_valid_and_stable() -> None:
    problem = _problem()
    engine = OesosLab((AiryNewtonProposalSolver(),))

    first = engine.solve(problem)
    second = engine.solve(problem)

    assert first.terminal_status is TerminalStatus.LAB_EXACT_CANDIDATE
    assert first.locally_resolved
    assert first.evidence_valid()
    assert first.accepted_steps == 1
    assert first.final_projection.is_exact
    assert first.event_root == second.event_root
    assert second.evidence_valid()
    assert len(first.candidate_artifacts) == 1

    final_state = first.final_native_state
    assert type(final_state) is AiryCriticalStateV1
    assert final_state.slot_ids == problem.native_initial_state.slot_ids
    assert len(final_state.slots) == 5
    roots = tuple(slot.value.to_complex() for slot in final_state.slots)
    assert set(roots) == {-1.0 + 0.0j, 1.0 + 0.0j}

    metadata = thaw(first.candidate_artifacts[0].metadata)
    assert metadata["all_slots_converged"] is True
    assert metadata["unique_root_count"] == 2
    assert metadata["duplicates_preserved_as_labeled_slots"] is True
    assert metadata["authority_effect"] == "None"


def test_airy_projector_controls_and_retraction_law_are_independent() -> None:
    problem = _problem()
    projector = problem.projector
    exact = problem.detector_cases[0].native_state
    obstructed = problem.detector_cases[1].native_state

    assert projector.project(exact).is_exact
    red = projector.project(obstructed)
    assert red.active_ids == (AIRY_OBSTRUCTION_ID,)
    assert red.obstructions[0].magnitude == abs(
        projector.carrier.lambda_scalar.to_complex()
    )
    assert projector.verify_retraction(
        AIRY_SOLVER_ID,
        problem.native_initial_state,
        exact,
    )
    assert not projector.verify_retraction(
        "untrusted-solver",
        problem.native_initial_state,
        exact,
    )
    assert not projector.verify_retraction(
        AIRY_SOLVER_ID,
        problem.native_initial_state,
        problem.native_initial_state,
    )
    assert not projector.verify_retraction(
        AIRY_SOLVER_ID,
        problem.native_initial_state,
        obstructed,
    )


@pytest.mark.parametrize(
    ("field", "value"),
    (("parent_event_id", "3" * 64), ("source_digest", "4" * 64)),
)
def test_airy_oesos_refuses_packet_binding_mutation(field: str, value: str) -> None:
    problem = _problem()
    forged = replace(problem, envelope=replace(problem.envelope, **{field: value}))

    run = OesosLab((AiryNewtonProposalSolver(),)).solve(forged)

    assert run.terminal_status is TerminalStatus.INVALID_PACKET
    assert "PACKET_RUNTIME_SEMANTICS_MISMATCH" in run.prime000.blockers
    assert not run.locally_resolved


def test_airy_solver_refuses_a_zero_derivative_seed_without_laundering() -> None:
    problem = build_airy_problem(
        seeds=(0.0j, 0.5 + 0.5j, -0.5 - 0.5j, 2.0 + 0.1j, -2.0 + 0.3j),
        research_parent_event_id=PARENT_ID,
        source_digest=SOURCE_DIGEST,
    )

    run = OesosLab((AiryNewtonProposalSolver(),)).solve(problem)

    assert not run.locally_resolved
    assert run.accepted_steps == 0
    assert run.attempts[0].reason == "no-proposal"
    assert run.active_obstructions == (AIRY_OBSTRUCTION_ID,)


