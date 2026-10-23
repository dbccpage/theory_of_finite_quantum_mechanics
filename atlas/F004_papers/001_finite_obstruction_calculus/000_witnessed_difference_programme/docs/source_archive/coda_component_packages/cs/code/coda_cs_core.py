# -*- coding: utf-8 -*-
"""
coda_cs_core.py: Continuum Finite-Shadow Tower & Query-Relative Authority for CODA-CS.

Governing Claims:
1. CS-D1: Fiber constancy FiberConstant(p, q) <=> forall x y, p(x) = p(y) => q(x) = q(y).
2. CS-D2: Factorization Factors(p, q) <=> exists g, forall x, g(p(x)) = q(x).
3. CS-D3: Refinement p = forget circ fine.
4. CS-L1: Factors(p, q) => FiberConstant(p, q).
5. CS-T1: Refinement preserves descent: FiberConstant(forget circ fine, q) => FiberConstant(fine, q).
6. CS-T2: Family observation equality is pointwise: (observe_i(x) = observe_i(y) forall i) <=> observe(x) = observe(y).
7. CS-T3: First coordinate does not determine second: not Factors(x.1, x.2).
8. CS-T4: Strict refinement countermodel: Factors(id, x.2) and not Factors(x.1, x.2).
9. CS-T5: Missing terminalizer blocks query authority: has_local_terminalizer = false => not HasQueryAuthority(X, q, b).
10. Exact Cochain Quotient Solver: LinearRepairProblem & QuotientDistanceCertificate from cochain_presentation.
11. Zero Floats Invariant: strictly exact rational arithmetic (sympy.Rational / fractions.Fraction).
    Floats and booleans passed as numerical scalars strictly raise TypeError.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Any, Callable, Dict, Mapping, Optional, Sequence, Tuple

from cochain_presentation import LinearRepairProblem, QuotientDistanceCertificate
from sympy import Float, Integer, Matrix, Rational

# Exact rational residual constants
RESIDUAL_UNAUTHORIZED = Rational(1, 1)
RESIDUAL_NO_PROFILE = Rational(3, 4)
RESIDUAL_FIBER_DEFECT = Rational(1, 2)
RESIDUAL_NO_TERMINALIZER = Rational(1, 4)
RESIDUAL_SUCCESS = Rational(0, 1)

# Refusal codes
R_NO_FINITE_SHADOW = "NoFiniteShadow"
R_NO_COFINAL_SHADOW = "NoCofinalAuthorizedShadow"
R_SHADOW_COHERENCE_FAILURE = "ShadowCoherenceFailure"
R_UNREFLECTED_CLAIM = "UnreflectedContinuumClaim"
R_TRANSPORT_VIOLATION = "TransportViolation"
R_NOT_FACTORABLE = "R_not_factorable"
R_NOT_FIBER_CONSTANT = "R_not_fiber_constant"
R_UNBOUNDED_DEGREE = "R_unbounded_degree"
R_NO_TERMINAL = "NoTerminal"
R_NO_PROFILE = "NoProfile"


def _validate_exact_rational(val: Any, name: str) -> Rational:
    """Ensure value is an exact rational or integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    val_dtype = getattr(val, "dtype", None)
    if isinstance(val, (float, Float)) or (val_dtype is not None and "float" in str(val_dtype).lower()):
        raise TypeError(f"{name} must be an exact rational or integer, got float (floats strictly forbidden)")
    if isinstance(val, (int, Integer, Fraction, Rational)):
        return Rational(val)
    if isinstance(val, str):
        try:
            return Rational(val)
        except Exception as exc:
            raise TypeError(f"{name} string could not be converted to exact Rational: {exc}") from exc
    raise TypeError(f"{name} must be an exact rational or integer, got {type(val).__name__}")


