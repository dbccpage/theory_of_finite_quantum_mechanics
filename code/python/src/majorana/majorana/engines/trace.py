from __future__ import annotations


import argparse
import json
import sys
from pathlib import Path
from typing import Any

from omega_engine.crates.majorana.core.gf2_schema import mod2
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix
from omega_engine.crates.majorana.adapters.graph_to_complex import GraphToComplexAdapter
from omega_engine.crates.majorana.engines.terminalizer import terminalize


def resolve_trace_residual(
    shots: list[int],
    num_checks: int,
    shot_checks: list[int] | None = None,
    readout_policy: str = "majority",
    threshold: float = 0.5,
    declared_window: list[int] | None = None,
) -> list[int]:
    """Resolve a raw sequence of shots into a binary residual vector of size num_checks."""
    if not shots:
        return [0] * num_checks

    check_shots: list[list[int]] = [[] for _ in range(num_checks)]

    if shot_checks is not None:
        for idx, shot in enumerate(shots):
            if idx < len(shot_checks):
                check_idx = shot_checks[idx]
                if 0 <= check_idx < num_checks:
                    check_shots[check_idx].append(shot)
    else:
        if len(shots) == num_checks:
            for i, s in enumerate(shots):
                check_shots[i].append(s)
        elif len(shots) % num_checks == 0:
            k = len(shots) // num_checks
            for i in range(num_checks):
                check_shots[i] = shots[i * k : (i + 1) * k]
        else:
            for idx, s in enumerate(shots):
                check_idx = idx % num_checks
                check_shots[check_idx].append(s)

    residual = [0] * num_checks
    for i in range(num_checks):
        shots_i = list(check_shots[i])

        if declared_window is not None and len(declared_window) == 2:
            start, end = declared_window[0], declared_window[1]
            shots_i = shots_i[start:end]

        if not shots_i:
            residual[i] = 0
            continue

        one_count = sum(1 for s in shots_i if s == 1)
        fraction = one_count / len(shots_i)

        if readout_policy == "majority" or readout_policy == "declared_window":
            residual[i] = 1 if fraction > 0.5 else 0
        elif readout_policy == "threshold":
            residual[i] = 1 if fraction >= threshold else 0
        else:
            residual[i] = 1 if fraction > 0.5 else 0

    return residual


def process_trace(trace_data: dict[str, Any]) -> dict[str, Any]:
    """Parse raw trace dict, build chain complex, and evaluate parity obstruction class."""
    shots = trace_data.get("shots", [])
    declared_checks = trace_data.get("declared_parity_checks", [])
    shot_checks = trace_data.get("shot_checks")
    declared_cycles = trace_data.get("declared_cycles")
    readout_policy = trace_data.get("readout_policy", "majority")
    threshold = trace_data.get("threshold", 0.5)
    declared_window = trace_data.get("declared_window")

    if not declared_checks:
        return {
            "terminal_status": "RepresentationInvalid",
            "reason": "Missing declared_parity_checks",
            "certificate_alpha": None,
            "normal_form": None,
            "coherence_witness": None,
            "q1_norm": None,
            "algebraic_class_id": "representation-invalid:missing_checks",
        }

    v_set = set()
    for edge in declared_checks:
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            return {
                "terminal_status": "RepresentationInvalid",
                "reason": "Each declared check must be an edge pair of length 2",
                "certificate_alpha": None,
                "normal_form": None,
                "coherence_witness": None,
                "q1_norm": None,
                "algebraic_class_id": "representation-invalid:malformed_checks",
            }
        v_set.update(edge)

    v_list = sorted(list(v_set))
    v_to_idx = {v: idx for idx, v in enumerate(v_list)}
    edges = [(v_to_idx[u], v_to_idx[v]) for u, v in declared_checks]

    residual = resolve_trace_residual(
        shots=shots,
        num_checks=len(declared_checks),
        shot_checks=shot_checks,
        readout_policy=readout_policy,
        threshold=threshold,
        declared_window=declared_window,
    )

    try:
        adapter = GraphToComplexAdapter(v_list, edges, declared_cycles or [])
    except ValueError as exc:
        return {
            "terminal_status": "RepresentationInvalid",
            "reason": f"Complex reconstruction failed: {str(exc)}",
            "certificate_alpha": None,
            "normal_form": None,
            "coherence_witness": None,
            "q1_norm": None,
            "algebraic_class_id": "representation-invalid:complex_reconstruction_error",
        }

    return terminalize(adapter.D0, adapter.D1, residual)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ingest raw parity traces and resolve obstruction classes"
    )
    parser.add_argument("trace_file", type=Path, help="Path to raw trace JSON file")
    args = parser.parse_args()

    try:
        with args.trace_file.open("r", encoding="utf-8") as f:
            trace_data = json.load(f)

        result = process_trace(trace_data)
        print(json.dumps(result, indent=2))
        return 0
    except Exception as e:
        print(json.dumps({"error": f"Trace processing failed: {str(e)}"}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())




