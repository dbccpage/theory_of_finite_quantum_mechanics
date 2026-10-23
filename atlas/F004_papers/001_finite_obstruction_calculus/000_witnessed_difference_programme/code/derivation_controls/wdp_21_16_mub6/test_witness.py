import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_21_16_mub6_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_four_labelled_mub6_carriers_are_exact() -> None:
    module = _load()
    result = module.witness()
    assert result["tao_column_sums"] == (0, -4, -4, 0, 2, 0)
    assert result["tao_column_residues_mod3"] == (0, 2, 2, 0, 2, 0)
    assert result["tao_residue_counts"] == (3, 0, 3)
    assert result["tao_eisenstein_norm_sq"] == 9
    assert result["alpha_2_values"] == (-9, -3, 3, 9)
    assert result["parity_pair_sums"] == (0, 0, 0, 0)
    assert result["synthetic_nerve_sum_012"] == 12133
    assert result["synthetic_coboundary_cycle_sum"] == 0
    assert result["spectral_floor_frac"] == Fraction(31, 800)
    assert result["lookup_row_counts"]["Haagerup"] == 1
    assert result["external_haagerup_minus_one_rows"] == 5


def test_moduli_phi1_coverage_promotion_is_refused() -> None:
    module = _load()
    for val in (0, 9, 12133, Fraction(12133, 5000)):
        with pytest.raises(ValueError, match="CHM\\(6\\)"):
            module.reject_moduli_phi1_coverage_claim(val)
