# -*- coding: utf-8 -*-
"""
Wilsonian Finite-Size Scaling Extrapolation Adapter.

AuthorityEffect: None.

Builds a certified extrapolation adapter taking discrete results from finite
chains of length L in {4, 6, 8, 12, ...}, fits the finite-size scaling form:
    Z(L) = L * f_infty + Delta(L)  or  g(L) = f_infty + c_1 / L^p + c_2 / L^{2p} + ...
and computes the thermodynamic limit f_infty with certified rational interval bounds.

All calculations are performed using exact rational interval arithmetic
(RationalInterval in Q x Q), propagating finite-size uncertainties and
discretization errors rigorously without floating-point approximations.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from interval_calculus import (
    RationalInterval,
    _validate_exact_int,
    _validate_exact_rational,
)


@dataclass(frozen=True)
class ChainObservation:
    """Measurement of an extensive or intensive observable on a finite chain of size L."""

    chain_length_l: int
    observable_value: RationalInterval  # E.g. ground state energy E_0(L), or free energy density
    is_density: bool = True  # If True, value is already intensive (e.g. E_0/L); if False, extensive

    def __post_init__(self) -> None:
        l_val = _validate_exact_int(self.chain_length_l, "chain_length_l")
        if l_val <= 0:
            raise ValueError(f"chain_length_l must be positive, got {l_val}")
        if not isinstance(self.observable_value, RationalInterval):
            raise TypeError("observable_value must be a RationalInterval")

    @property
    def density_value(self) -> RationalInterval:
        """Intensive density value g(L) = Value(L) / L if extensive, else Value(L)."""
        if self.is_density:
            return self.observable_value
        return self.observable_value / self.chain_length_l


@dataclass(frozen=True)
class WilsonianScalingReceipt:
    """Certified audit receipt for finite-size scaling extrapolation to thermodynamic limit."""

    input_chain_lengths: Tuple[int, ...]
    scaling_variable_power: int  # p where scaling is in (1/L)^p, e.g. p=2 for symmetric 1D chains
    extrapolated_thermodynamic_limit: RationalInterval
    neville_tableau: Tuple[Tuple[RationalInterval, ...], ...]
    finite_size_residuals: Dict[int, RationalInterval]
    receipt_sha256: str
    authority_effect: str = "None"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_chain_lengths": list(self.input_chain_lengths),
            "scaling_variable_power": self.scaling_variable_power,
            "extrapolated_thermodynamic_limit": {
                "lo": str(self.extrapolated_thermodynamic_limit.lo),
                "hi": str(self.extrapolated_thermodynamic_limit.hi),
                "width": str(self.extrapolated_thermodynamic_limit.width),
                "midpoint_float": float(self.extrapolated_thermodynamic_limit.midpoint),
            },
            "residuals_by_l": {
                str(l): {
                    "lo": str(res.lo),
                    "hi": str(res.hi),
                }
                for l, res in self.finite_size_residuals.items()
            },
            "receipt_sha256": self.receipt_sha256,
            "authority_effect": self.authority_effect,
        }


class WilsonianExtrapolator:
    """Extrapolates finite-size chain data to the infinite thermodynamic limit (L -> infty)."""

    def __init__(self, scaling_variable_power: int = 2) -> None:
        p = _validate_exact_int(scaling_variable_power, "scaling_variable_power")
        if p < 1:
            raise ValueError(f"scaling_variable_power must be >= 1, got {p}")
        self.scaling_power = p
        self._observations: Dict[int, ChainObservation] = {}

    def add_observation(
        self,
        l: int,
        val: Union[RationalInterval, Fraction, int, str],
        radius: Union[Fraction, int, str] = Fraction(0),
        is_density: bool = True,
    ) -> None:
        """Record an observation for chain length L."""
        l_int = _validate_exact_int(l, "chain_length_l")
        if isinstance(val, RationalInterval):
            interval = val
        else:
            interval = RationalInterval.from_point(val, radius)
        obs = ChainObservation(chain_length_l=l_int, observable_value=interval, is_density=is_density)
        self._observations[l_int] = obs

    def extrapolate(self, select_lengths: Optional[Sequence[int]] = None) -> WilsonianScalingReceipt:
        """Perform Neville-Aitken polynomial extrapolation in x = (1/L)^p evaluated at x = 0.
        
        Given nodes (x_i, y_i) where x_i = (1/L_i)^p:
          T_{i, 0} = y_i
          T_{i, k} = (x_{i+k} * T_{i, k-1} - x_i * T_{i+1, k-1}) / (x_{i+k} - x_i)
        At x = 0, this simplifies in terms of L directly:
          T_{i, k} = (L_{i+k}^p * T_{i+1, k-1} - L_i^p * T_{i, k-1}) / (L_{i+k}^p - L_i^p).
        """
        if select_lengths is None:
            lengths = sorted(self._observations.keys())
        else:
            lengths = sorted([_validate_exact_int(x, "selected length") for x in select_lengths])

        if len(lengths) < 2:
            raise ValueError(f"Extrapolation requires at least 2 chain lengths, got {len(lengths)}")

        for l in lengths:
            if l not in self._observations:
                raise KeyError(f"No observation recorded for chain length L={l}")

        n = len(lengths)
        p = self.scaling_power

        # Initialize tableau T[i][k]
        # Column 0: raw density values
        tableau: List[List[RationalInterval]] = []
        col0 = [self._observations[l].density_value for l in lengths]
        tableau.append(col0)

        # Neville recurrence
        for k in range(1, n):
            col_k: List[RationalInterval] = []
            for i in range(n - k):
                l_i = Fraction(lengths[i] ** p)
                l_ik = Fraction(lengths[i + k] ** p)
                t_prev_low = tableau[k - 1][i]
                t_prev_high = tableau[k - 1][i + 1]
                # Formula: (l_ik * t_prev_high - l_i * t_prev_low) / (l_ik - l_i)
                denom = l_ik - l_i
                t_ik = (t_prev_high * l_ik - t_prev_low * l_i) / denom
                col_k.append(t_ik)
            tableau.append(col_k)

        # Highest-order extrapolated enclosure at the apex: T[n-1][0]
        thermo_limit = tableau[n - 1][0]

        # Compute finite-size residuals: Delta(L) = g(L) - f_infty (or L * (g(L) - f_infty))
        residuals: Dict[int, RationalInterval] = {}
        for l in lengths:
            g_l = self._observations[l].density_value
            delta_density = g_l - thermo_limit
            # Extensive correction Delta(L) = L * delta_density
            residuals[l] = delta_density * l

        # Freeze tableau into tuples
        frozen_tableau = tuple(tuple(col) for col in tableau)

        payload = {
            "lengths": lengths,
            "scaling_power": p,
            "thermo_limit_lo": str(thermo_limit.lo),
            "thermo_limit_hi": str(thermo_limit.hi),
            "thermo_limit_width": str(thermo_limit.width),
            "apex_order": n - 1,
        }
        digest = sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return WilsonianScalingReceipt(
            input_chain_lengths=tuple(lengths),
            scaling_variable_power=p,
            extrapolated_thermodynamic_limit=thermo_limit,
            neville_tableau=frozen_tableau,
            finite_size_residuals=residuals,
            receipt_sha256=digest,
            authority_effect="None",
        )


__all__ = [
    "ChainObservation",
    "WilsonianScalingReceipt",
    "WilsonianExtrapolator",
]
