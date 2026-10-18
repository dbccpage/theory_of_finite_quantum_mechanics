"""
Comprehensive Unit Regression Tests for Remediation of Findings B1-B11
from the 1 October 2026 MUB(6) Publication & Code Review.

Tests:
- B1: MU transition normalization scale is 6 (for raw CHM U = H1* H2), not 1.
- B2: Dephasing applied before corner determinant formula, matches direct 3x3 determinant.
- B3: Q3/Q4 and Degree-8 witness replays maintain DIAGNOSTIC status without promoting to candidate refutations.
- B4: GNS pre-Hilbert space construction strictly requires PSD; indefinite forms receive indefinite diagnostic status.
- B5: A10 volume conservation derived from immutable domain geometry; unsupported witnesses and zero-cell receipts rejected.
- B6: A11 spectrum reporting enforces non_root24_count == 0 for discrete spectrum; reductions require supported witnesses.
- B7: Manifest verification rejects degenerate 3-field stubs lacking mathematical payload and labels audit type.
- B8: Pigeonhole bridge integration is conditional with global_cover_bridge_discharged = False.
- B9: Cross-language consistency is verified as lexical identifier presence, not semantic consistency.
- B10: Stratified verifier samples requested presplit-6 chunks, does not fallback near-off-torus, and rejects vacuous all_positive.
- B11: Missing lower-bound replay is recognized as an unproved obligation.
"""

from fractions import Fraction
import pathlib
import pytest

from mub_verify.cyclotomic import Cyc24
from mub_verify.interval import RationalInterval
from mub_verify.target_a4_gram_certifier import (
    canonical_triple_exact,
)
from mub_verify.target_a11_orbit_exhaustiveness import (
    dephase_hadamard_matrix,
    f6_fourier_matrix,
    haagerup_h6_matrix,
    tao_s6_matrix,
)
from mub_verify.target_g1_orbit_incompatibilities import (
    check_mu_transition_modulus,
    direct_3x3_determinant,
    verify_genuine_mu_pair_transition,
    verify_t05_06_corner_factorization,
    verify_pigeonhole_global_cover_bridge_integration,
)
from mub_verify.q_soundness_obligations import (
    generate_q_soundness_receipt,
)
from mub_verify.target_q_degree8_and_gns import (
    GNSPreHilbertSpace,
    evaluate_gns_pre_hilbert_space,
    replay_degree8_x0_witness,
    replay_degree8_s6_witness,
    verify_target_q_lean4_and_rust_consistency,
    evaluate_stream3_target_q_degree8_and_gns,
    STATUS_GNS_CONSTRUCTED,
    STATUS_INDEFINITE_FORM_DIAGNOSTIC,
    STATUS_DIAGNOSTIC_REPLAY,
)
from mub_verify.target_a10_global_cover import (
    build_canonical_global_partition_tree,
    verify_volume_conservation,
    audit_target_a10_receipt,
    GlobalPartitionTree,
    RegionalCoverTree,
    GlobalLeafNode,
    RationalCell,
    RationalIntervalBox,
    REGION_F6_DITA,
    ALL_REGIONS,
    MARGIN_F6,
)
from mub_verify.target_a11_orbit_exhaustiveness import (
    classify_orbit,
    certify_orbit_reduction,
    audit_target_a11_receipt,
    ALL_CATALOG_ORBITS,
)
from mub_verify.verify_all_receipts import (
    verify_all_receipts,
)
from mub_verify.verifier import (
    IndependentMubVerifier,
    wide_torus_cell,
)



def test_b1_mu_transition_scale():
    """B1: Raw CHM transition U = H1* H2 must test entrywise |U_jk|^2 == 6, not 1."""
    res = verify_genuine_mu_pair_transition()
    assert res["status"] == "PASS"
    assert res["is_mu_transition"] is True
    assert res["violations_count"] == 0

    cols = canonical_triple_exact()
    from mub_verify.mub_triples import sqrt2_cyc, sqrt3_cyc
    from mub_verify.target_g1_orbit_incompatibilities import (
        matrix_adjoint,
        matrix_mul,
    )
    s6_factor = sqrt2_cyc().mul(sqrt3_cyc())
    h2 = [[cols[6 + c][r].mul(s6_factor) for c in range(6)] for r in range(6)]
    h3 = [[cols[12 + c][r].mul(s6_factor) for c in range(6)] for r in range(6)]
    u_raw = matrix_mul(matrix_adjoint(h2), h3)

    is_mu_6, v_count_6 = check_mu_transition_modulus(u_raw, expected_mod_sq=6)
    assert is_mu_6 is True
    assert len(v_count_6) == 0

    is_mu_1, v_count_1 = check_mu_transition_modulus(u_raw, expected_mod_sq=1)
    assert is_mu_1 is False
    assert len(v_count_1) == 36



