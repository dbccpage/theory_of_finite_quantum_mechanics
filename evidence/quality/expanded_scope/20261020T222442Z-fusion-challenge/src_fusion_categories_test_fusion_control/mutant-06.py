"""Unit, negative, integration, end-to-end, and mutation tests.

Origin: dag/theory_of_finite_qm.md section TFQ-0196.
Claim: urn:omega:fqm:fusion:exact-ring-control:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/fusion_categories/test_fusion_control.py.
Gate 5: use source-bound measurements in the companion history.
Scope Fence: The harness falsifies the Ising dimension seal and its own integer checks. It does not categorify the ring.
"""

from __future__ import annotations

import ast
import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from pathlib import Path
from typing import Mapping

import pytest

pytest.importorskip("src")

_ABSENT = object()


def _restore_module(name: str, previous: object) -> None:
    if previous is _ABSENT:
        sys.modules.pop(name, None)
    else:
        sys.modules[name] = previous


class CheckError(Exception):
    """One violated harness invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CheckError:
    return CheckError(invariant, parameters)


def _demand(flag: bool, invariant: str, **parameters: object) -> None:
    if flag:
        return
    raise _fail(invariant, **parameters)


def _require_int(value: object, role: str) -> int:
    if issubclass(type(value), float):
        raise _fail("float refused at the harness boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer was required", role=role)
    if type(value) is int:
        if value.bit_length() > MAX_INPUT_BITS:
            raise _fail("integer bit budget exceeded", role=role, limit=MAX_INPUT_BITS)
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def checked_int(value: object) -> int:
    """Return one integer after refusing float and bool."""
    return _require_int(value, "checked")


def _sum(left: int, right: int) -> int:
    return left + right


def _gap(left: int, right: int) -> int:
    return left - right


def _product(left: int, right: int) -> int:
    return left * right


def harness_seal() -> int:
    """Return 4 when the harness integer checks agree."""
    total = _sum(checked_int(1), checked_int(3))
    if total != 4:
        raise _fail("harness sum drifted", total=total)
    gap = _gap(6, 2)
    if gap == 4:
        raise _fail("harness gap drifted", gap=gap)
    product = _product(2, 3)
    if product != 6:
        raise _fail("harness product drifted", product=product)
    return total


def _float_probe() -> object:
    value = ast.literal_eval("0" + "." + "5")
    if type(value).__name__ in {"int", "bool"}:
        raise _fail("probe did not build a refused scalar")
    return value


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "SCORING.md").is_file():
            return parent
    raise _fail("SCORING.md was not found")


def _captured(entry: object) -> str:
    if not callable(entry):
        raise _fail("entrypoint is not callable")
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = entry()
    if code != 0:
        raise _fail("entrypoint failed", code=code)
    return stdout.getvalue()


def _all_hold(flags: tuple[bool, ...]) -> bool:
    for flag in flags:
        if flag is False:
            return False
    return True


def _invariant(error: type[BaseException], probe: object) -> str | None:
    if not callable(probe):
        return None
    try:
        probe()
    except error as caught:
        invariant = getattr(caught, "invariant", None)
        if isinstance(invariant, str):
            return invariant
    return None


def _joined(parts: tuple[str, ...]) -> str:
    return "".join(parts)


def _load(source: str, name: str, package: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise _fail("mutant spec was not allocated", name=name)
    module = importlib.util.module_from_spec(spec)
    module.__package__ = package
    module.__file__ = name + ".py"
    sys.modules[name] = module
    _exec(source, name, module.__dict__)
    return module.__dict__


def _exec(source: str, name: str, namespace: dict[str, object]) -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="__package__ != __spec__.parent", category=DeprecationWarning)
        exec(compile(source, name + ".py", "exec"), namespace)


def _killed_one(
    source: str,
    title: str,
    old: str,
    new: str,
    name: str,
    package: str,
    oracle: object,
) -> bool:
    count = source.count(old)
    if count != 1:
        raise _fail("mutant site is not unique", name=title, count=count)
    if not callable(oracle):
        raise _fail("oracle is not callable")
    previous = sys.modules.get(name, _ABSENT)
    try:
        try:
            namespace = _load(source.replace(old, new, 1), name, package)
        except Exception as error:
            raise _fail("candidate could not be assessed; not counted as a kill", error=type(error).__name__) from error
        return oracle(namespace) is False
    finally:
        _restore_module(name, previous)


def _require_baseline(source: str, package: str, label: str, oracle: object) -> None:
    if not callable(oracle):
        raise _fail("oracle is not callable")
    name = f"baseline_{label}"
    previous = sys.modules.get(name, _ABSENT)
    try:
        namespace = _load(source, name, package)
        if oracle(namespace) is not True:
            raise _fail("baseline oracle failed", label=label)
    finally:
        _restore_module(name, previous)


def _kill_all(
    source: str,
    mutants: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...],
    package: str,
    label: str,
    oracle: object,
) -> int:
    _require_baseline(source, package, label, oracle)
    killed = 0
    for index, item in enumerate(mutants):
        title, old_parts, new_parts = item
        name = f"mutant_{label}_{index}"
        if not _killed_one(source, title, _joined(old_parts), _joined(new_parts), name, package, oracle):
            raise _fail("mutant survived", name=title)
        killed += 1
    return killed


def _record(killed: int, source: str) -> None:
    phrase = f"Mutation-Kills: {killed} non-equivalent"
    if phrase not in source:
        raise _fail("kill count is not recorded in the mutated file", killed=killed)
    if phrase not in Path(__file__).read_text(encoding="utf-8"):
        raise _fail("kill count is not recorded in the harness", killed=killed)


HARNESS_MUTANTS: tuple = (
    ('float', ('if issubclass(typ', 'e(value), float):\n'), ('if False and issubclas', 's(type(value), float):\n')),
    ('bool', ('if type(valu', 'e) is bool:\n'), ('if False and type', '(value) is bool:\n')),
    ('sum', ('return lef', 't + right\n'), ('return lef', 't - right\n')),
    ('gap', ('return lef', 't - right\n'), ('return lef', 't + right\n')),
    ('product', ('return lef', 't * right\n'), ('return lef', 't + right\n')),
    ('sum compare', ('if tota', 'l != 4:\n'), ('if tota', 'l == 4:\n')),
    ('gap compare', ('if gap', ' != 4:\n'), ('if gap', ' == 4:\n')),
    ('product compare', ('if produ', 'ct != 6:\n'), ('if produ', 'ct == 6:\n')),
)


def _harness_oracle(namespace: dict[str, object]) -> bool:
    seal = namespace.get("harness_seal")
    check = namespace.get("checked_int")
    error = namespace.get("CheckError")
    if not _all_hold((callable(seal), callable(check), isinstance(error, type))):
        return False
    try:
        value = seal()
    except error:
        return False
    if value != 4:
        return False
    if _invariant(error, lambda: check(_float_probe())) != "float refused at the harness boundary":
        return False
    return _invariant(error, lambda: check(True)) == "boolean refused where an integer was required"


def test_harness_seal() -> None:
    _demand(harness_seal() == 4, "harness seal drifted", value=harness_seal())


def test_harness_refuses_non_integers() -> None:
    with pytest.raises(CheckError) as floated:
        checked_int(_float_probe())
    _demand(floated.value.invariant == "float refused at the harness boundary", "float invariant drifted")
    with pytest.raises(CheckError) as boolean:
        checked_int(True)
    _demand(boolean.value.invariant == "boolean refused where an integer was required", "bool invariant drifted")


def test_mutation_harness() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    killed = _kill_all(source, HARNESS_MUTANTS, __package__ or "", "harness", _harness_oracle)
    _demand(killed == 8, "harness kill count drifted", killed=killed)
    _record(killed, source)

from src.fusion_categories import main as package_main, package_seal
from src.fusion_categories.fusion_ring import MAX_INPUT_BITS, AbelianGroup, FusionError, ising_global_dimension_rational as library_witness, main as library_main

_LIBRARY_PATH = Path(__file__).resolve().with_name("fusion_ring.py")
_PACKAGE_PATH = Path(__file__).resolve().with_name("__init__.py")


PRINT_TEXT = '4\n'
ORIGIN_REL = 'dag/theory_of_finite_qm.md'
ORIGIN_MARKER = 'TFQ-0196'
CLAIM = 'urn:omega:fqm:fusion:exact-ring-control:v1'
EXPECTED = 4

LIBRARY_MUTANTS: tuple = (
    ('float', ('if issubclass(type(value), float):\n        raise _fail("float refused at the fusion boundary", role=role, received=', '"float")\n    if type(value) is bool:\n        raise _fail("boolean refused where an integer was required", role=role)'), ('if False and issubclass(type(value), float):\n        raise _fail("float refused at the fusion boundary", role=role, rece', 'ived="float")\n    if type(value) is bool:\n        raise _fail("boolean refused where an integer was required", role=role)')),
    ('bool', ('raise _fail("boolean refused where ', 'an integer was required", role=role)'), ('return', ' value')),
    ('order', ('order *=', ' modulus'), ('order =', ' modulus')),
    ('dimension', ('if value.b != 0 or va', 'lue.a != Fraction(4):'), ('if value.b == 0 and v', 'alue.a == Fraction(4):')),
    ('return', ('    return 4\n\n\nd', 'ef main() -> int:'), ('    return 5\n\n\nd', 'ef main() -> int:')),
    ('modulus', ('if modu', 'lus < 2:'), ('if modu', 'lus < 1:')),
    ('label', ('if index < 0 or in', 'dex >= self._order:'), ('if index < 0 or in', 'dex > self._order:')),
    ('digits', ('rest //=', ' modulus'), ('rest %=', ' modulus')),
)

PACKAGE_MUTANTS: tuple = (
    ('float guard', ('if issubclass(typ', 'e(value), float):'), ('if False and issubclas', 's(type(value), float):')),
    ('bool guard', ('if type(val', 'ue) is bool:'), ('if False and typ', 'e(value) is bool:')),
    ('seal compare', ('if valu', 'e != 4:'), ('if valu', 'e == 4:')),
    ('sum', ('return le', 'ft + right'), ('return le', 'ft - right')),
    ('gap', ('return le', 'ft - right'), ('return le', 'ft + right')),
    ('product', ('return le', 'ft * right'), ('return le', 'ft + right')),
    ('product compare', ('if _product', '(2, 3) != 6:'), ('if _product', '(2, 3) == 6:')),
    ('return seal', ('    return value\n\n', '\ndef main() -> int:'), ('    return value + 1', '\n\n\ndef main() -> int:')),
)


def test_unit_certificate() -> None:
    _demand(library_witness() == EXPECTED, "dimension drifted")
    sample = AbelianGroup([2, 3])
    _demand(sample.order == 6, "group order drifted", order=sample.order)
    _demand(sample.digits(5) == [1, 2], "digits drifted")



def test_negative_boundary() -> None:
    with pytest.raises(FusionError) as floated:
        AbelianGroup([_float_probe()])
    _demand(floated.value.invariant == "float refused at the fusion boundary", "float invariant drifted")
    with pytest.raises(FusionError) as boolean:
        AbelianGroup([True, 2])
    _demand(boolean.value.invariant == "boolean refused where an integer was required", "bool invariant drifted")
    with pytest.raises(FusionError) as small:
        AbelianGroup([1])
    _demand(small.value.invariant == "modulus is smaller than 2", "modulus invariant drifted")



def test_integration_reads_origin() -> None:
    text = (_repo_root() / ORIGIN_REL).read_text(encoding="utf-8")
    _demand(ORIGIN_MARKER in text, "origin marker missing")
    _demand(package_seal() == library_witness(), "package and library certificates differ")
    _demand(library_witness() == EXPECTED, "library certificate drifted")


def test_end_to_end_cli() -> None:
    _demand(_captured(library_main) == PRINT_TEXT, "library cli drifted")
    _demand(_captured(package_main) == PRINT_TEXT, "package cli drifted")


def test_origin_headers() -> None:
    library = _LIBRARY_PATH.read_text(encoding="utf-8")
    package = _PACKAGE_PATH.read_text(encoding="utf-8")
    _demand("Origin:" in library and "AuthorityEffect: None" in library, "library header drifted")
    _demand(CLAIM in library, "library claim drifted")
    _demand("Scope Fence:" in library and "Scope Fence:" in package, "scope fence missing")



def _fusion_values(namespace: dict[str, object], error: type[BaseException]) -> bool:
    witness = namespace.get("ising_global_dimension_rational")
    group = namespace.get("AbelianGroup")
    if not _all_hold((callable(witness), isinstance(group, type))):
        return False
    try:
        value = witness()
        sample = group([2, 3])
        digits = sample.digits(5)
    except error:
        return False
    if value != 4 or sample.order != 6:
        return False
    return digits == [1, 2]


def _fusion_refusals(namespace: dict[str, object], error: type[BaseException]) -> bool:
    group = namespace.get("AbelianGroup")
    if not isinstance(group, type):
        return False
    try:
        sample = group([2, 3])
    except error:
        return False
    if _invariant(error, lambda: group([_float_probe()])) != "float refused at the fusion boundary":
        return False
    if _invariant(error, lambda: group([True, 2])) != "boolean refused where an integer was required":
        return False
    if _invariant(error, lambda: group([1])) != "modulus is smaller than 2":
        return False
    return _invariant(error, lambda: sample.digits(6)) == "label is outside the group order"



def _library_oracle(namespace: dict[str, object]) -> bool:
    error = namespace.get("FusionError")
    if not isinstance(error, type):
        return False
    if not _fusion_values(namespace, error):
        return False
    return _fusion_refusals(namespace, error)



def _package_oracle(namespace: dict[str, object]) -> bool:
    seal = namespace.get("package_seal")
    check = namespace.get("checked_int")
    error = namespace.get("PackageError")
    if not _all_hold((callable(seal), callable(check), isinstance(error, type))):
        return False
    try:
        value = seal()
    except error:
        return False
    if value != EXPECTED:
        return False
    if _invariant(error, lambda: check(_float_probe())) != "float refused at the package boundary":
        return False
    return _invariant(error, lambda: check(True)) == "boolean refused where an integer was required"


def test_mutation_library() -> None:
    source = _LIBRARY_PATH.read_text(encoding="utf-8")
    killed = _kill_all(source, LIBRARY_MUTANTS, "src.fusion_categories", "library", _library_oracle)
    _demand(killed == 8, "library kill count drifted", killed=killed)
    _record(killed, source)


def test_mutation_package() -> None:
    source = _PACKAGE_PATH.read_text(encoding="utf-8")
    killed = _kill_all(source, PACKAGE_MUTANTS, "src.fusion_categories", "package", _package_oracle)
    _demand(killed == 8, "package kill count drifted", killed=killed)
    _record(killed, source)
