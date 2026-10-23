"""Declared finite U(1) calculations with an explicit reconstruction firewall."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from itertools import combinations, permutations, product
from math import isfinite
from typing import Mapping

from .exact import as_fraction
from .outcomes import Accepted, Outcome, RefusalCode, Refused
from .projective import ONE, GaussianRational

# Legacy tolerance argument is range-checked, but never relaxes exact U(1) membership.
MAX_U1_TOLERANCE = 1e-6


def _integer_component(value: float) -> Fraction | None:
    """Admit a float only when it is a finite integer value."""
    if not isfinite(value) or not value.is_integer():
        return None
    as_int = int(value)
    if float(as_int) != value:
        return None
    return Fraction(as_int)


def to_gaussian_rational(val: object) -> GaussianRational | None:
    if isinstance(val, GaussianRational):
        return val
    if isinstance(val, bool):
        return None
    if isinstance(val, tuple):
        if len(val) != 2:
            return None
        try:
            return GaussianRational(as_fraction(val[0]), as_fraction(val[1]))
        except (TypeError, ValueError, ZeroDivisionError):
            return None
    if type(val) is complex:
        real = _integer_component(val.real)
        imag = _integer_component(val.imag)
        if real is None or imag is None:
            return None
        return GaussianRational(real, imag)
    if isinstance(val, float):
        component = _integer_component(val)
        if component is None:
            return None
        return GaussianRational(component, Fraction(0))
    if isinstance(val, (int, Fraction)):
        try:
            return GaussianRational(as_fraction(val), Fraction(0))
        except (TypeError, ValueError, ZeroDivisionError):
            return None
    return None


@dataclass(frozen=True)
class U1Connection:
    vertices: tuple[str, ...]
    phases: tuple[tuple[str, str, GaussianRational], ...]
    tolerance: float | Fraction = 1e-12

    def __post_init__(self) -> None:
        if type(self.vertices) is not tuple or type(self.phases) is not tuple:
            raise ValueError("connection vertices and phases must be immutable tuples")
        if (
            not self.vertices
            or any(not isinstance(vertex, str) or not vertex for vertex in self.vertices)
            or len(set(self.vertices)) != len(self.vertices)
        ):
            raise ValueError("connection needs unique named vertices")
        labels = set(self.vertices)
        if not _valid_tolerance(self.tolerance):
            raise ValueError(
                f"connection tolerance must be finite and in (0, {MAX_U1_TOLERANCE}]"
            )
        table: dict[tuple[str, str], GaussianRational] = {}
        normalized: list[tuple[str, str, GaussianRational]] = []
        for item in self.phases:
            if type(item) is not tuple or len(item) != 3:
                raise ValueError("connection phases must be oriented edge triples")
            source, target, supplied_phase = item
            phase = to_gaussian_rational(supplied_phase)
            if source == target or source not in labels or target not in labels:
                raise ValueError("connection edge leaves the carrier")
            if phase is None or not _phase_is_unit(phase, self.tolerance):
                raise ValueError("connection phase is not finite unit modulus")
            if (source, target) in table:
                raise ValueError("connection edge is duplicated")
            if (target, source) in table and table[(target, source)] != phase.conjugate():
                raise ValueError("reverse edge is not the conjugate phase")
            table[(source, target)] = phase
            normalized.append((source, target, phase))
        object.__setattr__(self, "phases", tuple(sorted(normalized, key=lambda item: (item[0], item[1]))))
        if not isinstance(self.tolerance, Fraction):
            object.__setattr__(self, "tolerance", float(self.tolerance))


def _valid_tolerance(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float, Fraction)):
        return False
    try:
        numeric = float(value)
    except (TypeError, ValueError, OverflowError):
        return False
    return isfinite(numeric) and 0 < numeric <= MAX_U1_TOLERANCE


def _phase_is_unit(phase: GaussianRational, tolerance: object) -> bool:
    """Conjugation is inversion only for exact unit phases, for either tolerance type."""
    return phase.norm_squared() == Fraction(1)


def _unit(value: object, tolerance: float | Fraction) -> bool:
    if not _valid_tolerance(tolerance):
        return False
    phase = to_gaussian_rational(value)
    if phase is None:
        return False
    return _phase_is_unit(phase, tolerance)


def make_connection(
    vertices: tuple[str, ...],
    phases: tuple[tuple[str, str, GaussianRational | complex], ...],
    *,
    tolerance: float | Fraction = 1e-12,
) -> Outcome[U1Connection]:
    if type(vertices) is not tuple or type(phases) is not tuple:
        return Refused(
            RefusalCode.INVALID_INPUT,
            "connection vertices and phases must be immutable tuples",
        )
    if (
        not vertices
        or any(not isinstance(vertex, str) or not vertex for vertex in vertices)
        or len(set(vertices)) != len(vertices)
    ):
        return Refused(RefusalCode.INVALID_INPUT, "connection needs unique named vertices")
    if not _valid_tolerance(tolerance):
        return Refused(
            RefusalCode.INVALID_INPUT,
            f"connection tolerance must be finite and in (0, {MAX_U1_TOLERANCE}]",
        )
    labels = set(vertices)
    table: dict[tuple[str, str], GaussianRational] = {}
    normalized_phases: list[tuple[str, str, GaussianRational]] = []
    for item in phases:
        if type(item) is not tuple or len(item) != 3:
            return Refused(RefusalCode.INVALID_INPUT, "connection phases must be edge triples")
        source, target, supplied_phase = item
        phase = to_gaussian_rational(supplied_phase)
        if source == target or source not in labels or target not in labels:
            return Refused(RefusalCode.OUTSIDE_CARRIER, "connection edge leaves the carrier")
        if phase is None or not _unit(phase, tolerance):
            return Refused(RefusalCode.NON_UNIT_PHASE, "connection phase is not unit modulus")
        if (source, target) in table:
            return Refused(RefusalCode.INVALID_INPUT, "connection edge is duplicated")
        if (target, source) in table and table[(target, source)] != phase.conjugate():
            return Refused(RefusalCode.NON_UNIT_PHASE, "reverse edge is not the conjugate phase")
        table[(source, target)] = phase
        normalized_phases.append((source, target, phase))
    stored_tolerance: float | Fraction = tolerance if isinstance(tolerance, Fraction) else float(tolerance)
    return Accepted(U1Connection(vertices, tuple(normalized_phases), stored_tolerance))


def edge_phase(connection: U1Connection, source: str, target: str) -> Outcome[GaussianRational]:
    table = {(u, v): phase for u, v, phase in connection.phases}
    if (source, target) in table:
        return Accepted(table[(source, target)])
    if (target, source) in table:
        return Accepted(table[(target, source)].conjugate())
    return Refused(RefusalCode.MISSING_EDGE, f"missing connection edge {source!r}->{target!r}")


def holonomy(connection: U1Connection, path: tuple[str, ...]) -> Outcome[GaussianRational]:
    if len(path) < 2:
        return Refused(RefusalCode.INVALID_INPUT, "holonomy path needs at least one edge")
    if path[0] != path[-1]:
        return Refused(RefusalCode.OPEN_PATH, "holonomy requires an explicitly closed path")
    value = ONE
    for source, target in zip(path, path[1:]):
        phase = edge_phase(connection, source, target)
        if isinstance(phase, Refused):
            return phase
        value = value * phase.value
    return Accepted(value)


def gauge_transform(
    connection: U1Connection,
    gauge: Mapping[str, GaussianRational | complex],
    *,
    tolerance: float | Fraction | None = None,
) -> Outcome[U1Connection]:
    active_tolerance = connection.tolerance if tolerance is None else tolerance
    if not _valid_tolerance(active_tolerance):
        return Refused(
            RefusalCode.INVALID_INPUT,
            f"gauge tolerance must be finite and in (0, {MAX_U1_TOLERANCE}]",
        )
    normalized_gauge = {vertex: to_gaussian_rational(value) for vertex, value in gauge.items()}
    gauge_covers_vertices = set(gauge) == set(connection.vertices)
    gauge_phases_are_unit = all(
        value is not None and _unit(value, active_tolerance)
        for value in normalized_gauge.values()
    )
    if not gauge_covers_vertices or not gauge_phases_are_unit:
        return Refused(RefusalCode.NON_UNIT_PHASE, "gauge must assign one unit phase to every vertex")
    valid_gauge: dict[str, GaussianRational] = {
        v: val for v, val in normalized_gauge.items() if val is not None
    }
    transformed = tuple(
        (
            source,
            target,
            valid_gauge[source].conjugate() * phase * valid_gauge[target],
        )
        for source, target, phase in connection.phases
    )
    return make_connection(connection.vertices, transformed, tolerance=active_tolerance)


def fixed_scale_phase(value: float, scale: float) -> Outcome[GaussianRational]:
    if (
        isinstance(value, bool)
        or isinstance(scale, bool)
        or not isinstance(value, (int, float, Fraction))
        or not isinstance(scale, (int, float, Fraction))
    ):
        return Refused(RefusalCode.INVALID_INPUT, "phase value and scale must be finite real numbers")
    if isinstance(value, float):
        try:
            numeric_value = float(value)
        except (TypeError, ValueError, OverflowError):
            return Refused(RefusalCode.INVALID_INPUT, "phase value and scale must be finite real numbers")
        if not isfinite(numeric_value):
            return Refused(RefusalCode.INVALID_INPUT, "phase scale must be finite, nonzero, and declared")
        exact_zero = numeric_value == 0.0
    else:
        exact_zero = value == 0
    if isinstance(scale, float):
        try:
            numeric_scale = float(scale)
        except (TypeError, ValueError, OverflowError):
            return Refused(RefusalCode.INVALID_INPUT, "phase value and scale must be finite real numbers")
        if not isfinite(numeric_scale) or numeric_scale == 0.0:
            return Refused(RefusalCode.INVALID_INPUT, "phase scale must be finite, nonzero, and declared")
    elif scale == 0:
        return Refused(RefusalCode.INVALID_INPUT, "phase scale must be finite, nonzero, and declared")
    if exact_zero:
        return Accepted(GaussianRational(Fraction(1), Fraction(0)))
    return Refused(
        RefusalCode.NOT_EXACT,
        "this helper constructs the Gaussian rational (1, 0) only for an exact zero angle",
    )


class QuantumEvidence(str, Enum):
    DECLARED_U1_CALCULATION = "declared_u1_calculation"
    CLASSICAL_SHADOW = "classical_shadow"
    FINITE_CONTEXTUALITY_WITNESS = "finite_contextuality_witness"


def supports_quantum_reconstruction(evidence: QuantumEvidence) -> Refused:
    """Finite calculations never certify a full quantum reconstruction here."""

    return Refused(
        RefusalCode.SCOPE_VIOLATION,
        f"{evidence.value} is finite evidence, not a reconstruction theorem",
    )


# --- Stage 2: Classical Representation & Audited Quantum Reconstruction Boundary ---


@dataclass(frozen=True)
class PresentedCarrier:
    """Finite carrier presentation X -> Q with fibers representing same-report relations."""

    carrier_states: tuple[str, ...]
    report_states: tuple[str, ...]
    presentation_map: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if (
            type(self.carrier_states) is not tuple
            or type(self.report_states) is not tuple
            or type(self.presentation_map) is not tuple
        ):
            raise ValueError("presented carrier components must be immutable tuples")
        if not self.carrier_states or len(set(self.carrier_states)) != len(self.carrier_states):
            raise ValueError("carrier states must be unique and nonempty")
        if not self.report_states or len(set(self.report_states)) != len(self.report_states):
            raise ValueError("report states must be unique and nonempty")
        for item in self.presentation_map:
            if (
                type(item) is not tuple
                or len(item) != 2
                or not isinstance(item[0], str)
                or not isinstance(item[1], str)
            ):
                raise ValueError("presentation map elements must be pairs of string labels")
        pres_keys = [item[0] for item in self.presentation_map]
        if len(pres_keys) != len(set(pres_keys)):
            raise ValueError("presentation map must have unique source keys")
        pres_dict = dict(self.presentation_map)
        if set(pres_dict) != set(self.carrier_states):
            raise ValueError("presentation map must cover all carrier states")
        if any(target not in set(self.report_states) for target in pres_dict.values()):
            raise ValueError("presentation map targets must belong to report states")

    def same_report(self, x: str, y: str) -> bool:
        pres = dict(self.presentation_map)
        return pres[x] == pres[y]


@dataclass(frozen=True)
class IntegerWeights:
    """Integer weight assignment w: Q -> Z preserving total mass under updates."""

    weights: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        if type(self.weights) is not tuple:
            raise ValueError("weights must be an immutable tuple of pairs")
        if any(type(item) is not tuple or len(item) != 2 or not isinstance(item[0], str)
               or not item[0] for item in self.weights):
            raise ValueError("weight entries must be pairs with nonempty string labels")
        labels = [item[0] for item in self.weights]
        if len(labels) != len(set(labels)):
            raise ValueError("weights must have unique state keys")
        if any(type(item[1]) is not int for item in self.weights):
            raise ValueError("weights must be integers")

    @property
    def total_mass(self) -> int:
        return sum(w for _, w in self.weights)

    def weight_of(self, state: str) -> int:
        table = dict(self.weights)
        return table.get(state, 0)


@dataclass(frozen=True)
class PermutationIsometryEnvelope:
    """Isometry envelope over Z preserving the standard Euclidean quadratic form."""

    dimension: int
    permutation: tuple[tuple[str, str], ...]
    states: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.dimension) is not int or self.dimension <= 0:
            raise ValueError("dimension must be a positive integer")
        if type(self.permutation) is not tuple or type(self.states) is not tuple:
            raise ValueError("permutation and states must be immutable tuples")
        if len(self.states) != self.dimension or len(set(self.states)) != self.dimension:
            raise ValueError("states must match dimension and be unique")
        if (len(self.permutation) != self.dimension
                or any(type(pair) is not tuple or len(pair) != 2 for pair in self.permutation)
                or len({pair[0] for pair in self.permutation}) != self.dimension):
            raise ValueError("permutation must contain one pair per source state")
        mapping = dict(self.permutation)
        if set(mapping.keys()) != set(self.states) or set(mapping.values()) != set(self.states):
            raise ValueError("permutation must be a bijection on declared states")

    def matrix(self) -> tuple[tuple[int, ...], ...]:
        mapping = dict(self.permutation)
        index_of = {s: i for i, s in enumerate(self.states)}
        mat: list[tuple[int, ...]] = []
        for i in range(self.dimension):
            row = [0] * self.dimension
            target = mapping[self.states[i]]
            row[index_of[target]] = 1
            mat.append(tuple(row))
        return tuple(mat)

    def is_isometry(self) -> bool:
        """Verifies P^T P = I (preserving the standard Euclidean quadratic form)."""
        mat = self.matrix()
        dim = self.dimension
        for i in range(dim):
            for j in range(dim):
                inner_prod = sum(mat[k][i] * mat[k][j] for k in range(dim))
                expected = 1 if i == j else 0
                if inner_prod != expected:
                    return False  # pragma: no cover # unreachable defensive check
        return True

    def apply(self, weights: IntegerWeights) -> IntegerWeights:
        """Permutation updates preserve total mass identically."""
        if set(k for k, _ in weights.weights) != set(self.states):
            raise ValueError("weights keys must match envelope states exactly")
        mapping = dict(self.permutation)
        inv = {v: k for k, v in mapping.items()}
        new_weights = tuple((s, weights.weight_of(inv[s])) for s in self.states)
        return IntegerWeights(new_weights)

    def inverse(self) -> PermutationIsometryEnvelope:
        inv_perm = tuple((v, k) for k, v in self.permutation)
        return PermutationIsometryEnvelope(self.dimension, inv_perm, self.states)


@dataclass(frozen=True)
class PhaseBlindReadout:
    """Coordinatewise quadratic readout pi(v)_q = |v_q|^2 over Q."""

    @staticmethod
    def readout(
        amplitudes: tuple[GaussianRational | complex | int | Fraction, ...],
    ) -> tuple[Fraction, ...]:
        result = []
        for z in amplitudes:
            gz = to_gaussian_rational(z)
            if gz is None:
                raise ValueError(f"Invalid amplitude: {z!r}")
            result.append(gz.norm_squared())
        return tuple(result)

    @staticmethod
    def fiber_relative_phase(
        v1: tuple[GaussianRational | complex | int | Fraction, ...],
        v2: tuple[GaussianRational | complex | int | Fraction, ...],
    ) -> bool:
        """Verifies equal readouts with non-trivial relative phase over Q(i)."""
        if len(v1) != len(v2):
            return False
        pi1 = PhaseBlindReadout.readout(v1)
        pi2 = PhaseBlindReadout.readout(v2)
        if pi1 != pi2:
            return False

        g1 = [to_gaussian_rational(x) for x in v1]
        g2 = [to_gaussian_rational(x) for x in v2]
        if any(x is None for x in g1) or any(x is None for x in g2):
            return False

        ratios: list[GaussianRational] = []
        for a, b in zip(g1, g2):
            assert a is not None and b is not None
            a_zero = a.norm_squared() == Fraction(0)
            b_zero = b.norm_squared() == Fraction(0)
            if a_zero != b_zero:
                return False
            if not a_zero:
                ratios.append(b / a)
        if not ratios:
            return False
        first_ratio = ratios[0]
        return any(r != first_ratio for r in ratios[1:])


@dataclass(frozen=True)
class InterferenceObstruction:
    """Hadamard mixing separates equal-weight fiber states strictly over Z."""

    @staticmethod
    def unnormalized_hadamard_2() -> tuple[tuple[int, int], tuple[int, int]]:
        return ((1, 1), (1, -1))

    @staticmethod
    def mix(v: tuple[int, int]) -> tuple[int, int]:
        h = InterferenceObstruction.unnormalized_hadamard_2()
        return (h[0][0] * v[0] + h[0][1] * v[1], h[1][0] * v[0] + h[1][1] * v[1])

    @staticmethod
    def demonstrates_non_descent() -> bool:
        v1 = (1, 1)
        v2 = (1, -1)
        pre1 = (v1[0] ** 2, v1[1] ** 2)
        pre2 = (v2[0] ** 2, v2[1] ** 2)
        if pre1 != pre2:
            return False  # pragma: no cover # unreachable defensive check
        post1 = InterferenceObstruction.mix(v1)
        post2 = InterferenceObstruction.mix(v2)
        readout1 = (post1[0] ** 2, post1[1] ** 2)
        readout2 = (post2[0] ** 2, post2[1] ** 2)
        return post1 == (2, 0) and post2 == (0, 2) and readout1 != readout2


@dataclass(frozen=True)
class AlgebraicNonFactorableWitness:
    """Algebraic non-factorable rank >= 2 witness on Bool x Bool (matrix determinant != 0).

    Witnesses algebraic tensor rank >= 2 over Z (or Z[i]). Explicitly distinguished
    from physical quantum entanglement, which requires a composite Hilbert state
    space and LOCC interfaces that remain unpaid in Chapter 19.
    """

    state_matrix: tuple[tuple[int, int], tuple[int, int]] = ((1, 0), (0, 1))

    @property
    def determinant(self) -> int:
        m = self.state_matrix
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    def is_algebraically_nonfactorable(self) -> bool:
        """Witness algebraic tensor rank >= 2 (non-factorable state matrix over Z)."""
        return self.determinant != 0

    def is_entangled(self) -> bool:
        """Backward-compatible alias for is_algebraically_nonfactorable.

        Note: Witnesses algebraic non-factorability over Z, not physical quantum
        entanglement, which requires an explicit composite Hilbert space.
        """
        return self.is_algebraically_nonfactorable()


# Backward-compatible alias
EntanglementWitness = AlgebraicNonFactorableWitness


@dataclass(frozen=True)
class CombiningSystemsInterface:
    """Exposes tensorComb vs dumpRightComb to prove tensor product is not uniquely forced."""

    @staticmethod
    def tensor_comb(
        u: tuple[int, int], v: tuple[int, int]
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        return ((u[0] * v[0], u[0] * v[1]), (u[1] * v[0], u[1] * v[1]))

    @staticmethod
    def dump_right_comb(
        u: tuple[int, int], v: tuple[int, int]
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        v_sum = v[0] + v[1]
        return ((u[0] * v_sum, 0), (u[1] * v_sum, 0))

    @staticmethod
    def demonstrates_non_forcing() -> bool:
        u = (0, 1)
        v = (0, 1)
        t = CombiningSystemsInterface.tensor_comb(u, v)
        d = CombiningSystemsInterface.dump_right_comb(u, v)
        return t != d and t[1][1] == 1 and d[1][1] == 0


@dataclass(frozen=True)
class QuantumImport:
    index: int
    name: str
    mathematical_cost: str
    host_verdict: str  # 'refused' or 'imported'; this catalogue is not a verification receipt


def get_exposed_quantum_imports() -> tuple[QuantumImport, ...]:
    """Catalogues the 8 external quantum interfaces exposed along this route."""
    return (
        QuantumImport(
            1,
            "Field C",
            "Cauchy completeness, topological density, algebraic closure",
            "refused",
        ),
        QuantumImport(
            2,
            "Continuous Circle Group U(1)",
            "Connected Lie group phase symmetry; integer interference needs only {+1, -1}",
            "refused",
        ),
        QuantumImport(
            3,
            "Spectral Theorem for Self-Adjoint Operators",
            "Complete orthonormal eigenbases; GaussInt matrices need not have GaussInt eigenvalues",
            "refused",
        ),
        QuantumImport(
            4,
            "Gleason Frame Continuity (n >= 3)",
            "Continuum sphere frame additivity for dimension >= 3 forcing Born quadratic rule; finite exact ray configurations admit non-Bornian vertices",
            "imported",
        ),
        QuantumImport(
            5,
            "Unique Hilbert Tensor Product",
            "Postulates Hilbert tensor product and universal bilinear property; composite tagging excludes dumpRight but does not uniquely force Hilbert tensor structure",
            "imported",
        ),
        QuantumImport(
            6,
            "CPTP Channels & Unitary Dilation",
            "Completely positive trace-preserving channel structure and unitary dilation on an enlarged system (finite channels admit finite environment r <= d_A d_B; missing structures are CPTP, complex Hilbert space, and unitary embedding)",
            "imported",
        ),
        QuantumImport(
            7,
            "Continuous 1-Parameter Unitary Groups / Stone's Theorem",
            "Continuous time evolution exp(-i H t) requiring R; SO(n, Q) is topologically dense in SO(n, R), but discrete dynamics is restricted to integer steps tau in Z",
            "refused",
        ),
        QuantumImport(
            8,
            "Continuous Dual Cone Completion",
            "Assumes the full positive semidefinite state cone. Finite rational LP fixtures do not verify the continuous cone or its completion.",
            "imported",
        ),
    )


# --- Literal Evidence Anchors corresponding to Chapter 18 P1–P12 fixtures ---


def H006_permutation_isometry() -> PermutationIsometryEnvelope:
    """P1: Permutation isometry envelope over Z preserving total mass and pairing."""
    perm = (("q0", "q1"), ("q1", "q0"))
    return PermutationIsometryEnvelope(2, perm, ("q0", "q1"))


def H009_phase_blind_readout_fiber() -> tuple[tuple[complex, ...], tuple[complex, ...]]:
    """P2: Phase-blind readout fiber states separated by relative phase."""
    v1 = (1 + 0j, 1 + 0j)
    v2 = (1 + 0j, -1 + 0j)
    return v1, v2


def H010_int_no_descent() -> bool:
    """P3: Hadamard mixing separates equal-weight fiber states over Z."""
    return InterferenceObstruction.demonstrates_non_descent()


def H011Circle() -> bool:
    """P4: Binary signs {+1, -1} suffice for destructive cancellation over Z."""
    return (1 + (-1)) == 0


def H013Contract() -> tuple[bool, bool]:
    """One rational frame counterexample, not a proof of Gleason uniqueness.

    For state (1,0), compare the standard frame with ((3,4)/5,(-4,3)/5).
    Both frames are orthonormal. Squared-coordinate sums equal 1; fourth-power
    sums are 1 and 337/625. Functional evaluations use the canonical owner.
    """
    from witnessed_difference.native_functionals import squared_l2
    state = (Fraction(1), Fraction(0))
    frames = (((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))),
              ((Fraction(3, 5), Fraction(4, 5)), (Fraction(-4, 5), Fraction(3, 5))))
    coefficients = [tuple(sum((x*y for x, y in zip(state, ray)), Fraction(0))
                          for ray in frame) for frame in frames]
    quadratic = [squared_l2(values) for values in coefficients]
    quartic = [squared_l2(tuple(squared_l2((a,)) for a in values)) for values in coefficients]
    return quartic[0] != quartic[1], quadratic[0] == quadratic[1] == 1


def H014_bell_not_product() -> bool:
    """P7: Algebraic non-factorable rank >= 2 vector witness on Bool x Bool."""
    witness = AlgebraicNonFactorableWitness()
    return witness.is_algebraically_nonfactorable()


def H014Interface() -> bool:
    """P8: Combining systems interface demonstrates tensor non-forcing (dumpRight)."""
    return CombiningSystemsInterface.demonstrates_non_forcing()


def _finite_endomap(mapping: tuple[int, ...]) -> int:
    if type(mapping) is not tuple or not mapping:
        raise ValueError("a finite endomap needs a nonempty tuple")
    size = len(mapping)
    if any(type(value) is not int or not 0 <= value < size for value in mapping):
        raise ValueError("endomap entries must be integer indices in the carrier")
    return size


def H015_collapse_no_isometry(mapping: tuple[int, ...] = (0, 0)) -> bool:
    """P10 instance: test the Gram matrix of e_j -> e_mapping[j].

    True means this declared basis action fails to be an isometry. No
    alternative action agreeing on every basis vector can repair that failure.
    """
    size = _finite_endomap(mapping)
    columns = tuple(tuple(int(i == mapping[j]) for i in range(size)) for j in range(size))
    gram = tuple(tuple(sum(a * b for a, b in zip(u, v)) for v in columns) for u in columns)
    return any(gram[i][j] != int(i == j) for i in range(size) for j in range(size))


def collapse_dilations(
    mapping: tuple[int, ...] = (0, 0), *, environment_size: int = 2, prepared: int = 0
) -> tuple[tuple[int, ...], ...]:
    """Enumerate every reversible dilation of a supplied report endomap.

    Composite index s * environment_size + e denotes (system, environment).
    Only the prepared slice e=prepared is constrained. The explicit census
    supports composite carriers of at most eight elements; larger inputs refuse.
    """
    size = _finite_endomap(mapping)
    if type(environment_size) is not int or environment_size < 1:
        raise ValueError("environment_size must be a positive integer")
    if type(prepared) is not int or not 0 <= prepared < environment_size:
        raise ValueError("prepared environment index is outside the carrier")
    total = size * environment_size
    if total > 8:
        raise ValueError("dilation census supports at most eight composite states")
    return tuple(
        permutation
        for permutation in permutations(range(total))
        if all(
            permutation[s * environment_size + prepared] // environment_size == mapping[s]
            for s in range(size)
        )
    )


def H015CollapseDilations(
    mapping: tuple[int, ...] = (0, 0), *, environment_size: int = 2, prepared: int = 0
) -> int:
    """P10 instance: count the permutations in the actual finite dilation census."""
    return len(collapse_dilations(mapping, environment_size=environment_size, prepared=prepared))


def report_square_roots(mapping: tuple[int, ...] = (1, 0)) -> tuple[tuple[int, ...], ...]:
    """Exhaust all endomaps on the supplied carrier and retain roots f(f(q))=T(q)."""
    size = _finite_endomap(mapping)
    if size > 6:
        raise ValueError("square-root census supports at most six report states")
    return tuple(
        candidate
        for candidate in product(range(size), repeat=size)
        if all(candidate[candidate[q]] == mapping[q] for q in range(size))
    )


def H016_no_report_half_step(mapping: tuple[int, ...] = (1, 0)) -> bool:
    """P11 instance: absence of an endomap square root, checked by a full census."""
    return not report_square_roots(mapping)


GaussianMatrix = tuple[tuple[GaussianRational, ...], ...]


@dataclass(frozen=True)
class FiniteMatrixRecovery:
    """A supplied finite Z[i]-linear map, adjoint, and composition witness.

    basis_images[j] is the full image of e_j, so the declared action on every
    vector is its linear extension. This does not admit arbitrary nonlinear
    callables or claim that testing finitely many vectors establishes linearity.
    """

    basis_images: GaussianMatrix
    matrix: GaussianMatrix
    adjoint: GaussianMatrix
    other_matrix: GaussianMatrix
    composition: GaussianMatrix


def finite_matrix_recovery_fixture() -> FiniteMatrixRecovery:
    """A non-real, nonsymmetric two-dimensional instance, with hand-stated products."""
    z, o, t = GaussianRational(0), GaussianRational(1), GaussianRational(2)
    i = GaussianRational(0, 1)
    return FiniteMatrixRecovery(
        basis_images=((o, t), (i, -i)),
        matrix=((o, i), (t, -i)),
        adjoint=((o, t), (-i, i)),
        other_matrix=((z, o), (-o, o)),
        composition=((-i, o + i), (i, t - i)),
    )


def _gaussian_integer_square(matrix: GaussianMatrix, size: int) -> None:
    if type(matrix) is not tuple or len(matrix) != size:
        raise ValueError("matrix dimension differs from the declared basis")
    for row in matrix:
        if type(row) is not tuple or len(row) != size:
            raise ValueError("matrix must be square on the declared basis")
        if any(
            type(entry) is not GaussianRational
            or entry.real.denominator != 1
            or entry.imag.denominator != 1
            for entry in row
        ):
            raise TypeError("matrix entries must be exact Gaussian integers")


def H017Fin(witness: FiniteMatrixRecovery | None = None) -> bool:
    """P12 instance check: columns, conjugate adjoint, and composition over Z[i].

    The universal isomorphism theorem remains a written linear-algebra theorem.
    This executable anchor checks the supplied finite witness, not that theorem
    by extrapolating from a single example.
    """
    if witness is None:
        witness = finite_matrix_recovery_fixture()
    if type(witness) is not FiniteMatrixRecovery:
        raise TypeError("expected a finite matrix recovery witness")
    if type(witness.basis_images) is not tuple or not witness.basis_images:
        raise ValueError("matrix recovery needs a nonempty declared basis")
    size = len(witness.basis_images)
    for matrix in (
        witness.basis_images, witness.matrix, witness.adjoint,
        witness.other_matrix, witness.composition,
    ):
        _gaussian_integer_square(matrix, size)
    reconstructed = tuple(tuple(witness.basis_images[j][i] for j in range(size)) for i in range(size))
    adjoint = tuple(tuple(witness.matrix[j][i].conjugate() for j in range(size)) for i in range(size))
    composed = tuple(
        tuple(
            sum((witness.matrix[i][k] * witness.other_matrix[k][j] for k in range(size)), GaussianRational(0))
            for j in range(size)
        )
        for i in range(size)
    )
    return reconstructed == witness.matrix and adjoint == witness.adjoint and composed == witness.composition


# The CH18-P06 table, indexed by first occurrence, not the faulty historical table.
CABELLO_RAYS = (
    (0, 0, 0, 1), (0, 0, 1, 0), (1, 1, 0, 0), (1, -1, 0, 0),
    (0, 1, 0, 0), (1, 0, 1, 0), (1, 0, -1, 0), (1, -1, 1, -1),
    (1, -1, -1, 1), (0, 0, 1, 1), (1, 1, 1, 1), (0, 1, 0, -1),
    (1, 0, 0, 1), (1, 0, 0, -1), (0, 1, -1, 0), (1, 1, -1, 1),
    (1, 1, 1, -1), (1, -1, -1, -1),
)
CABELLO_CONTEXTS = (
    (0, 1, 2, 3), (0, 4, 5, 6), (7, 8, 2, 9),
    (7, 10, 6, 11), (1, 4, 12, 13), (8, 10, 13, 14),
    (15, 16, 3, 9), (15, 17, 5, 11), (16, 17, 12, 14),
)


def H020(
    rays: tuple[tuple[int | Fraction, ...], ...] = CABELLO_RAYS,
    contexts: tuple[tuple[int, ...], ...] = CABELLO_CONTEXTS,
) -> bool:
    """P9: verify the supplied 18-ray, nine-tetrad parity obstruction over Q.

    Checks all nonzero distinct projective rays, all 54 inner products, all
    incidences, and the final mod-two contradiction. Invalid arithmetic or
    malformed shapes raise; well-typed but false witnesses return False.
    """
    if type(rays) is not tuple or len(rays) != 18:
        raise ValueError("the Cabello witness needs eighteen rays")
    for ray in rays:
        if type(ray) is not tuple or len(ray) != 4:
            raise ValueError("rays must be four-dimensional tuples")
        if any(type(value) not in (int, Fraction) for value in ray):
            raise TypeError("ray coordinates must be exact rational scalars")
    if type(contexts) is not tuple or len(contexts) != 9:
        raise ValueError("the Cabello witness needs nine contexts")
    for context in contexts:
        if type(context) is not tuple or len(context) != 4:
            raise ValueError("each context must have four ray indices")
        if any(type(index) is not int or not 0 <= index < len(rays) for index in context):
            raise ValueError("context index is outside the declared rays")
    if any(not any(ray) for ray in rays):
        return False
    normalized = tuple(
        tuple(Fraction(value) / next(value for value in ray if value != 0) for value in ray)
        for ray in rays
    )
    if len(set(normalized)) != len(rays):
        return False
    if any(len(set(context)) != 4 for context in contexts):
        return False
    if len({tuple(sorted(context)) for context in contexts}) != len(contexts):
        return False
    for context in contexts:
        for first, second in combinations(context, 2):
            if sum(a * b for a, b in zip(rays[first], rays[second])) != 0:
                return False
    incidence = tuple(sum(index in context for context in contexts) for index in range(len(rays)))
    return all(count == 2 for count in incidence) and len(contexts) % 2 == 1


def H021() -> bool:
    """P5: Vanishing third-order interference I_3 == 0 in quadratic measure model."""
    psi = (1, 1, 1)

    def p(*indices: int) -> int:
        return sum(psi[i] for i in indices) ** 2

    i3 = p(0, 1, 2) - p(0, 1) - p(1, 2) - p(2, 0) + p(0) + p(1) + p(2)
    return i3 == 0


EVIDENCE_ANCHORS: dict[str, object] = {
    "H006.permutation_isometry": H006_permutation_isometry,
    "H009": H009_phase_blind_readout_fiber,
    "H010.int_no_descent": H010_int_no_descent,
    "H011Circle": H011Circle,
    "H013Contract": H013Contract,
    "H014.bell_not_product": H014_bell_not_product,
    "H014Interface": H014Interface,
    "H015.collapse_no_isometry": H015_collapse_no_isometry,
    "H015CollapseDilations": H015CollapseDilations,
    "H016.no_report_half_step": H016_no_report_half_step,
    "H017Fin": H017Fin,
    "H020": H020,
    "H021": H021,
}

# Executable finite evidence; AuthorityEffect: None.
