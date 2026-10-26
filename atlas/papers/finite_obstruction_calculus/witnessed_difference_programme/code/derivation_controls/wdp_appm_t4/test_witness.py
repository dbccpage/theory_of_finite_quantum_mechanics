import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_appm_t4_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pentatope_bivector_simplicity_closure_and_bianchi() -> None:
    module = _load()
    result = module.witness()
    assert result["boundary_tetrahedra"] == 5
    assert result["triangular_hinges"] == 10
    assert result["single_hinge_pfaffian_max"] == 0
    assert result["intra_tetrahedral_pfaffian_max"] == 0
    assert result["opposite_hinge_nonzero_pairs"] == 15
    assert result["tetrahedral_closure_max_norm"] == 0
    assert result["chain_boundary_squared_max"] == 0
    assert result["coordinate_hinge_area"] == Fraction(1, 2)
    assert result["outer_hinge_area_sq"] == Fraction(3, 4)
    assert result["coordinate_regge_action_turns"] == Fraction(1, 4)
    assert result["cayley_so4_trace"] == Fraction(16, 5)


def test_opposite_hinge_simplicity_and_eh_bound_refuse() -> None:
    module = _load()
    with pytest.raises(ValueError, match="Pfaffian 1"):
        module.reject_universal_bivector_simplicity()
    with pytest.raises(ValueError, match="Einstein-Hilbert"):
        module.reject_unproved_eh_action_bound("|S_Regge - S_EH| <= C * a^2")
