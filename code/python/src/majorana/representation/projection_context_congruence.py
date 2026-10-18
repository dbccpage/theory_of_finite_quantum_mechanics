"""Projection-Context Congruence & Partition Refinement Engine.

PO-OE-CORE-001 implementation:
Computes the behavioral quotient partition Core_C(ker o) under action generators,
generating returning projection witnesses with separating context words.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class ReturningProjectionWitness:
    """Witness exhibiting an action word that separates two previously unseparated states."""

    state_x: str
    state_y: str
    context_word: Tuple[str, ...]
    obs_x_after: str
    obs_y_after: str

    def __post_init__(self) -> None:
        if self.obs_x_after == self.obs_y_after:
            raise ValueError(
                f"witness {self.state_x}/{self.state_y} records identical "
                f"observations {self.obs_x_after}"
            )


@dataclass
class ProjectionContextCongruenceResult:
    """Result of computing Core_C(ker o) partition refinement."""

    initial_blocks: List[List[str]]
    final_blocks: List[List[str]]
    splits_count: int
    witnesses: List[ReturningProjectionWitness]
    is_invariant: bool
    receipt_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "initial_blocks": self.initial_blocks,
            "final_blocks": self.final_blocks,
            "splits_count": self.splits_count,
            "witnesses": [
                {
                    "state_x": w.state_x,
                    "state_y": w.state_y,
                    "context_word": list(w.context_word),
                    "obs_x_after": w.obs_x_after,
                    "obs_y_after": w.obs_y_after,
                }
                for w in self.witnesses
            ],
            "is_invariant": self.is_invariant,
            "receipt_hash": self.receipt_hash,
            "authority_effect": "None",
        }


class ProjectionContextCongruenceEngine:
    """Computes relational partition refinement over a state space and action generators."""

    def __init__(
        self,
        states: Sequence[Any],
        generators: Dict[str, Callable[[Any], Any]],
        observation_fn: Callable[[Any], Any],
        state_id_fn: Optional[Callable[[Any], str]] = None,
    ) -> None:
        self.state_id_fn = state_id_fn or (lambda s: str(s))
        self.generators = generators
        self.observation_fn = observation_fn

        # Verify no state ID collisions
        self.raw_states = list(states)
        self.state_ids: List[str] = []
        self.id_to_state: Dict[str, Any] = {}
        for s in self.raw_states:
            sid = self.state_id_fn(s)
            if sid in self.id_to_state:
                raise ValueError(f"collision: state ID '{sid}' already present")
            self.state_ids.append(sid)
            self.id_to_state[sid] = s

        # Verify generator domain closure
        for gname, gen in self.generators.items():
            for s in self.raw_states:
                succ = gen(s)
                succ_id = self.state_id_fn(succ)
                if succ_id not in self.id_to_state:
                    raise ValueError(
                        f"generator '{gname}' produces successor outside state space: {succ}"
                    )

    def _apply_word(self, sid: str, word: Tuple[str, ...]) -> str:
        curr = self.id_to_state[sid]
        for sym in word:
            curr = self.generators[sym](curr)
        return self.state_id_fn(curr)

    def compute_core_c(self) -> ProjectionContextCongruenceResult:
        # Step 1: Initial observation partition
        obs_groups: Dict[Any, List[str]] = {}
        for sid in self.state_ids:
            val = self.observation_fn(self.id_to_state[sid])
            # Normalize unhashable observation if necessary
            key = val if isinstance(val, (int, str, float, bool, tuple)) else str(val)
            obs_groups.setdefault(key, []).append(sid)

        initial_blocks = [sorted(block) for block in obs_groups.values()]
        # Sort blocks canonically by their first element
        initial_blocks.sort(key=lambda b: b[0] if b else "")

        # Current partition: list of sets of state IDs
        current_blocks: List[List[str]] = [list(b) for b in initial_blocks]
        splits_count = 0

        # Step 2: Partition refinement loop (Moore / Hopcroft)
        changed = True
        while changed:
            changed = False
            new_blocks: List[List[str]] = []
            for block in current_blocks:
                if len(block) <= 1:
                    new_blocks.append(block)
                    continue

                # Check if this block can be split by any generator
                block_split = False
                for gname in sorted(self.generators.keys()):
                    gen = self.generators[gname]
                    # Map each state in block to the index of the block containing its successor
                    subgroups: Dict[int, List[str]] = {}
                    for sid in block:
                        succ = gen(self.id_to_state[sid])
                        succ_id = self.state_id_fn(succ)
                        # Find block index of succ_id
                        b_idx = -1
                        for idx, b in enumerate(current_blocks):
                            if succ_id in b:
                                b_idx = idx
                                break
                        subgroups.setdefault(b_idx, []).append(sid)

                    if len(subgroups) > 1:
                        # Block is split!
                        for sub in subgroups.values():
                            new_blocks.append(sub)
                        splits_count += 1
                        block_split = True
                        changed = True
                        break

                if not block_split:
                    new_blocks.append(block)

            current_blocks = new_blocks

        # Canonical sort of final blocks
        final_blocks = [sorted(b) for b in current_blocks]
        final_blocks.sort(key=lambda b: b[0] if b else "")

        # Map initial and final block indices
        initial_of = {
            sid: idx for idx, block in enumerate(initial_blocks) for sid in block
        }
        final_of = {
            sid: idx for idx, block in enumerate(final_blocks) for sid in block
        }

        # Step 3: Find separating witness context words for returning pairs
        # Returning pairs: x, y where initial_of[x] == initial_of[y] but final_of[x] != final_of[y]
        witnesses: List[ReturningProjectionWitness] = []
        gen_keys = sorted(self.generators.keys())

        # For every pair separated by refinement
        seen_pairs = set()
        for i, sid_x in enumerate(self.state_ids):
            for sid_y in self.state_ids[i + 1 :]:
                if initial_of[sid_x] == initial_of[sid_y] and final_of[sid_x] != final_of[sid_y]:
                    pair_key = (min(sid_x, sid_y), max(sid_x, sid_y))
                    if pair_key in seen_pairs:
                        continue
                    seen_pairs.add(pair_key)

                    # BFS to find the shortest separating word
                    queue: deque[Tuple[str, ...]] = deque([()])
                    found_word: Optional[Tuple[str, ...]] = None
                    obs_x_str = ""
                    obs_y_str = ""

                    while queue:
                        w = queue.popleft()
                        if len(w) > 0:
                            end_x_id = self._apply_word(sid_x, w)
                            end_y_id = self._apply_word(sid_y, w)
                            ox = self.observation_fn(self.id_to_state[end_x_id])
                            oy = self.observation_fn(self.id_to_state[end_y_id])
                            if ox != oy:
                                found_word = w
                                obs_x_str = str(ox)
                                obs_y_str = str(oy)
                                break
                        # Limit depth to prevent runaway on huge state spaces
                        if len(w) < len(self.state_ids):
                            for gk in gen_keys:
                                queue.append(w + (gk,))

                    if found_word is not None:
                        witnesses.append(
                            ReturningProjectionWitness(
                                state_x=sid_x,
                                state_y=sid_y,
                                context_word=found_word,
                                obs_x_after=obs_x_str,
                                obs_y_after=obs_y_str,
                            )
                        )

        is_invariant = (splits_count == 0)

        # Step 4: Canonical receipt hash (permutation invariant)
        canonical_quotient = [sorted(b) for b in final_blocks]
        canonical_quotient.sort(key=lambda b: b[0] if b else "")
        digest_bytes = json.dumps(canonical_quotient, sort_keys=True).encode("utf-8")
        receipt_hash = sha256(digest_bytes).hexdigest()

        return ProjectionContextCongruenceResult(
            initial_blocks=initial_blocks,
            final_blocks=final_blocks,
            splits_count=splits_count,
            witnesses=witnesses,
            is_invariant=is_invariant,
            receipt_hash=receipt_hash,
        )


__all__ = [
    "ProjectionContextCongruenceEngine",
    "ProjectionContextCongruenceResult",
    "ReturningProjectionWitness",
]
