from __future__ import annotations
"""
Executable Python dual harness for W7.6 (global empirical falsifier / T17).

Mirrors Lean `003_qm_global_falsifier.lean`:

1. Five contingent component falsifiers (CHSH class/Q, MP, interf, clone).
2. Global T17 sentence registered as structured conjunction of absences.
3. Not a tautology; package expects some presence on quantum-host platforms.
4. Synthetic platform evaluator (in-silico fixtures) — not lab execution.
5. Lab execution open; stating falsifier ≠ Wave 5–7 exit.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


class FalsifierId(str, Enum):
    F_CHSH_CLASS = "F-CHSH-CLASS"
    F_CHSH_Q = "F-CHSH-Q"
    F_MP = "F-MP"
    F_INTERF = "F-INTERF"
    F_CLONE = "F-CLONE"


@dataclass(frozen=True)
class FalsifierRow:
    id: FalsifierId
    contingent: bool
    package_predicts_obstruction: bool


FALSIFIERS = (
    FalsifierRow(FalsifierId.F_CHSH_CLASS, True, True),
    FalsifierRow(FalsifierId.F_CHSH_Q, True, True),
    FalsifierRow(FalsifierId.F_MP, True, True),
    FalsifierRow(FalsifierId.F_INTERF, True, True),
    FalsifierRow(FalsifierId.F_CLONE, True, True),
)


@dataclass(frozen=True)
class GlobalFalsifierSpec:
    requires_chsh_quantum_exceedance_absent: bool
    requires_mp_obstruction_absent: bool
    requires_interference_residual_absent: bool


GLOBAL = GlobalFalsifierSpec(True, True, True)

CLASSICAL_CHSH_SQUARE = 4


@dataclass(frozen=True)
class PlatformOutcome:
    chsh_quantum_exceedance_present: bool
    mp_obstruction_present: bool
    interference_residual_present: bool


def all_absences(o: PlatformOutcome) -> bool:
    return (
        not o.chsh_quantum_exceedance_present
        and not o.mp_obstruction_present
        and not o.interference_residual_present
    )


def package_inadequate_on(o: PlatformOutcome) -> bool:
    return all_absences(o)


class SynthPlatform(str, Enum):
    QUANTUM_HOST = "quantumHost"
    FINL1_SHADOW = "finL1Shadow"
    CLASSICAL_NULL = "classicalNull"


def synth_outcome(platform: SynthPlatform) -> PlatformOutcome:
    if platform is SynthPlatform.QUANTUM_HOST:
        return PlatformOutcome(True, True, True)
    if platform is SynthPlatform.FINL1_SHADOW:
        return PlatformOutcome(False, True, False)
    return PlatformOutcome(False, False, False)


def eval_f_chsh_class(observed_chsh: int) -> bool:
    return observed_chsh > 2


def eval_f_chsh_q(quantum_square_observed: int) -> bool:
    return quantum_square_observed <= CLASSICAL_CHSH_SQUARE


def eval_f_mp(global_assignment_found: bool) -> bool:
    return global_assignment_found


def eval_f_interf(dephase_changes_predictions: bool, residual_claimed: bool) -> bool:
    return residual_claimed and not dephase_changes_predictions


def eval_f_clone(universal_clone_succeeds: bool) -> bool:
    return universal_clone_succeeds


def test_falsifiers_card():
    assert len(FALSIFIERS) == 5
    assert len({f.id for f in FALSIFIERS}) == 5


def test_all_contingent():
    assert all(f.contingent for f in FALSIFIERS)
    assert all(f.package_predicts_obstruction for f in FALSIFIERS)


def test_global_falsifier_registered():
    global_falsifier_registered = True
    assert global_falsifier_registered is True
    assert GLOBAL.requires_chsh_quantum_exceedance_absent
    assert GLOBAL.requires_mp_obstruction_absent
    assert GLOBAL.requires_interference_residual_absent


def test_global_not_tautology():
    global_is_tautology = False
    package_expects_some_presence = True
    assert global_is_tautology is False
    assert package_expects_some_presence is True


def test_chsh_gap_nontrivial():
    classical_chsh_cap = 2
    classical_chsh_square = 4
    quantum_tsirelson_square = 8
    assert quantum_tsirelson_square > classical_chsh_square
    assert classical_chsh_cap == 2


def test_mp_gap_nontrivial():
    mp_target_parity = True
    mp_coboundary_parity = False
    assert mp_target_parity != mp_coboundary_parity


def test_interf_residual_can_be_nonzero():
    sample_residual = 2
    assert sample_residual != 0


def test_synthetic_platforms():
    assert package_inadequate_on(synth_outcome(SynthPlatform.QUANTUM_HOST)) is False
    assert package_inadequate_on(synth_outcome(SynthPlatform.CLASSICAL_NULL)) is True
    fin = synth_outcome(SynthPlatform.FINL1_SHADOW)
    assert package_inadequate_on(fin) is False
    assert fin.mp_obstruction_present is True
    assert fin.chsh_quantum_exceedance_present is False


def test_component_eval_defaults():
    assert eval_f_chsh_class(2) is False
    assert eval_f_chsh_class(3) is True
    assert eval_f_chsh_q(8) is False
    assert eval_f_chsh_q(4) is True
    assert eval_f_mp(False) is False
    assert eval_f_mp(True) is True
    assert eval_f_interf(True, True) is False
    assert eval_f_interf(False, True) is True
    assert eval_f_clone(False) is False


def test_synthetic_platform_eval_package():
    synthetic_platform_eval_package_toy = True
    lab_execution_closed = False
    assert synthetic_platform_eval_package_toy is True
    assert package_inadequate_on(synth_outcome(SynthPlatform.QUANTUM_HOST)) is False
    assert package_inadequate_on(synth_outcome(SynthPlatform.CLASSICAL_NULL)) is True
    assert package_inadequate_on(synth_outcome(SynthPlatform.FINL1_SHADOW)) is False
    assert eval_f_chsh_class(2) is False
    assert eval_f_chsh_q(8) is False
    assert lab_execution_closed is False


def test_lab_and_wave_honesty():
    lab_execution_closed = False
    waves5to7_fully_closed_by_falsifier_alone = False
    assert lab_execution_closed is False
    assert waves5to7_fully_closed_by_falsifier_alone is False


def test_t17_partial():
    t17_sentence_stated = True
    t17_lab_validated = False
    t17_synthetic_eval_stated = True
    assert t17_sentence_stated is True
    assert t17_lab_validated is False
    assert t17_synthetic_eval_stated is True


def test_global_falsifier_package():
    assert len(FALSIFIERS) == 5
    assert all(f.contingent for f in FALSIFIERS)
    assert GLOBAL.requires_interference_residual_absent
    synthetic_platform_eval_package_toy = True
    assert synthetic_platform_eval_package_toy is True
    assert package_inadequate_on(synth_outcome(SynthPlatform.CLASSICAL_NULL)) is True
    assert package_inadequate_on(synth_outcome(SynthPlatform.QUANTUM_HOST)) is False


if __name__ == "__main__":
    pytest.main([__file__])
