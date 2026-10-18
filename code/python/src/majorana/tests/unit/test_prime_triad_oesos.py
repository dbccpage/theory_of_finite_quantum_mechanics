"""Prime triad (OE-000) + OESOS object set tests. AuthorityEffect: None."""

from __future__ import annotations

from omega_engine.crates.prime import (
    AdmissionKind,
    AntiCheatFlags,
    CanContinueInput,
    CandidatePacket,
    DeclarationPacket,
    IntakeTrace,
    IntakeTraceRecord,
    admit_declaration,
    can_continue,
    check_adapter,
    propose_candidate,
)
from omega_engine.crates.prime.prime_001 import AdapterStatus
from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers import (
    CascadeStage,
    ObstructionProblem,
    OesosCascade,
    SolverRegistry,
    StageKind,
)


def test_prime_minus_one_proposed_only() -> None:
    c = propose_candidate(
        artifact_id="a1",
        locus_id="L0",
        problem_family="claim",
        carrier_proposal="C0",
    )
    assert c.status == "proposed_only"
    assert c.authority_effect == "None"


def test_prime_000_accept_and_refuse_locus() -> None:
    ok = admit_declaration(
        DeclarationPacket(
            domain="d",
            locus_hash="h",
            carrier="c",
            observer="o",
            primitive_difference="δ",
            zero_rel="z",
            witness="w",
        )
    )
    assert ok.kind == AdmissionKind.ACCEPT_DECLARATION
    bad = admit_declaration(
        DeclarationPacket(
            domain="d",
            locus_hash=None,
            carrier="c",
            observer="o",
            primitive_difference="δ",
            zero_rel="z",
            witness="w",
        )
    )
    assert bad.kind == AdmissionKind.REFUSE_MISSING_LOCUS


def test_prime_001_intake_does_not_enter_dda() -> None:
    chk = check_adapter(
        placement="intake",
        source_typed=False,
        locus_grounded=True,
        adapter_adequate=True,
        preserves_authority_fence=True,
    )
    assert chk.status == AdapterStatus.REFUSED_UNTYPED
    assert chk.enters_dda_trace is False


def test_intake_trace_rejects_dda_flag() -> None:
    tr = IntakeTrace()
    cand = propose_candidate(artifact_id="a", locus_id="L", problem_family="x")
    try:
        tr.append(
            IntakeTraceRecord(
                raw_artifact_hash="h",
                candidate_locus="L",
                candidate_packet=cand,
                intake_adapter_status="REFUSED_UNTYPED",
                enters_dda_trace=True,
            )
        )
        assert False, "should refuse enters_dda_trace=True"
    except ValueError:
        pass


def test_prime_002_budget_and_anti_cheat() -> None:
    base = CanContinueInput(
        outstanding_obligation=True,
        higher_obligation_witness=True,
        next_carrier_declared=True,
        adapter_sound=True,
        detector_adequate=True,
        minimal_licensed_lift=True,
        skeleton_preserved=True,
        budget_available=True,
        gtla_continuation_refusal=False,
        anti_cheat=AntiCheatFlags(),
        budget_total=1.0,
        cost_floor=0.25,
        ops_so_far=0,
    )
    assert can_continue(base).may_continue is True
    halt = can_continue(
        CanContinueInput(
            outstanding_obligation=True,
            higher_obligation_witness=True,
            next_carrier_declared=True,
            adapter_sound=True,
            detector_adequate=True,
            minimal_licensed_lift=True,
            skeleton_preserved=True,
            budget_available=True,
            gtla_continuation_refusal=False,
            anti_cheat=AntiCheatFlags(degree_laundering=True),
            budget_total=1.0,
            cost_floor=0.25,
            ops_so_far=0,
        )
    )
    assert halt.may_continue is False
    assert "NoDegreeLaundering" in halt.anti_cheat_violations


def test_oesos_cascade_refuses_without_admission() -> None:
    reg = SolverRegistry()
    reg.register("gauge_residual", ["l1_gauge"])
    cascade = OesosCascade(
        registry=reg,
        stages=[CascadeStage(kind=StageKind.FOUNDATION, solver_id="l1_gauge")],
    )
    problem = ObstructionProblem(
        problem_id="p1",
        carrier_ref="net",
        residual_class="gauge_residual",
        scope="local",
    )
    decl = DeclarationPacket(domain="d", locus_hash=None, carrier="c")
    receipt = cascade.run(problem, decl)
    assert receipt.terminal_status == AdmissionKind.REFUSE_MISSING_LOCUS.value
    assert receipt.authority_effect == "None"


def test_oesos_cascade_declared_stages_after_accept() -> None:
    reg = SolverRegistry()
    reg.register("gauge_residual", ["l1_gauge"])

    def handler(**kwargs):
        return {"status": "SOLVED", "residual_mass": 0.0}

    cascade = OesosCascade(
        registry=reg,
        stages=[
            CascadeStage(kind=StageKind.FOUNDATION, solver_id="l1_gauge", handler=handler),
            CascadeStage(kind=StageKind.TERMINAL, solver_id="term"),
        ],
    )
    problem = ObstructionProblem(
        problem_id="p2",
        carrier_ref="net",
        residual_class="gauge_residual",
        scope="local",
    )
    decl = DeclarationPacket(
        domain="d",
        locus_hash="h",
        carrier="c",
        observer="o",
        primitive_difference="δ",
        zero_rel="z",
        witness="w",
    )
    receipt = cascade.run(problem, decl)
    assert receipt.terminal_status == "SOLVED"
    assert "foundation" in receipt.stage_names()


