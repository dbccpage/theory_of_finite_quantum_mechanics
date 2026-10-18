/-!
LT-F — registry-relative minimality ⊬ universal minimality.

Paper: `06_tower_walk_registry_relative_interface_lift.md` §11; `20_…` §6 (O022);
`11_…` final verdict.

Interfaces are modelled by a cost in `ℕ`. `MinimalInRegistry R F` says `F` is a
least-cost row of the *declared* registry `R`; `UniversalMinimal F` says `F` is
least-cost among *all* interfaces. The firewall: registry-relative minimality does
**not** imply universal minimality — a smaller interface can exist outside the
declared registry. This blocks reading the O022 registry-relative result as a
universal uniqueness claim. No authority; Mathlib-free.
-/

namespace QM

/-- `F` is minimal within the declared registry `R` (least cost among its rows). -/
def MinimalInRegistry (R : List Nat) (F : Nat) : Prop :=
  F ∈ R ∧ ∀ G ∈ R, F ≤ G

/-- `F` is minimal among ALL interfaces (universally least cost). -/
def UniversalMinimal (F : Nat) : Prop := ∀ G : Nat, F ≤ G

/-- Registry-relative minimality does not imply universal minimality: there is a
registry in which `F` is minimal yet a strictly smaller interface exists outside it. -/
theorem registry_minimal_not_universal :
    ∃ (R : List Nat) (F : Nat), MinimalInRegistry R F ∧ ¬ UniversalMinimal F := by
  refine ⟨[5, 7], 5, ⟨?_, ?_⟩, ?_⟩
  · decide
  · intro G hG
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hG
    rcases hG with rfl | rfl <;> omega
  · intro h
    have h0 := h 0
    omega

/-- The general non-implication fails: `MinimalInRegistry → UniversalMinimal` does
not hold for all registries. -/
theorem not_registry_implies_universal :
    ¬ (∀ (R : List Nat) (F : Nat), MinimalInRegistry R F → UniversalMinimal F) := by
  intro h
  obtain ⟨R, F, hmin, hnot⟩ := registry_minimal_not_universal
  exact hnot (h R F hmin)

end QM

#print axioms QM.registry_minimal_not_universal
#print axioms QM.not_registry_implies_universal
