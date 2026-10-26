"""Regression tests for archive admission and mutation-audit evidence."""

from __future__ import annotations

import sys
import subprocess
import zipfile
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))
sys.path.insert(0, str(PACKAGE / "scripts"))

import deposit_files  # noqa: E402
import mutation_audit  # noqa: E402
import verify_deposit  # noqa: E402


@pytest.fixture
def deposit(tmp_path, monkeypatch):
    (tmp_path / "README.md").write_text("Current package\n", encoding="utf-8")
    (tmp_path / "payload.py").write_text("VALUE = 3\n", encoding="utf-8")
    (tmp_path / deposit_files.MANIFEST).write_text(
        deposit_files.render_sums(tmp_path, deposit_files.manifest_names(tmp_path)), encoding="utf-8"
    )
    deposit_files.build_archive(tmp_path / deposit_files.ARCHIVE, root=tmp_path)
    monkeypatch.setattr(verify_deposit, "ROOT", tmp_path)
    monkeypatch.setattr(verify_deposit, "manifest_names", lambda: deposit_files.manifest_names(tmp_path))
    monkeypatch.setattr(verify_deposit, "deposit_files", lambda: deposit_files.deposit_files(tmp_path))
    monkeypatch.setattr(
        verify_deposit, "REQUIRED",
        ("README.md", "payload.py", deposit_files.MANIFEST, deposit_files.SUMS, deposit_files.ARCHIVE),
    )
    refresh_outer_sums(tmp_path)
    return tmp_path


def refresh_outer_sums(root):
    names = [name for name in deposit_files.deposit_files(root) if name != deposit_files.SUMS]
    (root / deposit_files.SUMS).write_text(deposit_files.render_sums(root, names), encoding="utf-8")


def rewrite_archive(root, transform):
    path = root / deposit_files.ARCHIVE
    with zipfile.ZipFile(path) as archive:
        members = [(name, archive.read(name)) for name in archive.namelist()]
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in transform(members):
            archive.writestr(name, content)
    refresh_outer_sums(root)


def test_archive_matches_current_package(deposit):
    assert verify_deposit.check_required() == []
    assert verify_deposit.check_hashes() == []
    assert verify_deposit.check_archive() == []


def test_linter_cache_does_not_enter_manifest_or_archive(deposit):
    before = deposit_files.manifest_names(deposit)
    cache = deposit / ".ruff_cache" / "tool-version"
    cache.mkdir(parents=True)
    (cache / "local-state").write_bytes(b"host-specific cache")
    assert deposit_files.manifest_names(deposit) == before
    deposit_files.build_archive(deposit / deposit_files.ARCHIVE, root=deposit)
    assert verify_deposit.check_archive() == []


def test_outer_hash_does_not_admit_stale_archive_payload(deposit):
    rewrite_archive(
        deposit,
        lambda members: [(name, b"Stale package\n" if name.endswith("/README.md") else data)
                         for name, data in members],
    )
    assert verify_deposit.check_hashes() == []
    assert any("README.md differs" in problem for problem in verify_deposit.check_archive())


@pytest.mark.parametrize("kind", ["missing", "extra", "duplicate"])
def test_archive_rejects_incorrect_member_set(deposit, kind):
    def transform(members):
        if kind == "missing":
            return members[1:]
        if kind == "extra":
            return members + [(f"{deposit_files.ARCHIVE_ROOT}/extra.txt", b"extra")]
        return members + [members[0]]

    if kind == "duplicate":
        with pytest.warns(UserWarning, match="Duplicate name"):
            rewrite_archive(deposit, transform)
    else:
        rewrite_archive(deposit, transform)
    assert verify_deposit.check_hashes() == []
    assert verify_deposit.check_archive()


def test_archive_rejects_invalid_zip(deposit):
    (deposit / deposit_files.ARCHIVE).write_bytes(b"not a ZIP archive")
    assert any("cannot verify archive" in problem for problem in verify_deposit.check_archive())


