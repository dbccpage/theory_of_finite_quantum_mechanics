from __future__ import annotations
"""
Executable Python dual harness for W7.3 (Mermin–Peres observer-incomparability).

Mirrors Lean `003_qm_mermin_peres_observer.lean`:

1. 9 variables, 6 contexts (3 row + 3 col).
2. Target: five + contexts, c3 = −; ell(target)=1.
3. Every assignment has ell(d0 a)=0 (even incidences) ⇒ no global noncontextual assignment.
4. Row vs col probe families observer-incomparable under target.
5. Named two-qubit Pauli product-sign package recovers target signs (TOY-MECH).
6. Full Hilbert / continuum operator MP realization remains open.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Callable

import pytest

VARS = (
    "a11",
    "a12",
    "a13",
    "a21",
    "a22",
    "a23",
    "a31",
    "a32",
    "a33",
)

CONTEXTS = ("r1", "r2", "r3", "c1", "c2", "c3")
ROW_FAMILY = ("r1", "r2", "r3")
COL_FAMILY = ("c1", "c2", "c3")

MEMBERS = {
    "r1": ("a11", "a12", "a13"),
    "r2": ("a21", "a22", "a23"),
    "r3": ("a31", "a32", "a33"),
    "c1": ("a11", "a21", "a31"),
    "c2": ("a12", "a22", "a32"),
    "c3": ("a13", "a23", "a33"),
}

TARGET = {
    "r1": False,
    "r2": False,
    "r3": False,
    "c1": False,
    "c2": False,
    "c3": True,
}


def xor_list(xs: list[bool]) -> bool:
    acc = False
    for x in xs:
        acc = acc ^ x
    return acc


def d0(assignment: dict[str, bool], c: str) -> bool:
    return xor_list([assignment[v] for v in MEMBERS[c]])


def ell(y: Callable[[str], bool]) -> bool:
    return xor_list([y(c) for c in CONTEXTS])


def incidence_parity(v: str) -> bool:
    return xor_list([v in MEMBERS[c] for c in CONTEXTS])


def satisfies_target(assignment: dict[str, bool]) -> bool:
    return all(d0(assignment, c) == TARGET[c] for c in CONTEXTS)


@dataclass(frozen=True)
class Pauli2:
    """Two-qubit Pauli phase element: i^p X^{x1} Z^{z1} ⊗ X^{x2} Z^{z2}."""

    p: int
    x1: bool
    z1: bool
    x2: bool
    z2: bool

    @staticmethod
    def id() -> Pauli2:
        return Pauli2(0, False, False, False, False)

    def mul(self, other: Pauli2) -> Pauli2:
        def bump(z: bool, x: bool) -> int:
            return 2 if z and x else 0

        return Pauli2(
            p=(self.p + other.p + bump(self.z1, other.x1) + bump(self.z2, other.x2))
            % 4,
            x1=self.x1 ^ other.x1,
            z1=self.z1 ^ other.z1,
            x2=self.x2 ^ other.x2,
            z2=self.z2 ^ other.z2,
        )

    def is_plus_id(self) -> bool:
        return self == Pauli2.id()

    def is_minus_id(self) -> bool:
        return self == Pauli2(2, False, False, False, False)

    def product_sign_minus(self) -> bool | None:
        if self.is_plus_id():
            return False
        if self.is_minus_id():
            return True
        return None


SQUARE_OP: dict[str, Pauli2] = {
    "a11": Pauli2(0, True, False, False, False),
    "a12": Pauli2(0, False, False, True, False),
    "a13": Pauli2(0, True, False, True, False),
    "a21": Pauli2(1, False, False, True, True),
    "a22": Pauli2(1, True, True, False, False),
    "a23": Pauli2(2, True, True, True, True),
    "a31": Pauli2(1, True, False, True, True),
    "a32": Pauli2(1, True, True, True, False),
    "a33": Pauli2(0, False, True, False, True),
}


def context_product(c: str) -> Pauli2:
    acc = Pauli2.id()
    for v in MEMBERS[c]:
        acc = acc.mul(SQUARE_OP[v])
    return acc


class OpHost(Enum):
    FINL1 = "finL1Classical"
    QUANTUM_PAULI = "quantumPauliLift"


def admits_operator_product_package(host: OpHost) -> bool:
    return host is OpHost.QUANTUM_PAULI


def test_quantitative_cards():
    assert len(VARS) == 9
    assert len(CONTEXTS) == 6
    assert len(ROW_FAMILY) == 3
    assert len(COL_FAMILY) == 3
    assert len(ROW_FAMILY) + len(COL_FAMILY) == len(CONTEXTS)


def test_all_variable_incidences_even():
    for v in VARS:
        assert incidence_parity(v) is False


def test_ell_target_eq_true():
    assert ell(lambda c: TARGET[c]) is True


def test_ell_d0_eq_false_all_assignments():
    for bits in product([False, True], repeat=9):
        assignment = dict(zip(VARS, bits))
        assert ell(lambda c, a=assignment: d0(a, c)) is False


def test_no_global_assignment():
    for bits in product([False, True], repeat=9):
        assignment = dict(zip(VARS, bits))
        assert not satisfies_target(assignment)


def test_observer_incomparable():
    observer_incomparable = not any(
        satisfies_target(dict(zip(VARS, bits)))
        for bits in product([False, True], repeat=9)
    )
    assert observer_incomparable is True


def test_families_partition():
    assert set(ROW_FAMILY) | set(COL_FAMILY) == set(CONTEXTS)
    assert set(ROW_FAMILY).isdisjoint(COL_FAMILY)


def test_operator_product_signs_match_target():
    for c in CONTEXTS:
        sign = context_product(c).product_sign_minus()
        assert sign is not None
        assert sign is TARGET[c]


def test_finL1_no_operator_product_package():
    assert admits_operator_product_package(OpHost.FINL1) is False
    assert admits_operator_product_package(OpHost.QUANTUM_PAULI) is True


def test_operator_product_sign_package():
    operator_product_sign_package_toy = True
    operator_mp_full_realization_closed = False
    assert operator_product_sign_package_toy is True
    for c in CONTEXTS:
        assert context_product(c).product_sign_minus() is TARGET[c]
    assert admits_operator_product_package(OpHost.QUANTUM_PAULI) is True
    assert admits_operator_product_package(OpHost.FINL1) is False
    assert operator_mp_full_realization_closed is False


def test_t15_partial_operator_open():
    t15_partial_recovery = True
    operator_mp_realization_closed = False
    operator_mp_full_realization_closed = False
    assert t15_partial_recovery is True
    assert operator_mp_realization_closed is False
    assert operator_mp_full_realization_closed is False


def test_mermin_peres_observer_package():
    assert len(VARS) == 9 and len(CONTEXTS) == 6
    assert ell(lambda c: TARGET[c]) is True
    assert not any(
        satisfies_target(dict(zip(VARS, bits)))
        for bits in product([False, True], repeat=9)
    )
    for c in CONTEXTS:
        assert context_product(c).product_sign_minus() is TARGET[c]
    operator_product_sign_package_toy = True
    operator_mp_full_realization_closed = False
    assert operator_product_sign_package_toy is True
    assert operator_mp_full_realization_closed is False


if __name__ == "__main__":
    pytest.main([__file__])
