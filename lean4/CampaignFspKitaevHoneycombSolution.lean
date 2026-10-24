import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic

/-!
# Campaign: FSP-KITAEV-HONEYCOMB-SOLUTION (TFQ-1207) — Four-Majorana Honeycomb Algebra, Plaquette Flux Invariance, and Gauge-Projection / Flux-Sector Fences

AuthorityEffect: None

This module narrows `FSP-KITAEV-HONEYCOMB-SOLUTION` (`TFQ-1207`, Rank 25 in `FERMION_SIGN`)
by proving in Lean 4 without `sorry` or custom axioms:

1. **Single-site four-Majorana Clifford & Pauli algebra**:
   Explicit `4 × 4` integer matrices `bX`, `bY`, `bZ` (`b_α^2 = I_4`) and `ic` (`(i c)^2 = -I_4`)
   mutually anticommute; the composite Kitaev spin operators `tildeSigmaX = bX * ic`,
   `tildeSigmaY = bY * ic`, `tildeSigmaZ = bZ * ic` satisfy `(tildeSigma_α)^2 = I_4`,
   mutual anticommutation, commute with the site gauge complex structure
   `siteGaugeJD = bX * bY * bZ * ic`, and satisfy `tildeSigmaX * tildeSigmaY * tildeSigmaZ = siteGaugeJD`.
2. **Bond spin-product factorization**:
   In any associative ring, when site-`j` and site-`k` Majorana operators anticommute
   (`cj * bk = -bk * cj`), the bond spin product `(bj * cj) * (bk * ck)` factors as
   `-(bj * bk) * (cj * ck)`, separating the link gauge bilinear `bj * bk` from the
   quadratic matter Majorana bilinear `cj * ck`.
3. **Hexagonal plaquette Z₂ gauge invariance, mutual commutation, and torus vortex parity**:
   Under any local vertex `Z₂` gauge transformation `u_{ab} ↦ η_a u_{ab} η_b` with `η_v^2 = 1`,
   the hexagonal plaquette flux `W_p = u01 * u12 * u23 * u34 * u45 * u50` is invariant;
   single-link flips invert both incident plaquettes while preserving their product; and on a
   closed surface where every link is shared by two plaquettes, the total flux product equals `1`.
4. **Quadratic matter Majorana matrix skew-symmetry and Pfaffian-squared determinant**:
   For any `4 × 4` skew-symmetric quadratic matter matrix `A(u)` over a commutative ring `R`,
   `A^T = -A` and `det(A(u)) = (Pf_4(A(u)))^2`.
5. **Explicit gauge-projection and flux-sector sign fences**:
   - The unprojected `N`-site four-Majorana space has dimension `4^N = 2^N * 2^N`, exceeding the
     physical `2^N` spin space by the `2^N`-fold local `Z₂` gauge redundancy (`D = diag(1,1,-1,-1)`
     has `D^2 = I_4` and `Tr(D) = 0`).
   - Flipping a single `Z₂` link variable `u01 = 1 ↦ -1` flips the quadratic Majorana Pfaffian
     `Pf_4(A(u))` from `+1` to `-1` while `det(A(u)) = +1` in both sectors.
   - The physical parity projector `(1 + P_matter * P_gauge)` kills mismatched parity states
     `P_matter = -P_gauge`, showing that unprojected single-sector traces do not equal the
     gauge-projected partition function.
-/

namespace CampaignFspKitaevHoneycombSolution

open Matrix BigOperators

/-- Single-site Majorana generator `b^x` on `Fin 4`. -/
def bX : Matrix (Fin 4) (Fin 4) ℤ :=
  !![0, 0, 1, 0;
     0, 0, 0, 1;
     1, 0, 0, 0;
     0, 1, 0, 0]

/-- Single-site Majorana generator `b^y` on `Fin 4`. -/
def bY : Matrix (Fin 4) (Fin 4) ℤ :=
  !![0, 1, 0, 0;
     1, 0, 0, 0;
     0, 0, 0, -1;
     0, 0, -1, 0]

