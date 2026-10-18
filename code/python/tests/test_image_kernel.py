"""Unit, negative, integration, end-to-end, and mutation tests for image and kernel."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

from src.linear_algebra import image_basis, kernel_basis
from src.linear_algebra.image_kernel import (
    ExactMatrix,
    ImageKernelError,
    RankNullityCertificate,
    _require_annihilator,
    _require_data_length,
    _require_factorization,
    _require_kernel,
    _require_pivot_identity,
    _require_rank_nullity,
    _stored_fraction,
    rank_nullity_certificate,
)
from src.linear_algebra.scalars import GaussianRational

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "image_kernel.py"


def _singular() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(2), Fraction(3)],
            [Fraction(4), Fraction(5), Fraction(6)],
            [Fraction(7), Fraction(8), Fraction(9)],
        ]
    )


def _cycle_coboundary() -> ExactMatrix:
    """Matrix of d0 φ x = φ(x + 1) - φ x on the n = 3 cycle, in the standard basis."""
    return ExactMatrix.from_rows(
        [
            [Fraction(-1), Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(-1), Fraction(1)],
            [Fraction(1), Fraction(0), Fraction(-1)],
        ]
    )


def test_singular_image_and_kernel_are_exact() -> None:
    certificate = rank_nullity_certificate(_singular())
    assert type(certificate) is RankNullityCertificate
    assert certificate.rank == 2
    assert certificate.nullity == 1
    assert certificate.columns == 3
    assert certificate.rank + certificate.nullity == certificate.columns
    assert image_basis(_singular()) == [
        [Fraction(1), Fraction(4), Fraction(7)],
        [Fraction(2), Fraction(5), Fraction(8)],
    ]
    assert kernel_basis(_singular()) == [[Fraction(1), Fraction(-2), Fraction(1)]]
    assert type(kernel_basis(_singular())[0][0]) is Fraction


def test_negative_boundary_failures() -> None:
    with pytest.raises(ImageKernelError, match="float refused") as floated:
        rank_nullity_certificate(ExactMatrix.from_rows([[1.5]]))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0]"
    assert type(floated.value) is ImageKernelError

    with pytest.raises(ImageKernelError, match="boolean refused where a rational") as boolean:
        rank_nullity_certificate(ExactMatrix.from_rows([[True]]))
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    gaussian = ExactMatrix.from_rows([[GaussianRational(0, 1)]])
    with pytest.raises(ImageKernelError, match="Gaussian rational refused") as gaussian_error:
        rank_nullity_certificate(gaussian)
    assert gaussian_error.value.parameters["role"] == "entry[0]"

    with pytest.raises(ImageKernelError, match="not an exact rational") as text:
        rank_nullity_certificate(ExactMatrix.from_rows([["1"]]))
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = True
    with pytest.raises(ImageKernelError, match="boolean refused where a matrix dimension") as dim_bool:
        rank_nullity_certificate(shaped)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = 1.0
    with pytest.raises(ImageKernelError, match="float refused") as dim_float:
        rank_nullity_certificate(shaped)
    assert dim_float.value.parameters["role"] == "rows"

    negative = ExactMatrix(-1, 0, [])
    with pytest.raises(ImageKernelError, match="negative") as negative_error:
        rank_nullity_certificate(negative)
    assert negative_error.value.parameters["received"] == -1

    named = ExactMatrix.from_rows([[Fraction(1)]])
    named.rows = "1"
    with pytest.raises(ImageKernelError, match="not an integer") as named_error:
        rank_nullity_certificate(named)
    assert named_error.value.parameters["received"] == "str"

    with pytest.raises(ImageKernelError, match="not an ExactMatrix") as bare:
        rank_nullity_certificate("matrix")  # type: ignore[arg-type]
    assert bare.value.parameters["received"] == "str"

    mismatched = ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]])
    mismatched.rows = 1
    with pytest.raises(ImageKernelError, match="data length") as length_error:
        rank_nullity_certificate(mismatched)
    assert length_error.value.parameters["length"] == 4

    with pytest.raises(ImageKernelError, match="float refused on a stored") as stored_float:
        _stored_fraction(0.5, "image")
    assert stored_float.value.parameters["role"] == "image"

    with pytest.raises(ImageKernelError, match="left the rational carrier") as stored:
        _stored_fraction(1, "image")
    assert stored.value.parameters["received"] == "int"

    with pytest.raises(ImageKernelError, match="pivot entry is not one") as pivot:
        _require_pivot_identity(ExactMatrix.from_rows([[Fraction(0)]]), [0])
    assert pivot.value.parameters["pivot"] == 0

    source = ExactMatrix.from_rows([[Fraction(1)]])
    image = ExactMatrix.from_rows([[Fraction(0)]])
    coordinates = ExactMatrix.identity(1)
    with pytest.raises(ImageKernelError, match="do not rebuild") as rebuilt:
        _require_factorization(source, image, coordinates)
    assert rebuilt.value.parameters["rank"] == 1

    with pytest.raises(ImageKernelError, match="not annihilated") as annihilated:
        _require_annihilator(source, [Fraction(1)], 0)
    assert annihilated.value.parameters["free_col"] == 0

    with pytest.raises(ImageKernelError, match="kernel count") as counted:
        _require_kernel(ExactMatrix.zeros(1, 1), [], [])
    assert counted.value.parameters["nullity"] == 1

    with pytest.raises(ImageKernelError, match="rank plus nullity") as counted_rank:
        _require_rank_nullity(1, 0, 2)
    assert counted_rank.value.parameters["columns"] == 2

    short = ExactMatrix.from_rows([[Fraction(1), Fraction(0)]])
    with pytest.raises(ImageKernelError, match="data length"):
        _require_data_length(short, 2, 2)


def test_integration_cycle_coboundary_matches_cited_nullity() -> None:
    root = Path(__file__).resolve().parents[3]
    rank_note = (root / "research" / "lean4" / "qm_superposition_h1_rank.md").read_text(encoding="utf-8")
    cochain = (root / "research" / "lean4" / "qm_superposition_cochain.md").read_text(encoding="utf-8")
    assert "theorem finrank_H1_eq_one" in rank_note
    assert "LinearMap.finrank_range_add_finrank_ker" in rank_note
    assert "def d0 [Sub A] (φ : ZMod n → A) : ZMod n → A := fun x => φ (x + 1) - φ x" in cochain
    certificate = rank_nullity_certificate(_cycle_coboundary())
    assert certificate.rank == 2
    assert certificate.nullity == 1
    assert certificate.columns == 3
    assert certificate.kernel == ((Fraction(1), Fraction(1), Fraction(1)),)
    assert len(certificate.image) == certificate.rank
    assert [len(column) for column in certificate.image] == [3, 3]
    assert _cycle_coboundary().mul_vec(list(certificate.kernel[0])) == [
        Fraction(0),
        Fraction(0),
        Fraction(0),
    ]


def test_end_to_end_public_contract() -> None:
    assert image_basis(ExactMatrix.identity(2)) == [
        [Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1)],
    ]
    assert kernel_basis(ExactMatrix.identity(2)) == []
    assert kernel_basis(ExactMatrix.zeros(2, 3)) == [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
    ]
    empty = rank_nullity_certificate(ExactMatrix(0, 0, []))
    assert empty.rank == 0
    assert empty.nullity == 0
    assert empty.columns == 0
    wide = rank_nullity_certificate(ExactMatrix(0, 2, []))
    assert wide.rank == 0
    assert wide.nullity == 2
    tampered = ExactMatrix.identity(1)
    tampered.data[0] = 0.25
    with pytest.raises(ImageKernelError, match="float refused"):
        image_basis(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    rank_note = (root / "research" / "lean4" / "qm_superposition_h1_rank.md").read_text(encoding="utf-8")
    cochain = (root / "research" / "lean4" / "qm_superposition_cochain.md").read_text(encoding="utf-8")
    assert "theorem finrank_H1_eq_one" in rank_note
    assert "def d0 [Sub A]" in cochain
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:image-kernel-rank-nullity:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float entry admitted",
        'if type(value) is float:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if type(value) is float:\n        return Fraction(0)\n    if False:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
    ),
    (
        "boolean entry admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a rational entry was required", role=role)',
        'if type(value) is bool:\n        return Fraction(1)\n    if False:\n        raise _fail("boolean refused where a rational entry was required", role=role)',
    ),
    (
        "Gaussian entry admitted",
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; image-kernel certificate is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; image-kernel certificate is over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "rank-nullity check inverted",
        "if rank + nullity != columns:",
        "if rank + nullity == columns:",
    ),
    (
        "factorization check inverted",
        "if image * coordinates != source:",
        "if image * coordinates == source:",
    ),
    (
        "annihilator check inverted",
        "if not _is_zero_image(source.mul_vec(vector)):",
        "if _is_zero_image(source.mul_vec(vector)):",
    ),
    (
        "pivot identity inverted",
        "if entry != Fraction(1):",
        "if entry == Fraction(1):",
    ),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.linear_algebra"
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
    certify = namespace["rank_nullity_certificate"]
    columns = namespace["image_basis"]
    vectors = namespace["kernel_basis"]
    matrix = namespace["ExactMatrix"]
    if not callable(certify) or not callable(columns) or not callable(vectors) or not isinstance(matrix, type):
        return False
    try:
        singular = certify(_singular())
        cycle = certify(_cycle_coboundary())
        zero = certify(matrix.zeros(2, 3))
        eye = certify(matrix.identity(2))
        singular_kernel = vectors(_singular())
        singular_image = columns(_singular())
    except error:
        return False
    singular_ok = bool(
        getattr(singular, "rank", None) == 2
        and getattr(singular, "nullity", None) == 1
        and getattr(singular, "columns", None) == 3
        and singular_kernel == [[Fraction(1), Fraction(-2), Fraction(1)]]
        and singular_image[0] == [Fraction(1), Fraction(4), Fraction(7)]
    )
    cycle_ok = bool(getattr(cycle, "rank", None) == 2 and getattr(cycle, "nullity", None) == 1)
    zero_ok = bool(getattr(zero, "rank", None) == 0 and getattr(zero, "nullity", None) == 3)
    eye_ok = bool(getattr(eye, "rank", None) == 2 and getattr(eye, "nullity", None) == 0)
    return singular_ok and cycle_ok and zero_ok and eye_ok


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    certify = namespace["rank_nullity_certificate"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not callable(certify) or not isinstance(matrix, type) or not callable(gaussian):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    shaped = build([[Fraction(1)]])
    shaped.rows = True
    probes = (
        (lambda: certify(build([[1.5]])), "float refused at the public boundary"),
        (lambda: certify(build([[True]])), "boolean refused where a rational entry was required"),
        (lambda: certify(build([[gaussian(0, 1)]])), "Gaussian rational refused; image-kernel certificate is over Q"),
        (lambda: certify(shaped), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["ImageKernelError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_image_kernel_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_image_kernel_{index}"
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
