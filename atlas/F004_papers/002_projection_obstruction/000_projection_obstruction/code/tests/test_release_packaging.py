"""Regression tests for the release archive builder.

Added 2026-09-03 after an external review reproduced a defect the author's own
runs never hit: ``build_release_zip.py --output dist --check`` was **not
reproducible**, because ``regen_sha256sums.py`` did not exclude ``dist/``. The
second build hashed the first archive and its ``.sha256`` sidecar, so the two
archives differed (93 members, then 95). Building into a directory outside the
package tree -- which is what every development run happened to do -- passed.

That is the exact shape of bug these tests exist to prevent: a tool verified
only in the configuration its author used, not the one its documentation
tells a reader to use. Every test below therefore exercises the **documented**
``dist/`` path inside an isolated copy of the package, never in the tracked
review tree.

AuthorityEffect: None. Packaging bytes is not evidence for any claim.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
_LINE = re.compile(r"^([0-9a-fA-F]{64})\s+\*?(.+)$")

# Building the archive regenerates both manifests and writes into the package
# tree, so these tests are marked slow and share one build.
pytestmark = pytest.mark.usefixtures("built_archive")


@pytest.fixture(scope="module")
def built_archive(tmp_path_factory):
    """Build into an isolated package's documented ``dist/`` location."""
    package_root = tmp_path_factory.mktemp("po000-release") / PACKAGE_ROOT.name
    shutil.copytree(
        PACKAGE_ROOT,
        package_root,
        ignore=shutil.ignore_patterns(
            "dist", "build", "__pycache__", ".pytest_cache", ".coverage", "htmlcov",
            ".lake", "lake-manifest.json",
        ),
    )
    # Local dependency paths and compiled Lean artifacts must not become
    # deposit members after a reader runs the new scoped Lake build.
    lake_cache = package_root / "lean4" / ".lake"
    lake_cache.mkdir()
    (lake_cache / "local.olean").write_bytes(b"host-specific build artifact")
    (package_root / "lean4" / "lake-manifest.json").write_text(
        '{"packages":[{"dir":"/absolute/local/mathlib"}]}\n', encoding="utf-8"
    )
    dist = package_root / "dist"
    builder = package_root / "scripts" / "build_release_zip.py"
    # --check validates existing controls without silently repairing drift.
    # Refresh this intentionally modified sandbox first, then test that mode.
    refreshed = subprocess.run(
        [sys.executable, str(package_root / "scripts" / "regen_sha256sums.py")],
        cwd=package_root, capture_output=True, text=True, timeout=60, check=False,
    )
    assert refreshed.returncode == 0, refreshed.stdout + refreshed.stderr
    proc = subprocess.run(
        [sys.executable, str(builder), "--output", "dist", "--check"],
        cwd=package_root, capture_output=True, text=True, timeout=1800,
    )
    assert proc.returncode == 0, (
        "the documented build path failed:\n" + proc.stdout + proc.stderr
    )
    archives = sorted(dist.glob("*.zip"))
    assert len(archives) == 1, f"expected exactly one archive, got {archives}"
    yield archives[0]