def test_extracted_mode_checks_payload_without_external_controls(deposit):
    (deposit / deposit_files.ARCHIVE).unlink()
    (deposit / deposit_files.SUMS).unlink()
    assert len(verify_deposit.check_required()) == 2
    assert verify_deposit.check_required(extracted=True) == []
    assert verify_deposit.check_hashes(extracted=True) == []
    (deposit / "payload.py").write_text("VALUE = 4\n", encoding="utf-8")
    assert any("payload.py hash mismatch" in problem
               for problem in verify_deposit.check_hashes(extracted=True))
    (deposit / "payload.py").unlink()
    assert verify_deposit.check_required(extracted=True)


@pytest.mark.parametrize(
    ("returncode", "tests", "failures", "errors", "expected"),
    [(0, 35, 0, 0, "PASS"), (1, 35, 1, 0, "KILLED"),
     (1, 35, 0, 1, "ERROR"), (2, 1, 1, 0, "ERROR"),
     (3, 0, 0, 0, "ERROR"), (4, 0, 0, 0, "ERROR"),
     (5, 0, 0, 0, "ERROR"), (1, 0, 1, 0, "ERROR")],
)
def test_mutation_result_requires_test_failure(returncode, tests, failures, errors, expected):
    assert mutation_audit.SuiteResult(returncode, tests, failures, errors, "").classification() == expected


def test_mutation_anchors_match_current_implementation_once():
    for law, filename, old, _ in mutation_audit.MUTATIONS:
        assert (PACKAGE / "code" / filename).read_text(encoding="utf-8").count(old) == 1, law


def test_mutation_audit_refuses_failing_baseline(tmp_path, monkeypatch, capsys):
    (tmp_path / "code").mkdir()
    monkeypatch.setattr(mutation_audit, "PACKAGE", tmp_path)
    monkeypatch.setattr(mutation_audit, "run_suite",
                        lambda root: mutation_audit.SuiteResult(1, 1, 1, 0, "baseline failure"))
    assert mutation_audit.main() == 2
    assert "unchanged suite must pass" in capsys.readouterr().out


def test_mutation_audit_refuses_collection_error_after_green_baseline(tmp_path, monkeypatch, capsys):
    (tmp_path / "code").mkdir()
    (tmp_path / "code" / "fixture.py").write_text("original", encoding="utf-8")
    results = iter([mutation_audit.SuiteResult(0, 1, 0, 0, "green"),
                    mutation_audit.SuiteResult(2, 1, 0, 1, "collection error")])
    monkeypatch.setattr(mutation_audit, "PACKAGE", tmp_path)
    monkeypatch.setattr(mutation_audit, "MUTATIONS", [("fixture law", "fixture.py", "original", "mutant")])
    monkeypatch.setattr(mutation_audit, "run_suite", lambda root: next(results))
    assert mutation_audit.main() == 2
    output = capsys.readouterr().out
    assert "runner or test-report failure" in output
    assert "KILLED" not in output


@pytest.mark.parametrize(("source", "expected"), [("def test_failure():\n    assert False\n", "KILLED"),
                                                   ("def test_broken(:\n", "ERROR")])
def test_mutation_runner_distinguishes_assertion_and_collection_failure(tmp_path, source, expected):
    (tmp_path / "code").mkdir()
    (tmp_path / "code" / "test_oe_prime_algorithms.py").write_text(source, encoding="utf-8")
    assert mutation_audit.run_suite(tmp_path).classification() == expected


@pytest.mark.parametrize("filename", ["01_enter_the_triad.ipynb", "02_falsify_the_laws.ipynb"])
def test_notebook_code_cells_in_fresh_cpython(filename):
    """Exercise the printed assertions; this is not a Jupyter kernel replay."""
    path = PACKAGE / "jupyter_notebooks" / filename
    original = path.read_bytes()
    worker = """import json, sys
from pathlib import Path
path = Path(sys.argv[1])
notebook = json.loads(path.read_text(encoding="utf-8"))
namespace = {"__name__": "__main__"}
cells = 0
for index, cell in enumerate(notebook["cells"]):
    if cell["cell_type"] == "code":
        exec(compile("".join(cell["source"]), f"{path.name}:cell{index + 1}", "exec"), namespace)
        cells += 1
print(f"CPython replay: {cells} code cells completed")
"""
    result = subprocess.run([sys.executable, "-c", worker, str(path)], cwd=path.parent,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CPython replay: 5 code cells completed" in result.stdout
    assert path.read_bytes() == original
