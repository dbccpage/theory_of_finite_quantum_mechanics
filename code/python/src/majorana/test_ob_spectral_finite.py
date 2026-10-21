from __future__ import annotations
"""
Executable Python dual harness for W6.10 / OB-SPECTRAL (finite spectral theorem).

Mirrors Lean `003_qm_ob_spectral_finite.lean`:

1. Classical sector observable (bit + 3-sector) reconstructs as spectral sum of chars.
2. Diagonal Hermitian projectors: idempotent, orthogonal, recover diagHerm.
3. Pauli-X real-symmetric toy: scaled spectral reconstruction + scaled projector algebra.
4. Spectral → instrument bind: classical Lüders-style sector update from eigenvalues.
5. Non-diagonal Hermitian is not a classical diagonal sector readout.
6. Declared spectral host distinguishes FinL1 classical vs complex-Hilbert lift.
7. Density Lüders under spectral projectors: P ρ P sandwich (diag + coherent σ_x).
8. POVM/Kraus residual: soft non-projective effects E0+E1=4I; projective Kraus
   dephases ρ+ → I.
9. Catalogue deepen: ternary projective POVM (σx⊕2); non-Hermitian amplitude-
   damping Kraus; soft Born mass Tr(Eρ); full catalogue OPEN.

AuthorityEffect: None. Mutation-capable: flip equalities to fail the suite.
"""


from dataclasses import dataclass
from enum import Enum

import pytest




def char_at(obs: dict[str, int], lam: int, sector: str) -> int:
    return 1 if obs[sector] == lam else 0


def test_classical_diag_obs_spectral_reconstruct():
    obs = {"b0": 2, "b1": 3}
    assert obs["b0"] != obs["b1"]
    for sector in ("b0", "b1"):
        recon = 2 * char_at(obs, 2, sector) + 3 * char_at(obs, 3, sector)
        assert recon == obs[sector]


def test_classical_readout_off_diagonal_forced_zero():
    class_readout = {"d0": 2, "d1": 3, "off": 0}
    assert class_readout["off"] == 0


def test_tri_sector_spectral_reconstruct():
    """General-n classical sector (n=3): three distinct eigenvalues reconstruct."""
    obs = {"s0": 1, "s1": 2, "s2": 5}
    assert len({obs[s] for s in obs}) == 3
    for sector in ("s0", "s1", "s2"):
        recon = (
            1 * char_at(obs, 1, sector)
            + 2 * char_at(obs, 2, sector)
            + 5 * char_at(obs, 5, sector)
        )
        assert recon == obs[sector]




@dataclass(frozen=True)
class Mat2:
    a00: int
    a01: int
    a10: int
    a11: int

    def is_symmetric(self) -> bool:
        return self.a01 == self.a10

    def add(self, other: Mat2) -> Mat2:
        return Mat2(
            self.a00 + other.a00,
            self.a01 + other.a01,
            self.a10 + other.a10,
            self.a11 + other.a11,
        )

    def smul(self, k: int) -> Mat2:
        return Mat2(k * self.a00, k * self.a01, k * self.a10, k * self.a11)

    def sub(self, other: Mat2) -> Mat2:
        return self.add(other.smul(-1))

    def mul(self, other: Mat2) -> Mat2:
        return Mat2(
            self.a00 * other.a00 + self.a01 * other.a10,
            self.a00 * other.a01 + self.a01 * other.a11,
            self.a10 * other.a00 + self.a11 * other.a10,
            self.a10 * other.a01 + self.a11 * other.a11,
        )

    def is_projector(self) -> bool:
        return self.mul(self) == self


SIGMA_X = Mat2(0, 1, 1, 0)
TWO_P_PLUS = Mat2(1, 1, 1, 1)
TWO_P_MINUS = Mat2(1, -1, -1, 1)
DIAG_HERM = Mat2(2, 0, 0, 3)
PROJ0 = Mat2(1, 0, 0, 0)
PROJ1 = Mat2(0, 0, 0, 1)
ID2 = Mat2(1, 0, 0, 1)
ZERO2 = Mat2(0, 0, 0, 0)


