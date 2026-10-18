from __future__ import annotations
# SPDX-License-Identifier: Apache-2.0


import json
import sys
from typing import Any, cast
from omega_engine.crates.homology_theory.graph_complex import (
    get_line_wire_complex,
    get_t_junction_complex,
    get_measurement_loop_complex,
    get_two_island_parity_box_complex,
    get_braid_like_square_move_complex,
)
from omega_engine.crates.majorana.adapters.graph_to_complex import GraphToComplexAdapter
from omega_engine.crates.majorana.engines.terminalizer import terminalize, validate_complex


def run_gallery_demo() -> dict[str, Any]:
    """Execute validation and terminalization for the extended graph complex gallery."""
    gallery = {
        "line_wire": {
            "adapter": get_line_wire_complex(),
            "residual": [1, 0],
        },
        "t_junction": {
            "adapter": get_t_junction_complex(),
            "residual": [1, 0, 0],
        },
        "measurement_loop": {
            "adapter": get_measurement_loop_complex(),
            "residual": [1, 1, 0, 0],
        },
        "two_island_parity_box": {
            "adapter": get_two_island_parity_box_complex(),
            "residual": [0, 0, 1],
        },
        "braid_like_square_move": {
            "adapter": get_braid_like_square_move_complex(),
            "residual": [0, 0, 0, 0, 1, 1, 0],
        },
    }

    report = {}
    for name, item in gallery.items():
        adapter = cast(GraphToComplexAdapter, item["adapter"])
        residual = cast(list[int], item["residual"])

        valid = validate_complex(adapter.D0, adapter.D1)

        term_res = terminalize(adapter.D0, adapter.D1, residual)

        report[name] = {
            "vertices": adapter.vertices,
            "edges": adapter.edges,
            "faces": adapter.faces,
            "D1_D0_exact_validation": valid,
            "residual": residual,
            "terminal_status": term_res["terminal_status"],
            "q1_norm": str(term_res["q1_norm"]),
            "algebraic_class_id": term_res["algebraic_class_id"],
        }

    return report


def main() -> int:
    result = run_gallery_demo()
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())




