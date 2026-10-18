
import PrimitiveDifference



namespace OmegaCore.CochainWindow

structure AddCommGroupCarrier (C : Type) where
  zero : C
  add : C → C → C
  neg : C → C
  add_assoc : ∀ x y z, add (add x y) z = add x (add y z)
  add_comm : ∀ x y, add x y = add y x
  zero_add : ∀ x, add zero x = x
  add_neg : ∀ x, add x (neg x) = zero

theorem AddCommGroupCarrier.add_zero
    (carrier : AddCommGroupCarrier C) (x : C) :
    carrier.add x carrier.zero = x := by
  rw [carrier.add_comm, carrier.zero_add]

structure Window (C0 C1 C2 : Type) where
  c0 : AddCommGroupCarrier C0
  c1 : AddCommGroupCarrier C1
  c2 : AddCommGroupCarrier C2
  d0 : C0 → C1
  d1 : C1 → C2
  d0_zero : d0 c0.zero = c1.zero
  d0_add : ∀ x y, d0 (c0.add x y) = c1.add (d0 x) (d0 y)
  d1_zero : d1 c1.zero = c2.zero
  d1_add : ∀ x y, d1 (c1.add x y) = c2.add (d1 x) (d1 y)
  chain : ∀ x, d1 (d0 x) = c2.zero

variable {C0 C1 C2 : Type}

def repair (window : Window C0 C1 C2) (omega : C1) (alpha : C0) : C1 :=
  window.c1.add omega (window.d0 alpha)

def Exact (window : Window C0 C1 C2) (omega : C1) : Prop :=
  ∃ alpha, repair window omega alpha = window.c1.zero

def Closed (window : Window C0 C1 C2) (omega : C1) : Prop :=
  window.d1 omega = window.c2.zero

def ActiveClosureFailure (window : Window C0 C1 C2) (omega : C1) : Prop :=
  window.d1 omega ≠ window.c2.zero

def ClosedResidual (window : Window C0 C1 C2) (omega : C1) : Prop :=
  Closed window omega ∧ ¬ Exact window omega

theorem closure_repair_invariant
    (window : Window C0 C1 C2) (omega : C1) (alpha : C0) :
    window.d1 (repair window omega alpha) = window.d1 omega := by
  rw [repair, window.d1_add, window.chain, window.c2.add_zero]

theorem exact_implies_closed
    (window : Window C0 C1 C2) (omega : C1)
    (exact : Exact window omega) :
    Closed window omega := by
  rcases exact with ⟨alpha, repaired⟩
  have invariant := closure_repair_invariant window omega alpha
  rw [repaired, window.d1_zero] at invariant
  exact invariant.symm

theorem exact_not_active
    (window : Window C0 C1 C2) (omega : C1)
    (exact : Exact window omega) :
    ¬ ActiveClosureFailure window omega := by
  intro active
  exact active (exact_implies_closed window omega exact)

theorem sector_trichotomy
    (window : Window C0 C1 C2) (omega : C1) :
    Exact window omega ∨
      ActiveClosureFailure window omega ∨
      ClosedResidual window omega := by
  classical
  by_cases exact : Exact window omega
  · exact Or.inl exact
  · by_cases closed : Closed window omega
    · exact Or.inr (Or.inr ⟨closed, exact⟩)
    · exact Or.inr (Or.inl closed)

theorem active_closure_survives_every_repair
    (window : Window C0 C1 C2) (omega : C1)
    (active : ActiveClosureFailure window omega) :
    ∀ alpha, window.d1 (repair window omega alpha) ≠ window.c2.zero := by
  intro alpha
  rw [closure_repair_invariant]
  exact active

#print axioms closure_repair_invariant
#print axioms exact_implies_closed
#print axioms exact_not_active
#print axioms sector_trichotomy
#print axioms active_closure_survives_every_repair

end OmegaCore.CochainWindow

private def l5aProvenance : String :=
  "Origin: lean4/CochainWindow.lean Claim: AddCommGroupCarrier AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
