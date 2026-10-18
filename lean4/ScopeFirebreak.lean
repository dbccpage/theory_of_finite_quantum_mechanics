/-!
MUB scope firebreaks for the Omega-native run.

This file does not formalize Hilbert spaces or the analytic MUB problem. It
formalizes the authority gates around the current run:

* a pinned T0 wall certificate is not a full MUB(6) theorem without cover,
  transport, and basis-gluing data;
* representation, comparison, and continuum wrappers do not create authority;
* MUB(10) and all-N claims require exact carrier/certificate families.
-/

namespace MUB

inductive Target where
  | pinnedT0
  | fullMub6
  | mub10
  | generalN
  deriving DecidableEq

inductive RepresentationLayer where
  | coordinate
  | projectorPolytope
  | weylBoard
  | gtmurTransport
  | gtorCompletion
  | gttcContinuum
  deriving DecidableEq

structure PinnedWallCertificate where
  lowerReplayed : Prop
  upperReplayed : Prop
  lowerReplayCert : lowerReplayed
  upperReplayCert : upperReplayed

structure TripleClassCover where
  exhaustive : Prop
  transportsAllClasses : Prop
  wallTransfersToEveryClass : Prop
  exhaustiveCert : exhaustive
  transportsAllClassesCert : transportsAllClasses
  wallTransfersToEveryClassCert : wallTransfersToEveryClass

structure BasisGluing where
  fourthVectorObstructionImpliesNoCompleteSet : Prop
  fourthVectorObstructionImpliesNoCompleteSetCert :
    fourthVectorObstructionImpliesNoCompleteSet

structure BasisGluingGate where
  pinnedUpperReplay : Prop
  exhaustiveCover : Prop
  wallTransportEveryClass : Prop
  overlapCompatibility : Prop
  zeroRelPreserved : Prop
  terminalizerPreserved : Prop
  classwiseFourthVectorObstruction : Prop
  gluingTheorem : Prop
  completeMub6NoGo : Prop
  completeNoGoRequiresPinnedUpper :
    completeMub6NoGo -> pinnedUpperReplay
  completeNoGoRequiresCover :
    completeMub6NoGo -> exhaustiveCover
  completeNoGoRequiresTransport :
    completeMub6NoGo -> wallTransportEveryClass
  completeNoGoRequiresOverlap :
    completeMub6NoGo -> overlapCompatibility
  completeNoGoRequiresZeroRel :
    completeMub6NoGo -> zeroRelPreserved
  completeNoGoRequiresTerminalizer :
    completeMub6NoGo -> terminalizerPreserved
  completeNoGoRequiresClasswiseObstruction :
    completeMub6NoGo -> classwiseFourthVectorObstruction
  completeNoGoRequiresGluing :
    completeMub6NoGo -> gluingTheorem

structure LocalHTransport where
  transportClosedInsidePinnedHLane : Prop
  transportClosedInsidePinnedHLaneCert :
    transportClosedInsidePinnedHLane

structure FullMub6NoGoAuthority where
  pinned : PinnedWallCertificate
  cover : TripleClassCover
  gluing : BasisGluing

structure WallCertifiedAtlas where
  cover : TripleClassCover
  gluing : BasisGluing
  zeroRelPreservedAcrossAtlas : Prop
  terminalizerPreservedAcrossAtlas : Prop
  zeroRelPreservedAcrossAtlasCert : zeroRelPreservedAcrossAtlas
  terminalizerPreservedAcrossAtlasCert : terminalizerPreservedAcrossAtlas

theorem full_mub6_authority_from_wall_certified_atlas
    (pinned : PinnedWallCertificate)
    (atlas : WallCertifiedAtlas) :
    Nonempty FullMub6NoGoAuthority := by
  exact ⟨{
    pinned := pinned
    cover := atlas.cover
    gluing := atlas.gluing
  }⟩

theorem wall_certified_atlas_requires_zeroRel_preservation
    (atlas : WallCertifiedAtlas) :
    atlas.zeroRelPreservedAcrossAtlas :=
  atlas.zeroRelPreservedAcrossAtlasCert

theorem wall_certified_atlas_requires_terminalizer_preservation
    (atlas : WallCertifiedAtlas) :
    atlas.terminalizerPreservedAcrossAtlas :=
  atlas.terminalizerPreservedAcrossAtlasCert

theorem full_mub6_authority_requires_upper_replay
    (A : FullMub6NoGoAuthority) : A.pinned.upperReplayed :=
  A.pinned.upperReplayCert

theorem full_mub6_authority_requires_exhaustive_cover
    (A : FullMub6NoGoAuthority) : A.cover.exhaustive :=
  A.cover.exhaustiveCert

theorem full_mub6_authority_requires_transport
    (A : FullMub6NoGoAuthority) : A.cover.transportsAllClasses :=
  A.cover.transportsAllClassesCert

theorem full_mub6_authority_requires_basis_gluing
    (A : FullMub6NoGoAuthority) :
    A.gluing.fourthVectorObstructionImpliesNoCompleteSet :=
  A.gluing.fourthVectorObstructionImpliesNoCompleteSetCert

theorem no_full_mub6_authority_without_exhaustive_cover
    (h : (C : TripleClassCover) -> Not C.exhaustive) :
    FullMub6NoGoAuthority -> False := by
  intro A
  exact h A.cover A.cover.exhaustiveCert

theorem no_full_mub6_authority_without_transport
    (h : (C : TripleClassCover) -> Not C.transportsAllClasses) :
    FullMub6NoGoAuthority -> False := by
  intro A
  exact h A.cover A.cover.transportsAllClassesCert

theorem no_full_mub6_authority_without_basis_gluing
    (h : (G : BasisGluing) ->
      Not G.fourthVectorObstructionImpliesNoCompleteSet) :
    FullMub6NoGoAuthority -> False := by
  intro A
  exact h A.gluing A.gluing.fourthVectorObstructionImpliesNoCompleteSetCert

theorem basis_gluing_gate_no_go_requires_cover_transport_and_gluing
    (gate : BasisGluingGate) :
    gate.completeMub6NoGo ->
      gate.exhaustiveCover ∧
      gate.wallTransportEveryClass ∧
      gate.classwiseFourthVectorObstruction ∧
      gate.gluingTheorem := by
  intro h
  exact ⟨gate.completeNoGoRequiresCover h,
    gate.completeNoGoRequiresTransport h,
    gate.completeNoGoRequiresClasswiseObstruction h,
    gate.completeNoGoRequiresGluing h⟩

theorem basis_gluing_gate_no_go_requires_zeroRel_and_terminalizer
    (gate : BasisGluingGate) :
    gate.completeMub6NoGo ->
      gate.zeroRelPreserved ∧ gate.terminalizerPreserved := by
  intro h
  exact ⟨gate.completeNoGoRequiresZeroRel h,
    gate.completeNoGoRequiresTerminalizer h⟩

theorem basis_gluing_gate_without_cover_no_complete_mub6_nogo
    (gate : BasisGluingGate)
    (hNoCover : Not gate.exhaustiveCover) :
    Not gate.completeMub6NoGo := by
  intro h
  exact hNoCover (gate.completeNoGoRequiresCover h)

theorem basis_gluing_gate_without_gluing_theorem_no_complete_mub6_nogo
    (gate : BasisGluingGate)
    (hNoGluing : Not gate.gluingTheorem) :
    Not gate.completeMub6NoGo := by
  intro h
  exact hNoGluing (gate.completeNoGoRequiresGluing h)

theorem local_h_transport_without_cover_no_full_mub6_authority
    (_local : LocalHTransport)
    (hNoCover : (C : TripleClassCover) -> Not C.exhaustive) :
    FullMub6NoGoAuthority -> False := by
  intro A
  exact hNoCover A.cover A.cover.exhaustiveCert

structure ExactCarrier where
  coefficientFieldDeclared : Prop
  zeroRelDeclared : Prop
  observerDeclared : Prop
  terminalizerDeclared : Prop
  coefficientFieldCert : coefficientFieldDeclared
  zeroRelCert : zeroRelDeclared
  observerCert : observerDeclared
  terminalizerCert : terminalizerDeclared

