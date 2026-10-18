/-
  H003 -- reversibility gate. AuthorityEffect: None. Candidate only.
  Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H003
  Source-paper contact: QM_121 rung "reversible dynamics"; work
  order hard obligation 7 (determinism does not imply
  reversibility). E007 toggle fixture reused as the positive case.

  Target proposition
    Reversibility is a supplied two-sided inverse, not a consequence
    of determinism. A reversible report map acts on weight vectors
    by permutation: the pushforward is exactly precomposition with
    the inverse (proved generally). The two-state collapse map is
    deterministic and has no inverse.

  Imports added at this rung
    The inverse map and its two laws (declared data + supplied
    proofs). Nothing else.

  Theorem or counterexample
    collapse_not_reversible: obligation 7 discharged by the exact
    countermodel the work order names ("a two-state map collapsing
    both states to one").
    pushforward_reversible: reversible pushforward = w o inv, so
    counting measure and each weight value are preserved (the H003
    invariant, proved generally, not on a fixture).

  Nonclaim boundary
    No claim that physical dynamics is reversible. No unitarity yet:
    that needs H004+H005+H006 imports. Determinism itself remains a
    modelling choice recorded at H002.

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
-/

import HWKernel

namespace FableHilbertWalk20260819.H003

open FableHilbertWalk20260819.HWKernel

/-- A supplied two-sided inverse: the reversibility import. -/
structure Reversible {Q : Type} (τ : Q → Q) where
  inv : Q → Q
  left : ∀ q : Q, inv (τ q) = q
  right : ∀ q : Q, τ (inv q) = q

/-! ## Positive case: the toggle is reversible. -/

def toggle (q : Bool) : Bool := !q

def toggleRev : Reversible toggle where
  inv := toggle
  left := fun q => by cases q <;> rfl
  right := fun q => by cases q <;> rfl

/-! ## Obligation 7: determinism does not imply reversibility. -/

def collapse (_ : Bool) : Bool := false

theorem collapse_not_reversible : ¬ Nonempty (Reversible collapse) := by
  intro hne
  rcases hne with ⟨R⟩
  have h1 : R.inv false = true := R.left true
  have h2 : R.inv false = false := R.left false
  rw [h1] at h2
  cases h2

#print axioms collapse_not_reversible

/-! ## The H003 invariant: reversible pushforward is precomposition
    with the inverse -- a permutation of weights. -/

/-- Under a two-sided inverse, the fiber of q is exactly {inv q}. -/
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

/-- H003 punchline: reversibility is an import with a two-state
    countermodel, and a reversible map permutes weights. -/
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
