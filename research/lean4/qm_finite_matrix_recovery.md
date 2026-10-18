import Mathlib.Tactic

/-!
# QMFiniteMatrixRecovery — W7.1 (partial finite matrix QM reconstruction)

Programme target: DERIV-MASTER W7.1 (path §F.37).

**Job:** package a **partial reconstruction** of finite-dimensional matrix QM from
FinL1 + Rung 5–6 surplus + working import basis $B_4$ + spectral/instrument
toys + Wave-7 ops + Born import (W6.5) + lift package (W5.8). Component card
can reach 17/17 under the **full-ops package**; the sealed full $M_n(\mathbb{C})$
recovery theorem remains **OPEN**.

## Honesty (package ≠ construction)

- Boolean package flags = checklist / presence registry, **not** construction witnesses.
- `partial_recovered_card` = 17 Recovered flags under the full-ops **package map**,
  **not** sealed reconstruction of $M_n(\mathbb{C})$.
- Full sealed recovery theorem remains **OPEN** (`sealedFullMatrixRecovery = false`).
- Mat2 / CHSH / spectral toys remain toys.

**This residual (A1 design outline):** deepen `REC-FULL-THEOREM` as a **sealed
recovery design** — staged reconstruction map (T01–T17 → `RecoveryStage`),
`sealedRecoveryClosed = false`, and packaging that 17/17 full-ops recovery
does **not** close the sealed $M_n(\mathbb{C})$ theorem. Depends on W6.21
sealed-sufficiency design posture; Gleason residual `GLEASON-ABS` stays OPEN.

**Residual 4 (obligation ledger):** `SealedRecoveryObligations` lists seal-grade
requirements that package/checklist flags do **not** discharge (algebra ≃ $M_n(\mathbb{C})$,
spectral theorem, GLEASON-ABS, import-independence absolute uniqueness). One
constructive TOY may be marked closed (`mat2AlgebraToyClosed`); overall
`sealedFullMatrixRecovery` remains **false**. Seal flip is human + proofs +
encyclopedia only — never auto-true from package card.

**Not claimed:** sealed full matrix QM theorem; real $M_n(\mathbb{C})$ construction;
Gleason; absolute outside-registry uniqueness; Wave-7 exit; authority.

AuthorityEffect: None.
-/

namespace QM
namespace FiniteMatrixRecovery

/-! ## Reconstruction components (aligned with freeze T01–T17) -/

inductive Component where
  | C_POP        -- T01
  | C_DIAG       -- T02
  | C_PURITY     -- T03
  | C_CHANNEL    -- T04
  | C_PATHSUM    -- T05
  | S_PHASE      -- T06
  | S_INTERF     -- T07
  | M_UNITARY    -- T12 (B4)
  | M_CLONE      -- T16 (B4)
  | R_LIFT       -- T08
  | R_SPECTRAL   -- T09
  | R_BORN       -- T10
  | R_COMPOSE    -- T11
  | R_INSTRUMENT -- T13
  | R_BELL       -- T14
  | R_CONTEXT    -- T15
  | R_FALSIFIER  -- T17
  deriving DecidableEq, Repr

def allComponents : List Component :=
  [.C_POP, .C_DIAG, .C_PURITY, .C_CHANNEL, .C_PATHSUM,
   .S_PHASE, .S_INTERF, .M_UNITARY, .M_CLONE,
   .R_LIFT, .R_SPECTRAL, .R_BORN, .R_COMPOSE,
   .R_INSTRUMENT, .R_BELL, .R_CONTEXT, .R_FALSIFIER]

theorem components_card : allComponents.length = 17 := by
  decide

inductive RecoverStatus where
  | Recovered
  | ResidualOpen
  deriving DecidableEq, Repr

/-- Full-ops package recovery map (all 17 components; sealed theorem still OPEN). -/
def recoverStatus : Component → RecoverStatus
  | .C_POP | .C_DIAG | .C_PURITY | .C_CHANNEL | .C_PATHSUM => .Recovered
  | .S_PHASE | .S_INTERF => .Recovered
  | .M_UNITARY | .M_CLONE => .Recovered
  | .R_SPECTRAL | .R_INSTRUMENT => .Recovered
  | .R_BELL | .R_CONTEXT | .R_FALSIFIER | .R_COMPOSE => .Recovered
  | .R_BORN => .Recovered
  | .R_LIFT => .Recovered

def recoveredComponents : List Component :=
  allComponents.filter (fun c => recoverStatus c = .Recovered)

def openComponents : List Component :=
  allComponents.filter (fun c => recoverStatus c = .ResidualOpen)

theorem partial_recovered_card : recoveredComponents.length = 17 := by
  decide

theorem residual_open_card : openComponents.length = 0 := by
  decide

/-! ## Package flags -/

structure RecoveryPackage where
  finL1 : Bool
  surplus : Bool
  b4 : Bool
  spectralToy : Bool
  instrumentToy : Bool
  bellToy : Bool
  contextToy : Bool
  falsifierToy : Bool
  composeToy : Bool
  bornToy : Bool
  liftToy : Bool
  deriving DecidableEq, Repr

/-- Core pathway only (legacy 9-component shape without spectral/instrument toys). -/
def corePartialPackage : RecoveryPackage :=
  { finL1 := true, surplus := true, b4 := true,
    spectralToy := false, instrumentToy := false,
    bellToy := false, contextToy := false,
    falsifierToy := false, composeToy := false, bornToy := false, liftToy := false }

/-- Spectral+instrument package (legacy 11-component shape). -/
def spectralInstrumentPackage : RecoveryPackage :=
  { finL1 := true, surplus := true, b4 := true,
    spectralToy := true, instrumentToy := true,
    bellToy := false, contextToy := false,
    falsifierToy := false, composeToy := false, bornToy := false, liftToy := false }

/-- Ops-extended package without Born/lift (legacy 15-component fence). -/
def opsExtendedWithoutBornPackage : RecoveryPackage :=
  { finL1 := true, surplus := true, b4 := true,
    spectralToy := true, instrumentToy := true,
    bellToy := true, contextToy := true,
    falsifierToy := true, composeToy := true, bornToy := false, liftToy := false }

/-- Born-ops-extended package without lift (legacy 16-component fence). -/
def bornOpsWithoutLiftPackage : RecoveryPackage :=
  { finL1 := true, surplus := true, b4 := true,
    spectralToy := true, instrumentToy := true,
    bellToy := true, contextToy := true,
    falsifierToy := true, composeToy := true, bornToy := true, liftToy := false }

/-- Full-ops partial package: ops + Born + lift pathways. -/
def partialPackage : RecoveryPackage :=
  { finL1 := true, surplus := true, b4 := true,
    spectralToy := true, instrumentToy := true,
    bellToy := true, contextToy := true,
    falsifierToy := true, composeToy := true, bornToy := true, liftToy := true }

def pureFinL1Package : RecoveryPackage :=
  { finL1 := true, surplus := false, b4 := false,
    spectralToy := false, instrumentToy := false,
    bellToy := false, contextToy := false,
    falsifierToy := false, composeToy := false, bornToy := false, liftToy := false }

def componentCovered (pkg : RecoveryPackage) : Component → Bool
  | .C_POP | .C_DIAG | .C_PURITY | .C_CHANNEL | .C_PATHSUM => pkg.finL1
  | .S_PHASE | .S_INTERF => pkg.surplus
  | .M_UNITARY | .M_CLONE => pkg.b4
  | .R_SPECTRAL => pkg.spectralToy
  | .R_INSTRUMENT => pkg.instrumentToy
  | .R_BELL => pkg.bellToy
  | .R_CONTEXT => pkg.contextToy
  | .R_FALSIFIER => pkg.falsifierToy
  | .R_COMPOSE => pkg.composeToy
  | .R_BORN => pkg.bornToy
  | .R_LIFT => pkg.liftToy

