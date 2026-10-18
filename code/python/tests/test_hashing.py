"""Unit, negative, integration, end-to-end, and mutation tests for the entry digest."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from src.homology.hashing import HashWitnessError, hash_bytes, hash_distinguishes_entry, hash_matrix
from src.linear_algebra.matrix import ExactMatrix
from src.linear_algebra.scalars import GaussianRational

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "hashing.py"


class _Grid:
    def __init__(self, rows: int, cols: int, data: list[object]) -> None:
        self.rows = rows
        self.cols = cols
        self.data = data


def _expected_half() -> str:
    digest = hashlib.sha256()
    digest.update(b"1x1:")
    digest.update(b"1/2")
    digest.update(b",")
    return digest.hexdigest()


def test_reduced_entries_share_a_digest() -> None:
    half = hash_matrix(_Grid(1, 1, [Fraction(1, 2)]))
    same = hash_matrix(_Grid(1, 1, [Fraction(2, 4)]))
    whole = hash_matrix(_Grid(1, 1, [Fraction(1, 1)]))
    assert half == same == _expected_half()
    assert half != whole
    assert hash_distinguishes_entry() is True
    assert hash_bytes(b"fqm") == hashlib.sha256(b"fqm").hexdigest()


def test_negative_boundary_failures() -> None:
    with pytest.raises(HashWitnessError, match="float refused") as floated:
        hash_matrix(_Grid(1, 1, [1.0]))
    assert floated.value.parameters["received"] == "float"

    with pytest.raises(HashWitnessError, match="boolean refused") as boolean:
        hash_matrix(_Grid(1, 1, [True]))
    assert boolean.value.parameters["received"] == "bool"

    with pytest.raises(HashWitnessError, match="no canonical") as text:
        hash_matrix(_Grid(1, 1, ["1/2"]))
    assert text.value.parameters["received"] == "str"

    with pytest.raises(HashWitnessError, match="refuses booleans") as shape:
        hash_matrix(_Grid(True, 1, [1]))
    assert shape.value.parameters["rows"] == "bool"

    with pytest.raises(HashWitnessError, match="does not match shape") as length:
        hash_matrix(_Grid(2, 2, [1]))
    assert length.value.parameters["length"] == 1

    with pytest.raises(HashWitnessError, match="requires bytes") as raw:
        hash_bytes("fqm")
    assert raw.value.parameters["received"] == "str"


def test_integration_with_matrix_and_scalar_neighbors() -> None:
    """ExactMatrix delegates to its own sha256, and Gaussian entries use canonical bytes."""
    matrix = ExactMatrix.from_rows([[Fraction(1, 2)]])
    assert hash_matrix(matrix) == matrix.sha256()
    committed = hash_matrix(_Grid(1, 1, [GaussianRational(1, 2)]))
    digest = hashlib.sha256()
    digest.update(b"1x1:")
    digest.update(GaussianRational(1, 2).canonical_bytes())
    digest.update(b",")
    assert committed == digest.hexdigest()


def test_end_to_end_public_contract() -> None:
    assert hash_matrix(_Grid(1, 2, [Fraction(1, 2), 0])) != hash_matrix(_Grid(1, 2, [Fraction(1, 2), 1]))
    with pytest.raises(HashWitnessError, match="float refused") as caught:
        hash_bytes(hash_matrix(_Grid(1, 1, [0.5])))
    assert caught.value.invariant == "float refused at the public boundary"


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "H001Rats.lean").read_text(encoding="utf-8")
    assert "def qrel" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:reduced-entry-digest:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return f\"{Fraction(value).numerator}/{Fraction(value).denominator}\".encode(\"utf-8\")\n    if False:",
    ),
    (
        "boolean admitted as an integer",
        "if isinstance(value, bool):",
        "if isinstance(value, bool) and False:",
    ),
    (
        "denominator dropped",
        'return f"{value.numerator}/{value.denominator}".encode("utf-8")',
        'return f"{value.numerator}/1".encode("utf-8")',
    ),
    ("length check inverted", "if rows < 0 or cols < 0 or len(data) != rows * cols:", "if rows < 0 or cols < 0 or len(data) == rows * cols:"),
    ("comma separator dropped", 'digest.update(b",")', 'digest.update(b"")'),
    ("digest algorithm weakened", "digest = hashlib.sha256()", "digest = hashlib.sha1()"),
    ("byte digest algorithm weakened", "return hashlib.sha256(data).hexdigest()", "return hashlib.sha1(data).hexdigest()"),
    ("shape boolean check removed", "if isinstance(rows, bool) or isinstance(cols, bool):", "if isinstance(rows, bool) and isinstance(cols, bool):"),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
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


class _OracleGrid:
    def __init__(self, rows: object, cols: object, data: object) -> None:
        self.rows = rows
        self.cols = cols
        self.data = data


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    digest_matrix = namespace["hash_matrix"]
    digest_bytes = namespace["hash_bytes"]
    if not callable(digest_matrix) or not callable(digest_bytes):
        return False
    try:
        half = digest_matrix(_OracleGrid(1, 1, [Fraction(1, 2)]))
        same = digest_matrix(_OracleGrid(1, 1, [Fraction(2, 4)]))
        whole = digest_matrix(_OracleGrid(1, 1, [Fraction(1, 1)]))
        raw = digest_bytes(b"fqm")
    except error:
        return False
    if half != same or half == whole:
        return False
    if half != _expected_half():
        return False
    if raw != hashlib.sha256(b"fqm").hexdigest():
        return False
    return True


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    digest_matrix = namespace["hash_matrix"]
    if not callable(digest_matrix):
        return False
    expected = (
        (lambda: digest_matrix(_OracleGrid(1, 1, [1.0])), "float refused at the public boundary"),
        (lambda: digest_matrix(_OracleGrid(1, 1, [True])), "boolean refused where a rational entry was required"),
        (lambda: digest_matrix(_OracleGrid(True, 1, [1])), "matrix shape refuses booleans"),
    )
    for probe, invariant in expected:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["HashWitnessError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_hash_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_hash_{index}"
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
    finally:
        for module_name in loaded:
            sys.modules.pop(module_name, None)
