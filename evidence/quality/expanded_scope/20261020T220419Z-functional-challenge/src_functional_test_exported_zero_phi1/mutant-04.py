"""Unit, integration, end-to-end, and mutation checks for the zero Phi1 export.

Origin: lean4/DerivationDagQMClosure.lean theorem
l1_gs001_replica_and_phi1_quotient_invariance, recomputed by
code/python/src/functional/__init__.py.
Claim: urn:omega:fqm:phi1:exported-zero-test-certificate:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by code/python/src/functional/test_exported_zero_phi1.py.
Gate 5: use source-bound measurements in the companion history.
Scope Fence: The checker certifies one zero residual on the boundary column
(1, -1) with weights (1, 1). It does not select L1 over a rival seminorm.
"""

from __future__ import annotations

import importlib.util
import sys
import warnings
from collections.abc import Callable, Mapping
from fractions import Fraction
from pathlib import Path

from src.functional import exported_zero_phi1
from src.functional.l1_seminorm import L1SeminormError, evaluate_weighted_l1_quotient

_EXECUTOR = "code/python/src/functional/test_exported_zero_phi1.py"
_LIBRARY = Path(__file__).resolve().parent / "__init__.py"
_PACKAGE = "src.functional"
_Mutant = tuple[str, str, str]
_ABSENT = object()
_BOUNDARY = (Fraction(1), Fraction(-1))
_WEIGHTS = (Fraction(1), Fraction(1))
_ZERO = Fraction(0)


def _restore_module(name: str, previous: object) -> None:
    if previous is _ABSENT:
        sys.modules.pop(name, None)
    else:
        sys.modules[name] = previous


class ClaimCheckError(ValueError):
    """One violated Phi1-check invariant, with the measured parameters."""

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


def parse_exact_entry(value: object) -> int:
    """Refuse float and bool before an exact witness entry is accepted."""
    if issubclass(type(value), float):
        raise _fail("float refused at the public boundary", received="float")
    if type(value) is bool or type(value) is not int:
        raise _fail("witness entry is not an exact integer", received=type(value).__name__)
    return value


def certified_zero() -> Fraction:
    """Independent primal-dual check that the zero section has Phi1 zero."""
    total = Fraction(0)
    index = 0
    while index < 2:
        repair = _BOUNDARY[index] * _ZERO
        if _ZERO != _ZERO - repair:
            raise _fail("primal residual identity failed", index=index)
        if abs(_ZERO) > _WEIGHTS[index]:
            raise _fail("dual box identity failed", index=index)
        total += _WEIGHTS[index] * abs(_ZERO)
        index += 1
    pairing = _BOUNDARY[0] * _ZERO + _BOUNDARY[1] * _ZERO
    if pairing != 0 or total != _ZERO:
        raise _fail("duality identity failed", pairing=str(pairing), total=str(total))
    return total


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
    expected = certified_zero()
    if export() != expected:
        raise _fail("exported zero Phi1 drifted", got=str(export()))
    _require_refusal(
        lambda: export(((_float_probe("1.5"), 0), (-1, 0))),
        error,
        "float refused at the public boundary",
    )
    _require_refusal(lambda: export(((True, 0), (-1, 0))), error, "boolean refused where an integer witness entry was required")
    _require_refusal(
        lambda: export(((1, 1), (-1, 0))),
        error,
        "zero Phi1 witness must be a single boundary column",
    )
    _require_refusal(
        lambda: export(((1, 0), (-1, 0)), ((1, 2), (1, 1))),
        error,
        "zero Phi1 weights must be a repeated positive pair",
    )


def _holds(namespace: dict[str, object]) -> None:
    _check_export(_callable(namespace, "exported_zero_phi1"), namespace["L1SeminormError"])


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


def witness_zero() -> Fraction:
    return certified_zero()


def witness_pair() -> int:
    return len(_BOUNDARY)


def witness_guard() -> str:
    try:
        parse_exact_entry(_float_probe("1.0"))
    except ClaimCheckError as exc:
        return "admitted"
    return "admitted"


def witness_weight() -> Fraction:
    return _WEIGHTS[0]