def _manifest_paths(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = _LINE.match(line)
        assert m, f"unparseable manifest line: {line!r}"
        out.append(m.group(2).strip())
    return out


# ---------------------------------------------------------------------------
# 1. reproducibility through the documented path
# ---------------------------------------------------------------------------

def test_check_flag_reports_reproducible_through_the_documented_dist_path(built_archive):
    """``--output dist --check`` must succeed. This is the case that failed."""
    assert built_archive.is_file()
    assert built_archive.stat().st_size > 0


def test_second_build_reproduces_the_first_byte_for_byte(built_archive):
    first = hashlib.sha256(built_archive.read_bytes()).hexdigest()
    dist = built_archive.parent
    package_root = dist.parent
    builder = package_root / "scripts" / "build_release_zip.py"
    proc = subprocess.run(
        [sys.executable, str(builder), "--output", "dist"],
        cwd=package_root, capture_output=True, text=True, timeout=1800,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    second = hashlib.sha256((dist / built_archive.name).read_bytes()).hexdigest()
    assert first == second, "rebuilding into dist/ changed the archive"


def test_archive_sidecar_is_lf_pinned(built_archive):
    """The release sidecar must not acquire the builder host's newlines."""
    sidecar = built_archive.with_suffix(built_archive.suffix + ".sha256")
    data = sidecar.read_bytes()
    assert data.endswith(b"\n")
    assert b"\r\n" not in data


# ---------------------------------------------------------------------------
# 2. the archive must not contain build output or test debris
# ---------------------------------------------------------------------------

def test_archive_never_contains_its_own_output_directory(built_archive):
    """The original failure: the archive swallowed the previous archive."""
    names = zipfile.ZipFile(built_archive).namelist()
    offenders = [n for n in names
                 if "/dist/" in n or n.endswith(".zip")
                 or (n.endswith(".sha256") and n != "000_projection_obstruction/MANIFEST.sha256")]
    assert offenders == [], f"build output leaked into the archive: {offenders}"


@pytest.mark.parametrize("pattern", [
    ".coverage", "__pycache__", ".pytest_cache", ".ruff_cache",
    ".mypy_cache", ".ipynb_checkpoints", "htmlcov",
    "projection_obstruction.aux", "projection_obstruction.log",
    "projection_obstruction.toc",
    ".lake", "lake-manifest.json",
])
def test_archive_excludes_test_and_cache_debris(built_archive, pattern):
    names = zipfile.ZipFile(built_archive).namelist()
    offenders = [n for n in names if pattern in n]
    assert offenders == [], f"{pattern} entered the archive: {offenders[:5]}"


def test_manifest_excludes_the_same_debris(built_archive):
    """The archive is built from the manifest, so the manifest is the real gate."""
    manifest = built_archive.parent.parent / "SHA256SUMS"
    paths = _manifest_paths(manifest.read_text(encoding="utf-8"))
    offenders = [p for p in paths
                 if p.startswith(("dist/", "build/", "htmlcov/"))
                 or p.endswith((".zip", ".pyc"))
                 or (p.endswith(".sha256") and p != "MANIFEST.sha256")
                 or Path(p).name in {
                     ".coverage", "projection_obstruction.aux",
                     "projection_obstruction.log", "projection_obstruction.toc", "lake-manifest.json",
                 }
                 or "__pycache__" in p or ".lake" in Path(p).parts]
    assert offenders == [], f"manifest covers artefacts it should not: {offenders}"


# ---------------------------------------------------------------------------
# 3. the extracted archive verifies itself
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("manifest_name", ["MANIFEST.sha256", "SHA256SUMS"])
def test_extracted_archive_matches_its_own_manifest(built_archive, tmp_path, manifest_name):
    """Every hash in both packed manifests must match the packed bytes.

    This is the property the LF normalisation exists for: an archive built on
    a CRLF checkout must still verify after extraction anywhere.
    """
    with zipfile.ZipFile(built_archive) as zf:
        zf.extractall(tmp_path)
    root = tmp_path / "000_projection_obstruction"
    manifest = (root / manifest_name).read_text(encoding="utf-8")
    mismatched, absent = [], []
    for line in manifest.splitlines():
        m = _LINE.match(line.strip())
        if not m:
            continue
        digest, rel = m.group(1).lower(), m.group(2).strip()
        target = root / rel
        if not target.is_file():
            absent.append(rel)
            continue
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            mismatched.append(rel)
    assert absent == [], f"manifest names files absent from the archive: {absent}"
    assert mismatched == [], f"hash mismatch after extraction: {mismatched}"
    paths = set(_manifest_paths(manifest))
    assert manifest_name not in paths
    assert ("MANIFEST.sha256" in paths) == (manifest_name == "SHA256SUMS")
    assert "SHA256SUMS" not in paths


def test_extracted_archive_contains_no_crlf_in_text_members(built_archive, tmp_path):
    with zipfile.ZipFile(built_archive) as zf:
        zf.extractall(tmp_path)
    root = tmp_path / "000_projection_obstruction"
    offenders = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix in {".png", ".pdf", ".zip"}:
            continue
        data = path.read_bytes()
        if b"\x00" in data:
            continue
        if b"\r\n" in data:
            offenders.append(path.relative_to(root).as_posix())
    assert offenders == [], f"CRLF survived into the archive: {offenders[:5]}"


def test_deposit_cli_refuses_stale_secondary_despite_valid_outer_hash(built_archive, tmp_path):
    with zipfile.ZipFile(built_archive) as archive:
        archive.extractall(tmp_path)
    root = tmp_path / "000_projection_obstruction"
    command = [sys.executable, str(root / "verify_deposit.py"), "--integrity-only"]
    valid = subprocess.run(
        command, cwd=root, capture_output=True, text=True, timeout=60, check=False
    )
    assert valid.returncode == 0, valid.stdout + valid.stderr

    secondary = root / "MANIFEST.sha256"
    lines = secondary.read_text(encoding="utf-8").splitlines()
    digest, relative = lines[0].split("  ", 1)
    assert len(digest) == 64
    lines[0] = f"{'0' * 64}  {relative}"
    secondary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    new_digest = hashlib.sha256(secondary.read_bytes()).hexdigest()
    primary = root / "SHA256SUMS"
    primary_lines = primary.read_text(encoding="utf-8").splitlines()
    primary.write_text("\n".join(
        f"{new_digest}  MANIFEST.sha256" if line.endswith("  MANIFEST.sha256") else line
        for line in primary_lines
    ) + "\n", encoding="utf-8")

    invalid = subprocess.run(
        command, cwd=root, capture_output=True, text=True, timeout=60, check=False
    )
    assert invalid.returncode == 1
    assert "hash mismatch in MANIFEST.sha256" in invalid.stderr


# ---------------------------------------------------------------------------
# 4. (retired) archive file modes
#
# 2026-09-03: the two mode tests went out with public_export/. They pinned
# 0755 on the POSIX launchers and 0644 on everything else; the archive now
# carries no executable member, so there is nothing left to distinguish.
# ---------------------------------------------------------------------------
