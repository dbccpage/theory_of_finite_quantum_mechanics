"""Mutation tests: the independent verifier must reject wrong dispositions.

Added 2026-09-03.  A review found that ``EXPECTED_EVIDENCE_KINDS`` omitted
``D8a``, ``E4-second``, ``E4-commutator``, ``H8`` and ``H9``.  The disposition
loop skips claims absent from that table, so assigning those five a
deliberately wrong ``numerical_replay``/``pass`` disposition produced **no
errors**.  Coverage tests did not catch it because coverage only asks whether
a claim is mentioned, not whether it is mentioned correctly.

These tests mutate a real receipt one claim at a time and require the verifier
to complain.  They fail if the verifier ever goes quiet about a claim again.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

import pytest

_CODE = str(Path(__file__).resolve().parents[1])
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

import replay
import verify_certificate

PACKAGE_ROOT = Path(_CODE).parent

# The five claims whose dispositions were unpinned until 2026-09-03.
REGRESSION_CLAIMS = ("D8a", "E4-second", "E4-commutator", "H8", "H9")


@pytest.fixture(scope="module")
def receipt() -> dict:
    return replay.build_mechanization_run().model_dump(mode="json")


@pytest.fixture
def isolated_identity(tmp_path):
    """Copy actual identity inputs, without manufacturing a different version."""
    for name in ("release_identity.json", "pyproject.toml", "projection_obstruction.md"):
        shutil.copyfile(PACKAGE_ROOT / name, tmp_path / name)
    return tmp_path


@pytest.mark.parametrize("name", [
    "test_observable_duhamel_certification_boundary", "test_tangent_certification_boundary",
])
def test_release_identity_and_new_regression_are_bound(receipt, name):
    assert "release_identity.json" in verify_certificate.REQUIRED_PUBLICATION_PATHS
    assert "release_identity.json" in receipt["publication_hashes"]
    path = f"code/tests/{name}.py"
    assert path in verify_certificate.REQUIRED_SOURCE_PATHS
    assert path in receipt["source_hashes"]


@pytest.mark.parametrize("field", ["paper_version", "python_package_version"])
def test_stale_receipt_version_rejected(receipt, field):
    mutated = {**receipt, field: "0.0.0"}
    errors = verify_certificate.verify_document(mutated, PACKAGE_ROOT)
    assert any(field in error and "release_identity.json" in error for error in errors)


@pytest.mark.parametrize("payload", [
    None,
    "{",
    "null",
    "[]",
    '{"schema":"po000.release_identity.v1","schema":"duplicate"}',
])
def test_absent_or_malformed_identity_fails_before_execution(
    receipt, isolated_identity, monkeypatch, payload
):
    path = isolated_identity / "release_identity.json"
    if payload is None:
        path.unlink()
    else:
        path.write_text(payload, encoding="utf-8")
    monkeypatch.setattr(replay, "_covering_edge_receipt", lambda: pytest.fail("checks ran before identity validation"))
    with pytest.raises((OSError, ValueError)):
        replay.build_mechanization_run(isolated_identity)
    errors = verify_certificate.verify_document(receipt, isolated_identity)
    assert any("missing or malformed release_identity.json" in error for error in errors)


@pytest.mark.parametrize("key,value", [
    ("schema", "unknown"),
    ("manuscript_version", True),
    ("code_version", 6),
    ("release_version", "0.0.0"),
    ("release_date", "2026-02-30"),
    ("release_date", "20261013"),
    ("status", ""),
    ("authority_effect", "publish"),
])
def test_identity_contract_rejected_independently(
    receipt, isolated_identity, monkeypatch, key, value
):
    path = isolated_identity / "release_identity.json"
    identity = json.loads(path.read_text(encoding="utf-8"))
    identity[key] = value
    path.write_text(json.dumps(identity), encoding="utf-8")
    monkeypatch.setattr(replay, "_covering_edge_receipt", lambda: pytest.fail("checks ran before identity validation"))
    with pytest.raises(ValueError):
        replay.build_mechanization_run(isolated_identity)
    assert verify_certificate.verify_release_identity(receipt, isolated_identity)


def test_code_version_must_match_producer_and_project(receipt, isolated_identity):
    path = isolated_identity / "release_identity.json"
    identity = json.loads(path.read_text(encoding="utf-8"))
    identity["code_version"] = "0.0.0"
    path.write_text(json.dumps(identity), encoding="utf-8")
    with pytest.raises(ValueError, match="replay producer"):
        replay.build_mechanization_run(isolated_identity)
    forged = {**receipt, "python_package_version": "0.0.0"}
    assert any("pyproject.toml" in error for error in verify_certificate.verify_release_identity(forged, isolated_identity))


def test_coordinated_identity_and_receipt_cannot_mislabel_manuscript(receipt, isolated_identity):
    path = isolated_identity / "release_identity.json"
    identity = json.loads(path.read_text(encoding="utf-8"))
    identity.update(manuscript_version="0.0.0", release_version="0.0.0")
    path.write_text(json.dumps(identity), encoding="utf-8")
    forged = {**receipt, "paper_version": "0.0.0"}
    with pytest.raises(ValueError, match="manuscript header"):
        replay.build_mechanization_run(isolated_identity)
    errors = verify_certificate.verify_release_identity(forged, isolated_identity)
    assert any("manuscript header" in error for error in errors)


def test_changed_identity_bytes_invalidate_receipt_even_when_versions_match(receipt, isolated_identity):
    path = isolated_identity / "release_identity.json"
    original_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    identity = json.loads(path.read_text(encoding="utf-8"))
    identity["status"] = "changed review status; still not deposited"
    path.write_text(json.dumps(identity), encoding="utf-8")
    assert hashlib.sha256(path.read_bytes()).hexdigest() != original_digest
    assert verify_certificate.verify_release_identity(receipt, isolated_identity) == []
    errors = verify_certificate.verify_document(receipt, isolated_identity)
    assert "hash mismatch: publication_hashes.release_identity.json" in errors


def test_identity_cannot_be_dropped_from_publication_inventory(receipt):
    hashes = {key: value for key, value in receipt["publication_hashes"].items() if key != "release_identity.json"}
    errors = verify_certificate.verify_document({**receipt, "publication_hashes": hashes}, PACKAGE_ROOT)
    assert any("inventory missing" in error and "release_identity.json" in error for error in errors)


def _mutate(doc: dict, claim_id: str, *, kind: str, verdict: str) -> dict:
    """Return a copy of the receipt with one claim's disposition replaced."""
    out = {**doc, "results": [dict(r) for r in doc["results"]]}
    for result in out["results"]:
        if claim_id in result["claim_ids"]:
            if len(result["claim_ids"]) > 1:
                # isolate the claim so the mutation targets only it
                result["claim_ids"] = [c for c in result["claim_ids"] if c != claim_id]
                clone = dict(result)
                clone["claim_ids"] = [claim_id]
                clone["evidence_kind"] = kind
                clone["verdict"] = verdict
                out["results"].append(clone)
            else:
                result["evidence_kind"] = kind
                result["verdict"] = verdict
            return out
    raise AssertionError(f"{claim_id} not present in the receipt")


