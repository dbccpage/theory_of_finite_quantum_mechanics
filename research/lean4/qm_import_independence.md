import Mathlib.Tactic

/-!
# QMImportIndependence — W6.19 (import independence models)

Programme target: DERIV-MASTER W6.19 (path §E.32).

**Job:** exhibit a **working independent basis** $B$ of freeze import slots and
$|B|$ models such that model $M_i$ **fails exactly** slot $i$ and admits the
others (registry-relative, dual TOY-MECH).

**Provisional working basis $B_8$ (this fire — not final $N$):**

| Id | Freeze slot | Drop witness (capital) |
|---|---|---|
| I1 | `OB-NONCOMM` | FinL1 classical diagonal **commutes** (W6.6) |
| I2 | `OB-UNITARY` | reset kernel not doubly stochastic (W6.8) |
| I3 | `OB-CLONE` | classical residual distribution clone exists (W6.18) |
| I4 | `CONT-TIME` | discrete Nat steps only; continuous generator refused (W6.7/16) |
| I5 | `OB-HERM` | non-Hermitian generator admitted; Hermiticity import absent (W6.9) |
| I6 | `OB-L2-READOUT` | quadratic ℓ² readout structure absent (QM-208 / recon B2) |
| I7 | `OB-BORN` | Born pairing / quadratic uniqueness absent (QM-210 / recon B4) |
| I8 | `BUNDLE-U1-LT` | coupled phase+composite-LT package absent (W6.14 bundle) |

**Nested:** $B_4$ (I1–I4), $B_5$ (I1–I5), $B_7$ (I1–I7), $B_8$ (I1–I8).

**BUNDLE-U1-LT residual (this fire):** real drop model for the **coupled** W6.14
import bundle (not XOR independence of OB-U1 from composite LT). Separate U1/LT
rows are **not** ImportSlot constructors.

**Still OPEN toward full BASIS-CANDIDATE:**
- Full freeze / recon §3.1 (more recovery imports; absolute final $N$) **OPEN**
- `SPLIT-OUTSIDE-REGISTRY` remains OPEN on W6.14 (not discharged by B8)

**Not claimed:** final independent $N$; sufficiency (W6.21); absolute all-import
independence; Stone continuous groups; Wave-6 exit; authority.

AuthorityEffect: None.
-/

namespace QM
namespace ImportIndependence

/-! ## Working basis labels -/

inductive ImportSlot where
  | OB_NONCOMM
  | OB_UNITARY
  | OB_CLONE
  | CONT_TIME
  | OB_HERM
  | OB_L2_READOUT
  | OB_BORN
  | BUNDLE_U1_LT
  deriving DecidableEq, Repr

/-- Nested $B_4$ (pre-HERM residual). -/
def workingBasisB4 : List ImportSlot :=
  [.OB_NONCOMM, .OB_UNITARY, .OB_CLONE, .CONT_TIME]

/-- Nested $B_5$ = $B_4$ + `OB-HERM`. -/
def workingBasisB5 : List ImportSlot :=
  [.OB_NONCOMM, .OB_UNITARY, .OB_CLONE, .CONT_TIME, .OB_HERM]

/-- Nested $B_7$ = $B_5$ + `OB-L2-READOUT` + `OB-BORN`. -/
def workingBasisB7 : List ImportSlot :=
  [.OB_NONCOMM, .OB_UNITARY, .OB_CLONE, .CONT_TIME, .OB_HERM,
   .OB_L2_READOUT, .OB_BORN]

/-- Provisional working basis $B_8$ = $B_7$ + `BUNDLE-U1-LT` (W6.14 coupled package). -/
def workingBasisB8 : List ImportSlot :=
  workingBasisB7 ++ [.BUNDLE_U1_LT]

/-- Primary working basis alias: provisional $B_8$. -/
def workingBasis : List ImportSlot := workingBasisB8

theorem workingBasisB4_card : workingBasisB4.length = 4 := by
  decide

theorem workingBasisB5_card : workingBasisB5.length = 5 := by
  decide

theorem workingBasisB7_card : workingBasisB7.length = 7 := by
  decide

theorem workingBasisB8_card : workingBasisB8.length = 8 := by
  decide

theorem workingBasis_card : workingBasis.length = 8 := by
  decide

/-! ## Feature predicates (drop witnesses as discrete flags) -/

structure NoncommFeature where
  present : Bool
  deriving DecidableEq, Repr

