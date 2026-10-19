






import HWKernel

namespace FableHilbertWalk20260819.H003

open FableHilbertWalk20260819.HWKernel

structure Reversible {Q : Type} (τ : Q → Q) where
  inv : Q → Q
  left : ∀ q : Q, inv (τ q) = q
  right : ∀ q : Q, τ (inv q) = q


def toggle (q : Bool) : Bool := !q

def toggleRev : Reversible toggle where
  inv := toggle
  left := fun q => by cases q <;> rfl
  right := fun q => by cases q <;> rfl


def collapse (_ : Bool) : Bool := false

theorem collapse_not_reversible : ¬ Nonempty (Reversible collapse) := by
  intro hne
  rcases hne with ⟨R⟩
  have h1 : R.inv false = true := R.left true
  have h2 : R.inv false = false := R.left false
  rw [h1] at h2
  cases h2

#print axioms collapse_not_reversible


theorem pushforward_reversible {Q : Type} [DecidableEq Q]
    (E : Enum Q) (τ : Q → Q) (R : Reversible τ) (w : Q → Int) (q : Q) :
    rsum intPack ((E.elems.filter (fun x => τ x == q)).map w) =
      w (R.inv q) := by
  have hpred : ∀ x ∈ E.elems, (τ x == q) = (x == R.inv q) := by
    intro x _
    by_cases hx : x = R.inv q
    · subst hx
      rw [R.right q, beq_self_eq_true, beq_self_eq_true]
    · have hτ : τ x ≠ q := by
        intro h
        exact hx (by rw [← R.left x, h])
      rw [beq_eq_false_iff_ne.mpr hτ, beq_eq_false_iff_ne.mpr hx]
  rw [filter_congr_mem hpred,
    rsum_filter_key intPack w (E.complete (R.inv q)) E.nodup,
    intPack.add_zero]

#print axioms pushforward_reversible

theorem reversibility_gate :
    (toggleRev.inv = toggle) ∧
      ¬ Nonempty (Reversible collapse) ∧
      (∀ (w : Bool → Int) (q : Bool),
        rsum intPack
          ((enumBool.elems.filter (fun x => toggle x == q)).map w) =
        w (toggle q)) :=
  ⟨rfl, collapse_not_reversible,
    fun w q => pushforward_reversible enumBool toggle toggleRev w q⟩

#print axioms reversibility_gate

end FableHilbertWalk20260819.H003

private def l5aProvenance : String :=
  "Origin: lean4/H003ReversibilityGate.lean Claim: collapse_not_reversible AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
