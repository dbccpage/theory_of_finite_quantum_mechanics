"""Paper-side client for the native ``majorana_gf2_diagnostic`` action.

AuthorityEffect: None.

Classification, tetron homology, the LGGR witness, and repair capacity are owned
by the Rust crate. This module checks the wire shape and does not solve GF(2)
systems when the host is absent.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from omega_engine_operating_system.adapters.rust_host.majorana_math import call_native

_ACTION = "majorana_gf2_diagnostic"
_TERMINALS = frozenset(
    {
        "Exact",
        "OpenObstruction",
        "ClosedResidual",
        "TypedHarmonic",
        "RepresentationInvalid",
    }
)
_TOPOLOGY = {"disk": "Disk", "cylinder": "Cylinder", "torus": "Torus"}


def _count(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, not a bool or float")
    if value < 0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def _bit(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("GF(2) entry must be integer 0 or 1, not a bool or float")
    if value not in (0, 1):
        raise ValueError(f"GF(2) entry must be 0 or 1, got {value}")
    return value


def _flag(value: object, name: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{name} must be a bool")
    return value


def _required_int(result: Mapping[str, Any], key: str) -> int:
    value = result[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"native {key} must be an integer")
    return value


def _authority(result: Mapping[str, Any]) -> None:
    if result.get("authority_effect") != "None":
        raise ValueError("native diagnostic authority_effect must be None")


def topology_name(topology: str) -> str:
    """Return the native topology spelling, or refuse an unknown name."""
    if not isinstance(topology, str):
        raise TypeError("topology must be a string")
    try:
        return _TOPOLOGY[topology.lower()]
    except KeyError as error:
        raise ValueError(f"Unknown topology: {topology}") from error


def matrix_wire(rows: int, cols: int, data: Sequence[Sequence[int]]) -> dict[str, Any]:
    """Build a GF(2) matrix object of integer bits. Floats are refused."""
    row_count = _count(rows, "rows")
    col_count = _count(cols, "cols")
    wired: list[list[int]] = []
    for row in data:
        bits = [_bit(entry) for entry in row]
        if len(bits) != col_count:
            raise ValueError("matrix row width does not match cols")
        wired.append(bits)
    if len(wired) != row_count:
        raise ValueError("matrix row count does not match rows")
    return {"rows": row_count, "cols": col_count, "data": wired}


def _invoke(payload: dict[str, Any]) -> dict[str, Any]:
    result = call_native(_ACTION, payload)
    if not isinstance(result, dict):
        raise ValueError("native diagnostic result must be an object")
    return result


def _wire_field(value: object) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("native matrix must be an object")
    return matrix_wire(value["rows"], value["cols"], value["data"])


def classify(
    d0: Mapping[str, Any],
    d1: Mapping[str, Any],
    residual: Sequence[int],
    *,
    budget: int,
    diagnostics: bool,
) -> dict[str, Any]:
    """Classify one residual. The terminal is the native schedule class."""
    payload = {
        "operation": "classify",
        "d0": _wire_field(d0),
        "d1": _wire_field(d1),
        "residual": [_bit(bit) for bit in residual],
        "budget": _count(budget, "budget"),
        "diagnostics": _flag(diagnostics, "diagnostics"),
    }
    result = _invoke(payload)
    _authority(result)
    if result.get("terminal") not in _TERMINALS:
        raise ValueError(f"native terminal is not a diagnostic class: {result.get('terminal')!r}")
    return result


def tetron(rows: int, cols: int, topology: str) -> dict[str, Any]:
    """Fetch one tetron carrier. ``dim_h1`` is the native measurement."""
    payload = {
        "operation": "tetron",
        "rows": _count(rows, "rows"),
        "cols": _count(cols, "cols"),
        "topology": topology_name(topology),
    }
    result = _invoke(payload)
    _authority(result)
    for key in ("dim_h1", "num_mzm", "num_channels", "num_islands"):
        _required_int(result, key)
    d0 = _wire_field(result["d0"])
    d1 = _wire_field(result["d1"])
    if (d0["rows"], d0["cols"]) != (result["num_channels"], result["num_mzm"]):
        raise ValueError("native tetron d0 does not match the reported counts")
    if (d1["rows"], d1["cols"]) != (result["num_islands"], result["num_channels"]):
        raise ValueError("native tetron d1 does not match the reported counts")
    return result


def lggr(d0: Mapping[str, Any], d1: Mapping[str, Any], omega: Sequence[int]) -> dict[str, Any]:
    """Read the native local-green / global-red witness."""
    payload = {
        "operation": "lggr",
        "d0": _wire_field(d0),
        "d1": _wire_field(d1),
        "omega": [_bit(bit) for bit in omega],
    }
    result = _invoke(payload)
    _authority(result)
    for key in ("local_green", "global_red", "is_lggr", "d1_omega"):
        if key not in result:
            raise ValueError(f"native lggr reply lacks {key}")
    status = result.get("status")
    certificate = result.get("certificate")
    if status is None and isinstance(certificate, Mapping):
        status = certificate.get("status")
    if not isinstance(status, str) or not status:
        raise ValueError("native lggr reply lacks status")
    for key in ("local_green", "global_red", "is_lggr"):
        if type(result[key]) is not bool:
            raise TypeError(f"native {key} must be a bool")
    return result


def repair_capacity(
    *,
    distance: int | None = None,
    cycles: Sequence[Sequence[int]] | None = None,
) -> int | None:
    """Native repair radius, or the native minimum cycle weight.

    Pass ``distance`` for ``t = floor((d-1)/2)``. Pass ``cycles`` for the minimum
    weight. ``distance`` 0 is sent and refused by the host; this function does
    not compute the radius itself. A null ``min_weight`` stays null.
    """
    if (distance is None) == (cycles is None):
        raise TypeError("repair_capacity requires exactly one of distance or cycles")
    if distance is not None:
        result = _invoke(
            {"operation": "repair_capacity", "distance": _count(distance, "distance")}
        )
        value = result["t"]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("native repair capacity t must be an integer")
        return value
    result = _invoke(
        {
            "operation": "repair_capacity",
            "cycles": [[_bit(bit) for bit in cycle] for cycle in cycles or ()],
        }
    )
    weight = result["min_weight"]
    if weight is None:
        return None
    if isinstance(weight, bool) or not isinstance(weight, int):
        raise ValueError("native min_weight must be an integer or null")
    return weight
