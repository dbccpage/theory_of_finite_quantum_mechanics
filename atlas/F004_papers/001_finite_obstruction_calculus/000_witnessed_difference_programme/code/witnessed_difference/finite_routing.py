"""Finite declared routing contracts. No authority or infinite-limit conclusion."""
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from .obstruction import MatrixQuotientCertificate, verify_matrix_certificate
from .outcomes import Accepted
from .native_functionals import closure


class Refusal(Enum):
    MISSING_POLICY = "missing policy"
    MISSING_CONTRACT = "missing contract"
    INVALID_CONTRACT = "invalid contract"
    NO_DESCENT = "no strict Phi descent"
    DAMAGE = "closure damage exceeded"
    MISSING_STABILITY = "missing fixed-point witness"
    INVALID_STABILITY = "invalid fixed-point witness"


def _shape(matrix, rows, cols):
    return (type(matrix) is tuple and len(matrix) == rows
            and all(type(row) is tuple and len(row) == cols
                    and all(type(x) is Fraction for x in row) for row in matrix))


def _product(a, b, columns):
    return tuple(tuple(sum((aij * b[j][k] for j, aij in enumerate(row)), Fraction(0))
                       for k in range(columns)) for row in a)


def _apply(matrix, vector):
    return tuple(sum((a*b for a, b in zip(row, vector)), Fraction(0)) for row in matrix)


@dataclass(frozen=True)
class Packet:
    certificate: MatrixQuotientCertificate
    d1: tuple

    def __post_init__(self):
        c = self.certificate
        if not isinstance(verify_matrix_certificate(c), Accepted):
            raise ValueError("independent Phi replay failed")
        if not _shape(self.d1, len(self.d1), len(c.delta)):
            raise ValueError("closure shape or scalar")
        if any(x for row in _product(self.d1, c.matrix, c.columns) for x in row):
            raise ValueError("d1 d0 is not zero")

    @property
    def gamma(self):
        c = self.certificate
        return closure(c.matrix, c.columns, self.d1, c.residual)

    @property
    def row(self):
        return 0 if self.certificate.value == 0 else 1 if self.gamma == 0 else 2

    @property
    def dimensions(self):
        return self.certificate.columns, len(self.certificate.delta), len(self.d1)


@dataclass(frozen=True)
class Lift:
    maps: tuple
    coordinate_inclusion: bool = False


def check_lift(source, target, contract):
    if contract is None:
        return Refusal.MISSING_CONTRACT
    if len(contract.maps) != 3 or any(not _shape(m, target.dimensions[i], source.dimensions[i]) for i, m in enumerate(contract.maps)):
        return Refusal.INVALID_CONTRACT
    f0, f1, f2 = contract.maps
    a, b = source.certificate, target.certificate
    if (_product(b.matrix, f0, source.dimensions[0]) != _product(f1, a.matrix, source.dimensions[0])
            or _product(target.d1, f1, source.dimensions[1]) != _product(f2, source.d1, source.dimensions[1])
            or _apply(f1, a.delta) != b.delta):
        return Refusal.INVALID_CONTRACT
    if contract.coordinate_inclusion:
        for degree, m in enumerate(contract.maps):
            occupied = set()
            for j in range(source.dimensions[degree]):
                ones = [i for i, row in enumerate(m) if row[j] == 1]
                if len(ones) != 1 or any(row[j] not in (0, 1) for row in m) or ones[0] in occupied:
                    return Refusal.INVALID_CONTRACT
                occupied.add(ones[0])
    return None


def guarded_edit(before, after, damage_budget):
    if damage_budget is None:
        return Refusal.MISSING_CONTRACT
    a, b = before.certificate, after.certificate
    if (type(damage_budget) is not Fraction or damage_budget < 0
            or (a.matrix, a.columns, a.weights, before.d1) != (b.matrix, b.columns, b.weights, after.d1)):
        return Refusal.INVALID_CONTRACT
    if b.value >= a.value:
        return Refusal.NO_DESCENT
    if after.gamma - before.gamma > damage_budget:
        return Refusal.DAMAGE
    return after


def terminalize(packet, policy, dynamics=None, state=None):
    if policy is None:
        return Refusal.MISSING_POLICY
    if type(policy) is not tuple or len(policy) != 3 or policy[packet.row] is None:
        return Refusal.MISSING_POLICY
    terminal = policy[packet.row]
    if terminal == "Hold" or terminal == ("ExactCertified", "ClosedCertified", "ActiveCertified")[packet.row]:
        return terminal
    if terminal != "StabilizedSurvivor" or packet.row != 1:
        return Refusal.INVALID_CONTRACT
    if dynamics is None:
        return Refusal.MISSING_STABILITY
    packets, next_states = dynamics
    if (not packets or any(not isinstance(p, Packet) for p in packets)
            or len(packets) != len(next_states)
            or any(type(i) is not int or not 0 <= i < len(packets) for i in next_states)
            or type(state) is not int or not 0 <= state < len(packets)
            or packets[state] != packet or next_states[state] != state):
        return Refusal.INVALID_STABILITY
    return terminal
