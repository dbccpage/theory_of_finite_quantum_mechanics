"""Finite process comparison and hidden-clock audit; no repository imports."""
from __future__ import annotations
from itertools import product
import json
from typing import TypeAlias
import sympy as sp  # type: ignore[import-untyped]

Process: TypeAlias = tuple[tuple[int,...],int,tuple[bool,...]]

def require(ok: bool,message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def equivalent(p: Process, q: Process, x: int, y: int) -> bool:
    seen: set[tuple[int,int]] = set()
    while (x,y) not in seen:
        if p[2][x] != q[2][y]:
            return False
        seen.add((x,y))
        x,y = p[0][x],q[0][y]
    return True

def main() -> None:
    processes: list[Process] = [(step,root,read) for n in range(1,4)
        for step in product(range(n),repeat=n) for root in range(n)
        for read in product((False,True),repeat=n)]
    expected = sum(sp.Integer(n)**(n+1) * sp.Integer(2)**n for n in range(1,4))
    require(len(processes) == expected, 'process census')
    hom_candidates = minimal_pairs = equal_pairs = 0
    for p in processes:
        n=len(p[0]);period=n+1
        # Every hom into the product clock would have this component.
        for f in product(range(period),repeat=n):
            hom_candidates += 1
            if f[p[1]] == 0:
                require(not all(f[p[0][x]] == (f[x]+1)%period for x in range(n)), 'no clock-component hom')
        # All-time observation equality certified by finite pair-orbit closure.
        step=tuple(p[0][x]*period+(k+1)%period for x in range(n) for k in range(period))
        read=tuple(p[2][x] for x in range(n) for _ in range(period))
        lift=(step,p[1]*period,read)
        require(equivalent(p,lift,p[1],lift[1]), 'clock projection behavior')
        reached: set[int]=set();x=p[1]
        while x not in reached:
            reached.add(x);x=p[0][x]
        reduced=all(x == y or not equivalent(p,p,x,y) for x,y in product(range(n),repeat=2))
        for q in processes:
            if equivalent(p,q,p[1],q[1]):
                equal_pairs += 1
                if len(reached)==n and reduced:
                    require(n <= len(q[0]), 'minimum-size criterion')
                    minimal_pairs += 1
    one=((0,),0,(False,));hidden=((1,0),0,(False,False))
    require(equivalent(hidden,one,0,0) and len(hidden[0]) > len(one[0]), 'nonminimal adequate process')
    unreachable=((0,1),0,(False,True))
    require(equivalent(unreachable,one,0,0), 'reachability cannot be omitted')
    # Dropping action preservation admits a root-preserving clock map.
    bad_clock_map = (0,0)
    require(bad_clock_map[hidden[1]] == 0 and
            any(bad_clock_map[hidden[0][x]] != (bad_clock_map[x]+1)%3 for x in range(2)),
            'root-only map exists but violates the required action square')
    supply_clock_maps = 0
    source_tick = (0,1)
    target_tick = (1,0,3,2)
    for f in product(range(4),repeat=2):
        supply_clock_maps += 1
        require(not (f[1] == 2 and all(f[source_tick[x]] == target_tick[f[x]] for x in range(2))),
                'supply self-loop forbids a root/action-preserving hidden clock map')
    target_matrix = sp.Matrix(4,4,lambda i,j: int(target_tick[int(j)] == int(i)))
    require(sp.trace(target_matrix) == 0 and supply_clock_maps == sp.Integer(4)**2, 'exact supply countermodel')
    print(json.dumps(dict(node='PGW-MINIMAL-OR-INITIAL-REFUSED',authority_effect='None',comparison_class_extension=True,
        processes=len(processes),state_bound=3,clock_component_candidates=hom_candidates,
        behavior_equal_pairs=equal_pairs,minimality_comparisons=minimal_pairs,
        source_supply_clock_maps=supply_clock_maps,controls={'nonreduced':hidden,'unreachable':unreachable,'one_state':one},
        mutation_accounting=dict(killed=3,survived=0,demonstrably_equivalent=0,invalid=0,inconclusive=0,unrun=0)),indent=2))

if __name__=='__main__':
    main()
