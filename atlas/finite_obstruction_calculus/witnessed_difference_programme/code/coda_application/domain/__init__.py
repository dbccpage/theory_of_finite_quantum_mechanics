# -*- coding: utf-8 -*-
"""
Domain layer for the CODA application.
Contains entities, immutable values, evaluator interfaces and layer contracts.
No file or network I/O and no clock: time limits use a clock the use cases inject, and
the persistent anomalon store is configured by the use-case layer.

AuthorityEffect: None.
"""

from coda_application.domain.entities import (
    AuthorityToken,
    Cochain,
    MasterNormalFormOutcome,
    ProblemInstance,
    ResidualPair,
    Section,
    TerminalKind,
)
from coda_application.domain.value_objects import (
    DualWitness,
    ExactRational,
    FirewallDecision,
)

__all__ = [
    "AuthorityToken",
    "Cochain",
    "DualWitness",
    "ExactRational",
    "FirewallDecision",
    "MasterNormalFormOutcome",
    "ProblemInstance",
    "ResidualPair",
    "Section",
    "TerminalKind",
]
