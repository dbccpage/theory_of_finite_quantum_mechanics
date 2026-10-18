/-
  H000 -- finite presented carrier. AuthorityEffect: None.
  Candidate only. Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H000
  Source-paper contact: J011 mini spine (carrier -> presentation map
  -> same-report relation -> quotient); E003 fiberPD; E005
  fiberSetoid. QM_121 rung "finite sector set".

  Target proposition
    A finite carrier X with a declared presentation p : X -> Q packs
    into a presented-carrier record whose same-report relation is a
    PrimitiveDifference zero-relation (trunk contact, not new math).
    Finiteness is a supplied Enum witness, not a theorem.

  Imports added at this rung
    Enum (explicit finite enumeration) from HWKernel. Nothing else:
    no coefficients, no weights, no dynamics.

  Theorem or counterexample
    presented_carrier_replays: the Bool x Bool / fstBool fixture
    packs, and its same-report relation replays the trunk fiberPD.
    no_enum_nat: the infinite carrier Nat admits no Enum, while the
    SAME presentation laws (fiberPD parity) still hold on it -- so
    finiteness is an assumption independent of the presentation
    calculus, exactly as the work order's countermodel demands.

  Nonclaim boundary
    No claim that any physical carrier is finite. No claim that the
    presentation map is canonical (E003 presentation_is_supplied
    already records the opposite). Finiteness of a chosen window is
    an import unless separately derived.

  AuthorityEffect: None
-/

import HWKernel
import Core
import E003_projection_fiber_primitive_difference
import E005_fiber_quotient_equivalence

namespace FableHilbertWalk20260819.H000

open FableHilbertWalk20260819.HWKernel
open GrokPdNight20260814.Core
open GrokPdNight20260814.E003 (fiberPD fiberPD_zeroRel_iff fstBool)
open GrokPdNight20260814.E005 (fiberSetoid)

/-- H000 pack: carrier, declared presentation, and supplied finite
    enumerations for both ends. Finiteness is data, not a theorem. -/
structure PresentedCarrier (X Q : Type) where
  pres : X → Q
  enumX : Enum X
  enumQ : Enum Q

/-- The same-report relation of a presented carrier, spelled as the
    trunk's PrimitiveDifference zero-relation (E003 fiberPD). -/
def sameReport {X Q : Type} (C : PresentedCarrier X Q) (x y : X) : Prop :=
  ZeroRel (fiberPD C.pres) x y

theorem sameReport_iff {X Q : Type} (C : PresentedCarrier X Q) (x y : X) :
    sameReport C x y ↔ C.pres x = C.pres y :=
  fiberPD_zeroRel_iff C.pres x y

/-- Report states are the quotient by the trunk's fiber setoid. -/
def ReportState {X Q : Type} (C : PresentedCarrier X Q) : Type :=
  ResidualQuotient (fiberSetoid C.pres)

/-! ## Positive finite witness: the Bool x Bool trunk fixture packs. -/

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

/-! ## Refusal: finiteness is an assumption. The countermodel keeps
    the SAME presentation laws on an infinite carrier. -/

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

/-- No finite enumeration of Nat exists. -/
theorem no_enum_nat : ¬ Nonempty (Enum Nat) := by
  intro hne
  rcases hne with ⟨E⟩
  have h := le_maxList (E.complete (maxList E.elems + 1))
  omega

#print axioms no_enum_nat

/-- The parity presentation on the infinite carrier still satisfies
    every PrimitiveDifference law: presentation calculus does not
    secretly contain finiteness. -/
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

/-- H000 punchline: the fixture packs and replays the trunk; the
    infinite carrier keeps the presentation laws but has no Enum. -/
theorem finite_presented_carrier :
    sameReport boolFixture (false, false) (false, true) ∧
      ¬ sameReport boolFixture (false, false) (true, false) ∧
      ¬ Nonempty (Enum Nat) ∧
      (ZeroRel parityPD 0 2 ∧ ¬ ZeroRel parityPD 0 1) :=
  ⟨presented_carrier_replays, presented_carrier_separates,
    no_enum_nat, parity_laws_hold⟩

#print axioms finite_presented_carrier

end FableHilbertWalk20260819.H000
