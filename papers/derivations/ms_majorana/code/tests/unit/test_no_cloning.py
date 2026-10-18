from __future__ import annotations
"""
Executable Python dual harness for W6.18 / OB-CLONE (no-cloning).

Mirrors Lean `003_qm_no_cloning.lean`:

1. Classical residual bit weights admit a distribution-level clone (product copy).
2. Universal no-cloning is therefore not forced by FinL1 alone (classical countermodel).
3. Basis-cloner (CNOT-style) succeeds on computational basis, fails on unnormalized |+⟩.
4. Linear-lift no-cloning is conditional/import; full unitary theorem remains open.
5. Linearity obstruction residual: cloner linear; forced image |00>+|11| ≠ |+>⊗|+>;
   population shadow ≠ independent clone; full unitary OPEN.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class BitWeight:
    w0: int
    w1: int

    @property
    def total(self) -> int:
        return self.w0 + self.w1

    @property
    def is_pure(self) -> bool:
        return (self.w0 > 0 and self.w1 == 0) or (self.w0 == 0 and self.w1 > 0)

    @property
    def is_mixed(self) -> bool:
        return self.w0 > 0 and self.w1 > 0


@dataclass(frozen=True)
class JointWeight:
    w00: int
    w01: int
    w10: int
    w11: int

    @property
    def total(self) -> int:
        return self.w00 + self.w01 + self.w10 + self.w11

    @property
    def marg_a(self) -> BitWeight:
        return BitWeight(self.w00 + self.w01, self.w10 + self.w11)

    @property
    def marg_b(self) -> BitWeight:
        return BitWeight(self.w00 + self.w10, self.w01 + self.w11)


PURE0 = BitWeight(1, 0)
PURE1 = BitWeight(0, 1)
FAIR = BitWeight(1, 1)


def classical_clone(w: BitWeight) -> JointWeight:
    """Independent product clone of a classical residual weight table."""
    return JointWeight(
        w00=w.w0 * w.w0,
        w01=w.w0 * w.w1,
        w10=w.w1 * w.w0,
        w11=w.w1 * w.w1,
    )


def test_classical_clone_marginals_pure0():
    j = classical_clone(PURE0)
    assert j == JointWeight(1, 0, 0, 0)
    assert j.marg_a == BitWeight(PURE0.w0 * PURE0.total, PURE0.w1 * PURE0.total)
    assert j.marg_b == BitWeight(PURE0.w0 * PURE0.total, PURE0.w1 * PURE0.total)


def test_classical_clone_fair_mixed():
    j = classical_clone(FAIR)
    assert FAIR.is_mixed
    assert j == JointWeight(1, 1, 1, 1)
    assert j.total == 4
    assert j.marg_a == BitWeight(2, 2)
    assert j.marg_b == BitWeight(2, 2)


def test_classical_clone_exists_for_all():
    for w in (PURE0, PURE1, FAIR, BitWeight(2, 3)):
        j = classical_clone(w)
        scaled = BitWeight(w.w0 * w.total, w.w1 * w.total)
        assert j.marg_a == scaled
        assert j.marg_b == scaled


@dataclass(frozen=True)
class Amp2:
    a0: int
    a1: int


@dataclass(frozen=True)
class AmpJoint:
    a00: int
    a01: int
    a10: int
    a11: int


AMP0 = Amp2(1, 0)
AMP1 = Amp2(0, 1)
AMP_PLUS = Amp2(1, 1)


def product_amp(a: Amp2, b: Amp2) -> AmpJoint:
    return AmpJoint(
        a00=a.a0 * b.a0,
        a01=a.a0 * b.a1,
        a10=a.a1 * b.a0,
        a11=a.a1 * b.a1,
    )


def basis_cloner(j: AmpJoint) -> AmpJoint:
    """CNOT-style computational-basis copy into blank register (toy total map)."""
    return AmpJoint(
        a00=j.a00,
        a01=j.a01,
        a10=0,
        a11=j.a10 + j.a11,
    )


def test_basis_cloner_ok_on_computational_basis():
    assert basis_cloner(product_amp(AMP0, AMP0)) == product_amp(AMP0, AMP0)
    assert basis_cloner(product_amp(AMP1, AMP0)) == product_amp(AMP1, AMP1)


def test_basis_cloner_fails_on_plus():
    image = basis_cloner(product_amp(AMP_PLUS, AMP0))
    target = product_amp(AMP_PLUS, AMP_PLUS)
    assert image == AmpJoint(1, 0, 0, 1)
    assert target == AmpJoint(1, 1, 1, 1)
    assert image != target


def test_linear_lift_no_clone_witness():
    assert basis_cloner(product_amp(AMP0, AMP0)) == product_amp(AMP0, AMP0)
    assert basis_cloner(product_amp(AMP1, AMP0)) == product_amp(AMP1, AMP1)
    assert basis_cloner(product_amp(AMP_PLUS, AMP0)) != product_amp(AMP_PLUS, AMP_PLUS)


class ImportStatus(str, Enum):
    DERIVED = "derived"
    UNDERIVABLE = "underivable"
    CONDITIONAL_IMPORT = "conditionalImport"


OB_CLONE_CLASSICAL = ImportStatus.DERIVED
OB_CLONE_FROM_FINL1 = ImportStatus.UNDERIVABLE
OB_CLONE_UNDER_LINEAR_LIFT = ImportStatus.CONDITIONAL_IMPORT


def test_import_status_packaging():
    assert OB_CLONE_CLASSICAL is ImportStatus.DERIVED
    assert OB_CLONE_FROM_FINL1 is ImportStatus.UNDERIVABLE
    assert OB_CLONE_UNDER_LINEAR_LIFT is ImportStatus.CONDITIONAL_IMPORT
    # Classical countermodel: FinL1 admits clone ⇒ universal no-cloning not FinL1-forced
    assert classical_clone(FAIR).total == 4


def test_no_cloning_package():
    assert classical_clone(FAIR).total == 4
    assert basis_cloner(product_amp(AMP_PLUS, AMP0)) != product_amp(AMP_PLUS, AMP_PLUS)
    assert OB_CLONE_CLASSICAL is ImportStatus.DERIVED
    assert OB_CLONE_FROM_FINL1 is ImportStatus.UNDERIVABLE
    assert OB_CLONE_UNDER_LINEAR_LIFT is ImportStatus.CONDITIONAL_IMPORT


# --- Linearity obstruction residual ---


def amp_joint_add(j: AmpJoint, k: AmpJoint) -> AmpJoint:
    return AmpJoint(
        a00=j.a00 + k.a00,
        a01=j.a01 + k.a01,
        a10=j.a10 + k.a10,
        a11=j.a11 + k.a11,
    )


def joint_pop(j: AmpJoint) -> JointWeight:
    return JointWeight(j.a00, j.a01, j.a10, j.a11)


def test_plus_blank_splits_as_basis_products():
    left = product_amp(AMP_PLUS, AMP0)
    right = amp_joint_add(product_amp(AMP0, AMP0), product_amp(AMP1, AMP0))
    assert left == right == AmpJoint(1, 0, 1, 0)


def test_basis_cloner_linear():
    j = product_amp(AMP0, AMP0)
    k = product_amp(AMP1, AMP0)
    assert basis_cloner(amp_joint_add(j, k)) == amp_joint_add(
        basis_cloner(j), basis_cloner(k)
    )


def test_linear_forced_image_neq_product_clone():
    forced = amp_joint_add(product_amp(AMP0, AMP0), product_amp(AMP1, AMP1))
    assert forced == AmpJoint(1, 0, 0, 1)
    assert basis_cloner(product_amp(AMP_PLUS, AMP0)) == forced
    assert forced != product_amp(AMP_PLUS, AMP_PLUS)


def test_cloner_pop_neq_independent_clone_pop():
    image_pop = joint_pop(basis_cloner(product_amp(AMP_PLUS, AMP0)))
    ideal_pop = joint_pop(product_amp(AMP_PLUS, AMP_PLUS))
    assert image_pop == JointWeight(1, 0, 0, 1)
    assert ideal_pop == classical_clone(FAIR)
    assert image_pop != ideal_pop


def test_no_cloning_linearity_obstruction_package():
    assert product_amp(AMP_PLUS, AMP0) == amp_joint_add(
        product_amp(AMP0, AMP0), product_amp(AMP1, AMP0)
    )
    forced = amp_joint_add(product_amp(AMP0, AMP0), product_amp(AMP1, AMP1))
    assert basis_cloner(product_amp(AMP_PLUS, AMP0)) == forced
    assert forced != product_amp(AMP_PLUS, AMP_PLUS)
    assert joint_pop(basis_cloner(product_amp(AMP_PLUS, AMP0))) != joint_pop(
        product_amp(AMP_PLUS, AMP_PLUS)
    )
    assert classical_clone(FAIR) == joint_pop(product_amp(AMP_PLUS, AMP_PLUS))
    full_unitary_no_cloning_open = True
    assert full_unitary_no_cloning_open is True
    assert OB_CLONE_UNDER_LINEAR_LIFT is ImportStatus.CONDITIONAL_IMPORT
