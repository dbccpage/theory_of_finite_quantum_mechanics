"""Exact finite-dimensional reference implementation for CODA-FOC.

Bounded Context: CODA.FOC (Finite Obstruction Calculus)
AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e).
Self-contained: Zero external monorepo dependencies.
Constraint: Zero floating-point operations in exact algebraic decision paths.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure local package imports work even when imported via arbitrary CWD or file-location loaders
_code_dir = str(Path(__file__).resolve().parent)
if _code_dir not in sys.path:
    sys.path.insert(0, _code_dir)

from foc_core import (  # noqa: E402
    Diagnostic,
    ExactnessCertificate,
    FiniteObstructionPacket,
    FiniteRepairMove,
    FiniteRepairRegistry,
    LinearRepairProblem,
    ObstructionResult,
    QuotientCertificate,
    QuotientDistanceCertificate,
    RepairCheck,
    RepairDisposition,
    StabilizationEvidence,
    TerminalRoute,
    TransportResiduals,
    _as_exact_rational,
    _check_no_floats,
    _digest_exact,
    _digest_strings,
    _exact_l1_dual_vertex,
    _exact_l1_primal_vertex,
    _exact_matrix,
    _exact_scalar,
    _exact_vector,
    _independent_column_indices,
    _is_sha256,
    as_rational,
    diagnose,
    direct_sum,
    exact_equal,
    exact_matrix_from_matrix,
    is_full_subspace_annihilator,
    quotient_certificate,
    terminal_route,
    transport_residuals,
    weighted_l1_operator_norm,
)

__all__ = [
    "Diagnostic",
    "ExactnessCertificate",
    "FiniteObstructionPacket",
    "FiniteRepairMove",
    "FiniteRepairRegistry",
    "LinearRepairProblem",
    "ObstructionResult",
    "QuotientCertificate",
    "QuotientDistanceCertificate",
    "RepairCheck",
    "RepairDisposition",
    "StabilizationEvidence",
    "TerminalRoute",
    "TransportResiduals",
    "_as_exact_rational",
    "_check_no_floats",
    "_digest_exact",
    "_digest_strings",
    "_exact_l1_dual_vertex",
    "_exact_l1_primal_vertex",
    "_exact_matrix",
    "_exact_scalar",
    "_exact_vector",
    "_independent_column_indices",
    "_is_sha256",
    "as_rational",
    "diagnose",
    "direct_sum",
    "exact_equal",
    "exact_matrix_from_matrix",
    "is_full_subspace_annihilator",
    "quotient_certificate",
    "terminal_route",
    "transport_residuals",
    "weighted_l1_operator_norm",
]
