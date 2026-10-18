"""Firewall conformance tests for py_updates_3 defects.

Asserts that diagnostic statistics cannot coerce into authority terminals and
that the schema boundary returns typed Refusals instead of raising raw errors.
"""

from omega_engine.crates.type.epk.core import ComposedPath
from omega_engine.crates.type.epk.metrics import MetricReport
from omega_engine.crates.type.epk.schemas import validate_and_normalize_row
from omega_engine.crates.type.refusal import Refusal


def _valid_row() -> dict:
    return {
        "task_id": "swe_doc3",
        "example_type": "swe",
        "source_state": "S_a",
        "boundary_state": "S_b",
        "target_state": "S_c",
        "first_local_pass": True,
        "second_local_pass": True,
        "global_pass": False,
        "first_cost": 1.0,
        "second_cost": 2.0,
    }


def test_metric_report_has_no_to_authority():
    """Diagnostic statistics must never expose an authority-coercion method."""
    assert not hasattr(MetricReport, "to_authority")


def test_validate_returns_refusal_on_missing_field():
    row = _valid_row()
    del row["boundary_state"]
    result = validate_and_normalize_row(row)
    assert isinstance(result, Refusal)
    assert "Missing required field" in result.reason


def test_validate_returns_refusal_on_unknown_example_type():
    row = _valid_row()
    row["example_type"] = "not_a_real_type"
    result = validate_and_normalize_row(row)
    assert isinstance(result, Refusal)
    assert "Unknown example type" in result.reason


def test_validate_returns_composed_path_on_valid_row():
    result = validate_and_normalize_row(_valid_row())
    assert isinstance(result, ComposedPath)
    assert not isinstance(result, Refusal)
    assert result.id == "swe_doc3"


