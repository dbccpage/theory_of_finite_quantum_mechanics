from __future__ import annotations

import copy
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
MANIFEST = ROOT / "manifests" / "historical_claim_occurrences.json"


def test_historical_occurrence_manifest_preserves_census_without_status_inheritance() -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = payload["records"]
    assert payload["authority_effect"] == "None"
    assert payload["status_inheritance"] == "forbidden"
    assert len(records) == payload["expected_occurrence_count"] == 1010
    assert len({record["historical_id"] for record in records}) == 869
    assert len({record["occurrence_key"] for record in records}) == 1010
    assert Counter(record["source_path"] for record in records) == Counter(
        payload["expected_per_file_unique_id_counts"]
    )
    assert Counter(record["disposition"] for record in records) == Counter(
        {"EXACT_CANONICAL": 15, "NOT_CARRIED": 984, "WITHDRAWN": 11}
    )
    assert all(record["inherits_historical_status"] is False for record in records)
    assert all(record["mentions"] and record["source_context"] for record in records)
    assert all(
        bool(record["canonical_targets"]) == (record["disposition"] == "EXACT_CANONICAL")
        for record in records
    )


def test_historical_crosswalk_verifier_matches_json_to_the_only_canonical_ledger() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_historical_claim_crosswalk.py"),
            "--check",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result == {
        "absorbed_source_checked": False,
        "authority_effect": "None",
        "dispositions": {"EXACT_CANONICAL": 15, "NOT_CARRIED": 984, "WITHDRAWN": 11},
        "global_unique_historical_ids": 869,
        "historical_occurrences": 1010,
        "live_source_checked": False,
        "status": "PASS",
    }


def test_offline_check_refuses_a_disposition_edited_with_its_census() -> None:
    spec = importlib.util.spec_from_file_location(
        "wdp_crosswalk_under_test", ROOT / "scripts" / "generate_historical_claim_crosswalk.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
        ledger = (ROOT / "witnessed_difference_programme_claim_ledger.md").read_text(
            encoding="utf-8"
        )
        records = json.loads(MANIFEST.read_text(encoding="utf-8"))["records"]
        assert module._validate_records(copy.deepcopy(records), ledger)
        forged = copy.deepcopy(records)
        target = next(record for record in forged if record["disposition"] == "NOT_CARRIED")
        target["disposition"] = "EXACT_CANONICAL"
        target["canonical_targets"] = ["WDP-CH14-P02"]
        with pytest.raises(ValueError, match="disagrees with the crosswalk tables"):
            module._validate_records(forged, ledger)
    finally:
        sys.modules.pop(spec.name, None)


def test_historical_source_context_is_inert_display_text() -> None:
    ledger = (ROOT / "witnessed_difference_programme_claim_ledger.md").read_text(
        encoding="utf-8"
    )
    section = ledger.split("<!-- HISTORICAL-CLAIM-OCCURRENCES:BEGIN -->", 1)[1].split(
        "<!-- HISTORICAL-CLAIM-OCCURRENCES:END -->", 1
    )[0]
    assert re.search(r"!?\[[^\]]*\]\([^)]*\)", section) is None
    assert "<script" not in section.lower()


# Provenance only; no historical status promotion; AuthorityEffect: None.
