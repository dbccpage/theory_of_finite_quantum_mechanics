import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    name = "wdp_repair_policy_witness"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("witness module did not load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _no_float(value: object) -> None:
    if isinstance(value, float):
        raise AssertionError("float tolerance is not a claim")
    if isinstance(value, tuple):
        for item in value:
            _no_float(item)
    elif isinstance(value, dict):
        for item in value.values():
            _no_float(item)


def test_witness_is_the_nonterminating_dyadic_run() -> None:
    result = _load().witness()
    assert result == {
        "one_cell_composition": Fraction(0),
        "triangle_composition": (Fraction(0), Fraction(0), Fraction(0)),
        "one_cell_operator_norm": Fraction(1),
        "triangle_operator_norm": Fraction(1),
        "one_cell_phi": (Fraction(1), Fraction(1, 2), Fraction(1, 4)),
        "one_cell_gamma": (Fraction(1), Fraction(1, 2), Fraction(1, 4)),
        "one_cell_r_cl": (Fraction(1), Fraction(1), Fraction(1)),
        "one_cell_class": (2, 2, 2),
        "one_cell_drops": (Fraction(1, 2), Fraction(1, 4)),
        "one_cell_successor_phi": Fraction(1, 8),
        "one_cell_successor_r_cl": Fraction(1),
        "one_cell_successor_class": 2,
        "one_cell_successor_accepted": 1,
        "triangle_phi": (Fraction(2), Fraction(1), Fraction(1, 2)),
        "triangle_gamma": (Fraction(2), Fraction(1), Fraction(1, 2)),
        "triangle_r_cl": (Fraction(1), Fraction(1), Fraction(1)),
        "triangle_class": (2, 2, 2),
        "triangle_drops": (Fraction(1), Fraction(1, 2)),
        "triangle_successor_phi": Fraction(1, 4),
        "triangle_successor_r_cl": Fraction(1),
        "triangle_successor_class": 2,
        "triangle_successor_accepted": 1,
        "windows_distinct": 1,
        "coboundary_drop": Fraction(0),
        "coboundary_accepted": 0,
        "reaches_zero": 0,
        "termination_admitted": 0,
        "undershooting_epsilon": Fraction(1, 4),
        "undershooting_drop_n": 2,
        "undershooting_drop": Fraction(1, 8),
        "grid_denominator": 4,
        "grid_escape_n": 3,
        "grid_escape_phi": Fraction(1, 8),
        "far_n": 10,
        "one_cell_far_phi": Fraction(1, 1024),
        "one_cell_far_r_cl": Fraction(1),
        "one_cell_far_accepted": 1,
        "triangle_far_phi": Fraction(1, 512),
        "triangle_far_r_cl": Fraction(1),
        "triangle_far_accepted": 1,
    }
    _no_float(result)


def test_one_cell_mass_and_limit_zero_are_refused() -> None:
    module = _load()
    with pytest.raises(ValueError, match="one-cell"):
        module.refuse_one_cell_mass_as_triangle(0, Fraction(1))
    with pytest.raises(ValueError, match="one-cell"):
        module.refuse_one_cell_mass_as_triangle(10, Fraction(1, 1024))
    with pytest.raises(ValueError, match="not a state"):
        module.refuse_limit_zero(0)
    with pytest.raises(ValueError, match="not a state"):
        module.refuse_limit_zero(Fraction(0))
    with pytest.raises(TypeError, match="float"):
        module.refuse_limit_zero(0.0)
    with pytest.raises(TypeError, match="float"):
        module.refuse_one_cell_mass_as_triangle(0, 2.0)
    module.refuse_one_cell_mass_as_triangle(0, Fraction(2))
    module.refuse_one_cell_mass_as_triangle(1, Fraction(1))
    module.refuse_one_cell_mass_as_triangle(10, Fraction(1, 512))
    module.refuse_limit_zero(Fraction(1, 8))
