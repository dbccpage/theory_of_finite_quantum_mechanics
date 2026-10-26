import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_appm_t1_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_origin_face_and_row_are_labelled() -> None:
    module = _load()
    origin_face = module.faces()[0]
    assert origin_face == frozenset(
        {
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((0, 1), (1, 1)),
            ((0, 0), (0, 1)),
        }
    )
    assert module.rows()[0] == frozenset(
        {
            ((0, 0), (1, 0)),
            ((1, 0), (2, 0)),
            ((2, 0), (3, 0)),
            ((0, 0), (3, 0)),
        }
    )
    assert module.cols()[0] == frozenset(
        {
            ((0, 0), (0, 1)),
            ((0, 1), (0, 2)),
            ((0, 2), (0, 3)),
            ((0, 0), (0, 3)),
        }
    )


def test_enumerated_partition_is_exact() -> None:
    result = _load().witness()
    assert result["sites"] == 16
    assert result["cycles"] == 24
    assert result["faces"] == 16
    assert result["generators"] == 8
    assert result["orientations"] == 48
    assert result["Z"] == 32
    assert result["N"] == 16
    assert result["average_sign"] == Fraction(2, 3)
    assert result["expectation"] == Fraction(1, 2)


def test_pinned_one_dimensional_trace_is_refused() -> None:
    module = _load()
    with pytest.raises(ValueError, match="912"):
        module.reject_pinned_scalar(912)
    module.reject_pinned_scalar(module.witness()["Z"])
