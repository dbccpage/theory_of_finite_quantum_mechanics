"""Bound certificates to the complete, independently declared finite cases."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .algebra import certify_homology, check_homology, check_top_cycle_pairing, matrices
from .model import (
    MAX_PAIRS,
    TopologyRefusal,
    boundary,
    direct_cell_baseline,
    enumerate_cells,
    task_cells,
)

SCHEMA = "wdp-guarded-schedule-topology-certificate-v1"


def encoded(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("ascii")


def digest(value: object) -> str:
    return hashlib.sha256(encoded(value)).hexdigest()


def source_hashes(package: Path) -> dict[str, str]:
    paths = [*sorted((package / "code/guarded_schedule_topology").glob("*.py")),
             *(package / "scripts" / name for name in (
                 "verify_guarded_schedule_topology.py", "check_guarded_coherence.py",
                 "check_causal_execution.py", "check_causal_three_cells.py", "check_ideal_prices.py"))]
    return {path.relative_to(package).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths}


def read_certificate_data(path: Path) -> tuple[object, bytes]:
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise TopologyRefusal("duplicate JSON object key")
            result[key] = value
        return result

    def reject_number(value):
        raise TopologyRefusal(f"nonintegral certificate number: {value}")

    with path.open("rb") as stream:
        data = stream.read(16 * 1024 * 1024 + 1)
    if len(data) > 16 * 1024 * 1024:
        raise TopologyRefusal("certificate exceeds the declared sixteen-MiB input bound")
    value = json.loads(data, object_pairs_hook=pairs, parse_float=reject_number,
                       parse_constant=reject_number)
    return value, data


def read_certificate(path: Path) -> object:
    return read_certificate_data(path)[0]


def case_keys() -> tuple[tuple[int, int], ...]:
    return tuple((n, capacity) for n in range(1, MAX_PAIRS + 1)
                 for capacity in range(n + 1))


def build_certificate(package: Path) -> dict:
    cases = []
    for n, capacity in case_keys():
        native = enumerate_cells(n, capacity)
        tasks = task_cells(n, capacity)
        native_proof, _ = certify_homology(matrices(native))
        task_proof, _ = certify_homology(matrices(tasks))
        witness = None
        if n >= 3 and capacity == n - 1:
            facets = boundary((tuple(range(n)),))
            cycle = [[i, facets[cell]] for i, cell in enumerate(tasks[-1])]
            witness = {"degree": n - 2, "cycle": cycle,
                       "cochain": [[0, 1]], "pairing": cycle[0][1]}
        cases.append({"pairs": n, "capacity": capacity,
                      "native_cells_sha256": digest(native),
                      "task_cells_sha256": digest(tasks),
                      "native_reduction": native_proof, "task_reduction": task_proof,
                      "top_cycle_pairing": witness})
    return {"schema": SCHEMA, "authority_effect": "None",
            "sources": source_hashes(package), "cases": cases}


def _essential_betti(betti: list[int] | None) -> list[int] | None:
    if betti is None:
        return None
    trimmed = list(betti)
    while trimmed and trimmed[-1] == 0:
        trimmed.pop()
    return trimmed


def check_certificate(package: Path, certificate: object, *, direct_baseline: bool = True) -> dict:
    if (type(certificate) is not dict
            or set(certificate) != {"schema", "authority_effect", "sources", "cases"}
            or certificate["schema"] != SCHEMA or certificate["authority_effect"] != "None"):
        raise TopologyRefusal("invalid topology certificate envelope")
    if certificate["sources"] != source_hashes(package):
        raise TopologyRefusal("certificate sources differ from the checked implementation")
    cases = certificate["cases"]
    if type(cases) is not list or len(cases) != len(case_keys()):
        raise TopologyRefusal("certificate must cover every declared pair/capacity case")
    results = []
    for (n, capacity), case in zip(case_keys(), cases):
        if (type(case) is not dict or set(case) != {
                "pairs", "capacity", "native_cells_sha256", "task_cells_sha256",
                "native_reduction", "task_reduction", "top_cycle_pairing"}
                or type(case["pairs"]) is not int or case["pairs"] != n
                or type(case["capacity"]) is not int or case["capacity"] != capacity):
            raise TopologyRefusal("case inventory changed or a case is out of order")
        native, tasks = enumerate_cells(n, capacity), task_cells(n, capacity)
        if case["native_cells_sha256"] != digest(native) or case["task_cells_sha256"] != digest(tasks):
            raise TopologyRefusal("certificate cell inventory changed")
        checked = check_homology(matrices(native), case["native_reduction"])
        task_checked = check_homology(matrices(tasks), case["task_reduction"])
        witness_result = None
        if n >= 3 and capacity == n - 1:
            witness_result = check_top_cycle_pairing(matrices(tasks), case["top_cycle_pairing"])
        elif case["top_cycle_pairing"] is not None:
            raise TopologyRefusal("top pairing is outside its declared maximal-capacity cases")
        # Compare actual computed homology after trailing zero groups are
        # removed; cell dimensions differ between the two constructions.
        if (checked["status"] != "CERTIFIED" or task_checked["status"] != "CERTIFIED"
                or _essential_betti(checked["integral_betti"])
                != _essential_betti(task_checked["integral_betti"])):
            raise TopologyRefusal("the proposed native/task integral homology comparison is unproved")
        if direct_baseline and native != direct_cell_baseline(n, capacity):
            raise TopologyRefusal("block recursion disagrees with exhaustive word-refinement baseline")
        results.append({"pairs": n, "capacity": capacity, "native": checked,
                        "task": task_checked,
                        "top_cycle_pairing": witness_result,
                        "all_vertex_refinements_checked": direct_baseline})
    return {"schema": "wdp-guarded-schedule-topology-check-v1", "status": "PASS",
            "authority_effect": "None", "cases": results,
            "finite_scope": {"pair_counts": [1, 2, 3, 4], "capacities": "every integer 0..n"},
            "homology_convention": "ordinary integral H_k for k >= 0; empty complex has no nonzero such groups",
            "homotopy_claim_from_computation": False}
