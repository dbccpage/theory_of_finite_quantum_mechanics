"""Public-contract checks for the frozen binomial witness C(6, 3) = 20.

Origin: code/rust/src/combinatorics/enumeration.rs function binomial,
rechecked against code/python/src/combinatorics/__init__.py.
Claim: urn:omega:fqm:combinatorics:exported-binomial-test-certificate:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by code/python/src/combinatorics/test_exported_binomial.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 6; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: exported_binomial is checked only on the pair (6, 3). The
factorial quotient is an independent arithmetic check. No plane existence
and no Weyl trace obstruction is claimed.
"""

from __future__ import annotations

import importlib.util
import sys
import warnings
from collections.abc import Callable, Mapping
from pathlib import Path

from src.combinatorics import exported_binomial
from src.combinatorics.finite_combinatorics import CombinatoricsError, binomial_exact

_EXECUTOR = "code/python/src/combinatorics/test_exported_binomial.py"
_LIBRARY = Path(__file__).resolve().parent / "__init__.py"
_PACKAGE = "src.combinatorics"
_Mutant = tuple[str, str, str]
_ABSENT = object()


def _restore_module(name: str, previous: object) -> None:
    if previous is _ABSENT:
        sys.modules.pop(name, None)
    else:
        sys.modules[name] = previous


