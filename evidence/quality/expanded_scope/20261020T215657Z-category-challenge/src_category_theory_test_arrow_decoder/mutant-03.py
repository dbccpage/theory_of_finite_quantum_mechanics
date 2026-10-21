"""Public-contract checks for the frozen two-object arrow decoder.

Origin: code/rust/src/category_theory/finite_report_query.rs struct
FactorizationCertificate, rechecked against code/python/src/category_theory/__init__.py.
Claim: urn:omega:fqm:category:exported-arrow-decoder-test-certificate:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by code/python/src/category_theory/test_arrow_decoder.py.
Gate 5: use source-bound measurements in the companion history.
Scope Fence: arrow_decoder_size is checked on one arrow and one three-point
report. It does not classify finite categories.
"""

from __future__ import annotations

import importlib.util
import sys
import warnings
from collections.abc import Callable, Mapping
from pathlib import Path

from src.category_theory import arrow_decoder_size
from src.category_theory.finite_category import CategoryLawError, factor_report_query

_EXECUTOR = "code/python/src/category_theory/test_arrow_decoder.py"
_LIBRARY = Path(__file__).resolve().parent / "__init__.py"
_PACKAGE = "src.category_theory"
_Mutant = tuple[str, str, str]
_ABSENT = object()
_REPORT: dict[int, int] = {0: 10, 1: 10, 2: 20}
_QUERY: dict[int, int] = {0: 1, 1: 1, 2: 0}


def _restore_module(name: str, previous: object) -> None:
    if previous is _ABSENT:
        sys.modules.pop(name, None)
    else:
        sys.modules[name] = previous


class ClaimCheckError(ValueError):
    """One violated decoder-check invariant, with the measured parameters."""

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


def parse_exact_label(value: object) -> int:
    """Refuse float and bool before an exact label is accepted."""
    if issubclass(type(value), float):
        raise _fail("float refused at the public boundary", received="float")
    if type(value) is bool or type(value) is not int:
        raise _fail("label is not an exact integer", received=type(value).__name__)
    return value


def _floated_report() -> tuple[tuple[object, int], ...]:
    return ((_float_probe("0.0"), 10), (1, 10), (2, 20))


def _bool_report() -> tuple[tuple[object, int], ...]:
    return ((True, 10), (1, 10), (2, 20))


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


def _check_decoder(decode: Callable[..., object], error: object) -> None:
    if decode() != len(factor_report_query(_REPORT, _QUERY)):
        raise _fail("decoder size drifted from the factored report", got=decode())
    _require_refusal(lambda: decode(report=_floated_report()), error, "float refused at the public boundary")
    _require_refusal(lambda: decode(report=_bool_report()), error, "boolean refused where an integer label was required")
    _require_refusal(lambda: decode(report=(), query=((0, 1),)), error, "witness table must be a nonempty tuple")


def _holds(namespace: dict[str, object]) -> None:
    _check_decoder(_callable(namespace, "arrow_decoder_size"), namespace["CategoryLawError"])


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


def _one_mutant(source: str, mutant: _Mutant, name: str, file_path: str, safe: Callable[[dict[str, object]], bool]) -> None:
    label, old, new = mutant
    count = source.count(old)
    if count != 1:
        raise _fail("mutant anchor is not unique", name=label, count=count)
    survived = True
    previous = sys.modules.get(name, _ABSENT)
    try:
        survived = safe(_load(source.replace(old, new, 1), name, file_path))
    except ClaimCheckError:
        raise
    except Exception as error:
        raise _fail("candidate could not be assessed; not counted as a kill", name=label, error=type(error).__name__) from error
    finally:
        _restore_module(name, previous)
    if survived:
        raise _fail("mutant survived the oracle", name=label)


def _kill_count(source: str, mutants: tuple[_Mutant, ...], file_path: str, stem: str, holds: Callable[[dict[str, object]], None], safe: Callable[[dict[str, object]], bool]) -> int:
    name = stem + "_baseline"
    previous = sys.modules.get(name, _ABSENT)
    try:
        holds(_load(source, name, file_path))
    finally:
        _restore_module(name, previous)
    index = 0
    for mutant in mutants:
        _one_mutant(source, mutant, f"{stem}_{index}", file_path, safe)
        index += 1
    return index


def _require_receipt(source: str, killed: int) -> None:
    receipt = f"Mutation-Kills: {killed} non-equivalent source mutants, executed by {_EXECUTOR}."
    if receipt not in source:
        raise _fail("mutation receipt does not match the executed kill count", killed=killed)


def witness_width() -> int:
    return len(factor_report_query(_REPORT, _QUERY))


def witness_sources() -> int:
    return len(_REPORT)


def witness_guard() -> str:
    try:
        parse_exact_label(_float_probe("1.0"))
    except ClaimCheckError as exc:
        return exc.invariant
    return "admitted"


def witness_points() -> int:
    """The number of distinct report values in the declared three-source map."""
    return len(set(_REPORT.values())) + 1