theorem partial_covers_pathway :
    componentCovered partialPackage .C_POP = true ∧
    componentCovered partialPackage .S_INTERF = true ∧
    componentCovered partialPackage .M_UNITARY = true ∧
    componentCovered partialPackage .M_CLONE = true ∧
    componentCovered partialPackage .R_SPECTRAL = true ∧
    componentCovered partialPackage .R_INSTRUMENT = true ∧
    componentCovered partialPackage .R_BELL = true ∧
    componentCovered partialPackage .R_CONTEXT = true ∧
    componentCovered partialPackage .R_FALSIFIER = true ∧
    componentCovered partialPackage .R_COMPOSE = true ∧
    componentCovered partialPackage .R_BORN = true ∧
    componentCovered partialPackage .R_LIFT = true := by
  decide

theorem core_partial_excludes_spectral_instrument :
    componentCovered corePartialPackage .R_SPECTRAL = false ∧
    componentCovered corePartialPackage .R_INSTRUMENT = false ∧
    componentCovered corePartialPackage .M_UNITARY = true := by
  decide

theorem spectral_instrument_excludes_ops :
    componentCovered spectralInstrumentPackage .R_SPECTRAL = true ∧
    componentCovered spectralInstrumentPackage .R_BELL = false ∧
    componentCovered spectralInstrumentPackage .R_CONTEXT = false ∧
    componentCovered spectralInstrumentPackage .R_FALSIFIER = false ∧
    componentCovered spectralInstrumentPackage .R_COMPOSE = false ∧
    componentCovered spectralInstrumentPackage .R_BORN = false ∧
    componentCovered spectralInstrumentPackage .R_LIFT = false := by
  decide

theorem ops_without_born_excludes_born :
    componentCovered opsExtendedWithoutBornPackage .R_BELL = true ∧
    componentCovered opsExtendedWithoutBornPackage .R_BORN = false ∧
    componentCovered opsExtendedWithoutBornPackage .R_LIFT = false := by
  decide

theorem born_ops_without_lift_excludes_lift :
    componentCovered bornOpsWithoutLiftPackage .R_BORN = true ∧
    componentCovered bornOpsWithoutLiftPackage .R_LIFT = false := by
  decide

theorem pure_finl1_incomplete :
    componentCovered pureFinL1Package .C_POP = true ∧
    componentCovered pureFinL1Package .S_PHASE = false ∧
    componentCovered pureFinL1Package .M_UNITARY = false ∧
    componentCovered pureFinL1Package .R_SPECTRAL = false ∧
    componentCovered pureFinL1Package .R_BORN = false ∧
    componentCovered pureFinL1Package .R_LIFT = false := by
  decide

/-! ## Concrete Amp2 + diagonal density toy -/

structure SectorWeight where
  w0 : Nat
  w1 : Nat
  deriving DecidableEq, Repr

/-- Diagonal density shadow: copy of sector weights (Rung 2 shape). -/
def diagFromWeights (w : SectorWeight) : Nat × Nat := (w.w0, w.w1)

theorem diag_from_weights :
    diagFromWeights { w0 := 3, w1 := 5 } = (3, 5) := by
  rfl

/-- Unnormalized Amp2 amplitudes (integer toy). -/
structure Amp2 where
  a0 : Int
  a1 : Int
  deriving DecidableEq, Repr

/-- Population weights via squares (Born-shape toy on computational basis). -/
def amp2Pop (ψ : Amp2) : Nat × Nat :=
  (ψ.a0.natAbs * ψ.a0.natAbs, ψ.a1.natAbs * ψ.a1.natAbs)

def ampPlus : Amp2 := { a0 := 1, a1 := 1 }
def ampZero : Amp2 := { a0 := 1, a1 := 0 }

theorem amp2_pop_squares :
    amp2Pop ampPlus = (1, 1) ∧ amp2Pop ampZero = (1, 0) := by
  decide

/-! ## Mat2 Pauli noncommute (matrix core toy; W6.6 shape) -/

structure Mat2 where
  a00 : Int
  a01 : Int
  a10 : Int
  a11 : Int
  deriving DecidableEq, Repr

def matMul (m n : Mat2) : Mat2 :=
  { a00 := m.a00 * n.a00 + m.a01 * n.a10
    a01 := m.a00 * n.a01 + m.a01 * n.a11
    a10 := m.a10 * n.a00 + m.a11 * n.a10
    a11 := m.a10 * n.a01 + m.a11 * n.a11 }

def matSub (m n : Mat2) : Mat2 :=
  { a00 := m.a00 - n.a00
    a01 := m.a01 - n.a01
    a10 := m.a10 - n.a10
    a11 := m.a11 - n.a11 }

def matZero : Mat2 := { a00 := 0, a01 := 0, a10 := 0, a11 := 0 }

def sigmaX : Mat2 := { a00 := 0, a01 := 1, a10 := 1, a11 := 0 }
def sigmaZ : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := -1 }

def commutator (A B : Mat2) : Mat2 := matSub (matMul A B) (matMul B A)

theorem pauli_xz_noncommute : commutator sigmaX sigmaZ ≠ matZero := by
  decide

theorem diag_observables_commute :
    commutator
      { a00 := 2, a01 := 0, a10 := 0, a11 := 3 }
      { a00 := 5, a01 := 0, a10 := 0, a11 := 7 } = matZero := by
  decide

/-! ## Spectral reconstruction toy (W6.10 capital bind — R_SPECTRAL)

Scaled spectral identity for $\sigma_x$: $2P_+ - 2P_- = 2\sigma_x$.
-/

def matAdd (m n : Mat2) : Mat2 :=
  { a00 := m.a00 + n.a00, a01 := m.a01 + n.a01
    a10 := m.a10 + n.a10, a11 := m.a11 + n.a11 }

def matSmul (k : Int) (m : Mat2) : Mat2 :=
  { a00 := k * m.a00, a01 := k * m.a01
    a10 := k * m.a10, a11 := k * m.a11 }

def twoPplus : Mat2 := { a00 := 1, a01 := 1, a10 := 1, a11 := 1 }
def twoPminus : Mat2 := { a00 := 1, a01 := -1, a10 := -1, a11 := 1 }

/-- Spectral reconstruction (scaled): $2P_+ - 2P_- = 2\sigma_x$. -/
theorem sigmaX_spectral_scaled :
    matSub twoPplus twoPminus = matSmul 2 sigmaX := by
  decide

/-! ## Instrument sector update toy (W6.12 capital bind — R_INSTRUMENT) -/

structure BitWeight where
  w0 : Nat
  w1 : Nat
  deriving DecidableEq, Repr

inductive SpectralOutcome where
  | lam0
  | lam1
  deriving DecidableEq, Repr

def spectralUpdate (w : BitWeight) : SpectralOutcome → BitWeight
  | .lam0 => { w0 := w.w0, w1 := 0 }
  | .lam1 => { w0 := 0, w1 := w.w1 }

theorem spectral_update_example :
    spectralUpdate { w0 := 3, w1 := 1 } .lam1 = { w0 := 0, w1 := 1 } := rfl

theorem spectral_update_idempotent (w : BitWeight) (o : SpectralOutcome) :
    spectralUpdate (spectralUpdate w o) o = spectralUpdate w o := by
  cases o <;> simp [spectralUpdate]

/-! ## Wave-7 ops recovery binds (this residual)

