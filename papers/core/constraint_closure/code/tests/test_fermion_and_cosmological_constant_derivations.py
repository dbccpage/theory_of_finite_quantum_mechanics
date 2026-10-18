"""
Unit tests for Fermion Mass Spectrum and Cosmological Constant L1 Derivations (GR-002).
Verifies exact Lean 4 proof witness bridges, spectral eigenvalues, and residual density output structures.
AuthorityEffect: None.
"""

import sys
from pathlib import Path
import pytest


from l1_topological_defects import (
    derive_fermion_mass_spectrum_lggr,
    derive_cosmological_constant_residual,
    evaluate_c3_hodge_split_inflation,
)
from constraint_closure_l1_structure import ConstraintClosureL1Structure


def test_c3_hodge_split_inflation_sharp_ceiling():
    res = evaluate_c3_hodge_split_inflation(cochain_omega=[0.0, 1.0, 0.0])

    assert res["r_split"] == pytest.approx(7.0 / 3.0, abs=1e-12)
    assert res["r_rep"] == pytest.approx(1.0, abs=1e-12)
    assert res["phi_1"] == pytest.approx(1.0, abs=1e-12)
    assert res["is_sharp_c3_ceiling"] is True
    assert res["authority"] == "None"


def test_fermion_mass_spectrum_lggr_witness_and_structure():
    res = derive_fermion_mass_spectrum_lggr(cochain_1cycle=[1.0, 1.0, 1.0], v_ew_gev=246.0)

    assert res["lean4_proof_witness"] == "OmegaCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction"
    assert len(res["z3_spectral_eigenvalues"]) == 3
    assert len(res["raw_residual_mass_gaps"]) == 3
    assert res["raw_residual_mass_gaps"][0] == pytest.approx(0.0, abs=1e-12)
    assert res["raw_residual_mass_gaps"][1] > 0.0
    assert res["raw_residual_mass_gaps"][2] > 0.0
    assert res["scaled_masses_gev"] is not None
    assert res["is_pure_topological_derivation"] is True
    assert res["authority"] == "None"


def test_cosmological_constant_residual_witness_and_structure():
    res = derive_cosmological_constant_residual(
        hinge_valencies_4d=[5, 4, 5, 4], immirzi_gamma=0.274066, cell_volume_l_p4=1.0
    )

    assert res["lean4_proof_witness"] == "OmegaCore.PrimitiveDifferenceFinite.deltaFactorOn_exists_iff_deltaCongruentOn"
    assert res["lambda_residual_density"] > 0.0
    assert len(res["epsilon_4d_rad"]) == 4
    assert res["authority"] == "None"


def test_facade_integration():
    facade = ConstraintClosureL1Structure()

    res_f = facade.derive_fermion_mass_spectrum_lggr()
    assert "raw_residual_mass_gaps" in res_f

    res_l = facade.derive_cosmological_constant_residual()
    assert "lambda_residual_density" in res_l
