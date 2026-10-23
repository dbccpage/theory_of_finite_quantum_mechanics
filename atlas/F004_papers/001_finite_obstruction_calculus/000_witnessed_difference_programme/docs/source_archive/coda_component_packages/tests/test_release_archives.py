from __future__ import annotations

import importlib.util
import json
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "rebuild_release.py"
SPEC = importlib.util.spec_from_file_location("f005_rebuild_release", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
RELEASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RELEASE)
PACKAGES = (
    "a",
    "coda",
    "coda_gtla",
    "cs",
    "cs_q",
    "fda",
    "foc",
    "mur",
    "or",
    "q",
)


def _release_fixture(tmp_path: Path) -> Path:
    package = tmp_path / "fixture"
    package.mkdir()
    payload = package / "payload.txt"
    payload.write_bytes(b"pinned payload\n")
    digest = RELEASE.sha256_file(payload)
    (package / "MANIFEST.sha256").write_bytes(f"{digest}  payload.txt\n".encode())
    with zipfile.ZipFile(package / "fixture_2026-09-27.zip", "w"):
        pass
    RELEASE.refresh(package)
    assert RELEASE.validate(package) == []
    return package


def _archive_members(package: Path) -> list[tuple[str, bytes]]:
    with zipfile.ZipFile(RELEASE.archive_path(package)) as archive:
        return [(info.filename, archive.read(info)) for info in archive.infolist()]


def _replace_archive(package: Path, members: list[tuple[str, bytes]]) -> None:
    with zipfile.ZipFile(RELEASE.archive_path(package), "w") as archive:
        for name, data in members:
            info = zipfile.ZipInfo(name, date_time=RELEASE.ZIP_DATE)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


@pytest.mark.parametrize("name", PACKAGES)
def test_archive_integrity_and_recorded_legacy_cs_envelope(name: str) -> None:
    errors = RELEASE.validate(ROOT / name)
    if name == "cs":
        # This author-managed 2026-09-27 archive predates the strict
        # byte-envelope rule. Keep its noncanonical envelope visible until a
        # separately versioned CS release replaces it.
        assert errors == ["ZIP envelope differs from canonical deterministic build"]
    else:
        assert errors == []


def test_notebooks_do_not_publish_error_streams_or_host_paths() -> None:
    for notebook in ROOT.glob("*/jupyter_notebooks/*.ipynb"):
        payload = json.loads(notebook.read_text(encoding="utf-8"))
        serialized = json.dumps(payload)
        assert ":\\\\Users\\\\" not in serialized, notebook
        for cell in payload.get("cells", []):
            for output in cell.get("outputs", []):
                assert output.get("output_type") != "error", notebook
                assert output.get("name") != "stderr", notebook


def test_binary_gitattributes_override_global_text_rule() -> None:
    for name in PACKAGES:
        attributes = (ROOT / name / ".gitattributes").read_text(encoding="utf-8").splitlines()
        global_index = attributes.index("* text=auto eol=lf")
        for pattern in ("*.zip -text", "*.pdf -text", "*.png -text"):
            assert global_index < attributes.index(pattern), (name, pattern)


def test_pending_and_mismatched_dois_are_not_asserted_by_sources() -> None:
    coda_references = (ROOT / "coda/docs/references.md").read_text(encoding="utf-8")
    mur_sources = "\n".join(
        (ROOT / relative).read_text(encoding="utf-8")
        for relative in (
            "mur/coda_mur.md",
            "mur/coda_mur.tex",
            "mur/zenodo_metadata.json",
        )
    )
    assert "10.5281/zenodo.coda.020" not in coda_references
    assert "10.5281/zenodo.20677250" not in mur_sources


def test_validator_rejects_missing_zip_member(tmp_path: Path) -> None:
    package = _release_fixture(tmp_path)
    _replace_archive(package, _archive_members(package)[:-1])
    assert "ZIP membership or ordering differs from SHA256SUMS" in RELEASE.validate(package)


def test_validator_rejects_zip_traversal_member(tmp_path: Path) -> None:
    package = _release_fixture(tmp_path)
    members = [("fixture/../escape.txt", b"escape")] + _archive_members(package)
    _replace_archive(package, members)
    errors = RELEASE.validate(package)
    assert "ZIP membership or ordering differs from SHA256SUMS" in errors
    assert "unsafe ZIP member: fixture/../escape.txt" in errors


def test_validator_rejects_zip_member_hash_mismatch(tmp_path: Path) -> None:
    package = _release_fixture(tmp_path)
    members = [
        (name, b"tampered" if name.endswith("/payload.txt") else data)
        for name, data in _archive_members(package)
    ]
    _replace_archive(package, members)
    assert "ZIP member hash mismatch: payload.txt" in RELEASE.validate(package)


def test_validator_rejects_bytes_after_zip_end_record(tmp_path: Path) -> None:
    package = _release_fixture(tmp_path)
    archive = RELEASE.archive_path(package)
    archive.write_bytes(archive.read_bytes() + b"trailing payload")
    assert "ZIP envelope differs from canonical deterministic build" in RELEASE.validate(package)


def test_validator_rejects_nonregular_manifest_control(tmp_path: Path) -> None:
    package = _release_fixture(tmp_path)
    manifest = package / "MANIFEST.sha256"
    manifest.unlink()
    manifest.mkdir()
    assert "non-regular release control: MANIFEST.sha256" in RELEASE.validate(package)


def test_validator_rejects_same_byte_symlink_control(tmp_path: Path) -> None:
    package = _release_fixture(tmp_path)
    sums = package / "SHA256SUMS"
    copy = package / "same_bytes.txt"
    copy.write_bytes(sums.read_bytes())
    sums.unlink()
    try:
        sums.symlink_to(copy.name)
    except OSError as error:
        pytest.skip(f"Windows symlink creation unavailable: {error}")
    assert "non-regular release control: SHA256SUMS" in RELEASE.validate(package)
