"""Injected-fault mutants for CODA-CS-Q decision procedures.

Each mutant locally redefines one production decision. Tests assert that the
mutant disagrees with the real oracle on a known packet, so the suite kills
the fault if it is ever injected into production.

Reconstruction CSQ-03: Factors((f(0), f(1)), f(1/2)) is false; witnesses are
the zero function and t(1-t).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any, cast

import coda_cs_q_engine as engine
import pytest
from coda_cs_q_bridge_core import (
    CofinalShadowTower,
    ProfileFactorizationSolver,
    QueryProbe,
    ShadowNode,
    _validate_exact_int,
    _validate_exact_rational,
)
from sympy import Float, Rational

ZERO = Rational(0)
ONE = Rational(1)
HALF = Rational(1, 2)


def _sample(fn: Callable[[Rational], Rational]) -> dict[Rational, Rational]:
    return {ZERO: fn(ZERO), ONE: fn(ONE), HALF: fn(HALF)}


def _zero_signal() -> dict[Rational, Rational]:
    return _sample(lambda t: ZERO)


def _quadratic_signal() -> dict[Rational, Rational]:
    return _sample(lambda t: t * (ONE - t))


def _endpoint_profile(signal: dict[Rational, Rational]) -> tuple[Rational, Rational]:
    return (signal[ZERO], signal[ONE])


def _midpoint_query(signal: dict[Rational, Rational]) -> Rational:
    return signal[HALF]


def _endpoint_sum_query(signal: dict[Rational, Rational]) -> Rational:
    return signal[ZERO] + signal[ONE]


def _core_endpoint_tower() -> CofinalShadowTower:
    return CofinalShadowTower(
        [ShadowNode("t0", 1), ShadowNode("t1", 1)],
        {"t0": lambda s: s[ZERO], "t1": lambda s: s[ONE]},
        {},
    )


def _engine_endpoint_tower() -> engine.CofinalShadowTower:
    return engine.CofinalShadowTower(
        [engine.ShadowNode("t0", 1), engine.ShadowNode("t1", 1)],
        {"t0": lambda s: s[ZERO], "t1": lambda s: s[ONE]},
        {},
    )


def _parity_domain() -> list[int]:
    return [0, 1, 2, 3]


def _core_parity_tower() -> CofinalShadowTower:
    return CofinalShadowTower(
        [ShadowNode("parity", 1)],
        {"parity": lambda x: x % 2},
        {},
    )


def _engine_parity_tower() -> engine.CofinalShadowTower:
    return engine.CofinalShadowTower(
        [engine.ShadowNode("parity", 1)],
        {"parity": lambda x: x % 2},
        {},
    )


def mutant_endpoints_determine_midpoint(
    tower: Any,
    query: Any,
    domain: Sequence[Any],
) -> tuple[bool, Callable[[tuple[Any, ...]], Any], None]:
    """Treat (f(0), f(1)) as determining f(1/2), ignoring midpoint collisions."""
    claimed: dict[tuple[Any, ...], Any] = {}
    for signal in domain:
        prof = tower.evaluate_profile(signal)
        if prof not in claimed:
            claimed[prof] = query.evaluate(signal)

    def q_bar(prof: tuple[Any, ...]) -> Any:
        return claimed[prof]

    return True, q_bar, None


def mutant_skip_fiber_constancy_claim_factor(
    solver: Any,
) -> tuple[bool, Callable[[tuple[Any, ...]], Any] | None, str | None]:
    """Skip fiber-constancy and still claim a factor on the same packet."""
    success, q_bar, err = solver.solve_factorization()
    if success:
        return success, q_bar, err
    claimed: dict[tuple[Any, ...], Any] = {}
    for x in solver.domain:
        prof = solver.tower.evaluate_profile(x)
        if prof not in claimed:
            claimed[prof] = solver.query.evaluate(x)

    def claimed_bar(prof: tuple[Any, ...]) -> Any:
        return claimed[prof]

    return True, claimed_bar, None


def mutant_validate_accept_float(val: Any, name: str) -> Rational:
    """Accept IEEE 754 floats by converting them instead of refusing."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    if isinstance(val, (float, Float)):
        return Rational(val)
    if getattr(val, "dtype", None) is not None and "float" in str(val.dtype).lower():
        return Rational(val)
    return _validate_exact_rational(val, name)


