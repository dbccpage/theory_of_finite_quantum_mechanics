"""Five-field observer-draft classifier for one Bell label.

Recomputes the finite cases of the narrowed statement. No repository imports.
AuthorityEffect: None.
"""

from __future__ import annotations

FIELDS = ("kernel", "admissibility", "norm", "terminal", "layer")

BELL_KERNEL = (
    "support presheaf over the maximal-context cover "
    "{0,2}|{0,3}|{1,2}|{1,3} with arities 2,2,2,2"
)
ACCEPTED_ADMISSIBILITY = "noncontextual polytope conv(A)"
ACCEPTED_NORM = "L1"
ACCEPTED_TERMINAL = (
    "defect = 0 -> ExactRepair; defect > 0 and a support-level global section "
    "exists -> ClosedResidual; defect > 0 and none exists -> OpenObstruction"
)
ACCEPTED_LAYER = "WDP-CH10-D01 diagnostic"
AUTHORITY_NONE = "None"

ACCEPTED = {
    "kernel": BELL_KERNEL,
    "admissibility": ACCEPTED_ADMISSIBILITY,
    "norm": ACCEPTED_NORM,
    "terminal": ACCEPTED_TERMINAL,
    "layer": ACCEPTED_LAYER,
}

BLANKS = (None, "", " ")
MISMATCHES = {
    "kernel": ("other-kernel", "  "),
    "admissibility": ("other-admissibility", "  "),
    "norm": ("L", "  "),
    "terminal": ("other-terminal", "  "),
    "layer": ("other-layer", "  "),
}


def classify(draft: dict[str, str | None]) -> tuple[str, ...]:
    for field in FIELDS:
        value = draft[field]
        if value is None or value == "" or value == " ":
            return ("undeclared", field)
        if value != ACCEPTED[field]:
            return ("unsupported", field, value)
    return ("accepted",)


def authority_of(kind: tuple[str, ...]) -> str | None:
    if kind == ("accepted",):
        return AUTHORITY_NONE
    return None


def main() -> int:
    failures: list[str] = []
    accepted = dict(ACCEPTED)
    got = classify(accepted)
    if got != ("accepted",):
        failures.append(f"accepted draft -> {got}")
    if authority_of(got) != AUTHORITY_NONE:
        failures.append(f"authority -> {authority_of(got)}")
    for field in FIELDS:
        for blank in BLANKS:
            draft = dict(accepted)
            draft[field] = blank
            got = classify(draft)
            if got != ("undeclared", field):
                failures.append(f"blank {field} {blank!r} -> {got}")
        for text in MISMATCHES[field]:
            if text in BLANKS or text == ACCEPTED[field]:
                failures.append(f"witness collided {field} {text!r}")
                continue
            draft = dict(accepted)
            draft[field] = text
            got = classify(draft)
            if got != ("unsupported", field, text):
                failures.append(f"mismatch {field} {text!r} -> {got}")
    print("bell_label=" + BELL_KERNEL)
    print("admissibility=" + ACCEPTED_ADMISSIBILITY)
    print("norm=" + ACCEPTED_NORM)
    print("terminal=" + ACCEPTED_TERMINAL)
    print("layer=" + ACCEPTED_LAYER)
    print("authority=" + AUTHORITY_NONE)
    print(f"blank_cases={len(FIELDS) * len(BLANKS)}")
    print(f"mismatch_cases={sum(len(v) for v in MISMATCHES.values())}")
    print(f"failures={len(failures)}")
    for item in failures:
        print(item)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
