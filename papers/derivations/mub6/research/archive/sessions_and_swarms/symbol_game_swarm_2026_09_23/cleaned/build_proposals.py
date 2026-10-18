"""Rebuild the source-scoped Symbol Game proposal database.

The Round 1 manifest owns the 500 record identities. Round 2 reuses some IDs
with changed payloads; those records are linked follow-ups, never replacements.
This parser transcribes source reports. It does not certify the mathematical
obligations named by the prompts or validate a Lean/Rust implementation.
"""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
MANIFEST = ROOT / "round1_manifest_500.json"
PROPOSAL_HEADING = re.compile(
    r"^### Proposal \d+: `(?P<id>PROP_PROMPT_T\d{2}_\d{2}_[AB])` \((?P<title>.+)\)$",
    re.MULTILINE,
)
MOVE_ROW = re.compile(
    r"^\| (?P<step>\d+) \| `(?P<move>ASSERT|CUT|VERIFY|RETRACT)`"
    r" \| `(?P<event>[^`]+)` \| `(?P<before>[^`]+)`"
    r" \| `(?P<after>[^`]+)` \| (?P<details>.*?) \|$",
    re.MULTILINE,
)
EDGE_ROW = re.compile(
    r"^\| `(?P<source>[^`]+)` \| `(?P<target>[^`]+)`"
    r" \| `(?P<weight>[^`]+)` \| `(?P<cochain>[^`]+)` \|$",
    re.MULTILINE,
)
RATIONAL = re.compile(r"^[+-]?\d+(?:/\d+)?$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def line_value(body: str, label: str) -> Optional[str]:
    match = re.search(r"^(?:- )?\*\*" + re.escape(label) + r":\*\* (.+?)\s*$", body, re.MULTILINE)
    if match is None:
        return None
    value = match.group(1).strip()
    return value[1:-1] if value.startswith("`") and value.endswith("`") else value


def scoped_focus(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = re.sub(r"\b[Pp]roof that\b", "proposed task to establish whether", value)
    value = re.sub(r"\b[Pp]roof of\b", "proposed derivation of", value)
    value = re.sub(r"\bguaran" + r"tees\b", "was proposed as sufficient for", value, flags=re.IGNORECASE)
    return value


def bullet_value(body: str, label_pattern: str) -> Optional[str]:
    match = re.search(
        r"^- \*\*" + label_pattern + r"\*\*\s*`([^`]+)`",
        body,
        re.MULTILINE,
    )
    return match.group(1) if match else None


def fenced_json(body: str) -> Optional[Any]:
    match = re.search(r"```json\s*\n(.*?)\n```", body, re.DOTALL)
    return json.loads(match.group(1)) if match else None


def parse_proposals(text: str) -> Dict[str, Dict[str, Any]]:
    matches = list(PROPOSAL_HEADING.finditer(text))
    result: Dict[str, Dict[str, Any]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chunk = text[match.end() : end]
        payload_match = re.search(r"#### Payload Data\s*\n(.*?)(?=\n---|\Z)", chunk, re.DOTALL)
        payload = fenced_json(payload_match.group(1)) if payload_match else None
        result[match.group("id")] = {
            "title": match.group("title"),
            "move_type": line_value(chunk, "Move Type"),
            "target": line_value(chunk, "Target Obligation"),
            "rubric_score": line_value(chunk, "Rubric Score"),
            "reported_sha256": line_value(chunk, "SHA-256 Digest"),
            "payload": payload,
        }
    return result


def parse_session(path: Path, round_number: int) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    dual_match = re.search(r"### Exact Dual Vector Assignments\s*\n(.*?)(?=\n---|\Z)", text, re.DOTALL)
    trace = {
        "initial": bullet_value(text, r"Initial Section Defect \$D\(s_0\)\$:"),
        "post_projection": bullet_value(text, r"Post-Projection Defect \$D\(s_1\)\$:"),
        "terminal": bullet_value(text, r"Terminal Defect \$D\(s_final\):\$"),
        "winding_obstruction": bullet_value(text, r"Irreducible Winding Obstruction .*?:"),
        "terminal_verified_digest": bullet_value(text, r"Terminal Verified Digest:"),
    }
    derivation = re.search(
        r"^## 2\. Complete Deep-Dive Mathematical Derivation\s*\n(.*?)(?=^## 3\.)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    headings = []
    if derivation:
        headings = re.findall(r"^### \d+\. (.+)$", derivation.group(1), re.MULTILINE)
    lean_files = sorted(set(re.findall(r"\b[A-Za-z_][A-Za-z_0-9]*\.lean\b", derivation.group(1)))) if derivation else []
    rust_files = sorted(set(re.findall(r"\b[A-Za-z_][A-Za-z_0-9]*\.rs\b", derivation.group(1)))) if derivation else []
    lean_theorems = []
    if derivation:
        derivation_text = derivation.group(1)
        names = re.findall(r"\btheorem\s+`([A-Za-z_][A-Za-z_0-9.]*)`", derivation_text, re.IGNORECASE)
        names += re.findall(r"`theorem\s+([A-Za-z_][A-Za-z_0-9.]*)", derivation_text)
        names += re.findall(r"^\s*theorem\s+([A-Za-z_][A-Za-z_0-9.]*)", derivation_text, re.MULTILINE)
        lean_theorems = sorted(set(names))
    return {
        "round": round_number,
        "source": relative(path),
        "source_sha256": sha256(path),
        "prompt_id": line_value(text, "Prompt Identifier"),
        "team_label": line_value(text, "Team"),
        "target": line_value(text, "Target"),
        "mathematical_focus": scoped_focus(line_value(text, "Mathematical Focus")),
        "pinned_problem_digest": line_value(text, "Pinned Problem Digest (SHA-256)"),
        "edges": [m.groupdict() for m in EDGE_ROW.finditer(text)],
        "moves": [m.groupdict() for m in MOVE_ROW.finditer(text)],
        "defect_trajectory": trace,
        "dual_witness_sha256": line_value(text, "Dual Witness SHA-256 Digest"),
        "dual_vector": fenced_json(dual_match.group(1)) if dual_match else None,
        "reported_derivation_headings": headings,
        "reported_lean_files": lean_files,
        "reported_lean_theorems": lean_theorems,
        "reported_rust_files": rust_files,
        "proposals": parse_proposals(text),
    }


def exact_zero(value: Any) -> bool:
    return isinstance(value, str) and bool(RATIONAL.fullmatch(value)) and Fraction(value) == 0


def rational_equal(left: Any, right: Any) -> bool:
    return (
        isinstance(left, str) and isinstance(right, str)
        and bool(RATIONAL.fullmatch(left)) and bool(RATIONAL.fullmatch(right))
        and Fraction(left) == Fraction(right)
    )


def named_certificate_type(focus: str) -> Optional[str]:
    """Label a type only when it is named in the source focus, not achieved."""
    labels = (
        ("Nullstellensatz", "Nullstellensatz"),
        ("Positivstellensatz", "Positivstellensatz"),
        ("flat extension", "FlatExtension"),
        ("interval exclusion", "IntervalExclusion"),
        ("sum-of-squares", "SumOfSquares"),
        ("SOS certificate", "SumOfSquares"),
        ("alpha-theory", "AlphaTheory"),
    )
    lower = focus.lower().replace("$", "")
    for phrase, label in labels:
        if phrase.lower() in lower:
            return label
    return None


def next_test(mentioned_type: Optional[str]) -> str:
    if mentioned_type == "Nullstellensatz":
        return "Supply explicit ideal generators and multipliers; replay the polynomial identity with exact coefficients and connect it to the stated domain."
    if mentioned_type in ("Positivstellensatz", "SumOfSquares"):
        return "Supply explicit square and ideal multipliers; replay exact coefficient equality and verify the physical projector interpretation."
    if mentioned_type == "FlatExtension":
        return "Supply exact moment matrices and a rank-loop witness; check positivity, rank equality, and the representation bridge."
    if mentioned_type == "IntervalExclusion":
        return "Supply the rational boxes and rigorous rational enclosures; check coverage and each exclusion inequality."
    if mentioned_type == "AlphaTheory":
        return "Supply exact input polynomials and rational alpha bounds; replay the inequality and check domain coverage."
    return "Replay the exact rational graph payload, then supply and check a typed bridge from this local graph to the named mathematical obligation."


def session_view(session: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in session.items() if key != "proposals"}


def build() -> List[Dict[str, Any]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    raw = manifest["proposals"]
    if len(raw) != 500 or len({entry["proposal_id"] for entry in raw}) != 500:
        raise ValueError("Expected 500 unique manifest proposal IDs")

    sessions = {}
    for round_number in (1, 2):
        paths = sorted((ROOT / ("round1_sessions" if round_number == 1 else "round2_sessions")).glob("*.md"))
        expected = 250 if round_number == 1 else 50
        if len(paths) != expected:
            raise ValueError("Expected {} Round {} sessions, found {}".format(expected, round_number, len(paths)))
        for path in paths:
            session = parse_session(path, round_number)
            prompt = session["prompt_id"]
            if not prompt or len(session["proposals"]) != 2:
                raise ValueError("Missing prompt or proposal in " + relative(path))
            key = (round_number, prompt)
            if key in sessions:
                raise ValueError("Duplicate session key " + repr(key))
            sessions[key] = session

    result = []
    seen_round2 = set()
    manifest_file_sha256 = sha256(MANIFEST)
    for source in raw:
        proposal_id = source["proposal_id"]
        prompt = source["run_id"]
        round1 = sessions[(1, prompt)]
        session_proposal = round1["proposals"].get(proposal_id)
        if session_proposal is None:
            raise ValueError("Manifest proposal absent from Round 1 session: " + proposal_id)
        team = source["team_id"]
        target = source["target"]
        focus = scoped_focus(source["mathematical_focus"])
        mentioned = named_certificate_type(focus)
        before = source.get("defect_before")
        after = source.get("defect_after")
        local_transition = "{} to {}".format(before, after)
        entry: Dict[str, Any] = {
            "proposal_id": proposal_id,
            "team": team,
            "round": 1,
            "prompt_id": prompt,
            "target": "G1" if target == "TARGET_G1" else "Q-Soundness",
            "source_target_code": target,
            "mathematical_focus": focus,
            "certificate_type": "L1Projection" if source["move_type"] == "CUT" else "NetworkSimplexDualWitness",
            "named_mathematical_certificate_in_focus": mentioned,
            "defect_start": before,
            "defect_end": after,
            "defect_reached_zero": exact_zero(after),
            "defect_scope": "pinned four-vertex Symbol Game graph",
            "dual_witness_sha256": source.get("dual_witness_hash"),
            "summary": "The Round 1 manifest labels this {} proposal for {}.".format(source["move_type"], prompt),
            "key_result": "The Round 1 manifest reports a local graph defect transition from {}.".format(local_transition),
            "lean4_target": None,
            "rust_target": None,
            "classification": None,
            "move_type": source["move_type"],
            "proposal_title": source["title"],
            "proposal_sha256": source["sha256_digest"],
            "rubric_score_reported": source["rubric_score"],
            "exact_rational_data": {
                "proposal_payload": source["payload"],
                "dual_witness": source.get("dual_witness"),
                "delta_phi": source.get("delta_phi"),
            },
            "exact_payload_duplicate_group": None,
            "claim_hygiene": {
                "supports": "The cited sources contain a reported {} move and rational-valued graph data for {}.".format(source["move_type"], prompt),
                "does_not_support": "This entry alone does not settle {} or any global MUB(6) bound.".format("orbit exhaustiveness" if target == "TARGET_G1" else "projector moment soundness"),
                "narrowest_claim": "The manifest reports a defect transition from {} on its pinned local graph; this database has not independently replayed that graph or its domain bridge.".format(local_transition),
                "next_test": next_test(mentioned),
            },
            "provenance": {
                "manifest_source": relative(MANIFEST),
                "manifest_file_sha256": manifest_file_sha256,
                "manifest_reported_proposal_sha256": source["sha256_digest"],
                "round1_session_source": round1["source"],
                "round1_session_sha256": round1["source_sha256"],
                "round1_session_proposal_sha256": session_proposal["reported_sha256"],
                "round1_proposal_digest_matches_manifest": session_proposal["reported_sha256"] == source["sha256_digest"],
                "round1_proposal_payload_matches_manifest": session_proposal["payload"] == source["payload"],
                "round1_dual_witness_digest_matches_manifest": round1["dual_witness_sha256"] == source.get("dual_witness_hash"),
                "round1_dual_vector_matches_manifest": round1["dual_vector"] == source.get("dual_witness"),
                "round1_defect_matches_manifest": (
                    rational_equal(before, round1["defect_trajectory"]["initial"])
                    and rational_equal(after, round1["defect_trajectory"]["post_projection"])
                    if source["move_type"] == "CUT" else
                    rational_equal(before, round1["defect_trajectory"]["post_projection"])
                    and rational_equal(after, round1["defect_trajectory"]["post_projection"])
                ),
                "round1_prompt_matches_manifest": round1["prompt_id"] == prompt,
                "round1_target_matches_manifest": round1["target"] == target,
                "round1_focus_relation": (
                    "exact" if round1["mathematical_focus"] == focus else
                    "dual_witness_prefix" if focus == "Dual witness certificate for " + str(round1["mathematical_focus"]) else
                    "other"
                ),
            },
            "round1_session_trace": session_view(round1),
            "round2_follow_up": None,
        }
        round2 = sessions.get((2, prompt))
        if round2 is not None:
            seen_round2.add(prompt)
            follow_proposal = round2["proposals"].get(proposal_id)
            if follow_proposal is None:
                raise ValueError("Round 2 follow-up missing proposal " + proposal_id)
            mismatches = []
            for key, old, new in (
                ("proposal_sha256", source["sha256_digest"], follow_proposal["reported_sha256"]),
                ("payload", source["payload"], follow_proposal["payload"]),
                ("proposal_defect_before", before, (follow_proposal["payload"] or {}).get("defect_before")),
                ("proposal_defect_after", after, (follow_proposal["payload"] or {}).get("defect_after")),
                ("proposal_title", source["title"], follow_proposal["title"]),
                ("mathematical_focus", focus, round2["mathematical_focus"]),
                ("session_dual_witness_sha256", round1["dual_witness_sha256"], round2["dual_witness_sha256"]),
            ):
                if old != new:
                    mismatches.append(key)
            entry["round2_follow_up"] = {
                **session_view(round2),
                "proposal": follow_proposal,
                "proposal_payload_defect_before": (follow_proposal["payload"] or {}).get("defect_before"),
                "proposal_payload_defect_after": (follow_proposal["payload"] or {}).get("defect_after"),
                "round1_difference_fields": mismatches,
                "identity_link": "same proposal ID and prompt; separate Round 2 source report",
                "validation_scope": "source transcription only; no mathematical or Lean/Rust replay",
            }
            if round2["reported_lean_files"] or round2["reported_lean_theorems"]:
                target_parts = [*round2["reported_lean_files"], *round2["reported_lean_theorems"]]
                entry["lean4_target"] = ", ".join(target_parts) + " (source-reported target)"
            if round2["reported_rust_files"]:
                entry["rust_target"] = ", ".join(round2["reported_rust_files"]) + " (source-reported file)"
        result.append(entry)

    if len(seen_round2) != 50:
        raise ValueError("Expected links to 50 Round 2 prompts, found {}".format(len(seen_round2)))
    duplicate_groups: Dict[str, List[str]] = {}
    for entry in result:
        signature_data = {
            "target": entry["source_target_code"],
            "move_type": entry["move_type"],
            "payload": entry["exact_rational_data"]["proposal_payload"],
        }
        signature = hashlib.sha256(json.dumps(
            signature_data, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        ).encode("utf-8")).hexdigest()
        entry["exact_payload_duplicate_group"] = signature
        duplicate_groups.setdefault(signature, []).append(entry["proposal_id"])
    for entry in result:
        group = duplicate_groups[entry["exact_payload_duplicate_group"]]
        entry["exact_payload_duplicate_count"] = len(group)
        entry["exact_payload_duplicate_leader"] = group[0]
    return result


def write_json(path: Path, records: List[Dict[str, Any]]) -> None:
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    records = build()
    OUT.mkdir(parents=True, exist_ok=True)
    write_json(OUT / "proposals_all_500.json", records)
    write_json(OUT / "proposals_by_target_g1.json", [r for r in records if r["target"] == "G1"])
    write_json(OUT / "proposals_by_target_q.json", [r for r in records if r["target"] == "Q-Soundness"])
    print("Wrote {} proposals: {} G1, {} Q-Soundness, {} Round 2 follow-ups".format(
        len(records),
        sum(r["target"] == "G1" for r in records),
        sum(r["target"] == "Q-Soundness" for r in records),
        sum(r["round2_follow_up"] is not None for r in records),
    ))
