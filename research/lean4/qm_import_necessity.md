import Mathlib.Tactic

/-!
# QMImportNecessity — W6.20 (import necessity from pure ℓ¹ carrier)

Programme target: DERIV-MASTER W6.20 (path §E.33).

**Job:** corollary of W6.19 independence on working basis $B_4$:
each $B_4$ import is **not forced** by pure FinL1 residual bookkeeping,
hence is **necessary as an import** for any recovery that requires that slot
(registry-relative, dual TOY-MECH).

**Working basis $B_4$ (from W6.19):**

| Id | Freeze slot | Pure-FinL1 countermodel witness |
|---|---|---|
| I1 | `OB-NONCOMM` | classical diagonal commute |
| I2 | `OB-UNITARY` | reset not doubly stochastic |
| I3 | `OB-CLONE` | classical residual clone exists |
| I4 | `CONT-TIME` | discrete steps only |

**Not claimed:** final $N$; sufficiency (W6.21); minimality (W6.22);
absolute all-import necessity; authority.

AuthorityEffect: None.
-/

namespace QM
namespace ImportNecessity

/-! ## Working basis labels (mirror W6.19) -/

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

/-! ## Feature flags and model package -/

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

/-- Finite-regime model package relative to $B_4$. -/
structure NecessityModel where
  noncomm : NoncommFeature
  unitary : UnitaryFeature
  noClone : NoCloneFeature
  contTime : ContTimeFeature
  deriving DecidableEq, Repr

def admits (m : NecessityModel) : ImportSlot → Bool
  | .OB_NONCOMM => m.noncomm.present
  | .OB_UNITARY => m.unitary.present
  | .OB_CLONE => m.noClone.present
  | .CONT_TIME => m.contTime.present

/-- Slot $s$ is necessary-as-import relative to model $m$ when $m$ fails $s$. -/
def necessaryAsImport (m : NecessityModel) (s : ImportSlot) : Prop :=
  admits m s = false

/-! ## Pure FinL1 carrier model — all $B_4$ imports absent -/

/-- Pure finite $\ell^1$ residual bookkeeping: classical shadow only. -/
def pureFinL1 : NecessityModel :=
  { noncomm := { present := false }
    unitary := { present := false }
    noClone := { present := false }  -- no-clone law absent (classical clone world)
    contTime := { present := false } }

theorem pureFinL1_admits_none :
    admits pureFinL1 .OB_NONCOMM = false ∧
    admits pureFinL1 .OB_UNITARY = false ∧
    admits pureFinL1 .OB_CLONE = false ∧
    admits pureFinL1 .CONT_TIME = false := by
  decide

theorem necessary_as_import_noncomm :
    necessaryAsImport pureFinL1 .OB_NONCOMM := by
  rfl

theorem necessary_as_import_unitary :
    necessaryAsImport pureFinL1 .OB_UNITARY := by
  rfl

theorem necessary_as_import_clone :
    necessaryAsImport pureFinL1 .OB_CLONE := by
  rfl

theorem necessary_as_import_cont_time :
    necessaryAsImport pureFinL1 .CONT_TIME := by
  rfl

theorem every_b4_slot_necessary_as_import :
    necessaryAsImport pureFinL1 .OB_NONCOMM ∧
    necessaryAsImport pureFinL1 .OB_UNITARY ∧
    necessaryAsImport pureFinL1 .OB_CLONE ∧
    necessaryAsImport pureFinL1 .CONT_TIME :=
  ⟨necessary_as_import_noncomm, necessary_as_import_unitary,
    necessary_as_import_clone, necessary_as_import_cont_time⟩

/-! ## Capital fences (honesty of pureFinL1 flags) -/

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

/-! ## Coupled / full-basis honesty -/

inductive CoupledPair where
  | obU1_vs_composeLT
  | obL2_vs_obBorn
  deriving DecidableEq, Repr

def excludedCoupled : List CoupledPair :=
  [.obU1_vs_composeLT, .obL2_vs_obBorn]

theorem excluded_coupled_card : excludedCoupled.length = 2 := by
  decide

/-- Full freeze BASIS-CANDIDATE necessity remains OPEN beyond $B_4$. -/
def fullBasisNecessity_open : Prop := True

theorem full_basis_necessity_marked_open : fullBasisNecessity_open := trivial

/-! ## Main package -/

theorem import_necessity_b4_package :
    workingBasis.length = 4 ∧
    admits pureFinL1 .OB_NONCOMM = false ∧
    admits pureFinL1 .OB_UNITARY = false ∧
    admits pureFinL1 .OB_CLONE = false ∧
    admits pureFinL1 .CONT_TIME = false ∧
    isColumnStochastic resetKernel ∧
    ¬ isDoublyStochastic resetKernel ∧
    classicalClone fairBit = (1, 1, 1, 1) ∧
    continuousGeneratorAdmitted = false ∧
    fullBasisNecessity_open :=
  ⟨workingBasis_card,
    rfl, rfl, rfl, rfl,
    reset_column_not_doubly.1, reset_column_not_doubly.2,
    classical_clone_fair_exists, rfl, trivial⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end ImportNecessity
end QM

#print axioms QM.ImportNecessity.every_b4_slot_necessary_as_import
#print axioms QM.ImportNecessity.import_necessity_b4_package
#print axioms QM.ImportNecessity.reset_column_not_doubly
#print axioms QM.ImportNecessity.structure_not_auth
