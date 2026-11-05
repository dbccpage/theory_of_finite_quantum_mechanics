/-
Letter C: context exposure. AuthorityEffect: None.
-/
import Ddc.Law

namespace Ddc

/-- An edge crosses a window when exactly one endpoint lies inside. -/
def crosses {α : Type} (inW : α → Bool) (u v : α) : Bool := inW u != inW v

/-- DDC-C: the boundary of an intersection of windows lies in the union of boundaries. -/
theorem C_boundary_of_intersection {α : Type} (W₁ W₂ : α → Bool) (u v : α)
    (h : crosses (fun x => W₁ x && W₂ x) u v = true) :
    crosses W₁ u v = true ∨ crosses W₂ u v = true := by
  have key : ∀ a b c d : Bool, ((a && c) != (b && d)) = true → (a != b) = true ∨ (c != d) = true := by
    decide
  exact key (W₁ u) (W₁ v) (W₂ u) (W₂ v) h

/-- Law 8: context exposure is not repair — C never lowers Φ₁ or Γ₂. -/
theorem C_is_not_repair (b a : State) (w : Witness) (h : stepLaw .C b a w = true) :
    b.phi ≤ a.phi ∧ b.gamma ≤ a.gamma := by
  obtain ⟨-, hp, hg⟩ := law_C.1 h
  exact ⟨hp, hg⟩

/-- C changes the carrier. -/
theorem C_changes_carrier (b a : State) (w : Witness) (h : stepLaw .C b a w = true) :
    b.carrier ≠ a.carrier := (law_C.1 h).1

end Ddc