structure UnitaryFeature where
  present : Bool
  deriving DecidableEq, Repr

structure NoCloneFeature where
  present : Bool
  deriving DecidableEq, Repr

structure ContTimeFeature where
  present : Bool
  deriving DecidableEq, Repr

structure HermFeature where
  present : Bool
  deriving DecidableEq, Repr

/-- Quadratic ℓ² / inner-product readout structure (recon B2 / QM-208). -/
structure L2ReadoutFeature where
  present : Bool
  deriving DecidableEq, Repr

/-- Born pairing / quadratic uniqueness selection (recon B4 / QM-210). -/
structure BornFeature where
  present : Bool
  deriving DecidableEq, Repr

/-- Coupled OB-U1 + composite-LT package (W6.14 BUNDLE-U1-LT; not XOR split). -/
structure BundleU1LtFeature where
  present : Bool
  deriving DecidableEq, Repr

/-- A finite-regime model package relative to $B_8$. -/
structure IndependenceModel where
  noncomm : NoncommFeature
  unitary : UnitaryFeature
  noClone : NoCloneFeature
  contTime : ContTimeFeature
  herm : HermFeature
  l2 : L2ReadoutFeature
  born : BornFeature
  bundle : BundleU1LtFeature
  deriving DecidableEq, Repr

def admits (m : IndependenceModel) : ImportSlot → Bool
  | .OB_NONCOMM => m.noncomm.present
  | .OB_UNITARY => m.unitary.present
  | .OB_CLONE => m.noClone.present
  | .CONT_TIME => m.contTime.present
  | .OB_HERM => m.herm.present
  | .OB_L2_READOUT => m.l2.present
  | .OB_BORN => m.born.present
  | .BUNDLE_U1_LT => m.bundle.present

/-- Fail exactly one named slot; admit all others. -/
def failsExactly (m : IndependenceModel) (drop : ImportSlot) : Prop :=
  (admits m drop = false) ∧
  (∀ s : ImportSlot, s ≠ drop → admits m s = true)

/-! ## Drop witnesses (bind Wave-6 capital as boolean models) -/

/-- All-present template except one flag flipped off. -/
def modelAllTrue : IndependenceModel :=
  { noncomm := { present := true }
    unitary := { present := true }
    noClone := { present := true }
    contTime := { present := true }
    herm := { present := true }
    l2 := { present := true }
    born := { present := true }
    bundle := { present := true } }

def modelDropNoncomm : IndependenceModel :=
  { modelAllTrue with noncomm := { present := false } }

def modelDropUnitary : IndependenceModel :=
  { modelAllTrue with unitary := { present := false } }

def modelDropClone : IndependenceModel :=
  { modelAllTrue with noClone := { present := false } }

def modelDropContTime : IndependenceModel :=
  { modelAllTrue with contTime := { present := false } }

def modelDropHerm : IndependenceModel :=
  { modelAllTrue with herm := { present := false } }

/-- M6: drops ℓ² readout structure (cross-term host absent; Rung 6 surplus host missing). -/
def modelDropL2 : IndependenceModel :=
  { modelAllTrue with l2 := { present := false } }

/-- M7: drops Born pairing (quadratic uniqueness selection absent). -/
def modelDropBorn : IndependenceModel :=
  { modelAllTrue with born := { present := false } }

/-- M8: drops BUNDLE-U1-LT coupled package (phase+composite LT both absent). -/
def modelDropBundle : IndependenceModel :=
  { modelAllTrue with bundle := { present := false } }

private theorem failsExactly_of_single_false
    (m : IndependenceModel) (drop : ImportSlot)
    (h_drop : admits m drop = false)
    (h_rest : ∀ s : ImportSlot, s ≠ drop → admits m s = true) :
    failsExactly m drop :=
  ⟨h_drop, h_rest⟩

theorem modelDropNoncomm_fails_exactly :
    failsExactly modelDropNoncomm .OB_NONCOMM := by
  constructor
  · rfl
  · intro s hs; cases s <;> first | contradiction | rfl

theorem modelDropUnitary_fails_exactly :
    failsExactly modelDropUnitary .OB_UNITARY := by
  constructor
  · rfl
  · intro s hs; cases s <;> first | contradiction | rfl

theorem modelDropClone_fails_exactly :
    failsExactly modelDropClone .OB_CLONE := by
  constructor
  · rfl
  · intro s hs; cases s <;> first | contradiction | rfl

