r"""
Pytest Test Suite for Universe CODA (CODA-000 through CODA-009 & OE-000 Prime Triad).
AuthorityEffect: None.
"""

from omega_engine.crates.engine.eng_coda import (
    SelfRepairAdjunction,
    CandidatePacket,
    CODAMasterSuite,
    CohomologicalEngine,
    ColimitAggregationEngine,
    DDATerminalizer,
    IntakeTrace,
    LocalDeclarationOrder,
    ObserverPacket,
    ObstructionCalculus,
    PrimeTriadEngine,
    ResidualEvaluator,
    ResidualFunctional,
    SimplicialCarrier,
    StepRecord,
    run_coda_master_suite,
    verify_merkle_tape,
)
import numpy as np


def test_coda_000_foc_curvature():
    edges = [(0, 1), (1, 2), (2, 0)]
    faces = [(0, 1, 2)]
    coda = CODAMasterSuite(3, edges, faces)
    cochain = np.array([1.0, 1.0, 1.0])
    curv = coda.coda_000_foc_curvature(cochain)
    assert abs(curv[0] - 3.0) < 1e-6


def test_coda_002_mur_gauge_norm():
    edges = [(0, 1), (1, 2), (2, 0)]
    faces = [(0, 1, 2)]
    coda = CODAMasterSuite(3, edges, faces)
    cochain = np.array([1.0, 0.5, -0.8])
    phi_1 = coda.coda_002_mur_l1_gauge_norm(cochain)
    assert phi_1 > 0.0


def test_coda_008_q_rates():
    edges = [(0, 1)]
    faces = []
    coda = CODAMasterSuite(2, edges, faces)
    nu_e, a_e, mi = coda.coda_008_q_rates(J_int=1.5, t=0.05)
    assert nu_e == 3.0
    assert a_e == 4.5
    assert mi >= 0.0


def test_coda_009_master_ledger():
    ledger = run_coda_master_suite()
    assert ledger["coda_002_l1_gauge_norm_phi1"] > 0.0
    assert ledger["coda_008_nu_e"] == 3.0


def test_oe_000_coboundary_d0_and_d1_nilpotency():
    carrier = SimplicialCarrier(
        vertices=[0, 1, 2, 3],
        edges=[(0, 1), (1, 2), (0, 2), (2, 3), (1, 3)],
        faces=[(0, 1, 2), (1, 2, 3)]
    )
    assert carrier.validate() is True
    f0 = {0: 10.5, 1: -2.3, 2: 4.1, 3: 100.0}
    is_nilpotent = CohomologicalEngine.verify_nilpotency(carrier, f0)
    assert is_nilpotent is True


def test_oe_000_obstruction_signature():
    carrier = SimplicialCarrier(
        vertices=["a", "b", "c"],
        edges=[("a", "b"), ("b", "c"), ("a", "c")],
        faces=[("a", "b", "c")]
    )
    f0 = {"a": 0.0, "b": 5.0, "c": 12.0}
    d0_f = CohomologicalEngine.d0(carrier, f0)

    sig = ObstructionCalculus.analyze_1cochain(carrier, d0_f)
    assert sig.status_label == "REMOVABLE_GAUGE"
    assert sig.phi_1 < 1e-5


def test_oe_000_7step_local_declaration():
    carrier = SimplicialCarrier(vertices=["v0", "v1"], edges=[("v0", "v1")])
    observer = ObserverPacket(observer_id="obs_01", gauge_name="L1_norm")
    h1 = {("v0", "v1"): 1.5}

    decl = LocalDeclarationOrder(
        step0_grounding_hash="sha256_abc",
        step1_carrier=carrier,
        step2_observer=observer,
        step3_primitive_difference=h1,
        step4_zero_rel_rule="gauge_equality",
        step5_witness_certificate="cert_001"
    )
    ok, msg = decl.validate_declaration_order()
    assert ok is True
    assert msg == "ACCEPT_DECLARATION"


def test_oe_000_can_continue_predicate():
    engine = PrimeTriadEngine()
    assert engine.can_continue(0, True, True, True) is True
    assert engine.can_continue(0, False, True, True) is False