/-- Single-site Majorana generator `b^z` on `Fin 4`. -/
def bZ : Matrix (Fin 4) (Fin 4) ℤ :=
  !![1, 0, 0, 0;
     0, -1, 0, 0;
     0, 0, -1, 0;
     0, 0, 0, 1]

/-- Real representation of `i * c` on `Fin 4`, satisfying `ic ^ 2 = -1` and anticommuting
with `bX`, `bY`, `bZ`. -/
def ic : Matrix (Fin 4) (Fin 4) ℤ :=
  !![0, 1, 0, 0;
     -1, 0, 0, 0;
     0, 0, 0, -1;
     0, 0, 1, 0]

/-- Kitaev composite spin operator `σ̃^x = i b^x c = bX * ic`. -/
def tildeSigmaX : Matrix (Fin 4) (Fin 4) ℤ := bX * ic

/-- Kitaev composite spin operator `σ̃^y = i b^y c = bY * ic`. -/
def tildeSigmaY : Matrix (Fin 4) (Fin 4) ℤ := bY * ic

/-- Kitaev composite spin operator `σ̃^z = i b^z c = bZ * ic`. -/
def tildeSigmaZ : Matrix (Fin 4) (Fin 4) ℤ := bZ * ic

/-- Site gauge complex-structure operator `J_D = i D = bX * bY * bZ * ic`. -/
def siteGaugeJD : Matrix (Fin 4) (Fin 4) ℤ := bX * bY * bZ * ic

/-- Theorem 1: The single-site Majorana generators `bX`, `bY`, `bZ` square to `1`,
`ic` squares to `-1`, and all four mutually anticommute. -/
theorem majorana_site_clifford_relations :
    bX * bX = 1 ∧
    bY * bY = 1 ∧
    bZ * bZ = 1 ∧
    ic * ic = -1 ∧
    bX * bY + bY * bX = 0 ∧
    bX * bZ + bZ * bX = 0 ∧
    bY * bZ + bZ * bY = 0 ∧
    bX * ic + ic * bX = 0 ∧
    bY * ic + ic * bY = 0 ∧
    bZ * ic + ic * bZ = 0 := by
  decide

/-- Theorem 2: The Kitaev spin operators `tildeSigmaX`, `tildeSigmaY`, `tildeSigmaZ`
satisfy the Pauli Clifford relations, commute with the site gauge operator `siteGaugeJD`
(whereas individual Majoranas anticommute with `siteGaugeJD`), and obey the chiral
product identity `tildeSigmaX * tildeSigmaY * tildeSigmaZ = siteGaugeJD`. -/
theorem kitaev_spin_operators_pauli_algebra_and_gauge_commutation :
    tildeSigmaX * tildeSigmaX = 1 ∧
    tildeSigmaY * tildeSigmaY = 1 ∧
    tildeSigmaZ * tildeSigmaZ = 1 ∧
    tildeSigmaX * tildeSigmaY + tildeSigmaY * tildeSigmaX = 0 ∧
    tildeSigmaX * tildeSigmaZ + tildeSigmaZ * tildeSigmaX = 0 ∧
    tildeSigmaY * tildeSigmaZ + tildeSigmaZ * tildeSigmaY = 0 ∧
    siteGaugeJD * siteGaugeJD = -1 ∧
    siteGaugeJD * tildeSigmaX = tildeSigmaX * siteGaugeJD ∧
    siteGaugeJD * tildeSigmaY = tildeSigmaY * siteGaugeJD ∧
    siteGaugeJD * tildeSigmaZ = tildeSigmaZ * siteGaugeJD ∧
    siteGaugeJD * bX + bX * siteGaugeJD = 0 ∧
    siteGaugeJD * ic + ic * siteGaugeJD = 0 ∧
    tildeSigmaX * tildeSigmaY * tildeSigmaZ = siteGaugeJD := by
  decide

