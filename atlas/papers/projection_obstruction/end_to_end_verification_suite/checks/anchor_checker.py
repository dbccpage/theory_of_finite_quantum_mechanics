"""Automated Proof Anchor Resolution Checker.

Verifies Acceptance Criterion 2(a):
Every local proof_anchor in projection_obstruction_claim_ledger.yaml
and docs/claim_dependencies.json resolves in projection_obstruction.md.

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
class AnchorCheckResult:
    total_local_claims: int = 0
    resolved_count: int = 0
    unresolved_count: int = 0
    resolved_anchors: list[dict[str, str]] = field(default_factory=list)
    unresolved_anchors: list[dict[str, str]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.unresolved_count == 0 and len(self.errors) == 0


def clean_anchor_text(anchor: str) -> str:
    """Strip markdown formatting like leading/trailing ** and trailing dots/colons for flexible matching."""
    cleaned = anchor.strip()
    if cleaned.startswith("**") and cleaned.endswith("**"):
        cleaned = cleaned[2:-2].strip()
    cleaned = cleaned.rstrip(".:")
    return cleaned


def check_proof_anchors(
    po000_dir: Path,
    manuscript_name: str = "projection_obstruction.md",
) -> AnchorCheckResult:
    """Validate that every local proof anchor resolves in the manuscript."""
    result = AnchorCheckResult()
    manuscript_path = po000_dir / manuscript_name
    if not manuscript_path.is_file():
        result.errors.append(f"Manuscript not found at {manuscript_path}")
        return result

    manuscript_text = manuscript_path.read_text(encoding="utf-8")
    norm_manuscript = re.sub(r"\s+", " ", manuscript_text)

    # 1. Check claim_dependencies.json
    deps_path = po000_dir / "docs" / "claim_dependencies.json"
    if deps_path.is_file():
        try:
            deps_data = json.loads(deps_path.read_text(encoding="utf-8"))
            claims = deps_data.get("claims", [])
            for c in claims:
                cid = c.get("id", "UNKNOWN")
                proof_file = c.get("proof_file", "")
                anchor = c.get("proof_anchor", "")
                disposition = c.get("disposition", "local")

                # Sibling imported claims or explicitly omitted/archived claims are not local proof obligations
                if disposition in ("omitted", "imported_sibling", "archived_code"):
                    continue
                if proof_file and proof_file != manuscript_name:
                    continue
                if not anchor:
                    continue

                result.total_local_claims += 1
                cleaned = clean_anchor_text(anchor)
                
                # Check exact or cleaned substring in manuscript
                if anchor in manuscript_text or cleaned in manuscript_text or cleaned in norm_manuscript:
                    result.resolved_count += 1
                    result.resolved_anchors.append({
                        "source": "claim_dependencies.json",
                        "claim_id": cid,
                        "anchor": anchor,
                    })
                else:
                    result.unresolved_count += 1
                    result.unresolved_anchors.append({
                        "source": "claim_dependencies.json",
                        "claim_id": cid,
                        "anchor": anchor,
                        "cleaned": cleaned,
                    })
        except Exception as e:
            result.errors.append(f"Failed parsing claim_dependencies.json: {e}")

    # 2. Check projection_obstruction_claim_ledger.yaml
    yaml_path = po000_dir / "projection_obstruction_claim_ledger.yaml"
    if yaml_path.is_file():
        try:
            yaml_data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
            claims = yaml_data.get("claims", []) if isinstance(yaml_data, dict) else []
            for c in claims:
                cid = c.get("claim_id", "UNKNOWN")
                pointer = c.get("paper_pointer", {})
                heading = pointer.get("heading", "")
                section = pointer.get("section", "")
                status = c.get("claim_status", "")

                # If claim is omitted or imported, skip local resolution
                if status in ("OMITTED", "IMPORTED_SIBLING", "HISTORICAL_RETAINED"):
                    continue

                # Check evidence pointers
                evidence_list = c.get("evidence", [])
                for ev in evidence_list:
                    if ev.get("kind") == "prose_proof":
                        ev_ptr = ev.get("pointer", "")
                        if ev_ptr and ev_ptr.startswith("§"):
                            # Section pointer check
                            sec_num = ev_ptr.lstrip("§").strip()
                            if f"## {sec_num}" not in manuscript_text and f"### {sec_num}" not in manuscript_text and ev_ptr not in manuscript_text:
                                result.unresolved_count += 1
                                result.unresolved_anchors.append({
                                    "source": "claim_ledger.yaml",
                                    "claim_id": cid,
                                    "anchor": f"Section {ev_ptr}",
                                })
        except Exception as e:
            result.errors.append(f"Failed parsing claim_ledger.yaml: {e}")

    return result
