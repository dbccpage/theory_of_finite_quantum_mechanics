r"""
L1 Forgetful Functor & Information Loss Component Module (GR-002 / PO-012).
Forgetful Functor L1 -> L2 Information Loss Diagnostic.
AuthorityEffect: None.
"""

from typing import Dict, Any
import numpy as np


def evaluate_forgetful_functor_l1_l2(cochain: np.ndarray) -> Dict[str, Any]:
    r"""
    Quantifies information loss under forgetful map L1 -> L2.
    ||w||_1 = \sum |w_i| vs ||w||_2 = \sqrt{\sum w_i^2}.
    By Cauchy-Schwarz, ||w||_2 <= ||w||_1 <= \sqrt{d} ||w||_2.
    Information loss \Delta = ||w||_1 - ||w||_2 >= 0.
    """
    norm_l1 = float(np.sum(np.abs(cochain)))
    norm_l2 = float(np.linalg.norm(cochain, 2))
    info_loss = norm_l1 - norm_l2
    d = len(cochain)
    theoretical_max = norm_l2 * (np.sqrt(d) - 1.0)

    return {
        "cochain_dim": d,
        "norm_l1": norm_l1,
        "norm_l2": norm_l2,
        "information_loss": info_loss,
        "theoretical_max_loss": float(theoretical_max),
        "forgetful_functor_loss_certified": bool(info_loss >= -1e-12),
        "authority": "None"
    }
