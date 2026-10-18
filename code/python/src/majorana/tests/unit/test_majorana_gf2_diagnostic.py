"""Native GF(2) diagnostic boundary. These mocks do not test Rust math."""

from __future__ import annotations

import majorana_gf2_diagnostic as diagnostic
import majorana_evaluator as evaluator
import numpy as np
import pytest
from majorana.core import gf2_matrix as gf2_native

from omega_engine_operating_system.adapters.rust_host.majorana_math import NativeMathRefusal


def _assert_no_float(value: object) -> None:
    if isinstance(value, float):
        raise AssertionError(f"float in payload: {value!r}")
    if isinstance(value, dict):
        for item in value.values():
            _assert_no_float(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _assert_no_float(item)


def _report(dim_h1: int) -> dict:
    return {
        "dim_h1": dim_h1,
        "expected_dim_h1": dim_h1,
        "homology_matches_prediction": dim_h1 == 0,
        "num_mzm": 1,
        "num_channels": 1,
        "num_islands": 1,
        "d0": {"rows": 1, "cols": 1, "data": [[0]]},
        "d1": {"rows": 1, "cols": 1, "data": [[0]]},
        "authority_effect": "None",
    }


def _complex() -> evaluator.F2CochainComplex:
    return evaluator.F2CochainComplex(
        n0=3,
        n1=3,
        n2=1,
        d0=evaluator.GF2Matrix.from_array([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        d1=evaluator.GF2Matrix.from_array([[1, 1, 0]]),
    )


def test_disk_tetron_payload_uses_native_spelling_and_dimension(monkeypatch):
    calls = []

    def native(action, payload):
        calls.append((action, payload))
        return _report(0)

    monkeypatch.setattr(diagnostic, "call_native", native)
    carrier = evaluator.build_tetron_carrier("disk", 2, 2)
    assert carrier.h1_dim == 0
    assert carrier.code_distance is None
    assert carrier.topology == "disk"
    assert calls == [
        (
            "majorana_gf2_diagnostic",
            {"operation": "tetron", "rows": 2, "cols": 2, "topology": "Disk"},
        )
    ]
    action, payload = calls[0]
    assert action == "majorana_gf2_diagnostic"
    assert payload["operation"] == "tetron"
    assert payload["topology"] == "Disk"
    assert type(payload["rows"]) is int
    assert type(payload["cols"]) is int
    _assert_no_float(payload)


def test_cylinder_dimension_is_the_native_measurement_not_a_local_betti(monkeypatch):
    calls = []

    def native(action, payload):
        calls.append(payload)
        return _report(5)

    monkeypatch.setattr(diagnostic, "call_native", native)
    carrier = evaluator.build_tetron_carrier("cylinder", 2, 3)
    assert carrier.h1_dim == 5
    assert carrier.code_distance == 3
    assert calls == [{"operation": "tetron", "rows": 2, "cols": 3, "topology": "Cylinder"}]
    _assert_no_float(calls[0])


def test_classify_invalid_complex_and_length_mismatch_use_the_native_terminal(monkeypatch):
    calls = []
    replies = iter(
        [
            {
                "terminal": "RepresentationInvalid",
                "reason": "d1 * d0 != 0",
                "dim_h1": None,
                "certificate_alpha": None,
                "phi1_weight": None,
                "authority_effect": "None",
            },
            {
                "terminal": "RepresentationInvalid",
                "reason": "residual length does not match the channel count",
                "dim_h1": None,
                "certificate_alpha": None,
                "phi1_weight": None,
                "authority_effect": "None",
            },
        ]
    )

    def native(action, payload):
        calls.append((action, payload))
        _assert_no_float(payload)
        return next(replies)

    monkeypatch.setattr(diagnostic, "call_native", native)
    status, meta = evaluator.classify_residual(_complex(), np.array([1, 0, 0]))
    assert status == evaluator.TrichotomyClass.REPRESENTATION_INVALID
    assert meta["reason"] == "d1 * d0 != 0"
    short, short_meta = evaluator.classify_residual(_complex(), np.array([1]))
    assert short == evaluator.TrichotomyClass.REPRESENTATION_INVALID
    assert short_meta["reason"] == "residual length does not match the channel count"
    assert [payload["operation"] for _action, payload in calls] == ["classify", "classify"]
    assert calls[0][1]["diagnostics"] is False
    assert type(calls[0][1]["diagnostics"]) is bool
    assert calls[0][1]["budget"] == 1_000_000
    assert type(calls[0][1]["budget"]) is int
    assert calls[0][1]["residual"] == [1, 0, 0]
    assert calls[1][1]["residual"] == [1]
    assert all(type(bit) is int for bit in calls[0][1]["residual"])


def test_open_syndrome_weight_and_typed_harmonic_follow_the_native_terminal(monkeypatch):
    replies = iter(
        [
            {
                "terminal": "OpenObstruction",
                "reason": "d1 * r != 0",
                "dim_h1": 0,
                "certificate_alpha": None,
                "phi1_weight": None,
                "coherence_witness": [1, 0, 1],
                "authority_effect": "None",
            },
            {
                "terminal": "TypedHarmonic",
                "reason": "certified logical class",
                "dim_h1": 1,
                "certificate_alpha": None,
                "phi1_weight": 3,
                "authority_effect": "None",
            },
        ]
    )

    def native(action, payload):
        return next(replies)

    def refuse_local_algebra(action, payload):
        raise AssertionError("syndrome must come from the native witness")

    monkeypatch.setattr(diagnostic, "call_native", native)
    monkeypatch.setattr(gf2_native, "call_native", refuse_local_algebra)
    status, meta = evaluator.classify_residual(_complex(), np.array([1, 0, 0]))
    assert status == evaluator.TrichotomyClass.OPEN_OBSTRUCTION
    assert meta["syndrome_weight"] == 2
    assert meta["syndrome"] == [1, 0, 1]
    folded, folded_meta = evaluator.classify_residual(_complex(), np.array([1, 1, 1]))
    assert folded == evaluator.TrichotomyClass.CLOSED_RESIDUAL
    assert folded_meta["native_terminal"] == "TypedHarmonic"


def test_coset_weight_is_native_phi1_not_the_residual_popcount(monkeypatch):
    calls = []

    def native(action, payload):
        calls.append(payload)
        _assert_no_float(payload)
        return {
            "terminal": "OpenObstruction",
            "reason": "d1 * r != 0",
            "dim_h1": 2,
            "certificate_alpha": None,
            "phi1_weight": 4,
            "phi1_exact": False,
            "authority_effect": "None",
        }

    monkeypatch.setattr(diagnostic, "call_native", native)
    weight, exact = evaluator.compute_coset_weight(_complex(), np.array([1, 0, 0]), budget_max=16)
    assert (weight, exact) == (4, False)
    assert calls == [
        {
            "operation": "classify",
            "d0": {
                "rows": 3,
                "cols": 3,
                "data": [[1, 1, 0], [0, 1, 1], [1, 0, 1]],
            },
            "d1": {"rows": 1, "cols": 3, "data": [[1, 1, 0]]},
            "residual": [1, 0, 0],
            "budget": 16,
            "diagnostics": True,
        }
    ]
    assert type(calls[0]["diagnostics"]) is bool
    assert type(calls[0]["budget"]) is int


def test_repair_capacity_distance_five_is_two_and_zero_refuses(monkeypatch):
    calls = []

    def native(action, payload):
        calls.append((action, payload))
        _assert_no_float(payload)
        if payload["distance"] == 0:
            raise NativeMathRefusal("NATIVE_MATH_REFUSED", "d must be positive", outcome=payload)
        return {"t": {5: 2, 4: 9}[payload["distance"]]}

    monkeypatch.setattr(diagnostic, "call_native", native)
    assert diagnostic.repair_capacity(distance=5) == 2
    assert diagnostic.repair_capacity(distance=4) == 9
    with pytest.raises(NativeMathRefusal, match="d must be positive"):
        diagnostic.repair_capacity(distance=0)
    with pytest.raises(TypeError):
        diagnostic.repair_capacity(distance=5.0)  # type: ignore[arg-type]
    assert calls == [
        ("majorana_gf2_diagnostic", {"operation": "repair_capacity", "distance": 5}),
        ("majorana_gf2_diagnostic", {"operation": "repair_capacity", "distance": 4}),
        ("majorana_gf2_diagnostic", {"operation": "repair_capacity", "distance": 0}),
    ]
    assert all(type(payload["distance"]) is int for _action, payload in calls)


def test_repair_min_weight_preserves_a_native_null(monkeypatch):
    calls = []

    def native(action, payload):
        calls.append(payload)
        _assert_no_float(payload)
        return {"min_weight": None}

    monkeypatch.setattr(diagnostic, "call_native", native)
    assert diagnostic.repair_capacity(cycles=[[0, 0], [1, 0, 1]]) is None
    assert calls == [
        {"operation": "repair_capacity", "cycles": [[0, 0], [1, 0, 1]]}
    ]
    assert all(type(bit) is int for cycle in calls[0]["cycles"] for bit in cycle)


def test_lggr_payload_keeps_the_native_flag(monkeypatch):
    calls = []
    replies = iter(
        [
            {
                "local_green": False,
                "global_red": False,
                "is_lggr": True,
                "d1_omega": [0, 1],
                "status": "ClosedResidual",
                "authority_effect": "None",
            },
            {
                "local_green": True,
                "global_red": True,
                "is_lggr": True,
                "d1_omega": [0, 0],
                "certificate": {"status": "ClosedResidual"},
                "authority_effect": "None",
            },
            {
                "local_green": False,
                "global_red": False,
                "is_lggr": False,
                "d1_omega": [1],
                "authority_effect": "None",
            },
        ]
    )

    def native(action, payload):
        calls.append((action, payload))
        _assert_no_float(payload)
        return next(replies)

    monkeypatch.setattr(diagnostic, "call_native", native)
    matrices = (
        {"rows": 1, "cols": 2, "data": [[1, 0]]},
        {"rows": 1, "cols": 2, "data": [[0, 1]]},
    )
    witness = diagnostic.lggr(*matrices, [1, 0])
    assert witness["is_lggr"] is True
    nested = diagnostic.lggr(*matrices, [1, 0])
    assert nested["certificate"]["status"] == "ClosedResidual"
    with pytest.raises(ValueError, match="lacks status"):
        diagnostic.lggr(*matrices, [1, 0])
    assert calls[0][0] == "majorana_gf2_diagnostic"
    assert calls[0][1]["operation"] == "lggr"
    assert calls[0][1]["omega"] == [1, 0]
    assert calls[0][1]["d0"]["data"] == [[1, 0]]
    assert "status" not in calls[0][1]


def test_gf2_rank_solve_and_product_follow_the_native_fixture(monkeypatch):
    def native(action, payload):
        assert action == "math_gf2_matrix"
        _assert_no_float(payload)
        operation = payload["operation"]
        if operation == "rref":
            # True GF(2) rank is 2 and the real rank is 3. The fixture rank is
            # neither, so a local elimination cannot satisfy the assertion.
            assert payload["matrix"]["data"] == [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
            return {"matrix": payload["matrix"], "pivots": [0]}
        if operation == "solve":
            assert payload["vector"] == [1, 0]
            return {"solution": [0, 1]}
        if operation == "multiply":
            return {"matrix": {"rows": 1, "cols": 1, "data": [[1]]}}
        raise AssertionError(operation)

    monkeypatch.setattr(gf2_native, "call_native", native)
    singular_over_reals = evaluator.GF2Matrix.from_array([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    assert singular_over_reals.rank() == 1
    solved = evaluator.GF2Matrix.from_array([[1, 0], [0, 1]]).solve(np.array([1, 0]))
    assert solved is not None
    assert solved.tolist() == [0, 1]
    cochain = evaluator.F2CochainComplex(
        n0=1,
        n1=1,
        n2=1,
        d0=evaluator.GF2Matrix.from_array([[0]]),
        d1=evaluator.GF2Matrix.from_array([[1]]),
    )
    assert cochain.is_nilpotent() is False


def test_float_residual_is_refused_before_the_native_call(monkeypatch):
    def native(action, payload):
        raise AssertionError("float residual reached native")

    monkeypatch.setattr(diagnostic, "call_native", native)
    with pytest.raises(TypeError):
        evaluator.classify_residual(_complex(), np.array([1.0, 0.0, 0.0]))


def test_logical_column_weight_is_the_row_count():
    rows, cols = 3, 4
    n0 = rows * cols
    n1 = 2 * n0
    n2 = n0
    carrier = evaluator.TetronCarrier(
        topology="torus",
        rows=rows,
        cols=cols,
        complex=evaluator.F2CochainComplex(
            n0,
            n1,
            n2,
            evaluator.GF2Matrix.from_array([[0] * n0 for _ in range(n1)]),
            evaluator.GF2Matrix.from_array([[0] * n1 for _ in range(n2)]),
        ),
        h1_dim=2,
        code_distance=min(rows, cols),
    )
    column = evaluator.logical_representative(carrier, axis="column", index=0)
    row = evaluator.logical_representative(carrier, axis="row", index=0)
    assert int(column.sum()) == 3
    assert int(row.sum()) == 4
    assert int(np.sum(row ^ column)) == 7