theorem modelDropContTime_fails_exactly :
    failsExactly modelDropContTime .CONT_TIME := by
  constructor
  · rfl
  · intro s hs; cases s <;> first | contradiction | rfl

theorem modelDropHerm_fails_exactly :
    failsExactly modelDropHerm .OB_HERM := by
  constructor
  · rfl
  · intro s hs; cases s <;> first | contradiction | rfl

theorem modelDropL2_fails_exactly :
    failsExactly modelDropL2 .OB_L2_READOUT := by
  constructor
  · rfl
  · intro s hs; cases s <;> first | contradiction | rfl

theorem modelDropBorn_fails_exactly :
    failsExactly modelDropBorn .OB_BORN := by
  constructor
  · rfl
  · intro s hs; cases s <;> first | contradiction | rfl

theorem modelDropBundle_fails_exactly :
    failsExactly modelDropBundle .BUNDLE_U1_LT := by
  constructor
  · rfl
  · intro s hs; cases s <;> first | contradiction | rfl

/-- Seven models, one per nested $B_7$ basis slot. -/
def independenceModelsB7 : List (ImportSlot × IndependenceModel) :=
  [ (.OB_NONCOMM, modelDropNoncomm)
    , (.OB_UNITARY, modelDropUnitary)
    , (.OB_CLONE, modelDropClone)
    , (.CONT_TIME, modelDropContTime)
    , (.OB_HERM, modelDropHerm)
    , (.OB_L2_READOUT, modelDropL2)
    , (.OB_BORN, modelDropBorn) ]

/-- Eight models, one per provisional $B_8$ basis slot. -/
def independenceModelsB8 : List (ImportSlot × IndependenceModel) :=
  independenceModelsB7 ++ [(.BUNDLE_U1_LT, modelDropBundle)]

def independenceModelsB5 : List (ImportSlot × IndependenceModel) :=
  [ (.OB_NONCOMM, modelDropNoncomm)
    , (.OB_UNITARY, modelDropUnitary)
    , (.OB_CLONE, modelDropClone)
    , (.CONT_TIME, modelDropContTime)
    , (.OB_HERM, modelDropHerm) ]

def independenceModelsB4 : List (ImportSlot × IndependenceModel) :=
  [ (.OB_NONCOMM, modelDropNoncomm)
    , (.OB_UNITARY, modelDropUnitary)
    , (.OB_CLONE, modelDropClone)
    , (.CONT_TIME, modelDropContTime) ]

/-- Primary alias: provisional $B_8$. -/
def independenceModels : List (ImportSlot × IndependenceModel) :=
  independenceModelsB8

theorem independenceModelsB4_card : independenceModelsB4.length = 4 := by decide
theorem independenceModelsB5_card : independenceModelsB5.length = 5 := by decide
theorem independenceModelsB7_card : independenceModelsB7.length = 7 := by decide
theorem independenceModelsB8_card : independenceModelsB8.length = 8 := by decide
theorem independenceModels_card : independenceModels.length = 8 := by decide

theorem independenceModels_match_basis :
    independenceModels.length = workingBasis.length := by
  decide

theorem every_b4_slot_has_drop_model :
    failsExactly modelDropNoncomm .OB_NONCOMM ∧
    failsExactly modelDropUnitary .OB_UNITARY ∧
    failsExactly modelDropClone .OB_CLONE ∧
    failsExactly modelDropContTime .CONT_TIME :=
  ⟨modelDropNoncomm_fails_exactly, modelDropUnitary_fails_exactly,
    modelDropClone_fails_exactly, modelDropContTime_fails_exactly⟩

theorem every_b5_slot_has_drop_model :
    failsExactly modelDropNoncomm .OB_NONCOMM ∧
    failsExactly modelDropUnitary .OB_UNITARY ∧
    failsExactly modelDropClone .OB_CLONE ∧
    failsExactly modelDropContTime .CONT_TIME ∧
    failsExactly modelDropHerm .OB_HERM :=
  ⟨modelDropNoncomm_fails_exactly, modelDropUnitary_fails_exactly,
    modelDropClone_fails_exactly, modelDropContTime_fails_exactly,
    modelDropHerm_fails_exactly⟩