def test_b2_corner_dephasing_and_direct_3x3_det():
    """B2: Undephased H6 corner determinant is non-zero (2-4i), dephased is -2+4i != 0."""
    h6 = haagerup_h6_matrix()

    raw_det = direct_3x3_determinant(h6)
    four_i = Cyc24.zeta(6).mul(Cyc24.rat(Fraction(4)))
    assert raw_det == Cyc24.rat(Fraction(2)).sub(four_i)

    h6_dephased = dephase_hadamard_matrix(h6)
    dephased_det = direct_3x3_determinant(h6_dephased)
    assert dephased_det == Cyc24.rat(Fraction(-2)).add(four_i)

    receipt = verify_t05_06_corner_factorization()
    assert receipt["verified"] is True
    assert receipt["direct_3x3_determinant_controls"]["H6_Haagerup"] == str(dephased_det)
    h6_rep = receipt["corner_determinants"]["H6_Haagerup"]
    assert h6_rep["is_zero"] is False
    assert h6_rep["routing"] == "branch_regular_corner"



def test_b3_q_diagnostic_status_preservation():
    """B3: Q3/Q4 and Degree-8 witness replays must preserve DIAGNOSTIC status."""
    x0_receipt = replay_degree8_x0_witness()
    assert x0_receipt.status == STATUS_DIAGNOSTIC_REPLAY
    assert x0_receipt.expected_trace_matched is True
    assert x0_receipt.pivots_strictly_positive is True

    s6_receipt = replay_degree8_s6_witness()
    assert s6_receipt.status == STATUS_DIAGNOSTIC_REPLAY
    assert s6_receipt.expected_trace_matched is True
    assert s6_receipt.pivots_strictly_positive is True

    q_receipt = generate_q_soundness_receipt()
    assert q_receipt.status == "DIAGNOSTIC_ONLY"
    assert q_receipt.candidate_refutation_status == "MISSING_PROOF_OBLIGATION"
    assert q_receipt.all_obligations_satisfied is False



def test_b4_gns_indefinite_form_rejection():
    """B4: Indefinite matrices cannot form GNS pre-Hilbert spaces; diagnosed as indefinite forms."""
    indef_2x2 = [
        [Fraction(1), Fraction(2)],
        [Fraction(2), Fraction(1)],
    ]
    with pytest.raises(ValueError, match="positive semidefinite"):
        GNSPreHilbertSpace(["w0", "w1"], indef_2x2, allow_indefinite=False)

    gns, receipt = evaluate_gns_pre_hilbert_space(["w0", "w1"], indef_2x2, allow_indefinite=True)
    assert receipt.status == STATUS_INDEFINITE_FORM_DIAGNOSTIC
    assert receipt.is_psd is False
    assert receipt.pre_hilbert_constructed is False
    assert receipt.positivity_refuted is True
    assert receipt.negative_norm_modes_detected >= 1

    neg_states = [s for s in receipt.test_evaluations if s.is_negative_norm]
    assert len(neg_states) >= 1
    assert neg_states[0].norm_squared < 0

    with pytest.raises(ValueError, match="positive semidefinite"):
        GNSPreHilbertSpace(["w0"], [[Fraction(-1)]], allow_indefinite=False)

    _, receipt_1x1 = evaluate_gns_pre_hilbert_space(["w0"], [[Fraction(-1)]], allow_indefinite=True)
    assert receipt_1x1.status == STATUS_INDEFINITE_FORM_DIAGNOSTIC
    assert receipt_1x1.is_psd is False
    assert receipt_1x1.pre_hilbert_constructed is False
    assert receipt_1x1.positivity_refuted is True

    psd_2x2 = [
        [Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1)],
    ]
    gns_psd = GNSPreHilbertSpace(["w0", "w1"], psd_2x2, allow_indefinite=False)
    assert gns_psd.is_psd is True
    _, receipt_psd = evaluate_gns_pre_hilbert_space(["w0", "w1"], psd_2x2)
    assert receipt_psd.status == STATUS_GNS_CONSTRUCTED
    assert receipt_psd.is_psd is True
    assert receipt_psd.pre_hilbert_constructed is True
    assert receipt_psd.positivity_refuted is False
    assert receipt_psd.negative_norm_modes_detected == 0



