"""Validator for the computability-carrier candidate inventory (Python port).

Origin: PowerShell test code/tests/test_computability_carrier_candidates.ps1 (function
Test-CarrierRecord), recovered from
C:/.ana/coda_university/coda_research/authorization_an_incompleteness_theory (recovery 2026-10-21).
Claim: urn:omega:fqm:authincomp:carrier-candidates-validator-python-port:v1
AuthorityEffect: None

What this computes: a structural gate over computability_carrier_candidates.json. The record must
stay globally `open`, no candidate may be selected or admitted, every candidate must carry exactly the
eight required admission fields with a ceiling and evidence, a `closed` field needs a closure basis,
evidence paths must be relative without parent segments, and the candidate id set must be exactly
{AIT-DTM0, PO-022, PO-023, AIT-PACKET4}. It admits nothing: it only refuses premature promotion.

Differences from the PowerShell original: evidence paths outside the recovered folder (PO-022 and
PO-023 sources, the GenX lakefile) do not exist in this repository, so `strict=False` collects them in
`unresolved` instead of failing; `strict=True` reproduces the original all-must-exist behaviour. The
original also grepped the PO-022 and PO-023 Lean scaffolds for `theorem POxx_C1 : True`; those files are
not recovered, so that check is reported as not rerunnable.

Scope Fence: passing this validator selects, admits and proves nothing about Turing-completeness.
"""

from __future__ import annotations

import copy
import json
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .replay_packet import ORIGINAL_PREFIX, PREFIX_MAP, map_path

SCHEMA = "ait.computability_carrier_candidates.v1"
REQUIRED_TOP_LEVEL = ("schema_version", "authority_effect", "admission_status", "required_admission_fields", "candidates")
REQUIRED_IDS = ("AIT-DTM0", "PO-022", "PO-023", "AIT-PACKET4")
FIELD_STATUSES = ("open", "partial", "closed")
PROSE_DIR = "papers/foundations/authorization_incompleteness/"
RECORD_RELATIVE = ORIGINAL_PREFIX + "computability_carrier_candidates.json"


class CarrierRecordError(Exception):
    """The record violates a structural rule (message mirrors the PowerShell throw text)."""


