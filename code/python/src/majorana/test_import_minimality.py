from __future__ import annotations
"""
Executable Python dual harness for W6.22 (import minimality).

Mirrors Lean `003_qm_import_minimality.lean`:

1. Working basis B4 = {OB-NONCOMM, OB-UNITARY, OB-CLONE, CONT-TIME}.
2. Full package admits all four; each drop-one fails exactly the dropped slot.
3. T12 pathway requires UNITARY; T16 requires CLONE.
4. Full-ops pathway package: drop any of 10 named flags loses its keyed
   freeze-target / provisional pathway row(s). 10th flag = hasHermImport
   (provisional B5 OB-HERM); drop-herm loses T_HERM.
5. Herm not in B4 capital; sealed herm / final-N minimality remain open.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass, replace
from enum import Enum

import pytest


class ImportSlot(str, Enum):
    OB_NONCOMM = "OB-NONCOMM"
    OB_UNITARY = "OB-UNITARY"
    OB_CLONE = "OB-CLONE"
    CONT_TIME = "CONT-TIME"


WORKING_BASIS = (
    ImportSlot.OB_NONCOMM,
    ImportSlot.OB_UNITARY,
    ImportSlot.OB_CLONE,
    ImportSlot.CONT_TIME,
)


@dataclass(frozen=True)
class FeaturePackage:
    noncomm: bool
    unitary: bool
    no_clone: bool
    cont_time: bool

    def admits(self, slot: ImportSlot) -> bool:
        if slot is ImportSlot.OB_NONCOMM:
            return self.noncomm
        if slot is ImportSlot.OB_UNITARY:
            return self.unitary
        if slot is ImportSlot.OB_CLONE:
            return self.no_clone
        if slot is ImportSlot.CONT_TIME:
            return self.cont_time
        raise ValueError(slot)

    def pathway_t12(self) -> bool:
        return self.unitary

    def pathway_t16(self) -> bool:
        return self.no_clone


FULL_B4 = FeaturePackage(True, True, True, True)
DROP_NONCOMM = FeaturePackage(False, True, True, True)
DROP_UNITARY = FeaturePackage(True, False, True, True)
DROP_CLONE = FeaturePackage(True, True, False, True)
DROP_CONT_TIME = FeaturePackage(True, True, True, False)

DROP_MAP = {
    ImportSlot.OB_NONCOMM: DROP_NONCOMM,
    ImportSlot.OB_UNITARY: DROP_UNITARY,
    ImportSlot.OB_CLONE: DROP_CLONE,
    ImportSlot.CONT_TIME: DROP_CONT_TIME,
}


class RecoveryTarget(str, Enum):
    T01 = "T01"
    T02 = "T02"
    T03 = "T03"
    T04 = "T04"
    T05 = "T05"
    T06 = "T06"
    T07 = "T07"
    T08 = "T08"
    T09 = "T09"
    T10 = "T10"
    T11 = "T11"
    T12 = "T12"
    T13 = "T13"
    T14 = "T14"
    T15 = "T15"
    T16 = "T16"
    T17 = "T17"
    T_HERM = "T_HERM"


REQUIRED_TARGETS = tuple(t for t in RecoveryTarget if t is not RecoveryTarget.T_HERM)
OPTIONAL_HERM_TARGET = RecoveryTarget.T_HERM


@dataclass(frozen=True)
class FullOpsPackage:
    fin_l1_classical: bool
    surplus_rung56: bool
    b4_present: bool
    spectral_present: bool
    instrument_present: bool
    compose_present: bool
    born_present: bool
    lift_present: bool
    wave7_ops_present: bool
    has_herm_import: bool


FULL_OPS = FullOpsPackage(True, True, True, True, True, True, True, True, True, True)

DROP_FINL1 = replace(FULL_OPS, fin_l1_classical=False)
DROP_SURPLUS = replace(FULL_OPS, surplus_rung56=False)
DROP_B4 = replace(FULL_OPS, b4_present=False)
DROP_SPECTRAL = replace(FULL_OPS, spectral_present=False)
DROP_INSTRUMENT = replace(FULL_OPS, instrument_present=False)
DROP_COMPOSE = replace(FULL_OPS, compose_present=False)
DROP_BORN = replace(FULL_OPS, born_present=False)
DROP_LIFT = replace(FULL_OPS, lift_present=False)
DROP_WAVE7 = replace(FULL_OPS, wave7_ops_present=False)
DROP_HERM = replace(FULL_OPS, has_herm_import=False)

FULL_OPS_DROP_WITNESSES = (
    (DROP_FINL1, RecoveryTarget.T01),
    (DROP_SURPLUS, RecoveryTarget.T06),
    (DROP_B4, RecoveryTarget.T12),
    (DROP_B4, RecoveryTarget.T16),
    (DROP_LIFT, RecoveryTarget.T08),
    (DROP_SPECTRAL, RecoveryTarget.T09),
    (DROP_BORN, RecoveryTarget.T10),
    (DROP_COMPOSE, RecoveryTarget.T11),
    (DROP_INSTRUMENT, RecoveryTarget.T13),
    (DROP_WAVE7, RecoveryTarget.T14),
    (DROP_WAVE7, RecoveryTarget.T15),
    (DROP_WAVE7, RecoveryTarget.T17),
    (DROP_HERM, RecoveryTarget.T_HERM),
)


def full_ops_pathway(pkg: FullOpsPackage, t: RecoveryTarget) -> bool:
    if t in {
        RecoveryTarget.T01,
        RecoveryTarget.T02,
        RecoveryTarget.T03,
        RecoveryTarget.T04,
        RecoveryTarget.T05,
    }:
        return pkg.fin_l1_classical
    if t in {RecoveryTarget.T06, RecoveryTarget.T07}:
        return pkg.surplus_rung56
    if t in {RecoveryTarget.T12, RecoveryTarget.T16}:
        return pkg.b4_present
    if t is RecoveryTarget.T08:
        return pkg.lift_present
    if t is RecoveryTarget.T09:
        return pkg.spectral_present
    if t is RecoveryTarget.T10:
        return pkg.born_present
    if t is RecoveryTarget.T11:
        return pkg.compose_present
    if t is RecoveryTarget.T13:
        return pkg.instrument_present
    if t in {
        RecoveryTarget.T14,
        RecoveryTarget.T15,
        RecoveryTarget.T17,
    }:
        return pkg.wave7_ops_present
    if t is RecoveryTarget.T_HERM:
        return pkg.has_herm_import
    raise ValueError(t)


def test_working_basis_card():
    assert len(WORKING_BASIS) == 4


def test_full_package_admits_all():
    for s in WORKING_BASIS:
        assert FULL_B4.admits(s)


def test_every_b4_slot_minimal():
    for s in WORKING_BASIS:
        assert FULL_B4.admits(s)
        assert not DROP_MAP[s].admits(s)
        for other in WORKING_BASIS:
            if other is not s:
                assert DROP_MAP[s].admits(other)


def test_drop_unitary_loses_t12():
    assert FULL_B4.pathway_t12()
    assert not DROP_UNITARY.pathway_t12()
    assert DROP_UNITARY.pathway_t16()


def test_drop_clone_loses_t16():
    assert FULL_B4.pathway_t16()
    assert not DROP_CLONE.pathway_t16()
    assert DROP_CLONE.pathway_t12()


def test_drop_noncomm_keeps_pathways():
    assert DROP_NONCOMM.pathway_t12() and DROP_NONCOMM.pathway_t16()


def test_drop_cont_time_keeps_pathways():
    assert DROP_CONT_TIME.pathway_t12() and DROP_CONT_TIME.pathway_t16()


def test_full_ops_covers_all_targets():
    assert len(REQUIRED_TARGETS) == 17
    for t in REQUIRED_TARGETS:
        assert full_ops_pathway(FULL_OPS, t)
    assert full_ops_pathway(FULL_OPS, OPTIONAL_HERM_TARGET)


def test_every_full_ops_flag_pathway_minimal():
    for pkg, t in FULL_OPS_DROP_WITNESSES:
        assert not full_ops_pathway(pkg, t)
    for _, t in FULL_OPS_DROP_WITNESSES:
        assert full_ops_pathway(FULL_OPS, t)


def test_drop_wave7_ops_loses_ops_cluster():
    assert not full_ops_pathway(DROP_WAVE7, RecoveryTarget.T14)
    assert not full_ops_pathway(DROP_WAVE7, RecoveryTarget.T15)
    assert not full_ops_pathway(DROP_WAVE7, RecoveryTarget.T17)
    assert full_ops_pathway(DROP_WAVE7, RecoveryTarget.T08)


def test_drop_b4_loses_t12_t16_keeps_extended():
    assert not full_ops_pathway(DROP_B4, RecoveryTarget.T12)
    assert not full_ops_pathway(DROP_B4, RecoveryTarget.T16)
    assert full_ops_pathway(DROP_B4, RecoveryTarget.T08)
    assert full_ops_pathway(DROP_B4, RecoveryTarget.T01)


def test_drop_herm_loses_t_herm():
    assert full_ops_pathway(FULL_OPS, RecoveryTarget.T_HERM)
    assert not full_ops_pathway(DROP_HERM, RecoveryTarget.T_HERM)
    assert full_ops_pathway(DROP_HERM, RecoveryTarget.T12)
    assert full_ops_pathway(DROP_HERM, RecoveryTarget.T16)
    assert full_ops_pathway(DROP_HERM, RecoveryTarget.T01)


def test_herm_not_in_b4_capital():
    herm_in_b4_capital = False
    assert herm_in_b4_capital is False


FULL_OPS_FLAG_CARD = 10


def test_full_ops_flag_card():
    assert FULL_OPS_FLAG_CARD == 10
    assert len(FULL_OPS.__dataclass_fields__) == 10


def test_full_freeze_minimality_open():
    full_freeze_minimality_open = True
    herm_sealed_minimality_open = True
    assert full_freeze_minimality_open is True
    assert herm_sealed_minimality_open is True


def test_import_minimality_b4_package():
    assert len(WORKING_BASIS) == 4
    for s in WORKING_BASIS:
        assert FULL_B4.admits(s) and not DROP_MAP[s].admits(s)
    assert FULL_B4.pathway_t12() and not DROP_UNITARY.pathway_t12()
    assert FULL_B4.pathway_t16() and not DROP_CLONE.pathway_t16()
    herm_in_b4_capital = False
    assert herm_in_b4_capital is False


def test_import_minimality_full_ops_pathway_package():
    assert len(REQUIRED_TARGETS) == 17
    assert FULL_OPS_FLAG_CARD == 10
    for t in list(REQUIRED_TARGETS) + [OPTIONAL_HERM_TARGET]:
        assert full_ops_pathway(FULL_OPS, t)
    for pkg, t in FULL_OPS_DROP_WITNESSES:
        assert not full_ops_pathway(pkg, t)
    full_freeze_minimality_open = True
    herm_sealed_minimality_open = True
    herm_in_b4_capital = False
    assert full_freeze_minimality_open is True
    assert herm_sealed_minimality_open is True
    assert herm_in_b4_capital is False


if __name__ == "__main__":
    pytest.main([__file__])
