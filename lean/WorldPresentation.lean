import PrimitiveDifference

/-!
# F0: finite presentation boundary

This is the scoped Lean completion of frontier-ledger item F0.  It packages a
finite index carrier, PrimitiveDifference/ZeroRel, an admissible subobject,
repairs, an observer-indexed evaluator, witness predicate, terminal type, and
an authority ceiling with no escalating constructor.

It does not derive this presentation from the literal token `<>`.
-/

namespace OmegaWorld

/-- The pure mathematical World has no authority-increasing constructor. -/
inductive AuthorityEffect where
  | none
  deriving DecidableEq

/-- Evaluation either uses a bound observer or refuses explicitly. -/
inductive EvalOrRefuse (Residual : Type) where
  | evaluated (value : Residual)
  | refusedNoObserver
  deriving DecidableEq

/--
A finite declared presentation.  `admissible` is deliberately separate from
the zero relation induced by `primitive`.
-/
structure Presentation where
  presentationId : Nat
  stage : Nat
  carrierSize : Nat
  differenceSize : Nat
  primitive : OmegaCore.PrimitiveDifference (Fin carrierSize) (Fin differenceSize)
  admissible : Fin carrierSize -> Prop
  Repair : Type
  applyRepair : Repair -> Fin carrierSize -> Fin carrierSize
  Residual : Type
  Observer : Type
  observer : Option Observer
  evaluate : Observer -> Fin carrierSize -> Residual
  Witness : Type
  verifies : Witness -> Fin carrierSize -> Residual -> Prop
  Terminal : Type
  authorityEffect : AuthorityEffect
  authority_none : authorityEffect = .none

namespace Presentation

/-- Absence of an observer is data and produces a typed refusal. -/
def evaluateOrRefuse (P : Presentation) (x : Fin P.carrierSize) :
    EvalOrRefuse P.Residual :=
  match P.observer with
  | none => .refusedNoObserver
  | some observer => .evaluated (P.evaluate observer x)

/-- Remove only the observer binding, keeping the remainder of the declaration. -/
def withoutObserver (P : Presentation) : Presentation :=
  { P with observer := none }

theorem withoutObserver_refuses (P : Presentation) (x : Fin P.carrierSize) :
    (P.withoutObserver.evaluateOrRefuse x) = .refusedNoObserver := by
  rfl

/-- Change presentation identity without conflating the raw carrier. -/
def reidentify (P : Presentation) (newId : Nat) : Presentation :=
  { P with presentationId := newId }

theorem reidentify_id (P : Presentation) (newId : Nat) :
    (P.reidentify newId).presentationId = newId := by
  rfl

/-- Two differently identified declarations remain distinct even on one raw carrier. -/
theorem reidentify_ne (P : Presentation) {leftId rightId : Nat}
    (h : leftId ≠ rightId) :
    P.reidentify leftId ≠ P.reidentify rightId := by
  intro presentationsEqual
  apply h
  exact congrArg Presentation.presentationId presentationsEqual

/-- The authority field cannot contain a stronger value. -/
theorem authority_is_none (P : Presentation) :
    P.authorityEffect = .none :=
  P.authority_none

/-- The declared zero relation is exactly the shared-kernel relation. -/
theorem zeroRel_is_declared (P : Presentation) (x y : Fin P.carrierSize) :
    P.primitive.ZeroRel x y = P.primitive.Zero (P.primitive.δ x y) := by
  rfl

end Presentation
end OmegaWorld
