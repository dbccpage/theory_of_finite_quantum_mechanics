import ScopeFirebreak
/-!
MUB cochain-obstruction: a contract surface plus one concrete discharged instance.

This module binds the Rust `omega_discrete_deformation_algebra::mub_cochain`
diagnostic objects to Lean obligations. The `MubCochainObstructionContract` /
`D10GtfocCrossValidationContract` structures are a **contract surface**: most
theorems below are projections of caller-supplied certificate fields, so they
prove "IF the obstruction machine supplies these certificates THEN the promotion
rules hold" — they do NOT themselves prove a MUB(6)/MUB(10) no-go or the wall.

Caveat (read before citing): each `Prop` field is bundled with its own proof
(`xCert : x`), so a hypothesis such as `(C : TripleClassCover) -> Not C.exhaustive`
can be unsatisfiable (every `TripleClassCover` carries `exhaustiveCert`). Those
"no authority without X" theorems are firewall scaffolding, not mathematical
content.

To give the cochain side REAL content (rather than only an opaque
`d1d0ZeroOrSupportDefect` hypothesis), this module also formalizes a concrete
finite cochain complex — the 3-edge triangle — and PROVES `d1 ∘ d0 = 0` for it
(`triangle_d1_comp_d0_zero`), then instantiates the contract from it
(`triangleWitnessContract`), so the cochain law is a genuinely discharged
obligation for at least one explicit instance and the contract is demonstrably
inhabitable.
-/

namespace MUB
namespace CochainObstruction

inductive Target where
  | mub6
  | mub10
  | generalN
  deriving DecidableEq

inductive RepairKind where
  | phaseGauge
  | basisRelabeling
  | vectorRelabeling
  | localUnitaryGauge
  | antiunitaryGauge
  | cliffordWeylGauge
  | galoisTransport
  | projectorLift
  | atlasTransportPotential
  | basisGluingPotential
  | psdSosLift
  deriving DecidableEq

inductive PrimitiveDefectKind where
  | orthonormality
  | mutualUnbiasedness
  | fourthVectorFeasibility
  | centeredProjectorResidual
  | simplexTiling
  | weylBoardIncidence
  | productFactor
  | atlasTransport
  | basisGluing
  | psdSosCertificate
  | gtmurRepresentationLoss
  deriving DecidableEq

inductive ClosureFailureKind where
  | atlasTransport
  | basisGluing
  | transportCoherence
  | tripleClassCover
  | certificateIdentity
  | representationLoss
  deriving DecidableEq

structure MubCochainObstructionContract where
  target : Target
  dimension : Nat
  requiredBasisCount : Nat
  fixedBasisCount : Nat
  repairKinds : List RepairKind
  primitiveDefectKinds : List PrimitiveDefectKind
  closureFailureKinds : List ClosureFailureKind
  zeroRelValidity : Prop
  d1d0ZeroOrSupportDefect : Prop
  quotientWellDefined : Prop
  phiGammaSeparated : Prop
  phi1Irreducible : Prop
  gamma2ClosureCharge : Prop
  atlasTransportPreservation : Prop
  basisGluingValidity : Prop
  pinnedTripleNoPromotion : Prop
  supportRealizationDefect : Prop
  c3AtlasCoherence : Prop
  d2c3AtlasCoherenceClassifiesMissingCover : Prop
  c3DefectsPreserveC2SourceKind : Prop
  classwiseObstruction : Prop
  basisGluingRequired : Prop
  basisGluingBlockedUntilC3Coherent : Prop
  basisGluingRequiresClasswiseObstruction : Prop
  tripleCarrierAtlasClassification : Prop
  atlasTransportToT0OrOwnCertificate : Prop
  classwiseCertificateBeforeBasisGluing : Prop
  fullMub6Authority : Prop
  zeroRelValidityCert : zeroRelValidity
  d1d0ZeroOrSupportDefectCert : d1d0ZeroOrSupportDefect
  quotientWellDefinedCert : quotientWellDefined
  phiGammaSeparatedCert : phiGammaSeparated
  phi1IrreducibleCert : phi1Irreducible
  gamma2ClosureChargeCert : gamma2ClosureCharge
  atlasTransportPreservationCert : atlasTransportPreservation
  basisGluingValidityCert : basisGluingValidity
  pinnedTripleNoPromotionCert : pinnedTripleNoPromotion
  d2c3AtlasCoherenceClassifiesMissingCoverCert :
    d2c3AtlasCoherenceClassifiesMissingCover
  c3DefectsPreserveC2SourceKindCert : c3DefectsPreserveC2SourceKind
  basisGluingBlockedUntilC3CoherentCert :
    basisGluingBlockedUntilC3Coherent
  basisGluingRequiresClasswiseObstructionCert :
    basisGluingRequiresClasswiseObstruction
  tripleCarrierAtlasClassificationCert :
    tripleCarrierAtlasClassification
  atlasTransportToT0OrOwnCertificateCert :
    atlasTransportToT0OrOwnCertificate
  classwiseCertificateBeforeBasisGluingCert :
    classwiseCertificateBeforeBasisGluing
  supportDefectRequiresC3 : supportRealizationDefect -> c3AtlasCoherence
  fullAuthorityRequiresC3 : fullMub6Authority -> c3AtlasCoherence
  classwiseObstructionRequiresBasisGluing :
    classwiseObstruction -> basisGluingRequired

