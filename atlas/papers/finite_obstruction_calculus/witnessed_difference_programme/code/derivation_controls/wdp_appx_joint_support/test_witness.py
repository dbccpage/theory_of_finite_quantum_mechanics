import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_appx_joint_support_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _expected():
    f = Fraction
    worlds = (
        (0, (f(-1), f(-1))),
        (1, (f(0), f(-2))),
        (0, (f(0), f(0))),
        (0, (f(1, 2), f(1, 2))),
        (1, (f(1, 2), f(-3, 2))),
        (0, (f(1), f(1))),
        (1, (f(1), f(-1))),
        (0, (f(-1, 2), f(-1, 2))),
        (1, (f(3, 2), f(-1, 2))),
        (1, (f(2), f(0))),
    )
    carrier_table = (
        (0, f(0), False),
        (1, f(1), False),
        (2, f(1), False),
        (3, f(2), True),
    )
    product_table = (
        (0, f(0), False),
        (1, f(1), False),
        (2, f(1), False),
        (3, f(2), False),
    )
    return {
        "worlds": worlds,
        "carrier_fixed": f(2),
        "carrier_adaptive": f(2),
        "carrier_fixed_table": carrier_table,
        "segment_fixed": f(2),
        "segment_adaptive": f(2),
        "identity_slope": f(0),
        "identity_constants": (f(0), f(2)),
        "instrument_fixed": (None, None),
        "joint_admits_A0": (0, 1),
        "joint_admits_00": (0,),
        "joint_admits_0_m2": (1,),
        "joint_admits_01": (),
        "joint_status_A0": "ABSTAIN",
        "joint_status_00_answer_0": "VERIFIED",
        "joint_status_00_answer_1": "INVALID_PROPOSAL",
        "joint_status_0_m2_answer_1": "VERIFIED",
        "joint_status_01": "INCONSISTENT",
        "product_world_count": 8,
        "product_fixed": None,
        "product_adaptive": None,
        "product_fixed_table": product_table,
        "product_admits_00": (0, 1),
        "product_status_00": "ABSTAIN",
        "product_admits_01": (0,),
        "product_status_01_answer_0": "VERIFIED",
        "sound_upper_bound": f(2),
        "upper_bound_equals_carrier_optima": True,
        "product_price_is_optimum": False,
    }


def test_shared_noise_joint_costs_are_exact() -> None:
    result = _load().witness()
    expected = _expected()
    assert result == expected
    for key in (
        "carrier_fixed",
        "carrier_adaptive",
        "segment_fixed",
        "segment_adaptive",
        "sound_upper_bound",
        "identity_slope",
    ):
        assert type(result[key]) is Fraction
    assert result["product_fixed"] is None and result["product_adaptive"] is None
    assert result["instrument_fixed"] == (None, None)
    assert result["product_fixed_table"][3] == (3, Fraction(2), False)
    assert result["upper_bound_equals_carrier_optima"] is True
    assert result["product_price_is_optimum"] is False


def test_marginal_certificate_at_shared_zero_is_refused() -> None:
    module = _load()
    assert module.refuse_coordinate_enclosure((Fraction(0), Fraction(0)), 0) == "VERIFIED"
    assert module.refuse_coordinate_enclosure((Fraction(0), Fraction(-2)), 1) == "VERIFIED"
    with pytest.raises(ValueError, match="not a realizable joint"):
        module.refuse_coordinate_enclosure((Fraction(0), Fraction(0)), 1)
    with pytest.raises(ValueError, match="not a realizable joint"):
        module.refuse_coordinate_enclosure((Fraction(0), Fraction(1)), 0)
    with pytest.raises(TypeError, match="float tolerance"):
        module.refuse_coordinate_enclosure((0.0, 0.0), 1)
