
import WorldReconstructionRetraction






namespace OmegaWorld
namespace WGOCSealedRefusal

open ReconstructionQ12

inductive RecFullDependency where
  | scalarQiC
  | obU1
  | liftCHilbertMatrix
  | posOrder
  | obComposeLocalTomography
  | obInstrument
  | obBorn
  | obCptp
  deriving DecidableEq

def dependencyId : RecFullDependency -> String
  | .scalarQiC => "SCALAR-QI-C"
  | .obU1 => "OB-U1"
  | .liftCHilbertMatrix => "LIFT-C-HILBERT-MATRIX"
  | .posOrder => "POS-ORDER"
  | .obComposeLocalTomography => "OB-COMPOSE-LT"
  | .obInstrument => "OB-INSTRUMENT"
  | .obBorn => "OB-BORN"
  | .obCptp => "OB-CPTP"

theorem dependency_id_injective : Function.Injective dependencyId := by
  intro left right
  cases left <;> cases right <;> decide

structure LocalPremiseAudit where
  retraction : DiagonalReconstructionRetraction
  retractionIsExact : retraction = diagonalReconstructionRetraction
  generalMatrixHostConstructed : Bool
  generalMatrixHostOpen : generalMatrixHostConstructed = false

def exactFixtureAudit : LocalPremiseAudit where
  retraction := diagonalReconstructionRetraction
  retractionIsExact := rfl
  generalMatrixHostConstructed := false
  generalMatrixHostOpen := rfl

def premiseClaim (audit : LocalPremiseAudit) : RecFullDependency -> Bool
  | .scalarQiC => audit.retraction.complexHostConstructed
  | .obU1 => audit.retraction.u1StructureConstructed
  | .liftCHilbertMatrix => audit.generalMatrixHostConstructed
  | .posOrder => audit.retraction.generalPositivityOrderConstructed
  | .obComposeLocalTomography =>
      audit.retraction.monoidalStructureConstructed &&
        audit.retraction.localTomographyConstructed
  | .obInstrument => audit.retraction.instrumentHostConstructed
  | .obBorn => audit.retraction.bornSelectionConstructed
  | .obCptp => audit.retraction.cptpStructureConstructed

def PremiseFlagAsserted (audit : LocalPremiseAudit)
    (dependency : RecFullDependency) : Prop :=
  premiseClaim audit dependency = true

def SealedRecFullSurface (audit : LocalPremiseAudit) : Prop :=
  forall dependency, PremiseFlagAsserted audit dependency

theorem exact_fixture_refuses_each_dependency
    (dependency : RecFullDependency) :
    premiseClaim exactFixtureAudit dependency = false := by
  cases dependency <;> rfl

theorem exact_fixture_not_sealed :
    ¬ SealedRecFullSurface exactFixtureAudit := by
  intro sealed
  have claimed : premiseClaim exactFixtureAudit .scalarQiC = true :=
    sealed .scalarQiC
  have refused := exact_fixture_refuses_each_dependency .scalarQiC
  rw [refused] at claimed
  cases claimed

abbrev LocalPackage :=
  ConditionalPackage LocalPremiseAudit DiagonalReconstructionRetraction

def exactLocalPackage : LocalPackage :=
  packageConditional (exactFixtureAudit, diagonalReconstructionRetraction)

theorem exact_local_package_roundtrip :
    exposeConditional exactLocalPackage =
      (exactFixtureAudit, diagonalReconstructionRetraction) := by
  exact expose_package_roundtrip _

theorem package_preserves_premise_claim
    (audit : LocalPremiseAudit)
    (recovery : DiagonalReconstructionRetraction)
    (dependency : RecFullDependency) :
    premiseClaim
        (packageConditional (audit, recovery)).explicitImports dependency =
      premiseClaim audit dependency := by
  rfl

theorem exact_local_package_refuses_each_dependency
    (dependency : RecFullDependency) :
    premiseClaim exactLocalPackage.explicitImports dependency = false := by
  exact exact_fixture_refuses_each_dependency dependency

theorem exact_local_package_not_sealed :
    ¬ SealedRecFullSurface exactLocalPackage.explicitImports := by
  intro sealed
  have claimed :
      premiseClaim exactLocalPackage.explicitImports .scalarQiC = true :=
    sealed .scalarQiC
  have refused := exact_local_package_refuses_each_dependency .scalarQiC
  rw [refused] at claimed
  cases claimed

