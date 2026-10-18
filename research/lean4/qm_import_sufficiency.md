import Mathlib.Tactic

/-!
# QMImportSufficiency — W6.21 (sufficiency skeleton vs freeze targets)

Programme target: DERIV-MASTER W6.21 (path §E.34).
Freeze bind: FINITE-L1-FREEZE §3.1 required targets T01–T17.

**Job:** registry-relative **sufficiency skeleton** — a typed discharge map from
each required recovery target to
`ClassicalDerived | SurplusDerived | ImportBoundB4 | ImportBoundExtended | ResidualOpen`.

**This residual (A1 design outline):** full-ops pathway card remains 17/17
TOY-MECH; add `SealedObligation` / `sealedDesign` (premise package + lemma IDs +
`PathwayPriced | SealedOpen`). Classical/surplus are PathwayPriced; import-bound
rows are SealedOpen. **`fullSufficiency_closed` remains false** — not Wave-6
exit; not sealed $M_n(\mathbb{C})$ theorem.

**Not claimed:** closed carrier+imports ⇒ all T01–T17 as theorems; Wave-6 exit;
Wave-7 exit; minimality; authority.

AuthorityEffect: None.
-/

namespace QM
namespace ImportSufficiency

/-! ## Freeze required targets (W0.2 / §3.1) -/

inductive RecoveryTarget where
  | T01  -- finite sector state / probabilities
  | T02  -- diagonal density shadow
  | T03  -- purity on shadow
  | T04  -- population stochastic channel
  | T05  -- finite path-sum / Chapman–Kolmogorov
  | T06  -- superposition / phase fiber
  | T07  -- interference non-ℓ¹ cross-term
  | T08  -- complex Hilbert lift / conditional uniqueness
  | T09  -- finite spectral theorem
  | T10  -- Born readout
  | T11  -- composition monoidal structure
  | T12  -- dynamics (stochastic and/or unitary)
  | T13  -- measurement instrument
  | T14  -- Bell/CHSH / Tsirelson-facing
  | T15  -- contextuality-facing
  | T16  -- no-cloning
  | T17  -- global empirical falsifier
  deriving DecidableEq, Repr

def requiredTargets : List RecoveryTarget :=
  [.T01, .T02, .T03, .T04, .T05, .T06, .T07, .T08, .T09, .T10,
   .T11, .T12, .T13, .T14, .T15, .T16, .T17]

theorem requiredTargets_card : requiredTargets.length = 17 := by
  decide

/-! ## Discharge kinds -/

inductive DischargeKind where
  | ClassicalDerived
  | SurplusDerived
  | ImportBoundB4
  | ImportBoundExtended
  | ResidualOpen
  deriving DecidableEq, Repr

/-- Typed discharge for extended skeleton (not a closed theorem). -/
def discharge : RecoveryTarget → DischargeKind
  | .T01 | .T02 | .T03 | .T04 | .T05 => .ClassicalDerived
  | .T06 | .T07 => .SurplusDerived
  | .T12 | .T16 => .ImportBoundB4
  | .T08 | .T09 | .T10 | .T11 | .T13 | .T14 | .T15 | .T17 => .ImportBoundExtended

theorem classical_targets_derived :
    discharge .T01 = .ClassicalDerived ∧
    discharge .T02 = .ClassicalDerived ∧
    discharge .T03 = .ClassicalDerived ∧
    discharge .T04 = .ClassicalDerived ∧
    discharge .T05 = .ClassicalDerived := by
  decide

theorem surplus_targets_derived :
    discharge .T06 = .SurplusDerived ∧
    discharge .T07 = .SurplusDerived := by
  decide

theorem import_bound_b4_targets :
    discharge .T12 = .ImportBoundB4 ∧
    discharge .T16 = .ImportBoundB4 := by
  decide

theorem import_bound_extended_targets :
    discharge .T08 = .ImportBoundExtended ∧
    discharge .T09 = .ImportBoundExtended ∧
    discharge .T10 = .ImportBoundExtended ∧
    discharge .T11 = .ImportBoundExtended ∧
    discharge .T13 = .ImportBoundExtended ∧
    discharge .T14 = .ImportBoundExtended ∧
    discharge .T15 = .ImportBoundExtended ∧
    discharge .T17 = .ImportBoundExtended := by
  decide