structure WitnessOrNoGoCertificate where
  replayable : Prop
  replayCert : replayable

structure Mub10Authority where
  carrier : ExactCarrier
  certificate : WitnessOrNoGoCertificate

structure PartialMubControl where
  dimension : Nat
  basisCount : Nat
  partialSetVerified : Prop
  partialSetVerifiedCert : partialSetVerified

structure CompositeCompletionGate where
  dimension : Nat
  lowerBasisCount : Nat
  requiredCompleteBasisCount : Nat
  exactLowerControl : Prop
  completeWitness : Prop
  noGoCertificate : Prop
  basisCountGap : Prop
  completeAuthority : Prop
  exactLowerControlCert : exactLowerControl
  basisCountGapCert : basisCountGap
  completeAuthorityRequiresCertificate :
    completeAuthority -> completeWitness ∨ noGoCertificate

structure CompositeTensorFamilyGate where
  dimension : Nat
  pairedTensorBasisCount : Nat
  requiredCompleteBasisCount : Nat
  factorProductDeclared : Prop
  exactFactorControls : Prop
  pairedTensorBases : Prop
  pairedOrthonormality : Prop
  pairedUnbiasedness : Prop
  minFactorBasisCount : Prop
  basisCountGap : Prop
  completeWitness : Prop
  noGoCertificate : Prop
  completeAuthority : Prop
  factorProductDeclaredCert : factorProductDeclared
  exactFactorControlsCert : exactFactorControls
  pairedTensorBasesCert : pairedTensorBases
  pairedOrthonormalityCert : pairedOrthonormality
  pairedUnbiasednessCert : pairedUnbiasedness
  minFactorBasisCountCert : minFactorBasisCount
  basisCountGapCert : basisCountGap
  completeAuthorityRequiresCertificate :
    completeAuthority -> completeWitness ∨ noGoCertificate

theorem mub10_authority_requires_exact_carrier
    (A : Mub10Authority) :
    A.carrier.coefficientFieldDeclared ∧
      A.carrier.zeroRelDeclared ∧
      A.carrier.observerDeclared ∧
      A.carrier.terminalizerDeclared := by
  exact ⟨A.carrier.coefficientFieldCert,
    A.carrier.zeroRelCert,
    A.carrier.observerCert,
    A.carrier.terminalizerCert⟩

theorem mub10_authority_requires_replayable_certificate
    (A : Mub10Authority) : A.certificate.replayable :=
  A.certificate.replayCert

theorem no_mub10_authority_without_replayable_certificate
    (h : (C : WitnessOrNoGoCertificate) -> Not C.replayable) :
    Mub10Authority -> False := by
  intro A
  exact h A.certificate A.certificate.replayCert

theorem partial_control_with_count_gap_is_not_complete
    (control : PartialMubControl)
    (hGap : control.basisCount ≠ control.dimension + 1) :
    control.basisCount ≠ control.dimension + 1 :=
  hGap

theorem composite_completion_gate_records_basis_gap
    (gate : CompositeCompletionGate) :
    gate.exactLowerControl ∧ gate.basisCountGap := by
  exact ⟨gate.exactLowerControlCert, gate.basisCountGapCert⟩

theorem composite_completion_gate_authority_requires_witness_or_nogo
    (gate : CompositeCompletionGate) :
    gate.completeAuthority -> gate.completeWitness ∨ gate.noGoCertificate :=
  gate.completeAuthorityRequiresCertificate

theorem composite_lower_control_without_certificate_no_complete_authority
    (gate : CompositeCompletionGate)
    (hWitness : Not gate.completeWitness)
    (hNoGo : Not gate.noGoCertificate) :
    Not gate.completeAuthority := by
  intro hAuthority
  cases gate.completeAuthorityRequiresCertificate hAuthority with
  | inl hWitnessPresent => exact hWitness hWitnessPresent
  | inr hNoGoPresent => exact hNoGo hNoGoPresent

theorem composite_tensor_family_gate_records_pairing_and_gap
    (gate : CompositeTensorFamilyGate) :
    gate.factorProductDeclared ∧
      gate.exactFactorControls ∧
      gate.pairedTensorBases ∧
      gate.pairedOrthonormality ∧
      gate.pairedUnbiasedness ∧
      gate.minFactorBasisCount ∧
      gate.basisCountGap := by
  exact ⟨gate.factorProductDeclaredCert,
    gate.exactFactorControlsCert,
    gate.pairedTensorBasesCert,
    gate.pairedOrthonormalityCert,
    gate.pairedUnbiasednessCert,
    gate.minFactorBasisCountCert,
    gate.basisCountGapCert⟩

theorem composite_tensor_family_gate_authority_requires_witness_or_nogo
    (gate : CompositeTensorFamilyGate) :
    gate.completeAuthority -> gate.completeWitness ∨ gate.noGoCertificate :=
  gate.completeAuthorityRequiresCertificate

theorem composite_tensor_family_lower_control_without_certificate_no_complete_authority
    (gate : CompositeTensorFamilyGate)
    (hWitness : Not gate.completeWitness)
    (hNoGo : Not gate.noGoCertificate) :
    Not gate.completeAuthority := by
  intro hAuthority
  cases gate.completeAuthorityRequiresCertificate hAuthority with
  | inl hWitnessPresent => exact hWitness hWitnessPresent
  | inr hNoGoPresent => exact hNoGo hNoGoPresent

theorem d10_lower_control_without_complete_certificate_no_mub10_authority
    (_control : PartialMubControl)
    (h : (C : WitnessOrNoGoCertificate) -> Not C.replayable) :
    Mub10Authority -> False := by
  intro A
  exact h A.certificate A.certificate.replayCert

theorem d6_lower_control_without_cover_no_full_mub6_authority
    (_control : PartialMubControl)
    (hNoCover : (C : TripleClassCover) -> Not C.exhaustive) :
    FullMub6NoGoAuthority -> False := by
  intro A
  exact hNoCover A.cover A.cover.exhaustiveCert

structure DimensionParametricFamily where
  carrierFamily : Prop
  zeroRelFamily : Prop
  certificateFamily : Prop
  transportsFiniteBenchmarksToAllNQuery : Prop
  carrierFamilyCert : carrierFamily
  zeroRelFamilyCert : zeroRelFamily
  certificateFamilyCert : certificateFamily
  transportsFiniteBenchmarksToAllNQueryCert :
    transportsFiniteBenchmarksToAllNQuery

structure GeneralMubNAuthority where
  family : DimensionParametricFamily

structure DimensionStratification where
  finiteCasesClassified : Prop
  tensorLowerBoundsSeparatedFromCompleteAuthority : Prop
  finiteCasesClassifiedCert : finiteCasesClassified
  tensorLowerBoundsSeparatedFromCompleteAuthorityCert :
    tensorLowerBoundsSeparatedFromCompleteAuthority

structure CompleteMubControl where
  dimension : Nat
  basisCount : Nat
  completeSetVerified : Prop
  completeSetVerifiedCert : completeSetVerified

structure DimensionMubAuthority where
  dimension : Nat
  completeSetVerified : Prop
  completeSetVerifiedCert : completeSetVerified

structure OddPrimeWeylFamilySchema where
  primeDimension : Nat
  basisCount : Nat
  finiteFieldCarrier : Prop
  additiveCharacterOrthogonality : Prop
  quadraticGaussNorm : Prop
  coefficientFieldDeclared : Prop
  hilbertBasisTransport : Prop
  completeSetVerified : Prop
  finiteFieldCarrierCert : finiteFieldCarrier
  additiveCharacterOrthogonalityCert : additiveCharacterOrthogonality
  quadraticGaussNormCert : quadraticGaussNorm
  coefficientFieldDeclaredCert : coefficientFieldDeclared
  hilbertBasisTransportCert : hilbertBasisTransport
  completeSetVerifiedCert : completeSetVerified

