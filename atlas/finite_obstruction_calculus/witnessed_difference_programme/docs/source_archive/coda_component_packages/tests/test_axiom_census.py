from __future__ import annotations

import importlib.util
import sys
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "replay_lean_axiom_census.py"
SPEC = importlib.util.spec_from_file_location("f005_axiom_census", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CENSUS = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CENSUS
SPEC.loader.exec_module(CENSUS)


@pytest.mark.parametrize("package", CENSUS.PACKAGES)
def test_generated_census_matches_pinned_report_and_release(package: str) -> None:
    declarations = CENSUS.parse_report(package)
    assert len(declarations) == CENSUS.EXPECTED_COUNTS[package]
    CENSUS.check_census(package)

    manifest = (ROOT / package / "MANIFEST.sha256").read_text(encoding="utf-8")
    assert "  lean4/Census.lean\n" in manifest
    archive = next((ROOT / package).glob("*_2026-09-27.zip"))
    with zipfile.ZipFile(archive) as release:
        assert f"{package}/lean4/Census.lean" in release.namelist()


def test_reports_bind_exactly_522_case_sensitive_declarations() -> None:
    declarations = [
        declaration
        for package in CENSUS.PACKAGES
        for declaration in CENSUS.parse_report(package)
    ]
    assert len(declarations) == CENSUS.EXPECTED_TOTAL == 522
    a_names = {declaration.name for declaration in CENSUS.parse_report("a")}
    assert "CodaA.ResidualTerminal" in a_names
    assert "CodaA.residualTerminal" in a_names
