"""Port of the six-case carrier-candidate corpus (code/tests/test_computability_carrier_candidates.ps1).

Origin: papers/foundations/authorization_incompleteness/evidence/original/code/tests/test_computability_carrier_candidates.ps1
Claim: urn:omega:fqm:authincomp:carrier-candidates-corpus-python-port:v1
AuthorityEffect: None
Mutation-Kills: 5 premature-promotion or malformed-record mutations must be refused.
Scope Fence: passing admits no candidate; PO-022/PO-023 scaffold greps are not rerunnable here.
"""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
_pkg = types.ModuleType("staged_auth_incompleteness")
_pkg.__path__ = [str(REPO / "code/python/src/qm/auth_incompleteness")]
sys.modules.setdefault(_pkg.__name__, _pkg)
cc = importlib.import_module("staged_auth_incompleteness.carrier_candidates")
rp = importlib.import_module("staged_auth_incompleteness.replay_packet")

RECORD_PATH = REPO / rp.map_path(cc.RECORD_RELATIVE, rp.PREFIX_MAP)


@pytest.fixture(scope="module")
def record() -> dict:
    return cc.load_record(RECORD_PATH)


@pytest.fixture(scope="module")
def exists():
    return cc.default_exists(REPO)


def test_case_1_recovered_record_passes_nonstrict(record, exists) -> None:
    report = cc.validate_record(record, exists, strict=False)
    assert report["candidates"] == sorted(cc.REQUIRED_IDS)
    assert report["scaffold_ceiling_check"].startswith("not_rerunnable")


def test_unresolved_evidence_is_exactly_the_unrecovered_sources(record, exists) -> None:
    report = cc.validate_record(record, exists, strict=False)
    unresolved = report["unresolved_evidence"]
    assert unresolved, "expected PO-022/PO-023 and lakefile evidence to be unrecovered"
    for path in unresolved:
        assert (
            path.startswith("lean4/")
            or "/002_projection_obstruction/" in path
            or path.endswith(("proof_program.md", "computability_lift_admission.md"))
        ), path


def test_strict_mode_refuses_unrecovered_evidence(record, exists) -> None:
    with pytest.raises(cc.CarrierRecordError, match="evidence is absent"):
        cc.validate_record(record, exists, strict=True)


def test_all_evidence_resolves_when_everything_exists(record) -> None:
    report = cc.validate_record(record, lambda _p: True, strict=True)
    assert report["unresolved_evidence"] == []


@pytest.mark.parametrize("index", range(5))
def test_cases_2_to_6_mutations_are_refused(record, index: int) -> None:
    label, mutated, needle = cc.mutation_cases(record)[index]
    with pytest.raises(cc.CarrierRecordError) as info:
        cc.validate_record(mutated, lambda _p: True, strict=True)
    assert needle in str(info.value), label


def test_record_is_globally_open_and_selects_nothing(record) -> None:
    assert record["admission_status"] == "open"
    assert all(not c["selected"] for c in record["candidates"])
    assert all(c["admission_status"] in ("open", "partial") for c in record["candidates"])


def test_direct_machine_candidate_ceilings(record) -> None:
    direct = next(c for c in record["candidates"] if c["id"] == "AIT-DTM0")
    assert direct["fields"]["universality"]["status"] == "open"
    assert direct["fields"]["extensionality"]["status"] == "open"
    assert direct["fields"]["nontriviality"]["status"] == "open"
    assert direct["fields"]["effective_reduction"]["status"] == "open"
