# -*- coding: utf-8 -*-
"""Independent check for the PGW-CONTEXT-FIDELITY two-code witness."""
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


stale = 0
replay = 1


def empty_claim(ctx):
    return ctx == 0


def accept_binding(declared, replayed):
    return declared == replayed


check("codes differ", stale != replay)
check("empty claim on stale", empty_claim(stale) is True)
check("empty claim on replay", empty_claim(replay) is False)
check("binding refuses stale pair", accept_binding(stale, replay) is False)
check("binding accepts matched replay", accept_binding(replay, replay) is True)
check("binding accepts matched stale", accept_binding(stale, stale) is True)
check("binding refuses swapped pair", accept_binding(replay, stale) is False)

pairs = [(0, 0), (0, 1), (1, 0), (1, 1)]
accepted = [pair for pair in pairs if accept_binding(*pair)]
check("four ordered pairs", len(pairs) == 4)
check("accepted pairs are the diagonal", accepted == [(0, 0), (1, 1)])
check("accept count is 2", len(accepted) == 2)

lean = (ROOT / "lean4" / "CampaignPgwContextFidelity.lean").read_text(encoding="utf-8")
for name in (
    "pgwContext_codes_differ",
    "pgwContext_empty_claim_on_stale",
    "pgwContext_empty_claim_on_replay",
    "pgwContext_binding_refuses_stale",
    "pgwContext_binding_accepts_match",
    "pgwContext_accept_count",
):
    check("lean names " + name, ("theorem " + name) in lean)
check("lean has no sorry", "sorry" not in lean)
check("lean has no admit tactic", "\nadmit" not in lean and " admit" not in lean)
check("lean has no axiom declaration", "\naxiom " not in lean)
check("lean has no native_decide", "native_decide" not in lean)
check("lean has no unsafe", "unsafe" not in lean)

paper = (ROOT / "dag" / "derivations" / "01_pregenesis" / "tfq_0427_context_fidelity.md").read_text(encoding="utf-8")
check("paper keeps open obligation status", "OPEN_OBLIGATION" in paper)
check("paper names the two-code witness", "two-code" in paper)

print(f"checked {checked} claims, failures {len(failures)}")
if failures:
    print("FAILED", ", ".join(failures))
    sys.exit(1)
