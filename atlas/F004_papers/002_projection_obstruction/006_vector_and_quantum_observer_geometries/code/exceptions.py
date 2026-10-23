"""
Typed Domain Exceptions for 006 Vector and Quantum Observer Geometries.
Paper: GS-003 (006_vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""


class ObserverGeometryError(ValueError):
    """Base exception for observer geometry domain violations."""

    pass


class NonHermitianOperatorError(ObserverGeometryError):
    """Raised when an operator expected to be Hermitian violates Hermiticity."""

    pass


class NonCPTPChannelError(ObserverGeometryError):
    """Raised when a channel fails Completely Positive Trace-Preserving conditions."""

    pass


class IntertwiningViolationError(ObserverGeometryError):
    """Raised when a cochain morphism fails the coboundary intertwining condition Lambda^1 d0 = d0' Lambda^0."""

    pass


class BoundaryConditionError(ObserverGeometryError):
    """Raised when a chain/cochain complex fails the boundary property d1 d0 = 0."""

    pass


class DimensionMismatchError(ObserverGeometryError):
    """Raised when dimensions of cochains, complexes, or operators mismatch."""

    pass
