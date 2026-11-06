"""Replay the small Symbol Game graph arithmetic with exact fractions.

This checks only the four-vertex graph data printed in the session files. It
does not check the Hadamard or projector obligations named by those files.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EDGE = re.compile(
    r"^\| `([^`]+)` \| `([^`]+)` \| `([0-9/-]+)` \| `([0-9/-]+)` \|$",
    re.MULTILINE,
)
VECTOR = re.compile(r"### Exact Dual Vector Assignments\s*```json\s*(\{.*?\})\s*```", re.S)
PROPOSAL_A = re.compile(r"### Proposal 1:.*?#### Payload Data\s*```json\s*(\{.*?\})\s*```", re.S)
TRACE_CUT = re.compile(r"\| [0-9]+ \| `CUT` \|[^\n]*?\| `([0-9/]+)` \| `([0-9/]+)` \|")
POST_DEFECT = re.compile(r"Post-Projection Defect.*?:\*\* `([0-9/]+)`")
INITIAL_DEFECT = re.compile(r"Initial Section Defect.*?:\*\* `([0-9/]+)`")
VERIFY_MUTATION = re.compile(r"\| [0-9]+ \| `VERIFY` \|[^\n]*\| `1/4` \| `0` \|")


def audit(path: Path) -> dict:
    source = path.read_text(encoding="utf-8")
    edges = [(u, v, Fraction(w), Fraction(c)) for u, v, w, c in EDGE.findall(source)]
    match = VECTOR.search(source)
    post = POST_DEFECT.search(source)
    initial = INITIAL_DEFECT.search(source)
    proposal = PROPOSAL_A.search(source)
    trace_cut = TRACE_CUT.search(source)
    if len(edges) != 4 or match is None or post is None or initial is None or proposal is None or trace_cut is None:
        raise ValueError(f"Missing graph data: {path}")
    witness = {key: Fraction(value) for key, value in json.loads(match.group(1)).items()}
    proposal_payload = json.loads(proposal.group(1))
    divergence = Counter()
    bounded = True
    dual_value = Fraction(0)
    initial_l1 = Fraction(0)
    for u, v, weight, cochain in edges:
        key = f"{u}->{v}"
        z = witness[key]
        divergence[u] -= z
        divergence[v] += z
        bounded &= abs(z) <= weight
        dual_value += z * cochain
        initial_l1 += weight * abs(cochain)
    cycle_sum = sum((e[3] for e in edges), Fraction(0))
    section = proposal_payload.get("proposed_section")
    section_l1 = None
    if section is not None:
        section_l1 = sum(
            (weight * abs(cochain - (Fraction(section[v]) - Fraction(section[u])))
             for u, v, weight, cochain in edges),
            Fraction(0),
        )
    return {
        "source": path.relative_to(ROOT).as_posix(),
        "round": 1 if path.parent.name == "round1_sessions" else 2,
        "initial_l1_from_edges": str(initial_l1),
        "cycle_sum": str(cycle_sum),
        "printed_initial_matches_edges": Fraction(initial.group(1)) == initial_l1,
        "printed_post_matches_cycle_lower_bound": Fraction(post.group(1)) == abs(cycle_sum),
        "cut_section_l1": str(section_l1) if section_l1 is not None else None,
        "cut_section_matches_post": section_l1 == Fraction(post.group(1)) if section_l1 is not None else None,
        "proposal_cut_after_matches_trace": Fraction(proposal_payload["defect_after"]) == Fraction(trace_cut.group(2)),
        "dual_value_matches_cycle_lower_bound": dual_value == abs(cycle_sum),
        "verify_changes_defect_without_cut": bool(VERIFY_MUTATION.search(source)),
        "dual_value": str(dual_value),
        "dual_bounded": bounded,
        "dual_divergence_zero": all(value == 0 for value in divergence.values()),
        "dual_divergence": {vertex: str(value) for vertex, value in divergence.items()},
    }


def main() -> None:
    rows = [
        audit(path)
        for folder in ("round1_sessions", "round2_sessions")
        for path in sorted((ROOT / folder).glob("*.md"))
    ]
    print(json.dumps({
        "scope": "printed four-edge graphs only",
        "sessions": len(rows),
        "by_round": {
            str(round_id): {
                "sessions": sum(row["round"] == round_id for row in rows),
                "zero_cycle_sum": sum(
                    row["round"] == round_id and Fraction(row["cycle_sum"]) == 0
                    for row in rows
                ),
                "initial_matches_edges": sum(
                    row["round"] == round_id and row["printed_initial_matches_edges"]
                    for row in rows
                ),
                "dual_matches_cycle_lower_bound": sum(
                    row["round"] == round_id and row["dual_value_matches_cycle_lower_bound"]
                    for row in rows
                ),
                "nonzero_divergence": sum(
                    row["round"] == round_id and not row["dual_divergence_zero"]
                    for row in rows
                ),
                "out_of_bound": sum(
                    row["round"] == round_id and not row["dual_bounded"]
                    for row in rows
                ),
                "post_above_cycle_lower_bound": sum(
                    row["round"] == round_id and not row["printed_post_matches_cycle_lower_bound"]
                    for row in rows
                ),
                "cut_sections_checked": sum(
                    row["round"] == round_id and row["cut_section_matches_post"] is not None
                    for row in rows
                ),
                "cut_section_mismatches": sum(
                    row["round"] == round_id and row["cut_section_matches_post"] is False
                    for row in rows
                ),
                "proposal_cut_trace_mismatches": sum(
                    row["round"] == round_id and not row["proposal_cut_after_matches_trace"]
                    for row in rows
                ),
                "verify_changes_defect_without_cut": sum(
                    row["round"] == round_id and row["verify_changes_defect_without_cut"]
                    for row in rows
                ),
            }
            for round_id in (1, 2)
        },
        "example_nonzero_divergence": next(
            (row for row in rows if not row["dual_divergence_zero"]), None
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