def test_repair_to_closed_l2_hodge_projection():
    """Verify Option A: l2 Hodge projection cancels face curvature d1(h_closed) = 0."""
    carrier = SimplicialCarrier(
        vertices=[0, 1, 2],
        edges=[(0, 1), (1, 2), (0, 2)],
        faces=[(0, 1, 2)]
    )
    h1 = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 0.0}

    receipt = ObstructionCalculus.repair_to_closed_l2(carrier, h1)
    assert receipt["letter"] == "E"
    assert receipt["authority_effect"] == "None"
    assert receipt["gamma_2_before"] > 0.0
    assert receipt["gamma_2_after"] < 1e-6

    h_closed = receipt["h_closed"]
    c2_closed = CohomologicalEngine.d1(carrier, h_closed)
    assert abs(c2_closed[(0, 1, 2)]) < 1e-6


def test_repair_to_closed_local_stencil():
    """Verify Option C: Fast local stencil repair."""
    carrier = SimplicialCarrier(
        vertices=[0, 1, 2],
        edges=[(0, 1), (1, 2), (0, 2)],
        faces=[(0, 1, 2)]
    )
    h1 = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 0.0}
    receipt = ObstructionCalculus.repair_to_closed_local_stencil(carrier, h1)
    assert receipt["gamma_2_after"] < 1e-6
    assert receipt["letter"] == "E"


def test_pullback_carrier_span_options():
    carrier_A = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2)], faces=[])
    carrier_B = SimplicialCarrier(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)], faces=[])

    pulled_A, loss_A = ObstructionCalculus.pullback_carrier_span(carrier_A, carrier_B, "strict")
    assert pulled_A.vertices == [1, 2]
    assert pulled_A.edges == [(1, 2)]
    assert len(loss_A) == 0

    pulled_B, loss_B = ObstructionCalculus.pullback_carrier_span(carrier_A, carrier_B, "homotopy_coherent")
    assert len(loss_B) == 1


def test_observer_resolution_guard():
    obs_fine = ObserverPacket(observer_id="obs_fine", gauge_name="L2", resolution=0.01)
    obs_coarse = ObserverPacket(observer_id="obs_coarse", gauge_name="L2", resolution=0.5)

    valid_fine, msg_fine = ObstructionCalculus.validate_observer_resolution(obs_fine, phi_1_min=0.1)
    assert valid_fine is True
    assert msg_fine == "OBSERVER_RESOLUTION_VALIDATED"

    valid_coarse, msg_coarse = ObstructionCalculus.validate_observer_resolution(obs_coarse, phi_1_min=0.1)
    assert valid_coarse is False
    assert msg_coarse == "REFUSED_OBSERVER_DISTORTION"


def test_e_letter_progress_predicate():
    carrier = SimplicialCarrier(
        vertices=[0, 1, 2],
        edges=[(0, 1), (1, 2), (0, 2)],
        faces=[(0, 1, 2)]
    )
    h1 = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 0.0}
    receipt = ObstructionCalculus.repair_to_closed_l2(carrier, h1)
    assert receipt["progress_predicate"] is True
    assert ObstructionCalculus.evaluate_e_letter_progress(receipt) is True


def test_multi_carrier_lens_span_composition():
    cA = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2)], faces=[])
    cB = SimplicialCarrier(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)], faces=[])
    cC = SimplicialCarrier(vertices=[1, 2, 4], edges=[(1, 2), (2, 4)], faces=[])

    composite, loss = ObstructionCalculus.compose_lens_spans([cA, cB, cC], lens_type="strict")
    assert composite.vertices == [1, 2]
    assert composite.edges == [(1, 2)]
    assert len(loss) == 0


def test_3way_hodge_decomposition():
    carrier = SimplicialCarrier(
        vertices=[0, 1, 2],
        edges=[(0, 1), (1, 2), (0, 2)],
        faces=[(0, 1, 2)]
    )
    h1 = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 0.0}
    decomp = ObstructionCalculus.hodge_decompose_l2(carrier, h1)

    assert decomp["status"] == "HODGE_DECOMPOSED"
    assert decomp["authority_effect"] == "None"
    assert decomp["curvature_mass"] > 0.0
    assert decomp["gamma_2_of_harmonic"] < 1e-6
    assert decomp["d0_adj_norm_of_harmonic"] < 1e-6


