"""Keep later supplements out of the frozen canonical identifier scan."""

import importlib.util
from pathlib import Path


def test_exact_claim_tokens_exclude_later_and_extended_identifiers() -> None:
    paper = next(
        parent for parent in Path(__file__).resolve().parents
        if (parent / "witnessed_difference_programme_claim_ledger.md").is_file()
    )
    spec = importlib.util.spec_from_file_location(
        "canonical_claim_verifier", paper / "scripts/verify_claim_map.py"
    )
    assert spec is not None and spec.loader is not None
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    text = (
        "`WDP-CH00-N03` WDP-CH22-P01 WDP-CH23-P01 WDP-CH23-P01C "
        "WDP-CH04-P01C WDP-CH04-P010 WDP-CH04-P01_suffix "
        "WDP-CHU-P01 prefixWDP-CH04-P01 WDP-R12-P01"
    )
    assert verifier.CLAIM_PATTERN.findall(text) == ["WDP-CH00-N03", "WDP-CH22-P01"]
    assert verifier.main() == 0
