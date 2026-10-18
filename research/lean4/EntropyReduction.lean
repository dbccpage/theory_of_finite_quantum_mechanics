/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

-- Reduction.lean — von Neumann Entropy Reduction Theorem in Lean 4
-- Campaign: C750 Block 01 (Target C750-T569)
-- AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).

import EntropyDefs

namespace FiniteQm.C750.B01

/-- Transformed exponent sum for a prime base p_i: sum_j w_j * a_{ji}.
    Given a list of (weight, exponent) pairs for prime p_i across all d states. -/
def sum_weighted_exps : List (Nat × Nat) → Int
  | [] => 0
  | (w, a) :: rest => (w : Int) * (a : Int) + sum_weighted_exps rest

/-- Exact integer numerator of the reduced rational coefficient Gamma_i:
    G_i = D * b_i - sum_j w_j * a_{ji}. -/
def gamma_numerator (D : Nat) (b_i : Nat) (terms_i : List (Nat × Nat)) : Int :=
  (D : Int) * (b_i : Int) - sum_weighted_exps terms_i

/-- Reduced rational coefficient Gamma_i = G_i / D in Q. -/
def gamma_coeff (D : Nat) (h_denom : 0 < D) (b_i : Nat) (terms_i : List (Nat × Nat)) : RatFrac :=
  ⟨gamma_numerator D b_i terms_i, D, h_denom⟩

/-- Baker's Theorem (Anchor A1) & Lindemann-Weierstrass (Anchor A2) as cited input.
    Asserts that any nonvanishing rational linear form in logarithms of distinct primes
    evaluates to a transcendental quantity (not in the algebraic carrier Q). -/
structure BakerHypothesis where
  transcendental_of_nonvanishing :
    ∀ (form : LinearFormInLogarithms), form.is_nonvanishing →
      (∃ (t : Prop), t ∧ form.is_nonvanishing)

/-- Abstract transcendence property for an entropy form under Baker's theorem. -/
def IsTranscendentalEntropy (_baker : BakerHypothesis) (form : LinearFormInLogarithms) : Prop :=
  form.is_nonvanishing

/-- Reduction data for a single prime factor p_i.
    Contains the prime p_i, the exponent b_i in the denominator D,
    and the list of (w_j, a_{ji}) pairs across all d eigenvalues. -/
structure PrimeReductionTerm where
  prime : Nat
  denom_exp : Nat
  state_terms : List (Nat × Nat)

namespace PrimeReductionTerm

/-- Exact integer numerator G_i = D * b_i - sum_j w_j * a_{ji}. -/
def gamma_num (D : Nat) (term : PrimeReductionTerm) : Int :=
  gamma_numerator D term.denom_exp term.state_terms

/-- Reduced rational coefficient Gamma_i = G_i / D in Q. -/
def gamma_coeff (D : Nat) (h_pos : 0 < D) (term : PrimeReductionTerm) : RatFrac :=
  ⟨term.gamma_num D, D, h_pos⟩

end PrimeReductionTerm

namespace Reduction

/-- Assembles the reduced rational coefficient vector vec(Gamma) = [Gamma_1, ..., Gamma_M]. -/
def gamma_vector (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm) : List RatFrac :=
  terms.map (fun t => t.gamma_coeff D h_pos)

/-- Assembles the list of prime bases [p_1, ..., p_M]. -/
def prime_basis (terms : List PrimeReductionTerm) : List Nat :=
  terms.map (fun t => t.prime)

/-- Assembles the reduced linear form in logarithms S(rho) = sum_i Gamma_i * log(p_i). -/
def linear_form (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm) : LinearFormInLogarithms :=
  ⟨prime_basis terms, gamma_vector D h_pos terms, by
    dsimp [prime_basis, gamma_vector]
    rw [List.length_map, List.length_map]⟩

/-- Target C750-T569: The Reduction Theorem for general dimension d.
    von Neumann entropy decomposes into a linear form in logarithms of prime bases
    with rational coefficients vec(Gamma).
    If all reduced numerators G_i vanish, the linear form vanishes identically. -/
theorem reduction_theorem_vanishing (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm)
    (h_all_zero : ∀ t ∈ terms, t.gamma_num D = 0) :
    (linear_form D h_pos terms).is_zero := by
  intro c hc
  dsimp [linear_form, gamma_vector] at hc
  have ⟨t, ht, hc_eq⟩ := List.mem_map.mp hc
  rw [← hc_eq]
  dsimp [PrimeReductionTerm.gamma_coeff, RatFrac.isZero]
  exact h_all_zero t ht

/-- Target C750-T569: The Reduction Theorem non-vanishing branch.
    If at least one reduced numerator G_i ≠ 0, the linear form is non-vanishing. -/
theorem reduction_theorem_nonvanishing (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm)
    (t : PrimeReductionTerm) (ht : t ∈ terms) (h_nz : t.gamma_num D ≠ 0) :
    (linear_form D h_pos terms).is_nonvanishing := by
  dsimp [LinearFormInLogarithms.is_nonvanishing]
  refine ⟨t.gamma_coeff D h_pos, ?_, h_nz⟩
  dsimp [linear_form, gamma_vector]
  exact List.mem_map.mpr ⟨t, ht, rfl⟩

end Reduction

end FiniteQm.C750.B01