def load_record(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def default_exists(root: Path, prefix_map: dict[str, str] | None = PREFIX_MAP) -> Callable[[str], bool]:
    def exists(relative: str) -> bool:
        if (root / map_path(relative, prefix_map)).exists():
            return True
        # Prose files (proof_program.md, computability_lift_admission.md, ...) live beside the evidence tree.
        if relative.startswith(ORIGINAL_PREFIX):
            return (root / PROSE_DIR / relative[len(ORIGINAL_PREFIX):]).exists()
        return False

    return exists


def _check_evidence(candidate_id: str, field_name: str, paths: list[str], exists: Callable[[str], bool],
                    strict: bool, unresolved: list[str]) -> None:
    for relative in paths:
        if os.path.isabs(relative) or (len(relative) > 1 and relative[1] == ":") or ".." in relative.split("/"):
            raise CarrierRecordError(f"candidate {candidate_id} field {field_name} has unsafe evidence path")
        if not exists(relative):
            if strict:
                raise CarrierRecordError(f"candidate {candidate_id} field {field_name} evidence is absent")
            if relative not in unresolved:
                unresolved.append(relative)


def _check_field(candidate_id: str, field_name: str, field: dict[str, Any], exists: Callable[[str], bool],
                 strict: bool, unresolved: list[str]) -> None:
    if field["status"] not in FIELD_STATUSES:
        raise CarrierRecordError(f"candidate {candidate_id} field {field_name} has an invalid status")
    if field["status"] == "closed" and not str(field.get("closure_basis") or "").strip():
        raise CarrierRecordError(f"candidate {candidate_id} field {field_name} closed field lacks closure basis")
    if not str(field.get("ceiling") or "").strip():
        raise CarrierRecordError(f"candidate {candidate_id} field {field_name} lacks a ceiling")
    if not field.get("evidence"):
        raise CarrierRecordError(f"candidate {candidate_id} field {field_name} lacks evidence")
    _check_evidence(candidate_id, field_name, list(field["evidence"]), exists, strict, unresolved)


def _check_candidate(candidate: dict[str, Any], required: list[str], seen: set[str], exists: Callable[[str], bool],
                     strict: bool, unresolved: list[str]) -> None:
    cid = str(candidate["id"])
    if cid in seen:
        raise CarrierRecordError("candidate identifiers must be unique")
    seen.add(cid)
    if candidate["selected"]:
        raise CarrierRecordError(f"record is globally open; candidate {cid} cannot be selected")
    if candidate["admission_status"] == "admitted":
        raise CarrierRecordError(f"candidate {cid} cannot be admitted while the record is open")
    if candidate["admission_status"] not in ("open", "partial"):
        raise CarrierRecordError(f"candidate {cid} has an invalid admission status")
    if len(candidate["fields"]) != len(required):
        raise CarrierRecordError(f"candidate {cid} has an invalid admission field set")
    for name in required:
        if name not in candidate["fields"]:
            raise CarrierRecordError(f"candidate {cid} is missing field {name}")
        _check_field(cid, name, candidate["fields"][name], exists, strict, unresolved)


def validate_record(record: dict[str, Any], exists: Callable[[str], bool], strict: bool = False) -> dict[str, Any]:
    """Port of Test-CarrierRecord. Returns a report; raises CarrierRecordError on a violation."""
    if len(record) != len(REQUIRED_TOP_LEVEL):
        raise CarrierRecordError("record has an invalid top-level field set")
    for key in REQUIRED_TOP_LEVEL:
        if key not in record:
            raise CarrierRecordError(f"record is missing required top-level field {key}")
    if record["schema_version"] != SCHEMA:
        raise CarrierRecordError("record schema version is not supported")
    if record["authority_effect"] != "None":
        raise CarrierRecordError("record authority effect must be None")
    if record["admission_status"] != "open":
        raise CarrierRecordError("record must remain globally open")
    required = list(record["required_admission_fields"])
    if len(required) != 8:
        raise CarrierRecordError("record must name exactly eight admission fields")
    if len(set(required)) != len(required):
        raise CarrierRecordError("record admission fields must be unique")
    seen: set[str] = set()
    unresolved: list[str] = []
    for candidate in record["candidates"]:
        _check_candidate(candidate, required, seen, exists, strict, unresolved)
    if sorted(seen) != sorted(REQUIRED_IDS):
        raise CarrierRecordError("record candidate identifiers do not match the declared inventory")
    direct = [c for c in record["candidates"] if c["id"] == "AIT-DTM0"]
    if len(direct) != 1:
        raise CarrierRecordError("direct-machine candidate is not unique")
    fields = direct[0]["fields"]
    expectations = (
        (direct[0]["admission_status"], "partial", "direct candidate status"),
        (fields["syntax_and_encoding"]["status"], "partial", "direct syntax ceiling"),
        (fields["execution_semantics"]["status"], "partial", "direct execution ceiling"),
        (fields["universality"]["status"], "open", "direct universality ceiling"),
    )
    for actual, wanted, label in expectations:
        if actual != wanted:
            raise CarrierRecordError(f"{label} expected '{wanted}' but got '{actual}'")
    return {
        "candidates": sorted(seen),
        "unresolved_evidence": sorted(unresolved),
        "scaffold_ceiling_check": "not_rerunnable_po022_po023_sources_not_recovered",
    }


def mutation_cases(record: dict[str, Any]) -> list[tuple[str, dict[str, Any], str]]:
    """The five mutations of the original test: (label, mutated record, expected error fragment)."""
    cases: list[tuple[str, dict[str, Any], str]] = []

    def fresh() -> dict[str, Any]:
        return copy.deepcopy(record)

    m = fresh(); m["candidates"][0]["selected"] = True
    cases.append(("premature selection mutation", m, "globally open"))
    m = fresh(); m["candidates"][0]["admission_status"] = "admitted"
    cases.append(("premature admission mutation", m, "cannot be admitted"))
    m = fresh(); m["candidates"][0]["fields"]["universality"]["status"] = "closed"
    cases.append(("unsupported closure mutation", m, "closed field lacks closure basis"))
    m = fresh(); m["candidates"][0]["fields"]["syntax_and_encoding"]["evidence"][0] = "../outside.lean"
    cases.append(("evidence path escape mutation", m, "unsafe evidence path"))
    m = fresh(); del m["candidates"][0]["fields"]["universality"]
    cases.append(("missing field mutation", m, "invalid admission field set"))
    return cases
