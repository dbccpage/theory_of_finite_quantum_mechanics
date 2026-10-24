"""Independent check for PGW-DRIVER-B-SEVENTH-EVENT.

Recomputes the six constructor names of the sealed derivation Event.
Does not import repository code and does not call a harness.
"""

from __future__ import annotations

import re
from pathlib import Path

KINDS = [
    "Supply",
    "AdmitDatum",
    "AdmitForm",
    "AdmitInst",
    "AdmitRuleAll",
    "Impose",
]
SEVENTH = "Seventh"
THEOREM_NAMES = [
    "pgwDrvB_kind_count",
    "pgwDrvB_kind_nodup",
    "pgwDrvB_kindName_mem",
    "pgwDrvB_names_realized",
    "pgwDrvB_seventh_outside",
    "pgwDrvB_no_seventh_name",
]
LEAN = Path(__file__).resolve().parents[2] / "lean4" / "CampaignPgwDriverBSeventhEvent.lean"


def kind_name(tag: str) -> str:
    if tag not in KINDS:
        raise ValueError(tag)
    return tag


def main() -> int:
    failures = 0
    claims = 0

    def check(ok: bool, label: str) -> None:
        nonlocal failures, claims
        claims += 1
        if not ok:
            failures += 1
            print("FAIL", label)

    check(len(KINDS) == 6, "length 6")
    check(len(set(KINDS)) == 6, "no duplicate names")
    check(SEVENTH not in KINDS, "Seventh outside the list")
    check(all(kind_name(name) == name for name in KINDS), "each name is realized")
    check(all(name != SEVENTH for name in KINDS), "each name differs from Seventh")
    text = LEAN.read_text(encoding="utf-8")
    lines = text.splitlines()
    check("\r" not in text, "lean file has no CR")
    listed = re.search(r"def pgwDrvB_kindNames : List String :=\n  \[(.*)\]", text)
    check(listed is not None, "name list present")
    if listed:
        found = re.findall(r"\"([^\"]+)\"", listed.group(1))
        check(found == KINDS, "lean list matches the six names")
    for name in THEOREM_NAMES:
        check(any(line.startswith(f"theorem {name}") for line in lines), f"theorem {name}")
        prints = [line for line in lines if line == f"#print axioms {name}"]
        check(len(prints) == 1, f"print {name}")
    for index, line in enumerate(lines, 1):
        code = line.split("--", 1)[0]
        if code.strip().startswith("#print"):
            continue
        for token in ("sorry", "admit", "axiom", "native_decide", "unsafe"):
            if re.search(rf"(?<![\w.']){token}(?![\w'])", code):
                check(False, f"forbidden {token} on line {index}")
    print(f"checked {claims} claims, failures {failures}")
    print("names", KINDS)
    print("seventh outside", SEVENTH not in KINDS)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