R_BELL ← W7.2 CHSH classical cap + Tsirelson square pathway (TOY).
R_CONTEXT ← W7.3 F₂ target parity obstruction shape (TOY).
R_FALSIFIER ← W7.6 T17 registered + synthetic inadequate classicalNull (TOY).
R_COMPOSE ← W6.14 product dimensions 2×2 → 4 (TOY).
-/

/-- Classical CHSH cap ≤ 2 (W7.2 classical half). -/
def sBool (b : Bool) : Int := if b then 1 else -1
def chsh (a₀ a₁ b₀ b₁ : Bool) : Int :=
  sBool a₀ * sBool b₀ + sBool a₀ * sBool b₁ + sBool a₁ * sBool b₀ - sBool a₁ * sBool b₁

theorem chsh_le_two : ∀ a₀ a₁ b₀ b₁ : Bool, chsh a₀ a₁ b₀ b₁ ≤ 2 := by
  decide

def classicalChshSquare : Nat := 4
def tsirelsonChshSquare : Nat := 8

theorem tsirelson_square_exceeds_classical :
    tsirelsonChshSquare > classicalChshSquare := by
  decide

/-- R_BELL recovered under quantum-host square package (not FinL1 alone). -/
def bellRecoveredUnderQuantumHost : Bool := true
def bellRecoveredUnderFinL1Alone : Bool := false

theorem r_bell_host_gated :
    bellRecoveredUnderQuantumHost = true ∧
    bellRecoveredUnderFinL1Alone = false ∧
    tsirelsonChshSquare > classicalChshSquare ∧
    chsh true true true true = 2 := by
  decide

/-- R_CONTEXT: MP F₂ target parity 1 ≠ coboundary parity 0 (W7.3 shape). -/
def mpTargetParity : Bool := true
def mpCoboundaryParity : Bool := false
def contextObstructionPresent : Bool := true

theorem r_context_obstruction :
    mpTargetParity ≠ mpCoboundaryParity ∧
    contextObstructionPresent = true := by
  decide

/-- R_FALSIFIER: T17 registered; classicalNull synthetic inadequate (W7.6). -/
def t17Registered : Bool := true
def classicalNullInadequate : Bool := true
def labExecution_closed : Bool := false

theorem r_falsifier_registered :
    t17Registered = true ∧
    classicalNullInadequate = true ∧
    labExecution_closed = false := by
  decide

/-- R_COMPOSE: product dimensions 2×2 → 4 (W6.14 product toy). -/
def dimA : Nat := 2
def dimB : Nat := 2
def productDim : Nat := dimA * dimB

theorem r_compose_product_dim :
    productDim = 4 ∧ dimA = 2 ∧ dimB = 2 := by
  decide

/-! ## R_BORN recovery bind (W6.5 capital — this residual)

Born-style diagonal pairing is effect-relative; pathway recovered only under
named Born import host (not FinL1 alone). Gleason uniqueness remains OPEN.
-/

structure Amp2Born where
  a0 : Nat
  a1 : Nat
  deriving DecidableEq, Repr

structure Effect2Born where
  e0 : Nat
  e1 : Nat
  deriving DecidableEq, Repr

def amp21Born : Amp2Born := { a0 := 2, a1 := 1 }
def eff0Born : Effect2Born := { e0 := 1, e1 := 0 }
def eff1Born : Effect2Born := { e0 := 0, e1 := 1 }

def bornPairingScalar (amp : Amp2Born) (eff : Effect2Born) : Nat :=
  amp.a0 * amp.a0 * eff.e0 + amp.a1 * amp.a1 * eff.e1

theorem born_pairing_effect_relative :
    bornPairingScalar amp21Born eff0Born ≠ bornPairingScalar amp21Born eff1Born := by
  decide

inductive BornHost where
  | finL1Alone
  | bornImportPackage
  deriving DecidableEq, Repr

def rBornPathwayRecovered : BornHost → Bool
  | .finL1Alone => false
  | .bornImportPackage => true

theorem r_born_host_gated :
    rBornPathwayRecovered .bornImportPackage = true ∧
    rBornPathwayRecovered .finL1Alone = false ∧
    bornPairingScalar amp21Born eff0Born = 4 ∧
    bornPairingScalar amp21Born eff1Born = 1 := by
  decide

def gleasonUniqueness_closed : Bool := false
def bornOpsExtendedPackage_toy : Bool := true

theorem born_ops_extended_recovery_package :
    bornOpsExtendedPackage_toy = true ∧
    componentCovered bornOpsWithoutLiftPackage .R_BORN = true ∧
    componentCovered bornOpsWithoutLiftPackage .R_LIFT = false ∧
    componentCovered opsExtendedWithoutBornPackage .R_BORN = false ∧
    componentCovered pureFinL1Package .R_BORN = false ∧
    rBornPathwayRecovered .bornImportPackage = true ∧
    rBornPathwayRecovered .finL1Alone = false ∧
    gleasonUniqueness_closed = false := by
  decide

/-! ## R_LIFT recovery bind (W5.8 capital — this residual)

Lift pathway recovered only under AX-LIFT-V0 package host selecting complex
Hilbert on the registry; not under FinL1 alone. Absolute uniqueness refused.
Sealed full matrix recovery theorem remains OPEN even at 17/17 component card.
-/

inductive LiftHost where
  | finL1Alone
  | axLiftV0Package
  deriving DecidableEq, Repr

def rLiftPathwayRecovered : LiftHost → Bool
  | .finL1Alone => false
  | .axLiftV0Package => true

theorem r_lift_host_gated :
    rLiftPathwayRecovered .axLiftV0Package = true ∧
    rLiftPathwayRecovered .finL1Alone = false := by
  decide

def fullOpsPackage_toy : Bool := true
def absoluteUniquenessClaim : Bool := false

/-! ## Full recovery fence

Component card 17/17 is **not** a sealed $M_n(\mathbb{C})$ theorem and is **not**
Wave-7 exit. Absolute uniqueness and Gleason remain open/refused.
-/

def fullMatrixRecovery_closed : Bool := false

theorem full_recovery_marked_open : fullMatrixRecovery_closed = false := by
  decide

theorem full_ops_lift_recovery_package :
    fullOpsPackage_toy = true ∧
    recoveredComponents.length = 17 ∧
    openComponents.length = 0 ∧
    componentCovered partialPackage .R_LIFT = true ∧
    componentCovered bornOpsWithoutLiftPackage .R_LIFT = false ∧
    componentCovered pureFinL1Package .R_LIFT = false ∧
    rLiftPathwayRecovered .axLiftV0Package = true ∧
    rLiftPathwayRecovered .finL1Alone = false ∧
    absoluteUniquenessClaim = false ∧
    fullMatrixRecovery_closed = false := by
  decide

def opsExtendedPackage_toy : Bool := true

theorem ops_extended_recovery_package :
    opsExtendedPackage_toy = true ∧
    componentCovered opsExtendedWithoutBornPackage .R_BELL = true ∧
    componentCovered opsExtendedWithoutBornPackage .R_CONTEXT = true ∧
    componentCovered opsExtendedWithoutBornPackage .R_FALSIFIER = true ∧
    componentCovered opsExtendedWithoutBornPackage .R_COMPOSE = true ∧
    componentCovered opsExtendedWithoutBornPackage .R_BORN = false ∧
    componentCovered spectralInstrumentPackage .R_BELL = false ∧
    chsh true true true true ≤ 2 ∧
    tsirelsonChshSquare > classicalChshSquare ∧
    mpTargetParity ≠ mpCoboundaryParity ∧
    t17Registered = true ∧
    productDim = 4 := by
  decide

