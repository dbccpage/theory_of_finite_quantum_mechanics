"""Conditional Hilbert Lifts of ℓ¹ Sector Weights and Born Normalization Redundancy Core Evaluator Module.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, Sequence
import numpy as np

try:
    from .qm.campaigns.born_normalization import (
        BornNormalizationError,
        exact_born_purity,
        l1_to_l2_amplitude_lift,
        verify_born_normalization,
    )
except (ImportError, ValueError):
    try:
        from src.qm.campaigns.born_normalization import (
            BornNormalizationError,
            exact_born_purity,
            l1_to_l2_amplitude_lift,
            verify_born_normalization,
        )
    except (ImportError, ValueError):
        from qm.campaigns.born_normalization import (
            BornNormalizationError,
            exact_born_purity,
            l1_to_l2_amplitude_lift,
            verify_born_normalization,
        )


@dataclass(frozen=True)
class PaperEvaluator:
    paper_id: str = "qm_020_born_normalization_and_conditional_hilbert_lift"

    def evaluate(self) -> Dict[str, Any]:
        rho_sample = np.array([0.25, 0.75])
        psi_sample = l1_to_l2_amplitude_lift(rho_sample)
        born_pass = verify_born_normalization(psi_sample)
        purity = exact_born_purity((Fraction(1, 4), Fraction(3, 4)))
        return {
            "paper_id": self.paper_id,
            "status": "EVALUATED_PASS" if born_pass else "EVALUATED_FAIL",
            "authority": "None",
            "sample_l2_norm_sq": float(np.sum(np.abs(psi_sample) ** 2)),
            "exact_purity": purity,
            "born_normalization": born_pass,
        }


__all__ = [
    "BornNormalizationError",
    "PaperEvaluator",
    "exact_born_purity",
    "l1_to_l2_amplitude_lift",
    "verify_born_normalization",
]


if __name__ == "__main__":
    evaluator = PaperEvaluator()
    print(evaluator.evaluate())
