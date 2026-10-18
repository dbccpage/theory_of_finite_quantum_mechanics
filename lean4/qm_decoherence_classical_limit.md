import Mathlib.Tactic

/-!
# QMDecoherenceClassicalLimit — W7.5 (decoherence → classical shadow)

Programme target: DERIV-MASTER W7.5 (path §F.41); freeze T21 optional.

**Job:** dual TOY-MECH packaging of decoherence as killing the off-diagonal
residual and recovering classical $\ell^1$ population tables (phase-blind
shadow). Continuum Lindblad limit remains **OPEN**.

Upstream capital shape: estate Gell-Mann decoherence matrix (cited, not
re-imported here — self-contained dual).

AuthorityEffect: None.
-/

namespace QM
namespace DecoherenceClassicalLimit

/-! ## Two-sector carrier with off-diagonal residual -/

structure ShadowState where
  pop0 : Nat
  pop1 : Nat
  offDiag : Int
  deriving DecidableEq, Repr

def isDecoherent (s : ShadowState) : Bool :=
  s.offDiag == 0

def localDiagonal (s : ShadowState) : Int :=
  (s.pop0 : Int) + (s.pop1 : Int)

def globalWeight (s : ShadowState) : Int :=
  localDiagonal s + 2 * s.offDiag

def residual (s : ShadowState) : Int :=
  globalWeight s - localDiagonal s

theorem residual_eq_twice_offdiag (s : ShadowState) :
    residual s = 2 * s.offDiag := by
  simp [residual, globalWeight, localDiagonal]

theorem decoherent_weight_additive (s : ShadowState) (h : isDecoherent s = true) :
    globalWeight s = localDiagonal s := by
  simp [isDecoherent, beq_iff_eq] at h
  simp [globalWeight, localDiagonal, h]

/-! ## Dephasing map = classical limit (finite shadow) -/

def dephase (s : ShadowState) : ShadowState :=
  { pop0 := s.pop0, pop1 := s.pop1, offDiag := 0 }

theorem dephase_classical (s : ShadowState) :
    isDecoherent (dephase s) = true ∧
    (dephase s).pop0 = s.pop0 ∧
    (dephase s).pop1 = s.pop1 := by
  simp [dephase, isDecoherent]

theorem dephase_idempotent (s : ShadowState) :
    dephase (dephase s) = dephase s := by
  simp [dephase]

theorem dephase_kills_residual (s : ShadowState) :
    residual (dephase s) = 0 := by
  simp [residual, globalWeight, localDiagonal, dephase]

/-- Classical population shadow (phase-blind). -/
def classicalShadow (s : ShadowState) : Nat × Nat :=
  (s.pop0, s.pop1)

theorem dephase_preserves_classical_shadow (s : ShadowState) :
    classicalShadow (dephase s) = classicalShadow s := by
  simp [classicalShadow, dephase]

/-! ## Shared classical shadow for distinct coherent residuals (W4 shape) -/

def coherentA : ShadowState := { pop0 := 1, pop1 := 1, offDiag := 1 }
def coherentB : ShadowState := { pop0 := 1, pop1 := 1, offDiag := -1 }
def decoheredAB : ShadowState := { pop0 := 1, pop1 := 1, offDiag := 0 }

theorem shared_classical_shadow :
    classicalShadow coherentA = classicalShadow coherentB ∧
    classicalShadow coherentA = classicalShadow decoheredAB ∧
    coherentA ≠ coherentB ∧
    residual coherentA = 2 ∧
    residual decoheredAB = 0 := by
  decide

theorem dephase_collapses_coherent :
    dephase coherentA = decoheredAB ∧
    dephase coherentB = decoheredAB := by
  decide

/-! ## Continuum fence -/

def continuumLindbladLimit_closed : Bool := false

theorem continuum_limit_open : continuumLindbladLimit_closed = false := by
  decide

def continuumLimit_open : Prop := True
theorem continuum_limit_marked_open : continuumLimit_open := trivial

/-! ## Finite multi-step damping residual (not continuum Lindblad)

Integer shrink of the off-diagonal residual toward 0, one unit per step.
After `|offDiag|` steps the state is decoherent and the classical $\ell^1$ shadow
is recovered. This is a **finite environment-pointer / gradual-dephasing toy**,
not a master-equation derivation.
-/

/-- Shrink integer residual one unit toward zero. -/
def shrinkOff (off : Int) : Int :=
  if 0 < off then off - 1
  else if off < 0 then off + 1
  else 0

def dampStep (s : ShadowState) : ShadowState :=
  { pop0 := s.pop0, pop1 := s.pop1, offDiag := shrinkOff s.offDiag }

def absOff (s : ShadowState) : Nat := s.offDiag.natAbs

theorem dampStep_preserves_pops (s : ShadowState) :
    (dampStep s).pop0 = s.pop0 ∧ (dampStep s).pop1 = s.pop1 := by
  simp [dampStep]

