from __future__ import annotations
"""
Executable Python dual harness for W6.12 / OB-INSTRUMENT.

Mirrors Lean `003_qm_ob_instrument_luders.lean`:

1. Classical sector Lüders / Bayesian update (qm_021 capital).
2. Density Lüders PρP under spectral projectors (W6.10 capital bind).
3. Diagonal density population matches classical update; coherence needs lift host.
4. Soft / Kraus / ternary instrument bind (W6.10 catalogue capital).
5. Full POVM/Kraus instrument catalogue remains OPEN.

AuthorityEffect: None.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


@dataclass(frozen=True)
class BitWeight:
    w0: int
    w1: int

    @property
    def total(self) -> int:
        return self.w0 + self.w1

    def supported_on_0(self) -> bool:
        return self.w1 == 0

    def supported_on_1(self) -> bool:
        return self.w0 == 0


class Outcome(str, Enum):
    O0 = "o0"
    O1 = "o1"


def update(w: BitWeight, o: Outcome) -> BitWeight:
    if o is Outcome.O0:
        return BitWeight(w.w0, 0)
    return BitWeight(0, w.w1)


def outcome_mass(w: BitWeight, o: Outcome) -> int:
    return w.w0 if o is Outcome.O0 else w.w1


def test_outcome_mass_matches_prior():
    w = BitWeight(3, 1)
    assert outcome_mass(w, Outcome.O0) == 3
    assert outcome_mass(w, Outcome.O1) == 1


def test_update_support_and_idempotence():
    w = BitWeight(3, 1)
    u0 = update(w, Outcome.O0)
    u1 = update(w, Outcome.O1)
    assert u0 == BitWeight(3, 0) and u0.supported_on_0()
    assert u1 == BitWeight(0, 1) and u1.supported_on_1()
    assert update(u0, Outcome.O0) == u0
    assert update(u1, Outcome.O1) == u1


def test_repeatability():
    w = BitWeight(3, 1)
    u1 = update(w, Outcome.O1)
    assert outcome_mass(u1, Outcome.O1) == u1.total == 1
    u0 = update(w, Outcome.O0)
    assert outcome_mass(u0, Outcome.O0) == u0.total == 3


def test_qm021_worked_example():
    prior = BitWeight(3, 1)
    assert update(prior, Outcome.O1) == BitWeight(0, 1)
    assert update(update(prior, Outcome.O1), Outcome.O1) == BitWeight(0, 1)


def test_declared_instrument_hosts():
    classical = {"host": "finL1Classical", "n_outcomes": 2}
    qubit = {"host": "complexHilbertLift", "n_outcomes": 2}
    assert classical["n_outcomes"] > 0 and qubit["n_outcomes"] > 0
    assert density_luders_requires_lift_host("finL1Classical") is False
    assert density_luders_requires_lift_host("complexHilbertLift") is True


# --- Density Lüders (W6.10 spectral projector bind) ---


@dataclass(frozen=True)
class Mat2:
    a00: int
    a01: int
    a10: int
    a11: int

    def mul(self, other: "Mat2") -> "Mat2":
        return Mat2(
            self.a00 * other.a00 + self.a01 * other.a10,
            self.a00 * other.a01 + self.a01 * other.a11,
            self.a10 * other.a00 + self.a11 * other.a10,
            self.a10 * other.a01 + self.a11 * other.a11,
        )

    def smul(self, k: int) -> "Mat2":
        return Mat2(k * self.a00, k * self.a01, k * self.a10, k * self.a11)


def luders(p: Mat2, rho: Mat2) -> Mat2:
    return p.mul(rho.mul(p))


def diag_density(rho00: int, rho11: int) -> Mat2:
    return Mat2(rho00, 0, 0, rho11)


PROJ0 = Mat2(1, 0, 0, 0)
PROJ1 = Mat2(0, 0, 0, 1)
TWO_P_PLUS = Mat2(1, 1, 1, 1)
TWO_P_MINUS = Mat2(1, -1, -1, 1)
RHO_PLUS = TWO_P_PLUS
RHO_MINUS = TWO_P_MINUS
ZERO2 = Mat2(0, 0, 0, 0)


def density_luders_requires_lift_host(host: str) -> bool:
    if host == "finL1Classical":
        return False
    if host == "complexHilbertLift":
        return True
    raise ValueError(host)


def test_diag_luders_sector_support():
    post0 = luders(PROJ0, diag_density(3, 1))
    post1 = luders(PROJ1, diag_density(3, 1))
    assert post0 == diag_density(3, 0)
    assert post1 == diag_density(0, 1)
    assert post0.a11 == 0 and post1.a00 == 0


def test_diag_luders_matches_classical_population():
    """Density diagonal o1 update matches classical (3,1)→(0,1)."""
    post = luders(PROJ1, diag_density(3, 1))
    classical = update(BitWeight(3, 1), Outcome.O1)
    assert post.a00 == 0 and post.a11 == 1
    assert classical == BitWeight(0, 1)
    assert classical.w0 == post.a00 and classical.w1 == post.a11


def test_proj_luders_idempotent():
    rho = Mat2(2, 1, 1, 4)
    assert luders(PROJ0, luders(PROJ0, rho)) == luders(PROJ0, rho)
    assert luders(PROJ1, luders(PROJ1, rho)) == luders(PROJ1, rho)


def test_coherent_sigma_x_luders():
    assert luders(TWO_P_PLUS, RHO_PLUS) == TWO_P_PLUS.smul(4)
    assert luders(TWO_P_MINUS, RHO_PLUS) == ZERO2
    assert luders(TWO_P_PLUS, RHO_MINUS) == ZERO2
    assert RHO_PLUS.a01 != 0


def test_classical_update_erases_coherence():
    assert RHO_PLUS.a01 != 0
    post = update(BitWeight(1, 1), Outcome.O0)
    assert post == BitWeight(1, 0)
    assert post.w1 == 0


def test_density_luders_instrument_package():
    assert luders(PROJ0, diag_density(3, 1)) == diag_density(3, 0)
    assert luders(PROJ1, diag_density(3, 1)) == diag_density(0, 1)
    assert luders(TWO_P_PLUS, RHO_PLUS) == TWO_P_PLUS.smul(4)
    assert luders(TWO_P_MINUS, RHO_PLUS) == ZERO2
    assert RHO_PLUS.a01 != 0
    assert density_luders_requires_lift_host("complexHilbertLift") is True
    assert density_luders_requires_lift_host("finL1Classical") is False


def test_general_povm_marked_open():
    general_povm_instrument_open = True
    assert general_povm_instrument_open is True


# --- Soft / Kraus / ternary instrument bind (W6.10 capital) ---

ID2 = Mat2(1, 0, 0, 1)
SOFT_EFFECT0 = Mat2(2, 1, 1, 2)
SOFT_EFFECT1 = Mat2(2, -1, -1, 2)
DAMP_KRAUS0 = Mat2(1, 0, 0, 0)
DAMP_KRAUS1 = Mat2(0, 1, 0, 0)
RHO1 = Mat2(0, 0, 0, 1)


def mat2_add(a: Mat2, b: Mat2) -> Mat2:
    return Mat2(a.a00 + b.a00, a.a01 + b.a01, a.a10 + b.a10, a.a11 + b.a11)


def mat2_transpose(m: Mat2) -> Mat2:
    return Mat2(m.a00, m.a10, m.a01, m.a11)


def is_projector(m: Mat2) -> bool:
    return m.mul(m) == m


def soft_outcome_mass(e: Mat2, rho: Mat2) -> int:
    return e.a00 * rho.a00 + e.a01 * rho.a10 + e.a10 * rho.a01 + e.a11 * rho.a11


def projective_kraus_channel(rho: Mat2) -> Mat2:
    return mat2_add(luders(PROJ0, rho), luders(PROJ1, rho))


def kraus_effect(k: Mat2) -> Mat2:
    return mat2_transpose(k).mul(k)


def damp_instrument_channel(rho: Mat2) -> Mat2:
    k0t = mat2_transpose(DAMP_KRAUS0)
    k1t = mat2_transpose(DAMP_KRAUS1)
    return mat2_add(
        DAMP_KRAUS0.mul(rho.mul(k0t)),
        DAMP_KRAUS1.mul(rho.mul(k1t)),
    )


def test_soft_instrument_effects_resolution():
    assert mat2_add(SOFT_EFFECT0, SOFT_EFFECT1) == ID2.smul(4)
    assert not is_projector(SOFT_EFFECT0)
    assert SOFT_EFFECT0.a01 != 0


def test_soft_instrument_mass_resolution():
    m0 = soft_outcome_mass(SOFT_EFFECT0, RHO_PLUS)
    m1 = soft_outcome_mass(SOFT_EFFECT1, RHO_PLUS)
    assert m0 == 6 and m1 == 2 and m0 + m1 == 8


def test_projective_kraus_instrument_dephase():
    assert projective_kraus_channel(RHO_PLUS) == ID2
    assert projective_kraus_channel(RHO_PLUS).a01 == 0


def test_damp_instrument_kraus():
    completeness = mat2_add(kraus_effect(DAMP_KRAUS0), kraus_effect(DAMP_KRAUS1))
    assert completeness == ID2
    assert is_projector(DAMP_KRAUS0)
    assert not is_projector(DAMP_KRAUS1)
    assert damp_instrument_channel(RHO1) == PROJ0


def test_ternary_instrument_declaration():
    ternary = {"host": "complexHilbertLift", "n_outcomes": 3}
    assert ternary["n_outcomes"] == 3
    assert density_luders_requires_lift_host(ternary["host"]) is True


def test_instrument_kraus_catalogue_bind_package():
    assert mat2_add(SOFT_EFFECT0, SOFT_EFFECT1) == ID2.smul(4)
    assert not is_projector(SOFT_EFFECT0)
    assert (
        soft_outcome_mass(SOFT_EFFECT0, RHO_PLUS)
        + soft_outcome_mass(SOFT_EFFECT1, RHO_PLUS)
        == 8
    )
    assert projective_kraus_channel(RHO_PLUS) == ID2
    assert mat2_add(kraus_effect(DAMP_KRAUS0), kraus_effect(DAMP_KRAUS1)) == ID2
    assert not is_projector(DAMP_KRAUS1)
    assert damp_instrument_channel(RHO1) == PROJ0
    assert {"host": "complexHilbertLift", "n_outcomes": 3}["n_outcomes"] == 3
    general_povm_instrument_open = True
    assert general_povm_instrument_open is True


if __name__ == "__main__":
    pytest.main([__file__])
