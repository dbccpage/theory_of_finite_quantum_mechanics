from __future__ import annotations
"""
Executable Python dual harness for W6.21 (import sufficiency skeleton).

Mirrors Lean `003_qm_import_sufficiency.lean`:

1. Required freeze targets T01–T17 (card 17).
2. Discharge kinds: Classical / Surplus / ImportBoundB4 / ImportBoundExtended.
3. Legacy B4 skeleton covers 9 pathway rows.
4. Full-ops package covers all 17 pathway rows (import-bound extended).
5. Pure FinL1 fails surplus + import-bound rows.
6. Sealed full sufficiency remains OPEN (pathway card ≠ theorem).
7. Sealed design outline A1: premisePackage + lemmaObligations + status
   (PathwayPriced for classical/surplus; SealedOpen for import-bound).

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


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


REQUIRED_TARGETS = tuple(RecoveryTarget)


class DischargeKind(str, Enum):
    ClassicalDerived = "ClassicalDerived"
    SurplusDerived = "SurplusDerived"
    ImportBoundB4 = "ImportBoundB4"
    ImportBoundExtended = "ImportBoundExtended"
    ResidualOpen = "ResidualOpen"


def discharge(t: RecoveryTarget) -> DischargeKind:
    if t in {
        RecoveryTarget.T01,
        RecoveryTarget.T02,
        RecoveryTarget.T03,
        RecoveryTarget.T04,
        RecoveryTarget.T05,
    }:
        return DischargeKind.ClassicalDerived
    if t in {RecoveryTarget.T06, RecoveryTarget.T07}:
        return DischargeKind.SurplusDerived
    if t in {RecoveryTarget.T12, RecoveryTarget.T16}:
        return DischargeKind.ImportBoundB4
    return DischargeKind.ImportBoundExtended


@dataclass(frozen=True)
class SufficiencyPackage:
    fin_l1_classical: bool
    surplus_rung56: bool
    b4_present: bool
    spectral_present: bool
    instrument_present: bool
    compose_present: bool
    born_present: bool
    lift_present: bool
    wave7_ops_present: bool


SKELETON = SufficiencyPackage(
    True, True, True, False, False, False, False, False, False
)
FULL_OPS = SufficiencyPackage(True, True, True, True, True, True, True, True, True)
PURE_FINL1 = SufficiencyPackage(
    True, False, False, False, False, False, False, False, False
)


def pathway_covered(pkg: SufficiencyPackage, t: RecoveryTarget) -> bool:
    kind = discharge(t)
    if kind is DischargeKind.ClassicalDerived:
        return pkg.fin_l1_classical
    if kind is DischargeKind.SurplusDerived:
        return pkg.surplus_rung56
    if kind is DischargeKind.ImportBoundB4:
        return pkg.b4_present
    if kind is DischargeKind.ImportBoundExtended:
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
        return False
    return False


def covered_count(pkg: SufficiencyPackage) -> int:
    return sum(1 for t in REQUIRED_TARGETS if pathway_covered(pkg, t))




class SealedStatus(str, Enum):
    PathwayPriced = "PathwayPriced"
    SealedOpen = "SealedOpen"


@dataclass(frozen=True)
class PremisePackage:
    fin_l1: bool
    surplus: bool
    b4: bool
    extended: bool


@dataclass(frozen=True)
class SealedObligation:
    premise_package: PremisePackage
    lemma_obligations: tuple[str, ...]
    status: SealedStatus


def _pkg(
    fin_l1: bool = True,
    surplus: bool = False,
    b4: bool = False,
    extended: bool = False,
) -> PremisePackage:
    return PremisePackage(fin_l1, surplus, b4, extended)


def sealed_design(t: RecoveryTarget) -> SealedObligation:
    """Mirror Lean `sealedDesign` — design outline, not a sealed theorem."""
    table: dict[RecoveryTarget, SealedObligation] = {
        RecoveryTarget.T01: SealedObligation(
            _pkg(),
            ("FINL1-STATE-PROB", "W2-CLASSICAL-HEART"),
            SealedStatus.PathwayPriced,
        ),
        RecoveryTarget.T02: SealedObligation(
            _pkg(),
            ("FINL1-DIAG-SHADOW", "W2-CLASSICAL-HEART"),
            SealedStatus.PathwayPriced,
        ),
        RecoveryTarget.T03: SealedObligation(
            _pkg(),
            ("FINL1-PURITY-SHADOW",),
            SealedStatus.PathwayPriced,
        ),
        RecoveryTarget.T04: SealedObligation(
            _pkg(),
            ("FINL1-POP-CHANNEL", "W2-STOCH-CK"),
            SealedStatus.PathwayPriced,
        ),
        RecoveryTarget.T05: SealedObligation(
            _pkg(),
            ("FINL1-PATH-SUM", "W2-STOCH-CK"),
            SealedStatus.PathwayPriced,
        ),
        RecoveryTarget.T06: SealedObligation(
            _pkg(surplus=True),
            ("SURPLUS-PHASE-FIBER", "W4-FIN3-SURPLUS"),
            SealedStatus.PathwayPriced,
        ),
        RecoveryTarget.T07: SealedObligation(
            _pkg(surplus=True),
            ("SURPLUS-CROSS-TERM", "W4-FIN3-SURPLUS"),
            SealedStatus.PathwayPriced,
        ),
        RecoveryTarget.T08: SealedObligation(
            _pkg(extended=True),
            ("W5.8-COND-UNIQ", "W5.6-AX-LIFT-V0", "W5.11-LIFT-FENCE"),
            SealedStatus.SealedOpen,
        ),
        RecoveryTarget.T09: SealedObligation(
            _pkg(extended=True),
            ("W6.10-OB-SPECTRAL", "PL-005-1-GENERAL-N"),
            SealedStatus.SealedOpen,
        ),
        RecoveryTarget.T10: SealedObligation(
            _pkg(extended=True),
            ("W6.5-L2-VS-BORN", "OB-BORN-READOUT"),
            SealedStatus.SealedOpen,
        ),
        RecoveryTarget.T11: SealedObligation(
            _pkg(extended=True),
            ("W6.14-COMPOSE-MONOIDAL", "LT-OB-U1-COUPLED"),
            SealedStatus.SealedOpen,
        ),
        RecoveryTarget.T12: SealedObligation(
            _pkg(b4=True),
            ("W6.19-B4-INDEP", "W6.8-UNITARY-NOT-STOCH", "W6.16-TIME-GEN"),
            SealedStatus.SealedOpen,
        ),
        RecoveryTarget.T13: SealedObligation(
            _pkg(extended=True),
            ("W6.12-OB-INSTRUMENT", "W6.17-BACKACTION"),
            SealedStatus.SealedOpen,
        ),
        RecoveryTarget.T14: SealedObligation(
            _pkg(extended=True),
            ("W7.2-TSIRELSON-CHSH", "W5.5-SEP-PRED"),
            SealedStatus.SealedOpen,
        ),
        RecoveryTarget.T15: SealedObligation(
            _pkg(extended=True),
            ("W7.3-MERMIN-PERES", "W6.6-NONCOMM"),
            SealedStatus.SealedOpen,
        ),
        RecoveryTarget.T16: SealedObligation(
            _pkg(b4=True),
            ("W6.19-B4-INDEP", "W6.18-NO-CLONE"),
            SealedStatus.SealedOpen,
        ),
        RecoveryTarget.T17: SealedObligation(
            _pkg(extended=True),
            ("W7.6-GLOBAL-FALSIFIER", "W7.1-FIN-MATRIX"),
            SealedStatus.SealedOpen,
        ),
    }
    return table[t]


SEALED_DESIGN = {t: sealed_design(t) for t in REQUIRED_TARGETS}

FULL_SUFFICIENCY_CLOSED = False
FULL_OPS_SUFFICIENCY_PATHWAY_PACKAGE_TOY = True


def test_required_targets_card():
    assert len(REQUIRED_TARGETS) == 17
    assert len(set(REQUIRED_TARGETS)) == 17


def test_classical_targets_derived():
    for t in (
        RecoveryTarget.T01,
        RecoveryTarget.T02,
        RecoveryTarget.T03,
        RecoveryTarget.T04,
        RecoveryTarget.T05,
    ):
        assert discharge(t) is DischargeKind.ClassicalDerived


def test_surplus_targets_derived():
    assert discharge(RecoveryTarget.T06) is DischargeKind.SurplusDerived
    assert discharge(RecoveryTarget.T07) is DischargeKind.SurplusDerived


def test_import_bound_b4_targets():
    assert discharge(RecoveryTarget.T12) is DischargeKind.ImportBoundB4
    assert discharge(RecoveryTarget.T16) is DischargeKind.ImportBoundB4


def test_import_bound_extended_targets():
    for t in (
        RecoveryTarget.T08,
        RecoveryTarget.T09,
        RecoveryTarget.T10,
        RecoveryTarget.T11,
        RecoveryTarget.T13,
        RecoveryTarget.T14,
        RecoveryTarget.T15,
        RecoveryTarget.T17,
    ):
        assert discharge(t) is DischargeKind.ImportBoundExtended


def test_residual_open_under_map_empty():
    residual = [
        t for t in REQUIRED_TARGETS if discharge(t) is DischargeKind.ResidualOpen
    ]
    assert len(residual) == 0


def test_b4_only_pathway_card():
    pathway = [
        t
        for t in REQUIRED_TARGETS
        if discharge(t)
        in {
            DischargeKind.ClassicalDerived,
            DischargeKind.SurplusDerived,
            DischargeKind.ImportBoundB4,
        }
    ]
    assert len(pathway) == 9


def test_extended_pathway_card():
    pathway = [
        t
        for t in REQUIRED_TARGETS
        if discharge(t)
        in {
            DischargeKind.ClassicalDerived,
            DischargeKind.SurplusDerived,
            DischargeKind.ImportBoundB4,
            DischargeKind.ImportBoundExtended,
        }
    ]
    assert len(pathway) == 17


def test_skeleton_covers_b4_not_extended():
    assert pathway_covered(SKELETON, RecoveryTarget.T12)
    assert pathway_covered(SKELETON, RecoveryTarget.T16)
    assert pathway_covered(SKELETON, RecoveryTarget.T01)
    assert pathway_covered(SKELETON, RecoveryTarget.T07)
    assert not pathway_covered(SKELETON, RecoveryTarget.T08)
    assert not pathway_covered(SKELETON, RecoveryTarget.T10)
    assert not pathway_covered(SKELETON, RecoveryTarget.T14)
    assert not pathway_covered(SKELETON, RecoveryTarget.T17)
    assert covered_count(SKELETON) == 9


def test_full_ops_covers_all_targets():
    for t in REQUIRED_TARGETS:
        assert pathway_covered(FULL_OPS, t)
    assert covered_count(FULL_OPS) == 17


def test_pure_finl1_fails_import_bound_and_surplus():
    assert pathway_covered(PURE_FINL1, RecoveryTarget.T01)
    assert not pathway_covered(PURE_FINL1, RecoveryTarget.T12)
    assert not pathway_covered(PURE_FINL1, RecoveryTarget.T16)
    assert not pathway_covered(PURE_FINL1, RecoveryTarget.T06)
    assert not pathway_covered(PURE_FINL1, RecoveryTarget.T07)
    assert covered_count(PURE_FINL1) == 5


def test_full_sufficiency_open():
    assert FULL_SUFFICIENCY_CLOSED is False


def test_full_ops_sufficiency_pathway_package():
    assert FULL_OPS_SUFFICIENCY_PATHWAY_PACKAGE_TOY is True
    assert covered_count(FULL_OPS) == 17
    assert covered_count(SKELETON) == 9
    assert pathway_covered(FULL_OPS, RecoveryTarget.T08)
    assert pathway_covered(FULL_OPS, RecoveryTarget.T10)
    assert pathway_covered(FULL_OPS, RecoveryTarget.T17)
    assert not pathway_covered(SKELETON, RecoveryTarget.T08)
    assert not pathway_covered(PURE_FINL1, RecoveryTarget.T12)
    assert FULL_SUFFICIENCY_CLOSED is False


def test_import_sufficiency_skeleton_package():
    assert len(REQUIRED_TARGETS) == 17
    assert discharge(RecoveryTarget.T10) is DischargeKind.ImportBoundExtended
    assert pathway_covered(SKELETON, RecoveryTarget.T12)
    assert pathway_covered(FULL_OPS, RecoveryTarget.T17)
    assert not pathway_covered(PURE_FINL1, RecoveryTarget.T12)
    assert FULL_SUFFICIENCY_CLOSED is False
    assert sealed_design(RecoveryTarget.T08).status is SealedStatus.SealedOpen


def test_sealed_design_statuses_partition():
    pathway_priced = [
        t
        for t in REQUIRED_TARGETS
        if sealed_design(t).status is SealedStatus.PathwayPriced
    ]
    sealed_open = [
        t
        for t in REQUIRED_TARGETS
        if sealed_design(t).status is SealedStatus.SealedOpen
    ]
    assert len(pathway_priced) == 7
    assert len(sealed_open) == 10
    assert len(pathway_priced) + len(sealed_open) == 17
    assert set(pathway_priced) | set(sealed_open) == set(REQUIRED_TARGETS)


def test_classical_surplus_pathway_priced():
    for t in (
        RecoveryTarget.T01,
        RecoveryTarget.T02,
        RecoveryTarget.T03,
        RecoveryTarget.T04,
        RecoveryTarget.T05,
        RecoveryTarget.T06,
        RecoveryTarget.T07,
    ):
        assert sealed_design(t).status is SealedStatus.PathwayPriced


def test_import_bound_sealed_open():
    for t in (
        RecoveryTarget.T08,
        RecoveryTarget.T09,
        RecoveryTarget.T10,
        RecoveryTarget.T11,
        RecoveryTarget.T12,
        RecoveryTarget.T13,
        RecoveryTarget.T14,
        RecoveryTarget.T15,
        RecoveryTarget.T16,
        RecoveryTarget.T17,
    ):
        assert sealed_design(t).status is SealedStatus.SealedOpen


def test_import_bound_lemma_obligations_nonempty():
    for t in (
        RecoveryTarget.T08,
        RecoveryTarget.T09,
        RecoveryTarget.T10,
        RecoveryTarget.T11,
        RecoveryTarget.T12,
        RecoveryTarget.T13,
        RecoveryTarget.T14,
        RecoveryTarget.T15,
        RecoveryTarget.T16,
        RecoveryTarget.T17,
    ):
        assert len(sealed_design(t).lemma_obligations) > 0


def test_sealed_design_premise_flags():
    assert sealed_design(RecoveryTarget.T06).premise_package.surplus is True
    assert sealed_design(RecoveryTarget.T09).premise_package.extended is True
    assert sealed_design(RecoveryTarget.T12).premise_package.b4 is True
    assert sealed_design(RecoveryTarget.T16).premise_package.b4 is True
    assert sealed_design(RecoveryTarget.T01).premise_package.fin_l1 is True
    assert sealed_design(RecoveryTarget.T01).premise_package.extended is False


def test_sealed_design_key_lemma_ids():
    t08 = sealed_design(RecoveryTarget.T08).lemma_obligations
    t09 = sealed_design(RecoveryTarget.T09).lemma_obligations
    t12 = sealed_design(RecoveryTarget.T12).lemma_obligations
    assert "W5.8-COND-UNIQ" in t08
    assert "W6.10-OB-SPECTRAL" in t09
    assert "W6.19-B4-INDEP" in t12


def test_sealed_sufficiency_design_package():
    """Design statuses + pathway toy + full sufficiency still open."""
    assert len(SEALED_DESIGN) == 17
    assert sealed_design(RecoveryTarget.T01).status is SealedStatus.PathwayPriced
    assert sealed_design(RecoveryTarget.T07).status is SealedStatus.PathwayPriced
    assert sealed_design(RecoveryTarget.T08).status is SealedStatus.SealedOpen
    assert sealed_design(RecoveryTarget.T17).status is SealedStatus.SealedOpen
    assert FULL_OPS_SUFFICIENCY_PATHWAY_PACKAGE_TOY is True
    assert covered_count(FULL_OPS) == 17
    assert FULL_SUFFICIENCY_CLOSED is False




class IndepSlotId(str, Enum):
    NONCOMM = "NONCOMM"
    UNITARY = "UNITARY"
    CLONE = "CLONE"
    CONT_TIME = "CONT_TIME"
    HERM = "HERM"
    L2_READOUT = "L2_READOUT"
    BORN = "BORN"


PROVISIONAL_IMPORT_LEDGER_B7 = (
    IndepSlotId.NONCOMM,
    IndepSlotId.UNITARY,
    IndepSlotId.CLONE,
    IndepSlotId.CONT_TIME,
    IndepSlotId.HERM,
    IndepSlotId.L2_READOUT,
    IndepSlotId.BORN,
)


def required_indep_slots(t: RecoveryTarget) -> tuple[IndepSlotId, ...]:
    table: dict[RecoveryTarget, tuple[IndepSlotId, ...]] = {
        RecoveryTarget.T01: (),
        RecoveryTarget.T02: (),
        RecoveryTarget.T03: (),
        RecoveryTarget.T04: (),
        RecoveryTarget.T05: (),
        RecoveryTarget.T06: (IndepSlotId.L2_READOUT,),
        RecoveryTarget.T07: (IndepSlotId.L2_READOUT,),
        RecoveryTarget.T08: (IndepSlotId.NONCOMM,),
        RecoveryTarget.T09: (IndepSlotId.HERM, IndepSlotId.UNITARY),
        RecoveryTarget.T10: (IndepSlotId.L2_READOUT, IndepSlotId.BORN),
        RecoveryTarget.T11: (),
        RecoveryTarget.T12: (IndepSlotId.UNITARY, IndepSlotId.CONT_TIME),
        RecoveryTarget.T13: (IndepSlotId.NONCOMM,),
        RecoveryTarget.T14: (IndepSlotId.NONCOMM, IndepSlotId.L2_READOUT),
        RecoveryTarget.T15: (IndepSlotId.NONCOMM,),
        RecoveryTarget.T16: (IndepSlotId.CLONE,),
        RecoveryTarget.T17: (
            IndepSlotId.NONCOMM,
            IndepSlotId.L2_READOUT,
            IndepSlotId.BORN,
        ),
    }
    return table[t]


def uses_only_b7_slots(t: RecoveryTarget) -> bool:
    return all(s in PROVISIONAL_IMPORT_LEDGER_B7 for s in required_indep_slots(t))


@dataclass(frozen=True)
class FiniteCalculusClosureChecklist:
    classical_shadow: bool
    interference_surplus: bool
    import_independence_b7: bool
    sufficiency_pathway_17: bool
    sealed_theorem: bool
    wave6_exit: bool


FINITE_CALCULUS_CLOSURE_CHECKLIST = FiniteCalculusClosureChecklist(
    classical_shadow=True,
    interference_surplus=True,
    import_independence_b7=True,
    sufficiency_pathway_17=True,
    sealed_theorem=False,
    wave6_exit=False,
)


def test_provisional_import_ledger_b7_card():
    assert len(PROVISIONAL_IMPORT_LEDGER_B7) == 7
    assert len(set(PROVISIONAL_IMPORT_LEDGER_B7)) == 7


def test_t10_requires_l2_and_born():
    assert required_indep_slots(RecoveryTarget.T10) == (
        IndepSlotId.L2_READOUT,
        IndepSlotId.BORN,
    )


def test_t11_compose_not_on_b7_ledger():
    """Mutation-sensitive: compose/LT stays off B7 (OB-U1 coupled)."""
    assert required_indep_slots(RecoveryTarget.T11) == ()


def test_b7_consumers_use_only_ledger_slots():
    for t in (
        RecoveryTarget.T06,
        RecoveryTarget.T10,
        RecoveryTarget.T12,
        RecoveryTarget.T16,
        RecoveryTarget.T17,
        RecoveryTarget.T11,
    ):
        assert uses_only_b7_slots(t) is True


def test_finite_calculus_closure_checklist_honesty():
    c = FINITE_CALCULUS_CLOSURE_CHECKLIST
    assert c.classical_shadow is True
    assert c.interference_surplus is True
    assert c.import_independence_b7 is True
    assert c.sufficiency_pathway_17 is True
    assert c.sealed_theorem is False
    assert c.wave6_exit is False
    assert FULL_SUFFICIENCY_CLOSED is False


def test_b7_sufficiency_design_handoff_package():
    assert len(PROVISIONAL_IMPORT_LEDGER_B7) == 7
    assert required_indep_slots(RecoveryTarget.T10) == (
        IndepSlotId.L2_READOUT,
        IndepSlotId.BORN,
    )
    assert required_indep_slots(RecoveryTarget.T11) == ()
    assert FINITE_CALCULUS_CLOSURE_CHECKLIST.sealed_theorem is False
    assert FULL_SUFFICIENCY_CLOSED is False
    assert FULL_OPS_SUFFICIENCY_PATHWAY_PACKAGE_TOY is True


if __name__ == "__main__":
    pytest.main([__file__])
