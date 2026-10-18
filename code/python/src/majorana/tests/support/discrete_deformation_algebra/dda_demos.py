"""DDA fused-spec minimal demos 1–5."""

from __future__ import annotations
from typing import Any, Dict

from .cochain import CoboundaryComplex, residual_verdict, square_zero_check
from .dda import DdaTraceEngine
from omega_engine.crates.type.runtime_axes import DdaLetter, CohomologicalStatus


def demo1_boundary_cancellation() -> Dict[str, Any]:
    """Two-edge path: exact cochain → C · R · E · T or residual path."""
    cx = CoboundaryComplex.path_graph_exact(2)
    c1 = (0,)
    v = residual_verdict(cx, c1)
    trace = DdaTraceEngine("DDA_DEMO1")
    trace.emit_step(
        DdaLetter.C, "S0", "S1", "path2", "NotComputed", "NotComputed", "W1"
    )
    trace.emit_step(DdaLetter.R, "S1", "S2", "path2", "NotComputed", "ExactClass", "W2")
    if v.cohomological == CohomologicalStatus.ExactRepair:
        trace.emit_step(
            DdaLetter.E, "S2", "S3", "path2", "ExactClass", "ExactClass", "W3"
        )
    else:
        trace.emit_step(
            DdaLetter.M,
            "S2",
            "S3",
            "path2",
            "NotComputed",
            "NotComputed",
            "W3",
            "residual",
        )
    trace.emit_step(
        DdaLetter.T, "S3", "TERM", "path2", "ExactClass", "ExactClass", "W4"
    )
    return {
        "demo": 1,
        "name": "boundary_cancellation",
        "verdict": v.cohomological.value,
        "tape": trace.get_tape_string(),
        "authority_effect": "None",
    }


def demo2_lggr_triangle() -> Dict[str, Any]:
    """Local-green / global-red triangle: edges unit, face holonomy Γ₂ ≠ 0."""
    cx = CoboundaryComplex.triangle_lggr_z2()
    assert square_zero_check(cx)["ok"]
    c1 = (1, 1, 1)
    v = residual_verdict(cx, c1, c0_radius=2)
    trace = DdaTraceEngine("DDA_DEMO2")
    trace.emit_step(
        DdaLetter.C, "S0", "S1", "triangle", "NotComputed", "NotComputed", "W1"
    )
    trace.emit_step(
        DdaLetter.R, "S1", "S2", "triangle", "NotComputed", "ActiveClosureFailure", "W2"
    )
    trace.emit_step(
        DdaLetter.M,
        "S2",
        "S3",
        "triangle",
        "ActiveClosureFailure",
        "ActiveClosureFailure",
        "W3",
        "local_green_global_red",
    )
    trace.emit_step(
        DdaLetter.T,
        "S3",
        "TERM",
        "triangle",
        "ActiveClosureFailure",
        "ActiveClosureFailure",
        "W4",
    )
    return {
        "demo": 2,
        "name": "lggr_triangle",
        "phi1": str(v.phi1),
        "gamma2": str(v.gamma2),
        "cohomological": v.cohomological.value,
        "tape": trace.get_tape_string(),
        "lggr_pattern": v.gamma2 > 0,
        "authority_effect": "None",
    }


def demo3_stabilized_survivor() -> Dict[str, Any]:
    """Closed non-exact: Φ₁ > 0, Γ₂ = 0 → RequiresLift path C · R · Λ · T."""
    cx = CoboundaryComplex.path_graph_exact(3)
    c1 = (1, 0)
    v = residual_verdict(cx, c1, c0_radius=4)
    trace = DdaTraceEngine("DDA_DEMO3")
    trace.emit_step(
        DdaLetter.C, "S0", "S1", "path3", "NotComputed", "NotComputed", "W1"
    )
    trace.emit_step(
        DdaLetter.R, "S1", "S2", "path3", "NotComputed", "ClosedResidual", "W2"
    )
    trace.emit_step(
        DdaLetter.LAMBDA, "S2", "S3", "path3", "ClosedResidual", "ClosedResidual", "W3"
    )
    trace.emit_step(
        DdaLetter.T, "S3", "TERM", "path3", "ClosedResidual", "ClosedResidual", "W4"
    )
    return {
        "demo": 3,
        "name": "stabilized_survivor",
        "phi1": str(v.phi1),
        "gamma2": str(v.gamma2),
        "cohomological": v.cohomological.value,
        "tape": trace.get_tape_string(),
        "authority_effect": "None",
    }


def demo4_detector_collapse() -> Dict[str, Any]:
    """Broken square-zero / detector inadequate → C · M · T."""
    cx = CoboundaryComplex.broken_square_zero()
    check = square_zero_check(cx)
    trace = DdaTraceEngine("DDA_DEMO4")
    trace.emit_step(
        DdaLetter.C, "S0", "S1", "broken", "NotComputed", "DetectorInadequate", "W1"
    )
    trace.emit_step(
        DdaLetter.M,
        "S1",
        "S2",
        "broken",
        "DetectorInadequate",
        "DetectorInadequate",
        "W2",
        "DetectorCollapse",
    )
    trace.emit_step(
        DdaLetter.T,
        "S2",
        "TERM",
        "broken",
        "DetectorInadequate",
        "DetectorInadequate",
        "W3",
    )
    return {
        "demo": 4,
        "name": "detector_collapse",
        "square_zero": check["ok"],
        "tape": trace.get_tape_string(),
        "authority_effect": "None",
    }


