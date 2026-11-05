/-
Prime Triad Theorems: Admission, Embedding, Continuation, and Bounded Termination.
AuthorityEffect: None.
-/

import Prime.Basic

namespace Prime

/-- OE001-01: Measurement never precedes admission. -/
theorem admission_precedes_measurement (p : Packet) (p' : Packet)
    (h : measure p = some p') : p.admitted = true := by
  unfold measure at h
  split at h
  · assumption
  · contradiction

/-- OE004-02: Phase embedding theorem: admission order embeds order-preservingly into execution order. -/
theorem embedding_order_preserving (e : PhaseEmbedding) (i j : Nat) (hij : i ≤ j) :
    e.toFun i ≤ e.toFun j :=
  e.monotone i j hij

/-- OE003-01: The canonical 9 conjuncts imply the weakened 3-condition summary form. -/
theorem cc9_implies_cc3 (c : CanContinue9) (h : c.evaluate = true) :
    (cc9_to_cc3 c).evaluate = true := by
  unfold CanContinue9.evaluate at h
  unfold cc9_to_cc3
  unfold CanContinue3.evaluate
  exact h

/-- OE003-03: Bounded operational termination: number of ops is at most floor div b / d. -/
theorem ops_le_floor_div (b d n : Nat) (hd : 0 < d) (hn : n * d ≤ b) :
    n ≤ b / d := by
  exact (Nat.le_div_iff_mul_le hd).2 hn

end Prime
