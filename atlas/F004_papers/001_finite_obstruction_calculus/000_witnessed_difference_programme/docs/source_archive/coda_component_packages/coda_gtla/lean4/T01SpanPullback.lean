import D01D02Records

/-!
# CODA-GTLA T01: Span Pullback Theorems & Two-Level Cost Accounting

Formalizes:
1. Diagonal identity span extensional cost is zero.
2. Composite span cost is subadditive (additive in concrete representation).
3. Identity trace work cost is zero.
4. Trace erasure preserves identity and composition.

AuthorityEffect: None.
-/

namespace CodaGtla

set_option linter.unusedVariables false

/-- Theorem 1.4a: Identity span has zero extensional cost. -/
theorem diagSpan_cost_zero (P : Presentation) : extCost (diagSpan P) = 0 := rfl

/-- Theorem 1.4b: Span pullback composition satisfies subadditive cost bound. -/
theorem compSpan_cost_subadditive {P1 P2 P3 : Presentation}
    (S1 : ComparisonSpan P1 P2) (S2 : ComparisonSpan P2 P3) :
    extCost (compSpan S1 S2) ≤ extCost S1 + extCost S2 := by
  dsimp [extCost, compSpan]
  exact Nat.le_refl _

/-- Identity trace has zero intensional work cost. -/
theorem idTrace_work_zero (P : Presentation) : traceCost (idTrace P) = 0 := rfl

/-- Erasure quotient map preserves identity. -/
theorem eraseTrace_id (P : Presentation) : eraseTrace (idTrace P) = diagSpan P := rfl

/-- Erasure quotient map commutes with composition: q(T1 . T2) = q(T1) * q(T2). -/
theorem eraseTrace_comp {P1 P2 P3 : Presentation}
    (T1 : Trace P1 P2) (T2 : Trace P2 P3) :
    eraseTrace (compTrace T1 T2) = compSpan (eraseTrace T1) (eraseTrace T2) := rfl

end CodaGtla
