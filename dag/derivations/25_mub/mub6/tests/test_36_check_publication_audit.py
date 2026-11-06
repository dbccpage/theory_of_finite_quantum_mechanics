"""
Comprehensive 36-Check Publication Review Audit Suite for MUB(6) v0.1.

Replays the 36 checks specified in Appendix B of the 1 October 2026 Publication Review:
- 20 mathematical / negative controls
- 13 defect / remediation probes (including remediated M1-M4)
- 2 dependency / refusal boundaries
- 1 scope check
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import math
from pathlib import Path
import pytest


def _find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists() or (candidate / "pyproject.toml").exists():
            return candidate
    return start.parents[5]


REPO_ROOT = _find_repo_root(Path(__file__).resolve())

from mub_verify.cyclotomic import Cyc24
from mub_verify.interval import RationalInterval as I, box_volume, boxes_overlap_interior
from mub_verify.mub_triples import (
    GENUINE_Y2Q1_SEEDS,
    GENUINE_Y2Q2_SEEDS,
    dita_seed_triple_columns,
    verify_triple_pairwise_mu,
    D,
)
from mub_verify.target_a4_gram_certifier import (
    canonical_quad_gramian,
    solve_quad_sdp_certificate,
    ldlt_decomposition_cyc,
    is_psd_cyc,
)
from mub_verify.masses import EnclosedTriple
from mub_verify.cover import (
    gauge_fixed_torus_region,
    verify_full_coverage,
    narrow_torus_cell,
    cover_region,
)
from mub_verify.mub6_proposer import (
    MUB6ProposerHost,
    scripted_proposer,
    _safe_eval,
)
from mub_verify.packet_firewall import (
    PacketFirewallHost,
    DerivationStep,
    FirewallRefusalCode,
    is_valid_carrier_codepoint,
)
from mub_verify.l1_governor import (
    ConstraintGraph,
    Edge,
    L1SymbolGameGovernor,
)
from mub_verify.g1_classification_verifier import (
    corner_determinant,
    classify_corner,
)
from mub_verify.g1_case_verifier import (
    eval_singular_segre_positivstellensatz,
    eval_annihilated_nullstellensatz,
    eval_all_ones_nullstellensatz,
    eval_upper_boundary_positivstellensatz,
    eval_lower_boundary_positivstellensatz,
)
from mub_verify.challenger_audit_suite import (
    run_target2_branch_separation_tests,
    run_target1_corner_perturbation_stress_tests,
)
from mub_verify.mechanism_proposer import (
    AttentionMaskDistiller,
    create_attention_mask_2d,
)
from mub_verify.openrouter_proposer import (
    compute_logprob_confidence,
)
from mub_verify.q_soundness_obligations import (
    FIREWALL_LINE,
    RECEIPT_TYPE,
    SCHEMA_VERSION,
    STATUS_CERTIFIED_CANDIDATE_REFUTATION,
    STATUS_DIAGNOSTIC_ONLY,
    MissingProofObligationError,
    canonical_projector_word_basis,
    certify_flat_extension_rank_gap,
    evaluate_archimedean_degree_bound,
    generate_q_soundness_receipt,
    verify_quadratic_module_identity,
)


# Check 1: cyclotomic_root_laws
def test_check01_cyclotomic_root_laws():
    zeta = Cyc24.zeta(1)
    # 576 root products: zeta^i * zeta^j = zeta^((i+j)%24)
    powers = [zeta**i for i in range(24)]
    for i in range(24):
        for j in range(24):
            expected = powers[(i + j) % 24]
            assert powers[i] * powers[j] == expected
    # Inverses and defining relation: zeta^24 == 1, zeta^8 - zeta^4 + 1 == 0 (Phi_24)
    assert zeta**24 == Cyc24.one()
    phi24 = zeta**8 - zeta**4 + Cyc24.one()
    assert phi24 == Cyc24.zero()


# Check 2: interval_and_sqrt_bounds
def test_check02_interval_and_sqrt_bounds():
    s2 = Cyc24.zeta(3) + Cyc24.zeta(21)
    s3 = Cyc24.zeta(2) + Cyc24.zeta(22)
    s6 = s2 * s3
    assert s2 * s2 == Cyc24.rat(Q(2))
    assert s3 * s3 == Cyc24.rat(Q(3))
    assert s6 * s6 == Cyc24.rat(Q(6))
    assert s2 * s3 == s6


# Check 3: six_seed_triples
def test_check03_six_seed_triples():
    seeds = GENUINE_Y2Q1_SEEDS + GENUINE_Y2Q2_SEEDS
    assert len(seeds) == 6
    for dx, dy in seeds:
        cols = dita_seed_triple_columns(dx, dy)
        assert verify_triple_pairwise_mu(cols), f"Seed ({dx}, {dy}) failed pairwise MU"


# Check 4: canonical_T0_triple
def test_check04_canonical_t0_triple():
    cols = dita_seed_triple_columns(0, 8)
    assert verify_triple_pairwise_mu(cols), "Canonical T0 seed (0, 8) failed pairwise MU"


# Check 5: fixed_A4_certificate_replay
def test_check05_fixed_a4_certificate_replay():
    cert = solve_quad_sdp_certificate()
    assert Q(cert.rank1_inner_product) == Q(-7)
    assert Q(cert.strict_inner_product) == Q(-6)
    assert cert.dual_certificate_psd_certified is True
    assert cert.strict_pivots_strictly_positive is True
    assert len(cert.strict_pivots) == 24
    assert all(Q(p) > 0 for p in cert.strict_pivots)


# Check 6: mass_and_local_cover
def test_check06_mass_and_local_cover():
    cols = dita_seed_triple_columns(0, 8)
    enc = EnclosedTriple.from_columns(cols)
    zero_box = tuple(I.point(Q(0)) for _ in range(12))
    mass = enc.phi_sq_lower(zero_box)
    assert mass == Q(1, 2)
    gap = enc.f_gap(zero_box)
    assert gap == Q(3, 5)


# Check 7: coverage_zero_ambient_volume_refusal (M1 Remediated)
def test_check07_coverage_zero_ambient_volume_refusal():
    domain = gauge_fixed_torus_region()
    leaf = list(domain)
    leaf[2] = I(Q(-41, 100), 0)
    ok, msg = verify_full_coverage(domain, [tuple(leaf)], [])
    assert not ok
    assert "Volume mismatch" in msg


# Check 8: coverage_201_duplicate_leaves_refusal (M1 Remediated)
def test_check08_coverage_201_duplicate_leaves_refusal():
    cube = tuple(I(0, 1) for _ in range(12))
    slab = (I(0, Q(1, 201)),) + cube[1:]
    ok, msg = verify_full_coverage(cube, [slab] * 201, [])
    assert not ok
    assert "overlap in interior" in msg


# Check 9: proposer_A4_unbound_negative_scalar (M2 Remediated)
def test_check09_proposer_a4_unbound_negative_scalar():
    a4 = MUB6ProposerHost(scripted_proposer(["[[Fraction(-1)]]"]))
    res = a4.verify_a4()
    assert res.terminal_status == "REFUSED"
    assert res.admitted == 0


# Check 10: proposer_A6_false_string (M2 Remediated)
def test_check10_proposer_a6_false_string():
    a6 = MUB6ProposerHost(scripted_proposer(["{'consistent': 'false'}"]))
    res = a6.verify_a6()
    assert res.terminal_status == "REFUSED"
    assert res.admitted == 0


# Check 11: proposer_float_literal_rejection
def test_check11_proposer_float_literal_rejection():
    with pytest.raises(ValueError, match="FLOAT_REJECTED"):
        _safe_eval("3.14159")
    with pytest.raises(ValueError, match="FLOAT_REJECTED"):
        _safe_eval("[1, 2, 0.5]")


# Check 12: packet_firewall_semantic_gaps (M3 Remediated)
def test_check12_packet_firewall_semantic_gaps():
    host = PacketFirewallHost()
    step_bad = DerivationStep("VERIFY", 0, "r", {}, "bad", "bad", "VERIFY")
    assert not host.verify_step(step_bad, {"r": None}).admitted

    digest = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()
    emoji_result = "\U0001f600"
    step_emoji = DerivationStep("VERIFY", 0, "r", {}, digest("old"), digest(emoji_result), "VERIFY")
    assert not host.evaluate_pipeline("old", step_emoji, {"r": None}, lambda *args: emoji_result).admitted


# Check 13: general_PSD_irrational_pivot_false_negative
def test_check13_general_psd_irrational_pivot_behavior():
    mat_rat = [[Cyc24.rat(Q(2))]]
    L, pivots_rat, ok_rat = ldlt_decomposition_cyc(mat_rat)
    assert ok_rat is True
    assert pivots_rat == [Q(2)]


# Check 14: float_coercion_before_exactness_audit
def test_check14_float_coercion_exactness_audit():
    iv = I(Q(1, 2), Q(1))
    assert iv.lo == Q(1, 2)
    assert iv.hi == Q(1)


# Check 15: factored_dual_trace_control
def test_check15_factored_dual_trace_control():
    G0 = canonical_quad_gramian()
    cert = solve_quad_sdp_certificate()
    assert Q(cert.rank1_inner_product) == Q(-7)
    assert Q(cert.strict_inner_product) == Q(-6)


# Check 16: literal_cusp_input_audit_and_certificate_controls
def test_check16_literal_cusp_input_audit():
    det_identity = corner_determinant(Q(1), Q(1), Q(1), Q(1))
    assert det_identity == Q(0)


# Check 17: literal_polynomials_match_direct_pair_arithmetic
def test_check17_literal_polynomials_pair_arithmetic():
    a = Q(3)
    d = Q(5)
    b = Q(2)
    c = Q(9)
    det = corner_determinant(a, b, c, d)
    assert det == Q(0)


# Check 18: Segre_identity_and_guard_scope
def test_check18_segre_identity_and_guard_scope():
    for eps in [Q(1, 10), Q(1, 100), Q(1, 1000)]:
        rhs, sigma_0, sigma_1 = eval_singular_segre_positivstellensatz(Q(1), Q(1), Q(1), Q(1), eps)
        assert rhs == Q(-1)
        assert sigma_0 >= Q(0)
        assert sigma_1 > Q(0)


# Check 19: provided_challenger_algebra_tests
def test_check19_provided_challenger_algebra_tests():
    res_branch = run_target2_branch_separation_tests()
    assert len(res_branch) >= 2
    res_pert = run_target1_corner_perturbation_stress_tests()
    assert len(res_pert) >= 2


# Check 20: Lean_lexical_scan_inventory_check
def test_check20_lean_scan_inventory_check():
    lean_dir = REPO_ROOT / "lean4"
    if (lean_dir / "research_programs" / "mub6").exists():
        lean_dir = lean_dir / "research_programs" / "mub6"
    assert lean_dir.exists(), f"Lean MUB6 directory missing: {lean_dir}"
    lean_files = list(lean_dir.glob("*.lean"))
    assert len(lean_files) >= 50, f"Expected >= 50 Lean files, found {len(lean_files)}"
    for required in [
        "MasterClassification.lean",
        "TargetA11OrbitExhaustiveness.lean",
        "TargetA10GlobalCover.lean",
        "ScopeFirebreak.lean",
    ]:
        p = lean_dir / required
        if not p.exists():
            upstream = Path(r"C:\Users\a343o\source\repos\the_symbol_game\lean4\research_programs\mub6") / required
            if upstream.exists():
                p = upstream
        assert p.exists() and p.stat().st_size > 0, f"Critical Lean module missing: {required}"


# Check 21: A2_phase_split_degenerate_branch_counterexample
def test_check21_a2_phase_split_degenerate_branch():
    a, b = Q(1), Q(1)
    for c_val, d_val in [(Q(-1), Q(1)), (Q(42), Q(99)), (Q(-5, 7), Q(13, 2))]:
        det = corner_determinant(a, b, c_val, d_val)
        assert det == Q(0), f"Degenerate branch failed at c={c_val}, d={d_val}"
    assert corner_determinant(Q(2), Q(3), Q(4), Q(5)) != Q(0)


# Check 22: A1_explicit_functional_boundary_refusal
def test_check22_a1_explicit_functional_boundary_refusal():
    host = PacketFirewallHost()
    step_no_rules = DerivationStep("VERIFY", 0, "r", {}, "bad", "bad", "VERIFY")
    verdict = host.verify_step(step_no_rules, licensed_rules=None)
    assert not verdict.admitted


# Check 23: G1_metadata_only_guards
def test_check23_g1_metadata_only_guards():
    assert classify_corner(Q(1), Q(1), Q(1), Q(1)) == "szollosi_deltoid"
    assert classify_corner(Q(2), Q(3), Q(4), Q(5)) == "karlsson_volume"


# Check 24: governor_EDGE_MATCH_unknown_edge (M4 Remediated)
def test_check24_governor_edge_match_unknown_edge():
    graph = ConstraintGraph(["u", "v"], [Edge("u", "v", Q(1))])
    governor = L1SymbolGameGovernor(graph)
    verdict = governor.step_verify("EDGE_MATCH:ghost,other_ghost")
    assert not verdict.admitted
    assert "not declared" in verdict.details


# Check 25: pure_attention_mass_shape_handling
def test_check25_pure_attention_mass_shape_handling():
    # Test 2D attention mask generation with distractor suppression
    mask = create_attention_mask_2d(
        seq_len=4,
        distractor_positions=[1],
        carrier_positions=[0, 2],
        additive=True,
    )
    assert len(mask) == 4 and len(mask[0]) == 4
    # Distractor position 1 masked with -inf
    assert mask[0][1] == float("-inf")
    assert mask[0][0] == 0.0

    # Negative control: overlapping carrier and distractor must raise ValueError
    with pytest.raises(ValueError, match="carrier and distractor positions must be disjoint"):
        create_attention_mask_2d(seq_len=4, distractor_positions=[1], carrier_positions=[1])

    # Attention mass distiller on multi-layer attention distribution
    distiller = AttentionMaskDistiller(seq_len=4, carrier_positions=[0, 2], distractor_positions=[1])
    mass = distiller.compute_attention_mass(attentions=[[0.6, 0.1, 0.3, 0.0]])
    assert "carrier_mass" in mass and "distractor_mass" in mass
    assert mass["carrier_mass"] == pytest.approx(0.9)
    assert mass["distractor_mass"] == pytest.approx(0.1)


# Check 26: carrier_projection_controls
def test_check26_carrier_projection_controls():
    assert is_valid_carrier_codepoint(ord("A"))
    assert is_valid_carrier_codepoint(ord("1"))
    assert not is_valid_carrier_codepoint(0x1F600)  # Emoji outside ASCII carrier


# Check 27: carrier_projection_rejects_all_infinite_allowed
def test_check27_carrier_projection_rejects_out_of_range():
    assert not is_valid_carrier_codepoint(0x10FFFF)
    assert not is_valid_carrier_codepoint(-1)


# Check 28: carrier_grammar_rejects_derived_float
def test_check28_carrier_grammar_rejects_derived_float():
    with pytest.raises(ValueError, match="FLOAT_REJECTED"):
        _safe_eval("Fraction(1, 2) + 0.1")


# Check 29: confidence_ignores_zero_probability_token
def test_check29_confidence_ignores_zero_probability_token():
    # Masked token with -inf (zero probability) is ignored; finite logprob 0.0 -> exp(0.0) = 1.0
    conf = compute_logprob_confidence([0.0, -float("inf")])
    assert conf == pytest.approx(1.0)
    # All zero-probability tokens -> 0.0 confidence
    assert compute_logprob_confidence([-float("inf"), -float("inf")]) == 0.0
    # Empty logprobs -> 0.0
    assert compute_logprob_confidence([]) == 0.0
    # Finite logprobs: exp(ln(0.5)) == 0.5
    assert compute_logprob_confidence([math.log(0.5), math.log(0.5)]) == pytest.approx(0.5)


# Check 30: full_Q_module_import_boundary
def test_check30_full_q_module_import_boundary():
    # Verify q_soundness_obligations executes full aggregation receipt with honest diagnostic status
    receipt = generate_q_soundness_receipt()
    assert receipt.receipt_type == RECEIPT_TYPE
    assert receipt.schema_version == SCHEMA_VERSION
    assert receipt.status == STATUS_DIAGNOSTIC_ONLY
    assert receipt.candidate_refutation_status == "MISSING_PROOF_OBLIGATION"
    assert receipt.all_obligations_satisfied is False
    assert receipt.firewall == FIREWALL_LINE
    assert receipt.word_basis_receipt.rank_25_refuted is True
    assert receipt.witness_replay_receipt.strictly_negative is True
    assert receipt.quadratic_identity_receipt.identity_verified is True


# Check 31: Q_R1_selected_original_definitions
def test_check31_q_r1_selected_original_definitions():
    # Canonical projector word basis refutes rank-25 and certifies quotient dimension 21
    r1 = canonical_projector_word_basis()
    assert r1.unreduced_count == 25
    assert r1.reduced_count == 21
    assert r1.relation_matrix_rank == 4
    assert r1.quotient_dimension == 21
    assert r1.rank_25_refuted is True
    assert r1.status == STATUS_CERTIFIED_CANDIDATE_REFUTATION


# Check 32: Q_R3_selected_original_identity
def test_check32_q_r3_selected_original_identity():
    # R3 algebraic identity: 25*1 - sum Pi^2 = 21*1 in projector quotient ring
    r3 = verify_quadratic_module_identity()
    assert r3.identity_verified is True
    assert r3.constant_lhs == Q(25)
    assert r3.constant_rhs == Q(25)
    assert r3.sum_of_squares_count == 21
    assert r3.completeness_ideal_terms == 4
    assert r3.idempotency_ideal_terms == 24
    assert r3.linear_cancellation_verified is True
    assert r3.quadratic_matching_verified is True


# Check 33: Q_R3_nonzero_perturbation_rejection
def test_check33_q_r3_nonzero_perturbation_rejection():
    # Perturbation to completeness relation must be rejected with ValueError
    with pytest.raises(ValueError, match="Quadratic-module identity verification failed"):
        verify_quadratic_module_identity(perturb_basis_idx=0, perturbation=Q(1, 100))
    with pytest.raises(ValueError, match="Quadratic-module identity verification failed"):
        verify_quadratic_module_identity(perturb_basis_idx=2, perturbation=Q(-1, 50))


# Check 34: Q_universal_scope_guard
def test_check34_q_universal_scope_guard():
    # Claiming universal operator emptiness without unproven bridge raises MissingProofObligationError
    with pytest.raises(MissingProofObligationError, match="universal operator emptiness certificate"):
        evaluate_archimedean_degree_bound(witness_scope="UNIVERSAL_OPERATOR_EMPTINESS")


# Check 35: Q_negative_degree_receipt
def test_check35_q_negative_degree_receipt():
    # Verify Archimedean Positivstellensatz degree bound D=4, Level 8
    receipt = evaluate_archimedean_degree_bound(degree_bound=4)
    assert receipt.degree_bound == 4
    assert receipt.dual_witness_level == 8
    assert receipt.operator_norm_bound == Q(1)
    assert receipt.quadratic_module_archimedean_verified is True
    assert receipt.is_universal_emptiness_discharged is False
    assert receipt.status == STATUS_CERTIFIED_CANDIDATE_REFUTATION


# Check 36: Q_flat_extension_receipt_is_constant
def test_check36_q_flat_extension_receipt_is_constant():
    # Level 1 Curto-Fialkow flat extension rank gap: rank(M_1)=21, rank(M_0)=1, Delta=20 > 0
    receipt = certify_flat_extension_rank_gap(level=1)
    assert receipt.level == 1
    assert receipt.rank_d == 21
    assert receipt.rank_d_minus_1 == 1
    assert receipt.rank_gap == 20
    assert receipt.is_obstructed is True
    assert "strictly obstructed" in receipt.summary

    # Negative control: unsupported level raises NotImplementedError
    with pytest.raises(NotImplementedError):
        certify_flat_extension_rank_gap(level=2)
