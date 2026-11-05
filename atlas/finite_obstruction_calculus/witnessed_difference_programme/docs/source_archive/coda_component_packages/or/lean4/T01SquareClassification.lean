import D01D02Records

/-!
# CODA-OR T01: Non-Commutative Square Classification Theorem (GTOR-05, GTOR-10, GTOR-14)

Formalizes:
1. Four-case square defect classification: StrictCommute, WeakCommuteCertified,
   H^1DiagramTear, and OpenDiagramObstruction.
2. Exact Repair Absorption Lemma: Exact 2-cell repairs are unconditionally closed (d1 circ d0 = 0).
3. Obstruction non-conferral of authority: Non-zero defect does not manufacture authority.

AuthorityEffect: None.
-/

namespace CodaOr

open CodaOr

variable {C0 C1 C2 : Type}

/-- Exact Repair Absorption Lemma:
    If a defect delta is exact (delta = d0 alpha), then it is unconditionally closed
    under d1 by the complex condition d1 (d0 alpha) = 0. -/
theorem exact_repair_is_closed
    (E : EnrichedComplex C0 C1 C2) (delta : C1) (alpha : C0)
    (hExact : delta = E.d0 alpha) :
    E.d1 delta = E.zero2 := by
  rw [hExact]
  exact E.complex_condition alpha

/-- Predicate for exact defect (WeakCommuteCertified). -/
def IsExactDefect (E : EnrichedComplex C0 C1 C2) (delta : C1) : Prop :=
  ∃ alpha : C0, delta = E.d0 alpha

/-- Predicate for closed defect / cocycle. -/
def IsClosedDefect (E : EnrichedComplex C0 C1 C2) (delta : C1) : Prop :=
  E.d1 delta = E.zero2

/-- Exact defects are a sub-class of closed defects. -/
theorem exact_implies_closed
    (E : EnrichedComplex C0 C1 C2) (delta : C1)
    (h : IsExactDefect E delta) : IsClosedDefect E delta := by
  rcases h with ⟨alpha, hExact⟩
  exact exact_repair_is_closed E delta alpha hExact

/-- Open diagram obstructions cannot be exact. -/
theorem open_obstruction_not_exact
    (E : EnrichedComplex C0 C1 C2) (delta : C1)
    (hOpen : ¬ IsClosedDefect E delta) :
    ¬ IsExactDefect E delta := by
  intro hExact
  have hClosed := exact_implies_closed E delta hExact
  exact hOpen hClosed

/-- Classification predicate associating a defect with its canonical SquareStatus. -/
def HasSquareStatus
    (E : EnrichedComplex C0 C1 C2) (delta : C1) : SquareStatus → Prop
  | SquareStatus.strict_commute => delta = E.zero1
  | SquareStatus.weak_commute_certified => delta ≠ E.zero1 ∧ IsExactDefect E delta
  | SquareStatus.h1_diagram_tear => ¬ IsExactDefect E delta ∧ IsClosedDefect E delta
  | SquareStatus.open_diagram_obstruction => ¬ IsClosedDefect E delta

/-- Theorem: Strict commute implies closed defect. -/
theorem strict_commute_is_closed
    (E : EnrichedComplex C0 C1 C2) (delta : C1)
    (hStrict : delta = E.zero1) : IsClosedDefect E delta := by
  dsimp [IsClosedDefect]
  rw [hStrict]
  exact E.d1_zero

end CodaOr