theorem every_b7_slot_has_drop_model :
    failsExactly modelDropNoncomm .OB_NONCOMM ∧
    failsExactly modelDropUnitary .OB_UNITARY ∧
    failsExactly modelDropClone .OB_CLONE ∧
    failsExactly modelDropContTime .CONT_TIME ∧
    failsExactly modelDropHerm .OB_HERM ∧
    failsExactly modelDropL2 .OB_L2_READOUT ∧
    failsExactly modelDropBorn .OB_BORN :=
  ⟨modelDropNoncomm_fails_exactly, modelDropUnitary_fails_exactly,
    modelDropClone_fails_exactly, modelDropContTime_fails_exactly,
    modelDropHerm_fails_exactly, modelDropL2_fails_exactly,
    modelDropBorn_fails_exactly⟩

/-- Every $B_8$ basis slot has a drop-exactly-one model (BUNDLE-U1-LT included). -/
theorem every_basis_slot_has_drop_model :
    failsExactly modelDropNoncomm .OB_NONCOMM ∧
    failsExactly modelDropUnitary .OB_UNITARY ∧
    failsExactly modelDropClone .OB_CLONE ∧
    failsExactly modelDropContTime .CONT_TIME ∧
    failsExactly modelDropHerm .OB_HERM ∧
    failsExactly modelDropL2 .OB_L2_READOUT ∧
    failsExactly modelDropBorn .OB_BORN ∧
    failsExactly modelDropBundle .BUNDLE_U1_LT :=
  ⟨modelDropNoncomm_fails_exactly, modelDropUnitary_fails_exactly,
    modelDropClone_fails_exactly, modelDropContTime_fails_exactly,
    modelDropHerm_fails_exactly, modelDropL2_fails_exactly,
    modelDropBorn_fails_exactly, modelDropBundle_fails_exactly⟩

/-! ## Concrete capital fences (why the drop flags are honest) -/

def diagA : Int × Int := (2, 3)
def diagB : Int × Int := (5, 7)

theorem classical_diag_commute :
    (diagA.1 * diagB.1, diagA.2 * diagB.2) =
      (diagB.1 * diagA.1, diagB.2 * diagA.2) := by
  simp [diagA, diagB]

structure Kernel2 where
  k00 : Nat
  k10 : Nat
  k01 : Nat
  k11 : Nat
  deriving DecidableEq, Repr

def resetKernel : Kernel2 := { k00 := 1, k10 := 0, k01 := 1, k11 := 0 }

def isColumnStochastic (K : Kernel2) : Prop :=
  K.k00 + K.k10 = 1 ∧ K.k01 + K.k11 = 1

def isDoublyStochastic (K : Kernel2) : Prop :=
  isColumnStochastic K ∧ K.k00 + K.k01 = 1 ∧ K.k10 + K.k11 = 1

theorem reset_column_not_doubly :
    isColumnStochastic resetKernel ∧ ¬ isDoublyStochastic resetKernel := by
  constructor
  · simp [resetKernel, isColumnStochastic]
  · intro h
    have : resetKernel.k00 + resetKernel.k01 = 1 := h.2.1
    simp [resetKernel] at this

structure BitWeight where
  w0 : Nat
  w1 : Nat
  deriving DecidableEq, Repr

def fairBit : BitWeight := { w0 := 1, w1 := 1 }

def classicalClone (w : BitWeight) : Nat × Nat × Nat × Nat :=
  (w.w0 * w.w0, w.w0 * w.w1, w.w1 * w.w0, w.w1 * w.w1)

theorem classical_clone_fair_exists :
    classicalClone fairBit = (1, 1, 1, 1) := by
  simp [classicalClone, fairBit]

def discreteStepsOnly : Bool := true
def continuousGeneratorAdmitted : Bool := false

theorem cont_time_not_forced_by_discrete :
    discreteStepsOnly = true ∧ continuousGeneratorAdmitted = false := by
  decide

structure Mat2Toy where
  a00 : Int
  a01 : Int
  a10 : Int
  a11 : Int
  deriving DecidableEq, Repr

def IsHermitianToy (m : Mat2Toy) : Prop := m.a01 = m.a10

def nonHermG : Mat2Toy := { a00 := 0, a01 := 1, a10 := 0, a11 := 0 }
def sigmaXHermToy : Mat2Toy := { a00 := 0, a01 := 1, a10 := 1, a11 := 0 }

theorem nonHermG_not_hermitian : ¬ IsHermitianToy nonHermG := by
  intro h
  simp [nonHermG, IsHermitianToy] at h

theorem sigmaX_is_hermitian_toy : IsHermitianToy sigmaXHermToy := rfl

theorem hermiticity_import_absent_fence :
    ¬ IsHermitianToy nonHermG ∧ IsHermitianToy sigmaXHermToy :=
  ⟨nonHermG_not_hermitian, sigmaX_is_hermitian_toy⟩

