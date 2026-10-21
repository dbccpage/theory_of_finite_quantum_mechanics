"""Independent finite counting oracles, policy edges and immutable record tests."""
from dataclasses import FrozenInstanceError
from itertools import combinations, product
from math import comb
from pathlib import Path
import sys
import types

import pytest

from src import combinatorics as exported
from src.combinatorics import finite_combinatorics as api


def test_policy_is_declared_not_an_empirical_constant():
    assert (api.MAX_INPUT_BITS, api.MAX_BINOMIAL_STEPS, api.MAX_BINOMIAL_BITS) == (1024, 4096, 8192)
    assert (api.MAX_WORD_LENGTH, api.MAX_WORDS, api.MAX_WORD_CELLS) == (256, 4096, 65536)
    assert (api.MAX_PARTITION_N, api.MAX_PARTITIONS) == (256, 4096)


def test_huge_input_has_typed_refusal_without_decimal_rendering():
    huge = -(1 << 20000)
    for operation in [lambda: exported.exported_binomial(huge, 3), lambda: api.binomial_exact(huge, 0),
                      lambda: api.integer_partitions(huge), lambda: api.finite_plane_parameters(huge),
                      lambda: api.weyl_heisenberg_displacement_count(huge),
                      lambda: api.enumerate_cartesian_words(2, huge, 0)]:
        with pytest.raises(api.CombinatoricsBudgetError, match="integer bit budget exceeded"):
            operation()


def test_binomial_iteration_and_result_budgets(monkeypatch):
    # The effective number of multiplicative steps is min(k,n-k).
    assert api.binomial_exact(2 * 4096, 4096) == comb(8192, 4096)
    with pytest.raises(api.CombinatoricsBudgetError, match="iteration budget"):
        api.binomial_exact(8194, 4097)
    monkeypatch.setattr(api, "MAX_BINOMIAL_BITS", 3)
    assert api.binomial_exact(6, 1) == 6
    with pytest.raises(api.CombinatoricsBudgetError, match="result bit budget"):
        api.binomial_exact(6, 3)  # 20 needs 5 bits.


def _cut_partitions(size):
    # Every composition is obtained by selecting cuts between n unit marks.
    # Sorting and deduplicating gives partitions, independently of production's
    # bounded DP and explicit DFS stack. Only n<=9 is used in this oracle.
    if size == 0:
        return {()}
    result = set()
    for count in range(size):
        for cuts in combinations(range(1, size), count):
            boundaries = (0, *cuts, size)
            parts = [right - left for left, right in zip(boundaries, boundaries[1:])]
            result.add(tuple(sorted(parts, reverse=True)))
    return result


def test_partitions_against_independent_cut_oracle():
    for size in range(10):
        actual = api.integer_partitions(size)
        assert set(actual) == _cut_partitions(size)
        assert len(actual) == len(set(actual))
        assert actual == sorted(actual, reverse=True)
        assert all(sum(row) == size for row in actual)


def test_partition_refusal_precedes_result_enumeration(monkeypatch):
    # Classical values p(28)=3718 and p(29)=4565 also follow from the
    # independent generating-function coefficient computation below.
    assert len(api.integer_partitions(28)) == 3718
    def should_not_enumerate(size):
        raise AssertionError("oversized partition request reached enumeration")
    monkeypatch.setattr(api, "_partition_rows", should_not_enumerate)
    with pytest.raises(api.CombinatoricsBudgetError, match="count exceeds policy") as caught:
        api.integer_partitions(29)
    assert caught.value.parameters["count_lower_bound"] == 4097
    with pytest.raises(api.CombinatoricsBudgetError, match="input exceeds policy"):
        api.integer_partitions(257)


def test_partition_count_finite_geometric_product():
    # Truncate prod_{k=1}^n(1+x^k+x^(2k)+...) at x^n, using
    # independent coefficient convolution rather than in-place production DP.
    for n, expected in [(28, 3718), (29, 4565)]:
        coefficients = [1] + [0] * n
        for part in range(1, n + 1):
            coefficients = [sum(coefficients[degree - multiple] for multiple in range(0, degree + 1, part))
                            for degree in range(n + 1)]
        assert coefficients[n] == expected


def test_cartesian_policy_covers_degenerate_cases_and_allocation(monkeypatch):
    assert api.enumerate_cartesian_words((1 << 1024) - 1, 0, 1) == [()]
    assert api.enumerate_cartesian_words(0, 256, 0) == []
    assert api.enumerate_cartesian_words(1, 256, 1) == [(0,) * 256]
    assert len(api.enumerate_cartesian_words(2, 12, 4096)) == 4096
    def should_not_enumerate(*args, **kwargs):
        raise AssertionError("over-budget request reached Cartesian allocation")
    monkeypatch.setattr(api, "product", should_not_enumerate)
    for alphabet, width, budget in [(2, 13, 8192), (1, 257, 1), (2, 10, 2)]:
        with pytest.raises(api.CombinatoricsBudgetError):
            api.enumerate_cartesian_words(alphabet, width, budget)
    monkeypatch.setattr(api, "MAX_WORD_CELLS", 7)
    with pytest.raises(api.CombinatoricsBudgetError, match="storage exceeds policy"):
        api.enumerate_cartesian_words(2, 3, 8)


