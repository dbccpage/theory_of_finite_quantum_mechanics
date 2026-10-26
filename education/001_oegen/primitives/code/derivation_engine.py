"""Genesis Derivation Engine, Tree, Node, Edge, and Branch Primitives.

Selected educational models related to 19L57G1:
- code/derivation/engine.py
- code/derivation/bridge.py
- code/derivation/generator.py
- code/derivation/graph_genesis.py
- code/derivation/weight_profile.py
- lean4/Derivation/Rounds.lean

Classification: Autonomous tree exploration, branch quotienting, and evidence ledgers.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .canonical import validate_typed_fields
from .seed_and_regime import (
    AdmitDatum,
    Bounds,
    Delta,
    Event,
    Pair,
    Regime,
    Supply,
)

CanonKey = tuple[tuple[int, ...], ...]
Weights = dict[int, int]


# ---------------------------------------------------------------------------
# The Two Surviving Readings (L and F)
# ---------------------------------------------------------------------------

GENESIS_L: tuple[Event, ...] = (
    Supply("<>"),
    Supply("<a>"),
    Supply("<a>"),
    Supply("<ab>"),
    AdmitDatum("<a>"),
    AdmitDatum("<ab>"),
)

GENESIS_F: tuple[Event, ...] = (
    Supply("<>"),
    AdmitDatum("<>"),
    Supply("<a>"),
    Supply("<a>"),
    Supply("<ab>"),
    AdmitDatum("<a>"),
    AdmitDatum("<ab>"),
)


@dataclass(frozen=True)
class Reading:
    """A surviving reading of the genesis challenge text."""

    name: str
    description: str
    genesis: tuple[Event, ...]
    target: Pair

    def __post_init__(self) -> None:
        validate_typed_fields(self)


READING_L = Reading(
    "L",
    "strict admission: only explicit retention admits; initial inscription is presented but never retained",
    GENESIS_L,
    (0, 1),
)

READING_F = Reading(
    "F",
    "possession admission: initial inscription is admitted at genesis; supplied inscriptions admitted on retention",
    GENESIS_F,
    (1, 2),
)

READINGS: tuple[Reading, ...] = (READING_L, READING_F)


# ---------------------------------------------------------------------------
# Composed State Class (Bridge Invariants)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StateClass:
    """Coarse equivalence class of regimes over key structural features:
    carrier size, presence of binary forms, oriented witness,
    symmetric witness, irreflexivity facts, self loops.
    """

    carrier: int
    has_binary_form: bool
    oriented_witness: bool
    symmetric_witness: bool
    irreflexive_fact: bool
    self_edge: bool

    def __post_init__(self) -> None:
        validate_typed_fields(self)


# ---------------------------------------------------------------------------
# Branch Tree: Node and Edge
# ---------------------------------------------------------------------------


@dataclass
class Node:
    """A node in the derivation branch tree:
    node_id: unique index
    history: sequence of events from genesis
    regime: admitted state
    depth: tree depth
    canon: canonical isomorphism key
    status: open, expanded, closed, or refused
    merged_count: number of isomorphic regimes collapsed to this node
    certified: legacy field; True requires the separate source engine and is refused here
    """

    node_id: int
    history: tuple[Event, ...]
    regime: Regime
    depth: int
    canon: CanonKey
    status: str = "open"
    merged_count: int = 1
    certified: bool = False

    def __setattr__(self, name: str, value: object) -> None:
        if name == "certified" and value is not False:
            raise ValueError("REFUSED_UNVERIFIED_SOURCE_CERTIFICATE: use the source-engine adapter")
        object.__setattr__(self, name, value)


@dataclass
class Edge:
    """A directed edge in the derivation branch tree:
    parent: source node_id
    child: target node_id
    round_no: round index
    challenge: requirement or continuation challenge
    response_label: neutral string label
    response: accepted item delta
    tie_classes: number of tied minimum response classes
    class_size: number of deltas in chosen tie class
    cost: (item_count, arity_sum)
    orbits: automorphism orbit count
    kind: creation or modification
    """

    parent: int
    child: int
    round_no: int
    challenge: str
    response_label: str
    response: Delta
    tie_classes: int
    class_size: int
    cost: tuple[int, int]
    orbits: int = 1
    kind: str = "creation"
    merge_dmap: Optional[tuple[int, ...]] = None
    merge_fmap: Optional[tuple[int, ...]] = None


@dataclass
class Tree:
    """A derivation branch tree explored from genesis under declared bounds."""

    reading: str
    measure: str
    bounds: Bounds
    max_rounds: int
    pre_expansion_node_guard: int
    supply: bool
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)

    def stats(self) -> dict[str, object]:
        by_status: dict[str, int] = {}
        for n in self.nodes:
            by_status[n.status] = by_status.get(n.status, 0) + 1
        return {
            "reading": self.reading,
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "by_status": by_status,
            "max_depth": max((n.depth for n in self.nodes), default=0),
            "all_certified": False,
            "certification_status": "SOURCE_ENGINE_REPLAY_REQUIRED",
        }


# ---------------------------------------------------------------------------
# Proposal and Generator Records
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProposalRecord:
    """One represented extension proposal (GraphGenesis):
    block: target stage block name
    embed: embedding map
    retract: retraction down-map (d o u = id)
    new_pair: fresh pair
    parent_pos: parent index
    fresh_pos: fresh index
    cost: declared fuel cost
    """

    block: str
    embed: tuple[int, ...]
    retract: tuple[int, ...]
    new_pair: Pair
    parent_pos: int
    fresh_pos: int
    cost: int

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class RoundRecord:
    """Record of one round of the autonomous challenge generator."""

    round_no: int
    obstructions_before: int
    first_pair: Optional[Pair]
    repairs: int
    imports_this_round: int
    obstructions_after: int

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class BranchReport:
    """Report of an autonomous generator run across multiple rounds."""

    strategy: str
    rounds: tuple[RoundRecord, ...]

    def __post_init__(self) -> None:
        validate_typed_fields(self)