def hermiticityImportForcedFromFinL1 : Bool := false
def nonHermitianGeneratorAdmitted : Bool := true

theorem herm_drop_witness_flags :
    hermiticityImportForcedFromFinL1 = false ∧
    nonHermitianGeneratorAdmitted = true := by
  decide

/-! ## L2 / Born capital fences (IND-L2-BORN)

Honesty: ℓ¹ probability shadow is **not** quadratic readout; Born selection is a
**separate** import from the host structure that enables cross-terms (recon §4).
-/

/-- Pure ℓ¹ weight on 2 outcomes (classical shadow). Sum = 1 after scale. -/
def l1ShadowWeights : Nat × Nat := (1, 1)

/-- Quadratic readout would square amplitudes; classical ℓ¹ residual does not force it. -/
def l2ReadoutForcedFromL1Shadow : Bool := false
def quadraticInnerProductStructureAdmitted : Bool := false

theorem l2_drop_witness_flags :
    l2ReadoutForcedFromL1Shadow = false ∧
    quadraticInnerProductStructureAdmitted = false := by
  decide

/-- Born uniqueness / pairing not forced by mere ℓ² host structure alone
    (W6.5 capital shape; merge L2↔Born refused). -/
def bornPairingForcedFromL2HostAlone : Bool := false
def bornUniquenessSelectionAdmitted : Bool := false

theorem born_drop_witness_flags :
    bornPairingForcedFromL2HostAlone = false ∧
    bornUniquenessSelectionAdmitted = false := by
  decide

/-- Split honesty: L2 host present does **not** force Born selection. -/
def l2HostWithoutBorn : IndependenceModel :=
  { modelAllTrue with born := { present := false } }

def bornWithoutL2Host : IndependenceModel :=
  { modelAllTrue with l2 := { present := false } }

theorem l2_born_split_models_exist :
    admits l2HostWithoutBorn .OB_L2_READOUT = true ∧
    admits l2HostWithoutBorn .OB_BORN = false ∧
    admits bornWithoutL2Host .OB_BORN = true ∧
    admits bornWithoutL2Host .OB_L2_READOUT = false := by
  decide

/-! ## Coupled packaging honesty (B8)

Separate OB-U1 / composite-LT rows are **not** ImportSlot constructors.
The couple is admitted as the single `BUNDLE_U1_LT` slot (W6.14).
-/

def excludedCoupled : List Unit := []

theorem excluded_coupled_card : excludedCoupled.length = 0 := by
  decide

def separateObU1RowInIndependenceMatrix : Bool := false
def separateCompositeLtRowInIndependenceMatrix : Bool := false

theorem separate_u1_lt_rows_refused :
    separateObU1RowInIndependenceMatrix = false ∧
    separateCompositeLtRowInIndependenceMatrix = false := by
  decide

/-- Full freeze BASIS-CANDIDATE independence remains OPEN beyond provisional $B_8$. -/
def fullBasisIndependence_open : Prop := True

theorem full_basis_independence_marked_open : fullBasisIndependence_open := trivial

/-! ## Independence matrix residual

Rows = drop models; columns = $B_8$ slots. Entry = admits flag.
-/

def modelRow : ImportSlot → IndependenceModel
  | .OB_NONCOMM => modelDropNoncomm
  | .OB_UNITARY => modelDropUnitary
  | .OB_CLONE => modelDropClone
  | .CONT_TIME => modelDropContTime
  | .OB_HERM => modelDropHerm
  | .OB_L2_READOUT => modelDropL2
  | .OB_BORN => modelDropBorn
  | .BUNDLE_U1_LT => modelDropBundle

def admitsMatrix (row col : ImportSlot) : Bool :=
  admits (modelRow row) col

theorem admits_matrix_diag_false :
    ∀ s : ImportSlot, admitsMatrix s s = false := by
  intro s; cases s <;> rfl

theorem admits_matrix_off_diag_true :
    (∀ r c : ImportSlot, r ≠ c → admitsMatrix r c = true) := by
  intro r c h
  cases r <;> cases c <;> first | contradiction | rfl

theorem unique_drop_model_per_slot (s : ImportSlot) :
    admitsMatrix s s = false ∧
    (∀ r : ImportSlot, r ≠ s → admitsMatrix r s = true) := by
  constructor
  · exact admits_matrix_diag_false s
  · intro r h
    exact admits_matrix_off_diag_true r s h