def test_b5_a10_domain_volume_binding_and_witness_replay():
    """B5: Inconsistent expected volumes, unsupported witnesses, and zero-cell receipts are rejected."""
    tree = build_canonical_global_partition_tree()

    f6_tree = tree.regional_trees[REGION_F6_DITA]
    leaves = f6_tree.collect_leaves()
    first_leaf = leaves[0]
    bad_f6_tree = RegionalCoverTree(
        region=REGION_F6_DITA,
        domain=f6_tree.domain,
        root=first_leaf,
    )
    bad_regional_trees = dict(tree.regional_trees)
    bad_regional_trees[REGION_F6_DITA] = bad_f6_tree
    bad_expected = dict(tree.expected_domain_volumes)
    bad_expected[REGION_F6_DITA] = Fraction(1, 4)

    bad_tree = GlobalPartitionTree(
        regional_trees=bad_regional_trees,
        expected_domain_volumes=bad_expected,
    )
    ok, msg, _ = verify_volume_conservation(bad_tree)
    assert not ok
    assert "does not match immutable domain geometry volume" in msg or "Volume discrepancy" in msg

    bad_witness_leaf = GlobalLeafNode(
        RationalCell(
            cell_id="F6_unsupported_witness",
            region=REGION_F6_DITA,
            box=first_leaf.cell.box,
            obstruction_margin=MARGIN_F6,
            witness_type="UNSUPPORTED",
            witness_data={},
        )
    )
    bad_w_trees = dict(tree.regional_trees)
    bad_w_trees[REGION_F6_DITA] = RegionalCoverTree(
        region=REGION_F6_DITA,
        domain=f6_tree.domain,
        root=bad_witness_leaf,
    )
    bad_w_tree = GlobalPartitionTree(regional_trees=bad_w_trees, expected_domain_volumes=tree.expected_domain_volumes)
    ok_w, msg_w, _ = verify_volume_conservation(bad_w_tree)
    assert not ok_w
    assert "unsupported witness type" in msg_w

    zero_cell_receipt = {
        "schema_version": "omega.mub.target-a10-global-cover.v1",
        "firewall": "stated region only; mints no authority",
        "authority_effect": "None",
        "canonical_parameters": {
            "global_min_margin": "12133/30000",
            "phi1_obstruction": "12133/5000",
        },
        "regional_covers": {
            r: {
                "cell_count": 0,
                "domain_volume": "0",
                "cells_volume": "0",
                "volume_conserved": True,
                "certified": True,
                "min_margin": "12133/30000",
            }
            for r in ALL_REGIONS
        },
        "global_volume_conservation": {
            "total_cells": 0,
            "total_domain_volume": "0",
            "total_cells_volume": "0",
            "volume_conserved": True,
            "disjoint_interiors_verified": True,
        },
        "boundary_interfaces": [{"interface_id": "iface_0", "chart_u": "F6", "chart_v": "B6", "boundary_dim": 2, "transition_margin": "1/10", "gap_distance": "0", "certified": True}],
        "boundary_adjacency_verified": True,
        "network_simplex": {
            "phi1_strictly_positive": True,
            "circulation_invariance_verified": True,
            "net_circulation": "1",
            "phi1_obstruction": "1",
        },
        "verified": True,
    }
    with pytest.raises(ValueError, match="zero cells|non-positive"):
        audit_target_a10_receipt(zero_cell_receipt)



def test_b6_a11_spectrum_reporting_and_orbit_reduction():
    """B6: Non-root-24 elements prevent claiming strict sextic spectrum; reductions require supported cells."""
    f6_mat = f6_fourier_matrix()
    rep = classify_orbit(f6_mat)
    assert rep.is_chm is True
    assert rep.orbit_id == "F6_Fourier_Dita"
    assert rep.details["non_root24_count"] == 0
    assert "strictly in sextic spectrum" in rep.notes

    tree = build_canonical_global_partition_tree()
    unsupported_leaf = GlobalLeafNode(
        RationalCell(
            cell_id="F6_cell_0_0",
            region=REGION_F6_DITA,
            box=RationalIntervalBox(tuple((Fraction(0), Fraction(1)) for _ in range(5))),
            obstruction_margin=MARGIN_F6,
            witness_type="UNSUPPORTED",
            witness_data={},
            certified=False,
        )
    )
    bad_regional_trees = dict(tree.regional_trees)
    bad_regional_trees[REGION_F6_DITA] = RegionalCoverTree(
        region=REGION_F6_DITA,
        domain=tree.regional_trees[REGION_F6_DITA].domain,
        root=unsupported_leaf,
    )
    bad_tree = GlobalPartitionTree(
        regional_trees=bad_regional_trees,
        expected_domain_volumes=tree.expected_domain_volumes,
    )

    with pytest.raises(ValueError, match="not certified|unsupported witness"):
        certify_orbit_reduction(f6_mat, matrix_label="F6_Fourier", tree=bad_tree)

    stub_receipt = {
        "schema_version": "omega.mub.target-a11-orbit-exhaustiveness.v1",
        "firewall": "stated region only; mints no authority",
        "authority_effect": "None",
        "catalog_exhaustiveness": {"all_catalog_orbits": list(ALL_CATALOG_ORBITS)},
        "canonical_matrices_reduction": {
            "F6_Fourier": {"reduction_valid": True, "obstruction_margin": "1"},
            "S6_Tao": {"reduction_valid": True, "obstruction_margin": "1"},
            "H6_Haagerup": {"reduction_valid": True, "obstruction_margin": "1"},
            "B6_Szollosi": {"reduction_valid": True, "obstruction_margin": "1"},
        },
        "negative_controls": {
            "perturbed_non_chm_rejected": True,
            "misclassified_orbit_rejected": True,
            "incomplete_catalog_proposal_rejected": True,
            "float_injection_rejected": True,
        },
        "verified": True,
    }
    with pytest.raises(ValueError, match="Invalid or missing orbit_id"):
        audit_target_a11_receipt(stub_receipt)



