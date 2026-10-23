"""Independent exact audit of the admitted SEEK policy extension; no repo imports."""
from __future__ import annotations
from itertools import product
import json
import sympy as sp  # type: ignore[import-untyped]

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def main() -> None:
    regimes = rounds = saturated = 0
    for n, forms in product(range(4), ((), (1,), (2,))):
        atoms = tuple((f, xs) for f, a in enumerate(forms) for xs in product(range(n), repeat=a))
        pairs = tuple((i,j) for i in range(n) for j in range(i+1,n))
        contexts = tuple((f,xs) for f,a in enumerate(forms)
                         for xs in product((None,*range(n)), repeat=a) if None in xs)
        for fb,rb,qb in product(range(1 << len(atoms)),range(1 << len(forms)),range(1 << len(pairs))):
            facts = frozenset(x for k,x in enumerate(atoms) if fb & (1 << k))
            rules = frozenset(f for f in range(len(forms)) if rb & (1 << f))
            reqs = tuple(q for k,q in enumerate(pairs) if qb & (1 << k))
            profile = tuple(tuple(f in rules or (f,tuple(d if x is None else x for x in xs)) in facts
                                  for f,xs in contexts) for d in range(n))
            # Generator computes a direct all-context agreement test.
            def agenda(requirements: tuple[tuple[int,int], ...]) -> tuple[tuple[int,int], ...]:
                return tuple((i,j) for i in range(n) for j in range(n) if i < j and (i,j) not in requirements
                    and all((f in rules or (f,tuple(i if x is None else x for x in xs)) in facts) ==
                            (f in rules or (f,tuple(j if x is None else x for x in xs)) in facts)
                            for f,xs in contexts))
            wanted = tuple(q for q in pairs if profile[q[0]] == profile[q[1]] and q not in reqs)
            require(agenda(reqs) == wanted, 'soundness and completeness')
            original = reqs
            while agenda(reqs):
                q = agenda(reqs)[0]
                require(0 <= q[0] < q[1] < n and q not in reqs, 'source impose guard and freshness')
                before = len(reqs)
                reqs += (q,)
                require(len(reqs) == before+1 and q not in agenda(reqs), 'growth and no repeat')
                rounds += 1
            require(set(reqs) == set(original) | set(wanted), 'exact saturation; no new observations')
            require(len(reqs) <= len(pairs), 'finite requirement bound')
            regimes += 1
            saturated += 1
    expected = sum(sp.Integer(2)**(sum(sp.Integer(n)**a for a in forms)+len(forms)+n*(n-1)//2)
                   for n,forms in product(range(4), ((),(1,),(2,))))
    require(regimes == expected and regimes == saturated, 'exact census')
    # Wrong policies each have an explicit witness: reissue Q, infer a demand
    # with policy HALT, or claim an already separated pair remains collapsed.
    controls = {'duplicate_requirement': {'n':2,'Q':[[0,1]],'correct_next':None,'mutant_next':[0,1]},
                'ignore_halt': {'n':2,'policy':'halt','correct_next':None,'mutant_next':[0,1]},
                'ignore_observation': {'unary_fact':[0],'profiles':[[True],[False]],'correct_next':None,'mutant_next':[0,1]}}
    def choose(profiles: tuple[tuple[bool,...],...], requirements: tuple[tuple[int,int],...],
               enabled: bool, mutant: str = '') -> tuple[int,int] | None:
        if not enabled and mutant != 'ignore_halt':
            return None
        for i,j in product(range(len(profiles)),repeat=2):
            if i < j and (mutant == 'duplicate_requirement' or (i,j) not in requirements) and (
                    mutant == 'ignore_observation' or profiles[i] == profiles[j]):
                return (i,j)
        return None
    fixtures = {'duplicate_requirement': (((),()),((0,1),),True),
                'ignore_halt': (((),()),(),False),
                'ignore_observation': (((True,),(False,)),(),True)}
    for name,(profiles,requirements,enabled) in fixtures.items():
        correct = choose(profiles,requirements,enabled)
        mutant = choose(profiles,requirements,enabled,name)
        require(correct is None and mutant == (0,1), 'concrete semantic mutant: '+name)
    print(json.dumps(dict(node='PGW-ENDOGENOUS-DEMAND-OB1',authority_effect='None',extension=True,
        regimes_checked=regimes,seek_rounds=rounds,saturated=saturated,datum_bound=3,
        signatures=[[],[1],[2]],policy_controls=controls,
        mutation_accounting=dict(killed=len(controls),survived=0,demonstrably_equivalent=0,invalid=0,inconclusive=0,unrun=0)),indent=2))

if __name__ == '__main__':
    main()
