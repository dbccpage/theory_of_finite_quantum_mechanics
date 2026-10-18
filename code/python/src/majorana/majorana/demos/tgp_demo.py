from __future__ import annotations


import json
import sys
from typing import Any
from omega_engine.crates.majorana.engines.terminalizer import terminalize


def run_tgp_demo() -> dict[str, Any]:
    """Simulate topological gap protocol parameter sensitivity under parameter transport."""

    t_A = 0.35
    residual_A = [1, 1, 0]
    D0_A = [[1, 0], [0, 1], [1, 1]]
    D1_A = [[1, 1, 1]]

    res_A = terminalize(D0_A, D1_A, residual_A)

    t_B = 0.45
    residual_B = [1, 0, 0]
    D0_B = [[1, 0], [0, 1], [1, 1]]
    D1_B = [[1, 1, 1]]

    res_B = terminalize(D0_B, D1_B, residual_B)

    mutation_status = "SilentMutationDetected" if res_A["terminal_status"] != res_B["terminal_status"] else "None"

    return {
        "parameter_t_window_A": {
            "value": t_A,
            "residual": residual_A,
            "terminal_status": res_A["terminal_status"],
            "algebraic_class_id": res_A["algebraic_class_id"],
        },
        "parameter_t_window_B": {
            "value": t_B,
            "residual": residual_B,
            "terminal_status": res_B["terminal_status"],
            "algebraic_class_id": res_B["algebraic_class_id"],
        },
        "transport_status": mutation_status,
        "interpretation": "The same pipeline can expose whether a finite diagnostic changes terminal class under declared parameter transport.",
    }


def main() -> int:
    demo_out = run_tgp_demo()
    print(json.dumps(demo_out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())




