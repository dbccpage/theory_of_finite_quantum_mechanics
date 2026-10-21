"""Independent rational controls and lifecycle challenges for the bounded simplex.

Scope: finite Python API and its engineering budgets, not a Born-rule proof.
"""
from dataclasses import FrozenInstanceError
from fractions import Fraction
from itertools import product

import pytest

from src.finite_probability import simplex as api


def test_declared_policy_matches_the_contract():
    assert (api.MAX_DIMENSION, api.MAX_MATRIX_ENTRIES, api.MAX_INPUT_BITS,
            api.MAX_WORK_BITS, api.MAX_LABEL_LENGTH) == (4096, 65536, 1024, 8192, 256)


class HostileList(list):
    def __iter__(self):
        raise RuntimeError("the API must refuse before invoking user iteration")


class HostileTuple(tuple):
    def __iter__(self):
        raise RuntimeError("the API must refuse before invoking user iteration")

    def __len__(self):
        raise RuntimeError("the API must refuse before invoking user length")


class ClassCallback:
    @property
    def __class__(self):
        raise RuntimeError("the API must refuse without consulting user __class__")


def test_scalar_and_container_checks_do_not_consult_user_class():
    for operation in [lambda: api.ProbabilitySimplex([ClassCallback()]),
                      lambda: api.ProbabilitySimplex(ClassCallback()),
                      lambda: api.ProbabilitySimplex.uniform(ClassCallback()),
                      lambda: api.StochasticMap(ClassCallback())]:
        with pytest.raises(api.SimplexError):
            operation()


def test_freeze_and_snapshot_lifecycle():
    raw = [Fraction(1, 3), Fraction(2, 3)]
    state = api.ProbabilitySimplex(raw)
    raw[0] = 0
    copy = state.probs
    copy[0] = 0
    assert tuple(state) == (Fraction(1, 3), Fraction(2, 3))
    assert state[-1] == Fraction(2, 3)
    assert state != object()
    assert state == api.ProbabilitySimplex([(1, 3), (2, 3)])
    assert state != api.ProbabilitySimplex([1, 0])
    for attribute, replacement in [("_probs", (0,)), ("label", "corrupt")]:
        with pytest.raises(FrozenInstanceError):
            setattr(state, attribute, replacement)
    with pytest.raises(TypeError, match="does not admit subclasses"):
        type("UnsafeState", (api.ProbabilitySimplex,), {})
    with pytest.raises(TypeError, match="does not admit subclasses"):
        type("UnsafeMap", (api.StochasticMap,), {})
    matrix = [[0, 1], [1, 0]]
    channel = api.StochasticMap(matrix)
    matrix[0][0] = 1
    assert channel.rows == channel.cols == 2
    assert channel.apply(state).probs == [Fraction(2, 3), Fraction(1, 3)]
    with pytest.raises(FrozenInstanceError):
        channel._data = ((1,),)
    with pytest.raises(api.SimplexError, match="already initialized"):
        state.__init__([1])
    with pytest.raises(api.SimplexError, match="already initialized"):
        channel.__init__([[1]])
    assert state.dim == channel.rows == 2


@pytest.mark.parametrize("value", [HostileList([1]), HostileTuple((1,))])
def test_container_callbacks_are_not_executed(value):
    state = api.ProbabilitySimplex([1])
    for operation in [lambda: api.ProbabilitySimplex(value), lambda: state.expectation(value),
                      lambda: api.StochasticMap(value), lambda: api.StochasticMap([value])]:
        with pytest.raises(api.SimplexError, match="container subclass refused"):
            operation()
    with pytest.raises(api.SimplexError, match="not an exact rational"):
        api.ProbabilitySimplex([HostileTuple((1, 1))])


@pytest.mark.parametrize("index", [True, False, Fraction(0), "0", slice(None), 1, -2])
def test_indices_have_typed_refusals(index):
    with pytest.raises(api.SimplexError):
        api.ProbabilitySimplex([1])[index]


@pytest.mark.parametrize("weights", [[(1, 0)], [(1,)], [(True, 1)], [object()], [0], [-1, 2]])
def test_scalar_and_mass_refusals(weights):
    with pytest.raises(api.SimplexError):
        api.ProbabilitySimplex(weights)


