"""
Integration tests for tetron array surface codes, code distance, and Kitaev MZM boundary isolation.
AuthorityEffect: None.
"""

import numpy as np
import pytest

from majorana_evaluator import (
    build_tetron_carrier,
    compute_coset_weight,
    classify_residual,
    TrichotomyClass,
    KitaevSweetSpotChain,
)


def test_tetron_homology_dimensions():
    disk = build_tetron_carrier("disk", rows=2, cols=2)
    assert disk.complex.is_nilpotent() is True
    assert disk.h1_dim == 0
    assert disk.code_distance is None

    cylinder = build_tetron_carrier("cylinder", rows=2, cols=3)
    assert cylinder.complex.is_nilpotent() is True
    assert cylinder.h1_dim == 1
    assert cylinder.code_distance == 2 + 1

    torus = build_tetron_carrier("torus", rows=3, cols=4)
    assert torus.complex.is_nilpotent() is True
    assert torus.h1_dim == 2
    assert torus.code_distance == min(3, 4)


def test_torus_per_class_minimum_weights():
    torus = build_tetron_carrier("torus", rows=3, cols=4)
    from majorana_evaluator import logical_representative

    col_edges = logical_representative(torus, axis="column", index=0)
    status_col, _ = classify_residual(torus.complex, col_edges)
    assert status_col == TrichotomyClass.CLOSED_RESIDUAL
    min_w_col, exact_col = compute_coset_weight(torus.complex, col_edges)
    assert exact_col is True
    assert min_w_col == 3

    row_edges = logical_representative(torus, axis="row", index=0)
    status_row, _ = classify_residual(torus.complex, row_edges)
    assert status_row == TrichotomyClass.CLOSED_RESIDUAL
    min_w_row, exact_row = compute_coset_weight(torus.complex, row_edges)
    assert exact_row is True
    assert min_w_row == 4

    diag_edges = row_edges ^ col_edges
    status_diag, _ = classify_residual(torus.complex, diag_edges)
    assert status_diag == TrichotomyClass.CLOSED_RESIDUAL
    min_w_diag, exact_diag = compute_coset_weight(torus.complex, diag_edges)
    assert exact_diag is True
    assert min_w_diag == 7


def test_coset_weight_budget_capping():
    torus = build_tetron_carrier("torus", rows=4, cols=4)
    res = np.zeros(torus.complex.n1, dtype=int)
    res[0] = 1
    wt, exact = compute_coset_weight(torus.complex, res, budget_max=16)
    assert exact is False


def test_kitaev_sweet_spot_boundary_isolation():
    chain = KitaevSweetSpotChain(length=5)
    assert chain.is_boundary_isolated() is True

    gamma_l, gamma_r = chain.boundary_modes()
    assert gamma_l == 0
    assert gamma_r == 9

    bulk_pairs = chain.bulk_pairs()
    assert len(bulk_pairs) == 4
    for u, v in bulk_pairs:
        assert u not in (0, 9)
        assert v not in (0, 9)


def test_detector_adequacy_syndrome_vs_homology():
    """Verifies Claims MAJ-C1 & MAJ-C10: Syndrome-only detector inadequacy vs homology readout adequacy."""
    from majorana_evaluator import DetectorAdequacyAudit

    torus = build_tetron_carrier("torus", rows=2, cols=2)
    receipt_syn = DetectorAdequacyAudit.audit_syndrome_readout(torus)
    assert receipt_syn.is_adequate is False
    assert receipt_syn.status == "DETECTOR_INADEQUATE"
    assert receipt_syn.unresolved_pairs == 1

    receipt_hom = DetectorAdequacyAudit.audit_homology_readout(torus)
    assert receipt_hom.is_adequate is True
    assert receipt_hom.status == "DETECTOR_ADEQUATE"
    assert receipt_hom.unresolved_pairs == 0


def test_audit_legacy_carrier_retraction():
    """Verifies Claim MAJ-C13: Legacy carrier retraction due to identically trivial homology."""
    from majorana_evaluator import audit_legacy_carrier

    audit = audit_legacy_carrier()
    assert audit["legacy_supports_logical_classes"] is False
    assert audit["torus_supports_logical_classes"] is True
    assert all(dim == 0 for dim in audit["legacy_h1_dimensions"].values())
    assert all(dim == 2 for dim in audit["torus_h1_dimensions"].values())

