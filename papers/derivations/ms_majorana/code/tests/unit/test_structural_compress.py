"""Test suite for structural_compress module (LIB4-008)."""

import pytest
from omega_engine.crates.type.structural_manifest import pilot_foc_nonclaims_manifest
from omega_engine.crates.type.obs_ledger import witnessed_difference_site, build_obs_ledger_for_site
from omega_engine.crates.type.structural_compress import compress_cover, CompressRefuse


def test_compress_cover_basic():
    manifest = pilot_foc_nonclaims_manifest()
    site = witnessed_difference_site()
    rows = build_obs_ledger_for_site(site, [])
    res = compress_cover("WD0_COVER", manifest, rows)

    assert res.cover_id == "WD0_COVER"
    assert res.authority_effect == "None"
    assert len(res.chosen_sections) >= 1
    assert len(res.obstruction_rows) >= 1
    dict_res = res.to_dict()
    assert dict_res["authority_effect"] == "None"


def test_compress_cover_refuse_empty():
    manifest = pilot_foc_nonclaims_manifest()
    with pytest.raises(CompressRefuse):
        compress_cover("", manifest, [])


