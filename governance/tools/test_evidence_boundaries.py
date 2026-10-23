"""Regression support for bounded command ownership and reversible mutations."""
from __future__ import annotations
import importlib.util
import os
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, cast
if TYPE_CHECKING:
    from capture_evidence import CommandResult
import pytest


def load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("missing evidence tool")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


capture = load("capture_evidence")
mutation = load("mutation_campaign")


@pytest.mark.parametrize("code,output,expected", [
    (101, "error: failed to download dependency", "INCONCLUSIVE"),
    (101, "error: could not compile due to a linker failure", "INCONCLUSIVE"),
    (101, "error[E0308]: mismatched types", "INVALID"),
    (101, "test result: FAILED. 4 passed; 1 failed; 0 ignored;", "KILLED"),
    (0, "test result: ok. 5 passed; 0 failed; 0 ignored;", "SURVIVED"),
    (0, "test result: ok. 0 passed; 0 failed; 0 ignored;", "INCONCLUSIVE"),
    (101, "arbitrary failure", "INCONCLUSIVE"),
    (0, "", "INCONCLUSIVE"),
])
def test_outcomes_require_libtest_evidence(code: int, output: str, expected: str) -> None:
    assert mutation.classify_outcome(code, output) == expected


@pytest.mark.parametrize("seconds,size", [(0, 1), (-1, 1), (3601, 1), (1, 0), (1, 2**27)])
def test_invalid_limits_refused(seconds: int, size: int) -> None:
    with pytest.raises(ValueError):
        capture.Limits(seconds, size).validate()


def execute(tmp_path: Path, code: str, seconds: float = 10, size: int = 10000) -> CommandResult:
    return cast("CommandResult", capture.run([sys.executable, "-c", code], tmp_path, os.environ,
                       tmp_path / "run.log", capture.Limits(seconds, size)))


def test_command_and_exit_code(tmp_path: Path) -> None:
    result = execute(tmp_path, "print('known output'); raise SystemExit(7)")
    assert result.state == capture.State.COMPLETED
    assert result.exit_status == 7
    assert not result.passed
    assert capture.read_output(result).strip() == "known output"
    (tmp_path / "run.log").unlink()  # no leaked inherited handle


def test_timeout_releases_log(tmp_path: Path) -> None:
    result = execute(tmp_path, "import time; time.sleep(20)", seconds=0.5)
    assert result.state == capture.State.TIMEOUT
    assert result.seconds < 5
    (tmp_path / "run.log").unlink()


def test_output_limit_is_not_a_pass(tmp_path: Path) -> None:
    result = execute(tmp_path, "print('x'*100000)", size=1000)
    assert result.state == capture.State.OUTPUT_LIMIT
    assert not result.passed
    assert len(capture.read_output(result, 100)) == 100


def test_existing_log_is_preserved(tmp_path: Path) -> None:
    log = tmp_path / "run.log"
    log.write_bytes(b"original receipt")
    with pytest.raises(FileExistsError):
        execute(tmp_path, "print('replaced')")
    assert log.read_bytes() == b"original receipt"


