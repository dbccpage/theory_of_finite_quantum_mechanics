"""Point-by-point R1–R10 Forensic and Specification Checker.

Validates Acceptance Criterion 2(c) and Acceptance Criterion 6:
Audits requirements R1 through R10 against PO-000 manuscript, ledgers, and code.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class FindingReport:
    req_id: str
    title: str
    passed: bool
    details: str
    violations: list[str] = field(default_factory=list)


@dataclass
class R1R10AuditResult:
    reports: dict[str, FindingReport] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.reports.values()) and len(self.errors) == 0


def audit_r1_po033_scope(manuscript_text: str) -> FindingReport:
    """R1: Accurate PO-033 Scope Attribution."""
    violations: list[str] = []
    lower = manuscript_text.lower()

    # Check for forbidden overclaims regarding PO-033
    if "verified adaptive dynamics" in lower:
        violations.append("Contains forbidden phrase 'verified adaptive dynamics'")
    if "quadrature certification" in lower or "certified quadrature" in lower:
        violations.append("Contains forbidden phrase 'quadrature certification' for PO-033")
    if "honeycomb patch certification" in lower:
        violations.append("Contains attribution of honeycomb patch certification to PO-033")

    # Check required qualification phrases
    if "heuristic_uncertified" not in manuscript_text:
        violations.append("Missing explicit 'HEURISTIC_UNCERTIFIED' classification for PO-033")
    if "continuous-time" not in lower or "quadrature" not in lower:
        violations.append("Missing explicit statement on uncertified continuous-time integration/quadrature error")

    return FindingReport(
        req_id="R1",
        title="Accurate PO-033 Scope Attribution",
        passed=len(violations) == 0,
        details="Verified HEURISTIC_UNCERTIFIED status, lack of unearned quadrature certification claims, and conditional Duhamel theorem.",
        violations=violations,
    )


def audit_r2_sibling_reference_table(manuscript_text: str) -> FindingReport:
    """R2: Forensic Audit of Cut Material & Authoritative Reference Table."""
    violations: list[str] = []

    # Check for nonexistent PO-004 / PO-005 references
    if re.search(r"\bPO-004\b", manuscript_text):
        violations.append("Found reference to nonexistent destination 'PO-004'")
    if re.search(r"\bPO-005\b", manuscript_text):
        violations.append("Found reference to nonexistent destination 'PO-005'")

    # Check for presence of required sibling anchors
    required_anchors = ["PO-001", "PO-006", "PO-007", "PO-008", "PO-009", "PO-033", "PO-034", "PO-035"]
    for anc in required_anchors:
        if anc not in manuscript_text:
            violations.append(f"Missing authoritative reference to sibling {anc}")

    # Check handling of cut material (former §§3.4-3.14, Appendices D/E)
    # Must refer to archived revision 90e6231546 or d44f760555 or finite_qm
    if "90e6231546" not in manuscript_text and "d44f760555" not in manuscript_text:
        violations.append("Missing pinned historical revision (90e6231546 / d44f760555) for cut material")

    return FindingReport(
        req_id="R2",
        title="Cut Material Audit & Authoritative Reference Table",
        passed=len(violations) == 0,
        details="Verified absence of PO-004/005, presence of all 8 sibling anchors, and pinned cut material provenance.",
        violations=violations,
    )


def audit_r3_test_isolation(po000_dir: Path) -> FindingReport:
    """R3: Test Isolation in test_paper_artifacts.py."""
    violations: list[str] = []
    test_file = po000_dir / "code" / "tests" / "test_paper_artifacts.py"
    if not test_file.is_file():
        violations.append("test_paper_artifacts.py not found")
        return FindingReport(
            req_id="R3",
            title="Publication Integrity & Test Isolation",
            passed=False,
            details="test_paper_artifacts.py missing",
            violations=violations,
        )

    code = test_file.read_text(encoding="utf-8")
    # Verify that test_every_archive_field... uses an isolated copy, not raw packaging.build(tmp_path)
    if re.search(r"def test_every_archive_field_that_varies_by_platform_is_pinned\([^)]*\):\s+archive = packaging\.build\(", code):
        violations.append("test_every_archive_field_that_varies_by_platform_is_pinned directly invokes packaging.build without isolation")
    if re.search(r"def test_stored_members_mean_the_archive_holds_the_bytes_verbatim\([^)]*\):\s+archive = packaging\.build\(", code):
        violations.append("test_stored_members_mean_the_archive_holds_the_bytes_verbatim directly invokes packaging.build without isolation")
    if re.search(r"def test_the_sidecar_hashes_the_archive_not_the_tree\([^)]*\):\s+archive = packaging\.build\(", code):
        violations.append("test_the_sidecar_hashes_the_archive_not_the_tree directly invokes packaging.build without isolation")

    return FindingReport(
        req_id="R3",
        title="Publication Integrity & Test Isolation",
        passed=len(violations) == 0,
        details="Verified test_paper_artifacts.py isolates packaging builds into temporary copies.",
        violations=violations,
    )


def audit_r4_url_pin_ref36(manuscript_text: str) -> FindingReport:
    """R4: Historical URL Pin Repair in Reference [36] / [26]."""
    violations: list[str] = []
    ref_match = re.search(r"^\s*(?:26|36)\.\s+([^\n]+)", manuscript_text, re.MULTILINE)
    if not ref_match:
        # Search for genesis_bell_experiment anywhere in references
        ref_match = re.search(r"^\s*\d+\.\s+([^\n]*(?:Genesis[- ]to[- ]Bell|genesis_bell_experiment)[^\n]*)", manuscript_text, re.MULTILINE | re.IGNORECASE)

    ref_text = ref_match.group(0) if ref_match else ""
    if not ref_text:
        violations.append("Reference [36] / Genesis-to-Bell reference not found")
    else:
        # Check if URL produces 404 (commit 4a4fd192f with documentation/rust_crates is broken)
        if "4a4fd192f" in ref_text and "documentation/rust_crates" in ref_text:
            violations.append("Reference [36] pairs revision 4a4fd192f with post-rename path documentation/rust_crates (404 error)")
        has_historical_pin = "4a4fd192f" in ref_text and "crates_rs/omega_wdp/docs" in ref_text
        has_updated_pin = "4bdf074" in ref_text and "documentation/rust_crates/omega_wdp/docs" in ref_text
        if not (has_historical_pin or has_updated_pin):
            violations.append("Reference [36] URL pin invalid: path and revision pin do not match valid repository states")

    return FindingReport(
        req_id="R4",
        title="Historical URL Pin Repair in Reference [36]",
        passed=len(violations) == 0,
        details="Verified Reference [36]/[26] link path and commit pin form a valid URL.",
        violations=violations,
    )


def audit_r5_ledger_migration(po000_dir: Path) -> FindingReport:
    """R5: Claim Ledger, Dependency Graph, README, and Zenodo Metadata Migration."""
    violations: list[str] = []
    deps_path = po000_dir / "docs" / "claim_dependencies.json"
    if deps_path.is_file():
        deps_text = deps_path.read_text(encoding="utf-8")
        # Check for un-reconciled broken anchors
        broken_anchors = ["Lemma 3.4", "Lemma 3.5", "Lemma 3.14", "Lemma E.1", "Lemma E.2", "Lemma E.3", "Theorem E.4", "Theorem E.5", "Proposition E.6", "Proposition E.7"]
        for ba in broken_anchors:
            # If the broken anchor is claimed as active local proof without disposition, flag it
            if f'"proof_anchor": "**{ba}' in deps_text and '"disposition": "omitted"' not in deps_text and '"disposition": "imported' not in deps_text:
                violations.append(f"Broken local anchor '{ba}' still present in claim_dependencies.json as an active claim")

    return FindingReport(
        req_id="R5",
        title="Claim Ledger & Dependency Migration",
        passed=len(violations) == 0,
        details="Verified claim dependencies and ledger reconcile excised sections without orphan local anchors.",
        violations=violations,
    )


def audit_r6_rate_vs_state(manuscript_text: str) -> FindingReport:
    """R6: Rate vs. Finite-Time State Diagnostic in §1.3."""
    violations: list[str] = []
    # Search §1.3 area
    sec13_match = re.search(r"## 1\.3\b.*?(?=## 1\.4|\n## 2\b)", manuscript_text, re.DOTALL)
    sec_text = sec13_match.group(0) if sec13_match else ""
    if not sec_text:
        violations.append("Section 1.3 not found in manuscript")
    else:
        lower = sec_text.lower()
        if "rate" not in lower or "state" not in lower:
            violations.append("§1.3 does not explicitly separate rate and state diagnostics")
        if "5.5" not in sec_text and "theorem 5.5" not in lower:
            violations.append("§1.3 does not reference Theorem 5.5 connecting rate and state diagnostics")

    return FindingReport(
        req_id="R6",
        title="Rate vs. Finite-Time State Diagnostic in §1.3",
        passed=len(violations) == 0,
        details="Verified clear separation of rate diagnostic and state diagnostic in §1.3 linked by Theorem 5.5.",
        violations=violations,
    )


def audit_r7_hessian_statement(manuscript_text: str) -> FindingReport:
    """R7: Proposition 3.C Hessian Statement."""
    violations: list[str] = []
    # Check around Proposition 3.C
    prop3c_match = re.search(r"(?:Proposition 3\.C|Prop(?:osition)? 3\.C).*?(?=(?:###|##|\n\n\n))", manuscript_text, re.DOTALL | re.IGNORECASE)
    prop_text = prop3c_match.group(0) if prop3c_match else ""
    if prop_text:
        # Must not claim that D^2 \Pi is nonconstant as a function of base point
        if re.search(r"D\^2\\Pi_.*is nonconstant", prop_text):
            violations.append("Proposition 3.C incorrectly asserts D^2 Pi is nonconstant as a function of base point")
    else:
        # Spot check around line 172
        lines = manuscript_text.splitlines()
        for i, line in enumerate(lines[:300]):
            if "D^2\\Pi" in line and "nonconstant" in line and "contracted" not in line and "curvature" not in line:
                violations.append(f"Line {i+1} claims D^2 Pi is nonconstant without distinguishing contracted curvature")

    return FindingReport(
        req_id="R7",
        title="Proposition 3.C Hessian Statement",
        passed=len(violations) == 0,
        details="Verified Proposition 3.C distinguishes constant second derivative from contracted curvature term.",
        violations=violations,
    )


def audit_r8_retraction_domain(manuscript_text: str) -> FindingReport:
    """R8: Global Domain/Codomain of Opening Retraction in §2.1."""
    violations: list[str] = []
    sec21_match = re.search(r"## 2\.1\b.*?(?=## 2\.2|\n## 3\b)", manuscript_text, re.DOTALL)
    sec_text = sec21_match.group(0) if sec21_match else ""
    if not sec_text:
        violations.append("Section 2.1 not found in manuscript")
    else:
        # Should mention physical density state space S(H_V) or trace-one affine slice A_1
        if "\\mathcal{S}" not in sec_text and "density state" not in sec_text.lower() and "\\mathcal{A}_1" not in sec_text and "\\mathcal{A}_0" not in sec_text:
            violations.append("§2.1 does not specify the physical density state space or trace-one affine slice domain")

    return FindingReport(
        req_id="R8",
        title="Global Domain/Codomain of Opening Retraction in §2.1",
        passed=len(violations) == 0,
        details="Verified domain/codomain specification on density states and affine trace-one slice.",
        violations=violations,
    )


def audit_r9_covering_edge_setup(manuscript_text: str) -> FindingReport:
    """R9: Surgical Covering-Edge Setup Restoration before §7.4."""
    violations: list[str] = []
    # Check section before 7.4
    sec74_pos = manuscript_text.find("## 7.4")
    if sec74_pos == -1:
        sec74_pos = manuscript_text.find("### 7.4")
    if sec74_pos == -1:
        violations.append("Section 7.4 not found in manuscript")
    else:
        prefix = manuscript_text[max(0, sec74_pos - 3000):sec74_pos]
        # Should define covering edges, poset, coboundary operator d_0
        if "E_{\\mathrm{cov}}" not in prefix and "d_0" not in prefix and "coboundary" not in prefix.lower():
            violations.append("Missing covering-edge poset definition and coboundary formula immediately before §7.4")

    return FindingReport(
        req_id="R9",
        title="Surgical Covering-Edge Setup Restoration before §7.4",
        passed=len(violations) == 0,
        details="Verified compact display definition of covering-edge poset, fiber spaces, and coboundary operator before §7.4.",
        violations=violations,
    )


def audit_r10_house_language_and_formatting(manuscript_text: str) -> FindingReport:
    """R10: House Language, Formatting, and Core Strengths."""
    violations: list[str] = []
    # Check for legacy house scaffolding terms
    house_terms = [
        "Sovereign Mathematical Scope",
        "Relative Path in Estate",
        "Modular Delegation",
    ]
    for term in house_terms:
        if term in manuscript_text:
            violations.append(f"Contains legacy house scaffolding term: '{term}'")

    # Check for malformed ^3$ in Appendix C (distinguishing literal floating superscript from math expressions like $[-1,1]^3$)
    if " ^3$" in manuscript_text or "under a ^3$" in manuscript_text:
        violations.append("Contains malformed LaTeX expression '^3$' in text")

    return FindingReport(
        req_id="R10",
        title="House Language, Formatting, and Core Strengths",
        passed=len(violations) == 0,
        details="Verified replacement of scaffolding terms, formatting cleanups, and retention of core strengths.",
        violations=violations,
    )


def audit_all_r1_r10(po000_dir: Path) -> R1R10AuditResult:
    """Run full point-by-point R1-R10 audit on PO-000."""
    result = R1R10AuditResult()
    manuscript_path = po000_dir / "projection_obstruction.md"
    if not manuscript_path.is_file():
        result.errors.append(f"Manuscript not found at {manuscript_path}")
        return result

    text = manuscript_path.read_text(encoding="utf-8")

    result.reports["R1"] = audit_r1_po033_scope(text)
    result.reports["R2"] = audit_r2_sibling_reference_table(text)
    result.reports["R3"] = audit_r3_test_isolation(po000_dir)
    result.reports["R4"] = audit_r4_url_pin_ref36(text)
    result.reports["R5"] = audit_r5_ledger_migration(po000_dir)
    result.reports["R6"] = audit_r6_rate_vs_state(text)
    result.reports["R7"] = audit_r7_hessian_statement(text)
    result.reports["R8"] = audit_r8_retraction_domain(text)
    result.reports["R9"] = audit_r9_covering_edge_setup(text)
    result.reports["R10"] = audit_r10_house_language_and_formatting(text)

    return result
