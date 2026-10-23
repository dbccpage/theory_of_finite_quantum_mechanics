import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_appm_t3_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_3d_torus_cycles_linking_and_characters() -> None:
    module = _load()
    result = module.witness()
    assert result["sites"] == 64
    assert result["cycles"] == 240
    assert result["plaquettes"] == 192
    assert result["generators"] == 48
    assert result["orientations"] == 480
    assert result["Z"] == 384
    assert result["N"] == 96
    assert result["average_sign"] == Fraction(4, 5)
    assert result["expectation"] == Fraction(1, 4)
    assert result["hopf_linking"] == 1
    assert result["reversed_linking"] == -1
    assert result["shifted_linking"] == 0
    assert result["trivial_character_sum"] == 64
    assert result["max_nontrivial_character_residual"] == 0


def test_boundary_collision_and_pinned_residual_refuse() -> None:
    module = _load()
    bad_loop = module.hopf_loop(0, False)
    bad_loop[0] = ((0, 0, 0), (0, 0, 1))
    with pytest.raises(ValueError, match="boundary C1"):
        module.linking_with_square_patch(bad_loop)
    with pytest.raises(ValueError, match="10\\^-25"):
        module.reject_pinned_t3_string_only_claim("max residual 10^-25")
