"""Regression checks for the read-only changed-source contract boundary.

Origin: scripts/test_changed_since_contracts.py
Claim: isolated CLI and API checks include Git index, worktree and untracked changes,
refuse missing/invalid companions, and leave audit bytes and timestamps untouched.
AuthorityEffect: None. This suite does not score or certify the repository estate.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
from types import ModuleType

import pytest

Subjects = tuple[ModuleType, ModuleType]

SOURCE = Path(__file__).resolve().parent


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load test subject")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def subjects(tmp_path: Path) -> Subjects:
    """Use a private Git repository, including for the real isolated CLI."""
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    shutil.copyfile(SOURCE.parent / "SCORING.md", tmp_path / "SCORING.md")
    for name in ("contract_scores.py", "score_scope_contracts.py"):
        shutil.copyfile(SOURCE / name, scripts / name)
    (tmp_path / "code/python").mkdir(parents=True)
    audit = tmp_path / "evidence/contract_score_coverage_scope_audit.json"
    audit.parent.mkdir()
    audit.write_text('{"fixture": true}\n', encoding="utf-8")
    git(tmp_path, "init")
    git(tmp_path, "config", "user.email", "review@example.invalid")
    git(tmp_path, "config", "user.name", "Local test")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "fixture")
    return (load(scripts / "contract_scores.py", "review_scores"),
            load(scripts / "score_scope_contracts.py", "review_scope"))


def stamp(scope: ModuleType) -> tuple[int, int, bytes]:
    path = scope.AUDIT_PATH
    stat = path.stat()
    return stat.st_mtime_ns, stat.st_size, path.read_bytes()


def test_clean_change_passes_without_writing_the_audit(subjects: Subjects) -> None:
    scores, scope = subjects
    before = stamp(scope)
    assert scope.main(["check", "--changed-since", "HEAD"]) == 0
    scores.main(["check", "--changed-since", "HEAD"])
    assert stamp(scope) == before


def test_missing_companion_on_a_changed_source_is_refused(subjects: Subjects) -> None:
    scores, scope = subjects
    before = stamp(scope)
    (scope.ROOT / "code/python/probe.py").write_text("probe = 1\n", encoding="utf-8")
    assert scope.main(["check", "--changed-since", "HEAD"]) == 1
    with pytest.raises(SystemExit) as caught:
        scores.main(["check", "--changed-since", "HEAD"])
    assert caught.value.code == 1
    assert stamp(scope) == before


def test_empty_change_set_does_not_read_invalid_companion(subjects: Subjects) -> None:
    scores, scope = subjects
    (scope.ROOT / "code/python/probe.contract.score.yaml").write_text("{broken", encoding="utf-8")
    scores.check(changed=set())


def test_named_invalid_companion_is_refused(subjects: Subjects) -> None:
    scores, scope = subjects
    name = "code/python/probe.contract.score.yaml"
    (scope.ROOT / name).write_text("{broken", encoding="utf-8")
    with pytest.raises(SystemExit) as caught:
        scores.check(changed={name})
    assert caught.value.code == 1


def test_prepare_rejects_changed_since(subjects: Subjects) -> None:
    _, scope = subjects
    with pytest.raises(SystemExit) as caught:
        scope.main(["prepare", "--changed-since", "HEAD"])
    assert caught.value.code == 2


def test_documented_isolated_cli_does_not_need_a_script_search_path(subjects: Subjects) -> None:
    scores, scope = subjects
    before = stamp(scope)
    completed = subprocess.run(
        [sys.executable, "-I", "-X", "utf8", str(scores.ROOT / "scripts/contract_scores.py"),
         "check", "--changed-since", "HEAD"],
        cwd=scores.ROOT, capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert json.loads(completed.stdout)["all_passed"] is True
    assert stamp(scope) == before


def test_git_scope_includes_index_worktree_and_untracked(subjects: Subjects) -> None:
    _, scope = subjects
    root = scope.ROOT
    source = root / "code/python"
    for name in ("staged.py", "unstaged.py", "companion.py", "deleted.py"):
        (source / name).write_text("value = 1\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-m", "sources")
    (source / "staged.py").write_text("value = 2\n", encoding="utf-8")
    git(root, "add", "code/python/staged.py")
    (source / "unstaged.py").write_text("value = 3\n", encoding="utf-8")
    (source / "untracked.py").write_text("value = 4\n", encoding="utf-8")
    (source / "companion.contract.score.yaml").write_text("{}\n", encoding="utf-8")
    (source / "deleted.py").unlink()
    base, names = scope.changed_paths("HEAD")
    assert base == git(root, "rev-parse", "HEAD")
    assert names == {"code/python/" + name for name in (
        "staged.py", "unstaged.py", "untracked.py", "companion.contract.score.yaml", "deleted.py")}
    assert {p.name for p in scope.sources_in_change(names)} == {
        "staged.py", "unstaged.py", "untracked.py", "companion.py"}


def test_invalid_comparison_ref_fails_closed(subjects: Subjects) -> None:
    _, scope = subjects
    with pytest.raises(subprocess.CalledProcessError):
        scope.changed_paths("refs/heads/does-not-exist-review-fixture")



def test_valid_companion_then_changed_source_is_refused(subjects: Subjects) -> None:
    scores, scope = subjects
    source = scope.ROOT / "code/python/probe.py"
    source.write_text("value = 1\n", encoding="utf-8")
    assert scope.prepare_source(source)
    assert scope.main(["check", "--changed-since", "HEAD"]) == 0
    scores.main(["check", "--changed-since", "HEAD"])
    before = stamp(scope)
    source.write_text("value = 2\n", encoding="utf-8")
    assert scope.main(["check", "--changed-since", "HEAD"]) == 1
    assert stamp(scope) == before


def test_tampered_history_is_refused(subjects: Subjects) -> None:
    scores, scope = subjects
    source = scope.ROOT / "code/python/probe.py"
    source.write_text("value = 1\n", encoding="utf-8")
    scope.prepare_source(source)
    companion = scope.companion_for(source)
    document = json.loads(companion.read_text(encoding="utf-8"))
    document["contract_history"][0]["raw_utf8"] += "\n"
    companion.write_text(json.dumps(document), encoding="utf-8")
    assert scope.main(["check", "--changed-since", "HEAD"]) == 1
    with pytest.raises(SystemExit) as caught:
        scores.main(["check", "--changed-since", "HEAD"])
    assert caught.value.code == 1


def test_legacy_bytes_round_trip_without_recreating_sidecar(subjects: Subjects) -> None:
    scores, scope = subjects
    source = scope.ROOT / "code/python/probe.py"
    source.write_text("value = 1\n", encoding="utf-8")
    legacy = source.with_suffix(".contract.yaml")
    raw = b"claim: fixture\r\nAuthorityEffect: None\r\n"
    scores.write_legacy(legacy, raw)
    assert not legacy.exists()
    assert scores.read_bytes(legacy) == raw
    logical = scores.RecordPath(legacy)
    assert logical.is_file()
    assert logical.read_text(encoding="utf-8", newline="") == raw.decode("utf-8")
    assert logical.read_text(encoding="utf-8") == raw.decode("utf-8").replace("\r\n", "\n")


def test_record_path_reads_live_newline_mode(subjects: Subjects) -> None:
    scores, scope = subjects
    path = scope.ROOT / "live.txt"
    path.write_bytes(b"a\r\nb\r\n")
    assert scores.RecordPath(path).read_text(encoding="utf-8", newline="") == "a\r\nb\r\n"
