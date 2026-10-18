from __future__ import annotations
"""Homological error taxonomy (port of Rust ``HomologicalError``)."""



class HomologicalError(Exception):
    """Base class for all homological-algebra errors."""


class DimensionMismatch(HomologicalError):
    """A matrix shape does not match the declared chain-group dimensions."""


class CoboundaryLawViolation(HomologicalError):
    """The chain-complex law d1 . d0 = 0 (or d2 . d1 = 0) is violated."""


class NonPositiveWeight(HomologicalError):
    """A carrier weight is not strictly positive."""


class TriangleMissingEdge(HomologicalError):
    """A declared triangle face references an edge absent from the graph."""


class NotCycle(HomologicalError):
    """A chain claimed to be a cycle has nonzero boundary."""


class InvalidProvenance(HomologicalError):
    """Provenance string was empty or otherwise invalid."""

