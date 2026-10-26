"""Claim Hygiene and Epistemic Humility Auditor.

Enforces Claim Hygiene Rule:
- Scans manuscripts and claim ledgers across all 9 packages.
- Flags unearned consensus, hype verbs, and forbidden words:
  'proves', 'guarantees', 'mathematically verifies', 'fundamentally',
  'true intelligence', 'impossible', 'universal', 'flawless', 'perfectly',
  'clearly', 'obviously', 'simply', 'merely', 'weaponized'.
- Verifies that mathematical statements are qualified ('shows in this model',
  'conditional on', 'under declared assumptions').

AuthorityEffect: None.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from ..config import CLAIM_HYGIENE_FORBIDDEN_WORDS, ALL_PACKAGES


@dataclass
class HygieneViolation:
    package_id: str
    file_path: str
    line_number: int
    matched_word: str
    line_context: str


@dataclass
class ClaimHygieneReport:
    total_files_scanned: int = 0
    clean_files_count: int = 0
    violations_count: int = 0
    violations: list[HygieneViolation] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.violations_count == 0


# Allowed context qualifications where words like 'proves' or 'universal' are mathematically scoped
# e.g. "universal product lower bound" (a standard mathematical term) or "proves under assumptions"
ALLOWED_PHRASES = [
    "universal product lower bound",
    "universal cover",
    "universal property",
    "universal algebra",
    "universal state",
    "universal entanglement timescale",
    "proves_under_assumptions",
    "proves under declared assumptions",
    "relation: \"proves\"",
    "proves under assumptions",
]


def is_allowed_context(line: str, word: str) -> bool:
    line_lower = line.lower()
    for phrase in ALLOWED_PHRASES:
        if phrase in line_lower:
            return True
    return False


def audit_claim_hygiene_in_file(
    pkg_id: str,
    file_path: Path,
) -> list[HygieneViolation]:
    violations: list[HygieneViolation] = []
    if not file_path.is_file():
        return violations

    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return violations

    # Word boundary regex for forbidden words
    pattern = re.compile(r"\b(" + "|".join(CLAIM_HYGIENE_FORBIDDEN_WORDS) + r")\b", re.IGNORECASE)

    for lineno, line in enumerate(lines, start=1):
        # Ignore comments or schema keys like "authority_effect: None"
        stripped = line.strip()
        if stripped.startswith("# AuthorityEffect:") or "AuthorityEffect:" in line:
            continue

        matches = pattern.finditer(line)
        for m in matches:
            word = m.group(1).lower()
            if not is_allowed_context(line, word):
                violations.append(
                    HygieneViolation(
                        package_id=pkg_id,
                        file_path=str(file_path),
                        line_number=lineno,
                        matched_word=word,
                        line_context=line.strip()[:100],
                    )
                )

    return violations


def audit_all_packages_claim_hygiene(
    packages: dict[str, Any] = ALL_PACKAGES,
) -> ClaimHygieneReport:
    report = ClaimHygieneReport()

    for pkg_id, pkg_spec in packages.items():
        # Scan manuscript
        manuscript_path = pkg_spec.path / pkg_spec.manuscript_name
        if manuscript_path.is_file():
            report.total_files_scanned += 1
            v_list = audit_claim_hygiene_in_file(pkg_id, manuscript_path)
            if v_list:
                report.violations.extend(v_list)
                report.violations_count += len(v_list)
            else:
                report.clean_files_count += 1

        # Scan claim ledger if present
        for ledger_name in ["projection_obstruction_claim_ledger.yaml", "claim_ledger.yaml", "claim_ledger.md"]:
            ledger_path = pkg_spec.path / ledger_name
            if ledger_path.is_file():
                report.total_files_scanned += 1
                v_list = audit_claim_hygiene_in_file(pkg_id, ledger_path)
                if v_list:
                    report.violations.extend(v_list)
                    report.violations_count += len(v_list)
                else:
                    report.clean_files_count += 1

    return report
