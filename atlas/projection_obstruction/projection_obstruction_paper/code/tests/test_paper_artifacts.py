"""Guards for the .tex/.pdf build and for portable archive determinism.

Added 2026-09-03 after an external review rejected the first release objects
for two reasons this module now makes impossible to ship again:

* The PDF was built with a monospace font carrying no Greek and no relational
  symbols, so omega, subscript one, less-or-equal, greater-or-equal and nu
  were **silently dropped** out of a dependency diagram, and script ell out of
  a reference title. xelatex reported eleven "Missing character" warnings and
  exited 0. A PDF that renders with holes in it is worse than one that fails
  to build, because it looks finished.
* The archive was byte-identical only on the machine that built it. A Linux
  rebuild produced content-identical members at 606,567 bytes rather than
  607,244, because ``zipfile.ZipInfo`` stamps a platform-dependent
  ``create_system`` and this machine's zlib is zlib-ng, whose deflate output
  differs from stock zlib.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
BUILDER = PACKAGE_ROOT / "scripts" / "build_paper_artifacts.py"
PREAMBLE = PACKAGE_ROOT / "scripts" / "obstruction-preamble.tex"
PAPER_MD = PACKAGE_ROOT / "projection_obstruction.md"
PAPER_TEX = PACKAGE_ROOT / "projection_obstruction.tex"
PAPER_PDF = PACKAGE_ROOT / "projection_obstruction.pdf"


def _load(path: Path, name: str):
    scripts_dir = str(PACKAGE_ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location(name, path)
    if not (spec and spec.loader):
        raise ImportError(f"Cannot load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


artifacts = _load(BUILDER, "build_paper_artifacts")
packaging = _load(PACKAGE_ROOT / "scripts" / "build_release_zip.py",
                  "build_release_zip")


# ---------------------------------------------------------------------------
# the log gate
# ---------------------------------------------------------------------------

MISSING_LOG = (
    "Missing character: There is no ν in font Latin Modern Mono 8 Regular!\n"
    "Missing character: There is no ℓ in font Latin Modern Roman 10 Regular!\n"
)
OVERFULL_LOG = "Overfull \\hbox (150.12422pt too wide) in paragraph at lines 1486--1487\n"
TINY_OVERFULL_LOG = "Overfull \\hbox (1.5pt too wide) in paragraph at lines 10--11\n"


def test_a_dropped_glyph_blocks_the_build():
    with pytest.raises(SystemExit) as excinfo:
        artifacts.audit_log(MISSING_LOG)
    message = str(excinfo.value)
    assert "characters dropped" in message
    assert "ν" in message and "ℓ" in message


def test_text_past_the_margin_blocks_the_build():
    with pytest.raises(SystemExit) as excinfo:
        artifacts.audit_log(OVERFULL_LOG)
    assert "past the margin" in str(excinfo.value)
    assert "1486--1487" in str(excinfo.value)


def test_a_hairline_overfull_box_does_not_block():
    """A gate that refuses everything would just be turned off."""
    artifacts.audit_log(TINY_OVERFULL_LOG)


def test_a_clean_log_passes():
    artifacts.audit_log("This is a normal xelatex log.\nOutput written.\n")


def test_the_threshold_is_visible_and_not_absurd():
    assert 1.0 < artifacts.OVERFULL_LIMIT_PT <= 20.0


# ---------------------------------------------------------------------------
# the shipped artifacts
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not PAPER_PDF.is_file(), reason="pdf not built")
def test_pdf_is_a_pdf_and_not_empty():
    data = PAPER_PDF.read_bytes()
    assert data.startswith(b"%PDF-")
    assert len(data) > 100_000


@pytest.mark.skipif(not PAPER_TEX.is_file(), reason="tex not built")
def test_tex_carries_no_control_characters():
    """The subtitle once reached xelatex carrying a raw ESC byte.

    `\\ell` was written into a double-quoted YAML scalar, where `\\e` is a YAML
    escape for ESC (0x1B). xelatex answered "Text line contains an invalid
    character" and the cause was three layers away from the message.
    """
    text = PAPER_TEX.read_text(encoding="utf-8", errors="replace")
    assert b"\r\n" not in PAPER_TEX.read_bytes()
    offenders = [(i, repr(line[:60]))
                 for i, line in enumerate(text.splitlines(), 1)
                 if any(ord(ch) < 32 and ch != "\t" for ch in line)]
    assert offenders == [], f"control characters in the generated TeX: {offenders}"


@pytest.mark.skipif(not PAPER_TEX.is_file(), reason="tex not built")
def test_tex_is_newer_than_nothing_and_matches_the_manuscript_title():
    text = PAPER_TEX.read_text(encoding="utf-8", errors="replace")
    assert artifacts.TITLE in text


def test_manuscript_keeps_unicode_out_of_verbatim_blocks():
    """Monospace faces that ship with TeX carry no Greek and no relations.

    These characters are fine in prose, where the roman face has them, and
    fine in math, where the math font does. Inside a fenced block they are set
    in the monospace face and vanish.
    """
    forbidden = set("ωνℓ₁≤≥")
    lines = PAPER_MD.read_text(encoding="utf-8").splitlines()
    in_fence = False
    offenders = []
    for number, line in enumerate(lines, 1):
        stripped = line.lstrip("> ").lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence and (set(line) & forbidden):
            offenders.append((number, line.strip()[:70]))
    assert offenders == [], (
        "characters that no TeX monospace face can set, inside a code block: "
        f"{offenders}")


# ---------------------------------------------------------------------------
# portable archive determinism
# ---------------------------------------------------------------------------

def _build_isolated_archive(tmp_path: Path) -> Path:
    """Build the release archive in an isolated copy of the package tree.

    Matches the test isolation pattern in test_release_packaging.py to ensure
    that running packaging tests never modifies MANIFEST.sha256 or SHA256SUMS
    in the live package root.
    """
    package_root = tmp_path / PACKAGE_ROOT.name
    shutil.copytree(
        PACKAGE_ROOT,
        package_root,
        ignore=shutil.ignore_patterns(
            "dist", "build", "__pycache__", ".pytest_cache", ".coverage", "htmlcov",
            ".lake", "lake-manifest.json",
        ),
    )
    dist = package_root / "dist"
    builder = package_root / "scripts" / "build_release_zip.py"
    proc = subprocess.run(
        [sys.executable, str(builder), "--output", str(dist)],
        cwd=package_root, capture_output=True, text=True, timeout=300,
    )
    assert proc.returncode == 0, (
        f"isolated release build failed:\n{proc.stdout}\n{proc.stderr}"
    )
    archives = sorted(dist.glob("*.zip"))
    assert len(archives) == 1, f"expected exactly one archive, got {archives}"
    return archives[0]


def test_every_archive_field_that_varies_by_platform_is_pinned(tmp_path):
    archive = _build_isolated_archive(tmp_path)
    with zipfile.ZipFile(archive) as zf:
        infos = zf.infolist()
    assert infos, "empty archive"
    creators = {info.create_system for info in infos}
    assert creators == {packaging.CREATE_SYSTEM_UNIX}, (
        f"create_system is not pinned: {creators}. ZipInfo stamps 0 on "
        "Windows and 3 elsewhere, so this alone breaks cross-platform "
        "reproducibility.")
    methods = {info.compress_type for info in infos}
    assert methods == {zipfile.ZIP_STORED}, (
        f"members are not stored: {methods}. Deflate output differs between "
        "zlib and zlib-ng at the same level, so a compressed archive is "
        "reproducible only on the machine that built it.")
    stamps = {info.date_time for info in infos}
    assert stamps == {packaging.FIXED_TIME}, f"timestamps not fixed: {stamps}"


def test_stored_members_mean_the_archive_holds_the_bytes_verbatim(tmp_path):
    """A stored member's compressed size equals its real size.

    This is the property that removes the compressor from the reproducibility
    question, so it is asserted rather than assumed.
    """
    archive = _build_isolated_archive(tmp_path)
    with zipfile.ZipFile(archive) as zf:
        mismatched = [info.filename for info in zf.infolist()
                      if info.compress_size != info.file_size]
    assert mismatched == [], f"these members were compressed: {mismatched[:5]}"


def test_the_sidecar_hashes_the_archive_not_the_tree(tmp_path):
    """Two checksum files exist and answer different questions.

    `SHA256SUMS` covers the payload as stored inside the archive; the sidecar
    covers the archive itself. Uploading the former beside the `.zip` states
    something false, and the working-tree copy does not even describe the
    packed bytes -- it describes a CRLF checkout.
    """
    archive = _build_isolated_archive(tmp_path)
    sidecar = archive.with_suffix(archive.suffix + ".sha256")
    assert sidecar.is_file(), "the builder wrote no sidecar"
    digest, _, name = sidecar.read_text(encoding="utf-8").strip().partition("  ")
    assert name == archive.name
    assert digest == hashlib.sha256(archive.read_bytes()).hexdigest()

    packed = zipfile.ZipFile(archive).read(
        f"{packaging.ARCHIVE_ROOT}/SHA256SUMS").decode("utf-8")
    assert archive.name not in packed, (
        "the in-archive manifest must not claim to hash the archive")


def test_preamble_pins_a_font_that_ships_with_tex():
    """The first build named DejaVu Sans Mono, which this machine lacks.

    Naming a font the builder happens to have is the same defect shape as
    verifying a tool only in the configuration its author uses.
    """
    text = PREAMBLE.read_text(encoding="utf-8")
    mono = re.search(r"\\setmonofont\{([^}]+)\}", text)
    assert mono, "no monospace font declared"
    assert "Latin Modern" in mono.group(1), (
        f"monospace font is {mono.group(1)!r}; use a face that ships with "
        "every TeX distribution so the archive builds elsewhere")
