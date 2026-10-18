"""Unit, negative, integration, end-to-end, and mutation tests for quintic splitting degree."""

from __future__ import annotations

import copy
import importlib.util
import io
import json
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra import field_factors as factors
from src.linear_algebra.field_factors import FieldFactorError, factor_polynomial
from src.linear_algebra.quintic_split import (
    QuinticDegreeError,
    SplittingAlgebra,
    dispatch,
    quintic_splitting_degree,
    validate_quintic_degree,
)
from src.linear_algebra import quintic_split as quintic


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "quintic_split.py"
_Q = Fraction
_QUAD = [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(-1), _Q(0))]
_F20 = [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0)), (_Q(-2), _Q(0))]
_S5 = [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0)), (_Q(-1), _Q(0)), (_Q(-1), _Q(0))]
_A5 = [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0)), (_Q(20), _Q(0)), (_Q(16), _Q(0))]
_REDUCIBLE = [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0)), (_Q(-1), _Q(0))]


def _raises(probe: Any, invariant: str) -> QuinticDegreeError:
    with pytest.raises(QuinticDegreeError) as caught:
        probe()
    assert caught.value.invariant == invariant
    assert all(type(item) is not float for item in caught.value.parameters.values())
    return caught.value


def _quadratic() -> SplittingAlgebra:
    return SplittingAlgebra(1, _QUAD)


def _expect(certificate: dict[str, Any], group: str, degree: int, square: bool) -> None:
    assert certificate["schema"] == "quintic_splitting_degree_v1"
    assert certificate["authority_effect"] == "None"
    assert certificate["algorithm"] == "EXACT_LOCALIZED_QUINTIC_FIXED_ALGEBRAS"
    assert certificate["scope"] == "E_QUINTIC_SPLITTING_DEGREE_NO_CARRIER_TRANSPORT_OR_DEPENDENCE"
    assert certificate["galois_group"] == group
    assert type(certificate["galois_group"]) is str
    assert certificate["degree_over_real_field"] == degree
    assert type(certificate["degree_over_real_field"]) is int
    assert certificate["algebra_rank"] == 120
    assert type(certificate["algebra_rank"]) is int
    assert certificate["discriminant_square"]["is_square"] is square
    assert certificate["full_fixed_algebra"]["primitive_parameter"] == 1
    assert type(certificate["full_fixed_algebra"]["primitive_parameter"]) is int
    assert certificate["full_fixed_algebra"]["dimension"] == 6
    assert certificate["coefficient_field"] == "Q"
    assert certificate["conductor"] == 1
    assert certificate["real_generator_radicand"] == 0


@pytest.fixture(scope="module")
def published() -> dict[str, dict[str, Any]]:
    return {
        "F20": quintic_splitting_degree(1, _F20),
        "S5": quintic_splitting_degree(1, _S5),
        "A5": quintic_splitting_degree(1, _A5),
    }


def test_hand_certificates_match_classical_groups(published: dict[str, dict[str, Any]]) -> None:
    frobenius = published["F20"]
    symmetric = published["S5"]
    alternating = published["A5"]
    _expect(frobenius, "F20", 20, False)
    _expect(symmetric, "S5", 120, False)
    _expect(alternating, "A5", 60, True)
    assert isinstance(frobenius["localized_fixed_algebra"], dict)
    assert frobenius["localized_fixed_algebra"]["ideal_dimension"] == 20
    assert frobenius["localized_fixed_algebra"]["cyclic_fixed_algebra"]["dimension"] == 4
    assert symmetric["localized_fixed_algebra"] is None
    assert alternating["localized_fixed_algebra"] is None
    validate_quintic_degree(1, _F20, frobenius)
    validate_quintic_degree(1, _S5, symmetric)
    validate_quintic_degree(1, _A5, alternating)


