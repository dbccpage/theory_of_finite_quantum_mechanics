"""Port of ``omega_solvers/src/network_simplex/error.rs``."""

from __future__ import annotations
class NetworkSimplexError(Exception):
    """Mirror of the Rust ``NetworkSimplexError`` enum.

    ``kind`` carries the variant name; ``data`` carries the variant payload.
    Equality matches on (kind, data) like the Rust derive.
    """

    EMPTY_GRAPH = "EmptyGraph"
    DEMAND_LENGTH_MISMATCH = "DemandLengthMismatch"
    UNBALANCED_DEMAND = "UnbalancedDemand"
    NEGATIVE_WEIGHT = "NegativeWeight"
    INFEASIBLE = "Infeasible"
    ITERATION_LIMIT_EXCEEDED = "IterationLimitExceeded"
    INVALID_BASIS = "InvalidBasis"
    ARITHMETIC_OVERFLOW = "ArithmeticOverflow"
    INVALID_CARRIER = "InvalidCarrier"
    UNSUPPORTED_ARC_BOUNDS = "UnsupportedArcBounds"

    def __init__(self, kind: str, **data):
        self.kind = kind
        self.data = data
        super().__init__(self._format())

    def _format(self) -> str:
        if self.kind == self.DEMAND_LENGTH_MISMATCH:
            return (
                f"Demand length mismatch: expected {self.data['expected']}, "
                f"found {self.data['found']}"
            )
        if self.kind == self.UNBALANCED_DEMAND:
            return f"Unbalanced demand sum: {self.data['sum']} (must be 0)"
        if self.kind == self.NEGATIVE_WEIGHT:
            return (
                f"Negative edge weight for edge {self.data['edge']}: "
                f"{self.data['weight']}"
            )
        if self.kind == self.ITERATION_LIMIT_EXCEEDED:
            return f"Iteration limit exceeded: {self.data['limit']}"
        if self.kind == self.INVALID_CARRIER:
            return f"Invalid carrier: {self.data.get('message', '')}"
        if self.kind == self.UNSUPPORTED_ARC_BOUNDS:
            return f"Unsupported arc bounds: {self.data.get('message', '')}"
        return self.kind

    @classmethod
    def empty_graph(cls):
        return cls(cls.EMPTY_GRAPH)

    @classmethod
    def invalid_carrier(cls, message: str):
        return cls(cls.INVALID_CARRIER, message=message)

    @classmethod
    def demand_length_mismatch(cls, expected: int, found: int):
        return cls(cls.DEMAND_LENGTH_MISMATCH, expected=expected, found=found)

    @classmethod
    def unbalanced_demand(cls, sum: int):
        return cls(cls.UNBALANCED_DEMAND, sum=sum)

    @classmethod
    def negative_weight(cls, edge: int, weight: int):
        return cls(cls.NEGATIVE_WEIGHT, edge=edge, weight=weight)

    @classmethod
    def infeasible(cls):
        return cls(cls.INFEASIBLE)

    @classmethod
    def iteration_limit_exceeded(cls, limit: int):
        return cls(cls.ITERATION_LIMIT_EXCEEDED, limit=limit)

    @classmethod
    def invalid_basis(cls):
        return cls(cls.INVALID_BASIS)

    @classmethod
    def arithmetic_overflow(cls):
        return cls(cls.ARITHMETIC_OVERFLOW)

    @classmethod
    def unsupported_arc_bounds(cls, message: str):
        return cls(cls.UNSUPPORTED_ARC_BOUNDS, message=message)

    def __eq__(self, other):
        return (
            isinstance(other, NetworkSimplexError)
            and self.kind == other.kind
            and self.data == other.data
        )

    def __hash__(self):
        return hash((self.kind, tuple(sorted(self.data.items()))))

