from __future__ import annotations
"""C3S3-003: kill-fake tests for admit batch code claims."""



import pytest

from omega_engine_governance.contracts.c3s3_admit_index import (
    _CORPUS,
    _DEFAULT_BATCH,
    _REPO,
    kill_fake_code_claim,
    load_batch,
    validate_batch,
)


def test_batch_code_claims_honest() -> None:
    batch = load_batch(_DEFAULT_BATCH)
    validate_batch(batch, _CORPUS)
    for e in batch["entries"]:
        kill_fake_code_claim(str(e.get("code_claim") or "none"), repo=_REPO)


def test_basic_matrix_has_real_code() -> None:
    batch = load_batch(_DEFAULT_BATCH)
    entry = next(e for e in batch["entries"] if "basic_matrix" in e["path"])
    claim = entry["code_claim"]
    assert claim != "none"
    assert (_REPO / claim).is_file()


def test_kill_fake_negative_missing_path() -> None:
    with pytest.raises(FileNotFoundError, match="kill-fake"):
        kill_fake_code_claim(
            "omega_engine/crates/definitely_not_a_real_module.rs",
            repo=_REPO,
        )


def test_kill_fake_none_passes() -> None:
    kill_fake_code_claim("none", repo=_REPO)
    kill_fake_code_claim("n/a", repo=_REPO)


def test_prose_entries_declare_none() -> None:
    batch = load_batch(_DEFAULT_BATCH)
    prose = [e for e in batch["entries"] if "basic_matrix" not in e["path"]]
    assert len(prose) >= 5
    for e in prose:
        assert str(e.get("code_claim") or "").lower() in {
            "none",
            "n/a",
            "na",
            "",
        }