def test_compute_exact_betti_1():
    triangle = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[(0, 1, 2)])
    b1_tri, _, _ = ObstructionCalculus.compute_exact_betti_1(triangle)
    assert b1_tri == 0

    cycle = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[])
    b1_cyc, _, _ = ObstructionCalculus.compute_exact_betti_1(cycle)
    assert b1_cyc == 1


def test_extract_orthonormal_harmonic_basis():
    cycle = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[])
    B_on = ObstructionCalculus.extract_orthonormal_harmonic_basis(cycle)
    assert B_on.shape == (3, 1)
    assert abs(np.linalg.norm(B_on) - 1.0) < 1e-6


def test_evaluate_dda_transition():
    receipt_exact = {"gamma_2_after": 0.0, "harmonic_mass": 0.0, "loss_ledger": []}
    trans_exact = ObstructionCalculus.evaluate_dda_transition(receipt_exact)
    assert trans_exact["next_letter"] == "T"
    assert trans_exact["reason"] == "EXACT_CLASS"

    receipt_harm = {"gamma_2_after": 0.0, "harmonic_mass": 0.5, "loss_ledger": []}
    trans_harm = ObstructionCalculus.evaluate_dda_transition(receipt_harm)
    assert trans_harm["next_letter"] == "M"
    assert trans_harm["reason"] == "HARMONIC_RESIDUAL_SURVIVES"


def test_l1_l2_gap_dual_certificate():
    carrier = SimplicialCarrier(
        vertices=[0, 1, 2],
        edges=[(0, 1), (1, 2), (0, 2)],
        faces=[(0, 1, 2)]
    )
    h1 = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 0.0}
    receipt = ObstructionCalculus.repair_to_closed_l2(carrier, h1)
    cert = ObstructionCalculus.l1_l2_gap_dual_certificate(carrier, h1, receipt)
    assert cert["gamma_2"] > 0.0
    assert cert["linear_gap_bound"] >= cert["gamma_2"]


def test_hodge_decompose_weighted_l2():
    carrier = SimplicialCarrier(
        vertices=[0, 1, 2],
        edges=[(0, 1), (1, 2), (0, 2)],
        faces=[(0, 1, 2)]
    )
    h1 = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 0.0}
    weights = {(0, 1): 1.0, (1, 2): 2.5, (0, 2): 0.4}

    decomp = ObstructionCalculus.hodge_decompose_weighted_l2(carrier, h1, edge_weights=weights)
    assert decomp["status"] == "HODGE_DECOMPOSED"
    assert decomp["edge_weights_source"] == "user_supplied"
    assert decomp["harmonic_mass_weighted"] >= 0.0


def test_monotone_l1_cycle_step():
    cycle = SimplicialCarrier(
        vertices=[0, 1, 2],
        edges=[(0, 1), (1, 2), (0, 2)],
        faces=[]
    )
    h1 = {(0, 1): 2.0, (1, 2): 2.0, (0, 2): 2.0}
    c_cochain = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): -1.0}

def test_fet_triad_and_merkle_verification():
    carrier = SimplicialCarrier(
        vertices=[0, 1, 2],
        edges=[(0, 1), (1, 2), (0, 2)],
        faces=[(0, 1, 2)]
    )
    h1 = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 0.0}

    func_vals = ResidualFunctional.evaluate(carrier, h1)
    assert func_vals["gamma_2"] > 0.0

    eval_receipt = ResidualEvaluator.evaluate(func_vals)
    assert eval_receipt["label"] == "ACTIVE_CLOSURE_FAILURE"

    engine = PrimeTriadEngine()
    terminalizer = DDATerminalizer(engine, genesis_hash="GENESIS_TEST")

    repair_receipt = ObstructionCalculus.repair_to_closed_l2(carrier, h1)
    status = terminalizer.process_step("E", repair_receipt)
    assert status == "STEP_RECORDED"
    assert len(terminalizer.merkle_tape) == 1

    valid, msg = verify_merkle_tape(terminalizer.merkle_tape, genesis_hash="GENESIS_TEST")
    assert valid is True
    assert msg == "MERKLE_TAPE_VERIFIED"


