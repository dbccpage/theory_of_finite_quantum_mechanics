from __future__ import annotations


import json
import sys
from typing import Any

from omega_engine.crates.majorana.engines.terminalizer import terminalize


def run_ambiguity_demo() -> dict[str, Any]:
    """Compare topological vs trivial carrier complexes with the same observed residual."""
    observed_residual = [0, 0, 1]

    D0_topological = [
        [1, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
    ]
    D1_topological = [
        [0, 0, 0],
    ]

    res_topological = terminalize(D0_topological, D1_topological, observed_residual)

    D0_trivial = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 1],
    ]
    D1_trivial = [
        [0, 0, 0],
    ]

    res_trivial = terminalize(D0_trivial, D1_trivial, observed_residual)

    return {
        "observed_residual": observed_residual,
        "topological_carrier": {
            "terminal_status": res_topological["terminal_status"],
            "q1_norm": str(res_topological["q1_norm"]),
            "reason": res_topological["reason"],
            "algebraic_class_id": res_topological["algebraic_class_id"],
        },
        "trivial_carrier": {
            "terminal_status": res_trivial["terminal_status"],
            "q1_norm": str(res_trivial["q1_norm"]),
            "reason": res_trivial["reason"],
            "algebraic_class_id": res_trivial["algebraic_class_id"],
        },
        "interpretation": "same observation, different obstruction class under declared carrier",
    }


def main() -> int:
    demo_out = run_ambiguity_demo()
    print(json.dumps(demo_out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())




