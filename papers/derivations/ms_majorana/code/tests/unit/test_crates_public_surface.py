"""Every name `omega_engine.crates` advertises must actually resolve.

`__all__` listed five names with no corresponding package. Four of them
(`contracts`, `operator_algebra`, `representation`, `solvers`) raised
`ModuleNotFoundError` from `__getattr__` on first access, so the package
advertised a public surface that did not exist. They were stale spellings of
`contract_core`, `operator` and `solver`, plus one crate that is Rust-only.

Listing a name is a promise. This test is the promise being kept.

AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib

import pytest

import omega_engine.crates as crates

_CRATES_DIR = pathlib.Path(crates.__file__).resolve().parent


def test_all_is_not_empty() -> None:
    """Guard the degenerate fix: emptying __all__ would pass everything below."""
    assert len(crates.__all__) > 40


def test_all_has_no_duplicates() -> None:
    assert len(crates.__all__) == len(set(crates.__all__))


@pytest.mark.parametrize("name", sorted(crates.__all__))
def test_every_advertised_name_resolves(name: str) -> None:
    module = getattr(crates, name)
    assert module is not None


@pytest.mark.parametrize("name", sorted(crates.__all__))
def test_every_advertised_name_has_a_home(name: str) -> None:
    """Either a directory here, or a documented re-home elsewhere.

    `symbol_game` is the one deliberate exception: it is special-cased onto
    `omega_engine_pfp.domain`, which is a real package at a different
    path.
    """
    if name == "symbol_game":
        module = getattr(crates, name)
        assert "omega_engine_pfp" in module.__name__
        return
    assert (_CRATES_DIR / name).is_dir(), f"{name} has no package directory"


def test_retired_spellings_stay_retired() -> None:
    """No alias was added for the removed names, per move-rewrite-delete."""
    for retired in ("contracts", "operator_algebra", "representation", "solvers"):
        assert retired not in crates.__all__
        with pytest.raises(AttributeError):
            getattr(crates, retired)


def test_the_real_names_are_the_ones_advertised() -> None:
    """The packages the retired spellings pointed at do exist under their own names."""
    for real in ("contract_core", "operator", "solver"):
        assert real in crates.__all__
        assert getattr(crates, real) is not None
