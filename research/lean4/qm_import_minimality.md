import Mathlib.Tactic

/-!
# QMImportMinimality — W6.22 (B₄ + full-ops pathway minimality)

Programme target: DERIV-MASTER W6.22 (path §E.35).

**Job:** show working basis $B_4$ is **minimal** for the independence /
sufficiency-skeleton package, and that the **full-ops pathway package**
(10 named flags, including provisional B5 herm) is pathway-minimal:
dropping any named package flag loses at least one freeze-target /
provisional pathway row (registry-relative).

**Herm residual (this fire):** `hasHermImport` is the optional 10th full-ops
flag (provisional OB-HERM / B5). Drop-herm loses pathway target `T_HERM`
(dynamics herm path). Herm is **not** in $B_4$ capital; sealed B5 herm
minimality remains OPEN.

**Not claimed:** final $N$; absolute minimal generator of all freeze targets as
sealed theorems; completeness audit (W6.23); authority; Wave-6 exit.

AuthorityEffect: None.
-/

namespace QM
namespace ImportMinimality

/-! ## Working basis labels (B₄ capital) -/

inductive ImportSlot where
  | OB_NONCOMM
  | OB_UNITARY
  | OB_CLONE
  | CONT_TIME
  deriving DecidableEq, Repr

def workingBasis : List ImportSlot :=
  [.OB_NONCOMM, .OB_UNITARY, .OB_CLONE, .CONT_TIME]

theorem workingBasis_card : workingBasis.length = 4 := by
  decide

/-! ## Feature package (boolean presence of each B₄ import) -/

structure FeaturePackage where
  noncomm : Bool
  unitary : Bool
  noClone : Bool
  contTime : Bool
  deriving DecidableEq, Repr

def admits (p : FeaturePackage) : ImportSlot → Bool
  | .OB_NONCOMM => p.noncomm
  | .OB_UNITARY => p.unitary
  | .OB_CLONE => p.noClone
  | .CONT_TIME => p.contTime

/-- Full $B_4$ package. -/
def fullB4 : FeaturePackage :=
  { noncomm := true, unitary := true, noClone := true, contTime := true }

def dropNoncomm : FeaturePackage :=
  { noncomm := false, unitary := true, noClone := true, contTime := true }

def dropUnitary : FeaturePackage :=
  { noncomm := true, unitary := false, noClone := true, contTime := true }

def dropClone : FeaturePackage :=
  { noncomm := true, unitary := true, noClone := false, contTime := true }

def dropContTime : FeaturePackage :=
  { noncomm := true, unitary := true, noClone := true, contTime := false }

theorem full_package_admits_all :
    admits fullB4 .OB_NONCOMM = true ∧
    admits fullB4 .OB_UNITARY = true ∧
    admits fullB4 .OB_CLONE = true ∧
    admits fullB4 .CONT_TIME = true := by
  decide

/-- Slot $s$ is load-bearing: full admits $s$, drop-$s$ does not. -/
def loadBearing (s : ImportSlot) (dropped : FeaturePackage) : Prop :=
  admits fullB4 s = true ∧ admits dropped s = false

theorem drop_noncomm_minimal :
    loadBearing .OB_NONCOMM dropNoncomm := by
  constructor <;> rfl

theorem drop_unitary_minimal :
    loadBearing .OB_UNITARY dropUnitary := by
  constructor <;> rfl

theorem drop_clone_minimal :
    loadBearing .OB_CLONE dropClone := by
  constructor <;> rfl

theorem drop_cont_time_minimal :
    loadBearing .CONT_TIME dropContTime := by
  constructor <;> rfl

theorem every_b4_slot_minimal :
    loadBearing .OB_NONCOMM dropNoncomm ∧
    loadBearing .OB_UNITARY dropUnitary ∧
    loadBearing .OB_CLONE dropClone ∧
    loadBearing .CONT_TIME dropContTime :=
  ⟨drop_noncomm_minimal, drop_unitary_minimal,
    drop_clone_minimal, drop_cont_time_minimal⟩