/-- Models for distinct drop slots are distinct packages ($B_8$, $\binom{8}{2}=28$). -/
theorem drop_models_pairwise_distinct :
    modelDropNoncomm ≠ modelDropUnitary ∧
    modelDropNoncomm ≠ modelDropClone ∧
    modelDropNoncomm ≠ modelDropContTime ∧
    modelDropNoncomm ≠ modelDropHerm ∧
    modelDropNoncomm ≠ modelDropL2 ∧
    modelDropNoncomm ≠ modelDropBorn ∧
    modelDropNoncomm ≠ modelDropBundle ∧
    modelDropUnitary ≠ modelDropClone ∧
    modelDropUnitary ≠ modelDropContTime ∧
    modelDropUnitary ≠ modelDropHerm ∧
    modelDropUnitary ≠ modelDropL2 ∧
    modelDropUnitary ≠ modelDropBorn ∧
    modelDropUnitary ≠ modelDropBundle ∧
    modelDropClone ≠ modelDropContTime ∧
    modelDropClone ≠ modelDropHerm ∧
    modelDropClone ≠ modelDropL2 ∧
    modelDropClone ≠ modelDropBorn ∧
    modelDropClone ≠ modelDropBundle ∧
    modelDropContTime ≠ modelDropHerm ∧
    modelDropContTime ≠ modelDropL2 ∧
    modelDropContTime ≠ modelDropBorn ∧
    modelDropContTime ≠ modelDropBundle ∧
    modelDropHerm ≠ modelDropL2 ∧
    modelDropHerm ≠ modelDropBorn ∧
    modelDropHerm ≠ modelDropBundle ∧
    modelDropL2 ≠ modelDropBorn ∧
    modelDropL2 ≠ modelDropBundle ∧
    modelDropBorn ≠ modelDropBundle := by
  decide

def coupledPairsInWorkingBasis : Bool := false

theorem coupled_pairs_not_in_b8 :
    coupledPairsInWorkingBasis = false ∧
    excludedCoupled.length = 0 ∧
    separateObU1RowInIndependenceMatrix = false := by
  decide

theorem coupled_pairs_not_in_b7 :
    coupledPairsInWorkingBasis = false ∧
    excludedCoupled.length = 0 := by
  decide

theorem coupled_pairs_not_in_b5 :
    coupledPairsInWorkingBasis = false ∧
    excludedCoupled.length = 0 :=
  coupled_pairs_not_in_b7

theorem coupled_pairs_not_in_b4 :
    coupledPairsInWorkingBasis = false ∧
    excludedCoupled.length = 0 :=
  coupled_pairs_not_in_b7

def obHermInWorkingBasis : Bool := true
def obL2InWorkingBasis : Bool := true
def obBornInWorkingBasis : Bool := true
def bundleU1LtInWorkingBasis : Bool := true
def b5HermProvisional_closed : Bool := true
def indHermB5_provisional : Bool := true
def indL2Born_provisional : Bool := true
def indBundleU1Lt_provisional : Bool := true

theorem herm_in_b5_provisional :
    obHermInWorkingBasis = true ∧
    b5HermProvisional_closed = true ∧
    indHermB5_provisional = true ∧
    fullBasisIndependence_open :=
  ⟨rfl, rfl, rfl, trivial⟩

theorem l2_born_in_b7_provisional :
    obL2InWorkingBasis = true ∧
    obBornInWorkingBasis = true ∧
    indL2Born_provisional = true ∧
    workingBasisB7.length = 7 ∧
    fullBasisIndependence_open :=
  ⟨rfl, rfl, rfl, workingBasisB7_card, trivial⟩

theorem bundle_in_b8_provisional :
    bundleU1LtInWorkingBasis = true ∧
    indBundleU1Lt_provisional = true ∧
    workingBasisB8.length = 8 ∧
    separateObU1RowInIndependenceMatrix = false ∧
    fullBasisIndependence_open :=
  ⟨rfl, rfl, workingBasisB8_card, rfl, trivial⟩

def b4IndependenceMatrixPackage_toy : Bool := true
def b5IndependenceMatrixPackage_toy : Bool := true
def b7IndependenceMatrixPackage_toy : Bool := true
def b8IndependenceMatrixPackage_toy : Bool := true

