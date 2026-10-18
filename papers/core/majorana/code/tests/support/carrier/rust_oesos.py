"""Rust OESOS Fresh Solve Replay Request model and builder.

AuthorityEffect: None (const).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from omega_engine.crates.carrier.cochain_carrier import MAX_PROJECTION_EDGES


@dataclass(frozen=True, slots=True)
class RustOesosFreshSolveReplayRequestV1:
    packet_id: str
    num_vertices: int
    edges: tuple[tuple[int, int, int], ...]
    faces: tuple[tuple[int, int, int], ...]
    omega: tuple[int, ...]
    expected_carrier_hash_blake3: str
    solver_registry_hash: str
    source_revision: str
    replay_required: bool = True
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        if len(self.edges) > MAX_PROJECTION_EDGES:
            raise ValueError("carrier exceeds the Rust exact-L1 edge resource fence")

    @property
    def request_id(self) -> str:
        serialized = json.dumps(
            {
                "packet_id": self.packet_id,
                "num_vertices": self.num_vertices,
                "edges": self.edges,
                "faces": self.faces,
                "omega": self.omega,
                "expected_carrier_hash_blake3": self.expected_carrier_hash_blake3,
                "solver_registry_hash": self.solver_registry_hash,
                "source_revision": self.source_revision,
            },
            sort_keys=True,
        )
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def solve_args(self) -> dict[str, Any]:
        return {
            "carrier": {
                "num_vertices": self.num_vertices,
                "edges": self.edges,
                "faces": self.faces,
            },
            "omega": self.omega,
            "expected_carrier_hash_blake3": self.expected_carrier_hash_blake3,
            "solver_registry_hash": self.solver_registry_hash,
            "source_revision": self.source_revision,
        }


def rust_replay_request(
    problem: Any,
    *,
    expected_carrier_hash_blake3: str,
    solver_registry_hash: str,
    source_revision: str,
) -> RustOesosFreshSolveReplayRequestV1:
    carrier = problem.projector.carrier
    edges = tuple((tail, head, weight) for (tail, head), weight in zip(carrier.edges, carrier.weights))
    if hasattr(problem, "native_initial_state") and hasattr(problem.native_initial_state, "as_mapping"):
        mapping = problem.native_initial_state.as_mapping()
        omega = tuple(int(mapping.get(edge, 0)) for edge in carrier.edges)
    elif hasattr(problem, "envelope") and isinstance(problem.envelope.payload, dict) and "omega" in problem.envelope.payload:
        raw_omega = problem.envelope.payload["omega"]
        if isinstance(raw_omega, dict):
            omega = tuple(int(raw_omega.get(edge, 0)) for edge in carrier.edges)
        elif isinstance(raw_omega, (tuple, list)):
            if len(raw_omega) > 0 and isinstance(raw_omega[0], (tuple, list)) and len(raw_omega[0]) == 2:
                mapping = dict(raw_omega)
                omega = tuple(int(mapping.get(edge, 0)) for edge in carrier.edges)
            else:
                omega = tuple(int(x) for x in raw_omega)
        else:
            omega = (0,) * len(edges)
    elif hasattr(problem, "omega"):
        omega = tuple(int(x) for x in problem.omega)
    else:
        omega = (0,) * len(edges)
    return RustOesosFreshSolveReplayRequestV1(
        packet_id=getattr(problem, "problem_id", getattr(getattr(problem, "envelope", None), "task_id", hashlib.sha256(b"problem").hexdigest())),
        num_vertices=len(carrier.nodes),
        edges=edges,
        faces=carrier.faces,
        omega=omega,
        expected_carrier_hash_blake3=expected_carrier_hash_blake3,
        solver_registry_hash=solver_registry_hash,
        source_revision=source_revision,
    )
