"""Bridge connecting DDAEngine terminal residual sector weights (Algorithms 1-3) to QM_020 free L1 normalization and optional Hilbert lifts.

Demonstrates that DDA residual sector weights w_gamma produce normalized profiles P(gamma) = w_gamma / sum(w)
via free arithmetic (QM_020 Theorem 1), and that the complex Hilbert amplitude lift c_gamma = sqrt(w_gamma) * e^{i theta}
is a redundant, optional representation choice (QM_020 Theorem 4) under AuthorityEffect = None.
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple
import numpy as np

code_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path(".")
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

qm_020_path = (
    code_dir.parents[2]
    / "published"
    / "003_quantum_foundations"
    / "qm_020_born_normalization_and_conditional_hilbert_lift"
    / "coda"
)
if str(qm_020_path) not in sys.path and qm_020_path.exists():
    sys.path.insert(0, str(qm_020_path))

from omega_engine.crates.discrete_deformation_algebra.dda_engine import DDAEngine, FoundationCert, TerminationCert, TerminationStatus
from omega_engine.crates.residuals.network_residual import Network
try:
    from omega_engine.crates.quantum_physics.born_normalization import (
        l1_to_l2_amplitude_lift,
        verify_born_normalization,
    )
except ImportError:
    try:
        from qm.born_normalization import (
            l1_to_l2_amplitude_lift,
            verify_born_normalization,
        )
    except ImportError:
        from src.qm.born_normalization import (
            l1_to_l2_amplitude_lift,
            verify_born_normalization,
        )



@dataclass
class DDASectorWeightResult:
    """Represents terminal DDA residual sector weights and optional QM_020 representation lifts."""
    sector_weights: Dict[Any, float]
    total_mass: float
    normalized_profile: Dict[Any, float]
    optional_hilbert_amplitudes: Dict[Any, complex]
    born_normalization_verified: bool
    authority_effect: str = "None"
    stage_breakdown: Dict[str, str] = None

    def __post_init__(self):
        if self.stage_breakdown is None:
            object.__setattr__(self, "stage_breakdown", {
                "Algorithms 1-3": "Executable residual sector weights w_gamma (AuthorityEffect: None)",
                "Free Normalization": "P(gamma) = w_gamma / sum(w) (Pure L1 arithmetic)",
                "Optional Hilbert Lift": "c_gamma = sqrt(w_gamma) * e^{i theta} (Representational choice, priced)",
                "Born Uniqueness": "Imported representation assumption (OracleNeeded)",
            })


def dda_residuals_to_qm020_lift(
    sector_weights: Dict[Any, float],
    phases: Dict[Any, float] | None = None
) -> DDASectorWeightResult:
    """Maps DDA residual sector weights to free L1 normalized profile and optional Hilbert lift."""
    sectors = list(sector_weights.keys())
    weights_arr = np.array([sector_weights[s] for s in sectors], dtype=float)

    if np.any(weights_arr < 0):
        raise ValueError("DDA sector weights must be non-negative")

    total_mass = float(np.sum(weights_arr))
    if total_mass <= 0:
        norm_dict = {s: 0.0 for s in sectors}
        amp_dict = {s: 0.0 + 0.0j for s in sectors}
        return DDASectorWeightResult(
            sector_weights=sector_weights,
            total_mass=0.0,
            normalized_profile=norm_dict,
            optional_hilbert_amplitudes=amp_dict,
            born_normalization_verified=True,
        )

    norm_profile = weights_arr / total_mass
    norm_dict = {s: float(p) for s, p in zip(sectors, norm_profile)}

    phases_arr = (
        np.array([phases.get(s, 0.0) for s in sectors], dtype=float)
        if phases is not None else None
    )
    amplitudes = l1_to_l2_amplitude_lift(weights_arr, phases=phases_arr)
    amp_dict = {s: complex(c) for s, c in zip(sectors, amplitudes)}

    born_pass = verify_born_normalization(amplitudes)

    return DDASectorWeightResult(
        sector_weights=sector_weights,
        total_mass=total_mass,
        normalized_profile=norm_dict,
        optional_hilbert_amplitudes=amp_dict,
        born_normalization_verified=born_pass,
    )


if __name__ == "__main__":
    sample_weights = {(0, 1, 2): 3.0, (1, 2, 3): 1.0, (0, 2, 3): 4.0}
    res = dda_residuals_to_qm020_lift(sample_weights)

    print("=== DDA Terminal Residual Sector Weights -> QM_020 Lift ===")
    print(f"Sector Weights w_gamma: {res.sector_weights}")
    print(f"Total Mass W: {res.total_mass}")
    print(f"Normalized Profile P(gamma): {res.normalized_profile}")
    print(f"Optional Hilbert Amplitudes c_gamma: {res.optional_hilbert_amplitudes}")
    print(f"Born Normalization Verified: {res.born_normalization_verified}")
    print(f"AuthorityEffect: {res.authority_effect}")
    print("\nStage Breakdown:")
    for stage, desc in res.stage_breakdown.items():
        print(f"  [{stage}]: {desc}")





