"""Canonical Residual models for Python (omega_types)."""

import math
from pydantic import BaseModel


class ResidualDefect(BaseModel):
    residual_id: str
    phi1_mass: float
    gamma2_mass: float
    is_closed: bool
    description: str


class ResidualToleranceGate(BaseModel):
    tolerance: float = 1e-8

    def is_closed(self, residual_l1: float) -> bool:
        return math.isfinite(residual_l1) and 0.0 <= residual_l1 < self.tolerance
