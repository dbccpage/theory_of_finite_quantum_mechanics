# Second implementation of the Admit core rules.
# No repository imports. Lists grow by consing at the front, as in AdmitCore.

from __future__ import annotations


def empty():
    return {"data": [], "forms": [], "cuts": []}


def copy_regime(regime):
    return {
        "data": list(regime["data"]),
        "forms": list(regime["forms"]),
        "cuts": list(regime["cuts"]),
    }


def step(regime, event):
    kind = event[0]
    if kind == "supply":
        return copy_regime(regime)
    if kind == "admitData":
        n = event[1]
        out = copy_regime(regime)
        out["data"] = [n] + out["data"]
        return out
    if kind == "admitForm":
        i, k = event[1], event[2]
        out = copy_regime(regime)
        out["forms"] = [(i, k)] + out["forms"]
        return out
    if kind == "admitCut":
        a, b = event[1], event[2]
        if a not in regime["data"] or b not in regime["data"] or a == b:
            return None
        out = copy_regime(regime)
        out["cuts"] = [(a, b)] + out["cuts"]
        return out
    if kind == "impose":
        return None
    raise AssertionError("unknown event")


def holds_apart(regime, a, b):
    return (a, b) in regime["cuts"] and a != b


def holds_admitted_data(regime, n):
    return n in regime["data"]


def typed_form(regime, i, idx):
    return (i, len(idx)) in regime["forms"] and all(n in regime["data"] for n in idx)


def core_holds_apart(regime, imports, a, b):
    del imports
    return holds_apart(regime, a, b)


def main():
    failures = []

    derived = empty()
    derived = step(derived, ("admitData", 0))
    derived = step(derived, ("admitData", 1))
    derived = step(derived, ("admitCut", 0, 1))
    if derived is None or derived["data"] != [1, 0] or derived["cuts"] != [(0, 1)]:
        failures.append("derivation did not reach data [1, 0] and cut (0, 1)")
    elif not holds_apart(derived, 0, 1):
        failures.append("apart 0 1 does not hold after the three admissions")

    if holds_apart(empty(), 0, 1):
        failures.append("apart 0 1 holds in the empty regime")

    supplied = step(empty(), ("supply", 0))
    if supplied["data"] != [] or holds_admitted_data(supplied, 0):
        failures.append("supply admitted an index")

    if step(empty(), ("admitCut", 0, 0)) is not None:
        failures.append("self-cut was admitted")

    if step(empty(), ("impose",)) is not None:
        failures.append("impose stepped")

    forward = {"data": [0, 1], "forms": [], "cuts": [(0, 1)]}
    if holds_apart(forward, 1, 0):
        failures.append("the opposite cut holds")

    if holds_apart({"data": [0, 1], "forms": [], "cuts": []}, 0, 1):
        failures.append("distinct data yielded a cut")

    nullary = step(empty(), ("admitForm", 0, 0))
    if not typed_form(nullary, 0, []):
        failures.append("arity 0 did not type the empty application")
    if typed_form(nullary, 0, [1]):
        failures.append("a length-1 application typed at arity 0")

    records = [{"name": "S(n)"}, {"name": "MSS-N"}, {"name": "rules"}]
    if core_holds_apart(empty(), records, 0, 1):
        failures.append("import records made apart 0 1 hold in the empty regime")
    if not core_holds_apart(derived, records, 0, 1):
        failures.append("import records changed a judgment that already held")

    if failures:
        for item in failures:
            print("FAIL:", item)
        return 1

    print("checked derivation: admitData 0, admitData 1, admitCut 0 1 derives apart 0 1")
    print("checked non-derivation: empty regime does not derive apart 0 1")
    print("checked supply, self-cut, impose, opposite cut, distinct-without-cut, arity, import records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