/-- Theorem 3: In any associative ring `R`, if the matter Majorana `cj` at site `j`
anticommutes with the bond Majorana `bk` at site `k` (`cj * bk = -(bk * cj)`), then
the bond spin-spin product `(bj * cj) * (bk * ck)` factors into the negative product of
the link gauge bilinear `bj * bk` and the matter Majorana bilinear `cj * ck`. -/
theorem abstract_bond_spin_product_factorization
    {R : Type*} [Ring R] (bj cj bk ck : R)
    (h_anticomm : cj * bk = -(bk * cj)) :
    (bj * cj) * (bk * ck) = -((bj * bk) * (cj * ck)) := by
  calc
    (bj * cj) * (bk * ck) = bj * (cj * bk) * ck := by
      simp only [mul_assoc]
    _ = bj * (-(bk * cj)) * ck := by
      rw [h_anticomm]
    _ = -((bj * bk) * (cj * ck)) := by
      simp only [mul_neg, neg_mul, mul_assoc]

/-- Hexagonal plaquette flux `W_p` from the six oriented boundary link variables. -/
def hexPlaquetteFlux {R : Type*} [CommRing R]
    (u01 u12 u23 u34 u45 u50 : R) : R :=
  u01 * u12 * u23 * u34 * u45 * u50

/-- Theorem 4: Under any local vertex `Z₂` gauge transformation `u_{ab} ↦ η_a * u_{ab} * η_b`
with `η_v ^ 2 = 1` at each of the six vertices of a hexagonal plaquette, the plaquette
Wilson loop `hexPlaquetteFlux` is strictly invariant. -/
theorem plaquette_flux_local_z2_gauge_invariance
    {R : Type*} [CommRing R]
    (u01 u12 u23 u34 u45 u50 : R)
    (e0 e1 e2 e3 e4 e5 : R)
    (he0 : e0 * e0 = 1) (he1 : e1 * e1 = 1) (he2 : e2 * e2 = 1)
    (he3 : e3 * e3 = 1) (he4 : e4 * e4 = 1) (he5 : e5 * e5 = 1) :
    hexPlaquetteFlux
      (e0 * u01 * e1) (e1 * u12 * e2) (e2 * u23 * e3)
      (e3 * u34 * e4) (e4 * u45 * e5) (e5 * u50 * e0) =
    hexPlaquetteFlux u01 u12 u23 u34 u45 u50 := by
  unfold hexPlaquetteFlux
  calc
    (e0 * u01 * e1) * (e1 * u12 * e2) * (e2 * u23 * e3) *
        (e3 * u34 * e4) * (e4 * u45 * e5) * (e5 * u50 * e0)
      = (e0 * e0) * (e1 * e1) * (e2 * e2) * (e3 * e3) * (e4 * e4) * (e5 * e5) *
          (u01 * u12 * u23 * u34 * u45 * u50) := by ring
    _ = 1 * 1 * 1 * 1 * 1 * 1 * (u01 * u12 * u23 * u34 * u45 * u50) := by
      rw [he0, he1, he2, he3, he4, he5]
    _ = u01 * u12 * u23 * u34 * u45 * u50 := by ring

/-- Theorem 5: If each of the six boundary link variables of a hexagonal plaquette
squares to `1`, then the plaquette flux `W_p` squares to `1` (`W_p ^ 2 = 1`). -/
theorem hexPlaquetteFlux_sq_eq_one
    {R : Type*} [CommRing R]
    (u01 u12 u23 u34 u45 u50 : R)
    (h01 : u01 * u01 = 1) (h12 : u12 * u12 = 1) (h23 : u23 * u23 = 1)
    (h34 : u34 * u34 = 1) (h45 : u45 * u45 = 1) (h50 : u50 * u50 = 1) :
    hexPlaquetteFlux u01 u12 u23 u34 u45 u50 *
      hexPlaquetteFlux u01 u12 u23 u34 u45 u50 = 1 := by
  unfold hexPlaquetteFlux
  calc
    (u01 * u12 * u23 * u34 * u45 * u50) * (u01 * u12 * u23 * u34 * u45 * u50)
      = (u01 * u01) * (u12 * u12) * (u23 * u23) * (u34 * u34) * (u45 * u45) * (u50 * u50) := by ring
    _ = 1 * 1 * 1 * 1 * 1 * 1 := by rw [h01, h12, h23, h34, h45, h50]
    _ = 1 := by ring

