"""Revalidation and disposition control for PLAN-WDP-RELEASE-CHECKS.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[3]


def evaluate_ci_policy_disposition(
    *,
    affected_checks_passed: bool,
    silent_baseline_refresh: bool,
    repin_owner_approved: bool,
    unresolved_policy_items: tuple[str, ...],
) -> dict[str, object]:
    """Enforce explicit CI/policy disposition without silent baseline refresh."""
    if not isinstance(affected_checks_passed, bool) or not isinstance(
        silent_baseline_refresh, bool
    ) or not isinstance(repin_owner_approved, bool):
        raise ValueError("disposition flags must be booleans")
    if silent_baseline_refresh:
        raise ValueError("silent trusted-baseline refresh is refused; DEC-WDP-REPIN is separate")
    if not affected_checks_passed:
        raise ValueError("affected local checks must pass before revalidation")
    return {
        "affected_checks_passed": affected_checks_passed,
        "silent_baseline_refresh": False,
        "dec_wdp_repin_separate": not repin_owner_approved,
        "unresolved_policy_items": unresolved_policy_items,
        "publication_clearance_claimed": False,
    }


def check_artifact_and_manifest_alignment(root: Path = PACKAGE_ROOT) -> dict[str, object]:
    """Verify manuscript, TeX, PDF, and manifest alignment in 000_witnessed_difference_programme."""
    md_path = root / "witnessed_difference_programme.md"
    tex_path = root / "witnessed_difference_programme.tex"
    pdf_path = root / "witnessed_difference_programme.pdf"
    evidence_path = root / "manifests" / "current_claim_evidence.json"
    release_manifest_path = root / "manifests" / "release_manifest.json"
    release_ver_path = root / "manifests" / "release_verification.json"

    for p in (
        md_path,
        tex_path,
        pdf_path,
        evidence_path,
        release_manifest_path,
        release_ver_path,
    ):
        if not p.is_file():
            raise ValueError(f"missing required artifact or manifest: {p.name}")

    md_sha = hashlib.sha256(md_path.read_bytes()).hexdigest()
    tex_text = tex_path.read_text(encoding="utf-8")
    first_line = tex_text.splitlines()[0].strip()
    tex_binds_md = first_line == f"% manuscript-sha256: {md_sha}"

    hrefs = re.findall(r"\\href\{([^}]+)\}", tex_text)
    relative_dir_hrefs = [
        h
        for h in hrefs
        if not h.startswith(("http://", "https://", "#")) and h.endswith("/")
    ]

    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    release_manifest = json.loads(release_manifest_path.read_text(encoding="utf-8"))
    release_ver = json.loads(release_ver_path.read_text(encoding="utf-8"))

    if (
        evidence.get("authority_effect") != "None"
        or release_manifest.get("authority_effect") != "None"
        or release_ver.get("authority_effect") != "None"
    ):
        raise ValueError("authority_effect must be None across all manifests")

    return {
        "tex_binds_manuscript_sha256": tex_binds_md,
        "pdf_nonempty": pdf_path.stat().st_size > 0,
        "relative_directory_href_count": len(relative_dir_hrefs),
        "evidence_record_count": len(evidence.get("claims", [])),
        "release_verification_status": release_ver.get("status"),
    }


def witness() -> dict[str, object]:
    disposition = evaluate_ci_policy_disposition(
        affected_checks_passed=True,
        silent_baseline_refresh=False,
        repin_owner_approved=False,
        unresolved_policy_items=("DEC-WDP-REPIN",),
    )
    alignment = check_artifact_and_manifest_alignment()
    if (
        not alignment["tex_binds_manuscript_sha256"]
        or not alignment["pdf_nonempty"]
        or alignment["relative_directory_href_count"] != 0
        or alignment["evidence_record_count"] < 150
        or alignment["release_verification_status"] != "PASS"
    ):
        raise RuntimeError(f"release check alignment invariant failed: {alignment}")
    return {
        "affected_checks_passed": disposition["affected_checks_passed"],
        "silent_baseline_refresh": disposition["silent_baseline_refresh"],
        "dec_wdp_repin_separate": disposition["dec_wdp_repin_separate"],
        "publication_clearance_claimed": disposition["publication_clearance_claimed"],
        "relative_directory_href_count": alignment["relative_directory_href_count"],
        "pdf_nonempty": alignment["pdf_nonempty"],
        "release_verification_status": alignment["release_verification_status"],
    }
