from __future__ import annotations
"""
Executable Python dual harness for W6.23 (completeness as audit).

Mirrors Lean `003_qm_import_completeness_audit.lean`:

1. Audit inventory of 17 entries covering W6.19–W6.22 skeleton + full-ops
   packages + residual gaps + B5/sealed handoff markers.
2. Mechanized card = 11; residual open card = 6.
3. A-SUF-FULL-OPS and A-MIN-FULL-OPS are mechanized (W6.21 / W6.22 residual).
4. A-IND-B5-PROV, A-RES-SEALED-SUF, A-RES-SEALED-REC are ResidualOpen
   (not Mechanized seal; A1 handoff design markers).
5. A-RES-T / A-RES-N / A-RES-COUPLED remain ResidualOpen.
6. Universal completeness claim refused; Wave-6 exit not claimed.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


class AuditId(str, Enum):
    A_IND_PKG = "A-IND-PKG"
    A_IND_DROP = "A-IND-DROP"
    A_IND_FENCE = "A-IND-FENCE"
    A_NEC_PKG = "A-NEC-PKG"
    A_NEC_PURE = "A-NEC-PURE"
    A_SUF_PKG = "A-SUF-PKG"
    A_SUF_MAP = "A-SUF-MAP"
    A_SUF_FULL_OPS = "A-SUF-FULL-OPS"
    A_MIN_PKG = "A-MIN-PKG"
    A_MIN_PATH = "A-MIN-PATH"
    A_MIN_FULL_OPS = "A-MIN-FULL-OPS"
    A_RES_T = "A-RES-T"
    A_RES_N = "A-RES-N"
    A_RES_COUPLED = "A-RES-COUPLED"
    A_IND_B5_PROV = "A-IND-B5-PROV"
    A_RES_SEALED_SUF = "A-RES-SEALED-SUF"
    A_RES_SEALED_REC = "A-RES-SEALED-REC"


class AuditClass(str, Enum):
    Mechanized = "Mechanized"
    ResidualOpen = "ResidualOpen"


AUDIT_ENTRIES = (
    AuditId.A_IND_PKG,
    AuditId.A_IND_DROP,
    AuditId.A_IND_FENCE,
    AuditId.A_NEC_PKG,
    AuditId.A_NEC_PURE,
    AuditId.A_SUF_PKG,
    AuditId.A_SUF_MAP,
    AuditId.A_SUF_FULL_OPS,
    AuditId.A_MIN_PKG,
    AuditId.A_MIN_PATH,
    AuditId.A_MIN_FULL_OPS,
    AuditId.A_RES_T,
    AuditId.A_RES_N,
    AuditId.A_RES_COUPLED,
    AuditId.A_IND_B5_PROV,
    AuditId.A_RES_SEALED_SUF,
    AuditId.A_RES_SEALED_REC,
)

MECHANIZED = {
    AuditId.A_IND_PKG,
    AuditId.A_IND_DROP,
    AuditId.A_IND_FENCE,
    AuditId.A_NEC_PKG,
    AuditId.A_NEC_PURE,
    AuditId.A_SUF_PKG,
    AuditId.A_SUF_MAP,
    AuditId.A_SUF_FULL_OPS,
    AuditId.A_MIN_PKG,
    AuditId.A_MIN_PATH,
    AuditId.A_MIN_FULL_OPS,
}

RESIDUAL = {
    AuditId.A_RES_T,
    AuditId.A_RES_N,
    AuditId.A_RES_COUPLED,
    AuditId.A_IND_B5_PROV,
    AuditId.A_RES_SEALED_SUF,
    AuditId.A_RES_SEALED_REC,
}

PACKAGE_IDS = (
    AuditId.A_IND_PKG,
    AuditId.A_NEC_PKG,
    AuditId.A_SUF_PKG,
    AuditId.A_MIN_PKG,
    AuditId.A_SUF_FULL_OPS,
    AuditId.A_MIN_FULL_OPS,
)

WAVE_OF = {
    AuditId.A_IND_PKG: "W619",
    AuditId.A_IND_DROP: "W619",
    AuditId.A_IND_FENCE: "W619",
    AuditId.A_NEC_PKG: "W620",
    AuditId.A_NEC_PURE: "W620",
    AuditId.A_SUF_PKG: "W621",
    AuditId.A_SUF_MAP: "W621",
    AuditId.A_SUF_FULL_OPS: "W621",
    AuditId.A_MIN_PKG: "W622",
    AuditId.A_MIN_PATH: "W622",
    AuditId.A_MIN_FULL_OPS: "W622",
    AuditId.A_RES_T: "Residual",
    AuditId.A_RES_N: "Residual",
    AuditId.A_RES_COUPLED: "Residual",
    AuditId.A_IND_B5_PROV: "Residual",
    AuditId.A_RES_SEALED_SUF: "Residual",
    AuditId.A_RES_SEALED_REC: "Residual",
}


def audit_class(a: AuditId) -> AuditClass:
    if a in MECHANIZED:
        return AuditClass.Mechanized
    return AuditClass.ResidualOpen


def test_audit_entries_card():
    assert len(AUDIT_ENTRIES) == 17
    assert len(set(AUDIT_ENTRIES)) == 17


def test_mechanized_audit_card():
    mech = [a for a in AUDIT_ENTRIES if audit_class(a) is AuditClass.Mechanized]
    assert len(mech) == 11


def test_residual_audit_card():
    res = [a for a in AUDIT_ENTRIES if audit_class(a) is AuditClass.ResidualOpen]
    assert len(res) == 6
    assert set(res) == RESIDUAL


def test_packages_audited():
    assert len(PACKAGE_IDS) == 6
    for a in PACKAGE_IDS:
        assert a in AUDIT_ENTRIES
        assert audit_class(a) is AuditClass.Mechanized


def test_full_ops_packages_mechanized():
    assert audit_class(AuditId.A_SUF_FULL_OPS) is AuditClass.Mechanized
    assert audit_class(AuditId.A_MIN_FULL_OPS) is AuditClass.Mechanized
    assert AuditId.A_SUF_FULL_OPS in AUDIT_ENTRIES
    assert AuditId.A_MIN_FULL_OPS in AUDIT_ENTRIES


def test_residual_rows_still_open():
    for a in (
        AuditId.A_RES_T,
        AuditId.A_RES_N,
        AuditId.A_RES_COUPLED,
    ):
        assert audit_class(a) is AuditClass.ResidualOpen


def test_b5_prov_independence_residual_open():
    assert audit_class(AuditId.A_IND_B5_PROV) is AuditClass.ResidualOpen
    assert AuditId.A_IND_B5_PROV in AUDIT_ENTRIES
    herm_in_b4_audit = False
    assert herm_in_b4_audit is False


def test_sealed_handoff_markers_residual_open():
    assert audit_class(AuditId.A_RES_SEALED_SUF) is AuditClass.ResidualOpen
    assert audit_class(AuditId.A_RES_SEALED_REC) is AuditClass.ResidualOpen
    assert AuditId.A_RES_SEALED_SUF in AUDIT_ENTRIES
    assert AuditId.A_RES_SEALED_REC in AUDIT_ENTRIES


def test_wave_cover_independence_block():
    assert WAVE_OF[AuditId.A_IND_PKG] == "W619"
    assert WAVE_OF[AuditId.A_NEC_PKG] == "W620"
    assert WAVE_OF[AuditId.A_SUF_PKG] == "W621"
    assert WAVE_OF[AuditId.A_SUF_FULL_OPS] == "W621"
    assert WAVE_OF[AuditId.A_MIN_PKG] == "W622"
    assert WAVE_OF[AuditId.A_MIN_FULL_OPS] == "W622"
    assert WAVE_OF[AuditId.A_IND_B5_PROV] == "Residual"
    assert WAVE_OF[AuditId.A_RES_SEALED_SUF] == "Residual"
    assert WAVE_OF[AuditId.A_RES_SEALED_REC] == "Residual"


def test_universal_completeness_refused():
    universal_completeness_claim = False
    assert universal_completeness_claim is False


def test_wave6_exit_not_claimed():
    wave6_exit_claimed = False
    assert wave6_exit_claimed is False


def test_wave7_exit_not_claimed():
    wave7_exit_claimed = False
    assert wave7_exit_claimed is False




@dataclass(frozen=True)
class Wave6ExitCriteria:
    full_basis_independence_sealed: bool
    sealed_sufficiency: bool
    sealed_minimality: bool
    universal_completeness: bool
    operator_ack: bool


@dataclass(frozen=True)
class Wave7ExitCriteria:
    rec_full_theorem: bool
    gleason_abs: bool
    lab_falsifier_closed: bool
    operator_ack: bool


WAVE6_EXIT_CRITERIA = Wave6ExitCriteria(
    full_basis_independence_sealed=False,
    sealed_sufficiency=False,
    sealed_minimality=False,
    universal_completeness=False,
    operator_ack=False,
)

WAVE7_EXIT_CRITERIA = Wave7ExitCriteria(
    rec_full_theorem=False,
    gleason_abs=False,
    lab_falsifier_closed=False,
    operator_ack=False,
)


def test_wave6_exit_criteria_all_unmet():
    c = WAVE6_EXIT_CRITERIA
    assert c.full_basis_independence_sealed is False
    assert c.sealed_sufficiency is False
    assert c.sealed_minimality is False
    assert c.universal_completeness is False
    assert c.operator_ack is False


def test_wave7_exit_criteria_all_unmet():
    c = WAVE7_EXIT_CRITERIA
    assert c.rec_full_theorem is False
    assert c.gleason_abs is False
    assert c.lab_falsifier_closed is False
    assert c.operator_ack is False
    assert audit_class(AuditId.A_RES_SEALED_REC) is AuditClass.ResidualOpen


def test_wave_exit_criteria_package():
    assert WAVE6_EXIT_CRITERIA.operator_ack is False
    assert WAVE7_EXIT_CRITERIA.operator_ack is False
    assert WAVE6_EXIT_CRITERIA.sealed_sufficiency is False
    assert WAVE7_EXIT_CRITERIA.rec_full_theorem is False
    assert audit_class(AuditId.A_RES_SEALED_SUF) is AuditClass.ResidualOpen
    assert audit_class(AuditId.A_RES_SEALED_REC) is AuditClass.ResidualOpen


def test_import_completeness_audit_package():
    assert len(AUDIT_ENTRIES) == 17
    assert len(MECHANIZED) == 11
    assert len(RESIDUAL) == 6
    assert all(a in AUDIT_ENTRIES for a in PACKAGE_IDS)
    assert audit_class(AuditId.A_SUF_FULL_OPS) is AuditClass.Mechanized
    assert audit_class(AuditId.A_MIN_FULL_OPS) is AuditClass.Mechanized
    assert audit_class(AuditId.A_IND_B5_PROV) is AuditClass.ResidualOpen
    assert audit_class(AuditId.A_RES_SEALED_SUF) is AuditClass.ResidualOpen
    assert audit_class(AuditId.A_RES_SEALED_REC) is AuditClass.ResidualOpen
    for a in (AuditId.A_RES_T, AuditId.A_RES_N, AuditId.A_RES_COUPLED):
        assert audit_class(a) is AuditClass.ResidualOpen
    herm_in_b4_audit = False
    assert herm_in_b4_audit is False
    assert WAVE6_EXIT_CRITERIA.sealed_sufficiency is False
    assert WAVE7_EXIT_CRITERIA.rec_full_theorem is False


if __name__ == "__main__":
    pytest.main([__file__])
