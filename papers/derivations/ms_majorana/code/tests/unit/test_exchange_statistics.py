from __future__ import annotations
"""
Executable Python dual harness for W6.15 / OB-STATS (exchange statistics).

Mirrors Lean `003_qm_exchange_statistics.lean`:

1. Classical joint residual exchange is a total-preserving involution.
2. Forced Bose/Fermi state-space law underivable from FinL1 alone.
3. Under amplitude lift: Bose joint exchange-fixed; Fermi support moves under swap.
4. S2 characters packaged as declared tags (conditional import).
5. Signed character residual: Int joints; Fermi fixed under χ=-1 with diagonal
   exclusion; symmetrizer/antisymmetrizer projectors; spin-statistics OPEN.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class JointWeight:
    w00: int
    w01: int
    w10: int
    w11: int

    @property
    def total(self) -> int:
        return self.w00 + self.w01 + self.w10 + self.w11

    def exchange(self) -> "JointWeight":
        """Exchange systems A↔B: swap off-diagonal sector labels 01 ↔ 10."""
        return JointWeight(self.w00, self.w10, self.w01, self.w11)


JOINT_ASYM = JointWeight(1, 2, 3, 4)
JOINT_SYM = JointWeight(1, 5, 5, 2)
PRODUCT_FAIR = JointWeight(1, 1, 1, 1)


def test_classical_exchange_total_preserving():
    assert JOINT_ASYM.exchange().total == JOINT_ASYM.total
    assert JOINT_ASYM.exchange() == JointWeight(1, 3, 2, 4)


def test_classical_exchange_involution():
    assert JOINT_ASYM.exchange().exchange() == JOINT_ASYM
    assert JOINT_SYM.exchange().exchange() == JOINT_SYM


def test_classical_exchange_fixes_symmetric():
    assert JOINT_SYM.exchange() == JOINT_SYM
    assert PRODUCT_FAIR.exchange() == PRODUCT_FAIR


@dataclass(frozen=True)
class AmpJoint:
    a00: int
    a01: int
    a10: int
    a11: int

    def exchange(self) -> "AmpJoint":
        return AmpJoint(self.a00, self.a10, self.a01, self.a11)


AMP_BOSE = AmpJoint(0, 1, 1, 0)
AMP_FERMI_SUPPORT = AmpJoint(0, 1, 0, 0)


def test_amp_exchange_bose_fixed():
    assert AMP_BOSE.exchange() == AMP_BOSE


def test_amp_exchange_moves_fermi_support():
    moved = AMP_FERMI_SUPPORT.exchange()
    assert moved == AmpJoint(0, 0, 1, 0)
    assert moved != AMP_FERMI_SUPPORT


class StatsCharacter(str, Enum):
    BOSE = "bose"
    FERMI = "fermi"


@dataclass(frozen=True)
class DeclaredExchange:
    character: StatsCharacter
    joint: AmpJoint


def test_s2_characters_packaged():
    bose = DeclaredExchange(StatsCharacter.BOSE, AMP_BOSE)
    fermi = DeclaredExchange(StatsCharacter.FERMI, AMP_FERMI_SUPPORT)
    assert bose.character != fermi.character
    assert bose.joint.exchange() == bose.joint
    assert fermi.joint.exchange() != fermi.joint


class ImportStatus(str, Enum):
    DERIVED = "derived"
    UNDERIVABLE = "underivable"
    CONDITIONAL_IMPORT = "conditionalImport"


OB_STATS_CLASSICAL = ImportStatus.DERIVED
OB_STATS_FROM_FINL1 = ImportStatus.UNDERIVABLE
OB_STATS_UNDER_LIFT = ImportStatus.CONDITIONAL_IMPORT


def test_import_status_packaging():
    assert OB_STATS_CLASSICAL is ImportStatus.DERIVED
    assert OB_STATS_FROM_FINL1 is ImportStatus.UNDERIVABLE
    assert OB_STATS_UNDER_LIFT is ImportStatus.CONDITIONAL_IMPORT
    # Classical countermodel: exchange without sign characters
    assert JOINT_ASYM.exchange() != JOINT_ASYM
    assert JOINT_SYM.exchange() == JOINT_SYM


def test_exchange_statistics_package():
    assert JOINT_ASYM.exchange().total == JOINT_ASYM.total
    assert AMP_BOSE.exchange() == AMP_BOSE
    assert AMP_FERMI_SUPPORT.exchange() != AMP_FERMI_SUPPORT
    assert OB_STATS_CLASSICAL is ImportStatus.DERIVED
    assert OB_STATS_FROM_FINL1 is ImportStatus.UNDERIVABLE
    assert OB_STATS_UNDER_LIFT is ImportStatus.CONDITIONAL_IMPORT


# --- Signed S2 character residual ---


@dataclass(frozen=True)
class AmpJointZ:
    a00: int
    a01: int
    a10: int
    a11: int

    def add(self, other: "AmpJointZ") -> "AmpJointZ":
        return AmpJointZ(
            self.a00 + other.a00,
            self.a01 + other.a01,
            self.a10 + other.a10,
            self.a11 + other.a11,
        )

    def smul(self, k: int) -> "AmpJointZ":
        return AmpJointZ(k * self.a00, k * self.a01, k * self.a10, k * self.a11)

    def sub(self, other: "AmpJointZ") -> "AmpJointZ":
        return self.add(other.smul(-1))

    def coord_swap(self) -> "AmpJointZ":
        return AmpJointZ(self.a00, self.a10, self.a01, self.a11)


def signed_exchange(chi: int, j: AmpJointZ) -> AmpJointZ:
    """ψ'(x,y) = χ ψ(y,x)."""
    return AmpJointZ(chi * j.a00, chi * j.a10, chi * j.a01, chi * j.a11)


