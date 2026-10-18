from __future__ import annotations

from dataclasses import dataclass

MAX_PROJECTION_EDGES = 36


@dataclass(frozen=True, slots=True)
class CochainCarrier:
    nodes: tuple[int, ...]
    edges: tuple[tuple[int, int], ...]
    faces: tuple[tuple[int, int, int], ...]
    weights: tuple[int, ...]

    @property
    def carrier_id(self) -> str:
        return "finite-cochain-2-v1"

    def __post_init__(self) -> None:
        if not self.nodes or len(set(self.nodes)) != len(self.nodes):
            raise ValueError("carrier nodes must be non-empty and unique")
        if len(self.edges) != len(self.weights):
            raise ValueError("carrier requires one weight per edge")
        if not self.edges:
            raise ValueError("carrier requires at least one edge")
        if len(self.edges) > MAX_PROJECTION_EDGES:
            raise ValueError("carrier exceeds the Rust exact-L1 edge resource fence")
        if len(self.nodes) + len(self.faces) > MAX_PROJECTION_EDGES:
            raise ValueError("carrier exceeds the Rust projection resource fence")
        if len({frozenset(edge) for edge in self.edges}) != len(self.edges):
            raise ValueError("carrier unordered edge pairs must be unique")
        node_set = set(self.nodes)
        if any(
            tail == head or tail not in node_set or head not in node_set
            for tail, head in self.edges
        ):
            raise ValueError("carrier edges require distinct declared endpoints")
        if any(weight <= 0 or weight >= 1 << 127 for weight in self.weights):
            raise ValueError("edge weights must be positive Rust i128 values")
        undirected_edges = {frozenset(edge) for edge in self.edges}
        if len({tuple(sorted(face)) for face in self.faces}) != len(self.faces):
            raise ValueError("carrier unordered faces must be unique")
        for face in self.faces:
            if len(set(face)) != 3 or any(node not in node_set for node in face):
                raise ValueError("faces require three distinct declared vertices")
            a, b, c = face
            if any(
                frozenset(side) not in undirected_edges
                for side in ((a, b), (b, c), (c, a))
            ):
                raise ValueError("every face boundary must use declared carrier edges")


def carrier_to_network(carrier: CochainCarrier) -> Any:
    """Adapt a CochainCarrier domain entity into a numerical Network object."""
    try:
        from ..residuals.network_residual import Network
    except ImportError:
        from omega_engine.crates.residuals.network_residual import Network
    return Network(
        nodes=list(carrier.nodes),
        edges=list(carrier.edges),
        faces=list(carrier.faces),
    )

