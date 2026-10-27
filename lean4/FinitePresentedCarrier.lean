






import HWKernel
import Core
import ProjectionFiberPrimitiveDifference
import FiberQuotientEquivalence

namespace HilbertWalk.FinitePresentedCarrier

open HilbertWalk.HWKernel
open ProjectionFiber.Core
open ProjectionFiber.E003 (fiberPD fiberPD_zeroRel_iff fstBool)
open ProjectionFiber.E005 (fiberSetoid)

structure PresentedCarrier (X Q : Type) where
  pres : X → Q
  enumX : Enum X
  enumQ : Enum Q

def sameReport {X Q : Type} (C : PresentedCarrier X Q) (x y : X) : Prop :=
  ZeroRel (fiberPD C.pres) x y

theorem sameReport_iff {X Q : Type} (C : PresentedCarrier X Q) (x y : X) :
    sameReport C x y ↔ C.pres x = C.pres y :=
  fiberPD_zeroRel_iff C.pres x y

def ReportState {X Q : Type} (C : PresentedCarrier X Q) : Type :=
  ResidualQuotient (fiberSetoid C.pres)


def boolFixture : PresentedCarrier (Bool × Bool) Bool where
  pres := fstBool
  enumX := enumBoolProd
  enumQ := enumBool

theorem presented_carrier_replays :
    sameReport boolFixture (false, false) (false, true) :=
  (sameReport_iff boolFixture (false, false) (false, true)).mpr rfl

#print axioms presented_carrier_replays

theorem presented_carrier_separates :
    ¬ sameReport boolFixture (false, false) (true, false) := by
  intro h
  have h' := (sameReport_iff boolFixture (false, false) (true, false)).mp h
  cases h'

#print axioms presented_carrier_separates


def maxList : List Nat → Nat
  | [] => 0
  | a :: t => max a (maxList t)

theorem le_maxList {l : List Nat} {x : Nat} (h : x ∈ l) : x ≤ maxList l := by
  induction l with
  | nil => cases h
  | cons a t ih =>
      rcases List.mem_cons.mp h with rfl | ht
      · exact Nat.le_max_left _ _
      · exact Nat.le_trans (ih ht) (Nat.le_max_right _ _)

theorem no_enum_nat : ¬ Nonempty (Enum Nat) := by
  intro hne
  rcases hne with ⟨E⟩
  have h := le_maxList (E.complete (maxList E.elems + 1))
  omega

#print axioms no_enum_nat

def parityPres (n : Nat) : Bool :=
  n % 2 == 1

def parityPD : PrimitiveDifference Nat (Nat × Nat) :=
  fiberPD parityPres

theorem parity_laws_hold :
    ZeroRel parityPD 0 2 ∧ ¬ ZeroRel parityPD 0 1 := by
  constructor
  · exact (fiberPD_zeroRel_iff parityPres 0 2).mpr rfl
  · intro h
    have h' := (fiberPD_zeroRel_iff parityPres 0 1).mp h
    cases h'

#print axioms parity_laws_hold

theorem finite_presented_carrier :
    sameReport boolFixture (false, false) (false, true) ∧
      ¬ sameReport boolFixture (false, false) (true, false) ∧
      ¬ Nonempty (Enum Nat) ∧
      (ZeroRel parityPD 0 2 ∧ ¬ ZeroRel parityPD 0 1) :=
  ⟨presented_carrier_replays, presented_carrier_separates,
    no_enum_nat, parity_laws_hold⟩

#print axioms finite_presented_carrier

end HilbertWalk.FinitePresentedCarrier

private def l5aProvenance : String :=
  "Origin: lean4/FinitePresentedCarrier.lean Claim: sameReport_iff AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