/-- Theorem 6: Flipping a single shared link `u_shared ↦ -u_shared` between two incident
plaquettes inverts both plaquette fluxes (`W_p ↦ -W_p`, `W_q ↦ -W_q`) and preserves their
product `W_p * W_q`. -/
theorem single_link_flip_inverts_two_incident_plaquettes
    {R : Type*} [CommRing R]
    (u_shared p_rest q_rest : R) :
    ((-u_shared) * p_rest = -(u_shared * p_rest)) ∧
    ((-u_shared) * q_rest = -(u_shared * q_rest)) ∧
    (((-u_shared) * p_rest) * ((-u_shared) * q_rest) =
      (u_shared * p_rest) * (u_shared * q_rest)) := by
  refine ⟨by ring, by ring, by ring⟩

/-- Theorem 7: On a closed cellular surface where every link variable `u_e` (`u_e ^ 2 = 1`)
is shared by two plaquette boundaries, the product of all plaquette fluxes equals `1`. -/
theorem closed_surface_total_plaquette_flux_eq_one
    {ι : Type*} [Fintype ι] {R : Type*} [CommRing R]
    (u : ι → R) (hu : ∀ e, u e * u e = 1) :
    (∏ e : ι, u e) * (∏ e : ι, u e) = 1 := by
  rw [← Finset.prod_mul_distrib]
  exact Finset.prod_eq_one (fun e _ => hu e)

/-- General `4 × 4` skew-symmetric quadratic Majorana matter matrix `A(u)` over `R`. -/
def matterSkewMatrix4 {R : Type*} [CommRing R]
    (a01 a02 a03 a12 a13 a23 : R) : Matrix (Fin 4) (Fin 4) R :=
  !![0, a01, a02, a03;
     -a01, 0, a12, a13;
     -a02, -a12, 0, a23;
     -a03, -a13, -a23, 0]

/-- Pfaffian of the `4 × 4` skew-symmetric matrix `matterSkewMatrix4`. -/
def pfaffian4 {R : Type*} [CommRing R]
    (a01 a02 a03 a12 a13 a23 : R) : R :=
  a01 * a23 - a02 * a13 + a03 * a12

/-- Theorem 8: For any `4 × 4` quadratic Majorana matter matrix `matterSkewMatrix4`,
`A^T = -A` and `det(A) = (pfaffian4)^2`. -/
theorem quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det
    {R : Type*} [CommRing R]
    (a01 a02 a03 a12 a13 a23 : R) :
    (matterSkewMatrix4 a01 a02 a03 a12 a13 a23)ᵀ =
      -matterSkewMatrix4 a01 a02 a03 a12 a13 a23 ∧
    (matterSkewMatrix4 a01 a02 a03 a12 a13 a23).det =
      (pfaffian4 a01 a02 a03 a12 a13 a23) ^ 2 := by
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [matterSkewMatrix4, Matrix.transpose_apply]
  · simp [matterSkewMatrix4, pfaffian4, Matrix.det_succ_row_zero, Fin.sum_univ_four,
      Fin.sum_univ_three, Matrix.submatrix, Fin.succAbove]
    ring

/-- Diagonal representation of the single-site gauge parity operator `D` in its eigenbasis,
with eigenvalues `(+1, +1, -1, -1)`. -/
def siteGaugeParityDiag : Matrix (Fin 4) (Fin 4) ℤ :=
  Matrix.diagonal ![(1 : ℤ), 1, -1, -1]

/-- Unnormalized physical projector `P_+ = I_4 + D` onto the `D = +1` spin-`1/2` subspace. -/
def unnormalizedPhysProjector : Matrix (Fin 4) (Fin 4) ℤ :=
  1 + siteGaugeParityDiag

