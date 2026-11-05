#!/usr/bin/env python3
"""Build deterministic release manifests and ZIP bundle for PO-033.

AuthorityEffect: None. Packaging bytes is not evidence for any claim.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_NAME = "certified_adaptive_quantum_dynamics_2026-10-01.zip"
ARCHIVE_PREFIX = "certified_adaptive_quantum_dynamics"
ZIP_DATE = (2026, 10, 1, 12, 0, 0)

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".ipynb_checkpoints",
    ".lake",
    "dist",
    "build",
    "htmlcov",
    "scratch",
}
EXCLUDED_NAMES = {".coverage", "cov.json", "coverage.xml"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".out"}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def enumerate_payload(root: Path) -> list[str]:
    """Enumerate relative POSIX paths of all payload files in UTF-8 ordinal order."""
    payload: list[str] = []
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if any(part in EXCLUDED_DIRS or part.endswith((".egg-info", ".dist-info")) for part in rel.parts):
            continue
        if p.is_symlink():
            raise ValueError(f"symlink is not a release payload: {rel}")
        if not p.is_file():
            continue
        if p.name in EXCLUDED_NAMES or p.suffix in EXCLUDED_SUFFIXES:
            continue
        rel_posix = rel.as_posix()
        if rel_posix in ("SHA256SUMS", "MANIFEST.sha256") or rel_posix.endswith(".zip"):
            continue
        payload.append(rel_posix)
    payload.sort(key=lambda s: s.encode("utf-8"))
    return payload


def parse_manifest(data: str) -> dict[str, str]:
    """Reject malformed, empty, duplicate, ambiguous, or escaping inventories."""
    entries = {}
    seen = set()
    for line in data.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            raise ValueError("malformed checksum record")
        digest, name = match.groups()
        path = PurePosixPath(name)
        if (path.is_absolute() or path.as_posix() != name
                or ".." in path.parts or "\\" in name
                or any(ord(c) < 32 for c in name) or name.casefold() in seen):
            raise ValueError(f"unsafe or duplicate manifest path: {name}")
        seen.add(name.casefold())
        entries[name] = digest
    if not entries:
        raise ValueError("empty manifest")
    return entries


def generate_manifests(root: Path) -> tuple[dict[str, str], dict[str, str]]:
    payload = enumerate_payload(root)
    
    # 1. MANIFEST.sha256 covers exactly the payload files
    manifest_entries = {rel: sha256_of(root / rel) for rel in payload}
    manifest_lines = [
        f"{digest}  {rel}"
        for rel, digest in sorted(manifest_entries.items(), key=lambda pair: pair[0].encode("utf-8"))
    ]
    manifest_bytes = ("\n".join(manifest_lines) + "\n").encode("utf-8")
    (root / "MANIFEST.sha256").write_bytes(manifest_bytes)

    # 2. SHA256SUMS covers payload files PLUS MANIFEST.sha256
    manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
    sums_entries = dict(manifest_entries)
    sums_entries["MANIFEST.sha256"] = manifest_sha
    sums_lines = [
        f"{digest}  {rel}"
        for rel, digest in sorted(sums_entries.items(), key=lambda pair: pair[0].encode("utf-8"))
    ]
    sums_bytes = ("\n".join(sums_lines) + "\n").encode("utf-8")
    (root / "SHA256SUMS").write_bytes(sums_bytes)

    return manifest_entries, sums_entries


def build_archive(root: Path, archive_path: Path) -> None:
    # Read all files that must be packed: all payload files plus MANIFEST.sha256 and SHA256SUMS
    payload = enumerate_payload(root)
    all_members = sorted(
        [*payload, "MANIFEST.sha256", "SHA256SUMS"],
        key=lambda s: s.encode("utf-8")
    )
    
    seen: set[str] = set()
    with zipfile.ZipFile(
        archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for rel in all_members:
            key = rel.casefold()
            if key in seen:
                raise ValueError(f"duplicate archive member: {rel}")
            seen.add(key)
            member_name = f"{ARCHIVE_PREFIX}/{rel}"
            info = zipfile.ZipInfo(filename=member_name, date_time=ZIP_DATE)
            info.create_system = 3  # Unix
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            data = (root / rel).read_bytes()
            archive.writestr(info, data)


def verify_release(root: Path, archive_path: Path | None) -> bool:
    """Verify every declared hash, exact inventory, and (when supplied) ZIP bytes.

    archive_path=None is an explicitly extracted-bundle check, not a ZIP check.
    """
    try:
        payload = enumerate_payload(root)
        manifest_map = parse_manifest((root / "MANIFEST.sha256").read_text(encoding="utf-8"))
        sums_map = parse_manifest((root / "SHA256SUMS").read_text(encoding="utf-8"))
        if set(manifest_map) != set(payload):
            raise ValueError("MANIFEST.sha256 inventory differs from payload")
        if set(sums_map) != set(payload) | {"MANIFEST.sha256"}:
            raise ValueError("SHA256SUMS inventory differs from payload plus manifest")
        for entries in (manifest_map, sums_map):
            for name, digest in entries.items():
                if sha256_of(root / name) != digest:
                    raise ValueError(f"hash mismatch: {name}")
        if archive_path is not None:
            expected = {f"{ARCHIVE_PREFIX}/{name}" for name in [*payload, "MANIFEST.sha256", "SHA256SUMS"]}
            with zipfile.ZipFile(archive_path) as archive:
                names = archive.namelist()
                if len({name.casefold() for name in names}) != len(names):
                    raise ValueError("duplicate ZIP member")
                if set(names) != expected:
                    raise ValueError("ZIP inventory differs from release inventory")
                for info in archive.infolist():
                    if info.external_attr >> 16 != 0o100644 or info.date_time != ZIP_DATE:
                        raise ValueError(f"noncanonical ZIP metadata: {info.filename}")
                    relative = info.filename[len(ARCHIVE_PREFIX) + 1:]
                    if archive.read(info) != (root / relative).read_bytes():
                        raise ValueError(f"ZIP content mismatch: {relative}")
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}")
        return False
    scope = "release ZIP" if archive_path is not None else "extracted payload (ZIP not checked)"
    print(f"OK: Verified {len(payload)} payload files, 2 manifests, and {scope}.")
    return True


def update_verify_deposit(root: Path, all_files: list[str]) -> None:
    vd_path = root / "verify_deposit.py"
    if not vd_path.is_file():
        return
    text = vd_path.read_text(encoding="utf-8")
    # Update REQUIRED_FILES
    req_files = sorted(all_files, key=lambda s: s.encode("utf-8"))
    replacement = f"REQUIRED_FILES = {req_files!r}"
    text = re.sub(r"REQUIRED_FILES\s*=\s*\[[^\]]*\]", replacement, text)
    # Update claim ledger reference if needed
    text = text.replace("'claim_ledger.md'", "'033_certified_adaptive_quantum_dynamics_claim_ledger.md'")
    text = text.replace('"claim_ledger.md"', '"033_certified_adaptive_quantum_dynamics_claim_ledger.md"')
    vd_path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check manifests and release archive without rebuilding")
    parser.add_argument("--extracted", action="store_true", help="Check an extracted bundle without requiring its outer ZIP")
    args = parser.parse_args()
    if args.extracted and not args.check:
        parser.error("--extracted requires --check")

    archive_path = PACKAGE_ROOT / ARCHIVE_NAME

    if args.check:
        ok = verify_release(PACKAGE_ROOT, None if args.extracted else archive_path)
        return 0 if ok else 1

    # First update verify_deposit.py with candidate files
    pre_payload = enumerate_payload(PACKAGE_ROOT)
    all_release_files = sorted([*pre_payload, "MANIFEST.sha256", "SHA256SUMS"], key=lambda s: s.encode("utf-8"))
    update_verify_deposit(PACKAGE_ROOT, all_release_files)

    # Now generate manifests with updated verify_deposit.py
    generate_manifests(PACKAGE_ROOT)

    # Build release zip
    print(f"Building archive: {archive_path.name}")
    build_archive(PACKAGE_ROOT, archive_path)

    # Verify release
    ok = verify_release(PACKAGE_ROOT, archive_path)
    if ok:
        print(f"SUCCESS: {archive_path.name} built and verified.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
