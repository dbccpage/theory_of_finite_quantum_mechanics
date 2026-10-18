"""Adversarial tests for the proposal-only Symbol Game to DDA bridge."""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from omega_engine.crates.discrete_deformation_algebra.symbol_game_bridge import (
    ADMISSION_RESIDUAL_METRIC,
    PRIME_EVIDENCE_LEVEL,
    RESIDUAL_METRIC,
    compute_rust_host_outcome_root,
    emit_symbol_game_dda_trace,
    emit_symbol_game_dda_trace_v3,
    verify_symbol_game_dda_bridge,
    verify_symbol_game_dda_bridge_v3,
)
from omega_engine.crates.solver.solv_coda_cascade_proposal import (
    CodaCascadeProposalSolver,
)
from omega_engine_pfp.use_cases.problem_builders.coda_problem import (
    build_coda_problem,
)
from omega_engine_pfp.fixtures import (
    ExhaustiveCspSolver,
    NoOpClaimingSolver,
    build_demo_problem,
)
from omega_engine.crates.engine.eng_symbol_game import (
    OesosLab,
    RunReceipt,
)


def _records(path: str) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in Path(path).read_text("utf-8").splitlines()
        if line.strip()
    ]


def _unsigned_partial_rust_outcome(
    run: RunReceipt,
    *,
    request_id: str,
    challenge: str,
) -> dict[str, object]:
    accepted = next(attempt for attempt in reversed(run.attempts) if attempt.accepted)
    assert accepted.candidate_id is not None
    assert accepted.candidate_state_hash is not None
    rational_zero = {"n": "0", "d": "1"}
    rational_three_halves = {"n": "3", "d": "2"}
    outcome: dict[str, object] = {
        "schema_version": "omega.oesos.rust-prime-host-outcome.v1",
        "request_id_sha256": request_id,
        "challenge_hex": challenge,
        "outcome_root_sha256": "",
        "host_registry_hash_sha256": "1" * 64,
        "host_source_revision": "test-rust-host-revision",
        "authority_effect": "None",
        "execution_status": "EXECUTED_REPLAYED_EXACT_LAB_EVIDENCE",
        "source_bindings": {
            "packet_id": {
                "supplied": run.packet_id,
                "derived": run.packet_id,
                "verdict": "MATCH",
            },
            "runtime_id_sha256": run.runtime_id,
            "runtime_id_verdict": (
                "BOUND_ONLY_RUNTIME_ARTIFACT_SCHEMA_NOT_YET_PUBLISHED"
            ),
            "candidate_id_sha256": accepted.candidate_id,
            "candidate_id_verdict": (
                "BOUND_ONLY_CANDIDATE_ARTIFACT_BYTES_NOT_SUPPLIED"
            ),
            "candidate_state_hash_sha256": accepted.candidate_state_hash,
            "candidate_state_verdict": (
                "BOUND_ONLY_PYTHON_IDENTITY;HOST_VECTOR_HASH_REPORTED_SEPARATELY"
            ),
            "source_event_root_sha256": run.event_root,
            "source_event_root_verdict": (
                "BOUND_ONLY_EVENT_BUNDLE_SCHEMA_NOT_YET_PUBLISHED"
            ),
            "source_wire_receipt_id_sha256": run.to_wire_receipt().receipt_id,
            "source_wire_receipt_verdict": (
                "BOUND_ONLY_SOURCE_RECEIPT_BYTES_NOT_SUPPLIED"
            ),
            "solver_registry_hash_sha256": run.solver_registry_hash,
            "solver_registry_verdict": (
                "BOUND_ONLY_SOURCE_REGISTRY_MANIFEST_NOT_SUPPLIED"
            ),
            "source_revision": "test-python-source-revision",
            "source_revision_verdict": "BOUND_ONLY_DISTINCT_SOURCE_REVISION",
        },
        "carrier_manifest": None,
        "prime001_result": None,
        "oesos_result": {
            "kind": "ExecutedExact",
            "input_commitment_sha256": "2" * 64,
            "fresh_solve_commitment_sha256": "3" * 64,
            "replay_commitment_sha256": "4" * 64,
            "pipeline_declaration_carrier_hash_blake3": "5" * 64,
            "gauge": {
                "status": "Optimal",
                "raw_weighted_l1": rational_three_halves,
                "phi1": rational_three_halves,
                "gamma2": rational_zero,
            },
            "final_stage": {
                "status": "Optimal",
                "raw_weighted_l1": rational_zero,
                "phi1": rational_zero,
                "gamma2": rational_zero,
            },
            "normal_form": [rational_zero],
            "b1_over_q": 0,
            "span_distance": rational_zero,
            "closure_premium": rational_zero,
            "candidate_relation": {
                "kind": "ExactMatch",
                "candidate_vector_sha256": "6" * 64,
                "normal_form_sha256": "7" * 64,
                "exact_match": True,
            },
        },
        "prime000_result": {
            "kind": "Prime000ShapeReplay",
            "receipt_commitment_sha256": "8" * 64,
            "terminal": "Partial",
            "evidence_provenance": "RustExactLabReplay",
            "letter_tape": "R.C.E.T",
            "phi1_u64": 0,
            "gamma2_u64": 0,
            "conformance": {
                "verdict": "Partial",
                "conforms": False,
                "no_decidable_violation": True,
                "violations": [],
                "unchecked_laws": ["P-000-L4"],
            },
        },
        "prime002_result": {
            "kind": "RustPrime002LabReceipt",
            "scope_commitments_sha256": ["9" * 64],
            "claim_commitments_sha256": ["a" * 64],
            "evidence_commitments_sha256": ["b" * 64],
            "permit_bindings_sha256": [],
            "rust_letters": ["R", "C", "M", "T"],
            "terminal_head_sha256": "c" * 64,
            "budget_before": {"max_ops": 100, "spent": 0},
            "budget_after": {"max_ops": 100, "spent": 7},
            "refusal_laws": ["UNSIGNED_LAB_ATTESTATION"],
            "evidence_caveat": "unsigned laboratory evidence",
        },
        "diagnostic_kind": None,
        "admission": {
            "kind": "Refused",
            "codes": [
                "UNSIGNED_LAB_ATTESTATION",
                "PRIME000_CONFORMANCE_PARTIAL",
            ],
            "reason_commitment_sha256": "d" * 64,
        },
        "attestation": "unsigned_lab",
        "refusal": None,
    }
    outcome["outcome_root_sha256"] = compute_rust_host_outcome_root(outcome)
    return outcome