class ClaimCheckError(ValueError):
    """One violated export-check invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ClaimCheckError:
    return ClaimCheckError(invariant, parameters)


def _float_probe(text: str) -> object:
    import ast as ast_mod

    value = ast_mod.literal_eval(text)
    if type(value).__name__ in {"int", "bool"}:
        raise _fail("admitted scalar is not a refusal probe", received=type(value).__name__)
    return value


def parse_exact_size(value: object) -> int:
    """Refuse float and bool before an exact size is accepted."""
    if issubclass(type(value), float):
        raise _fail("float refused at the public boundary", received="float")
    if type(value) is bool or type(value) is not int:
        raise _fail("size is not an exact integer", received=type(value).__name__)
    return value


def _factorial(n: int) -> int:
    result = 1
    index = 1
    while index <= n:
        result *= index
        index += 1
    return result


def _factorial_choose(n: int, k: int) -> int:
    if n < 0 or k < 0 or k > n:
        return 0
    return _factorial(n) // (_factorial(k) * _factorial(n - k))


def _as_error(value: object) -> type[BaseException]:
    if isinstance(value, type) and issubclass(value, BaseException):
        return value
    raise _fail("error class missing", received=type(value).__name__)


def _callable(namespace: dict[str, object], name: str) -> Callable[..., object]:
    value = namespace[name]
    if not callable(value):
        raise _fail("required callable is missing", name=name)
    return value


def _require_refusal(probe: Callable[[], object], error: object, invariant: str) -> None:
    caught = _as_error(error)
    try:
        probe()
    except caught as exc:
        if getattr(exc, "invariant", None) != invariant:
            raise _fail("refusal named the wrong invariant", expected=invariant, got=getattr(exc, "invariant", None))
        return
    raise _fail("invalid input was accepted", expected=invariant)


def _check_export(export: Callable[..., object], error: object) -> None:
    expected = _factorial_choose(6, 3)
    if export() != expected or export(6, 3) != binomial_exact(6, 3):
        raise _fail("exported binomial drifted from the factorial quotient", got=export())
    _require_refusal(lambda: export(5, 2), error, "exported binomial witness is only (6, 3)")
    _require_refusal(lambda: export(_float_probe("6.0"), 3), error, "float refused at the public boundary")
    _require_refusal(lambda: export(True, False), error, "boolean refused where an integer was required")


def _holds(namespace: dict[str, object]) -> None:
    _check_export(_callable(namespace, "exported_binomial"), namespace["CombinatoricsError"])


def _exec_module(module: object, source: str, name: str) -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        exec(compile(source, name + ".py", "exec"), module.__dict__)


def _load(source: str, name: str, file_path: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise _fail("mutant module spec was not allocated", name=name)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = file_path
    module.__package__ = _PACKAGE
    sys.modules[name] = module
    try:
        _exec_module(module, source, name)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module.__dict__


def _safe_holds(namespace: dict[str, object]) -> bool:
    try:
        _holds(namespace)
    except (ClaimCheckError, ValueError, ArithmeticError, AssertionError):
        return False
    return True


def _require_baseline(source: str) -> None:
    name = "mutant_export_baseline"
    previous = sys.modules.get(name, _ABSENT)
    try:
        _holds(_load(source, name, str(_LIBRARY)))
    finally:
        _restore_module(name, previous)


def _one_mutant(source: str, mutant: _Mutant, name: str) -> None:
    label, old, new = mutant
    count = source.count(old)
    if count != 1:
        raise _fail("mutant anchor is not unique", name=label, count=count)
    survived = True
    previous = sys.modules.get(name, _ABSENT)
    try:
        survived = _safe_holds(_load(source.replace(old, new, 1), name, str(_LIBRARY)))
    except ClaimCheckError:
        raise
    except Exception as error:
        survived = False
    finally:
        _restore_module(name, previous)
    if survived:
        raise _fail("mutant survived the oracle", name=label)


def _kill_count(source: str, mutants: tuple[_Mutant, ...], stem: str) -> int:
    _require_baseline(source)
    index = 0
    for mutant in mutants:
        _one_mutant(source, mutant, f"{stem}_{index}")
        index += 1
    return index


def _require_receipt(source: str, killed: int) -> None:
    receipt = f"Mutation-Kills: {killed} non-equivalent source mutants, executed by {_EXECUTOR}."
    if receipt not in source:
        raise _fail("mutation receipt does not match the executed kill count", killed=killed)


def witness_primary() -> int:
    return _factorial_choose(6, 3)


def witness_outside() -> int:
    return _factorial_choose(5, 2)


def witness_library() -> int:
    return binomial_exact(6, 3)


def witness_size_guard() -> str:
    try:
        parse_exact_size(_float_probe("1.0"))
    except ClaimCheckError as exc:
        return exc.invariant
    return "admitted"


def _self_holds(namespace: dict[str, object]) -> None:
    primary = _callable(namespace, "witness_primary")
    outside = _callable(namespace, "witness_outside")
    library = _callable(namespace, "witness_library")
    guard = _callable(namespace, "witness_size_guard")
    if primary() != 20 or library() != _factorial_choose(6, 3):
        raise _fail("primary witness drifted", got=primary())
    if outside() != 10:
        raise _fail("outside witness drifted", got=outside())
    if guard() != "float refused at the public boundary":
        raise _fail("size guard witness drifted", got=guard())


def _safe_self(namespace: dict[str, object]) -> bool:
    try:
        _self_holds(namespace)
    except ClaimCheckError:
        return False
    return True


def _one_self(source: str, mutant: _Mutant, name: str) -> None:
    label, old, new = mutant
    count = source.count(old)
    if count != 1:
        raise _fail("self mutant anchor is not unique", name=label, count=count)
    survived = True
    previous = sys.modules.get(name, _ABSENT)
    try:
        survived = _safe_self(_load(source.replace(old, new, 1), name, str(Path(__file__).resolve())))
    except ClaimCheckError:
        raise
    except Exception as error:
        raise _fail("self mutant could not be assessed; not counted as a kill", name=label, error=type(error).__name__) from error
    finally:
        _restore_module(name, previous)
    if survived:
        raise _fail("self mutant survived the oracle", name=label)


def _self_kill_count(source: str, mutants: tuple[_Mutant, ...]) -> int:
    name = "mutant_export_test_baseline"
    previous = sys.modules.get(name, _ABSENT)
    try:
        _self_holds(_load(source, name, str(Path(__file__).resolve())))
    finally:
        _restore_module(name, previous)
    index = 0
    for mutant in mutants:
        _one_self(source, mutant, f"self_export_{index}")
        index += 1
    return index


def _anchor(left: str, right: str) -> str:
    return left + right


_LIBRARY_MUTANTS: tuple[_Mutant, ...] = (
    (
        "float admitted",
        '    if issubclass(type(value), float):\n        raise _fail("float refused at the public boundary", role=role, received="float")\n',
        "    if issubclass(type(value), float):\n        return int(value)\n",
    ),
    (
        "boolean admitted",
        '    if type(value) is bool:\n        raise _fail("boolean refused where an integer was required", role=role)\n',
        '    if type(value) is bool:\n        return 6 if role == "n" else 3\n',
    ),
    ("pair gate flipped", "if (left, right) != (6, 3):", "if (left, right) == (6, 3):"),
    ("value gate flipped", "if value != 20:", "if value == 20:"),
    ("partition gate flipped", "if len(integer_partitions(4)) != 5:", "if len(integer_partitions(4)) == 5:"),
    (
        "plane gate flipped",
        "if plane.pg_points != 13 or plane.ag_lines != 12:",
        "if plane.pg_points == 13 or plane.ag_lines == 12:",
    ),
    (
        "displacement gate flipped",
        "if weyl_heisenberg_displacement_count(6) != (36, 35):",
        "if weyl_heisenberg_displacement_count(6) == (36, 35):",
    ),
    (
        "export incremented",
        "    value = binomial_exact(left, right)\n    _require_neighbors(value)\n    return value\n",
        "    value = binomial_exact(left, right)\n    _require_neighbors(value)\n    return value + 1\n",
    ),
)

_SELF_MUTANTS: tuple[_Mutant, ...] = (
    ("primary witness shifted", _anchor("return _factorial_choose(6, ", "3)"), _anchor("return _factorial_choose(6, ", "2)")),
    ("outside witness shifted", _anchor("return _factorial_choose(5, ", "2)"), _anchor("return _factorial_choose(5, ", "1)")),
    ("library witness shifted", _anchor("return binomial_exact(6, ", "3)"), _anchor("return binomial_exact(6, ", "2)")),
    ("guard witness silenced", _anchor("return exc.", "invariant"), _anchor('return "', "admitted" + '"')),
)


def test_unit() -> None:
    """The export equals the factorial quotient C(6, 3)."""
    if exported_binomial() != _factorial_choose(6, 3):
        raise _fail("unit export drifted")


def test_integration() -> None:
    """The export agrees with the multiplicative binomial in the neighbor module."""
    if exported_binomial(6, 3) != binomial_exact(6, 3):
        raise _fail("export and binomial_exact diverged")


def test_end_to_end() -> None:
    """The default public call is the frozen witness 20."""
    if exported_binomial() != 20:
        raise _fail("end-to-end witness drifted", got=exported_binomial())


def test_negative() -> None:
    """A foreign pair, a float, and a bool are refused."""
    _check_export(exported_binomial, CombinatoricsError)
    _require_refusal(lambda: parse_exact_size(_float_probe("1.0")), ClaimCheckError, "float refused at the public boundary")
    if parse_exact_size(6) != 6:
        raise _fail("exact size guard changed an integer")


def test_origin() -> None:
    """The binomial origin resolves in this repository."""
    rust = (Path(__file__).resolve().parents[4] / "code" / "rust" / "src" / "combinatorics" / "enumeration.rs").read_text(encoding="utf-8")
    if "pub fn binomial" not in rust:
        raise _fail("origin binomial is not in enumeration.rs")
    source = _LIBRARY.read_text(encoding="utf-8")
    if "AuthorityEffect: None" not in source or "Scope Fence:" not in source:
        raise _fail("library provenance header is incomplete")
    if "urn:omega:fqm:combinatorics:exported-binomial-six-three:v1" not in source:
        raise _fail("library claim is missing")


def test_library_mutation() -> None:
    """Execute export mutants and require the recorded kill count."""
    source = _LIBRARY.read_text(encoding="utf-8")
    killed = _kill_count(source, _LIBRARY_MUTANTS, "export")
    _require_receipt(source, killed)


def test_self_mutation() -> None:
    """Execute mutants of this checker and require the recorded kill count."""
    source = Path(__file__).read_text(encoding="utf-8")
    killed = _self_kill_count(source, _SELF_MUTANTS)
    _require_receipt(source, killed)


def _main() -> None:
    test_unit()
    test_integration()
    test_end_to_end()
    test_negative()
    test_origin()
    test_library_mutation()
    test_self_mutation()


if __name__ == "__main__":
    _main()
