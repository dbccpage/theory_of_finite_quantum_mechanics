#!/usr/bin/env python3
"""Build the deterministic PO-000 release archive for Zenodo.

AuthorityEffect: None.  Packaging bytes is not evidence for any claim.

Why this exists (2026-09-03).  The deposit previously shipped no current
archive, while the manuscript told a reader to extract one, and the Zenodo
record carried a stale archive whose contents contradicted the tree.  The
archive and sidecar are derived release objects under dist/, so this builder makes
their derivation from the covered tree explicit and reproducible.  They must
be regenerated whenever a covered payload changes.

Two properties this guarantees, both of which the previous archives lacked:

1.  **Self-consistency.**  Both manifests are regenerated before packing.
    ``MANIFEST.sha256`` covers the payload and ``SHA256SUMS`` covers the payload
    plus that manifest. Only those members and the primary manifest are packed.
    The generated TeX and PDF
    are tracked inputs, so a clean checkout contains every release member. A
    file present in the tree but absent from the manifest is an error, not a
    silent extra.

2.  **Platform independence.**  Text members are normalised to LF *inside the
    archive*, and both packed manifests are computed over those normalised
    bytes, inner manifest first. Without this, a CRLF checkout carries hashes
    no Linux extraction can reproduce -- the working tree here is CRLF while
    the repository stores LF, so the manifest was checkout-dependent.

Determinism: members are sorted, every timestamp is fixed, the creator-system
byte is fixed, and members are **stored, not deflated**, so two builds of the
same tree are byte-identical *on any machine* -- not merely on the one that
built it.

The last property was added 2026-09-03 after an external rebuild on Linux
produced content-identical members at a different size and hash (606,567 bytes
against 607,244). Two causes, both platform rather than content:
``zipfile.ZipInfo`` stamps ``create_system`` 0 on Windows and 3 elsewhere, and
this machine's zlib is zlib-ng, whose deflate output differs from stock zlib
at the same level. Storing the members removes the compressor from the
question entirely; the archive roughly doubles, to about 1.3 MB, which is a
cheap price for a reproducibility claim that survives leaving this laptop.

Usage:
    python scripts/build_release_zip.py --output dist/
    python scripts/build_release_zip.py --output dist/ --check
"""

from __future__ import annotations

import argparse
import hashlib
import io
import sys
import tempfile
import zipfile
from pathlib import Path

from regen_sha256sums import (
    MANIFEST_NAME,
    PAYLOAD_MANIFEST_NAME,
    check_manifests,
    iter_payload_files,
    regenerate,
)
from release_custody import identity, regular, snapshot

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = PACKAGE_ROOT / "SHA256SUMS"
ARCHIVE_ROOT = "000_projection_obstruction"
# Fixed DOS timestamp (1980-01-01 00:00:00), the ZIP epoch.
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
# 3 = Unix. Pinned rather than inherited so a Windows build and a Linux
# build of the same tree agree byte for byte.
CREATE_SYSTEM_UNIX = 3


def _version() -> str:
    return identity(PACKAGE_ROOT)["release_version"]


def _is_text(data: bytes) -> bool:
    """Text iff it is valid UTF-8 and holds no NUL byte."""
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def _normalise(data: bytes) -> bytes:
    """CRLF and lone CR to LF, for text members only."""
    if not _is_text(data):
        return data
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def regenerate_manifest() -> None:
    regenerate(PACKAGE_ROOT)


def _snapshot_with_controls(root: Path) -> dict[str, str]:
    state = snapshot(root)
    # release_custody.files excludes derived .sha256 sidecars. This named root
    # manifest is a control, and is checked explicitly instead of relaxing that
    # payload selector for every archive sidecar.
    secondary = root / PAYLOAD_MANIFEST_NAME
    regular(secondary, root)
    state[PAYLOAD_MANIFEST_NAME] = hashlib.sha256(secondary.read_bytes()).hexdigest()
    return state


def canonical_bytes(root: Path = PACKAGE_ROOT) -> bytes:
    problems = check_manifests(root)
    if problems:
        raise ValueError("; ".join(problems))
    initial = _snapshot_with_controls(root)
    members = [path.relative_to(root).as_posix() for path in iter_payload_files(root)]
    payload = {relative: _normalise((root / relative).read_bytes()) for relative in members}
    payload[PAYLOAD_MANIFEST_NAME] = "".join(
        f"{hashlib.sha256(payload[relative]).hexdigest()}  {relative}\n" for relative in members
    ).encode("utf-8")
    members = sorted(payload)
    packed_manifest = "".join(
        f"{hashlib.sha256(payload[relative]).hexdigest()}  {relative}\n" for relative in members
    ).encode("utf-8")
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for relative in [*members, MANIFEST_NAME]:
            entry = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{relative}", date_time=FIXED_TIME)
            entry.create_system = CREATE_SYSTEM_UNIX
            entry.external_attr = (0o100755 if relative.endswith(".sh") else 0o100644) << 16
            entry.compress_type = zipfile.ZIP_STORED
            archive.writestr(entry, packed_manifest if relative == MANIFEST_NAME else payload[relative])
    if _snapshot_with_controls(root) != initial:
        raise ValueError("payload changed while building archive")
    return output.getvalue()


def build(output_dir: Path) -> Path:
    regenerate_manifest()
    data = canonical_bytes()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"projection_obstruction_v{_version()}.zip"
    for control in (archive, archive.with_suffix(".zip.sha256")):
        if control.exists() or control.is_symlink():
            regular(control)
    archive.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    archive.with_suffix(".zip.sha256").write_bytes(f"{digest}  {archive.name}\n".encode("utf-8"))
    print(f"archive: {archive.name}; bytes: {len(data)}; sha256: {digest}")
    return archive


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=PACKAGE_ROOT / "dist")
    ap.add_argument(
        "--check", action="store_true",
        help="verify both existing manifests, then build twice and compare complete archives",
    )
    args = ap.parse_args(argv)

    if args.check:
        problems = check_manifests(PACKAGE_ROOT)
        if problems:
            print("FAIL: " + "; ".join(problems), file=sys.stderr)
            return 1
    first = build(args.output)
    if args.check:
        # 2026-09-03: both builds used to land in the same directory, so with
        # the documented `--output dist` the second build hashed the first
        # archive and its sidecar (93 members, then 95) and reported NOT
        # REPRODUCIBLE for an entirely self-inflicted reason.  `dist/` is now
        # excluded from the manifest, and the comparison build additionally
        # goes to a throwaway directory so the check cannot pollute itself.
        digest_a = hashlib.sha256(first.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as scratch:
            second = build(Path(scratch))
            digest_b = hashlib.sha256(second.read_bytes()).hexdigest()
        if digest_a != digest_b:
            print("NOT REPRODUCIBLE: two builds differ", file=sys.stderr)
            return 1
        print("  reproducible: two builds are byte-identical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
