#!/usr/bin/env python3
"""Build the deterministic PO-035 release archive."""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import tempfile
import zipfile
from pathlib import Path

from regen_sha256sums import render
from release_custody import identity, regular, snapshot

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = PACKAGE_ROOT / "SHA256SUMS"
ARCHIVE_ROOT = "zero_container_relational_spacetime_and_witness_holonomy"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
CREATE_SYSTEM_UNIX = 3


def _version() -> str:
    return identity(PACKAGE_ROOT)["release_version"]


def _is_text(data: bytes) -> bool:
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def _normalise(data: bytes) -> bytes:
    if not _is_text(data):
        return data
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def regenerate_manifest() -> None:
    if MANIFEST.exists() or MANIFEST.is_symlink():
        regular(MANIFEST, PACKAGE_ROOT)
    initial = snapshot(PACKAGE_ROOT, include_manifest=False)
    MANIFEST.write_bytes(render(PACKAGE_ROOT).encode("utf-8"))
    if snapshot(PACKAGE_ROOT, include_manifest=False) != initial:
        raise ValueError("payload changed during manifest regeneration")


def canonical_bytes(root: Path = PACKAGE_ROOT) -> bytes:
    initial = snapshot(root)
    manifest = root / "SHA256SUMS"
    regular(manifest, root)
    if manifest.read_bytes() != render(root).encode("utf-8"):
        raise ValueError("SHA256SUMS differs from retained tree")
    members = sorted(relative for relative in initial if relative != "SHA256SUMS")
    payload = {relative: _normalise((root / relative).read_bytes()) for relative in members}
    packed_manifest = "".join(
        f"{hashlib.sha256(payload[relative]).hexdigest()}  {relative}\n" for relative in members
    ).encode("utf-8")
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for relative in [*members, "SHA256SUMS"]:
            entry = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{relative}", date_time=FIXED_TIME)
            entry.create_system = CREATE_SYSTEM_UNIX
            entry.external_attr = (0o100755 if relative.endswith(".sh") else 0o100644) << 16
            entry.compress_type = zipfile.ZIP_STORED
            archive.writestr(entry, packed_manifest if relative == "SHA256SUMS" else payload[relative])
    if snapshot(root) != initial:
        raise ValueError("payload changed while building archive")
    return output.getvalue()


def build(output_dir: Path) -> Path:
    regenerate_manifest()
    data = canonical_bytes()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"zero_container_relational_spacetime_and_witness_holonomy_v{_version()}.zip"
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
        help="build twice and confirm the two archives are byte-identical",
    )
    args = ap.parse_args(argv)

    first = build(args.output)
    if args.check:
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