def test_negative_paths_record_every_invariant(published: dict[str, dict[str, Any]]) -> None:
    refused = _raises(lambda: quintic_splitting_degree(1.0, _QUAD), "float refused at the public boundary")
    assert refused.parameters == {"role": "conductor", "received": "float"}
    nested = _raises(
        lambda: quintic_splitting_degree(1, ((1.5, _Q(0)),)),
        "float refused at the public boundary",
    )
    assert nested.parameters == {"role": "coefficient", "received": "float"}
    with pytest.raises(FieldFactorError) as conductor:
        quintic_splitting_degree(True, _QUAD)
    assert conductor.value.invariant == "boolean refused where a conductor was required"

    algebra = _quadratic()
    basis = [{0: quintic.ONE}, {1: quintic.ONE}]
    boolean = _raises(
        lambda: algebra.primitive(basis, parameter=True),
        "boolean refused where an exact integer was required",
    )
    assert boolean.parameters == {"role": "primitive_parameter"}
    _raises(lambda: quintic._exact_counter("1", "primitive_parameter"), "quintic_degree: exact integer required")
    _raises(lambda: quintic._div(quintic.ONE, quintic.ZERO, 0), "splitting_algebra: division by zero E coefficient")
    _raises(lambda: quintic.Span(0).coordinates({0: quintic.ONE}), "splitting_algebra: vector outside certified subspace")
    _raises(
        lambda: quintic._relation_polynomial([{}], [{}], 0, (0,), 2),
        "splitting_algebra: triangular relation is not monic",
    )
    degree = _raises(
        lambda: SplittingAlgebra(1, [(_Q(1), _Q(0))]),
        "splitting_algebra: polynomial degree must be two through five",
    )
    assert degree.parameters["degree"] == 0
    _raises(
        lambda: SplittingAlgebra(1, [(_Q(1), _Q(0)), (_Q(0), _Q(0)), (_Q(0), _Q(0))]),
        "splitting_algebra: separable polynomial required",
    )
    _raises(lambda: algebra.action_columns(None), "splitting_algebra: exact root permutation required")
    _raises(lambda: algebra.action_columns((True, 0)), "splitting_algebra: exact root permutation required")
    _raises(lambda: algebra.action_columns((0, 0)), "splitting_algebra: exact root permutation required")
    _raises(
        lambda: algebra.fixed_basis([], [{0: quintic.ONE}, {0: quintic.ONE}]),
        "splitting_algebra: dependent ambient basis",
    )
    _raises(lambda: algebra.primitive([{0: quintic.ONE}, {0: quintic.ONE}]), "splitting_algebra: dependent fixed basis")
    _raises(
        lambda: algebra.primitive(basis, parameter=-1),
        "splitting_algebra: nonnegative exact primitive parameter required",
    )
    _raises(
        lambda: algebra.primitive(basis, parameter=0),
        "splitting_algebra: primitive Krylov rank failed for parameter family",
    )
    _raises(lambda: algebra.localized_basis({}), "splitting_algebra: nonzero idempotent required")
    span = quintic.Span(0)
    span.insert({0: quintic.ONE})
    span.insert({1: quintic.ONE})
    krylov = quintic.Span(0)
    krylov.insert({0: quintic.ONE})
    krylov.insert({1: quintic.ONE})
    _raises(
        lambda: quintic._squarefree_relation(span, krylov, {0: (_Q(-1), _Q(0)), 1: (_Q(2), _Q(0))}, 0),
        "splitting_algebra: primitive polynomial is not squarefree",
    )
    for label in ("result", "request", "fixed algebra", "localized algebra"):
        _raises(lambda label=label: quintic._fields([], set(), label), f"quintic_degree: exact {label} field census required")
    for label in (
        "conductor",
        "real_generator_radicand",
        "algebra_rank",
        "fixed dimension",
        "ideal dimension",
        "splitting degree",
    ):
        _raises(lambda label=label: quintic._integer(True, 1, label), f"quintic_degree: exact {label} integer differs")
    _raises(lambda: quintic._parse_element(algebra, "no"), "quintic_degree: sparse element array required")
    _raises(
        lambda: quintic._parse_element(algebra, [[2, ["1/1", "0/1"]]]),
        "quintic_degree: ordered bounded exact element indices required",
    )
    _raises(
        lambda: quintic._parse_element(algebra, [[0, ["0/1", "0/1"]]]),
        "quintic_degree: zero sparse coefficient forbidden",
    )
    wide = _raises(lambda: quintic_splitting_degree(1, _QUAD), "quintic_degree: degree-five polynomial required")
    assert wide.parameters["degree"] == 2
    _raises(lambda: quintic_splitting_degree(1, _REDUCIBLE), "quintic_degree: irreducibility over actual E is required")
    _raises(
        lambda: quintic._pattern({"factors": [{"polynomial": ["1/1", "-1/1"], "multiplicity": 2}]}),
        "quintic_degree: resolvent must have distinct irreducible factors",
    )
    _raises(lambda: quintic._require_generators([[True]], [(1,)]), "quintic_degree: root-label generators differ")
    _raises(lambda: quintic._require_generators([[0]], [(1,)]), "quintic_degree: root-label generators differ")
    occupied = quintic.Span(algebra.d)
    occupied.insert({0: quintic.ONE})
    _raises(
        lambda: quintic._require_one_fixed(algebra, occupied, {0: quintic.ONE}, [], algebra.unit),
        "quintic_degree: fixed basis is linearly dependent",
    )
    _raises(
        lambda: quintic._require_one_fixed(algebra, quintic.Span(algebra.d), algebra.roots[0], [(1, 0)], algebra.unit),
        "quintic_degree: basis vector is not subgroup-invariant",
    )
    _raises(
        lambda: quintic._require_one_fixed(algebra, quintic.Span(algebra.d), {0: quintic.ONE}, [], {1: quintic.ONE}),
        "quintic_degree: fixed vector outside unital component",
    )
    _raises(
        lambda: quintic._require_fixed_basis(algebra, {"basis": []}, [], 1, algebra.unit),
        "quintic_degree: full fixed basis census required",
    )
    _raises(
        lambda: quintic._require_kernel(algebra, quintic.Span(algebra.d), [], 1, None),
        "quintic_degree: exact invariant kernel dimension differs",
    )

    parameter, theta, polynomial = algebra.primitive(basis)
    record = {
        "primitive_parameter": parameter,
        "primitive_element": quintic._wire_element(theta),
        "polynomial": factors._wire(polynomial),
        "factorization": factors.factor_polynomial(1, polynomial),
    }
    negative = dict(record)
    negative["primitive_parameter"] = -1
    _raises(
        lambda: quintic._require_primitive_binding(algebra, negative, basis, algebra.unit),
        "quintic_degree: exact nonnegative primitive parameter required",
    )
    shifted = dict(record)
    shifted["primitive_element"] = quintic._wire_element(algebra.unit)
    _raises(
        lambda: quintic._require_primitive_binding(algebra, shifted, basis, algebra.unit),
        "quintic_degree: primitive element does not bind to parameter and basis",
    )
    rewritten = dict(record)
    rewritten_polynomial = copy.deepcopy(record["polynomial"])
    rewritten_polynomial[-1] = ["3/1", "0/1"]
    rewritten["polynomial"] = rewritten_polynomial
    _raises(
        lambda: quintic._require_primitive_binding(algebra, rewritten, basis, algebra.unit),
        "quintic_degree: restricted primitive polynomial differs",
    )
    algebra.evaluate = lambda coefficients, element, unit=None: {0: quintic.ONE}  # type: ignore[method-assign]
    _raises(
        lambda: quintic._require_primitive_binding(algebra, record, basis, algebra.unit),
        "quintic_degree: primitive polynomial does not annihilate element",
    )

    _raises(lambda: quintic._root(1, {"factors": []}), "quintic_degree: unique E resolvent root required")
    _raises(
        lambda: quintic._idempotent_scalar([quintic.ZERO], (_Q(1), _Q(0)), 0),
        "quintic_degree: idempotent scalar denominator is zero",
    )
    _raises(lambda: quintic._classify("yes", [6], None), "quintic_degree: exact discriminant Boolean required")
    _raises(lambda: quintic._classify(False, [1, 5], [1]), "quintic_degree: inconsistent resolvent pattern or discriminant")
    _raises(lambda: quintic._require_nonzero(quintic.ZERO), "quintic_degree: irreducible polynomial has zero discriminant")
    _raises(lambda: dispatch({}), "quintic_degree: exact request field census required")
    _raises(
        lambda: dispatch({"operation": "factor", "conductor": 1, "coefficients": []}),
        "quintic_degree: quintic_splitting_degree operation required",
    )
    _raises(lambda: quintic._reject_inexact("1.5"), "quintic_degree: inexact JSON number forbidden")

    frobenius = published["F20"]
    metadata = {key: frobenius[key] for key in ("schema", "authority_effect", "algorithm", "scope", "coefficient_field")}
    metadata["authority_effect"] = "Some"
    _raises(lambda: quintic._require_metadata(metadata, 0), "quintic_degree: metadata binding differs")
    values = factors._parse_polynomial(1, frobenius["coefficients"])
    monic = factors._parse_polynomial(1, frobenius["monic_polynomial"])
    original = {"coefficients": copy.deepcopy(frobenius["coefficients"]), "monic_polynomial": frobenius["monic_polynomial"]}
    original["coefficients"][-1] = ["0/1", "0/1"]
    _raises(
        lambda: quintic._require_polynomial_bindings(1, original, values, monic),
        "quintic_degree: original polynomial binding differs",
    )
    rebound = {"coefficients": frobenius["coefficients"], "monic_polynomial": copy.deepcopy(frobenius["monic_polynomial"])}
    rebound["monic_polynomial"][-1] = ["0/1", "0/1"]
    _raises(
        lambda: quintic._require_polynomial_bindings(1, rebound, values, monic),
        "quintic_degree: monic polynomial binding differs",
    )
    _raises(
        lambda: quintic._require_discriminant(1, monic, 0, {"discriminant": ["0/1", "0/1"], "discriminant_square": frobenius["discriminant_square"]}),
        "quintic_degree: nonzero discriminant binding differs",
    )

    quintic_algebra = SplittingAlgebra(1, _F20)
    localized = copy.deepcopy(frobenius["localized_fixed_algebra"])
    assert isinstance(localized, dict)
    localized["root"] = ["99/1", "0/1"]
    _raises(
        lambda: quintic._validate_localized(quintic_algebra, 1, frobenius["full_fixed_algebra"], localized, quintic_algebra.unit, [quintic.ONE]),
        "quintic_degree: localized E-root binding differs",
    )
    _raises(
        lambda: quintic._require_idempotent(quintic_algebra, {}, quintic_algebra.unit, (_Q(1), _Q(0))),
        "quintic_degree: fiber element is not a nonzero idempotent",
    )
    _raises(
        lambda: quintic._require_idempotent(quintic_algebra, quintic_algebra.unit, quintic_algebra.roots[0], (_Q(1), _Q(0))),
        "quintic_degree: idempotent selects wrong primitive fiber",
    )
    root = quintic._root(1, frobenius["full_fixed_algebra"]["factorization"])
    theta = quintic._parse_element(quintic_algebra, frobenius["full_fixed_algebra"]["primitive_element"])
    resolvent = factors._parse_polynomial(1, frobenius["full_fixed_algebra"]["polynomial"])
    _raises(
        lambda: quintic._resolvent_quotient(quintic_algebra, resolvent, (_Q(99), _Q(0))),
        "quintic_degree: supplied E value is not a resolvent root",
    )
    idempotent = quintic._idempotent(quintic_algebra, resolvent, theta, root)
    moved = quintic_algebra.act

    def _displace(element: dict[int, Any], permutation: object) -> dict[int, Any]:
        if element == idempotent:
            return {0: quintic.ONE}
        return moved(element, permutation)

    quintic_algebra.act = _displace  # type: ignore[method-assign]
    _raises(
        lambda: quintic._require_idempotent(quintic_algebra, idempotent, theta, root),
        "quintic_degree: idempotent is not H-invariant",
    )
    element = quintic._wire_element({0: quintic.ONE})
    _raises(
        lambda: quintic._require_ideal_basis(
            quintic_algebra,
            {"ideal_dimension": 20, "ideal_basis": []},
            quintic_algebra.unit,
            quintic_algebra.d,
        ),
        "quintic_degree: full ideal basis census required",
    )
    _raises(
        lambda: quintic._require_ideal_basis(
            quintic_algebra,
            {"ideal_dimension": 20, "ideal_basis": [element] * 20},
            quintic_algebra.unit,
            quintic_algebra.d,
        ),
        "quintic_degree: independent idempotent-ideal basis required",
    )
    quintic_algebra.localized_basis = lambda _idempotent: []  # type: ignore[method-assign]
    _raises(
        lambda: quintic._require_ideal_rank(quintic_algebra, [{0: quintic.ONE}], {}),
        "quintic_degree: multiplication-by-idempotent rank differs",
    )
    matched = copy.deepcopy(frobenius["localized_fixed_algebra"])
    assert isinstance(matched, dict)
    matched["idempotent"] = element
    _raises(
        lambda: quintic._validate_localized(
            SplittingAlgebra(1, _F20),
            1,
            frobenius["full_fixed_algebra"],
            matched,
            theta,
            resolvent,
        ),
        "quintic_degree: localized idempotent binding differs",
    )

    symmetric = copy.deepcopy(published["S5"])
    symmetric["localized_fixed_algebra"] = {}
    _raises(
        lambda: validate_quintic_degree(1, _S5, symmetric),
        "quintic_degree: inapplicable localized algebra must be null",
    )
    regrouped = copy.deepcopy(published["F20"])
    regrouped["galois_group"] = "S5"
    _raises(
        lambda: validate_quintic_degree(1, _F20, regrouped),
        "quintic_degree: Galois group differs from exact arithmetic",
    )