/-- No residual-open components under full-ops map; sealed theorem still open. -/
theorem residual_open_is_empty :
    openComponents = ([] : List Component) := by
  decide

/-! ## Sealed recovery design outline (REC-FULL-THEOREM / A1)

Staged reconstruction design binding freeze T01–T17 components to five
recovery stages. This is a **design outline**, not a proved sealed theorem.
Depends on W6.21 sealed-sufficiency posture (`fullSufficiency_closed = false`
there). Gleason residual remains OPEN. Wave-7 exit not claimed.
-/

/-- Five-stage reconstruction ladder (design, not theorem). -/
inductive RecoveryStage where
  | ClassicalShadow   -- Stage 1: T01–T05 / FinL1
  | Surplus           -- Stage 2: T06–T07 / Rung 5–6
  | LiftHost          -- Stage 3: T08 / W5.8 conditional
  | SpectralBornCompose -- Stage 4: T09–T11, T13 / imports
  | Ops               -- Stage 5: T12, T14–T17 / dynamics·CHSH·MP·falsifier·clone
  deriving DecidableEq, Repr

/-- Component → stage map (freeze-aligned). -/
def componentStage : Component → RecoveryStage
  | .C_POP | .C_DIAG | .C_PURITY | .C_CHANNEL | .C_PATHSUM => .ClassicalShadow
  | .S_PHASE | .S_INTERF => .Surplus
  | .R_LIFT => .LiftHost
  | .R_SPECTRAL | .R_BORN | .R_COMPOSE | .R_INSTRUMENT => .SpectralBornCompose
  | .M_UNITARY | .M_CLONE | .R_BELL | .R_CONTEXT | .R_FALSIFIER => .Ops

def stageComponents (s : RecoveryStage) : List Component :=
  allComponents.filter (fun c => componentStage c = s)

theorem stage_classical_card : (stageComponents .ClassicalShadow).length = 5 := by
  decide

theorem stage_surplus_card : (stageComponents .Surplus).length = 2 := by
  decide

theorem stage_lift_card : (stageComponents .LiftHost).length = 1 := by
  decide

theorem stage_spectral_born_compose_card :
    (stageComponents .SpectralBornCompose).length = 4 := by
  decide

theorem stage_ops_card : (stageComponents .Ops).length = 5 := by
  decide

theorem stage_partition_card :
    (stageComponents .ClassicalShadow).length +
    (stageComponents .Surplus).length +
    (stageComponents .LiftHost).length +
    (stageComponents .SpectralBornCompose).length +
    (stageComponents .Ops).length = 17 := by
  decide

theorem component_stage_freeze_align :
    componentStage .C_POP = .ClassicalShadow ∧
    componentStage .S_PHASE = .Surplus ∧
    componentStage .R_LIFT = .LiftHost ∧
    componentStage .R_SPECTRAL = .SpectralBornCompose ∧
    componentStage .R_BORN = .SpectralBornCompose ∧
    componentStage .R_COMPOSE = .SpectralBornCompose ∧
    componentStage .R_INSTRUMENT = .SpectralBornCompose ∧
    componentStage .M_UNITARY = .Ops ∧
    componentStage .R_BELL = .Ops ∧
    componentStage .R_CONTEXT = .Ops ∧
    componentStage .R_FALSIFIER = .Ops ∧
    componentStage .M_CLONE = .Ops := by
  decide

/-- Named premise / obligation IDs per stage (design ledger strings). -/
def premiseDeps : RecoveryStage → List String
  | .ClassicalShadow =>
      ["OBL-FINL1-STATE", "OBL-DIAG-SHADOW", "OBL-PURITY",
       "OBL-CHANNEL-STOCH", "OBL-PATHSUM-CK"]
  | .Surplus =>
      ["OBL-PHASE-FIBER", "OBL-INTERF-CROSS"]
  | .LiftHost =>
      ["OBL-AX-LIFT-V0", "OBL-W5.8-CONDITIONAL", "OBL-NO-ABS-UNIQUENESS"]
  | .SpectralBornCompose =>
      ["OBL-SPECTRAL-FINITE", "OBL-BORN-IMPORT", "OBL-COMPOSE-MONOIDAL",
       "OBL-INSTRUMENT-LUDERS", "OBL-W6.21-SUF-PATHWAY"]
  | .Ops =>
      ["OBL-UNITARY-DYNAMICS", "OBL-CHSH-TSIRELSON", "OBL-MP-CONTEXT",
       "OBL-NO-CLONE", "OBL-GLOBAL-FALSIFIER"]

theorem premise_deps_nonempty :
    (premiseDeps .ClassicalShadow).length = 5 ∧
    (premiseDeps .Surplus).length = 2 ∧
    (premiseDeps .LiftHost).length = 3 ∧
    (premiseDeps .SpectralBornCompose).length = 5 ∧
    (premiseDeps .Ops).length = 5 := by
  decide

/-- Design seal flag: sealed full $M_n(\mathbb{C})$ recovery remains OPEN. -/
def sealedRecoveryClosed : Bool := false

/-- Canonical sealed $M_n(\mathbb{C})$ recovery flag (always false). Alias of sealedRecoveryClosed. -/
def sealedFullMatrixRecovery : Bool := false

/-- Package card 17/17 does **not** close sealed full matrix recovery. -/
theorem package_card_not_sealed_recovery :
    recoveredComponents.length = 17 ∧ sealedFullMatrixRecovery = false := by
  decide

theorem sealed_recovery_marked_open : sealedRecoveryClosed = false := by
  decide

theorem sealed_full_matrix_recovery_open : sealedFullMatrixRecovery = false := by
  decide

/-- Alias consistency: design seal ↔ legacy full-matrix closed flag. -/
theorem sealed_eq_full_matrix_flag :
    sealedRecoveryClosed = fullMatrixRecovery_closed := by
  decide

/-- Gleason residual remains OPEN under this design outline. -/
def gleasonAbs_closed : Bool := false

theorem gleason_abs_remains_open : gleasonAbs_closed = false := by
  decide

/-- Wave-7 exit not claimed by stage packaging. -/
def wave7Exit_claimed : Bool := false

theorem wave7_exit_not_claimed : wave7Exit_claimed = false := by
  decide

/-- W6.21 sealed-sufficiency dependency posture (design bind, not import of Lean). -/
def w621SealedSufficiency_dependency : Bool := true
def w621SealedSufficiency_closed : Bool := false

/-- Packaging: 17/17 recovered under full-ops **and** sealed still false. -/
theorem full_ops_recovered_sealed_still_open :
    recoveredComponents.length = 17 ∧
    openComponents.length = 0 ∧
    fullOpsPackage_toy = true ∧
    componentCovered partialPackage .R_LIFT = true ∧
    componentCovered partialPackage .R_BORN = true ∧
    componentCovered partialPackage .M_UNITARY = true ∧
    sealedRecoveryClosed = false ∧
    fullMatrixRecovery_closed = false ∧
    gleasonAbs_closed = false ∧
    wave7Exit_claimed = false ∧
    absoluteUniquenessClaim = false ∧
    w621SealedSufficiency_dependency = true ∧
    w621SealedSufficiency_closed = false := by
  decide

/-- Stage map packages all 17 components; none left unstaged. -/
theorem sealed_recovery_design_package :
    allComponents.length = 17 ∧
    recoveredComponents.length = 17 ∧
    (stageComponents .ClassicalShadow).length = 5 ∧
    (stageComponents .Surplus).length = 2 ∧
    (stageComponents .LiftHost).length = 1 ∧
    (stageComponents .SpectralBornCompose).length = 4 ∧
    (stageComponents .Ops).length = 5 ∧
    sealedRecoveryClosed = false ∧
    gleasonUniqueness_closed = false ∧
    gleasonAbs_closed = false ∧
    wave7Exit_claimed = false ∧
    fullOpsPackage_toy = true := by
  decide