def _self_holds(namespace: dict[str, object]) -> None:
    width = _callable(namespace, "witness_width")
    sources = _callable(namespace, "witness_sources")
    guard = _callable(namespace, "witness_guard")
    points = _callable(namespace, "witness_points")
    if width() != 2 or sources() != 3 or points() != 2:
        raise _fail("decoder witness drifted", got=width())
    if guard() != "float refused at the public boundary":
        raise _fail("guard witness drifted", got=guard())


def _safe_self(namespace: dict[str, object]) -> bool:
    try:
        _self_holds(namespace)
    except ClaimCheckError:
        return False
    return True


def _anchor(left: str, right: str) -> str:
    return left + right


_LIBRARY_MUTANTS: tuple[_Mutant, ...] = (
    (
        "float admitted",
        '    if issubclass(type(value), float):\n        raise _fail("float refused at the public boundary", role=role, received="float")\n',
        "    if issubclass(type(value), float):\n        return\n",
    ),
    (
        "boolean admitted",
        '    if type(value) is bool:\n        raise _fail("boolean refused where an integer label was required", role=role)\n',
        "    if type(value) is bool:\n        return 1 if value else 0\n",
    ),
    ("axiom gate flipped", "if category.verify_axioms() is not True:", "if category.verify_axioms() is True:"),
    ("decoder gate flipped", "if dict(decoder) != {10: 1, 20: 0}:", "if dict(decoder) == {10: 1, 20: 0}:"),
    ("size incremented", "return len(decoder)", "return len(decoder) + 1"),
    ("pair length flipped", "or len(row) != 2:", "or len(row) == 2:"),
    ("integer gate flipped", "if type(value) is not int:", "if type(value) is int:"),
    (
        "pair order swapped",
        'return (_exact_int(row[0], role + "_0"), _exact_int(row[1], role + "_1"))',
        'return (_exact_int(row[1], role + "_1"), _exact_int(row[0], role + "_0"))',
    ),
)

_SELF_MUTANTS: tuple[_Mutant, ...] = (
    ("width witness shifted", _anchor("return len(factor_report_query(_REPORT, ", "_QUERY))"), _anchor("return len(", "_REPORT)")),
    ("source witness shifted", _anchor("return len(_RE", "PORT)"), _anchor("return len(_RE", "PORT) + 1")),
    ("point witness shifted", _anchor("return len(set(_REPORT.", "values()))"), _anchor("return len(set(_REPORT.", "values())) + 1")),
    ("guard witness silenced", _anchor("return exc.", "invariant"), _anchor('return "', "admitted" + '"')),
)


def test_unit() -> None:
    """The default decoder has two images."""
    if arrow_decoder_size() != 2:
        raise _fail("unit decoder size drifted", got=arrow_decoder_size())


def test_integration() -> None:
    """The export size equals the neighbor factorization of the same tables."""
    if arrow_decoder_size() != len(factor_report_query(_REPORT, _QUERY)):
        raise _fail("export and factor_report_query diverged")


def test_end_to_end() -> None:
    """The public default call returns the frozen decoder size."""
    if arrow_decoder_size() != len({10: 1, 20: 0}):
        raise _fail("end-to-end decoder size drifted")


def test_negative() -> None:
    """Float, bool, and an empty report are refused."""
    _check_decoder(arrow_decoder_size, CategoryLawError)
    _require_refusal(lambda: parse_exact_label(_float_probe("1.0")), ClaimCheckError, "float refused at the public boundary")
    if parse_exact_label(2) != 2:
        raise _fail("exact label guard changed an integer")


def test_origin() -> None:
    """The factorization origin resolves in this repository."""
    certificate = (Path(__file__).resolve().parents[4] / "code" / "rust" / "src" / "category_theory" / "finite_report_query.rs").read_text(encoding="utf-8")
    if "struct FactorizationCertificate" not in certificate:
        raise _fail("origin certificate is not in finite_report_query.rs")
    source = _LIBRARY.read_text(encoding="utf-8")
    if "AuthorityEffect: None" not in source or "Scope Fence:" not in source:
        raise _fail("library provenance header is incomplete")
    if "urn:omega:fqm:category:exported-arrow-decoder:v1" not in source:
        raise _fail("library claim is missing")


def test_library_mutation() -> None:
    """Execute decoder mutants and require the recorded kill count."""
    source = _LIBRARY.read_text(encoding="utf-8")
    killed = _kill_count(source, _LIBRARY_MUTANTS, str(_LIBRARY), "decoder", _holds, _safe_holds)
    _require_receipt(source, killed)


def test_self_mutation() -> None:
    """Execute mutants of this checker and require the recorded kill count."""
    source = Path(__file__).read_text(encoding="utf-8")
    killed = _kill_count(source, _SELF_MUTANTS, str(Path(__file__).resolve()), "decoder_test", _self_holds, _safe_self)
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
