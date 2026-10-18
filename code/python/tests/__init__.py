"""Unit, integration, and negative tests for the test-package witness.

Origin: code/python/tests/__init__.py
Claim: the test-package witness (3/5)^2 + (4/5)^2 equals 1.
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

from fractions import Fraction
from pathlib import Path


def test_package_two_square() -> Fraction:
    norm = Fraction(3, 5) ** 2 + Fraction(4, 5) ** 2
    if norm != 1:
        raise ValueError("test package norm drifted")
    return norm


def _bad_norm() -> Fraction:
    norm = Fraction(2, 5) ** 2 + Fraction(4, 5) ** 2
    if norm != 1:
        raise ValueError("test package norm drifted")
    return norm


def test_unit_package_two_square() -> None:
    assert test_package_two_square() == 1
    assert type(test_package_two_square()) is Fraction


def test_negative_package_norm_refuses_drift() -> None:
    try:
        _bad_norm()
    except ValueError as caught:
        if type(caught) is not ValueError:
            raise
        return
    raise AssertionError("drift was admitted")


def test_integration_package_file_resolves() -> None:
    path = Path(__file__).resolve()
    assert path.name == "__init__.py"
    assert path.parent.name == "tests"
    assert "Mutation-Kills: 1 non-equivalent" in path.read_text(encoding="utf-8")


def _norm_holds(source: str) -> bool:
    start = source.index("def test_package_two_square")
    end = source.index("def _bad_norm")
    namespace: dict[str, object] = {"Fraction": Fraction}
    exec(compile(source[start:end], "tests_init_witness.py", "exec"), namespace)
    witness = namespace["test_package_two_square"]
    try:
        return witness() == 1
    except ValueError:
        return False


def _confirm_package_certificate() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    old = "Fraction(" + "3, 5) ** 2 + Fraction(4, 5) ** 2"
    new = "Fraction(" + "2, 5) ** 2 + Fraction(4, 5) ** 2"
    if source.count(old) != 1:
        raise AssertionError("witness expression is not unique")
    if _norm_holds(source) is False:
        raise AssertionError("baseline witness failed")
    killed = 0
    if _norm_holds(source.replace(old, new, 1)) is False:
        killed += 1
    if killed != 1:
        raise AssertionError("mutant survived")
    if "Mutation-Kills: 1 non-equivalent" not in source:
        raise AssertionError("kill count missing")
    test_unit_package_two_square()
    test_negative_package_norm_refuses_drift()
    test_integration_package_file_resolves()


_confirm_package_certificate()
