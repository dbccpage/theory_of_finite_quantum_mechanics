"""Compatibility facade redirecting legacy dda_engine to discrete_descent_engine.

AuthorityEffect: None.
"""
from __future__ import annotations

from discrete_descent_engine import (
    TerminationStatus,
    FoundationCert,
    DDAStepCert,
    WindowLiftCert,
    TerminationCert,
    DiscreteDescentEngine,
    DDAEngine,
)

__all__ = [
    "TerminationStatus",
    "FoundationCert",
    "DDAStepCert",
    "WindowLiftCert",
    "TerminationCert",
    "DiscreteDescentEngine",
    "DDAEngine",
]
