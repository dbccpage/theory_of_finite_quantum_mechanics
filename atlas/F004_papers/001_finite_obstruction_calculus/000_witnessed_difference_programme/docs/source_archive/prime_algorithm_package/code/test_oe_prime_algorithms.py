"""Unit, property, and regression tests for OE-000 Algorithm Prime Triad reference implementation."""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import pytest

code_dir = Path(__file__).resolve().parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from oe_prime_algorithms import (  # noqa: E402
    AdapterContract,
    CanContinueInput,
    CandidatePacket,
    CohomologicalEngine,
    DDATerminalizer,
    EvaluatorDefect,
    IntakeTrace,
    LocalDeclarationOrder,
    ObserverPacket,
    ObstructionCalculus,
    PrimeTriadEngine,
    ResidualEvaluator,
    ResidualFunctional,
    ResidualQueueScheduler,
    SimplicialCarrier,
    StepRecord,
    check_adapter,
    verify_merkle_tape,
)

# --- Section 1: Candidate Proposal & Local Declaration Order (OE001-01 .. 04) ---

def test_candidate_packet_and_intake_trace_schema():
    packet = CandidatePacket(
        artifact_id="doc_001",
        locus_id="locus_01",
        problem_family="proof",
        primitive_difference_proposal="diff",
        carrier_proposal="space",
        zero_rel_proposal="rel",
        observer_proposal="probe",
        witness_available=True,
    )
    trace = IntakeTrace(
        raw_artifact_hash="hash01",
        candidate_locus="lines 1-10",
        candidate_packet=packet,
        enters_dda_trace=False,
    )
    assert trace.enters_dda_trace is False
    engine = PrimeTriadEngine()
    assert engine.evaluate_intake(trace) == "ACCEPT_DECLARATION"


def test_intake_refusals():
    engine = PrimeTriadEngine()
    p_no_carrier = CandidatePacket("id", "loc", "fam", "diff", "", "rel", "probe", witness_available=True)
    assert engine.evaluate_intake(IntakeTrace("h", "loc", p_no_carrier)) == "REFUSED_MISSING_CARRIER"

    p_no_obs = CandidatePacket("id", "loc", "fam", "diff", "space", "rel", "", witness_available=True)
    assert engine.evaluate_intake(IntakeTrace("h", "loc", p_no_obs)) == "REFUSED_MISSING_OBSERVER"

    p_no_wit = CandidatePacket("id", "loc", "fam", "diff", "space", "rel", "probe", witness_available=False)
    assert engine.evaluate_intake(IntakeTrace("h", "loc", p_no_wit)) == "REFUSED_MISSING_WITNESS"

    p_inadeq = CandidatePacket("id", "loc", "fam", "diff", "space", "rel", "probe", witness_available=True, adapter_confidence="inadequate")
    assert engine.evaluate_intake(IntakeTrace("h", "loc", p_inadeq)) == "ADAPTER_INADEQUATE"
    assert len(engine.loss_ledger) == 1


def test_prime_000_local_packet_declaration_order():
    carrier = SimplicialCarrier(vertices=["v0", "v1"], edges=[("v0", "v1")])
    observer = ObserverPacket(observer_id="obs_01", gauge_name="L1")
    h1 = {("v0", "v1"): Fraction(3, 2)}
    decl = LocalDeclarationOrder(
        step0_grounding_hash="sha256_ground",
        step1_carrier=carrier,
        step2_observer=observer,
        step3_primitive_difference=h1,
        step4_zero_rel_rule="gauge_equality",
        step5_witness_certificate="cert_001",
    )
    ok, msg = decl.validate_declaration_order()
    assert ok is True
    assert msg == "ACCEPT_DECLARATION"


