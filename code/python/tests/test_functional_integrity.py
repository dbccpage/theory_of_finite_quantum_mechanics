"""Owned primal/dual certificates, public constructor and resource controls."""
from dataclasses import FrozenInstanceError
from fractions import Fraction
from itertools import product
from pathlib import Path
import sys
import types

import pytest

from src import functional as facade
from src.functional import l1_seminorm as api


class ClassCallback:
    @property
    def __class__(self):
        raise RuntimeError("must not invoke user class metadata")


class HostileList(list):
    def __iter__(self):
        raise RuntimeError("must refuse user iteration")


class HostileTuple(tuple):
    def __len__(self):
        raise RuntimeError("must refuse user length")


class LeakingFraction(Fraction):
    def __mul__(self, other):
        return 1.0


def submitted(omega=2, reported=2):
    return api.ExactPhi1Certificate([omega], [[0]], [1], [0], [2], [1], reported)


def test_verified_context_is_detached_from_raw_and_exported_witnesses():
    raw = submitted()
    presentation = api.L1Seminorm([[0]], [1])
    result = presentation.verify_certificate(raw)
    assert type(result.value) is Fraction and result.value == Fraction(2)
    raw.omega[0] = 100
    raw.d0[0][0] = 99
    raw.weights[0] = 77
    raw.primal_residual[0] = 88
    assert result.value == Fraction(2)
    snapshot = result.certificate
    assert snapshot.omega == [Fraction(2)] and snapshot.d0 == [[Fraction(0)]]
    assert snapshot.weights == [Fraction(1)] and snapshot.primal_residual == [Fraction(2)]
    snapshot.omega[0] = 999
    result.weights[0] = 0
    result.d0[0][0] = 1000
    assert result.certificate.omega == [Fraction(2)]
    assert result.weights == [Fraction(1)] and result.d0 == [[Fraction(0)]]
    assert result.certificate is not raw


def test_all_public_verified_construction_checks_the_math():
    with pytest.raises(api.L1SeminormError, match="Primal residual mismatch"):
        api.VerifiedExactPhi1(submitted(omega=100))
    with pytest.raises(api.L1SeminormError, match="Duality gap not closed"):
        api.VerifiedExactPhi1(submitted(reported=99))
    assert api.VerifiedExactPhi1(submitted()).value == Fraction(2)
    with pytest.raises(api.L1SeminormError, match="Weight binding mismatch"):
        api.VerifiedExactPhi1(submitted(), api.L1Seminorm([[0]], [2]))
    for value in [ClassCallback(), None, {}, 0]:
        with pytest.raises(api.L1SeminormError, match="submitted ExactPhi1Certificate"):
            api.VerifiedExactPhi1(value)


def test_presentation_and_verified_lifecycle_are_frozen():
    boundary = [[0]]; weights = [1]
    presentation = api.L1Seminorm(boundary, weights)
    result = presentation.verify_certificate(submitted())
    boundary[0][0] = 20; weights[0] = 3
    assert presentation.boundary == [[Fraction(0)]] and presentation.weights == [Fraction(1)]
    with pytest.raises(FrozenInstanceError):
        presentation._weights = (Fraction(99),)
    with pytest.raises(FrozenInstanceError):
        result._parts = ()
    with pytest.raises(api.L1SeminormError, match="already initialized"):
        result.__init__(submitted())
    with pytest.raises(api.L1SeminormError, match="already initialized"):
        presentation.__init__([[0]], [3])
    for cls in [api.L1Seminorm, api.VerifiedExactPhi1]:
        with pytest.raises(TypeError, match="does not admit subclasses"):
            type("UnsafeSubclass", (cls,), {})


def test_scalar_container_and_context_admission_has_no_callbacks():
    for value in [ClassCallback(), LeakingFraction(1), True]:
        with pytest.raises(api.L1SeminormError):
            api.require_rational(value, "fixture")
    for values in [ClassCallback(), HostileList([1]), HostileTuple((1,))]:
        with pytest.raises(api.L1SeminormError):
            api.require_vector(values, "fixture")
    with pytest.raises(api.L1SeminormError, match="not an exact rational"):
        api.evaluate_weighted_l1_quotient([[0]], [LeakingFraction(1)], [1], [0], [1], [1], 1)
    with pytest.raises(api.L1SeminormError):
        api.require_rational(1, ClassCallback())
    with pytest.raises(api.L1SeminormError, match="role length budget exceeded"):
        api.require_vector([1], "x" * 241)
    assert api.require_rational(1, "x" * 256) == Fraction(1)
    with pytest.raises(api.L1SeminormError, match="role length budget exceeded"):
        api.require_rational(1, "x" * 257)


