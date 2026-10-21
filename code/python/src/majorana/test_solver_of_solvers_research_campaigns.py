"""End-to-end evidence test for the Witten/GR lettered-algebra campaign."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest
from omega_engine.crates.discrete_deformation_algebra import research_campaigns as campaign_module
from omega_engine.crates.discrete_deformation_algebra.research_campaigns import (
    run_gr_constraint_campaign,
    run_research_campaigns,
    run_symbol_game_coda_campaign,
)
from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_oesos import (
    CascadeSolver,
)

from omega_engine_pfp.domain import (
    SourceIntakeBundleV1,
    parse_research_claim_envelope,
    read_research_run_root,
    verify_research_run_root,
)
from omega_engine_pfp.domain.entities.oesos_evidence_bundle import (
    read_oesos_evidence_bundle,
    verify_oesos_evidence_bundle,
)
from omega_engine_pfp.domain.entities.packet_envelope import PacketEnvelopeV2


def test_standalone_coda_artifacts_are_content_addressed_across_no_host_rerun(
    tmp_path: Path,
) -> None:
    def wire(payload: dict[str, str]) -> SimpleNamespace:
        return SimpleNamespace(to_dict=lambda: payload)

    evaluation = SimpleNamespace(
        description=wire({"schema": "description", "revision": "one"}),
        carrier_manifest=wire({"schema": "manifest", "carrier": "one"}),
        request=wire({"schema": "request", "request_id": "one"}),
        outcome=wire({"schema": "outcome", "outcome_root": "one"}),
    )
    first = campaign_module._write_rust_host_artifacts(tmp_path, evaluation)
    first_paths = {label: Path(path) for label, path in first.items()}
    first_bytes = {label: path.read_bytes() for label, path in first_paths.items()}
    for path in first_paths.values():
        assert (
            path.stem.rsplit("_", 1)[-1]
            == hashlib.sha256(path.read_bytes()).hexdigest()
        )

    changed = SimpleNamespace(
        description=evaluation.description,
        carrier_manifest=evaluation.carrier_manifest,
        request=evaluation.request,
        outcome=wire({"schema": "outcome", "outcome_root": "two"}),
    )
    second = campaign_module._write_rust_host_artifacts(tmp_path, changed)
    assert second["description"] == first["description"]
    assert second["carrier_manifest"] == first["carrier_manifest"]
    assert second["request"] == first["request"]
    assert second["outcome"] != first["outcome"]

    for name in campaign_module._LEGACY_RUST_HOST_ARTIFACTS:
        (tmp_path / name).write_text("stale\n", encoding="utf-8")
    no_host = run_symbol_game_coda_campaign(tmp_path)

    assert no_host.status == "RUST_HOST_NOT_RUN_GLOBAL_REFUSAL"
    assert no_host.metrics["rust_host"] == {
        "status": "NOT_RUN",
        "authority_effect": "None",
    }
    assert all(
        not (tmp_path / name).exists()
        for name in campaign_module._LEGACY_RUST_HOST_ARTIFACTS
    )
    for label, path in first_paths.items():
        assert path.read_bytes() == first_bytes[label]


def test_deleted_rust_host_adapter_fails_closed(tmp_path: Path) -> None:
    outcome = run_symbol_game_coda_campaign(tmp_path, tmp_path / "not-executed")

    assert outcome.status == "RUST_HOST_CLIENT_REFUSED_GLOBAL_REFUSAL"
    assert outcome.metrics["rust_host"] == {
        "status": "CLIENT_REFUSED",
        "code": "RUST_HOST_ADAPTER_UNAVAILABLE",
        "detail": (
            "the legacy Rust Prime/OESOS adapter was deleted; "
            "external host execution remains disabled"
        ),
        "authority_effect": "None",
    }
    assert "RUST_HOST_CLIENT_REFUSED" in outcome.retained_obstructions
    assert "RUST_HOST_ADAPTER_UNAVAILABLE" in outcome.retained_obstructions


def test_research_campaign_emits_valid_closed_and_refused_tapes(tmp_path: Path) -> None:
    result = run_research_campaigns(tmp_path, CascadeSolver)
    outcomes = {outcome["name"]: outcome for outcome in result["outcomes"]}

    assert result["dag"]["total_runs"] == 7
    assert result["dag"]["valid_runs"] == 7
    assert result["dag"]["invalid_runs"] == 0
    assert result["dag"]["obstructions_removed_steps"] == 4
    assert result["dag"]["refusal_steps"] == 4
    assert result["dag"]["structure_built_steps"] == 1

    airy = outcomes["solver_of_solvers_witten_airy_finite"]
    assert airy["status"].startswith("FINITE_NUMERICAL_SHADOW_CLOSED")
    if not airy["metrics"]["source_artifact_present"]:
        assert airy["status"].endswith("_SOURCE_UNVERIFIED")
    assert airy["tape"] == ["R", "C", "E", "Lambda", "I", "T"]
    assert airy["residual_final"] == 0.0
    assert airy["metrics"]["real_cycle_check"]["matching_orientation_count"] == 1
    assert airy["metrics"]["oesos"]["locally_resolved"]
    assert airy["metrics"]["oesos"]["bridge_valid"]
    assert airy["metrics"]["oesos"]["tape"] == ["R", "C", "E", "I", "T"]

    gr = outcomes["solver_of_solvers_gr_constraint_closure"]
    assert gr["status"] == "FINITE_RESIDUAL_CLOSED"
    assert gr["tape"] == ["R", "C", "E", "I", "T"]
    assert gr["residual_initial"] == 19.0
    assert gr["residual_final"] == 0.0
    assert gr["metrics"]["execution_relation"] == "LIVE_PORT_EXECUTION"
    assert gr["metrics"]["initial_phi1"] == 7.0
    assert gr["metrics"]["initial_gamma2"] == 12.0
    assert gr["metrics"]["bridge_valid"]

    for refused_name in (
        "solver_of_solvers_witten_full_chern_simons",
        "solver_of_solvers_gr_stretch_claims",
    ):
        refused = outcomes[refused_name]
        assert refused["status"] == "REFUSED"
        assert refused["tape"] == ["R", "C", "Z", "T"]
        assert refused["residual_final"] == refused["residual_initial"]

    research_names = (
        "solver_of_solvers_witten_airy_finite",
        "solver_of_solvers_witten_full_chern_simons",
        "solver_of_solvers_gr_constraint_closure",
        "solver_of_solvers_gr_stretch_claims",
    )
    research_packet_ids = {}
    for name in research_names:
        outcome = outcomes[name]
        packet_metrics = outcome["metrics"]["research_packet"]
        packet_path = Path(packet_metrics["packet_artifact"])
        intake_path = Path(packet_metrics["source_intake_artifact"])
        root_metrics = outcome["metrics"]["research_run_root"]
        root_path = Path(root_metrics["artifact"])
        assert packet_path.is_file()
        assert intake_path.is_file()
        assert root_path.is_file()
        for path in (packet_path, intake_path, root_path):
            assert (
                path.stem.rsplit("_", 1)[-1]
                == hashlib.sha256(path.read_bytes()).hexdigest()
            )

        packet = PacketEnvelopeV2.from_dict(json.loads(packet_path.read_text("utf-8")))
        payload = parse_research_claim_envelope(packet)
        intake = SourceIntakeBundleV1.from_dict(
            json.loads(intake_path.read_text("utf-8"))
        )
        run_root = read_research_run_root(root_path)
        assert packet.packet_id == packet_metrics["packet_id"]
        assert payload.family == packet_metrics["packet_family"]
        assert intake.packet_id == packet.packet_id
        assert intake.receipt_id == packet_metrics["source_intake_receipt_id"]
        assert run_root.claim_packet_id == packet.packet_id
        assert run_root.root_id == root_metrics["root_id"]
        assert verify_research_run_root(run_root, tmp_path)
        if name in {
            "solver_of_solvers_witten_airy_finite",
            "solver_of_solvers_gr_constraint_closure",
        }:
            bundle_metrics = root_metrics["oesos_evidence_bundle"]
            bundle_path = Path(bundle_metrics["artifact"])
            bundle = read_oesos_evidence_bundle(bundle_path)
            assert verify_oesos_evidence_bundle(
                bundle,
                expected_research_parent_packet_id=packet.packet_id,
            )
            assert bundle.bundle_id == bundle_metrics["bundle_id"]
            assert run_root.oesos_event_root == bundle.evaluation_receipt.event_root
            assert run_root.oesos_runtime_root == bundle.runtime_problem.runtime_id
            assert run_root.oesos_wire_root == bundle.wire_receipt_id
            assert run_root.oesos_bridge_root is None
        else:
            assert "oesos_evidence_bundle" not in root_metrics
            assert run_root.oesos_event_root is None
        research_packet_ids[name] = packet.packet_id

    assert len(set(research_packet_ids.values())) == 4
    assert (
        outcomes["solver_of_solvers_witten_airy_finite"]["metrics"]["oesos"][
            "parent_research_packet_id"
        ]
        == research_packet_ids["solver_of_solvers_witten_airy_finite"]
    )
    assert (
        outcomes["solver_of_solvers_gr_constraint_closure"]["metrics"][
            "parent_research_packet_id"
        ]
        == research_packet_ids["solver_of_solvers_gr_constraint_closure"]
    )

    symbol_game = outcomes["solver_of_solvers_symbol_game_coda"]
    assert symbol_game["status"] == "RUST_HOST_NOT_RUN_GLOBAL_REFUSAL"
    assert symbol_game["tape"] == ["R", "C", "E", "Z", "T"]
    assert symbol_game["metrics"]["bridge_valid"]
    assert symbol_game["metrics"]["prime000_shape_only"]["blockers"] == ()
    assert symbol_game["metrics"]["sealed_prime002_status"] == "NOT_RUN"
    assert symbol_game["metrics"]["rust_oesos_replay_status"] == "NOT_RUN"
    local_bridge = symbol_game["metrics"]["bridge"]["v2_bridge"]
    assert local_bridge["initial_raw_mass"] == 9.0
    assert local_bridge["initial_phi1"] == 7.0
    assert local_bridge["initial_gamma2"] == 12.0
    assert symbol_game["metrics"]["bridge"]["local_residual_metric"] == (
        "aggregate_obstruction_mass(phi1+gamma2)"
    )
    assert symbol_game["metrics"]["local_math_residual_initial"] == 19.0
    assert symbol_game["metrics"]["local_math_residual_final"] == 0.0
    assert symbol_game["residual_initial"] == 19.0
    assert symbol_game["residual_final"] == 0.0
    assert symbol_game["metrics"]["admission_residual_initial"] == 3
    assert symbol_game["metrics"]["admission_residual_final"] == 3
    assert symbol_game["metrics"]["admission_residual_metric"] == (
        "admission_obstruction_count"
    )
    assert "RUST_HOST_NOT_RUN" in symbol_game["retained_obstructions"]

    self_improvement = outcomes["solver_of_solvers_symbol_game_self_improvement"]
    assert self_improvement["status"] == (
        "SELF_IMPROVEMENT_PROPOSAL_PACKETIZED_GLOBAL_REFUSAL"
    )
    assert self_improvement["tape"] == ["R", "C", "E", "Z", "T"]
    assert self_improvement["metrics"]["strict_improvement"]
    assert self_improvement["metrics"]["non_regression_passed"]
    assert not self_improvement["metrics"]["applied_locally"]
    assert self_improvement["metrics"]["production_promotion"] == "NOT_AUTHORIZED"

    dag = json.loads((tmp_path / "dda_dag.json").read_text("utf-8"))
    assert dag["residual_reduction_comparison"] == "NOT_COMPARABLE_ACROSS_CARRIERS"
    assert dag["measured_residual_reduction"] is None
    assert len(dag["within_run_residual_reductions"]) == 7
    assert (tmp_path / "solver_of_solvers_report.md").exists()

    rerun = run_research_campaigns(tmp_path, CascadeSolver)
    assert rerun["dag"]["total_runs"] == 7
    assert rerun["dag"]["valid_runs"] == 7
    trace_paths = list(tmp_path.glob("*_dda_trace.jsonl"))
    assert len(trace_paths) == 10
    for trace_path in trace_paths:
        steps = [
            json.loads(line) for line in trace_path.read_text("utf-8").splitlines()
        ]
        assert all(
            steps[index - 1]["residual_after"] == steps[index]["residual_before"]
            for index in range(1, len(steps))
        )


def test_witten_outer_rail_refuses_an_unresolved_oesos_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = campaign_module.AiryNewtonProposalSolver().manifest

    class NoProposalAirySolver:
        def __init__(self) -> None:
            self.manifest = manifest

        def propose(self, _problem, _packet_state, _projection):
            return None

    monkeypatch.setattr(
        campaign_module,
        "AiryNewtonProposalSolver",
        NoProposalAirySolver,
    )

    outcome = campaign_module.run_witten_airy_finite_campaign(tmp_path)

    assert outcome.status == "REFUSED"
    assert outcome.tape == ["R", "C", "Z", "T"]
    assert "E" not in outcome.tape
    assert "Lambda" not in outcome.tape
    assert not outcome.metrics["oesos"]["locally_resolved"]
    assert "WITTEN_AIRY_OESOS_UNRESOLVED" in outcome.retained_obstructions


def test_witten_real_cycle_failure_has_nonzero_residual(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        campaign_module,
        "trace_thimble",
        lambda *_args, **_kwargs: SimpleNamespace(
            h_monotone_decreasing=True,
            max_im_drift=0.0,
        ),
    )
    monkeypatch.setattr(
        campaign_module,
        "_airy_real_cycle_check",
        lambda: {
            "lambda": "(1+0.25j)",
            "reference": "negative-control",
            "thimble_values": {},
            "best_orientation": [1, 1],
            "best_error": 0.0,
            "matching_orientation_count": 0,
            "tolerance": 2.0e-3,
        },
    )

    outcome = campaign_module.run_witten_airy_finite_campaign(tmp_path)

    assert outcome.status == "REFUSED"
    assert outcome.residual_final is not None
    assert outcome.residual_final >= 1.0
    assert outcome.metrics["real_cycle_defect"] >= 1.0


def test_live_rust_host_is_anchored_but_globally_refused(tmp_path: Path) -> None:
    executable = os.environ.get("OMEGA_PRIME_OESOS_HOST")
    if not executable:
        pytest.skip("OMEGA_PRIME_OESOS_HOST is not configured")

    outcome = run_symbol_game_coda_campaign(tmp_path, Path(executable))

    assert outcome.status == "RUST_REPLAYED_ADMISSION_REFUSED"
    assert outcome.tape == ["R", "C", "E", "Z", "T"]
    assert outcome.residual_initial == 19.0
    assert outcome.residual_final == 0.0
    assert (
        outcome.metrics["admission_residual_initial"]
        == outcome.metrics["admission_residual_final"]
        == outcome.metrics["admission_obstruction_count"]
    )
    assert outcome.metrics["bridge_valid"]
    assert outcome.metrics["bridge"]["rust_host_outcome_validated"]
    assert outcome.metrics["rust_oesos_replay_status"] == (
        "EXECUTED_REPLAYED_EXACT_LAB_EVIDENCE"
    )
    assert outcome.metrics["sealed_prime002_status"] == (
        "exact_step_written_then_terminalized"
    )
    assert outcome.metrics["rust_host"]["oesos"]["gauge"]["phi1"] == {
        "n": "7",
        "d": "1",
    }
    assert outcome.metrics["rust_host"]["oesos"]["final_stage"]["phi1"] == {
        "n": "0",
        "d": "1",
    }
    assert "PRIME000_CONFORMANCE_PARTIAL" in outcome.retained_obstructions
    assert "UNSIGNED_LAB_ATTESTATION" in outcome.retained_obstructions
    for path in outcome.metrics["rust_host"]["retained_artifacts"].values():
        assert Path(path).is_file()


def test_gr_campaign_refuses_when_non_phi1_residual_survives(tmp_path: Path) -> None:
    class ResidualTripleSolver:
        def __init__(self, _network, observer_name: str) -> None:
            self.observer_name = observer_name
            self.dda_engine = SimpleNamespace(step_history=[], lift_history=[])

        def solve(self, _omega, **_kwargs):
            return SimpleNamespace(
                initial_residual_size=1.0,
                carrier_nodes=4,
                carrier_edges=5,
                admitted_complex_verified=True,
                final_residual_triple=(0.0, 1.0, 0.0),
                terminal_status="Exact",
                is_certified=True,
                duality_gap=0.0,
                stages_executed=("Synthetic",),
                authority_effect="None",
            )

    outcome = run_gr_constraint_campaign(tmp_path, ResidualTripleSolver)
    assert outcome.status == "REFUSED"
    assert outcome.residual_final == 1.0
    assert outcome.tape == ["R", "C", "Z", "T"]
    assert "injected-test-rail" in Path(outcome.trace_path).name
    assert outcome.metrics["execution_relation"] == "INJECTED_TEST_RAIL_NOT_PRODUCTION"

    production_target = tmp_path / "production"
    with pytest.raises(TypeError, match="requires the canonical CascadeSolver"):
        run_research_campaigns(production_target, ResidualTripleSolver)
    assert not production_target.exists()

    packet_target = tmp_path / "packet-context"
    packet_target.mkdir()
    contexts = campaign_module._build_research_contexts(packet_target)
    with pytest.raises(TypeError, match="cannot consume a production research packet"):
        run_gr_constraint_campaign(
            packet_target,
            ResidualTripleSolver,
            contexts[campaign_module.GR_FINITE_FAMILY],
        )