structure OddPrimeExactControl where
  primeDimension : Nat
  basisCount : Nat
  quadraticWeylBases : Prop
  coefficientFieldDeclared : Prop
  hilbertBasisTransport : Prop
  exactOrthonormality : Prop
  exactCrossUnbiasedness : Prop
  completeSetVerified : Prop
  quadraticWeylBasesCert : quadraticWeylBases
  coefficientFieldDeclaredCert : coefficientFieldDeclared
  hilbertBasisTransportCert : hilbertBasisTransport
  exactOrthonormalityCert : exactOrthonormality
  exactCrossUnbiasednessCert : exactCrossUnbiasedness
  completeSetVerifiedCert : completeSetVerified

structure OddPrimeGaussCertificateControl where
  primeDimension : Nat
  basisCount : Nat
  quadraticWeylBasesDeclared : Prop
  coefficientFieldDeclared : Prop
  sqrtNormalizerDeclared : Prop
  linearCharacterSumsVanish : Prop
  quadraticGaussNormsHold : Prop
  hilbertBasisTransport : Prop
  completeSetVerified : Prop
  quadraticWeylBasesDeclaredCert : quadraticWeylBasesDeclared
  coefficientFieldDeclaredCert : coefficientFieldDeclared
  sqrtNormalizerDeclaredCert : sqrtNormalizerDeclared
  linearCharacterSumsVanishCert : linearCharacterSumsVanish
  quadraticGaussNormsHoldCert : quadraticGaussNormsHold
  hilbertBasisTransportCert : hilbertBasisTransport
  completeSetVerifiedCert : completeSetVerified

structure OddPrimePowerWeylFamilySchema where
  prime : Nat
  exponent : Nat
  dimension : Nat
  basisCount : Nat
  finiteFieldCarrier : Prop
  traceOrthogonality : Prop
  quadraticGaussNorm : Prop
  coefficientFieldDeclared : Prop
  hilbertBasisTransport : Prop
  completeSetVerified : Prop
  finiteFieldCarrierCert : finiteFieldCarrier
  traceOrthogonalityCert : traceOrthogonality
  quadraticGaussNormCert : quadraticGaussNorm
  coefficientFieldDeclaredCert : coefficientFieldDeclared
  hilbertBasisTransportCert : hilbertBasisTransport
  completeSetVerifiedCert : completeSetVerified

structure OddPrimePowerExactControl where
  prime : Nat
  exponent : Nat
  dimension : Nat
  basisCount : Nat
  finiteFieldCarrier : Prop
  traceCharacterBases : Prop
  coefficientFieldDeclared : Prop
  hilbertBasisTransport : Prop
  exactOrthonormality : Prop
  exactCrossUnbiasedness : Prop
  completeSetVerified : Prop
  finiteFieldCarrierCert : finiteFieldCarrier
  traceCharacterBasesCert : traceCharacterBases
  coefficientFieldDeclaredCert : coefficientFieldDeclared
  hilbertBasisTransportCert : hilbertBasisTransport
  exactOrthonormalityCert : exactOrthonormality
  exactCrossUnbiasednessCert : exactCrossUnbiasedness
  completeSetVerifiedCert : completeSetVerified

structure OddPrimePowerExactControlPair where
  first : OddPrimePowerExactControl
  second : OddPrimePowerExactControl
  distinctDeclaredDimensions : Prop
  distinctDeclaredDimensionsCert : distinctDeclaredDimensions

structure OddPrimePowerExactControlTriple where
  first : OddPrimePowerExactControl
  second : OddPrimePowerExactControl
  third : OddPrimePowerExactControl
  pairwiseDistinctDeclaredDimensions : Prop
  pairwiseDistinctDeclaredDimensionsCert : pairwiseDistinctDeclaredDimensions

structure OddPrimePowerExactControlFiniteBatch where
  controlCount : Nat
  finiteDeclaredControlBatch : Prop
  everyDeclaredControlExact : Prop
  declaredDimensionsOnly : Prop
  finiteDeclaredControlBatchCert : finiteDeclaredControlBatch
  everyDeclaredControlExactCert : everyDeclaredControlExact
  declaredDimensionsOnlyCert : declaredDimensionsOnly

structure OddPrimePowerFiniteFieldTheoremGate where
  finiteSchemasRecorded : Prop
  finiteFieldFamily : Prop
  additiveCharacterOrthogonalityFamily : Prop
  quadraticGaussNormFamily : Prop
  acceptedFieldTheorem : Prop
  acceptedRequiresFiniteSchemas :
    acceptedFieldTheorem -> finiteSchemasRecorded
  acceptedRequiresFiniteFieldFamily :
    acceptedFieldTheorem -> finiteFieldFamily
  acceptedRequiresCharacterOrthogonality :
    acceptedFieldTheorem -> additiveCharacterOrthogonalityFamily
  acceptedRequiresQuadraticGauss :
    acceptedFieldTheorem -> quadraticGaussNormFamily

structure OddPrimePowerParametricFamilyGate where
  finiteSchemasRecorded : Prop
  finiteExactControlsRecorded : Prop
  finiteFieldTheoremAccepted : Prop
  finiteFieldFamily : Prop
  additiveCharacterOrthogonalityFamily : Prop
  quadraticGaussNormFamily : Prop
  coefficientFieldFamily : Prop
  hilbertBasisTransportFamily : Prop
  gtmurLossLedgerFamily : Prop
  terminalizerPreservedFamily : Prop
  acceptedFamily : Prop
  acceptedRequiresFiniteSchemas :
    acceptedFamily -> finiteSchemasRecorded
  acceptedRequiresFiniteExactControls :
    acceptedFamily -> finiteExactControlsRecorded
  acceptedRequiresFiniteFieldTheorem :
    acceptedFamily -> finiteFieldTheoremAccepted
  acceptedRequiresFiniteFieldFamily :
    acceptedFamily -> finiteFieldFamily
  acceptedRequiresCharacterOrthogonality :
    acceptedFamily -> additiveCharacterOrthogonalityFamily
  acceptedRequiresQuadraticGauss :
    acceptedFamily -> quadraticGaussNormFamily
  acceptedRequiresCoefficientField :
    acceptedFamily -> coefficientFieldFamily
  acceptedRequiresHilbertTransport :
    acceptedFamily -> hilbertBasisTransportFamily
  acceptedRequiresGtmurLedger :
    acceptedFamily -> gtmurLossLedgerFamily
  acceptedRequiresTerminalizer :
    acceptedFamily -> terminalizerPreservedFamily

structure CharTwoWeylBoardSchema where
  exponent : Nat
  dimension : Nat
  lineCount : Nat
  finiteFieldCarrier : Prop
  symplecticSpread : Prop
  isotropicLines : Prop
  pairwiseZeroIntersections : Prop
  nonzeroVectorCover : Prop
  spectralProjectorLift : Prop
  completeSetVerified : Prop
  finiteFieldCarrierCert : finiteFieldCarrier
  symplecticSpreadCert : symplecticSpread
  isotropicLinesCert : isotropicLines
  pairwiseZeroIntersectionsCert : pairwiseZeroIntersections
  nonzeroVectorCoverCert : nonzeroVectorCover
  spectralProjectorLiftCert : spectralProjectorLift
  completeSetVerifiedCert : completeSetVerified

structure SpectralProjectorLiftSchema where
  dimension : Nat
  basisCount : Nat
  projectorCount : Nat
  boardSpreadVerified : Prop
  finiteCharacterOrthogonality : Prop
  weylTraceOrthogonality : Prop
  selfAdjointPhaseConvention : Prop
  projectorPositivity : Prop
  rankOneResolution : Prop
  crossBasisUnbiasedness : Prop
  completeSetVerified : Prop
  boardSpreadVerifiedCert : boardSpreadVerified
  finiteCharacterOrthogonalityCert : finiteCharacterOrthogonality
  weylTraceOrthogonalityCert : weylTraceOrthogonality
  selfAdjointPhaseConventionCert : selfAdjointPhaseConvention
  projectorPositivityCert : projectorPositivity
  rankOneResolutionCert : rankOneResolution
  crossBasisUnbiasednessCert : crossBasisUnbiasedness
  completeSetVerifiedCert : completeSetVerified