/-! ## Pathway cover (W6.21 skeleton rows bound to B₄) -/

inductive PathwayTarget where
  | T12  -- dynamics unitary half
  | T16  -- no-cloning
  deriving DecidableEq, Repr

/-- T12 covered only if unitary present; T16 only if no-clone law present. -/
def pathwayCovered (p : FeaturePackage) : PathwayTarget → Bool
  | .T12 => p.unitary
  | .T16 => p.noClone

theorem full_covers_pathways :
    pathwayCovered fullB4 .T12 = true ∧
    pathwayCovered fullB4 .T16 = true := by
  decide

theorem drop_unitary_loses_t12 :
    pathwayCovered dropUnitary .T12 = false ∧
    pathwayCovered dropUnitary .T16 = true := by
  decide

theorem drop_clone_loses_t16 :
    pathwayCovered dropClone .T16 = false ∧
    pathwayCovered dropClone .T12 = true := by
  decide

/-- Dropping NONCOMM or CONT-TIME does not by itself unbind T12/T16
    (those rows are not keyed to those slots in the W6.21 skeleton). -/
theorem drop_noncomm_keeps_pathways :
    pathwayCovered dropNoncomm .T12 = true ∧
    pathwayCovered dropNoncomm .T16 = true := by
  decide

theorem drop_cont_time_keeps_pathways :
    pathwayCovered dropContTime .T12 = true ∧
    pathwayCovered dropContTime .T16 = true := by
  decide

/-! ## Full-ops pathway package (W6.21 residual bind; registry-relative) -/

inductive RecoveryTarget where
  | T01 | T02 | T03 | T04 | T05
  | T06 | T07
  | T08 | T09 | T10 | T11
  | T12 | T13 | T14 | T15 | T16 | T17
  | T_HERM  -- provisional B5 OB-HERM dynamics herm path (not a sealed freeze card)
  deriving DecidableEq, Repr

/-- Sealed freeze pathway card T01–T17 (T_HERM is provisional, not counted). -/
def requiredTargets : List RecoveryTarget :=
  [.T01, .T02, .T03, .T04, .T05, .T06, .T07, .T08, .T09, .T10,
   .T11, .T12, .T13, .T14, .T15, .T16, .T17]

theorem requiredTargets_card : requiredTargets.length = 17 := by
  decide

/-- Provisional herm pathway target (B5; not in sealed T01–T17 card). -/
def optionalHermTarget : RecoveryTarget := .T_HERM

/-- Named flags of the full-ops sufficiency package (10th = provisional herm). -/
structure FullOpsPackage where
  finL1Classical : Bool
  surplusRung56 : Bool
  b4Present : Bool
  spectralPresent : Bool
  instrumentPresent : Bool
  composePresent : Bool
  bornPresent : Bool
  liftPresent : Bool
  wave7OpsPresent : Bool
  hasHermImport : Bool
  deriving DecidableEq, Repr

def fullOps : FullOpsPackage :=
  { finL1Classical := true
    surplusRung56 := true
    b4Present := true
    spectralPresent := true
    instrumentPresent := true
    composePresent := true
    bornPresent := true
    liftPresent := true
    wave7OpsPresent := true
    hasHermImport := true }

def dropFinL1 : FullOpsPackage :=
  { fullOps with finL1Classical := false }

def dropSurplus : FullOpsPackage :=
  { fullOps with surplusRung56 := false }

def dropB4 : FullOpsPackage :=
  { fullOps with b4Present := false }

def dropSpectral : FullOpsPackage :=
  { fullOps with spectralPresent := false }

def dropInstrument : FullOpsPackage :=
  { fullOps with instrumentPresent := false }

def dropCompose : FullOpsPackage :=
  { fullOps with composePresent := false }

def dropBorn : FullOpsPackage :=
  { fullOps with bornPresent := false }

def dropLift : FullOpsPackage :=
  { fullOps with liftPresent := false }

def dropWave7Ops : FullOpsPackage :=
  { fullOps with wave7OpsPresent := false }

def dropHerm : FullOpsPackage :=
  { fullOps with hasHermImport := false }

