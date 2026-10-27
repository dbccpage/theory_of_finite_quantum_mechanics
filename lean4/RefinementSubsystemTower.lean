

namespace HilbertWalk.RefinementSubsystemTower


theorem divisibility_refl (d : Nat) : d ∣ d := by
  exact Nat.dvd_refl d

theorem divisibility_trans {d1 d2 d3 : Nat} (h12 : d1 ∣ d2) (h23 : d2 ∣ d3) : d1 ∣ d3 := by
  exact Nat.dvd_trans h12 h23

theorem multiplicity_composition (d1 k12 k23 : Nat) :
    let d2 := k12 * d1
    let d3 := k23 * d2
    d3 = (k12 * k23) * d1 := by
  dsimp
  rw [← Nat.mul_assoc]
  rw [Nat.mul_comm k23 k12]



theorem dyadic_step_divides (k : Nat) : 2^k ∣ 2^(k + 1) :=
  ⟨2, by rw [Nat.pow_succ, Nat.mul_comm]⟩

theorem dyadic_jump_divides (k m : Nat) : 2^k ∣ 2^(k + m) :=
  ⟨2^m, by rw [Nat.pow_add, Nat.mul_comm]⟩

theorem triadic_step_divides (k : Nat) : 3^k ∣ 3^(k + 1) :=
  ⟨3, by rw [Nat.pow_succ, Nat.mul_comm]⟩



theorem phase_fraction_inequality (d1 d2 : Nat) (_hd1 : d1 > 0) (_hd2 : d2 > 0) (h_ne : d1 ≠ d2) :
    1 * d2 ≠ 1 * d1 := by
  rw [Nat.one_mul, Nat.one_mul]
  exact Ne.symm h_ne

theorem dyadic_step_phase_mismatch : (2 : Nat) ≠ 4 := by decide



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

theorem declared_arrow_labels_differ :
    preservation_for_arrow ArrowClass.UnitalStarHomomorphism ≠
    preservation_for_arrow ArrowClass.CPTPCoarseGrainingChannel := by
  intro h
  nomatch h



inductive CategoricalDirection where
  | ForwardDirectColimit
  | BackwardStateRestrictionSystem
  deriving DecidableEq, Repr

theorem categorical_directions_are_distinct :
    CategoricalDirection.ForwardDirectColimit ≠
    CategoricalDirection.BackwardStateRestrictionSystem := by
  intro h
  nomatch h



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

end HilbertWalk.RefinementSubsystemTower

private def l5aProvenance : String :=
  "Origin: lean4/RefinementSubsystemTower.lean Claim: divisibility_refl AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