@pytest.mark.skipif(os.name != "nt", reason="Windows job assignment failure boundary")
def test_assignment_failure_never_starts_command(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def refuse(self: object, pid: int) -> None:
        raise OSError("injected job assignment refusal")
    monkeypatch.setattr(capture.WindowsJob, "assign", refuse)
    result = execute(tmp_path, "from pathlib import Path; Path('started').write_text('bad')")
    assert result.state == capture.State.EXECUTION_ERROR
    assert "assignment refusal" in result.error
    assert not (tmp_path / "started").exists()
    (tmp_path / "run.log").unlink()


def test_child_is_terminated_when_parent_exits(tmp_path: Path) -> None:
    # Use a physical interpreter: Store activation is an external service, not a job descendant.
    direct = str(Path(sys.base_prefix) / "python.exe") if os.name == "nt" else sys.executable
    child = "import time; from pathlib import Path; time.sleep(1); Path('escaped').write_text('bad')"
    result = execute(tmp_path, f"import subprocess; subprocess.Popen([{direct!r}, '-I', '-c', {child!r}])")
    assert result.passed
    time.sleep(1.1)
    assert not (tmp_path / "escaped").exists()
    (tmp_path / "run.log").unlink()


@pytest.fixture
def crate(tmp_path: Path) -> Path:
    root = tmp_path / "crate"
    (root / "src").mkdir(parents=True)
    (root / "src/lib.rs").write_bytes(b"pub fn value() -> bool { true }\n")
    (root / "Cargo.toml").write_text("[package]\nname='fixture'\nversion='0.1.0'\n")
    (root / "clippy.toml").write_text("")
    return root


def test_mutation_restores_original_without_copy(crate: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    before = (crate / "src/lib.rs").read_bytes()
    item = next(mutation.mutants(crate))
    def fake(*args: object, **kwargs: object) -> object:
        assert b"false" in (crate / "src/lib.rs").read_bytes()
        return mutation.capture.CommandResult(("fixture",), mutation.capture.State.COMPLETED, 101,
            str(tmp_path / "test.log"), "", 0, 0)
    (tmp_path / "test.log").write_text("test result: FAILED. 0 passed; 1 failed;")
    monkeypatch.setattr(mutation.capture, "run", fake)
    with mutation.MutationSession(crate) as session:
        result = mutation.run_one(item, session, tmp_path / "unused", 1)
    assert result["outcome"] == "KILLED"
    assert (crate / "src/lib.rs").read_bytes() == before
    assert not (crate / ".mutation.lock").exists()
    assert not (crate / ".mutation.original").exists()


def test_failed_execution_still_restores(crate: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    before = (crate / "src/lib.rs").read_bytes()
    def fail(*args: object, **kwargs: object) -> object:
        raise OSError("injected execution failure")
    monkeypatch.setattr(mutation.capture, "run", fail)
    with mutation.MutationSession(crate) as session:
        with pytest.raises(OSError, match="injected"):
            mutation.run_one(next(mutation.mutants(crate)), session, tmp_path / "log", 1)
    assert (crate / "src/lib.rs").read_bytes() == before
    assert not (crate / ".mutation.lock").exists()


def test_foreign_edit_retains_recovery_bytes(crate: Path) -> None:
    original = (crate / "src/lib.rs").read_bytes()
    with mutation.MutationSession(crate) as session:
        path, before, changed = session.apply(next(mutation.mutants(crate)))
        path.write_bytes(b"other writer")
        with pytest.raises(mutation.RecoveryRequired):
            session.restore(path, before, changed)
    assert (crate / ".mutation.lock").exists()
    assert (crate / ".mutation.original").read_bytes() == original
    assert (crate / "src/lib.rs").read_bytes() == b"other writer"
    with pytest.raises(mutation.RecoveryRequired):
        with mutation.MutationSession(crate):
            pass


def test_concurrent_writer_is_refused(crate: Path) -> None:
    with mutation.MutationSession(crate):
        with pytest.raises(FileExistsError):
            with mutation.MutationSession(crate):
                pass


def test_stale_mutant_is_refused_before_edit(crate: Path) -> None:
    item = next(mutation.mutants(crate))
    (crate / "src/lib.rs").write_bytes(b"later source")
    with mutation.MutationSession(crate) as session:
        with pytest.raises(ValueError, match="different bytes"):
            session.apply(item)
    assert (crate / "src/lib.rs").read_bytes() == b"later source"
    assert not (crate / ".mutation.original").exists()


def test_exact_conservative_accounting() -> None:
    results = [{"outcome": kind} for kind in ("KILLED", "SURVIVED", "INVALID", "INCONCLUSIVE", "UNRUN")]
    summary = mutation.summarize(results)
    assert summary["killed_numerator"] == 1
    assert summary["eligible_denominator"] == 4
    assert summary["conservative_ratio"] == "1/4"
    assert mutation.summarize([])["conservative_ratio"] is None



def test_aborted_campaign_accounts_for_every_candidate(crate: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    items = list(mutation.mutants(crate)) * 3
    out = tmp_path / "evidence"
    out.mkdir()
    (out / "baseline.log").write_bytes(b"baseline")
    def fail(*args: object, **kwargs: object) -> object:
        raise OSError("deliberate failure")
    monkeypatch.setattr(mutation, "run_one", fail)
    report: dict[str, object] = {}
    with mutation.MutationSession(crate) as session:
        results = mutation.execute_items(items, session, out, 1, True, report)
    assert len(results) == len(items)
    assert results[0]["outcome"] == "INCONCLUSIVE"
    assert all(result["outcome"] == "UNRUN" for result in results[1:])
    assert mutation.summarize(results)["conservative_ratio"] == "0/3"
    assert (out / "receipt.json").exists()


def test_failed_baseline_runs_no_mutations(crate: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    items = list(mutation.mutants(crate))
    out = tmp_path / "evidence"
    out.mkdir()
    (out / "baseline.log").write_bytes(b"failure")
    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("must not mutate after baseline failure")
    monkeypatch.setattr(mutation, "run_one", forbidden)
    with mutation.MutationSession(crate) as session:
        results = mutation.execute_items(items, session, out, 1, False, {})
    assert all(result["outcome"] == "UNRUN" for result in results)
