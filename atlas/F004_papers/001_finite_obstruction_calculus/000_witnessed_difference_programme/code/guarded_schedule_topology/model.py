"""Full legal permutohedral cells of a finite paired count-guard family.

Event 2*i removes one count and event 2*i+1 restores it. The remove must
precede its own restore. An ordered block represents every ordering inside
that block, not an arbitrarily selected representative. All arithmetic is
integral. The experiment admits at most four pairs; the written theorem is
not restricted to that computational bound.
"""

from __future__ import annotations

from collections.abc import Iterator
from itertools import permutations, product

Cell = tuple[tuple[int, ...], ...]
Levels = tuple[tuple[Cell, ...], ...]
MAX_PAIRS = 4


class TopologyRefusal(ValueError):
    """The proposed finite object or certificate was not admitted."""


def parameters(n: int, capacity: int) -> None:
    if type(n) is not int or not 1 <= n <= MAX_PAIRS:
        raise TopologyRefusal(f"pair count must be an integer in 1..{MAX_PAIRS}")
    if type(capacity) is not int or not 0 <= capacity <= n:
        raise TopologyRefusal("capacity must be an integer between zero and pair count")


def subsets(values: tuple[int, ...]) -> Iterator[tuple[int, ...]]:
    for mask in range(1 << len(values)):
        yield tuple(x for i, x in enumerate(values) if mask & (1 << i))


def admit_cell(cell: object, n: int) -> Cell:
    if type(n) is not int or not 1 <= n <= MAX_PAIRS:
        raise TopologyRefusal("invalid pair count")
    if type(cell) is not tuple or not cell:
        raise TopologyRefusal("a cell must be a nonempty tuple of blocks")
    flat: list[int] = []
    for block in cell:
        if type(block) is not tuple or not block or any(type(e) is not int for e in block):
            raise TopologyRefusal("blocks must be nonempty integer tuples")
        if tuple(sorted(set(block))) != block:
            raise TopologyRefusal("each block must be sorted and duplicate-free")
        flat.extend(block)
    if sorted(flat) != list(range(2 * n)):
        raise TopologyRefusal("blocks must partition exactly the declared endpoints")
    return cell


def dimension(cell: Cell) -> int:
    return sum(len(block) - 1 for block in cell)


def block_coarsenings(word: tuple[int, ...]) -> Iterator[Cell]:
    """Every ordered cut of one nonempty word, each block written sorted."""
    width = len(word)
    for mask in range(1 << (width - 1)):
        blocks: list[tuple[int, ...]] = []
        start = 0
        for index in range(width - 1):
            if mask & (1 << index):
                blocks.append(tuple(sorted(word[start:index + 1])))
                start = index + 1
        blocks.append(tuple(sorted(word[start:])))
        yield tuple(blocks)


def count_trace(word: tuple[int, ...], capacity: int) -> list[int] | None:
    """Counts after each event, or None if the guard or the final count fails.

    An odd event restores one count only after its own remove. An even event
    removes one count and refuses an empty counter. The trace starts at the
    supplied capacity and must end there.
    """
    count = capacity
    seen: set[int] = set()
    trace = [count]
    for event in word:
        if event % 2:
            if event - 1 not in seen:
                return None
            count += 1
        else:
            if count == 0:
                return None
            count -= 1
        seen.add(event)
        trace.append(count)
    if count != capacity:
        return None
    return trace


def _packed(levels: list) -> Levels:
    while levels and not levels[-1]:
        levels.pop()
    return tuple(tuple(sorted(cells)) for cells in levels)