def test_resource_policy_edges_and_refusal_before_allocation():
    maximum = api.ProbabilitySimplex.uniform(api.MAX_DIMENSION)
    assert maximum.dim == api.MAX_DIMENSION
    assert maximum[0] == Fraction(1, api.MAX_DIMENSION)
    with pytest.raises(api.SimplexError, match="dimension budget exceeded"):
        api.ProbabilitySimplex.uniform(api.MAX_DIMENSION + 1)
    with pytest.raises(api.SimplexError, match="sequence budget exceeded"):
        api.ProbabilitySimplex([0] * (api.MAX_DIMENSION + 1))
    row = [1] + [0] * (api.MAX_DIMENSION - 1)
    with pytest.raises(api.SimplexError, match="matrix entry budget exceeded"):
        api.StochasticMap([row] * (api.MAX_MATRIX_ENTRIES // len(row) + 1))
    # Large integer fixtures are already allocated by the caller. No huge string
    # rendering or Fraction normalization is needed to refuse their bit length.
    huge = 1 << api.MAX_INPUT_BITS
    for value in [huge, Fraction(1, huge), Fraction(huge + 1, 2), (1, huge)]:
        with pytest.raises(api.SimplexError, match="bit budget exceeded"):
            api.ProbabilitySimplex([value])
    assert api.ProbabilitySimplex([1], "x" * api.MAX_LABEL_LENGTH).dim == 1
    with pytest.raises(api.SimplexError, match="label budget exceeded"):
        api.ProbabilitySimplex([1], "x" * (api.MAX_LABEL_LENGTH + 1))


def test_accumulator_budget_preserves_exactness_or_refuses(monkeypatch):
    # Lowering the policy exercises accumulation refusal without a costly input.
    # 1/2 and 1/3 fit 2 bits; their sum 5/6 requires 3 bits.
    state = api.ProbabilitySimplex([Fraction(1, 2), Fraction(1, 2)])
    monkeypatch.setattr(api, "MAX_WORK_BITS", 2)
    with pytest.raises(api.SimplexError, match="bit budget exceeded"):
        state.expectation([1, Fraction(2, 3)])


def test_shape_and_composition_refusals():
    state = api.ProbabilitySimplex([1])
    for operation in [lambda: state.total_variation_distance([1]),
                      lambda: state.total_variation_distance(api.ProbabilitySimplex.uniform(2)),
                      lambda: state.mixture(state, -1), lambda: state.mixture(state, 2),
                      lambda: state.mixture(api.ProbabilitySimplex.uniform(2), 0),
                      lambda: state.expectation([]), lambda: api.StochasticMap([]),
                      lambda: api.StochasticMap([[]]), lambda: api.StochasticMap([[1], [0, 1]]),
                      lambda: api.StochasticMap([[1, -1]]), lambda: api.StochasticMap([[0]]),
                      lambda: api.StochasticMap([[1]]).apply(api.ProbabilitySimplex.uniform(2)),
                      lambda: api.ProbabilitySimplex.uniform(0),
                      lambda: api.ProbabilitySimplex.dirac(1, 1),
                      lambda: api.ProbabilitySimplex([1], label=object())]:
        with pytest.raises(api.SimplexError):
            operation()


def test_generated_small_rational_domains_against_integer_formulas():
    # Independent integer numerators provide exact expected values; no source
    # helper computes the oracle. All two-state distributions at scale 1..8.
    for scale in range(1, 9):
        for left, right in product(range(scale + 1), repeat=2):
            p = api.ProbabilitySimplex([(left, scale), (scale - left, scale)])
            q = api.ProbabilitySimplex([(right, scale), (scale - right, scale)])
            assert p.total_variation_distance(q) == Fraction(abs(left - right), scale)
            assert p.expectation([2, -1]) == Fraction(3 * left - scale, scale)
            for m in range(4):
                mix = p.mixture(q, Fraction(m, 3))
                first = Fraction(m * left + (3 - m) * right, 3 * scale)
                assert mix.probs == [first, 1 - first]
                assert all(type(value) is Fraction for value in mix.probs)
            # Row map (1/3,2/3), (1,0) gives (1 - 2p/3, 2p/3).
            output = api.StochasticMap([[(1, 3), (2, 3)], [1, 0]]).apply(p)
            assert output.probs == [Fraction(3 * scale - 2 * left, 3 * scale),
                                    Fraction(2 * left, 3 * scale)]