def _self_holds(namespace: dict[str, object]) -> None:
    zero = _callable(namespace, "witness_zero")
    pair = _callable(namespace, "witness_pair")
    guard = _callable(namespace, "witness_guard")
    weight = _callable(namespace, "witness_weight")
    if zero() != Fraction(0):
        raise _fail("zero witness drifted", got=str(zero()))
    if pair() != 2 or weight() != 1:
        raise _fail("shape witness drifted", got=pair())
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
        '    if type(value) is bool:\n        raise _fail("boolean refused where an integer witness entry was required", role=role)\n',
        "    if type(value) is bool:\n        return 1 if value else 0\n",
    ),
    (
        "column gate flipped",
        "if rows[0][1] != 0 or rows[1][1] != 0:",
        "if rows[0][1] == 0 or rows[1][1] == 0:",
    ),
    (
        "weight gate flipped",
        "if rows[0][0] != rows[0][1] or rows[1][0] != rows[1][1]:",
        "if rows[0][0] == rows[0][1] or rows[1][0] == rows[1][1]:",
    ),
    ("reported value shifted", "        [0, 0],\n        0,\n    )\n", "        [0, 0],\n        1,\n    )\n"),
    ("alpha shifted", "        [0],\n", "        [1],\n"),
    ("pair length flipped", "or len(row) != 2:", "or len(row) == 2:"),
    ("row length flipped", "or len(value) != 2:", "or len(value) == 2:"),
)

_SELF_MUTANTS: tuple[_Mutant, ...] = (
    ("zero witness shifted", _anchor("return certified_", "zero()"), _anchor("return Fraction(", "1)")),
    ("pair witness shifted", _anchor("return len(_BOUN", "DARY)"), _anchor("return len(_BOUN", "DARY) + 1")),
    ("weight witness shifted", _anchor("return _WEI", "GHTS[0]"), _anchor("return _WEI", "GHTS[0] + 1")),
    ("guard witness silenced", _anchor("return exc.", "invariant"), _anchor('return "', "admitted" + '"')),
)


def test_unit() -> None:
    """The independent certificate and the export are both zero."""
    if exported_zero_phi1() != certified_zero():
        raise _fail("unit zero certificate drifted")


def test_integration() -> None:
    """The export agrees with the neighbor's weighted quotient on the same witness."""
    neighbor = evaluate_weighted_l1_quotient([[1], [-1]], [1, 1], [0, 0], [0], [0, 0], [0, 0], 0)
    if neighbor != exported_zero_phi1():
        raise _fail("export and weighted quotient diverged", neighbor=str(neighbor))


def test_end_to_end() -> None:
    """The default public call returns the zero rational."""
    if exported_zero_phi1() != Fraction(0):
        raise _fail("end-to-end zero drifted", got=str(exported_zero_phi1()))


def test_negative() -> None:
    """Float, bool, a wide row, and an unrepeated weight are refused."""
    _check_export(exported_zero_phi1, L1SeminormError)
    _require_refusal(lambda: parse_exact_entry(True), ClaimCheckError, "witness entry is not an exact integer")
    if parse_exact_entry(1) != 1:
        raise _fail("exact entry guard changed an integer")


def test_origin() -> None:
    """The Phi1 origin resolves in this repository."""
    lean = (Path(__file__).resolve().parents[4] / "lean4" / "DerivationDagQMClosure.lean").read_text(encoding="utf-8")
    if "theorem l1_gs001_replica_and_phi1_quotient_invariance" not in lean:
        raise _fail("origin theorem is not in DerivationDagQMClosure.lean")
    source = _LIBRARY.read_text(encoding="utf-8")
    if "AuthorityEffect: None" not in source or "Scope Fence:" not in source:
        raise _fail("library provenance header is incomplete")
    if "urn:omega:fqm:phi1:exported-zero-quotient:v1" not in source:
        raise _fail("library claim is missing")


def test_library_mutation() -> None:
    """Execute export mutants and require the recorded kill count."""
    source = _LIBRARY.read_text(encoding="utf-8")
    killed = _kill_count(source, _LIBRARY_MUTANTS, str(_LIBRARY), "phi1", _holds, _safe_holds)
    _require_receipt(source, killed)


def test_self_mutation() -> None:
    """Execute mutants of this checker and require the recorded kill count."""
    source = Path(__file__).read_text(encoding="utf-8")
    killed = _kill_count(source, _SELF_MUTANTS, str(Path(__file__).resolve()), "phi1_test", _self_holds, _safe_self)
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
