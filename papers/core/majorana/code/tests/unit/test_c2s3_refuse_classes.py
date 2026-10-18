from __future__ import annotations
"""C2S3-001: refuse-class catalog load + required codes."""


from pathlib import Path

import pytest

from omega_engine_governance.contracts.c2s3_parity_refuse import (
    REQUIRED_CLASS_CODES,
    _DEFAULT_CLASSES,
    assert_catalog_complete,
    load_refuse_classes,
)


def test_default_catalog_file_exists() -> None:
    assert _DEFAULT_CLASSES.is_file(), f"missing catalog: {_DEFAULT_CLASSES}"


def test_required_codes_exact_membership() -> None:
    codes = load_refuse_classes()
    assert_catalog_complete(codes)
    for c in REQUIRED_CLASS_CODES:
        assert c in codes
    # exact set size from catalog (may grow later; must include all required)
    assert len(codes) >= len(REQUIRED_CLASS_CODES)
    assert len(codes) == len(set(codes)), "duplicate codes in catalog"


def test_catalog_incomplete_raises(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text(
        '{"classes": [{"code": "DEV-UNCONTRACTED"}]}',
        encoding="utf-8",
    )
    codes = load_refuse_classes(p)
    with pytest.raises(ValueError, match="missing codes"):
        assert_catalog_complete(codes)


def test_authority_effect_none_in_file() -> None:
    text = _DEFAULT_CLASSES.read_text(encoding="utf-8")
    assert "None" in text
    assert "DEV-AUTHORITY" in text


