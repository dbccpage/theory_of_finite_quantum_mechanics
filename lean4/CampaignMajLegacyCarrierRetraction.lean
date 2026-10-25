-- Campaign: MAJ-LEGACY-CARRIER-RETRACTION. Not a default target.
-- Identity coboundary on Fin t → Bool. Sizes 1, 2, 3 and 4 are the standing window.
-- The missing tetron_carrier.py measurement stays outside this module.

abbrev V (t : Nat) := Fin t → Bool

def zero1 : V 1 := fun _ => false

def d0 {t : Nat} (a : V t) : V t := a

def d1 {t : Nat} (_w : V t) : V 1 := zero1

def isExact {t : Nat} (w : V t) : Prop :=
  ∃ a : V t, d0 a = w

def isCocycle {t : Nat} (w : V t) : Prop :=
  d1 w = zero1

def isClosed {t : Nat} (w : V t) : Prop :=
  isCocycle w ∧ ¬ isExact w

theorem d0_id {t : Nat} (a : V t) : d0 a = a := rfl

theorem nilpotent {t : Nat} (a : V t) : d1 (d0 a) = zero1 := rfl

theorem all_cocycle {t : Nat} (w : V t) : isCocycle w := rfl

theorem all_exact {t : Nat} (w : V t) : isExact w :=
  ⟨w, rfl⟩

theorem no_closed {t : Nat} (w : V t) : ¬ isClosed w := by
  intro h
  exact h.2 (all_exact w)

theorem window_no_closed :
    (∀ w : V 1, ¬ isClosed w) ∧
    (∀ w : V 2, ¬ isClosed w) ∧
    (∀ w : V 3, ¬ isClosed w) ∧
    (∀ w : V 4, ¬ isClosed w) := by
  exact ⟨fun w => no_closed w, fun w => no_closed w, fun w => no_closed w, fun w => no_closed w⟩

#print axioms d0_id
#print axioms nilpotent
#print axioms all_cocycle
#print axioms all_exact
#print axioms no_closed
#print axioms window_no_closed
