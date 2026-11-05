from __future__ import annotations
from .witness import verify_clean_export_manifest, witness_wdp_dp7_03

def test_wdp_dp7_03_clean_export_verification() -> None:
    summary = witness_wdp_dp7_03()
    assert summary["positive_status"] == "PASS"
    assert summary["verified_files"] == 2
    assert summary["escaped_status"] == "REFUSED"
    assert summary["escaped_reason"] == "HERMETIC_ESCAPE_TO_CHECKOUT"

def test_wdp_dp7_03_refuses_mismatch_and_unsafe_paths() -> None:
    manifest = {"manuscript.md": "sha256:aaa"}
    mismatch = verify_clean_export_manifest(manifest, {"manuscript.md": "sha256:zzz"})
    assert mismatch.status == "REFUSED"
    assert mismatch.reason == "HASH_MISMATCH:manuscript.md"
    unsafe = verify_clean_export_manifest({"../escape.md": "sha256:aaa"}, {"../escape.md": "sha256:aaa"})
    assert unsafe.status == "REFUSED"
    assert unsafe.reason == "UNSAFE_MANIFEST_PATH"
