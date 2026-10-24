/-
Exact algebraic model; AuthorityEffect: None.
Explicit integer matrices obey Clifford identities; one anticommutation hypothesis gives bond factorization; a six-factor commutative-ring flux is gauge invariant; a product of all supplied involutions squared equals one; and a 4x4 skew matrix has determinant equal to the squared explicit Pfaffian polynomial. No cellular surface incidence map is built, so the product-square lemma is not a theorem about all plaquettes on closed tori. The independent diagonal parity matrix is not identified with the supplied Majorana gauge operator. No physical Hilbert-space projection or thermal partition function is constructed.
Historical names are labels; their physical or operational interpretations require separate evidence.
-/

import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic



namespace CampaignFspKitaevHoneycombSolution

open Matrix BigOperators


def bX : Matrix (Fin 4) (Fin 4) ℤ :=
  !![0, 0, 1, 0;
     0, 0, 0, 1;
     1, 0, 0, 0;
     0, 1, 0, 0]


def bY : Matrix (Fin 4) (Fin 4) ℤ :=
  !![0, 1, 0, 0;
     1, 0, 0, 0;
     0, 0, 0, -1;
     0, 0, -1, 0]


def bZ : Matrix (Fin 4) (Fin 4) ℤ :=
  !![1, 0, 0, 0;
     0, -1, 0, 0;
     0, 0, -1, 0;
     0, 0, 0, 1]


def ic : Matrix (Fin 4) (Fin 4) ℤ :=
  !![0, 1, 0, 0;
     -1, 0, 0, 0;
     0, 0, 0, -1;
     0, 0, 1, 0]


def tildeSigmaX : Matrix (Fin 4) (Fin 4) ℤ := bX * ic


def tildeSigmaY : Matrix (Fin 4) (Fin 4) ℤ := bY * ic


def tildeSigmaZ : Matrix (Fin 4) (Fin 4) ℤ := bZ * ic


def siteGaugeJD : Matrix (Fin 4) (Fin 4) ℤ := bX * bY * bZ * ic


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


def hexPlaquetteFlux {R : Type*} [CommRing R]
    (u01 u12 u23 u34 u45 u50 : R) : R :=
  u01 * u12 * u23 * u34 * u45 * u50


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


theorem single_link_flip_inverts_two_incident_plaquettes
    {R : Type*} [CommRing R]
    (u_shared p_rest q_rest : R) :
    ((-u_shared) * p_rest = -(u_shared * p_rest)) ∧
    ((-u_shared) * q_rest = -(u_shared * q_rest)) ∧
    (((-u_shared) * p_rest) * ((-u_shared) * q_rest) =
      (u_shared * p_rest) * (u_shared * q_rest)) := by
  refine ⟨by ring, by ring, by ring⟩


theorem closed_surface_total_plaquette_flux_eq_one
    {ι : Type*} [Fintype ι] {R : Type*} [CommRing R]
    (u : ι → R) (hu : ∀ e, u e * u e = 1) :
    (∏ e : ι, u e) * (∏ e : ι, u e) = 1 := by
  rw [← Finset.prod_mul_distrib]
  exact Finset.prod_eq_one (fun e _ => hu e)


def matterSkewMatrix4 {R : Type*} [CommRing R]
    (a01 a02 a03 a12 a13 a23 : R) : Matrix (Fin 4) (Fin 4) R :=
  !![0, a01, a02, a03;
     -a01, 0, a12, a13;
     -a02, -a12, 0, a23;
     -a03, -a13, -a23, 0]


def pfaffian4 {R : Type*} [CommRing R]
    (a01 a02 a03 a12 a13 a23 : R) : R :=
  a01 * a23 - a02 * a13 + a03 * a12


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


def siteGaugeParityDiag : Matrix (Fin 4) (Fin 4) ℤ :=
  Matrix.diagonal ![(1 : ℤ), 1, -1, -1]


def unnormalizedPhysProjector : Matrix (Fin 4) (Fin 4) ℤ :=
  1 + siteGaugeParityDiag


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


theorem link_flip_flips_matter_pfaffian_sign_while_det_stays_positive_fence :
    pfaffian4 (1 : ℤ) 0 0 0 0 1 = 1 ∧
    pfaffian4 (-1 : ℤ) 0 0 0 0 1 = -1 ∧
    (matterSkewMatrix4 (1 : ℤ) 0 0 0 0 1).det = 1 ∧
    (matterSkewMatrix4 (-1 : ℤ) 0 0 0 0 1).det = 1 ∧
    pfaffian4 (1 : ℤ) 0 0 0 0 1 + pfaffian4 (-1 : ℤ) 0 0 0 0 1 = 0 := by
  refine ⟨by rfl, by rfl, ?_, ?_, by rfl⟩
  · exact (quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det (1 : ℤ) 0 0 0 0 1).2
  · exact (quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det (-1 : ℤ) 0 0 0 0 1).2


def parityProjectionWeight (pMatter pGauge : ℤ) : ℤ :=
  1 + pMatter * pGauge


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