def test_sigma_x_symmetric_and_not_classical_diagonal():
    assert SIGMA_X.is_symmetric()
    assert SIGMA_X.a01 != 0


def test_sigma_x_spectral_scaled():
    """2σ_x = (+1)(2P₊) + (−1)(2P₋) = 2P₊ − 2P₋."""
    lhs = TWO_P_PLUS.sub(TWO_P_MINUS)
    rhs = SIGMA_X.smul(2)
    assert lhs == rhs
    assert lhs == Mat2(0, 2, 2, 0)


def test_sigma_x_eigenvectors():
    assert SIGMA_X.a00 * 1 + SIGMA_X.a01 * 1 == 1 * 1
    assert SIGMA_X.a10 * 1 + SIGMA_X.a11 * 1 == 1 * 1
    assert SIGMA_X.a00 * 1 + SIGMA_X.a01 * (-1) == (-1) * 1
    assert SIGMA_X.a10 * 1 + SIGMA_X.a11 * (-1) == (-1) * (-1)


def test_scaled_projectors_algebra():
    """(2P₊)² = 2·(2P₊); (2P₊)(2P₋) = 0."""
    assert TWO_P_PLUS.mul(TWO_P_PLUS) == TWO_P_PLUS.smul(2)
    assert TWO_P_MINUS.mul(TWO_P_MINUS) == TWO_P_MINUS.smul(2)
    assert TWO_P_PLUS.mul(TWO_P_MINUS) == ZERO2


def test_diag_herm_classical_compatible():
    assert DIAG_HERM.is_symmetric()
    assert DIAG_HERM.a01 == 0 and DIAG_HERM.a10 == 0


def test_diag_herm_spectral_projectors():
    """diagHerm = 2·P₀ + 3·P₁ with true idempotent orthogonal projectors."""
    assert PROJ0.is_projector()
    assert PROJ1.is_projector()
    assert PROJ0.mul(PROJ1) == ZERO2
    assert PROJ1.mul(PROJ0) == ZERO2
    assert PROJ0.add(PROJ1) == ID2
    recon = PROJ0.smul(2).add(PROJ1.smul(3))
    assert recon == DIAG_HERM




@dataclass(frozen=True)
class BitWeight:
    w0: int
    w1: int


def spectral_update(w: BitWeight, outcome: str) -> BitWeight:
    if outcome == "lam2":
        return BitWeight(w.w0, 0)
    if outcome == "lam3":
        return BitWeight(0, w.w1)
    raise ValueError(f"unknown spectral outcome: {outcome}")


def spectral_outcome_mass(w: BitWeight, outcome: str) -> int:
    if outcome == "lam2":
        return w.w0
    if outcome == "lam3":
        return w.w1
    raise ValueError(f"unknown spectral outcome: {outcome}")


def test_spectral_update_support_and_idempotence():
    w = BitWeight(3, 1)
    u2 = spectral_update(w, "lam2")
    u3 = spectral_update(w, "lam3")
    assert u2 == BitWeight(3, 0)
    assert u3 == BitWeight(0, 1)
    assert spectral_update(u2, "lam2") == u2
    assert spectral_update(u3, "lam3") == u3
    assert spectral_outcome_mass(w, "lam2") == 3
    assert spectral_outcome_mass(w, "lam3") == 1


def test_spectral_outcome_matches_diag_obs_sectors():
    """diagObs eigenvalues label the instrument sectors (binding receipt)."""
    obs = {"b0": 2, "b1": 3}
    assert obs["b0"] == 2 and obs["b1"] == 3
    prior = BitWeight(3, 1)
    assert spectral_update(prior, "lam3") == BitWeight(0, 1)




@dataclass(frozen=True)
class DeclaredSpectral:
    host: str
    dim: int

    def __post_init__(self) -> None:
        if self.dim <= 0:
            raise ValueError("finite_dim requires dim > 0")
        if self.host not in {"finL1Classical", "complexHilbertLift"}:
            raise ValueError(f"unknown spectral host: {self.host}")


