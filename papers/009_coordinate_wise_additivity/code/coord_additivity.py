"""GS-000 — Coordinate-wise additivity forces edgewise ℓ¹ (finite R^k).

AuthorityEffect: None. Conditional on H1–H5 observer assumptions in the paper.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from numbers import Integral
from typing import Callable, Sequence

import numpy as np

Seminorm = Callable[[np.ndarray], float]
RationalSeminorm = Callable[[Sequence[Fraction]], Fraction]


def _finite_vector(x: np.ndarray | Sequence[float]) -> np.ndarray:
    """Require a real finite vector; do not silently flatten a different carrier."""
    if np.iscomplexobj(x):
        raise ValueError("vector must be real")
    v = np.asarray(x, dtype=float)
    if v.ndim != 1 or not np.all(np.isfinite(v)):
        raise ValueError("vector must be one-dimensional and finite")
    return v


def _nonnegative_scalar(value: float, label: str = "value") -> float:
    result = float(value)
    if not np.isfinite(result) or result < 0:
        raise ValueError(f"{label} must be finite and nonnegative")
    return result


def _dimension(value: int, *, positive: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral) or value < int(positive):
        raise ValueError("dimension must be a positive integer" if positive else
                         "dimension must be a nonnegative integer")
    return int(value)


def _probe_value(nu: Seminorm, x: np.ndarray) -> float:
    return _nonnegative_scalar(nu(x), "diagnostic output")


def coord_l1(x: np.ndarray | Sequence[float], weight: float = 1.0) -> float:
    """Standard coordinatewise ℓ¹ norm with optional scalar weight."""
    v = _finite_vector(x)
    w = _nonnegative_scalar(weight, "weight")
    return _nonnegative_scalar(w * np.sum(np.abs(v)), "weighted norm")


def coord_l1_exact(x: Sequence[Fraction | int], weight: Fraction | int = 1) -> Fraction:
    """Exact rational coordinatewise ℓ¹ norm."""
    w = Fraction(weight)
    if w < 0:
        raise ValueError("weight must be nonnegative")
    return w * sum(abs(Fraction(xi)) for xi in x)


def coord_l2(x: np.ndarray | Sequence[float]) -> float:
    """Standard Euclidean ℓ² norm."""
    v = _finite_vector(x)
    return _nonnegative_scalar(np.hypot.reduce(v, initial=0.0), "Euclidean norm")


def coord_linf(x: np.ndarray | Sequence[float]) -> float:
    """Standard maximum/uniform ℓ^∞ norm."""
    v = _finite_vector(x)
    if v.size == 0:
        return 0.0
    return float(np.max(np.abs(v)))


def anisotropic_l1(x: np.ndarray | Sequence[float], a: tuple[float, ...] = (1.0, 2.0)) -> float:
    """Weighted coordinate ℓ¹ norm with coordinate-dependent weights a_i."""
    v = _finite_vector(x)
    if v.shape[0] != len(a):
        raise ValueError("dimension mismatch")
    weights = [_nonnegative_scalar(ai, "coordinate weight") for ai in a]
    return _nonnegative_scalar(sum(ai * abs(vi) for ai, vi in zip(weights, v)))


def is_absolutely_homogeneous(nu: Seminorm, x: np.ndarray, scalars: list[float], atol: float = 1e-9) -> bool:
    """Probe H5 on one vector and the listed scalars; passing is not an unbounded proof."""
    x = _finite_vector(x)
    atol = _nonnegative_scalar(atol, "tolerance")
    if not scalars or not np.all(np.isfinite(scalars)):
        raise ValueError("at least one finite scalar probe is required")
    base = _probe_value(nu, x)
    for c in scalars:
        scaled = _finite_vector(c * x)
        if abs(_probe_value(nu, scaled) - abs(c) * base) > atol:
            return False
    return True


def decompose_additive_basis(nu: Seminorm, dim: int) -> list[float]:
    """Compute basis seminorm weights w_i = ν(e_i) for standard basis vectors e_i."""
    dim = _dimension(dim)
    weights = []
    for i in range(dim):
        e_i = np.zeros(dim, dtype=float)
        e_i[i] = 1.0
        weights.append(_probe_value(nu, e_i))
    return weights


def decompose_additive_basis_exact(nu: RationalSeminorm, dim: int) -> list[Fraction]:
    """Compute exact rational basis seminorm weights w_i = ν(e_i)."""
    dim = _dimension(dim)
    weights = []
    for i in range(dim):
        e_i = [Fraction(1) if j == i else Fraction(0) for j in range(dim)]
        weights.append(nu(e_i))
    return weights


def is_coord_permutation_symmetric(nu: Seminorm, x: np.ndarray, atol: float = 1e-9) -> bool:
    """Probe H2 on permutations of one vector (k <= 4), not on every vector."""
    v = _finite_vector(x)
    atol = _nonnegative_scalar(atol, "tolerance")
    k = v.shape[0]
    if k > 4:
        raise ValueError("only k<=4 supported for exhaustive perm check")
    from itertools import permutations

    base = _probe_value(nu, v)
    for p in permutations(range(k)):
        if abs(_probe_value(nu, v[list(p)]) - base) > atol:
            return False
    return True


def is_disjoint_coord_additive(nu: Seminorm, k: int, atol: float = 1e-9, seed: int = 0) -> bool:
    """Probe H3 on one seeded basis decomposition; passing does not establish H3."""
    k = _dimension(k, positive=True)
    atol = _nonnegative_scalar(atol, "tolerance")
    rng = np.random.default_rng(seed)
    coeffs = rng.normal(size=k)
    e_sum = np.zeros(k)
    rhs = 0.0
    for i, a in enumerate(coeffs):
        ei = np.zeros(k)
        ei[i] = a
        e_sum += ei
        rhs += _probe_value(nu, ei)
    return abs(_probe_value(nu, e_sum) - rhs) <= atol


def is_disjoint_coord_additive_exact(nu: RationalSeminorm, coeffs: Sequence[Fraction]) -> bool:
    """Exact H3 probe on the specified rational coefficients, not a general proof."""
    k = len(coeffs)
    full_vec = [Fraction(c) for c in coeffs]
    lhs = nu(full_vec)
    rhs = Fraction(0)
    for i, c in enumerate(coeffs):
        ei = [Fraction(c) if j == i else Fraction(0) for j in range(k)]
        rhs += nu(ei)
    return lhs == rhs


def theorem1_weight(nu: Seminorm, k: int) -> float:
    """w = ν(e_1) under H2 (coord symmetry) — all basis weights are equal."""
    k = _dimension(k, positive=True)
    e1 = np.zeros(k)
    e1[0] = 1.0
    return _probe_value(nu, e1)


def theorem1_predict(x: np.ndarray, w: float) -> float:
    """Predicted edgewise value w * ||x||_1."""
    return coord_l1(x, weight=w)


def theorem1_holds(nu: Seminorm, probes: list[np.ndarray], atol: float = 1e-8) -> tuple[bool, float]:
    """Check ν(x) = w ||x||_1 on nonempty finite probes; not a theorem verifier."""
    atol = _nonnegative_scalar(atol, "tolerance")
    if not probes:
        raise ValueError("at least one probe is required")
    vectors = [_finite_vector(x) for x in probes]
    k = _dimension(len(vectors[0]), positive=True)
    if any(len(x) != k for x in vectors):
        raise ValueError("probe dimension mismatch")
    w = theorem1_weight(nu, k)
    for x in vectors:
        if abs(_probe_value(nu, x) - theorem1_predict(x, w)) > atol:
            return False, w
    return True, w


@dataclass(frozen=True)
class EdgeOrbitDiagnostic:
    """Declared orbit-weighted aggregation; this does not derive graph orbits."""

    orbit_of_edge: tuple[int, ...]  # edge -> orbit id
    orbit_weights: tuple[float, ...]  # per orbit id

    def __post_init__(self) -> None:
        for weight in self.orbit_weights:
            _nonnegative_scalar(weight, "orbit weight")
        for orbit in self.orbit_of_edge:
            if (isinstance(orbit, bool) or not isinstance(orbit, Integral)
                    or not 0 <= orbit < len(self.orbit_weights)):
                raise ValueError("orbit id must index the declared weight tuple")

    def total(self, edge_vectors: list[np.ndarray]) -> float:
        if len(edge_vectors) != len(self.orbit_of_edge):
            raise ValueError("edge count mismatch")
        vectors = [_finite_vector(x) for x in edge_vectors]
        if vectors and any(len(x) != len(vectors[0]) for x in vectors):
            raise ValueError("edge coordinate dimension mismatch")
        total = 0.0
        for e, x in enumerate(vectors):
            o = self.orbit_of_edge[e]
            total += self.orbit_weights[o] * coord_l1(x)
        return _nonnegative_scalar(total, "total")

    def total_exact(self, edge_vectors: list[Sequence[Fraction]]) -> Fraction:
        """Exact rational payload sum with weights interpreted by decimal spelling."""
        if len(edge_vectors) != len(self.orbit_of_edge):
            raise ValueError("edge count mismatch")
        if edge_vectors and any(len(x) != len(edge_vectors[0]) for x in edge_vectors):
            raise ValueError("edge coordinate dimension mismatch")
        total = Fraction(0)
        for e, x in enumerate(edge_vectors):
            o = self.orbit_of_edge[e]
            w = Fraction(str(self.orbit_weights[o]))
            total += coord_l1_exact(x, weight=w)
        return total


def ce1_l2_fails_additivity() -> bool:
    """CE1: ℓ² is perm-symmetric and homogeneous but not disjoint-additive."""
    x = np.array([1.0, 0.0])
    y = np.array([0.0, 1.0])
    return abs(coord_l2(x + y) - (coord_l2(x) + coord_l2(y))) > 1e-12


def ce2_anisotropic_fails_symmetry() -> bool:
    """CE2: weighted coord ℓ¹ is additive on disjoint supports but not perm-symmetric."""
    return not is_coord_permutation_symmetric(anisotropic_l1, np.array([1.0, 0.0]))


def ce3_max_fails_additivity() -> bool:
    """Legacy API: ℓ∞ is an additional H3 witness, not manuscript CE3."""
    x = np.array([1.0, 0.0])
    y = np.array([0.0, 1.0])
    return abs(coord_linf(x + y) - (coord_linf(x) + coord_linf(y))) > 1e-12


def ce3_cross_edge_fails_locality() -> bool:
    """Manuscript CE3: |a+b| cancels across edges, contradicting an edge sum."""
    a, b = 1, -1
    return abs(a + b) != abs(a) + abs(b)


def ce4_orbit_weights_do_not_collapse() -> bool:
    """CE4: without edge-transitivity or uniformity, orbit weights do not collapse to unweighted l1."""
    # Graph with 2 edges in distinct orbits: w1 = 1.0, w2 = 2.0
    diag = EdgeOrbitDiagnostic(orbit_of_edge=(0, 1), orbit_weights=(1.0, 2.0))
    e1 = np.array([1.0, 0.0])
    e2 = np.array([0.0, 1.0])
    # Probe on edge 0: (1.0, 0)
    val_e1 = diag.total([e1, np.zeros(2)])
    # Probe on edge 1: (0, 1.0)
    val_e2 = diag.total([np.zeros(2), e2])
    # For unweighted collapse to hold, there must exist alpha such that val_e1 = alpha*||e1||_1 and val_e2 = alpha*||e2||_1
    alpha_e1 = val_e1 / coord_l1(e1)  # 1.0
    alpha_e2 = val_e2 / coord_l1(e2)  # 2.0
    return abs(alpha_e1 - alpha_e2) > 1e-12


def ce5_lp_power_fails_homogeneity(p: float = 2.0) -> bool:
    """Finite non-homogeneity probe for p > 0; p > 1 also loses subadditivity."""
    if not np.isfinite(p) or p <= 0:
        raise ValueError("p must be finite and positive")
    x = np.array([2.0, 3.0])
    c = 2.0

    def phi(v: np.ndarray) -> float:
        return float(np.sum(np.abs(v) ** p))

    # Test |c| * phi(x) vs phi(c * x)
    expected_hom = abs(c) * phi(x)
    actual_scaled = phi(c * x)
    if not np.isfinite(actual_scaled) or not np.isfinite(expected_hom):
        raise ValueError("power-gauge probe overflowed")
    return abs(actual_scaled - expected_hom) > 1e-6


def uniform_collapse(orbit_weights: list[float], edge_l1: list[float]) -> tuple[float, float | None]:
    """Aggregate per-edge weights; report α only for exactly equal stored weights."""
    if len(orbit_weights) != len(edge_l1):
        raise ValueError("weight/value count mismatch")
    weights = [_nonnegative_scalar(w, "edge weight") for w in orbit_weights]
    values = [_nonnegative_scalar(n, "edge norm") for n in edge_l1]
    total = _nonnegative_scalar(sum(w * n for w, n in zip(weights, values)), "total")
    if not orbit_weights:
        return 0.0, None
    if all(w == weights[0] for w in weights):
        return float(total), float(orbit_weights[0])
    return float(total), None
