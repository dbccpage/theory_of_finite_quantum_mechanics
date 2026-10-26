# -*- coding: utf-8 -*-
"""
Meron-Cluster Fermion Chain to Continuum Wilsonian Bridge.

AuthorityEffect: None.

Bridges the exact finite Meron cluster partition sums / transfer matrix traces:
    L=4: Z = 912
    L=6: Z = 33012
    L=8: Z = 973824
to the infinite thermodynamic limit (L -> infty) using certified rational
interval calculus and Wilsonian finite-size scaling extrapolation.

For each periodic fermion chain of size L with 2*repetitions time steps,
computes the certified log partition density:
    g(L) = (1 / L) * ln(Z(L)) in Q x Q,
and eliminates (1/L)^2 and (1/L)^4 finite-size corrections via exact Neville
rational tableau elimination to isolate the thermodynamic free energy density
f_infty with certified rational bounds.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple

# Ensure projects are on path
REPO_ROOT = Path(__file__).resolve().parents[3]
FSP_CODE = str(REPO_ROOT / "omega_engine_projects" / "fsp" / "meron_sign_problem" / "code")
if FSP_CODE not in sys.path:
    sys.path.insert(0, FSP_CODE)

from interval_calculus import (
    RationalInterval,
    _validate_exact_int,
    _validate_exact_rational,
    certified_ln_interval,
)
from meron_exact_model import meron_transfer_trace
from wilsonian_extrapolator import WilsonianExtrapolator, WilsonianScalingReceipt


@dataclass(frozen=True)
class MeronThermodynamicReceipt:
    """Certified thermodynamic limit receipt for the Meron fermion chain."""

    chain_lengths: Tuple[int, ...]
    partition_sums: Dict[int, int]
    log_partition_densities: Dict[int, Dict[str, str]]
    thermodynamic_limit: Dict[str, str]
    finite_size_residuals: Dict[int, Dict[str, str]]
    receipt_sha256: str
    authority_effect: str = "None"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chain_lengths": list(self.chain_lengths),
            "partition_sums": {str(k): v for k, v in self.partition_sums.items()},
            "log_partition_densities": {str(k): v for k, v in self.log_partition_densities.items()},
            "thermodynamic_limit": self.thermodynamic_limit,
            "finite_size_residuals": {str(k): v for k, v in self.finite_size_residuals.items()},
            "receipt_sha256": self.receipt_sha256,
            "authority_effect": self.authority_effect,
        }


class MeronWilsonianBridge:
    """Calculates and extrapolates Meron cluster transfer traces to the thermodynamic limit."""

    # Checked-in ground truth traces for repetitions=2, q=3
    CANONICAL_TRACES: Dict[int, int] = {
        4: 912,
        6: 33012,
        8: 973824,
    }

    def __init__(self, repetitions: int = 2, q: str = "3") -> None:
        self.repetitions = _validate_exact_int(repetitions, "repetitions")
        self.q = q

    def get_or_compute_trace(self, sites: int) -> int:
        """Retrieve canonical trace or compute transfer trace directly."""
        s = _validate_exact_int(sites, "sites")
        if s in self.CANONICAL_TRACES and self.repetitions == 2 and self.q == "3":
            return self.CANONICAL_TRACES[s]
        trace_str = meron_transfer_trace(s, self.repetitions, self.q)
        return int(trace_str)

    def compute_log_density(self, sites: int, order: int = 25) -> RationalInterval:
        """Compute certified interval g(L) = (1/L) * ln(Z(L))."""
        s = _validate_exact_int(sites, "sites")
        z = self.get_or_compute_trace(s)
        z_interval = RationalInterval(Fraction(z), Fraction(z))
        ln_z = certified_ln_interval(z_interval, order=order)
        return ln_z / Fraction(s)

    def extrapolate_meron_continuum(
        self,
        chain_lengths: Sequence[int] = (4, 6, 8),
        order: int = 25,
    ) -> Tuple[MeronThermodynamicReceipt, WilsonianScalingReceipt]:
        """Perform Wilsonian finite-size scaling extrapolation in (1/L)^2."""
        extrapolator = WilsonianExtrapolator(scaling_variable_power=2)
        densities: Dict[int, RationalInterval] = {}
        traces: Dict[int, int] = {}

        for l in chain_lengths:
            l_val = _validate_exact_int(l, "chain_length")
            z = self.get_or_compute_trace(l_val)
            traces[l_val] = z
            g_l = self.compute_log_density(l_val, order=order)
            densities[l_val] = g_l
            extrapolator.add_observation(l_val, g_l)

        scaling_receipt = extrapolator.extrapolate()
        f_inf = scaling_receipt.extrapolated_thermodynamic_limit

        density_dict = {
            l: {
                "lo": str(densities[l].lo),
                "hi": str(densities[l].hi),
                "width": str(densities[l].width),
                "float_midpoint": f"{float(densities[l].midpoint):.10f}",
            }
            for l in chain_lengths
        }

        residuals_dict = {
            l: {
                "lo": str(scaling_receipt.finite_size_residuals[l].lo),
                "hi": str(scaling_receipt.finite_size_residuals[l].hi),
            }
            for l in chain_lengths
        }

        thermo_dict = {
            "lo": str(f_inf.lo),
            "hi": str(f_inf.hi),
            "width": str(f_inf.width),
            "float_midpoint": f"{float(f_inf.midpoint):.10f}",
        }

        payload = {
            "chain_lengths": list(chain_lengths),
            "traces": traces,
            "thermodynamic_limit": thermo_dict,
            "densities": density_dict,
        }
        digest = sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        meron_receipt = MeronThermodynamicReceipt(
            chain_lengths=tuple(chain_lengths),
            partition_sums=traces,
            log_partition_densities=density_dict,
            thermodynamic_limit=thermo_dict,
            finite_size_residuals=residuals_dict,
            receipt_sha256=digest,
            authority_effect="None",
        )

        return meron_receipt, scaling_receipt


__all__ = [
    "MeronThermodynamicReceipt",
    "MeronWilsonianBridge",
]
