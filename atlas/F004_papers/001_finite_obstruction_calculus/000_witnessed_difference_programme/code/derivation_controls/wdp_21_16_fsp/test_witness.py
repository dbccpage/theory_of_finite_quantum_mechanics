import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_21_16_fsp_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_is_the_star_and_orbit() -> None:
    module = _load()
    result = module.witness()
    assert result["signs"] == module.cycle_signs()
    assert result == {
        "sites": 4,
        "center": 0,
        "particles": 2,
        "hops": 6,
        "signs": (1, -1, 1, 1, -1, -1),
        "sign_product": -1,
        "parity_bit_sum": 3,
        "f2_cycle_sum": 1,
        "gauges": 64,
        "gauges_with_product_plus": 0,
        "site_edges": 3,
        "site_cycle_rank": 0,
        "all_negative_product": 1,
        "k": 1,
        "A": 1,
        "s": 1,
        "m": 1,
        "Z_U": 0,
        "hat_O": Fraction(1, 1),
        "N_U": 2,
        "holonomy_removed": 0,
        "numerator_preserved": 0,
        "conjunction": 0,
    }


def test_foreign_fixture_scalars_are_refused() -> None:
    module = _load()
    result = module.witness()
    with pytest.raises(ValueError, match="912"):
        module.refuse_foreign_scalar(912)
    with pytest.raises(ValueError, match="36864"):
        module.refuse_foreign_scalar(36864)
    module.refuse_foreign_scalar(result["sign_product"])
    module.refuse_foreign_scalar(result["N_U"])
    module.refuse_foreign_scalar(result["Z_U"])
    module.refuse_foreign_scalar(result["f2_cycle_sum"])
