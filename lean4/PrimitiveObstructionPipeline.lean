
import PointedObstructionClassifier


namespace OmegaCore
namespace PrimitiveObstructionPipeline

universe u v

variable {α : Type u} {β : Type v}

def phiQuot
    (P : PointedPrimitiveDifference α β)
    (phiRaw : α → Nat)
    (phi_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference phiRaw) :
    PointedResidualQuotient P → Nat :=
  PrimitiveDifference.invariantFactor P.toPrimitiveDifference phiRaw phi_congr

def gammaQuot
    (P : PointedPrimitiveDifference α β)
    (gammaRaw : α → Nat)
    (gamma_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference gammaRaw) :
    PointedResidualQuotient P → Nat :=
  PrimitiveDifference.invariantFactor P.toPrimitiveDifference gammaRaw gamma_congr

def rawObstructionClassifier
    (P : PointedPrimitiveDifference α β)
    (phiRaw gammaRaw : α → Nat)
    (phi_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference phiRaw)
    (gamma_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference gammaRaw) :
    ObstructionClassifier (PointedResidualQuotient P) where
  Phi := phiQuot P phiRaw phi_congr
  Gamma := gammaQuot P gammaRaw gamma_congr

def terminalizeRawClass
    (P : PointedPrimitiveDifference α β)
    (phiRaw gammaRaw : α → Nat)
    (phi_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference phiRaw)
    (gamma_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference gammaRaw)
    (x : α) : ObstructionStatus :=
  (rawObstructionClassifier P phiRaw gammaRaw phi_congr gamma_congr).terminalize
    (PrimitiveDifference.classOf P.toPrimitiveDifference x)

theorem phiQuot_classOf
    (P : PointedPrimitiveDifference α β)
    (phiRaw : α → Nat)
    (phi_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference phiRaw)
    (x : α) :
    phiQuot P phiRaw phi_congr
      (PrimitiveDifference.classOf P.toPrimitiveDifference x) = phiRaw x :=
  PrimitiveDifference.invariantFactor_classOf
    P.toPrimitiveDifference phiRaw phi_congr x

theorem gammaQuot_classOf
    (P : PointedPrimitiveDifference α β)
    (gammaRaw : α → Nat)
    (gamma_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference gammaRaw)
    (x : α) :
    gammaQuot P gammaRaw gamma_congr
      (PrimitiveDifference.classOf P.toPrimitiveDifference x) = gammaRaw x :=
  PrimitiveDifference.invariantFactor_classOf
    P.toPrimitiveDifference gammaRaw gamma_congr x

theorem terminalize_classOf_exact_iff
    (P : PointedPrimitiveDifference α β)
    (phiRaw gammaRaw : α → Nat)
    (phi_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference phiRaw)
    (gamma_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference gammaRaw)
    (x : α) :
    terminalizeRawClass P phiRaw gammaRaw phi_congr gamma_congr x =
      ObstructionStatus.exactRepair ↔ phiRaw x = 0 := by
  unfold terminalizeRawClass
  rw [ObstructionClassifier.terminalize_exactRepair_iff]
  unfold ObstructionClassifier.IsExactRepair rawObstructionClassifier
  change phiQuot P phiRaw phi_congr
      (PrimitiveDifference.classOf P.toPrimitiveDifference x) = 0 ↔
    phiRaw x = 0
  rw [phiQuot_classOf P phiRaw phi_congr x]

theorem terminalize_classOf_stabilized_iff
    (P : PointedPrimitiveDifference α β)
    (phiRaw gammaRaw : α → Nat)
    (phi_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference phiRaw)
    (gamma_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference gammaRaw)
    (x : α) :
    terminalizeRawClass P phiRaw gammaRaw phi_congr gamma_congr x =
      ObstructionStatus.stabilizedSurvivor ↔
      phiRaw x ≠ 0 ∧ gammaRaw x = 0 := by
  unfold terminalizeRawClass
  rw [ObstructionClassifier.terminalize_stabilizedSurvivor_iff]
  unfold ObstructionClassifier.IsStabilizedSurvivor rawObstructionClassifier
  change (phiQuot P phiRaw phi_congr
      (PrimitiveDifference.classOf P.toPrimitiveDifference x) ≠ 0 ∧
    gammaQuot P gammaRaw gamma_congr
      (PrimitiveDifference.classOf P.toPrimitiveDifference x) = 0) ↔
    phiRaw x ≠ 0 ∧ gammaRaw x = 0
  rw [phiQuot_classOf P phiRaw phi_congr x,
    gammaQuot_classOf P gammaRaw gamma_congr x]

theorem terminalize_classOf_open_iff
    (P : PointedPrimitiveDifference α β)
    (phiRaw gammaRaw : α → Nat)
    (phi_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference phiRaw)
    (gamma_congr :
      PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference gammaRaw)
    (x : α) :
    terminalizeRawClass P phiRaw gammaRaw phi_congr gamma_congr x =
      ObstructionStatus.openObstruction ↔
      phiRaw x ≠ 0 ∧ gammaRaw x ≠ 0 := by
  unfold terminalizeRawClass
  rw [ObstructionClassifier.terminalize_openObstruction_iff]
  unfold ObstructionClassifier.IsOpenObstruction rawObstructionClassifier
  change (phiQuot P phiRaw phi_congr
      (PrimitiveDifference.classOf P.toPrimitiveDifference x) ≠ 0 ∧
    gammaQuot P gammaRaw gamma_congr
      (PrimitiveDifference.classOf P.toPrimitiveDifference x) ≠ 0) ↔
    phiRaw x ≠ 0 ∧ gammaRaw x ≠ 0
  rw [phiQuot_classOf P phiRaw phi_congr x,
    gammaQuot_classOf P gammaRaw gamma_congr x]

theorem no_phiQuot_if_not_congruent
    (P : PointedPrimitiveDifference α β)
    (phiRaw : α → Nat)
    (hnot :
      ¬ PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference phiRaw) :
    ¬ (∃ Phi : PointedResidualQuotient P → Nat,
        ∀ x : α,
          Phi (PrimitiveDifference.classOf P.toPrimitiveDifference x) =
            phiRaw x) := by
  intro h
  rcases h with ⟨Phi, hPhi⟩
  exact hnot
    (PrimitiveDifference.invariantFactor_requires_congruence
      P.toPrimitiveDifference phiRaw Phi hPhi)

theorem no_gammaQuot_if_not_congruent
    (P : PointedPrimitiveDifference α β)
    (gammaRaw : α → Nat)
    (hnot :
      ¬ PrimitiveDifference.InvariantCongruent P.toPrimitiveDifference gammaRaw) :
    ¬ (∃ Gamma : PointedResidualQuotient P → Nat,
        ∀ x : α,
          Gamma (PrimitiveDifference.classOf P.toPrimitiveDifference x) =
            gammaRaw x) := by
  intro h
  rcases h with ⟨Gamma, hGamma⟩
  exact hnot
    (PrimitiveDifference.invariantFactor_requires_congruence
      P.toPrimitiveDifference gammaRaw Gamma hGamma)

end PrimitiveObstructionPipeline
end OmegaCore

private def l5aProvenance : String :=
  "Origin: lean4/PrimitiveObstructionPipeline.lean Claim: phiQuot_classOf AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