/-- Under the discharge map, no target is ResidualOpen (all priced as import-bound
    or classical/surplus). Sealed theorem still OPEN separately. -/
def residualOpenUnderMap : List RecoveryTarget :=
  requiredTargets.filter (fun t => discharge t = .ResidualOpen)

theorem residual_open_under_map_empty : residualOpenUnderMap.length = 0 := by
  decide

def extendedPathwayTargets : List RecoveryTarget :=
  requiredTargets.filter (fun t =>
    discharge t = .ClassicalDerived ∨
    discharge t = .SurplusDerived ∨
    discharge t = .ImportBoundB4 ∨
    discharge t = .ImportBoundExtended)

theorem extended_pathway_card : extendedPathwayTargets.length = 17 := by
  decide

/-- Legacy $B_4$-only pathway (classical + surplus + B4) = 9 rows. -/
def b4OnlyPathwayTargets : List RecoveryTarget :=
  requiredTargets.filter (fun t =>
    discharge t = .ClassicalDerived ∨
    discharge t = .SurplusDerived ∨
    discharge t = .ImportBoundB4)

theorem b4_only_pathway_card : b4OnlyPathwayTargets.length = 9 := by
  decide

/-! ## Package presence flags -/

structure SufficiencyPackage where
  finL1Classical : Bool
  surplusRung56 : Bool
  b4Present : Bool
  spectralPresent : Bool
  instrumentPresent : Bool
  composePresent : Bool
  bornPresent : Bool
  liftPresent : Bool
  wave7OpsPresent : Bool
  deriving DecidableEq, Repr

/-- Legacy $B_4$ skeleton package. -/
def skeletonPackage : SufficiencyPackage :=
  { finL1Classical := true
    surplusRung56 := true
    b4Present := true
    spectralPresent := false
    instrumentPresent := false
    composePresent := false
    bornPresent := false
    liftPresent := false
    wave7OpsPresent := false }

/-- Full-ops package (W7.1 capital bind). -/
def fullOpsPackage : SufficiencyPackage :=
  { finL1Classical := true
    surplusRung56 := true
    b4Present := true
    spectralPresent := true
    instrumentPresent := true
    composePresent := true
    bornPresent := true
    liftPresent := true
    wave7OpsPresent := true }

/-- Pure FinL1 alone (links W6.20 necessity). -/
def pureFinL1Package : SufficiencyPackage :=
  { finL1Classical := true
    surplusRung56 := false
    b4Present := false
    spectralPresent := false
    instrumentPresent := false
    composePresent := false
    bornPresent := false
    liftPresent := false
    wave7OpsPresent := false }

/-- Extended pathway covered by package (registry-relative, not sealed theorem). -/
def pathwayCovered (pkg : SufficiencyPackage) (t : RecoveryTarget) : Bool :=
  match discharge t with
  | .ClassicalDerived => pkg.finL1Classical
  | .SurplusDerived => pkg.surplusRung56
  | .ImportBoundB4 => pkg.b4Present
  | .ImportBoundExtended =>
      match t with
      | .T08 => pkg.liftPresent
      | .T09 => pkg.spectralPresent
      | .T10 => pkg.bornPresent
      | .T11 => pkg.composePresent
      | .T13 => pkg.instrumentPresent
      | .T14 | .T15 | .T17 => pkg.wave7OpsPresent
      | _ => false
  | .ResidualOpen => false

theorem skeleton_covers_b4_not_extended :
    pathwayCovered skeletonPackage .T01 = true ∧
    pathwayCovered skeletonPackage .T07 = true ∧
    pathwayCovered skeletonPackage .T12 = true ∧
    pathwayCovered skeletonPackage .T16 = true ∧
    pathwayCovered skeletonPackage .T08 = false ∧
    pathwayCovered skeletonPackage .T10 = false ∧
    pathwayCovered skeletonPackage .T14 = false ∧
    pathwayCovered skeletonPackage .T17 = false := by
  decide