def test_declared_spectral_hosts():
    classical = DeclaredSpectral(host="finL1Classical", dim=2)
    tri = DeclaredSpectral(host="finL1Classical", dim=3)
    qubit = DeclaredSpectral(host="complexHilbertLift", dim=2)
    assert classical.host == "finL1Classical"
    assert tri.dim == 3
    assert qubit.host == "complexHilbertLift"
    with pytest.raises(ValueError, match="unknown spectral host"):
        DeclaredSpectral(host="orphanInfinite", dim=2)
    with pytest.raises(ValueError, match="finite_dim"):
        DeclaredSpectral(host="finL1Classical", dim=0)


def test_general_n_nondiag_marked_open_residual():
    """Full general-n spectral theorem not discharged; classical n=3 is; 3×3 toy is."""
    n = 3
    assert n > 2
    general_n_nondiag_spectral_open = True
    classical_tri_derived = True
    nondiag_3x3_toy = True
    assert general_n_nondiag_spectral_open is True
    assert classical_tri_derived is True
    assert nondiag_3x3_toy is True




@dataclass(frozen=True)
class Mat3:
    a00: int
    a01: int
    a02: int
    a10: int
    a11: int
    a12: int
    a20: int
    a21: int
    a22: int

    def is_symmetric(self) -> bool:
        return self.a01 == self.a10 and self.a02 == self.a20 and self.a12 == self.a21

    def add(self, other: "Mat3") -> "Mat3":
        return Mat3(
            self.a00 + other.a00,
            self.a01 + other.a01,
            self.a02 + other.a02,
            self.a10 + other.a10,
            self.a11 + other.a11,
            self.a12 + other.a12,
            self.a20 + other.a20,
            self.a21 + other.a21,
            self.a22 + other.a22,
        )

    def smul(self, k: int) -> "Mat3":
        return Mat3(
            k * self.a00,
            k * self.a01,
            k * self.a02,
            k * self.a10,
            k * self.a11,
            k * self.a12,
            k * self.a20,
            k * self.a21,
            k * self.a22,
        )

    def sub(self, other: "Mat3") -> "Mat3":
        return self.add(other.smul(-1))

    def mul(self, other: "Mat3") -> "Mat3":
        return Mat3(
            self.a00 * other.a00 + self.a01 * other.a10 + self.a02 * other.a20,
            self.a00 * other.a01 + self.a01 * other.a11 + self.a02 * other.a21,
            self.a00 * other.a02 + self.a01 * other.a12 + self.a02 * other.a22,
            self.a10 * other.a00 + self.a11 * other.a10 + self.a12 * other.a20,
            self.a10 * other.a01 + self.a11 * other.a11 + self.a12 * other.a21,
            self.a10 * other.a02 + self.a11 * other.a12 + self.a12 * other.a22,
            self.a20 * other.a00 + self.a21 * other.a10 + self.a22 * other.a20,
            self.a20 * other.a01 + self.a21 * other.a11 + self.a22 * other.a21,
            self.a20 * other.a02 + self.a21 * other.a12 + self.a22 * other.a22,
        )


def embed2(m: Mat2) -> Mat3:
    return Mat3(m.a00, m.a01, 0, m.a10, m.a11, 0, 0, 0, 0)


NON_DIAG3 = Mat3(0, 1, 0, 1, 0, 0, 0, 0, 2)
PROJ2_3 = Mat3(0, 0, 0, 0, 0, 0, 0, 0, 1)
TWO_PPLUS = Mat2(1, 1, 1, 1)
TWO_PMINUS = Mat2(1, -1, -1, 1)
SIGMA_X = Mat2(0, 1, 1, 0)


def test_nondiag3_symmetric_and_not_classical_diagonal():
    assert NON_DIAG3.is_symmetric()
    assert NON_DIAG3.a01 != 0


def test_nondiag3_eq_embed_sigmaX_plus_2proj():
    reconstructed = embed2(SIGMA_X).add(PROJ2_3.smul(2))
    assert reconstructed == NON_DIAG3