theorem zeroRel_validity
    (contract : MubCochainObstructionContract) :
    contract.zeroRelValidity :=
  contract.zeroRelValidityCert

theorem d1_d0_zero_or_support_defect
    (contract : MubCochainObstructionContract) :
    contract.d1d0ZeroOrSupportDefect :=
  contract.d1d0ZeroOrSupportDefectCert

/-! ### Concrete finite cochain instance (real content, not a contract field)

The contract field `d1d0ZeroOrSupportDefect` above is an opaque recorded
obligation. Here is a concrete finite cochain complex with a genuinely PROVED
`d1 ∘ d0 = 0`, so the cochain law is discharged for at least one explicit instance
rather than only recorded. `C0` = integer vertex potentials, `C1` = oriented edge
differences on the triangle, `C2` = the single triangle-closure value. -/

/-- `d0`: vertex potentials `(p0, p1, p2)` ↦ oriented edge differences on the
triangle, for edges `0→1`, `1→2`, `0→2`. -/
def triangleD0 (p : Int × Int × Int) : Int × Int × Int :=
  (p.2.1 - p.1, p.2.2 - p.2.1, p.2.2 - p.1)

/-- `d1`: oriented-edge cochain `(e01, e12, e02)` ↦ the single triangle closure
`e01 + e12 - e02`. -/
def triangleD1 (e : Int × Int × Int) : Int :=
  e.1 + e.2.1 - e.2.2

/-- The cochain law `d1 ∘ d0 = 0`, PROVED (not asserted) for the concrete triangle
complex: the closure of any coboundary vanishes. -/
theorem triangle_d1_comp_d0_zero (p : Int × Int × Int) :
    triangleD1 (triangleD0 p) = 0 := by
  obtain ⟨a, b, c⟩ := p
  show (b - a) + (c - b) - (c - a) = 0
  omega