def test_compute_exact_betti_1_with_snf():
    cycle = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[])
    res_cycle = ObstructionCalculus.compute_exact_betti_1_with_snf(cycle)
    assert res_cycle["b1"] == 1
    assert res_cycle["rank_d0"] == 2
    assert res_cycle["snf_diagonal_d0"] == [1, 1]

def test_compute_exact_betti_numbers():
    tri = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[(0, 1, 2)])
    res_tri = ObstructionCalculus.compute_exact_betti_numbers(tri)
    assert (res_tri["b0"], res_tri["b1"], res_tri["b2"]) == (1, 0, 0)

    cycle = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[])
    res_cyc = ObstructionCalculus.compute_exact_betti_numbers(cycle)
    assert (res_cyc["b0"], res_cyc["b1"], res_cyc["b2"]) == (1, 1, 0)

    path = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2)], faces=[])
    res_path = ObstructionCalculus.compute_exact_betti_numbers(path)
    assert (res_path["b0"], res_path["b1"], res_path["b2"]) == (1, 0, 0)

    disc = SimplicialCarrier(vertices=[0, 1, 2, 3], edges=[(0, 1), (2, 3)], faces=[])
    res_disc = ObstructionCalculus.compute_exact_betti_numbers(disc)
    assert (res_disc["b0"], res_disc["b1"], res_disc["b2"]) == (2, 0, 0)


def test_solve_l1_gauge_minimization():
    carrier = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[])
    cochain = np.array([2.0, 4.0, 6.0])
    min_l1, alpha_opt = ObstructionCalculus.solve_l1_gauge_minimization(carrier, cochain)
    assert abs(min_l1) < 1e-6


def test_coda_deriv_001_autopoietic_adjunction():
    carrier = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[])
    f0 = {0: 1.0, 1: 4.0, 2: 9.0}

    f_alpha = SelfRepairAdjunction.section_functor_F(carrier, f0)
    assert f_alpha[(0, 1)] == 3.0

    galois_ok = SelfRepairAdjunction.verify_galois_insertion(carrier, f0)
    assert galois_ok is True

    h1 = {e: float(val) for e, val in f_alpha.items()}
    stab_ok = SelfRepairAdjunction.verify_autopoietic_stability(carrier, h1)
    assert stab_ok is True


def test_coda_deriv_004_colimit_aggregation_engine():
    carrier = SimplicialCarrier(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)], faces=[(0, 1, 2)])
    lc1 = {(0, 1): 1.0, (1, 2): 2.0, (0, 2): 3.0}
    lc2 = {(0, 1): 2.0, (1, 2): 4.0, (0, 2): 6.0}

    global_cochain = ColimitAggregationEngine.aggregate_local_cochains(carrier, [lc1, lc2])
    assert global_cochain[(0, 1)] == 1.5
    assert global_cochain[(1, 2)] == 3.0
    assert global_cochain[(0, 2)] == 4.5

    res = ColimitAggregationEngine.verify_bilipschitz_defect_bounds(carrier, global_cochain)
    assert res["status"] == "BILIPSCHITZ_BOUNDS_VERIFIED"
    assert res["bounds_hold"] is True


def test_coda_deriv_003_monotone_l1_multi_cycle_descent():
    carrier = SimplicialCarrier(
        vertices=[0, 1, 2, 3],
        edges=[(0, 1), (1, 2), (0, 2), (2, 3), (0, 3)],
        faces=[]
    )
    h1 = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): -1.0, (2, 3): 2.0, (0, 3): -2.0}
    res = ObstructionCalculus.monotone_l1_multi_cycle_descent(carrier, h1)
    assert res["b1"] == 2
    assert res["status"] == "MULTI_CYCLE_DESCENT_SUCCESS"
    assert res["phi1_optimal"] <= res["phi1_initial"] + 1e-6


def test_prime_triad_record_transform_move():
    engine = PrimeTriadEngine()
    entry = engine.record_transform_move(
        move="D",
        loss_or_gain="loss of fine-grained gauge angle",
        forcing_obstruction="OB_U1",
    )
    assert entry["move"] == "D"
    assert entry["forcing_obstruction"] == "OB_U1"
    assert len(engine.loss_ledger) == 1
    assert "[D] loss of fine-grained gauge angle" in engine.loss_ledger[0]