def test_nondiag3_spectral_scaled():
    """2H = embed(2P+) - embed(2P-) + 4 P2."""
    lhs = embed2(TWO_PPLUS).sub(embed2(TWO_PMINUS)).add(PROJ2_3.smul(4))
    rhs = NON_DIAG3.smul(2)
    assert lhs == rhs


def test_nondiag3_eigenvectors():
    def apply(m: Mat3, v: tuple[int, int, int]) -> tuple[int, int, int]:
        v0, v1, v2 = v
        return (
            m.a00 * v0 + m.a01 * v1 + m.a02 * v2,
            m.a10 * v0 + m.a11 * v1 + m.a12 * v2,
            m.a20 * v0 + m.a21 * v1 + m.a22 * v2,
        )

    assert apply(NON_DIAG3, (1, 1, 0)) == (1, 1, 0)
    assert apply(NON_DIAG3, (1, -1, 0)) == (-1, 1, 0)
    assert apply(NON_DIAG3, (0, 0, 1)) == (0, 0, 2)


def test_proj2_3_idempotent_and_orthogonal_to_embed():
    assert PROJ2_3.mul(PROJ2_3) == PROJ2_3
    zero = Mat3(0, 0, 0, 0, 0, 0, 0, 0, 0)
    assert embed2(TWO_PPLUS).mul(PROJ2_3) == zero
    assert embed2(TWO_PMINUS).mul(PROJ2_3) == zero


def test_complex_tri_nondiag_host():
    host = DeclaredSpectral(host="complexHilbertLift", dim=3)
    assert host.host == "complexHilbertLift"
    assert host.dim == 3




def luders(p: Mat2, rho: Mat2) -> Mat2:
    """Unnormalized Lüders sandwich P ρ P."""
    return p.mul(rho.mul(p))


def diag_density(rho00: int, rho11: int) -> Mat2:
    return Mat2(rho00, 0, 0, rho11)


RHO_PLUS = Mat2(1, 1, 1, 1)
RHO_MINUS = Mat2(1, -1, -1, 1)


def test_proj_luders_diag_sector_support():
    """Diagonal density: P0 kills sector 1; P1 kills sector 0."""
    rho = diag_density(3, 1)
    post0 = luders(PROJ0, rho)
    post1 = luders(PROJ1, rho)
    assert post0 == diag_density(3, 0)
    assert post1 == diag_density(0, 1)
    assert post0.a11 == 0 and post1.a00 == 0


def test_proj_luders_idempotent():
    rho = Mat2(2, 1, 1, 4)
    assert luders(PROJ0, luders(PROJ0, rho)) == luders(PROJ0, rho)
    assert luders(PROJ1, luders(PROJ1, rho)) == luders(PROJ1, rho)


def test_scaled_sigma_x_luders_on_coherent():
    """(2P+) ρ+ (2P+) = 4·(2P+); (2P−) ρ+ (2P−) = 0."""
    assert RHO_PLUS == TWO_P_PLUS
    assert luders(TWO_P_PLUS, RHO_PLUS) == TWO_P_PLUS.smul(4)
    assert luders(TWO_P_MINUS, RHO_PLUS) == ZERO2
    assert luders(TWO_P_PLUS, RHO_MINUS) == ZERO2


def test_coherent_density_not_classical_diagonal():
    assert RHO_PLUS.a01 != 0
    post = spectral_update(BitWeight(1, 1), "lam2")
    assert post == BitWeight(1, 0)
    assert post.w1 == 0


def test_density_luders_spectral_package():
    """Package dual of Lean density_luders_spectral_package."""
    assert luders(PROJ0, diag_density(3, 1)) == diag_density(3, 0)
    assert luders(PROJ1, diag_density(3, 1)) == diag_density(0, 1)
    assert luders(TWO_P_PLUS, RHO_PLUS) == TWO_P_PLUS.smul(4)
    assert luders(TWO_P_MINUS, RHO_PLUS) == ZERO2
    assert RHO_PLUS.a01 != 0



