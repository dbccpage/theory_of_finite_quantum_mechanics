"""Unit, integration, end-to-end, and mutation checks for exact counting.

Origin: code/rust/src/combinatorics/enumeration.rs function binomial,
rechecked against code/python/src/combinatorics/finite_combinatorics.py.
Claim: urn:omega:fqm:combinatorics:exact-binomial-test-certificate:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by code/python/src/combinatorics/test_finite_combinatorics.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 6; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: The factorial quotient, the ascending partition walk, and the
order polynomial (q^3-1)/(q-1) are independent checks. They do not prove that
a projective plane exists and do not prove the Weyl trace obstruction.
"""

from __future__ import annotations

import importlib.util
import sys
import warnings
from collections.abc import Callable, Mapping
from pathlib import Path

import src.combinatorics.finite_combinatorics as finite_combinatorics
from src.combinatorics.finite_combinatorics import (
    CombinatoricsBudgetError,
    CombinatoricsError,
    binomial_exact,
    enumerate_cartesian_words,
    finite_plane_parameters,
    integer_partitions,
    weyl_heisenberg_displacement_count,
)

_EXECUTOR = "code/python/src/combinatorics/test_finite_combinatorics.py"
_LIBRARY = Path(__file__).resolve().parent / "finite_combinatorics.py"
_Mutant = tuple[str, str, str]
_ABSENT = object()


def _restore_module(name: str, previous: object) -> None:
    if previous is _ABSENT:
        sys.modules.pop(name, None)
    else:
        sys.modules[name] = previous


class ClaimCheckError(ValueError):
    """One violated counting-check invariant, with the measured parameters."""

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
    if isinstance(value, float):
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


def _projective_points(order: int) -> int:
    return (order * order * order - 1) // (order - 1)


def _affine_lines(order: int) -> int:
    return order * order + order


def _displacement(dimension: int) -> tuple[int, int]:
    square = 0
    step = 0
    while step < dimension:
        square += dimension
        step += 1
    return (square, square - 1)


def _power(base: int, exponent: int) -> int:
    result = 1
    step = 0
    while step < exponent:
        result *= base
        step += 1
    return result


def _record_ascending(remain: int, cap: int, prefix: list[int], found: list[tuple[int, ...]]) -> None:
    if remain == 0:
        found.append(tuple(prefix))
        return
    _walk_ascending(remain, cap, prefix, found)


def _walk_ascending(remain: int, cap: int, prefix: list[int], found: list[tuple[int, ...]]) -> None:
    part = 1
    while part <= cap and part <= remain:
        prefix.append(part)
        _record_ascending(remain - part, part, prefix, found)
        prefix.pop()
        part += 1


def _ascending_partitions(size: int) -> list[tuple[int, ...]]:
    found: list[tuple[int, ...]] = []
    if size == 0:
        found.append(())
        return found
    _record_ascending(size, size, [], found)
    return found


def _same_parts(left: object, right: list[tuple[int, ...]]) -> bool:
    if not isinstance(left, list) or len(left) != len(right):
        return False
    return sorted(left) == sorted(right)


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


def _check_binomial(binomial: Callable[..., object]) -> None:
    if binomial(6, 3) != _factorial_choose(6, 3):
        raise _fail("binomial drifted from the factorial quotient", got=binomial(6, 3))
    if binomial(5, 7) != 0 or binomial(-1, 2) != 0:
        raise _fail("binomial outside the triangle did not return zero")
    if binomial(0, 0) != 1:
        raise _fail("empty choice drifted from one")


def _check_partitions(parts: Callable[..., object]) -> None:
    if not _same_parts(parts(4), _ascending_partitions(4)):
        raise _fail("partitions of 4 drifted from the ascending walk")
    if not _same_parts(parts(5), _ascending_partitions(5)):
        raise _fail("partitions of 5 drifted from the ascending walk")
    if parts(0) != [()]:
        raise _fail("partition of zero drifted from the empty part tuple")


def _attr(value: object, name: str) -> object:
    if not hasattr(value, name):
        raise _fail("counting record missed a field", field=name)
    return getattr(value, name)


def _check_plane(plane_of: Callable[..., object], weyl: Callable[..., object]) -> None:
    plane = plane_of(3)
    points = _projective_points(3)
    if _attr(plane, "pg_points") != points or _attr(plane, "pg_lines") != points:
        raise _fail("projective counting polynomial drifted", points=_attr(plane, "pg_points"))
    if _attr(plane, "ag_lines") != _affine_lines(3) or _attr(plane, "ag_points") != 3 * 3:
        raise _fail("affine counting polynomial drifted", lines=_attr(plane, "ag_lines"))
    if weyl(6) != _displacement(6):
        raise _fail("displacement count drifted", received=str(weyl(6)))