def test_every_claim_has_a_pinned_disposition():
    """No claim may be silently unverifiable."""
    unpinned = set(verify_certificate.REQUIRED_CLAIMS) - set(
        verify_certificate.EXPECTED_EVIDENCE_KINDS
    )
    assert unpinned == set(), f"claims with no expected disposition: {sorted(unpinned)}"


def test_unmutated_receipt_verifies(receipt):
    assert verify_certificate.verify_document(receipt, PACKAGE_ROOT) == []


@pytest.mark.parametrize("claim_id", REGRESSION_CLAIMS)
def test_regression_claims_reject_numerical_replay(receipt, claim_id):
    """The exact mutation that used to pass clean must now be rejected."""
    mutated = _mutate(receipt, claim_id, kind="numerical_replay", verdict="pass")
    errors = verify_certificate.verify_document(mutated, PACKAGE_ROOT)
    assert any(claim_id in e and "evidence_kind" in e for e in errors), (
        f"verifier accepted numerical_replay/pass for {claim_id}: {errors}"
    )


@pytest.mark.parametrize("claim_id", sorted(verify_certificate.EXPECTED_EVIDENCE_KINDS))
def test_wrong_evidence_kind_is_rejected(receipt, claim_id):
    """Flip every claim to a kind it is not, and require a complaint."""
    expected = verify_certificate.EXPECTED_EVIDENCE_KINDS[claim_id]
    wrong = "premise_check" if expected != "premise_check" else "counterexample"
    mutated = _mutate(receipt, claim_id, kind=wrong,
                      verdict=verify_certificate.EXPECTED_VERDICTS[claim_id])
    errors = verify_certificate.verify_document(mutated, PACKAGE_ROOT)
    assert any(claim_id in e and "evidence_kind" in e for e in errors), (
        f"verifier accepted {wrong} for {claim_id}: {errors}"
    )


@pytest.mark.parametrize("claim_id", sorted(verify_certificate.EXPECTED_EVIDENCE_KINDS))
def test_wrong_verdict_is_rejected(receipt, claim_id):
    """Flip every claim's verdict and require a complaint."""
    expected_verdict = verify_certificate.EXPECTED_VERDICTS[claim_id]
    wrong = "pass" if expected_verdict != "pass" else "refused"
    mutated = _mutate(receipt, claim_id,
                      kind=verify_certificate.EXPECTED_EVIDENCE_KINDS[claim_id],
                      verdict=wrong)
    errors = verify_certificate.verify_document(mutated, PACKAGE_ROOT)
    assert any(claim_id in e and "verdict" in e for e in errors), (
        f"verifier accepted verdict {wrong} for {claim_id}: {errors}"
    )


@pytest.mark.parametrize("claim_id", verify_certificate.PROSE_SUPPLEMENT_CLAIMS)
def test_written_theorem_groups_cannot_be_promoted_to_executable_proof(receipt, claim_id):
    mutated = _mutate(receipt, claim_id, kind="exact_finite", verdict="pass")
    errors = verify_certificate.verify_document(mutated, PACKAGE_ROOT)
    assert any(claim_id in error and "evidence_kind" in error for error in errors)


def test_alpha_group_ids_and_unknown_rows_are_not_silently_ignored(tmp_path, monkeypatch):
    import evidence

    assert "E-LIMITS" in evidence.REQUIRED_CLAIM_IDS
    assert "E-LIMITS" in verify_certificate.REQUIRED_CLAIMS
    ledger = tmp_path / "ledger.md"
    ledger.write_text("| E-LIMITS | written |\n| Z-UNKNOWN | unknown |\n", encoding="utf-8")
    ids = evidence.load_required_claim_ids(ledger)
    assert set(ids) == {"E-LIMITS", "Z-UNKNOWN"}
    assert set(verify_certificate._LEDGER_ROW.findall(ledger.read_text())) == set(ids)
    monkeypatch.setattr(replay, "REQUIRED_LEDGER_CLAIM_IDS", (*evidence.REQUIRED_CLAIM_IDS, "Z-UNKNOWN"))
    with pytest.raises(ArithmeticError, match="coverage mismatch"):
        replay.build_mechanization_run()
