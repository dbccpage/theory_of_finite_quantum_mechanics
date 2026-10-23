import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location(
        "wdp_o10_signed_measure_positivity_witness", path
    )
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("witness loader is missing")
    spec.loader.exec_module(module)
    return module


def _expected():
    disk_denominator = 21743271936
    if 384**4 != disk_denominator or (1 << 28) * 3**4 != disk_denominator:
        raise AssertionError("disk denominator disagrees with 384^4")
    weight_disk = Fraction(1, disk_denominator)
    if weight_disk != Fraction(1, 384) ** 4:
        raise AssertionError("disk weight disagrees with ((q-1)/2)^4")
    q_disk = Fraction(193, 192)
    if (q_disk - 1) / 2 != Fraction(1, 384) or q_disk != 1 + Fraction(1, 192):
        raise AssertionError("q=193/192 is not the in-disk endpoint")
    return {
        "L": 4,
        "M": 1,
        "times": 2,
        "LM": 4,
        "plaquettes": 4,
        "fock": 16,
        "graphs_enumerated": 1,
        "gid": 15,
        "cycles": 2,
        "cycle_length": 4,
        "orientations": 4,
        "mask_lo": 1,
        "mask_hi": 2,
        "q_algebraic": Fraction(3),
        "q_disk": q_disk,
        "horizontal_q3": Fraction(1),
        "horizontal_disk": Fraction(1, 384),
        "vertical": Fraction(1),
        "weight_q3": Fraction(1),
        "weight_disk": weight_disk,
        "opposite_charge_q3": Fraction(-1),
        "opposite_charge_disk": Fraction(-1, disk_denominator),
        "equal_charge_q3": Fraction(1),
        "equal_charge_disk": Fraction(1, disk_denominator),
        "negative_atom_count": 2,
        "orientation_sum_q3": Fraction(0),
        "orientation_sum_disk": Fraction(0),
        "merons": 2,
        "reduced_weight_q3": Fraction(0),
        "reduced_weight_disk": Fraction(0),
        "is_positive_measure": 0,
        "is_probability_measure": 0,
        "atoms_deleted": 0,
        "fock_summed": 0,
        "continuum_limit": 0,
    }


def test_all_horizontal_charges_are_exact() -> None:
    result = _load().witness()
    expected = _expected()
    assert result == expected
    for key in (
        "q_algebraic",
        "q_disk",
        "horizontal_q3",
        "horizontal_disk",
        "vertical",
        "weight_q3",
        "weight_disk",
        "opposite_charge_q3",
        "opposite_charge_disk",
        "equal_charge_q3",
        "equal_charge_disk",
        "orientation_sum_q3",
        "orientation_sum_disk",
        "reduced_weight_q3",
        "reduced_weight_disk",
    ):
        assert type(result[key]) is Fraction
    for key in (
        "L",
        "M",
        "times",
        "LM",
        "plaquettes",
        "fock",
        "graphs_enumerated",
        "gid",
        "cycles",
        "cycle_length",
        "orientations",
        "mask_lo",
        "mask_hi",
        "negative_atom_count",
        "merons",
        "is_positive_measure",
        "is_probability_measure",
        "atoms_deleted",
        "fock_summed",
        "continuum_limit",
    ):
        assert type(result[key]) is int
    assert result["opposite_charge_q3"] == -1
    assert result["opposite_charge_disk"] == Fraction(-1, 21743271936)
    assert result["opposite_charge_q3"] < 0
    assert result["opposite_charge_disk"] < 0
    assert result["equal_charge_q3"] > 0
    assert result["equal_charge_disk"] > 0
    assert result["weight_q3"] > 0
    assert result["weight_disk"] > 0
    assert result["opposite_charge_q3"] == -result["weight_q3"]
    assert result["opposite_charge_disk"] == -result["weight_disk"]
    assert result["orientation_sum_q3"] == 0
    assert result["orientation_sum_disk"] == 0
    assert result["orientation_sum_q3"] != 1
    assert result["merons"] == 2
    assert result["reduced_weight_q3"] == 0
    assert result["atoms_deleted"] == 0
    assert result["is_positive_measure"] == 0
    assert result["is_probability_measure"] == 0
    assert result["fock_summed"] == 0
    assert result["continuum_limit"] == 0
    assert result["graphs_enumerated"] == 1
    assert result["gid"] == 15
    assert result["mask_lo"] == 1 and result["mask_hi"] == 2


def test_negative_atoms_are_not_declared_a_positive_measure() -> None:
    module = _load()
    with pytest.raises(ValueError, match="not a positive measure"):
        module.refuse_positive_measure()
    with pytest.raises(ValueError, match="sites below 4"):
        module.refuse_l2()
    with pytest.raises(ValueError, match="912"):
        module.refuse_m2_partition(912)
    with pytest.raises(ValueError, match="Gibbs"):
        module.refuse_gibbs()
    with pytest.raises(ValueError, match="zero-meron"):
        module.refuse_zero_meron()
    with pytest.raises(ValueError, match="continuum"):
        module.refuse_continuum()
    with pytest.raises(ValueError, match="higher-dimensional"):
        module.refuse_higher_dimensional_sum(4, 1)
    module.refuse_higher_dimensional_sum(1, 1)
    with pytest.raises(ValueError, match="outside L=4"):
        module.signed_breakup(sites=2, repetitions=1, q=3)
    with pytest.raises(ValueError, match="outside L=4"):
        module.signed_breakup(sites=4, repetitions=2, q=3)
    with pytest.raises(ValueError, match="exact rational"):
        module.signed_breakup(q=3.0)
    with pytest.raises(ValueError, match="outside the two selected"):
        module.signed_breakup(q=Fraction(2))
    with pytest.raises(ValueError, match="exact rational"):
        module.refuse_higher_dimensional_sum(1, -1 / 21743271936)
