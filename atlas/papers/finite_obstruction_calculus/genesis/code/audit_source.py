"""Check a pinned Genesis checkout against the companion's saved inventory.

This is a byte and population audit, not a test runner or proof checker. The
caller trusts the committed manifest and its SHA-256-bound inventory document.
Git administrative files are excluded; all other untracked files, including
ignored files, are refused. The declared population contains regular files
only: symlinks, submodules, and symlinked parent directories are refused.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path, PurePosixPath


class AuditFailure(ValueError):
    """The supplied checkout or audit inputs do not satisfy the contract."""


def git(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise AuditFailure(f"git {' '.join(arguments)} failed: {result.stderr.decode().strip()}")
    return result.stdout


def digest_file(path: Path, algorithm: str = "sha256") -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or path.as_posix() != value
        or ".." in path.parts
        or "\\" in value
        or ".git" in path.parts
        or ":" in value
    ):
        raise AuditFailure(f"unsafe or noncanonical inventory path: {value!r}")
    return path


def regular_file(root: Path, relative: PurePosixPath) -> Path:
    current = root
    for index, part in enumerate(relative.parts):
        current = current / part
        mode = current.lstat().st_mode
        expected = stat.S_ISREG(mode) if index == len(relative.parts) - 1 else stat.S_ISDIR(mode)
        if not expected:
            raise AuditFailure(f"not a regular file beneath real directories: {relative}")
    return current


def load_contract(manifest_path: Path) -> tuple[dict, dict[str, dict]]:
    # Do not resolve first: resolution would erase evidence that a control
    # file or one of its parent directories is a symlink. Inspect each
    # component before reading either the manifest or its bound inventory.
    manifest_path = manifest_path.absolute()
    anchor = Path(manifest_path.anchor)
    components = manifest_path.relative_to(anchor).parts
    if not components or ".." in components:
        raise AuditFailure("manifest path must name a file without parent traversal")
    manifest_path = regular_file(anchor, PurePosixPath(*components))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["schema_version"] != "genesis.source_inventory.v1":
        raise AuditFailure("unsupported inventory manifest schema")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["source_commit"]):
        raise AuditFailure("source commit must be a full lowercase Git SHA-1")
    # The manifest is in paper/manifests; the inventory reference is relative
    # to the explicitly declared paper root, not a repository ancestor index.
    if manifest_path.parent.name != "manifests":
        raise AuditFailure("manifest must be placed in its paper's manifests directory")
    paper_root = manifest_path.parent.parent
    reference = manifest["full_inventory"]
    inventory_path = regular_file(paper_root, relative_path(reference["path"]))
    if digest_file(inventory_path) != reference["sha256"]:
        raise AuditFailure("saved inventory document SHA-256 mismatch")
    document = json.loads(inventory_path.read_text(encoding="utf-8"))
    if document["snapshots"]["source"]["commit"] != manifest["source_commit"]:
        raise AuditFailure("inventory document and manifest have different source commits")
    entries = document[reference["json_key"]]
    population = {}
    for entry in entries:
        path = relative_path(entry["path"]).as_posix()
        if path in population:
            raise AuditFailure(f"duplicate inventory path: {path}")
        if entry["mode"] not in {"100644", "100755"}:
            raise AuditFailure(f"unsupported Git mode at {path}: {entry['mode']}")
        size = entry["size_bytes"]
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise AuditFailure(f"invalid byte count at {path}")
        if not re.fullmatch(r"[0-9a-f]{40}", entry["git_blob_sha1"]):
            raise AuditFailure(f"invalid blob digest at {path}")
        population[path] = entry
    if len(population) != manifest["tracked_files"]:
        raise AuditFailure("inventory file count mismatch")
    if sum(entry["size_bytes"] for entry in population.values()) != manifest["tracked_bytes"]:
        raise AuditFailure("inventory byte count mismatch")
    return manifest, population


def tree_metadata(root: Path) -> dict[str, tuple[str, str, int]]:
    result = {}
    for record in git(root, "ls-tree", "-r", "-z", "-l", "HEAD").split(b"\0"):
        if not record:
            continue
        metadata, name = record.split(b"\t", 1)
        mode, kind, digest, size = metadata.split()
        if kind != b"blob" or mode not in {b"100644", b"100755"}:
            raise AuditFailure(f"unsupported tree entry: {name.decode()}")
        result[name.decode()] = (mode.decode(), digest.decode(), int(size))
    return result


def audit_source(source_root: Path, manifest_path: Path) -> dict:
    manifest, expected = load_contract(manifest_path)
    source_root = source_root.resolve(strict=True)
    actual_root = Path(git(source_root, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if actual_root != source_root:
        raise AuditFailure("source-root must be the Git checkout root")
    head = git(source_root, "rev-parse", "HEAD").decode().strip()
    if head != manifest["source_commit"]:
        raise AuditFailure(f"source commit mismatch: {head}")
    recorded = {
        path: (entry["mode"], entry["git_blob_sha1"], entry["size_bytes"])
        for path, entry in expected.items()
    }
    actual = tree_metadata(source_root)
    if actual != recorded:
        differing = sorted(
            path
            for path in actual.keys() | recorded.keys()
            if actual.get(path) != recorded.get(path)
        )
        raise AuditFailure(f"Git tree inventory mismatch: {differing[:10]}")
    # Do not pass --exclude-standard: ignored files also violate the declared
    # pristine population. No generated files are written into source_root.
    extras = git(source_root, "ls-files", "--others", "-z").split(b"\0")
    extras = [path.decode() for path in extras if path]
    if extras:
        raise AuditFailure(f"untracked or ignored files present: {extras[:10]}")
    staged = {}
    for record in git(source_root, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        metadata, name = record.split(b"\t", 1)
        mode, digest, stage = metadata.split()
        if stage != b"0":
            raise AuditFailure("unmerged Git index")
        staged[name.decode()] = (mode.decode(), digest.decode())
    if staged != {path: value[:2] for path, value in recorded.items()}:
        raise AuditFailure("Git index differs from pinned tree")
    for name, entry in expected.items():
        path = regular_file(source_root, relative_path(name))
        size = path.stat().st_size
        if size != entry["size_bytes"]:
            raise AuditFailure(f"working file size mismatch: {name}")
        digest = hashlib.sha1(b"blob " + str(size).encode() + b"\0")
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != entry["git_blob_sha1"]:
            raise AuditFailure(f"working file blob mismatch: {name}")
    top_counts = Counter(name.split("/")[0] for name in expected)
    branch_counts = Counter(
        "/".join(name.split("/")[:2])
        for name in expected
        if name.startswith("research/") and len(name.split("/")) > 2
    )
    expected_top = {row["part"]: row["file_count"] for row in manifest["top_level_coverage"]}
    expected_branches = {
        row["source_directory"]: row["file_count"] for row in manifest["research_coverage"]
    }
    if dict(top_counts) != expected_top or dict(branch_counts) != expected_branches:
        raise AuditFailure("top-level or research crosswalk population mismatch")
    declaration_count = 0
    for row in manifest["research_coverage"]:
        names = [entry["path"] for entry in row["declaration_documents"]]
        if row["primary_document"] not in names or len(names) != len(set(names)):
            raise AuditFailure("missing primary declaration or duplicate declaration document")
        for entry in row["declaration_documents"]:
            name = relative_path(entry["path"]).as_posix()
            if name not in expected or not name.startswith(row["source_directory"] + "/"):
                raise AuditFailure(
                    f"declaration is outside its inventoried research directory: {name}"
                )
            source = expected[name]
            if any(entry[key] != source[key] for key in ("git_blob_sha1", "size_bytes")):
                raise AuditFailure(f"declaration metadata mismatch: {name}")
            if digest_file(source_root / name) != entry["sha256"]:
                raise AuditFailure(f"declaration SHA-256 mismatch: {name}")
            declaration_count += 1
    return {
        "status": "PASS",
        "authority_effect": "None",
        "source_commit": head,
        "manifest_sha256": digest_file(manifest_path),
        "inventory_sha256": manifest["full_inventory"]["sha256"],
        "tracked_files_checked": len(expected),
        "tracked_bytes_checked": sum(entry["size_bytes"] for entry in expected.values()),
        "top_level_areas_checked": len(top_counts),
        "research_directories_checked": len(branch_counts),
        "declaration_documents_checked": declaration_count,
        "scope": "Git pin, complete tracked tree and index, exact working bytes, no extra files; no proof or test-suite execution",
        "tool_versions": {
            "python": platform.python_version(),
            "git": git(source_root, "--version").decode().strip(),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        result = audit_source(arguments.source_root, arguments.manifest)
        exit_status = 0
    except (
        AuditFailure,
        OSError,
        KeyError,
        TypeError,
        UnicodeError,
        json.JSONDecodeError,
    ) as error:
        result = {
            "status": "FAIL",
            "authority_effect": "None",
            "error": str(error),
            "tool_versions": {"python": platform.python_version()},
            "scope": "Source byte and population audit; stopped at the reported failure",
        }
        exit_status = 1
    result["command"] = [sys.executable, *sys.argv]
    result["exit_status"] = exit_status
    print(json.dumps(result, indent=2, sort_keys=True))
    return exit_status


if __name__ == "__main__":
    raise SystemExit(main())
