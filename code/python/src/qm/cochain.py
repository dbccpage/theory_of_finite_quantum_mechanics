"""The finite cochain packet of QM-001 §1, computed rather than asserted.

QM_001 declares, in prose:

    D(x, y) := y - x,   with   x = y  <=>  D(x, y) = 0            (QM-001-C4)

    C^0 --d0--> C^1 --d1--> C^2,   with   d1 d0 = 0               (QM-001-C5)

    B^1 := im(d0),  Q^1 := C^1/B^1,  Z^1 := ker(d1),  H^1 := Z^1/B^1

    ||x||_{1,w} := sum_e w_e |x_e|

    Phi_1([x]) := inf_{alpha in C^0} ||x - d0 alpha||_{1,w}
    Gamma_2([x]) := || d1bar [x] ||

    Phi_1 = 0                    -> ExactClass                    (QM-001-C6)
    Phi_1 > 0, Gamma_2 = 0       -> ClosedResidual
    Phi_1 > 0, Gamma_2 > 0       -> ActiveClosureFailure

Every one of those is finitely computable on a declared graph, so none of them
needs to be taken on trust. This module computes them; `tests/unit/test_cochain.py`
checks them against fixtures and against negative controls that must fail.

Scope. This is a *finite computation over declared complexes*. It does not derive
the cochain packet, does not select the weights, and says nothing about quantum
mechanics. `Phi_1` is evaluated numerically as a linear program using HiGHS with
declared feasibility tolerance `TOL = 1e-9`, not an infinite-precision exact solver;
sub-tolerance variations are subject to solver feasibility limits.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linprog

EXACT_CLASS = "ExactClass"
CLOSED_RESIDUAL = "ClosedResidual"
ACTIVE_CLOSURE_FAILURE = "ActiveClosureFailure"

TOL = 1e-9


def primitive_difference(x: float, y: float) -> float:
    """QM-001-C4: `D(x, y) := y - x`."""
    return y - x


def is_same(x: float, y: float, tol: float = TOL) -> bool:
    """QM-001-C4: sameness is certified zero difference, never assumed."""
    return abs(primitive_difference(x, y)) <= tol


@dataclass(frozen=True)
class Complex:
    """A declared finite 2-complex: vertices, directed edges, and 2-cells.

    `d0` is the vertex-to-edge coboundary `(d0 f)(u, v) = f(v) - f(u)`.
    `d1` sums a 1-cochain around each 2-cell with the given orientations, which
    is what makes `d1 d0 = 0` hold: every vertex value enters a closed loop once
    positively and once negatively.
    """

    n_vertices: int
    edges: tuple[tuple[int, int], ...]
    faces: tuple[tuple[tuple[int, int], ...], ...] = ()
    weights: tuple[float, ...] | None = None

    _w: np.ndarray = field(init=False, repr=False, compare=False, default=None)

    def __post_init__(self) -> None:
        w = np.ones(len(self.edges)) if self.weights is None else np.asarray(self.weights, float)
        if w.shape != (len(self.edges),):
            raise ValueError(f"weights must have one entry per edge, got {w.shape}")
        if np.any(w <= 0):
            raise ValueError("edge weights must be strictly positive")
        object.__setattr__(self, "_w", w)

    @property
    def weight_vector(self) -> np.ndarray:
        return self._w

    def d0(self) -> np.ndarray:
        """Matrix of `d0 : C^0 -> C^1`."""
        m = np.zeros((len(self.edges), self.n_vertices))
        for i, (u, v) in enumerate(self.edges):
            m[i, v] += 1.0
            m[i, u] -= 1.0
        return m

    def d1(self) -> np.ndarray:
        """Matrix of `d1 : C^1 -> C^2`."""
        m = np.zeros((len(self.faces), len(self.edges)))
        for j, face in enumerate(self.faces):
            for edge_index, orientation in face:
                m[j, edge_index] += float(orientation)
        return m


def d1_d0_is_zero(cx: Complex, tol: float = TOL) -> bool:
    """QM-001-C5: the packet is a complex, `d1 d0 = 0`."""
    return bool(np.all(np.abs(cx.d1() @ cx.d0()) <= tol))


def weighted_l1(cx: Complex, x: np.ndarray) -> float:
    """`||x||_{1,w} = sum_e w_e |x_e|`."""
    return float(np.sum(cx.weight_vector * np.abs(np.asarray(x, float))))


def phi_1(cx: Complex, x: np.ndarray) -> float:
    """`Phi_1([x]) = inf_{alpha} ||x - d0 alpha||_{1,w}`, evaluated via LP (HiGHS).

    Variables are `(alpha, t)` with `t` bounding `|x - d0 alpha|` coordinatewise:

        minimise  sum_e w_e t_e
        s.t.       (x - d0 alpha)_e <= t_e
                  -(x - d0 alpha)_e <= t_e

    The objective is bounded below by 0, so the LP is always feasible and
    bounded even though `d0` has constants in its kernel.
    """
    x = np.asarray(x, float)
    a = cx.d0()
    n_e, n_v = a.shape
    if x.shape != (n_e,):
        raise ValueError(f"cochain must have one entry per edge, got {x.shape}")

    scale = float(np.max(np.abs(x))) if len(x) > 0 else 0.0
    if scale < 1e-15:
        return 0.0

    x_scaled = x / scale

    c = np.concatenate([np.zeros(n_v), cx.weight_vector])
    upper = np.hstack([-a, -np.eye(n_e)])
    lower = np.hstack([a, -np.eye(n_e)])
    a_ub = np.vstack([upper, lower])
    b_ub = np.concatenate([-x_scaled, x_scaled])
    bounds = [(None, None)] * n_v + [(0, None)] * n_e

    res = linprog(
        c,
        A_ub=a_ub,
        b_ub=b_ub,
        bounds=bounds,
        method="highs",
        options={
            "primal_feasibility_tolerance": 1e-10,
            "dual_feasibility_tolerance": 1e-10,
        },
    )
    if not res.success:
        raise RuntimeError(f"Phi_1 LP did not solve: {res.message}")
    return float(res.fun) * scale


def gamma_2(cx: Complex, x: np.ndarray) -> float:
    """`Gamma_2([x]) = ||d1bar [x]||`, the closure defect.

    Well defined on the quotient exactly because `d1 d0 = 0`: adding any `d0
    alpha` to `x` leaves `d1 x` unchanged, so this reads the class, not the
    representative. `test_cochain.py` checks that invariance rather than assuming
    it.
    """
    return float(np.linalg.norm(cx.d1() @ np.asarray(x, float), ord=1))


def classify(cx: Complex, x: np.ndarray, tol: float = TOL) -> str:
    """QM-001-C6: the exact obstruction diagnostic trichotomy.

    Diagnostic only. Landing in a class authorizes nothing.
    """
    p = phi_1(cx, x)
    if p <= tol:
        return EXACT_CLASS
    return CLOSED_RESIDUAL if gamma_2(cx, x) <= tol else ACTIVE_CLOSURE_FAILURE


def triangle(weights: tuple[float, ...] | None = None) -> Complex:
    """The oriented 3-cycle 0->1->2->0 with its single 2-cell.

    The smallest complex on which `Phi_1` and `Gamma_2` can disagree, so it is
    the fixture the trichotomy is exercised on.
    """
    return Complex(
        n_vertices=3,
        edges=((0, 1), (1, 2), (2, 0)),
        faces=(((0, +1), (1, +1), (2, +1)),),
        weights=weights,
    )

__all__ = ['ACTIVE_CLOSURE_FAILURE', 'CLOSED_RESIDUAL', 'Complex', 'EXACT_CLASS', 'TOL', 'classify', 'd1_d0_is_zero', 'gamma_2', 'is_same', 'phi_1', 'primitive_difference', 'triangle', 'weighted_l1']