structure WGOCSealedEntryPremises
    (ActionLaws GateSurface : Prop)
    (audit : LocalPremiseAudit) : Prop where
  actionLaws : ActionLaws
  gateSurface : GateSurface
  sealedRecFull : SealedRecFullSurface audit

theorem exact_local_package_refuses_wgoc_sealed_entry
    (ActionLaws GateSurface : Prop) :
    ¬ WGOCSealedEntryPremises
        ActionLaws GateSurface exactLocalPackage.explicitImports := by
  intro entry
  exact exact_local_package_not_sealed entry.sealedRecFull

theorem exact_local_package_rec_full_promotion_false :
    exactLocalPackage.conditionalRecovery.recFullClaimed = false := by
  rfl

theorem exact_local_package_primitive_difference_promotion_false :
    exactLocalPackage.conditionalRecovery.primitiveDifferenceDerivationClaimed =
      false := by
  rfl

theorem exact_local_package_authority_none :
    exactLocalPackage.conditionalRecovery.authorityEffect = AuthorityEffect.none := by
  rfl

structure FiniteWGOCSealedRefusal where
  package : LocalPackage
  packageIsExact : package = exactLocalPackage
  dependencyIdsInjective : Function.Injective dependencyId
  eachDependencyRefused : forall dependency,
    premiseClaim package.explicitImports dependency = false
  sealedSurfaceRefused :
    ¬ SealedRecFullSurface package.explicitImports
  wgocSealedEntryRefused : forall ActionLaws GateSurface : Prop,
    ¬ WGOCSealedEntryPremises
        ActionLaws GateSurface package.explicitImports
  recFullPromotionFalse :
    package.conditionalRecovery.recFullClaimed = false
  primitiveDifferencePromotionFalse :
    package.conditionalRecovery.primitiveDifferenceDerivationClaimed = false
  authorityEffect : AuthorityEffect
  authorityIsPackageEffect :
    authorityEffect = package.conditionalRecovery.authorityEffect
  authorityNone : authorityEffect = .none
  globalNonexistenceClaimed : Bool
  globalNonexistenceOpen : globalNonexistenceClaimed = false
  wgocTheoremClaimed : Bool
  wgocTheoremOpen : wgocTheoremClaimed = false
  externalHostSemanticsClaimed : Bool
  externalHostSemanticsOpen : externalHostSemanticsClaimed = false

def finiteWGOCSealedRefusal : FiniteWGOCSealedRefusal where
  package := exactLocalPackage
  packageIsExact := rfl
  dependencyIdsInjective := dependency_id_injective
  eachDependencyRefused := exact_local_package_refuses_each_dependency
  sealedSurfaceRefused := exact_local_package_not_sealed
  wgocSealedEntryRefused :=
    exact_local_package_refuses_wgoc_sealed_entry
  recFullPromotionFalse := exact_local_package_rec_full_promotion_false
  primitiveDifferencePromotionFalse :=
    exact_local_package_primitive_difference_promotion_false
  authorityEffect := .none
  authorityIsPackageEffect := rfl
  authorityNone := rfl
  globalNonexistenceClaimed := false
  globalNonexistenceOpen := rfl
  wgocTheoremClaimed := false
  wgocTheoremOpen := rfl
  externalHostSemanticsClaimed := false
  externalHostSemanticsOpen := rfl

#print axioms dependency_id_injective
#print axioms exact_fixture_refuses_each_dependency
#print axioms exact_fixture_not_sealed
#print axioms exact_local_package_roundtrip
#print axioms package_preserves_premise_claim
#print axioms exact_local_package_refuses_each_dependency
#print axioms exact_local_package_not_sealed
#print axioms exact_local_package_refuses_wgoc_sealed_entry
#print axioms exact_local_package_rec_full_promotion_false
#print axioms exact_local_package_primitive_difference_promotion_false
#print axioms exact_local_package_authority_none
#print axioms finiteWGOCSealedRefusal

end WGOCSealedRefusal
end OmegaWorld

private def l5aProvenance : String :=
  "Origin: lean4/WorldWGOCSealedRefusal.lean Claim: dependency_id_injective AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