def _check_words(words_of: Callable[..., object], error: object) -> None:
    words = words_of(2, 3, budget=8)
    if not isinstance(words, list) or len(words) != _power(2, 3):
        raise _fail("cartesian word count drifted from iterated multiplication")
    _require_refusal(lambda: words_of(2, 3, budget=3), error, "Cartesian word count exceeds budget")


def _check_refusals(binomial: Callable[..., object], error: object) -> None:
    _require_refusal(lambda: binomial(_float_probe("1.5"), 0), error, "float refused at the public boundary")
    _require_refusal(lambda: binomial(True, False), error, "boolean refused where an integer was required")
    _require_refusal(lambda: integer_partitions(-1), CombinatoricsError, "n must be non-negative")


def _check_guard() -> None:
    _require_refusal(lambda: parse_exact_size(_float_probe("1.0")), ClaimCheckError, "float refused at the public boundary")
    _require_refusal(lambda: parse_exact_size(True), ClaimCheckError, "size is not an exact integer")


def _holds(namespace: dict[str, object]) -> None:
    error = namespace["CombinatoricsError"]
    _check_binomial(_callable(namespace, "binomial_exact"))
    _check_partitions(_callable(namespace, "integer_partitions"))
    _check_plane(_callable(namespace, "finite_plane_parameters"), _callable(namespace, "weyl_heisenberg_displacement_count"))
    _check_words(_callable(namespace, "enumerate_cartesian_words"), namespace["CombinatoricsBudgetError"])
    _check_refusals(_callable(namespace, "binomial_exact"), error)


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


def _require_baseline(source: str, file_path: str) -> None:
    name = "mutant_counting_baseline"
    previous = sys.modules.get(name, _ABSENT)
    try:
        _holds(_load(source, name, file_path))
    finally:
        _restore_module(name, previous)


def _one_mutant(source: str, mutant: _Mutant, name: str, file_path: str) -> None:
    label, old, new = mutant
    count = source.count(old)
    if count != 1:
        raise _fail("mutant anchor is not unique", name=label, count=count)
    survived = True
    previous = sys.modules.get(name, _ABSENT)
    try:
        survived = _safe_holds(_load(source.replace(old, new, 1), name, file_path))
    except ClaimCheckError:
        raise
    except Exception as error:
        raise _fail("mutant could not be assessed; not counted as a kill", name=label, error=type(error).__name__) from error
    finally:
        _restore_module(name, previous)
    if survived:
        raise _fail("mutant survived the oracle", name=label)


def _kill_count(source: str, mutants: tuple[_Mutant, ...], file_path: str, stem: str) -> int:
    _require_baseline(source, file_path)
    index = 0
    for mutant in mutants:
        _one_mutant(source, mutant, f"{stem}_{index}", file_path)
        index += 1
    return index


def _require_receipt(source: str, killed: int) -> None:
    receipt = f"Mutation-Kills: {killed} non-equivalent source mutants, executed by {_EXECUTOR}."
    if receipt not in source:
        raise _fail("mutation receipt does not match the executed kill count", killed=killed)


def witness_primary() -> int:
    return _factorial_choose(6, 3)


def witness_outside() -> int:
    return _factorial_choose(5, 7)


def witness_plane() -> int:
    return _projective_points(3)


def witness_size_guard() -> str:
    try:
        parse_exact_size(_float_probe("1.0"))
    except ClaimCheckError as exc:
        return exc.invariant
    return "admitted"


def _self_holds(namespace: dict[str, object]) -> None:
    primary = _callable(namespace, "witness_primary")
    outside = _callable(namespace, "witness_outside")
    plane = _callable(namespace, "witness_plane")
    guard = _callable(namespace, "witness_size_guard")
    if primary() != _factorial_choose(6, 3):
        raise _fail("primary witness drifted", got=primary())
    if outside() != 0:
        raise _fail("outside witness drifted", got=outside())
    if plane() != _projective_points(3):
        raise _fail("plane witness drifted", got=plane())
    if guard() != "float refused at the public boundary":
        raise _fail("size guard witness drifted", got=guard())


def _safe_self(namespace: dict[str, object]) -> bool:
    try:
        _self_holds(namespace)
    except ClaimCheckError:
        return False
    return True


def _self_baseline(source: str, file_path: str) -> None:
    name = "mutant_counting_test_baseline"
    previous = sys.modules.get(name, _ABSENT)
    try:
        _self_holds(_load(source, name, file_path))
    finally:
        _restore_module(name, previous)


def _one_self(source: str, mutant: _Mutant, name: str, file_path: str) -> None:
    label, old, new = mutant
    count = source.count(old)
    if count != 1:
        raise _fail("self mutant anchor is not unique", name=label, count=count)
    survived = True
    previous = sys.modules.get(name, _ABSENT)
    try:
        survived = _safe_self(_load(source.replace(old, new, 1), name, file_path))
    except ClaimCheckError:
        raise
    except Exception as error:
        raise _fail("self mutant could not be assessed; not counted as a kill", name=label, error=type(error).__name__) from error
    finally:
        _restore_module(name, previous)
    if survived:
        raise _fail("self mutant survived the oracle", name=label)


