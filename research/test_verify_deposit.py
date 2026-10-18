"""Origin: test_verify_deposit.py
Claim: deposit manifest and junit gates reject hash, count, boolean, and unexecuted-test failures
AuthorityEffect: None
Scope Fence: this file does not claim the live archive matches SHA256SUMS
Level: L5
MutationKillCount: 4
"""

from __future__ import annotations

import hashlib
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

SOURCE = Path(__file__).resolve().parent / "verify_deposit.py"
_REQUIRED = (
    "finite_quantum_mechanics.md",
    "finite_quantum_mechanics.pdf",
    "finite_quantum_mechanics_change_log.md",
    "README.md",
    "LICENSE",
    "LICENSE-CODE",
    "zenodo_metadata.json",
)


def _load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _library_source() -> Path:
    bundled = SOURCE.parent / "code" / "deposit_paths.py"
    if bundled.is_file():
        return bundled
    return SOURCE.parent / "deposit_paths.py"


def _call(module: ModuleType, name: str, *args: object) -> object:
    function: object = getattr(module, name)
    if not callable(function):
        raise RuntimeError(name)
    return function(*args)


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        raise RuntimeError("expected a list")
    lines: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise RuntimeError("expected text")
        lines.append(item)
    return lines


def _raises_exact(module: ModuleType, name: str, *args: object) -> None:
    try:
        _call(module, name, *args)
    except Exception as error:
        if type(error).__name__ == "ExactIntegerError":
            return
        raise
    raise AssertionError(name)


def test_exact_guards_reject_bool_and_zero_denominator() -> None:
    module = _load(SOURCE, "verify_deposit_unit")
    _raises_exact(module, "exact_int", True)
    _raises_exact(module, "big_rational", 1, 0)
    ratio = _call(module, "big_rational", 64, 64)
    assert ratio == _call(module, "big_rational", 1, 1)
    verification = _call(module, "verify_original_count", 67)
    assert getattr(verification, "holds") is True


def test_hash_mismatch_and_original_count(tmp_path: Path) -> None:
    module = _load(SOURCE, "verify_deposit_hash")
    note = tmp_path / "note.txt"
    note.write_text("abc", encoding="utf-8")
    manifest = tmp_path / "SHA256SUMS"
    manifest.write_text(f"{'0' * 64}  note.txt\n", encoding="utf-8")
    setattr(module, "ROOT", tmp_path)
    errors = _string_list(_call(module, "check_manifest", manifest))
    assert "Hash mismatch: note.txt" in errors
    assert _string_list(_call(module, "_originals_error", tmp_path))


def test_junit_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = _load(SOURCE, "verify_deposit_junit")
    setattr(module, "ROOT", tmp_path)
    (tmp_path / "test_selected.py").write_text("def test_selected():\n    pass\n", encoding="utf-8")
    xml = '<testsuites><testsuite><testcase name="ran"/></testsuite></testsuites>'
    _stub(module, monkeypatch, xml, 0)
    assert _call(module, "check_tests", ["test_selected.py"]) == []
    _stub(module, monkeypatch, '<testsuite><testcase name="ran"><skipped/></testcase></testsuite>', 0)
    assert _string_list(_call(module, "check_tests", ["test_selected.py"]))
    assert _call(module, "check_tests", []) == ["No test files found in tests/e2e/"]


def _stub(module: ModuleType, monkeypatch: pytest.MonkeyPatch, xml: str, code: int) -> None:
    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        assert command[1:5] == ["-m", "pytest", "test_selected.py", "-q"]
        assert command[5:7] == ["-o", "xfail_strict=true"]
        assert kwargs["cwd"] == getattr(module, "ROOT")
        report = Path(next(arg.split("=", 1)[1] for arg in command if arg.startswith("--junitxml=")))
        report.write_text(xml, encoding="utf-8")
        return subprocess.CompletedProcess(command, code, "pytest summary", "")

    monkeypatch.setattr(getattr(module, "subprocess"), "run", run)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed(root: Path) -> None:
    _write(root / "code" / "deposit_paths.py", _library_source().read_text(encoding="utf-8"))
    _write(root / "verify_deposit.py", SOURCE.read_text(encoding="utf-8"))
    for name in _REQUIRED:
        _write(root / name, "x\n")
    _write(root / "pyproject.toml", "[project]\nname = \"mini\"\nversion = \"0.0.0\"\n")
    _write(root / "docs" / "descriptions.md", "d\n")
    _write(root / "docs" / "references.md", "r\n")
    index = 0
    while index < 67:
        _write(root / "sources" / "original_papers" / "pack" / f"{index}.md", "m\n")
        index = index + 1
    _write(
        root / "tests" / "e2e" / "test_mini.py",
        "def test_mini() -> None:\n    assert 1 == 1\n",
    )