def test_success_keeps_candidate_refusal_nested_and_emits_outer_success(
    tmp_path: Path,
) -> None:
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(
        build_demo_problem(task_id="bridge-success")
    )

    bridge = emit_symbol_game_dda_trace(
        run,
        trace_dir=tmp_path,
        runner_id="symbol-game-bridge-success",
        campaign_name="Symbol Game bridge success",
    )

    assert bridge.dda_tape == ("R", "C", "E", "I", "T")
    assert "M" in bridge.source_process_tape
    assert "Z" not in bridge.dda_tape
    assert bridge.final_residual == 0.0
    assert bridge.prime_evidence_level == PRIME_EVIDENCE_LEVEL
    assert bridge.sealed_prime002_status == "NOT_RUN"
    assert bridge.rust_oesos_replay_status == "NOT_RUN"
    assert verify_symbol_game_dda_bridge(run, bridge)

    records = _records(bridge.dda_trace_path)
    source = records[0]["evidence"]
    assert isinstance(source, dict)
    assert "M" in source["source_process_tape"]
    assert source["sealed_prime002_status"] == "NOT_RUN"
    assert records[2]["effect"] == "obstruction_eliminated"
    assert records[2]["residual_delta"] < 0.0


def test_unresolved_run_becomes_z_t_and_retains_residual(tmp_path: Path) -> None:
    run = OesosLab((NoOpClaimingSolver(),)).solve(
        build_demo_problem(task_id="bridge-refusal")
    )

    bridge = emit_symbol_game_dda_trace(
        run,
        trace_dir=tmp_path,
        runner_id="symbol-game-bridge-refusal",
        campaign_name="Symbol Game bridge refusal",
    )

    assert bridge.dda_tape == ("R", "C", "Z", "T")
    assert bridge.initial_residual == bridge.final_residual
    assert not bridge.locally_resolved
    assert verify_symbol_game_dda_bridge(run, bridge)

    records = _records(bridge.dda_trace_path)
    refusal = records[-2]
    assert refusal["effect"] == "refusal"
    assert refusal["residual_before"] == refusal["residual_after"]
    assert refusal["residual_delta"] == 0.0


