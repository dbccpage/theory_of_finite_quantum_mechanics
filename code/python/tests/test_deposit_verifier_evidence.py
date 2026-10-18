"""A successful pytest exit alone must not certify unexecuted deposit tests."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def verifier(tmp_path, monkeypatch):
    repo_root = Path(__file__).resolve().parents[3]
    source = repo_root / "verify_deposit.py"
    if not source.exists():
        source = repo_root / "research" / "verify_deposit.py"
    spec = importlib.util.spec_from_file_location("finite_qm_deposit_test_gate", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load verifier: {source}")
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    (tmp_path / "test_selected.py").write_text("def test_selected(): pass\n", encoding="utf-8")
    return module


def stub_pytest(verifier, monkeypatch, xml, returncode=0):
    def run(command, **kwargs):
        assert command[1:5] == ["-m", "pytest", "test_selected.py", "-q"]
        assert command[5:7] == ["-o", "xfail_strict=true"]
        assert kwargs["cwd"] == verifier.ROOT
        report = Path(next(arg.split("=", 1)[1] for arg in command if arg.startswith("--junitxml=")))
        if xml is not None:
            report.write_text(xml, encoding="utf-8")
        return subprocess.CompletedProcess(command, returncode, "pytest summary", "")

    monkeypatch.setattr(verifier.subprocess, "run", run)


def test_executed_passing_cases_are_accepted(verifier, monkeypatch):
    stub_pytest(verifier, monkeypatch, '<testsuites><testsuite><testcase name="ran"/></testsuite></testsuites>')
    assert verifier.check_tests(["test_selected.py"]) == []


@pytest.mark.parametrize("report", [
    None,
    "not XML",
    "<testsuites><testsuite tests=\"10\"/></testsuites>",
    '<other><testcase name="ran"/></other>',
    '<testsuites><testsuite><testcase name="skipped"><skipped/></testcase></testsuite></testsuites>',
    '<testsuites><testsuite><testcase name="failed"><failure/></testcase></testsuite></testsuites>',
    '<testsuites><testsuite><testcase name="error"><error/></testcase></testsuite></testsuites>',
])
def test_exit_zero_cannot_replace_executed_test_evidence(verifier, monkeypatch, report):
    stub_pytest(verifier, monkeypatch, report)
    assert verifier.check_tests(["test_selected.py"])


def test_nonzero_pytest_exit_is_not_overridden_by_a_green_report(verifier, monkeypatch):
    stub_pytest(verifier, monkeypatch, '<testsuite><testcase name="ran"/></testsuite>', returncode=1)
    assert verifier.check_tests(["test_selected.py"])
