import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_appw_all_m_inertia_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def api():
    return _load()


def test_witness_is_the_four_finite_inertias(api) -> None:
    result = api.witness()
    assert result == {
        "L": 4,
        "fock": 16,
        "theta": Fraction(1, 10),
        "M": (1, 2, 3, 4),
        "step": (Fraction(1, 10), Fraction(1, 20), Fraction(1, 30), Fraction(1, 40)),
        "order": (8, 16, 24, 32),
        "inertia": ((4, 1, 3), (8, 1, 7), (12, 1, 11), (16, 1, 15)),
        "partition": (
            Fraction(17661, 1100),
            Fraction(755374987, 47040000),
            Fraction(1395062306051761, 86870556000000),
            Fraction(2379246859363301568641, 148151258316800000000),
        ),
        "staggered": (
            Fraction(-1, 706440),
            Fraction(-35281, 90644998440),
            Fraction(-12188547841, 55802492242070440),
            Fraction(-14588472130734881, 95169874374532062745640),
        ),
        "m1_multiplicity": (
            (Fraction(10, 21), 1),
            (Fraction(21, 40), 1),
            (Fraction(420, 841), 2),
            (Fraction(0), 3),
            (Fraction(-1, 706440), 1),
        ),
        "all_m_formula": 0,
        "continuum_limit": 0,
    }
    for depth, triple, order in zip(result["M"], result["inertia"], result["order"], strict=True):
        assert triple[0] + triple[1] + triple[2] == order == 8 * depth
        assert triple == (4 * depth, 1, 4 * depth - 1)
    assert api.inertia_of(1) == (4, 1, 3)
    assert api.inertia_of(4, theta=Fraction(1, 10), sites=4) == (16, 1, 15)
    assert result["all_m_formula"] == 0
    assert result["continuum_limit"] == 0


def test_all_m_formula_and_out_of_scope_claims_are_refused(api) -> None:
    found = api.witness()
    with pytest.raises(ValueError, match="not an all-M"):
        api.refuse_all_m_formula(found["inertia"])
    with pytest.raises(ValueError, match="not an all-M"):
        api.inertia_of(5)
    with pytest.raises(ValueError, match="theta"):
        api.inertia_of(1, theta=Fraction(1, 192))
    with pytest.raises(ValueError, match="L is outside"):
        api.inertia_of(1, sites=5)
    with pytest.raises(ValueError, match="exact rational"):
        api.inertia_of(1, theta=0.1)
    with pytest.raises(ValueError, match="higher-dimensional"):
        api.refuse_higher_dimensional_sum(8, Fraction(-1, 706440))
    api.refuse_higher_dimensional_sum(1, Fraction(-1, 706440))
    with pytest.raises(ValueError, match="continuum"):
        api.refuse_continuum()