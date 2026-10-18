import DeltoidCuspLiteralSemantics
import DeltoidCuspPhaseReduction

/-!
# Literal matrix overlap obstruction without a phase-gauge assumption

The matrix in these statements is the displayed mission input `D6`, which fails
the repository's Hadamard predicate. The statements do not concern a corrected
deltoid cusp matrix or identify any cusp-family representative.

AuthorityEffect: None.
-/

namespace MUB.DeltoidCuspLiteralVector

open DeltoidCuspInputAudit
open DeltoidCuspPhaseReduction

/-- The literal overlap system has no unit-entry complex vector, without fixing a phase. -/
theorem no_literal_unit_entry_vector (z : Fin 6 → ℂ)
    (hunit : ∀ k, Complex.normSq (z k) = 1)
    (hfourier : ∀ i, Complex.normSq (rowAmplitude F6 z i) = 6)
    (hliteral : ∀ i, Complex.normSq (rowAmplitude D6 z i) = 6) : False := by
  apply DeltoidCuspLiteralSemantics.no_dephased_literal_vector (dephase z)
  · exact dephase_zero z (hunit 0)
  · exact dephase_unit z hunit
  · intro i
    change Complex.normSq (rowAmplitude F6 (dephase z) i) = 6
    rw [dephase_rowAmplitude_normSq F6 z (hunit 0) i]
    exact hfourier i
  · intro i
    change Complex.normSq (rowAmplitude D6 (dephase z) i) = 6
    rw [dephase_rowAmplitude_normSq D6 z (hunit 0) i]
    exact hliteral i

/-- The mission's literal equations in the original normalized-vector convention. -/
theorem no_literal_normalized_vector (u : Fin 6 → ℂ)
    (hunit : ∀ k, Complex.normSq (u k) = 1 / 6)
    (hfourier : ∀ i, Complex.normSq (rowAmplitude F6 u i) = 1)
    (hliteral : ∀ i, Complex.normSq (rowAmplitude D6 u i) = 1) : False := by
  exact no_literal_unit_entry_vector (scaleBySqrtSix u)
    (scaleBySqrtSix_unit u hunit)
    (scaleBySqrtSix_overlaps F6 u hfourier)
    (scaleBySqrtSix_overlaps D6 u hliteral)

#print axioms no_literal_unit_entry_vector
#print axioms no_literal_normalized_vector

end MUB.DeltoidCuspLiteralVector
