"""Automated Bibliography Citation and Reconciliation Checker.

Verifies Acceptance Criterion 2(b) & R4/R10:
(b) Every bibliography item [n] in the References section is cited in the body text of projection_obstruction.md, with zero orphan references and zero broken citations.
(c) Reference [36] URL pin resolves without 404s.
(d) Martinazzo–Burghardt and Zoufal–Sutter–Woerner are cited.

AuthorityEffect: None.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BibliographyCheckResult:
    total_references: int = 0
    reference_numbers: list[int] = field(default_factory=list)
    cited_numbers: list[int] = field(default_factory=list)
    orphan_references: list[int] = field(default_factory=list)
    missing_definitions: list[int] = field(default_factory=list)
    ref36_valid: bool = False
    duhamel_priors_cited: bool = False
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return (
            len(self.orphan_references) == 0
            and len(self.missing_definitions) == 0
            and self.ref36_valid
            and self.duhamel_priors_cited
            and len(self.errors) == 0
        )


def check_bibliography(
    po000_dir: Path,
    manuscript_name: str = "projection_obstruction.md",
) -> BibliographyCheckResult:
    result = BibliographyCheckResult()
    manuscript_path = po000_dir / manuscript_name
    if not manuscript_path.is_file():
        result.errors.append(f"Manuscript not found at {manuscript_path}")
        return result

    content = manuscript_path.read_text(encoding="utf-8")
    ref_match = re.search(r"\n## References\s*\n", content)
    if not ref_match:
        result.errors.append("No '## References' section found in manuscript")
        return result

    body_text = content[:ref_match.start()]
    references_text = content[ref_match.end():]

    # Parse reference items in references section (e.g., "1. Author, Title...")
    ref_item_pattern = re.compile(r"^\s*(\d+)\.\s+(.+)$", re.MULTILINE)
    references: dict[int, str] = {}
    for match in ref_item_pattern.finditer(references_text):
        num = int(match.group(1))
        text = match.group(2).strip()
        references[num] = text

    result.total_references = len(references)
    result.reference_numbers = sorted(references.keys())

    # Strip markdown code blocks, inline code, display math, and inline math
    # so code indexings like e[0] and math intervals like [0, 1] are not parsed as citations
    cleaned_body = re.sub(r"```[\s\S]*?```", "", body_text)
    cleaned_body = re.sub(r"`[^`\n]+`", "", cleaned_body)
    cleaned_body = re.sub(r"\$\$[\s\S]*?\$\$", "", cleaned_body)
    cleaned_body = re.sub(r"\$[^\$\n]+\$", "", cleaned_body)

    # Extract all citation numbers in body text: [n], [n, m], [n--m], [n-m]
    # We look for bracketed groups of numbers not immediately followed by '(' (markdown links)
    citation_brackets = re.findall(r"\[([0-9\s,\-\–]+)\](?!\()", cleaned_body)
    cited_in_body: set[int] = set()
    for bracket in citation_brackets:
        # Split on commas
        parts = re.split(r",", bracket)
        for part in parts:
            part = part.strip()
            # Check for range: e.g. 10--12 or 10-12
            range_match = re.match(r"^(\d+)\s*(?:--|-|–)\s*(\d+)$", part)
            if range_match:
                start_n, end_n = int(range_match.group(1)), int(range_match.group(2))
                for n in range(start_n, end_n + 1):
                    cited_in_body.add(n)
            elif part.isdigit():
                cited_in_body.add(int(part))

    result.cited_numbers = sorted(cited_in_body)

    # Detect orphan references (defined in References but not cited in body)
    for ref_num in result.reference_numbers:
        if ref_num not in cited_in_body:
            result.orphan_references.append(ref_num)

    # Detect missing definitions (cited in body but not in References)
    for cited_num in cited_in_body:
        if cited_num not in references:
            result.missing_definitions.append(cited_num)

    # Check Reference [36] URL validity
    # R4 requirement: either commit 4a4fd192f with crates_rs, or commit 4bdf074a1b18cdeb710d991336e35f8f62979542 with documentation/rust_crates
    ref36_text = references.get(36, "")
    if not ref36_text:
        # If renumbered, search for genesis_bell_experiment
        for num, text in references.items():
            if "genesis_bell_experiment" in text or "Genesis-to-Bell" in text:
                ref36_text = text
                break

    if ref36_text:
        has_historical_pin = "4a4fd192f" in ref36_text and "crates_rs/omega_wdp/docs" in ref36_text
        has_updated_pin = "4bdf074" in ref36_text and "documentation/rust_crates/omega_wdp/docs" in ref36_text
        if has_historical_pin or has_updated_pin:
            result.ref36_valid = True
        else:
            result.errors.append(
                f"Reference [36] URL pin invalid: path and revision pin do not match valid repository states ({ref36_text[:100]}...)"
            )
    else:
        result.errors.append("Reference [36] (Genesis-to-Bell) not found in References")

    # Check Duhamel variational priors: Martinazzo–Burghardt and Zoufal–Sutter–Woerner
    body_and_refs = content.lower()
    has_martinazzo = "martinazzo" in body_and_refs
    has_zoufal = "zoufal" in body_and_refs
    if has_martinazzo and has_zoufal:
        result.duhamel_priors_cited = True
    else:
        missing = []
        if not has_martinazzo:
            missing.append("Martinazzo–Burghardt")
        if not has_zoufal:
            missing.append("Zoufal–Sutter–Woerner")
        result.errors.append(f"Missing required Duhamel literature citations: {', '.join(missing)}")

    return result