/-- A `MubCochainObstructionContract` whose `d1d0ZeroOrSupportDefect` obligation is
discharged by the concrete `triangle_d1_comp_d0_zero` above (remaining obligations
recorded as `True`). Witnesses that the contract is inhabitable (non-vacuous) and
that its cochain-law field can be met by real proved content. -/
def triangleWitnessContract : MubCochainObstructionContract where
  target := Target.mub6
  dimension := 6
  requiredBasisCount := 7
  fixedBasisCount := 3
  repairKinds := []
  primitiveDefectKinds := []
  closureFailureKinds := []
  zeroRelValidity := True
  d1d0ZeroOrSupportDefect := ∀ p : Int × Int × Int, triangleD1 (triangleD0 p) = 0
  quotientWellDefined := True
  phiGammaSeparated := True
  phi1Irreducible := True
  gamma2ClosureCharge := True
  atlasTransportPreservation := True
  basisGluingValidity := True
  pinnedTripleNoPromotion := True
  supportRealizationDefect := True
  c3AtlasCoherence := True
  d2c3AtlasCoherenceClassifiesMissingCover := True
  c3DefectsPreserveC2SourceKind := True
  classwiseObstruction := True
  basisGluingRequired := True
  basisGluingBlockedUntilC3Coherent := True
  basisGluingRequiresClasswiseObstruction := True
  tripleCarrierAtlasClassification := True
  atlasTransportToT0OrOwnCertificate := True
  classwiseCertificateBeforeBasisGluing := True
  fullMub6Authority := True
  zeroRelValidityCert := True.intro
  d1d0ZeroOrSupportDefectCert := triangle_d1_comp_d0_zero
  quotientWellDefinedCert := True.intro
  phiGammaSeparatedCert := True.intro
  phi1IrreducibleCert := True.intro
  gamma2ClosureChargeCert := True.intro
  atlasTransportPreservationCert := True.intro
  basisGluingValidityCert := True.intro
  pinnedTripleNoPromotionCert := True.intro
  d2c3AtlasCoherenceClassifiesMissingCoverCert := True.intro
  c3DefectsPreserveC2SourceKindCert := True.intro
  basisGluingBlockedUntilC3CoherentCert := True.intro
  basisGluingRequiresClasswiseObstructionCert := True.intro
  tripleCarrierAtlasClassificationCert := True.intro
  atlasTransportToT0OrOwnCertificateCert := True.intro
  classwiseCertificateBeforeBasisGluingCert := True.intro
  supportDefectRequiresC3 := fun _ => True.intro
  fullAuthorityRequiresC3 := fun _ => True.intro
  classwiseObstructionRequiresBasisGluing := fun _ => True.intro

/-- The witness contract really does discharge the cochain law (a sanity check
that `triangleWitnessContract` is well-formed and its `d1d0` obligation is the
proved one). -/
theorem triangleWitnessContract_discharges_cochain_law :
    triangleWitnessContract.d1d0ZeroOrSupportDefect :=
  triangleWitnessContract.d1d0ZeroOrSupportDefectCert

theorem quotient_well_defined
    (contract : MubCochainObstructionContract) :
    contract.quotientWellDefined :=
  contract.quotientWellDefinedCert

theorem phi_gamma_separation
    (contract : MubCochainObstructionContract) :
    contract.phiGammaSeparated :=
  contract.phiGammaSeparatedCert

theorem phi1_irreducible
    (contract : MubCochainObstructionContract) :
    contract.phi1Irreducible :=
  contract.phi1IrreducibleCert

theorem gamma2_closure_charge
    (contract : MubCochainObstructionContract) :
    contract.gamma2ClosureCharge :=
  contract.gamma2ClosureChargeCert

theorem atlas_transport_preservation
    (contract : MubCochainObstructionContract) :
    contract.atlasTransportPreservation :=
  contract.atlasTransportPreservationCert

theorem basis_gluing_validity
    (contract : MubCochainObstructionContract) :
    contract.basisGluingValidity :=
  contract.basisGluingValidityCert

theorem no_promotion_from_pinned_triple_to_full_mub6
    (contract : MubCochainObstructionContract) :
    contract.pinnedTripleNoPromotion :=
  contract.pinnedTripleNoPromotionCert

theorem mub6_support_realization_defect_requires_higher_coherence
    (contract : MubCochainObstructionContract) :
    contract.supportRealizationDefect -> contract.c3AtlasCoherence :=
  contract.supportDefectRequiresC3

