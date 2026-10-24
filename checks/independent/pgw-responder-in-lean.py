# -*- coding: utf-8 -*-
"""Independent check for the PGW-RESPONDER-IN-LEAN shadow."""
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


def read_demand(kind, holds_uniform):
    return kind == "collapsed" and not holds_uniform


def arity_sum(items):
    total = 0
    for kind, payload in items:
        if kind == "form":
            total += payload
    return total


def has_rule(items):
    return any(kind == "rule" for kind, _ in items)


def within(items):
    return len(items) <= 2 and arity_sum(items) <= 2 and not has_rule(items)


def lex_lt(left, right):
    if left[0] < right[0]:
        return True
    if left[0] == right[0] and left[1] < right[1]:
        return True
    return False


flags = (
    ("collapsed", False),
    ("collapsed", True),
    ("separable", False),
    ("separable", True),
)
reads = [read_demand(kind, flag) for kind, flag in flags]
check("four flag pairs", len(flags) == 4)
check("read table", reads == [True, False, False, False])
check("read count", sum(1 for item in reads if item) == 1)

mark = [("form", 1), ("inst", (0,))]
link = [("form", 2), ("inst", (0, 1))]
ruled = [("form", 1), ("rule", 0)]
three = [("form", 1), ("inst", (0,)), ("inst", (1,))]

check("mark length", len(mark) == 2)
check("link length", len(link) == 2)
check("mark arity", arity_sum(mark) == 1)
check("link arity", arity_sum(link) == 2)
check("lists differ", mark != link)
check("mu1 mark", len(mark) == 2)
check("mu1 link", len(link) == 2)
check("mu1 tie", len(mark) == len(link))
mu2_mark = (len(mark), arity_sum(mark))
mu2_link = (len(link), arity_sum(link))
check("mu2 mark", mu2_mark == (2, 1))
check("mu2 link", mu2_link == (2, 2))
check("lex order", lex_lt(mu2_mark, mu2_link))
check("equal counts", mu2_mark[0] == mu2_link[0])
check("arity order", mu2_mark[1] < mu2_link[1])
check("mark inside", within(mark) is True)
check("link inside", within(link) is True)
check("ruled length", len(ruled) == 2)
check("ruled outside", within(ruled) is False)
check("three length", len(three) == 3)
check("three outside", within(three) is False)
check("three above bound", len(three) > 2)

src = (
    ROOT / "lean4" / "Imported" / "Genesis19l57g1" / "Derivation" / "Minimality.lean"
).read_text(encoding="utf-8")
for needle in (
    "def deltaU0 : List Item := [.newForm 1, .newInst 0 [0]]",
    "def deltaBL : List Item := [.newForm 2, .newInst 0 [0, 1]]",
):
    check("source " + needle.split()[1], needle in src)

lean = (ROOT / "lean4" / "CampaignPgwResponderInLean.lean").read_text(encoding="utf-8")
for name in (
    "pgwRead_table",
    "pgwRead_count",
    "pgwMark_link_shape",
    "pgwMu1_tie",
    "pgwMu2_pairs",
    "pgwMu2_mark_before_link",
    "pgwBound_inside",
    "pgwRuled_outside",
    "pgwThree_outside",
):
    check("lean " + name, ("theorem " + name) in lean)
check("no sorry", "sorry" not in lean)
check("no admit", "admit" not in lean)
check("no native_decide", "native_decide" not in lean)
check("no unsafe", "unsafe" not in lean)
check("no axiom decl", "\naxiom " not in lean)

print("checked %d claims, failures %d" % (checked, len(failures)))
if failures:
    print("FAILED", ", ".join(failures))
    sys.exit(1)
