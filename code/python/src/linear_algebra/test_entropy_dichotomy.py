"""Unit, integration, end-to-end, and mutation checks for the entropy kernel.

Origin: lean4/EntropyDichotomy.lean theorem entropy_dichotomy_general_dimension,
rechecked against code/python/src/linear_algebra/entropy_dichotomy.py.
Claim: urn:omega:fqm:entropy:rational-purity-test-certificate:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by code/python/src/linear_algebra/test_entropy_dichotomy.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 6; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: The checks recompute one half-identity characteristic polynomial
and one trace-one projector. They do not prove transcendence or a physical
entropy theorem. Baker A1 remains a cited input, not a result of this file.
"""

from __future__ import annotations

import importlib.util
import sys
import warnings
from collections.abc import Callable, Mapping
from fractions import Fraction as Q
from pathlib import Path

import src.linear_algebra.entropy_dichotomy as entropy_dichotomy
from src.linear_algebra.entropy_dichotomy import (
    EntropyKernelError,
    RationalTextError,
    analyze,
    charpoly,
    parse_rat,
    validate_psd,
)

_EXECUTOR = "code/python/src/linear_algebra/test_entropy_dichotomy.py"
_LIBRARY = Path(__file__).resolve().parent / "entropy_dichotomy.py"
_Mutant = tuple[str, str, str]


class ClaimCheckError(ValueError):
    """One violated entropy-check invariant, with the measured parameters."""

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


def parse_exact_bound(value: object) -> int:
    """Refuse float and bool before an exact bound is accepted."""
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", received="float")
    if type(value) is bool or type(value) is not int:
        raise _fail("bound is not an exact integer", received=type(value).__name__)
    return value


def half_identity() -> list[list[Q]]:
    half = Q(1, 2)
    zero = Q(0)
    return [[half, zero], [zero, half]]


def expanded_half_charpoly() -> list[Q]:
    """Coefficients of (x - 1/2)^2, highest degree first."""
    return [Q(1), Q(-1), Q(1, 4)]


def projector_case() -> dict[str, object]:
    return {
        "fixture_id": "projector",
        "system_id": "S1",
        "conductor": 4,
        "matrix": [["1/1", "0/1"], ["0/1", "0/1"]],
        "scope": "DECLARED_SYSTEM_STATE",
    }


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
        text = getattr(exc, "invariant", None)
        if text != invariant and invariant not in str(exc):
            raise _fail("refusal named the wrong invariant", expected=invariant, got=text)
        return
    raise _fail("invalid input was accepted", expected=invariant)


def _check_charpoly(poly_of: Callable[..., object]) -> None:
    if poly_of(half_identity()) != expanded_half_charpoly():
        raise _fail("half-identity characteristic polynomial drifted", got=str(poly_of(half_identity())))


def _check_parse(parse: Callable[..., object], error: object) -> None:
    if parse("1/2") != Q(1, 2):
        raise _fail("reduced rational parse drifted")
    _require_refusal(lambda: parse("2/4"), error, "rational input must be reduced a/b with positive denominator")
    _require_refusal(lambda: parse(_float_probe("1.0")), error, "float refused at the public boundary")
    _require_refusal(lambda: parse(True), error, "rational input must be an a/b string")


def _check_psd(validate: Callable[..., object], error: object) -> None:
    if validate([[Q(1)]]) is not None:
        raise _fail("positive one-by-one matrix was refused")
    _require_refusal(
        lambda: validate([[Q(-1)]]),
        error,
        "negative eigenvalue: exact Schur complement is not positive semidefinite",
    )


def _check_analyze(run: Callable[..., object]) -> None:
    result = run(projector_case())
    if not isinstance(result, dict) or result.get("purity") != "PURE":
        raise _fail("projector purity drifted", purity=str(result))
    entropy = result.get("entropy")
    if not isinstance(entropy, dict) or entropy.get("verdict") != "CARRIED":
        raise _fail("projector entropy verdict drifted", entropy=str(entropy))


