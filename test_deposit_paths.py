"""Origin: test_deposit_paths.py
Claim: deposit path, manifest, and rational-width checks reject every listed invariant failure
AuthorityEffect: None
Scope Fence: this file does not claim the deposit archive is complete
Level: L5
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import deposit_paths as paths


def test_exact_integer_guard_rejects_bool_and_text() -> None:
    with pytest.raises(paths.ExactIntegerError):
        paths.exact_int(True)
    with pytest.raises(paths.ExactIntegerError):
        paths.exact_int("1")
    with pytest.raises(paths.ExactIntegerError):
        paths.exact_nat(-1)
    with pytest.raises(paths.ExactIntegerError):
        paths.big_rational(1, 0)
    assert paths.big_rational(2, 4) == paths.big_rational(1, 2)
    assert paths.verify_digest_width("a" * 64).holds
    assert not paths.verify_digest_width("aa").holds


def test_safe_path_accepts_relative_parts(tmp_path: Path) -> None:
    chosen = paths.safe_path(tmp_path, "dir/note.txt")
    assert chosen == tmp_path.absolute() / "dir" / "note.txt"


@pytest.mark.parametrize(
    "relative",
    ["", "..", "../x", "foo/../bar", "/abs", "a\\b", "a:b", "CON", "foo.", "a/b ", "ok\nname"],
)
def test_safe_path_rejects_unsafe_syntax(tmp_path: Path, relative: str) -> None:
    with pytest.raises(ValueError, match="unsafe deposit path"):
        paths.safe_path(tmp_path, relative)


def test_safe_path_rejects_non_text(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unsafe deposit path"):
        paths.safe_path(tmp_path, paths._relative_text(True))


def test_safe_path_rejects_linked_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(paths, "_link", lambda _path: True)
    with pytest.raises(ValueError, match="symlink or junction in deposit root"):
        paths.safe_path(tmp_path, "note.txt")


def test_walk_and_manifest_roundtrip(tmp_path: Path) -> None:
    kept = tmp_path / "sources" / "original_papers" / "packet"
    kept.mkdir(parents=True)
    (kept / "one.md").write_text("body", encoding="utf-8")
    (tmp_path / "sources" / "other").mkdir()
    (tmp_path / "sources" / "other" / "skip.md").write_text("no", encoding="utf-8")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("x", encoding="utf-8")
    (tmp_path / "note.pyc").write_bytes(b"x")
    (tmp_path / "claim_ledger_extra.md").write_text("x", encoding="utf-8")
    found = paths.walk_files(tmp_path)
    relative = [item.relative_to(tmp_path).as_posix() for item in found]
    assert relative == ["sources/original_papers/packet/one.md"]
    digest = paths.sha256_of(found[0])
    manifest = tmp_path / "sha256sums"
    manifest.write_text(f"{digest.upper()}  sources/original_papers/packet/one.md\n", encoding="utf-8")
    entries = paths.read_manifest(tmp_path, manifest)
    assert entries == [("sources/original_papers/packet/one.md", digest)]


def test_manifest_negative_lines(tmp_path: Path) -> None:
    target = tmp_path / "note.txt"
    target.write_text("body", encoding="utf-8")
    manifest = tmp_path / "sha256sums"
    manifest.write_text("not-a-digest\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed manifest line"):
        paths.read_manifest(tmp_path, manifest)
    digest = paths.sha256_of(target)
    manifest.write_text(
        f"{digest}  note.txt\n{digest}  note.txt\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate or case-colliding"):
        paths.read_manifest(tmp_path, manifest)
    manifest.write_text(f"{digest}  archive.zip\n", encoding="utf-8")
    with pytest.raises(ValueError, match="circular manifest entry"):
        paths.read_manifest(tmp_path, manifest)


def test_case_collision_is_rejected(tmp_path: Path) -> None:
    first = tmp_path / "Same.txt"
    first.write_text("body", encoding="utf-8")
    seen: set[str] = set()
    files: list[Path] = []
    paths._take_file(tmp_path, first, set(), set(), seen, files)
    with pytest.raises(ValueError, match="case-colliding deposit path"):
        paths._take_file(tmp_path, tmp_path / "same.txt", set(), set(), seen, files)


def _load_mutant(text: str, name: str) -> ModuleType:
    path = ROOT / f"_mutant_{name}.py"
    path.write_text(text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    path.unlink()
    return module


def _accepted(call: Callable[[], object]) -> bool:
    try:
        call()
    except ValueError:
        return False
    return True


def test_mutation_kills_are_recorded(tmp_path: Path) -> None:
    source = (ROOT / "deposit_paths.py").read_text(encoding="utf-8")
    mutants = {
        "trail": (
            'if part.rstrip(" .") != part:\n        return True',
            'if False and part.rstrip(" .") != part:\n        return True',
        ),
        "reserved": ('"CON",', ""),
        "control": (
            "return any(ord(char) < 32 for char in relative)",
            "return False and any(ord(char) < 32 for char in relative)",
        ),
        "link": ("if _link(ancestor):", "if False and _link(ancestor):"),
        "collision": ("if key in seen:", "if False and key in seen:"),
        "digest": ("return relative, digest.lower()", "return relative, digest"),
        "denom": ("if den == 0:", "if den == 1:"),
        "bool": (
            "if isinstance(value, bool) or not isinstance(value, int):",
            "if not isinstance(value, int):",
        ),
        "evidence": ('"evidence",', ""),
    }
    killed = _count_kills(source, mutants, tmp_path)
    assert killed == 9
    assert "MutationKillCount: 9" in source


def _count_kills(source: str, mutants: dict[str, tuple[str, str]], tmp_path: Path) -> int:
    killed = 0
    for name, (old, new) in mutants.items():
        if source.count(old) != 1:
            raise AssertionError(name)
        module = _load_mutant(source.replace(old, new, 1), f"deposit_mut_{name}")
        if not _killed(module, name, tmp_path / name):
            raise AssertionError(name)
        killed += 1
    return killed


def _killed(module: ModuleType, name: str, tmp_path: Path) -> bool:
    tmp_path.mkdir()
    if name in {"trail", "reserved", "control"}:
        sample = {"trail": "foo.", "reserved": "CON", "control": "ok\nname"}[name]
        return _accepted(lambda: module.safe_path(tmp_path, sample))
    if name == "link":
        root_abs = tmp_path.absolute()

        def only_root(path: Path) -> bool:
            return path == root_abs

        setattr(module, "_link", only_root)
        return _accepted(lambda: module.safe_path(tmp_path, "note.txt"))
    if name == "collision":
        return _collision_accepted(module, tmp_path)
    if name == "digest":
        return _digest_kept_case(module, tmp_path)
    if name == "denom":
        return _call_failed(lambda: module.big_rational(1, 1))
    if name == "bool":
        return _call_ok(lambda: module.exact_int(True))
    return _evidence_walked(module, tmp_path)


def _collision_accepted(module: ModuleType, tmp_path: Path) -> bool:
    target = tmp_path / "Same.txt"
    target.write_text("body", encoding="utf-8")
    seen: set[str] = set()
    module._take_file(tmp_path, target, set(), set(), seen, [])
    return _accepted(lambda: module._take_file(tmp_path, tmp_path / "same.txt", set(), set(), seen, []))


def _digest_kept_case(module: ModuleType, tmp_path: Path) -> bool:
    target = tmp_path / "note.txt"
    target.write_text("body", encoding="utf-8")
    digest: object = module.sha256_of(target)
    if not isinstance(digest, str):
        return False
    manifest = tmp_path / "sha256sums"
    manifest.write_text(f"{digest.upper()}  note.txt\n", encoding="utf-8")
    entries: object = module.read_manifest(tmp_path, manifest)
    if not isinstance(entries, list) or not entries:
        return False
    first: object = entries[0]
    if not isinstance(first, tuple) or len(first) < 2:
        return False
    stored: object = first[1]
    return stored != digest


def _evidence_walked(module: ModuleType, tmp_path: Path) -> bool:
    hidden = tmp_path / "evidence"
    hidden.mkdir()
    (hidden / "note.txt").write_text("x", encoding="utf-8")
    found: object = module.walk_files(tmp_path)
    if not isinstance(found, list):
        return False
    return len(found) != 0


def _call_failed(call: Callable[[], object]) -> bool:
    try:
        call()
    except (ValueError, ZeroDivisionError):
        return True
    return False


def _call_ok(call: Callable[[], object]) -> bool:
    try:
        call()
    except ValueError:
        return False
    return True