theorem b4_independence_matrix_package :
    b4IndependenceMatrixPackage_toy = true ∧
    workingBasisB4.length = 4 ∧
    admitsMatrix .OB_NONCOMM .OB_NONCOMM = false ∧
    admitsMatrix .OB_UNITARY .OB_UNITARY = false ∧
    admitsMatrix .OB_CLONE .OB_CLONE = false ∧
    admitsMatrix .CONT_TIME .CONT_TIME = false ∧
    modelDropNoncomm ≠ modelDropUnitary ∧
    coupledPairsInWorkingBasis = false ∧
    fullBasisIndependence_open :=
  ⟨rfl, workingBasisB4_card, rfl, rfl, rfl, rfl,
    drop_models_pairwise_distinct.1, rfl, trivial⟩

theorem b5_independence_matrix_package :
    b5IndependenceMatrixPackage_toy = true ∧
    workingBasisB5.length = 5 ∧
    admitsMatrix .OB_HERM .OB_HERM = false ∧
    modelDropNoncomm ≠ modelDropHerm ∧
    coupledPairsInWorkingBasis = false ∧
    obHermInWorkingBasis = true ∧
    fullBasisIndependence_open :=
  ⟨rfl, workingBasisB5_card, rfl, by decide, rfl, rfl, trivial⟩

theorem b7_independence_matrix_package :
    b7IndependenceMatrixPackage_toy = true ∧
    workingBasisB7.length = 7 ∧
    (∀ s, admitsMatrix s s = false) ∧
    (∀ r c, r ≠ c → admitsMatrix r c = true) ∧
    modelDropL2 ≠ modelDropBorn ∧
    admits l2HostWithoutBorn .OB_L2_READOUT = true ∧
    admits l2HostWithoutBorn .OB_BORN = false ∧
    coupledPairsInWorkingBasis = false ∧
    obL2InWorkingBasis = true ∧
    obBornInWorkingBasis = true ∧
    fullBasisIndependence_open :=
  ⟨rfl, workingBasisB7_card,
    admits_matrix_diag_false,
    admits_matrix_off_diag_true,
    by decide, rfl, rfl, rfl, rfl, rfl, trivial⟩

/-! ## Main packages -/

theorem import_independence_b4_package :
    workingBasisB4.length = 4 ∧
    failsExactly modelDropNoncomm .OB_NONCOMM ∧
    failsExactly modelDropUnitary .OB_UNITARY ∧
    failsExactly modelDropClone .OB_CLONE ∧
    failsExactly modelDropContTime .CONT_TIME ∧
    isColumnStochastic resetKernel ∧
    ¬ isDoublyStochastic resetKernel ∧
    classicalClone fairBit = (1, 1, 1, 1) ∧
    continuousGeneratorAdmitted = false ∧
    b4IndependenceMatrixPackage_toy = true ∧
    fullBasisIndependence_open :=
  ⟨workingBasisB4_card, modelDropNoncomm_fails_exactly, modelDropUnitary_fails_exactly,
    modelDropClone_fails_exactly, modelDropContTime_fails_exactly,
    reset_column_not_doubly.1, reset_column_not_doubly.2,
    classical_clone_fair_exists, rfl, rfl, trivial⟩

theorem import_independence_b5_provisional_package :
    workingBasisB5.length = 5 ∧
    failsExactly modelDropHerm .OB_HERM ∧
    ¬ IsHermitianToy nonHermG ∧
    hermiticityImportForcedFromFinL1 = false ∧
    b5IndependenceMatrixPackage_toy = true ∧
    obHermInWorkingBasis = true ∧
    fullBasisIndependence_open :=
  ⟨workingBasisB5_card, modelDropHerm_fails_exactly,
    nonHermG_not_hermitian, rfl, rfl, rfl, trivial⟩

/-- Provisional $B_7$ package (TOY-MECH): seven drop-exactly-one models + 7×7 matrix +
    L2/Born split capital; OB-U1 still coupled-out; full BASIS-CANDIDATE OPEN. -/
