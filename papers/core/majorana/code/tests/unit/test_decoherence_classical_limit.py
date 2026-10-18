from __future__ import annotations
"""
Executable Python dual harness for W7.5 (decoherence & classical limit).

Mirrors Lean `003_qm_decoherence_classical_limit.lean`:

1. ShadowState = (pop0, pop1, offDiag); residual = 2*offDiag.
2. Decoherent ⇒ global weight = local diagonal sum.
3. Dephasing kills offDiag, preserves pops, idempotent.
4. Distinct coherent residuals can share classical shadow.
5. Finite multi-step damping + environment pointer-record toy.
6. Continuum Lindblad limit remains open.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


@dataclass(frozen=True)
class ShadowState:
    pop0: int
    pop1: int
    off_diag: int

    def is_decoherent(self) -> bool:
        return self.off_diag == 0

    def local_diagonal(self) -> int:
        return self.pop0 + self.pop1

    def global_weight(self) -> int:
        return self.local_diagonal() + 2 * self.off_diag

    def residual(self) -> int:
        return self.global_weight() - self.local_diagonal()

    def dephase(self) -> "ShadowState":
        return ShadowState(self.pop0, self.pop1, 0)

    def classical_shadow(self) -> tuple[int, int]:
        return (self.pop0, self.pop1)

    def abs_off(self) -> int:
        return abs(self.off_diag)

    def damp_step(self) -> "ShadowState":
        off = self.off_diag
        if off > 0:
            new_off = off - 1
        elif off < 0:
            new_off = off + 1
        else:
            new_off = 0
        return ShadowState(self.pop0, self.pop1, new_off)

    def damp_n(self, n: int) -> "ShadowState":
        s = self
        for _ in range(n):
            s = s.damp_step()
        return s


COHERENT_A = ShadowState(1, 1, 1)
COHERENT_B = ShadowState(1, 1, -1)
DECOHERED = ShadowState(1, 1, 0)
COHERENT_TWO = ShadowState(2, 3, 2)


class EnvHost(Enum):
    NO_POINTER = "noPointer"
    POINTER_RECORDED = "pointerRecorded"


def env_apply(host: EnvHost, s: ShadowState) -> ShadowState:
    if host is EnvHost.NO_POINTER:
        return s
    return s.dephase()


def recovers_classical_l1_shadow(host: EnvHost) -> bool:
    return host is EnvHost.POINTER_RECORDED


def test_residual_eq_twice_offdiag():
    s = ShadowState(3, 5, 2)
    assert s.residual() == 4
    assert s.residual() == 2 * s.off_diag


def test_decoherent_weight_additive():
    assert DECOHERED.is_decoherent()
    assert DECOHERED.global_weight() == DECOHERED.local_diagonal()


def test_dephase_classical():
    d = COHERENT_A.dephase()
    assert d.is_decoherent()
    assert d.pop0 == COHERENT_A.pop0 and d.pop1 == COHERENT_A.pop1
    assert d.residual() == 0


def test_dephase_idempotent():
    d = COHERENT_A.dephase()
    assert d.dephase() == d


def test_dephase_preserves_classical_shadow():
    assert COHERENT_A.dephase().classical_shadow() == COHERENT_A.classical_shadow()


def test_shared_classical_shadow():
    assert COHERENT_A.classical_shadow() == COHERENT_B.classical_shadow()
    assert COHERENT_A.classical_shadow() == DECOHERED.classical_shadow()
    assert COHERENT_A != COHERENT_B
    assert COHERENT_A.residual() == 2
    assert DECOHERED.residual() == 0


def test_dephase_collapses_coherent():
    assert COHERENT_A.dephase() == DECOHERED
    assert COHERENT_B.dephase() == DECOHERED


def test_damp_step_shrinks_off():
    assert COHERENT_A.damp_step() == DECOHERED
    assert COHERENT_TWO.damp_step() == ShadowState(2, 3, 1)
    assert COHERENT_TWO.damp_step().damp_step() == ShadowState(2, 3, 0)


def test_damp_n_reaches_decoherent():
    assert COHERENT_A.damp_n(1) == DECOHERED
    assert COHERENT_A.damp_n(1).is_decoherent()
    assert COHERENT_A.damp_n(1).residual() == 0
    assert COHERENT_TWO.abs_off() == 2
    assert COHERENT_TWO.damp_n(2).is_decoherent()
    assert COHERENT_TWO.damp_n(2).residual() == 0
    assert COHERENT_TWO.damp_n(2).classical_shadow() == COHERENT_TWO.classical_shadow()


def test_damp_preserves_classical_shadow():
    assert COHERENT_A.damp_step().classical_shadow() == COHERENT_A.classical_shadow()
    assert COHERENT_TWO.damp_n(2).classical_shadow() == COHERENT_TWO.classical_shadow()


def test_env_pointer_record():
    assert env_apply(EnvHost.NO_POINTER, COHERENT_A) == COHERENT_A
    assert env_apply(EnvHost.POINTER_RECORDED, COHERENT_A).is_decoherent()
    assert env_apply(EnvHost.POINTER_RECORDED, COHERENT_A).residual() == 0
    assert env_apply(EnvHost.NO_POINTER, COHERENT_A).residual() == 2
    assert (
        env_apply(EnvHost.POINTER_RECORDED, COHERENT_A).classical_shadow()
        == COHERENT_A.classical_shadow()
    )


def test_finL1_shadow_after_pointer():
    assert recovers_classical_l1_shadow(EnvHost.POINTER_RECORDED) is True
    assert recovers_classical_l1_shadow(EnvHost.NO_POINTER) is False


def test_finite_damping_pointer_package():
    finite_damping_pointer_package_toy = True
    continuum_lindblad_limit_closed = False
    assert finite_damping_pointer_package_toy is True
    assert COHERENT_A.damp_n(1) == DECOHERED
    assert COHERENT_TWO.damp_n(2).is_decoherent()
    assert env_apply(EnvHost.POINTER_RECORDED, COHERENT_A).residual() == 0
    assert recovers_classical_l1_shadow(EnvHost.POINTER_RECORDED) is True
    assert continuum_lindblad_limit_closed is False


def test_continuum_limit_open():
    continuum_lindblad_limit_closed = False
    assert continuum_lindblad_limit_closed is False


def test_decoherence_classical_limit_package():
    assert COHERENT_A.residual() == 2 * COHERENT_A.off_diag
    assert DECOHERED.global_weight() == DECOHERED.local_diagonal()
    assert COHERENT_A.dephase().is_decoherent()
    assert COHERENT_A.classical_shadow() == COHERENT_B.classical_shadow()
    finite_damping_pointer_package_toy = True
    assert finite_damping_pointer_package_toy is True
    assert env_apply(EnvHost.POINTER_RECORDED, COHERENT_A).residual() == 0


if __name__ == "__main__":
    pytest.main([__file__])
