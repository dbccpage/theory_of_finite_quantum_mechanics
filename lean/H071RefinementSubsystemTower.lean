/-
  H071RefinementSubsystemTower.lean
  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)

  Campaign C500 Block 04: Refinement Arrows and Coherent Finite Towers.
  Scope: arithmetic on dimension indices and distinctions between declared
  labels. This file contains no matrix algebras, channels, states, roots of
  unity or analytic limits; those mathematical bridges remain open here.
  Arithmetic/label inventory:
  1. Divisibility preorder and category of finite dimension indices:
       d1 | d2 reflexive and transitive.
  2. Multiplicity factor composition law:
       (d2 / d1) * (d3 / d2) = (d3 / d1) for d1 | d2 and d2 | d3.
  3. Arrow class distinctions:
       Labels for algebra embeddings, coarse-graining channels and generator maps.
  4. Phase mismatch obstruction:
       The natural-number cross products for 1/d1 and 1/d2 differ when d1 != d2.
  5. Distinct labels for direct and inverse system directions.
-/

namespace FableHilbertWalk20260819.H071

-- ===========================================================================
-- Section 1: Divisibility Index Preorder and Category Laws
-- ===========================================================================

/-- Reflexivity of divisibility: identity arrow for dimension d. -/
theorem divisibility_refl (d : Nat) : d ∣ d := by
  exact Nat.dvd_refl d

/-- Transitivity of divisibility: composition of refinement arrows d1 | d2 and d2 | d3. -/
theorem divisibility_trans {d1 d2 d3 : Nat} (h12 : d1 ∣ d2) (h23 : d2 ∣ d3) : d1 ∣ d3 := by
  exact Nat.dvd_trans h12 h23

/-- Exact multiplicity factor composition law for block-diagonal embeddings:
    If d1 > 0, d2 = k12 * d1, and d3 = k23 * d2, then d3 = (k12 * k23) * d1. -/
theorem multiplicity_composition (d1 k12 k23 : Nat) :
    let d2 := k12 * d1
    let d3 := k23 * d2
    d3 = (k12 * k23) * d1 := by
  dsimp
  rw [← Nat.mul_assoc]
  rw [Nat.mul_comm k23 k12]


-- ===========================================================================
-- Section 2: Concrete Prime-Power Towers (Dyadic and Triadic)
-- ===========================================================================

/-- Dyadic refinement step: 2^k divides 2^(k+1). -/
theorem dyadic_step_divides (k : Nat) : 2^k ∣ 2^(k + 1) :=
  ⟨2, by rw [Nat.pow_succ, Nat.mul_comm]⟩

/-- Dyadic jump: 2^k divides 2^(k+m). -/
theorem dyadic_jump_divides (k m : Nat) : 2^k ∣ 2^(k + m) :=
  ⟨2^m, by rw [Nat.pow_add, Nat.mul_comm]⟩

/-- Triadic step: 3^k divides 3^(k+1). -/
theorem triadic_step_divides (k : Nat) : 3^k ∣ 3^(k + 1) :=
  ⟨3, by rw [Nat.pow_succ, Nat.mul_comm]⟩


-- ===========================================================================
-- Section 3: Phase Mismatch Obstruction for Generator Preservation
-- ===========================================================================

/-- Inequality of natural-number cross products; no roots of unity or
    homomorphism obstruction are represented in this statement. -/
theorem phase_fraction_inequality (d1 d2 : Nat) (_hd1 : d1 > 0) (_hd2 : d2 > 0) (h_ne : d1 ≠ d2) :
    1 * d2 ≠ 1 * d1 := by
  rw [Nat.one_mul, Nat.one_mul]
  exact Ne.symm h_ne

/-- Explicit obstruction for dyadic step 2 to 4: 2 != 4. -/
theorem dyadic_step_phase_mismatch : (2 : Nat) ≠ 4 := by decide


-- ===========================================================================
-- Section 4: Arrow Class Typings
-- ===========================================================================

inductive ArrowClass where
  | UnitalStarHomomorphism
  | CPTPCoarseGrainingChannel
  | GeneratorPreservingMap
  deriving DecidableEq, Repr

inductive ArrowPreservation where
  | ObservableAlgebraEmbedding
  | IrreversibleStateContraction
  | ObstructedByPhaseMismatch
  deriving DecidableEq, Repr

def preservation_for_arrow : ArrowClass → ArrowPreservation
  | ArrowClass.UnitalStarHomomorphism => ArrowPreservation.ObservableAlgebraEmbedding
  | ArrowClass.CPTPCoarseGrainingChannel => ArrowPreservation.IrreversibleStateContraction
  | ArrowClass.GeneratorPreservingMap => ArrowPreservation.ObstructedByPhaseMismatch

/-- Two authored arrow-preservation labels differ; no state preservation theorem. -/
theorem declared_arrow_labels_differ :
    preservation_for_arrow ArrowClass.UnitalStarHomomorphism ≠
    preservation_for_arrow ArrowClass.CPTPCoarseGrainingChannel := by
  intro h
  nomatch h


-- ===========================================================================
-- Section 5: Declared Direct and State-Restriction Direction Labels
-- ===========================================================================

inductive CategoricalDirection where
  | ForwardDirectColimit
  | BackwardStateRestrictionSystem
  deriving DecidableEq, Repr

theorem categorical_directions_are_distinct :
    CategoricalDirection.ForwardDirectColimit ≠
    CategoricalDirection.BackwardStateRestrictionSystem := by
  intro h
  nomatch h


-- ===========================================================================
-- Section 6: Axiom Census & Auditing
-- ===========================================================================

#print axioms divisibility_refl
#print axioms divisibility_trans
#print axioms multiplicity_composition
#print axioms dyadic_step_divides
#print axioms dyadic_jump_divides
#print axioms triadic_step_divides
#print axioms phase_fraction_inequality
#print axioms dyadic_step_phase_mismatch
#print axioms declared_arrow_labels_differ
#print axioms categorical_directions_are_distinct

end FableHilbertWalk20260819.H071