structure CharTwoProjectorAlgebraSchema where
  dimension : Nat
  basisCount : Nat
  projectorCount : Nat
  boardSpreadVerified : Prop
  hermitianInvolutions : Prop
  commutingGenerators : Prop
  lineGroupLaw : Prop
  characterProjectorIdempotence : Prop
  basisResolution : Prop
  rankOneTrace : Prop
  crossBasisUnbiasedTrace : Prop
  positivityLift : Prop
  completeSetVerified : Prop
  boardSpreadVerifiedCert : boardSpreadVerified
  hermitianInvolutionsCert : hermitianInvolutions
  commutingGeneratorsCert : commutingGenerators
  lineGroupLawCert : lineGroupLaw
  characterProjectorIdempotenceCert : characterProjectorIdempotence
  basisResolutionCert : basisResolution
  rankOneTraceCert : rankOneTrace
  crossBasisUnbiasedTraceCert : crossBasisUnbiasedTrace
  positivityLiftCert : positivityLift
  completeSetVerifiedCert : completeSetVerified

structure FiniteHilbertTransportSchema where
  dimension : Nat
  basisCount : Nat
  projectorCount : Nat
  matrixRealization : Prop
  pauliTraceFormula : Prop
  positiveFactorization : Prop
  projectorIdempotence : Prop
  rankOneTrace : Prop
  basisResolution : Prop
  sameBasisOrthogonality : Prop
  crossBasisTraceTransport : Prop
  gtmurLossLedger : Prop
  completeSetVerified : Prop
  matrixRealizationCert : matrixRealization
  pauliTraceFormulaCert : pauliTraceFormula
  positiveFactorizationCert : positiveFactorization
  projectorIdempotenceCert : projectorIdempotence
  rankOneTraceCert : rankOneTrace
  basisResolutionCert : basisResolution
  sameBasisOrthogonalityCert : sameBasisOrthogonality
  crossBasisTraceTransportCert : crossBasisTraceTransport
  gtmurLossLedgerCert : gtmurLossLedger
  completeSetVerifiedCert : completeSetVerified

structure FiniteGtmurProjectorLedger where
  dimension : Nat
  basisCount : Nat
  projectorCount : Nat
  boardToSpectralZeroRelPreserved : Prop
  spectralToAlgebraZeroRelPreserved : Prop
  algebraToHilbertZeroRelPreserved : Prop
  terminalizerPreserved : Prop
  finiteOnlyBoundary : Prop
  boardToSpectralZeroRelPreservedCert : boardToSpectralZeroRelPreserved
  spectralToAlgebraZeroRelPreservedCert : spectralToAlgebraZeroRelPreserved
  algebraToHilbertZeroRelPreservedCert : algebraToHilbertZeroRelPreserved
  terminalizerPreservedCert : terminalizerPreserved
  finiteOnlyBoundaryCert : finiteOnlyBoundary

structure FiniteProjectorCompleteControl where
  dimension : Nat
  basisCount : Nat
  projectorCount : Nat
  hilbertMatrixTransport : Prop
  positiveRankOneProjectors : Prop
  basisResolution : Prop
  sameBasisOrthogonality : Prop
  crossBasisUnbiasedness : Prop
  gtmurLedgerClosed : Prop
  finiteOnlyBoundary : Prop
  completeSetVerified : Prop
  hilbertMatrixTransportCert : hilbertMatrixTransport
  positiveRankOneProjectorsCert : positiveRankOneProjectors
  basisResolutionCert : basisResolution
  sameBasisOrthogonalityCert : sameBasisOrthogonality
  crossBasisUnbiasednessCert : crossBasisUnbiasedness
  gtmurLedgerClosedCert : gtmurLedgerClosed
  finiteOnlyBoundaryCert : finiteOnlyBoundary
  completeSetVerifiedCert : completeSetVerified

structure CharTwoParametricProjectorFamilyGate where
  finiteSamplesClosed : Prop
  binaryFieldFamily : Prop
  irreducibleModulusFamily : Prop
  symplecticSpreadFamily : Prop
  boardIncidenceFamily : Prop
  spectralProjectorLiftFamily : Prop
  pauliPhaseFamily : Prop
  positiveProjectorFamily : Prop
  hilbertTransportFamily : Prop
  gtmurLossLedgerFamily : Prop
  terminalizerPreservedFamily : Prop
  acceptedFamily : Prop
  acceptedRequiresFiniteSamples :
    acceptedFamily -> finiteSamplesClosed
  acceptedRequiresBinaryField :
    acceptedFamily -> binaryFieldFamily
  acceptedRequiresIrreducibleModulus :
    acceptedFamily -> irreducibleModulusFamily
  acceptedRequiresSpread :
    acceptedFamily -> symplecticSpreadFamily
  acceptedRequiresBoardIncidence :
    acceptedFamily -> boardIncidenceFamily
  acceptedRequiresSpectralLift :
    acceptedFamily -> spectralProjectorLiftFamily
  acceptedRequiresPauliPhase :
    acceptedFamily -> pauliPhaseFamily
  acceptedRequiresPositiveProjectors :
    acceptedFamily -> positiveProjectorFamily
  acceptedRequiresHilbertTransport :
    acceptedFamily -> hilbertTransportFamily
  acceptedRequiresGtmurLedger :
    acceptedFamily -> gtmurLossLedgerFamily
  acceptedRequiresTerminalizer :
    acceptedFamily -> terminalizerPreservedFamily

structure PrimePowerGtmurBoundaryLedger where
  oddPrimeRegimeRecorded : Prop
  oddPrimePowerRegimeRecorded : Prop
  charTwoRegimeRecorded : Prop
  compositeTensorLowerControlOnly : Prop
  primePowerOnlyBoundary : Prop
  oddPrimeRegimeRecordedCert : oddPrimeRegimeRecorded
  oddPrimePowerRegimeRecordedCert : oddPrimePowerRegimeRecorded
  charTwoRegimeRecordedCert : charTwoRegimeRecorded
  compositeTensorLowerControlOnlyCert : compositeTensorLowerControlOnly
  primePowerOnlyBoundaryCert : primePowerOnlyBoundary

theorem complete_control_authorizes_declared_dimension
    (control : CompleteMubControl) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := control.dimension
    completeSetVerified := control.completeSetVerified
    completeSetVerifiedCert := control.completeSetVerifiedCert
  }⟩

theorem odd_prime_weyl_schema_authorizes_declared_prime_dimension
    (schema : OddPrimeWeylFamilySchema) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := schema.primeDimension
    completeSetVerified := schema.completeSetVerified
    completeSetVerifiedCert := schema.completeSetVerifiedCert
  }⟩

theorem odd_prime_exact_control_authorizes_declared_dimension
    (control : OddPrimeExactControl) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := control.primeDimension
    completeSetVerified := control.completeSetVerified
    completeSetVerifiedCert := control.completeSetVerifiedCert
  }⟩

theorem odd_prime_exact_control_requires_field_and_hilbert_transport
    (control : OddPrimeExactControl) :
    control.quadraticWeylBases ∧
      control.coefficientFieldDeclared ∧
      control.hilbertBasisTransport := by
  exact ⟨control.quadraticWeylBasesCert,
    control.coefficientFieldDeclaredCert,
    control.hilbertBasisTransportCert⟩

theorem odd_prime_exact_control_requires_exact_mub_checks
    (control : OddPrimeExactControl) :
    control.exactOrthonormality ∧ control.exactCrossUnbiasedness := by
  exact ⟨control.exactOrthonormalityCert,
    control.exactCrossUnbiasednessCert⟩

