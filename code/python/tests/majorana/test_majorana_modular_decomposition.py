"""
test_majorana_modular_decomposition.py — Verification of modular decomposed Majorana components.

Validates that:
1. `majorana_f2_trichotomy` functions independently of the monolithic evaluator.
2. `majorana_mzm_ising` functions independently.
3. `majorana_transfer_bounds` functions independently.
4. `majorana_evaluator` successfully re-exports all symbols from the modules.
"""

from __future__ import annotations

import numpy as np
import pytest

from majorana.majorana_f2_trichotomy import (
    GF2Matrix,
    F2CochainComplex,
    TrichotomyClass,
    build_tetron_carrier,
    classify_residual,
    compute_coset_weight,
    logical_representative,
    verify_norm_equivalence,
)
from majorana.majorana_mzm_ising import (
    IsingFusionAlgebra,
    KitaevSweetSpotChain,
    ParityAlgebraModel,
    audit_legacy_carrier,
    compute_skew_pfaffian,
    pfaffian_z2_invariant,
)
from majorana.majorana_transfer_bounds import (
    ContinuumCrossJunctionFemModel,
    DetectorAdequacyAudit,
    NonMarkovianBosonicBathModel,
    OpenSystemMajoranaBraidModel,
)
from majorana.majorana_evaluator import (
    GF2Matrix as ReexportedGF2Matrix,
    IsingFusionAlgebra as ReexportedIsing,
    OpenSystemMajoranaBraidModel as ReexportedOpenSystem,
)


def test_modular_f2_trichotomy_direct() -> None:
    carrier = build_tetron_carrier("torus", rows=3, cols=4)
    assert carrier.h1_dim == 2
    assert carrier.code_distance == 3

    w_col = logical_representative(carrier, axis="column", index=0)
    assert len(w_col) == carrier.complex.n1

    cls, info = classify_residual(carrier.complex, w_col)
    assert cls == TrichotomyClass.CLOSED_RESIDUAL
    assert info["homology_class"] == "non_trivial"

    wt, exact = compute_coset_weight(carrier.complex, w_col)
    assert exact is True
    assert wt == 3
    assert verify_norm_equivalence(w_col) is True


def test_modular_mzm_ising_direct() -> None:
    chain = KitaevSweetSpotChain(length=6)
    assert chain.boundary_modes() == (0, 11)
    assert chain.is_boundary_isolated() is True

    assert IsingFusionAlgebra.verify_quantum_dimensions() is True
    assert IsingFusionAlgebra.verify_yang_baxter_braid() is True

    pam = ParityAlgebraModel(num_modes=2)
    assert pam.verify_involutory_and_hermitian() is True

    skew = np.array([
        [0.0, 2.0],
        [-2.0, 0.0]
    ])
    assert compute_skew_pfaffian(skew) == 2.0

    sign_topo = pfaffian_z2_invariant(mu=0.5, t=1.0, delta=1.0, L=4)
    sign_triv = pfaffian_z2_invariant(mu=3.0, t=1.0, delta=1.0, L=4)
    assert sign_topo == -1
    assert sign_triv == 1

    audit = audit_legacy_carrier()
    assert audit["legacy_supports_logical_classes"] is False
    assert audit["torus_supports_logical_classes"] is True


def test_modular_transfer_bounds_direct() -> None:
    model = OpenSystemMajoranaBraidModel(delta=1.0, gamma_qp=0.01)
    receipt = model.audit_transfer(braid_time=50.0)
    assert receipt.is_positive_lower_bounded is True
    assert receipt.minimum_defect > 0.0

    bath = NonMarkovianBosonicBathModel(spectral_index=0.5, coupling_alpha=0.01)
    bath_receipt = bath.audit_transfer()
    assert bath_receipt.is_sub_ohmic is True
    assert bath_receipt.minimum_defect > 0.0

    carrier = build_tetron_carrier("torus", rows=2, cols=2)
    det_receipt = DetectorAdequacyAudit.audit_syndrome_readout(carrier)
    assert det_receipt.is_adequate is False

    fem = ContinuumCrossJunctionFemModel(num_terminals=4, disorder_strength=0.1)
    fem_receipt = fem.audit_transfer()
    assert fem_receipt.is_topological_phase_preserved is True
    assert fem_receipt.minimum_defect > 0.0


def test_modular_facade_parity() -> None:
    assert ReexportedGF2Matrix is GF2Matrix
    assert ReexportedIsing is IsingFusionAlgebra
    assert ReexportedOpenSystem is OpenSystemMajoranaBraidModel