def test_computed_dimension_guards_fire(monkeypatch: pytest.MonkeyPatch) -> None:
    original = SplittingAlgebra.fixed_basis

    def short_h(self: SplittingAlgebra, permutations: list[tuple[int, ...]], ambient: list[dict[int, Any]] | None = None) -> list[dict[int, Any]]:
        basis = original(self, permutations, ambient)
        if len(permutations) == 2:
            return basis[:5]
        return basis

    monkeypatch.setattr(SplittingAlgebra, "fixed_basis", short_h)
    _raises(lambda: quintic_splitting_degree(1, _F20), "quintic_degree: H-fixed dimension must be six")
    monkeypatch.setattr(SplittingAlgebra, "fixed_basis", original)
    monkeypatch.setattr(SplittingAlgebra, "localized_basis", lambda self, _idempotent: [])
    _raises(lambda: quintic_splitting_degree(1, _F20), "quintic_degree: selected ideal dimension must be twenty")
    monkeypatch.undo()

    def short_cyclic(self: SplittingAlgebra, permutations: list[tuple[int, ...]], ambient: list[dict[int, Any]] | None = None) -> list[dict[int, Any]]:
        basis = original(self, permutations, ambient)
        if len(permutations) == 1:
            return basis[:3]
        return basis

    monkeypatch.setattr(SplittingAlgebra, "fixed_basis", short_cyclic)
    _raises(lambda: quintic_splitting_degree(1, _F20), "quintic_degree: localized C-fixed dimension must be four")


