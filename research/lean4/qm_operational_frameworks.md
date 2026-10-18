import Mathlib.Tactic

/-!
# QMOperationalFrameworks — W7.4 (Hardy / MM / CBH crosswalk)

Programme target: DERIV-MASTER W7.4 (path §F.40).

**Job:** typed crosswalk from our finite classical-heart slots to named
operational reconstruction frameworks (Hardy 2001; Masanes–Müller 2011; CBH).
**Not** a reconstruction equivalence theorem.

AuthorityEffect: None.
-/

namespace QM
namespace OperationalFrameworks

/-! ## Framework registry -/

inductive Framework where
  | Hardy2001
  | MasanesMueller2011
  | CBH
  deriving DecidableEq, Repr

def frameworks : List Framework :=
  [.Hardy2001, .MasanesMueller2011, .CBH]

theorem frameworks_card : frameworks.length = 3 := by
  decide

/-! ## Our programme slots -/

inductive OurSlot where
  | FinL1Classical
  | SurplusPhaseInterf
  | ObNoncomm
  | ObUnitary
  | ObClone
  | ContTime
  | LocalTomography
  | ChshRecovery
  | MerminPeres
  | BornSpectralResidual
  | FullHardyAxiomSet
  | FullMmCbhEquivalence
  deriving DecidableEq, Repr

inductive MapStatus where
  | Aligned
  | Partial
  | ResidualOpen
  | NotClaimed
  deriving DecidableEq, Repr

/-! ## Crosswalk as status function (avoid List bang indexing) -/

def mapStatus : OurSlot → MapStatus
  | .FinL1Classical | .ObClone => .Aligned
  | .SurplusPhaseInterf | .ObNoncomm | .ObUnitary | .ContTime
  | .LocalTomography | .ChshRecovery | .MerminPeres => .Partial
  | .BornSpectralResidual => .ResidualOpen
  | .FullHardyAxiomSet | .FullMmCbhEquivalence => .NotClaimed

def primaryFramework : OurSlot → Framework
  | .FinL1Classical | .SurplusPhaseInterf | .MerminPeres
  | .BornSpectralResidual | .FullHardyAxiomSet => .Hardy2001
  | .ObNoncomm | .ObUnitary | .ContTime | .LocalTomography
  | .FullMmCbhEquivalence => .MasanesMueller2011
  | .ObClone | .ChshRecovery => .CBH

def allSlots : List OurSlot :=
  [.FinL1Classical, .ObClone, .SurplusPhaseInterf, .ObNoncomm, .ObUnitary,
   .ContTime, .LocalTomography, .ChshRecovery, .MerminPeres,
   .BornSpectralResidual, .FullHardyAxiomSet, .FullMmCbhEquivalence]

theorem crosswalk_card : allSlots.length = 12 := by
  decide

def slotsWith (s : MapStatus) : List OurSlot :=
  allSlots.filter (fun sl => mapStatus sl = s)

theorem aligned_card : (slotsWith .Aligned).length = 2 := by
  decide

theorem partial_card : (slotsWith .Partial).length = 7 := by
  decide

theorem residual_card : (slotsWith .ResidualOpen).length = 1 := by
  decide

theorem not_claimed_card : (slotsWith .NotClaimed).length = 2 := by
  decide

theorem status_partition :
    (slotsWith .Aligned).length +
    (slotsWith .Partial).length +
    (slotsWith .ResidualOpen).length +
    (slotsWith .NotClaimed).length = allSlots.length := by
  decide

/-! ## Specific honest binds -/

theorem finL1_aligned_hardy :
    mapStatus .FinL1Classical = .Aligned ∧
    primaryFramework .FinL1Classical = .Hardy2001 := by
  decide

theorem clone_aligned_cbh :
    mapStatus .ObClone = .Aligned ∧
    primaryFramework .ObClone = .CBH := by
  decide

theorem lt_partial_mm :
    mapStatus .LocalTomography = .Partial ∧
    primaryFramework .LocalTomography = .MasanesMueller2011 := by
  decide

theorem full_equivalence_not_claimed :
    mapStatus .FullMmCbhEquivalence = .NotClaimed := by
  decide

/-! ## Equivalence fence -/

def reconstructionEquivalenceClaim : Bool := false

theorem equivalence_refused : reconstructionEquivalenceClaim = false := by
  decide

def fullOperationalMap_closed : Bool := false

theorem full_map_open : fullOperationalMap_closed = false := by
  decide

/-! ## Framework coverage -/

theorem hardy_appears : primaryFramework .FinL1Classical = .Hardy2001 := by
  decide

theorem mm_appears : primaryFramework .LocalTomography = .MasanesMueller2011 := by
  decide

theorem cbh_appears : primaryFramework .ObClone = .CBH := by
  decide

/-! ## Main package -/

theorem operational_frameworks_package :
    frameworks.length = 3 ∧
    allSlots.length = 12 ∧
    (slotsWith .Aligned).length = 2 ∧
    (slotsWith .Partial).length = 7 ∧
    (slotsWith .ResidualOpen).length = 1 ∧
    (slotsWith .NotClaimed).length = 2 ∧
    reconstructionEquivalenceClaim = false ∧
    fullOperationalMap_closed = false :=
  ⟨frameworks_card, crosswalk_card, aligned_card, partial_card,
    residual_card, not_claimed_card, rfl, rfl⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end OperationalFrameworks
end QM

#print axioms QM.OperationalFrameworks.crosswalk_card
#print axioms QM.OperationalFrameworks.operational_frameworks_package
#print axioms QM.OperationalFrameworks.finL1_aligned_hardy
#print axioms QM.OperationalFrameworks.equivalence_refused
#print axioms QM.OperationalFrameworks.structure_not_auth