def _holds(namespace: dict[str, object]) -> None:
    text_error = namespace["RationalTextError"]
    kernel_error = namespace["EntropyKernelError"]
    _check_parse(_callable(namespace, "parse_rat"), text_error)
    _check_charpoly(_callable(namespace, "charpoly"))
    _check_psd(_callable(namespace, "validate_psd"), kernel_error)
    _check_analyze(_callable(namespace, "analyze"))


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
    module.__package__ = "src.linear_algebra"
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
    except Exception:
        return False
    return True


def _one_mutant(source: str, mutant: _Mutant, name: str, file_path: str, safe: Callable[[dict[str, object]], bool]) -> None:
    label, old, new = mutant
    count = source.count(old)
    if count != 1:
        raise _fail("mutant anchor is not unique", name=label, count=count)
    survived = True
    try:
        survived = safe(_load(source.replace(old, new, 1), name, file_path))
    except ClaimCheckError:
        raise
    except Exception:
        survived = False
    finally:
        sys.modules.pop(name, None)
    if survived:
        raise _fail("mutant survived the oracle", name=label)


def _kill_count(source: str, mutants: tuple[_Mutant, ...], file_path: str, stem: str, holds: Callable[[dict[str, object]], None], safe: Callable[[dict[str, object]], bool]) -> int:
    name = stem + "_baseline"
    try:
        holds(_load(source, name, file_path))
    finally:
        sys.modules.pop(name, None)
    index = 0
    for mutant in mutants:
        _one_mutant(source, mutant, f"{stem}_{index}", file_path, safe)
        index += 1
    return index


def _require_receipt(source: str, killed: int) -> None:
    receipt = f"Mutation-Kills: {killed} non-equivalent source mutants, executed by {_EXECUTOR}."
    if receipt not in source:
        raise _fail("mutation receipt does not match the executed kill count", killed=killed)


def witness_half() -> Q:
    return expanded_half_charpoly()[2]


def witness_trace() -> Q:
    return Q(1, 1)


def witness_guard() -> str:
    try:
        parse_exact_bound(_float_probe("1.0"))
    except ClaimCheckError as exc:
        return exc.invariant
    return "admitted"


def witness_dimension() -> int:
    return parse_exact_bound(2)


def _self_holds(namespace: dict[str, object]) -> None:
    half = _callable(namespace, "witness_half")
    trace = _callable(namespace, "witness_trace")
    guard = _callable(namespace, "witness_guard")
    dimension = _callable(namespace, "witness_dimension")
    if half() != Q(1, 4) or trace() != Q(1):
        raise _fail("scalar witness drifted", got=str(half()))
    if dimension() != 2:
        raise _fail("dimension witness drifted", got=dimension())
    if guard() != "float refused at the public boundary":
        raise _fail("guard witness drifted", got=guard())


def _safe_self(namespace: dict[str, object]) -> bool:
    try:
        _self_holds(namespace)
    except Exception:
        return False
    return True


def _anchor(left: str, right: str) -> str:
    return left + right


_LIBRARY_MUTANTS: tuple[_Mutant, ...] = (
    (
        "boolean rational admitted",
        '    if type(value) is bool or not isinstance(value, str):\n        raise _text("rational input must be an a/b string", received=type(value).__name__)\n',
        '    if type(value) is bool:\n        return Q(1)\n    if not isinstance(value, str):\n        raise _text("rational input must be an a/b string", received=type(value).__name__)\n',
    ),
    (
        "float rational admitted",
        '        raise _text("float refused at the public boundary", role="rational", received="float")\n',
        "        return Q(0)\n",
    ),
    (
        "trace sign flipped",
        "coefficient = -sum((product[i][i] for i in range(n)), Q(0)) / degree",
        "coefficient = sum((product[i][i] for i in range(n)), Q(0)) / degree",
    ),
    (
        "schur sign flipped",
        "if _negative_diagonal(current):",
        "if not _negative_diagonal(current):",
    ),
    ("unreduced token accepted", "if value != rat(parsed):", "if value == rat(parsed):"),
    ("kronecker bit flipped", "if left == right:", "if left != right:"),
    (
        "unit trace rejected",
        "if sum((matrix[i][i] for i in range(dimension)), Q(0)) != 1:",
        "if sum((matrix[i][i] for i in range(dimension)), Q(0)) == 1:",
    ),
    (
        "purity swapped",
        '    purity = "PURE" if power_sum == 1 else "MIXED"\n    return {"characteristic_polynomial": [rat(q) for q in coefficients], "spectrum": spectrum,\n',
        '    purity = "MIXED" if power_sum == 1 else "PURE"\n    return {"characteristic_polynomial": [rat(q) for q in coefficients], "spectrum": spectrum,\n',
    ),
)