/-- Pathway cover mirrors W6.21 `pathwayCovered` (not a sealed theorem).
    `T_HERM` is provisional B5 herm dynamics path keyed to `hasHermImport`. -/
def fullOpsPathway (pkg : FullOpsPackage) : RecoveryTarget → Bool
  | .T01 | .T02 | .T03 | .T04 | .T05 => pkg.finL1Classical
  | .T06 | .T07 => pkg.surplusRung56
  | .T12 | .T16 => pkg.b4Present
  | .T08 => pkg.liftPresent
  | .T09 => pkg.spectralPresent
  | .T10 => pkg.bornPresent
  | .T11 => pkg.composePresent
  | .T13 => pkg.instrumentPresent
  | .T14 | .T15 | .T17 => pkg.wave7OpsPresent
  | .T_HERM => pkg.hasHermImport

theorem full_ops_covers_all :
    (∀ t : RecoveryTarget, fullOpsPathway fullOps t = true) := by
  intro t
  cases t <;> rfl

/-- Dropping a flag loses its keyed pathway target(s). -/
theorem drop_finl1_loses_t01 :
    fullOpsPathway dropFinL1 .T01 = false ∧
    fullOpsPathway dropFinL1 .T12 = true := by
  decide

theorem drop_surplus_loses_t06 :
    fullOpsPathway dropSurplus .T06 = false ∧
    fullOpsPathway dropSurplus .T01 = true := by
  decide

theorem drop_b4_loses_t12_t16 :
    fullOpsPathway dropB4 .T12 = false ∧
    fullOpsPathway dropB4 .T16 = false ∧
    fullOpsPathway dropB4 .T01 = true ∧
    fullOpsPathway dropB4 .T08 = true := by
  decide

theorem drop_lift_loses_t08 :
    fullOpsPathway dropLift .T08 = false ∧
    fullOpsPathway dropLift .T09 = true := by
  decide

theorem drop_spectral_loses_t09 :
    fullOpsPathway dropSpectral .T09 = false ∧
    fullOpsPathway dropSpectral .T08 = true := by
  decide

theorem drop_born_loses_t10 :
    fullOpsPathway dropBorn .T10 = false ∧
    fullOpsPathway dropBorn .T08 = true := by
  decide

theorem drop_compose_loses_t11 :
    fullOpsPathway dropCompose .T11 = false ∧
    fullOpsPathway dropCompose .T08 = true := by
  decide

theorem drop_instrument_loses_t13 :
    fullOpsPathway dropInstrument .T13 = false ∧
    fullOpsPathway dropInstrument .T08 = true := by
  decide

theorem drop_wave7_ops_loses_t14_t15_t17 :
    fullOpsPathway dropWave7Ops .T14 = false ∧
    fullOpsPathway dropWave7Ops .T15 = false ∧
    fullOpsPathway dropWave7Ops .T17 = false ∧
    fullOpsPathway dropWave7Ops .T08 = true := by
  decide

/-- Drop provisional herm flag loses T_HERM; sealed T12/T16 stay pathway-covered. -/
theorem drop_herm_loses_t_herm :
    fullOpsPathway dropHerm .T_HERM = false ∧
    fullOpsPathway dropHerm .T12 = true ∧
    fullOpsPathway dropHerm .T16 = true ∧
    fullOpsPathway dropHerm .T01 = true := by
  decide

theorem full_ops_covers_herm :
    fullOpsPathway fullOps .T_HERM = true := by
  decide

/-- Every named full-ops flag is load-bearing for at least one pathway row. -/
theorem every_full_ops_flag_pathway_minimal :
    fullOpsPathway dropFinL1 .T01 = false ∧
    fullOpsPathway dropSurplus .T06 = false ∧
    fullOpsPathway dropB4 .T12 = false ∧
    fullOpsPathway dropLift .T08 = false ∧
    fullOpsPathway dropSpectral .T09 = false ∧
    fullOpsPathway dropBorn .T10 = false ∧
    fullOpsPathway dropCompose .T11 = false ∧
    fullOpsPathway dropInstrument .T13 = false ∧
    fullOpsPathway dropWave7Ops .T17 = false ∧
    fullOpsPathway dropHerm .T_HERM = false := by
  decide