def test_declaration_order_missing_fields():
    carrier = SimplicialCarrier(vertices=["v0", "v1"], edges=[("v0", "v1")])
    observer = ObserverPacket(observer_id="obs_01", gauge_name="L1")
    h1 = {("v0", "v1"): Fraction(1)}

    d0 = LocalDeclarationOrder("", carrier, observer, h1, "rel", "wit")
    assert d0.validate_declaration_order() == (False, "REFUSE_MISSING_GROUNDING")

    d1 = LocalDeclarationOrder("hash", SimplicialCarrier([], []), observer, h1, "rel", "wit")
    assert d1.validate_declaration_order() == (False, "REFUSE_MISSING_CARRIER")

    d2 = LocalDeclarationOrder("hash", carrier, ObserverPacket("", ""), h1, "rel", "wit")
    assert d2.validate_declaration_order() == (False, "REFUSE_MISSING_OBSERVER")

    d3 = LocalDeclarationOrder("hash", carrier, observer, None, "rel", "wit")  # type: ignore
    assert d3.validate_declaration_order() == (False, "REFUSE_MISSING_PRIMITIVE_DIFFERENCE")

    d4 = LocalDeclarationOrder("hash", carrier, observer, h1, "", "wit")
    assert d4.validate_declaration_order() == (False, "REFUSE_MISSING_ZERO_REL")

    d5 = LocalDeclarationOrder("hash", carrier, observer, h1, "rel", None)
    assert d5.validate_declaration_order() == (False, "REFUSE_MISSING_WITNESS")


def test_measurement_never_precedes_admission():
    carrier = SimplicialCarrier(vertices=["a", "b"], edges=[("a", "b")])
    h = {("a", "b"): Fraction(1)}
    with pytest.raises(PermissionError, match="MEASUREMENT_REFUSED_UNADMITTED_PACKET"):
        ObstructionCalculus.analyze_1cochain(carrier, h, admitted=False)
    with pytest.raises(PermissionError, match="MEASUREMENT_REFUSED_UNADMITTED_PACKET"):
        ObstructionCalculus.analyze_1cochain(carrier, h)


def test_multi_carrier_lens_span_pullback():
    cA = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2)], faces=[])
    cB = SimplicialCarrier(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)], faces=[])
    pulled_strict, loss_strict = ObstructionCalculus.pullback_carrier_span(cA, cB, "strict")
    assert pulled_strict.vertices == (1, 2)
    assert pulled_strict.edges == ((1, 2),)
    assert len(loss_strict) == 0

    pulled_hc, loss_hc = ObstructionCalculus.pullback_carrier_span(cA, cB, "homotopy_coherent")
    assert len(loss_hc) == 1


def test_scoped_terminalization_routing():
    engine = PrimeTriadEngine(budget=100, delta_control=10)
    terminalizer = DDATerminalizer(engine, genesis_hash="GENESIS_ROOT")

    ok, status = terminalizer.terminalize(Fraction(0), Fraction(0), detector_adequate=True)
    assert ok is True
    assert status == "LOCAL_GREEN_FOR_SCOPE"

    ok, status = terminalizer.terminalize(Fraction(0), Fraction(0), detector_adequate=False)
    assert ok is False
    assert status == "REFUSED_BLIND_OBSERVER"

    ok, status = terminalizer.terminalize(Fraction(1), Fraction(0), detector_adequate=True)
    assert ok is False
    assert status == "REFUSED_OPEN_RESIDUAL"


# --- Section 2: Prime 001 Adapter Descent Soundness (OE002-01 .. 03) ---

def test_dual_prime_001_boundary_placement():
    cA = SimplicialCarrier(vertices=[0, 1], edges=[(0, 1)])
    cB = SimplicialCarrier(vertices=[1, 2], edges=[(1, 2)])
    composite, loss = ObstructionCalculus.compose_lens_spans([cA, cB], "strict")
    assert composite.vertices == (1,)
    assert composite.edges == ()


def test_adapter_descent_soundness():
    contract = AdapterContract(
        source_carrier="C_ast",
        target_carrier="C_cochain",
        preserved_operations=("d0", "d1"),
        preserved_equations=("d1_circ_d0",),
        preserved_witnesses=("cert_exact",),
        protected_distinctions=("locus_vs_carrier",),
        authority_fences=("None",),
        loss_ledger=(),
    )
    # Sound transport: target preserves all declared items
    target_good = {"d0": True, "d1": True, "d1_circ_d0": True, "cert_exact": True}
    is_sound, status, losses = check_adapter(contract, {}, target_good)
    assert is_sound is True
    assert status == "ADAPTER_SOUND"
    assert len(losses) == 0

    # Inadequate transport: target loses operation d1 and equation d1_circ_d0
    target_lossy = {"d0": True}
    is_sound_l, status_l, losses_l = check_adapter(contract, {}, target_lossy)
    assert is_sound_l is False
    assert status_l == "ADAPTER_WITH_LOSS"
    assert any("Operation d1 lost" in msg for msg in losses_l)
    assert any("Equation d1_circ_d0 violated" in msg for msg in losses_l)


