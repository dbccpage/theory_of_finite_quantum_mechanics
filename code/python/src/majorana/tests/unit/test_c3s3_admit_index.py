from __future__ import annotations
"""C3S3-002: admit index apply + disposition query."""


import json
from pathlib import Path

import pytest

from omega_engine_governance.contracts.c3s3_admit_index import (
    apply_admit,
    disposition_of,
    load_batch,
    load_index,
    validate_batch,
)


def test_default_batch_bounds_and_files() -> None:
    from omega_engine_governance.contracts.c3s3_admit_index import _CORPUS, _DEFAULT_BATCH

    batch = load_batch(_DEFAULT_BATCH)
    paths = validate_batch(batch, _CORPUS)
    assert 5 <= len(paths) <= 15
    assert len(paths) == 10


def test_apply_admit_marks_batch_only(tmp_path: Path) -> None:
    from omega_engine_governance.contracts.c3s3_admit_index import _CORPUS, _DEFAULT_BATCH

    base = tmp_path / "base.json"
    base.write_text(
        json.dumps(
            {
                "schema": "review_status_index.v1",
                "authority_effect": "None",
                "default_disposition": "suspect",
                "entries": {},
            }
        ),
        encoding="utf-8",
    )
    out = tmp_path / "out.json"
    report = apply_admit(
        batch_path=_DEFAULT_BATCH,
        base_index_path=base,
        out_index_path=out,
        corpus=_CORPUS,
    )
    assert report.authority_effect == "None"
    assert report.batch_size == 10
    idx = load_index(out)
    for rel in report.admitted_paths:
        assert disposition_of(idx, rel) == "admitted"
    # non-batch math path remains suspect
    assert disposition_of(idx, "math/a_infinity_algebra.contract.yaml") == "suspect"


def test_batch_too_small_raises(tmp_path: Path) -> None:
    from omega_engine_governance.contracts.c3s3_admit_index import _CORPUS

    batch_path = tmp_path / "b.json"
    batch_path.write_text(
        json.dumps(
            {
                "entries": [
                    {"path": "math/basic_matrix.contract.yaml", "code_claim": "none"}
                ]
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="outside"):
        validate_batch(load_batch(batch_path), _CORPUS)


