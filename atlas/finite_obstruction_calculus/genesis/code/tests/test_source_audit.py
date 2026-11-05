"""Adversarial controls for the source custody audit, using isolated Git repos."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "genesis_source_audit", Path(__file__).resolve().parent.parent / "audit_source.py"
)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


def run_git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


@pytest.fixture
def checkout(tmp_path: Path) -> tuple[Path, Path]:
    source = tmp_path / "source"
    source.mkdir()
    run_git(source, "init", "--quiet")
    run_git(source, "config", "user.name", "Source audit fixture")
    run_git(source, "config", "user.email", "fixture@example.invalid")
    run_git(source, "config", "core.autocrlf", "false")
    (source / "research" / "example").mkdir(parents=True)
    (source / "README.md").write_bytes(b"Pinned source.\n")
    (source / "research" / "example" / "STATUS.md").write_bytes(b"A finite claim.\n")
    (source / ".gitignore").write_bytes(b"ignored*\n")
    run_git(source, "add", ".")
    run_git(source, "commit", "--quiet", "-m", "fixture")
    pin = run_git(source, "rev-parse", "HEAD")
    entries = []
    for name, (mode, digest, size) in AUDIT.tree_metadata(source).items():
        entries.append({"path": name, "mode": mode, "git_blob_sha1": digest, "size_bytes": size})
    paper = tmp_path / "paper"
    (paper / "docs").mkdir(parents=True)
    (paper / "manifests").mkdir()
    inventory = paper / "docs" / "inventory.json"
    inventory.write_text(
        json.dumps({"snapshots": {"source": {"commit": pin}}, "files": entries}),
        encoding="utf-8",
    )
    manifest = paper / "manifests" / "source_inventory.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "genesis.source_inventory.v1",
                "source_commit": pin,
                "tracked_files": len(entries),
                "tracked_bytes": sum(entry["size_bytes"] for entry in entries),
                "full_inventory": {
                    "path": "docs/inventory.json",
                    "sha256": hashlib.sha256(inventory.read_bytes()).hexdigest(),
                    "json_key": "files",
                },
                "top_level_coverage": [
                    {"part": ".gitignore", "file_count": 1},
                    {"part": "README.md", "file_count": 1},
                    {"part": "research", "file_count": 1},
                ],
                "research_coverage": [
                    {
                        "source_directory": "research/example",
                        "file_count": 1,
                        "primary_document": "research/example/STATUS.md",
                        "declaration_documents": [
                            {
                                **next(
                                    entry
                                    for entry in entries
                                    if entry["path"] == "research/example/STATUS.md"
                                ),
                                "sha256": hashlib.sha256(
                                    (source / "research/example/STATUS.md").read_bytes()
                                ).hexdigest(),
                            }
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return source, manifest


def test_exact_checkout_is_accepted_without_mutation(checkout: tuple[Path, Path]) -> None:
    source, manifest = checkout
    before = run_git(source, "status", "--porcelain", "--ignored")
    result = AUDIT.audit_source(source, manifest)
    assert result["status"] == "PASS"
    assert result["tracked_files_checked"] == 3
    assert result["research_directories_checked"] == 1
    assert run_git(source, "status", "--porcelain", "--ignored") == before == ""


@pytest.mark.parametrize(
    "failure", ["tampered", "missing", "untracked", "ignored", "staged", "wrong_pin"]
)
def test_checkout_defects_are_refused(checkout: tuple[Path, Path], failure: str) -> None:
    source, manifest = checkout
    path = source / "README.md"
    if failure == "tampered":
        path.write_bytes(b"Pinned source!\n")  # Same length; digest must detect it.
    elif failure == "missing":
        path.unlink()
    elif failure in {"untracked", "ignored"}:
        (source / failure).write_text("extra", encoding="utf-8")
    elif failure == "staged":
        run_git(source, "update-index", "--force-remove", "README.md")
    else:
        run_git(source, "commit", "--allow-empty", "--quiet", "-m", "different revision")
    with pytest.raises((AUDIT.AuditFailure, FileNotFoundError)):
        AUDIT.audit_source(source, manifest)


@pytest.mark.parametrize("location", ["file", "parent"])
def test_symlink_cannot_substitute_identical_bytes(
    checkout: tuple[Path, Path], tmp_path: Path, location: str
) -> None:
    source, manifest = checkout
    if location == "file":
        path = source / "README.md"
        target = tmp_path / "same_bytes.md"
        target.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(target)
    else:
        path = source / "research"
        target = tmp_path / "relocated_research"
        path.rename(target)
        path.symlink_to(target, target_is_directory=True)
    with pytest.raises(AUDIT.AuditFailure):
        AUDIT.audit_source(source, manifest)


def test_inventory_document_tampering_is_refused(checkout: tuple[Path, Path]) -> None:
    source, manifest = checkout
    inventory = manifest.parent.parent / "docs" / "inventory.json"
    inventory.write_text(inventory.read_text(encoding="utf-8") + " ", encoding="utf-8")
    with pytest.raises(AUDIT.AuditFailure, match="SHA-256"):
        AUDIT.audit_source(source, manifest)


@pytest.mark.parametrize(
    "location", ["manifest_file", "manifest_parent", "inventory_file", "inventory_parent"]
)
def test_control_symlink_is_refused_even_with_identical_bytes(
    checkout: tuple[Path, Path], tmp_path: Path, location: str
) -> None:
    source, manifest = checkout
    inventory = manifest.parent.parent / "docs" / "inventory.json"
    control = manifest if location.startswith("manifest") else inventory
    original = control.parent if location.endswith("parent") else control
    target = tmp_path / "relocated_control"
    original.rename(target)
    original.symlink_to(target, target_is_directory=location.endswith("parent"))
    with pytest.raises(AUDIT.AuditFailure, match="not a regular file"):
        AUDIT.audit_source(source, manifest)


@pytest.mark.parametrize("location", ["manifest", "inventory"])
def test_control_directory_cannot_replace_file(checkout: tuple[Path, Path], location: str) -> None:
    source, manifest = checkout
    control = manifest if location == "manifest" else manifest.parent.parent / "docs/inventory.json"
    control.unlink()
    control.mkdir()
    with pytest.raises(AUDIT.AuditFailure, match="not a regular file"):
        AUDIT.audit_source(source, manifest)


@pytest.mark.parametrize("location", ["manifest", "inventory", "source"])
def test_unreadable_traversal_returns_failure_receipt(
    checkout: tuple[Path, Path],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    location: str,
) -> None:
    source, manifest = checkout
    blocked = {
        "manifest": manifest.parent,
        "inventory": manifest.parent.parent / "docs",
        "source": source / "research",
    }[location]
    original_lstat = Path.lstat

    def denied_lstat(path: Path, *args, **kwargs):
        if path == blocked:
            raise PermissionError(f"injected unreadable directory: {path}")
        return original_lstat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "lstat", denied_lstat)
    monkeypatch.setattr(
        sys,
        "argv",
        [str(AUDIT.__file__), "--source-root", str(source), "--manifest", str(manifest)],
    )
    assert AUDIT.main() == 1
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["status"] == "FAIL"
    assert receipt["exit_status"] == 1
    assert "injected unreadable directory" in receipt["error"]


def test_tree_metadata_is_checked_even_with_rebound_document(checkout: tuple[Path, Path]) -> None:
    source, manifest = checkout
    inventory = manifest.parent.parent / "docs" / "inventory.json"
    document = json.loads(inventory.read_text(encoding="utf-8"))
    document["files"][0]["git_blob_sha1"] = "0" * 40
    inventory.write_text(json.dumps(document), encoding="utf-8")
    contract = json.loads(manifest.read_text(encoding="utf-8"))
    contract["full_inventory"]["sha256"] = hashlib.sha256(inventory.read_bytes()).hexdigest()
    manifest.write_text(json.dumps(contract), encoding="utf-8")
    with pytest.raises(AUDIT.AuditFailure, match="Git tree inventory mismatch"):
        AUDIT.audit_source(source, manifest)


def test_crosswalk_cannot_omit_research_directory(checkout: tuple[Path, Path]) -> None:
    source, manifest = checkout
    contract = json.loads(manifest.read_text(encoding="utf-8"))
    contract["research_coverage"] = []
    manifest.write_text(json.dumps(contract), encoding="utf-8")
    with pytest.raises(AUDIT.AuditFailure, match="crosswalk population"):
        AUDIT.audit_source(source, manifest)


def test_declaration_cannot_claim_different_bytes(checkout: tuple[Path, Path]) -> None:
    source, manifest = checkout
    contract = json.loads(manifest.read_text(encoding="utf-8"))
    contract["research_coverage"][0]["declaration_documents"][0]["sha256"] = "0" * 64
    manifest.write_text(json.dumps(contract), encoding="utf-8")
    with pytest.raises(AUDIT.AuditFailure, match="declaration SHA-256"):
        AUDIT.audit_source(source, manifest)


def test_cli_returns_failure_receipt_for_missing_source(checkout: tuple[Path, Path]) -> None:
    source, manifest = checkout
    result = subprocess.run(
        [
            sys.executable,
            str(AUDIT.__file__),
            "--source-root",
            str(source / "missing"),
            "--manifest",
            str(manifest),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    receipt = json.loads(result.stdout)
    assert receipt["status"] == "FAIL"
    assert receipt["exit_status"] == 1