def test_bridge_refuses_a_forged_source_or_anchor(tmp_path: Path) -> None:
    run = OesosLab((ExhaustiveCspSolver(),)).solve(
        build_demo_problem(task_id="bridge-forgery")
    )
    bridge = emit_symbol_game_dda_trace(
        run,
        trace_dir=tmp_path,
        runner_id="symbol-game-bridge-forgery",
        campaign_name="Symbol Game bridge forgery control",
    )

    forged_source = replace(run, event_root="0" * 64)
    with pytest.raises(ValueError, match="does not reconcile"):
        emit_symbol_game_dda_trace(
            forged_source,
            trace_dir=tmp_path,
            runner_id="forged-source",
            campaign_name="forged source",
        )
    assert not verify_symbol_game_dda_bridge(
        run,
        replace(bridge, bridge_root="f" * 64),
    )


def test_projection_keeps_raw_mass_phi1_gamma2_and_aggregate_distinct() -> None:
    problem = build_coda_problem(task_id="phi1-gamma2-separation")
    projection = problem.projector.project(problem.native_initial_state)
    by_id = {
        obstruction.obstruction_id: obstruction
        for obstruction in projection.obstructions
    }

    assert projection.phi1 == pytest.approx(by_id["cochain:phi1"].magnitude)
    assert projection.gamma2 == pytest.approx(by_id["cochain:gamma2"].magnitude)
    assert projection.raw_mass == pytest.approx(9.0)
    assert projection.obstruction_mass == pytest.approx(
        projection.phi1 + projection.gamma2
    )
    assert projection.raw_mass != pytest.approx(projection.obstruction_mass)


def test_bridge_binds_each_residual_axis_and_labels_the_outer_scalar(
    tmp_path: Path,
) -> None:
    run = OesosLab((CodaCascadeProposalSolver(),)).solve(
        build_coda_problem(task_id="bridge-residual-axes")
    )
    bridge = emit_symbol_game_dda_trace(
        run,
        trace_dir=tmp_path,
        runner_id="symbol-game-bridge-residual-axes",
        campaign_name="Symbol Game residual-axis bridge",
    )

    assert bridge.residual_metric == RESIDUAL_METRIC
    assert bridge.initial_raw_mass == pytest.approx(9.0)
    assert bridge.initial_phi1 == pytest.approx(7.0)
    assert bridge.initial_gamma2 == pytest.approx(12.0)
    assert bridge.initial_residual == pytest.approx(19.0)
    assert bridge.initial_residual != pytest.approx(bridge.initial_raw_mass)
    assert bridge.final_raw_mass == pytest.approx(0.0)
    assert bridge.final_phi1 == pytest.approx(0.0)
    assert bridge.final_gamma2 == pytest.approx(0.0)
    assert verify_symbol_game_dda_bridge(run, bridge)


