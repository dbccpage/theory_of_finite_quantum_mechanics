"""Unit, negative, integration, end-to-end, and mutation tests.

Origin: dag/derivation_dag_operads.binding.yaml schema omega_operad_binding_v1.
Claim: urn:omega:fqm:operad:disjoint-graft-witness:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/operad_theory/test_operad_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: The harness falsifies the disjoint-graft certificate and its own integer checks.
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
    if isinstance(value, float) is True:
        raise _fail("float refused at the harness boundary", role=role, received="float")
    if isinstance(value, bool) is True:
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
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
    if gap != 4:
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
    try:
        try:
            namespace = _load(source.replace(old, new, 1), name, package)
        except Exception:
            return True
        try:
            return oracle(namespace) is False
        except Exception:
            return True
    finally:
        sys.modules.pop(name, None)


def _require_baseline(source: str, package: str, label: str, oracle: object) -> None:
    if not callable(oracle):
        raise _fail("oracle is not callable")
    name = f"baseline_{label}"
    try:
        namespace = _load(source, name, package)
        if oracle(namespace) is not True:
            raise _fail("baseline oracle failed", label=label)
    finally:
        sys.modules.pop(name, None)


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


HARNESS_MUTANTS: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("float", ("if isinstance(value, float) ", "is True:"), ("if False and isinstance(value, float) ", "is True:")),
    ("bool", ("if isinstance(value, bool) ", "is True:"), ("if False and isinstance(value, bool) ", "is True:")),
    ("sum", ("return left ", "+ right"), ("return left ", "- right")),
    ("gap", ("return left ", "- right"), ("return left ", "+ right")),
    ("product", ("return left ", "* right"), ("return left ", "+ right")),
    ("sum compare", ("if total ", "!= 4:"), ("if total ", "== 4:")),
    ("gap compare", ("if gap ", "!= 4:"), ("if gap ", "== 4:")),
    ("product compare", ("if product ", "!= 6:"), ("if product ", "== 6:")),
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

from src.operad_theory import main as package_main, package_seal
from src.operad_theory.planar_operad import OperadColour, OperadError, Operation, PlanarTree, disjoint_graft_witness as library_witness, main as library_main

_LIBRARY_PATH = Path(__file__).resolve().with_name("planar_operad.py")
_PACKAGE_PATH = Path(__file__).resolve().with_name("__init__.py")


PRINT_TEXT = '2\n'
ORIGIN_REL = 'dag/derivation_dag_operads.binding.yaml'
ORIGIN_MARKER = 'omega_operad_binding_v1'
CLAIM = 'urn:omega:fqm:operad:disjoint-graft-witness:v1'
EXPECTED = 2

LIBRARY_MUTANTS: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    ('float', ('if isinstance(', 'value, float):'), ('if False and isinst', 'ance(value, float):')),
    ('bool', ('if isinstance', '(value, bool):'), ('if False and isins', 'tance(value, bool):')),
    ('terms', ('if left.term_repr() ', '!= right.term_repr():'), ('if left.term_repr() ', '== right.term_repr():')),
    ('arity', ('if left.arity != binary.arity - ', '1 + eta.arity - 1 + theta.arity:'), ('if left.arity == binary.arity - ', '1 + eta.arity - 1 + theta.arity:')),
    ('name', ('if left.term_repr() != "mu(', 'eta(leaf:V),theta(leaf:V))":'), ('if left.term_repr() == "mu(', 'eta(leaf:V),theta(leaf:V))":')),
    ('total', ('return ch', 'ild.arity'), ('return chil', 'd.arity + 1')),
    ('corolla', ('if not isinstance(op', 'eration, Operation):'), ('if isinstance(oper', 'ation, Operation):')),
    ('return', ('    return ', 'left.arity\n'), ('    return le', 'ft.arity + 1\n')),
)

PACKAGE_MUTANTS: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    ('float guard', ('if isinstance(', 'value, float):'), ('if False and isinst', 'ance(value, float):')),
    ('bool guard', ('if isinstance', '(value, bool):'), ('if False and isins', 'tance(value, bool):')),
    ('seal compare', ('if valu', 'e != 2:'), ('if valu', 'e == 2:')),
    ('sum', ('return le', 'ft + right'), ('return le', 'ft - right')),
    ('gap', ('return le', 'ft - right'), ('return le', 'ft + right')),
    ('product', ('return le', 'ft * right'), ('return le', 'ft + right')),
    ('product compare', ('if _product', '(2, 3) != 6:'), ('if _product', '(2, 3) == 6:')),
    ('return seal', ('    return value\n\n', '\ndef main() -> int:'), ('    return value + 1', '\n\n\ndef main() -> int:')),
)


def test_unit_certificate() -> None:
    _demand(library_witness() == EXPECTED, "witness drifted")



def test_negative_boundary() -> None:
    colour = OperadColour("V")
    tree = PlanarTree.corolla(Operation("mu", (colour, colour), OperadColour("W")))
    with pytest.raises(OperadError) as floated:
        tree.graft(_float_probe(), tree)
    _demand(floated.value.invariant == "float refused where a graft slot was required", "float invariant drifted")
    with pytest.raises(OperadError) as boolean:
        tree.graft(True, tree)
    _demand(boolean.value.invariant == "boolean refused where a graft slot was required", "bool invariant drifted")



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





def _library_oracle(namespace: dict[str, object]) -> bool:
    witness = namespace.get("disjoint_graft_witness")
    colour_type = namespace.get("OperadColour")
    operation = namespace.get("Operation")
    tree_type = namespace.get("PlanarTree")
    error = namespace.get("OperadError")
    if not _all_hold((callable(witness), isinstance(colour_type, type), isinstance(operation, type), isinstance(tree_type, type), isinstance(error, type))):
        return False
    try:
        value = witness()
        colour = colour_type("V")
        tree = tree_type.corolla(operation("mu", (colour, colour), colour_type("W")))
    except error:
        return False
    if value != 2:
        return False
    if _invariant(error, lambda: tree.graft(_float_probe(), tree)) != "float refused where a graft slot was required":
        return False
    return _invariant(error, lambda: tree.graft(True, tree)) == "boolean refused where a graft slot was required"



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
    killed = _kill_all(source, LIBRARY_MUTANTS, "src.operad_theory", "library", _library_oracle)
    _demand(killed == 8, "library kill count drifted", killed=killed)
    _record(killed, source)


def test_mutation_package() -> None:
    source = _PACKAGE_PATH.read_text(encoding="utf-8")
    killed = _kill_all(source, PACKAGE_MUTANTS, "src.operad_theory", "package", _package_oracle)
    _demand(killed == 8, "package kill count drifted", killed=killed)
    _record(killed, source)