def _manifest_lines(root: Path) -> None:
    module = _load(root / "code" / "deposit_paths.py", "mini_deposit_paths")
    walked = _call(module, "walk_files", root)
    if not isinstance(walked, list):
        raise RuntimeError("walk")
    lines: list[str] = []
    for item in walked:
        if not isinstance(item, Path):
            raise RuntimeError("path")
        digest = hashlib.sha256(item.read_bytes()).hexdigest()
        lines.append(f"{digest}  {item.relative_to(root).as_posix()}")
    _write(root / "SHA256SUMS", "\n".join(lines) + "\n")


def test_end_to_end_standalone_deposit(tmp_path: Path) -> None:
    _seed(tmp_path)
    _manifest_lines(tmp_path)
    result = subprocess.run(
        [sys.executable, str(tmp_path / "verify_deposit.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: Manifest and two-way sweep checks passed." in result.stdout
    assert "OK: Companion tests passed (1 files)." in result.stdout
    assert "Verification PASSED for the standalone scope only" in result.stdout


def _mutant(tmp_path: Path, label: str, old: str, new: str) -> ModuleType:
    text = SOURCE.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise AssertionError(label)
    folder = tmp_path / label
    folder.mkdir()
    shutil.copy(_library_source(), folder / "deposit_paths.py")
    (folder / "code").mkdir()
    shutil.copy(_library_source(), folder / "code" / "deposit_paths.py")
    destination = folder / "verify_deposit.py"
    destination.write_text(text.replace(old, new, 1), encoding="utf-8")
    return _load(destination, f"verify_mutant_{label}")


def test_mutation_kills(tmp_path: Path) -> None:
    killed = _kill_hash(tmp_path)
    killed = killed + _kill_originals(tmp_path)
    killed = killed + _kill_returncode(tmp_path)
    killed = killed + _kill_bool(tmp_path)
    assert killed == 4


def _kill_hash(tmp_path: Path) -> int:
    module = _mutant(
        tmp_path,
        "hash",
        "if _sha256_of(path) != digest:",
        "if False and _sha256_of(path) != digest:",
    )
    note = tmp_path / "hash" / "note.txt"
    note.write_text("abc", encoding="utf-8")
    manifest = tmp_path / "hash" / "SHA256SUMS"
    manifest.write_text(f"{'0' * 64}  note.txt\n", encoding="utf-8")
    setattr(module, "ROOT", tmp_path / "hash")
    errors = _string_list(_call(module, "check_manifest", manifest))
    if "Hash mismatch: note.txt" in errors:
        return 0
    return 1


def _kill_originals(tmp_path: Path) -> int:
    module = _mutant(
        tmp_path,
        "originals",
        "if verify_original_count(len(originals)).holds:",
        "if True:",
    )
    errors = _string_list(_call(module, "_originals_error", tmp_path))
    if errors:
        return 0
    return 1


def _kill_returncode(tmp_path: Path) -> int:
    module = _mutant(
        tmp_path,
        "returncode",
        "if result.returncode:",
        "if False and result.returncode:",
    )
    root = tmp_path / "returncode"
    root.mkdir(exist_ok=True)
    (root / "test_selected.py").write_text("def test_selected():\n    pass\n", encoding="utf-8")
    setattr(module, "ROOT", root)

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        del kwargs
        report = Path(next(arg.split("=", 1)[1] for arg in command if arg.startswith("--junitxml=")))
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text('<testsuite><testcase name="ran"/></testsuite>', encoding="utf-8")
        return subprocess.CompletedProcess(command, 1, "fail", "")

    setattr(getattr(module, "subprocess"), "run", run)
    errors = _string_list(_call(module, "check_tests", ["test_selected.py"]))
    if errors:
        return 0
    return 1


def _kill_bool(tmp_path: Path) -> int:
    module = _mutant(
        tmp_path,
        "bool",
        "if isinstance(value, bool) or not isinstance(value, int):",
        "if not isinstance(value, int):",
    )
    try:
        _call(module, "exact_int", True)
    except Exception:
        return 0
    return 1
