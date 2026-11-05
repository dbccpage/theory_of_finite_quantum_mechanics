"""Cryptographic Manifest Checker across Paper Packages.

Audits SHA256SUMS and MANIFEST.sha256 byte-level integrity.
AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ManifestCheckResult:
    package_name: str
    manifest_name: str
    total_entries: int = 0
    matched_entries: int = 0
    missing_files: list[str] = field(default_factory=list)
    mismatches: list[dict[str, str]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return (
            len(self.missing_files) == 0
            and len(self.mismatches) == 0
            and len(self.errors) == 0
            and self.matched_entries > 0
        )


def check_manifest(
    package_dir: Path,
    manifest_name: str = "SHA256SUMS",
) -> ManifestCheckResult:
    result = ManifestCheckResult(
        package_name=package_dir.name,
        manifest_name=manifest_name,
    )
    manifest_path = package_dir / manifest_name
    if not manifest_path.is_file():
        result.errors.append(f"Manifest file {manifest_name} not found in {package_dir}")
        return result

    try:
        content = manifest_path.read_text(encoding="utf-8")
    except Exception as e:
        result.errors.append(f"Failed to read {manifest_name}: {e}")
        return result

    lines = content.splitlines()
    for lineno, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        match = re.fullmatch(r"([0-9a-fA-F]{64})\s+\*?(.+)", line)
        if not match:
            result.errors.append(f"Malformed manifest line {lineno} in {manifest_name}: {line!r}")
            continue

        expected_hash, rel_path = match.group(1).lower(), match.group(2).strip()
        file_path = package_dir / rel_path
        result.total_entries += 1

        if not file_path.is_file():
            result.missing_files.append(rel_path)
            continue

        try:
            actual_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
            if actual_hash == expected_hash:
                result.matched_entries += 1
            else:
                result.mismatches.append({
                    "path": rel_path,
                    "expected": expected_hash,
                    "actual": actual_hash,
                })
        except Exception as e:
            result.errors.append(f"Error hashing {rel_path}: {e}")

    return result
