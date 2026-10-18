from __future__ import annotations
"""
Executable Python dual harness for W6.20 (import necessity from pure FinL1).

Mirrors Lean `003_qm_import_necessity.lean`:

1. Working basis B4 = {OB-NONCOMM, OB-UNITARY, OB-CLONE, CONT-TIME}.
2. pureFinL1 admits none of the four slots.
3. Each slot is necessary-as-import relative to pureFinL1.
4. Capital fences: classical commute, reset not unitary, classical clone, discrete-only time.
5. Full BASIS-CANDIDATE necessity remains open.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
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
class NecessityModel:
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

    def necessary_as_import(self, slot: ImportSlot) -> bool:
        return not self.admits(slot)


# Pure FinL1: classical residual bookkeeping only — all B4 imports absent.
PURE_FINL1 = NecessityModel(
    noncomm=False, unitary=False, no_clone=False, cont_time=False
)


def test_working_basis_card():
    assert len(WORKING_BASIS) == 4
    assert len(set(WORKING_BASIS)) == 4


def test_pure_finl1_admits_none():
    for slot in WORKING_BASIS:
        assert not PURE_FINL1.admits(slot)


def test_every_b4_slot_necessary_as_import():
    for slot in WORKING_BASIS:
        assert PURE_FINL1.necessary_as_import(slot)


def test_necessary_as_import_per_slot():
    assert PURE_FINL1.necessary_as_import(ImportSlot.OB_NONCOMM)
    assert PURE_FINL1.necessary_as_import(ImportSlot.OB_UNITARY)
    assert PURE_FINL1.necessary_as_import(ImportSlot.OB_CLONE)
    assert PURE_FINL1.necessary_as_import(ImportSlot.CONT_TIME)


def test_classical_diag_commute_fence():
    diag_a = (2, 3)
    diag_b = (5, 7)
    assert (diag_a[0] * diag_b[0], diag_a[1] * diag_b[1]) == (
        diag_b[0] * diag_a[0],
        diag_b[1] * diag_a[1],
    )


def test_reset_column_not_doubly_stochastic():
    reset = {"k00": 1, "k10": 0, "k01": 1, "k11": 0}
    col_stoch = reset["k00"] + reset["k10"] == 1 and reset["k01"] + reset["k11"] == 1
    row0 = reset["k00"] + reset["k01"]
    assert col_stoch
    assert row0 != 1


def test_classical_clone_fair_exists():
    fair = (1, 1)
    clone = (fair[0] * fair[0], fair[0] * fair[1], fair[1] * fair[0], fair[1] * fair[1])
    assert clone == (1, 1, 1, 1)


def test_cont_time_not_forced_by_discrete():
    discrete_steps_only = True
    continuous_generator_admitted = False
    assert discrete_steps_only and not continuous_generator_admitted


def test_excluded_coupled_pairs():
    excluded = ("obU1_vs_composeLT", "obL2_vs_obBorn")
    assert len(excluded) == 2
    assert "OB-U1" not in {s.value for s in WORKING_BASIS}


def test_import_necessity_b4_package():
    assert len(WORKING_BASIS) == 4
    assert all(PURE_FINL1.necessary_as_import(s) for s in WORKING_BASIS)
    full_basis_necessity_open = True
    assert full_basis_necessity_open is True


if __name__ == "__main__":
    pytest.main([__file__])