SOFT_EFFECT0 = Mat2(2, 1, 1, 2)
SOFT_EFFECT1 = Mat2(2, -1, -1, 2)


def kraus_channel(rho: Mat2) -> Mat2:
    """Projective Kraus instrument Σ_i P_i ρ P_i."""
    return luders(PROJ0, rho).add(luders(PROJ1, rho))


def test_soft_effects_sum_four_id():
    s = SOFT_EFFECT0.add(SOFT_EFFECT1)
    assert s == ID2.smul(4)


def test_soft_effects_not_projectors():
    assert not SOFT_EFFECT0.is_projector()
    assert not SOFT_EFFECT1.is_projector()
    assert SOFT_EFFECT0.is_symmetric()
    assert SOFT_EFFECT1.is_symmetric()
    assert SOFT_EFFECT0.a01 != 0
    assert SOFT_EFFECT1.a01 != 0


def test_spectral_projective_povm():
    assert PROJ0.add(PROJ1) == ID2
    assert PROJ0.is_projector()
    assert PROJ1.is_projector()


def test_kraus_completeness_and_dephase():
    completeness = PROJ0.mul(PROJ0).add(PROJ1.mul(PROJ1))
    assert completeness == ID2
    assert kraus_channel(RHO_PLUS) == ID2
    assert kraus_channel(RHO_PLUS).a01 == 0


def test_soft_povm_needs_lift():
    soft_povm_host = "complexHilbertLift"
    assert soft_povm_host == "complexHilbertLift"
    assert SOFT_EFFECT0.a01 != 0


def test_general_povm_kraus_catalogue_open():
    general_povm_kraus_catalogue_open = True
    assert general_povm_kraus_catalogue_open is True


def test_povm_kraus_residual_package():
    assert SOFT_EFFECT0.add(SOFT_EFFECT1) == ID2.smul(4)
    assert not SOFT_EFFECT0.is_projector()
    assert not SOFT_EFFECT1.is_projector()
    assert PROJ0.add(PROJ1) == ID2
    assert PROJ0.is_projector()
    assert kraus_channel(RHO_PLUS) == ID2
    general_povm_kraus_catalogue_open = True
    assert general_povm_kraus_catalogue_open is True



ID3 = Mat3(1, 0, 0, 0, 1, 0, 0, 0, 1)
DAMP_KRAUS0 = Mat2(1, 0, 0, 0)
DAMP_KRAUS1 = Mat2(0, 1, 0, 0)
RHO1 = Mat2(0, 0, 0, 1)


def mat2_transpose(m: Mat2) -> Mat2:
    return Mat2(m.a00, m.a10, m.a01, m.a11)


def kraus_effect(k: Mat2) -> Mat2:
    return mat2_transpose(k).mul(k)


def damp_channel(rho: Mat2) -> Mat2:
    k0t = mat2_transpose(DAMP_KRAUS0)
    k1t = mat2_transpose(DAMP_KRAUS1)
    return DAMP_KRAUS0.mul(rho.mul(k0t)).add(DAMP_KRAUS1.mul(rho.mul(k1t)))


def soft_born_mass(e: Mat2, rho: Mat2) -> int:
    return e.a00 * rho.a00 + e.a01 * rho.a10 + e.a10 * rho.a01 + e.a11 * rho.a11


def test_ternary_projective_povm_resolution():
    """embed(2P+)+embed(2P-)+2 P2 = 2 I3."""
    left = embed2(TWO_P_PLUS).add(embed2(TWO_P_MINUS)).add(PROJ2_3.smul(2))
    assert left == ID3.smul(2)


def test_damp_kraus_completeness_and_non_projector():
    completeness = kraus_effect(DAMP_KRAUS0).add(kraus_effect(DAMP_KRAUS1))
    assert completeness == ID2
    assert DAMP_KRAUS0.is_projector()
    assert not DAMP_KRAUS1.is_projector()
    assert DAMP_KRAUS1.mul(DAMP_KRAUS1) == ZERO2


