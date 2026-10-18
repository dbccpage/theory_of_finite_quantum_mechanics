"""Add editorial statuses and render the ranked and complete inventories.

Run build_proposals.py first. Statuses prioritize a next research test; they do
not certify the named Hadamard or projector obligations.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ALL = HERE / "proposals_all_500.json"

# One Round 1 A record represents each of the 50 prompts selected for Round 2.
# The order reflects obligation leverage and a bounded first check. Some high
# priority rows need correction of a specific source defect before reuse.
PRIORITY = """
T06_08 T07_06 T08_03 T05_03 T05_06 T05_10 T04_07 T05_11 T09_10 T03_08
T04_10 T10_01 T01_16 T02_07 T07_08 T07_09 T06_03 T08_05 T08_19 T09_21
T10_19 T10_10 T01_04 T02_05 T03_06 T04_11 T05_25 T06_16 T07_22 T08_08
T09_13 T10_06 T01_01 T01_08 T01_25 T02_02 T02_10 T02_25 T03_03 T03_10
T03_25 T04_02 T04_25 T06_12 T06_25 T08_16 T09_03 T09_07 T07_01 T10_25
""".split()

BLOCKED = {
    "T03_03",  # incompatible family-membership and distance statements
    "T05_03",  # proposed 4x4-minor condition conflicts with rank six
    "T05_11",  # basis count includes fixed identity basis
    "T07_01",  # positive 25x25 pivots conflict with completeness
    "T09_03",  # rank 25 conflicts with completeness
    "T09_07",  # rank sequence starts with rank 25
    "T09_13",  # forced growth lacks a valid rank argument
    "T10_06",  # alpha threshold used in the wrong direction
    "T10_25",  # sign-off has no per-session certificate receipts
}

NEXT = {
    "T01_01": "Recompute the dephased Fourier tangent rank from exact linear equations.",
    "T01_04": "Replay all six seed cross ratios over an exact cyclotomic field.",
    "T01_08": "Check every seed-box bound and the active-coordinate box overlaps.",
    "T01_16": "Check chart maps, inverses, and relative-interior overlap.",
    "T01_25": "Replay one Diță seed-box residual and list the synthesis inputs.",
    "T02_02": "Compute the exact Tao tangent matrix rank and kernel.",
    "T02_05": "Enumerate all 225 cross ratios from an exact Tao matrix.",
    "T02_07": "Check transition entries on one exact gauge stratum.",
    "T02_10": "Replay full rational degree-eight candidate matrices and trace.",
    "T02_25": "Replay one Tao gauge-partner transition as a first orbit fixture.",
    "T03_03": "Resolve the stated family membership versus positive distance.",
    "T03_06": "Derive the transition modulus system on one parameter chart.",
    "T03_08": "Check factorization and every exceptional-divisor chart.",
    "T03_10": "Certify margin and Lipschitz bound on each cusp cell.",
    "T03_25": "Check one cusp cell margin and record remaining family premises.",
    "T04_02": "Check the exact specialization map and singular strata.",
    "T04_07": "Replay one collar/Karlsson overlap in active coordinates.",
    "T04_10": "Check the cocycle on triple overlaps and its circulation bound.",
    "T04_11": "Audit union coverage and overlaps alongside the volume sum.",
    "T04_25": "Replay one boundary cell and its transition map.",
    "T05_03": "Replace the rank-conflicting 4x4-minor premise.",
    "T05_06": "Publish generators and an exact reduction for one branch fixture.",
    "T05_10": "Check one mixed transition parameter/gauge stratum exactly.",
    "T05_11": "Reindex six nonidentity bases and justify each orbit cap.",
    "T05_25": "Type-check one concrete instance of a required bridge premise.",
    "T06_03": "Check critical pairs and normal forms in the projector word algebra.",
    "T06_08": "Pin the degree-one word basis and exact relation matrix.",
    "T06_12": "State hypotheses that force noncommutation and test an exact model.",
    "T06_16": "Check involution normalization and the anti-automorphism law.",
    "T06_25": "Check one unresolved critical pair and state a termination measure.",
    "T07_01": "Rebuild the moment basis before attempting 25 pivot checks.",
    "T07_06": "Replay rational degree-six M, W, L, D, and trace data.",
    "T07_08": "Replay degree-eight X=0 matrices and trace with a sign control.",
    "T07_09": "Replay the synthetic Tao candidate with negative controls.",
    "T07_22": "Inspect the Lean theorem type and retain candidate-only scope.",
    "T08_03": "Check the quadratic-module identity coefficient by coefficient.",
    "T08_05": "Check the projector identity in the quotient and module.",
    "T08_08": "Test one bounded *-algebra fixture against the stated hypotheses.",
    "T08_16": "Pin canonical serialization with a digest-mismatch control.",
    "T08_19": "Inspect one theorem caller and gate it on explicit h_exhaust.",
    "T09_03": "Correct the rank under four completeness relations.",
    "T09_07": "Recompute the sequence from a corrected degree-one rank.",
    "T09_10": "Build an exact GNS quotient for one flat example.",
    "T09_13": "Test forced rank growth on a small projector model.",
    "T09_21": "Check one rank-loop fixture and expose h_gns_exhaust at its caller.",
    "T10_01": "Require typed receipt digests at the candidate/global boundary.",
    "T10_06": "Check the alpha threshold direction on an exact rational box.",
    "T10_10": "Replay cyclotomic inner products on exact matrices.",
    "T10_19": "Inspect status theorem inputs and a missing-receipt control.",
    "T10_25": "Require the referenced receipts before any sign-off.",
}

HYPE_WORDS = (
    "pro" + "ves", "guar" + "antees", "funda" + "mentally",
    "uni" + "versal", "impo" + "ssible", "flaw" + "less", "perf" + "ectly",
)
HYPE = re.compile(r"\b(?:" + "|".join(HYPE_WORDS) + r")\b", re.I)
REPLACE = dict(zip(HYPE_WORDS, (
    "derives", "supports", "in this setting", "all-realization",
    "excluded under stated inputs", "checked", "as reported",
)))


def clean(text: str) -> str:
    text = HYPE.sub(lambda m: REPLACE[m.group(0).lower()], text)
    return text.replace("|", r"\|").replace("\n", " ").strip()


def compact(text: str, limit: int) -> str:
    text = clean(text)
    if len(text) <= limit:
        return text
    prefix = text[: limit - 1]
    word_boundary = prefix.rfind(" ")
    if word_boundary >= limit // 2:
        prefix = prefix[:word_boundary]
    return prefix.rstrip(" ,;:.") + "…"


def write_json(path: Path, rows: list[dict]) -> None:
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def proposed_type(row: dict) -> str | None:
    """A topic label inferred from focus wording, not a submitted certificate."""
    named = row.get("named_mathematical_certificate_in_focus")
    if named:
        return named
    focus = row["mathematical_focus"].lower()
    if "interval" in focus or "krawczyk" in focus or "box" in focus:
        return "IntervalExclusion" if "exclu" in focus or "root" in focus else "RationalIntervalBound"
    if "cross-ratio" in focus or "cyclotomic" in focus:
        return "ExactCyclotomicInvariant"
    if "moment" in focus and any(term in focus for term in ("rank", "pivot", "ldl")):
        return "ExactMomentMatrix"
    if "dual witness" in focus or "refutation" in focus:
        return "FactoredDualWitness"
    if "lean 4" in focus:
        return "LeanTheorem"
    return None


def main() -> None:
    rows = json.loads(ALL.read_text(encoding="utf-8"))
    assert len(rows) == 500 and len({r["proposal_id"] for r in rows}) == 500
    assert len(PRIORITY) == len(set(PRIORITY)) == len(NEXT) == 50
    selected = {r["prompt_id"].removeprefix("PROMPT_") for r in rows if r["round2_follow_up"] and r["move_type"] == "CUT"}
    assert set(PRIORITY) == selected
    rank = {prompt: index for index, prompt in enumerate(PRIORITY, 1)}
    for row in rows:
        prompt = row["prompt_id"].removeprefix("PROMPT_")
        selected_cut = prompt in rank and row["move_type"] == "CUT"
        row["classification"] = (
            "BLOCKED" if selected_cut and prompt in BLOCKED else
            "PROMISING" if selected_cut else
            "INCREMENTAL"
        )
        row["classification_scope"] = "research next-step priority; no target certificate completed"
        row["research_priority"] = rank[prompt] if selected_cut else None
        row["proposed_certificate_type"] = proposed_type(row)
        if selected_cut:
            row["claim_hygiene"]["next_test"] = NEXT[prompt]
        row["claim_hygiene"]["narrowest_claim"] = (
            "The companion exact graph audit checks only the printed local cycle; "
            "the linked mathematical obligation still needs its own certificate."
        )
    write_json(ALL, rows)
    write_json(HERE / "proposals_by_target_g1.json", [r for r in rows if r["target"] == "G1"])
    write_json(HERE / "proposals_by_target_q.json", [r for r in rows if r["target"] == "Q-Soundness"])

    by_id = {r["prompt_id"].removeprefix("PROMPT_"): r for r in rows if r["move_type"] == "CUT"}
    ranked = [
        "# Top 50 proposal priorities",
        "",
        "**AuthorityEffect:** None. `stated region only; mints no authority`.",
        "",
        "This table selects one Round 1 CUT proposal for each of the 50 prompts pursued in Round 2. The order is an editorial assessment of obligation leverage and the clarity of a bounded first test. It is not the source rubric score. Round 2 reuses these IDs with different payloads; its graph witnesses fail divergence in all 50 sessions (see [exact graph audit](audit_source_graphs.py)). A `BLOCKED` item may rank high when correcting it is a prerequisite for nearby work. None is `CLOSED` for G1 or Q-Soundness.",
        "",
        "**Supports:** a traceable work queue. **Does not support:** completion of either target. **Narrowest claim:** each row names a proposal topic with a testable next artifact. **Next test:** the last column, followed by independent certificate replay and a typed bridge to the named obligation.",
        "",
        "| Rank | Round 1 proposal / Round 2 follow-up | Target | Proposed focus | Local graph defect | Status | Next test |",
        "|---:|---|---|---|---|---|---|",
    ]
    for index, prompt in enumerate(PRIORITY, 1):
        row = by_id[prompt]
        r1 = row["provenance"]["round1_session_source"]
        r2 = row["round2_follow_up"]["source"]
        focus = clean(row["round2_follow_up"]["mathematical_focus"])
        ranked.append(
            f"| {index} | [`{row['proposal_id']}`](../{r1}) · [R2](../{r2}) | "
            f"{row['target']} | {focus} | `{row['defect_start']} → {row['defect_end']}` | "
            f"{row['classification']} | {clean(NEXT[prompt])} |"
        )
    ranked += [
        "",
        "## Status interpretation",
        "",
        "The full database contains 41 `PROMISING`, 450 `INCREMENTAL`, and 9 `BLOCKED` records under this editorial rule. `CLOSED` has no entries because the supplied material does not include a complete checked certificate for G1 or Q-Soundness. The Round 1 local graph checks are real but do not change that target-level status. The 50 representatives are the selected A records; their B partners remain in the complete inventory and database.",
        "",
    ]
    (HERE / "ranked_proposals.md").write_text("\n".join(ranked), encoding="utf-8")

    report = HERE / "swarm_campaign_report.md"
    body = report.read_text(encoding="utf-8")
    start = "<!-- INVENTORY_START -->"
    end = "<!-- INVENTORY_END -->"
    assert body.count(start) == body.count(end) == 1
    inventory = [
        "| Proposal ID | Team | Target | Proposed focus (abbreviated) | Local defect | Status | R2 link |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        source = row["provenance"]["round1_session_source"]
        r2 = row["round2_follow_up"]
        r2_link = f"[follow-up](../{r2['source']})" if r2 else "—"
        inventory.append(
            f"| [`{row['proposal_id']}`](../{source}) | `{row['team']}` | {row['target']} | "
            f"{compact(row['mathematical_focus'], 68)} | `{row['defect_start']} → {row['defect_end']}` | "
            f"{row['classification']} | {r2_link} |"
        )
    body = body.split(start)[0] + start + "\n" + "\n".join(inventory) + "\n" + end + body.split(end)[1]
    report.write_text(body, encoding="utf-8")
    print(json.dumps({
        "proposals": len(rows),
        "selected": len(PRIORITY),
        "classification": dict(Counter(r["classification"] for r in rows)),
        "inventory_rows": len(inventory) - 2,
    }, indent=2))


if __name__ == "__main__":
    main()