def test_refusal_and_debt_taxonomy():
    engine = PrimeTriadEngine()
    untyped = engine.coda_reentry("untyped_locus", carrier_declared=False)
    assert untyped["status"] == "REFUSED_UNTYPED_LOCUS_WITHOUT_CARRIER"

    p_inadeq = CandidatePacket("id", "loc", "fam", "diff", "space", "rel", "probe", witness_available=True, adapter_confidence="inadequate")
    assert engine.evaluate_intake(IntakeTrace("h", "loc", p_inadeq)) == "ADAPTER_INADEQUATE"


# --- Section 3: Prime 002 Continuation Control (OE003-01 .. 06) ---

def test_formal_continuation_predicate_can_continue():
    engine = PrimeTriadEngine(budget=100, delta_control=10)
    assert engine.can_continue(
        0,
        has_obligation=True,
        has_witness=True,
        next_carrier_declared=True,
        adapter_sound=True,
        detector_adequate=True,
        minimal_lift=True,
        skeleton_preserved=True,
        budget_remains=True,
        gtla_refusal=False,
    ) is True

    # Any single False must fail
    assert engine.can_continue(0, False, True, True, True, True, True, True, True) is False
    assert engine.can_continue(0, True, False, True, True, True, True, True, True) is False
    assert engine.can_continue(0, True, True, False, True, True, True, True, True) is False
    assert engine.can_continue(0, True, True, True, False, True, True, True, True) is False
    assert engine.can_continue(0, True, True, True, True, False, True, True, True) is False
    assert engine.can_continue(0, True, True, True, True, True, False, True, True) is False
    assert engine.can_continue(0, True, True, True, True, True, True, False, True) is False
    assert engine.can_continue(0, True, True, True, True, True, True, True, False) is False
    assert engine.can_continue(0, True, True, True, True, True, True, True, True, gtla_refusal=True) is False

    inp = CanContinueInput(True, True, True, True, True, True, True, True, True)
    assert inp.evaluate() is True
    structural, budget, no_stop = inp.to_three_condition_summary()
    assert structural is True and budget is True and no_stop is True


def test_six_anti_cheat_halting_laws():
    # Law 1 & 2: Positive cost floor and budget debit execution
    engine = PrimeTriadEngine(budget=10, delta_control=10)
    assert engine.execute_step() == "STEP_EXECUTED"
    # Budget exhausted prevents endless loops -> TERMINAL_WITH_DEBT
    assert engine.execute_step() == "TERMINAL_WITH_DEBT"

    # Law 3: Nonpositive cost floor strictly rejected
    with pytest.raises(ValueError):
        PrimeTriadEngine(budget=10, delta_control=0)
    with pytest.raises(ValueError):
        PrimeTriadEngine(budget=10, delta_control=-5)
    with pytest.raises(ValueError):
        PrimeTriadEngine(budget=-1, delta_control=10)

    # Law 4: Verified green requires verified zero residual
    assert engine.execute_step(diagnostic={"phi_1": 0, "gamma_2": 0}) == "TERMINAL_WITH_DEBT"
    engine2 = PrimeTriadEngine(budget=20, delta_control=10)
    assert engine2.execute_step(diagnostic={"phi_1": 0, "gamma_2": 0}) == "LOCAL_GREEN_FOR_SCOPE"


def test_bounded_operational_termination():
    # Budget = 25, floor = 10 -> at most 2 steps
    engine = PrimeTriadEngine(budget=25, delta_control=10)
    assert engine.execute_step() == "STEP_EXECUTED"
    assert engine.execute_step() == "STEP_EXECUTED"
    assert engine.execute_step() == "TERMINAL_WITH_DEBT"
    assert engine.ops_count == 2
    assert engine.ops_count <= 25 // 10


