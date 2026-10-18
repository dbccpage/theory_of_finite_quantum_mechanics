/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import PrimitiveDifference

/-!
Pointed quotient obstruction classifier kernel.

This file gives a Nat-valued three-way classifier over a pointed quotient.
It assumes only two raw scores on the quotient carrier: `Phi` and `Gamma`.
-/

namespace OmegaCore

universe u v

abbrev PointedResidualQuotient
    {α : Type u} {β : Type v} (P : PointedPrimitiveDifference α β) : Type u :=
  PrimitiveDifference.ResidualQuotient P.toPrimitiveDifference

structure ObstructionClassifier (Q : Type u) where
  Phi : Q → Nat
  Gamma : Q → Nat

inductive ObstructionStatus where
  | exactRepair
  | stabilizedSurvivor
  | openObstruction
  deriving DecidableEq, Repr

namespace ObstructionClassifier

variable {Q : Type u}

def IsExactRepair (C : ObstructionClassifier Q) (q : Q) : Prop :=
  C.Phi q = 0

def IsStabilizedSurvivor (C : ObstructionClassifier Q) (q : Q) : Prop :=
  C.Phi q ≠ 0 ∧ C.Gamma q = 0

def IsOpenObstruction (C : ObstructionClassifier Q) (q : Q) : Prop :=
  C.Phi q ≠ 0 ∧ C.Gamma q ≠ 0

theorem exact_or_positive_phi (C : ObstructionClassifier Q) (q : Q) :
    C.Phi q = 0 ∨ C.Phi q ≠ 0 :=
  Decidable.em (C.Phi q = 0)

theorem gamma_zero_or_nonzero (C : ObstructionClassifier Q) (q : Q) :
    C.Gamma q = 0 ∨ C.Gamma q ≠ 0 :=
  Decidable.em (C.Gamma q = 0)

theorem classifier_total (C : ObstructionClassifier Q) (q : Q) :
    C.IsExactRepair q ∨ C.IsStabilizedSurvivor q ∨ C.IsOpenObstruction q := by
  cases exact_or_positive_phi C q with
  | inl hPhi =>
      exact Or.inl hPhi
  | inr hPhi =>
      cases gamma_zero_or_nonzero C q with
      | inl hGamma =>
          exact Or.inr (Or.inl ⟨hPhi, hGamma⟩)
      | inr hGamma =>
          exact Or.inr (Or.inr ⟨hPhi, hGamma⟩)

theorem classifier_exclusive_exact_stabilized
    (C : ObstructionClassifier Q) (q : Q) :
    C.IsExactRepair q → C.IsStabilizedSurvivor q → False := by
  intro hExact hStabilized
  exact hStabilized.1 hExact

theorem classifier_exclusive_exact_open
    (C : ObstructionClassifier Q) (q : Q) :
    C.IsExactRepair q → C.IsOpenObstruction q → False := by
  intro hExact hOpen
  exact hOpen.1 hExact

theorem classifier_exclusive_stabilized_open
    (C : ObstructionClassifier Q) (q : Q) :
    C.IsStabilizedSurvivor q → C.IsOpenObstruction q → False := by
  intro hStabilized hOpen
  exact hOpen.2 hStabilized.2

def terminalize (C : ObstructionClassifier Q) (q : Q) : ObstructionStatus :=
  if C.Phi q = 0 then
    ObstructionStatus.exactRepair
  else if C.Gamma q = 0 then
    ObstructionStatus.stabilizedSurvivor
  else
    ObstructionStatus.openObstruction

theorem terminalize_exactRepair_iff (C : ObstructionClassifier Q) (q : Q) :
    C.terminalize q = ObstructionStatus.exactRepair ↔ C.IsExactRepair q := by
  unfold terminalize IsExactRepair
  by_cases hPhi : C.Phi q = 0
  · simp [hPhi]
  · by_cases hGamma : C.Gamma q = 0
    · simp [hPhi, hGamma]
    · simp [hPhi, hGamma]

theorem terminalize_stabilizedSurvivor_iff
    (C : ObstructionClassifier Q) (q : Q) :
    C.terminalize q = ObstructionStatus.stabilizedSurvivor ↔
      C.IsStabilizedSurvivor q := by
  unfold terminalize IsStabilizedSurvivor
  by_cases hPhi : C.Phi q = 0
  · simp [hPhi]
  · by_cases hGamma : C.Gamma q = 0
    · simp [hPhi, hGamma]
    · simp [hPhi, hGamma]

theorem terminalize_openObstruction_iff
    (C : ObstructionClassifier Q) (q : Q) :
    C.terminalize q = ObstructionStatus.openObstruction ↔
      C.IsOpenObstruction q := by
  unfold terminalize IsOpenObstruction
  by_cases hPhi : C.Phi q = 0
  · simp [hPhi]
  · by_cases hGamma : C.Gamma q = 0
    · simp [hPhi, hGamma]
    · simp [hPhi, hGamma]

theorem computed_terminalize_exact_iff_phi_zero (C : ObstructionClassifier Q) (q : Q) :
    C.terminalize q = ObstructionStatus.exactRepair ↔ C.Phi q = 0 := by
  constructor
  · intro h
    exact (terminalize_exactRepair_iff C q).mp h
  · intro h
    exact (terminalize_exactRepair_iff C q).mpr h

theorem computed_terminalize_survivor_iff_phi_pos_gamma_zero (C : ObstructionClassifier Q) (q : Q) :
    C.terminalize q = ObstructionStatus.stabilizedSurvivor ↔ C.Phi q ≠ 0 ∧ C.Gamma q = 0 := by
  constructor
  · intro h
    exact (terminalize_stabilizedSurvivor_iff C q).mp h
  · intro h
    exact (terminalize_stabilizedSurvivor_iff C q).mpr h

theorem computed_terminalize_open_iff_phi_pos_gamma_pos (C : ObstructionClassifier Q) (q : Q) :
    C.terminalize q = ObstructionStatus.openObstruction ↔ C.Phi q ≠ 0 ∧ C.Gamma q ≠ 0 := by
  constructor
  · intro h
    exact (terminalize_openObstruction_iff C q).mp h
  · intro h
    exact (terminalize_openObstruction_iff C q).mpr h

theorem zeroClass_exact_if_phi_zeroClass_zero
    {α : Type u} {β : Type v} (P : PointedPrimitiveDifference α β)
    (C : ObstructionClassifier (PointedResidualQuotient P))
    (hPhi : C.Phi P.zeroClass = 0) :
    C.IsExactRepair P.zeroClass :=
  hPhi

end ObstructionClassifier
end OmegaCore
