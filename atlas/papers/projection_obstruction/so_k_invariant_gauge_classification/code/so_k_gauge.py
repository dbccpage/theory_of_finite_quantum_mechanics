"""
Compatibility facade for so_k_gauge.
Paper: GS-002 (so_k_invariant_gauge_classification)
"""

from __future__ import annotations
import sys
from pathlib import Path

# Mark as package to allow submodule import lookups (e.g. from so_k_gauge.carrier import ...)
__path__ = [str(Path(__file__).resolve().parent)]

import carrier
import gauges
import solver
import cycle_analytics
import closure
import falsification
import socp_certifier
import socp_exact_certifier

sys.modules["so_k_gauge"] = sys.modules[__name__]
sys.modules["so_k_gauge.carrier"] = carrier
sys.modules["so_k_gauge.gauges"] = gauges
sys.modules["so_k_gauge.solver"] = solver
sys.modules["so_k_gauge.cycle_analytics"] = cycle_analytics
sys.modules["so_k_gauge.closure"] = closure
sys.modules["so_k_gauge.falsification"] = falsification
sys.modules["so_k_gauge.socp_certifier"] = socp_certifier
sys.modules["so_k_gauge.socp_exact_certifier"] = socp_exact_certifier

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
    SOCPCertifier,
    CycleClosedFormCertifier,
    ExactSOCPCertifier,
    SOCPDualityCertificate,
)
from solver import (
    MixedNormSolver,
    CoordinateL1Solver,
    DualityCertificate,
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
    "SOCPCertifier",
    "CycleClosedFormCertifier",
    "ExactSOCPCertifier",
    "SOCPDualityCertificate",
    "MixedNormSolver",
    "CoordinateL1Solver",
    "DualityCertificate",
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
