"""Xi witness construction and validation functions."""

from __future__ import annotations

import math

from omega_engine.crates.type.cycle_aware import XiDiagnostic, XiWitness


class XiWitnessError(Exception):
    pass


class DimensionMismatch(XiWitnessError):
    def __init__(self, omega_len: int, harmonic_len: int):
        super().__init__(f"Dimension mismatch: omega={omega_len}, harmonic={harmonic_len}")


class InvalidXiValue(XiWitnessError):
    pass


class NonFiniteEdgeValue(XiWitnessError):
    pass


def try_compute_xi_witness(omega: list, harmonic_projection: list, xi_value: float, top_k: int) -> XiWitness:
    if len(omega) != len(harmonic_projection):
        raise DimensionMismatch(len(omega), len(harmonic_projection))
    if not math.isfinite(xi_value) or not 0.0 <= xi_value <= 1.0:
        raise InvalidXiValue()
    if any(not math.isfinite(value) for value in omega + harmonic_projection):
        raise NonFiniteEdgeValue()
    return XiWitness([abs(left - right) for left, right in zip(omega, harmonic_projection)], xi_value, top_k)


def validate_xi_diagnostic(diagnostic: XiDiagnostic, edge_count: int) -> bool:
    return (
        len(diagnostic.harmonic_projection) == edge_count
        and math.isfinite(diagnostic.xi_value)
        and 0.0 <= diagnostic.xi_value <= 1.0
        and diagnostic.witness.is_valid()
        and abs(diagnostic.xi_value - diagnostic.witness.xi_value) <= 1e-12
        and all(math.isfinite(value) for value in diagnostic.harmonic_projection)
    )


class XiDiagnosticFunctional:
    def diagnose(self, state) -> XiDiagnostic:
        raise NotImplementedError


__all__ = ["DimensionMismatch", "InvalidXiValue", "NonFiniteEdgeValue", "XiDiagnosticFunctional", "XiWitnessError", "try_compute_xi_witness", "validate_xi_diagnostic"]