theorem mub6_no_full_authority_without_c3_atlas_coherence
    (contract : MubCochainObstructionContract)
    (hNoC3 : Not contract.c3AtlasCoherence) :
    Not contract.fullMub6Authority := by
  intro hAuthority
  exact hNoC3 (contract.fullAuthorityRequiresC3 hAuthority)

theorem mub6_classwise_obstruction_requires_basis_gluing
    (contract : MubCochainObstructionContract) :
    contract.classwiseObstruction -> contract.basisGluingRequired :=
  contract.classwiseObstructionRequiresBasisGluing
theorem mub6_d2_c3_atlas_coherence_classifies_missing_cover
    (contract : MubCochainObstructionContract) :
    contract.d2c3AtlasCoherenceClassifiesMissingCover :=
  contract.d2c3AtlasCoherenceClassifiesMissingCoverCert

theorem mub6_c3_defects_preserve_c2_source_kind
    (contract : MubCochainObstructionContract) :
    contract.c3DefectsPreserveC2SourceKind :=
  contract.c3DefectsPreserveC2SourceKindCert
theorem mub6_basis_gluing_blocked_until_c3_coherent
    (contract : MubCochainObstructionContract) :
    contract.basisGluingBlockedUntilC3Coherent :=
  contract.basisGluingBlockedUntilC3CoherentCert

theorem mub6_basis_gluing_requires_classwise_obstruction
    (contract : MubCochainObstructionContract) :
    contract.basisGluingRequiresClasswiseObstruction :=
  contract.basisGluingRequiresClasswiseObstructionCert

theorem mub6_triple_carrier_atlas_classification
    (contract : MubCochainObstructionContract) :
    contract.tripleCarrierAtlasClassification :=
  contract.tripleCarrierAtlasClassificationCert

theorem mub6_atlas_transport_to_t0_or_own_certificate
    (contract : MubCochainObstructionContract) :
    contract.atlasTransportToT0OrOwnCertificate :=
  contract.atlasTransportToT0OrOwnCertificateCert

theorem mub6_classwise_certificate_before_basis_gluing
    (contract : MubCochainObstructionContract) :
    contract.classwiseCertificateBeforeBasisGluing :=
  contract.classwiseCertificateBeforeBasisGluingCert

theorem no_full_mub6_authority_from_pinned_wall_without_cover
    (hNoCover : (C : TripleClassCover) -> Not C.exhaustive) :
    FullMub6NoGoAuthority -> False :=
  MUB.no_full_mub6_authority_without_exhaustive_cover hNoCover

structure D10GtfocCrossValidationContract where
  phi1Matches : Prop
  closedSurvivorMatches : Prop
  h1NineDofMatches : Prop
  z2RealStructureMatches : Prop
  canonicalQubitTransportMatches : Prop
  canonicalQuintTransportMatches : Prop
  namedAntiunitaryTransportMatches : Prop
  f64PhiWallDiagnostic : Prop
  f64DiagnosticIntervalAttempt : Prop
  f64DiagnosticIntervalContainsTargets : Prop
  exactPhiWallCertificate : Prop
  globalWallCertificate : Prop
  terminalF64CrossValidationVerdict : Prop
  crossValidationMatch : Prop
  fullMub10Authority : Prop
  canonicalTransportsYieldNamedTransport :
    canonicalQubitTransportMatches ->
    canonicalQuintTransportMatches ->
    namedAntiunitaryTransportMatches
  componentsYieldMatch :
    phi1Matches ->
    closedSurvivorMatches ->
    h1NineDofMatches ->
    z2RealStructureMatches ->
    namedAntiunitaryTransportMatches ->
    crossValidationMatch
  matchDoesNotPromoteToMub10Authority :
    crossValidationMatch -> Not fullMub10Authority
  f64DiagnosticDoesNotPromoteToExactPhiWallCertificate :
    f64PhiWallDiagnostic -> Not exactPhiWallCertificate
  f64DiagnosticDoesNotPromoteToGlobalWallCertificate :
    f64PhiWallDiagnostic -> Not globalWallCertificate
  diagnosticIntervalAttemptContainsTargets :
    f64DiagnosticIntervalAttempt -> f64DiagnosticIntervalContainsTargets
  diagnosticIntervalAttemptCarriesF64Diagnostic :
    f64DiagnosticIntervalAttempt -> f64PhiWallDiagnostic
  diagnosticIntervalAttemptDoesNotPromoteToExactPhiWallCertificate :
    f64DiagnosticIntervalAttempt -> Not exactPhiWallCertificate
  diagnosticIntervalAttemptDoesNotPromoteToGlobalWallCertificate :
    f64DiagnosticIntervalAttempt -> Not globalWallCertificate
  terminalVerdictImpliesCrossValidationMatch :
    terminalF64CrossValidationVerdict -> crossValidationMatch
  terminalVerdictCarriesF64Diagnostic :
    terminalF64CrossValidationVerdict -> f64PhiWallDiagnostic
  terminalVerdictCarriesDiagnosticIntervalAttempt :
    terminalF64CrossValidationVerdict -> f64DiagnosticIntervalAttempt
  terminalVerdictDoesNotPromoteToMub10Authority :
    terminalF64CrossValidationVerdict -> Not fullMub10Authority

