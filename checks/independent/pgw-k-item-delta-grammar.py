"""Independent census for one empty base of PGW-K-ITEM-DELTA-GRAMMAR.

Arity one, two starting data, no forms, no instances, no rules.
The atom universe has ten constructors. Admission is recomputed here
and is not imported from the repository.
"""

from __future__ import annotations


DATUM = "datum"
FORM = "form1"
RULE0 = "rule0"
RULE1 = "rule1"
I0T0 = "i0t0"
I0T1 = "i0t1"
I0FR = "i0fr"
I1T0 = "i1t0"
I1T1 = "i1t1"
I1FR = "i1fr"

ATOMS = (DATUM, FORM, RULE0, RULE1, I0T0, I0T1, I0FR, I1T0, I1T1, I1FR)


def base():
    return {"data": 2, "forms": 0, "insts": (), "rules": ()}


def step(state, atom):
    data = state["data"]
    forms = state["forms"]
    insts = state["insts"]
    rules = state["rules"]
    if atom == DATUM:
        return {"data": data + 1, "forms": forms, "insts": insts, "rules": rules}
    if atom == FORM:
        return {"data": data, "forms": forms + 1, "insts": insts, "rules": rules}
    if atom == RULE0:
        if 0 < forms:
            return {"data": data, "forms": forms, "insts": insts, "rules": rules + (0,)}
        return None
    if atom == RULE1:
        if 1 < forms:
            return {"data": data, "forms": forms, "insts": insts, "rules": rules + (1,)}
        return None
    table = {
        I0T0: (0, 0),
        I0T1: (0, 1),
        I0FR: (0, 2),
        I1T0: (1, 0),
        I1T1: (1, 1),
        I1FR: (1, 2),
    }
    form, arg = table[atom]
    if form < forms and arg < data:
        return {
            "data": data,
            "forms": forms,
            "insts": insts + ((form, arg),),
            "rules": rules,
        }
    return None


def run(seq):
    state = base()
    for atom in seq:
        state = step(state, atom)
        if state is None:
            return None
    return state


def profile_at(state, form, arg):
    if not (form < state["forms"]):
        return False
    if form in state["rules"]:
        return True
    return (form, arg) in state["insts"]


def separates(state):
    if state is None:
        return False
    left = profile_at(state, 0, 0) != profile_at(state, 0, 1)
    right = (1 < state["forms"]) and (
        profile_at(state, 1, 0) != profile_at(state, 1, 1)
    )
    return left or right


def main():
    failures = 0
    checks = 0

    def expect(cond, label):
        nonlocal failures, checks
        checks += 1
        if not cond:
            failures += 1
            print("fail", label)

    singles = [a for a in ATOMS if run((a,)) is not None]
    pairs = [(a, b) for a in ATOMS for b in ATOMS if run((a, b)) is not None]
    separating_singles = [a for a in ATOMS if separates(run((a,)))]
    separating_pairs = [
        (a, b) for a in ATOMS for b in ATOMS if separates(run((a, b)))
    ]
    expect(singles == [DATUM, FORM], "singles")
    expect(
        pairs
        == [
            (DATUM, DATUM),
            (DATUM, FORM),
            (FORM, DATUM),
            (FORM, FORM),
            (FORM, RULE0),
            (FORM, I0T0),
            (FORM, I0T1),
        ],
        "pairs",
    )
    expect(separating_singles == [], "no single separator")
    expect(separating_pairs == [(FORM, I0T0), (FORM, I0T1)], "two separators")
    expect(len(singles) + len(pairs) == 9, "nine well-formed")
    expect(len(singles) + len(pairs) - len(separating_pairs) == 7, "seven equal")
    expect(len(ATOMS) == 10, "ten atoms")
    expect(len(ATOMS) * len(ATOMS) == 100, "one hundred pairs")

    for seq in ((DATUM, DATUM), (DATUM, FORM), (FORM, DATUM)):
        state = run(seq)
        expect(separates(state) is False, "fresh " + ",".join(seq))
        expect(state["data"] > 2, "data grew " + ",".join(seq))

    rule = run((FORM, RULE0))
    expect(profile_at(rule, 0, 0) is True, "rule bit 0")
    expect(profile_at(rule, 0, 1) is True, "rule bit 1")
    expect(separates(rule) is False, "rule does not separate")

    short = run((FORM, I0T0))
    long = run((FORM, I0T0, RULE0))
    expect(profile_at(short, 0, 0) is True and profile_at(short, 0, 1) is False, "short bits")
    expect(separates(short) is True, "short separates")
    expect(profile_at(long, 0, 0) is True and profile_at(long, 0, 1) is True, "long bits")
    expect(separates(long) is False, "long does not separate")
    expect(len((FORM, I0T0)) == 2 and len((FORM, I0T0, RULE0)) == 3, "lengths 2 and 3")
    expect(2 < 3, "two is shorter than three")

    off = run((DATUM, FORM, I0FR))
    expect(off["insts"] == ((0, 2),), "fresh instance recorded")
    expect(profile_at(off, 0, 0) is False and profile_at(off, 0, 1) is False, "off bits")
    expect(separates(off) is False, "off does not separate")
    expect(len((DATUM, FORM, I0FR)) == 3, "off length 3")

    # Arity two is outside this census: a binary form is not in the atom list.
    expect(FORM == "form1", "only unary form atom")
    expect(all(atom != "form2" for atom in ATOMS), "no arity-two atom")

    print(f"checked {checks} conditions, {failures} failures")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
