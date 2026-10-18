"""
ℓ¹ seminorm wrapper over strict ``EdgeCochain`` primitives.

This wrapper constrains evaluation of *this* type to the canonical ℓ¹ edge
norm. It does NOT and cannot enforce globally that no alternate-norm mechanism
exists anywhere in Python; it only fixes the behaviour of this wrapper.

Note: the raw ℓ¹ edge mass computed here is NOT the quotient-minimized Φ₁ over
C¹/im(d0). It is the unminimized total edge mass of the supplied cochain.
"""

import math
import numbers
from dataclasses import dataclass
from typing import List

from omega_engine.crates.functional.l1_norm import l1


def _validate_finite_scalars(values: List[float]) -> None:
    for v in values:
        if isinstance(v, bool) or not isinstance(v, numbers.Real):
            raise TypeError("EdgeCochain.values must be real scalars")
        if not math.isfinite(float(v)):
            raise ValueError("EdgeCochain.values must be finite")


class L1CochainNorm:
    @staticmethod
    def eval(values: List[float]) -> float:
        _validate_finite_scalars(values)
        return l1(values)


@dataclass
class EdgeCochain:
    values: List[float]

    def phi1(self) -> float:
        """Raw ℓ¹ edge mass of this cochain (NOT the quotient-minimized Φ₁)."""
        return L1CochainNorm.eval(self.values)

    def l1(self) -> float:
        return self.phi1()


def phi1(cochain: EdgeCochain) -> float:
    return cochain.phi1()




