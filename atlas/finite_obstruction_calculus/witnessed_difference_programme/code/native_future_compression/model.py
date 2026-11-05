"""Literal finite model, implemented without a native semantic dependency."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from functools import cache
from itertools import combinations, permutations

PROFILE = {"max_terms": 3, "max_count": 4, "horizon": 2}
PROFILES = ("terminal_present_only", "terminal_status_probes")
TASK = "literal-native-future-retention-2026-10-06-v1"
NATIVE_SCHEMA = "bounded-native-future/1"


class Refusal(ValueError):
    """A submitted claim does not match its declared inputs."""


def require(condition, message):
    if not condition:
        raise Refusal(message)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def same(actual, expected, message):
    # JSON byte equality also distinguishes true from 1 and 1.0 from 1.
    require(encoded(actual) == encoded(expected), message)


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def fields(value, names, where):
    require(type(value) is dict and set(value) == set(names), f"{where}: fields")


def natural(value, limit, where):
    require(type(value) is int and 0 <= value < limit, f"{where}: integer range")
    return value


def way_round(t):
    k = t.index(min(t))
    return tuple(t[k:] + t[:k])


@cache
def faces(n):
    return tuple(sorted(t for x, y, z in combinations(range(n), 3)
                        for t in ((x, y, z), (x, z, y))))


@dataclass(frozen=True, order=True, slots=True)
class State:
    n: int
    r: tuple[int, ...]
    s: tuple[int, ...]
    filled: tuple[tuple[int, int, int], ...] = ()

    def wire(self):
        return {"n": self.n, "r": list(self.r), "s": list(self.s),
                "filled": [list(t) for t in self.filled]}


def state_of(value, bounded=True):
    fields(value, ("n", "r", "s", "filled"), "raw state")
    n = natural(value["n"], 4 if bounded else 5, "terms")
    for key in ("r", "s"):
        require(type(value[key]) is list and len(value[key]) == n*n, "count shape")
        require(all(type(c) is int and c >= 0 for c in value[key]), "count integer")
    require(type(value["filled"]) is list, "filled shape")
    require(all(type(t) is list and len(t) == 3 and
                all(type(x) is int for x in t) for t in value["filled"]), "face shape")
    filled = tuple(tuple(t) for t in value["filled"])
    require(filled == tuple(sorted(set(filled))) and set(filled) <= set(faces(n)),
            "face keys")
    state = State(n, tuple(value["r"]), tuple(value["s"]), filled)
    require(not bounded or sum(state.r) + sum(state.s) <= 4, "count bound")
    return state


def actions():
    out = [{"kind": "identify", "x": x, "y": y} for x, y in combinations(range(3), 2)]
    for kind in ("remove", "add_assertion"):
        if kind == "add_assertion":
            out += [{"kind": "fill", "x": x, "y": y, "z": z} for x, y, z in faces(3)]
            out.append({"kind": "add_term"})
        out += [{"kind": kind, "relation": rel, "x": x, "y": y}
                for rel in ("r", "s") for x in range(3) for y in range(3)]
    return out


ACTIONS = actions()


def counts(width, allowance=4):
    if width == 0:
        yield ()
    else:
        for first in range(allowance + 1):
            for rest in counts(width - 1, allowance - first):
                yield (first,) + rest


def enumerate_states():
    out = []
    for n in range(4):
        fs = faces(n)
        subsets = sorted(tuple(fs[i] for i in range(len(fs)) if mask & (1 << i))
                         for mask in range(1 << len(fs)))
        for cs in counts(2*n*n):
            out.extend(State(n, cs[:n*n], cs[n*n:], subset) for subset in subsets)
    require(out == sorted(set(out)), "raw enumeration order or duplication")
    require(Counter(s.n for s in out) == {0: 1, 1: 15, 2: 495, 3: 29260},
            "raw enumeration totals")
    return out


@cache
def rewritings(n):
    return tuple(permutations(range(n)))


def mark(state):
    n = state.n
    candidates = []
    excess = tuple(a-b for a, b in zip(state.r, state.s))
    for p in rewritings(n):
        moved = [0] * (n*n)
        for i in range(n):
            for j in range(n):
                moved[p[i]*n+p[j]] = excess[i*n+j]
        potential = [0] + [moved[i*n] for i in range(1, n)] if n else []
        normal = tuple(moved[i*n+j] - potential[i] + potential[j]
                       for i in range(n) for j in range(n))
        filled = tuple(sorted(way_round(tuple(p[x] for x in t)) for t in state.filled))
        candidates.append((normal, filled))
    normal, filled = min(candidates)
    return n, normal, filled


def mark_wire(value):
    n, normal, filled = value
    return {"n": n, "normal": [str(x) for x in normal],
            "filled": [list(t) for t in filled]}


def balance(state):
    n = state.n
    return tuple((t, sum(state.r[x*n+y]-state.s[x*n+y]
                         for x, y in zip(t, t[1:]+t[:1])) == 0)
                 for t in state.filled)


def balance_wire(value):
    return [{"face": list(t), "balanced": answer} for t, answer in value]


def transition(state, action):
    """Return native price and raw post-state, or None for a disabled label."""
    n, r, s, filled = state.n, state.r, state.s, state.filled
    kind = action["kind"]
    if kind == "add_term":
        def embed(table):
            return tuple(table[x*n+y] if x < n and y < n else 0
                         for x in range(n+1) for y in range(n+1))
        return (1, 0), State(n+1, embed(r), embed(s), filled)
    x, y = action["x"], action["y"]
    if not (x < n and y < n):
        return None
    if kind == "identify":
        if not x < y:
            return None
        image = [x if i == y else i - (i > y) for i in range(n)]
        def push(table):
            out = [0] * ((n-1)*(n-1))
            for i in range(n):
                for j in range(n):
                    out[image[i]*(n-1)+image[j]] += table[i*n+j]
            return tuple(out)
        carried = {way_round(tuple(image[i] for i in t)) for t in filled
                   if len({image[i] for i in t}) == 3}
        return (0, 0), State(n-1, push(r), push(s), tuple(sorted(carried)))
    if kind == "fill":
        z = action["z"]
        t = (x, y, z)
        if not (x < y and x < z < n and y != z) or t in filled:
            return None
        return (0, 0), State(n, r, s, tuple(sorted((*filled, t))))
    table = list(r if action["relation"] == "r" else s)
    if kind == "remove" and table[x*n+y] == 0:
        return None
    table[x*n+y] += -1 if kind == "remove" else 1
    new_r, new_s = (tuple(table), s) if action["relation"] == "r" else (r, tuple(table))
    return ((0, 0) if kind == "remove" else (0, 1)), State(n, new_r, new_s, filled)


@dataclass(frozen=True, slots=True)
class Edge:
    status: str
    price: tuple[int, int] | None
    child: int | None
    occurrences: int

    def wire(self):
        return {"status": self.status, "price": list(self.price) if self.price else None,
                "child": self.child, "occurrences": self.occurrences}


class Model:
    def __init__(self):
        self.states = enumerate_states()
        self.index = {s: i for i, s in enumerate(self.states)}
        self.marks = [mark(s) for s in self.states]
        self.balances = [balance(s) for s in self.states]
        self.present = list(zip(self.marks, self.balances))
        self.edges = []
        for state in self.states:
            row = []
            for action in ACTIONS:
                result = transition(state, action)
                if result is None:
                    edge = Edge("native_disabled", None, None, 0)
                else:
                    price, child = result
                    if child.n > 3 or sum(child.r) + sum(child.s) > 4:
                        edge = Edge("bound_excluded", price, None, 0)
                    else:
                        edge = Edge("admitted", price, self.index[child], 1)
                row.append(edge)
            self.edges.append(tuple(row))

    def state_wire(self, i):
        return {**self.states[i].wire(), "mark": mark_wire(self.marks[i]),
                "balance": balance_wire(self.balances[i])}

    def signature(self, i, profile, previous=None):
        present = self.present[i]
        if previous is None:
            if profile == "terminal_present_only":
                return present
            return present, tuple((e.status, e.price) for e in self.edges[i])
        return present, tuple((e.status, e.price, None if e.child is None else previous[e.child],
                               e.occurrences) for e in self.edges[i])

    def partition(self):
        result = {}
        for profile in PROFILES:
            layers = []
            for layer in range(3):
                classes = {}
                labels = []
                for i in range(len(self.states)):
                    key = self.signature(i, profile, layers[-1] if layer else None)
                    labels.append(classes.setdefault(key, len(classes)))
                layers.append(labels)
            result[profile] = layers
        return result


def clipped_report(state):
    return {"mark": mark_wire(mark(state)), "filled": [list(t) for t in state.filled],
            "clip_r": [min(c, 2) for c in state.r], "clip_s": [min(c, 2) for c in state.s]}


def decode(report):
    fields(report, ("mark", "filled", "clip_r", "clip_s"), "clipped report")
    m = report["mark"]
    fields(m, ("n", "normal", "filled"), "mark")
    n = natural(m["n"], 4, "mark terms")
    require(type(m["normal"]) is list and len(m["normal"]) == n*n, "normal shape")
    try:
        require(all(type(x) is str and str(int(x)) == x for x in m["normal"]),
                "canonical normal integer")
        sigma = sum(int(x) for x in m["normal"])
    except (ValueError, TypeError) as exc:
        raise Refusal("canonical normal integer") from exc
    for key in ("clip_r", "clip_s"):
        require(type(report[key]) is list and len(report[key]) == n*n and
                all(type(c) is int and 0 <= c <= 2 for c in report[key]), "clipped count")
    cs = report["clip_r"] + report["clip_s"]
    signs = [1]*(n*n) + [-1]*(n*n)
    twos = [i for i, c in enumerate(cs) if c == 2]
    require(sum(cs) <= 4, "clipped allowance")
    if len(twos) == 1:
        j = twos[0]
        cs[j] = signs[j]*(sigma - sum(e*c for i, (e, c) in enumerate(zip(signs, cs)) if i != j))
        require(cs[j] >= 2, "clipped reconstruction")
    result = state_of({"n": n, "r": cs[:n*n], "s": cs[n*n:], "filled": report["filled"]})
    same(clipped_report(result), report, "decoded report mismatch")
    return result
