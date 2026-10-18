from __future__ import annotations

import warnings
from collections import deque
from dataclasses import dataclass
from typing import Any, Mapping, Sequence, TypeAlias, cast
import hashlib
import json


class DirectedGraphError(Exception):
    """Base class for finite directed graph construction/validation errors."""


class NodeCountMismatch(DirectedGraphError):
    def __str__(self) -> str:
        return "node count must match node index cardinality"


class InvalidNodeIndex(DirectedGraphError):
    def __str__(self) -> str:
        return "node index values must be unique and in range"


@dataclass(frozen=True)
class IndexOutOfRange(DirectedGraphError):
    index: int

    def __str__(self) -> str:
        return f"edge endpoint {self.index} is out of range"


@dataclass(frozen=True)
class SelfLoop(DirectedGraphError):
    index: int

    def __str__(self) -> str:
        return f"self-loops are not allowed at index {self.index}"


@dataclass(frozen=True)
class DuplicateEdge(DirectedGraphError):
    src: int
    dst: int

    def __str__(self) -> str:
        return f"duplicate edge ({self.src}, {self.dst}) is not allowed"


class ContainsCycles(DirectedGraphError):
    def __str__(self) -> str:
        return "graph contains cycles, violating poset antisymmetry"


class NamedEdgeResolutionError(Exception):
    """Base class for named-edge resolution failures."""


@dataclass(frozen=True)
class MissingNodeName(NamedEdgeResolutionError):
    name: str

    def __str__(self) -> str:
        return f"missing node name in edge endpoint: {self.name}"


@dataclass(frozen=True)
class DuplicateNode(NamedEdgeResolutionError):
    name: str

    def __str__(self) -> str:
        return f"duplicate node name: {self.name}"


@dataclass(frozen=True)
class NamedSelfLoop(NamedEdgeResolutionError):
    name: str

    def __str__(self) -> str:
        return f"self-loop at named node: {self.name}"


@dataclass(frozen=True)
class NamedGraphError(NamedEdgeResolutionError):
    error: DirectedGraphError

    def __str__(self) -> str:
        return f"graph construction error: {self.error}"


# ---------------------------------------------------------------------------
# Payload / provenance validation errors (typed)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MalformedGraphPayload(DirectedGraphError):
    field: str
    expected: str

    def __str__(self) -> str:
        return f"malformed graph payload field {self.field}: expected {self.expected}"


@dataclass(frozen=True)
class MalformedProvenancePayload(DirectedGraphError):
    field: str
    expected: str

    def __str__(self) -> str:
        return f"malformed provenance field {self.field}: expected {self.expected}"


@dataclass(frozen=True)
class InvalidProvenanceKind(DirectedGraphError):
    value: str

    def __str__(self) -> str:
        return f"invalid provenance kind: {self.value}"


@dataclass(frozen=True)
class DuplicateNodeName(DirectedGraphError):
    name: str

    def __str__(self) -> str:
        return f"duplicate node name: {self.name}"


@dataclass(frozen=True)
class DeprecatedPosetAliasUsed(DirectedGraphError):
    def __str__(self) -> str:
        return "FinitePosetGraph is removed; use FiniteDirectedGraph and call validate_poset() explicitly"


# ---------------------------------------------------------------------------
# Runtime validation helpers (no coercion)
# ---------------------------------------------------------------------------


def _require_int(value: object, field: str) -> int:
    # Reject booleans (subclass of int) and non-ints to avoid permissive coercion
    if isinstance(value, bool) or not isinstance(value, int):
        raise MalformedGraphPayload(field=field, expected="int")
    return value


def _require_str(value: object, field: str) -> str:
    if not isinstance(value, str) or value == "":
        raise MalformedGraphPayload(field=field, expected="non-empty str")
    return value


def _require_list(value: object, field: str) -> list[object]:
    # Require a concrete list (JSON-deserialized) rather than a generic Sequence
    if not isinstance(value, list):
        raise MalformedGraphPayload(field=field, expected="list")
    return value


