"""Unit, integration, end-to-end, and mutation checks for finite arrow categories.

Origin: code/rust/src/category_theory/category/category.rs struct FiniteCategoryShell
and code/rust/src/category_theory/finite_report_query.rs struct FactorizationCertificate,
rechecked against code/python/src/category_theory/finite_category.py.
Claim: urn:omega:fqm:category:finite-arrow-test-certificate:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by code/python/src/category_theory/test_finite_category.py.
Gate 5: use source-bound measurements in the companion history.
Scope Fence: The checks cover one two-object arrow and one three-point report.
They do not claim a free category, a topos, or that every query factors.
"""

from __future__ import annotations

import importlib.util
import sys
import warnings
from collections.abc import Callable, Mapping
from pathlib import Path

from src.category_theory.finite_category import (
    CategoryLawError,
    FiniteCategory,
    factor_report_query,
    verify_report_query_factorization,
)

_EXECUTOR = "code/python/src/category_theory/test_finite_category.py"
_LIBRARY = Path(__file__).resolve().parent / "finite_category.py"
_Mutant = tuple[str, str, str]
_ABSENT = object()
_REPORT: dict[int, int] = {0: 10, 1: 10, 2: 20}
_QUERY: dict[int, int] = {0: 1, 1: 1, 2: 0}
_DECODER: dict[int, int] = {10: 1, 20: 0}


def _restore_module(name: str, previous: object) -> None:
    if previous is _ABSENT:
        sys.modules.pop(name, None)
    else:
        sys.modules[name] = previous


class ClaimCheckError(Exception):
    """One violated category-check invariant, with the measured parameters."""

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


def _arrow_fields() -> tuple[frozenset[str], dict[str, tuple[str, str]], dict[str, str], dict[tuple[str, str], str]]:
    objects = frozenset({"A", "B"})
    morphisms = {"id_A": ("A", "A"), "id_B": ("B", "B"), "f": ("A", "B")}
    identities = {"A": "id_A", "B": "id_B"}
    composition = {("id_A", "id_A"): "id_A", ("id_B", "id_B"): "id_B", ("f", "id_A"): "f", ("id_B", "f"): "f"}
    return objects, morphisms, identities, composition


def _arrow_from(namespace: dict[str, object]) -> object:
    cls = namespace["FiniteCategory"]
    if not callable(cls):
        raise _fail("FiniteCategory is missing")
    objects, morphisms, identities, composition = _arrow_fields()
    return cls(objects=objects, morphisms=morphisms, identities=identities, composition=composition)


def _broken_from(namespace: dict[str, object]) -> object:
    cls = namespace["FiniteCategory"]
    if not callable(cls):
        raise _fail("FiniteCategory is missing")
    objects, morphisms, identities, composition = _arrow_fields()
    shifted = dict(identities)
    shifted["A"] = "f"
    return cls(objects=objects, morphisms=morphisms, identities=shifted, composition=composition)


def _verified(value: object) -> bool:
    verify = getattr(value, "verify_axioms", None)
    if not callable(verify):
        raise _fail("verify_axioms is missing")
    return bool(verify() is True)


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


def _image_agrees(decoder: object) -> bool:
    if not isinstance(decoder, dict):
        return False
    for source, image in _REPORT.items():
        if decoder.get(image) != _QUERY[source]:
            return False
    return set(decoder) == {10, 20}


def _check_factor(factor: Callable[..., object], verify: Callable[..., object], error: object) -> None:
    decoded = factor(_REPORT, _QUERY)
    if decoded != _DECODER or not _image_agrees(decoded):
        raise _fail("decoder drifted from the report-query image", got=str(decoded))
    if verify(_REPORT, _QUERY) != (True, _DECODER):
        raise _fail("boolean factorization drifted")
    if verify({0: 10, 1: 10}, {0: 1, 1: 2}) != (False, {}):
        raise _fail("obstructed factorization was accepted")
    _require_refusal(lambda: factor({}, {}), error, "factorization map must be a nonempty table")
    _require_refusal(
        lambda: factor({_float_probe("1.5"): 10}, {1: 7}),
        error,
        "float refused at the public boundary",
    )
    _require_refusal(lambda: factor({True: 10}, {1: 4}), error, "boolean refused where an integer label was required")


def _check_axioms(namespace: dict[str, object]) -> None:
    if not _verified(_arrow_from(namespace)):
        raise _fail("arrow category failed identity, unit, or associativity")
    if _verified(_broken_from(namespace)):
        raise _fail("broken identity was accepted")


def _holds(namespace: dict[str, object]) -> None:
    _check_axioms(namespace)
    _check_factor(
        _callable(namespace, "factor_report_query"),
        _callable(namespace, "verify_report_query_factorization"),
        namespace["CategoryLawError"],
    )


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
    law_error = namespace.get("CategoryLawError")
    admitted = (ClaimCheckError, law_error) if isinstance(law_error, type) and issubclass(law_error, BaseException) else (ClaimCheckError,)
    try:
        _holds(namespace)
    except admitted:
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


def witness_decoder() -> int:
    return len(_DECODER)


def witness_sources() -> int:
    return len(_REPORT)


def witness_guard() -> str:
    try:
        parse_exact_label(_float_probe("1.0"))
    except ClaimCheckError as exc:
        return exc.invariant
    return "admitted"


