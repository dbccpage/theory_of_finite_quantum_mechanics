"""Unit, integration, end-to-end, negative, and mutation certificates for GR003.

Origin: papers/derivations/relational_point_coincidence/relational_point_coincidence_and_witnessed_difference_claim_ledger.md
Claim: urn:omega:fqm:gr003:relational-coincidence-falsification:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/relational_point_coincidence/code/tests/test_relational_spacetime.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 10; AST Sonar cognitive complexity max 8; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 9.
Scope Fence: Killing a mutant certifies this harness, not continuous general relativity and not quantum gravity.
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from fractions import Fraction
from typing import cast
from pathlib import Path
from types import ModuleType

import pytest

from relational_spacetime import (
    DressingFieldProjection,
    DualWitnessCertificate,
    EventTuple,
    ExactRationalDualWitness,
    RelationalCertificateError,
    SpacetimeRelation,
)

_CODE = Path(__file__).resolve().parents[1]
_LIBRARY = _CODE / "relational_spacetime.py"
_INIT = _CODE / "__init__.py"
_CONFTEST = Path(__file__).resolve().parent / "conftest.py"
_LOADED: list[str] = []

_LIBRARY_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("float gate", "isinstance(value, float)", "isinstance(value, complex)"),
    ("unit ball", "norm > Fraction(1)", "norm >= Fraction(1)"),
    ("lower bound", "dual_value < claimed", "dual_value <= claimed"),
    ("rpcnf width", "len(key) != 4", "len(key) != 3"),
    ("dependency", "seen[lhs_vals] == rhs_vals", "seen[lhs_vals] != rhs_vals"),
    ("divergence", "value != 0", "value != 1"),
    ("idempotence", "dressed_1 == dressed_2", "dressed_1 != dressed_2"),
    ("heath rows", "set(self.tuples) == set(rebuilt.tuples)", "set(self.tuples) != set(rebuilt.tuples)"),
)

_INIT_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("key float", "isinstance(value, float)", "isinstance(value, complex)"),
    ("key width", "len(names) != 4", "len(names) != 5"),
    ("coincide", "left.project(names) == right.project(names)", "left.project(names) != right.project(names)"),
)

_CONFTEST_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("fixture width", "return 4", "return 5"),
    ("fixture rpcnf", "certificate.is_rpcnf is not True", "certificate.is_rpcnf is not False"),
    ("fixture float", "isinstance(value, float)", "isinstance(value, complex)"),
)

_HARNESS_MUTANTS: tuple[tuple[str, str, str], ...] = (
    ("pairing add", "total += left * " + "right", "total += left + right"),
    ("pairing target", "total != Fraction(" + "3)", "total != Fraction(4)"),
    ("float oracle", "type(value) is " + "float", "type(value) is complex"),
    ("bool oracle", "type(value) is " + "bool", "type(value) is int"),
)


class HarnessOracleError(ValueError):
    """One violated falsification invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: dict[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> HarnessOracleError:
    return HarnessOracleError(invariant, parameters)


def _as_fraction(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("independent witness entry is not rational", received=type(value).__name__)


def independent_c3_pairing(witness: object = None) -> Fraction:
    """Hand total of the standard cycle witness against omega = (1, 1, 1)."""
    if witness is None:
        raw: tuple[object, ...] = (Fraction(1), Fraction(1), Fraction(1))
    elif isinstance(witness, tuple):
        raw = witness
    else:
        raise _fail("independent witness is not a triple", received=type(witness).__name__)
    parts = tuple(_as_fraction(item) for item in raw)
    total = Fraction(0)
    for left, right in zip(parts, (Fraction(1), Fraction(1), Fraction(1)), strict=True):
        total += left * right
    if total != Fraction(3):
        raise _fail("independent cycle pairing is not 3", total=str(total))
    return total


def refuse_harness_scalar(value: object) -> str:
    """Refuse float and bool probes before any arithmetic."""
    if type(value) is float:
        raise _fail("float refused at the public boundary", role="harness", received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role="harness")
    return type(value).__name__


def _cycle_boundary() -> list[list[Fraction]]:
    return [
        [Fraction(-1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(-1), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(-1)],
    ]


def _gauge_action(group: object, state: object) -> tuple[Fraction, Fraction]:
    if not isinstance(group, Fraction) or not isinstance(state, tuple):
        raise _fail("gauge action received a non-rational state")
    theta = state[0]
    potential = state[1]
    if not isinstance(theta, Fraction) or not isinstance(potential, Fraction):
        raise _fail("gauge state is not a rational pair")
    return (theta + group, potential)


def _dressing_field(state: object) -> Fraction:
    if not isinstance(state, tuple) or not isinstance(state[0], Fraction):
        raise _fail("dressing field received a non-rational state")
    return -state[0]


def _two_observer_relation() -> SpacetimeRelation:
    attributes = {"phi0", "phi1", "phi2", "phi3", "obs_alpha_curr", "obs_beta_temp"}
    first = EventTuple(
        {
            "phi0": Fraction(1),
            "phi1": Fraction(0),
            "phi2": Fraction(0),
            "phi3": Fraction(0),
            "obs_alpha_curr": Fraction(100),
            "obs_beta_temp": Fraction(300),
        }
    )
    second = EventTuple(
        {
            "phi0": Fraction(2),
            "phi1": Fraction(1),
            "phi2": Fraction(0),
            "phi3": Fraction(0),
            "obs_alpha_curr": Fraction(200),
            "obs_beta_temp": Fraction(273),
        }
    )
    return SpacetimeRelation(attributes, [first, second])


def _fixture(name: str) -> Callable[..., object]:
    module = _load_path(_CONFTEST, "rpc_conftest_live")
    value = getattr(module, name)
    if not callable(value):
        raise _fail("harness fixture is not callable", fixture=name)
    return cast(Callable[..., object], value)


def _three_point() -> SpacetimeRelation:
    built = _fixture("canonical_three_point")()
    if not isinstance(built, SpacetimeRelation):
        raise _fail("canonical fixture was not a relation")
    return built


def _harness_width() -> int:
    value = _fixture("harness_key_width")()
    if type(value) is not int:
        raise _fail("harness width was not an integer", received=type(value).__name__)
    return value


def test_unit_rpcnf_key_and_dependency() -> None:
    relation = _three_point()
    key = {"phi0", "phi1", "phi2", "phi3"}
    assert relation.is_superkey(key) is True
    assert relation.check_functional_dependency({"phi1", "phi2", "phi3"}, {"matter_density"}) is True
    certificate = relation.check_rpcnf(key, {"t", "x", "y", "z"})
    assert certificate.is_rpcnf is True
    assert certificate.violations == ()
    assert certificate.tuple_count == 3


def test_unit_dual_witness_matches_independent_total() -> None:
    certificate = ExactRationalDualWitness.verify_dual_witness(
        _cycle_boundary(),
        [Fraction(1), Fraction(1), Fraction(1)],
        [Fraction(1), Fraction(1), Fraction(1)],
        Fraction(3),
    )
    assert isinstance(certificate, DualWitnessCertificate)
    assert certificate.dual_value == independent_c3_pairing()
    assert certificate.inf_norm == Fraction(1)
    assert certificate.is_divergence_free is True


def test_unit_dressing_retraction() -> None:
    projection = DressingFieldProjection(_gauge_action, _dressing_field)
    initial = (Fraction(3, 4), Fraction(42, 1))
    assert projection.dress(initial) == (Fraction(0), Fraction(42, 1))
    assert projection.verify_idempotence(initial) is True
    assert projection.verify_gauge_invariance(initial, Fraction(5, 7)) is True


def test_integration_heath_join_preserves_observers() -> None:
    relation = _two_observer_relation()
    key = {"phi0", "phi1", "phi2", "phi3"}
    assert relation.verify_heaths_theorem(key, {"obs_alpha_curr"}, {"obs_beta_temp"}) is True
    rebuilt = relation.project(key | {"obs_alpha_curr"}).natural_join(relation.project(key | {"obs_beta_temp"}))
    assert set(rebuilt.tuples) == set(relation.tuples)


def test_integration_fixture_and_package_key() -> None:
    init = _load_path(_INIT, "rpc_pkg_init_live")
    relation = _three_point()
    left = relation.tuples[0]
    right = relation.tuples[1]
    key = {"phi0", "phi1", "phi2", "phi3"}
    coincide = init.points_coincide
    width = init.witnessed_key_width
    assert width(key) == _harness_width()
    assert coincide(left, left, key) is True
    assert coincide(left, right, key) is False


def test_e2e_rpcnf_heath_dressing_and_dual() -> None:
    relation = _three_point()
    key = {"phi0", "phi1", "phi2", "phi3"}
    rpcnf = relation.check_rpcnf(key, {"t", "x", "y", "z"})
    observers = _two_observer_relation()
    projection = DressingFieldProjection(_gauge_action, _dressing_field)
    dual = ExactRationalDualWitness.verify_dual_witness(
        _cycle_boundary(),
        [Fraction(1), Fraction(1), Fraction(1)],
        [Fraction(1), Fraction(1), Fraction(1)],
        Fraction(3),
    )
    assert rpcnf.is_rpcnf is True
    assert observers.verify_heaths_theorem(key, {"obs_alpha_curr"}, {"obs_beta_temp"}) is True
    assert projection.dress((Fraction(3, 4), Fraction(42, 1))) == (Fraction(0), Fraction(42, 1))
    assert dual.certified_lower_bound == Fraction(3)


def test_negative_boundary_refusals() -> None:
    with pytest.raises(RelationalCertificateError, match="float refused") as floated:
        EventTuple({"phi0": 1.5})
    assert floated.value.parameters["role"] == "event value"
    with pytest.raises(RelationalCertificateError, match="boolean refused"):
        EventTuple({"phi0": True})
    with pytest.raises(RelationalCertificateError, match="undeclared attributes"):
        SpacetimeRelation({"phi0"}, [EventTuple({"phi0": 1, "extra": 2})])
    with pytest.raises(RelationalCertificateError, match="not an exact rational"):
        ExactRationalDualWitness.verify_dual_witness([["1"]], ["1"], ["1"], 0)
    with pytest.raises(RelationalCertificateError, match="jagged rational matrix"):
        ExactRationalDualWitness.verify_dual_witness([[Fraction(1), Fraction(0)], [Fraction(1)]], [Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)], Fraction(0))
    with pytest.raises(RelationalCertificateError, match="not divergence-free"):
        ExactRationalDualWitness.verify_dual_witness(
            _cycle_boundary(),
            [Fraction(1), Fraction(1), Fraction(1)],
            [Fraction(1), Fraction(0), Fraction(0)],
            Fraction(0),
        )
    with pytest.raises(RelationalCertificateError, match="unit infinity ball") as ball:
        ExactRationalDualWitness.verify_dual_witness(
            _cycle_boundary(),
            [Fraction(1), Fraction(0), Fraction(0)],
            [Fraction(2), Fraction(2), Fraction(2)],
            Fraction(0),
        )
    assert ball.value.parameters["inf_norm"] == "2"
    with pytest.raises(RelationalCertificateError, match="below the claimed quotient") as low:
        ExactRationalDualWitness.verify_dual_witness(
            _cycle_boundary(),
            [Fraction(1), Fraction(1), Fraction(1)],
            [Fraction(1), Fraction(1), Fraction(1)],
            Fraction(4),
        )
    assert low.value.parameters["claimed"] == "4"


def test_negative_rpcnf_and_package_key() -> None:
    attributes = {"phi0", "phi1", "phi2", "phi3", "t", "x"}
    row = EventTuple(
        {
            "phi0": Fraction(1),
            "phi1": Fraction(0),
            "phi2": Fraction(0),
            "phi3": Fraction(0),
            "t": Fraction(0),
            "x": Fraction(1),
        }
    )
    relation = SpacetimeRelation(attributes, [row])
    certificate = relation.check_rpcnf({"phi0", "phi1", "phi2", "phi3"}, {"t", "x", "y", "z"})
    assert certificate.is_rpcnf is False
    assert any("Forbidden coordinate" in item for item in certificate.violations)
    init = _load_path(_INIT, "rpc_pkg_init_negative")
    with pytest.raises(RelationalCertificateError, match="float refused"):
        init.witnessed_key_width({"phi0", "phi1", "phi2", 1.5})
    with pytest.raises(RelationalCertificateError, match="width is not 4"):
        init.witnessed_key_width({"phi0", "phi1", "phi2"})
    with pytest.raises(HarnessOracleError, match="float refused"):
        refuse_harness_scalar(1.5)
    with pytest.raises(HarnessOracleError, match="boolean refused"):
        refuse_harness_scalar(True)
    with pytest.raises(HarnessOracleError, match="not 3"):
        independent_c3_pairing((Fraction(1), Fraction(1), Fraction(0)))


def _load_path(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise _fail("module spec was not created", path=str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    _LOADED.append(name)
    spec.loader.exec_module(module)
    return module


def _library_positive(namespace: dict[str, object]) -> bool:
    relation_type = namespace["SpacetimeRelation"]
    event_type = namespace["EventTuple"]
    witness_type = namespace["ExactRationalDualWitness"]
    dressing_type = namespace["DressingFieldProjection"]
    if not isinstance(relation_type, type) or not isinstance(event_type, type):
        return False
    if not isinstance(witness_type, type) or not isinstance(dressing_type, type):
        return False
    row = event_type({"phi0": Fraction(1), "phi1": Fraction(0), "phi2": Fraction(0), "phi3": Fraction(0), "matter_density": Fraction(10)})
    relation = relation_type({"phi0", "phi1", "phi2", "phi3", "matter_density"}, [row])
    certificate = relation.check_rpcnf({"phi0", "phi1", "phi2", "phi3"}, {"t", "x", "y", "z"})
    if certificate.is_rpcnf is not True:
        return False
    duplicate = relation_type({"phi0", "phi1", "phi2", "phi3", "matter_density"}, [row, row])
    if duplicate.check_functional_dependency({"phi0"}, {"matter_density"}) is not True:
        return False
    verify = getattr(witness_type, "verify_dual_witness")
    dual = verify(
        _cycle_boundary(),
        [Fraction(1), Fraction(1), Fraction(1)],
        [Fraction(1), Fraction(1), Fraction(1)],
        Fraction(3),
    )
    if getattr(dual, "dual_value") != Fraction(3):
        return False
    observers = _two_observer_relation_from(event_type, relation_type)
    heath = getattr(observers, "verify_heaths_theorem")
    if heath({"phi0", "phi1", "phi2", "phi3"}, {"obs_alpha_curr"}, {"obs_beta_temp"}) is not True:
        return False
    projection = dressing_type(_gauge_action, _dressing_field)
    return projection.verify_idempotence((Fraction(3, 4), Fraction(42))) is True


def _two_observer_relation_from(event_type: type, relation_type: type) -> object:
    attributes = {"phi0", "phi1", "phi2", "phi3", "obs_alpha_curr", "obs_beta_temp"}
    first = event_type(
        {
            "phi0": Fraction(1),
            "phi1": Fraction(0),
            "phi2": Fraction(0),
            "phi3": Fraction(0),
            "obs_alpha_curr": Fraction(100),
            "obs_beta_temp": Fraction(300),
        }
    )
    second = event_type(
        {
            "phi0": Fraction(2),
            "phi1": Fraction(1),
            "phi2": Fraction(0),
            "phi3": Fraction(0),
            "obs_alpha_curr": Fraction(200),
            "obs_beta_temp": Fraction(273),
        }
    )
    return relation_type(attributes, [first, second])


def _library_negative(namespace: dict[str, object]) -> bool:
    error = namespace["RelationalCertificateError"]
    event_type = namespace["EventTuple"]
    witness_type = namespace["ExactRationalDualWitness"]
    if not isinstance(error, type) or not isinstance(event_type, type) or not isinstance(witness_type, type):
        return False
    probes = (
        (lambda: event_type({"phi0": 1.5}), "float refused at the public boundary"),
        (lambda: event_type({"phi0": True}), "boolean refused where a rational was required"),
        (
            lambda: getattr(witness_type, "verify_dual_witness")(
                _cycle_boundary(),
                [Fraction(1), Fraction(1), Fraction(1)],
                [Fraction(1), Fraction(0), Fraction(0)],
                Fraction(0),
            ),
            "dual witness is not divergence-free",
        ),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _invariant(error: type[BaseException], probe: Callable[[], object]) -> str:
    try:
        probe()
    except error as caught:
        invariant = getattr(caught, "invariant", "")
        if isinstance(invariant, str):
            return invariant
    return ""


def _library_oracle(namespace: dict[str, object]) -> bool:
    if not _library_positive(namespace):
        return False
    return _library_negative(namespace)


def _init_oracle(namespace: dict[str, object]) -> bool:
    width = namespace["witnessed_key_width"]
    coincide = namespace["points_coincide"]
    error = namespace["RelationalCertificateError"]
    event_type = namespace["EventTuple"]
    if not callable(width) or not callable(coincide) or not isinstance(error, type) or not isinstance(event_type, type):
        return False
    key = {"phi0", "phi1", "phi2", "phi3"}
    if width(key) != 4:
        return False
    left = event_type({"phi0": Fraction(1), "phi1": Fraction(0), "phi2": Fraction(0), "phi3": Fraction(0)})
    right = event_type({"phi0": Fraction(2), "phi1": Fraction(0), "phi2": Fraction(0), "phi3": Fraction(0)})
    if coincide(left, left, key) is not True or coincide(left, right, key) is not False:
        return False
    return _invariant(error, lambda: width({"a", "b", "c", 1.5})) == "float refused at the public boundary"


def _conftest_oracle(namespace: dict[str, object]) -> bool:
    width = namespace["harness_key_width"]
    build = namespace["canonical_three_point"]
    refuse = namespace["refuse_float_probe"]
    error = namespace["RelationalCertificateError"]
    if not callable(width) or not callable(build) or not callable(refuse) or not isinstance(error, type):
        return False
    if width() != 4:
        return False
    relation = build()
    certificate = relation.check_rpcnf({"phi0", "phi1", "phi2", "phi3"}, {"t", "x", "y", "z"})
    if certificate.is_rpcnf is not True or certificate.tuple_count != 3:
        return False
    return _invariant(error, lambda: refuse(1.5)) == "float refused at the public boundary"


def _harness_oracle(namespace: dict[str, object]) -> bool:
    pairing = namespace["independent_c3_pairing"]
    refuse = namespace["refuse_harness_scalar"]
    error = namespace["HarnessOracleError"]
    if not callable(pairing) or not callable(refuse) or not isinstance(error, type):
        return False
    if pairing() != Fraction(3):
        return False
    if _invariant(error, lambda: refuse(1.5)) != "float refused at the public boundary":
        return False
    return _invariant(error, lambda: refuse(True)) == "boolean refused where a rational was required"


def _survived(source: str, name: str, oracle: Callable[[dict[str, object]], bool]) -> bool:
    try:
        loaded = _load_source(source, name)
        return oracle(loaded.__dict__)
    except Exception:
        return False


def _load_source(source: str, name: str) -> ModuleType:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise _fail("source spec was not created", module=name)
    module = ModuleType(name)
    module.__spec__ = spec
    module.__file__ = name + ".py"
    sys.modules[name] = module
    _LOADED.append(name)
    exec(compile(source, name + ".py", "exec"), module.__dict__)
    return module


def _kill(source: str, mutants: tuple[tuple[str, str, str], ...], oracle: Callable[[dict[str, object]], bool], label: str) -> int:
    killed = 0
    for index, (name, old, new) in enumerate(mutants):
        count = source.count(old)
        if count != 1:
            raise _fail("mutant site was not unique", mutant=name, count=count, label=label)
        survived = _survived(source.replace(old, new, 1), f"{label}_{index}", oracle)
        if survived:
            raise _fail("mutant survived", mutant=name, label=label)
        killed += 1
    return killed


def test_mutation_suite_kills_library_init_and_harness() -> None:
    library = _LIBRARY.read_text(encoding="utf-8")
    init_source = _INIT.read_text(encoding="utf-8")
    conftest_source = _CONFTEST.read_text(encoding="utf-8")
    harness_source = Path(__file__).read_text(encoding="utf-8")
    assert _library_oracle(_load_source(library, "rpc_library_baseline").__dict__) is True
    library_kills = _kill(library, _LIBRARY_MUTANTS, _library_oracle, "lib")
    init_kills = _kill(init_source, _INIT_MUTANTS, _init_oracle, "init")
    conftest_kills = _kill(conftest_source, _CONFTEST_MUTANTS, _conftest_oracle, "conf")
    harness_kills = _kill(harness_source, _HARNESS_MUTANTS, _harness_oracle, "harness")
    assert library_kills == 8
    assert init_kills == 3
    assert conftest_kills == 3
    assert harness_kills == 4
    assert "Mutation-Kills: 8 non-equivalent" in library
    assert "Mutation-Kills: 3 non-equivalent" in init_source
    assert "Mutation-Kills: 3 non-equivalent" in conftest_source
    assert "Mutation-Kills: 4 non-equivalent" in harness_source


def teardown_module() -> None:
    for name in _LOADED:
        sys.modules.pop(name, None)
