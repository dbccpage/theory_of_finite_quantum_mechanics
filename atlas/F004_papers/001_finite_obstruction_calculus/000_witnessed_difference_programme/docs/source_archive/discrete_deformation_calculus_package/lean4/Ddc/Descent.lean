/-
Letter D: descent with a loss ledger. AuthorityEffect: None.
-/
import Ddc.StructuralLift

namespace Ddc

theorem l1_eq_zero_iff (v : List Int) : l1 v = 0 ↔ ∀ x ∈ v, x = 0 := by
  induction v with
  | nil => exact ⟨fun _ x hx => (nomatch hx), fun _ => rfl⟩
  | cons x xs ih =>
    simp only [l1, List.mem_cons, forall_eq_or_imp]
    constructor
    · intro h
      exact ⟨Int.natAbs_eq_zero.1 (by omega), ih.1 (by omega)⟩
    · rintro ⟨hx, hxs⟩
      rw [Int.natAbs_eq_zero.2 hx, ih.2 hxs]

/-- The loss of keeping the first `n` coordinates. -/
def loss (v : List Int) (n : Nat) : Nat := l1 (v.drop n)

/-- DDC-D-02: descent is lossless exactly when the dropped coordinates are zero. -/
theorem D_lossless_iff (v : List Int) (n : Nat) : loss v n = 0 ↔ ∀ x ∈ v.drop n, x = 0 :=
  l1_eq_zero_iff _

/-- DDC-D-03: projecting twice is projecting once. -/
theorem D_projection_idempotent (v : List Int) (n : Nat) : (v.take n).take n = v.take n := by
  rw [List.take_take, Nat.min_self]

/-- Law 6: a lawful descent carries a loss ledger and changes the carrier. -/
theorem D_needs_ledger (b a : State) (w : Witness) (h : stepLaw .D b a w = true) :
    b.carrier ≠ a.carrier ∧ w.ledger = true := law_D.1 h

end Ddc
