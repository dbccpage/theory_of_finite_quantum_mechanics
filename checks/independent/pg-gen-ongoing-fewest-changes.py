"""Independent complete finite-game source/array and shortest-path audit."""
from __future__ import annotations
from collections import deque
from itertools import product
import json
from typing import TypeAlias
import sympy as sp  # type: ignore[import-untyped]

Pair: TypeAlias = tuple[int,int]
State: TypeAlias = tuple[frozenset[int],frozenset[Pair],int,int]
Wire: TypeAlias = tuple[tuple[int,...],tuple[Pair,...],int,int]
Move: TypeAlias = tuple[str,int,int]

def require(ok: bool,msg: str) -> None:
    if not ok:raise RuntimeError(msg)

def decode(w: Wire) -> State:
    return frozenset(w[0]),frozenset(w[1]),w[2],w[3]

def legal(s: State) -> bool:
    return all(x != y for x,y in s[1])

def wf(s: State) -> bool:
    return all(x in s[0] and y in s[0] for x,y in s[1]) and s[2] in s[0] and s[3] in s[0]

def source(s: State,e: Move) -> State | None:
    t,a,x,y=s;kind,u,v=e
    if kind=='term':
        return (t|{u},a,x,y) if u not in t else None
    if kind=='assert':
        return (t,a|{(u,v)},x,y) if u in t and v in t and u != v and (u,v) not in a else None
    if kind=='remove':
        return (t,a-{(u,v)},x,y) if (u,v) in a else None
    if kind != 'merge':raise ValueError('unknown move kind')
    if not (u in t and v in t and u != v and (u,v) not in a and (v,u) not in a):return None
    def q(z: int) -> int:return u if z==v else z
    return t-{v},frozenset((q(i),q(j)) for i,j in a),q(x),q(y)

def array(w: Wire,e: Move) -> Wire | None:
    terms=list(w[0]);edges=list(w[1]);a,b=w[2:];kind,u,v=e
    if kind=='term':
        if u in terms:return None
        terms.append(u)
    elif kind=='assert':
        if u not in terms or v not in terms or u==v or (u,v) in edges:return None
        edges.append((u,v))
    elif kind=='remove':
        if (u,v) not in edges:return None
        edges=[p for p in edges if p != (u,v)]
    else:
        if kind != 'merge':raise ValueError('unknown move kind')
        if u not in terms or v not in terms or u==v or (u,v) in edges or (v,u) in edges:return None
        terms=[x for x in terms if x != v]
        edges=[(u if x==v else x,u if y==v else y) for x,y in edges]
        a=u if a==v else a;b=u if b==v else b
    return tuple(terms),tuple(edges),a,b

def cost(s: State,both: bool) -> int:
    lost=(3 if both else 2) if s[2]==s[3] else int((s[2],s[3]) not in s[1])+int(both and (s[3],s[2]) not in s[1])
    return len(s[0])+len(s[1])+2*lost

def enumerate_states(labels: tuple[int, ...]) -> list[State]:
    states: list[State] = []
    for bits in range(1, 1 << len(labels)):
        terms = frozenset(x for x in labels if bits & (1 << x))
        atoms = tuple((i, j) for i, j in product(sorted(terms), repeat=2) if i != j)
        for eb in range(1 << len(atoms)):
            edges = frozenset(e for k, e in enumerate(atoms) if eb & (1 << k))
            states.extend((terms, edges, a, b) for a, b in product(sorted(terms), repeat=2))
    expected = sum(sp.binomial(3, k) * sp.Integer(2)**(k*(k-1)) * k*k for k in range(1, 4))
    require(len(states) == expected, 'state census')
    return states


def moves_for(labels: tuple[int, ...]) -> tuple[Move, ...]:
    return tuple([('term', x, 0) for x in labels] +
                 [(kind, x, y) for kind in ('assert', 'remove', 'merge')
                  for x, y in product(labels, repeat=2)])


def check_transitions(states: list[State], moves: tuple[Move, ...]) -> tuple[dict[State, list[State]], int, int]:
    adjacency: dict[State, list[State]] = {s: [] for s in states}
    performed = refused = 0
    for s in states:
        w = (tuple(sorted(s[0]))*2, tuple(sorted(s[1]))*2, s[2], s[3])
        require(decode(w) == s, 'duplicate-tolerant wire representation')
        for e in moves:
            t = source(s, e)
            v = array(w, e)
            require(t == (decode(v) if v is not None else None), 'all guarded source/array transition squares')
            if t is None:
                refused += 1
                continue
            performed += 1
            require(legal(t) and wf(t), 'source Legal/WF preservation')
            require(all(cost(t, both) <= cost(s, both)+1 for both in (False, True)), 'potential transport')
            adjacency[s].append(t)
    return adjacency, performed, refused


