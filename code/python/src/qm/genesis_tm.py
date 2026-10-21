"""Independent checker for the Genesis computation chain: semi-Thue rewriting, bounded reachability,
and the Turing-machine encoding of ``lean4/GenesisCompTM.lean``.

AuthorityEffect: None.

This module re-implements, with a different data representation, what
``code/rust/src/wdp/genesis_tm.rs`` and ``lean4/GenesisComputation.lean`` /
``lean4/GenesisCompTM.lean`` state:

* words are Python strings, one character per mark;
* a machine tape is a dictionary from integer cell positions to symbols (the Rust and Lean sides
  use the left/right list form of ``Turing.Tape``), so the encoding of a configuration into a word
  and the machine step are compared through a position-free canonical form;
* the bounded decider returns the same three verdicts as ``Verdict`` in the Rust module.

Fences. Exact finite computation on explicit instances. The bounded decider answers only inside a
declared word-length bound. No physical Church-Turing claim; the identity convention and the
unbounded supply of blanks are declared inputs of the chain, not derived here.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

LEND = "["
REND = "]"

Rule = Tuple[str, str]


# ---------------------------------------------------------------------------------------------
# Semi-Thue rewriting
# ---------------------------------------------------------------------------------------------


def successors(rules: Sequence[Rule], word: str) -> Set[str]:
    """All one-step rewrites of ``word``: a rule applied to a factor, inside its context."""
    out: Set[str] = set()
    for lhs, rhs in rules:
        start = 0
        while True:
            pos = word.find(lhs, start)
            if pos < 0:
                break
            out.add(word[:pos] + rhs + word[pos + len(lhs):])
            start = pos + 1
            if start > len(word):
                break
    return out


def is_irreducible(rules: Sequence[Rule], word: str) -> bool:
    return not successors(rules, word)


def bounded_reach(rules: Sequence[Rule], start: str, bound: int) -> Tuple[Set[str], Optional[Tuple[str, str]]]:
    """Words reachable with every word at most ``bound`` long, and a step leaving the bound."""
    if len(start) > bound:
        raise ValueError("start word is longer than the declared bound")
    seen = {start}
    frontier = [start]
    exceeded: Optional[Tuple[str, str]] = None
    while frontier:
        nxt: List[str] = []
        for w in sorted(frontier):
            for v in sorted(successors(rules, w)):
                if len(v) > bound:
                    if exceeded is None:
                        exceeded = (w, v)
                elif v not in seen:
                    seen.add(v)
                    nxt.append(v)
        frontier = nxt
    return seen, exceeded


def decide_reach(rules: Sequence[Rule], start: str, target: str, bound: int) -> Tuple[str, Optional[Tuple[str, str]]]:
    """Three-valued bounded decider: ``reachable``, ``unreachable`` or ``bound_exceeded``.

    ``unreachable`` is a complete answer (the bounded search is closed); ``bound_exceeded`` carries
    the witness step that leaves the bound.
    """
    seen, exceeded = bounded_reach(rules, start, bound)
    if target in seen:
        return "reachable", None
    if exceeded is None:
        return "unreachable", None
    return "bound_exceeded", exceeded


def config_space_size(k: int, bound: int) -> int:
    return sum(k ** i for i in range(bound + 1))


# ---------------------------------------------------------------------------------------------
# Turing machines in the TM0 form: one write or one move per transition
# ---------------------------------------------------------------------------------------------

# a transition value is ("W", b) or ("L",) or ("R",), with its next state
Transition = Tuple[int, Tuple]


@dataclass(frozen=True)
class Machine:
    n_states: int
    n_symbols: int  # symbol 0 is the blank
    delta: Dict[Tuple[int, int], Transition]


def state_mark(q: int) -> str:
    return chr(ord("A") + q)


def sym_mark(a: int) -> str:
    return str(a)


def machine_step(m: Machine, state: int, tape: Dict[int, int], head: int):
    """One step on the dictionary tape; ``None`` when the machine halts."""
    scanned = tape.get(head, 0)
    t = m.delta.get((state, scanned))
    if t is None:
        return None
    q2, act = t
    new_tape = dict(tape)
    new_head = head
    if act[0] == "W":
        new_tape[head] = act[1]
    elif act[0] == "R":
        new_head = head + 1
    else:
        new_head = head - 1
    return q2, {k: v for k, v in new_tape.items() if v != 0}, new_head


def canonical(state: int, tape: Dict[int, int], head: int):
    """Position-free form: state, scanned symbol, and non-blank cells by offset from the head."""
    return (state, tape.get(head, 0), tuple(sorted((p - head, s) for p, s in tape.items() if s != 0 and p != head)))


def encode(m: Machine, state: int, tape: Dict[int, int], head: int) -> str:
    """Configuration word ``[ cells-left q a cells-right ]`` over the window around the head."""
    cells = [p for p, s in tape.items() if s != 0]
    lo = min(cells + [head])
    hi = max(cells + [head])
    left = "".join(sym_mark(tape.get(p, 0)) for p in range(lo, head))
    right = "".join(sym_mark(tape.get(p, 0)) for p in range(head + 1, hi + 1))
    return LEND + left + state_mark(state) + sym_mark(tape.get(head, 0)) + right + REND


def decode(m: Machine, word: str):
    """Canonical form of a configuration word, or ``None`` if the word is not one."""
    if len(word) < 4 or word[0] != LEND or word[-1] != REND:
        return None
    inner = word[1:-1]
    states = {state_mark(q) for q in range(m.n_states)}
    syms = {sym_mark(a) for a in range(m.n_symbols)}
    idx = [i for i, ch in enumerate(inner) if ch in states]
    if len(idx) != 1 or idx[0] + 1 >= len(inner):
        return None
    i = idx[0]
    if any(ch not in syms for j, ch in enumerate(inner) if j != i):
        return None
    state = ord(inner[i]) - ord("A")
    head_sym = int(inner[i + 1])
    cells: Dict[int, int] = {}
    for j in range(i):
        s = int(inner[j])
        if s:
            cells[j - i] = s
    for j in range(i + 2, len(inner)):
        s = int(inner[j])
        if s:
            cells[j - i - 1] = s
    return (state, head_sym, tuple(sorted(cells.items())))


def rules_for(m: Machine) -> List[Rule]:
    """The rewriting rules of a machine: write, right and right-end, left and left-end."""
    rules: List[Rule] = []
    for (q, a), (q2, act) in sorted(m.delta.items()):
        Q, A, Q2 = state_mark(q), sym_mark(a), state_mark(q2)
        if act[0] == "W":
            rules.append((Q + A, Q2 + sym_mark(act[1])))
        elif act[0] == "R":
            for c in range(m.n_symbols):
                C = sym_mark(c)
                rules.append((Q + A + C, A + Q2 + C))
            rules.append((Q + A + REND, A + Q2 + sym_mark(0) + REND))
        else:
            for c in range(m.n_symbols):
                C = sym_mark(c)
                rules.append((C + Q + A, Q2 + C + A))
            rules.append((LEND + Q + A, LEND + Q2 + sym_mark(0) + A))
    return rules


def run_checked(m: Machine, tape_input: Sequence[int], max_steps: int):
    """Run the machine and the rewriting side by side, comparing every step.

    Returns ``(steps, canonical_final)`` or ``None`` if ``max_steps`` is exhausted. Raises
    ``AssertionError`` on any divergence: a missing or non-unique rewrite, a decoded word that
    differs from the machine step, or a halted configuration that still has a rewrite.
    """
    rules = rules_for(m)
    tape = {i: s for i, s in enumerate(tape_input) if s}
    state, head = 0, 0
    word = encode(m, state, tape, head)
    for step in range(max_steps + 1):
        nxt = machine_step(m, state, tape, head)
        succ = successors(rules, word)
        if nxt is None:
            assert not succ, "halted configuration has a rewrite"
            return step, canonical(state, tape, head)
        assert len(succ) == 1, f"{len(succ)} rewrites at step {step}"
        word = next(iter(succ))
        state, tape, head = nxt
        dec = decode(m, word)
        assert dec is not None
        assert dec == canonical(state, tape, head), f"decoded word differs at step {step}"
    return None


# ---------------------------------------------------------------------------------------------
# Example machines (TM0 form)
# ---------------------------------------------------------------------------------------------


def incrementer() -> Machine:
    """Binary incrementer, least significant bit first; blank reads as zero."""
    return Machine(
        3,
        2,
        {
            (0, 1): (1, ("W", 0)),
            (1, 0): (0, ("R",)),
            (1, 1): (0, ("R",)),
            (0, 0): (2, ("W", 1)),
        },
    )


def busy_beaver_2() -> Machine:
    """Two-state two-symbol champion with each transition split into a write and a move."""
    return Machine(
        7,
        2,
        {
            (0, 0): (3, ("W", 1)),
            (3, 0): (1, ("R",)),
            (3, 1): (1, ("R",)),
            (0, 1): (4, ("W", 1)),
            (4, 0): (1, ("L",)),
            (4, 1): (1, ("L",)),
            (1, 0): (5, ("W", 1)),
            (5, 0): (0, ("L",)),
            (5, 1): (0, ("L",)),
            (1, 1): (6, ("W", 1)),
            (6, 0): (2, ("R",)),
            (6, 1): (2, ("R",)),
        },
    )


def right_runner() -> Machine:
    """Moves right forever; every step needs one more fresh blank mark."""
    return Machine(1, 2, {(0, 0): (0, ("R",)), (0, 1): (0, ("R",))})


def all_two_state_machines() -> Iterable[Machine]:
    """Every machine with two states and two symbols in the TM0 form (9 choices per entry)."""
    choices: List[Optional[Transition]] = [None]
    for q2 in range(2):
        choices += [(q2, ("W", 0)), (q2, ("W", 1)), (q2, ("L",)), (q2, ("R",))]
    keys = [(q, a) for q in range(2) for a in range(2)]
    for combo in product(choices, repeat=4):
        delta = {k: t for k, t in zip(keys, combo) if t is not None}
        yield Machine(2, 2, delta)


# ---------------------------------------------------------------------------------------------
# Genesis events (custody mirror), contexts, binary coding
# ---------------------------------------------------------------------------------------------


def step_e(regime: dict, event: tuple) -> Optional[dict]:
    """The sealed Genesis step: ``None`` refuses the event."""
    r = {k: (list(v) if isinstance(v, list) else v) for k, v in regime.items()}
    kind = event[0]
    if kind == "supply":
        return r
    if kind == "admitDatum":
        r["data"] += 1
        return r
    if kind == "admitForm":
        if event[1] >= 1:
            r["forms"].append(event[1])
            return r
        return None
    if kind == "admitInst":
        f, args = event[1], list(event[2])
        if f < len(r["forms"]) and len(args) == r["forms"][f] and all(x < r["data"] for x in args):
            if (f, args) not in r["insts"]:
                r["insts"].append((f, args))
            return r
        return None
    if kind == "admitRuleAll":
        if event[1] < len(r["forms"]):
            if event[1] not in r["rules"]:
                r["rules"].append(event[1])
            return r
        return None
    if kind == "impose":
        i, j = event[1], event[2]
        if i < j < r["data"]:
            if (i, j) not in r["reqs"]:
                r["reqs"].append((i, j))
            return r
        return None
    raise ValueError(kind)


def replay(history: Sequence[tuple], base: Optional[dict] = None) -> Optional[dict]:
    r = base or {"data": 0, "forms": [], "insts": [], "rules": [], "reqs": []}
    for e in history:
        r = step_e(r, e)
        if r is None:
            return None
    return r


FIRST_SEPARATION = [
    ("admitDatum",),
    ("admitDatum",),
    ("admitForm", 1),
    ("admitInst", 0, [0]),
    ("impose", 0, 1),
]


def unary_sep(r: dict, i: int, j: int) -> bool:
    """Datum ``i`` is told apart from ``j`` by a unary form instance."""
    insts = [(f, tuple(a)) for f, a in r["insts"]]
    return any(
        r["forms"][f] == 1 and (((f, (i,)) in insts) != ((f, (j,)) in insts))
        for f in range(len(r["forms"]))
    )


def collapsed(r: dict, i: int, j: int) -> bool:
    return not unary_sep(r, i, j) and not unary_sep(r, j, i)


def pairwise_separated(r: dict) -> bool:
    return all(i == j or unary_sep(r, i, j) for i in range(r["data"]) for j in range(r["data"]))


def canonical_regime(n: int) -> dict:
    """n data, n-1 unary forms, and the instance (i, [i]) for i < n-1."""
    k = max(n - 1, 0)
    return {"data": n, "forms": [1] * k, "insts": [(i, [i]) for i in range(k)], "rules": [], "reqs": []}


def context_counts(n: int, a: int) -> Tuple[int, int]:
    """(contexts with at least one hole, contexts with exactly one hole) by direct enumeration."""
    slots = [None] + list(range(n))
    total = one = 0
    for ctx in product(slots, repeat=a):
        holes = sum(1 for x in ctx if x is None)
        if holes >= 1:
            total += 1
        if holes == 1:
            one += 1
    return total, one


def code_width(card: int) -> int:
    """Fixed code width: ceil(log2 card) + 1."""
    return max(card - 1, 0).bit_length() + 1


def encode_binary(card: int, word: Sequence[int]) -> str:
    k = code_width(card)
    return "".join(format(a, "b").zfill(k)[::-1] for a in word)


def decode_binary(card: int, bits: str) -> Optional[List[int]]:
    k = code_width(card)
    if len(bits) % k:
        return None
    out = []
    for i in range(0, len(bits), k):
        v = int(bits[i:i + k][::-1], 2)
        if v >= card:
            return None
        out.append(v)
    return out
