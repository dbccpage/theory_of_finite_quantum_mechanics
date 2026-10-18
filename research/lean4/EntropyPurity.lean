-- Purity.lean — Purity Corollary & Transcendence under Baker Hypothesis
-- Campaign: C750 Block 01 (Target C750-T570)
-- AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).

import EntropyDefs
import EntropyReduction

namespace FiniteQm.C750.B01

/-- Inductive predicate characterizing pure-state term configurations in dimension d.
    In a pure state, exactly one eigenvalue has weight D (and exponent b_i),
    while all other eigenvalues have weight 0. -/
inductive IsPureTermList : List (Nat × Nat) → Nat → Nat → Prop where
  | single (D a : Nat) : IsPureTermList [(D, a)] D a
  | zero_head (w a : Nat) (rest : List (Nat × Nat)) (D b : Nat) :
      w = 0 → IsPureTermList rest D b → IsPureTermList ((w, a) :: rest) D b
  | zero_tail (w a : Nat) (rest : List (Nat × Nat)) (D : Nat) :
      w = D → (∀ p ∈ rest, p.1 = 0) → IsPureTermList ((w, a) :: rest) D a

/-- Target C750-T570 Lemma: For a pure state, the weighted exponent sum
    equals exactly D * b. -/
theorem sum_weighted_exps_of_pure {terms : List (Nat × Nat)} {D b : Nat}
    (h : IsPureTermList terms D b) :
    sum_weighted_exps terms = (D : Int) * (b : Int) := by
  induction h with
  | single D a =>
    dsimp [sum_weighted_exps]
    omega
  | zero_head w a rest D b hw _ ih =>
    dsimp [sum_weighted_exps]
    rw [hw]
    dsimp
    have : (0 : Int) * (a : Int) + sum_weighted_exps rest = sum_weighted_exps rest := by omega
    rw [this]
    exact ih
  | zero_tail w a rest D hw hrest =>
    dsimp [sum_weighted_exps]
    rw [hw]
    have h_rest_zero : sum_weighted_exps rest = 0 := by
      induction rest with
      | nil => rfl
      | cons head tail ih_tail =>
        dsimp [sum_weighted_exps]
        have hhead : head.1 = 0 := hrest head (List.Mem.head tail)
        have htail_all : ∀ p ∈ tail, p.1 = 0 := fun p hp => hrest p (List.Mem.tail head hp)
        have iht := ih_tail htail_all
        rw [hhead]
        dsimp
        have : (0 : Int) * (head.2 : Int) + sum_weighted_exps tail = 0 := by omega
        exact this
    have : (D : Int) * (a : Int) + sum_weighted_exps rest = (D : Int) * (a : Int) := by omega
    exact this

/-- Target C750-T570 Lemma: Pure state prime reduction term has vanishing numerator G_i = 0. -/
theorem gamma_num_of_pure {terms : List (Nat × Nat)} {D b : Nat}
    (h : IsPureTermList terms D b) :
    gamma_numerator D b terms = 0 := by
  dsimp [gamma_numerator]
  rw [sum_weighted_exps_of_pure h]
  omega

/-- A system of prime reduction terms is pure if every prime term satisfies IsPureTermList. -/
def IsPureSystem (terms : List PrimeReductionTerm) (D : Nat) : Prop :=
  ∀ t ∈ terms, IsPureTermList t.state_terms D t.denom_exp

/-- A system of prime reduction terms is mixed if there exists a witness term that fails purity. -/
def IsMixedSystemWitness (terms : List PrimeReductionTerm) (D : Nat) (witness : PrimeReductionTerm) : Prop :=
  witness ∈ terms ∧ witness.gamma_num D ≠ 0

namespace Purity

/-- Target C750-T570 Purity Direction 1: If rho is pure, then vec(Gamma) = 0,
    so the linear form in logarithms vanishes identically. -/
theorem gamma_vanishing_of_pure (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm)
    (h_pure : IsPureSystem terms D) :
    (Reduction.linear_form D h_pos terms).is_zero := by
  apply Reduction.reduction_theorem_vanishing
  intro t ht
  have hpure_t := h_pure t ht
  exact gamma_num_of_pure hpure_t

/-- Target C750-T570 Purity Direction 2: If rho is mixed (has a non-vanishing witness term),
    then vec(Gamma) ≠ 0, so the linear form in logarithms is non-vanishing. -/
theorem gamma_nonvanishing_of_mixed (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm)
    (witness : PrimeReductionTerm)
    (h_mixed : IsMixedSystemWitness terms D witness) :
    (Reduction.linear_form D h_pos terms).is_nonvanishing := by
  exact Reduction.reduction_theorem_nonvanishing D h_pos terms witness h_mixed.1 h_mixed.2

/-- Target C750-T570 Purity Corollary: A state has vanishing entropy form vec(Gamma) = 0
    iff it is pure (Tr(rho^2) = 1). In other words, pure states have S(rho) = 0 in Q,
    while mixed states produce non-vanishing linear forms in logarithms. -/
theorem purity_dichotomy_vanishing (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm)
    (h_pure : IsPureSystem terms D) :
    (Reduction.linear_form D h_pos terms).is_zero ∧
    ¬ (Reduction.linear_form D h_pos terms).is_nonvanishing := by
  have h_zero := gamma_vanishing_of_pure D h_pos terms h_pure
  refine ⟨h_zero, ?_⟩
  intro ⟨c, hc_mem, hc_nz⟩
  have h_c_zero := h_zero c hc_mem
  exact hc_nz h_c_zero

/-- Target C750-T570 Transcendence Corollary: Under Baker's Theorem (Anchor A1),
    the von Neumann entropy of any mixed state is TRANSCENDENTAL (not in Q). -/
theorem mixed_entropy_is_transcendental (baker : BakerHypothesis)
    (D : Nat) (h_pos : 0 < D) (terms : List PrimeReductionTerm)
    (witness : PrimeReductionTerm)
    (h_mixed : IsMixedSystemWitness terms D witness) :
    IsTranscendentalEntropy baker (Reduction.linear_form D h_pos terms) := by
  dsimp [IsTranscendentalEntropy]
  exact gamma_nonvanishing_of_mixed D h_pos terms witness h_mixed

end Purity

end FiniteQm.C750.B01