def test_policy_is_declared_and_boundary_admission_is_bounded():
    assert (api.MAX_VECTOR_LENGTH, api.MAX_COORDINATES, api.MAX_BOUNDARY_COLUMNS,
            api.MAX_BOUNDARY_ENTRIES, api.MAX_INPUT_BITS, api.MAX_WORK_BITS, api.MAX_ROLE_CHARACTERS) == (4096, 256, 256, 16384, 1024, 8192, 256)
    assert len(api.require_vector([0] * 4096, "edge")) == 4096
    with pytest.raises(api.L1SeminormError, match="vector entry budget exceeded"):
        api.require_vector([0] * 4097, "edge")
    with pytest.raises(api.L1SeminormError, match="coordinate budget exceeded"):
        api.L1Seminorm([[]] * 257, [1] * 257)
    with pytest.raises(api.L1SeminormError, match="coordinate budget exceeded"):
        api.require_positive_weights([1] * 257)
    with pytest.raises(api.L1SeminormError, match="height budget exceeded"):
        api.L1Seminorm([[]] * 257, [1])
    with pytest.raises(api.L1SeminormError, match="width budget exceeded"):
        api.L1Seminorm([[0] * 257], [1])
    with pytest.raises(api.L1SeminormError, match="entry budget exceeded"):
        api.L1Seminorm([[0] * 129 for _ in range(128)], [1] * 128)
    assert len(api.L1Seminorm([[]] * 256, [1] * 256).boundary) == 256
    assert len(api.L1Seminorm([[0] * 256], [1]).boundary[0]) == 256
    assert len(api.L1Seminorm([[0] * 128 for _ in range(128)], [1] * 128).boundary) == 128
    for value in [1 << 1024, -(1 << 20000), Fraction(1, 1 << 1024), (1, 1 << 1024)]:
        with pytest.raises(api.L1SeminormError, match="bit budget exceeded"):
            api.require_rational(value, "bits")


def test_work_budget_refusal_is_typed(monkeypatch):
    monkeypatch.setattr(api, "MAX_WORK_BITS", 3)
    # 3/5 is admitted at the input boundary; 9/25 needs more than 3 bits.
    cert = api.ExactPhi1Certificate([Fraction(3, 5)], [[0]], [Fraction(3, 5)], [0],
                                  [Fraction(3, 5)], [Fraction(3, 5)], Fraction(9, 25))
    with pytest.raises(api.L1SeminormError, match="bit budget exceeded") as cost:
        api.VerifiedExactPhi1(cert)
    assert cost.value.parameters["role"] == "weighted l1"
    repaired = api.ExactPhi1Certificate([Fraction(9, 25)], [[Fraction(3, 5)]], [1],
                                       [Fraction(3, 5)], [0], [0], 0)
    with pytest.raises(api.L1SeminormError, match="bit budget exceeded") as dot:
        api.VerifiedExactPhi1(repaired)
    assert dot.value.parameters["role"] == "dot product"
    orthogonal = api.ExactPhi1Certificate([0, 0], [[Fraction(3, 5)], [Fraction(3, 5)]], [1, 1],
        [0], [0, 0], [Fraction(3, 5), Fraction(-3, 5)], 0)
    with pytest.raises(api.L1SeminormError, match="bit budget exceeded") as column:
        api.VerifiedExactPhi1(orthogonal)
    assert column.value.parameters["role"] == "dual column pairing"


def test_nonzero_certificates_against_closed_one_column_problem():
    # For B=(1,1)^T and weights (p,q), the exact minimum is
    # min(p,q)*abs(x-y), attained by repairing to the heavier coordinate.
    for p, q, x, y in product(range(1, 4), range(1, 4), range(-2, 3), range(-2, 3)):
        shift = y if p <= q else x
        difference = x - y
        sign = (difference > 0) - (difference < 0)
        dual = min(p, q) * sign
        expected = min(p, q) * abs(difference)
        result = api.evaluate_weighted_l1_quotient([[1], [1]], [p, q], [x, y], [shift],
            [x - shift, y - shift], [dual, -dual], expected)
        assert type(result) is Fraction and result == Fraction(expected)
    assert api.evaluate_weighted_l1_quotient([], [], [], [], [], [], 0) == Fraction(0)


def test_frontend_guards_before_certificate_provider(monkeypatch):
    def must_not_delegate(*args):
        raise AssertionError("invalid frontend input reached provider")
    monkeypatch.setattr(facade, "evaluate_weighted_l1_quotient", must_not_delegate)
    for value in [HostileTuple(((1, 0), (-1, 0))), ((ClassCallback(), 0), (-1, 0)),
                  (((1 << 1024), 0), (-1, 0))]:
        with pytest.raises(api.L1SeminormError):
            facade.exported_zero_phi1(boundary=value)


def test_checker_witness_and_invalid_candidate_controls(monkeypatch):
    from src.functional import test_exported_zero_phi1 as checks
    assert checks.witness_zero() == Fraction(0)
    assert checks.witness_pair() == 2 and checks.witness_weight() == 1
    assert checks.witness_guard() == "float refused at the public boundary"
    with pytest.raises(checks.ClaimCheckError):
        checks.parse_exact_entry(ClassCallback())
    with pytest.raises(KeyError):
        checks._safe_holds({})
    with pytest.raises(KeyError):
        checks._safe_self({})
    name = "functional_invalid_lifecycle_guard"
    marker = types.ModuleType(name)
    monkeypatch.setitem(sys.modules, name, marker)
    source = Path(checks._LIBRARY).read_text()
    for old, new in [("return evaluate_weighted_l1_quotient(", "return evaluate_weighted_l1_quotient(("),
                     ("from fractions import Fraction", "import __functional_missing_dependency__")]:
        assert source.count(old) == 1
        with pytest.raises(checks.ClaimCheckError, match="not counted as a kill"):
            checks._one_mutant(source, ("invalid candidate", old, new), name, str(checks._LIBRARY), checks._safe_holds)
        assert sys.modules[name] is marker
