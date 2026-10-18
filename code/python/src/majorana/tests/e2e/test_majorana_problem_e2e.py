"""
End-to-End tests for The Majorana Problem monograph and claim ledger (MAJ-C1 .. MAJ-C18).
AuthorityEffect: None.
"""

import time
import numpy as np
import pytest

from majorana_evaluator import (
    build_tetron_carrier,
    compute_coset_weight,
    classify_residual,
    TrichotomyClass,
    verify_norm_equivalence,
    KitaevSweetSpotChain,
    DetectorAdequacyAudit,
    IsingFusionAlgebra,
    ParityAlgebraModel,
    pfaffian_z2_invariant,
    audit_legacy_carrier,
    OpenSystemMajoranaBraidModel,
    NonMarkovianBosonicBathModel,
    ContinuumCrossJunctionFemModel,
    F2CochainComplex,
    GF2Matrix,
    logical_representative,
)


def test_monograph_claims_e2e_verification_walk():
    """
    Executes the complete verification walk covering all 18 claims in the_majorana_problem_claim_ledger.md.
    """
    # -------------------------------------------------------------------------
    # 1. MAJ-C1 & MAJ-C10: The Microsoft Majorana Problem & Detector Inadequacy
    # -------------------------------------------------------------------------
    torus22 = build_tetron_carrier("torus", rows=2, cols=2)
    receipt_syn = DetectorAdequacyAudit.audit_syndrome_readout(torus22)
    assert receipt_syn.is_adequate is False
    assert receipt_syn.status == "DETECTOR_INADEQUATE"

    receipt_hom = DetectorAdequacyAudit.audit_homology_readout(torus22)
    assert receipt_hom.is_adequate is True
    assert receipt_hom.status == "DETECTOR_ADEQUATE"

    # -------------------------------------------------------------------------
    # 2. MAJ-C2 & MAJ-C3: GF(2) Residual Trichotomy and Polynomial Decidability
    # -------------------------------------------------------------------------
    torus = build_tetron_carrier("torus", rows=2, cols=2)
    assert torus.complex.is_nilpotent() is True

    # Check exact coboundary (MAJ-C2 Exact)
    coboundary = torus.complex.d0.to_array()[:, 0]
    status_exact, _ = classify_residual(torus.complex, coboundary)
    assert status_exact == TrichotomyClass.EXACT

    # Check open obstruction (MAJ-C2 OpenObstruction)
    single_edge = np.zeros(torus.complex.n1, dtype=int)
    single_edge[0] = 1
    status_open, meta_open = classify_residual(torus.complex, single_edge)
    assert status_open == TrichotomyClass.OPEN_OBSTRUCTION
    assert meta_open["syndrome_weight"] > 0

    # -------------------------------------------------------------------------
    # 3. MAJ-C4: Boundary Nilpotency Refusal
    # -------------------------------------------------------------------------
    broken_d1 = torus.complex.d1.to_array().copy()
    broken_d1[0, 0] ^= 1  # Guaranteed (broken_d1 @ d0) != 0 mod 2
    broken_complex = F2CochainComplex(
        n0=torus.complex.n0,
        n1=torus.complex.n1,
        n2=torus.complex.n2,
        d0=torus.complex.d0,
        d1=GF2Matrix.from_array(broken_d1),
    )
    assert broken_complex.is_nilpotent() is False
    status_refused, meta_refused = classify_residual(broken_complex, single_edge)
    assert status_refused == TrichotomyClass.REPRESENTATION_INVALID
    assert "d1 * d0 != 0" in meta_refused["reason"]

    # -------------------------------------------------------------------------
    # 4. MAJ-C5: Surface Toy Scope Fence (Carrier distance and cell counts)
    # -------------------------------------------------------------------------
    assert torus.code_distance == 2
    assert torus.complex.n0 == 4
    assert torus.complex.n1 == 8
    assert torus.complex.n2 == 4

    # -------------------------------------------------------------------------
    # 5. MAJ-C6: 1D Kitaev Wire Import & MZM Boundary Decoupling
    # -------------------------------------------------------------------------
    kitaev = KitaevSweetSpotChain(length=6)
    assert kitaev.is_boundary_isolated() is True
    assert kitaev.boundary_modes() == (0, 11)

    # -------------------------------------------------------------------------
    # 6. MAJ-C7: Ising Anyon Fusion Rules & Yang-Baxter Braiding
    # -------------------------------------------------------------------------
    assert IsingFusionAlgebra.verify_quantum_dimensions() is True
    assert IsingFusionAlgebra.verify_yang_baxter_braid() is True

    # -------------------------------------------------------------------------
    # 7. MAJ-C8: Parity Observable Algebra & Sector Splitting
    # -------------------------------------------------------------------------
    parity_model = ParityAlgebraModel(num_modes=2)
    assert parity_model.verify_involutory_and_hermitian() is True

    # -------------------------------------------------------------------------
    # 8. MAJ-C9: Pfaffian Topological Sign Invariant
    # -------------------------------------------------------------------------
    nu_topo = pfaffian_z2_invariant(mu=0.5, t=1.0, delta=1.0, L=4)
    nu_triv = pfaffian_z2_invariant(mu=2.5, t=1.0, delta=1.0, L=4)
    assert nu_topo == -1
    assert nu_triv == 1

    # -------------------------------------------------------------------------
    # 9. MAJ-C11 & MAJ-C12: Measured Tetron-Array Homology
    # -------------------------------------------------------------------------
    disk = build_tetron_carrier("disk", 2, 2)
    assert disk.h1_dim == 0
    cyl = build_tetron_carrier("cylinder", 2, 2)
    assert cyl.h1_dim == 1
    tor = build_tetron_carrier("torus", 2, 2)
    assert tor.h1_dim == 2

    # -------------------------------------------------------------------------
    # 10. MAJ-C13: Retraction of Legacy Carrier
    # -------------------------------------------------------------------------
    audit_leg = audit_legacy_carrier()
    assert audit_leg["legacy_supports_logical_classes"] is False
    assert audit_leg["torus_supports_logical_classes"] is True

    # -------------------------------------------------------------------------
    # 11. MAJ-C14: Toric Code Distance and Additive Diagonal Weight
    # -------------------------------------------------------------------------
    t34 = build_tetron_carrier("torus", 3, 4)
    assert t34.code_distance == 3

    col_edges = logical_representative(t34, axis="column", index=0)
    row_edges = logical_representative(t34, axis="row", index=0)
    diag_edges = row_edges ^ col_edges

    w_col, _ = compute_coset_weight(t34.complex, col_edges)
    w_row, _ = compute_coset_weight(t34.complex, row_edges)
    w_diag, _ = compute_coset_weight(t34.complex, diag_edges)

    assert w_col == 3
    assert w_row == 4
    assert w_diag == 7  # 3 + 4 = 7

    # -------------------------------------------------------------------------
    # 12. MAJ-C15: Syndrome Decoding Complexity and Budget Capping
    # -------------------------------------------------------------------------
    _, exact_capped = compute_coset_weight(t34.complex, diag_edges, budget_max=8)
    assert exact_capped is False

    # -------------------------------------------------------------------------
    # 13. MAJ-C16: Benchmark Verification on 6x6 Torus
    # -------------------------------------------------------------------------
    t66 = build_tetron_carrier("torus", rows=6, cols=6)
    res_bench = np.zeros(t66.complex.n1, dtype=int)
    res_bench[0] = 1
    t0 = time.perf_counter()
    st_bench, _ = classify_residual(t66.complex, res_bench)
    elapsed = time.perf_counter() - t0
    assert st_bench == TrichotomyClass.OPEN_OBSTRUCTION
    assert elapsed < 0.1

    # -------------------------------------------------------------------------
    # 14. MAJ-C17: Norm Equivalence on Binary Vectors
    # -------------------------------------------------------------------------
    assert verify_norm_equivalence(diag_edges) is True

    # -------------------------------------------------------------------------
    # 15. MAJ-C18: Continuous-to-Discrete Transfer Bound under Open-System Dynamics
    # -------------------------------------------------------------------------
    open_model = OpenSystemMajoranaBraidModel(delta=1.0, gamma_qp=0.02, length_over_xi=6.0)
    receipt = open_model.audit_transfer(braid_time=3.0)
    assert receipt.is_positive_lower_bounded is True
    assert receipt.status == "TRANSFER_OBSTRUCTED_NONZERO_DEFECT"
    assert receipt.trace_defect > 0.0
    assert receipt.minimum_defect > 0.0

    # -------------------------------------------------------------------------
    # 16. MAJ-C19: Non-Markovian Memory-Kernel Transfer Bounds
    # -------------------------------------------------------------------------
    sub_bath = NonMarkovianBosonicBathModel(spectral_index=0.5, coupling_alpha=0.01)
    super_bath = NonMarkovianBosonicBathModel(spectral_index=2.0, coupling_alpha=0.01)
    rcpt_sub = sub_bath.audit_transfer()
    rcpt_super = super_bath.audit_transfer()

    assert rcpt_sub.is_sub_ohmic is True
    assert abs(rcpt_sub.scaling_exponent_beta - (4.0 / 7.0)) < 1e-10
    assert rcpt_super.is_super_ohmic is True
    assert abs(rcpt_super.scaling_exponent_beta - 0.40) < 1e-10
    assert rcpt_sub.is_positive_lower_bounded is True
    assert rcpt_super.is_positive_lower_bounded is True
    assert rcpt_sub.minimum_defect > 0.0
    assert rcpt_super.minimum_defect > 0.0

    # -------------------------------------------------------------------------
    # 17. MAJ-C20: Continuum Finite-Element Multi-Terminal Cross-Junction Bounds
    # -------------------------------------------------------------------------
    fem_model = ContinuumCrossJunctionFemModel(
        num_terminals=4,
        arm_lengths=[6.0, 6.0, 6.0, 6.0],
        disorder_strength=0.2,
        critical_disorder=0.8,
    )
    fem_rcpt = fem_model.audit_transfer()

    assert fem_rcpt.num_terminals == 4
    assert fem_rcpt.effective_gap_delta_eff > 0.0
    assert fem_rcpt.is_topological_phase_preserved is True
    assert fem_rcpt.is_positive_lower_bounded is True
    assert fem_rcpt.status == "TRANSFER_OBSTRUCTED_MULTITERMINAL"
    assert fem_rcpt.minimum_defect > 0.0