/-! ## Sealed recovery design deepen (A1 → DAG + B7/B8 import bind)

Stage dependency DAG + provisional import-ledger bind (W6.19 B7 + W6.14
`BUNDLE-U1-LT` design). Still **not** a sealed $M_n(\mathbb{C})$ theorem.
-/

/-- Ordered stage ladder for the dependency DAG. -/
def stageOrder : List RecoveryStage :=
  [.ClassicalShadow, .Surplus, .LiftHost, .SpectralBornCompose, .Ops]

theorem stage_order_card : stageOrder.length = 5 := by
  decide

/-- Immediate prerequisites of each stage (design edges, not proved lemmas). -/
def stagePrereqs : RecoveryStage → List RecoveryStage
  | .ClassicalShadow => []
  | .Surplus => [.ClassicalShadow]
  | .LiftHost => [.ClassicalShadow, .Surplus]
  | .SpectralBornCompose => [.LiftHost]
  | .Ops => [.SpectralBornCompose]

theorem stage_prereq_classical_empty :
    stagePrereqs .ClassicalShadow = [] := rfl

theorem stage_prereq_ops_needs_spectral :
    stagePrereqs .Ops = [.SpectralBornCompose] := rfl

/-- Import-ledger slots the recovery design may consume (W6.19 B7 names). -/
inductive RecoveryImportSlot where
  | NONCOMM | UNITARY | CLONE | CONT_TIME | HERM | L2_READOUT | BORN
  | BUNDLE_U1_LT  -- W6.14 coupled bundle (not separate OB-U1)
  deriving DecidableEq, Repr

def provisionalRecoveryLedger : List RecoveryImportSlot :=
  [.NONCOMM, .UNITARY, .CLONE, .CONT_TIME, .HERM, .L2_READOUT, .BORN, .BUNDLE_U1_LT]

theorem provisional_recovery_ledger_card :
    provisionalRecoveryLedger.length = 8 := by
  decide

/-- Which recovery-import slots each stage is allowed to cite (design map). -/
def stageImportSlots : RecoveryStage → List RecoveryImportSlot
  | .ClassicalShadow => []
  | .Surplus => [.L2_READOUT]
  | .LiftHost => [.NONCOMM]
  | .SpectralBornCompose =>
      [.HERM, .UNITARY, .L2_READOUT, .BORN, .BUNDLE_U1_LT]
  | .Ops => [.UNITARY, .CLONE, .CONT_TIME, .NONCOMM, .L2_READOUT, .BORN]

theorem compose_stage_uses_bundle :
    RecoveryImportSlot.BUNDLE_U1_LT ∈ stageImportSlots .SpectralBornCompose := by
  decide

theorem classical_stage_uses_no_imports :
    stageImportSlots .ClassicalShadow = [] := rfl

/-- Per-stage sealed status under this design (no SealedClosed constructor). -/
inductive StageSealStatus where
  | PathwayPriced
  | SealedOpen
  deriving DecidableEq, Repr

def stageSealStatus : RecoveryStage → StageSealStatus
  | .ClassicalShadow => .PathwayPriced
  | .Surplus => .PathwayPriced
  | .LiftHost => .SealedOpen
  | .SpectralBornCompose => .SealedOpen
  | .Ops => .SealedOpen

theorem stage_seal_partition :
    stageSealStatus .ClassicalShadow = .PathwayPriced ∧
    stageSealStatus .Surplus = .PathwayPriced ∧
    stageSealStatus .LiftHost = .SealedOpen ∧
    stageSealStatus .SpectralBornCompose = .SealedOpen ∧
    stageSealStatus .Ops = .SealedOpen := by
  decide

/-- Finite-matrix reconstruction checklist (desire-1 packaging; not a seal). -/
structure FiniteMatrixReconstructionChecklist where
  classicalShadow : Bool
  interferenceSurplus : Bool
  importLedgerB8Design : Bool
  componentPathway17 : Bool
  stageDag : Bool
  sealedMnCTheorem : Bool
  wave7Exit : Bool
  gleasonAbs : Bool
  deriving DecidableEq, Repr

def finiteMatrixReconstructionChecklist : FiniteMatrixReconstructionChecklist :=
  { classicalShadow := true
    interferenceSurplus := true
    importLedgerB8Design := true
    componentPathway17 := true
    stageDag := true
    sealedMnCTheorem := false
    wave7Exit := false
    gleasonAbs := false }

theorem finite_matrix_reconstruction_checklist_honesty :
    finiteMatrixReconstructionChecklist.classicalShadow = true ∧
    finiteMatrixReconstructionChecklist.importLedgerB8Design = true ∧
    finiteMatrixReconstructionChecklist.stageDag = true ∧
    finiteMatrixReconstructionChecklist.sealedMnCTheorem = false ∧
    finiteMatrixReconstructionChecklist.wave7Exit = false ∧
    finiteMatrixReconstructionChecklist.gleasonAbs = false ∧
    sealedRecoveryClosed = false := by
  decide

/-- Sealed recovery design deepen package (A1 DAG + B8 ledger bind). -/
theorem sealed_recovery_design_deepen_package :
    stageOrder.length = 5 ∧
    provisionalRecoveryLedger.length = 8 ∧
    RecoveryImportSlot.BUNDLE_U1_LT ∈ stageImportSlots .SpectralBornCompose ∧
    stageSealStatus .Ops = .SealedOpen ∧
    finiteMatrixReconstructionChecklist.sealedMnCTheorem = false ∧
    sealedRecoveryClosed = false ∧
    wave7Exit_claimed = false ∧
    fullOpsPackage_toy = true ∧
    w621SealedSufficiency_closed = false := by
  decide

/-! ## SpectralBornCompose stage discharge (W6.10 / W6.14 / W6.5 / W6.12 bind)

Per-component **pathway discharge lemmas** for stage 4 under full-ops package.
Binds existing capital witnesses; does **not** seal `REC-FULL-THEOREM`.
-/

/-- Named capital witnesses consumed by SpectralBornCompose (dual of W6.10/14). -/
structure SpectralBornComposeWitness where
  /-- W6.10: $2P_+ - 2P_- = 2\sigma_x$ scaled spectral reconstruction. -/
  spectralScaledOk : Bool
  /-- W6.5: Born import host pathway present (not FinL1 alone). -/
  bornImportHost : Bool
  /-- W6.14: BUNDLE-U1-LT present in recovery ledger design. -/
  composeBundlePresent : Bool
  /-- W6.12: spectral sector update / Lüders-shape instrument bind. -/
  instrumentUpdateOk : Bool
  deriving DecidableEq, Repr

def spectralBornComposeWitness : SpectralBornComposeWitness :=
  { spectralScaledOk := true
    bornImportHost := true
    composeBundlePresent := true
    instrumentUpdateOk := true }

/-- Pathway discharge of a SpectralBornCompose component under a recovery package. -/
def sbcStageDischarges (pkg : RecoveryPackage) : Component → Bool
  | .R_SPECTRAL =>
      pkg.spectralToy && spectralBornComposeWitness.spectralScaledOk
  | .R_BORN =>
      pkg.bornToy && spectralBornComposeWitness.bornImportHost
  | .R_COMPOSE =>
      pkg.composeToy && spectralBornComposeWitness.composeBundlePresent
  | .R_INSTRUMENT =>
      pkg.instrumentToy && spectralBornComposeWitness.instrumentUpdateOk
  | _ => false