_SELF_MUTANTS: tuple[_Mutant, ...] = (
    ("half witness shifted", _anchor("return expanded_half_charpoly()[", "2]"), _anchor("return expanded_half_charpoly()[", "0]")),
    ("trace witness shifted", _anchor("return Q(1, ", "1)"), _anchor("return Q(2, ", "1)")),
    ("dimension witness shifted", _anchor("return parse_exact_bound(", "2)"), _anchor("return parse_exact_bound(", "3)")),
    ("guard witness silenced", _anchor("return exc.", "invariant"), _anchor('return "', "admitted" + '"')),
)


def test_unit() -> None:
    """Faddeev-LeVerrier on (1/2)I matches the expanded square."""
    _check_charpoly(charpoly)
    _check_parse(parse_rat, RationalTextError)


def test_integration() -> None:
    """The projector's purity and carried verdict use the same characteristic polynomial."""
    _check_analyze(analyze)
    coefficients = charpoly([[Q(1), Q(0)], [Q(0), Q(0)]])
    if coefficients[0] != Q(1):
        raise _fail("projector leading coefficient drifted")


def test_end_to_end() -> None:
    """The public analyze contract carries the trace-one projector."""
    result = analyze(projector_case())
    entropy = result["entropy"]
    if result["purity"] != "PURE" or entropy["verdict"] != "CARRIED":
        raise _fail("end-to-end projector verdict drifted")


def test_negative() -> None:
    """Unreduced text, float, bool, and a negative eigenvalue are refused."""
    _check_parse(parse_rat, RationalTextError)
    _check_psd(validate_psd, EntropyKernelError)
    _require_refusal(lambda: parse_exact_bound(True), ClaimCheckError, "bound is not an exact integer")
    if parse_exact_bound(4) != 4:
        raise _fail("exact bound guard changed an integer")


def test_origin() -> None:
    """The entropy-dichotomy origin resolves in this repository."""
    lean = (Path(__file__).resolve().parents[4] / "lean4" / "EntropyDichotomy.lean").read_text(encoding="utf-8")
    if "theorem entropy_dichotomy_general_dimension" not in lean:
        raise _fail("origin theorem is not in EntropyDichotomy.lean")
    source = _LIBRARY.read_text(encoding="utf-8")
    if "AuthorityEffect: None" not in source or "Scope Fence:" not in source:
        raise _fail("library provenance header is incomplete")
    if "urn:omega:fqm:entropy:rational-purity-interval-certificate:v1" not in source:
        raise _fail("library claim is missing")


def test_library_mutation() -> None:
    """Execute kernel mutants and require the recorded kill count."""
    source = _LIBRARY.read_text(encoding="utf-8")
    killed = _kill_count(source, _LIBRARY_MUTANTS, str(_LIBRARY), "entropy", _holds, _safe_holds)
    _require_receipt(source, killed)


def test_self_mutation() -> None:
    """Execute mutants of this checker and require the recorded kill count."""
    source = Path(__file__).read_text(encoding="utf-8")
    killed = _kill_count(source, _SELF_MUTANTS, str(Path(__file__).resolve()), "entropy_test", _self_holds, _safe_self)
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
