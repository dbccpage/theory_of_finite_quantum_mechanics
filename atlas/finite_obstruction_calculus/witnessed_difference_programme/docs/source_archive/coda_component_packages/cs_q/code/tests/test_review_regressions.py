"""Finite-domain integrity regressions from the F005 publication review."""

from __future__ import annotations

from collections.abc import Callable
from typing import cast

import pytest
from coda_cs_q_bridge_core import (
    BridgePacketCore,
    CofinalShadowTower,
    ImagePoint,
    ProfileFactorizationSolver,
    ProfileFiberQuotient,
    QueryProbe,
    ShadowNode,
)


def test_mutated_states_cannot_reuse_old_fibres() -> None:
    states = [[0, 0], [1, 1]]
    tower = CofinalShadowTower([ShadowNode("p", 1)], {"p": lambda x: x[0]}, {})
    query: QueryProbe[list[int], int] = QueryProbe("second", 1, lambda x: x[1])
    solver = ProfileFactorizationSolver(tower, query, states)
    states[1][0] = 0
    success, factor, error = solver.solve_factorization()
    assert not success and factor is None
    assert error is not None
    assert "Fiber constancy violation" in error


def test_changed_projector_is_checked_when_solving() -> None:
    tower = CofinalShadowTower([ShadowNode("p", 1)], {"p": lambda x: x}, {})
    solver: ProfileFactorizationSolver[int, int] = ProfileFactorizationSolver(
        tower, QueryProbe("id", 1, lambda x: x), [0, 1]
    )
    tower.projectors["p"] = lambda x: 0
    assert solver.solve_factorization()[0] is False


def test_factor_uses_one_observation_per_state_and_detaches_values() -> None:
    calls = {"profile": 0, "query": 0}
    values = {0: [10], 1: [20]}

    def profile(x: int) -> int:
        calls["profile"] += 1
        return x

    def query(x: int) -> list[int]:
        calls["query"] += 1
        return values[x]

    tower = CofinalShadowTower([ShadowNode("p", 1)], {"p": profile}, {})
    solver = ProfileFactorizationSolver(tower, QueryProbe("list", 1, query), [0, 1])
    assert calls == {"profile": 0, "query": 0}
    success, factor, error = solver.solve_factorization()
    assert success and factor is not None and error is None
    assert calls == {"profile": 2, "query": 2}
    values[0].append(99)
    observed = factor((0,))
    observed.append(100)
    assert factor((0,)) == [10]
    with pytest.raises(KeyError, match="outside the realized domain"):
        factor((2,))


def test_stateful_query_is_not_reread_after_constancy_check() -> None:
    answers = iter([7, 7, 8, 9])
    tower = CofinalShadowTower([ShadowNode("p", 1)], {"p": lambda x: 0}, {})
    solver = ProfileFactorizationSolver(tower, QueryProbe("observed", 1, lambda x: next(answers)), [1, 2])
    success, factor, _ = solver.solve_factorization()
    assert success and factor is not None
    assert factor((0,)) == 7
    assert next(answers) == 8


def test_fibre_helpers_refresh_after_domain_mutation() -> None:
    states = [[0, 0], [1, 1]]
    tower = CofinalShadowTower([ShadowNode("p", 1)], {"p": lambda x: x[0]}, {})
    quotient = ProfileFiberQuotient(tower, states)
    assert quotient.num_fibers() == 2
    states[1][0] = 0
    assert quotient.num_fibers() == 1
    assert len(quotient.get_fiber_of(states[0])) == 2
    assert quotient.get_fiber_of([99, 0]) == []
    assert QueryProbe("second", 1, lambda x: x[1]).check_fiber_constancy(quotient)[0] is False


@pytest.mark.parametrize("field,step", [
    ("completion_witness", "3_completion_realization"),
    ("q_held_paid", "4_q_admission"),
    ("route_independent", "6_route_independence"),
    ("reflection_descends", "7_reflection_descent"),
])
def test_each_admission_flag_requires_an_actual_boolean(field: str, step: str) -> None:
    tower = CofinalShadowTower([ShadowNode("p", 1)], {"p": lambda x: x}, {})
    query: QueryProbe[int, int] = QueryProbe("zero", 1, lambda x: 0)
    for invalid in ["False", 1, None, object()]:
        with pytest.raises(TypeError, match=field):
            # Dynamic call deliberately probes an invalid constructor argument.
            cast(Callable[..., object], BridgePacketCore)("bad", tower, [0], query, **{field: invalid})
    packet = BridgePacketCore("valid", tower, [0], query)
    assert packet.audit_8_step_admission()["is_admissible"] is True
    setattr(packet, field, False)
    audit = packet.audit_8_step_admission()
    assert audit["steps"][step] is False
    assert audit["is_admissible"] is False
    setattr(packet, field, "False")
    with pytest.raises(TypeError, match=field):
        packet.audit_8_step_admission()


def test_image_point_requires_a_bound_profile() -> None:
    with pytest.raises(TypeError):
        cast(Callable[..., object], ImagePoint)(val=(999,), witness=5)
    with pytest.raises(TypeError, match="callable profile_fn"):
        ImagePoint(val=(5,), witness=5, profile_fn=cast(Callable[[int], tuple[int]], None))
    with pytest.raises(ValueError, match="witness mismatch"):
        ImagePoint(val=(999,), witness=5, profile_fn=lambda x: (x,))


def test_image_witness_is_copied_and_revalidated_before_factor_use() -> None:
    state = [2]
    tower = CofinalShadowTower([ShadowNode("p", 1)], {"p": lambda x: x[0]}, {})
    query: QueryProbe[list[int], int] = QueryProbe("double", 1, lambda x: 2 * x[0])
    point = ImagePoint.from_tower(tower, state)
    success, factor, _ = ProfileFactorizationSolver(tower, query, [state]).solve_factorization()
    assert success and factor is not None
    state[0] = 99
    assert point.witness == [2]
    assert point.evaluate_factored(query, factor) == 4
    with pytest.raises(TypeError):
        cast(Callable[..., object], point.evaluate_factored)(query)
    with pytest.raises(ValueError, match="disagrees with the query"):
        point.evaluate_factored(query, lambda prof: 100)
    point.witness[0] = 3
    with pytest.raises(ValueError, match="witness mismatch"):
        point.evaluate_factored(query, factor)


def test_image_point_rejects_a_changed_profile_map() -> None:
    tower = CofinalShadowTower([ShadowNode("p", 1)], {"p": lambda x: x}, {})
    point = ImagePoint.from_tower(tower, 2)
    tower.projectors["p"] = lambda x: x + 1
    with pytest.raises(ValueError, match="witness mismatch"):
        point.evaluate_factored(QueryProbe("id", 1, lambda x: x), lambda prof: prof[0])


def test_remaining_input_and_diagnostic_boundaries() -> None:
    from coda_cs_q_bridge_core import BridgeResidualTaxonomy, _validate_exact_int, terminals_agree
    with pytest.raises(TypeError):
        _validate_exact_int("1", "dimension")
    with pytest.raises(ValueError, match="non-empty string"):
        ShadowNode("", 0)
    with pytest.raises(ValueError, match="Transition source"):
        CofinalShadowTower([ShadowNode("p", 1)], {"p": lambda x: x}, {("absent", "p"): lambda x: x})
    assert terminals_agree([], lambda x: x, lambda x: x)[0] is False
    residuals = BridgeResidualTaxonomy.classify_residual(False, False, False, "authority", False, False, False)
    assert len(residuals) == 7
    assert BridgeResidualTaxonomy.classify_residual(True, True, True, "None") == []