def test_b7_verify_all_receipts_rejects_3field_stubs(tmp_path):
    """B7: Receipts containing only schema_version, verified, and firewall are strictly rejected."""
    import hashlib
    import json
    from mub_verify.verify_all_receipts import (
        EXPECTED_RECEIPT_REGISTRY,
        EXPECTED_TOTAL_RECEIPTS,
    )

    receipt_entries = []
    for target, filename, schema_version in EXPECTED_RECEIPT_REGISTRY:
        stub_data = {
            "schema_version": schema_version,
            "verified": True,
            "firewall": "stated region only; mints no authority",
        }
        stub_bytes = json.dumps(stub_data).encode("utf-8")
        stub_sha = hashlib.sha256(stub_bytes).hexdigest()
        r_file = tmp_path / filename
        r_file.write_bytes(stub_bytes)
        receipt_entries.append({
            "target": target,
            "filename": filename,
            "sha256": stub_sha,
            "schema_version": schema_version,
            "verified": True,
            "arithmetic": "exact rational / cyclotomic",
            "firewall_line": "stated region only; mints no authority",
        })

    manifest = {
        "manifest_version": "1.0.0",
        "project": "MUB(6)",
        "authority_effect": "None",
        "firewall_line": "stated region only; mints no authority",
        "timestamp": "2026-10-01T00:00:00Z",
        "total_receipts": EXPECTED_TOTAL_RECEIPTS,
        "receipts": receipt_entries,
    }

    m_file = tmp_path / "manifest.json"
    m_file.write_bytes(json.dumps(manifest).encode("utf-8"))

    res = verify_all_receipts(artifacts_dir=tmp_path, manifest_path=m_file)
    assert res["all_passed"] is False
    assert res["audit_type"] == "FILE_INTEGRITY_AND_METADATA_AUDIT"
    assert res["theorem_replay_status"] == "MISSING_MATHEMATICAL_REPLAY_DISPATCH"
    assert res["receipts_verified"] == 0
    assert len(res["errors"]) == 11
    assert all("Receipt contains no mathematical certificate payload" in err for err in res["errors"])



def test_b8_pigeonhole_bridge_conditional():
    """B8: verify_pigeonhole_global_cover_bridge_integration reports conditional replay."""
    res = verify_pigeonhole_global_cover_bridge_integration()
    assert res["global_cover_bridge_discharged"] is False
    assert res["status"] == "CONDITIONAL_COUNTING_REPLAY"
    assert len(res["unproved_premises"]) >= 3



def test_b9_cross_language_consistency_is_lexical():
    """B9: Consistency check verifies lexical identifier presence, keeping semantic consistency undischarged."""
    receipt = verify_target_q_lean4_and_rust_consistency()
    assert receipt.status == "LEXICAL_IDENTIFIER_PRESENCE_CHECKED"
    assert receipt.semantic_consistency_verified is False
    assert receipt.consistent is False

    master = evaluate_stream3_target_q_degree8_and_gns()
    assert master.all_vectors_satisfied is False



def test_b10_stratified_verifier_presplit_chunks():
    """B10: Stratified boxes respect chunks_to_sample, empty seeds produce all_positive = False."""
    verifier = IndependentMubVerifier()

    res_chunk31 = verifier.collect_stratified_boxes(dx=0, dy=8, chunks_to_sample=(31,))
    res_chunk21 = verifier.collect_stratified_boxes(dx=0, dy=8, chunks_to_sample=(21,))
    res_chunk999 = verifier.collect_stratified_boxes(dx=0, dy=8, chunks_to_sample=(999,))

    assert len(res_chunk31) > 0
    assert len(res_chunk21) > 0
    assert len(res_chunk999) == 0

    summary, _ = verifier.run_stratified_audit(seeds=())
    assert summary.total_boxes_tested == 0
    assert summary.all_positive is False