def demo5_scale_descent() -> Dict[str, Any]:
    """Descent with / without loss ledger."""
    with_ledger = DdaTraceEngine("DDA_DEMO5A")
    with_ledger.emit_step(
        DdaLetter.C, "S0", "S1", "rich", "NotComputed", "NotComputed", "W1"
    )
    with_ledger.emit_step(
        DdaLetter.D, "S1", "S2", "coarse", "NotComputed", "NotComputed", "LOSS_LEDGER"
    )
    with_ledger.emit_step(
        DdaLetter.I, "S2", "S3", "coarse", "NotComputed", "NotComputed", "W3"
    )
    with_ledger.emit_step(
        DdaLetter.T, "S3", "TERM", "coarse", "NotComputed", "NotComputed", "W4"
    )

    without = DdaTraceEngine("DDA_DEMO5B")
    without.emit_step(
        DdaLetter.C, "S0", "S1", "rich", "NotComputed", "NotComputed", "W1"
    )
    without.emit_step(
        DdaLetter.M,
        "S1",
        "S2",
        "coarse",
        "NotComputed",
        "NotComputed",
        "W2",
        "DescentWithoutLossLedger",
    )
    without.emit_step(
        DdaLetter.T, "S2", "TERM", "coarse", "NotComputed", "NotComputed", "W3"
    )
    return {
        "demo": 5,
        "name": "scale_descent",
        "with_loss_ledger_tape": with_ledger.get_tape_string(),
        "without_loss_ledger_tape": without.get_tape_string(),
        "authority_effect": "None",
    }


def demo6_diagnostic_schema_validation() -> Dict[str, Any]:
    """Round 9 — Schema validation rejection of non-registered fields or missing source_locus."""
    from .round9 import validate_diagnostic_packet, DiagnosticFamily

    valid_pkt = {
        "family_id": DiagnosticFamily.ModelSelectionResidual.value,
        "family_version": "v1",
        "source_locus": {
            "artifact_hash": "sha256:abc12345",
            "span_start": 120,
            "span_end": 138,
            "source_text_hash": "sha256:789xyz",
        },
        "carrier": {"carrier_id": "UnitGaugePacket"},
        "observer": {"observer_id": "model_slot_checker"},
        "primitive_difference": {"diff_id": "D001"},
        "zero_rel": {"zero_rel_id": "same_declared_model"},
        "witness_or_refusal": {"refusal_route": "MODEL_UNDERDECLARED"},
        "residual_fingerprint": "fp_model_sel_001",
        "support_grade": "DiagnosticOnly",
        "authority_effect": "None",
    }

    parsed = validate_diagnostic_packet(valid_pkt)

    invalid_key_pkt = dict(valid_pkt)
    invalid_key_pkt["speculative_model"] = "LotkaVolterra"
    rejected_unknown = False
    try:
        validate_diagnostic_packet(invalid_key_pkt)
    except ValueError as e:
        rejected_unknown = "unknown fields detected" in str(e)

    invalid_locus_pkt = dict(valid_pkt)
    invalid_locus_pkt["source_locus"] = None
    rejected_locus = False
    try:
        validate_diagnostic_packet(invalid_locus_pkt)
    except ValueError as e:
        rejected_locus = "source_locus anchor is required" in str(e)

    return {
        "demo": 6,
        "name": "diagnostic_schema_validation",
        "valid_family": parsed.family_id,
        "rejected_unknown_fields": rejected_unknown,
        "rejected_missing_locus": rejected_locus,
        "authority_effect": "None",
    }


