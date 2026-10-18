"""GF(2) Majorana diagnostic calls. No Python homology or schedule fallback.

action: majorana_gf2_diagnostic
operations: classify, tetron, lggr, repair_capacity
terminals: Exact, OpenObstruction, ClosedResidual, TypedHarmonic, RepresentationInvalid
topologies: Disk, Cylinder, Torus

Empty matrices keep explicit ``cols``, matching ``math_gf2_matrix``.
AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from omega_engine_operating_system.adapters.rust_host.majorana_math import call_native

from .gf2_schema import mod2

ACTION = "majorana_gf2_diagnostic"

TERMINALS: tuple[str, ...] = (
    "Exact",
    "OpenObstruction",
    "ClosedResidual",
    "TypedHarmonic",
    "RepresentationInvalid",
)

TOPOLOGY_WIRE: dict[str, str] = {
    "disk": "Disk",
    "cylinder": "Cylinder",
    "torus": "Torus",
    "Disk": "Disk",
    "Cylinder": "Cylinder",
    "Torus": "Torus",
}

UNREFINED_TERMINAL: dict[str, str] = {
    "Exact": "Exact",
    "OpenObstruction": "OpenObstruction",
    "ClosedResidual": "ClosedResidual",
    "TypedHarmonic": "ClosedResidual",
    "RepresentationInvalid": "RepresentationInvalid",
}


def matrix_wire(data: Sequence[Sequence[int]], cols: int | None = None) -> dict[str, Any]:
    rows = [[mod2(entry) for entry in row] for row in data]
    width = len(rows[0]) if rows else (0 if cols is None else cols)
    if isinstance(width, bool) or not isinstance(width, int) or width < 0:
        raise ValueError("matrix columns must be a nonnegative integer")
    if rows and cols is not None and cols != width:
        raise ValueError("explicit columns do not match matrix data")
    if any(len(row) != width for row in rows):
        raise ValueError("All matrix rows must have equal length")
    return {"rows": len(rows), "cols": width, "data": rows}


def _require_authority(result: Mapping[str, Any]) -> None:
    if result["authority_effect"] != "None":
        raise ValueError("native majorana_gf2_diagnostic authority_effect must be None")


def _dim_h1(result: Mapping[str, Any]) -> int:
    dim = result["dim_h1"]
    if isinstance(dim, bool) or not isinstance(dim, int) or dim < 0:
        raise ValueError("native majorana_gf2_diagnostic classify returned no dim_h1")
    return dim


def classify_native(
    d0: Sequence[Sequence[int]],
    d1: Sequence[Sequence[int]],
    residual: Sequence[int],
    budget: int | None = None,
) -> Mapping[str, Any]:
    """Schedule class and ``dim_h1`` for one declared complex. Host refusal propagates."""
    channels = len(d0)
    payload: dict[str, Any] = {
        "operation": "classify",
        "d0": matrix_wire(d0, cols=len(d0[0]) if d0 else 0),
        "d1": matrix_wire(d1, cols=len(d1[0]) if d1 else channels),
        "residual": [mod2(bit) for bit in residual],
    }
    if budget is not None:
        if isinstance(budget, bool) or not isinstance(budget, int) or budget < 1:
            raise ValueError("budget must be >= 1")
        payload["budget"] = budget
    result = call_native(ACTION, payload)
    _require_authority(result)
    terminal = result["terminal"]
    if terminal not in TERMINALS:
        raise ValueError(f"native terminal {terminal!r} is not a schedule class")
    return result


def schedule_terminal(native_terminal: str) -> str:
    """Project the native five-way terminal onto the three-way receipt vocabulary."""
    try:
        return UNREFINED_TERMINAL[native_terminal]
    except KeyError as exc:
        raise ValueError(f"native terminal {native_terminal!r} is not a schedule class") from exc


def tetron_native(rows: int, cols: int, topology: str) -> Mapping[str, Any]:
    """Measured tetron homology. ``dim_h1`` is the native field, not a local nullity."""
    try:
        wired = TOPOLOGY_WIRE[topology]
    except KeyError as exc:
        raise ValueError(
            f"unknown topology {topology!r}; expected one of {tuple(TOPOLOGY_WIRE)}"
        ) from exc
    result = call_native(
        ACTION,
        {"operation": "tetron", "rows": rows, "cols": cols, "topology": wired},
    )
    _require_authority(result)
    if result["topology"] != wired:
        raise ValueError("native tetron topology does not match the requested payload")
    for name in ("rank_d0", "rank_d1", "graph_b1", "dim_h1"):
        value = result[name]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"native tetron {name} must be a nonnegative integer")
    return result


def native_dim_h1(
    d0: Sequence[Sequence[int]],
    d1: Sequence[Sequence[int]] | None = None,
) -> int:
    """``dim_h1`` from operation ``classify``.

    When no faces are declared, a single zero row keeps the wire rectangular.
    It adds no constraint, so the dimension is the native nullity of ``d0``.
    """
    channels = len(d0)
    faces: Sequence[Sequence[int]]
    if d1 is None:
        faces = [[0] * channels] if channels else []
    else:
        faces = d1
    result = classify_native(d0, faces, [0] * channels, budget=1)
    return _dim_h1(result)


def lggr_native(
    d0: Sequence[Sequence[int]],
    d1: Sequence[Sequence[int]],
    residual: Sequence[int],
) -> Mapping[str, Any]:
    channels = len(d0)
    result = call_native(
        ACTION,
        {
            "operation": "lggr",
            "d0": matrix_wire(d0, cols=len(d0[0]) if d0 else 0),
            "d1": matrix_wire(d1, cols=len(d1[0]) if d1 else channels),
            "residual": [mod2(bit) for bit in residual],
        },
    )
    _require_authority(result)
    return result


def repair_capacity_native(distance: int) -> int:
    if isinstance(distance, bool) or not isinstance(distance, int):
        raise TypeError("repair capacity distance must be an integer")
    result = call_native(
        ACTION,
        {"operation": "repair_capacity", "distance": distance},
    )
    _require_authority(result)
    capacity = result["repair_capacity"]
    if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 0:
        raise ValueError("native repair_capacity must be a nonnegative integer")
    return capacity