theorem odd_prime_gauss_certificate_authorizes_declared_dimension
    (control : OddPrimeGaussCertificateControl) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := control.primeDimension
    completeSetVerified := control.completeSetVerified
    completeSetVerifiedCert := control.completeSetVerifiedCert
  }⟩

theorem odd_prime_gauss_certificate_requires_character_and_gauss_checks
    (control : OddPrimeGaussCertificateControl) :
    control.linearCharacterSumsVanish ∧
      control.quadraticGaussNormsHold ∧
      control.sqrtNormalizerDeclared := by
  exact ⟨control.linearCharacterSumsVanishCert,
    control.quadraticGaussNormsHoldCert,
    control.sqrtNormalizerDeclaredCert⟩

theorem odd_prime_gauss_certificate_requires_field_and_transport
    (control : OddPrimeGaussCertificateControl) :
    control.quadraticWeylBasesDeclared ∧
      control.coefficientFieldDeclared ∧
      control.hilbertBasisTransport := by
  exact ⟨control.quadraticWeylBasesDeclaredCert,
    control.coefficientFieldDeclaredCert,
    control.hilbertBasisTransportCert⟩

theorem odd_prime_power_weyl_schema_authorizes_declared_prime_power_dimension
    (schema : OddPrimePowerWeylFamilySchema) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := schema.dimension
    completeSetVerified := schema.completeSetVerified
    completeSetVerifiedCert := schema.completeSetVerifiedCert
  }⟩

theorem odd_prime_power_exact_control_authorizes_declared_dimension
    (control : OddPrimePowerExactControl) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := control.dimension
    completeSetVerified := control.completeSetVerified
    completeSetVerifiedCert := control.completeSetVerifiedCert
  }⟩

theorem odd_prime_power_exact_control_requires_field_and_hilbert_transport
    (control : OddPrimePowerExactControl) :
    control.finiteFieldCarrier ∧
      control.traceCharacterBases ∧
      control.coefficientFieldDeclared ∧
      control.hilbertBasisTransport := by
  exact ⟨control.finiteFieldCarrierCert,
    control.traceCharacterBasesCert,
    control.coefficientFieldDeclaredCert,
    control.hilbertBasisTransportCert⟩

theorem odd_prime_power_exact_control_requires_exact_mub_checks
    (control : OddPrimePowerExactControl) :
    control.exactOrthonormality ∧ control.exactCrossUnbiasedness := by
  exact ⟨control.exactOrthonormalityCert,
    control.exactCrossUnbiasednessCert⟩

theorem odd_prime_power_exact_control_pair_authorizes_declared_dimensions
    (controls : OddPrimePowerExactControlPair) :
    Nonempty (DimensionMubAuthority × DimensionMubAuthority) := by
  exact ⟨({
    dimension := controls.first.dimension
    completeSetVerified := controls.first.completeSetVerified
    completeSetVerifiedCert := controls.first.completeSetVerifiedCert
  }, {
    dimension := controls.second.dimension
    completeSetVerified := controls.second.completeSetVerified
    completeSetVerifiedCert := controls.second.completeSetVerifiedCert
  })⟩

theorem odd_prime_power_exact_control_pair_requires_distinct_controls
    (controls : OddPrimePowerExactControlPair) :
    controls.distinctDeclaredDimensions :=
  controls.distinctDeclaredDimensionsCert

theorem odd_prime_power_exact_control_pair_requires_each_exact_mub_check
    (controls : OddPrimePowerExactControlPair) :
    controls.first.exactOrthonormality ∧
      controls.first.exactCrossUnbiasedness ∧
      controls.second.exactOrthonormality ∧
      controls.second.exactCrossUnbiasedness := by
  exact ⟨controls.first.exactOrthonormalityCert,
    controls.first.exactCrossUnbiasednessCert,
    controls.second.exactOrthonormalityCert,
    controls.second.exactCrossUnbiasednessCert⟩

theorem odd_prime_power_exact_control_triple_authorizes_declared_dimensions
    (controls : OddPrimePowerExactControlTriple) :
    Nonempty (DimensionMubAuthority × DimensionMubAuthority × DimensionMubAuthority) := by
  exact ⟨({
    dimension := controls.first.dimension
    completeSetVerified := controls.first.completeSetVerified
    completeSetVerifiedCert := controls.first.completeSetVerifiedCert
  }, {
    dimension := controls.second.dimension
    completeSetVerified := controls.second.completeSetVerified
    completeSetVerifiedCert := controls.second.completeSetVerifiedCert
  }, {
    dimension := controls.third.dimension
    completeSetVerified := controls.third.completeSetVerified
    completeSetVerifiedCert := controls.third.completeSetVerifiedCert
  })⟩

theorem odd_prime_power_exact_control_triple_requires_distinct_controls
    (controls : OddPrimePowerExactControlTriple) :
    controls.pairwiseDistinctDeclaredDimensions :=
  controls.pairwiseDistinctDeclaredDimensionsCert

theorem odd_prime_power_exact_control_triple_requires_each_exact_mub_check
    (controls : OddPrimePowerExactControlTriple) :
    controls.first.exactOrthonormality ∧
      controls.first.exactCrossUnbiasedness ∧
      controls.second.exactOrthonormality ∧
      controls.second.exactCrossUnbiasedness ∧
      controls.third.exactOrthonormality ∧
      controls.third.exactCrossUnbiasedness := by
  exact ⟨controls.first.exactOrthonormalityCert,
    controls.first.exactCrossUnbiasednessCert,
    controls.second.exactOrthonormalityCert,
    controls.second.exactCrossUnbiasednessCert,
    controls.third.exactOrthonormalityCert,
    controls.third.exactCrossUnbiasednessCert⟩

theorem odd_prime_power_exact_control_finite_batch_records_declared_only
    (batch : OddPrimePowerExactControlFiniteBatch) :
    batch.finiteDeclaredControlBatch ∧
      batch.everyDeclaredControlExact ∧
      batch.declaredDimensionsOnly := by
  exact ⟨batch.finiteDeclaredControlBatchCert,
    batch.everyDeclaredControlExactCert,
    batch.declaredDimensionsOnlyCert⟩

theorem odd_prime_power_finite_field_theorem_gate_acceptance_requires_field_and_characters
    (gate : OddPrimePowerFiniteFieldTheoremGate) :
    gate.acceptedFieldTheorem ->
      gate.finiteSchemasRecorded ∧
      gate.finiteFieldFamily ∧
      gate.additiveCharacterOrthogonalityFamily ∧
      gate.quadraticGaussNormFamily := by
  intro h
  exact ⟨gate.acceptedRequiresFiniteSchemas h,
    gate.acceptedRequiresFiniteFieldFamily h,
    gate.acceptedRequiresCharacterOrthogonality h,
    gate.acceptedRequiresQuadraticGauss h⟩

theorem odd_prime_power_finite_field_theorem_gate_without_character_orthogonality_no_field_theorem
    (gate : OddPrimePowerFiniteFieldTheoremGate)
    (hNoCharacters : Not gate.additiveCharacterOrthogonalityFamily) :
    Not gate.acceptedFieldTheorem := by
  intro h
  exact hNoCharacters (gate.acceptedRequiresCharacterOrthogonality h)

theorem odd_prime_power_finite_field_theorem_gate_without_gauss_no_field_theorem
    (gate : OddPrimePowerFiniteFieldTheoremGate)
    (hNoGauss : Not gate.quadraticGaussNormFamily) :
    Not gate.acceptedFieldTheorem := by
  intro h
  exact hNoGauss (gate.acceptedRequiresQuadraticGauss h)

theorem odd_prime_power_parametric_gate_acceptance_requires_finite_records
    (gate : OddPrimePowerParametricFamilyGate) :
    gate.acceptedFamily ->
      gate.finiteSchemasRecorded ∧ gate.finiteExactControlsRecorded := by
  intro h
  exact ⟨gate.acceptedRequiresFiniteSchemas h,
    gate.acceptedRequiresFiniteExactControls h⟩

