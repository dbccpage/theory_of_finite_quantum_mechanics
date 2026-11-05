import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_appm_t2_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cayley_menger_determinant_sign_and_degeneracy() -> None:
    module = _load()
    assert module.cayley_menger_det_2simplex(1, 1, 1) == Fraction(-3)
    assert module.cayley_menger_det_2simplex(1, 1, 4) == Fraction(0)
    assert module.cayley_menger_det_2simplex(1, 1, 9) == Fraction(45)


def test_five_and_six_triangle_star_metrics() -> None:
    module = _load()
    result = module.witness()
    assert result["triangles_k5"] == 5
    assert result["triangles_k6"] == 6
    assert result["cayley_menger_det"] == -3
    assert result["signed_volume_factor"] == 3
    assert result["triangle_area_sq"] == Fraction(3, 16)
    assert result["star_area_sq_k5"] == Fraction(75, 16)
    assert result["apex_cosine"] == Fraction(1, 2)
    assert result["apex_sin_sq"] == Fraction(3, 4)
    assert result["turn_sum_k5"] == Fraction(5, 6)
    assert result["turn_deficit_k5"] == Fraction(1, 6)
    assert result["turn_deficit_k6"] == Fraction(0)
    lo, hi = result["radian_deficit_interval"]
    assert lo < hi
    assert result["radian_deficit_width"] == Fraction(1, 1_000_000_000)


def test_pinned_determinant_and_continuum_bound_are_refused() -> None:
    module = _load()
    with pytest.raises(ValueError, match="-3, not \\+3"):
        module.reject_pinned_cm_determinant(3)
    module.reject_pinned_cm_determinant(-3)
    with pytest.raises(ValueError, match="Ricci"):
        module.reject_unproved_continuum_bound("|E(a)| <= (1/6) * a^2")