def test_v3_without_host_keeps_local_e_but_refuses_global_admission(
    tmp_path: Path,
) -> None:
    run = OesosLab((ExhaustiveCspSolver(),)).solve(
        build_demo_problem(task_id="bridge-v3-no-host")
    )

    bridge = emit_symbol_game_dda_trace_v3(
        run,
        trace_dir=tmp_path,
        runner_id="symbol-game-bridge-v3-no-host",
        campaign_name="Symbol Game v3 absent-host refusal",
        additional_admission_codes=("RUST_HOST_CLIENT_REFUSED",),
    )

    assert bridge.dda_tape == ("R", "C", "E", "Z", "T")
    assert bridge.global_admission == "Refused"
    assert bridge.admission_obstruction_count == len(bridge.admission_codes)
    assert bridge.admission_obstruction_count > 0
    assert bridge.admission_residual_metric == ADMISSION_RESIDUAL_METRIC
    assert "RUST_HOST_CLIENT_REFUSED" in bridge.admission_codes
    assert bridge.local_residual_metric == RESIDUAL_METRIC
    assert bridge.local_initial_residual > bridge.local_final_residual
    assert bridge.rust_host_outcome_root is None
    assert not bridge.rust_host_outcome_validated
    assert verify_symbol_game_dda_bridge(run, bridge.v2_bridge)
    assert verify_symbol_game_dda_bridge_v3(
        run,
        bridge,
        additional_admission_codes=("RUST_HOST_CLIENT_REFUSED",),
    )
    assert not verify_symbol_game_dda_bridge_v3(run, bridge)

    records = _records(bridge.dda_trace_path)
    elimination = records[2]
    refusal = records[3]
    assert elimination["letter"] == "E"
    assert elimination["evidence"]["residual_metric"] == RESIDUAL_METRIC
    assert elimination["residual_before"] > elimination["residual_after"]
    assert refusal["letter"] == "Z"
    assert refusal["evidence"]["residual_metric"] == RESIDUAL_METRIC
    assert (
        refusal["evidence"]["admission_residual_metric"]
        == ADMISSION_RESIDUAL_METRIC
    )
    assert refusal["residual_before"] == bridge.local_final_residual
    assert refusal["residual_after"] == bridge.local_final_residual
    assert refusal["evidence"]["admission_obstruction_count"] == len(
        bridge.admission_codes
    )
    assert tuple(refusal["evidence"]["admission_codes"]) == bridge.admission_codes
    assert all(
        previous["residual_after"] == current["residual_before"]
        for previous, current in zip(records, records[1:])
    )


def test_v3_validates_unsigned_rust_outcome_and_keeps_exact_axes_nested(
    tmp_path: Path,
) -> None:
    run = OesosLab((ExhaustiveCspSolver(),)).solve(
        build_demo_problem(task_id="bridge-v3-rust-outcome")
    )
    request_id = "e" * 64
    challenge = "f" * 64
    outcome = _unsigned_partial_rust_outcome(
        run,
        request_id=request_id,
        challenge=challenge,
    )

    bridge = emit_symbol_game_dda_trace_v3(
        run,
        trace_dir=tmp_path,
        runner_id="symbol-game-bridge-v3-rust",
        campaign_name="Symbol Game v3 Rust-host refusal",
        rust_host_outcome=outcome,
        expected_host_request_id_sha256=request_id,
        expected_host_challenge_hex=challenge,
    )

    assert bridge.dda_tape == ("R", "C", "E", "Z", "T")
    assert bridge.global_admission == "Refused"
    assert bridge.rust_host_outcome_validated
    assert bridge.rust_host_outcome_root == outcome["outcome_root_sha256"]
    assert "UNSIGNED_LAB_ATTESTATION" in bridge.admission_codes
    assert "PRIME000_CONFORMANCE_PARTIAL" in bridge.admission_codes
    assert "RUST_HOST_RUNTIME_ID_BOUND_ONLY" in bridge.admission_codes
    assert "RUST_HOST_CANDIDATE_ID_BOUND_ONLY" in bridge.admission_codes
    assert "RUST_HOST_CANDIDATE_STATE_BOUND_ONLY" in bridge.admission_codes
    assert "RUST_HOST_SOURCE_EVENT_ROOT_BOUND_ONLY" in bridge.admission_codes
    assert "RUST_HOST_WIRE_RECEIPT_BOUND_ONLY" in bridge.admission_codes
    assert "RUST_HOST_SOLVER_REGISTRY_BOUND_ONLY" in bridge.admission_codes
    assert "RUST_HOST_SOURCE_REVISION_BOUND_ONLY" in bridge.admission_codes
    assert verify_symbol_game_dda_bridge_v3(
        run,
        bridge,
        rust_host_outcome=outcome,
        expected_host_request_id_sha256=request_id,
        expected_host_challenge_hex=challenge,
    )
    assert not verify_symbol_game_dda_bridge_v3(run, bridge)

    records = _records(bridge.dda_trace_path)
    elimination_evidence = records[2]["evidence"]
    refusal_evidence = records[3]["evidence"]
    assert elimination_evidence["rust_exact_axes"]["gauge"]["phi1"] == {
        "n": "3",
        "d": "2",
    }
    assert refusal_evidence["rust_exact_axes"]["gauge"]["phi1"] == {
        "n": "3",
        "d": "2",
    }
    assert refusal_evidence["rust_canonical_letters"] == ["R", "C", "M", "T"]
    assert refusal_evidence["residual_metric"] == RESIDUAL_METRIC
    assert (
        refusal_evidence["admission_residual_metric"]
        == ADMISSION_RESIDUAL_METRIC
    )
    assert refusal_evidence["admission_obstruction_count"] == len(
        bridge.admission_codes
    )
    assert tuple(refusal_evidence["admission_codes"]) == bridge.admission_codes
    assert all(
        previous["residual_after"] == current["residual_before"]
        for previous, current in zip(records, records[1:])
    )
    assert refusal_evidence["rust_source_binding_verdicts"] == {
        "packet_id": "MATCH",
        "runtime_id_verdict": (
            "BOUND_ONLY_RUNTIME_ARTIFACT_SCHEMA_NOT_YET_PUBLISHED"
        ),
        "candidate_id_verdict": (
            "BOUND_ONLY_CANDIDATE_ARTIFACT_BYTES_NOT_SUPPLIED"
        ),
        "candidate_state_verdict": (
            "BOUND_ONLY_PYTHON_IDENTITY;HOST_VECTOR_HASH_REPORTED_SEPARATELY"
        ),
        "source_event_root_verdict": (
            "BOUND_ONLY_EVENT_BUNDLE_SCHEMA_NOT_YET_PUBLISHED"
        ),
        "source_wire_receipt_verdict": (
            "BOUND_ONLY_SOURCE_RECEIPT_BYTES_NOT_SUPPLIED"
        ),
        "solver_registry_verdict": (
            "BOUND_ONLY_SOURCE_REGISTRY_MANIFEST_NOT_SUPPLIED"
        ),
        "source_revision_verdict": "BOUND_ONLY_DISTINCT_SOURCE_REVISION",
    }
    assert "Z" not in refusal_evidence["rust_canonical_letters"]
    assert refusal_evidence["rust_letters_projected_to_outer_tape"] is False


