"""Exact independent five-coordinate and mode Genesis engine audit. AuthorityEffect: None.

No repository imports. Two transition implementations, partial failure,
mode switches, and all declared full-engine histories are compared.
The general representation theorem is in Lean; this census has printed bounds.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json
from typing import Literal

import sympy as sp  # type: ignore[import-untyped]

Kind = Literal["supply", "datum", "form", "inst", "rule", "impose"]
Instance = tuple[int, tuple[int, ...]]
Pair = tuple[int, int]
State = tuple[int, tuple[int, ...], tuple[Instance, ...], tuple[int, ...], tuple[Pair, ...]]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


@dataclass(frozen=True)
class Event:
    kind: Kind
    a: int = 0
    b: int = 0
    args: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in ("supply", "datum", "form", "inst", "rule", "impose"):
            raise ValueError("unknown event")
        if any(type(x) is not int or x < 0 for x in (self.a, self.b, *self.args)):
            raise ValueError("exact natural event coordinates required")
        if type(self.args) is not tuple:
            raise ValueError("immutable argument tuple required")


def step(r: State, e: Event) -> State | None:
    n, fs, ins, rules, qs = r
    if e.kind == "supply":
        return r
    if e.kind == "datum":
        return n + 1, fs, ins, rules, qs
    if e.kind == "form":
        return (n, (*fs, e.a), ins, rules, qs) if e.a >= 1 else None
    if e.kind == "inst":
        if not (e.a < len(fs) and len(e.args) == fs[e.a] and all(x < n for x in e.args)):
            return None
        item = (e.a, e.args)
        return n, fs, ins if item in ins else (*ins, item), rules, qs
    if e.kind == "rule":
        if e.a >= len(fs):
            return None
        return n, fs, ins, rules if e.a in rules else (*rules, e.a), qs
    if not e.a < e.b < n:
        return None
    q = (e.a, e.b)
    return n, fs, ins, rules, qs if q in qs else (*qs, q)


def array_step(r: State, e: Event) -> State | None:
    """Separate mutable-coordinate implementation, not a call to step()."""
    data, forms, instances, uniform, requirements = r
    f, i, u, q = list(forms), list(instances), list(uniform), list(requirements)
    if e.kind in ("form", "inst", "rule", "impose"):
        guards = {"form": e.a > 0,
                  "inst": e.a in range(len(f)) and len(e.args) == (f[e.a] if e.a < len(f) else 0)
                          and set(e.args).issubset(range(data)),
                  "rule": e.a in range(len(f)),
                  "impose": e.a in range(e.b) and e.b in range(data)}
        if not guards[e.kind]:
            return None
    if e.kind == "datum":
        data += 1
    elif e.kind == "form":
        f.append(e.a)
    elif e.kind == "inst" and (e.a, e.args) not in i:
        i.append((e.a, e.args))
    elif e.kind == "rule" and e.a not in u:
        u.append(e.a)
    elif e.kind == "impose" and (e.a, e.b) not in q:
        q.append((e.a, e.b))
    return data, tuple(f), tuple(i), tuple(u), tuple(q)


def replay(h: tuple[Event, ...], base: State, arrays: bool = False) -> State | None:
    state: State | None = base
    transition = array_step if arrays else step
    for e in h:
        if state is None:
            return None
        state = transition(state, e)
    return state


def potential(r: State) -> int:
    return r[0] + sum(len(xs) for xs in r[1:])


Engine = tuple[State,bool]

def engine_step(s: Engine,e: Event | None,arrays: bool = False) -> Engine | None:
    r,mode=s
    if e is None:
        return (r,False if mode else True) if arrays else (r,not mode)
    result=array_step(r,e) if arrays else step(r,e)
    return None if result is None else (result,mode)

def engine_replay(h: tuple[Event | None,...],s: Engine,arrays: bool = False) -> Engine | None:
    result: Engine | None=s
    for e in h:
        if result is None:return None
        result=engine_step(result,e,arrays)
    return result

def main() -> None:
    alphabet=(None,Event('supply',7),Event('datum'),Event('form',0),Event('form',1),
              Event('inst',0,args=(0,)),Event('inst',0,args=(0,1)),Event('rule',0),Event('impose',0,1))
    bases: tuple[State,...]=((0,(),(),(),()),(2,(),(),(),((0,1),)),(3,(),(),(),((1,2),)))
    cases=failures=regime_changes=mode_changes=0
    seen: set[Engine]=set()
    for base,mode in product(bases,(False,True)):
        start=(base,mode)
        for length in range(5):
            for history in product(alphabet,repeat=length):
                answer=engine_replay(history,start)
                require(answer==engine_replay(history,start,True),'full engine replay including failure')
                cases+=1;failures+=answer is None
                if answer is not None:seen.add(answer)
                state: Engine | None=start
                prior_regimes=[base]
                for e in history:
                    if state is None:break
                    nxt=engine_step(state,e)
                    if nxt is not None:
                        require(potential(state[0]) <= potential(nxt[0]),'cumulative potential')
                        if state[0] != nxt[0]:
                            require(potential(state[0]) < potential(nxt[0]),'every actual regime change is strict')
                            require(nxt[0] not in prior_regimes,'no return after a regime change')
                            regime_changes+=1
                        elif state[1] != nxt[1]:mode_changes+=1
                        prior_regimes.append(nxt[0])
                    state=nxt
    expected=6*sum(sp.Integer(len(alphabet))**k for k in range(5))
    require(cases==expected,'complete declared history census')
    for r,_ in seen:
        require(potential(r)==sp.Matrix([r[0],*(len(x) for x in r[1:])]).dot(sp.ones(5,1)), 'exact source potential')
    start=(bases[1],False)
    require(engine_replay((None,None),start)==start and engine_step(start,None)!=start,'mode-only changes refute full-state strictness')
    require(engine_replay((None,Event('form',0),None),start) is None,'invalid source event must preserve failure')
    require(engine_step(start,None)==(bases[1],True),'switch must toggle the mode')
    fresh: State=(2,(),(),(),())
    imposed=step(fresh,Event('impose',0,1));require(imposed is not None,'fresh requirement fixture')
    if imposed is None:raise RuntimeError('unreachable')
    require(potential(imposed)==potential(fresh)+1,'fresh requirements contribute to potential')
    duplicate: State=(2,(1,),((0,(0,)),),(),())
    require(step(duplicate,Event('inst',0,args=(0,)))==duplicate,'duplicate admissions can leave the regime unchanged')
    print(json.dumps(dict(node='PG-GEN-NO-RETURN',authority_effect='None',histories=cases,failures=failures,
        distinct_successful_engine_states=len(seen),regime_changes_in_tested_prefixes=regime_changes,
        mode_only_changes_in_tested_prefixes=mode_changes,bases=3,modes=2,alphabet_size=len(alphabet),maximum_history_length=4,
        negative_controls_checked=5, mutation_coverage='not measured by fixed regression fixtures'),indent=2))

if __name__=='__main__':main()
