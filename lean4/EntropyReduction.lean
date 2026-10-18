

import EntropyDefs

namespace FiniteQm.C750.B01

def sum_weighted_exps : List (Nat × Nat) → Int
  | [] => 0
  | (w, a) :: rest => (w : Int) * (a : Int) + sum_weighted_exps rest

def gamma_numerator (D : Nat) (b_i : Nat) (terms_i : List (Nat × Nat)) : Int :=
  (D : Int) * (b_i : Int) - sum_weighted_exps terms_i

def gamma_coeff (D : Nat) (h_denom : 0 < D) (b_i : Nat) (terms_i : List (Nat × Nat)) : RatFrac :=
  ⟨gamma_numerator D b_i terms_i, D, h_denom⟩

structure BakerHypothesis where
  transcendental_of_nonvanishing :
    ∀ (form : LinearFormInLogarithms), form.is_nonvanishing →
      (∃ (t : Prop), t ∧ form.is_nonvanishing)

def IsTranscendentalEntropy (_baker : BakerHypothesis) (form : LinearFormInLogarithms) : Prop :=
  form.is_nonvanishing

structure PrimeReductionTerm where
  prime : Nat
  denom_exp : Nat
  state_terms : List (Nat × Nat)

namespace PrimeReductionTerm

def gamma_num (D : Nat) (term : PrimeReductionTerm) : Int :=
  gamma_numerator D term.denom_exp term.state_terms

def gamma_coeff (D : Nat) (h_pos : 0 < D) (term : PrimeReductionTerm) : RatFrac :=
  ⟨term.gamma_num D, D, h_pos⟩

end PrimeReductionTerm

namespace Reduction

def gamma_vector (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm) : List RatFrac :=
  terms.map (fun t => t.gamma_coeff D h_pos)

def prime_basis (terms : List PrimeReductionTerm) : List Nat :=
  terms.map (fun t => t.prime)

def linear_form (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm) : LinearFormInLogarithms :=
  ⟨prime_basis terms, gamma_vector D h_pos terms, by
    dsimp [prime_basis, gamma_vector]
    rw [List.length_map, List.length_map]⟩

theorem reduction_theorem_vanishing (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm)
    (h_all_zero : ∀ t ∈ terms, t.gamma_num D = 0) :
    (linear_form D h_pos terms).is_zero := by
  intro c hc
  dsimp [linear_form, gamma_vector] at hc
  have ⟨t, ht, hc_eq⟩ := List.mem_map.mp hc
  rw [← hc_eq]
  dsimp [PrimeReductionTerm.gamma_coeff, RatFrac.isZero]
  exact h_all_zero t ht

theorem reduction_theorem_nonvanishing (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm)
    (t : PrimeReductionTerm) (ht : t ∈ terms) (h_nz : t.gamma_num D ≠ 0) :
    (linear_form D h_pos terms).is_nonvanishing := by
  dsimp [LinearFormInLogarithms.is_nonvanishing]
  refine ⟨t.gamma_coeff D h_pos, ?_, h_nz⟩
  dsimp [linear_form, gamma_vector]
  exact List.mem_map.mpr ⟨t, ht, rfl⟩

end Reduction

end FiniteQm.C750.B01

private def l5aProvenance : String :=
  "Origin: lean4/EntropyReduction.lean Claim: reduction_theorem_vanishing AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