def test_local_residual_queue_scheduler():
    scheduler = ResidualQueueScheduler()
    scheduler.push(Fraction(2), Fraction(3), 5, {"task": "hard_task"})
    scheduler.push(Fraction(0), Fraction(1), 1, {"task": "easy_task"})

    # Popping admissible step under current state (1, 2, 4) admits easy_task (0, 1, 1)
    admitted = scheduler.pop_admissible_step(current_vector=(Fraction(1), Fraction(2), 4))
    assert admitted is not None
    assert admitted["task"] == "easy_task"

    # No step admissible if candidate does not achieve strict progress
    none_admitted = scheduler.pop_admissible_step(current_vector=(Fraction(1), Fraction(1), 0))
    assert none_admitted is None

    carrier = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[(0, 1, 2)])
    h1 = {(0, 1): Fraction(1), (1, 2): Fraction(1), (0, 2): Fraction(0)}
    repair = ObstructionCalculus.repair_to_closed_l2(carrier, h1)
    assert repair["progress_predicate"] is True
    assert ObstructionCalculus.evaluate_e_letter_progress(repair) is True


def test_coda_taxonomy_pipeline_order():
    carrier = SimplicialCarrier(vertices=["a", "b"], edges=[("a", "b")])
    assert carrier.validate() is True
    obs = ObserverPacket(observer_id="obs", gauge_name="L1", resolution=Fraction(1, 100))
    assert obs.is_adequate(Fraction(1, 10)) is True
    assert obs.is_adequate(Fraction(1, 1000)) is False


def test_residual_aware_can_continue():
    carrier = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[])
    # Case with genuine quotient descent
    h = {(0, 1): Fraction(2), (1, 2): Fraction(2), (0, 2): Fraction(0)}
    c = {(0, 1): Fraction(1), (1, 2): Fraction(1), (0, 2): Fraction(-1)}
    res = ObstructionCalculus.monotone_l1_cycle_step(carrier, h, c)
    assert res["phi_1_before"] == 4
    assert res["phi_1_after"] == 1
    assert res["accepted"] is True


# --- Section 4: CODA Recursive Re-Entry & Ascent (OE004-01 .. 08) ---

def test_coda_recursive_reentry_protocol():
    engine = PrimeTriadEngine()
    carrier = SimplicialCarrier(vertices=[0, 1], edges=[(0, 1)])
    res = engine.coda_reentry("locus_math_001", carrier_declared=True, carrier=carrier)
    assert res["locus"] == "locus_math_001"
    assert res["carrier"] == "carrier_for_locus_math_001"
    assert res["status"] == "REENTERED_ADMITTED"
    assert res["authority_effect"] == "None"


def test_lawful_degree_ascent_and_embedding():
    carrier = SimplicialCarrier(
        vertices=[0, 1, 2, 3],
        edges=[(0, 1), (1, 2), (0, 2), (2, 3), (1, 3)],
        faces=[(0, 1, 2), (1, 2, 3)],
    )
    f0 = {0: Fraction(10), 1: Fraction(-2), 2: Fraction(4), 3: Fraction(100)}
    assert CohomologicalEngine.verify_nilpotency(carrier, f0) is True


def test_stop_conditions_partition():
    receipt_exact = {"gamma_2_after": Fraction(0), "harmonic_mass": Fraction(0)}
    trans_exact = ObstructionCalculus.evaluate_dda_transition(receipt_exact)
    assert trans_exact["next_letter"] == "T"
    assert trans_exact["reason"] == "EXACT_CLASS"

    receipt_harm = {"gamma_2_after": Fraction(0), "harmonic_mass": Fraction(1, 2)}
    trans_harm = ObstructionCalculus.evaluate_dda_transition(receipt_harm)
    assert trans_harm["next_letter"] == "M"
    assert trans_harm["reason"] == "HARMONIC_RESIDUAL_SURVIVES"

    receipt_rupture = {"gamma_2_after": Fraction(2), "harmonic_mass": Fraction(0)}
    trans_rupture = ObstructionCalculus.evaluate_dda_transition(receipt_rupture)
    assert trans_rupture["next_letter"] == "E"
    assert trans_rupture["reason"] == "CLOSURE_FAILURE"


