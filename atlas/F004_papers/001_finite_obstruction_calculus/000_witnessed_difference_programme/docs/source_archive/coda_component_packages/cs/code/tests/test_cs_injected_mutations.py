"""Injected-fault mutants for CODA-CS decision procedures.

Each mutant locally redefines one production decision. Tests assert that the
mutant disagrees with the real oracle on a known packet, so the suite kills
the fault if it is ever injected into production.

Reconstruction CS-03: Factors(fst, snd) is false on Bool×Bool.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Optional, Sequence

import pytest
from coda_cs_core import (
    R_NOT_FIBER_CONSTANT,
    R_SHADOW_COHERENCE_FAILURE,
    RESIDUAL_SUCCESS,
    BridgeAdmissibilityReport,
    ContinuumQuery,
    ContinuumSignal,
    ProfileMap,
    ShadowSlice,
    ShadowTower,
    _validate_exact_rational,
    compute_transition_quotient_obstruction,
    verify_bridge_admissibility,
)
from sympy import Float, Matrix, Rational


def _bool_pair_signals() -> tuple[ContinuumSignal, ...]:
    return tuple(
        ContinuumSignal(
            signal_id=f"({a},{b})",
            samples={Rational(0, 1): Rational(a), Rational(1, 1): Rational(b)},
        )
        for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))
    )


def _snd_query() -> ContinuumQuery:
    return ContinuumQuery(
        query_id="snd",
        degree_bound=1,
        evaluator=lambda s: s.evaluate_at(Rational(1, 1)),
    )


def _fst_query() -> ContinuumQuery:
    return ContinuumQuery(
        query_id="fst",
        degree_bound=1,
        evaluator=lambda s: s.evaluate_at(Rational(0, 1)),
    )


def _fst_profile() -> ProfileMap:
    return ProfileMap(profile_id="fst", sample_points=(Rational(0, 1),))


def _pair_tower() -> ShadowTower:
    return ShadowTower(
        tower_id="BoolxBool",
        slices=(ShadowSlice("pair", 2, True),),
        is_cofinal=True,
    )


def mutant_coarse_observation_enough(
    query: ContinuumQuery,
    tower: ShadowTower,
    profile: ProfileMap,
    test_signals: Sequence[ContinuumSignal],
) -> dict[tuple[Any, ...], Rational]:
    """Treat a defined coarse profile as enough, ignoring query variation on fibers."""
    claimed_factor: dict[tuple[Any, ...], Rational] = {}
    if not (tower.is_cofinal and tower.all_slices_authorized()):
        return claimed_factor
    for sig in test_signals:
        prof_vec = profile.project(sig)
        key = tuple(prof_vec[i, 0] for i in range(prof_vec.rows))
        q_val = _validate_exact_rational(query.evaluator(sig), f"query({sig.signal_id})")
        if key not in claimed_factor:
            claimed_factor[key] = q_val
    return claimed_factor


def mutant_skip_fiber_constancy_claim_factor(
    query: ContinuumQuery,
    tower: ShadowTower,
    profile: ProfileMap,
    test_signals: Sequence[ContinuumSignal],
    factored_evaluator: Optional[Any] = None,
    has_terminalizer: bool = True,
    max_degree: int = 4,
    d0_transition: Optional[Any] = None,
    defect_1cochain: Optional[Any] = None,
) -> BridgeAdmissibilityReport:
    """Skip fiber-constancy and still claim a factor on the same packet."""
    report = verify_bridge_admissibility(
        query=query,
        tower=tower,
        profile=profile,
        test_signals=test_signals,
        factored_evaluator=factored_evaluator,
        has_terminalizer=has_terminalizer,
        max_degree=max_degree,
        d0_transition=d0_transition,
        defect_1cochain=defect_1cochain,
    )
    if report.refusal_code == R_NOT_FIBER_CONSTANT:
        return replace(
            report,
            is_fiber_constant=True,
            is_factorable=True,
            overall_admissible=True,
            refusal_code=None,
            residual_mass=RESIDUAL_SUCCESS,
        )
    return report


def mutant_validate_accept_float(val: Any, name: str) -> Rational:
    """Accept IEEE 754 floats by converting them instead of refusing."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    if isinstance(val, (float, Float)):
        return Rational(val)
    if getattr(val, "dtype", None) is not None and "float" in str(val.dtype).lower():
        return Rational(val)
    return _validate_exact_rational(val, name)


def _real_float_outcome(val: Any) -> Any:
    try:
        return _validate_exact_rational(val, "x")
    except TypeError as exc:
        if "float" in str(exc):
            return "refused_float"
        raise


