"""
Vector and Quantum Observer Geometries: Gauge Relativity and Trace Metric Bounds.
Paper: GS-003 (vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

from exceptions import (
    ObserverGeometryError,
    NonHermitianOperatorError,
    NonCPTPChannelError,
    IntertwiningViolationError,
    BoundaryConditionError,
    DimensionMismatchError,
)

from cochain_complex import Cochain, GraphComplex
from classical_geometry import ClassicalDualityCertificate, ClassicalQuotientSolver
from quantum_geometry import (
    HermitianOperator,
    QuantumDualityCertificate,
    QuantumQuotientSolver,
)
from cptp_channels import KrausChannel, CochainMorphism
from demonstrations import (
    demo_classical_triangle_separation,
    demo_quantum_triangle_uniform_z,
    demo_bloch_isometry_vs_qutrit_crosspolytope,
    demo_cptp_quotient_monotonicity,
)

__all__ = [
    # Exceptions
    "ObserverGeometryError",
    "NonHermitianOperatorError",
    "NonCPTPChannelError",
    "IntertwiningViolationError",
    "BoundaryConditionError",
    "DimensionMismatchError",
    # Complex
    "Cochain",
    "GraphComplex",
    # Classical
    "ClassicalDualityCertificate",
    "ClassicalQuotientSolver",
    # Quantum
    "HermitianOperator",
    "QuantumDualityCertificate",
    "QuantumQuotientSolver",
    # CPTP Channels
    "KrausChannel",
    "CochainMorphism",
    # Demonstrations
    "demo_classical_triangle_separation",
    "demo_quantum_triangle_uniform_z",
    "demo_bloch_isometry_vs_qutrit_crosspolytope",
    "demo_cptp_quotient_monotonicity",
]