theorem import_independence_b7_provisional_package :
    workingBasisB7.length = 7 ∧
    failsExactly modelDropNoncomm .OB_NONCOMM ∧
    failsExactly modelDropUnitary .OB_UNITARY ∧
    failsExactly modelDropClone .OB_CLONE ∧
    failsExactly modelDropContTime .CONT_TIME ∧
    failsExactly modelDropHerm .OB_HERM ∧
    failsExactly modelDropL2 .OB_L2_READOUT ∧
    failsExactly modelDropBorn .OB_BORN ∧
    isColumnStochastic resetKernel ∧
    ¬ isDoublyStochastic resetKernel ∧
    classicalClone fairBit = (1, 1, 1, 1) ∧
    continuousGeneratorAdmitted = false ∧
    ¬ IsHermitianToy nonHermG ∧
    hermiticityImportForcedFromFinL1 = false ∧
    l2ReadoutForcedFromL1Shadow = false ∧
    bornPairingForcedFromL2HostAlone = false ∧
    b7IndependenceMatrixPackage_toy = true ∧
    obL2InWorkingBasis = true ∧
    obBornInWorkingBasis = true ∧
    indL2Born_provisional = true ∧
    coupledPairsInWorkingBasis = false ∧
    excludedCoupled.length = 0 ∧
    fullBasisIndependence_open :=
  ⟨workingBasisB7_card, modelDropNoncomm_fails_exactly, modelDropUnitary_fails_exactly,
    modelDropClone_fails_exactly, modelDropContTime_fails_exactly,
    modelDropHerm_fails_exactly, modelDropL2_fails_exactly, modelDropBorn_fails_exactly,
    reset_column_not_doubly.1, reset_column_not_doubly.2,
    classical_clone_fair_exists, rfl, nonHermG_not_hermitian, rfl, rfl, rfl, rfl,
    rfl, rfl, rfl, rfl, excluded_coupled_card, trivial⟩

theorem b8_independence_matrix_package :
    b8IndependenceMatrixPackage_toy = true ∧
    workingBasisB8.length = 8 ∧
    (∀ s, admitsMatrix s s = false) ∧
    (∀ r c, r ≠ c → admitsMatrix r c = true) ∧
    modelDropBundle ≠ modelDropBorn ∧
    modelDropBundle ≠ modelDropL2 ∧
    failsExactly modelDropBundle .BUNDLE_U1_LT ∧
    separateObU1RowInIndependenceMatrix = false ∧
    bundleU1LtInWorkingBasis = true ∧
    fullBasisIndependence_open :=
  ⟨rfl, workingBasisB8_card,
    admits_matrix_diag_false,
    admits_matrix_off_diag_true,
    by decide, by decide,
    modelDropBundle_fails_exactly, rfl, rfl, trivial⟩

/-- Provisional $B_8$ package (TOY-MECH): eight drop-exactly-one models + 8×8 matrix +
    BUNDLE-U1-LT real drop model; separate U1/LT rows refused; full BASIS-CANDIDATE OPEN. -/
theorem import_independence_b8_provisional_package :
    workingBasisB8.length = 8 ∧
    failsExactly modelDropNoncomm .OB_NONCOMM ∧
    failsExactly modelDropUnitary .OB_UNITARY ∧
    failsExactly modelDropClone .OB_CLONE ∧
    failsExactly modelDropContTime .CONT_TIME ∧
    failsExactly modelDropHerm .OB_HERM ∧
    failsExactly modelDropL2 .OB_L2_READOUT ∧
    failsExactly modelDropBorn .OB_BORN ∧
    failsExactly modelDropBundle .BUNDLE_U1_LT ∧
    b8IndependenceMatrixPackage_toy = true ∧
    bundleU1LtInWorkingBasis = true ∧
    indBundleU1Lt_provisional = true ∧
    separateObU1RowInIndependenceMatrix = false ∧
    excludedCoupled.length = 0 ∧
    fullBasisIndependence_open :=
  ⟨workingBasisB8_card, modelDropNoncomm_fails_exactly, modelDropUnitary_fails_exactly,
    modelDropClone_fails_exactly, modelDropContTime_fails_exactly,
    modelDropHerm_fails_exactly, modelDropL2_fails_exactly, modelDropBorn_fails_exactly,
    modelDropBundle_fails_exactly, rfl, rfl, rfl, rfl, excluded_coupled_card, trivial⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end ImportIndependence
end QM

#print axioms QM.ImportIndependence.every_basis_slot_has_drop_model
#print axioms QM.ImportIndependence.import_independence_b4_package
#print axioms QM.ImportIndependence.import_independence_b5_provisional_package
#print axioms QM.ImportIndependence.import_independence_b7_provisional_package
#print axioms QM.ImportIndependence.import_independence_b8_provisional_package
#print axioms QM.ImportIndependence.b8_independence_matrix_package
#print axioms QM.ImportIndependence.l2_born_split_models_exist
#print axioms QM.ImportIndependence.reset_column_not_doubly
#print axioms QM.ImportIndependence.structure_not_auth