theorem odd_prime_power_parametric_gate_acceptance_requires_field_and_characters
    (gate : OddPrimePowerParametricFamilyGate) :
    gate.acceptedFamily ->
      gate.finiteFieldTheoremAccepted ∧
      gate.finiteFieldFamily ∧
      gate.additiveCharacterOrthogonalityFamily ∧
      gate.quadraticGaussNormFamily ∧
      gate.coefficientFieldFamily := by
  intro h
  exact ⟨gate.acceptedRequiresFiniteFieldTheorem h,
    gate.acceptedRequiresFiniteFieldFamily h,
    gate.acceptedRequiresCharacterOrthogonality h,
    gate.acceptedRequiresQuadraticGauss h,
    gate.acceptedRequiresCoefficientField h⟩

theorem odd_prime_power_parametric_gate_acceptance_requires_hilbert_gtmur_terminalizer
    (gate : OddPrimePowerParametricFamilyGate) :
    gate.acceptedFamily ->
      gate.hilbertBasisTransportFamily ∧
      gate.gtmurLossLedgerFamily ∧
      gate.terminalizerPreservedFamily := by
  intro h
  exact ⟨gate.acceptedRequiresHilbertTransport h,
    gate.acceptedRequiresGtmurLedger h,
    gate.acceptedRequiresTerminalizer h⟩

theorem odd_prime_power_parametric_gate_without_hilbert_transport_no_family
    (gate : OddPrimePowerParametricFamilyGate)
    (hNoTransport : Not gate.hilbertBasisTransportFamily) :
    Not gate.acceptedFamily := by
  intro h
  exact hNoTransport (gate.acceptedRequiresHilbertTransport h)

theorem odd_prime_power_parametric_gate_without_field_theorem_no_family
    (gate : OddPrimePowerParametricFamilyGate)
    (hNoFieldTheorem : Not gate.finiteFieldTheoremAccepted) :
    Not gate.acceptedFamily := by
  intro h
  exact hNoFieldTheorem (gate.acceptedRequiresFiniteFieldTheorem h)

theorem odd_prime_power_parametric_gate_without_gtmur_no_family
    (gate : OddPrimePowerParametricFamilyGate)
    (hNoGtmur : Not gate.gtmurLossLedgerFamily) :
    Not gate.acceptedFamily := by
  intro h
  exact hNoGtmur (gate.acceptedRequiresGtmurLedger h)

theorem char_two_weyl_board_schema_authorizes_declared_dimension_after_lift
    (schema : CharTwoWeylBoardSchema) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := schema.dimension
    completeSetVerified := schema.completeSetVerified
    completeSetVerifiedCert := schema.completeSetVerifiedCert
  }⟩

theorem char_two_weyl_board_schema_requires_spectral_projector_lift
    (schema : CharTwoWeylBoardSchema) :
    schema.spectralProjectorLift :=
  schema.spectralProjectorLiftCert

theorem spectral_projector_lift_schema_authorizes_declared_dimension
    (schema : SpectralProjectorLiftSchema) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := schema.dimension
    completeSetVerified := schema.completeSetVerified
    completeSetVerifiedCert := schema.completeSetVerifiedCert
  }⟩

theorem spectral_projector_lift_schema_requires_positivity
    (schema : SpectralProjectorLiftSchema) :
    schema.projectorPositivity :=
  schema.projectorPositivityCert

theorem char_two_projector_algebra_schema_authorizes_declared_dimension
    (schema : CharTwoProjectorAlgebraSchema) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := schema.dimension
    completeSetVerified := schema.completeSetVerified
    completeSetVerifiedCert := schema.completeSetVerifiedCert
  }⟩

theorem char_two_projector_algebra_schema_requires_positivity_lift
    (schema : CharTwoProjectorAlgebraSchema) :
    schema.positivityLift :=
  schema.positivityLiftCert

theorem finite_hilbert_transport_schema_authorizes_declared_dimension
    (schema : FiniteHilbertTransportSchema) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := schema.dimension
    completeSetVerified := schema.completeSetVerified
    completeSetVerifiedCert := schema.completeSetVerifiedCert
  }⟩

theorem finite_hilbert_transport_schema_requires_gtmur_loss_ledger
    (schema : FiniteHilbertTransportSchema) :
    schema.gtmurLossLedger :=
  schema.gtmurLossLedgerCert

theorem finite_gtmur_projector_ledger_requires_zeroRel_preservation
    (ledger : FiniteGtmurProjectorLedger) :
    ledger.boardToSpectralZeroRelPreserved ∧
      ledger.spectralToAlgebraZeroRelPreserved ∧
      ledger.algebraToHilbertZeroRelPreserved := by
  exact ⟨ledger.boardToSpectralZeroRelPreservedCert,
    ledger.spectralToAlgebraZeroRelPreservedCert,
    ledger.algebraToHilbertZeroRelPreservedCert⟩

theorem finite_gtmur_projector_ledger_requires_terminalizer_preservation
    (ledger : FiniteGtmurProjectorLedger) :
    ledger.terminalizerPreserved :=
  ledger.terminalizerPreservedCert

theorem finite_projector_control_authorizes_declared_dimension
    (control : FiniteProjectorCompleteControl) :
    Nonempty DimensionMubAuthority := by
  exact ⟨{
    dimension := control.dimension
    completeSetVerified := control.completeSetVerified
    completeSetVerifiedCert := control.completeSetVerifiedCert
  }⟩

theorem finite_projector_control_requires_projector_zerorel
    (control : FiniteProjectorCompleteControl) :
    control.positiveRankOneProjectors ∧
      control.basisResolution ∧
      control.sameBasisOrthogonality ∧
      control.crossBasisUnbiasedness := by
  exact ⟨control.positiveRankOneProjectorsCert,
    control.basisResolutionCert,
    control.sameBasisOrthogonalityCert,
    control.crossBasisUnbiasednessCert⟩

theorem finite_projector_control_requires_gtmur_ledger
    (control : FiniteProjectorCompleteControl) :
    control.gtmurLedgerClosed :=
  control.gtmurLedgerClosedCert

theorem finite_projector_control_without_parametric_family_no_general_authority
    (_control : FiniteProjectorCompleteControl)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem char_two_parametric_gate_acceptance_requires_field_and_spread
    (gate : CharTwoParametricProjectorFamilyGate) :
    gate.acceptedFamily ->
      gate.binaryFieldFamily ∧
      gate.irreducibleModulusFamily ∧
      gate.symplecticSpreadFamily ∧
      gate.boardIncidenceFamily := by
  intro h
  exact ⟨gate.acceptedRequiresBinaryField h,
    gate.acceptedRequiresIrreducibleModulus h,
    gate.acceptedRequiresSpread h,
    gate.acceptedRequiresBoardIncidence h⟩

theorem char_two_parametric_gate_acceptance_requires_lift_hilbert_gtmur
    (gate : CharTwoParametricProjectorFamilyGate) :
    gate.acceptedFamily ->
      gate.spectralProjectorLiftFamily ∧
      gate.pauliPhaseFamily ∧
      gate.positiveProjectorFamily ∧
      gate.hilbertTransportFamily ∧
      gate.gtmurLossLedgerFamily ∧
      gate.terminalizerPreservedFamily := by
  intro h
  exact ⟨gate.acceptedRequiresSpectralLift h,
    gate.acceptedRequiresPauliPhase h,
    gate.acceptedRequiresPositiveProjectors h,
    gate.acceptedRequiresHilbertTransport h,
    gate.acceptedRequiresGtmurLedger h,
    gate.acceptedRequiresTerminalizer h⟩

theorem char_two_parametric_gate_without_positive_projectors_no_family
    (gate : CharTwoParametricProjectorFamilyGate)
    (hNoPositive : Not gate.positiveProjectorFamily) :
    Not gate.acceptedFamily := by
  intro h
  exact hNoPositive (gate.acceptedRequiresPositiveProjectors h)