theorem full_ops_covers_all_targets :
    (∀ t : RecoveryTarget, pathwayCovered fullOpsPackage t = true) := by
  intro t
  cases t <;> rfl

theorem pure_finl1_fails_import_bound :
    pathwayCovered pureFinL1Package .T12 = false ∧
    pathwayCovered pureFinL1Package .T16 = false ∧
    pathwayCovered pureFinL1Package .T01 = true := by
  decide

theorem pure_finl1_fails_surplus :
    pathwayCovered pureFinL1Package .T06 = false ∧
    pathwayCovered pureFinL1Package .T07 = false := by
  decide

/-- Sealed full sufficiency remains OPEN (component/pathway card ≠ theorem). -/
def fullSufficiency_closed : Bool := false

theorem full_sufficiency_marked_open : fullSufficiency_closed = false := by
  decide

def fullOpsSufficiencyPathwayPackage_toy : Bool := true

theorem full_ops_sufficiency_pathway_package :
    fullOpsSufficiencyPathwayPackage_toy = true ∧
    extendedPathwayTargets.length = 17 ∧
    b4OnlyPathwayTargets.length = 9 ∧
    pathwayCovered fullOpsPackage .T08 = true ∧
    pathwayCovered fullOpsPackage .T09 = true ∧
    pathwayCovered fullOpsPackage .T10 = true ∧
    pathwayCovered fullOpsPackage .T11 = true ∧
    pathwayCovered fullOpsPackage .T13 = true ∧
    pathwayCovered fullOpsPackage .T14 = true ∧
    pathwayCovered fullOpsPackage .T15 = true ∧
    pathwayCovered fullOpsPackage .T17 = true ∧
    pathwayCovered skeletonPackage .T08 = false ∧
    pathwayCovered skeletonPackage .T10 = false ∧
    pathwayCovered pureFinL1Package .T12 = false ∧
    fullSufficiency_closed = false := by
  decide

/-! ## Sealed sufficiency design outline (A1 / SUF-SEALED-THEOREM)

Design only: premise package flags + lemma obligation IDs + status.
Status is PathwayPriced (classical/surplus pathway capital) or SealedOpen
(import-bound sealed recovery still OPEN). Never a closed seal.
`fullSufficiency_closed` remains false. -/

/-- Pathway pricing ≠ sealed recovery. No SealedClosed constructor. -/
inductive SealedStatus where
  | PathwayPriced
  | SealedOpen
  deriving DecidableEq, Repr

/-- Coarse premise flags for the sealed-design row (design outline). -/
structure PremisePackageFlags where
  finL1 : Bool
  surplus : Bool
  b4 : Bool
  extended : Bool
  deriving DecidableEq, Repr

/-- Per-target sealed obligation (design outline, not a theorem). -/
structure SealedObligation where
  premisePackage : PremisePackageFlags
  lemmaObligations : List String
  status : SealedStatus
  deriving Repr

