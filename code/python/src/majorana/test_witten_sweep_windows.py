"""W-WITTEN.2 increments A + A2: unit tests for the windowed D-descent sweep
driver's window/ledger MACHINERY (`proof_packets/.../witten/sweep_feed.py`).

These tests are deliberately synthetic -- no PDF, no `witten_fulltext.txt`.
Both live only in the main checkout or as untracked sweep output, so a
collectable test suite must not depend on either. Instead these tests drive
`PromptDiagnosisEngine.diagnose` (the real, unmodified engine) over
hand-built "page" strings that are engineered to exercise specific descent
and ledger paths.

Run from omega_engine/research/ooutwire_docs with
PYTHONPATH="anomalon/coda;anomalon/codaq;.":

    python -m pytest anomalon/unit_test/test_witten_sweep_windows.py -q

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

_WITTEN_DIR = (
    Path(__file__).resolve().parents[2]
    / "proof_packets"
    / "fable_coda_codaq_sos_20260806"
    / "witten"
)
if str(_WITTEN_DIR) not in sys.path:
    sys.path.insert(0, str(_WITTEN_DIR))

try:
    import sweep_feed as sf
except ImportError:
    pytestmark = pytest.mark.skip(reason="sweep_feed not present")


def _neutral_page(page_num: int, n_clauses: int) -> str:
    """`n_clauses` newline-separated sentences, one clause each, with no
    "must"/"never"/"forbid"/"always"/"require"/"do not" trigger words, so
    every edge the engine builds is a plain `sequence` edge."""
    return "\n".join(
        f"Page {page_num} clause {i} records observation {page_num}{i}."
        for i in range(n_clauses)
    )


def test_descent_terminates_and_no_final_window_exceeds_budget() -> None:
    pages = [_neutral_page(p, 6) for p in range(1, 21)]
    engine = sf.PromptDiagnosisEngine()

    log = sf.sweep_windows(engine, pages)

    assert log["irreducible_saturation_count"] == 0, (
        "no page in this fixture is individually over budget; nothing "
        "should bottom out as irreducible"
    )
    assert log["accepted_window_count"] >= 2, "the whole-paper window must have split"

    covered: list[int] = []
    for leaf in log["leaves"]:
        lo, hi = leaf["page_range"]
        covered.extend(range(lo, hi + 1))
    assert covered == list(range(1, 21)), "leaves must exactly tile the page range"

    for window in log["accepted_windows"]:
        assert window["budget_status"] == "OK"
        assert window["c1_dim"] <= sf.DENSITY_BUDGET_DEFAULT
        assert window["c0_dim"] < sf.CLAUSE_CAP


def test_single_page_over_budget_alone_is_irreducible_saturation() -> None:
    page = "\n".join(f"Neutral clause number {i} on the only page." for i in range(40))
    pages = [page]
    engine = sf.PromptDiagnosisEngine()

    log = sf.sweep_windows(engine, pages)

    assert log["accepted_window_count"] == 0
    assert log["irreducible_saturation_count"] == 1
    [sat] = log["irreducible_saturations"]
    assert sat["page_range"] == [1, 1], "must not descend below page granularity"
    assert sat["reason"] == "BUDGET_EXCEEDED"
    assert sat["budget_status"] == "BUDGET_EXCEEDED"
    assert log["leaves"] == [
        {
            "kind": "saturated",
            "page_range": [1, 1],
            "reason": "BUDGET_EXCEEDED",
            "c0_dim": sat["c0_dim"],
            "c1_dim": sat["c1_dim"],
            "budget_status": "BUDGET_EXCEEDED",
        }
    ]


def test_loss_ledger_names_exact_boundary_edges() -> None:
    hot_pages = [
        "Alpha clause one.\nAlpha clause two.\nDo not skip validation.",
        "You must always verify the outcome.\nBeta clause two.",
    ]
    hot_leaves = [
        {"kind": "accepted", "page_range": [1, 1]},
        {"kind": "accepted", "page_range": [2, 2]},
    ]
    hot_ledger = sf.build_loss_ledger(hot_pages, hot_leaves)
    [hot_row] = hot_ledger["boundaries"]
    assert hot_row["boundary"] == [1, 2]
    assert hot_row["dropped_edges"] == ["sequence", "contradiction_witness"]
    assert len(hot_row["clause_pair_sha256s"]) == 2

    bland_pages = [
        "The quick brown fox jumps.\nAnother neutral clause here.",
        "A totally unrelated sentence follows.\nAnd one more after that.",
    ]
    bland_leaves = [
        {"kind": "accepted", "page_range": [1, 1]},
        {"kind": "accepted", "page_range": [2, 2]},
    ]
    bland_ledger = sf.build_loss_ledger(bland_pages, bland_leaves)
    [bland_row] = bland_ledger["boundaries"]
    assert bland_row["boundary"] == [1, 2]
    assert bland_row["dropped_edges"] == ["sequence"]

    assert sf.edge_kinds("Do not skip validation", "You must always verify") == [
        "sequence",
        "contradiction_witness",
    ]
    assert sf.edge_kinds("A neutral clause", "Another neutral clause") == ["sequence"]


def test_cap_hit_forces_descent_independent_of_budget_status() -> None:
    page = "\n".join(f"Neutral clause number {i} on a long page." for i in range(60))
    pages = [page]
    engine = sf.PromptDiagnosisEngine(density_budget=1000)

    diag = sf.diagnose_window(engine, pages, 1, 1)
    assert diag.cohomology.c0_dim == sf.CLAUSE_CAP
    assert diag.density.budget_status == "OK", (
        "budget must read OK at this elevated budget -- isolates the cap "
        "signal from the budget signal"
    )

    verdict = sf.window_verdict(diag)
    assert verdict["budget_exceeded"] is False
    assert verdict["cap_hit"] is True
    assert verdict["failed"] is True, "cap_hit alone must still fail the window"

    log = sf.sweep_windows(engine, pages)
    assert log["accepted_window_count"] == 0, "a capped single page must not be accepted"
    [sat] = log["irreducible_saturations"]
    assert sat["reason"] == "CAP_HIT"
    [cap_event] = log["cap_truncations"]
    assert cap_event["page_range"] == [1, 1]
    assert cap_event["total_clauses_uncapped"] == 60
    assert cap_event["clauses_lost_to_cap"] == 12




def test_subpage_descent_resolves_a_saturating_page_without_exceeding_budget() -> None:
    page = "\n".join(f"Neutral clause number {i} on the only page." for i in range(40))
    pages = [page]
    engine = sf.PromptDiagnosisEngine()

    page_log = sf.sweep_windows(engine, pages)
    assert page_log["irreducible_saturation_count"] == 1, (
        "sanity check: this fixture must still saturate at page granularity "
        "-- otherwise this test is not exercising A2 descent at all"
    )

    v2_log = sf.extend_with_subpage_descent(engine, pages, page_log)

    assert v2_log["irreducible_clause_saturation_count"] == 0
    assert v2_log["accepted_subpage_window_count"] == 2
    assert v2_log["pages_descended_to_subpage"] == [1]
    assert [w["clause_range"] for w in v2_log["accepted_subpage_windows"]] == [
        [0, 33],
        [33, 40],
    ]
    for window in v2_log["accepted_subpage_windows"]:
        assert window["budget_status"] == "OK"
        assert window["c1_dim"] <= sf.DENSITY_BUDGET_DEFAULT
        assert window["c0_dim"] <= sf.CLAUSE_CAP

    ledger = sf.build_loss_ledger_v2(pages, v2_log["leaves"])
    assert ledger["inter_page_boundaries"] == []
    assert len(ledger["intra_page_boundaries"]) == 1
    [row] = ledger["intra_page_boundaries"]
    assert row["page"] == 1
    assert row["boundary"] == [32, 33], (
        "boundary is [last clause index of the left window, first clause "
        "index of the right window]"
    )
    assert row["dropped_edges"] == ["sequence"]
    assert len(row["clause_pair_sha256s"]) == 2
    assert ledger["totals"]["by_boundary_type"] == {"inter_page": 0, "intra_page": 1}
    assert ledger["totals"]["boundary_count"] == 1


def test_uncapped_splitter_matches_capped_splitter_under_the_cap() -> None:
    text = "\n".join(f"Clause {i} of a short text." for i in range(40))
    uncapped = sf.split_clauses_uncapped(text)
    capped = sf._split_clauses(text)[: sf.CLAUSE_CAP]
    assert uncapped == capped
    assert len(uncapped) == 40

    long_text = "\n".join(f"Clause {i} of a long text." for i in range(60))
    uncapped_long = sf.split_clauses_uncapped(long_text)
    capped_long = sf._split_clauses(long_text)[: sf.CLAUSE_CAP]
    assert len(uncapped_long) == 60
    assert len(capped_long) == sf.CLAUSE_CAP
    assert uncapped_long[: sf.CLAUSE_CAP] == capped_long


