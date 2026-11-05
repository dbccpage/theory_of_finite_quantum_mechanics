"""Finite checks for WDP Paper 000."""

from __future__ import annotations

from pathlib import Path
import re

PAPER_DIR = Path(__file__).resolve().parents[1]
# These independent checks retain their historical ledger, not a current claim status.
LEDGER_PATH = PAPER_DIR / "code/fixtures/historical_claim_ledger.md"
TOY_STATUSES = ("definition", "proved", "negative boundary", "withdrawn")
CHECKED_IDS = (
    "WDP-P000-004",
    "WDP-P000-005",
    "WDP-P000-007",
    "WDP-P000-009",
    "WDP-P000-010",
)


class FactorError(ValueError):
    """A collapsed view was asked to answer two different values."""


def quotient_factor(report: dict[str, str], answer: dict[str, str]) -> dict[str, str] | None:
    """Return the descended answer, or None when the report fibers disagree."""
    descended: dict[str, str] = {}
    for point, image in report.items():
        value = answer[point]
        if image in descended and descended[image] != value:
            return None
        descended[image] = value
    return descended


def history_auditor(view: dict[str, str], state: dict[str, str]) -> dict[str, str] | None:
    """Return an auditor on the view, or None when the view is insufficient."""
    return quotient_factor(view, state)


def apply_act(has_form: bool, has_inst: bool, act: str) -> tuple[bool, bool]:
    if act == "datum":
        return (has_form, has_inst)
    if act == "form":
        return (True, has_inst)
    if act == "inst":
        if has_form:
            return (has_form, True)
        return (has_form, has_inst)
    raise ValueError(act)


def separates(has_form: bool, has_inst: bool) -> bool:
    return has_form and has_inst


def single_admission_report() -> dict[str, bool]:
    return {act: separates(*apply_act(False, False, act)) for act in ("datum", "form", "inst")}


def form_then_instance() -> bool:
    formed = apply_act(False, False, "form")
    instanced = apply_act(*formed, "inst")
    return separates(*instanced)


def max_pair_rounds(n: int) -> int:
    if n < 0:
        raise ValueError(n)
    return n * (n - 1) // 2


def monotone_pair_rounds(n: int) -> int:
    """Each positive unresolved count drops by one and then stays at zero."""
    unresolved = max_pair_rounds(n)
    steps = 0
    while unresolved:
        unresolved -= 1
        steps += 1
    return steps


def endpoint_distinct(left: str, right: str, reflexive_witness: bool) -> bool:
    if reflexive_witness:
        raise FactorError("irreflexive relation cannot hold at one point")
    return left != right


def ledger_rows(ledger_text: str | None = None) -> tuple[tuple[str, str], ...]:
    source = LEDGER_PATH.read_text(encoding="utf-8") if ledger_text is None else ledger_text
    rows = []
    for line in source.splitlines():
        match = re.match(r"^\|\s*(WDP-P000-\d+)\s*\|\s*([^|]+?)\s*\|", line)
        if match:
            rows.append((match.group(1), match.group(2).strip()))
    return tuple(rows)


def ledger_status_report() -> dict[str, object]:
    """Describe the source ledger. Local checks do not reclassify its rows."""
    rows = ledger_rows()
    ids = tuple(row_id for row_id, _ in rows)
    statuses = tuple(status for _, status in rows)
    return {
        "count": len(rows),
        "ids": ids,
        "ids_unique": len(set(ids)) == len(ids),
        "statuses_nonempty": all(status != "" for status in statuses),
        "checked_ids_present": all(claim_id in ids for claim_id in CHECKED_IDS),
        "toy_status_closure": all(status in TOY_STATUSES for status in statuses) and len(rows) == 12,
        "checked_ids": CHECKED_IDS,
    }


def run_reproduction() -> dict[str, object]:
    collapsed = quotient_factor({"x": "q", "y": "q"}, {"x": "yes", "y": "no"})
    separated = quotient_factor({"x": "qx", "y": "qy"}, {"x": "yes", "y": "no"})
    history = history_auditor({"h1": "v", "h2": "v"}, {"h1": "s1", "h2": "s2"})
    sufficient = history_auditor({"h1": "v1", "h2": "v2"}, {"h1": "s1", "h2": "s2"})
    singles = single_admission_report()
    rounds = {n: monotone_pair_rounds(n) for n in (0, 1, 2, 3, 4)}
    ledger = ledger_status_report()
    ok = all(
        (
            collapsed is None,
            separated == {"qx": "yes", "qy": "no"},
            history is None,
            sufficient == {"v1": "s1", "v2": "s2"},
            singles == {"datum": False, "form": False, "inst": False},
            form_then_instance() is True,
            rounds[0] == 0 and rounds[1] == 0 and rounds[2] == 1 and rounds[3] == 3 and rounds[4] == 6,
            endpoint_distinct("a", "b", False) is True,
            ledger["ids_unique"] is True,
            ledger["statuses_nonempty"] is True,
            ledger["checked_ids_present"] is True,
            ledger["toy_status_closure"] is False,
        )
    )
    return {
        "ok": ok,
        "collapsed_quotient": collapsed,
        "separated_quotient": separated,
        "insufficient_history": history,
        "sufficient_history": sufficient,
        "single_admission": singles,
        "form_then_instance": form_then_instance(),
        "pair_rounds": {str(n): steps for n, steps in rounds.items()},
        "endpoints_distinct": endpoint_distinct("a", "b", False),
        "checked_ids": list(CHECKED_IDS),
    }
