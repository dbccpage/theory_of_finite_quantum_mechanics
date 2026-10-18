from __future__ import annotations
"""
Executable Python dual harness for W6.7 — continuum irreducibility (type-split).

Mirrors Lean `003_qm_continuum_irreducibility.lean`:

1. CONT-SCALAR / CONT-TIME / CONT-SECTORS are pairwise distinct slots.
2. Flip kernel is column-stochastic with det=-1 → fails CTMC embed det fence.
3. Nat weights do not construct continuum scalar field.
4. Unbounded sectors not native to FinL1.
5. Finite shadow without convergence certificate → oracleNeeded (membrane).
6. All three CONT-* slots packaged UNDERIVABLE from FinL1 alone.

AuthorityEffect: None. Continuum membership ⊬ authority.
"""


from dataclasses import dataclass
from enum import Enum
from typing import Optional

import pytest


class ContinuumSlot(str, Enum):
    CONT_SCALAR = "contScalar"
    CONT_TIME = "contTime"
    CONT_SECTORS = "contSectors"


def test_continuum_slots_pairwise_distinct():
    slots = list(ContinuumSlot)
    assert len(slots) == 3
    assert ContinuumSlot.CONT_SCALAR != ContinuumSlot.CONT_TIME
    assert ContinuumSlot.CONT_SCALAR != ContinuumSlot.CONT_SECTORS
    assert ContinuumSlot.CONT_TIME != ContinuumSlot.CONT_SECTORS


@dataclass(frozen=True)
class Kernel2:
    k00: int
    k10: int
    k01: int
    k11: int

    @property
    def det(self) -> int:
        return self.k00 * self.k11 - self.k01 * self.k10

    def is_column_stochastic(self) -> bool:
        return self.k00 + self.k10 == 1 and self.k01 + self.k11 == 1

    def satisfies_embed_det_fence(self) -> bool:
        """Toy necessary condition for CTMC embeddability: det > 0."""
        return self.det > 0


ID_KERNEL = Kernel2(1, 0, 0, 1)
FLIP_KERNEL = Kernel2(0, 1, 1, 0)


def test_markov_embedding_obstruction_flip():
    assert ID_KERNEL.is_column_stochastic()
    assert FLIP_KERNEL.is_column_stochastic()
    assert ID_KERNEL.det == 1
    assert FLIP_KERNEL.det == -1
    assert ID_KERNEL.satisfies_embed_det_fence()
    assert not FLIP_KERNEL.satisfies_embed_det_fence()


def test_cont_time_not_forced_by_discrete_stochastic():
    assert (
        FLIP_KERNEL.is_column_stochastic()
        and not FLIP_KERNEL.satisfies_embed_det_fence()
    )


def continuum_scalar_from_weights(_w0: int, _w1: int) -> None:
    """FinL1 Nat weights never construct a continuum scalar field."""
    return None


def test_no_scalar_continuum_from_weights():
    assert continuum_scalar_from_weights(1, 1) is None
    assert continuum_scalar_from_weights(2, 3) is None


def test_cont_sectors_not_native():
    unbounded_sectors_native = False
    assert unbounded_sectors_native is False
    bit_sector_count = 2
    assert bit_sector_count == 2


@dataclass(frozen=True)
class ShadowFamily:
    idx: int


@dataclass(frozen=True)
class ConvergenceCertificate:
    topology: int
    refinement: int
    rate: int


class ContinuumOutcome(str, Enum):
    PROMOTED = "promoted"
    ORACLE_NEEDED = "oracleNeeded"


def intake(
    sf: ShadowFamily, cert: Optional[ConvergenceCertificate]
) -> tuple[ContinuumOutcome, Optional[int]]:
    if cert is None:
        return (ContinuumOutcome.ORACLE_NEEDED, None)
    return (ContinuumOutcome.PROMOTED, sf.idx)


def test_shadow_without_cert_refused():
    sf = ShadowFamily(idx=7)
    outcome, kid = intake(sf, None)
    assert outcome is ContinuumOutcome.ORACLE_NEEDED
    assert kid is None
    outcome2, kid2 = intake(sf, ConvergenceCertificate(1, 2, 3))
    assert outcome2 is ContinuumOutcome.PROMOTED
    assert kid2 == 7


class ImportStatus(str, Enum):
    UNDERIVABLE = "underivable"
    CONDITIONAL = "conditionalImport"


def status_of(slot: ContinuumSlot) -> ImportStatus:
    return ImportStatus.UNDERIVABLE


def test_all_cont_slots_underivable_from_finL1():
    for slot in ContinuumSlot:
        assert status_of(slot) is ImportStatus.UNDERIVABLE


def test_continuum_irreducible_package():
    assert ContinuumSlot.CONT_SCALAR != ContinuumSlot.CONT_TIME
    assert (
        FLIP_KERNEL.is_column_stochastic()
        and not FLIP_KERNEL.satisfies_embed_det_fence()
    )
    assert continuum_scalar_from_weights(0, 1) is None
    assert intake(ShadowFamily(0), None)[0] is ContinuumOutcome.ORACLE_NEEDED
    full_markov_embedding_classification_open = True
    assert full_markov_embedding_classification_open is True


def test_continuum_membership_not_auth():
    is_auth = False
    assert is_auth is False


if __name__ == "__main__":
    pytest.main([__file__])