theorem sbc_components_are_four :
    stageComponents .SpectralBornCompose =
      [.R_SPECTRAL, .R_BORN, .R_COMPOSE, .R_INSTRUMENT] ∨
    (stageComponents .SpectralBornCompose).length = 4 := by
  right; exact stage_spectral_born_compose_card

/-- R_SPECTRAL discharged under full-ops via W6.10 scaled spectral capital. -/
theorem sbc_r_spectral_discharged :
    sbcStageDischarges partialPackage .R_SPECTRAL = true ∧
    matSub twoPplus twoPminus = matSmul 2 sigmaX ∧
    componentCovered partialPackage .R_SPECTRAL = true := by
  refine ⟨rfl, sigmaX_spectral_scaled, rfl⟩

/-- R_BORN discharged under full-ops via Born import host (W6.5 pathway). -/
theorem sbc_r_born_discharged :
    sbcStageDischarges partialPackage .R_BORN = true ∧
    componentCovered partialPackage .R_BORN = true ∧
    componentCovered pureFinL1Package .R_BORN = false := by
  decide

/-- R_COMPOSE discharged under full-ops via product dim + BUNDLE-U1-LT ledger. -/
theorem sbc_r_compose_discharged :
    sbcStageDischarges partialPackage .R_COMPOSE = true ∧
    productDim = 4 ∧
    RecoveryImportSlot.BUNDLE_U1_LT ∈ stageImportSlots .SpectralBornCompose ∧
    componentCovered pureFinL1Package .R_COMPOSE = false := by
  refine ⟨rfl, rfl, compose_stage_uses_bundle, rfl⟩

/-- R_INSTRUMENT discharged under full-ops via spectral update capital (W6.12). -/
theorem sbc_r_instrument_discharged :
    sbcStageDischarges partialPackage .R_INSTRUMENT = true ∧
    spectralUpdate { w0 := 3, w1 := 1 } .lam1 = { w0 := 0, w1 := 1 } ∧
    componentCovered partialPackage .R_INSTRUMENT = true := by
  decide

/-- Full-ops package discharges **all four** SpectralBornCompose components. -/
theorem spectral_born_compose_stage_discharged_under_full_ops :
    sbcStageDischarges partialPackage .R_SPECTRAL = true ∧
    sbcStageDischarges partialPackage .R_BORN = true ∧
    sbcStageDischarges partialPackage .R_COMPOSE = true ∧
    sbcStageDischarges partialPackage .R_INSTRUMENT = true ∧
    (stageComponents .SpectralBornCompose).length = 4 ∧
    RecoveryImportSlot.BUNDLE_U1_LT ∈ stageImportSlots .SpectralBornCompose ∧
    stageSealStatus .SpectralBornCompose = .SealedOpen ∧
    sealedRecoveryClosed = false ∧
    wave7Exit_claimed = false := by
  decide

/-- Pure FinL1 fails every SpectralBornCompose component (necessity fence). -/
theorem spectral_born_compose_fails_under_pure_finl1 :
    sbcStageDischarges pureFinL1Package .R_SPECTRAL = false ∧
    sbcStageDischarges pureFinL1Package .R_BORN = false ∧
    sbcStageDischarges pureFinL1Package .R_COMPOSE = false ∧
    sbcStageDischarges pureFinL1Package .R_INSTRUMENT = false := by
  decide

/-- SpectralBornCompose stage discharge package (TOY-MECH pathway; not seal). -/
theorem spectral_born_compose_stage_discharge_package :
    sbcStageDischarges partialPackage .R_SPECTRAL = true ∧
    sbcStageDischarges partialPackage .R_BORN = true ∧
    sbcStageDischarges partialPackage .R_COMPOSE = true ∧
    sbcStageDischarges partialPackage .R_INSTRUMENT = true ∧
    sbcStageDischarges pureFinL1Package .R_SPECTRAL = false ∧
    matSub twoPplus twoPminus = matSmul 2 sigmaX ∧
    productDim = 4 ∧
    RecoveryImportSlot.BUNDLE_U1_LT ∈ stageImportSlots .SpectralBornCompose ∧
    sealedRecoveryClosed = false ∧
    wave7Exit_claimed = false :=
  ⟨rfl, rfl, rfl, rfl, rfl, sigmaX_spectral_scaled, rfl,
    compose_stage_uses_bundle, rfl, rfl⟩

/-! ## REC-FULL-THEOREM residual deepen: all-stage pathway discharge

Pathway discharge of **all five** recovery stages under full-ops package.
This deepens the sealed recovery *design* residual toward theorem-grade
stage maps; it does **not** flip `sealedRecoveryClosed` / REC-FULL-THEOREM.
-/

/-- Stage pathway discharged ⇔ every component of the stage is covered. -/
def stagePathwayDischarged (pkg : RecoveryPackage) (s : RecoveryStage) : Bool :=
  (stageComponents s).all (fun c => componentCovered pkg c)

theorem classical_shadow_pathway_full_ops :
    stagePathwayDischarged partialPackage .ClassicalShadow = true := by
  decide

theorem surplus_pathway_full_ops :
    stagePathwayDischarged partialPackage .Surplus = true := by
  decide

theorem lift_host_pathway_full_ops :
    stagePathwayDischarged partialPackage .LiftHost = true := by
  decide

theorem spectral_born_compose_pathway_full_ops :
    stagePathwayDischarged partialPackage .SpectralBornCompose = true := by
  decide

theorem ops_pathway_full_ops :
    stagePathwayDischarged partialPackage .Ops = true := by
  decide

/-- Full-ops discharges every stage pathway (card-17 partition). -/
theorem all_stages_pathway_discharged_under_full_ops :
    stagePathwayDischarged partialPackage .ClassicalShadow = true ∧
    stagePathwayDischarged partialPackage .Surplus = true ∧
    stagePathwayDischarged partialPackage .LiftHost = true ∧
    stagePathwayDischarged partialPackage .SpectralBornCompose = true ∧
    stagePathwayDischarged partialPackage .Ops = true ∧
    stageOrder.length = 5 ∧
    (stageComponents .ClassicalShadow).length +
      (stageComponents .Surplus).length +
      (stageComponents .LiftHost).length +
      (stageComponents .SpectralBornCompose).length +
      (stageComponents .Ops).length = 17 := by
  decide

/-- Pure FinL1 pathway: ClassicalShadow only; later stages refuse. -/
theorem pure_finl1_pathway_fence :
    stagePathwayDischarged pureFinL1Package .ClassicalShadow = true ∧
    stagePathwayDischarged pureFinL1Package .Surplus = false ∧
    stagePathwayDischarged pureFinL1Package .LiftHost = false ∧
    stagePathwayDischarged pureFinL1Package .SpectralBornCompose = false ∧
    stagePathwayDischarged pureFinL1Package .Ops = false := by
  decide

/-- Obligation ledger for REC-FULL-THEOREM (pathway ≠ seal). -/
structure RecFullTheoremObligations where
  pathwayAllStagesFullOps : Bool
  sealedMnCTheorem : Bool
  gleasonAbs : Bool
  wave7Exit : Bool
  w621SealedSufficiency : Bool
  deriving DecidableEq, Repr

def recFullTheoremObligations : RecFullTheoremObligations :=
  { pathwayAllStagesFullOps := true
    sealedMnCTheorem := false
    gleasonAbs := false
    wave7Exit := false
    w621SealedSufficiency := false }