def test_observer_envelope_comparability():
    obs_fine = ObserverPacket(observer_id="fine", gauge_name="L1", resolution=Fraction(1, 100))
    obs_coarse = ObserverPacket(observer_id="coarse", gauge_name="L1", resolution=Fraction(1, 2))

    valid_f, msg_f = ObstructionCalculus.validate_observer_resolution(obs_fine, Fraction(1, 10))
    assert valid_f is True
    assert msg_f == "OBSERVER_RESOLUTION_VALIDATED"

    valid_c, msg_c = ObstructionCalculus.validate_observer_resolution(obs_coarse, Fraction(1, 10))
    assert valid_c is False
    assert msg_c == "REFUSED_OBSERVER_DISTORTION"


def test_evaluator_defect_linearity():
    defect = EvaluatorDefect.defect(
        Fraction(4, 5), Fraction(1, 2), Fraction(3, 4)
    )
    assert defect == Fraction(4, 5) - (Fraction(1, 2) * Fraction(3, 4))
    assert EvaluatorDefect.gpr_minus_lpr(defect, covariance=Fraction(0)) == defect


def test_epk_overlay_diagnostic_scope_fence():
    carrier = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[(0, 1, 2)])
    h1 = {(0, 1): Fraction(1), (1, 2): Fraction(1), (0, 2): Fraction(0)}
    func_vals = ResidualFunctional.evaluate(carrier, h1)
    assert func_vals["gamma_2"] > 0
    eval_receipt = ResidualEvaluator.evaluate(func_vals)
    assert eval_receipt["label"] == "ACTIVE_CLOSURE_FAILURE"

    eval_closed = ResidualEvaluator.evaluate({"gamma_2": Fraction(0)})
    assert eval_closed["label"] == "EXACT_OR_CLOSED"


def test_self_examination_reentry_path():
    engine = PrimeTriadEngine()
    reentry = engine.coda_reentry("L_self", carrier_declared=True)
    assert reentry["status"] == "REENTERED_ADMITTED"
    assert reentry["authority_effect"] == "None"

    # Undeclared carrier refused
    reentry_bad = engine.coda_reentry("L_self", carrier_declared=False)
    assert reentry_bad["status"] == "REFUSED_UNTYPED_LOCUS_WITHOUT_CARRIER"


def test_anti_cheat_self_proposal_and_queue_upgrade():
    engine = PrimeTriadEngine()
    trace = IntakeTrace(
        raw_artifact_hash="hash_self",
        candidate_locus="engine_state",
        candidate_packet=CandidatePacket("self", "L_self", "engine", "diff", "C_self", "Z_self", "obs", witness_available=False),
        enters_dda_trace=False,
    )
    assert engine.evaluate_intake(trace) == "REFUSED_MISSING_WITNESS"


# --- Section 5: Additional Supporting Invariant Tests ---

def test_coboundary_d0_and_d1():
    carrier = SimplicialCarrier(
        vertices=["v0", "v1", "v2"],
        edges=[("v0", "v1"), ("v1", "v2"), ("v0", "v2")],
        faces=[("v0", "v1", "v2")],
    )
    assert carrier.validate() is True
    f0 = {"v0": Fraction(1), "v1": Fraction(3), "v2": Fraction(7)}
    d0_f = CohomologicalEngine.d0(carrier, f0)
    assert d0_f[("v0", "v1")] == Fraction(2)
    assert d0_f[("v1", "v2")] == Fraction(4)
    assert d0_f[("v0", "v2")] == Fraction(6)

    d1_d0_f = CohomologicalEngine.d1(carrier, d0_f)
    assert d1_d0_f[("v0", "v1", "v2")] == Fraction(0)


def test_obstruction_signature_removable_gauge():
    carrier = SimplicialCarrier(
        vertices=["a", "b", "c"],
        edges=[("a", "b"), ("b", "c"), ("a", "c")],
        faces=[("a", "b", "c")],
    )
    f0 = {"a": Fraction(0), "b": Fraction(5), "c": Fraction(12)}
    d0_f = CohomologicalEngine.d0(carrier, f0)
    sig = ObstructionCalculus.analyze_1cochain(carrier, d0_f, admitted=True)
    assert sig.status_label == "REMOVABLE_GAUGE"
    assert sig.phi_1 == 0
    assert sig.gamma_2 == 0


