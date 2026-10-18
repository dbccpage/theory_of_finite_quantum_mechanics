"""Native GF(2) diagnostic delegation. The host binary is not required."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_CONFTEST = Path(__file__).resolve().parents[2] / "tests" / "conftest.py"
_spec = importlib.util.spec_from_file_location("paper026_majorana_conftest", _CONFTEST)
assert _spec is not None and _spec.loader is not None
_spec.loader.exec_module(importlib.util.module_from_spec(_spec))

from omega_engine.crates.majorana.carriers.surface_carrier import build_tetron_array
from omega_engine.crates.majorana.carriers.tetron_carrier import build_tetron_array_carrier
from omega_engine.crates.majorana.core import gf2_diagnostic, gf2_matrix
from omega_engine.crates.majorana.core.gf2_diagnostic import (
    ACTION,
    repair_capacity_native,
)
from omega_engine.crates.majorana.demos.kitaev_ring_majorana_benchmark import (
    benchmark_kitaev_ring_majorana,
)
from omega_engine.crates.majorana.demos.microsoft_majorana_braiding_benchmark import (
    benchmark_microsoft_majorana_y_junction,
)
from omega_engine.crates.majorana.engines.classifier import classify
from omega_engine.crates.majorana.engines.harmonic import (
    H1Basis,
    class_coordinates,
    h1_basis,
    l1_harmonic_projection,
)
from omega_engine.crates.majorana.engines.terminalizer import terminalize
from omega_engine.crates.majorana.majorana_cohomology_bridge import (
    evaluate_network_majorana_parity,
)
from omega_engine.crates.residuals.network_residual import Network
from omega_engine_operating_system.adapters.rust_host.majorana_math import NativeMathRefusal

_DIM_H1 = {"Disk": 0, "Cylinder": 1, "Torus": 2}


def _classify_receipt(**overrides):
    receipt = {
        "terminal": "Exact",
        "reason": "residual lies in im(d0)",
        "dim_h1": 0,
        "class_coordinates": [0],
        "class_id": "h1:0",
        "coherence_witness": None,
        "certificate_alpha": [0],
        "certificate_verified": True,
        "phi1_weight": 0,
        "phi1_exact": True,
        "phi1_representative": [0],
        "phi1_alpha": [0],
        "phi1_searched": 1,
        "phi1_coset_size": 1,
        "phi1_verified": True,
        "authority_effect": "None",
    }
    receipt.update(overrides)
    return receipt


def _transpose(wire):
    rows, cols, data = wire["rows"], wire["cols"], wire["data"]
    if rows == 0:
        return {"rows": cols, "cols": 0, "data": [[] for _ in range(cols)]}
    transposed = [[data[row][col] for row in range(rows)] for col in range(cols)]
    return {"rows": cols, "cols": rows, "data": transposed}


def _math_fake(action, payload, host=None):
    assert action == "math_gf2_matrix"
    operation = payload["operation"]
    if operation == "transpose":
        return {"matrix": _transpose(payload["matrix"])}
    if operation == "rref":
        return {"matrix": payload["matrix"], "pivots": []}
    if operation == "solve":
        return {"solution": None}
    if operation == "kernel":
        cols = payload["matrix"]["cols"]
        basis = []
        for index in range(min(2, cols)):
            vector = [0] * cols
            vector[index] = 1
            basis.append(vector)
        return {"basis": basis}
    raise AssertionError(operation)


def test_disk_1x1_dim_h1_is_native_and_topology_swap_is_visible(monkeypatch):
    calls = []

    def fake(action, payload, host=None):
        assert action == ACTION
        calls.append(payload)
        topology = payload["topology"]
        dim = _DIM_H1[topology]
        return {
            "topology": topology,
            "rows": payload["rows"],
            "cols": payload["cols"],
            "rank_d0": 0,
            "rank_d1": 0,
            "graph_b1": dim,
            "dim_h1": dim,
            "authority_effect": "None",
        }

    monkeypatch.setattr(gf2_diagnostic, "call_native", fake)
    _carrier, report = build_tetron_array(1, 1, "disk")

    sent = calls[0]
    assert sent["operation"] == "tetron"
    assert sent["rows"] == 1 and sent["cols"] == 1
    assert sent["topology"] == "Disk"
    assert report.dim_h1 == 0
    assert report.rank_d0 == 0
    assert report.graph_b1 == 0
    assert report.num_channels == 4
    assert report.authority_effect == "None"
    assert report.dim_h1 != report.num_channels - report.rank_d1 - report.rank_d0

    swapped = dict(sent)
    swapped["topology"] = "Torus"
    swapped_dim = fake(ACTION, swapped)["dim_h1"]
    assert swapped_dim == 2
    assert swapped_dim != report.dim_h1


def test_classify_terminal_follows_the_native_payload(monkeypatch):
    calls = []

    def fake(action, payload, host=None):
        assert action == ACTION
        calls.append(payload)
        terminal = "Exact" if payload["residual"] == [0, 0, 0] else "OpenObstruction"
        return _classify_receipt(
            terminal=terminal,
            dim_h1=0,
            coherence_witness=[1] if terminal == "OpenObstruction" else None,
            class_coordinates=None if terminal == "OpenObstruction" else [0],
            class_id=None if terminal == "OpenObstruction" else "h1:0",
        )

    monkeypatch.setattr(gf2_diagnostic, "call_native", fake)
    monkeypatch.setattr(gf2_matrix, "call_native", _math_fake)
    d0 = [[1], [1], [0]]
    d1 = [[1, 1, 0]]
    certificate = classify(d0, d1, [1, 0, 0])

    assert calls[0]["operation"] == "classify"
    assert certificate["terminal_status"] == "OpenObstruction"
    assert certificate["dim_h1"] == 0
    assert certificate["authority_effect"] == "None"
    assert certificate["algebraic_class_id"] == "open-obstruction:1"

    swapped = dict(calls[0])
    swapped["residual"] = [0, 0, 0]
    assert fake(ACTION, swapped)["terminal"] == "Exact"
    assert fake(ACTION, swapped)["terminal"] != certificate["terminal_status"]


def test_terminalize_projects_native_typed_harmonic_without_redeciding(monkeypatch):
    def fake(action, payload, host=None):
        assert payload["operation"] == "classify"
        terminal = "TypedHarmonic" if payload["residual"] == [0, 0, 1] else "Exact"
        return _classify_receipt(terminal=terminal, certificate_alpha=[1])

    monkeypatch.setattr(gf2_diagnostic, "call_native", fake)
    monkeypatch.setattr(gf2_matrix, "call_native", _math_fake)
    closed = terminalize([[1], [1], [0]], [[1, 1, 0]], [0, 0, 1])
    exact = terminalize([[1], [1], [0]], [[1, 1, 0]], [1, 1, 0])
    assert closed["terminal_status"] == "ClosedResidual"
    assert closed["algebraic_class_id"].startswith("closed-residual:")
    assert exact["terminal_status"] == "Exact"
    assert exact["certificate_alpha"] == [1]
    assert exact["algebraic_class_id"] == "exact"
    assert "authority_effect" not in exact


def test_phi1_weight_is_the_native_field(monkeypatch):
    def fake(action, payload, host=None):
        assert payload["operation"] == "classify"
        exact = payload["budget"] >= 8
        return _classify_receipt(
            phi1_weight=4 if exact else 9,
            phi1_exact=exact,
            phi1_representative=[1, 0, 0],
            phi1_alpha=[1, 0],
            phi1_searched=payload["budget"],
            phi1_coset_size=16,
        )

    monkeypatch.setattr(gf2_diagnostic, "call_native", fake)
    projection = l1_harmonic_projection([[1, 0], [0, 1], [1, 1]], [1, 0, 0], budget=8)
    assert projection.weight == 4
    assert projection.exact is True
    assert projection.authority_effect == "None"
    assert sum(projection.representative) != projection.weight

    capped = dict(operation="classify", budget=1, residual=[1, 0, 0])
    assert fake(ACTION, capped)["phi1_weight"] == 9
    assert fake(ACTION, capped)["phi1_weight"] != projection.weight


def test_class_coordinates_follow_the_native_residual(monkeypatch):
    def fake(action, payload, host=None):
        bit = payload["residual"][0]
        return _classify_receipt(class_coordinates=[bit, 1 - bit], class_id=f"h1:{bit}{1 - bit}")

    monkeypatch.setattr(gf2_diagnostic, "call_native", fake)
    basis = H1Basis(
        dim=2,
        generators=[[1, 0], [0, 1]],
        num_channels=2,
        d0=[[1, 0], [0, 1]],
        d1=[[0, 0]],
    )
    coordinates = class_coordinates(basis, [1, 0])
    assert coordinates == [1, 0]
    swapped = {"operation": "classify", "residual": [0, 1]}
    assert fake(ACTION, swapped)["class_coordinates"] == [0, 1]
    assert fake(ACTION, swapped)["class_coordinates"] != coordinates


def test_h1_dimension_must_match_native_dim_h1(monkeypatch):
    def fake(action, payload, host=None):
        return _classify_receipt(dim_h1=0, terminal="Exact")

    monkeypatch.setattr(gf2_diagnostic, "call_native", fake)
    monkeypatch.setattr(gf2_matrix, "call_native", _math_fake)
    with pytest.raises(ValueError, match="native dim_h1"):
        h1_basis([[1, 0], [0, 1]], [[0, 0]])


def test_native_refusal_is_not_replaced_by_a_python_betti(monkeypatch):
    def boom(action, payload, host=None):
        raise NativeMathRefusal("NATIVE_MATH_REFUSED", "host missing", outcome={"action": action})

    monkeypatch.setattr(gf2_diagnostic, "call_native", boom)
    with pytest.raises(NativeMathRefusal) as refused:
        build_tetron_array(1, 1, "disk")
    assert refused.value.code == "NATIVE_MATH_REFUSED"
    with pytest.raises(NativeMathRefusal) as classified:
        classify([[1], [1], [0]], [[1, 1, 0]], [1, 0, 0])
    assert classified.value.code == "NATIVE_MATH_REFUSED"


def test_repair_capacity_distance_is_visible_in_the_payload(monkeypatch):
    def fake(action, payload, host=None):
        assert action == ACTION
        assert payload["operation"] == "repair_capacity"
        return {"repair_capacity": payload["distance"] - 1, "authority_effect": "None"}

    monkeypatch.setattr(gf2_diagnostic, "call_native", fake)
    assert repair_capacity_native(5) == 4
    assert fake(ACTION, {"operation": "repair_capacity", "distance": 1})["repair_capacity"] == 0


def test_graph_demos_print_native_dim_h1_not_edge_nullity(monkeypatch):
    def fake(action, payload, host=None):
        assert payload["operation"] == "classify"
        return _classify_receipt(dim_h1=7, terminal="Exact")

    monkeypatch.setattr(gf2_diagnostic, "call_native", fake)
    monkeypatch.setattr(gf2_matrix, "call_native", _math_fake)

    betti, _unsat, _f2, _free = benchmark_kitaev_ring_majorana(num_sites=2)
    assert betti == 7

    y_junction = benchmark_microsoft_majorana_y_junction(arm_sites=1, num_trials=1)
    assert y_junction["betti_1_f2"] == 7
    assert y_junction["authority_effect"] == "None"

    carrier = build_tetron_array_carrier(num_tetrons=1)
    assert carrier.metadata["dim_h1"] == 7
    assert carrier.metadata["betti_1_f2"] == 7
    assert carrier.metadata["authority_effect"] == "None"
    assert carrier.metadata["num_bonds"] != 7

    network = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (2, 0)])
    certificate = evaluate_network_majorana_parity(network)
    assert certificate.betti_1_f2 == 7
    assert certificate.is_solvable is True
    assert certificate.authority_effect == "None"
