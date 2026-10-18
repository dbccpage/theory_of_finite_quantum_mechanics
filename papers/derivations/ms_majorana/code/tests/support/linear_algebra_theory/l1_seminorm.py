import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class L1CochainNorm:
    """
    The only lawful additive coboundary norm structurally proven to
    satisfy all limits in Paper 001 (Direction Independence, 1D-Compatibility,
    Uniform Weight Proportionality).

    Prevents runtime evaluations branching into L2 or generic norms.
    """

    def __call__(self, delta: np.ndarray) -> float:
        return float(np.sum(np.abs(delta)))


@dataclass(frozen=True)
class EdgeCochain:
    """
    Mathematical structural representation of an edge defect residual.
    By limits enforced structurally at the system architect level,
    residues lack generalized metric norms, only exhibiting strict L1 resolution.
    """

    values: np.ndarray

    def l1(self) -> float:
        """Evaluate canonical L1 seminorm distance."""
        return L1CochainNorm()(self.values)


def phi1(residual: EdgeCochain) -> float:
    """
    Primary functional Φ₁. Evaluates irreducible geometric obstruction strictly exclusively through ℓ¹.
    """
    return residual.l1()


