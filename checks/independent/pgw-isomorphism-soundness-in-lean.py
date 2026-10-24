"""Independent check for PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN.

Recomputes the exhaustive canonical keys of the two-datum regimes U0, U1,
and BL. No repository module is imported.
"""
from __future__ import annotations

import pathlib
import re
import sys

U0 = (2, [1], [(0, [0])], [], [(0, 1)])
U1 = (2, [1], [(0, [1])], [], [(0, 1)])
BL = (2, [2], [(0, [0, 1])], [], [(0, 1)])

THEOREM_NAMES = [
    "pgwIso_U0_U1",
    "pgwIso_U0_wf",
    "pgwIso_U1_wf",
    "pgwIso_BL_wf",
    "pgwIso_set_collections",
    "pgwIso_candidate_counts",
    "pgwIso_keys_eq",
    "pgwIso_keys_ne",
    "pgwIso_U0_not_BL",
]


def permutations(values: list[int]) -> list[list[int]]:
    if not values:
        return [[]]
    head, tail = values[0], values[1:]
    out: list[list[int]] = []
    for perm in permutations(tail):
        for index in range(len(perm) + 1):
            out.append(perm[:index] + [head] + perm[index:])
    return out


def as_map(table: list[int]) -> dict[int, int]:
    return {index: value for index, value in enumerate(table)}


def map_req(fn: dict[int, int], pair: tuple[int, int]) -> tuple[int, int]:
    left, right = fn[pair[0]], fn[pair[1]]
    return (left, right) if left <= right else (right, left)


def relabel(regime, data_table: list[int], form_table: list[int]):
    data, forms, insts, rules, reqs = regime
    data_fn = as_map(data_table)
    form_fn = as_map(form_table)
    form_inv = {value: index for index, value in enumerate(form_table)}
    new_forms = [forms[form_inv[j]] for j in range(len(forms))]
    new_insts = [(form_fn[form], [data_fn[arg] for arg in args]) for form, args in insts]
    new_rules = [form_fn[rule] for rule in rules]
    new_reqs = [map_req(data_fn, req) for req in reqs]
    return (data, new_forms, sorted(new_insts), sorted(new_rules), sorted(new_reqs))


def candidate_keys(regime):
    data, forms, _insts, _rules, _reqs = regime
    keys = []
    for data_table in permutations(list(range(data))):
        for form_table in permutations(list(range(len(forms)))):
            keys.append(relabel(regime, data_table, form_table))
    return keys


def minimum(keys):
    best = keys[0]
    for key in keys[1:]:
        if key < best:
            best = key
    return best


def canonical(regime):
    return minimum(candidate_keys(regime))


def swap01(value: int) -> int:
    if value == 0:
        return 1
    if value == 1:
        return 0
    return value


def main() -> int:
    failures = 0
    claims = 0

    def check(ok: bool, label: str) -> None:
        nonlocal failures, claims
        claims += 1
        if not ok:
            failures += 1
            print("FAIL", label)

    u0_keys = candidate_keys(U0)
    u1_keys = candidate_keys(U1)
    bl_keys = candidate_keys(BL)
    u0_key = canonical(U0)
    u1_key = canonical(U1)
    bl_key = canonical(BL)
    expected = (2, [1], [(0, [0])], [], [(0, 1)])
    bl_expected = (2, [2], [(0, [0, 1])], [], [(0, 1)])
    check(len(u0_keys) == 2 and len(u1_keys) == 2 and len(bl_keys) == 2, "candidate counts")
    check(len(set(map(tuple_key, u0_keys))) == 2, "U0 candidates differ")
    check(u0_key == expected and u1_key == expected, "unary minima")
    check(bl_key == bl_expected, "binary minimum")
    check(u0_key == u1_key and u0_key != bl_key, "key comparison")
    swapped = (2, [1], [(0, [swap01(0)])], [], [(min(swap01(0), swap01(1)), max(swap01(0), swap01(1)))])
    check(swapped == U1, "swap sends U0 onto U1")
    check(U0[1] != BL[1], "form arities differ")
    check(all(1 <= arity for arity in U0[1] + U1[1] + BL[1]), "form arities at least 1")
    check(U0[4] == [(0, 1)] and U1[4] == [(0, 1)] and BL[4] == [(0, 1)], "one ordered requirement")
    check(U0[0] == 2 and U1[0] == 2 and BL[0] == 2, "data count 2")
    root = pathlib.Path(__file__).resolve().parents[2]
    lean = (root / "lean4" / "CampaignPgwIsomorphismSoundnessInLean.lean").read_text(encoding="utf-8")
    for name in THEOREM_NAMES:
        check(f"theorem {name} " in lean or f"theorem {name}:" in lean or f"def {name} " in lean, name)
        check(sum(1 for line in lean.splitlines() if line == f"#print axioms {name}") == 1, f"axioms {name}")
    check(re.search(r"\bsorry\b", lean) is None, "no sorry")
    check(re.search(r"\badmit\b", lean) is None, "no admit")
    check(re.search(r"\baxiom\b", lean) is None, "no axiom")
    check("native_decide" not in lean and "unsafe" not in lean, "no native_decide or unsafe")
    print(f"checked {claims} claims, failures {failures}")
    print("U0 key", u0_key)
    print("BL key", bl_key)
    return 1 if failures else 0


def tuple_key(key):
    data, forms, insts, rules, reqs = key
    return (data, tuple(forms), tuple((form, tuple(args)) for form, args in insts), tuple(rules), tuple(reqs))


if __name__ == "__main__":
    sys.exit(main())