theorem d10_gtfoc_canonical_transport_witnesses_match_named_antiunitary
    (contract : D10GtfocCrossValidationContract)
    (hQubit : contract.canonicalQubitTransportMatches)
    (hQuint : contract.canonicalQuintTransportMatches) :
    contract.namedAntiunitaryTransportMatches :=
  contract.canonicalTransportsYieldNamedTransport hQubit hQuint

theorem d10_gtfoc_components_yield_cross_validation_match
    (contract : D10GtfocCrossValidationContract)
    (hPhi : contract.phi1Matches)
    (hClass : contract.closedSurvivorMatches)
    (hH1 : contract.h1NineDofMatches)
    (hZ2 : contract.z2RealStructureMatches)
    (hQubit : contract.canonicalQubitTransportMatches)
    (hQuint : contract.canonicalQuintTransportMatches) :
    contract.crossValidationMatch :=
  contract.componentsYieldMatch hPhi hClass hH1 hZ2
    (contract.canonicalTransportsYieldNamedTransport hQubit hQuint)

theorem d10_gtfoc_match_does_not_promote_to_mub10_authority
    (contract : D10GtfocCrossValidationContract)
    (hMatch : contract.crossValidationMatch) :
    Not contract.fullMub10Authority :=
  contract.matchDoesNotPromoteToMub10Authority hMatch

theorem d10_gtfoc_f64_wall_diagnostic_does_not_promote_to_exact_or_global_wall_certificate
    (contract : D10GtfocCrossValidationContract)
    (hF64 : contract.f64PhiWallDiagnostic) :
    Not contract.exactPhiWallCertificate ∧ Not contract.globalWallCertificate :=
  ⟨contract.f64DiagnosticDoesNotPromoteToExactPhiWallCertificate hF64,
   contract.f64DiagnosticDoesNotPromoteToGlobalWallCertificate hF64⟩

theorem d10_gtfoc_diagnostic_interval_attempt_contains_targets_but_not_exact_or_global_certificate
    (contract : D10GtfocCrossValidationContract)
    (hAttempt : contract.f64DiagnosticIntervalAttempt) :
    contract.f64DiagnosticIntervalContainsTargets ∧
      Not contract.exactPhiWallCertificate ∧ Not contract.globalWallCertificate :=
  ⟨contract.diagnosticIntervalAttemptContainsTargets hAttempt,
   contract.diagnosticIntervalAttemptDoesNotPromoteToExactPhiWallCertificate hAttempt,
   contract.diagnosticIntervalAttemptDoesNotPromoteToGlobalWallCertificate hAttempt⟩