def test_obstruction_signature_rupture():
    carrier = SimplicialCarrier(
        vertices=["a", "b", "c"],
        edges=[("a", "b"), ("b", "c"), ("a", "c")],
        faces=[("a", "b", "c")],
    )
    h1 = {("a", "b"): Fraction(10), ("b", "c"): Fraction(10), ("a", "c"): Fraction(0)}
    sig = ObstructionCalculus.analyze_1cochain(carrier, h1, admitted=True)
    assert sig.gamma_2 > 0
    assert sig.status_label == "NON_CLOSED_RUPTURE"


def test_closed_obstruction_signature():
    carrier = SimplicialCarrier(
        vertices=["a", "b", "c"],
        edges=[("a", "b"), ("b", "c"), ("a", "c")],
        faces=[],
    )
    h1 = {("a", "b"): Fraction(1), ("b", "c"): Fraction(1), ("a", "c"): Fraction(0)}
    sig = ObstructionCalculus.analyze_1cochain(carrier, h1, admitted=True)
    assert sig.gamma_2 == 0
    assert sig.phi_1 > 0
    assert sig.status_label == "CLOSED_OBSTRUCTION"


def test_betti_numbers_and_harmonic_basis():
    tri = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[(0, 1, 2)])
    assert ObstructionCalculus.compute_exact_betti_numbers(tri) == {"b0": 1, "b1": 0, "b2": 0}

    cyc = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[])
    assert ObstructionCalculus.compute_exact_betti_numbers(cyc) == {"b0": 1, "b1": 1, "b2": 0}
    b1_snf = ObstructionCalculus.compute_exact_betti_1_with_snf(cyc)
    assert b1_snf["b1"] == 1
    assert b1_snf["rank_d0"] == 2

    basis = ObstructionCalculus.extract_orthonormal_harmonic_basis(cyc)
    assert len(basis) == 1


def test_hodge_decomposition_and_dual_certificate():
    carrier = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[(0, 1, 2)])
    h1 = {(0, 1): Fraction(1), (1, 2): Fraction(1), (0, 2): Fraction(0)}
    decomp = ObstructionCalculus.hodge_decompose_weighted_l2(carrier, h1)
    assert decomp["status"] == "HODGE_DECOMPOSED"
    assert decomp["edge_weights_source"] == "uniform"

    receipt = ObstructionCalculus.repair_to_closed_local_stencil(carrier, h1)
    cert = ObstructionCalculus.l1_l2_gap_dual_certificate(carrier, h1, receipt)
    assert cert["certificate_status"] == "CERTIFIED"


def test_merkle_tape_integrity_and_forgery():
    engine = PrimeTriadEngine()
    terminalizer = DDATerminalizer(engine, genesis_hash="GENESIS_TEST")
    terminalizer.process_step("E", {"status": "repaired", "gamma_2": 0})
    terminalizer.process_step("T", {"status": "sealed", "phi_1": 0})
    valid, msg = verify_merkle_tape(terminalizer.merkle_tape, genesis_hash="GENESIS_TEST")
    assert valid is True
    assert msg == "MERKLE_TAPE_VERIFIED"

    # Forgery test: mutate hash
    forged = list(terminalizer.merkle_tape)
    forged[1] = dict(forged[1], hash="forged_hash")
    valid_f, msg_f = verify_merkle_tape(forged, genesis_hash="GENESIS_TEST")
    assert valid_f is False
    assert msg_f == "ENTRY_HASH_MISMATCH"

    # Forgery test: mutate prev_hash
    forged_prev = list(terminalizer.merkle_tape)
    forged_prev[1] = dict(forged_prev[1], prev_hash="bad_prev")
    valid_p, msg_p = verify_merkle_tape(forged_prev, genesis_hash="GENESIS_TEST")
    assert valid_p is False
    assert msg_p == "HASH_CHAIN_BROKEN"

    # Forgery test: mutate outcome payload
    forged_payload = list(terminalizer.merkle_tape)
    forged_payload[1] = dict(forged_payload[1], outcome={"status": "FORGED_OUTCOME"})
    valid_payload, msg_payload = verify_merkle_tape(forged_payload, genesis_hash="GENESIS_TEST")
    assert valid_payload is False
    assert msg_payload == "ENTRY_HASH_MISMATCH"


