/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/GenesisContinuation.lean
   Original sha256: e22188ab63e6d5903267e9d78a5b55345d5ab518963466aade208217f010a1db (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.GenesisContinuation
   Reason         : genesis
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Std

/-!
Protected futures for a declared partial transition system. These are generic
mathematical theorems, not a verification of Rust, finite enumeration, or the
Genesis source port. No quantum or universal-machine premise is introduced.
-/
namespace GenesisContinuation

def run (step : S → I → Option S) : Option S → List I → Option S
  | s, [] => s
  | s, a :: w => run step (s.bind (fun t => step t a)) w

theorem run_append (step : S → I → Option S) (s : Option S) (u v : List I) :
    run step s (u ++ v) = run step (run step s u) v := by
  induction u generalizing s with
  | nil => rfl
  | cons a w ih => exact ih _

def Related (r : S → S → Prop) : Option S → Option S → Prop
  | none, none => True
  | some s, some t => r s t
  | _, _ => False

def Stable (r : S → S → Prop) (step : S → I → Option S) : Prop :=
  ∀ s t, r s t → ∀ a, Related r (step s a) (step t a)

theorem stable_run (step : S → I → Option S) (r : S → S → Prop)
    (stable : Stable r step) (s t : Option S) (h : Related r s t) (w : List I) :
    Related r (run step s w) (run step t w) := by
  induction w generalizing s t with
  | nil => exact h
  | cons a w ih =>
    apply ih
    cases s with
    | none => cases t <;> simp_all [Related]
    | some s =>
      cases t with
      | none => exact False.elim h
      | some t => exact stable s t h a

def FutureEq (step : S → I → Option S) (observe : S → A) (s t : S) : Prop :=
  ∀ w, (run step (some s) w).map observe = (run step (some t) w).map observe

theorem stable_preserves_futures (step : S → I → Option S) (observe : S → A)
    (r : S → S → Prop) (stable : Stable r step)
    (answers : ∀ s t, r s t → observe s = observe t) (s t : S) (h : r s t) :
    FutureEq step observe s t := by
  intro w
  have hr := stable_run step r stable (some s) (some t) h w
  cases hs : run step (some s) w <;> cases ht : run step (some t) w <;>
    simp_all [Related]
  exact answers _ _ hr

theorem future_eq_observes (h : FutureEq step observe s t) : observe s = observe t := by
  have := h []
  simpa [run] using this

theorem future_eq_stable (step : S → I → Option S) (observe : S → A) :
    Stable (FutureEq step observe) step := by
  intro s t h a
  cases hs : step s a with
  | none =>
    cases ht : step t a with
    | none => trivial
    | some t' =>
      have hh := h [a]
      simp [run, hs, ht] at hh
  | some s' =>
    cases ht : step t a with
    | none =>
      have hh := h [a]
      simp [run, hs, ht] at hh
    | some t' =>
      intro w
      have hh := h (a :: w)
      simpa [run, hs, ht] using hh

/- The preceding two directions characterize the greatest answer-preserving
stable relation. In a finite closed carrier Moore refinement computes it.
That last algorithmic termination/minimality statement is not proved here. -/

def futureSetoid (step : S → I → Option S) (observe : S → A) : Setoid S where
  r := FutureEq step observe
  iseqv := {
    refl := fun _ _ => rfl
    symm := fun h w => (h w).symm
    trans := fun h k w => (h w).trans (k w)
  }

abbrev Carrier (step : S → I → Option S) (observe : S → A) :=
  Quotient (futureSetoid step observe)

def carrierAnswer (step : S → I → Option S) (observe : S → A) :
    Carrier step observe → A :=
  Quotient.lift observe (fun _ _ h => future_eq_observes h)

def carrierStep (step : S → I → Option S) (observe : S → A) (a : I) :
    Carrier step observe → Option (Carrier step observe) :=
  Quotient.lift (fun s => (step s a).map (Quotient.mk (futureSetoid step observe))) (by
    intro s t h
    have hh := future_eq_stable step observe s t h a
    cases hs : step s a <;> cases ht : step t a <;> simp_all [Related]
    exact Quotient.sound hh)

theorem carrier_step_descends (step : S → I → Option S) (observe : S → A)
    (a : I) (s : S) :
    carrierStep step observe a (Quotient.mk _ s) =
      (step s a).map (Quotient.mk (futureSetoid step observe)) := rfl

theorem carrier_answer_descends (step : S → I → Option S) (observe : S → A) (s : S) :
    carrierAnswer step observe (Quotient.mk _ s) = observe s := rfl

theorem no_extension_iff (admitted : H → Prop) (fits : H → Prop) :
    (¬ ∃ h, admitted h ∧ fits h) ↔ ∀ h, admitted h → ¬ fits h := by
  constructor
  · intro h x ha hm; exact h ⟨x, ha, hm⟩
  · intro h ⟨x, ha, hm⟩; exact h x ha hm

theorem fact_requires_nonempty_fiber (fiber : H → Prop) (claim : H → Prop)
    (inhabited : ∃ h, fiber h) (constant_true : ∀ h, fiber h → claim h) :
    ∃ h, fiber h ∧ claim h := by
  obtain ⟨h, hf⟩ := inhabited
  exact ⟨h, hf, constant_true h hf⟩

#print axioms stable_preserves_futures
#print axioms future_eq_stable
#print axioms run_append
#print axioms no_extension_iff
#print axioms fact_requires_nonempty_fiber
#print axioms carrierStep
#print axioms carrier_step_descends
#print axioms carrier_answer_descends
end GenesisContinuation