def test_integration_matches_rust_origin_and_factorization(published: dict[str, dict[str, Any]]) -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "quintic_split.rs").read_text(encoding="utf-8")
    assert "Exact finite splitting algebras. Their ranks are not field degrees." in source
    assert "AuthorityEffect: None." in source
    assert "quintic_splitting_degree_v1" in source
    factorization = factor_polynomial(1, _F20)
    assert factorization == published["F20"]["factorization"]
    assert published["F20"]["degree_over_real_field"] == 20
    assert published["S5"]["galois_group"] == "S5"


def test_end_to_end_public_contract(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], published: dict[str, dict[str, Any]]) -> None:
    package = linear_algebra.quintic_split
    request = {
        "operation": "quintic_splitting_degree",
        "conductor": 1,
        "coefficients": published["F20"]["coefficients"],
    }
    assert package.dispatch(request) == published["F20"]
    monkeypatch.setattr(sys, "argv", ["quintic_split.py", "--extra"])
    assert package.main() == 2
    assert "stdin request only" in capsys.readouterr().err
    monkeypatch.setattr(sys, "argv", ["quintic_split.py"])
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(json.dumps(request).encode("ascii")), encoding="ascii"))
    assert package.main() == 0
    stdout = capsys.readouterr().out
    assert json.loads(stdout)["galois_group"] == "F20"
    assert stdout == json.dumps(json.loads(stdout), sort_keys=True, separators=(",", ":")) + "\n"
    floated = b'{"operation":"quintic_splitting_degree","conductor":1.5,"coefficients":[]}'
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(floated), encoding="ascii"))
    assert package.main() == 2
    assert "inexact JSON number forbidden" in capsys.readouterr().err


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "quintic_split.rs"
    assert origin.is_file()
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:quintic-splitting-degree:v1" in source
    assert "Scope Fence:" in source
    assert "Gate 5 measurement:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "schema renamed",
        'SCHEMA = "quintic_splitting_degree_v1"',
        'SCHEMA = "quintic_splitting_degree_v2"',
    ),
    (
        "frobenius degree lowered",
        'return "F20", 20',
        'return "F20", 19',
    ),
    (
        "alternating and symmetric branches swapped",
        'return ("A5", 60) if square else ("S5", 120)',
        'return ("S5", 120) if square else ("A5", 60)',
    ),
    (
        "authority ceiling raised",
        '"authority_effect": "None",\n        "algorithm": ALGORITHM,\n        "scope": SCOPE,\n        "conductor": number,',
        '"authority_effect": "Some",\n        "algorithm": ALGORITHM,\n        "scope": SCOPE,\n        "conductor": number,',
    ),
    (
        "algebra rank decremented",
        '"algebra_rank": algebra.rank,',
        '"algebra_rank": algebra.rank - 1,',
    ),
    (
        "fixed dimension census shifted",
        "if len(basis) != 6:",
        "if len(basis) != 7:",
    ),
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        "if isinstance(value, float):\n        return",
    ),
    (
        "boolean parameter admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where an exact integer was required", role=role)',
        'if False and type(value) is bool:\n        raise _fail("boolean refused where an exact integer was required", role=role)',
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