def test_simplicial_carrier_empty():
    empty_carrier = SimplicialCarrier([], [])
    assert empty_carrier.validate() is True
    b1, r0, r1 = ObstructionCalculus.compute_exact_betti_1(empty_carrier)
    assert (b1, r0, r1) == (0, 0, 0)
    basis = ObstructionCalculus.extract_orthonormal_harmonic_basis(empty_carrier)
    assert basis == []
    min_norm, alpha = ObstructionCalculus.solve_l1_gauge_minimization(empty_carrier, [])
    assert min_norm == 0
    c_empty, loss_empty = ObstructionCalculus.compose_lens_spans([])
    assert c_empty.vertices == ()
    m_empty = ObstructionCalculus.monotone_l1_cycle_step(empty_carrier, {})
    assert m_empty["accepted"] is False


def test_step_record_dataclass():
    rec = StepRecord(0, "E", "prev", "curr", {})
    assert rec.letter == "E"


# --- Section 6: Review Counterexample Regression Suite ---

def test_review_reproduction_regressions():
    """All 10 demonstrated failures from the Zenodo republication review."""
    tri = SimplicialCarrier([0, 1, 2], [(0, 1), (1, 2), (0, 2)])

    # 1. L1 gauge minimization on hollow triangle
    assert ObstructionCalculus.solve_l1_gauge_minimization(tri, [1, 1, 0])[0] == 2

    # 2. Nonzero exact edge is exact, not harmonic
    edge = SimplicialCarrier([0, 1], [(0, 1)])
    d_edge = ObstructionCalculus.hodge_decompose_l2(edge, {(0, 1): 1})
    assert d_edge["exact"][(0, 1)] == 1
    assert d_edge["harmonic"][(0, 1)] == 0
    assert d_edge["d0_adj_norm_of_harmonic"] == 0

    # 3. Two adjacent faces coupled repair
    two = SimplicialCarrier(
        [0, 1, 2, 3],
        [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)],
        [(0, 1, 2), (1, 2, 3)],
    )
    r_two = ObstructionCalculus.repair_to_closed_l2(two, {(0, 1): 1})
    assert CohomologicalEngine.d1(two, r_two["h_closed"])[(0, 1, 2)] == 0
    assert r_two["gamma_2_after"] == 0

    # 4. Monotone L1 cycle step rejects quotient inflation
    h = {(0, 1): 1, (1, 2): 1, (0, 2): 2}
    cycle = {(0, 1): 1, (1, 2): 1, (0, 2): -1}
    r_cycle = ObstructionCalculus.monotone_l1_cycle_step(tri, h, cycle)
    assert r_cycle["accepted"] is False
    assert r_cycle["h_updated"] == h
    assert ObstructionCalculus.analyze_1cochain(tri, h, True).phi_1 == 0

    # 5. Presentation invariance for quotient norm
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]
    assert ObstructionCalculus.analyze_1cochain(SimplicialCarrier([0, 1, 2, 3], edges), {(0, 1): 1}, True).phi_1 == 1
    assert ObstructionCalculus.analyze_1cochain(SimplicialCarrier([2, 0, 1, 3], edges), {(0, 1): 1}, True).phi_1 == 1

    # 6. DDA transition requires complete receipt and routes harmonic residual
    with pytest.raises(ValueError):
        ObstructionCalculus.evaluate_dda_transition({})
    d_obstruction = ObstructionCalculus.hodge_decompose_l2(tri, {(0, 1): 1, (1, 2): 1, (0, 2): 0})
    assert ObstructionCalculus.evaluate_dda_transition(d_obstruction)["reason"] == "HARMONIC_RESIDUAL_SURVIVES"
    assert ObstructionCalculus.evaluate_dda_transition(d_obstruction)["next_letter"] == "M"

    # 7. Payload tampering detected by Merkle tape
    t = DDATerminalizer(PrimeTriadEngine(), "genesis")
    t.process_step("T", {"phi_1": 1, "status": "REFUSED_OPEN_RESIDUAL"})
    t.merkle_tape[0]["outcome"] = {"phi_1": 0, "status": "LOCAL_GREEN_FOR_SCOPE"}
    assert verify_merkle_tape(t.merkle_tape, "genesis")[0] is False

    # 8. Invalid carrier validation and nilpotency protection
    bad = SimplicialCarrier([0, 1, 2], [(0, 1), (1, 2)], [(0, 1, 2)])
    assert bad.validate() is False
    assert CohomologicalEngine.verify_nilpotency(bad, {0: 0, 1: 1, 2: 2}) is False

    # 9. Exact Betti numbers on sphere (1,0,1) and sphere-wedge-circle (1,1,1)
    sphere_edges = list(combinations(range(4), 2))
    sphere_faces = list(combinations(range(4), 3))
    sphere = SimplicialCarrier(range(4), sphere_edges, sphere_faces)
    wedged = SimplicialCarrier(range(6), sphere_edges + [(0, 4), (4, 5), (0, 5)], sphere_faces)
    assert ObstructionCalculus.compute_exact_betti_numbers(sphere)["b2"] == 1
    assert ObstructionCalculus.compute_exact_betti_numbers(wedged)["b1"] == 1

    # 10. Nonpositive cost floors rejected at engine construction
    with pytest.raises(ValueError):
        PrimeTriadEngine(budget=1, delta_control=0)
    with pytest.raises(ValueError):
        PrimeTriadEngine(budget=1, delta_control=-2)