def _self_kill_count(source: str, mutants: tuple[_Mutant, ...], file_path: str) -> int:
    _self_baseline(source, str(Path(__file__).resolve()))
    index = 0
    for mutant in mutants:
        _one_self(source, mutant, f"self_counting_{index}", str(Path(__file__).resolve()))
        index += 1
    return index


_LIBRARY_MUTANTS: tuple[_Mutant, ...] = (
    (
        "float admitted",
        '    if isinstance(value, float):\n        raise _fail(CombinatoricsError, "float refused at the public boundary", role=role, received="float")\n',
        "    if isinstance(value, float):\n        return int(value)\n",
    ),
    (
        "boolean admitted",
        '    if type(value) is bool:\n        raise _fail(CombinatoricsError, "boolean refused where an integer was required", role=role)\n',
        "    if type(value) is bool:\n        return 1 if value else 0\n",
    ),
    (
        "integer division dropped",
        "result = result * (n - k + index) // index",
        "result = result * (n - k + index)",
    ),
    (
        "upper index accepted",
        "if left < 0 or right < 0 or right > left:",
        "if left < 0 or right < 0 or right < left:",
    ),
    (
        "empty partition dropped",
        "if size == 0:\n        return [()]",
        "if size == 0:\n        return []",
    ),
    (
        "projective point dropped",
        "points = order * order + order + 1",
        "points = order * order + order",
    ),
    (
        "traceless count dropped",
        "return (square, square - 1)",
        "return (square, square)",
    ),
    (
        "budget comparison flipped",
        "if total > limit:",
        "if total < limit:",
    ),
)

def _anchor(left: str, right: str) -> str:
    return left + right


_SELF_MUTANTS: tuple[_Mutant, ...] = (
    ("primary witness shifted", _anchor("return _factorial_choose(6, ", "3)"), _anchor("return _factorial_choose(6, ", "2)")),
    ("outside witness shifted", _anchor("return _factorial_choose(5, ", "7)"), _anchor("return _factorial_choose(5, ", "1)")),
    ("plane witness shifted", _anchor("return _projective_points(", "3)"), _anchor("return _projective_points(", "2)")),
    ("guard witness silenced", _anchor("return exc.", "invariant"), _anchor('return "', "admitted" + '"')),
)


def test_unit() -> None:
    """Factorial binomial and ascending partitions agree with the library."""
    _check_binomial(binomial_exact)
    _check_partitions(integer_partitions)


def test_integration() -> None:
    """The binomial row of order 4 sums to the cartesian power 2^4."""
    total = 0
    index = 0
    while index <= 4:
        total += binomial_exact(4, index)
        index += 1
    if total != _power(2, 4):
        raise _fail("binomial theorem power drifted", total=total)
    if len(integer_partitions(4)) != len(_ascending_partitions(4)):
        raise _fail("partition width drifted from the ascending walk")


def test_end_to_end() -> None:
    """Public counting contracts match the independent closed forms."""
    _check_plane(finite_plane_parameters, weyl_heisenberg_displacement_count)
    _check_words(enumerate_cartesian_words, CombinatoricsBudgetError)


def test_negative() -> None:
    """Float, bool, negative order, and a short budget are refused."""
    _check_refusals(binomial_exact, CombinatoricsError)
    _check_guard()
    if parse_exact_size(4) != 4:
        raise _fail("exact size guard changed an integer")


def test_origin() -> None:
    """The binomial origin resolves in this repository."""
    rust = (Path(__file__).resolve().parents[4] / "code" / "rust" / "src" / "combinatorics" / "enumeration.rs").read_text(encoding="utf-8")
    if "pub fn binomial" not in rust:
        raise _fail("origin binomial is not in enumeration.rs")
    source = _LIBRARY.read_text(encoding="utf-8")
    if "AuthorityEffect: None" not in source or "Scope Fence:" not in source:
        raise _fail("library provenance header is incomplete")
    if "urn:omega:fqm:combinatorics:exact-binomial-and-counts:v1" not in source:
        raise _fail("library claim is missing")


def test_library_mutation() -> None:
    """Execute library mutants and require the recorded kill count."""
    source = _LIBRARY.read_text(encoding="utf-8")
    killed = _kill_count(source, _LIBRARY_MUTANTS, str(_LIBRARY), "counting")
    _require_receipt(source, killed)


def test_self_mutation() -> None:
    """Execute mutants of this checker and require the recorded kill count."""
    source = Path(__file__).read_text(encoding="utf-8")
    killed = _self_kill_count(source, _SELF_MUTANTS, str(Path(__file__).resolve()))
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
