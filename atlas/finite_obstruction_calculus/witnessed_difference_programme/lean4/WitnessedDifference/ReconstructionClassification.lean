/-
AuthorityEffect: None. Core-only fixed no-go and quotient-factorization proofs.
The general rational positivity/Tsirelson operator theorem is NOT mechanized here.
-/
namespace WitnessedDifference.ReconstructionClassification

/-- A full indicator-preserving classical realization would have a nonnegative
    expectation equal to the signed negative indicator. No carrier enlargement
    can remove this contradiction while preserving that readout. -/
theorem negative_indicator_no_classical_realization
    (expectation : Int) (preserved : expectation = -1)
    (classical_nonnegative : 0 ≤ expectation) : False := by
  have bad : (0 : Int) ≤ -1 := preserved ▸ classical_nonnegative
  exact (by decide : ¬ ((0 : Int) ≤ -1)) bad

theorem signed_countermodel_positive_total : (2 : Int) + (-1) = 1 := by decide

theorem pr_violates_quantum_squared_bound : (4 : Int) * 4 > 8 := by decide

/-- Exact scaled rational witness: (14/5)^2 < 8 and 14/5 > 2. -/
theorem rational_quantum_witness_bound : (14 : Int) * 14 < 8 * (5 * 5) := by decide

theorem rational_quantum_witness_nonclassical : (14 : Int) > 2 * 5 := by decide

/-- With a chosen section of a surjective report map, factorization is equivalent
    to invariance on report fibres. This is the set-level part of the native
    signed-instrument descent classification; it imports no Hilbert structure. -/
theorem factors_of_fibre_invariance {A Q B : Type}
    (report : A → Q) (representative : Q → A)
    (right_inverse : ∀ q, report (representative q) = q)
    (readout : A → B)
    (invariant : ∀ a b, report a = report b → readout a = readout b) :
    ∃ quotient : Q → B, ∀ a, quotient (report a) = readout a := by
  refine ⟨fun q => readout (representative q), ?_⟩
  intro a
  exact invariant (representative (report a)) a (right_inverse (report a))

theorem fibre_invariance_of_factorization {A Q B : Type}
    (report : A → Q) (readout : A → B)
    (quotient : Q → B) (factors : ∀ a, quotient (report a) = readout a) :
    ∀ a b, report a = report b → readout a = readout b := by
  intro a b same
  calc
    readout a = quotient (report a) := (factors a).symm
    _ = quotient (report b) := congrArg quotient same
    _ = readout b := factors b

#print axioms negative_indicator_no_classical_realization
#print axioms signed_countermodel_positive_total
#print axioms pr_violates_quantum_squared_bound
#print axioms rational_quantum_witness_bound
#print axioms rational_quantum_witness_nonclassical
#print axioms factors_of_fibre_invariance
#print axioms fibre_invariance_of_factorization

end WitnessedDifference.ReconstructionClassification