def test_coverage_edge_branches():
    # _to_fraction with int, float
    assert ObstructionCalculus.validate_observer_resolution(ObserverPacket('o', 'L1', Fraction(1, 10)), 0.5)[0]
    assert ObstructionCalculus.validate_observer_resolution(ObserverPacket('o', 'L1', Fraction(1, 10)), 1)[0]

    # SimplicialCarrier invalid cases: duplicate vertices, self loops, duplicate edges, duplicate faces
    assert SimplicialCarrier([0, 0, 1], [(0, 1)]).validate() is False
    assert SimplicialCarrier([0, 1], [(0, 1), (0, 1)]).validate() is False
    assert SimplicialCarrier([0, 1], [(0, 0)]).validate() is False
    assert SimplicialCarrier([0, 1, 2], [(0, 1), (1, 2), (0, 2)], [(0, 1, 2), (0, 1, 2)]).validate() is False
    assert SimplicialCarrier([0, 1, 2], [(0, 1), (1, 2), (0, 2)], [(0, 0, 2)]).validate() is False

    # Weighted Hodge decomposition with non-uniform weights
    tri = SimplicialCarrier([0, 1, 2], [(0, 1), (1, 2), (0, 2)], [(0, 1, 2)])
    h_w = {(0, 1): Fraction(1), (1, 2): Fraction(2), (0, 2): Fraction(1)}
    w_dict = {(0, 1): Fraction(2), (1, 2): Fraction(3), (0, 2): Fraction(1)}
    d_w = ObstructionCalculus.hodge_decompose_weighted_l2(tri, h_w, edge_weights=w_dict)
    assert d_w['edge_weights_source'] == 'user_supplied'
    assert d_w['harmonic_mass_weighted'] == 0

    # DDA transition missing diagnostics error
    with pytest.raises(ValueError):
        ObstructionCalculus.evaluate_dda_transition({'other_field': 1})

    # DDA transition with harmonic dict and curvature_mass
    t_curv = ObstructionCalculus.evaluate_dda_transition({'curvature_mass': Fraction(2), 'harmonic': {(0, 1): Fraction(1)}})
    assert t_curv['next_letter'] == 'E'
    t_harm = ObstructionCalculus.evaluate_dda_transition({'gamma_2': Fraction(0), 'harmonic': {(0, 1): Fraction(1)}})
    assert t_harm['next_letter'] == 'M'

    # execute_step with non-green diagnostic
    eng = PrimeTriadEngine(budget=100, delta_control=10)
    assert eng.execute_step(diagnostic={'phi_1': 1, 'gamma_2': 0}) == 'STEP_EXECUTED'
