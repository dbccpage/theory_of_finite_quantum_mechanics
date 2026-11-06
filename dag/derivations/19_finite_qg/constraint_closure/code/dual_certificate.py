"""Local dual_certificate definitions for paper 002.

Self-contained module replacing legacy omega_engine.crates.linear_algebra_theory.dual_certificate.
AuthorityEffect: None.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import numpy as np

try:
    from .l1_seminorm import EdgeCochain
except ImportError:
    from l1_seminorm import EdgeCochain


@dataclass(frozen=True)
class DivergenceFreeDual:
    """Dual witness phi for the (weighted) L1 obstruction problem.

    Feasibility is the dual of the weighted-L1 primal ``min_f ||omega - B f||_{1,w}``:
    the dual norm of weighted-L1 is weighted-Linf, so the box constraint is
    ``|phi_e| <= w_e`` (per-edge), NOT a uniform ``|phi| <= 1``. With unit weights
    ``w_e = 1`` this reduces to the classical ``||phi||_inf <= 1`` divergence-free
    witness. ``B.T phi = 0`` (divergence-free) is the annihilator condition.
    """

    values: np.ndarray
    weights: Optional[np.ndarray] = None

    @classmethod
    def create(
        cls,
        B: np.ndarray,
        values: np.ndarray,
        tol: float = 1e-7,
        weights: Optional[np.ndarray] = None,
    ) -> "DivergenceFreeDual":
        div = B.T @ values
        if np.any(np.abs(div) > tol):
            raise ValueError(
                f"dual witness is not divergence-free. Max div: {np.max(np.abs(div))}"
            )
        w = (
            np.ones_like(values)
            if weights is None
            else np.asarray(weights, dtype=float)
        )
        if w.shape != values.shape:
            raise ValueError(
                f"weights shape {w.shape} does not match dual values shape {values.shape}"
            )
        if np.any(np.abs(values) > w + tol):
            raise ValueError(
                f"dual witness violates per-edge box ||phi_e|| <= w_e. "
                f"Max excess: {np.max(np.abs(values) - w)}"
            )
        return cls(values, None if weights is None else w)

    def pairing(self, omega: EdgeCochain) -> float:
        """Evaluate the dual objective <phi, omega>."""
        return float(np.dot(self.values, omega.values))

    def is_feasible(self, B: np.ndarray, tol: float = 1e-7) -> bool:
        """Re-check dual feasibility from B (divergence-free + per-edge box)."""
        div = B.T @ self.values
        if np.any(np.abs(div) > tol):
            return False
        w = np.ones_like(self.values) if self.weights is None else self.weights
        return bool(not np.any(np.abs(self.values) > w + tol))


@dataclass(frozen=True)
class PhiCertificate:
    """A *checkable* primal/dual certificate for Phi1 = min_f ||omega - B f||_{1,w}.

    This is NOT self-certifying by construction. ``phi1`` is the primal value
    (an upper bound) computed by a FLOAT LP; ``dual_value = <phi, omega>`` is the
    dual objective (a lower bound) of a feasible divergence-free witness. By weak
    duality ``dual_value <= phi1`` always; the value is *certified-optimal* only
    when the two agree (the duality gap is tight) AND the dual witness is feasible
    against ``B``. Call :meth:`verify` to decide ``certified``; until then the
    float ``phi1`` is only an ESTIMATE. ``weights`` records the per-edge L1
    weights (None == unit weights == classical unweighted Phi1).
    """

    phi1: float
    residual: EdgeCochain
    dual: DivergenceFreeDual
    dual_value: float
    B: Optional[np.ndarray] = None
    tol: float = 1e-6
    weights: Optional[np.ndarray] = None

    def verify(self, tol: Optional[float] = None) -> bool:
        """Return True iff this is a genuine optimality certificate.

        Conditions (all required):
          1. Dual feasibility: ``B.T phi = 0`` and ``|phi_e| <= w_e`` (recomputed
             from ``B`` here, not trusted from construction).
          2. Weak-duality direction: ``dual_value <= phi1 + tol`` (a strictly
             larger dual value signals a bug, never tightness).
          3. Tightness: ``phi1 - dual_value <= tol`` (gap closed).

        Diagnostic only -- mints no authority.
        """
        t = self.tol if tol is None else tol
        if self.B is None:
            return False
        if not self.dual.is_feasible(self.B, tol=max(t, 1e-7)):
            return False
        gap = self.phi1 - self.dual_value
        if self.dual_value > self.phi1 + t:
            return False
        return bool(abs(gap) <= t)

    @property
    def certified(self) -> bool:
        return self.verify()

    @property
    def is_certified(self) -> bool:
        return self.verify()

    @property
    def duality_gap(self) -> float:
        return float(self.phi1 - self.dual_value)