theorem d10_gtfoc_terminal_f64_verdict_is_cross_validation_not_mub10_authority
    (contract : D10GtfocCrossValidationContract)
    (hVerdict : contract.terminalF64CrossValidationVerdict) :
    contract.crossValidationMatch ∧ Not contract.fullMub10Authority :=
  ⟨contract.terminalVerdictImpliesCrossValidationMatch hVerdict,
   contract.terminalVerdictDoesNotPromoteToMub10Authority hVerdict⟩

theorem d10_gtfoc_terminal_f64_verdict_has_interval_attempt_but_no_exact_or_global_wall_certificate
    (contract : D10GtfocCrossValidationContract)
    (hVerdict : contract.terminalF64CrossValidationVerdict) :
    contract.f64DiagnosticIntervalAttempt ∧
      Not contract.exactPhiWallCertificate ∧ Not contract.globalWallCertificate :=
  let hAttempt := contract.terminalVerdictCarriesDiagnosticIntervalAttempt hVerdict
  ⟨hAttempt,
   contract.diagnosticIntervalAttemptDoesNotPromoteToExactPhiWallCertificate hAttempt,
   contract.diagnosticIntervalAttemptDoesNotPromoteToGlobalWallCertificate hAttempt⟩
end CochainObstruction
end MUB

#print axioms MUB.CochainObstruction.zeroRel_validity
#print axioms MUB.CochainObstruction.d1_d0_zero_or_support_defect
#print axioms MUB.CochainObstruction.quotient_well_defined
#print axioms MUB.CochainObstruction.phi_gamma_separation
#print axioms MUB.CochainObstruction.phi1_irreducible
#print axioms MUB.CochainObstruction.gamma2_closure_charge
#print axioms MUB.CochainObstruction.atlas_transport_preservation
#print axioms MUB.CochainObstruction.basis_gluing_validity
#print axioms MUB.CochainObstruction.no_promotion_from_pinned_triple_to_full_mub6
#print axioms MUB.CochainObstruction.mub6_support_realization_defect_requires_higher_coherence
#print axioms MUB.CochainObstruction.mub6_no_full_authority_without_c3_atlas_coherence
#print axioms MUB.CochainObstruction.mub6_classwise_obstruction_requires_basis_gluing
#print axioms MUB.CochainObstruction.mub6_d2_c3_atlas_coherence_classifies_missing_cover
#print axioms MUB.CochainObstruction.mub6_c3_defects_preserve_c2_source_kind
#print axioms MUB.CochainObstruction.mub6_basis_gluing_blocked_until_c3_coherent
#print axioms MUB.CochainObstruction.mub6_basis_gluing_requires_classwise_obstruction
#print axioms MUB.CochainObstruction.mub6_triple_carrier_atlas_classification
#print axioms MUB.CochainObstruction.mub6_atlas_transport_to_t0_or_own_certificate
#print axioms MUB.CochainObstruction.mub6_classwise_certificate_before_basis_gluing
#print axioms MUB.CochainObstruction.no_full_mub6_authority_from_pinned_wall_without_cover
#print axioms MUB.CochainObstruction.d10_gtfoc_canonical_transport_witnesses_match_named_antiunitary
#print axioms MUB.CochainObstruction.d10_gtfoc_components_yield_cross_validation_match
#print axioms MUB.CochainObstruction.d10_gtfoc_match_does_not_promote_to_mub10_authority
#print axioms MUB.CochainObstruction.d10_gtfoc_f64_wall_diagnostic_does_not_promote_to_exact_or_global_wall_certificate
#print axioms MUB.CochainObstruction.d10_gtfoc_diagnostic_interval_attempt_contains_targets_but_not_exact_or_global_certificate
#print axioms MUB.CochainObstruction.d10_gtfoc_terminal_f64_verdict_is_cross_validation_not_mub10_authority
#print axioms MUB.CochainObstruction.d10_gtfoc_terminal_f64_verdict_has_interval_attempt_but_no_exact_or_global_wall_certificate
#print axioms MUB.CochainObstruction.triangle_d1_comp_d0_zero
#print axioms MUB.CochainObstruction.triangleWitnessContract_discharges_cochain_law
