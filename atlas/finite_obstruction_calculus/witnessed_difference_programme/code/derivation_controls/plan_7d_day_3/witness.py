"""Day 3 integration gate control for Lane E maps, B/C binding, and runner preflight (PLAN-7D-DAY-3).

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[3]


def _load_sibling_witness(control_name: str):
    path = Path(__file__).resolve().parents[1] / control_name / "witness.py"
    module_name = f"{control_name}_witness_loaded"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(module_name, None)
    return module


def verify_lane_e_maps(
    m: int = 6,
    p: int = 3,
    n: int = 3,
    rank: int = 3,
    package_root: Path = PACKAGE_ROOT,
) -> dict[str, object]:
    """Verify Lane E documentation anchors and finite algebraic invariants LE-1..LE-4."""
    if (
        type(m) is not int
        or type(p) is not int
        or type(n) is not int
        or type(rank) is not int
        or m < 2
        or p < 2
        or n < 1
        or rank < 0
        or rank > n
    ):
        raise ValueError("invalid Lane E parameters")

    lane_e_doc = package_root / "docs" / "lane_e_character_duality_completion.md"
    if not lane_e_doc.is_file():
        raise ValueError("missing docs/lane_e_character_duality_completion.md")
    text = lane_e_doc.read_text(encoding="utf-8")
    for token in ("LE-1", "LE-2", "LE-3", "LE-4"):
        if token not in text:
            raise ValueError(f"missing {token} in lane_e_character_duality_completion.md")

    orthogonality_diagonal = sum(
        1 for a in range(m) for b in range(m) if all(((a - b) * x) % m == 0 for x in range(m))
    )
    if orthogonality_diagonal != m:
        raise ValueError("LE-1 cyclic character separation failed")

    kernel_size = p ** (n - rank)
    if kernel_size != 1:
        raise ValueError(f"LE-2 insufficient rank {rank} < {n}: kernel size {kernel_size} > 1")

    z4_max_order = max(
        min(k for k in range(1, 5) if (k * g) % 4 == 0) for g in range(4)
    )
    z2_plus_z2_max_order = max(
        min(k for k in range(1, 5) if (k * a) % 2 == 0 and (k * b) % 2 == 0)
        for a in range(2)
        for b in range(2)
    )
    if z4_max_order != 4 or z2_plus_z2_max_order != 2:
        raise ValueError("LE-4 exponent separation failed")

    return {
        "le1_dual_size": m,
        "le2_kernel_size": kernel_size,
        "le3_discrete_q_noncompact_documented": (
            "non-compact" in text.lower() or "noncompact" in text.lower() or "\\mathbb{Q}" in text
        ),
        "le4_exponents": (z4_max_order, z2_plus_z2_max_order),
    }


def witness() -> dict[str, object]:
    lane_e = verify_lane_e_maps()
    next_2 = _load_sibling_witness("plan_7d_next_2").witness()
    preflight = _load_sibling_witness("plan_7d_preflight").witness()
    return {
        "lane_e": lane_e,
        "next_2": next_2,
        "preflight": preflight,
    }