theorem char_two_parametric_gate_without_gtmur_no_family
    (gate : CharTwoParametricProjectorFamilyGate)
    (hNoGtmur : Not gate.gtmurLossLedgerFamily) :
    Not gate.acceptedFamily := by
  intro h
  exact hNoGtmur (gate.acceptedRequiresGtmurLedger h)

theorem prime_power_gtmur_boundary_requires_all_characteristic_records
    (ledger : PrimePowerGtmurBoundaryLedger) :
    ledger.oddPrimeRegimeRecorded ∧
      ledger.oddPrimePowerRegimeRecorded ∧
      ledger.charTwoRegimeRecorded := by
  exact ⟨ledger.oddPrimeRegimeRecordedCert,
    ledger.oddPrimePowerRegimeRecordedCert,
    ledger.charTwoRegimeRecordedCert⟩

theorem prime_power_gtmur_boundary_requires_composite_nonpromotion
    (ledger : PrimePowerGtmurBoundaryLedger) :
    ledger.compositeTensorLowerControlOnly ∧ ledger.primePowerOnlyBoundary := by
  exact ⟨ledger.compositeTensorLowerControlOnlyCert,
    ledger.primePowerOnlyBoundaryCert⟩

theorem finite_controls_without_parametric_family_no_general_authority
    (_controls : List CompleteMubControl)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem composite_completion_gate_without_parametric_family_no_general_authority
    (_gate : CompositeCompletionGate)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem composite_tensor_family_gate_without_parametric_family_no_general_authority
    (_gate : CompositeTensorFamilyGate)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem finite_stratification_without_parametric_family_no_general_authority
    (_stratification : DimensionStratification)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem odd_prime_weyl_schema_without_parametric_family_no_general_authority
    (_schema : OddPrimeWeylFamilySchema)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem odd_prime_exact_control_without_parametric_family_no_general_authority
    (_control : OddPrimeExactControl)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem odd_prime_gauss_certificate_without_parametric_family_no_general_authority
    (_control : OddPrimeGaussCertificateControl)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem odd_prime_power_weyl_schema_without_parametric_family_no_general_authority
    (_schema : OddPrimePowerWeylFamilySchema)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem odd_prime_power_exact_control_without_parametric_family_no_general_authority
    (_control : OddPrimePowerExactControl)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem odd_prime_power_exact_control_pair_without_parametric_family_no_general_authority
    (_controls : OddPrimePowerExactControlPair)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem odd_prime_power_exact_control_triple_without_parametric_family_no_general_authority
    (_controls : OddPrimePowerExactControlTriple)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem odd_prime_power_exact_control_finite_batch_without_parametric_family_no_general_authority
    (_batch : OddPrimePowerExactControlFiniteBatch)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem odd_prime_power_parametric_gate_without_general_certificate_family_no_general_authority
    (_gate : OddPrimePowerParametricFamilyGate)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem char_two_weyl_board_schema_without_parametric_family_no_general_authority
    (_schema : CharTwoWeylBoardSchema)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem spectral_projector_lift_schema_without_parametric_family_no_general_authority
    (_schema : SpectralProjectorLiftSchema)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem char_two_projector_algebra_schema_without_parametric_family_no_general_authority
    (_schema : CharTwoProjectorAlgebraSchema)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem finite_hilbert_transport_schema_without_parametric_family_no_general_authority
    (_schema : FiniteHilbertTransportSchema)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem finite_gtmur_projector_ledger_without_parametric_family_no_general_authority
    (_ledger : FiniteGtmurProjectorLedger)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem prime_power_gtmur_boundary_without_parametric_family_no_general_authority
    (_ledger : PrimePowerGtmurBoundaryLedger)
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

theorem general_mub_n_authority_requires_parametric_family
    (A : GeneralMubNAuthority) :
    A.family.carrierFamily ∧
      A.family.zeroRelFamily ∧
      A.family.certificateFamily ∧
      A.family.transportsFiniteBenchmarksToAllNQuery := by
  exact ⟨A.family.carrierFamilyCert,
    A.family.zeroRelFamilyCert,
    A.family.certificateFamilyCert,
    A.family.transportsFiniteBenchmarksToAllNQueryCert⟩

theorem no_general_mub_n_authority_without_certificate_family
    (h : (F : DimensionParametricFamily) -> Not F.certificateFamily) :
    GeneralMubNAuthority -> False := by
  intro A
  exact h A.family A.family.certificateFamilyCert

structure RepresentationCertificate where
  layer : RepresentationLayer
  zeroRelPreserved : Prop
  terminalizerPreserved : Prop
  lossLedgerClosed : Prop
  zeroRelPreservedCert : zeroRelPreserved
  terminalizerPreservedCert : terminalizerPreserved
  lossLedgerClosedCert : lossLedgerClosed

structure RepresentationAuthority where
  certificate : RepresentationCertificate

theorem representation_authority_requires_loss_closed
    (A : RepresentationAuthority) : A.certificate.lossLedgerClosed :=
  A.certificate.lossLedgerClosedCert

theorem no_representation_authority_without_closed_loss_ledger
    (h : (C : RepresentationCertificate) -> Not C.lossLedgerClosed) :
    RepresentationAuthority -> False := by
  intro A
  exact h A.certificate A.certificate.lossLedgerClosedCert

structure TerminalizedDescent (X : Type) where
  terminalized : Prop

structure Auth (X : Type) where
  descent : TerminalizedDescent X

structure ComparisonEnvelope (X : Type) where
  val : X

structure ContinuumShadow (X : Type) where
  val : X

structure GtorGttcGate where
  terminalizedComponents : Prop
  edgeCertificates : Prop
  directedGluing : Prop
  queryRelativeAuthority : Prop
  uniformCertificateFamily : Prop
  acceptedAuthority : Prop
  acceptedRequiresTerminalized :
    acceptedAuthority -> terminalizedComponents
  acceptedRequiresEdges :
    acceptedAuthority -> edgeCertificates
  acceptedRequiresGluing :
    acceptedAuthority -> directedGluing
  acceptedRequiresQueryAuthority :
    acceptedAuthority -> queryRelativeAuthority
  acceptedRequiresUniformFamily :
    acceptedAuthority -> uniformCertificateFamily

theorem gtor_gttc_gate_authority_requires_descent_and_gluing
    (gate : GtorGttcGate) :
    gate.acceptedAuthority ->
      gate.terminalizedComponents ∧
      gate.edgeCertificates ∧
      gate.directedGluing ∧
      gate.queryRelativeAuthority := by
  intro h
  exact ⟨gate.acceptedRequiresTerminalized h,
    gate.acceptedRequiresEdges h,
    gate.acceptedRequiresGluing h,
    gate.acceptedRequiresQueryAuthority h⟩

theorem gttc_gate_authority_requires_uniform_certificate_family
    (gate : GtorGttcGate) :
    gate.acceptedAuthority -> gate.uniformCertificateFamily :=
  gate.acceptedRequiresUniformFamily

theorem gtor_gttc_gate_without_terminalized_descent_no_authority
    (gate : GtorGttcGate)
    (hNoDescent : Not gate.terminalizedComponents) :
    Not gate.acceptedAuthority := by
  intro hAuthority
  exact hNoDescent (gate.acceptedRequiresTerminalized hAuthority)

theorem gtor_completion_does_not_create_auth
    {X : Type}
    (noDescent : TerminalizedDescent X -> False)
    (_env : ComparisonEnvelope X) :
    Auth X -> False := by
  intro A
  exact noDescent A.descent

theorem gttc_continuum_shadow_does_not_create_auth
    {X : Type}
    (noDescent : TerminalizedDescent X -> False)
    (_shadow : ContinuumShadow X) :
    Auth X -> False := by
  intro A
  exact noDescent A.descent

end MUB

