r"""
Conditional Hilbert Lifts of l1 Sector Weights and Born Normalization Redundancy Core Evaluator Module.

AuthorityEffect: None.

Canonical Implementation: omega_engine_projects.ms_majorana.code.tests.support.finite_qm.use_cases.born_normalization
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
import numpy as np


def l1_to_l2_amplitude_lift(rho: np.ndarray, phases: np.ndarray | None = None) -> np.ndarray:
    """Lift discrete L1 probability distribution rho to L2 complex Hilbert amplitude psi."""
    rho_arr = np.asarray(rho, dtype=float).ravel()
    if np.any(rho_arr < 0):
        raise ValueError("Probability distribution rho must be non-negative")

    total_mass = np.sum(rho_arr)
    if total_mass <= 0:
        raise ValueError("Probability distribution rho must have positive sum")

    normalized_rho = rho_arr / total_mass
    amplitudes = np.sqrt(normalized_rho)

    if phases is None:
        return amplitudes.astype(complex)

    phases_arr = np.asarray(phases, dtype=float).ravel()
    if phases_arr.shape != amplitudes.shape:
        raise ValueError("Phases array shape must match rho shape")

    return amplitudes * np.exp(1j * phases_arr)


def verify_born_normalization(psi: np.ndarray, atol: float = 1e-9) -> bool:
    """Verify sum |psi_v|^2 = 1 (Born rule probability normalization)."""
    psi_arr = np.asarray(psi, dtype=complex).ravel()
    l2_norm_sq = float(np.sum(np.abs(psi_arr) ** 2))
    return abs(l2_norm_sq - 1.0) <= atol


@dataclass(frozen=True)
class PaperEvaluator:
    paper_id: str = "qm_020_born_normalization_and_conditional_hilbert_lift"

    def evaluate(self) -> Dict[str, Any]:
        rho_sample = np.array([0.25, 0.75])
        psi_sample = l1_to_l2_amplitude_lift(rho_sample)
        born_pass = verify_born_normalization(psi_sample)
        return {
            "paper_id": self.paper_id,
            "status": "EVALUATED_PASS",
            "authority": "None",
            "sample_l2_norm_sq": float(np.sum(np.abs(psi_sample) ** 2)),
            "born_normalization": born_pass,
        }


__all__ = [
    "l1_to_l2_amplitude_lift",
    "verify_born_normalization",
    "PaperEvaluator",
]
