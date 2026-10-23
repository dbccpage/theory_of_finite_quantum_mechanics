/-
Letter Λ: licensed structural lift. AuthorityEffect: None.
-/
import Ddc.ExactRepair

namespace Ddc

def l1 : List Int → Nat
  | [] => 0
  | x :: xs => x.natAbs + l1 xs

theorem l1_append (u v : List Int) : l1 (u ++ v) = l1 u + l1 v := by
  induction u with
  | nil => simp [l1]
  | cons x xs ih => simp [l1, ih]; omega

theorem l1_replicate_zero (k : Nat) : l1 (List.replicate k 0) = 0 := by
  induction k with
  | zero => rfl
  | succ n ih => simp [List.replicate, l1, ih]

/-- DDC-L-01: zero-padding preserves the l1 norm. -/
theorem L_pad_preserves_l1 (v : List Int) (k : Nat) : l1 (v ++ List.replicate k 0) = l1 v := by
  rw [l1_append, l1_replicate_zero]
  omega

/-- A lift cannot make a residual exact: if restriction commutes with `d0` and the lifted
residual restricts to the old one, exactness of the lift forces exactness before. -/
theorem L_cannot_exactify (K₀ K₁ : Complex) (ρ0 ρ1 : (Nat → Int) → (Nat → Int))
    (commute : ∀ φ, ρ1 (K₁.d0 φ) = K₀.d0 (ρ0 φ)) (x x' : Nat → Int) (restricts : ρ1 x' = x)
    (h : IsExact K₁ x') : IsExact K₀ x := by
  obtain ⟨φ, hφ⟩ := h
  exact ⟨ρ0 φ, by rw [← commute, hφ, restricts]⟩

/-- Law 4: a lawful lift carries a licence and a trigger. -/
theorem L_needs_licence_and_trigger (b a : State) (w : Witness) (h : stepLaw .L b a w = true) :
    w.licence = true ∧ (b.cls = .closed ∨ b.adequate = false) := by
  obtain ⟨-, hl, ht⟩ := law_L.1 h
  exact ⟨hl, ht⟩

end Ddc