def mutant_validate_int_accept_float(val: Any, name: str) -> int:
    """Accept a float degree/dimension by truncating instead of refusing."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an integer, got bool")
    if isinstance(val, float):
        return int(val)
    return _validate_exact_int(val, name)


def _real_float_rational_outcome(val: Any) -> Any:
    try:
        return _validate_exact_rational(val, "x")
    except TypeError as exc:
        if "float" in str(exc):
            return "refused_float"
        raise


def _real_float_int_outcome(val: Any) -> Any:
    try:
        return _validate_exact_int(val, "dim")
    except TypeError as exc:
        if "float" in str(exc) or "must be an integer" in str(exc):
            return "refused_float"
        raise


def test_mutant_endpoints_determine_midpoint_killed() -> None:
    # Invariant: sampling at 0 and 1 does not determine f(1/2); zero and t(1-t) collide.
    zero = _zero_signal()
    poly = _quadratic_signal()
    domain = [zero, poly]
    tower = _core_endpoint_tower()
    q_mid = QueryProbe("midpoint", 1, _midpoint_query)
    q_sum = QueryProbe("endpoint_sum", 1, _endpoint_sum_query)

    assert _endpoint_profile(zero) == _endpoint_profile(poly)
    assert _endpoint_profile(zero) == (ZERO, ZERO)
    assert _midpoint_query(zero) == ZERO
    assert _midpoint_query(poly) == Rational(1, 4)
    assert _midpoint_query(zero) != _midpoint_query(poly)

    real = ProfileFactorizationSolver(tower, q_mid, domain).solve_factorization()
    mutant = mutant_endpoints_determine_midpoint(tower, q_mid, domain)
    endpoint_key = (ZERO, ZERO)
    assert real[0] is False
    assert real[1] is None
    assert "Fiber constancy violation" in str(real[2])
    assert mutant[0] is True
    assert mutant[1] is not None
    assert mutant[1](endpoint_key) == ZERO
    assert mutant[1](endpoint_key) != _midpoint_query(poly)
    assert mutant[0] is not real[0]

    real_sum = ProfileFactorizationSolver(tower, q_sum, domain).solve_factorization()
    mutant_sum = mutant_endpoints_determine_midpoint(tower, q_sum, domain)
    assert real_sum[0] is True
    assert real_sum[1] is not None
    assert real_sum[1](endpoint_key) == ZERO
    assert mutant_sum[0] is True
    assert mutant_sum[1](endpoint_key) == ZERO

    engine_real = engine.ProfileFactorizationSolver(
        _engine_endpoint_tower(),
        engine.QueryProbe("midpoint", 1, _midpoint_query),
        domain,
    ).solve_factorization()
    assert engine_real[0] is False
    assert engine_real[1] is None
    assert "Fiber constancy violation" in str(engine_real[2])
    assert engine_real[0] == real[0]

    engine_sum = engine.ProfileFactorizationSolver(
        _engine_endpoint_tower(),
        engine.QueryProbe("endpoint_sum", 1, _endpoint_sum_query),
        domain,
    ).solve_factorization()
    assert engine_sum[0] is True
    assert engine_sum[0] == real_sum[0]


def test_mutant_skip_fiber_constancy_claim_factor_killed() -> None:
    # Invariant: a non-constant fiber does not admit a factor; skipping the check is a fault.
    domain = _parity_domain()
    tower = _core_parity_tower()
    q_id: QueryProbe[int, int] = QueryProbe("identity", 1, lambda x: x)
    q_parity: QueryProbe[int, int] = QueryProbe("parity", 1, lambda x: x % 2)

    real_id = ProfileFactorizationSolver(tower, q_id, domain)
    real = real_id.solve_factorization()
    mutant = mutant_skip_fiber_constancy_claim_factor(real_id)
    even_key = (0,)
    assert real[0] is False
    assert real[1] is None
    assert "Fiber constancy violation" in str(real[2])
    assert mutant[0] is True
    assert mutant[1] is not None
    assert mutant[1](even_key) == 0
    assert mutant[1](even_key) != q_id.evaluate(2)
    assert mutant[0] is not real[0]

    real_ok = ProfileFactorizationSolver(tower, q_parity, domain)
    real_parity = real_ok.solve_factorization()
    mutant_parity = mutant_skip_fiber_constancy_claim_factor(real_ok)
    assert real_parity[0] is True
    assert real_parity[1] is not None
    assert real_parity[1](even_key) == 0
    assert mutant_parity[0] is True
    assert mutant_parity[1] is not None
    assert mutant_parity[1](even_key) == 0

    engine_solver: engine.ProfileFactorizationSolver[int, int] = engine.ProfileFactorizationSolver(
        _engine_parity_tower(),
        engine.QueryProbe("identity", 1, lambda x: x),
        domain,
    )
    engine_real = engine_solver.solve_factorization()
    engine_mutant = mutant_skip_fiber_constancy_claim_factor(engine_solver)
    assert engine_real[0] is False
    assert engine_mutant[0] is True
    assert engine_mutant[1] is not None
    assert engine_mutant[1](even_key) == 0
    assert engine_mutant[0] is not engine_real[0]


def test_mutant_accept_float_killed() -> None:
    # Invariant: floats are refused; a mutant that converts them disagrees.
    with pytest.raises(TypeError, match="got float"):
        _validate_exact_rational(0.5, "x")
    with pytest.raises(TypeError, match="must be an integer"):
        _validate_exact_int(2.0, "dim")

    real_half = _real_float_rational_outcome(0.5)
    mutant_half = mutant_validate_accept_float(0.5, "x")
    assert real_half == "refused_float"
    assert mutant_half == Rational(1, 2)
    assert mutant_half != real_half

    real_sympy = _real_float_rational_outcome(Float(0.5))
    mutant_sympy = mutant_validate_accept_float(Float(0.5), "x")
    assert real_sympy == "refused_float"
    assert mutant_sympy == Rational(1, 2)
    assert mutant_sympy != real_sympy

    real_dim = _real_float_int_outcome(2.0)
    mutant_dim = mutant_validate_int_accept_float(2.0, "dim")
    assert real_dim == "refused_float"
    assert mutant_dim == 2
    assert mutant_dim != real_dim

    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(False, "x")
    with pytest.raises(TypeError, match="got bool"):
        mutant_validate_accept_float(False, "x")
    with pytest.raises(TypeError, match="got bool"):
        mutant_validate_int_accept_float(True, "dim")

    real_int = _validate_exact_rational(2, "x")
    mutant_int = mutant_validate_accept_float(2, "x")
    assert real_int == Rational(2, 1)
    assert mutant_int == real_int
    assert mutant_validate_int_accept_float(3, "dim") == _validate_exact_int(3, "dim")

    with pytest.raises(TypeError):
        ShadowNode("N_Bad", cast(int, 2.5))
    with pytest.raises(TypeError):
        QueryProbe("Q_Bad", cast(int, 1.5), lambda x: 1)