/-- Sealed design map: classical/surplus PathwayPriced; import-bound SealedOpen. -/
def sealedDesign : RecoveryTarget → SealedObligation
  | .T01 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := false }
      lemmaObligations := ["FINL1-STATE-PROB", "W2-CLASSICAL-HEART"]
      status := .PathwayPriced }
  | .T02 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := false }
      lemmaObligations := ["FINL1-DIAG-SHADOW", "W2-CLASSICAL-HEART"]
      status := .PathwayPriced }
  | .T03 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := false }
      lemmaObligations := ["FINL1-PURITY-SHADOW"]
      status := .PathwayPriced }
  | .T04 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := false }
      lemmaObligations := ["FINL1-POP-CHANNEL", "W2-STOCH-CK"]
      status := .PathwayPriced }
  | .T05 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := false }
      lemmaObligations := ["FINL1-PATH-SUM", "W2-STOCH-CK"]
      status := .PathwayPriced }
  | .T06 =>
    { premisePackage := { finL1 := true, surplus := true, b4 := false, extended := false }
      lemmaObligations := ["SURPLUS-PHASE-FIBER", "W4-FIN3-SURPLUS"]
      status := .PathwayPriced }
  | .T07 =>
    { premisePackage := { finL1 := true, surplus := true, b4 := false, extended := false }
      lemmaObligations := ["SURPLUS-CROSS-TERM", "W4-FIN3-SURPLUS"]
      status := .PathwayPriced }
  | .T08 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := true }
      lemmaObligations := ["W5.8-COND-UNIQ", "W5.6-AX-LIFT-V0", "W5.11-LIFT-FENCE"]
      status := .SealedOpen }
  | .T09 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := true }
      lemmaObligations := ["W6.10-OB-SPECTRAL", "PL-005-1-GENERAL-N"]
      status := .SealedOpen }
  | .T10 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := true }
      lemmaObligations := ["W6.5-L2-VS-BORN", "OB-BORN-READOUT"]
      status := .SealedOpen }
  | .T11 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := true }
      lemmaObligations := ["W6.14-COMPOSE-MONOIDAL", "LT-OB-U1-COUPLED"]
      status := .SealedOpen }
  | .T12 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := true, extended := false }
      lemmaObligations := ["W6.19-B4-INDEP", "W6.8-UNITARY-NOT-STOCH", "W6.16-TIME-GEN"]
      status := .SealedOpen }
  | .T13 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := true }
      lemmaObligations := ["W6.12-OB-INSTRUMENT", "W6.17-BACKACTION"]
      status := .SealedOpen }
  | .T14 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := true }
      lemmaObligations := ["W7.2-TSIRELSON-CHSH", "W5.5-SEP-PRED"]
      status := .SealedOpen }
  | .T15 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := true }
      lemmaObligations := ["W7.3-MERMIN-PERES", "W6.6-NONCOMM"]
      status := .SealedOpen }
  | .T16 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := true, extended := false }
      lemmaObligations := ["W6.19-B4-INDEP", "W6.18-NO-CLONE"]
      status := .SealedOpen }
  | .T17 =>
    { premisePackage := { finL1 := true, surplus := false, b4 := false, extended := true }
      lemmaObligations := ["W7.6-GLOBAL-FALSIFIER", "W7.1-FIN-MATRIX"]
      status := .SealedOpen }

def pathwayPricedTargets : List RecoveryTarget :=
  requiredTargets.filter (fun t => (sealedDesign t).status = .PathwayPriced)

def sealedOpenTargets : List RecoveryTarget :=
  requiredTargets.filter (fun t => (sealedDesign t).status = .SealedOpen)

theorem pathway_priced_card : pathwayPricedTargets.length = 7 := by
  decide

theorem sealed_open_card : sealedOpenTargets.length = 10 := by
  decide

theorem sealed_design_partition :
    pathwayPricedTargets.length + sealedOpenTargets.length = 17 := by
  decide

theorem classical_surplus_pathway_priced :
    (sealedDesign .T01).status = .PathwayPriced ∧
    (sealedDesign .T05).status = .PathwayPriced ∧
    (sealedDesign .T06).status = .PathwayPriced ∧
    (sealedDesign .T07).status = .PathwayPriced := by
  decide

theorem import_bound_sealed_open :
    (sealedDesign .T08).status = .SealedOpen ∧
    (sealedDesign .T09).status = .SealedOpen ∧
    (sealedDesign .T10).status = .SealedOpen ∧
    (sealedDesign .T11).status = .SealedOpen ∧
    (sealedDesign .T12).status = .SealedOpen ∧
    (sealedDesign .T13).status = .SealedOpen ∧
    (sealedDesign .T14).status = .SealedOpen ∧
    (sealedDesign .T15).status = .SealedOpen ∧
    (sealedDesign .T16).status = .SealedOpen ∧
    (sealedDesign .T17).status = .SealedOpen := by
  decide

