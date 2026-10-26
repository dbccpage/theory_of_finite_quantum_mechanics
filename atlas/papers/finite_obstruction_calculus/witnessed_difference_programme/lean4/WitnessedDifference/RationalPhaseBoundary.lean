import Lean.Elab.Tactic.Omega

/- AuthorityEffect: None. Lean-distribution core only: no Mathlib, no rational-field axioms.
   Integer path telescoping is proved generally; the native rational-turn owner
   separately implements exact Q/Z arithmetic and cyclotomic evaluation. -/
namespace WitnessedDifference.RationalPhaseBoundary

/-- Coboundary contributions on a two-step path cancel at the middle vertex. -/
theorem path_coboundary_telescopes (a b f0 f1 f2 : Int) :
    (a + (f1-f0)) + (b + (f2-f1)) = (a+b) + (f2-f0) := by omega

/-- Closed three-edge holonomy survives the same gauge action. -/
theorem triangular_holonomy_gauge_invariant (a b c f0 f1 f2 : Int) :
    (a+(f1-f0)) + (b+(f2-f1)) - (c+(f2-f0)) = a+b-c := by omega

/-- An explicitly declared character carries the established telescoping
    equality to the phase carrier. No character or scalar tower is inferred. -/
theorem declared_character_carries_path_identity {Phase : Type}
    (character : Int → Phase) (a b f0 f1 f2 : Int) :
    character ((a + (f1-f0)) + (b + (f2-f1))) =
    character ((a+b) + (f2-f0)) := by
  exact congrArg character (path_coboundary_telescopes a b f0 f1 f2)

/-- For norms (1,4), normalized quadratic and quartic first probabilities
    are 1/5 and 1/17; equality would force the false cross-product 17=5. -/
theorem normalized_readouts_have_distinct_cross_products : (17 : Int) ≠ 5 := by decide

theorem both_normalization_denominators_positive : (0 : Int) < 5 ∧ 0 < 17 := by decide

#print axioms path_coboundary_telescopes
#print axioms triangular_holonomy_gauge_invariant
#print axioms declared_character_carries_path_identity
#print axioms normalized_readouts_have_distinct_cross_products
#print axioms both_normalization_denominators_positive

end WitnessedDifference.RationalPhaseBoundary