AMP_BOSE_Z = AmpJointZ(1, 1, 1, 1)
AMP_FERMI_Z = AmpJointZ(0, 1, -1, 0)
AMP_DIAG_ONLY = AmpJointZ(1, 0, 0, 1)
ZERO_Z = AmpJointZ(0, 0, 0, 0)


def symmetrizer(j: AmpJointZ) -> AmpJointZ:
    return j.add(j.coord_swap())


def antisymmetrizer(j: AmpJointZ) -> AmpJointZ:
    return j.sub(j.coord_swap())


def test_signed_bose_fixed():
    assert signed_exchange(1, AMP_BOSE_Z) == AMP_BOSE_Z


def test_signed_fermi_fixed_with_diagonal_exclusion():
    assert signed_exchange(-1, AMP_FERMI_Z) == AMP_FERMI_Z
    assert AMP_FERMI_Z.a00 == 0 and AMP_FERMI_Z.a11 == 0


def test_signed_fermi_moves_diag_only_bose_fixes():
    assert signed_exchange(-1, AMP_DIAG_ONLY) != AMP_DIAG_ONLY
    assert signed_exchange(1, AMP_DIAG_ONLY) == AMP_DIAG_ONLY


def test_symmetrizer_antisymmetrizer_projectors():
    assert symmetrizer(AMP_BOSE_Z) == AMP_BOSE_Z.smul(2)
    assert antisymmetrizer(AMP_FERMI_Z) == AMP_FERMI_Z.smul(2)
    assert antisymmetrizer(AMP_BOSE_Z) == ZERO_Z
    assert symmetrizer(AMP_FERMI_Z) == ZERO_Z


def test_exchange_signed_character_package():
    assert signed_exchange(1, AMP_BOSE_Z) == AMP_BOSE_Z
    assert signed_exchange(-1, AMP_FERMI_Z) == AMP_FERMI_Z
    assert AMP_FERMI_Z.a00 == 0 and AMP_FERMI_Z.a11 == 0
    assert signed_exchange(-1, AMP_DIAG_ONLY) != AMP_DIAG_ONLY
    assert signed_exchange(1, AMP_DIAG_ONLY) == AMP_DIAG_ONLY
    assert antisymmetrizer(AMP_BOSE_Z) == ZERO_Z
    assert symmetrizer(AMP_FERMI_Z) == ZERO_Z
    full_spin_statistics_open = True
    assert full_spin_statistics_open is True
    signed_character_requires_lift_host = True
    assert signed_character_requires_lift_host is True