/-- Import-bound design rows carry non-empty lemma obligation IDs. -/
theorem import_bound_lemmas_nonempty :
    (sealedDesign .T08).lemmaObligations ≠ [] ∧
    (sealedDesign .T09).lemmaObligations ≠ [] ∧
    (sealedDesign .T12).lemmaObligations ≠ [] ∧
    (sealedDesign .T16).lemmaObligations ≠ [] ∧
    (sealedDesign .T17).lemmaObligations ≠ [] := by
  decide

/-- Design outline package: statuses partition + global seal still OPEN. -/
theorem sealed_sufficiency_design_package :
    pathwayPricedTargets.length = 7 ∧
    sealedOpenTargets.length = 10 ∧
    pathwayPricedTargets.length + sealedOpenTargets.length = 17 ∧
    (sealedDesign .T01).status = .PathwayPriced ∧
    (sealedDesign .T07).status = .PathwayPriced ∧
    (sealedDesign .T08).status = .SealedOpen ∧
    (sealedDesign .T12).status = .SealedOpen ∧
    (sealedDesign .T17).status = .SealedOpen ∧
    (sealedDesign .T09).premisePackage.extended = true ∧
    (sealedDesign .T12).premisePackage.b4 = true ∧
    (sealedDesign .T06).premisePackage.surplus = true ∧
    fullSufficiency_closed = false ∧
    fullOpsSufficiencyPathwayPackage_toy = true := by
  decide

/-! ## B7 independence handoff (W6.19 → W6.21 design bind)

Provisional $B_7$ independence capital (W6.19 IND-L2-BORN) feeds the sealed
design ledger as **named import slots**, not as a closed sufficiency theorem.
Maps recovery targets to required independence-slot IDs. `fullSufficiency_closed`
stays false. OB-U1 still coupled (T11) — not a $B_7$ independence row.
-/

inductive IndepSlotId where
  | NONCOMM | UNITARY | CLONE | CONT_TIME | HERM | L2_READOUT | BORN
  deriving DecidableEq, Repr

/-- Provisional $B_7$ ledger as used by the sufficiency design (TOY-MECH bind). -/
def provisionalImportLedgerB7 : List IndepSlotId :=
  [.NONCOMM, .UNITARY, .CLONE, .CONT_TIME, .HERM, .L2_READOUT, .BORN]

theorem provisional_import_ledger_b7_card :
    provisionalImportLedgerB7.length = 7 := by
  decide

/-- Which independence slots a sealed-design target is allowed to consume
    (design map only; not a proof of recovery). -/
def requiredIndepSlots : RecoveryTarget → List IndepSlotId
  | .T01 | .T02 | .T03 | .T04 | .T05 => []  -- classical FinL1
  | .T06 | .T07 => [.L2_READOUT]  -- surplus host structure (Rung 5–6)
  | .T08 => [.NONCOMM]  -- lift / noncomm capital
  | .T09 => [.HERM, .UNITARY]  -- spectral / generator side
  | .T10 => [.L2_READOUT, .BORN]  -- Born pairing needs host + selection
  | .T11 => []  -- compose/LT: OB-U1 coupled — **not** in B7 ledger
  | .T12 => [.UNITARY, .CONT_TIME]  -- unitary dynamics / time
  | .T13 => [.NONCOMM]  -- instruments
  | .T14 => [.NONCOMM, .L2_READOUT]  -- Tsirelson / separating
  | .T15 => [.NONCOMM]  -- Mermin–Peres
  | .T16 => [.CLONE]  -- no-clone
  | .T17 => [.NONCOMM, .L2_READOUT, .BORN]  -- global falsifier package

def usesOnlyB7Slots (t : RecoveryTarget) : Bool :=
  (requiredIndepSlots t).all (fun s => provisionalImportLedgerB7.contains s)

theorem t10_requires_l2_and_born :
    requiredIndepSlots .T10 = [.L2_READOUT, .BORN] := by
  decide

theorem t11_compose_not_on_b7_ledger :
    requiredIndepSlots .T11 = [] := by
  decide

theorem classical_targets_need_no_import_slots :
    requiredIndepSlots .T01 = [] ∧
    requiredIndepSlots .T05 = [] := by
  decide

