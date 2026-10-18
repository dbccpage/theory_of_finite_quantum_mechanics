"""Exact rational image membership and preimage witnesses from native Rust.

Native elimination returns the solution with free variables set to zero. The
Python module only normalizes the public Fraction carrier and preserves shape.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    call_native,
    decode_rational,
)

from .errors import DimensionMismatch
from .qmatrix import QMatrix, _rational


def rank_of(m: QMatrix) -> int:
    """Return exact rank from the canonical native matrix implementation."""
    return m.rank()


def in_image(m: QMatrix, z: Sequence) -> bool:
    """Decide image membership by native exact elimination."""
    return solve(m, z) is not None


def solve(m: QMatrix, z: Sequence) -> list[Fraction] | None:
    """Return an exact preimage, or None when the system is inconsistent."""
    if len(z) != m.rows:
        raise DimensionMismatch(f"target vector length {len(z)} != matrix rows {m.rows}")
    result = call_native(
        "math_rational_matrix",
        {
            "operation": "solve",
            "matrix": m._wire(),
            "vector": [str(_rational(value)) for value in z],
        },
    )["solution"]
    return None if result is None else [decode_rational(value) for value in result]


def solve_witness(m: QMatrix, z: Sequence) -> tuple[bool, list[Fraction] | None]:
    """Return image membership and its native exact witness in one pass."""
    witness = solve(m, z)
    return witness is not None, witness