def check_shortest_paths(states: list[State], labels: tuple[int, ...],
                         adjacency: dict[State, list[State]]) -> list[dict[str, int | bool]]:
    distances: list[dict[str, int | bool]] = []
    for both in (False, True):
        seeds = [(frozenset({a, b}), frozenset({(a, b), (b, a)} if both else {(a, b)}), a, b)
                 for a, b in product(labels, repeat=2) if a != b]
        dist = {s: 0 for s in seeds}
        todo = deque(seeds)
        while todo:
            s = todo.popleft()
            for t in adjacency[s]:
                if t not in dist:
                    dist[t] = dist[s]+1
                    todo.append(t)
        require(set(dist) == set(states), 'all writings, apart and merged targets')
        offset = 4 if both else 3
        require(all(dist[s]+offset == cost(s, both) for s in states), 'matching lower and upper bounds')
        distances.append({'both_givens': both, 'targets': len(dist),
                          'maximum_distance': max(dist.values()), 'distance_sum': sum(dist.values())})
    return distances


def check_rewriting(states: list[State], moves: tuple[Move, ...]) -> int:
    rewrite = {0: 5, 1: 11, 2: 17}
    def renamed(s: State) -> State:
        return (frozenset(rewrite[x] for x in s[0]),
                frozenset((rewrite[x], rewrite[y]) for x, y in s[1]), rewrite[s[2]], rewrite[s[3]])
    checked = 0
    for s in states:
        for e in moves:
            t = source(s, e)
            ep = (e[0], rewrite[e[1]], rewrite[e[2]])
            tt = source(renamed(s), ep)
            require(tt == (renamed(t) if t is not None else None), 'renamed guarded transition')
            checked += 1
    return checked


def check_builds(states: list[State]) -> int:
    one_step_moves = moves_for(tuple(range(4)))
    checked = 0
    for s in states:
        for x in s[0]:
            t = source(s, ('term', 3, 0))
            if t is None:
                raise RuntimeError('fresh build term')
            g = source(t, ('assert', x, 3))
            if g is None:
                raise RuntimeError('legal build assertion')
            image = frozenset((x if a == 3 else a, x if b == 3 else b) for a, b in g[1])
            require((x, x) in image and legal(g), 'diagnostic quotient has loop; performed build is legal')
            require(source(g, ('merge', x, 3)) is None, 'obstructed image is not a performed identification')
            require(g != s and not any(source(s, e) == g for e in one_step_moves), 'no shorter build to this target')
            checked += 1
    return checked


def check_negative_controls(states: list[State]) -> None:
    # Fixed regressions; these do not execute four mutated source programs.
    require(any(s[2] == s[3] for s in states), 'merged-name coverage')
    s: State = (frozenset({0, 1}), frozenset(), 1, 1)
    t = source(s, ('merge', 0, 1))
    require(t is not None and t[2:] == (0, 0), 'tracked-name update')
    s = (frozenset({0, 1}), frozenset({(0, 1)}), 0, 1)
    require(source(s, ('merge', 0, 1)) is None, 'identification guard')
    s = (frozenset({0, 1, 2}), frozenset({(0, 2), (1, 2)}), 0, 1)
    t = source(s, ('merge', 0, 1))
    require(t is not None and len(t[1]) == 1, 'deduplicated image')


def main() -> None:
    labels = tuple(range(3))
    states = enumerate_states(labels)
    moves = moves_for(labels)
    adjacency, performed, refused = check_transitions(states, moves)
    distances = check_shortest_paths(states, labels, adjacency)
    renamed_steps = check_rewriting(states, moves)
    build_cases = check_builds(states)
    check_negative_controls(states)
    print(json.dumps(dict(node='PG-GEN-ONGOING-FEWEST-CHANGES', authority_effect='None', labels=list(labels),
        states=len(states), attempts=performed+refused, performed=performed, refused=refused,
        duplicate_wire_controls=len(states), all_writing_shortest_paths=distances,
        nonconsecutive_renaming_squares=renamed_steps, build_cases=build_cases,
        negative_controls_checked=4, mutation_coverage='not measured by fixed regression fixtures'), indent=2))


if __name__ == '__main__':
    main()
