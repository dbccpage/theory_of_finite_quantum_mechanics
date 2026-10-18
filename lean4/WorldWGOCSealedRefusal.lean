/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import WorldReconstructionRetraction

/-!
# W8.2: finite refusal at the sealed REC-FULL/WGOC entry boundary

The deferred Codebase-as-WGOC target requires a sealed REC-FULL premise
surface before a WGOC binding may be promoted.  This file records the smallest
typed refusal supported by the Q12 diagonal retraction.

Eight dependency names are represented by a finite inductive type.  Their
local status is read from the exact Q12 retraction, except for the separately
declared general matrix-host slot.  The combined composition/local-tomography
slot requires both corresponding Q12 flags.  Every status is false for this
one exact package, so packaging the diagonal fixture cannot inhabit the sealed
entry premise.

`ActionLaws` and `GateSurface` below are deliberately abstract propositions.
No external action, gate, repository, build-state, or WGOC semantics is
inspected or asserted.  The result is not global nonexistence, not a WGOC
theorem, and not REC-FULL.  It is only a finite refusal witness for the declared
local package.

Primitive-Difference promotion is false and AuthorityEffect is None.
-/

namespace OmegaWorld
namespace WGOCSealedRefusal

open ReconstructionQ12

/-- The eight ordered REC-FULL dependencies bound by the Q12 retraction. -/
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

/-- Exact source identifier for each typed dependency. -/
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

/-
The Q12 retraction has explicit negative fields for seven of the eight typed
dependency rows.  Its finite integer matrix is not a general finite-n complex
matrix host, so that separate row is carried as an explicit local false flag.
-/
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

/-- Read one declared dependency flag from a bounded local audit. -/
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

/--
A necessary declared flag surface has every row asserted.  This is only a
negative entry check: even all-true flags would not construct sealed evidence.
-/
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

/-- The Q12 local package contains exactly the finite audit and retraction. -/
def exactLocalPackage : LocalPackage :=
  packageConditional (exactFixtureAudit, diagonalReconstructionRetraction)

theorem exact_local_package_roundtrip :
    exposeConditional exactLocalPackage =
      (exactFixtureAudit, diagonalReconstructionRetraction) := by
  exact expose_package_roundtrip _

/-- Generic packaging preserves a supplied dependency status; it creates none. -/
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

/-
This is only a necessary sealed-flag entry shape used by the refusal.  It is
not a sufficient REC-FULL evidence type.  The two abstract propositions are
not definitions of real WGOC action or gate semantics, and no inhabitant for
either is constructed here.
-/
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

/-- Bundled finite witness, retaining every negative scope fence as data. -/
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