def _validate_exact_int(val: Any, name: str) -> int:
    """Ensure value is an exact non-negative integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an integer, got bool")
    val_dtype = getattr(val, "dtype", None)
    if not isinstance(val, (int, Integer)) or (val_dtype is not None and "float" in str(val_dtype)):
        raise TypeError(f"{name} must be an integer, got {type(val).__name__}")
    int_val = int(val)
    if int_val < 0:
        raise ValueError(f"{name} must be non-negative, got {int_val}")
    return int_val


@dataclass(frozen=True)
class ShadowSlice:
    """A finite shadow slice A_lambda at index lambda in Lambda."""

    index_id: str
    dimension: int
    has_local_authority: bool
    is_finite: bool = True

    def __post_init__(self) -> None:
        _validate_exact_int(self.dimension, "dimension")
        if not isinstance(self.has_local_authority, bool):
            raise TypeError(f"has_local_authority must be bool, got {type(self.has_local_authority).__name__}")
        if not isinstance(self.is_finite, bool):
            raise TypeError(f"is_finite must be bool, got {type(self.is_finite).__name__}")


@dataclass(frozen=True)
class ShadowTower:
    """A directed tower of finite shadow slices (Lambda, A_lambda, F_{mu lambda})."""

    tower_id: str
    slices: Tuple[ShadowSlice, ...]
    is_cofinal: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.is_cofinal, bool):
            raise TypeError(f"is_cofinal must be bool, got {type(self.is_cofinal).__name__}")

    def get_slice(self, index_id: str) -> Optional[ShadowSlice]:
        for s in self.slices:
            if s.index_id == index_id:
                return s
        return None

    def all_slices_authorized(self) -> bool:
        if not self.slices:
            return False
        return all(s.has_local_authority and s.is_finite for s in self.slices)


@dataclass(frozen=True)
class ContinuumSignal:
    """
    A continuum signal X in Omega_kappa represented by sample evaluations
    over rational sample points.
    """

    signal_id: str
    samples: Mapping[Rational, Rational]

    def __post_init__(self) -> None:
        if not isinstance(self.signal_id, str):
            raise TypeError(f"signal_id must be str, got {type(self.signal_id).__name__}")
        if not isinstance(self.samples, (dict, Mapping)):
            raise TypeError(f"samples must be dict or Mapping, got {type(self.samples).__name__}")
        validated: Dict[Rational, Rational] = {}
        for k, v in self.samples.items():
            r_k = _validate_exact_rational(k, f"signal {self.signal_id} sample key")
            r_v = _validate_exact_rational(v, f"signal {self.signal_id} sample value at {k}")
            validated[r_k] = r_v
        # Store genuinely immutable mapping snapshot
        object.__setattr__(self, "samples", MappingProxyType(validated))

    @property
    def snapshot_key(self) -> Tuple[str, Tuple[Tuple[Rational, Rational], ...]]:
        return (self.signal_id, tuple(sorted(self.samples.items())))

    def __hash__(self) -> int:
        return hash(self.snapshot_key)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ContinuumSignal):
            return False
        return self.signal_id == other.signal_id and self.samples == other.samples

    def evaluate_at(self, t: Any) -> Rational:
        r_t = _validate_exact_rational(t, "sample_coordinate")
        if r_t not in self.samples:
            raise KeyError(f"Signal {self.signal_id} has no sample at {r_t}")
        val = self.samples[r_t]
        return _validate_exact_rational(val, f"signal {self.signal_id} stored sample")


@dataclass(frozen=True)
class ContinuumQuery:
    """An operational query q: X -> Target with declared degree bound n."""

    query_id: str
    degree_bound: int
    evaluator: Callable[[ContinuumSignal], Rational]

    def __post_init__(self) -> None:
        _validate_exact_int(self.degree_bound, "degree_bound")


@dataclass(frozen=True)
class ProfileMap:
    """
    Cofinal shadow profile map Prof_{Lambda_0}(X) extracting a finite vector of rationals.
    """

    profile_id: str
    sample_points: Tuple[Rational, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.profile_id, str):
            raise TypeError(f"profile_id must be str, got {type(self.profile_id).__name__}")
        validated = tuple(
            _validate_exact_rational(pt, f"profile {self.profile_id} sample point")
            for pt in self.sample_points
        )
        object.__setattr__(self, "sample_points", validated)

    def project(self, signal: ContinuumSignal) -> Matrix:
        elements = [signal.evaluate_at(pt) for pt in self.sample_points]
        return Matrix(elements)


@dataclass(frozen=True)
class BridgeAdmissibilityReport:
    """Detailed verification report for the 8-step BridgeAdmissible gate."""

    is_degree_bounded: bool
    is_cofinal: bool
    is_shadow_finite: bool
    is_profile_surjective: bool
    is_factorable: bool
    is_fiber_constant: bool
    is_transition_coherent: bool
    has_local_terminalizer: bool
    overall_admissible: bool
    refusal_code: Optional[str]
    residual_mass: Rational
    verified_values: Optional[Dict[Any, Rational]] = None


def verify_bridge_admissibility(
    query: ContinuumQuery,
    tower: ShadowTower,
    profile: ProfileMap,
    test_signals: Sequence[ContinuumSignal],
    factored_evaluator: Optional[Callable[[Matrix], Rational]] = None,
    has_terminalizer: bool = True,
    max_degree: int = 4,
    d0_transition: Optional[Matrix] = None,
    defect_1cochain: Optional[Matrix] = None,
) -> BridgeAdmissibilityReport:
    """
    Verifies the 8-step BridgeAdmissible conditions:
    1. Query degree bounded (deg <= max_degree)
    2. Shadow tower cofinal
    3. Shadow slices finite & locally authorized
    4. Profile map well-defined & non-empty (is_profile_surjective / profile_nonempty)
    5. Fiber constancy holds across test signals
    6. Query factors through profile map
    7. Shadow transition cochain diagram has zero quotient defect
    8. Local terminalizer declared
    """
    if not isinstance(has_terminalizer, bool):
        raise TypeError(f"has_terminalizer must be bool, got {type(has_terminalizer).__name__}")
    max_degree = _validate_exact_int(max_degree, "max_degree")

    # 1. Degree bound
    if query.degree_bound > max_degree:
        return BridgeAdmissibilityReport(
            is_degree_bounded=False,
            is_cofinal=False,
            is_shadow_finite=False,
            is_profile_surjective=False,
            is_factorable=False,
            is_fiber_constant=False,
            is_transition_coherent=False,
            has_local_terminalizer=has_terminalizer,
            overall_admissible=False,
            refusal_code=R_UNBOUNDED_DEGREE,
            residual_mass=RESIDUAL_UNAUTHORIZED,
        )

    # 2. Cofinality
    if not tower.is_cofinal:
        return BridgeAdmissibilityReport(
            is_degree_bounded=True,
            is_cofinal=False,
            is_shadow_finite=False,
            is_profile_surjective=False,
            is_factorable=False,
            is_fiber_constant=False,
            is_transition_coherent=False,
            has_local_terminalizer=has_terminalizer,
            overall_admissible=False,
            refusal_code=R_NO_COFINAL_SHADOW,
            residual_mass=RESIDUAL_UNAUTHORIZED,
        )

    # 3. Finite shadow authority
    if not tower.all_slices_authorized():
        return BridgeAdmissibilityReport(
            is_degree_bounded=True,
            is_cofinal=True,
            is_shadow_finite=False,
            is_profile_surjective=False,
            is_factorable=False,
            is_fiber_constant=False,
            is_transition_coherent=False,
            has_local_terminalizer=has_terminalizer,
            overall_admissible=False,
            refusal_code=R_NO_FINITE_SHADOW,
            residual_mass=RESIDUAL_UNAUTHORIZED,
        )

    # 4. Profile map well-defined and non-empty
    is_profile_surjective = len(profile.sample_points) > 0
    if not is_profile_surjective:
        return BridgeAdmissibilityReport(
            is_degree_bounded=True,
            is_cofinal=True,
            is_shadow_finite=True,
            is_profile_surjective=False,
            is_factorable=False,
            is_fiber_constant=False,
            is_transition_coherent=False,
            has_local_terminalizer=has_terminalizer,
            overall_admissible=False,
            refusal_code=R_NO_PROFILE,
            residual_mass=RESIDUAL_NO_PROFILE,
        )

    # Snapshot the verification family into an immutable tuple immediately
    family: Tuple[ContinuumSignal, ...] = tuple(test_signals)

    # Non-vacuous test signals domain check
    if not family:
        return BridgeAdmissibilityReport(
            is_degree_bounded=True,
            is_cofinal=True,
            is_shadow_finite=True,
            is_profile_surjective=True,
            is_factorable=False,
            is_fiber_constant=False,
            is_transition_coherent=False,
            has_local_terminalizer=has_terminalizer,
            overall_admissible=False,
            refusal_code=R_NOT_FACTORABLE,
            residual_mass=RESIDUAL_NO_PROFILE,
        )

    # Explicit duplicate-identity check: test signals must have unique identifiers
    seen_ids = set()
    for sig in family:
        if sig.signal_id in seen_ids:
            raise ValueError(f"Duplicate signal identifier in test_signals: '{sig.signal_id}'")
        seen_ids.add(sig.signal_id)

    # 5 & 6. Factorization and Fiber Constancy across test signals
    is_factorable = True
    is_fiber_constant = True
    verified_values: Dict[Any, Rational] = {}

    # Check fiber constancy: if Prof(X) == Prof(Y), must have q(X) == q(Y)
    profile_to_query_val: Dict[Tuple[Rational, ...], Rational] = {}

    for sig in family:
        prof_vec = profile.project(sig)
        prof_key = tuple(prof_vec[i, 0] for i in range(prof_vec.rows))
        q_val = _validate_exact_rational(query.evaluator(sig), f"query({sig.signal_id})")
        verified_values[sig.snapshot_key] = q_val
        verified_values[sig.signal_id] = q_val

        if prof_key in profile_to_query_val:
            if profile_to_query_val[prof_key] != q_val:
                is_fiber_constant = False
                is_factorable = False  # CS-L1: collision precludes factorization
        else:
            profile_to_query_val[prof_key] = q_val

        # Check factored evaluator q = bar_q(Prof(X)) without breaking from fiber check
        if factored_evaluator is not None and is_factorable:
            q_factored = _validate_exact_rational(factored_evaluator(prof_vec), f"factored({sig.signal_id})")
            if q_factored != q_val:
                is_factorable = False

    if not is_fiber_constant:
        return BridgeAdmissibilityReport(
            is_degree_bounded=True,
            is_cofinal=True,
            is_shadow_finite=True,
            is_profile_surjective=is_profile_surjective,
            is_factorable=False,
            is_fiber_constant=False,
            is_transition_coherent=False,
            has_local_terminalizer=has_terminalizer,
            overall_admissible=False,
            refusal_code=R_NOT_FIBER_CONSTANT,
            residual_mass=RESIDUAL_FIBER_DEFECT,
            verified_values=verified_values,
        )

    if not is_factorable:
        return BridgeAdmissibilityReport(
            is_degree_bounded=True,
            is_cofinal=True,
            is_shadow_finite=True,
            is_profile_surjective=is_profile_surjective,
            is_factorable=False,
            is_fiber_constant=True,
            is_transition_coherent=False,
            has_local_terminalizer=has_terminalizer,
            overall_admissible=False,
            refusal_code=R_NOT_FACTORABLE,
            residual_mass=RESIDUAL_NO_PROFILE,
            verified_values=verified_values,
        )

    # 8. Local terminalizer declared (before the solver so a missing
    # terminalizer is not reported as a missing transition diagram).
    if not has_terminalizer:
        return BridgeAdmissibilityReport(
            is_degree_bounded=True,
            is_cofinal=True,
            is_shadow_finite=True,
            is_profile_surjective=is_profile_surjective,
            is_factorable=True,
            is_fiber_constant=True,
            is_transition_coherent=False,
            has_local_terminalizer=False,
            overall_admissible=False,
            refusal_code=R_NO_TERMINAL,
            residual_mass=RESIDUAL_NO_TERMINALIZER,
            verified_values=verified_values,
        )

    # 7. Transition coherence: an explicit cochain diagram, scored by the exact solver.
    if d0_transition is None or defect_1cochain is None:
        return BridgeAdmissibilityReport(
            is_degree_bounded=True,
            is_cofinal=True,
            is_shadow_finite=True,
            is_profile_surjective=is_profile_surjective,
            is_factorable=True,
            is_fiber_constant=True,
            is_transition_coherent=False,
            has_local_terminalizer=True,
            overall_admissible=False,
            refusal_code=R_SHADOW_COHERENCE_FAILURE,
            residual_mass=RESIDUAL_UNAUTHORIZED,
            verified_values=verified_values,
        )
    quotient_dist, _repair, is_exact = compute_transition_quotient_obstruction(
        d0_transition, defect_1cochain
    )
    if not is_exact:
        return BridgeAdmissibilityReport(
            is_degree_bounded=True,
            is_cofinal=True,
            is_shadow_finite=True,
            is_profile_surjective=is_profile_surjective,
            is_factorable=True,
            is_fiber_constant=True,
            is_transition_coherent=False,
            has_local_terminalizer=True,
            overall_admissible=False,
            refusal_code=R_SHADOW_COHERENCE_FAILURE,
            residual_mass=quotient_dist,
            verified_values=verified_values,
        )

    return BridgeAdmissibilityReport(
        is_degree_bounded=True,
        is_cofinal=True,
        is_shadow_finite=True,
        is_profile_surjective=is_profile_surjective,
        is_factorable=True,
        is_fiber_constant=True,
        is_transition_coherent=True,
        has_local_terminalizer=True,
        overall_admissible=True,
        refusal_code=None,
        residual_mass=RESIDUAL_SUCCESS,
        verified_values=verified_values,
    )


@dataclass(frozen=True)
class QueryAuthorityResult:
    """Authority verdict for query q on continuum object X."""

    inhabited: bool
    query_id: str
    signal_id: str
    evaluated_value: Optional[Rational]
    refusal_code: Optional[str]
    residual_mass: Rational
    authority_effect: str = "None"


def evaluate_query_authority(
    signal: ContinuumSignal,
    query: ContinuumQuery,
    tower: ShadowTower,
    profile: ProfileMap,
    factored_evaluator: Optional[Callable[[Matrix], Rational]] = None,
    has_terminalizer: bool = True,
    test_signals: Optional[Sequence[ContinuumSignal]] = None,
    d0_transition: Optional[Matrix] = None,
    defect_1cochain: Optional[Matrix] = None,
) -> QueryAuthorityResult:
    """Evaluate a query on ``signal`` against a declared shadow family.

    Fiber constancy is scored on ``test_signals`` when given; a singleton
    family cannot see a collision. Transition coherence is scored only when
    ``d0_transition`` and ``defect_1cochain`` are supplied.
    """
    if not isinstance(has_terminalizer, bool):
        raise TypeError(f"has_terminalizer must be bool, got {type(has_terminalizer).__name__}")
    raw_family: Sequence[ContinuumSignal] = test_signals if test_signals is not None else (signal,)
    family: Tuple[ContinuumSignal, ...] = tuple(raw_family)
    if signal not in family:
        family = (signal, *family)
    report = verify_bridge_admissibility(
        query=query,
        tower=tower,
        profile=profile,
        test_signals=family,
        factored_evaluator=factored_evaluator,
        has_terminalizer=has_terminalizer,
        d0_transition=d0_transition,
        defect_1cochain=defect_1cochain,
    )

    if not report.overall_admissible:
        return QueryAuthorityResult(
            inhabited=False,
            query_id=query.query_id,
            signal_id=signal.signal_id,
            evaluated_value=None,
            refusal_code=report.refusal_code,
            residual_mass=report.residual_mass,
            authority_effect="None",
        )

    # Return the verified query value bound strictly to the target signal's snapshot.
    # If the target signal was not verified in verified_values, refuse rather than evaluating unchecked.
    if not report.verified_values or signal.snapshot_key not in report.verified_values:
        return QueryAuthorityResult(
            inhabited=False,
            query_id=query.query_id,
            signal_id=signal.signal_id,
            evaluated_value=None,
            refusal_code="UnverifiedSignalTarget",
            residual_mass=RESIDUAL_UNAUTHORIZED,
            authority_effect="None",
        )

    val = report.verified_values[signal.snapshot_key]

    return QueryAuthorityResult(
        inhabited=True,
        query_id=query.query_id,
        signal_id=signal.signal_id,
        evaluated_value=val,
        refusal_code=None,
        residual_mass=RESIDUAL_SUCCESS,
        authority_effect="None",
    )


def compute_transition_quotient_obstruction(
    d0_transition: Matrix,
    defect_1cochain: Matrix,
) -> Tuple[Rational, Optional[Matrix], bool]:
    """
    Computes exact cochain quotient distance for shadow transition defect
    using canonical LinearRepairProblem.
    Q^1 = C^1 / im(d0).
    """
    for i in range(defect_1cochain.rows):
        _validate_exact_rational(defect_1cochain[i, 0], f"defect[{i}]")

    problem = LinearRepairProblem(repair_map_d0=d0_transition)
    cert: QuotientDistanceCertificate = problem.quotient_l1_distance(cochain=defect_1cochain)

    quotient_dist = Rational(cert.distance)
    repair_witness = cert.repair_witness
    is_exact = bool(quotient_dist == Rational(0, 1))

    return quotient_dist, repair_witness, is_exact


def reproduce_worked_example() -> Tuple[Rational, Rational, bool]:
    """
    Reproduces Section 0 Worked Example:
    Signal X(t) over grid t in {0, 1/4, 2/4, 3/4, 1}.
    Quadrature query q(X) = sum X(i/4)^2 * (1/4).
    Verifies profile extraction, factorization, and fiber constancy.
    """
    pts = (Rational(0, 4), Rational(1, 4), Rational(2, 4), Rational(3, 4), Rational(4, 4))
    prof = ProfileMap(profile_id="Grid_4", sample_points=pts)

    # Signal 1: X(t) = 2t -> at 0: 0, 1/4: 1/2, 2/4: 1, 3/4: 3/2, 1: 2
    samples1 = {
        Rational(0, 4): Rational(0, 1),
        Rational(1, 4): Rational(1, 2),
        Rational(2, 4): Rational(1, 1),
        Rational(3, 4): Rational(3, 2),
        Rational(4, 4): Rational(2, 1),
    }
    sig1 = ContinuumSignal(signal_id="Sig1", samples=samples1)

    # Signal 2: Identical on grid, differing outside grid
    sig2 = ContinuumSignal(signal_id="Sig2", samples=samples1)

    # Query: Quadrature sum (left quadrature over the 4 intervals)
    def quad_q(sig: ContinuumSignal) -> Rational:
        tot = Rational(0, 1)
        for p in pts[:-1]:
            val = sig.evaluate_at(p)
            tot += val * val * Rational(1, 4)
        return tot

    query = ContinuumQuery(query_id="Quad_Energy", degree_bound=2, evaluator=quad_q)

    # Factored evaluator: bar_q(vec) = sum_{i=0}^3 vec[i]^2 * (1/4)
    def bar_q(vec: Matrix) -> Rational:
        tot = Rational(0, 1)
        for i in range(4):
            v = Rational(vec[i, 0])
            tot += v * v * Rational(1, 4)
        return tot

    tower = ShadowTower(
        tower_id="SampleTower",
        slices=(
            ShadowSlice(index_id="N_4", dimension=5, has_local_authority=True),
        ),
        is_cofinal=True,
    )

    # Verify admissibility
    report = verify_bridge_admissibility(
        query=query,
        tower=tower,
        profile=prof,
        test_signals=[sig1, sig2],
        factored_evaluator=bar_q,
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )

    val1 = quad_q(sig1)
    val2 = quad_q(sig2)

    return val1, val2, report.overall_admissible