def _require_mapping(value: object, field: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise MalformedGraphPayload(field=field, expected="mapping")
    return cast(Mapping[str, object], value)


# ---------------------------------------------------------------------------
# Provenance and witness.
# ---------------------------------------------------------------------------

try:
    from omega_engine.crates.linear_algebra_theory.proof import TheoremProvenance, TheoremId, CertificateId, ReplayHash, BoundaryId, ReviewerId
except ImportError:
    from arithmos.linear_algebra.proof import TheoremProvenance, TheoremId, CertificateId, ReplayHash, BoundaryId, ReviewerId

@dataclass(frozen=True)
class DirectedGraphWitness:
    """Structural witness over canonical edge data."""

    edge_hash: bytes

    @classmethod
    def new(cls, edges: Sequence[tuple[int, int]], nodes: Sequence[str]) -> "DirectedGraphWitness":
        # Include node names and canonical edge list so witness distinguishes
        # graphs that share edge topology but differ in node identities.
        canonical_edges = sorted((int(src), int(dst)) for src, dst in edges)
        payload_obj = {"nodes": list(nodes), "edges": canonical_edges}
        payload = json.dumps(payload_obj, separators=(",", ":"), sort_keys=True).encode("utf-8")
        return cls(edge_hash=hashlib.sha256(payload).digest())

    def hex(self) -> str:
        return self.edge_hash.hex()

    def to_dict(self) -> dict[str, str]:
        return {"edge_hash": self.hex()}


# Compatibility alias
PosetWitness = DirectedGraphWitness


# ---------------------------------------------------------------------------
# Finite directed graph.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FiniteDirectedGraph:
    """Finite directed graph carrier.

    This is the universal graph type used across the Python POC: Hodge solvers,
    Hamiltonian flows, obstruction calculus, sheaf-theoretic carriers, routing
    DAGs, etc. It stores named vertices, directed edges, a structural witness
    hash, and provenance.

    Construction rejects self-loops and duplicate edges but permits cycles.
    For poset validation, call ``validate_poset()`` after construction.
    """

    _nodes: tuple[str, ...]
    _node_index: dict[str, int]
    _edges: tuple[tuple[int, int], ...]
    _witness: DirectedGraphWitness
    _provenance: TheoremProvenance

    @classmethod
    def new(
        cls,
        nodes: Sequence[str],
        node_index: Mapping[str, int],
        edges: Sequence[tuple[int, int]],
        provenance: TheoremProvenance,
    ) -> "FiniteDirectedGraph":
        # Validate node names (reject non-string and duplicates)
        node_list: list[str] = []
        seen_names: set[str] = set()
        for i, raw_name in enumerate(nodes):
            name = _require_str(raw_name, f"nodes[{i}]")
            if name in seen_names:
                raise DuplicateNodeName(name)
            seen_names.add(name)
            node_list.append(name)

        # Validate node index mapping (require string keys and int values)
        index_map: dict[str, int] = {}
        for raw_k, raw_v in node_index.items():
            k = _require_str(raw_k, "node_index.key")
            v = _require_int(raw_v, f"node_index[{k}]")
            index_map[k] = v

        if len(node_list) != len(index_map):
            raise NodeCountMismatch()

        # Ensure index ordering and uniqueness
        for expected_index, name in enumerate(node_list):
            mapped = index_map.get(name)
            if mapped != expected_index:
                raise InvalidNodeIndex()

        seen_indices: set[int] = set()
        for index in index_map.values():
            if index < 0 or index >= len(node_list) or index in seen_indices:
                raise InvalidNodeIndex()
            seen_indices.add(index)

        # Validate edges strictly (require 2-tuples of ints)
        edge_list: list[tuple[int, int]] = []
        for i, raw_edge in enumerate(edges):
            if not isinstance(raw_edge, Sequence) or isinstance(raw_edge, (str, bytes)):
                raise MalformedGraphPayload(field=f"edges[{i}]", expected="pair")
            if len(raw_edge) != 2:
                raise MalformedGraphPayload(field=f"edges[{i}]", expected="pair of two ints")
            src = _require_int(raw_edge[0], f"edges[{i}][0]")
            dst = _require_int(raw_edge[1], f"edges[{i}][1]")
            if src < 0 or src >= len(node_list):
                raise IndexOutOfRange(src)
            if dst < 0 or dst >= len(node_list):
                raise IndexOutOfRange(dst)
            if src == dst:
                raise SelfLoop(src)
            if (src, dst) in edge_list:
                raise DuplicateEdge(src, dst)
            edge_list.append((src, dst))

        witness = DirectedGraphWitness.new(edge_list, node_list)
        return cls(
            _nodes=tuple(node_list),
            _node_index=dict(index_map),
            _edges=tuple(edge_list),
            _witness=witness,
            _provenance=provenance,
        )

    @classmethod
    def from_pairs(
        cls,
        pairs: Sequence[tuple[int, int]],
        provenance: TheoremProvenance,
    ) -> "FiniteDirectedGraph":
        if len(pairs) == 0:
            raise MalformedGraphPayload(field="pairs", expected="non-empty pairs or explicit node count")
        max_idx = max((max(int(src), int(dst)) for src, dst in pairs))
        return DirectedGraphBuilder.from_anonymous(max_idx + 1, list(pairs), provenance)

    def validate_poset(self) -> None:
        """Validate strict acyclicity using Kahn's topological-sort algorithm.

        This is optional. It is intentionally not enforced during graph
        construction because this carrier is also used for general directed
        graphs where cycles are meaningful.
        """
        n = len(self._nodes)
        in_degree = [0 for _ in range(n)]
        adj: list[list[int]] = [[] for _ in range(n)]
        for src, dst in self._edges:
            adj[src].append(dst)
            in_degree[dst] += 1

        queue: deque[int] = deque(i for i, degree in enumerate(in_degree) if degree == 0)
        visited_count = 0
        while queue:
            u = queue.popleft()
            visited_count += 1
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if visited_count != n:
            raise ContainsCycles()

    def incidence_d0(self) -> Any:
        from .qmatrix import QMatrix
        n_edges = self.num_edges() if callable(self.num_edges) else self.num_edges
        n_nodes = self.num_nodes() if callable(self.num_nodes) else self.num_nodes
        d0 = QMatrix.zero(n_edges, n_nodes)
        for i, (u, v) in enumerate(self._edges):
            d0.data[i][u] = -1
            d0.data[i][v] = 1
        return d0

    def find_edge(self, src: int, dst: int) -> tuple[int, int] | None:
        for idx, (u, v) in enumerate(self._edges):
            if u == src and v == dst:
                return (idx, 1)
            if u == dst and v == src:
                return (idx, -1)
        return None

    # ------------------------------------------------------------------
    # Accessors matching Rust naming.
    # ------------------------------------------------------------------

    def num_nodes(self) -> int:
        return len(self._nodes)

    def node_count(self) -> int:
        return len(self._nodes)

    def num_edges(self) -> int:
        return len(self._edges)

    def edge_count(self) -> int:
        return len(self._edges)

    def nodes(self) -> tuple[str, ...]:
        return self._nodes

    def node_index(self) -> dict[str, int]:
        return dict(self._node_index)

    def edges(self) -> tuple[tuple[int, int], ...]:
        return self._edges

    def covering_edges(self) -> tuple[tuple[int, int], ...]:
        return self._edges

    def witness(self) -> DirectedGraphWitness:
        return self._witness

    def provenance(self) -> TheoremProvenance:
        return self._provenance

    def index_of(self, name: str) -> int:
        try:
            return self._node_index[name]
        except KeyError as exc:
            raise MissingNodeName(name) from exc

    def name_of(self, index: int) -> str:
        if index < 0 or index >= len(self._nodes):
            raise IndexOutOfRange(index)
        return self._nodes[index]

    def adjacency(self) -> tuple[tuple[int, ...], ...]:
        adj: list[list[int]] = [[] for _ in self._nodes]
        for src, dst in self._edges:
            adj[src].append(dst)
        return tuple(tuple(row) for row in adj)

    def in_degrees(self) -> tuple[int, ...]:
        deg = [0 for _ in self._nodes]
        for _, dst in self._edges:
            deg[dst] += 1
        return tuple(deg)

    def out_degrees(self) -> tuple[int, ...]:
        deg = [0 for _ in self._nodes]
        for src, _ in self._edges:
            deg[src] += 1
        return tuple(deg)

    def to_dict(self) -> dict[str, object]:
        return {
            "nodes": list(self._nodes),
            "node_index": dict(self._node_index),
            "edges": [list(edge) for edge in self._edges],
            "witness": self._witness.to_dict(),
            "provenance": self._provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "FiniteDirectedGraph":
        provenance_raw = payload.get("provenance")
        if provenance_raw is None:
            raise MalformedProvenancePayload(field="provenance", expected="mapping with provenance data")
        if not isinstance(provenance_raw, Mapping):
            raise MalformedProvenancePayload(field="provenance", expected="mapping")
        provenance_payload = cast(Mapping[str, object], provenance_raw)

        # In this POC, we reconstruct provenance from dict fields.
        # This is a bit simplified compared to the full proof.py logic.
        try:
            from omega_engine.crates.linear_algebra_theory.proof import ProvenanceKind, TheoremBoundaryRisk
        except ImportError:
            from arithmos.linear_algebra.proof import ProvenanceKind, TheoremBoundaryRisk
        # Provenance: require explicit, well-typed fields; do not fabricate defaults.
        kind_raw = provenance_payload.get("kind")
        if not isinstance(kind_raw, str):
            raise MalformedProvenancePayload(field="kind", expected="ProvenanceKind string")
        try:
            kind = ProvenanceKind(kind_raw)
        except ValueError as exc:
            raise InvalidProvenanceKind(kind_raw) from exc

        theorem_id_raw = provenance_payload.get("theorem_id")
        if not isinstance(theorem_id_raw, str) or theorem_id_raw == "":
            raise MalformedProvenancePayload(field="theorem_id", expected="non-empty string")

        certificate_id = None
        if "certificate_id" in provenance_payload:
            cert_raw = provenance_payload.get("certificate_id")
            if not isinstance(cert_raw, str) or cert_raw == "":
                raise MalformedProvenancePayload(field="certificate_id", expected="non-empty string")
            certificate_id = CertificateId(cert_raw)

        replay_hash = None
        if "replay_hash" in provenance_payload:
            rh_raw = provenance_payload.get("replay_hash")
            if not isinstance(rh_raw, str) or len(rh_raw) != 64:
                raise MalformedProvenancePayload(field="replay_hash", expected="64-char hex string")
            try:
                replay_hash = ReplayHash(bytes.fromhex(rh_raw))
            except ValueError:
                raise MalformedProvenancePayload(field="replay_hash", expected="valid hex string")

        boundary_id = None
        if "boundary_id" in provenance_payload:
            b_raw = provenance_payload.get("boundary_id")
            if not isinstance(b_raw, str) or b_raw == "":
                raise MalformedProvenancePayload(field="boundary_id", expected="non-empty string")
            boundary_id = BoundaryId(b_raw)

        reviewer = None
        if "reviewer" in provenance_payload:
            r_raw = provenance_payload.get("reviewer")
            if not isinstance(r_raw, str) or r_raw == "":
                raise MalformedProvenancePayload(field="reviewer", expected="non-empty string")
            reviewer = ReviewerId(r_raw)

        risk = None
        if "risk" in provenance_payload:
            risk_raw = provenance_payload.get("risk")
            if not isinstance(risk_raw, str) or risk_raw == "":
                raise MalformedProvenancePayload(field="risk", expected="non-empty string")
            risk = TheoremBoundaryRisk(risk_raw)

        provenance = TheoremProvenance(
            kind=kind,
            theorem_id=TheoremId(theorem_id_raw),
            certificate_id=certificate_id,
            replay_hash=replay_hash,
            boundary_id=boundary_id,
            reviewer=reviewer,
            risk=risk,
        )

        nodes_raw = payload.get("nodes")
        if nodes_raw is None:
            raise MalformedGraphPayload(field="nodes", expected="list of node names")
        # require concrete list to avoid treating strings as sequences
        nodes_list = _require_list(nodes_raw, "nodes")
        nodes = [ _require_str(x, f"nodes[{i}]") for i, x in enumerate(nodes_list) ]

        node_index_raw = payload.get("node_index")
        if node_index_raw is None:
            raise MalformedGraphPayload(field="node_index", expected="mapping")
        node_index_map = _require_mapping(node_index_raw, "node_index")
        node_index: dict[str, int] = {}
        for raw_k, raw_v in node_index_map.items():
            k = _require_str(raw_k, "node_index.key")
            v = _require_int(raw_v, f"node_index[{k}]")
            node_index[k] = v

        edges_raw = payload.get("edges")
        if edges_raw is None:
            raise MalformedGraphPayload(field="edges", expected="list of pairs")
        edges_seq = _require_list(edges_raw, "edges")
        edges: list[tuple[int, int]] = []
        for i, edge_raw in enumerate(edges_seq):
            if not isinstance(edge_raw, Sequence) or isinstance(edge_raw, (str, bytes)):
                raise MalformedGraphPayload(field=f"edges[{i}]", expected="pair of ints")
            if len(edge_raw) != 2:
                raise MalformedGraphPayload(field=f"edges[{i}]", expected="pair of ints")
            src = _require_int(edge_raw[0], f"edges[{i}][0]")
            dst = _require_int(edge_raw[1], f"edges[{i}][1]")
            edges.append((src, dst))

        return cls.new(nodes, node_index, edges, provenance)


class DirectedGraphBuilder:
    """Builder namespace for finite directed graphs."""

    @staticmethod
    def build(
        nodes: Sequence[str],
        node_index: Mapping[str, int],
        edges: Sequence[tuple[int, int]],
        provenance: TheoremProvenance,
    ) -> FiniteDirectedGraph:
        return FiniteDirectedGraph.new(nodes, node_index, edges, provenance)

    @staticmethod
    def from_named(
        nodes: Sequence[str],
        named_edges: Sequence[tuple[str, str]],
        provenance: TheoremProvenance,
    ) -> FiniteDirectedGraph:
        node_list = [str(name) for name in nodes]
        node_index: dict[str, int] = {}
        for index, name in enumerate(node_list):
            if name in node_index:
                raise DuplicateNode(name)
            node_index[name] = index

        edges: list[tuple[int, int]] = []
        for src, dst in named_edges:
            src = str(src)
            dst = str(dst)
            if src == dst:
                raise NamedSelfLoop(src)
            if src not in node_index:
                raise MissingNodeName(src)
            if dst not in node_index:
                raise MissingNodeName(dst)
            edges.append((node_index[src], node_index[dst]))

        try:
            return FiniteDirectedGraph.new(node_list, node_index, edges, provenance)
        except DirectedGraphError as exc:
            raise NamedGraphError(exc) from exc

    @staticmethod
    def from_anonymous(
        num_nodes: int,
        edges: Sequence[tuple[int, int]],
        provenance: TheoremProvenance,
    ) -> FiniteDirectedGraph:
        if num_nodes < 0:
            raise InvalidNodeIndex()
        nodes = [f"n{index}" for index in range(num_nodes)]
        node_index = {name: index for index, name in enumerate(nodes)}
        return FiniteDirectedGraph.new(nodes, node_index, list(edges), provenance)

    @staticmethod
    def chain(n: int, provenance: TheoremProvenance) -> FiniteDirectedGraph:
        if n < 0:
            raise InvalidNodeIndex()
        nodes = [f"v{index}" for index in range(n)]
        named_edges = [(f"v{index}", f"v{index + 1}") for index in range(max(0, n - 1))]
        return DirectedGraphBuilder.from_named(nodes, named_edges, provenance)

    @staticmethod
    def ring(n: int, provenance: TheoremProvenance) -> FiniteDirectedGraph:
        if n < 2:
            return DirectedGraphBuilder.chain(n, provenance)
        nodes = [f"v{index}" for index in range(n)]
        named_edges = [(f"v{index}", f"v{index + 1}") for index in range(n - 1)]
        named_edges.append((f"v{n - 1}", "v0"))
        return DirectedGraphBuilder.from_named(nodes, named_edges, provenance)

    @staticmethod
    def cycle_graph(n: int, provenance: TheoremProvenance) -> FiniteDirectedGraph:
        if n < 2:
            return DirectedGraphBuilder.from_anonymous(max(n, 1), [], provenance)
        edges = [(i, i + 1) for i in range(n - 1)]
        edges.append((n - 1, 0))
        return DirectedGraphBuilder.from_anonymous(n, edges, provenance)


class FinitePosetGraph(FiniteDirectedGraph):
    """Deprecated alias shell.

    Use ``FiniteDirectedGraph``. This subclass exists only to provide an explicit
    compatibility symbol for older imports. It does not alter semantics.
    """

    def __init__(
        self,
        _nodes: tuple[str, ...],
        _node_index: dict[str, int],
        _edges: tuple[tuple[int, int], ...],
        _witness: DirectedGraphWitness,
        _provenance: TheoremProvenance,
    ) -> None:
        warnings.warn(
            "FinitePosetGraph is deprecated; use FiniteDirectedGraph. Poset semantics are not enforced at construction.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(_nodes, _node_index, _edges, _witness, _provenance)


DeprecatedFiniteDirectedGraph: TypeAlias = FiniteDirectedGraph


__all__ = [
    "DirectedGraphError",
    "NodeCountMismatch",
    "InvalidNodeIndex",
    "IndexOutOfRange",
    "SelfLoop",
    "DuplicateEdge",
    "ContainsCycles",
    "NamedEdgeResolutionError",
    "MissingNodeName",
    "DuplicateNode",
    "NamedSelfLoop",
    "NamedGraphError",
    "TheoremProvenance",
    "PosetWitness",
    "FiniteDirectedGraph",
    "DirectedGraphBuilder",
    "FinitePosetGraph",
    "DeprecatedFiniteDirectedGraph",
]




