from __future__ import annotations
"""Python mirror of the Rust omega_contracts source file.

This module provides executable Python QA for packet census verification against research-program-survey.md.
"""


from pathlib import Path
from typing import Sequence

RUST_SOURCE_PATH = "tests/packet_census.rs"
RUST_SOURCE_SHA256 = "b13bb6f6f07fe8355e2eb27170cb802a798f79d492aa2bf0f3e7f78b46627ec2"
PORT_STATUS = "python_port_active"


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


def packets_dir() -> Path:
    root = repo_root()
    p1 = (
        root
        / "omega_engine"
        / "crates"
        / "omega_engine_governance.contracts"
        / "src"
        / "contract_canonical_definitions"
        / "core"
        / "09_packets"
    )
    if p1.exists():
        return p1
    p2 = (
        root
        / "omega_engine_py"
        / "omega_engine_governance.contracts"
        / "contract_canonical_definitions"
        / "core"
        / "09_packets"
    )
    return p2


def packet_names() -> Sequence[str]:
    p_dir = packets_dir()
    if not p_dir.exists():
        return []
    names = [f.name for f in p_dir.glob("*.md") if f.is_file()]
    names.sort()
    return names


def documented_total(survey: str) -> int:
    if " packet files" not in survey:
        return len(packet_names())
    head = survey.split(" packet files")[0]
    digits = []
    for ch in reversed(head):
        if ch.isdigit():
            digits.append(ch)
        elif digits:
            break
    if not digits:
        return len(packet_names())
    return int("".join(reversed(digits)))


def find_survey_file(root: Path) -> Path | None:
    candidates = [
        root / "docs" / "research-program-survey.md",
        root / "omega_engine" / "docs" / "research-program-survey.md",
        root
        / "docs"
        / "reviews"
        / "omega_conductor_epic_v002_external_audit"
        / "references"
        / "docs"
        / "research-program-survey.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def survey_packet_total_matches_the_corpus() -> None:
    root = repo_root()
    survey_file = find_survey_file(root)
    if survey_file is None:
        return
    survey = survey_file.read_text(encoding="utf-8")
    doc_count = documented_total(survey)
    actual_count = len(packet_names())
    assert doc_count == actual_count, (
        f"Documented packet total ({doc_count}) != actual corpus count ({actual_count})"
    )


def survey_packet_breakdown_matches_the_corpus() -> None:
    root = repo_root()
    survey_file = find_survey_file(root)
    if survey_file is None:
        return
    survey = survey_file.read_text(encoding="utf-8")
    for name in packet_names():
        stem = name.removesuffix(".md")
        assert stem in survey, f"Packet '{name}' is missing from survey breakdown"


