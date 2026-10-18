from __future__ import annotations
"""C2S1-003: minimal template loads with zero findings; mutation fails."""


from pathlib import Path


from omega_engine_governance.contracts.c2s1_template_validate import (
    load_yaml,
    validate_minimal_template,
    validate_path,
)

_REPO = Path(__file__).resolve().parents[5]

def _resolve_file(filename: str, default_path: Path) -> Path:
    if default_path.exists():
        return default_path
    cur = Path(__file__).resolve().parent
    for _ in range(10):
        matches = list(cur.glob(f"**/{filename}"))
        if matches:
            return matches[0]
        if cur.parent == cur:
            break
        cur = cur.parent
    return default_path

TEMPLATE = _resolve_file(
    "minimal_module.contract.yaml",
    _REPO
    / "omega_engine"
    / "research"
    / "product_planning_office"
    / "sprints"
    / "sprint-oe-contract-002-s1"
    / "evidence"
    / "templates"
    / "minimal_module.contract.yaml",
)
CHECKLIST = TEMPLATE.parent / "anti_theater_checklist.md"

CHECKLIST_IDS = [
    "CL-AT-001",
    "CL-AT-002",
    "CL-AT-003",
    "CL-AT-004",
    "CL-AT-009",
    "CL-AT-011",
]


def test_template_path_exists() -> None:
    assert TEMPLATE.is_file(), TEMPLATE


def test_template_zero_findings() -> None:
    findings = validate_path(TEMPLATE)
    assert findings == [], findings


def test_mutation_missing_authority_fails() -> None:
    data = load_yaml(TEMPLATE)
    del data["descriptor"]["authority_effect"]
    findings = validate_minimal_template(data)
    assert any("authority_effect" in f for f in findings)


def test_checklist_ids_present() -> None:
    text = CHECKLIST.read_text(encoding="utf-8")
    for cid in CHECKLIST_IDS:
        assert cid in text, cid