/-- Card of named flags exercised as load-bearing (10 flags: 9 + herm). -/
def fullOpsFlagCard : Nat := 10

theorem full_ops_flag_card : fullOpsFlagCard = 10 := rfl

/-- Herm is provisional B5 pathway flag, not a $B_4$ capital slot. -/
def hermInB4Capital : Bool := false

theorem herm_not_in_b4_capital : hermInB4Capital = false := rfl

/-! ## Honesty: final-N / sealed freeze minimality OPEN -/

def fullFreezeMinimality_open : Prop := True

theorem full_freeze_minimality_marked_open : fullFreezeMinimality_open := trivial

/-- Sealed B5 herm import minimality (beyond pathway dual) remains OPEN. -/
def hermSealedMinimality_open : Prop := True

theorem herm_sealed_minimality_marked_open : hermSealedMinimality_open := trivial

def fullOpsPathwayMinimalityPackage_toy : Bool := true

/-! ## Main packages -/

theorem import_minimality_b4_package :
    workingBasis.length = 4 ∧
    loadBearing .OB_NONCOMM dropNoncomm ∧
    loadBearing .OB_UNITARY dropUnitary ∧
    loadBearing .OB_CLONE dropClone ∧
    loadBearing .CONT_TIME dropContTime ∧
    pathwayCovered fullB4 .T12 = true ∧
    pathwayCovered dropUnitary .T12 = false ∧
    pathwayCovered fullB4 .T16 = true ∧
    pathwayCovered dropClone .T16 = false ∧
    hermInB4Capital = false ∧
    fullFreezeMinimality_open :=
  ⟨workingBasis_card,
    drop_noncomm_minimal, drop_unitary_minimal,
    drop_clone_minimal, drop_cont_time_minimal,
    rfl, rfl, rfl, rfl, rfl, trivial⟩

theorem import_minimality_full_ops_pathway_package :
    fullOpsPathwayMinimalityPackage_toy = true ∧
    requiredTargets.length = 17 ∧
    fullOpsFlagCard = 10 ∧
    (∀ t : RecoveryTarget, fullOpsPathway fullOps t = true) ∧
    fullOpsPathway dropLift .T08 = false ∧
    fullOpsPathway dropSpectral .T09 = false ∧
    fullOpsPathway dropBorn .T10 = false ∧
    fullOpsPathway dropCompose .T11 = false ∧
    fullOpsPathway dropInstrument .T13 = false ∧
    fullOpsPathway dropWave7Ops .T14 = false ∧
    fullOpsPathway dropWave7Ops .T15 = false ∧
    fullOpsPathway dropWave7Ops .T17 = false ∧
    fullOpsPathway dropB4 .T12 = false ∧
    fullOpsPathway dropB4 .T16 = false ∧
    fullOpsPathway dropSurplus .T06 = false ∧
    fullOpsPathway dropFinL1 .T01 = false ∧
    fullOpsPathway dropHerm .T_HERM = false ∧
    fullOpsPathway fullOps .T_HERM = true ∧
    hermInB4Capital = false ∧
    hermSealedMinimality_open ∧
    fullFreezeMinimality_open := by
  refine ⟨rfl, requiredTargets_card, rfl, ?_, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl,
    rfl, rfl, rfl, rfl, rfl, rfl, rfl, trivial, trivial⟩
  intro t
  cases t <;> rfl

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end ImportMinimality
end QM

#print axioms QM.ImportMinimality.every_b4_slot_minimal
#print axioms QM.ImportMinimality.import_minimality_b4_package
#print axioms QM.ImportMinimality.every_full_ops_flag_pathway_minimal
#print axioms QM.ImportMinimality.import_minimality_full_ops_pathway_package
#print axioms QM.ImportMinimality.drop_herm_loses_t_herm
#print axioms QM.ImportMinimality.structure_not_auth
