from __future__ import annotations
"""
Executable Python dual harness for W5.10 — unitary vs antiunitary/conjugation gauge.

Mirrors Lean `003_qm_unitary_antiunitary_gauge.lean`:

1. Gaussian-integer amplitudes; mul-by-i and conj preserve |z|².
2. The two gauges disagree as maps but agree on Born weights.
3. Two-level fair superposition: same born (1,1); distinct gauged states.
4. Wigner-style sesquilinear residual: unitary preserves ⟨u,v⟩; conj conjugates it.

AuthorityEffect: None.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


@dataclass(frozen=True)
class GaussInt:
    re: int
    im: int

    @property
    def norm_sq(self) -> int:
        return self.re * self.re + self.im * self.im

    def mul_i(self) -> GaussInt:
        return GaussInt(re=-self.im, im=self.re)

    def conj(self) -> GaussInt:
        return GaussInt(re=self.re, im=-self.im)

    def mul(self, other: "GaussInt") -> GaussInt:
        return GaussInt(
            re=self.re * other.re - self.im * other.im,
            im=self.re * other.im + self.im * other.re,
        )

    def sesqui(self, other: "GaussInt") -> GaussInt:
        """⟨self, other⟩ = conj(self) * other."""
        return self.conj().mul(other)


@dataclass(frozen=True)
class Amp2:
    z0: GaussInt
    z1: GaussInt

    @property
    def total_norm_sq(self) -> int:
        return self.z0.norm_sq + self.z1.norm_sq

    def apply_unitary_i(self) -> Amp2:
        return Amp2(self.z0.mul_i(), self.z1.mul_i())

    def apply_conj(self) -> Amp2:
        return Amp2(self.z0.conj(), self.z1.conj())

    def born_weights(self) -> tuple[int, int]:
        return (self.z0.norm_sq, self.z1.norm_sq)


def test_mul_i_and_conj_preserve_norm():
    for z in (GaussInt(1, 1), GaussInt(3, -4), GaussInt(0, 5), GaussInt(2, 0)):
        assert z.mul_i().norm_sq == z.norm_sq
        assert z.conj().norm_sq == z.norm_sq


def test_gauges_disagree_on_sample():
    sample = GaussInt(1, 1)
    assert sample.mul_i() == GaussInt(-1, 1)
    assert sample.conj() == GaussInt(1, -1)
    assert sample.mul_i() != sample.conj()
    assert sample.mul_i().norm_sq == sample.norm_sq == 2


def test_fair_superpos_born_invariant():
    fair = Amp2(GaussInt(1, 0), GaussInt(0, 1))
    assert fair.born_weights() == (1, 1)
    assert fair.apply_unitary_i().born_weights() == (1, 1)
    assert fair.apply_conj().born_weights() == (1, 1)
    assert fair.apply_unitary_i().total_norm_sq == fair.total_norm_sq
    assert fair.apply_conj().total_norm_sq == fair.total_norm_sq


def test_fair_gauges_disagree_as_states():
    fair = Amp2(GaussInt(1, 0), GaussInt(0, 1))
    assert fair.apply_unitary_i() != fair.apply_conj()


def test_gauge_kind_labels_distinct():
    kinds = {"unitaryPhaseI", "antiunitaryConj"}
    assert len(kinds) == 2


def test_mul_i_preserves_sesqui():
    pairs = [
        (GaussInt(1, 0), GaussInt(0, 1)),
        (GaussInt(1, 1), GaussInt(2, -1)),
        (GaussInt(3, -4), GaussInt(0, 5)),
    ]
    for u, v in pairs:
        assert u.mul_i().sesqui(v.mul_i()) == u.sesqui(v)


def test_conj_conjugates_sesqui():
    pairs = [
        (GaussInt(1, 0), GaussInt(0, 1)),
        (GaussInt(1, 1), GaussInt(2, -1)),
        (GaussInt(3, -4), GaussInt(0, 5)),
    ]
    for u, v in pairs:
        assert u.conj().sesqui(v.conj()) == u.sesqui(v).conj()


def test_conj_changes_nonreal_sesqui():
    u, v = GaussInt(1, 0), GaussInt(0, 1)
    assert u.sesqui(v) == GaussInt(0, 1)
    assert u.conj().sesqui(v.conj()) == GaussInt(0, -1)
    assert u.conj().sesqui(v.conj()) != u.sesqui(v)


def test_composition_algebra():
    sample = GaussInt(1, 1)
    assert sample.mul_i().mul_i() == GaussInt(-1, -1)
    assert sample.conj().conj() == sample
    assert sample.conj().mul_i() != sample.mul_i().conj()


class GaugeKind(str, Enum):
    UNITARY_PHASE_I = "unitaryPhaseI"
    ANTIUNITARY_CONJ = "antiunitaryConj"


class SesquiAction(str, Enum):
    PRESERVES = "preserves"
    CONJUGATES = "conjugates"


def sesqui_action_of(kind: GaugeKind) -> SesquiAction:
    if kind is GaugeKind.UNITARY_PHASE_I:
        return SesquiAction.PRESERVES
    return SesquiAction.CONJUGATES


def test_sesqui_action_separates_gauges():
    assert sesqui_action_of(GaugeKind.UNITARY_PHASE_I) is SesquiAction.PRESERVES
    assert sesqui_action_of(GaugeKind.ANTIUNITARY_CONJ) is SesquiAction.CONJUGATES
    assert sesqui_action_of(GaugeKind.UNITARY_PHASE_I) != sesqui_action_of(
        GaugeKind.ANTIUNITARY_CONJ
    )


def test_wigner_style_sesqui_package():
    u, v = GaussInt(1, 0), GaussInt(0, 1)
    assert u.mul_i().sesqui(v.mul_i()) == u.sesqui(v)
    assert u.conj().sesqui(v.conj()) == u.sesqui(v).conj()
    assert u.conj().sesqui(v.conj()) != u.sesqui(v)
    sample = GaussInt(1, 1)
    assert sample.conj().mul_i() != sample.mul_i().conj()
    full_wigner_theorem_open = True
    assert full_wigner_theorem_open is True


if __name__ == "__main__":
    pytest.main([__file__])