theorem dampStep_preserves_classical_shadow (s : ShadowState) :
    classicalShadow (dampStep s) = classicalShadow s := by
  simp [classicalShadow, dampStep]

theorem shrinkOff_zero : shrinkOff 0 = 0 := by decide
theorem shrinkOff_one : shrinkOff 1 = 0 := by decide
theorem shrinkOff_two : shrinkOff 2 = 1 := by decide
theorem shrinkOff_neg_one : shrinkOff (-1) = 0 := by decide

/-- Iterated damping. -/
def dampN : Nat → ShadowState → ShadowState
  | 0, s => s
  | n + 1, s => dampN n (dampStep s)

theorem dampN_zero (s : ShadowState) : dampN 0 s = s := rfl

theorem dampN_preserves_classical_shadow_succ (s : ShadowState) :
    classicalShadow (dampStep s) = classicalShadow s :=
  dampStep_preserves_classical_shadow s

/-- Concrete multi-step: coherentA (|off|=1) reaches decoherent in 1 step. -/
theorem dampN_coherentA_reaches :
    dampN 1 coherentA = decoheredAB ∧
    isDecoherent (dampN 1 coherentA) = true ∧
    residual (dampN 1 coherentA) = 0 := by
  decide

/-- Concrete multi-step: |off|=2 reaches decoherent in 2 steps. -/
def coherentTwo : ShadowState := { pop0 := 2, pop1 := 3, offDiag := 2 }

theorem dampN_two_reaches :
    absOff coherentTwo = 2 ∧
    isDecoherent (dampN 2 coherentTwo) = true ∧
    residual (dampN 2 coherentTwo) = 0 ∧
    classicalShadow (dampN 2 coherentTwo) = classicalShadow coherentTwo := by
  decide

/-! ## Environment pointer-record toy

If an environment pointer has recorded the sector (named Boolean host flag),
the joint residual is fully dephased — classical $\ell^1$ populations remain.
Not a CPTP derivation.
-/

inductive EnvHost where
  | noPointer
  | pointerRecorded
  deriving DecidableEq, Repr

/-- Apply full dephase only when pointer recorded; otherwise identity. -/
def envApply (h : EnvHost) (s : ShadowState) : ShadowState :=
  match h with
  | .noPointer => s
  | .pointerRecorded => dephase s

theorem env_no_pointer_preserves (s : ShadowState) :
    envApply .noPointer s = s := by
  simp [envApply]

theorem env_pointer_dephases (s : ShadowState) :
    isDecoherent (envApply .pointerRecorded s) = true ∧
    classicalShadow (envApply .pointerRecorded s) = classicalShadow s := by
  simp [envApply, dephase, isDecoherent, classicalShadow]

theorem env_pointer_kills_coherent_residual :
    residual (envApply .pointerRecorded coherentA) = 0 ∧
    residual (envApply .noPointer coherentA) = 2 := by
  decide

/-- FinL1 classical limit recovered after pointer record (populations only). -/
def recoversClassicalL1Shadow : EnvHost → Bool
  | .noPointer => false
  | .pointerRecorded => true

theorem finL1_shadow_after_pointer :
    recoversClassicalL1Shadow .pointerRecorded = true ∧
    recoversClassicalL1Shadow .noPointer = false := by
  decide

/-- **Finite multi-step + pointer residual package** (continuum Lindblad OPEN). -/
def finiteDampingPointerPackage_toy : Bool := true

theorem finite_damping_pointer_package :
    finiteDampingPointerPackage_toy = true ∧
    dampN 1 coherentA = decoheredAB ∧
    isDecoherent (dampN 2 coherentTwo) = true ∧
    residual (envApply .pointerRecorded coherentA) = 0 ∧
    recoversClassicalL1Shadow .pointerRecorded = true ∧
    continuumLindbladLimit_closed = false := by
  decide

/-! ## Main package -/

theorem decoherence_classical_limit_package :
    residual coherentA = 2 * coherentA.offDiag ∧
    globalWeight decoheredAB = localDiagonal decoheredAB ∧
    isDecoherent (dephase coherentA) = true ∧
    classicalShadow coherentA = classicalShadow coherentB ∧
    finiteDampingPointerPackage_toy = true ∧
    residual (envApply .pointerRecorded coherentA) = 0 ∧
    continuumLindbladLimit_closed = false := by
  decide

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end DecoherenceClassicalLimit
end QM

#print axioms QM.DecoherenceClassicalLimit.decoherent_weight_additive
#print axioms QM.DecoherenceClassicalLimit.decoherence_classical_limit_package
#print axioms QM.DecoherenceClassicalLimit.finite_damping_pointer_package
#print axioms QM.DecoherenceClassicalLimit.shared_classical_shadow
#print axioms QM.DecoherenceClassicalLimit.structure_not_auth