def block_legal(cell: Cell, n: int, capacity: int) -> bool:
    """Exact worst-refinement criterion, including strict pair precedence."""
    parameters(n, capacity)
    admit_cell(cell, n)
    states = [0] * n  # 0 unstarted, 1 active, 2 finished
    for block in cell:
        starts = [e // 2 for e in block if e % 2 == 0]
        finishes = [e // 2 for e in block if e % 2 == 1]
        if any(states[i] != 0 for i in starts) or any(states[i] != 1 for i in finishes):
            return False
        if states.count(1) + len(starts) > capacity:
            return False
        for i in starts:
            states[i] = 1
        for i in finishes:
            states[i] = 2
    return states == [2] * n


def enumerate_cells(n: int, capacity: int) -> Levels:
    """Enumerate all safe blocks by unstarted/active/finished state recursion."""
    parameters(n, capacity)
    levels: list[list[Cell]] = [[] for _ in range(2 * n)]

    def visit(states: tuple[int, ...], blocks: Cell) -> None:
        if all(s == 2 for s in states):
            levels[dimension(blocks)].append(blocks)
            return
        unstarted = tuple(i for i, s in enumerate(states) if s == 0)
        active = tuple(i for i, s in enumerate(states) if s == 1)
        for starts in subsets(unstarted):
            if len(active) + len(starts) > capacity:
                continue
            for finishes in subsets(active):
                if not starts and not finishes:
                    continue
                updated = list(states)
                for i in starts:
                    updated[i] = 1
                for i in finishes:
                    updated[i] = 2
                block = tuple(sorted((*[2 * i for i in starts],
                                      *[2 * i + 1 for i in finishes])))
                visit(tuple(updated), (*blocks, block))

    visit((0,) * n, ())
    return _packed(levels)


def direct_word_legal(word: object, n: int, capacity: int) -> bool:
    """Independent direct positive-count replay; no block-capacity formula."""
    parameters(n, capacity)
    if (type(word) is not tuple or any(type(e) is not int for e in word)
            or sorted(word) != list(range(2 * n))):
        raise TopologyRefusal("a schedule must permute every endpoint exactly once")
    return count_trace(word, capacity) is not None


def vertex_refinements(cell: Cell) -> Iterator[tuple[int, ...]]:
    for pieces in product(*(permutations(block) for block in cell)):
        yield tuple(e for piece in pieces for e in piece)


def direct_cell_baseline(n: int, capacity: int) -> Levels:
    """All word coarsenings admitted only if every refining word replays.

    A fully legal face has a legal vertex, so coarsenings of all legal words
    form a complete independent candidate pool. This is intentionally not
    the efficient block recursion used by ``enumerate_cells``.
    """
    parameters(n, capacity)
    legal = {word for word in permutations(range(2 * n))
             if direct_word_legal(word, n, capacity)}
    candidates: set[Cell] = set()
    for word in legal:
        candidates.update(block_coarsenings(word))
    levels: list[list[Cell]] = [[] for _ in range(2 * n)]
    for cell in candidates:
        if all(word in legal for word in vertex_refinements(cell)):
            levels[dimension(cell)].append(cell)
    return _packed(levels)


def task_cells(n: int, capacity: int) -> Levels:
    """Task permutohedron subcomplex: every tied task block has size <= c.

    These are cells on n task labels, rather than the 2*n native endpoints.
    A homotopy equivalence in the paper does not make this an execution-state
    quotient. The small enumeration uses all task words and all block cuts.
    """
    parameters(n, capacity)
    levels: list[set[Cell]] = [set() for _ in range(n)]
    for word in permutations(range(n)):
        for cell in block_coarsenings(word):
            if all(len(block) <= capacity for block in cell):
                levels[dimension(cell)].add(cell)
    return _packed(levels)


def boundary(cell: Cell) -> dict[Cell, int]:
    """Oriented cellular boundary from splitting exactly one ordered block.

    A sorted block b_1<...<b_m has tangent basis
    (e_{b_1}-e_{b_m},...,e_{b_{m-1}}-e_{b_m}). Blocks are oriented in
    their written order. The sign is checked against an independent outward
    normal determinant in the adversarial audit and test suite.
    """
    result: dict[Cell, int] = {}
    prefix_dimension = 0
    for position, block in enumerate(cell):
        for left in subsets(block):
            if not left or len(left) == len(block):
                continue
            right = tuple(e for e in block if e not in left)
            inversions = sum(x > y for x in left for y in right)
            sign = -1 if (prefix_dimension + len(left) + inversions) % 2 else 1
            face = (*cell[:position], left, right, *cell[position + 1:])
            result[face] = sign
        prefix_dimension += len(block) - 1
    return result