def test_v3_rejects_forged_rust_root_request_and_candidate(tmp_path: Path) -> None:
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(
        build_demo_problem(task_id="bridge-v3-forged-rust")
    )
    request_id = "1" * 64
    challenge = "2" * 64
    outcome = _unsigned_partial_rust_outcome(
        run,
        request_id=request_id,
        challenge=challenge,
    )
    forged = dict(outcome)
    forged["outcome_root_sha256"] = "0" * 64

    with pytest.raises(ValueError, match="outcome root does not reconcile"):
        emit_symbol_game_dda_trace_v3(
            run,
            trace_dir=tmp_path,
            runner_id="symbol-game-bridge-v3-forged-root",
            campaign_name="Symbol Game v3 forged Rust root",
            rust_host_outcome=forged,
            expected_host_request_id_sha256=request_id,
            expected_host_challenge_hex=challenge,
        )
    with pytest.raises(ValueError, match="expected request"):
        emit_symbol_game_dda_trace_v3(
            run,
            trace_dir=tmp_path,
            runner_id="symbol-game-bridge-v3-forged-request",
            campaign_name="Symbol Game v3 forged request binding",
            rust_host_outcome=outcome,
            expected_host_request_id_sha256="3" * 64,
            expected_host_challenge_hex=challenge,
        )

    rejected = next(
        attempt
        for attempt in run.attempts
        if not attempt.accepted
        and attempt.candidate_id is not None
        and attempt.candidate_state_hash is not None
    )
    rejected_binding = json.loads(json.dumps(outcome))
    rejected_binding["source_bindings"]["candidate_id_sha256"] = (
        rejected.candidate_id
    )
    rejected_binding["source_bindings"]["candidate_state_hash_sha256"] = (
        rejected.candidate_state_hash
    )
    rejected_binding["outcome_root_sha256"] = compute_rust_host_outcome_root(
        rejected_binding
    )
    with pytest.raises(ValueError, match="final accepted artifact"):
        emit_symbol_game_dda_trace_v3(
            run,
            trace_dir=tmp_path,
            runner_id="symbol-game-bridge-v3-rejected-candidate",
            campaign_name="Symbol Game v3 rejected Rust candidate",
            rust_host_outcome=rejected_binding,
            expected_host_request_id_sha256=request_id,
            expected_host_challenge_hex=challenge,
        )


