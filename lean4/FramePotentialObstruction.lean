/- These declarations are opaque and were not elaborated by Lake in this change. -/

/- Conditional interfaces and arithmetic examples only.
No Rust receipt instantiates the curvature, Gramian representation, or coverage
hypotheses in this module. The named theorem statements are the precise scope.
AuthorityEffect: None.
-/
import Gluing

namespace MUB6.Gluing.FramePotentialObstruction

open MUB6.Gluing

def ideal_mub_fp2 (d k : Nat) : Nat :=
  k * (d + k - 1)

theorem ideal_mub_fp2_1_6 : ideal_mub_fp2 6 1 = 6 := by rfl
theorem ideal_mub_fp2_2_6 : ideal_mub_fp2 6 2 = 14 := by rfl
theorem ideal_mub_fp2_3_6 : ideal_mub_fp2 6 3 = 24 := by rfl
theorem ideal_mub_fp2_4_6 : ideal_mub_fp2 6 4 = 36 := by rfl
theorem ideal_mub_fp2_5_6 : ideal_mub_fp2 6 5 = 50 := by rfl
theorem ideal_mub_fp2_6_6 : ideal_mub_fp2 6 6 = 66 := by rfl
theorem ideal_mub_fp2_7_6 : ideal_mub_fp2 6 7 = 84 := by rfl

def welch_numerator_24_6 : Nat := 1152

def welch_denominator_6 : Nat := 42

def welch_scaled_threshold : Nat := 192

theorem welch_bound_satisfied_ideal : welch_scaled_threshold ≤ 7 * (ideal_mub_fp2 6 4) := by
  decide

theorem welch_bound_satisfied_candidate : welch_scaled_threshold ≤ 7 * 45 := by
  decide

def fp_defect (actual ideal : Nat) : Nat :=
  actual - ideal

theorem candidate_defect_eq_9 : fp_defect 45 36 = 9 := by rfl

theorem candidate_defect_strictly_positive : 0 < fp_defect 45 36 := by
  decide

opaque frame_potential_2 (B : Fin 4 → Basis) : Nat

def GenuineMUB4FramePotentialProperty : Prop :=
  ∀ (B : Fin 4 → Basis), PairwiseMU B → frame_potential_2 B = 36

theorem frame_potential_obstruction
    (B : Fin 4 → Basis)
    (h_fp : frame_potential_2 B = 45)
    (h_prop : GenuineMUB4FramePotentialProperty) :
    ¬ (PairwiseMU B) := by
  intro h_mu
  have h_ideal : frame_potential_2 B = 36 := h_prop B h_mu
  rw [h_fp] at h_ideal
  contradiction

theorem non_unitary_povm_intra_defect (d : Nat) (eta : Nat) (h_eta : 0 < eta) :
    d < d + 2 * eta := by
  omega

def mub_coherence_scaled : Nat := 23

def etf_coherence_scaled : Nat := 18

theorem etf_mub_coherence_defect_eq_5 :
    mub_coherence_scaled - etf_coherence_scaled = 5 := by
  rfl

theorem etf_mub_incompatibility :
    mub_coherence_scaled ≠ etf_coherence_scaled := by
  decide

def MUBQuadruple : Prop :=
  ∃ (B : Fin 4 → Basis), PairwiseMU B

def embed47 (i : Fin 4) : Fin 7 :=
  ⟨i.val, by omega⟩

theorem embed47_injective (i j : Fin 4) (h : embed47 i = embed47 j) : i = j := by
  ext
  have h_val : (embed47 i).val = (embed47 j).val := by rw [h]
  exact h_val

def restrict47 (B : Fin 7 → Basis) : Fin 4 → Basis :=
  fun i => B (embed47 i)

theorem pairwise_mu_restrict47 (B : Fin 7 → Basis) (hB : PairwiseMU B) :
    PairwiseMU (restrict47 B) := by
  intro i j hij
  apply hB
  intro heq
  exact hij (embed47_injective i j heq)

theorem mub_quadruple_of_complete (h_comp : CompleteMUB6) : MUBQuadruple := by
  rcases h_comp with ⟨B7, hB7⟩
  exact ⟨restrict47 B7, pairwise_mu_restrict47 B7 hB7⟩

theorem no_complete_mub6_of_no_quadruple : ¬ MUBQuadruple → NoCompleteMUB6 := by
  intro h_no_quad h_comp
  apply h_no_quad
  exact mub_quadruple_of_complete h_comp

theorem no_complete_mub6_of_candidate_fp_defect
    (h_quad_excl : MUBQuadruple → ∃ (B : Fin 4 → Basis), PairwiseMU B ∧ frame_potential_2 B = 45)
    (h_prop : GenuineMUB4FramePotentialProperty) :
    NoCompleteMUB6 := by
  intro h_comp
  have h_quad := mub_quadruple_of_complete h_comp
  rcases h_quad_excl h_quad with ⟨B, h_mu, h_fp⟩
  have h_not_mu := frame_potential_obstruction B h_fp h_prop
  exact h_not_mu h_mu

#print axioms ideal_mub_fp2_4_6
#print axioms welch_bound_satisfied_ideal
#print axioms welch_bound_satisfied_candidate
#print axioms candidate_defect_eq_9
#print axioms candidate_defect_strictly_positive
#print axioms frame_potential_obstruction
#print axioms non_unitary_povm_intra_defect
#print axioms etf_mub_coherence_defect_eq_5
#print axioms etf_mub_incompatibility
#print axioms embed47_injective
#print axioms pairwise_mu_restrict47
#print axioms mub_quadruple_of_complete
#print axioms no_complete_mub6_of_no_quadruple
#print axioms no_complete_mub6_of_candidate_fp_defect

end MUB6.Gluing.FramePotentialObstruction