theorem rec_full_theorem_still_open :
    recFullTheoremObligations.sealedMnCTheorem = false ∧
    recFullTheoremObligations.gleasonAbs = false ∧
    recFullTheoremObligations.wave7Exit = false ∧
    recFullTheoremObligations.w621SealedSufficiency = false ∧
    sealedRecoveryClosed = false ∧
    wave7Exit_claimed = false ∧
    fullMatrixRecovery_closed = false := by
  decide

/-- REC-FULL residual deepen package: pathway capital under full-ops; theorem OPEN. -/
theorem rec_full_theorem_deepen_package :
    stagePathwayDischarged partialPackage .ClassicalShadow = true ∧
    stagePathwayDischarged partialPackage .Surplus = true ∧
    stagePathwayDischarged partialPackage .LiftHost = true ∧
    stagePathwayDischarged partialPackage .SpectralBornCompose = true ∧
    stagePathwayDischarged partialPackage .Ops = true ∧
    stagePathwayDischarged pureFinL1Package .SpectralBornCompose = false ∧
    stagePathwayDischarged pureFinL1Package .Ops = false ∧
    recFullTheoremObligations.pathwayAllStagesFullOps = true ∧
    recFullTheoremObligations.sealedMnCTheorem = false ∧
    sealedRecoveryClosed = false ∧
    wave7Exit_claimed = false ∧
    finiteMatrixReconstructionChecklist.sealedMnCTheorem = false ∧
    finiteMatrixReconstructionChecklist.wave7Exit = false ∧
    finiteMatrixReconstructionChecklist.gleasonAbs = false := by
  decide

/-! ## Sealed reconstruction obligation ledger (residual 4)

What sealed $M_n(\mathbb{C})$ recovery requires **beyond** package/checklist flags
and the 17/17 component pathway. Boolean package maps do not construct
algebra isomorphisms, spectral theorems, Gleason uniqueness, or absolute
import independence. One constructive **TOY** discharge is allowed
(`mat2AlgebraToyClosed`); overall seal remains false.

### Pathway to flip seal (never auto-true)

`sealedFullMatrixRecovery` may become true **only** after **all** of:

1. Human operator review of the encyclopedia + proof package
2. Lean proofs of algebra isomorphism / spectral / Born uniqueness
   (or documented residual retirement with human sign-off)
3. Import-independence absolute-uniqueness discharge or explicit residual keep
4. Encyclopedia entry recording seal promotion
5. Explicit human flip of the seal flag (not derived from package card)

Agents and package maps must not auto-set the seal.
-/

/-- Identity for the Mat2 integer matrix toy. -/
def matId : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := 1 }

/-- TOY: Mat2 as a constructive matrix-algebra witness (not $M_n(\mathbb{C})$).

Laws: closed under `matMul` by construction; unit; associativity on examples.
Labeled **TOY** — does not close sealed full matrix recovery.
-/
structure Mat2AsMatrixAlgebraToy where
  /-- `matMul : Mat2 → Mat2 → Mat2` lands in Mat2 (constructive closure). -/
  closedUnderMul : Bool
  /-- Left/right unit laws hold for `matId`. -/
  hasUnit : Bool
  /-- Multiplication associativity checked on concrete examples. -/
  mulAssocExamples : Bool
  /-- Left unit examples / general left unit. -/
  leftUnit : Bool
  /-- Right unit examples / general right unit. -/
  rightUnit : Bool
  deriving DecidableEq, Repr

/-- Constructive TOY discharge record for Mat2 integer matrix algebra. -/
def mat2_as_matrix_algebra_toy : Mat2AsMatrixAlgebraToy :=
  { closedUnderMul := true
    hasUnit := true
    mulAssocExamples := true
    leftUnit := true
    rightUnit := true }

theorem mat2_mul_left_unit (m : Mat2) : matMul matId m = m := by
  cases m with
  | mk a00 a01 a10 a11 =>
    have e00 : (1 : Int) * a00 + 0 * a10 = a00 := by omega
    have e01 : (1 : Int) * a01 + 0 * a11 = a01 := by omega
    have e10 : (0 : Int) * a00 + 1 * a10 = a10 := by omega
    have e11 : (0 : Int) * a01 + 1 * a11 = a11 := by omega
    simp [matMul, matId, e00, e01, e10, e11]

theorem mat2_mul_right_unit (m : Mat2) : matMul m matId = m := by
  cases m with
  | mk a00 a01 a10 a11 =>
    have e00 : a00 * (1 : Int) + a01 * 0 = a00 := by omega
    have e01 : a00 * (0 : Int) + a01 * 1 = a01 := by omega
    have e10 : a10 * (1 : Int) + a11 * 0 = a10 := by omega
    have e11 : a10 * (0 : Int) + a11 * 1 = a11 := by omega
    simp [matMul, matId, e00, e01, e10, e11]

/-- Concrete triple for associativity TOY (not general $n$). -/
def matToyA : Mat2 := sigmaX
def matToyB : Mat2 := sigmaZ
def matToyC : Mat2 := { a00 := 2, a01 := 1, a10 := 0, a11 := 3 }

theorem mat2_mul_assoc_example :
    matMul (matMul matToyA matToyB) matToyC =
      matMul matToyA (matMul matToyB matToyC) := by
  decide

theorem mat2_mul_assoc_pauli_xz :
    matMul (matMul sigmaX sigmaZ) sigmaX =
      matMul sigmaX (matMul sigmaZ sigmaX) := by
  decide

/-- Mat2 algebra TOY laws: unit + assoc examples + toy record true. -/
theorem mat2_as_matrix_algebra_toy_laws :
    matMul matId sigmaX = sigmaX ∧
    matMul sigmaX matId = sigmaX ∧
    matMul matId sigmaZ = sigmaZ ∧
    matMul sigmaZ matId = sigmaZ ∧
    matMul (matMul sigmaX sigmaZ) sigmaX =
      matMul sigmaX (matMul sigmaZ sigmaX) ∧
    matMul (matMul matToyA matToyB) matToyC =
      matMul matToyA (matMul matToyB matToyC) ∧
    mat2_as_matrix_algebra_toy.closedUnderMul = true ∧
    mat2_as_matrix_algebra_toy.hasUnit = true ∧
    mat2_as_matrix_algebra_toy.mulAssocExamples = true ∧
    mat2_as_matrix_algebra_toy.leftUnit = true ∧
    mat2_as_matrix_algebra_toy.rightUnit = true := by
  decide

/-- Seal-grade obligations package flags do **not** discharge.

Only the Mat2 algebra **TOY** may be marked closed; all real seal-grade
fields stay false, including overall `sealedFullMatrixRecovery`.
-/
structure SealedRecoveryObligations where
  /-- Algebra isomorphism to $M_n(\mathbb{C})$ (or star-algebra equiv). OPEN. -/
  algebraIsomorphismMnC : Bool
  /-- Spectral theorem for self-adjoints on the recovered carrier. OPEN. -/
  spectralTheoremSelfAdjoint : Bool
  /-- Born rule uniqueness residual `GLEASON-ABS`. OPEN. -/
  bornRuleUniquenessGleasonAbs : Bool
  /-- Import independence absolute uniqueness. OPEN. -/
  importIndependenceAbsoluteUniqueness : Bool
  /-- TOY only: Mat2 integer matrix algebra closed under mul + unit + assoc. -/
  mat2AlgebraToyClosed : Bool
  /-- Overall sealed full $M_n(\mathbb{C})$ recovery. Always false here. -/
  sealedFullMatrixRecovery : Bool
  deriving DecidableEq, Repr

