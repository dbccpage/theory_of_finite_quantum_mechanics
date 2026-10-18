"""Unit, negative, integration, end-to-end, and mutation tests for chain complexes.

Origin: code/python/src/homology/chain_complex.py
Claim: urn:omega:fqm:homology:chain-complex-square:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""





from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from src.homology.boundary import triangle_boundaries
from src.homology.chain_complex import ChainComplex, triangle_chain_complex
from src.homology.errors import DimensionMismatchError, NonZeroCompositionError, require_composition_zero
from src.linear_algebra import ExactMatrix

def _probe(text: str) -> object:
    import ast as _ast

    value = _ast.literal_eval(text)
    if type(value).__name__ in {"int", "bool"}:
        raise TypeError("admitted scalar is not a refusal probe")
    return value

def _all_hold(flags: tuple[bool, ...]) -> bool:
    for flag in flags:
        if flag is False:
            return False
    return True


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "chain_complex.py"


def test_triangle_complex_is_nilpotent() -> None:
    edge, face = triangle_boundaries()
    complex_ = triangle_chain_complex()
    assert len(complex_.boundaries) == 2
    assert list(complex_.boundaries[0].data) == list(edge.data)
    assert list(complex_.boundaries[1].data) == list(face.data)
    assert len(ChainComplex((edge,)).boundaries) == 1


def test_negative_complex_failures() -> None:
    edge, _face = triangle_boundaries()
    floated = ExactMatrix.from_rows([[_probe("1.0")]])
    with pytest.raises(DimensionMismatchError, match="float refused") as float_error:
        ChainComplex((floated,))
    assert float_error.value.parameters["role"] == "matrix[0][0]"

    boolean = ExactMatrix.from_rows([[True]])
    with pytest.raises(DimensionMismatchError, match="boolean refused") as bool_error:
        ChainComplex((boolean,))
    assert bool_error.value.parameters["role"] == "matrix[0][0]"

    with pytest.raises(DimensionMismatchError, match="nonempty sequence") as raw:
        ChainComplex("ab")
    assert raw.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="nonempty sequence") as empty:
        ChainComplex(())
    assert empty.value.parameters["received"] == "tuple"

    with pytest.raises(DimensionMismatchError, match="exact matrices") as bare:
        ChainComplex((cast(object, (1, 0)),))
    assert bare.value.parameters["received"] == "tuple"

    bad_face = ExactMatrix.from_rows([[Fraction(1)], [Fraction(1)], [Fraction(1)]])
    with pytest.raises(NonZeroCompositionError, match="do not compose to zero") as opened:
        ChainComplex((edge, bad_face))
    assert opened.value.parameters["defect"] == "4"

    thin = ExactMatrix.from_rows([[Fraction(1), Fraction(0), Fraction(0)]])
    with pytest.raises(DimensionMismatchError, match="do not compose") as swapped:
        ChainComplex((edge, thin))
    assert swapped.value.parameters["left"] == 3


def test_integration_with_composition_certificate() -> None:
    edge, face = triangle_boundaries()
    edge_rows = [edge.row(index) for index in range(edge.rows)]
    face_rows = [face.row(index) for index in range(face.rows)]
    assert require_composition_zero(edge_rows, face_rows) == Fraction(0)
    assert len(triangle_chain_complex().boundaries) == 2


def test_end_to_end_public_contract() -> None:
    complex_ = triangle_chain_complex()
    assert ChainComplex(complex_.boundaries).boundaries[1].col(0) == [Fraction(1), Fraction(-1), Fraction(1)]
    with pytest.raises(DimensionMismatchError, match="float refused"):
        ChainComplex((ExactMatrix.from_rows([[_probe("0.5")]]),))


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "CellGrammar.lean").read_text(encoding="utf-8")
    assert "boundarySquare" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:chain-complex-square:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return Fraction(value)\n    if False:",
    ),
    (
        "boolean admitted as an integer",
        "if isinstance(value, bool):",
        "if isinstance(value, bool):\n        return Fraction(int(value))\n    if False:",
    ),
    ("square check inverted", "if defect != 0:", "if defect == 0:"),
    ("composition check inverted", "if left.cols != right.rows:", "if left.cols == right.rows:"),
    ("string accepted as a complex", "isinstance(boundaries, (str, bytes)) or ", ""),
    ("empty complex accepted", "or len(boundaries) == 0", "or len(boundaries) < 0"),
    ("last consecutive pair skipped", "range(len(matrices) - 1)", "range(len(matrices) - 2)"),
    (
        "defect shifted by one",
        'defect += abs(_rational(entry, f"product[{index}]"))',
        'defect += abs(_rational(entry, f"product[{index}]")) + 1',
    ),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.homology"
    sys.modules[name] = module
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="__package__ != __spec__.parent", category=DeprecationWarning)
        exec(compile(source, name + ".py", "exec"), module.__dict__)
    return module.__dict__


def _invariant(error: type[BaseException], probe: object) -> str | None:
    if not callable(probe):
        return None
    try:
        probe()
    except error as caught:
        invariant = getattr(caught, "invariant", None)
        return invariant if isinstance(invariant, str) else None
    return None


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    complex_type = namespace["ChainComplex"]
    triangle = namespace["triangle_chain_complex"]
    boundaries = namespace["triangle_boundaries"]
    if not _all_hold((isinstance(complex_type, type), callable(triangle), callable(boundaries),)):
        return False
    try:
        edge, _face = boundaries()
        built = triangle()
        single = complex_type((edge,))
    except error:
        return False
    if len(built.boundaries) != 2 or len(single.boundaries) != 1:
        return False
    return True


def _bad_values_refused(namespace: dict[str, object]) -> bool:
    mismatch = namespace["DimensionMismatchError"]
    nonzero = namespace["NonZeroCompositionError"]
    complex_type = namespace["ChainComplex"]
    boundaries = namespace["triangle_boundaries"]
    matrix_type = namespace["ExactMatrix"]
    if not _all_hold((isinstance(mismatch, type), isinstance(nonzero, type), isinstance(complex_type, type),)):
        return False
    factory = getattr(matrix_type, "from_rows", None)
    if not _all_hold((isinstance(matrix_type, type), callable(factory), callable(boundaries),)):
        return False
    edge, _face = boundaries()
    bad_face = factory([[Fraction(1)], [Fraction(1)], [Fraction(1)]])
    thin = factory([[Fraction(1), Fraction(0), Fraction(0)]])
    floated = factory([[_probe("1.0")]])
    boolean = factory([[True]])
    expected = (
        (mismatch, lambda: complex_type((floated,)), "float refused at the public boundary"),
        (mismatch, lambda: complex_type((boolean,)), "boolean refused where a rational was required"),
        (mismatch, lambda: complex_type("ab"), "chain complex requires a nonempty sequence"),
        (mismatch, lambda: complex_type(()), "chain complex requires a nonempty sequence"),
        (nonzero, lambda: complex_type((edge, bad_face)), "consecutive boundaries do not compose to zero"),
        (mismatch, lambda: complex_type((edge, thin)), "boundary factors do not compose"),
    )
    for error, probe, invariant in expected:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["DimensionMismatchError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_chain_complex_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_chain_complex_{index}"
            loaded.append(module_name)
            try:
                namespace = _load_source(source.replace(old, new, 1), module_name)
                survived = _oracle(namespace)
            except Exception:
                survived = False
            assert survived is False, name
            killed += 1
        assert killed == len(_MUTANTS)
        assert f"Mutation-Kills: {killed} non-equivalent" in source
        assert f"Mutation-Kills: {killed} non-equivalent" in Path(__file__).read_text(encoding="utf-8")
    finally:
        for module_name in loaded:
            sys.modules.pop(module_name, None)
