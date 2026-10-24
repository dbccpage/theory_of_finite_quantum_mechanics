/-
Exact algebraic model; AuthorityEffect: None.
The declared rational Heron polynomial is symmetric and has the displayed evaluations; a supplied rational dot product is bilinear and an additive four-step telescoping sum is zero. Schlaefli cancellation is an explicit hypothesis, not derived geometry. The face vector and its interpretation as a sphere are supplied. No edge-length geometry, noncommutative Bianchi identity, continuum refinement theorem or actual Lorentzian exponential is constructed. The -I matrix and w-w identity do not identify a gravitational phase or resolve fermion signs.
Historical names are labels; their physical or operational interpretations require separate evidence.
-/

import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic
import ReggePachnerWdw



namespace CampaignFspReggeDeficitAction

open scoped BigOperators
open ReggePachnerWdw


def heronAreaSq (s01 s12 s02 : ℚ) : ℚ :=
  (2 * s01 * s12 + 2 * s12 * s02 + 2 * s02 * s01 - s01 ^ 2 - s12 ^ 2 - s02 ^ 2) / 16


theorem heronAreaSq_symmetric_and_orthogonal_pentatope_hinges (a b c : ℚ) :
    heronAreaSq a b c = heronAreaSq b a c ∧
    heronAreaSq a b c = heronAreaSq a c b ∧
    heronAreaSq 1 1 2 = 1 / 4 ∧
    heronAreaSq 2 2 2 = 3 / 4 ∧
    6 * heronAreaSq 1 1 2 + 4 * heronAreaSq 2 2 2 = 9 / 2 ∧
    heronAreaSq 1 1 4 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold heronAreaSq; ring
  · unfold heronAreaSq; ring
  · unfold heronAreaSq; norm_num
  · unfold heronAreaSq; norm_num
  · unfold heronAreaSq; norm_num
  · unfold heronAreaSq; norm_num


def hingeDeficit (fullTurn : ℚ) (dihedrals : List ℚ) : ℚ :=
  fullTurn - dihedrals.sum


def reggeAction {n : ℕ} (areas eps : Fin n → ℚ) : ℚ :=
  ∑ h : Fin n, areas h * eps h


theorem hingeDeficit_flat_sum_zero_and_reggeAction_bilinear
    (fullTurn : ℚ) (dihedrals : List ℚ) {n : ℕ} (areas eps1 eps2 : Fin n → ℚ) (c : ℚ) :
    (hingeDeficit fullTurn dihedrals = 0 ↔ dihedrals.sum = fullTurn) ∧
    reggeAction areas (fun _ => 0) = 0 ∧
    reggeAction areas (fun h => eps1 h + eps2 h) =
      reggeAction areas eps1 + reggeAction areas eps2 ∧
    reggeAction (fun h => c * areas h) eps1 = c * reggeAction areas eps1 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · unfold hingeDeficit
    constructor <;> intro h <;> linarith
  · simp [reggeAction]
  · simp [reggeAction, mul_add, Finset.sum_add_distrib]
  · simp [reggeAction, mul_assoc, ← Finset.mul_sum]


theorem reggeAction_positive_vs_mixed_deficit_sign
    {n : ℕ} (areas eps : Fin n → ℚ)
    (hA : ∀ h, 0 ≤ areas h) (hE : ∀ h, 0 ≤ eps h) :
    0 ≤ reggeAction areas eps ∧
    reggeAction ![1, 1] ![1, -2] = -1 ∧
    reggeAction ![1, 1] ![1, -2] < 0 ∧
    reggeAction ![1, 1] ![1, -1] = 0 ∧
    (![(1 : ℚ), -1] : Fin 2 → ℚ) 0 ≠ 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · unfold reggeAction
    exact Finset.sum_nonneg (fun h _ => mul_nonneg (hA h) (hE h))
  · simp [reggeAction, Fin.sum_univ_two]
    norm_num
  · simp [reggeAction, Fin.sum_univ_two]
  · simp [reggeAction, Fin.sum_univ_two]
  · norm_num


def s4BoundaryFaceVector : Fin 5 → ℕ :=
  ![6, 15, 20, 15, 6]


theorem s4_boundary_delta5_face_counts_and_euler_characteristic :
    Nat.choose 6 1 = s4BoundaryFaceVector 0 ∧
    Nat.choose 6 2 = s4BoundaryFaceVector 1 ∧
    Nat.choose 6 3 = s4BoundaryFaceVector 2 ∧
    Nat.choose 6 4 = s4BoundaryFaceVector 3 ∧
    Nat.choose 6 5 = s4BoundaryFaceVector 4 ∧
    (s4BoundaryFaceVector 0 : ℤ) - s4BoundaryFaceVector 1 + s4BoundaryFaceVector 2 -
      s4BoundaryFaceVector 3 + s4BoundaryFaceVector 4 = 2 ∧
    6 * Nat.choose 5 3 = 20 * 3 := by
  decide


