"""
so_k_gauge: SO(k)-Invariant Gauge Classification and Quotient Obstruction Solvers.
Paper: GS-002 (008_so_k_invariant_gauge_classification)
"""

from __future__ import annotations

from carrier import (
    GraphComplex,
    Cochain,
    SlaterViolationError,
    TopologicalDefectError,
)
from gauges import (
    StalkGauge,
    EuclideanGauge,
    CoordinateL1Gauge,
    LpGauge,
    AnisotropicGauge,
    make_so2_rotation,
    make_random_sok_rotation,
    make_signed_permutation,
    audit_so_k_invariance,
    audit_sphere_constancy,
)
from socp_certifier import (
    DualityCertificate,
    SOCPDualityCertificate,
    SOCPCertifier,
    CycleClosedFormCertifier,
    ExactSOCPCertifier,
)
from solver import (
    MixedNormSolver,
    CoordinateL1Solver,
)
from cycle_analytics import (
    compute_cycle_circulation,
    single_cycle_quotient_analytical,
    analyze_triangle_separation,
    analyze_dimension_scaling,
    compute_holonomy,
    apply_vertex_gauge_transformation,
)
from closure import (
    ClosureBoundEvaluator,
    ClosureBoundResult,
)
from falsification import (
    InvasiveAdversary,
    InjectionRecoveryResult,
)

__all__ = [
    "GraphComplex",
    "Cochain",
    "SlaterViolationError",
    "TopologicalDefectError",
    "StalkGauge",
    "EuclideanGauge",
    "CoordinateL1Gauge",
    "LpGauge",
    "AnisotropicGauge",
    "make_so2_rotation",
    "make_random_sok_rotation",
    "make_signed_permutation",
    "audit_so_k_invariance",
    "audit_sphere_constancy",
    "DualityCertificate",
    "SOCPDualityCertificate",
    "SOCPCertifier",
    "CycleClosedFormCertifier",
    "ExactSOCPCertifier",
    "MixedNormSolver",
    "CoordinateL1Solver",
    "compute_cycle_circulation",
    "single_cycle_quotient_analytical",
    "analyze_triangle_separation",
    "analyze_dimension_scaling",
    "compute_holonomy",
    "apply_vertex_gauge_transformation",
    "ClosureBoundEvaluator",
    "ClosureBoundResult",
    "InvasiveAdversary",
    "InjectionRecoveryResult",
]