theorem b7_consumers_use_only_ledger_slots :
    usesOnlyB7Slots .T06 = true ∧
    usesOnlyB7Slots .T10 = true ∧
    usesOnlyB7Slots .T12 = true ∧
    usesOnlyB7Slots .T16 = true ∧
    usesOnlyB7Slots .T17 = true ∧
    usesOnlyB7Slots .T11 = true := by  -- empty list ⊆ B7
  decide

/-- Finite-calculus closure design checklist (desire-1 packaging, not a seal).
    Each row is a design obligation; none flips `fullSufficiency_closed`. -/
structure FiniteCalculusClosureChecklist where
  classicalShadow : Bool      -- T01–T05 pathway
  interferenceSurplus : Bool  -- T06–T07 pathway
  importIndependenceB7 : Bool -- W6.19 B7 matrix
  sufficiencyPathway17 : Bool -- full-ops pathway card
  sealedTheorem : Bool        -- must stay false until real seals
  wave6Exit : Bool            -- must stay false
  deriving DecidableEq, Repr

def finiteCalculusClosureChecklist : FiniteCalculusClosureChecklist :=
  { classicalShadow := true
    interferenceSurplus := true
    importIndependenceB7 := true
    sufficiencyPathway17 := true
    sealedTheorem := false
    wave6Exit := false }

theorem finite_calculus_closure_checklist_honesty :
    finiteCalculusClosureChecklist.classicalShadow = true ∧
    finiteCalculusClosureChecklist.interferenceSurplus = true ∧
    finiteCalculusClosureChecklist.importIndependenceB7 = true ∧
    finiteCalculusClosureChecklist.sufficiencyPathway17 = true ∧
    finiteCalculusClosureChecklist.sealedTheorem = false ∧
    finiteCalculusClosureChecklist.wave6Exit = false ∧
    fullSufficiency_closed = false := by
  decide

/-- B7 → sufficiency design handoff package (TOY-MECH residual deepen). -/
theorem b7_sufficiency_design_handoff_package :
    provisionalImportLedgerB7.length = 7 ∧
    requiredIndepSlots .T10 = [.L2_READOUT, .BORN] ∧
    requiredIndepSlots .T11 = [] ∧
    usesOnlyB7Slots .T10 = true ∧
    finiteCalculusClosureChecklist.importIndependenceB7 = true ∧
    finiteCalculusClosureChecklist.sealedTheorem = false ∧
    fullSufficiency_closed = false ∧
    fullOpsSufficiencyPathwayPackage_toy = true := by
  decide

/-! ## Main package -/

theorem import_sufficiency_skeleton_package :
    requiredTargets.length = 17 ∧
    b4OnlyPathwayTargets.length = 9 ∧
    extendedPathwayTargets.length = 17 ∧
    residualOpenUnderMap.length = 0 ∧
    discharge .T01 = .ClassicalDerived ∧
    discharge .T07 = .SurplusDerived ∧
    discharge .T12 = .ImportBoundB4 ∧
    discharge .T10 = .ImportBoundExtended ∧
    pathwayCovered skeletonPackage .T12 = true ∧
    pathwayCovered fullOpsPackage .T17 = true ∧
    pathwayCovered pureFinL1Package .T12 = false ∧
    fullOpsSufficiencyPathwayPackage_toy = true ∧
    fullSufficiency_closed = false ∧
    pathwayPricedTargets.length = 7 ∧
    sealedOpenTargets.length = 10 ∧
    (sealedDesign .T08).status = .SealedOpen ∧
    provisionalImportLedgerB7.length = 7 ∧
    finiteCalculusClosureChecklist.sealedTheorem = false := by
  decide

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end ImportSufficiency
end QM

#print axioms QM.ImportSufficiency.requiredTargets_card
#print axioms QM.ImportSufficiency.import_sufficiency_skeleton_package
#print axioms QM.ImportSufficiency.full_ops_sufficiency_pathway_package
#print axioms QM.ImportSufficiency.sealed_sufficiency_design_package
#print axioms QM.ImportSufficiency.structure_not_auth