theorem discrete_bianchi_cyclic_holonomy_telescoping (A f0 f1 f2 f3 : ℚ) :
    (f1 - f0) + (f2 - f1) + (f3 - f2) + (f0 - f3) = 0 ∧
    A * (f1 - f0) + A * (f2 - f1) + A * (f3 - f2) + A * (f0 - f3) = 0 := by
  constructor <;> ring


def reggeFullVariation {n : ℕ} (A dA eps dTheta : Fin n → ℚ) : ℚ :=
  ∑ h : Fin n, (dA h * eps h - A h * dTheta h)


theorem schlaefli_variation_reduces_regge_variation_to_area_term
    {n : ℕ} (A dA eps dTheta : Fin n → ℚ)
    (hSchlaefli : ∑ h : Fin n, A h * dTheta h = 0) :
    reggeFullVariation A dA eps dTheta = reggeAction dA eps := by
  unfold reggeFullVariation reggeAction
  rw [Finset.sum_sub_distrib, hSchlaefli, sub_zero]


def defectBoundHolds (sRegge sEh c aSq : ℚ) : Prop :=
  0 ≤ c ∧ 0 ≤ aSq ∧ (sRegge - sEh) ^ 2 ≤ (c * aSq) ^ 2


theorem defectBoundHolds_exact_rust_witnesses_and_zero_scale_limit
    (sRegge sEh c : ℚ) :
    defectBoundHolds (1 / 3) (1 / 4) 2 (1 / 16) ∧
    ¬ defectBoundHolds 1 0 1 (1 / 4) ∧
    ¬ defectBoundHolds 1 0 (-1) 1 ∧
    (defectBoundHolds sRegge sEh c 0 → sRegge = sEh) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · unfold defectBoundHolds; norm_num
  · unfold defectBoundHolds; norm_num
  · unfold defectBoundHolds; norm_num
  · rintro ⟨_, _, hsq⟩
    have h0 : (sRegge - sEh) ^ 2 ≤ 0 := by simpa using hsq
    have hge : 0 ≤ (sRegge - sEh) ^ 2 := sq_nonneg (sRegge - sEh)
    have heq0 : (sRegge - sEh) ^ 2 = 0 := le_antisymm h0 hge
    have hsub : sRegge - sEh = 0 := sq_eq_zero_iff.mp heq0
    linarith


theorem regge_action_independent_of_fermion_occupation_fence
    {n : ℕ} (areas eps : Fin n → ℚ) (w : ℚ) (hw : 0 < w) :
    (1 : ℚ) * w > 0 ∧
    (-1 : ℚ) * w < 0 ∧
    (1 : ℚ) * w + (-1 : ℚ) * w = 0 ∧
    reggeAction areas eps = reggeAction areas eps := by
  refine ⟨by linarith, by linarith, by ring, rfl⟩


def lorentzianHalfTurnMat : Matrix (Fin 2) (Fin 2) ℤ :=
  !![-1, 0;
      0, -1]


theorem euclidean_vs_lorentzian_regge_phase_fence :
    Matrix.trace lorentzianHalfTurnMat = -2 ∧
    lorentzianHalfTurnMat * lorentzianHalfTurnMat = 1 ∧
    (1 : Matrix (Fin 2) (Fin 2) ℤ) + lorentzianHalfTurnMat = 0 := by
  decide


theorem flat_vertex_sum_vs_signed_cancellation_fence (d1 d2 : ℕ) :
    (sumDeficits [d1, d2] = 0 ↔ d1 = 0 ∧ d2 = 0) ∧
    ((1 : ℚ) + (-1 : ℚ) = 0 ∧ (1 : ℚ) ≠ 0 ∧ (-1 : ℚ) ≠ 0) := by
  refine ⟨?_, ?_⟩
  · simp [sumDeficits]
  · norm_num

end CampaignFspReggeDeficitAction

#print axioms CampaignFspReggeDeficitAction.heronAreaSq_symmetric_and_orthogonal_pentatope_hinges
#print axioms CampaignFspReggeDeficitAction.hingeDeficit_flat_sum_zero_and_reggeAction_bilinear
#print axioms CampaignFspReggeDeficitAction.reggeAction_positive_vs_mixed_deficit_sign
#print axioms CampaignFspReggeDeficitAction.s4_boundary_delta5_face_counts_and_euler_characteristic
#print axioms CampaignFspReggeDeficitAction.discrete_bianchi_cyclic_holonomy_telescoping
#print axioms CampaignFspReggeDeficitAction.schlaefli_variation_reduces_regge_variation_to_area_term
#print axioms CampaignFspReggeDeficitAction.defectBoundHolds_exact_rust_witnesses_and_zero_scale_limit
#print axioms CampaignFspReggeDeficitAction.regge_action_independent_of_fermion_occupation_fence
#print axioms CampaignFspReggeDeficitAction.euclidean_vs_lorentzian_regge_phase_fence
#print axioms CampaignFspReggeDeficitAction.flat_vertex_sum_vs_signed_cancellation_fence
