"""The Symbol Game imported by this suite is the repository package, not a copy.

Counterexample these tests name: a stale copy of ``omega_engine_pfp``
kept under ``tests/support/`` and put at the front of ``sys.path`` by the
conftest. Every ``import omega_engine_pfp`` in the suite then resolved
to the copy, and the Symbol Game architecture gate could not be collected.
"""

from __future__ import annotations

import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
SUPPORT_DIR = TESTS_DIR / "support"


def _find_repo_root(start: Path) -> Path:
    for parent in start.parents:
        if (parent / ".git").exists() or (parent / "pyproject.toml").exists():
            return parent
    return start.parents[5]


REPO_ROOT = _find_repo_root(TESTS_DIR)


def _norm(path: str | Path) -> str:
    return str(Path(path).resolve()).casefold()


def test_no_copy_of_the_symbol_game_package_lives_in_this_test_tree() -> None:
    copies = sorted(
        str(path.relative_to(TESTS_DIR))
        for path in TESTS_DIR.rglob("omega_engine_pfp")
        if path.is_dir()
    )
    assert copies == []


def test_the_support_directory_is_not_on_sys_path() -> None:
    support = _norm(SUPPORT_DIR)
    on_path = [entry for entry in sys.path if entry and _norm(entry) == support]
    assert on_path == []


def test_the_symbol_game_resolves_to_the_repository_package() -> None:
    import omega_engine_pfp

    expected = REPO_ROOT / "omega_engine_pfp" / "__init__.py"
    assert _norm(omega_engine_pfp.__file__) == _norm(expected)