def _coordinates(values: list[int]) -> list[tuple[Fraction, Fraction]]:
    return [(_Q(value), _Q(0)) for value in values]


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    degree = namespace["quintic_splitting_degree"]
    if not callable(degree):
        return False
    try:
        frobenius = degree(1, _coordinates([1, 0, 0, 0, 0, -2]))
        symmetric = degree(1, _coordinates([1, 0, 0, 0, -1, -1]))
    except error:
        return False
    if not isinstance(frobenius, dict) or not isinstance(symmetric, dict):
        return False
    return bool(
        frobenius.get("schema") == "quintic_splitting_degree_v1"
        and frobenius.get("authority_effect") == "None"
        and frobenius.get("algebra_rank") == 120
        and frobenius.get("galois_group") == "F20"
        and frobenius.get("degree_over_real_field") == 20
        and symmetric.get("galois_group") == "S5"
        and symmetric.get("degree_over_real_field") == 120
        and symmetric.get("discriminant_square", {}).get("is_square") is False
    )


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    degree = namespace["quintic_splitting_degree"]
    algebra_type = namespace["SplittingAlgebra"]
    one = namespace["ONE"]
    if not callable(degree) or not isinstance(algebra_type, type):
        return False
    try:
        algebra = algebra_type(1, _coordinates([1, 0, -1]))
        primitive = getattr(algebra, "primitive", None)
        if not callable(primitive):
            return False
        probes = (
            (lambda: degree(1.0, _coordinates([1, 0, -1])), "float refused at the public boundary"),
            (
                lambda: primitive([{0: one}, {1: one}], parameter=True),
                "boolean refused where an exact integer was required",
            ),
        )
    except error:
        return False
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["QuinticDegreeError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_quintic_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_quintic_{index}"
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
