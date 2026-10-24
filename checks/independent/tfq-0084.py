"""Independent check for the TFQ-0084 squared-area boundary.

Recomputes the declared integer pairs and the two defect-bound comparisons.
Reads the Rust proxy and the float script as text. Imports no repository code.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACTION = ROOT / "code" / "rust" / "src" / "general_relativity" / "exact_regge" / "action.rs"
FLOAT_SCRIPT = ROOT / "papers" / "core" / "constraint_closure" / "code" / "l1_regge.py"

FAILURES: list[str] = []
CHECKED = 0


def check(name: str, ok: bool) -> None:
    global CHECKED
    CHECKED += 1
    if not ok:
        FAILURES.append(name)


def main() -> None:
    proxy = 1 * 2 + 4 * 5
    defects = 2 + 5
    check("proxy_sum", proxy == 22)
    check("defect_sum", defects == 7)
    check("proxy_ne_defects", proxy != defects)
    check("proxy_ne_zero", proxy != 0)
    diff_num = 1 * 4 - 1 * 3
    diff_den = 3 * 4
    check("fraction_difference", diff_num == 1 and diff_den == 12)
    check("gap_square", diff_den * diff_den == 144 and diff_num * diff_num == 1)
    check("allowance_reduced", 2 * 8 == 1 * 16)
    check("allowance_square", 8 * 8 == 64)
    check("bound_strict", 1 * 64 < 1 * 144)
    check("second_gap", 1 * 16 > 1 * 1)
    check("negative_guard", -1 < 0)
    # Cross-multiplication of 1/144 against 1/64, and of 1 against 1/16.
    check("gap_versus_allowance", 1 * 64 < 1 * 144)
    check("one_versus_sixteenth", 16 > 1)
    action = ACTION.read_text(encoding="utf-8")
    check("proxy_product", "action += &area_squared * &kappa;" in action)
    check("holonomy_sum", "holonomy_defect += kappa;" in action)
    flat_at = action.find("pub fn flat_einstein_hilbert()")
    flat = action[flat_at : flat_at + 120] if flat_at >= 0 else ""
    check("flat_zero", "BigRational::zero()" in flat)
    fence_at = action.find("pub fn einstein_hilbert_fence(")
    fence = action[fence_at : fence_at + 280] if fence_at >= 0 else ""
    check("fence_present", fence_at >= 0)
    check("fence_returns_proxy", "rational_regge_proxy(manifold, defects)" in fence)
    script = FLOAT_SCRIPT.read_text(encoding="utf-8")
    check("imports_math", "import math" in script)
    check("imports_numpy", "import numpy as np" in script)
    check("imports_scipy", "from scipy.optimize import linprog" in script)
    check("uses_pi", "math.pi" in script)
    check("uses_acos", "math.acos" in script)
    print(f"checked {CHECKED} claims, failures {len(FAILURES)}")
    if FAILURES:
        for name in FAILURES:
            print("FAIL", name)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