def test_mutant_coarse_observation_enough_killed_on_cs03() -> None:
    # Invariant: a first-coordinate shadow does not determine a second-coordinate query.
    signals = _bool_pair_signals()
    query = _snd_query()
    tower = _pair_tower()
    profile = _fst_profile()
    real = verify_bridge_admissibility(
        query=query,
        tower=tower,
        profile=profile,
        test_signals=signals,
    )
    claimed = mutant_coarse_observation_enough(query, tower, profile, signals)
    coarse_false = (Rational(0, 1),)
    mutant_admits = coarse_false in claimed

    assert signals[0].evaluate_at(Rational(0, 1)) == signals[1].evaluate_at(Rational(0, 1))
    assert signals[0].evaluate_at(Rational(1, 1)) != signals[1].evaluate_at(Rational(1, 1))
    assert real.is_fiber_constant is False
    assert real.overall_admissible is False
    assert real.refusal_code == R_NOT_FIBER_CONSTANT
    assert mutant_admits is True
    assert claimed[coarse_false] != query.evaluator(signals[1])
    assert mutant_admits is not real.overall_admissible

    q_fst = _fst_query()
    real_fst = verify_bridge_admissibility(
        query=q_fst,
        tower=tower,
        profile=profile,
        test_signals=signals,
        factored_evaluator=lambda vec: Rational(vec[0, 0]),
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    claimed_fst = mutant_coarse_observation_enough(q_fst, tower, profile, signals)
    assert real_fst.overall_admissible is True
    assert claimed_fst[coarse_false] == q_fst.evaluator(signals[0])
    assert claimed_fst[coarse_false] == q_fst.evaluator(signals[1])


def test_mutant_skip_fiber_constancy_killed_on_cs03() -> None:
    # Invariant: skipping fiber-constancy and claiming a factor is a fault on CS-03.
    signals = _bool_pair_signals()
    query = _snd_query()
    tower = _pair_tower()
    profile = _fst_profile()
    real = verify_bridge_admissibility(
        query=query,
        tower=tower,
        profile=profile,
        test_signals=signals,
    )
    mutant = mutant_skip_fiber_constancy_claim_factor(query, tower, profile, signals)
    assert real.overall_admissible is False
    assert real.is_fiber_constant is False
    assert real.refusal_code == R_NOT_FIBER_CONSTANT
    assert mutant.overall_admissible is True
    assert mutant.is_fiber_constant is True
    assert mutant.is_factorable is True
    assert mutant.refusal_code is None
    assert mutant.overall_admissible is not real.overall_admissible

    real_fst = verify_bridge_admissibility(
        query=_fst_query(),
        tower=tower,
        profile=profile,
        test_signals=signals,
        factored_evaluator=lambda vec: Rational(vec[0, 0]),
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    mutant_fst = mutant_skip_fiber_constancy_claim_factor(
        _fst_query(),
        tower,
        profile,
        signals,
        factored_evaluator=lambda vec: Rational(vec[0, 0]),
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert real_fst.overall_admissible is True
    assert mutant_fst.overall_admissible is True
    assert mutant_fst.overall_admissible == real_fst.overall_admissible


def test_mutant_accept_float_killed() -> None:
    # Invariant: floats are refused; a mutant that converts them disagrees.
    with pytest.raises(TypeError, match="got float"):
        _validate_exact_rational(0.5, "x")

    real_half = _real_float_outcome(0.5)
    mutant_half = mutant_validate_accept_float(0.5, "x")
    assert real_half == "refused_float"
    assert mutant_half == Rational(1, 2)
    assert mutant_half != real_half

    real_sympy = _real_float_outcome(Float(0.5))
    mutant_sympy = mutant_validate_accept_float(Float(0.5), "x")
    assert real_sympy == "refused_float"
    assert mutant_sympy == Rational(1, 2)
    assert mutant_sympy != real_sympy

    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(False, "x")
    with pytest.raises(TypeError, match="got bool"):
        mutant_validate_accept_float(False, "x")

    real_int = _validate_exact_rational(2, "x")
    mutant_int = mutant_validate_accept_float(2, "x")
    assert real_int == Rational(2, 1)
    assert mutant_int == real_int


def mutant_skip_transition_solver_claim_coherent(
    query: ContinuumQuery,
    tower: ShadowTower,
    profile: ProfileMap,
    test_signals: Sequence[ContinuumSignal],
    factored_evaluator: Optional[Any] = None,
    d0_transition: Optional[Any] = None,
    defect_1cochain: Optional[Any] = None,
) -> BridgeAdmissibilityReport:
    """Skip the cochain solver and still mark transition coherence true."""
    report = verify_bridge_admissibility(
        query=query,
        tower=tower,
        profile=profile,
        test_signals=test_signals,
        factored_evaluator=factored_evaluator,
        d0_transition=d0_transition,
        defect_1cochain=defect_1cochain,
    )
    if report.refusal_code == R_SHADOW_COHERENCE_FAILURE:
        return replace(
            report,
            is_transition_coherent=True,
            overall_admissible=True,
            refusal_code=None,
            residual_mass=RESIDUAL_SUCCESS,
        )
    return report


def test_mutant_skip_transition_solver_killed() -> None:
    # Invariant: a leftover transition is not coherent; skipping the solver is a fault.
    pts = (Rational(0, 1), Rational(1, 1))
    prof = ProfileMap(profile_id="Grid_2", sample_points=pts)
    sig = ContinuumSignal("S", {p: p for p in pts})
    q = ContinuumQuery(query_id="Q", degree_bound=1, evaluator=lambda s: Rational(1, 1))
    tower = ShadowTower("T", (ShadowSlice("S1", 2, True),), True)
    def factored(v):
        return Rational(1, 1)
    d0 = Matrix([[1], [2]])
    leftover = Matrix([[1], [0]])
    dist, _w, is_exact = compute_transition_quotient_obstruction(d0, leftover)
    assert is_exact is False
    assert dist > Rational(0, 1)

    real = verify_bridge_admissibility(
        query=q,
        tower=tower,
        profile=prof,
        test_signals=[sig],
        factored_evaluator=factored,
        d0_transition=d0,
        defect_1cochain=leftover,
    )
    mutant = mutant_skip_transition_solver_claim_coherent(
        q, tower, prof, [sig], factored, d0, leftover
    )
    assert real.is_transition_coherent is False
    assert real.overall_admissible is False
    assert real.refusal_code == R_SHADOW_COHERENCE_FAILURE
    assert mutant.is_transition_coherent is True
    assert mutant.overall_admissible is True
    assert mutant.overall_admissible is not real.overall_admissible