#print axioms MUB.no_full_mub6_authority_without_exhaustive_cover
#print axioms MUB.full_mub6_authority_from_wall_certified_atlas
#print axioms MUB.wall_certified_atlas_requires_zeroRel_preservation
#print axioms MUB.wall_certified_atlas_requires_terminalizer_preservation
#print axioms MUB.no_full_mub6_authority_without_transport
#print axioms MUB.no_full_mub6_authority_without_basis_gluing
#print axioms MUB.basis_gluing_gate_no_go_requires_cover_transport_and_gluing
#print axioms MUB.basis_gluing_gate_no_go_requires_zeroRel_and_terminalizer
#print axioms MUB.basis_gluing_gate_without_cover_no_complete_mub6_nogo
#print axioms MUB.basis_gluing_gate_without_gluing_theorem_no_complete_mub6_nogo
#print axioms MUB.local_h_transport_without_cover_no_full_mub6_authority
#print axioms MUB.no_mub10_authority_without_replayable_certificate
#print axioms MUB.partial_control_with_count_gap_is_not_complete
#print axioms MUB.composite_completion_gate_records_basis_gap
#print axioms MUB.composite_completion_gate_authority_requires_witness_or_nogo
#print axioms MUB.composite_lower_control_without_certificate_no_complete_authority
#print axioms MUB.composite_tensor_family_gate_records_pairing_and_gap
#print axioms MUB.composite_tensor_family_gate_authority_requires_witness_or_nogo
#print axioms MUB.composite_tensor_family_lower_control_without_certificate_no_complete_authority
#print axioms MUB.d10_lower_control_without_complete_certificate_no_mub10_authority
#print axioms MUB.d6_lower_control_without_cover_no_full_mub6_authority
#print axioms MUB.complete_control_authorizes_declared_dimension
#print axioms MUB.odd_prime_weyl_schema_authorizes_declared_prime_dimension
#print axioms MUB.odd_prime_exact_control_authorizes_declared_dimension
#print axioms MUB.odd_prime_exact_control_requires_field_and_hilbert_transport
#print axioms MUB.odd_prime_exact_control_requires_exact_mub_checks
#print axioms MUB.odd_prime_gauss_certificate_authorizes_declared_dimension
#print axioms MUB.odd_prime_gauss_certificate_requires_character_and_gauss_checks
#print axioms MUB.odd_prime_gauss_certificate_requires_field_and_transport
#print axioms MUB.odd_prime_power_weyl_schema_authorizes_declared_prime_power_dimension
#print axioms MUB.odd_prime_power_exact_control_authorizes_declared_dimension
#print axioms MUB.odd_prime_power_exact_control_requires_field_and_hilbert_transport
#print axioms MUB.odd_prime_power_exact_control_requires_exact_mub_checks
#print axioms MUB.odd_prime_power_exact_control_pair_authorizes_declared_dimensions
#print axioms MUB.odd_prime_power_exact_control_pair_requires_distinct_controls
#print axioms MUB.odd_prime_power_exact_control_pair_requires_each_exact_mub_check
#print axioms MUB.odd_prime_power_exact_control_triple_authorizes_declared_dimensions
#print axioms MUB.odd_prime_power_exact_control_triple_requires_distinct_controls
#print axioms MUB.odd_prime_power_exact_control_triple_requires_each_exact_mub_check
#print axioms MUB.odd_prime_power_exact_control_finite_batch_records_declared_only
#print axioms MUB.odd_prime_power_finite_field_theorem_gate_acceptance_requires_field_and_characters
#print axioms MUB.odd_prime_power_finite_field_theorem_gate_without_character_orthogonality_no_field_theorem
#print axioms MUB.odd_prime_power_finite_field_theorem_gate_without_gauss_no_field_theorem
#print axioms MUB.odd_prime_power_parametric_gate_acceptance_requires_finite_records
#print axioms MUB.odd_prime_power_parametric_gate_acceptance_requires_field_and_characters
#print axioms MUB.odd_prime_power_parametric_gate_acceptance_requires_hilbert_gtmur_terminalizer
#print axioms MUB.odd_prime_power_parametric_gate_without_field_theorem_no_family
#print axioms MUB.odd_prime_power_parametric_gate_without_hilbert_transport_no_family
#print axioms MUB.odd_prime_power_parametric_gate_without_gtmur_no_family
#print axioms MUB.char_two_weyl_board_schema_authorizes_declared_dimension_after_lift
#print axioms MUB.char_two_weyl_board_schema_requires_spectral_projector_lift
#print axioms MUB.spectral_projector_lift_schema_authorizes_declared_dimension
#print axioms MUB.spectral_projector_lift_schema_requires_positivity
#print axioms MUB.char_two_projector_algebra_schema_authorizes_declared_dimension
#print axioms MUB.char_two_projector_algebra_schema_requires_positivity_lift
#print axioms MUB.finite_hilbert_transport_schema_authorizes_declared_dimension
#print axioms MUB.finite_hilbert_transport_schema_requires_gtmur_loss_ledger
#print axioms MUB.finite_gtmur_projector_ledger_requires_zeroRel_preservation
#print axioms MUB.finite_gtmur_projector_ledger_requires_terminalizer_preservation
#print axioms MUB.finite_projector_control_authorizes_declared_dimension
#print axioms MUB.finite_projector_control_requires_projector_zerorel
#print axioms MUB.finite_projector_control_requires_gtmur_ledger
#print axioms MUB.finite_projector_control_without_parametric_family_no_general_authority
#print axioms MUB.char_two_parametric_gate_acceptance_requires_field_and_spread
#print axioms MUB.char_two_parametric_gate_acceptance_requires_lift_hilbert_gtmur
#print axioms MUB.char_two_parametric_gate_without_positive_projectors_no_family
#print axioms MUB.char_two_parametric_gate_without_gtmur_no_family
#print axioms MUB.prime_power_gtmur_boundary_requires_all_characteristic_records
#print axioms MUB.prime_power_gtmur_boundary_requires_composite_nonpromotion
#print axioms MUB.finite_controls_without_parametric_family_no_general_authority
#print axioms MUB.composite_completion_gate_without_parametric_family_no_general_authority
#print axioms MUB.composite_tensor_family_gate_without_parametric_family_no_general_authority
#print axioms MUB.finite_stratification_without_parametric_family_no_general_authority
#print axioms MUB.odd_prime_weyl_schema_without_parametric_family_no_general_authority
#print axioms MUB.odd_prime_exact_control_without_parametric_family_no_general_authority
#print axioms MUB.odd_prime_gauss_certificate_without_parametric_family_no_general_authority
#print axioms MUB.odd_prime_power_weyl_schema_without_parametric_family_no_general_authority
#print axioms MUB.odd_prime_power_exact_control_without_parametric_family_no_general_authority
#print axioms MUB.odd_prime_power_exact_control_pair_without_parametric_family_no_general_authority
#print axioms MUB.odd_prime_power_exact_control_triple_without_parametric_family_no_general_authority
#print axioms MUB.odd_prime_power_exact_control_finite_batch_without_parametric_family_no_general_authority
#print axioms MUB.odd_prime_power_parametric_gate_without_general_certificate_family_no_general_authority
#print axioms MUB.char_two_weyl_board_schema_without_parametric_family_no_general_authority
#print axioms MUB.spectral_projector_lift_schema_without_parametric_family_no_general_authority
#print axioms MUB.char_two_projector_algebra_schema_without_parametric_family_no_general_authority
#print axioms MUB.finite_hilbert_transport_schema_without_parametric_family_no_general_authority
#print axioms MUB.finite_gtmur_projector_ledger_without_parametric_family_no_general_authority
#print axioms MUB.prime_power_gtmur_boundary_without_parametric_family_no_general_authority
#print axioms MUB.no_general_mub_n_authority_without_certificate_family
#print axioms MUB.no_representation_authority_without_closed_loss_ledger
#print axioms MUB.gtor_gttc_gate_authority_requires_descent_and_gluing
#print axioms MUB.gttc_gate_authority_requires_uniform_certificate_family
#print axioms MUB.gtor_gttc_gate_without_terminalized_descent_no_authority
#print axioms MUB.gtor_completion_does_not_create_auth
#print axioms MUB.gttc_continuum_shadow_does_not_create_auth