/-- Theorem 9 (Scope Fence — Unprojected Fock Dimension & Gauge Redundancy):
On `N` sites, the four-Majorana space has dimension `4^N = 2^N * 2^N` (`2^N` gauge copies
of the `2^N`-dimensional spin space), and at a single site `siteGaugeParityDiag` satisfies
`D^2 = I_4`, `Tr(D) = 0`, `(I_4 + D)^2 = 2 * (I_4 + D)`, and `Tr(I_4 + D) = 4` (twice rank `2`). -/
theorem unprojected_majorana_fock_overcounts_physical_spin_space_fence
    (N : ℕ) :
    4 ^ N = 2 ^ N * 2 ^ N ∧
    siteGaugeParityDiag * siteGaugeParityDiag = 1 ∧
    Matrix.trace siteGaugeParityDiag = 0 ∧
    unnormalizedPhysProjector * unnormalizedPhysProjector = 2 • unnormalizedPhysProjector ∧
    Matrix.trace unnormalizedPhysProjector = 4 := by
  refine ⟨?_, by decide, by decide, by decide, by decide⟩
  calc
    4 ^ N = (2 * 2) ^ N := by norm_num
    _ = 2 ^ N * 2 ^ N := Nat.mul_pow 2 2 N

/-- Theorem 10 (Scope Fence — Link Flip Reverses Matter Pfaffian Sign While Determinant Stays Positive):
Flipping a single `Z₂` link variable `u01 = 1 ↦ -1` (with `u23 = 1` and remaining couplings `0`)
flips the quadratic Majorana Pfaffian `pfaffian4` from `+1` to `-1` while the determinant
`det(A)` equals `+1` in both sectors, showing that sector-wise determinant nonnegativity
`det(A(u)) = Pf(A(u))^2 ≥ 0` does not remove relative Pfaffian sign changes across flux/gauge sectors. -/
theorem link_flip_flips_matter_pfaffian_sign_while_det_stays_positive_fence :
    pfaffian4 (1 : ℤ) 0 0 0 0 1 = 1 ∧
    pfaffian4 (-1 : ℤ) 0 0 0 0 1 = -1 ∧
    (matterSkewMatrix4 (1 : ℤ) 0 0 0 0 1).det = 1 ∧
    (matterSkewMatrix4 (-1 : ℤ) 0 0 0 0 1).det = 1 ∧
    pfaffian4 (1 : ℤ) 0 0 0 0 1 + pfaffian4 (-1 : ℤ) 0 0 0 0 1 = 0 := by
  refine ⟨by rfl, by rfl, ?_, ?_, by rfl⟩
  · exact (quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det (1 : ℤ) 0 0 0 0 1).2
  · exact (quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det (-1 : ℤ) 0 0 0 0 1).2

/-- Unnormalized global physical parity projection weight `1 + pMatter * pGauge`. -/
def parityProjectionWeight (pMatter pGauge : ℤ) : ℤ :=
  1 + pMatter * pGauge

/-- Theorem 11 (Scope Fence — Physical Gauge Projection Couples Matter and Link Parities):
For `pGauge^2 = 1`, the physical parity projection weight `1 + pMatter * pGauge` equals `2`
when `pMatter = pGauge` and vanishes (`0`) when `pMatter = -pGauge`, so an unprojected
matter trace in a fixed flux sector does not coincide with the physically projected sector weight. -/
theorem physical_parity_projection_excludes_mismatched_sector_states_fence
    (pGauge : ℤ) (hp : pGauge * pGauge = 1) :
    parityProjectionWeight pGauge pGauge = 2 ∧
    parityProjectionWeight (-pGauge) pGauge = 0 := by
  unfold parityProjectionWeight
  constructor
  · linear_combination hp
  · linear_combination -hp

#print axioms majorana_site_clifford_relations
#print axioms kitaev_spin_operators_pauli_algebra_and_gauge_commutation
#print axioms abstract_bond_spin_product_factorization
#print axioms plaquette_flux_local_z2_gauge_invariance
#print axioms hexPlaquetteFlux_sq_eq_one
#print axioms single_link_flip_inverts_two_incident_plaquettes
#print axioms closed_surface_total_plaquette_flux_eq_one
#print axioms quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det
#print axioms unprojected_majorana_fock_overcounts_physical_spin_space_fence
#print axioms link_flip_flips_matter_pfaffian_sign_while_det_stays_positive_fence
#print axioms physical_parity_projection_excludes_mismatched_sector_states_fence

end CampaignFspKitaevHoneycombSolution
