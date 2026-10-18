
import PrimitiveDifference




namespace OmegaWorld

inductive AuthorityEffect where
  | none
  deriving DecidableEq

inductive EvalOrRefuse (Residual : Type) where
  | evaluated (value : Residual)
  | refusedNoObserver
  deriving DecidableEq

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

def evaluateOrRefuse (P : Presentation) (x : Fin P.carrierSize) :
    EvalOrRefuse P.Residual :=
  match P.observer with
  | none => .refusedNoObserver
  | some observer => .evaluated (P.evaluate observer x)

def withoutObserver (P : Presentation) : Presentation :=
  { P with observer := none }

theorem withoutObserver_refuses (P : Presentation) (x : Fin P.carrierSize) :
    (P.withoutObserver.evaluateOrRefuse x) = .refusedNoObserver := by
  rfl

def reidentify (P : Presentation) (newId : Nat) : Presentation :=
  { P with presentationId := newId }

theorem reidentify_id (P : Presentation) (newId : Nat) :
    (P.reidentify newId).presentationId = newId := by
  rfl

theorem reidentify_ne (P : Presentation) {leftId rightId : Nat}
    (h : leftId ≠ rightId) :
    P.reidentify leftId ≠ P.reidentify rightId := by
  intro presentationsEqual
  apply h
  exact congrArg Presentation.presentationId presentationsEqual

theorem authority_is_none (P : Presentation) :
    P.authorityEffect = .none :=
  P.authority_none

theorem zeroRel_is_declared (P : Presentation) (x y : Fin P.carrierSize) :
    P.primitive.ZeroRel x y = P.primitive.Zero (P.primitive.δ x y) := by
  rfl

end Presentation
end OmegaWorld

private def l5aProvenance : String :=
  "Origin: lean4/WorldPresentation.lean Claim: withoutObserver_refuses AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
