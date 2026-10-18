"""Phi1-Xi Acceptance Law Decision Enforcement.

Conforms strictly to contract specification:
    urn:omega:governance:evaluator:v1.0.0
    (05_governance/evaluator.contract.yaml)
"""

from typing import Dict


def accept(prev: Dict, curr: Dict, eps: float = 1e-8) -> bool:
    """
    Φ₁-Ξ acceptance law enforcement.

    Accept iff:
        Φ₁ decreases
        OR (Φ₁ unchanged within eps AND Ξ decreases)
    """
    for k in ("Phi1", "Xi"):
        if k not in prev or k not in curr:
            raise KeyError(
                f"Acceptance law requires key '{k}' in both prev and curr states"
            )

    if curr["Phi1"] < prev["Phi1"] - eps:
        return True
    if abs(curr["Phi1"] - prev["Phi1"]) <= eps and curr["Xi"] < prev["Xi"] - eps:
        return True
    return False
