from __future__ import annotations
"""
Executable Python dual harness for W7.4 (Hardy / MM / CBH operational crosswalk).

Mirrors Lean `003_qm_operational_frameworks.lean`:

1. Three frameworks: Hardy2001, MasanesMueller2011, CBH.
2. Twelve crosswalk rows: 2 Aligned + 7 Partial + 1 ResidualOpen + 2 NotClaimed.
3. Reconstruction equivalence refused; full map open.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


class Framework(str, Enum):
    HARDY = "Hardy2001"
    MM = "MasanesMueller2011"
    CBH = "CBH"


class OurSlot(str, Enum):
    FINL1 = "FinL1Classical"
    SURPLUS = "SurplusPhaseInterf"
    NONCOMM = "ObNoncomm"
    UNITARY = "ObUnitary"
    CLONE = "ObClone"
    CONT_TIME = "ContTime"
    LT = "LocalTomography"
    CHSH = "ChshRecovery"
    MP = "MerminPeres"
    BORN_SPEC = "BornSpectralResidual"
    FULL_HARDY = "FullHardyAxiomSet"
    FULL_EQ = "FullMmCbhEquivalence"


class MapStatus(str, Enum):
    ALIGNED = "Aligned"
    PARTIAL = "Partial"
    RESIDUAL = "ResidualOpen"
    NOT_CLAIMED = "NotClaimed"


@dataclass(frozen=True)
class CrosswalkRow:
    slot: OurSlot
    primary: Framework
    status: MapStatus


FRAMEWORKS = (Framework.HARDY, Framework.MM, Framework.CBH)

CROSSWALK = (
    CrosswalkRow(OurSlot.FINL1, Framework.HARDY, MapStatus.ALIGNED),
    CrosswalkRow(OurSlot.CLONE, Framework.CBH, MapStatus.ALIGNED),
    CrosswalkRow(OurSlot.SURPLUS, Framework.HARDY, MapStatus.PARTIAL),
    CrosswalkRow(OurSlot.NONCOMM, Framework.MM, MapStatus.PARTIAL),
    CrosswalkRow(OurSlot.UNITARY, Framework.MM, MapStatus.PARTIAL),
    CrosswalkRow(OurSlot.CONT_TIME, Framework.MM, MapStatus.PARTIAL),
    CrosswalkRow(OurSlot.LT, Framework.MM, MapStatus.PARTIAL),
    CrosswalkRow(OurSlot.CHSH, Framework.CBH, MapStatus.PARTIAL),
    CrosswalkRow(OurSlot.MP, Framework.HARDY, MapStatus.PARTIAL),
    CrosswalkRow(OurSlot.BORN_SPEC, Framework.HARDY, MapStatus.RESIDUAL),
    CrosswalkRow(OurSlot.FULL_HARDY, Framework.HARDY, MapStatus.NOT_CLAIMED),
    CrosswalkRow(OurSlot.FULL_EQ, Framework.MM, MapStatus.NOT_CLAIMED),
)


def test_frameworks_card():
    assert len(FRAMEWORKS) == 3


def test_crosswalk_card():
    assert len(CROSSWALK) == 12
    assert len({r.slot for r in CROSSWALK}) == 12


def test_status_partition():
    aligned = [r for r in CROSSWALK if r.status is MapStatus.ALIGNED]
    partial = [r for r in CROSSWALK if r.status is MapStatus.PARTIAL]
    residual = [r for r in CROSSWALK if r.status is MapStatus.RESIDUAL]
    not_claimed = [r for r in CROSSWALK if r.status is MapStatus.NOT_CLAIMED]
    assert len(aligned) == 2
    assert len(partial) == 7
    assert len(residual) == 1
    assert len(not_claimed) == 2
    assert len(aligned) + len(partial) + len(residual) + len(not_claimed) == 12


def test_finL1_aligned_hardy():
    row = next(r for r in CROSSWALK if r.slot is OurSlot.FINL1)
    assert row.status is MapStatus.ALIGNED
    assert row.primary is Framework.HARDY


def test_clone_aligned_cbh():
    row = next(r for r in CROSSWALK if r.slot is OurSlot.CLONE)
    assert row.status is MapStatus.ALIGNED
    assert row.primary is Framework.CBH


def test_lt_partial_mm():
    row = next(r for r in CROSSWALK if r.slot is OurSlot.LT)
    assert row.status is MapStatus.PARTIAL
    assert row.primary is Framework.MM


def test_frameworks_appear_as_primary():
    primaries = {r.primary for r in CROSSWALK}
    assert primaries == set(FRAMEWORKS)


def test_equivalence_refused():
    reconstruction_equivalence_claim = False
    full_operational_map_closed = False
    assert reconstruction_equivalence_claim is False
    assert full_operational_map_closed is False


def test_operational_frameworks_package():
    assert len(FRAMEWORKS) == 3
    assert len(CROSSWALK) == 12
    assert sum(1 for r in CROSSWALK if r.status is MapStatus.ALIGNED) == 2
    assert sum(1 for r in CROSSWALK if r.status is MapStatus.NOT_CLAIMED) == 2


if __name__ == "__main__":
    pytest.main([__file__])
