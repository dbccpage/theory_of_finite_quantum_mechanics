"""Independent replay of the two sealed Lean reading histories.

Recomputes stepE and replayE for readings L and F. Does not import
repository code and does not claim a Python-to-Lean refinement.
"""
from __future__ import annotations

import re
from pathlib import Path

GENESIS = (0, (), (), (), ())
HISTORY_L = (
    ("supply", 0),
    ("supply", 1),
    ("supply", 1),
    ("supply", 2),
    ("admitDatum",),
    ("admitDatum",),
    ("impose", 0, 1),
)
HISTORY_F = (
    ("supply", 0),
    ("admitDatum",),
    ("supply", 1),
    ("supply", 1),
    ("supply", 2),
    ("admitDatum",),
    ("admitDatum",),
    ("impose", 1, 2),
)
THEOREM_NAMES = (
    "pgwHistoryL_replays",
    "pgwHistoryF_replays",
    "pgwR2L_ne_R2F",
    "pgwReplay_ne",
    "pgwData_counts",
    "pgwReqs",
    "pgwEmpty_carriers",
    "pgwHistory_lengths",
)


def insert_new(items, value):
    if value in items:
        return items
    return items + (value,)


def step(regime, event):
    data, forms, insts, rules, reqs = regime
    kind = event[0]
    if kind == "supply":
        return regime
    if kind == "admitDatum":
        return (data + 1, forms, insts, rules, reqs)
    if kind == "admitForm":
        arity = event[1]
        if arity >= 1:
            return (data, forms + (arity,), insts, rules, reqs)
        return None
    if kind == "admitInst":
        form, args = event[1], tuple(event[2])
        if form < len(forms) and len(args) == (forms[form] if form < len(forms) else 0) and all(
            x < data for x in args
        ):
            return (data, forms, insert_new(insts, (form, args)), rules, reqs)
        return None
    if kind == "admitRuleAll":
        form = event[1]
        if form < len(forms):
            return (data, forms, insts, insert_new(rules, form), reqs)
        return None
    if kind == "impose":
        i, j = event[1], event[2]
        if i < j and j < data:
            return (data, forms, insts, rules, insert_new(reqs, (i, j)))
        return None
    raise ValueError(kind)


def replay(history, base):
    regime = base
    for event in history:
        regime = step(regime, event)
        if regime is None:
            return None
    return regime


def main() -> None:
    failures: list[str] = []
    claims = 0

    def check(name: str, ok: bool) -> None:
        nonlocal claims
        claims += 1
        if not ok:
            failures.append(name)

    got_l = replay(HISTORY_L, GENESIS)
    got_f = replay(HISTORY_F, GENESIS)
    check("replay_l", got_l == (2, (), (), (), ((0, 1),)))
    check("replay_f", got_f == (3, (), (), (), ((1, 2),)))
    check("regimes_differ", got_l != got_f)
    check("data_counts", got_l is not None and got_f is not None and got_l[0] == 2 and got_f[0] == 3)
    check("reqs", got_l is not None and got_f is not None and got_l[4] == ((0, 1),) and got_f[4] == ((1, 2),))
    check(
        "empty_carriers",
        got_l is not None
        and got_f is not None
        and got_l[1] == ()
        and got_l[2] == ()
        and got_l[3] == ()
        and got_f[1] == ()
        and got_f[2] == ()
        and got_f[3] == (),
    )
    check("lengths", len(HISTORY_L) == 7 and len(HISTORY_F) == 8)
    check("supply_keeps_genesis", step(GENESIS, ("supply", 0)) == GENESIS)
    check("impose_needs_data", step(GENESIS, ("impose", 0, 1)) is None)
    check("histories_differ", HISTORY_L != HISTORY_F)

    root = Path(__file__).resolve().parents[2]
    lean = (root / "lean4" / "PregenesisPythonLeanCarrierBridge.lean").read_text(encoding="utf-8")
    check("lean_history_l", ".supply 0, .supply 1, .supply 1, .supply 2" in lean and ".impose 0 1" in lean)
    check("lean_history_f", ".impose 1 2" in lean and lean.count(".admitDatum") == 5)
    for name in THEOREM_NAMES:
        check(f"theorem_{name}", f"theorem {name}" in lean)
    for token in ("sorry", "native_decide", "unsafe"):
        check(f"no_{token}", token not in lean)
    check("no_axiom_decl", all(not line.startswith("axiom ") for line in lean.splitlines()))
    check("no_admit_tactic", re.search(r"\badmit\b", lean) is None)
    check("prints_axioms", lean.count("#print axioms ") == len(THEOREM_NAMES))

    print(f"checked {claims} claims, failures {len(failures)}")
    if failures:
        print("failures: " + ", ".join(failures))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
