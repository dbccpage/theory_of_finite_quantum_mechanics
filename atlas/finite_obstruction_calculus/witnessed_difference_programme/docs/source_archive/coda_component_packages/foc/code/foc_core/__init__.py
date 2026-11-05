"""Core exact rational arithmetic, solvers, certificates, packets, and routing for FOC.

Bounded Context: CODA.FOC (Finite Obstruction Calculus)
AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e).
Self-contained: Zero external monorepo dependencies.
Constraint: Zero floating-point operations in exact algebraic decision paths.
"""

from __future__ import annotations

from .diagnosis import (
    diagnose,
    direct_sum,
    is_full_subspace_annihilator,
    quotient_certificate,
)
from .exact_arithmetic import (
    _as_exact_rational,
    _check_no_floats,
    _digest_exact,
    _digest_strings,
    _exact_matrix,
    _exact_scalar,
    _exact_vector,
    _is_sha256,
    as_rational,
    exact_equal,
    exact_matrix_from_matrix,
)
from .packets import (
    Diagnostic,
    FiniteObstructionPacket,
    ObstructionResult,
    QuotientCertificate,
    RepairDisposition,
    TerminalRoute,
)
from .repair import (
    FiniteRepairMove,
    FiniteRepairRegistry,
    RepairCheck,
    StabilizationEvidence,
)
from .routing import (
    terminal_route,
)
from .solvers import (
    ExactnessCertificate,
    LinearRepairProblem,
    QuotientDistanceCertificate,
    _exact_l1_dual_vertex,
    _exact_l1_primal_vertex,
    _independent_column_indices,
)
from .transport import (
    TransportResiduals,
    transport_residuals,
    weighted_l1_operator_norm,
)

__all__ = [
    # Enums & Statuses
    "Diagnostic",
    "RepairDisposition",
    "TerminalRoute",
    # Core Value Objects & Certificates
    "ExactnessCertificate",
    "FiniteObstructionPacket",
    "FiniteRepairMove",
    "FiniteRepairRegistry",
    "LinearRepairProblem",
    "ObstructionResult",
    "QuotientCertificate",
    "QuotientDistanceCertificate",
    "RepairCheck",
    "StabilizationEvidence",
    "TransportResiduals",
    # Diagnosis & Morphism Operations
    "diagnose",
    "direct_sum",
    "is_full_subspace_annihilator",
    "quotient_certificate",
    "terminal_route",
    "transport_residuals",
    "weighted_l1_operator_norm",
    # Exact Arithmetic Gates & Utilities
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
    "exact_equal",
    "exact_matrix_from_matrix",
]
