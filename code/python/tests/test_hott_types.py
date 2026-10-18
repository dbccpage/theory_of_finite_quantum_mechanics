"""Tests for HoTT shape types: Path, ContractibleType, HigherInductiveType."""

import pytest
from src.homotopy_type_theory.hott_types import (
    Path,
    ContractibleType,
    PointConstructor,
    PathConstructor,
    HigherInductiveType,
    MissingReferenceError,
    InvalidHITError,
)


def test_path_validation():
    p = Path(type_id="A", source="x", target="y", path_ref="p_xy")
    p.validate()

    bad_p = Path(type_id="", source="x", target="y", path_ref="p")
    with pytest.raises(MissingReferenceError):
        bad_p.validate()


def test_contractible_type():
    c = ContractibleType(type_ref="Unit", center_ref="tt", contraction_ref="contr_unit")
    c.validate()

    bad_c = ContractibleType(type_ref="Unit", center_ref="", contraction_ref="contr")
    with pytest.raises(MissingReferenceError):
        bad_c.validate()


def test_circle_s1_hit():
    s1 = HigherInductiveType.circle_s1()
    assert s1.type_name == "S^1"
    assert len(s1.points) == 1
    assert s1.points[0].name == "base"
    assert len(s1.paths) == 1
    assert s1.paths[0].name == "loop"
    assert s1.paths[0].source_point == "base"
    assert s1.paths[0].target_point == "base"


def test_interval_i_hit():
    interval = HigherInductiveType.interval_i()
    assert interval.type_name == "Interval"
    assert len(interval.points) == 2
    assert len(interval.paths) == 1
    assert interval.paths[0].name == "seg"


def test_torus_t2_hit():
    t2 = HigherInductiveType.torus_t2()
    assert t2.type_name == "T^2"
    assert len(t2.points) == 1
    assert len(t2.paths) == 2


def test_invalid_hit_raises():
    bad_hit = HigherInductiveType(
        type_name="Broken",
        points=[PointConstructor("x")],
        paths=[PathConstructor("p", "x", "non_existent_point")],
    )
    with pytest.raises(InvalidHITError):
        bad_hit.validate()
