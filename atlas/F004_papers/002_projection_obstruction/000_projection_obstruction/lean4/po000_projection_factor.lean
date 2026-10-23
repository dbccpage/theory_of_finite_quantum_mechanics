/-
  Finite experiment: a retraction can leave a residual while the
  projected picture stays still. Authorization is an independent bit.
  Not a Banach theorem, not Theorem 5.1, not an authority grant.

  AuthorityEffect: None.
-/

namespace PO000ProjectionFactor

structure State where
  chart : Bool
  leftover : Bool
deriving DecidableEq, Repr

def onSlice (s : State) : Prop := s.leftover = false

def retract (s : State) : State := ⟨s.chart, false⟩

theorem retract_idempotent (s : State) : retract (retract s) = retract s := rfl

theorem retract_lands_on_slice (s : State) : onSlice (retract s) := rfl

/-- Ambient step that writes the leftover. -/
def ambientStep (s : State) : State := ⟨s.chart, true⟩

/-- Prop 3.B shape: the orbit leaves the slice. -/
theorem orbit_leaves (s : State) (_h : onSlice s) :
    ¬ onSlice (ambientStep s) := by
  intro h
  exact Bool.noConfusion h

/-- The projected family is the identity on the slice. -/
theorem projected_identity (s : State) (h : onSlice s) :
    retract (ambientStep s) = s := by
  cases s with
  | mk _ leftover =>
      simp [onSlice] at h
      subst leftover
      rfl

/-- Instantaneous leftover versus projected stillness are different facts. -/
theorem leftover_with_still_picture (s : State) (h : onSlice s) :
    ¬ onSlice (ambientStep s) ∧ retract (ambientStep s) = s :=
  ⟨orbit_leaves s h, projected_identity s h⟩

structure Engine where
  residualPositive : Bool
  authorized : Bool
deriving DecidableEq

/-- A legal engine may see a leftover and still not authorize. -/
def legalUnopened : Engine := ⟨true, false⟩

theorem residual_does_not_entail_authorization :
    ∃ e : Engine, e.residualPositive = true ∧ e.authorized = false :=
  ⟨legalUnopened, rfl, rfl⟩

/-- The illegal collapse: read a leftover as an act. -/
def collapse (residualPositive : Bool) : Bool := residualPositive

theorem collapse_disagrees_with_legal_engine :
    collapse legalUnopened.residualPositive ≠ legalUnopened.authorized := by
  decide

/-- A residual is a coboundary only after an exactness witness. -/
structure Residual where
  value : Bool

structure Adapter where
  witness : Bool

def isCoboundary (_r : Residual) : Option Adapter → Prop
  | none => False
  | some a => a.witness = true

theorem residual_not_coboundary_without_adapter (r : Residual) :
    ¬ isCoboundary r none := fun h => h

end PO000ProjectionFactor

#print axioms PO000ProjectionFactor.orbit_leaves
#print axioms PO000ProjectionFactor.projected_identity
#print axioms PO000ProjectionFactor.residual_does_not_entail_authorization
#print axioms PO000ProjectionFactor.residual_not_coboundary_without_adapter