/-- Live obligation ledger: one TOY closed; seal and seal-grade fields false. -/
def sealedRecoveryObligations : SealedRecoveryObligations :=
  { algebraIsomorphismMnC := false
    spectralTheoremSelfAdjoint := false
    bornRuleUniquenessGleasonAbs := false
    importIndependenceAbsoluteUniqueness := false
    mat2AlgebraToyClosed := true
    sealedFullMatrixRecovery := false }

/-- Human-only seal-flip pathway requirements (design ledger strings). -/
def sealedFlipPathwayRequirements : List String :=
  ["HUMAN-OPERATOR-REVIEW",
   "LEAN-ALGEBRA-ISOMORPHISM-MnC",
   "LEAN-SPECTRAL-SELF-ADJOINT",
   "GLEASON-ABS-RETIRE-OR-PROOF",
   "IMPORT-INDEPENDENCE-ABSOLUTE-UNIQUENESS",
   "ENCYCLOPEDIA-SEAL-PROMOTION-ENTRY",
   "EXPLICIT-HUMAN-FLAG-FLIP"]

/-- Seal must never auto-flip from package/checklist card. -/
def sealMayAutoFlipFromPackage : Bool := false

/-- Package card 17/17 + checklist do not imply sealed obligations discharged. -/
theorem sealed_recovery_requires_more_than_package :
    recoveredComponents.length = 17 ∧
    sealedFullMatrixRecovery = false ∧
    sealedRecoveryClosed = false ∧
    sealedRecoveryObligations.algebraIsomorphismMnC = false ∧
    sealedRecoveryObligations.spectralTheoremSelfAdjoint = false ∧
    sealedRecoveryObligations.bornRuleUniquenessGleasonAbs = false ∧
    sealedRecoveryObligations.importIndependenceAbsoluteUniqueness = false ∧
    sealedRecoveryObligations.mat2AlgebraToyClosed = true ∧
    sealedRecoveryObligations.sealedFullMatrixRecovery = false ∧
    finiteMatrixReconstructionChecklist.sealedMnCTheorem = false ∧
    recFullTheoremObligations.sealedMnCTheorem = false ∧
    gleasonAbs_closed = false ∧
    absoluteUniquenessClaim = false ∧
    sealMayAutoFlipFromPackage = false := by
  decide

/-- Mat2 TOY may close without flipping the overall seal. -/
theorem mat2_algebra_toy_does_not_seal_recovery :
    mat2_as_matrix_algebra_toy.closedUnderMul = true ∧
    sealedRecoveryObligations.mat2AlgebraToyClosed = true ∧
    sealedRecoveryObligations.sealedFullMatrixRecovery = false ∧
    sealedFullMatrixRecovery = false ∧
    matMul matId sigmaX = sigmaX ∧
    matMul (matMul sigmaX sigmaZ) sigmaX =
      matMul sigmaX (matMul sigmaZ sigmaX) := by
  decide

/-- Seal-flip pathway is non-empty design ledger; auto-flip refused. -/
theorem sealed_flip_pathway_human_only :
    sealedFlipPathwayRequirements.length = 7 ∧
    sealMayAutoFlipFromPackage = false ∧
    sealedFullMatrixRecovery = false ∧
    sealedRecoveryObligations.sealedFullMatrixRecovery = false ∧
    sealedRecoveryObligations.mat2AlgebraToyClosed = true := by
  decide

/-- Residual-4 package: obligation ledger + Mat2 TOY + seal still false. -/
theorem sealed_obligation_ledger_package :
    recoveredComponents.length = 17 ∧
    sealedRecoveryObligations.mat2AlgebraToyClosed = true ∧
    sealedRecoveryObligations.algebraIsomorphismMnC = false ∧
    sealedRecoveryObligations.spectralTheoremSelfAdjoint = false ∧
    sealedRecoveryObligations.bornRuleUniquenessGleasonAbs = false ∧
    sealedRecoveryObligations.importIndependenceAbsoluteUniqueness = false ∧
    sealedRecoveryObligations.sealedFullMatrixRecovery = false ∧
    sealedFullMatrixRecovery = false ∧
    mat2_as_matrix_algebra_toy.hasUnit = true ∧
    matMul matId matToyC = matToyC ∧
    sealMayAutoFlipFromPackage = false ∧
    sealedFlipPathwayRequirements.length = 7 := by
  decide

/-! ## Main package -/

theorem finite_matrix_recovery_partial_package :
    allComponents.length = 17 ∧
    recoveredComponents.length = 17 ∧
    openComponents.length = 0 ∧
    componentCovered partialPackage .M_UNITARY = true ∧
    componentCovered partialPackage .R_SPECTRAL = true ∧
    componentCovered partialPackage .R_INSTRUMENT = true ∧
    componentCovered partialPackage .R_BELL = true ∧
    componentCovered partialPackage .R_CONTEXT = true ∧
    componentCovered partialPackage .R_FALSIFIER = true ∧
    componentCovered partialPackage .R_COMPOSE = true ∧
    componentCovered partialPackage .R_BORN = true ∧
    componentCovered partialPackage .R_LIFT = true ∧
    componentCovered pureFinL1Package .M_UNITARY = false ∧
    componentCovered corePartialPackage .R_SPECTRAL = false ∧
    componentCovered bornOpsWithoutLiftPackage .R_LIFT = false ∧
    amp2Pop ampPlus = (1, 1) ∧
    commutator sigmaX sigmaZ ≠ matZero ∧
    matSub twoPplus twoPminus = matSmul 2 sigmaX ∧
    spectralUpdate { w0 := 3, w1 := 1 } .lam1 = { w0 := 0, w1 := 1 } ∧
    bornPairingScalar amp21Born eff0Born ≠ bornPairingScalar amp21Born eff1Born ∧
    rLiftPathwayRecovered .axLiftV0Package = true ∧
    fullOpsPackage_toy = true ∧
    fullMatrixRecovery_closed = false ∧
    sealedRecoveryClosed = false ∧
    sealedFullMatrixRecovery = false ∧
    sealedRecoveryObligations.sealedFullMatrixRecovery = false ∧
    sealedRecoveryObligations.mat2AlgebraToyClosed = true ∧
    provisionalRecoveryLedger.length = 8 ∧
    finiteMatrixReconstructionChecklist.sealedMnCTheorem = false := by
  decide

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end FiniteMatrixRecovery
end QM

#print axioms QM.FiniteMatrixRecovery.components_card
#print axioms QM.FiniteMatrixRecovery.finite_matrix_recovery_partial_package
#print axioms QM.FiniteMatrixRecovery.full_ops_lift_recovery_package
#print axioms QM.FiniteMatrixRecovery.born_ops_extended_recovery_package
#print axioms QM.FiniteMatrixRecovery.ops_extended_recovery_package
#print axioms QM.FiniteMatrixRecovery.full_ops_recovered_sealed_still_open
#print axioms QM.FiniteMatrixRecovery.sealed_recovery_design_package
#print axioms QM.FiniteMatrixRecovery.spectral_born_compose_stage_discharge_package
#print axioms QM.FiniteMatrixRecovery.rec_full_theorem_deepen_package
#print axioms QM.FiniteMatrixRecovery.sealed_recovery_requires_more_than_package
#print axioms QM.FiniteMatrixRecovery.mat2_as_matrix_algebra_toy_laws
#print axioms QM.FiniteMatrixRecovery.sealed_obligation_ledger_package
#print axioms QM.FiniteMatrixRecovery.pauli_xz_noncommute
#print axioms QM.FiniteMatrixRecovery.sigmaX_spectral_scaled
#print axioms QM.FiniteMatrixRecovery.structure_not_auth