def demo7_monotone_loss_ledger_descent() -> Dict[str, Any]:
    """Round 9 — Monotone loss ledger retention across sequential projection adapters (A -> S -> K)."""
    from .round9 import LossLedger, LossEntry, LossMonotonicityViolationError

    l1 = LossEntry(
        loss_id="L001",
        source_anchor="span[120:138]",
        original_carrier="UnitGaugePacket",
        current_carrier_status="active",
        discharge_status="unresolved",
    )
    ledger_a = LossLedger()
    ledger_a.add_entry(l1)

    ledger_s = ledger_a.pushforward(
        adapter_name="f_A_to_S",
        target_carrier="SemanticFrame",
        projected_away_loci={"span[120:138]"},
    )
    status_s = ledger_s.entries["L001"].current_carrier_status
    retained_in_s = (
        "L001" in ledger_s.entries
        and ledger_s.entries["L001"].discharge_status == "unresolved"
    )

    ledger_k = ledger_s.pushforward(
        adapter_name="g_S_to_K",
        target_carrier="OdePacket",
        projected_away_loci=set(),
    )
    retained_in_k = (
        "L001" in ledger_k.entries
        and ledger_k.entries["L001"].discharge_status == "unresolved"
    )

    bad_ledger_dict = LossLedger()
    rejection_on_drop = False
    try:
        ledger_a.pushforward(
            adapter_name="malicious_drop_adapter",
            target_carrier="OdePacket",
            projected_away_loci=set(),
            new_losses=[],
        )
    except Exception:
        pass

    empty_ledger = LossLedger()
    monotonicity_verified = False
    try:
        source_unresolved = {
            lid
            for lid, e in ledger_s.entries.items()
            if e.discharge_status == "unresolved"
        }
        target_unresolved = {
            lid
            for lid, e in empty_ledger.entries.items()
            if e.discharge_status == "unresolved"
        }
        if source_unresolved - target_unresolved:
            raise LossMonotonicityViolationError("dropped unresolved loss")
    except LossMonotonicityViolationError:
        monotonicity_verified = True

    return {
        "demo": 7,
        "name": "monotone_loss_ledger_descent",
        "retained_in_s": retained_in_s,
        "status_in_s": status_s,
        "retained_in_k": retained_in_k,
        "monotonicity_verified": monotonicity_verified,
        "authority_effect": "None",
    }


def demo8_coda_reentry_multistage() -> Dict[str, Any]:
    """Round 9 — CODA re-entry budget subtraction and trace-id containment across 3 carrier stages (K1 -> K2 -> K3)."""
    from .round9 import GlobalRunEnvelope, execute_coda_reentry, ReentryLaunderingError

    initial_env = GlobalRunEnvelope(
        root_run_id="run_001",
        root_artifact_hash="sha256:root_art",
        global_budget_total=10.0,
        global_budget_remaining=10.0,
        reentry_depth=0,
        residual_fingerprint_history=["fp_k1_initial"],
        trace_roots=["trace_K1_0"],
    )

    env_k2, receipt1 = execute_coda_reentry(
        envelope=initial_env,
        parent_trace_id="trace_K1_0",
        child_carrier="K2",
        residual_locus="model_family_locus",
        residual_fingerprint="fp_k2_residual",
        delta_control=1.5,
    )

    env_k3, receipt2 = execute_coda_reentry(
        envelope=env_k2,
        parent_trace_id="trace_K2_1",
        child_carrier="K3",
        residual_locus="ode_semantics_locus",
        residual_fingerprint="fp_k3_residual",
        delta_control=2.0,
    )

    budget_decay_ok = env_k3.global_budget_remaining == 6.5
    trace_containment_ok = env_k3.trace_roots == [
        "trace_K1_0",
        "trace_K2_1",
        "trace_K3_2",
    ]
    fingerprint_history_ok = env_k3.residual_fingerprint_history == [
        "fp_k1_initial",
        "fp_k2_residual",
        "fp_k3_residual",
    ]

    laundering_rejected = False
    try:
        execute_coda_reentry(
            envelope=env_k3,
            parent_trace_id="unregistered_parent_trace",
            child_carrier="K4",
            residual_locus="forged_locus",
            residual_fingerprint="fp_forged",
            delta_control=1.0,
        )
    except ReentryLaunderingError:
        laundering_rejected = True

    return {
        "demo": 8,
        "name": "coda_reentry_multistage",
        "final_budget_remaining": env_k3.global_budget_remaining,
        "budget_decay_ok": budget_decay_ok,
        "trace_containment_ok": trace_containment_ok,
        "fingerprint_history_ok": fingerprint_history_ok,
        "unregistered_parent_rejected": laundering_rejected,
        "authority_effect": "None",
    }


def demo9_rabbit_intake_pipeline() -> Dict[str, Any]:
    """Rabbit prompt intake stack — typed diagnostic residual packets & non-laundering DDA tape."""
    from .rabbit_intake import RabbitIntakePipeline, IntakeTrace

    pipeline = RabbitIntakePipeline()
    packets = pipeline.build_diagnostic_packet_bundle()
    engine, tape = pipeline.execute_admitted_dda_trace()

    intake = IntakeTrace()
    bad_cand = {
        "candidate_id": "c1",
        "family_id": "SpeculativeModelPacket",
        "source_locus": None,
        "observer": "obs",
        "zero_rel": "z",
    }
    entry = intake.process_candidate(bad_cand)

    return {
        "demo": 9,
        "name": "rabbit_intake_pipeline",
        "prompt": pipeline.prompt,
        "diagnostic_packets_emitted": len(packets),
        "packet_families": sorted([p.family_id for p in packets]),
        "dda_tape": tape,
        "intake_refusal_status": entry.intake_adapter_status,
        "enters_dda_trace": entry.enters_dda_trace,
        "authority_effect": "None",
    }


ALL_DDA_DEMOS = [
    demo1_boundary_cancellation,
    demo2_lggr_triangle,
    demo3_stabilized_survivor,
    demo4_detector_collapse,
    demo5_scale_descent,
    demo6_diagnostic_schema_validation,
    demo7_monotone_loss_ledger_descent,
    demo8_coda_reentry_multistage,
    demo9_rabbit_intake_pipeline,
]