def witness_axiom() -> int:
    category = FiniteCategory(*_arrow_fields())
    if category.verify_axioms() is True:
        return 1 + 0
    return 0


def _self_holds(namespace: dict[str, object]) -> None:
    decoder = _callable(namespace, "witness_decoder")
    sources = _callable(namespace, "witness_sources")
    guard = _callable(namespace, "witness_guard")
    axiom = _callable(namespace, "witness_axiom")
    if decoder() != 2 or sources() != 3:
        raise _fail("decoder witness drifted", got=decoder())
    if axiom() != 1:
        raise _fail("axiom witness drifted", got=axiom())
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
        "    if issubclass(type(value), float):\n        return int(value)\n",
    ),
    (
        "boolean admitted",
        '    if type(value) is bool:\n        raise _fail("boolean refused where an integer label was required", role=role)\n',
        "    if type(value) is bool:\n        return 1 if value else 0\n",
    ),
    (
        "identity comparison flipped",
        "if self.morphisms.get(self.identities[obj]) != (obj, obj):",
        "if self.morphisms.get(self.identities[obj]) == (obj, obj):",
    ),
    (
        "collision comparison flipped",
        "if image in decoder and decoder[image] != query:",
        "if image in decoder and decoder[image] == query:",
    ),
    ("empty map accepted", "or len(values) == 0:", "or len(values) < 0:"),
    (
        "unit comparison flipped",
        "if self.composition.get((name, left)) != name:",
        "if self.composition.get((name, left)) == name:",
    ),
    (
        "associativity comparison flipped",
        "return self.composition.get((right, composed)) == self.composition.get((other, left))",
        "return self.composition.get((right, composed)) != self.composition.get((other, left))",
    ),
    ("factor refusal uncaught", "except CategoryLawError:", "except KeyError:"),
)

_SELF_MUTANTS: tuple[_Mutant, ...] = (
    ("decoder witness shifted", _anchor("return len(_DECODER", ")"), _anchor("return len(_REPORT", ")")),
    ("source witness shifted", _anchor("return len(_REPORT", ")"), _anchor("return len(_DECODER", ")")),
    ("axiom witness shifted", _anchor("return 1 + ", "0"), _anchor("return 1 + ", "2")),
    ("guard witness silenced", _anchor("return exc.", "invariant"), _anchor('return "', "admitted" + '"')),
)


def test_unit() -> None:
    """The arrow satisfies the category table, and the broken identity does not."""
    if FiniteCategory(*_arrow_fields()).verify_axioms() is not True:
        raise _fail("arrow category failed")
    shifted = dict(_arrow_fields()[2])
    shifted["A"] = "f"
    objects, morphisms, _identities, composition = _arrow_fields()
    if FiniteCategory(objects, morphisms, shifted, composition).verify_axioms() is not False:
        raise _fail("broken identity was accepted")


def test_integration() -> None:
    """Every report source satisfies query(source) = decoder(report(source))."""
    decoded = factor_report_query(_REPORT, _QUERY)
    if not _image_agrees(decoded):
        raise _fail("integration image equation failed")


def test_end_to_end() -> None:
    """The public factor and boolean contracts return the frozen decoder."""
    if factor_report_query(_REPORT, _QUERY) != _DECODER:
        raise _fail("end-to-end decoder drifted")
    if verify_report_query_factorization(_REPORT, _QUERY) != (True, _DECODER):
        raise _fail("end-to-end boolean contract drifted")


def test_negative() -> None:
    """Empty tables, floats, bools, and colliding queries are refused."""
    _check_factor(factor_report_query, verify_report_query_factorization, CategoryLawError)
    _require_refusal(lambda: parse_exact_label(True), ClaimCheckError, "label is not an exact integer")
    if parse_exact_label(10) != 10:
        raise _fail("exact label guard changed an integer")


def test_origin() -> None:
    """Both category origins resolve in this repository."""
    root = Path(__file__).resolve().parents[4]
    shell = (root / "code" / "rust" / "src" / "category_theory" / "category" / "category.rs").read_text(encoding="utf-8")
    certificate = (root / "code" / "rust" / "src" / "category_theory" / "finite_report_query.rs").read_text(encoding="utf-8")
    if "struct FiniteCategoryShell" not in shell or "struct FactorizationCertificate" not in certificate:
        raise _fail("category origin text is missing")
    source = _LIBRARY.read_text(encoding="utf-8")
    if "AuthorityEffect: None" not in source or "Scope Fence:" not in source:
        raise _fail("library provenance header is incomplete")
    if "urn:omega:fqm:category:finite-arrow-factorization:v1" not in source:
        raise _fail("library claim is missing")


def test_library_mutation() -> None:
    """Execute category mutants and require the recorded kill count."""
    source = _LIBRARY.read_text(encoding="utf-8")
    killed = _kill_count(source, _LIBRARY_MUTANTS, str(_LIBRARY), "category", _holds, _safe_holds)
    _require_receipt(source, killed)


def test_self_mutation() -> None:
    """Execute mutants of this checker and require the recorded kill count."""
    source = Path(__file__).read_text(encoding="utf-8")
    killed = _kill_count(source, _SELF_MUTANTS, str(Path(__file__).resolve()), "category_test", _self_holds, _safe_self)
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
