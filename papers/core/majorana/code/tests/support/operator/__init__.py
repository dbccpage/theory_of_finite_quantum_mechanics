"""omega_operator_algebra: Operator algebra and quantum maps package facade."""

from .operator_algebra import (
    ClassificationInput,
    CompositionError,
    CompositionTable,
    DeclaredAction,
    OperatorClass,
    OperatorRegistry,
    OperatorCandidateRegistry,
    TieRCertificate,
    classify,
    lexicographic_tie_break,
    RTProjection,
)

__all__ = [
    "ClassificationInput",
    "CompositionError",
    "CompositionTable",
    "DeclaredAction",
    "OperatorClass",
    "OperatorRegistry",
    "OperatorCandidateRegistry",
    "TieRCertificate",
    "classify",
    "lexicographic_tie_break",
    "RTProjection",
]