def test_small_words_and_binomials_against_other_constructions():
    for alphabet, width in product(range(4), range(5)):
        assert api.enumerate_cartesian_words(alphabet, width, 4096) == list(product(range(alphabet), repeat=width))
    for n in range(21):
        for k in range(n + 2):
            assert api.binomial_exact(n, k) == (comb(n, k) if k <= n else 0)
    assert api.binomial_exact(-1, 0) == api.binomial_exact(0, -1) == 0


def test_plane_record_is_validated_and_cannot_be_reinitialized():
    record = api.finite_plane_parameters(3)
    assert (record.pg_points, record.pg_lines, record.ag_points, record.ag_lines) == (13, 13, 9, 12)
    with pytest.raises(FrozenInstanceError):
        record.ag_lines = 99
    with pytest.raises(api.CombinatoricsError, match="already initialized"):
        record.__init__(3, 13, 13, 4, 9, 99, 4)
    with pytest.raises(api.CombinatoricsError, match="already initialized"):
        record.__init__(2, 7, 7, 3, 4, 6, 3)
    assert record.ag_lines == 12
    with pytest.raises(api.CombinatoricsError, match="violates its polynomials"):
        api.FiniteProjectivePlaneParams(3, 13, 13, 4, 9, 99, 4)
    with pytest.raises(api.CombinatoricsError, match="violates its polynomials"):
        api.FiniteProjectivePlaneParams(2, 7, 7, 3, 4, 6, True)
    with pytest.raises(TypeError, match="does not admit subclasses"):
        type("UnsafePlane", (api.FiniteProjectivePlaneParams,), {})


def test_polynomials_are_counts_without_existence_claims():
    for q in range(2, 20):
        record = api.finite_plane_parameters(q)
        assert record.pg_points == (q ** 3 - 1) // (q - 1)
        assert record.ag_lines == q * q + q
        assert api.weyl_heisenberg_displacement_count(q) == (q * q, q * q - 1)


def test_invalid_mutants_and_loader_failures_are_not_kills():
    from src.combinatorics import test_finite_combinatorics as counting
    from src.combinatorics import test_exported_binomial as facade
    for harness, old, new in [
        (counting, "return _choose(left, right)", "return ("),
        (facade, "_require_neighbors(value)\n    return value", "_require_neighbors(value)\n    return ("),
        (counting, "from dataclasses import dataclass", "import __tfqm_missing_dependency__"),
        (facade, "from typing import Mapping", "import __tfqm_missing_dependency__"),
    ]:
        source = Path(harness._LIBRARY).read_text()
        assert source.count(old) == 1
        args = (source, ("deliberately invalid candidate", old, new), "invalid_candidate_guard")
        if harness is counting:
            args += (str(harness._LIBRARY),)
        with pytest.raises(harness.ClaimCheckError, match="not counted as a kill"):
            harness._one_mutant(*args)


def test_oracle_infrastructure_failure_is_not_silently_a_kill():
    from src.combinatorics import test_finite_combinatorics as counting
    from src.combinatorics import test_exported_binomial as facade
    for harness in [counting, facade]:
        with pytest.raises(KeyError):
            harness._safe_holds({})
        with pytest.raises(KeyError):
            harness._safe_self({})


def test_malformed_self_candidate_is_not_a_kill():
    from src.combinatorics import test_finite_combinatorics as counting
    from src.combinatorics import test_exported_binomial as facade
    for harness in [counting, facade]:
        source = Path(harness.__file__).read_text()
        args = (source, ("malformed self candidate", "def witness_primary() -> int:", "def witness_primary("), "invalid_self_candidate_guard")
        if harness is counting:
            args += (str(harness.__file__),)
        with pytest.raises(harness.ClaimCheckError, match="not counted as a kill"):
            harness._one_self(*args)


def test_checker_witnesses_have_independent_expected_values():
    from src.combinatorics import test_finite_combinatorics as counting
    from src.combinatorics import test_exported_binomial as facade
    assert (counting.witness_primary(), counting.witness_outside(), counting.witness_plane()) == (comb(6, 3), 0, 13)
    assert (facade.witness_primary(), facade.witness_outside(), facade.witness_library()) == (comb(6, 3), comb(5, 2), comb(6, 3))
    assert counting.witness_size_guard() == facade.witness_size_guard() == "float refused at the public boundary"


def test_failed_candidate_restores_existing_module_binding(monkeypatch):
    from src.combinatorics import test_finite_combinatorics as counting
    from src.combinatorics import test_exported_binomial as facade
    name = "invalid_candidate_lifecycle_guard"
    marker = types.ModuleType(name)
    monkeypatch.setitem(sys.modules, name, marker)
    for harness, old in [(counting, "return _choose(left, right)"),
                         (facade, "_require_neighbors(value)\n    return value")]:
        source = Path(harness._LIBRARY).read_text()
        args = (source, ("malformed lifecycle probe", old, "return ("), name)
        if harness is counting:
            args += (str(harness._LIBRARY),)
        with pytest.raises(harness.ClaimCheckError, match="not counted as a kill"):
            harness._one_mutant(*args)
        assert sys.modules[name] is marker
