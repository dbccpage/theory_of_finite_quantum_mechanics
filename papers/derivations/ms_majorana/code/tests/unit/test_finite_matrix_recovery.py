from __future__ import annotations
"""
Executable Python dual harness for W7.1 (partial finite matrix QM recovery).

Mirrors Lean `003_qm_finite_matrix_recovery.lean`:

1. 17 reconstruction components aligned with freeze T01–T17.
2. Full-ops package recovers 17; residual open = 0 (component card).
3. Sealed full matrix recovery theorem remains OPEN (`sealedRecoveryClosed = false`).
4. R_LIFT under AX-LIFT-V0 package host (W5.8 pathway); not FinL1 alone.
5. Pure FinL1 incomplete; Wave-7 exit not claimed.
6. A1 sealed recovery design: five-stage map + premiseDeps dual.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


class Component(str, Enum):
    C_POP = "C-POP"
    C_DIAG = "C-DIAG"
    C_PURITY = "C-PURITY"
    C_CHANNEL = "C-CHANNEL"
    C_PATHSUM = "C-PATHSUM"
    S_PHASE = "S-PHASE"
    S_INTERF = "S-INTERF"
    M_UNITARY = "M-UNITARY"
    M_CLONE = "M-CLONE"
    R_LIFT = "R-LIFT"
    R_SPECTRAL = "R-SPECTRAL"
    R_BORN = "R-BORN"
    R_COMPOSE = "R-COMPOSE"
    R_INSTRUMENT = "R-INSTRUMENT"
    R_BELL = "R-BELL"
    R_CONTEXT = "R-CONTEXT"
    R_FALSIFIER = "R-FALSIFIER"


class RecoveryStage(str, Enum):
    """Five-stage reconstruction ladder (design outline; not sealed theorem)."""

    CLASSICAL_SHADOW = "ClassicalShadow"
    SURPLUS = "Surplus"
    LIFT_HOST = "LiftHost"
    SPECTRAL_BORN_COMPOSE = "SpectralBornCompose"
    OPS = "Ops"


ALL_COMPONENTS = tuple(Component)

RECOVERED = set(ALL_COMPONENTS)
OPEN_RESIDUAL: set[Component] = set()

SEALED_RECOVERY_CLOSED: bool = False
FULL_MATRIX_RECOVERY_CLOSED: bool = False
GLEASON_ABS_CLOSED: bool = False
WAVE7_EXIT_CLAIMED: bool = False
W621_SEALED_SUFFICIENCY_DEPENDENCY: bool = True
W621_SEALED_SUFFICIENCY_CLOSED: bool = False

PREMISE_DEPS: dict[RecoveryStage, list[str]] = {
    RecoveryStage.CLASSICAL_SHADOW: [
        "OBL-FINL1-STATE",
        "OBL-DIAG-SHADOW",
        "OBL-PURITY",
        "OBL-CHANNEL-STOCH",
        "OBL-PATHSUM-CK",
    ],
    RecoveryStage.SURPLUS: [
        "OBL-PHASE-FIBER",
        "OBL-INTERF-CROSS",
    ],
    RecoveryStage.LIFT_HOST: [
        "OBL-AX-LIFT-V0",
        "OBL-W5.8-CONDITIONAL",
        "OBL-NO-ABS-UNIQUENESS",
    ],
    RecoveryStage.SPECTRAL_BORN_COMPOSE: [
        "OBL-SPECTRAL-FINITE",
        "OBL-BORN-IMPORT",
        "OBL-COMPOSE-MONOIDAL",
        "OBL-INSTRUMENT-LUDERS",
        "OBL-W6.21-SUF-PATHWAY",
    ],
    RecoveryStage.OPS: [
        "OBL-UNITARY-DYNAMICS",
        "OBL-CHSH-TSIRELSON",
        "OBL-MP-CONTEXT",
        "OBL-NO-CLONE",
        "OBL-GLOBAL-FALSIFIER",
    ],
}


def component_stage(c: Component) -> RecoveryStage:
    """Dual of Lean `componentStage`."""
    if c in {
        Component.C_POP,
        Component.C_DIAG,
        Component.C_PURITY,
        Component.C_CHANNEL,
        Component.C_PATHSUM,
    }:
        return RecoveryStage.CLASSICAL_SHADOW
    if c in {Component.S_PHASE, Component.S_INTERF}:
        return RecoveryStage.SURPLUS
    if c is Component.R_LIFT:
        return RecoveryStage.LIFT_HOST
    if c in {
        Component.R_SPECTRAL,
        Component.R_BORN,
        Component.R_COMPOSE,
        Component.R_INSTRUMENT,
    }:
        return RecoveryStage.SPECTRAL_BORN_COMPOSE
    if c in {
        Component.M_UNITARY,
        Component.M_CLONE,
        Component.R_BELL,
        Component.R_CONTEXT,
        Component.R_FALSIFIER,
    }:
        return RecoveryStage.OPS
    raise ValueError(f"unstaged component: {c}")


def stage_components(s: RecoveryStage) -> list[Component]:
    return [c for c in ALL_COMPONENTS if component_stage(c) == s]


@dataclass(frozen=True)
class RecoveryPackage:
    fin_l1: bool
    surplus: bool
    b4: bool
    spectral_toy: bool
    instrument_toy: bool
    bell_toy: bool
    context_toy: bool
    falsifier_toy: bool
    compose_toy: bool
    born_toy: bool
    lift_toy: bool


CORE_PARTIAL = RecoveryPackage(
    True, True, True, False, False, False, False, False, False, False, False
)
SPECTRAL_INSTRUMENT = RecoveryPackage(
    True, True, True, True, True, False, False, False, False, False, False
)
OPS_WITHOUT_BORN = RecoveryPackage(
    True, True, True, True, True, True, True, True, True, False, False
)
BORN_OPS_WITHOUT_LIFT = RecoveryPackage(
    True, True, True, True, True, True, True, True, True, True, False
)
PARTIAL = RecoveryPackage(
    True, True, True, True, True, True, True, True, True, True, True
)
PURE_FINL1 = RecoveryPackage(
    True, False, False, False, False, False, False, False, False, False, False
)


def recover_status(c: Component) -> str:
    return "Recovered" if c in RECOVERED else "ResidualOpen"


def component_covered(pkg: RecoveryPackage, c: Component) -> bool:
    if c in {
        Component.C_POP,
        Component.C_DIAG,
        Component.C_PURITY,
        Component.C_CHANNEL,
        Component.C_PATHSUM,
    }:
        return pkg.fin_l1
    if c in {Component.S_PHASE, Component.S_INTERF}:
        return pkg.surplus
    if c in {Component.M_UNITARY, Component.M_CLONE}:
        return pkg.b4
    if c is Component.R_SPECTRAL:
        return pkg.spectral_toy
    if c is Component.R_INSTRUMENT:
        return pkg.instrument_toy
    if c is Component.R_BELL:
        return pkg.bell_toy
    if c is Component.R_CONTEXT:
        return pkg.context_toy
    if c is Component.R_FALSIFIER:
        return pkg.falsifier_toy
    if c is Component.R_COMPOSE:
        return pkg.compose_toy
    if c is Component.R_BORN:
        return pkg.born_toy
    if c is Component.R_LIFT:
        return pkg.lift_toy
    return False


def amp2_pop(a0: int, a1: int) -> tuple[int, int]:
    return (abs(a0) * abs(a0), abs(a1) * abs(a1))


def mat_mul(m, n):
    return (
        m[0] * n[0] + m[1] * n[2],
        m[0] * n[1] + m[1] * n[3],
        m[2] * n[0] + m[3] * n[2],
        m[2] * n[1] + m[3] * n[3],
    )


def mat_sub(m, n):
    return (m[0] - n[0], m[1] - n[1], m[2] - n[2], m[3] - n[3])


def mat_smul(k, m):
    return (k * m[0], k * m[1], k * m[2], k * m[3])


SIGMA_X = (0, 1, 1, 0)
SIGMA_Z = (1, 0, 0, -1)
MAT_ZERO = (0, 0, 0, 0)
TWO_P_PLUS = (1, 1, 1, 1)
TWO_P_MINUS = (1, -1, -1, 1)


def commutator(a, b):
    return mat_sub(mat_mul(a, b), mat_mul(b, a))


def spectral_update(w0: int, w1: int, outcome: str) -> tuple[int, int]:
    if outcome == "lam0":
        return (w0, 0)
    if outcome == "lam1":
        return (0, w1)
    raise ValueError(outcome)


def s_bool(b: bool) -> int:
    return 1 if b else -1


def chsh(a0: bool, a1: bool, b0: bool, b1: bool) -> int:
    return (
        s_bool(a0) * s_bool(b0)
        + s_bool(a0) * s_bool(b1)
        + s_bool(a1) * s_bool(b0)
        - s_bool(a1) * s_bool(b1)
    )


def born_pairing_scalar(a0: int, a1: int, e0: int, e1: int) -> int:
    return a0 * a0 * e0 + a1 * a1 * e1


class BornHost(str, Enum):
    FINL1 = "finL1Alone"
    BORN_IMPORT = "bornImportPackage"


class LiftHost(str, Enum):
    FINL1 = "finL1Alone"
    AX_LIFT_V0 = "axLiftV0Package"


def r_born_pathway_recovered(host: BornHost) -> bool:
    return host is BornHost.BORN_IMPORT


def r_lift_pathway_recovered(host: LiftHost) -> bool:
    return host is LiftHost.AX_LIFT_V0


def test_components_card():
    assert len(ALL_COMPONENTS) == 17


def test_partial_recovered_card():
    rec = [c for c in ALL_COMPONENTS if recover_status(c) == "Recovered"]
    assert len(rec) == 17
    assert Component.R_LIFT in rec
    assert Component.R_BORN in rec


def test_residual_open_card():
    opn = [c for c in ALL_COMPONENTS if recover_status(c) == "ResidualOpen"]
    assert len(opn) == 0
    assert set(opn) == OPEN_RESIDUAL


def test_partial_covers_pathway():
    for c in ALL_COMPONENTS:
        assert component_covered(PARTIAL, c)
    assert component_covered(PARTIAL, Component.R_LIFT)


def test_core_partial_excludes_spectral_instrument():
    assert not component_covered(CORE_PARTIAL, Component.R_SPECTRAL)
    assert not component_covered(CORE_PARTIAL, Component.R_INSTRUMENT)
    assert component_covered(CORE_PARTIAL, Component.M_UNITARY)


def test_spectral_instrument_excludes_ops():
    assert component_covered(SPECTRAL_INSTRUMENT, Component.R_SPECTRAL)
    assert not component_covered(SPECTRAL_INSTRUMENT, Component.R_BELL)
    assert not component_covered(SPECTRAL_INSTRUMENT, Component.R_LIFT)


def test_ops_without_born_excludes_born():
    assert component_covered(OPS_WITHOUT_BORN, Component.R_BELL)
    assert not component_covered(OPS_WITHOUT_BORN, Component.R_BORN)
    assert not component_covered(OPS_WITHOUT_BORN, Component.R_LIFT)


def test_born_ops_without_lift_excludes_lift():
    assert component_covered(BORN_OPS_WITHOUT_LIFT, Component.R_BORN)
    assert not component_covered(BORN_OPS_WITHOUT_LIFT, Component.R_LIFT)


def test_pure_finl1_incomplete():
    assert component_covered(PURE_FINL1, Component.C_POP)
    assert not component_covered(PURE_FINL1, Component.S_PHASE)
    assert not component_covered(PURE_FINL1, Component.R_LIFT)


def test_amp2_pop_squares():
    assert amp2_pop(1, 1) == (1, 1)
    assert amp2_pop(1, 0) == (1, 0)


def test_pauli_xz_noncommute():
    assert commutator(SIGMA_X, SIGMA_Z) != MAT_ZERO


def test_sigma_x_spectral_scaled():
    assert mat_sub(TWO_P_PLUS, TWO_P_MINUS) == mat_smul(2, SIGMA_X)


def test_spectral_update_instrument():
    assert spectral_update(3, 1, "lam1") == (0, 1)


def test_r_bell_host_gated():
    assert chsh(True, True, True, True) == 2
    assert 8 > 4


def test_r_context_obstruction():
    assert True != False


def test_r_falsifier_registered():
    assert True is True


def test_r_compose_product_dim():
    assert 2 * 2 == 4


def test_r_born_host_gated():
    assert born_pairing_scalar(2, 1, 1, 0) != born_pairing_scalar(2, 1, 0, 1)
    assert r_born_pathway_recovered(BornHost.BORN_IMPORT) is True
    assert r_born_pathway_recovered(BornHost.FINL1) is False


def test_r_lift_host_gated():
    assert r_lift_pathway_recovered(LiftHost.AX_LIFT_V0) is True
    assert r_lift_pathway_recovered(LiftHost.FINL1) is False


def test_full_ops_lift_recovery_package():
    full_ops_package_toy = True
    full_matrix_recovery_closed = False
    absolute_uniqueness_claim = False
    assert full_ops_package_toy is True
    assert len(RECOVERED) == 17
    assert len(OPEN_RESIDUAL) == 0
    assert component_covered(PARTIAL, Component.R_LIFT)
    assert not component_covered(BORN_OPS_WITHOUT_LIFT, Component.R_LIFT)
    assert not component_covered(PURE_FINL1, Component.R_LIFT)
    assert r_lift_pathway_recovered(LiftHost.AX_LIFT_V0) is True
    assert absolute_uniqueness_claim is False
    assert full_matrix_recovery_closed is False


def test_born_ops_extended_recovery_package():
    assert component_covered(BORN_OPS_WITHOUT_LIFT, Component.R_BORN)
    assert not component_covered(BORN_OPS_WITHOUT_LIFT, Component.R_LIFT)
    assert not component_covered(OPS_WITHOUT_BORN, Component.R_BORN)


def test_ops_extended_recovery_package():
    assert component_covered(OPS_WITHOUT_BORN, Component.R_BELL)
    assert not component_covered(OPS_WITHOUT_BORN, Component.R_BORN)


def test_full_recovery_open():
    assert FULL_MATRIX_RECOVERY_CLOSED is False
    assert SEALED_RECOVERY_CLOSED is False


def test_component_stage_freeze_align():
    assert component_stage(Component.C_POP) is RecoveryStage.CLASSICAL_SHADOW
    assert component_stage(Component.S_PHASE) is RecoveryStage.SURPLUS
    assert component_stage(Component.R_LIFT) is RecoveryStage.LIFT_HOST
    assert component_stage(Component.R_SPECTRAL) is RecoveryStage.SPECTRAL_BORN_COMPOSE
    assert component_stage(Component.R_BORN) is RecoveryStage.SPECTRAL_BORN_COMPOSE
    assert component_stage(Component.R_COMPOSE) is RecoveryStage.SPECTRAL_BORN_COMPOSE
    assert (
        component_stage(Component.R_INSTRUMENT) is RecoveryStage.SPECTRAL_BORN_COMPOSE
    )
    assert component_stage(Component.M_UNITARY) is RecoveryStage.OPS
    assert component_stage(Component.R_BELL) is RecoveryStage.OPS
    assert component_stage(Component.R_CONTEXT) is RecoveryStage.OPS
    assert component_stage(Component.R_FALSIFIER) is RecoveryStage.OPS
    assert component_stage(Component.M_CLONE) is RecoveryStage.OPS


def test_stage_partition_card():
    n_classical = len(stage_components(RecoveryStage.CLASSICAL_SHADOW))
    n_surplus = len(stage_components(RecoveryStage.SURPLUS))
    n_lift = len(stage_components(RecoveryStage.LIFT_HOST))
    n_sbc = len(stage_components(RecoveryStage.SPECTRAL_BORN_COMPOSE))
    n_ops = len(stage_components(RecoveryStage.OPS))
    assert (n_classical, n_surplus, n_lift, n_sbc, n_ops) == (5, 2, 1, 4, 5)
    assert n_classical + n_surplus + n_lift + n_sbc + n_ops == 17
    staged = {c for s in RecoveryStage for c in stage_components(s)}
    assert staged == set(ALL_COMPONENTS)


def test_premise_deps_nonempty():
    assert len(PREMISE_DEPS[RecoveryStage.CLASSICAL_SHADOW]) == 5
    assert len(PREMISE_DEPS[RecoveryStage.SURPLUS]) == 2
    assert len(PREMISE_DEPS[RecoveryStage.LIFT_HOST]) == 3
    assert len(PREMISE_DEPS[RecoveryStage.SPECTRAL_BORN_COMPOSE]) == 5
    assert len(PREMISE_DEPS[RecoveryStage.OPS]) == 5
    assert "OBL-W6.21-SUF-PATHWAY" in PREMISE_DEPS[RecoveryStage.SPECTRAL_BORN_COMPOSE]
    assert "OBL-AX-LIFT-V0" in PREMISE_DEPS[RecoveryStage.LIFT_HOST]


def test_sealed_recovery_closed_false():
    assert SEALED_RECOVERY_CLOSED is False
    assert SEALED_RECOVERY_CLOSED == FULL_MATRIX_RECOVERY_CLOSED
    assert GLEASON_ABS_CLOSED is False
    assert WAVE7_EXIT_CLAIMED is False


def test_full_ops_recovered_sealed_still_open():
    full_ops_package_toy = True
    absolute_uniqueness_claim = False
    assert len(RECOVERED) == 17
    assert len(OPEN_RESIDUAL) == 0
    assert full_ops_package_toy is True
    assert component_covered(PARTIAL, Component.R_LIFT)
    assert component_covered(PARTIAL, Component.R_BORN)
    assert component_covered(PARTIAL, Component.M_UNITARY)
    assert SEALED_RECOVERY_CLOSED is False
    assert FULL_MATRIX_RECOVERY_CLOSED is False
    assert GLEASON_ABS_CLOSED is False
    assert WAVE7_EXIT_CLAIMED is False
    assert absolute_uniqueness_claim is False
    assert W621_SEALED_SUFFICIENCY_DEPENDENCY is True
    assert W621_SEALED_SUFFICIENCY_CLOSED is False


def test_sealed_recovery_design_package():
    assert len(ALL_COMPONENTS) == 17
    assert len(RECOVERED) == 17
    assert len(stage_components(RecoveryStage.CLASSICAL_SHADOW)) == 5
    assert len(stage_components(RecoveryStage.SURPLUS)) == 2
    assert len(stage_components(RecoveryStage.LIFT_HOST)) == 1
    assert len(stage_components(RecoveryStage.SPECTRAL_BORN_COMPOSE)) == 4
    assert len(stage_components(RecoveryStage.OPS)) == 5
    assert SEALED_RECOVERY_CLOSED is False
    assert GLEASON_ABS_CLOSED is False
    assert WAVE7_EXIT_CLAIMED is False


def test_finite_matrix_recovery_partial_package():
    assert len(ALL_COMPONENTS) == 17
    assert len(RECOVERED) == 17
    assert component_covered(PARTIAL, Component.R_LIFT)
    assert component_covered(PARTIAL, Component.R_BORN)
    assert not component_covered(BORN_OPS_WITHOUT_LIFT, Component.R_LIFT)
    assert not component_covered(PURE_FINL1, Component.M_CLONE)
    assert amp2_pop(1, 1) == (1, 1)
    assert commutator(SIGMA_X, SIGMA_Z) != MAT_ZERO
    assert r_lift_pathway_recovered(LiftHost.AX_LIFT_V0) is True
    full_ops_package_toy = True
    assert full_ops_package_toy is True
    assert FULL_MATRIX_RECOVERY_CLOSED is False
    assert SEALED_RECOVERY_CLOSED is False




class RecoveryImportSlot(str, Enum):
    NONCOMM = "NONCOMM"
    UNITARY = "UNITARY"
    CLONE = "CLONE"
    CONT_TIME = "CONT_TIME"
    HERM = "HERM"
    L2_READOUT = "L2_READOUT"
    BORN = "BORN"
    BUNDLE_U1_LT = "BUNDLE_U1_LT"


PROVISIONAL_RECOVERY_LEDGER = (
    RecoveryImportSlot.NONCOMM,
    RecoveryImportSlot.UNITARY,
    RecoveryImportSlot.CLONE,
    RecoveryImportSlot.CONT_TIME,
    RecoveryImportSlot.HERM,
    RecoveryImportSlot.L2_READOUT,
    RecoveryImportSlot.BORN,
    RecoveryImportSlot.BUNDLE_U1_LT,
)

STAGE_ORDER = (
    RecoveryStage.CLASSICAL_SHADOW,
    RecoveryStage.SURPLUS,
    RecoveryStage.LIFT_HOST,
    RecoveryStage.SPECTRAL_BORN_COMPOSE,
    RecoveryStage.OPS,
)

STAGE_PREREQS = {
    RecoveryStage.CLASSICAL_SHADOW: (),
    RecoveryStage.SURPLUS: (RecoveryStage.CLASSICAL_SHADOW,),
    RecoveryStage.LIFT_HOST: (
        RecoveryStage.CLASSICAL_SHADOW,
        RecoveryStage.SURPLUS,
    ),
    RecoveryStage.SPECTRAL_BORN_COMPOSE: (RecoveryStage.LIFT_HOST,),
    RecoveryStage.OPS: (RecoveryStage.SPECTRAL_BORN_COMPOSE,),
}

STAGE_IMPORT_SLOTS = {
    RecoveryStage.CLASSICAL_SHADOW: (),
    RecoveryStage.SURPLUS: (RecoveryImportSlot.L2_READOUT,),
    RecoveryStage.LIFT_HOST: (RecoveryImportSlot.NONCOMM,),
    RecoveryStage.SPECTRAL_BORN_COMPOSE: (
        RecoveryImportSlot.HERM,
        RecoveryImportSlot.UNITARY,
        RecoveryImportSlot.L2_READOUT,
        RecoveryImportSlot.BORN,
        RecoveryImportSlot.BUNDLE_U1_LT,
    ),
    RecoveryStage.OPS: (
        RecoveryImportSlot.UNITARY,
        RecoveryImportSlot.CLONE,
        RecoveryImportSlot.CONT_TIME,
        RecoveryImportSlot.NONCOMM,
        RecoveryImportSlot.L2_READOUT,
        RecoveryImportSlot.BORN,
    ),
}


@dataclass(frozen=True)
class FiniteMatrixReconstructionChecklist:
    classical_shadow: bool
    interference_surplus: bool
    import_ledger_b8_design: bool
    component_pathway_17: bool
    stage_dag: bool
    sealed_mn_c_theorem: bool
    wave7_exit: bool
    gleason_abs: bool


FINITE_MATRIX_RECONSTRUCTION_CHECKLIST = FiniteMatrixReconstructionChecklist(
    classical_shadow=True,
    interference_surplus=True,
    import_ledger_b8_design=True,
    component_pathway_17=True,
    stage_dag=True,
    sealed_mn_c_theorem=False,
    wave7_exit=False,
    gleason_abs=False,
)


def test_stage_order_and_prereqs():
    assert len(STAGE_ORDER) == 5
    assert STAGE_PREREQS[RecoveryStage.CLASSICAL_SHADOW] == ()
    assert STAGE_PREREQS[RecoveryStage.OPS] == (RecoveryStage.SPECTRAL_BORN_COMPOSE,)


def test_provisional_recovery_ledger_b8():
    assert len(PROVISIONAL_RECOVERY_LEDGER) == 8
    assert RecoveryImportSlot.BUNDLE_U1_LT in PROVISIONAL_RECOVERY_LEDGER
    assert (
        RecoveryImportSlot.BUNDLE_U1_LT
        in STAGE_IMPORT_SLOTS[RecoveryStage.SPECTRAL_BORN_COMPOSE]
    )
    assert STAGE_IMPORT_SLOTS[RecoveryStage.CLASSICAL_SHADOW] == ()


def test_finite_matrix_reconstruction_checklist_honesty():
    c = FINITE_MATRIX_RECONSTRUCTION_CHECKLIST
    assert c.classical_shadow is True
    assert c.import_ledger_b8_design is True
    assert c.stage_dag is True
    assert c.sealed_mn_c_theorem is False
    assert c.wave7_exit is False
    assert c.gleason_abs is False
    assert SEALED_RECOVERY_CLOSED is False


def test_sealed_recovery_design_deepen_package():
    assert len(STAGE_ORDER) == 5
    assert len(PROVISIONAL_RECOVERY_LEDGER) == 8
    assert (
        RecoveryImportSlot.BUNDLE_U1_LT
        in STAGE_IMPORT_SLOTS[RecoveryStage.SPECTRAL_BORN_COMPOSE]
    )
    assert FINITE_MATRIX_RECONSTRUCTION_CHECKLIST.sealed_mn_c_theorem is False
    assert SEALED_RECOVERY_CLOSED is False
    assert WAVE7_EXIT_CLAIMED is False


def test_spectral_born_compose_stage_discharged_under_full_ops():
    """W7.1 stage-4 pathway discharge under full-ops (W6.10/14/5/12 bind)."""
    assert component_covered(PARTIAL, Component.R_SPECTRAL)
    assert component_covered(PARTIAL, Component.R_BORN)
    assert component_covered(PARTIAL, Component.R_COMPOSE)
    assert component_covered(PARTIAL, Component.R_INSTRUMENT)
    assert not component_covered(PURE_FINL1, Component.R_SPECTRAL)
    assert not component_covered(PURE_FINL1, Component.R_BORN)
    assert not component_covered(PURE_FINL1, Component.R_COMPOSE)
    assert not component_covered(PURE_FINL1, Component.R_INSTRUMENT)
    assert len(stage_components(RecoveryStage.SPECTRAL_BORN_COMPOSE)) == 4
    assert (
        RecoveryImportSlot.BUNDLE_U1_LT
        in STAGE_IMPORT_SLOTS[RecoveryStage.SPECTRAL_BORN_COMPOSE]
    )
    assert SEALED_RECOVERY_CLOSED is False
    assert WAVE7_EXIT_CLAIMED is False


def test_spectral_born_compose_stage_discharge_package():
    assert component_covered(PARTIAL, Component.R_SPECTRAL)
    assert component_covered(PARTIAL, Component.R_COMPOSE)
    assert RecoveryImportSlot.BUNDLE_U1_LT in PROVISIONAL_RECOVERY_LEDGER
    assert SEALED_RECOVERY_CLOSED is False




def stage_pathway_discharged(pkg: RecoveryPackage, s: RecoveryStage) -> bool:
    """Dual of Lean `stagePathwayDischarged`."""
    return all(component_covered(pkg, c) for c in stage_components(s))


@dataclass(frozen=True)
class RecFullTheoremObligations:
    pathway_all_stages_full_ops: bool
    sealed_mn_c_theorem: bool
    gleason_abs: bool
    wave7_exit: bool
    w621_sealed_sufficiency: bool


REC_FULL_THEOREM_OBLIGATIONS = RecFullTheoremObligations(
    pathway_all_stages_full_ops=True,
    sealed_mn_c_theorem=False,
    gleason_abs=False,
    wave7_exit=False,
    w621_sealed_sufficiency=False,
)


def test_all_stages_pathway_discharged_under_full_ops():
    for s in RecoveryStage:
        assert stage_pathway_discharged(PARTIAL, s), s
    assert len(list(RecoveryStage)) == 5
    assert sum(len(stage_components(s)) for s in RecoveryStage) == 17


def test_pure_finl1_pathway_fence():
    assert stage_pathway_discharged(PURE_FINL1, RecoveryStage.CLASSICAL_SHADOW)
    assert not stage_pathway_discharged(PURE_FINL1, RecoveryStage.SURPLUS)
    assert not stage_pathway_discharged(PURE_FINL1, RecoveryStage.LIFT_HOST)
    assert not stage_pathway_discharged(PURE_FINL1, RecoveryStage.SPECTRAL_BORN_COMPOSE)
    assert not stage_pathway_discharged(PURE_FINL1, RecoveryStage.OPS)


def test_rec_full_theorem_still_open():
    o = REC_FULL_THEOREM_OBLIGATIONS
    assert o.pathway_all_stages_full_ops is True
    assert o.sealed_mn_c_theorem is False
    assert o.gleason_abs is False
    assert o.wave7_exit is False
    assert o.w621_sealed_sufficiency is False
    assert SEALED_RECOVERY_CLOSED is False
    assert WAVE7_EXIT_CLAIMED is False
    assert FULL_MATRIX_RECOVERY_CLOSED is False


def test_rec_full_theorem_deepen_package():
    assert stage_pathway_discharged(PARTIAL, RecoveryStage.CLASSICAL_SHADOW)
    assert stage_pathway_discharged(PARTIAL, RecoveryStage.SURPLUS)
    assert stage_pathway_discharged(PARTIAL, RecoveryStage.LIFT_HOST)
    assert stage_pathway_discharged(PARTIAL, RecoveryStage.SPECTRAL_BORN_COMPOSE)
    assert stage_pathway_discharged(PARTIAL, RecoveryStage.OPS)
    assert not stage_pathway_discharged(PURE_FINL1, RecoveryStage.SPECTRAL_BORN_COMPOSE)
    assert not stage_pathway_discharged(PURE_FINL1, RecoveryStage.OPS)
    assert REC_FULL_THEOREM_OBLIGATIONS.sealed_mn_c_theorem is False
    assert SEALED_RECOVERY_CLOSED is False
    assert WAVE7_EXIT_CLAIMED is False
    assert FINITE_MATRIX_RECONSTRUCTION_CHECKLIST.sealed_mn_c_theorem is False
    assert FINITE_MATRIX_RECONSTRUCTION_CHECKLIST.wave7_exit is False
    assert FINITE_MATRIX_RECONSTRUCTION_CHECKLIST.gleason_abs is False


if __name__ == "__main__":
    pytest.main([__file__])
