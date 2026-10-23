"""Verify the source snapshot manifest's canonical aggregate and optional bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "source_provenance.json"
SHA256 = re.compile(r"[0-9a-f]{64}")
SHA1 = re.compile(r"[0-9a-f]{40}")


def _safe_relative(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string")
    pure = PurePosixPath(value)
    if (
        not value
        or not pure.parts
        or "\\" in value
        or pure.is_absolute()
        or ".." in pure.parts
    ):
        raise ValueError(f"invalid {label}: {value!r}")
    return value


class _PathClaims:
    """Paths claimed so far, compared as a case-insensitive filesystem would see them.

    ``./code/a.py``, ``code//a.py``, and ``Code/A.py`` all name ``code/a.py``, and a
    file may not share a name with a directory that another path needs.
    """

    def __init__(self) -> None:
        self.files: set[str] = set()
        self.directories: set[str] = set()

    def claim(self, path: str) -> None:
        folded = tuple(part.casefold() for part in PurePosixPath(path).parts)
        key = "/".join(folded)
        ancestors = {"/".join(folded[:index]) for index in range(1, len(folded))}
        if key in self.files or key in self.directories or ancestors & self.files:
            raise ValueError(f"duplicate or case-colliding path: {path!r}")
        self.files.add(key)
        self.directories |= ancestors


def _file_item(item: object, label: str) -> dict[str, object]:
    if not isinstance(item, dict) or not {"path", "bytes", "sha256"} <= set(item):
        raise ValueError(f"{label} entry needs path, bytes, and sha256")
    return item


def _canonical_lines(files: list[dict[str, object]]) -> bytes:
    rows = [
        f"{item['path']}\t{item['sha256']}\t{item['bytes']}"
        for item in sorted(files, key=lambda item: str(item["path"]))
    ]
    return "\n".join(rows).encode("utf-8")


def verify(
    source_root: Path | None = None, absorbed_repo: Path | None = None
) -> dict[str, object]:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = payload["files"]
    snapshot = payload["snapshot"]
    paths: set[str] = set()
    claims = _PathClaims()
    for item in files:
        item = _file_item(item, "provenance")
        path = _safe_relative(item["path"], "provenance path")
        if path in paths:
            raise ValueError(f"duplicate provenance path: {path!r}")
        paths.add(path)
        claims.claim(path)
        if type(item["bytes"]) is not int or item["bytes"] < 0:
            raise ValueError(f"invalid byte count for {path}")
        if not isinstance(item["sha256"], str) or SHA256.fullmatch(item["sha256"]) is None:
            raise ValueError(f"invalid lowercase SHA-256 for {path}")

    custody = payload.get("durable_custody")
    if not isinstance(custody, dict):
        raise ValueError("durable custody declaration is required")
    uncommitted_paths = custody.get("uncommitted_source_paths")
    if not isinstance(uncommitted_paths, list):
        raise ValueError("durable custody needs an uncommitted source-path list")
    uncommitted = {
        _safe_relative(path, "uncommitted source path")
        for path in uncommitted_paths
    }
    if len(uncommitted) != len(uncommitted_paths):
        raise ValueError("duplicate uncommitted source path")
    if custody.get("uncommitted_file_count") != len(uncommitted):
        raise ValueError("durable custody uncommitted-file count drift")
    if not uncommitted <= paths:
        raise ValueError("uncommitted source path is absent from the provenance file list")

    archived_paths: set[str] = set()
    for item in files:
        path = str(item["path"])
        archived_value = item.get("archived_path")
        if path not in uncommitted:
            if archived_value is not None:
                raise ValueError(f"unexpected archive for tracked source: {path}")
            continue
        archived = _safe_relative(archived_value, "archived path")
        if archived in archived_paths:
            raise ValueError(f"duplicate archived path: {archived!r}")
        archived_paths.add(archived)
        archive_candidate = ROOT / archived
        if archive_candidate.is_symlink():
            raise ValueError(f"archived path must not be a symlink: {archived}")
        archive_path = archive_candidate.resolve()
        try:
            archive_path.relative_to(ROOT.resolve())
        except ValueError:
            raise ValueError(f"archived path escapes package root: {archived}") from None
        data = archive_path.read_bytes()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError(f"archived source byte drift: {path}")

    aggregate = hashlib.sha256(_canonical_lines(files)).hexdigest()
    total_bytes = sum(int(item["bytes"]) for item in files)
    if len(files) != snapshot["file_count"]:
        raise ValueError("source provenance file-count drift")
    if total_bytes != snapshot["total_bytes"]:
        raise ValueError("source provenance byte-count drift")
    if aggregate != snapshot["sha256"]:
        raise ValueError("source provenance aggregate drift")

    checked_source = False
    if source_root is not None:
        checked_source = True
        base = source_root.resolve()
        for item in files:
            path = (base / str(item["path"])).resolve()
            try:
                path.relative_to(base)
            except ValueError:
                raise ValueError(f"source path escapes root: {item['path']}") from None
            data = path.read_bytes()
            if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise ValueError(f"source byte drift: {item['path']}")

    absorbed = []
    identifiers: set[object] = set()
    for block in payload.get("absorbed_snapshots", []):
        identifier = block.get("id") if isinstance(block, dict) else None
        if identifier in identifiers:
            raise ValueError(f"duplicate absorbed snapshot id: {identifier!r}")
        identifiers.add(identifier)
        absorbed.append(_verify_absorbed(block, claims, absorbed_repo))

    return {
        "absorbed_snapshots": absorbed,
        "archived_files_checked": len(archived_paths),
        "archived_uncommitted_bytes_complete": len(archived_paths) == len(uncommitted),
        "authority_effect": "None",
        "file_count": len(files),
        "sha256": aggregate,
        "source_bytes_checked": checked_source,
        "status": "PASS",
        "total_bytes": total_bytes,
    }


def _verify_absorbed(
    block: object, claims: _PathClaims, absorbed_repo: Path | None
) -> dict[str, object]:
    """Check one absorbed sibling-package snapshot; its paths may not reuse earlier paths.

    The live check reads committed blobs at the recorded commit, because working
    trees may apply end-of-line conversion (for example ``*.bat eol=crlf``).
    """

    if not isinstance(block, dict):
        raise ValueError("absorbed snapshot must be an object")
    identifier = block.get("id")
    checkout = block.get("source_checkout")
    snapshot = block.get("snapshot")
    files = block.get("files")
    if not isinstance(identifier, str) or not identifier:
        raise ValueError("absorbed snapshot needs a nonempty id")
    if (
        not isinstance(checkout, dict)
        or SHA1.fullmatch(str(checkout.get("commit", ""))) is None
        or not isinstance(checkout.get("series_path"), str)
    ):
        raise ValueError(f"absorbed snapshot {identifier} needs a series path and a full commit")
    if not isinstance(snapshot, dict) or not isinstance(files, list) or not files:
        raise ValueError(f"absorbed snapshot {identifier} needs a snapshot and files")
    for item in files:
        item = _file_item(item, f"absorbed snapshot {identifier}")
        path = _safe_relative(item["path"], "absorbed path")
        claims.claim(path)
        if type(item["bytes"]) is not int or item["bytes"] < 0:
            raise ValueError(f"invalid byte count for {path}")
        if not isinstance(item["sha256"], str) or SHA256.fullmatch(item["sha256"]) is None:
            raise ValueError(f"invalid lowercase SHA-256 for {path}")
    aggregate = hashlib.sha256(_canonical_lines(files)).hexdigest()
    total_bytes = sum(int(item["bytes"]) for item in files)
    if (
        len(files) != snapshot.get("file_count")
        or total_bytes != snapshot.get("total_bytes")
        or aggregate != snapshot.get("sha256")
    ):
        raise ValueError(f"absorbed snapshot {identifier} aggregate drift")
    checked = False
    if absorbed_repo is not None:
        checked = True
        prefix = str(checkout["series_path"]).rstrip("/")
        for item in files:
            spec = f"{checkout['commit']}:{prefix}/{item['path']}"
            blob = subprocess.run(
                ["git", "-C", str(absorbed_repo), "cat-file", "blob", spec],
                capture_output=True,
                check=False,
            )
            if blob.returncode != 0:
                raise ValueError(f"absorbed source blob unavailable: {item['path']}")
            data = blob.stdout
            if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise ValueError(f"absorbed source byte drift: {item['path']}")
    return {
        "file_count": len(files),
        "id": identifier,
        "sha256": aggregate,
        "source_bytes_checked": checked,
        "total_bytes": total_bytes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path)
    parser.add_argument(
        "--absorbed-repo",
        type=Path,
        help="git checkout holding the recorded commit, for a live check of absorbed blobs",
    )
    args = parser.parse_args()
    try:
        result = verify(args.source_root, args.absorbed_repo)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"source provenance verification failed: {error}") from error
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
# Custody evidence only; AuthorityEffect: None.