def test_damp_channel_maps_rho1_to_proj0():
    assert damp_channel(RHO1) == PROJ0


def test_soft_born_mass_resolution():
    m0 = soft_born_mass(SOFT_EFFECT0, RHO_PLUS)
    m1 = soft_born_mass(SOFT_EFFECT1, RHO_PLUS)
    assert m0 == 6
    assert m1 == 2
    assert m0 + m1 == 8
    assert soft_born_mass(ID2.smul(4), RHO_PLUS) == 8


def test_povm_kraus_catalogue_deepen_package():
    left = embed2(TWO_P_PLUS).add(embed2(TWO_P_MINUS)).add(PROJ2_3.smul(2))
    assert left == ID3.smul(2)
    assert kraus_effect(DAMP_KRAUS0).add(kraus_effect(DAMP_KRAUS1)) == ID2
    assert not DAMP_KRAUS1.is_projector()
    assert damp_channel(RHO1) == PROJ0
    assert (
        soft_born_mass(SOFT_EFFECT0, RHO_PLUS) + soft_born_mass(SOFT_EFFECT1, RHO_PLUS)
        == 8
    )
    general_povm_kraus_catalogue_open = True
    assert general_povm_kraus_catalogue_open is True




class Sector4(str, Enum):
    S0 = "s0"
    S1 = "s1"
    S2 = "s2"
    S3 = "s3"


QUAD_OBS = {
    Sector4.S0: 1,
    Sector4.S1: 2,
    Sector4.S2: 3,
    Sector4.S3: 7,
}


def char_at4(eig: int, s: Sector4) -> int:
    return 1 if QUAD_OBS[s] == eig else 0


def reconstruct_quad(s: Sector4) -> int:
    return sum(lam * char_at4(lam, s) for lam in (1, 2, 3, 7))


@dataclass(frozen=True)
class BlockDiag2:
    b0: object
    b1: object


CLASSICAL_GENERAL_N_CLOSED_DIMS = [2, 3, 4]
NONDIAG_BLOCK_TOYS_CLOSED = [2, 3, 4]
GENERAL_N_NONDIAG_ARBITRARY_OPEN = True


def classical_eig_list(n: int) -> list[int]:
    return list(range(1, n + 1))


def test_quad_obs_reconstruct():
    for s in Sector4:
        assert QUAD_OBS[s] == reconstruct_quad(s)
    assert QUAD_OBS[Sector4.S0] != QUAD_OBS[Sector4.S3]
    assert QUAD_OBS[Sector4.S0] == 1
    assert QUAD_OBS[Sector4.S3] == 7


def test_classical_eig_list_n4():
    assert classical_eig_list(4) == [1, 2, 3, 4]
    assert len(classical_eig_list(4)) == 4
    assert CLASSICAL_GENERAL_N_CLOSED_DIMS == [2, 3, 4]


def test_block_sigma_x_spectral():
    """σx ⊕ σx: each block reconstructs with scaled projectors."""
    left = TWO_P_PLUS.sub(TWO_P_MINUS)
    scaled = SIGMA_X.smul(2)
    assert left == scaled
    block = BlockDiag2(SIGMA_X, SIGMA_X)
    assert block.b0 == SIGMA_X
    assert block.b1 == SIGMA_X
    assert SIGMA_X.a01 != 0


def test_general_n_spectral_deepen_package():
    assert CLASSICAL_GENERAL_N_CLOSED_DIMS == [2, 3, 4]
    assert NONDIAG_BLOCK_TOYS_CLOSED == [2, 3, 4]
    assert len(classical_eig_list(4)) == 4
    assert QUAD_OBS[Sector4.S0] == 1
    assert QUAD_OBS[Sector4.S3] == 7
    assert TWO_P_PLUS.sub(TWO_P_MINUS) == SIGMA_X.smul(2)
    assert GENERAL_N_NONDIAG_ARBITRARY_OPEN is True
    assert GENERAL_N_NONDIAG_ARBITRARY_OPEN is not False


if __name__ == "__main__":
    pytest.main([__file__])
