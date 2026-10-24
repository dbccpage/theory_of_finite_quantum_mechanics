# -*- coding: utf-8 -*-
"""Independent check for the four declared Challenge 3 delta lists."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
failures = []
checked = 0


def check(name, ok):
    global checked
    checked += 1
    if not ok:
        failures.append(name)


u0 = [("form", 1), ("inst", (0,))]
u1 = [("form", 1), ("inst", (1,))]
bl = [("form", 2), ("inst", (0, 1))]
bd = [("form", 2), ("inst", (0, 0))]
four = (("u0", u0, 1, (0,)), ("u1", u1, 1, (1,)),
        ("bl", bl, 2, (0, 1)), ("bd", bd, 2, (0, 0)))


def form_arity(items):
    for kind, payload in items:
        if kind == "form":
            return payload
    return None


def inst_args(items):
    for kind, payload in items:
        if kind == "inst":
            return payload
    return None


check("four lists", len(four) == 4)
for name, items, arity, args in four:
    check(name + " length", len(items) == 2)
    check(name + " arity", form_arity(items) == arity)
    check(name + " args", inst_args(items) == args)

check("arity sum", sum(form_arity(items) for _, items, _, _ in four) == 6)
pairs = []
rows = [items for _, items, _, _ in four]
for i in range(4):
    for j in range(i + 1, 4):
        pairs.append((rows[i], rows[j]))
check("six pairs", len(pairs) == 6)
check("pairwise distinct", all(a != b for a, b in pairs))
three = [("form", 1), ("inst", (0,)), ("inst", (1,))]
check("three-item length", len(three) == 3)
check("three above two", len(three) > len(u0))

src = (ROOT / "lean4" / "Imported" / "Genesis19l57g1" / "Derivation" / "Minimality.lean").read_text(encoding="utf-8")
for needle in (
    "def deltaU0 : List Item := [.newForm 1, .newInst 0 [0]]",
    "def deltaU1 : List Item := [.newForm 1, .newInst 0 [1]]",
    "def deltaBL : List Item := [.newForm 2, .newInst 0 [0, 1]]",
    "def deltaBD : List Item := [.newForm 2, .newInst 0 [0, 0]]",
):
    check("source " + needle.split()[1], needle in src)

lean = (ROOT / "lean4" / "CampaignPgwKItemDeltaGrammar.lean").read_text(encoding="utf-8")
for name in (
    "pgwKItem_lengths",
    "pgwKItem_arities",
    "pgwKItem_arity_sum",
    "pgwKItem_pairwise",
    "pgwKItem_three_length",
    "pgwKItem_three_above_two",
):
    check("lean " + name, ("theorem " + name) in lean)
check("no sorry", "sorry" not in lean)
check("no native_decide", "native_decide" not in lean)
check("no unsafe", "unsafe" not in lean)
check("no axiom decl", "\naxiom " not in lean)

print(f"checked {checked} claims, failures {len(failures)}")
if failures:
    print("FAILED", ", ".join(failures))
    sys.exit(1)
