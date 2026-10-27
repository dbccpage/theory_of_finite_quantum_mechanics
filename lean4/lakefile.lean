
import Lake
open Lake DSL

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.35.0"

package «FiniteQuantum» where
  version := v!"0.1.0"
  buildDir := "b"

@[default_target]
lean_lib «FiniteQuantum» where
  srcDir := "."
  roots := #[

    `FiniteGraphDressing,
    `TensorConeReconstruction,
    `TensorTomography,
    `ComplexFieldSelection,
    `OperationalTomography,
    `OperationalFieldSelection,
    `OperationalFilterFamily,
    `OperationalBoundaryWitnesses,
    `OperationalSymmetry,
    `OperationalCoherence,
    `OperationalIndependence,
    `TensorCoordinates,
    `TensorSchmidt,
    `TensorReachability,
    `TensorOperationalCone,
    `TensorComposition,
    `TensorEffectOrder,
    `TensorEffectCone,
    `TensorMeasurements,
    `TensorPartialTranspose,
    `TensorCountermodelCones,
    `TensorCountermodelWitnesses,
    `TensorCountermodelEmbeddings,
    `TensorHiddenCoordinates,
    `SwitchingNormalForm,
    `EntropyDichotomy,
    `BornNormalization,
    `CellGrammar,
    `CausalOrder,
    `NoSignalling,
    `NoSignallingCore,
    `U1AngleAddition,
    `U1TorsionExclusion,
    `U1PythagoreanObstruction,
    `U1PowerMapInjectivity,
    `U1CayleyProjectiveCircle,
    `U1CyclotomicTorsionTower,
    `U1CauchyCircleCompletion,
    `U1ChebyshevCauchyBridge,
    `U1QuadraticTowerAndCayleyStone,
    `U1PhaseSynthesis,
    `RotationGroups,
    `LorentzBoost,
    `BoostComposition,
    `QuantumCorrelation,
    `ContextualityObstruction,
    `CommutingObservables,
    `GroupParameter,
    `CausalPriceList,
    `CochainWindow,
    `Core,
    `DualWitness,
    `Entanglement,
    `EventEffects,
    `Expressivity,
    `FiniteQM,
    `FiniteQFTAndGravity,
    `FiniteCochain,
    `FiniteDensity,
    `FiniteN3ResidualDual,
    `GleasonTheorem,
    `GleasonRationalPlane,
    `BornEffectValuation,
    `BornLinearExtension,
    `BornMatrixCarrier,
    `BornPsdDecomposition,
    `BornTraceRepresentation,
    `BornRationalSphereObstruction,
    `DiscreteTimeStoneSpec,
    `BornGaussRat,
    `BornHermitianCarrier,
    `BornHermitianPsdDecomposition,
    `BornHermitianTraceRepresentation,
    `SectorFormUniqueness,
    `SectorFormHermitian,
    `FiniteWignerKernel,
    `FiniteWignerTheorem,
    `FiniteWignerSimilarity,
    `GaussRatAutomorphisms,
    `WeylCommutant,
    `ProbabilitySimplex,
    `HilbertWalkRationals,
    `ReversibilityGate,
    `FreeLinearization,
    `InnerProductAdmission,
    `HilbertWalkEnvelope,
    `PermutationUnitary,
    `Complexification,
    `HilbertWalkPhaseBlindPresentation,
    `PhaseFiber,
    `HilbertWalkHadamard,
    `InterferenceNonDescent,
    `HilbertWalkScale,
    `HilbertWalkCircle,
    `U1SelectorBoundary,
    `OperatorAlgebraShadow,
    `BornPairingBoundary,
    `FrameAdditivity,
    `QuarticRivalSeparation,
    `HilbertWalkSameContract,
    `BilinearProduct,
    `HilbertWalkInterface,
    `TensorCompositionBoundary,
    `CollapseDilations,
    `DilationCount,
    `IrreversibleFork,
    `ContinuousDynamicsFork,
    `HilbertWalkGleasonExtras,
    `FiniteHilbertBoundary,
    `HilbertWalkGleasonExtrasDropOne,
    `HilbertWalkGleasonFin,
    `HilbertWalkGleasonFinish,
    `HilbertWalkGleason,
    `MatrixFiniteRecovery,
    `HilbertWalkChannel,
    `HilbertWalkDensity,
    `RationalLieSpan,
    `CabelloSignPolytope,
    `TriangleNetworkComplexCarrier,
    `SimplicialAreaLawPageCurve,
    `DiscreteSpinfoamAmplitudes,
    `FourSimplexSpinfoamS4,
    `SpinfoamBoundaryUnitarity,
    `MasterConstraintSpinfoamKernel,
    `PachnerMasterConstraintFiniteness,
    `ArbitraryDegreePolynomialReduction,
    `Simplicial3complexCayleyEvolution,
    `OctahedralMubCliftonKent,
    `OctahedralDepolarizingThreshold,
    `DiscretePythagoreanBellChsh,
    `PythagoreanPellTsirelsonConvergence,
    `CliffordPauliConjugationAndTGateOrbit,
    `DiscreteWignerNegativityResource,
    `ThreeQubitCodeSyndromeRecovery,
    `FourQubitCssSurfaceCode,
    `SteaneFanoCodeTransversalGates,
    `DiscreteQuantumTeleportation,
    `DiscreteSuperdenseCoding,
    `PrimePWignerPhaseSpace,
    `ShorNineQubitCode,
    `DiscretePhaseEstimation,
    `SurfaceCodeToricTopology,
    `DiscreteGroverSearch,
    `DiscreteCliffordSymplectic,
    `StoneVonNeumannObstruction,
    `RichardsonErrorMitigation,
    `QuantumWalkSymmetricCayley,
    `MubTomographyInversion,
    `Mub4GaloisFieldContextuality,
    `CyclotomicTowerDirected,
    `EverettForkingTree,
    `GleasonCyclotomicObstruction,
    `DiscreteDynamicsStone,
    `ContinuumLiftBoundary,
    `HigherDimConductorBounds,
    `EffectFrameBusch,
    `RationalSector,
    `EmbeddingRelativity,
    `DynamicsDichotomy,
    `CompositionTensorMub,
    `CptpChannelsStinespring,
    `ContextualityThresholds,
    `CancellationCertificates,
    `GrowthRefinement,
    `TerminalPriceList,
    `HWKernel,
    `IntegralRefinementC3C6,
    `OntologyBasic,
    `OntologyPrimitiveBridge,
    `PointedObstructionClassifier,
    `PrimitiveAdmissibleRepair,
    `PrimitiveDifference,
    `PrimitiveDifferenceBridge,
    `PrimitiveLiftCandidate,
    `PrimitiveLiftCertificate,
    `PrimitiveObstructionPipeline,
    `PrimitiveRepairBoundary,
    `PrimitiveRepairCertificate,
    `PrimitiveRepairWitness,
    `PrimitiveSpineSummary,
    `PrimitiveTerminalPacket,
    `ResidualDensityBridge,
    `RetainedProfileCecBridge,
    `SolverFrontier,
    `Superposition,
    `WorldCHSH,
    `WorldCovariantWignerYanase,
    `WorldCycle3Quotient,
    `WorldFiniteReconstruction,
    `WorldFiniteToInfinite,
    `WorldGateVacuity,
    `WorldLGGRWitness,
    `WorldLiftExhaustion,
    `WorldObserverDirectedColimitNoGo,
    `WorldObserverFunctoriality,
    `WorldPresentation,
    `WorldRebitHiddenDirection,
    `WorldReconstructionRetraction,
    `WorldResidualGrowth,
    `WorldWGOCSealedRefusal,
    `WeylCcrResidual,
    `NormApproximationFrontier,
    `HeisenbergRepresentationUniqueness,
    `RefinementSubsystemTower,
    `TowerTopologicalCompletion,
    `ContinuousTimeLocalityLimit,
    `OperationalAxiomSelection,
    `TensorCommutingCorrelationFrontier,
    `LatticeGaugeManybodyBenchmark,
    `FiniteOperationalClosureContract,
    `GaussIntKernel,
    `PhaseBlindPresentation,
    `QuotientFiber,
    `MixingObstruction,
    `InterferenceDeficit,
    `CoboundaryHolonomy,
    `BuildabilitySetS,
    `BornRedundancy,
    `BornRedundancyAxioms,
    `TraceZeroDuality,
    `TraceZeroDualityAxioms,
    `FinitePresentedCarrier,
    `ReportDynamics,
    `HWCarrierThread,
    `HWFullThread,
    `HWThread,
    `HilbertWalkAll,
    `SharedCharacter,
    `T1ScalarPeriod,
    `T2MarkedFreeLift,
    `T4CharacterRemainder,
    `T5TorsionNotZ,
    `T7PiLocalization,
    `CoupledRelationalProjectors,
    `DerivationDagQMClosure,
    `BellClassicalJointExtension,
    `BellOperad,
    `BellSeparatorExtension,
    `PromptBellRational,
    `PromptBornRay,
    `CabelloVertexData,
    `PromptCabelloCensus,
    `PromptCabelloParity,
    `PromptCarrierContract,
    `PromptCechF2,
    `PromptC500Ledger,
    `PromptBornGap,
    `PromptPhaseScope,
    `PromptStructure,
    `PromptDynamics,
    `PromptResources,
    `PromptBoundaries, `PromptGenesisImplementation,
    `PromptEntropyExact,
    `PromptDeclaredInterface,
    `LggrFiniteResults,
    `CofiberBanachQuotient,
    `HilbertLiftFiniteTower,
    `HilbertLiftRationalUniformity,
    `HilbertLiftCompletion,
    `HilbertLiftComplexCarrier,
    `HilbertLiftIntrinsicUniformity,
    `HilbertLiftL2Model,
    `HilbertLiftOperators,
    -- Primitive difference foundation modules
    `ProjectionFiberPrimitiveDifference,
    `FiberQuotientEquivalence,
    `ProjectionEscapeResidual,
    `LiteralInvariance,
    `FiberDynamicsCongruence,
    `UniqueDescendedDynamics,
    `SelectedProjectedMap,
    `DescentFailureWithoutEscape,
    -- Pre-existing foundational modules
    `EntropyAxioms,
    `EntropyDefs,
    `EntropyPurity,
    `EntropyReduction,
    `RaveraDfmFiniteToContinuum,
    -- MUB(6) formalization modules
    `AdditiveCharacter,
    `AlgebraicCoefficientFieldContract,
    `AlgebraicCornerReconstruction,
    `AlgebraicGtmurLossLedgerContract,
    `AlgebraicHilbertBasisTransportContract,
    `AlgebraicTerminalizerPreservationContract,
    `AuditMub6Axioms,
    `BasisExtensionObstruction,
    `CADBranch,
    `CandidateGramPositivity,
    `CaseCoverage,
    `CertificatePilot,
    `CochainObstruction,
    `CollarGluing,
    `CommutativeFlatMoments,
    `ComplexCoefficientScalars,
    `ConcreteMubFlatExtension,
    `ConcreteMubMoments,
    `ConcreteMubPolynomials,
    `ConcreteMubProjectors,
    `ConcreteSemantics,
    `Conjecture2GeneralMechanization,
    `ContinuousBoundaryHomotopyPositivstellensatz,
    `CornerDeterminantCrossRatio,
    `DeltoidCuspGluing,
    `DeltoidCuspInputAudit,
    `DeltoidCuspLiteralSemantics,
    `DeltoidCuspLiteralVector,
    `DeltoidCuspPhaseReduction,
    `Discrete4DBianchiSpectralContraction,
    `ExportSzollosiCoefficients,
    `ExportSzollosiSystem,
    `ExtensionCurvatureObstruction,
    `FiniteBasisCover,
    `FiniteFieldCharacters,
    `FiniteFieldFamily,
    `FiniteFunctionGtmurLedger,
    `FiniteFunctionGtmurLossLedger,
    `FiniteFunctionHilbertBasisTransport,
    `FiniteFunctionTerminalizer,
    `FiniteVectorCover,
    `FixedTuplePsiCertificate,
    `FlatMomentBasisRelations,
    `FlatMomentProjectorExtraction,
    `FourierLandingBypass,
    `FramePotentialObstruction,
    `G1_Orbits,
    `GlobalGaugeChaining,
    `Gluing,
    `GrandUnifiedMasterSynthesis,
    `GroebnerBranch,
    `HilbertMubFamily,
    `HilbertMubStructure,
    `HilbertPhaseNormalization,
    `HilbertPhaseTransport,
    `HilbertPhaseVectors,
    `HilbertTransportEquiv,
    `HyperGramianObstruction,
    `KarlssonManifold,
    `KarlssonVolumeObstruction,
    `KernelReflection1024,
    `KernelReflectionB1Intervals,
    `KernelReflectionBisection,
    `KernelReflectionGrandFrontier,
    `KernelReflectionGrandUnified,
    `KernelReflectionKarlssonVolume,
    `KernelReflectionPilot,
    `KernelReflectionScaled,
    `KernelReflectionSzollosiDeltoid,
    `KernelReflectionTaoConfluence,
    `KernelReflectionTaoHaagerup,
    `L1CellBisectionBridge,
    `LipschitzGapPropagation,
    `LiteralCuspCertificate,
    `MUB,
    `MasterClassification,
    `ModuliReduction,
    `MomentPositivityObligation,
    `Mub6,
    `Mub6L1SnTower,
    `MubBalancedCodedSystem,
    `MubBalancedCoefficients,
    `MubBalancedCompletion,
    `MubBalancedExport,
    `MubBalancedIndices,
    `MubBalancedQuadraticLift,
    `MubBalancedQuadraticPolynomials,
    `MubBalancedTable,
    `MubBoundedBlockChart,
    `MubBoundedCodedSystem,
    `MubBoundedCoefficientExpansion,
    `MubBoundedCoordinates,
    `MubBoundedExport,
    `MubBoundedExportIndices,
    `MubBoundedExpressions,
    `MubBoundedMUFactor,
    `MubBoundedPolynomials,
    `MubBoundedQuartetEquations,
    `MubBoundedTermCollection,
    `MubGaugeSyzygy,
    `MubIndexTransport,
    `MubMinorChart,
    `MubMonomialTransport,
    `MubQuadraticCompatibilityPolynomials,
    `MubQuadraticLift,
    `MubQuadraticLiftCodedSystem,
    `MubQuadraticLiftCoefficients,
    `MubQuadraticLiftCompatibility,
    `MubQuadraticLiftDegree,
    `MubQuadraticLiftExport,
    `MubQuadraticLiftIndices,
    `MubQuadraticLiftNarrowBox,
    `MubQuadraticLiftPolynomials,
    `MubQuadraticLiftTable,
    `MubQuadraticTransitionSeparation,
    `MubQuartetTransportBridge,
    `MubTaoLaurent,
    `MultiChartTransitionCocycle,
    `NormalizedTriplesChart,
    `PolynomialEncoding,
    `QuadIncompatibility,
    `QuadraticGaussReduction,
    `RectangularQuadraticExclusion,
    `RouteCFourierLandingBypass,
    `ScopeFirebreak,
    `SharedKernelAdditiveCharacter,
    `SparseLanding,
    `SparseLandingGeneral,
    `SparseRectangularExclusion,
    `SzollosiColumnGauge,
    `SzollosiCommonRays,
    `SzollosiDeltoid,
    `SzollosiExecutableSystem,
    `SzollosiGaugeBalance,
    `SzollosiGaugedCover,
    `SzollosiGaugedExecutable,
    `SzollosiGaugedReflection,
    `SzollosiIntervalExclusion,
    `SzollosiLaurentPairing,
    `SzollosiNativeInterval,
    `SzollosiNativeReflection,
    `SzollosiQuadraticSystem,
    `SzollosiQuartetSystem,
    `SzollosiRectangularExclusion,
    `SzollosiRectangularJacobian0,
    `SzollosiRectangularJacobian1,
    `SzollosiRectangularJacobian2,
    `SzollosiRectangularJacobian3,
    `SzollosiRectangularJacobian4,
    `SzollosiRectangularJacobian5,
    `SzollosiRectangularJacobian6,
    `SzollosiRectangularJacobian7,
    `SzollosiRectangularJacobianCore,
    `SzollosiRectangularReflection,
    `SzollosiTermExpansion,
    `SzollosiTwoCirculant,
    `TaoConfluenceObstruction,
    `Target3NormalizedTriples,
    `Target4GapPropagation,
    `TargetA10GlobalCover,
    `TargetA11OrbitExhaustiveness,
    `TargetA12SmaleSentry,
    `TargetA13GrandSynthesis,
    `TargetA1CollarCover,
    `TargetA2DeltoidCusp,
    `TargetA4Gramian,
    `TargetA5FiniteCover,
    `TargetA6TaoConfluence,
    `TargetA7ZeroRelVariety,
    `TargetA8CollarBoundary,
    `TargetA9Haagerup,
    `TargetB1ContinuousChaining,
    `TargetB2GlobalGluing,
    `TargetB3ManifoldIntegration,
    `TargetG1OrbitExhaustiveness,
    `TargetQArchimedeanPositivstellensatz,
    `TotalUnimodularity,
    `TripleExtensionAssembly,
    `TripleGaugeReduction,
    `TripleHadamardDephase,
    `UnitaryInvariance,
    `WallTransport,
    `ZeroRelInvariance,
    `ZeroRelVariety,
    -- Fermion Sign Problem (FSP) formalization modules
    `BfLinkedFluxBraiding,
    `BqnfSignPacket,
    `ChiralAnomalyInflow,
    `ChiralSuperconductorCore,
    `Cobordism5dAnomaly,
    `FermionGinCore,
    `FermionSignAll,
    `FermionSignCore,
    `FibonacciAnyonBraiding,
    `FoliatedFracton2Gauge,
    `FqhLaughlinBraiding,
    `FrustratedSpectrumObstruction,
    `GenesisFspBridge,
    `GenesisComputation,
    `GenesisCompTM,
    `GenesisCompUniv,
    `HaltingQuotient,
    `Higher2GroupBraiding,
    `InstantonDyonGas,
    `IsingMajoranaBraiding,
    `KitaevHoneycombCore,
    `MajoranaGinCore,
    `MeronCharacter,
    `MeronClusterInvolution,
    `NonAbelianBfBraiding,
    `NonAbelianGaugeSigns,
    `NormalFormLaws,
    `ReggePachnerWdw,
    `regge_wdw_core,
    -- Majorana formalization modules
    `MajoranaF2Trichotomy,
    `MajoranaMZM,
    `MajoranaTransferBounds,
    `MajoranaCore
  ]

private def l5aProvenance : String :=
  "Origin: lean4/lakefile.lean Claim: package configuration AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"

lean_lib PromptL1Imports where
  roots := #[`PromptL1Imports]

lean_lib PromptBornBoundaries where
  roots := #[`PromptBornBoundaries]

-- Recovered Authorization-Incompleteness finite models (provenance: lean4/AuthIncompleteness/*.lean headers).
-- Not a default target: build with `lake build AuthIncompleteness`.
lean_lib AuthIncompleteness where
  roots := #[`AuthIncompleteness]

lean_lib QcSelfObstruction where
  roots := #[`QcConcatenation, `QcRepairQueue, `QcEntropySink, `QcSelfObstruction]

-- PFP batch 01 (positions 152-177) Lean modules, sealed by dag/results/batches/20261021T132245Z_prompts_152_164
-- and 20261021T175809Z_prompts_165_177. Not a default target: build with `lake build PfpBatch01`
-- or one module at a time, e.g. `lake build AdmissionFloor`.
lean_lib PfpBatch01 where
  roots := #[
    `PhaseBlindFiber,
    `ResidualSectorWeights,
    `U1SelectorSegment,
    `RealificationJ,
    `ObligationMonoid,
    `SnCarrierPfp,
    `AdmissionFloor,
    `ChainRetraction,
    `CollapseBarrier,
    `DemandAccounting,
    `FreeMonoidNoniso,
    `HistoryReport,
    `InertDiamond,
    `OldImageInjective,
    `PregenConstructive,
    `PrimdiffAxioms,
    `RefineSeparates,
    `RootDiffStructure,
    `SixOperations,
    `SnOffImageRefusal,
    `WdpBridgeObligations,
    `WdpDegree1Window,
    `WdpDiagnosticRouting,
    `WdpGrowthNoRepair,
    `WdpProtectedQuestions,
    `WdpQuotientSequence
  ]

-- Finite frontier target Lean modules (Task 3: CT, CQFT, ADS, LQG finite targets).
-- Not a default target: build with `lake build FrontierTargets` or per module.
lean_lib FrontierTargets where
  roots := #[
    `FrontierDistinguishability,
    `FrontierNoCloning,
    `FrontierEntanglingPhase,
    `FrontierPosetNet,
    `FrontierRsCyclicity,
    `FrontierLinearExtension,
    `FrontierMyrheimMeyer,
    `FrontierFiveQubitPerfectTensor,
    `FrontierLogicalReconstruction,
    `FrontierHappyMincut,
    `FrontierAreaSpectrum,
    `FrontierTvLevel2Pentagon,
    `FrontierClassical6j,
    `FrontierPrAllowedRegion
  ]

-- Lean imported from the sibling atlas (omega_engine_atlas / omega_engine_education) so that the evidence the DAG
-- cites lives in this repository. Provenance, original sha256 and any port notes are in each file header and in
-- lean4/Imported/import_manifest.json. Not a default target: build with `lake build ImportedAtlas`
-- or one module at a time, e.g. `lake build Imported.GenesisDerivation.Derivation.Inertia`.
lean_lib ImportedAtlas where
  roots := #[
    `Imported.GenesisDerivation.CanonicalMinimizer,
    `Imported.GenesisDerivation.Derivation,
    `Imported.GenesisDerivation.Derivation.Apartness,
    `Imported.GenesisDerivation.Derivation.Attachment,
    `Imported.GenesisDerivation.Derivation.Basic,
    `Imported.GenesisDerivation.Derivation.BoundaryCancellation,
    `Imported.GenesisDerivation.Derivation.Breaking,
    `Imported.GenesisDerivation.Derivation.Bridge,
    `Imported.GenesisDerivation.Derivation.CapacityBound,
    `Imported.GenesisDerivation.Derivation.ClosureSymmetry,
    `Imported.GenesisDerivation.Derivation.Completion,
    `Imported.GenesisDerivation.Derivation.Compression,
    `Imported.GenesisDerivation.Derivation.Constitution,
    `Imported.GenesisDerivation.Derivation.ContactBridge,
    `Imported.GenesisDerivation.Derivation.ContactKernel,
    `Imported.GenesisDerivation.Derivation.ControllerCategory,
    `Imported.GenesisDerivation.Derivation.CountTransport,
    `Imported.GenesisDerivation.Derivation.Counting,
    `Imported.GenesisDerivation.Derivation.DiffInterface,
    `Imported.GenesisDerivation.Derivation.EndogenousFidelityGenerator,
    `Imported.GenesisDerivation.Derivation.Erasure,
    `Imported.GenesisDerivation.Derivation.Ext,
    `Imported.GenesisDerivation.Derivation.FidelityClosure,
    `Imported.GenesisDerivation.Derivation.FormRenaming,
    `Imported.GenesisDerivation.Derivation.FormTransport,
    `Imported.GenesisDerivation.Derivation.G1Class,
    `Imported.GenesisDerivation.Derivation.Generator,
    `Imported.GenesisDerivation.Derivation.GraphGenesis,
    `Imported.GenesisDerivation.Derivation.HigherStructure,
    `Imported.GenesisDerivation.Derivation.Horizon,
    `Imported.GenesisDerivation.Derivation.Inertia,
    `Imported.GenesisDerivation.Derivation.Initiality,
    `Imported.GenesisDerivation.Derivation.InterpreterBoundary,
    `Imported.GenesisDerivation.Derivation.IsoCanon,
    `Imported.GenesisDerivation.Derivation.IsoCollapse,
    `Imported.GenesisDerivation.Derivation.LadderGeneral,
    `Imported.GenesisDerivation.Derivation.LocalStrategy,
    `Imported.GenesisDerivation.Derivation.Mention,
    `Imported.GenesisDerivation.Derivation.Minimality,
    `Imported.GenesisDerivation.Derivation.MinimalityF,
    `Imported.GenesisDerivation.Derivation.NoOutside,
    `Imported.GenesisDerivation.Derivation.NoOutsideFidelity,
    `Imported.GenesisDerivation.Derivation.ObsDescent,
    `Imported.GenesisDerivation.Derivation.ObserverInventory,
    `Imported.GenesisDerivation.Derivation.Pigeonhole,
    `Imported.GenesisDerivation.Derivation.PresentationDescent,
    `Imported.GenesisDerivation.Derivation.PresentationNaturality,
    `Imported.GenesisDerivation.Derivation.PresentationRelativity,
    `Imported.GenesisDerivation.Derivation.PrimDiff,
    `Imported.GenesisDerivation.Derivation.PrimitiveCats,
    `Imported.GenesisDerivation.Derivation.PrimitiveContact,
    `Imported.GenesisDerivation.Derivation.PrimitiveCore,
    `Imported.GenesisDerivation.Derivation.PrimitivePassage,
    `Imported.GenesisDerivation.Derivation.Progress,
    `Imported.GenesisDerivation.Derivation.Quot,
    `Imported.GenesisDerivation.Derivation.QuotientRetention,
    `Imported.GenesisDerivation.Derivation.Refusal,
    `Imported.GenesisDerivation.Derivation.RefusalFrontier,
    `Imported.GenesisDerivation.Derivation.RenamingStructure,
    `Imported.GenesisDerivation.Derivation.Represented,
    `Imported.GenesisDerivation.Derivation.ResidualClosure,
    `Imported.GenesisDerivation.Derivation.Rounds,
    `Imported.GenesisDerivation.Derivation.RuleBridge,
    `Imported.GenesisDerivation.Derivation.SeparationCapacity,
    `Imported.GenesisDerivation.Derivation.StableContent,
    `Imported.GenesisDerivation.Derivation.TraceAlgebra,
    `Imported.GenesisDerivation.Derivation.TransitionAlphabet,
    `Imported.GenesisDerivation.Derivation.TransitionTransport,
    `Imported.GenesisDerivation.Derivation.WeightProfile,
    `Imported.GenesisDerivation.Paper,
    `Imported.GenesisDerivation.Paper000,
    `Imported.GenesisDerivation.PaperCanonical,
    `Imported.GenesisDerivation.PaperOrbit,
    `Imported.GenesisDerivation.PaperSearch,
    `Imported.GenesisDerivation.PaperWire,
    `Imported.GenesisDerivation.Permutation,
    `Imported.GenesisDerivation.RegimeAction,
    `Imported.GenesisDerivation.SecondRun,
    `Imported.GenesisDerivation.SecondRun.Kernel,
    `Imported.GenesisDerivation.SecondRun.Run,
    `Imported.PreGenesisToMssn.Cochain,
    `Imported.PreGenesisToMssn.FreeAbelian,
    `Imported.PreGenesisToMssn.GraphHomology,
    `Imported.PreGenesisToMssn.Homology,
    `Imported.PreGenesisToMssn.Observation,
    `Imported.PreGenesisToMssn.Paper,
    `Imported.PreGenesisToMssn.SnCarrier,
    `Imported.PreGenesisToMssn.SnSyntax,
    `Imported.PreGenesisToMssn.SnTheorems,
    `Imported.PreGenesisToMssn.TriangleHomology,
    `Imported.WitnessedDifference.WitnessedDifference.BehavioralQuotient,
    `Imported.WitnessedDifference.WitnessedDifference.ComplexTensorBalancing,
    `Imported.WitnessedDifference.WitnessedDifference.Core,
    `Imported.WitnessedDifference.WitnessedDifference.Descent,
    `Imported.WitnessedDifference.WitnessedDifference.FoundationalBridges,
    `Imported.WitnessedDifference.WitnessedDifference.GenerativeHistoryCompression,
    `Imported.WitnessedDifference.WitnessedDifference.GenesisConstruction,
    `Imported.WitnessedDifference.WitnessedDifference.ObserverResolution,
    `Imported.WitnessedDifference.WitnessedDifference.Obstruction,
    `Imported.WitnessedDifference.WitnessedDifference.PointedRelation,
    `Imported.WitnessedDifference.WitnessedDifference.PrimitiveAdmissionFloor,
    `Imported.WitnessedDifference.WitnessedDifference.Probability,
    `Imported.WitnessedDifference.WitnessedDifference.ProposalAdmissionBridge,
    `Imported.WitnessedDifference.WitnessedDifference.RootGaugeNormalization,
    `Imported.WitnessedDifference.WitnessedDifference.Routing,
    `Imported.WitnessedDifference.WitnessedDifference.Succession,
    `Imported.WitnessedDifference.WitnessedDifference.Symmetry,
    `Imported.GenesisOngoing.Eighth.Compare,
    `Imported.GenesisOngoing.Eighth.Cost,
    `Imported.GenesisOngoing.Eighth.Reach,
    `Imported.GenesisOngoing.Eighth.Rename,
    `Imported.GenesisOngoing.Eighth.State,
    `Imported.GenesisOngoing.Eighth.Step,
    `Imported.GenesisOngoing.Eleventh.Compare,
    `Imported.GenesisOngoing.Eleventh.Rename,
    `Imported.GenesisOngoing.Eleventh.State,
    `Imported.GenesisOngoing.Eleventh.Step,
    `Imported.GenesisOngoing.Fifteenth.Compare,
    `Imported.GenesisOngoing.Fifteenth.Rename,
    `Imported.GenesisOngoing.Fifteenth.State,
    `Imported.GenesisOngoing.Fifteenth.Step,
    `Imported.GenesisOngoing.Fifth.Answers,
    `Imported.GenesisOngoing.Fifth.Compare,
    `Imported.GenesisOngoing.Fifth.Cost,
    `Imported.GenesisOngoing.Fifth.Reach,
    `Imported.GenesisOngoing.Fifth.Rename,
    `Imported.GenesisOngoing.Fifth.State,
    `Imported.GenesisOngoing.Fifth.Step,
    `Imported.GenesisOngoing.Fourteenth.Compare,
    `Imported.GenesisOngoing.Fourteenth.Rename,
    `Imported.GenesisOngoing.Fourteenth.State,
    `Imported.GenesisOngoing.Fourteenth.Step,
    `Imported.GenesisOngoing.Fourth.Answers,
    `Imported.GenesisOngoing.Fourth.Compare,
    `Imported.GenesisOngoing.Fourth.Contain,
    `Imported.GenesisOngoing.Fourth.Cost,
    `Imported.GenesisOngoing.Fourth.Rename,
    `Imported.GenesisOngoing.Fourth.State,
    `Imported.GenesisOngoing.Fourth.Step,
    `Imported.GenesisOngoing.H3V7N5QF.Answers,
    `Imported.GenesisOngoing.H3V7N5QF.Basic,
    `Imported.GenesisOngoing.H3V7N5QF.Cost,
    `Imported.GenesisOngoing.H3V7N5QF.Finite,
    `Imported.GenesisOngoing.H3V7N5QF.Paths,
    `Imported.GenesisOngoing.Ninth.Compare,
    `Imported.GenesisOngoing.Ninth.Cost,
    `Imported.GenesisOngoing.Ninth.Reach,
    `Imported.GenesisOngoing.Ninth.Rename,
    `Imported.GenesisOngoing.Ninth.State,
    `Imported.GenesisOngoing.Ninth.Step,
    `Imported.GenesisOngoing.Second.Answers,
    `Imported.GenesisOngoing.Second.Carry,
    `Imported.GenesisOngoing.Second.Cost,
    `Imported.GenesisOngoing.Second.Rename,
    `Imported.GenesisOngoing.Second.Step,
    `Imported.GenesisOngoing.Seventh.Compare,
    `Imported.GenesisOngoing.Seventh.Cost,
    `Imported.GenesisOngoing.Seventh.Reach,
    `Imported.GenesisOngoing.Seventh.Rename,
    `Imported.GenesisOngoing.Seventh.State,
    `Imported.GenesisOngoing.Seventh.Step,
    `Imported.GenesisOngoing.Sixteenth.Cost,
    `Imported.GenesisOngoing.Sixteenth.Reach,
    `Imported.GenesisOngoing.Sixteenth.State,
    `Imported.GenesisOngoing.Sixteenth.Step,
    `Imported.GenesisOngoing.Sixth.Compare,
    `Imported.GenesisOngoing.Sixth.Cost,
    `Imported.GenesisOngoing.Sixth.Reach,
    `Imported.GenesisOngoing.Sixth.Rename,
    `Imported.GenesisOngoing.Sixth.State,
    `Imported.GenesisOngoing.Sixth.Step,
    `Imported.GenesisOngoing.Tenth.Compare,
    `Imported.GenesisOngoing.Tenth.Rename,
    `Imported.GenesisOngoing.Tenth.State,
    `Imported.GenesisOngoing.Tenth.Step,
    `Imported.GenesisOngoing.Third.Answers,
    `Imported.GenesisOngoing.Third.Contain,
    `Imported.GenesisOngoing.Third.Cost,
    `Imported.GenesisOngoing.Third.Rename,
    `Imported.GenesisOngoing.Third.Step,
    `Imported.GenesisOngoing.Thirteenth.Compare,
    `Imported.GenesisOngoing.Thirteenth.Rename,
    `Imported.GenesisOngoing.Thirteenth.State,
    `Imported.GenesisOngoing.Thirteenth.Step,
    `Imported.GenesisOngoing.Twelfth.Compare,
    `Imported.GenesisOngoing.Twelfth.Rename,
    `Imported.GenesisOngoing.Twelfth.State,
    `Imported.GenesisOngoing.Twelfth.Step,
    `Imported.GenesisOngoing.Twentieth.Order,
    `Imported.GenesisOngoing.Twentyfirst.Refusal,
    `Imported.GenesisOngoingCore.Twentyfifth.Balance,
    `Imported.GenesisOngoingCore.Twentyfifth.Blind,
    `Imported.GenesisOngoingCore.Twentyfifth.Fill,
    `Imported.GenesisOngoingCore.Twentyfourth.Basic,
    `Imported.GenesisOngoingCore.Twentyfourth.Same,
    `Imported.GenesisOngoingCore.Twentyfourth.Tell,
    `Imported.GenesisOngoingCore.Twentysecond,
    `Imported.GenesisOngoingCore.Twentysecond.Basic,
    `Imported.GenesisOngoingCore.Twentysecond.Cost,
    `Imported.GenesisOngoingCore.Twentysecond.Merge,
    `Imported.GenesisOngoingCore.Twentysecond.Plain,
    `Imported.GenesisOngoingCore.Twentysecond.Reach,
    `Imported.GenesisOngoingCore.Twentysecond.Record,
    `Imported.GenesisOngoingCore.Twentysecond.Rename,
    `Imported.GenesisOngoingCore.Twentysecond.Same,
    `Imported.GenesisOngoingCore.Twentysecond.Seventh,
    `Imported.GenesisOngoingCore.Twentysecond.State,
    `Imported.GenesisOngoingCore.Twentysecond.Swap,
    `Imported.GenesisOngoingCore.Twentysecond.Undo,
    `Imported.GenesisOngoingCore.Twentythird,
    `Imported.GenesisOngoingCore.Twentythird.Cost,
    `Imported.GenesisOngoingCore.Twentythird.Fewest,
    `Imported.GenesisOngoingCore.Twentythird.Map,
    `Imported.GenesisOngoingCore.Twentythird.Nothing,
    `Imported.GenesisOngoingCore.Twentythird.Raise,
    `Imported.GenesisOngoingCore.Twentythird.Reach,
    `Imported.GenesisOngoingCore.Twentythird.Rename,
    `Imported.GenesisOngoingCore.Twentythird.Same,
    `Imported.SnMssn.Paper001,
    `Imported.L1ObstructionFramework.lp_cochains,
    `Imported.L1ObstructionFramework.lp_general_certificate,
    `Imported.ConditionalDensityLift.Xi,
    `Imported.OperatorLifts.Lifts,
    `Imported.OntologyBoundary.OntologyBasic,
    `Imported.CoordinateWiseAdditivity.gs003_coordinate_l1,
    `Imported.CoordinateWiseAdditivity.primitive_difference,
    `Imported.PregenesisEmptyMark.ListedHistorySummary,
    `Imported.GenesisPrimitives.SupplyErasure,
    `Imported.SymmetricGroupPresentations.SnCarrier,
    `Imported.SymmetricGroupPresentations.SnOffImage,
    `Imported.SymmetricGroupPresentations.SnSyntax,
    `Imported.SymmetricGroupPresentations.SnTheorems,
    `Imported.MinimalSymbolSystems.MssnObstructionDetector,
    `Imported.PfpCarriers.CarrierOrigin,
    `Imported.PfpCarriers.ThymusScreening,
    `Imported.WitnessedDifferenceProgramme.GenesisIncidence,
    `Imported.LegacyTopLevel.AntimorphicInvolution,
    `Imported.LegacyTopLevel.Demo3ProtocolInvariants,
    `Imported.LegacyTopLevel.Expressivity,
    `Imported.LegacyTopLevel.Family,
    `Imported.LegacyTopLevel.FidelityAdequacy,
    `Imported.LegacyTopLevel.GenesisBellCertificate,
    `Imported.LegacyTopLevel.GenesisContinuation,
    `Imported.LegacyTopLevel.GenesisJoint,
    `Imported.LegacyTopLevel.GenesisJointOperations,
    `Imported.LegacyTopLevel.GenesisSimulation,
    `Imported.LegacyTopLevel.GenesisTrace,
    `Imported.LegacyTopLevel.GrammarCeiling,
    `Imported.LegacyTopLevel.GrammarDepthCeiling,
    `Imported.LegacyTopLevel.LGGR1,
    `Imported.LegacyTopLevel.LGGR2,
    `Imported.LegacyTopLevel.LGGR3,
    `Imported.LegacyTopLevel.Level15AuthorityCalculus,
    `Imported.LegacyTopLevel.Level16IndObject,
    `Imported.LegacyTopLevel.Level17HodgeDecomposition,
    `Imported.LegacyTopLevel.Level18ZeroFloatLaw,
    `Imported.LegacyTopLevel.Level19IharaZetaQuarantine,
    `Imported.LegacyTopLevel.Level20AutopoieticCohomology,
    `Imported.LegacyTopLevel.Level21DiscreteRegge,
    `Imported.LegacyTopLevel.Level22FibredDependentContexts,
    `Imported.LegacyTopLevel.Level23SheafDescent,
    `Imported.LegacyTopLevel.Level80ScopedAuthorization,
    `Imported.LegacyTopLevel.Lib,
    `Imported.LegacyTopLevel.LiftPatchSemantics,
    `Imported.LegacyTopLevel.LpWeakDuality,
    `Imported.LegacyTopLevel.NormalFormsCore,
    `Imported.LegacyTopLevel.OperationTreeFold,
    `Imported.LegacyTopLevel.PrimitiveDifference,
    `Imported.LegacyTopLevel.ReportRepair,
    `Imported.LegacyTopLevel.RuntimeLimits,
    `Imported.LegacyTopLevel.SLevel,
    `Imported.LegacyTopLevel.ShadowBoundary,
    `Imported.LegacyTopLevel.ShadowFactorization,
    `Imported.LegacyTopLevel.SnPacketGame,
    `Imported.LegacyTopLevel.SnTower,
    `Imported.LegacyTopLevel.Stage0LiftNecessity,
    `Imported.LegacyTopLevel.Stage1LiftNecessity,
    `Imported.LegacyTopLevel.Sweeper,
    `Imported.LegacyTopLevel.SymbolCarrier,
    `Imported.LegacyTopLevel.TokenFrontier,
    `Imported.LegacyTopLevel.TowerLadder,
    `Imported.LegacyTopLevel.TowerZeta,
    `Imported.LegacyTopLevel.TriggerNotLicense,
    `Imported.LegacyTopLevel.TypedPacketShadow,
    `Imported.HigherCategoryTheory.Bicategory,
    `Imported.HigherCategoryTheory.Braided,
    `Imported.HigherCategoryTheory.Census,
    `Imported.HigherCategoryTheory.CoherenceTheorems,
    `Imported.HigherCategoryTheory.CompactlyGenerated,
    `Imported.HigherCategoryTheory.DGCategory,
    `Imported.HigherCategoryTheory.DendroidalSet,
    `Imported.HigherCategoryTheory.DerivedCategory,
    `Imported.HigherCategoryTheory.DoubleCategory,
    `Imported.HigherCategoryTheory.Enriched,
    `Imported.HigherCategoryTheory.HigherFunctor,
    `Imported.HigherCategoryTheory.HigherNaturalTransformation,
    `Imported.HigherCategoryTheory.Master,
    `Imported.HigherCategoryTheory.ModelCategory,
    `Imported.HigherCategoryTheory.Monoidal,
    `Imported.HigherCategoryTheory.OperadicNerve,
    `Imported.HigherCategoryTheory.Regression,
    `Imported.HigherCategoryTheory.Ribbon,
    `Imported.HigherCategoryTheory.SimplicialSet,
    `Imported.HigherCategoryTheory.StableInfinityCategory,
    `Imported.HigherCategoryTheory.Triangulated,
    `Imported.HigherCategoryTheory.TwoCategory,
    `Imported.WdpReasoning.ExecutableReasoning,
    `Imported.WdpReasoning.ReasoningAxioms,
    `Imported.WdpReasoning.RefinementAxioms,
    `Imported.WdpReasoning.WitnessedReasoning
  ]

-- Target: FSP-HUBBARD-PROTECTED-REPRESENTATIONS.
-- Not a default target: build with `lake build FermionSignHubbardProtected`.
lean_lib FermionSignHubbardProtected where
  roots := #[`FermionSignHubbardProtected]

-- Target: L1-IMP-SECTOR-SYMMETRY-LAW
-- Not a default target: build with `lake build L1SectorSymmetry`
lean_lib L1SectorSymmetry where
  roots := #[
    `L1SectorSymmetry
  ]

lean_lib FableGleasonRun2 where
  roots := #[`BornGaussianRationalFrameObstruction, `BornGaussianFrameRays]

-- FQ-GAP-BORN-UNIQUENESS-GLEASON (frame functions on all rational rays of Q^3 and the
-- residue-mod-2 class ansatz on Q(i)^3). Not a default target:
-- build with `lake build BornGleasonRays`.
lean_lib BornGleasonRays where
  roots := #[`BornRationalRayObstruction, `BornGaussianMod2ClassRigidity]

-- PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT
lean_lib PregenesisPresentationLift where
  roots := #[`PregenesisPresentationLift]

-- Target: CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT
-- Not a default target: build with `lake build ConstructorTheoryMediatorEntanglement`.
lean_lib ConstructorTheoryMediatorEntanglement where
  roots := #[
    `ConstructorTheoryMediatorEntanglement
  ]

-- (TFQ-0016): B2(Q) Semidirect Factorization, Two-Stage Dressing, Discrete Poset Curvature
lean_lib B2SemidirectDressing where
  roots := #[`B2SemidirectDressing]

-- FSP-WILSON-DIRAC-GAMMA5. Not a default target.
lean_lib FermionSignWilsonDiracGamma5 where
  roots := #[`FermionSignWilsonDiracGamma5]

-- Finite combinatorial shadow of Genesis admission. Not a default target.
lean_lib GenesisHottShadow where
  roots := #[`GenesisHottShadow]

lean_lib GenesisHottTruncation where
  roots := #[`GenesisHottTruncation]

lean_lib GenesisHottHorns where
  roots := #[`GenesisHottHorns, `GenesisHottModel]

lean_lib AdmitLang where
  roots := #[`AdmitCore, `AdmitReflect, `AdmitInterpret, `AdmitImport]

-- All finite Genesis slot contexts, beyond the unary-only mirror. Non-default.
lean_lib GenesisContextDecision where
  roots := #[`GenesisContextDecision]

-- Finite regulator obstruction; not a default target.
lean_lib FermionSignLatticeAnomalyInflow where
  roots := #[`FermionSignLatticeAnomalyInflow]

-- Operational hypotheses and exact countermodels. Not a default build target.
lean_lib TransitionProbability where
  roots := #[`TransitionProbability]

-- DFM-BPHZ-CONTINUUM-FENCE. Not a default target.
lean_lib DressingFieldBphzContinuumFence where
  roots := #[`DressingFieldBphzContinuumFence]

-- Compile the immutable, provenance-bound Genesis source through the shared cache.
lean_lib GenesisSealedSource where
  srcDir := "../atlas/papers/finite_obstruction_calculus/genesis/lean4"
  roots := #[`Derivation.Basic, `Derivation.Erasure, `Derivation.Inertia, `SecondRun.Run]
  globs := #[.submodules `Derivation, .submodules `SecondRun]

-- Exact array/copy/source partial replay transport. Non-default.
lean_lib GenesisReplayRefinement where
  roots := #[`GenesisReplayRefinement]

-- Certified carrier bridge reuses the sealed Genesis source library above.
lean_lib GenesisCarrierBridge where
  roots := #[`GenesisCarrierBridge]

-- Declared demand-policy extension. Non-default.
lean_lib GenesisDemandPolicy where
  roots := #[`GenesisDemandPolicy]

-- Supplied rooted-tree Borel dressing. Non-default.
lean_lib DressingFieldHierarchicalBorel where
  roots := #[`DressingFieldHierarchicalBorel]

-- DFM-ELECTROWEAK-CONTINUUM-FENCE. Not a default target.
lean_lib DressingFieldElectroweakContinuumFence where
  roots := #[`DressingFieldElectroweakContinuumFence]

-- Exact no-return engine replay, reusing the sealed source library.
lean_lib GenesisNoReturn where
  roots := #[`GenesisNoReturn]

-- Immutable Genesis-Ongoing dependencies; non-default source and proof targets.
lean_lib GenesisOngoingSource where
  srcDir := "../atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4"
  roots := #[`H3V7N5QF.Answers, `Second.Cost]
  globs := #[.submodules `H3V7N5QF, .submodules `Second]

lean_lib GenesisOngoingRename where
  roots := #[`GenesisOngoingRename]

lean_lib GenesisOngoingRefinement where
  roots := #[`GenesisOngoingRefinement]

-- Explicit comparison classes, reusing the sealed source library above.
lean_lib GenesisProcessComparison where
  roots := #[`GenesisProcessComparison]

-- DFM-CKM-PHYSICS-FENCE. Not a default target.
lean_lib DressingFieldCkmPhysicsFence where
  roots := #[`DressingFieldCkmPhysicsFence]

-- Target: DFM-CONTINUUM-INTERFACE.
-- Not a default target: build with `lake build DressingFieldContinuumInterface`.
lean_lib DressingFieldContinuumInterface where
  roots := #[`DressingFieldContinuumInterface]

-- FSP-U1-WILSON-ACTION. Not a default target.
lean_lib FermionSignU1WilsonAction where
  roots := #[`FermionSignU1WilsonAction]


-- DFM-GRIBOV-CONTINUUM-FENCE. Not a default target.
lean_lib DressingFieldGribovContinuumFence where
  roots := #[`DressingFieldGribovContinuumFence]

-- DFM-SYMANZIK-QED-AE-FENCE. Not a default target.
lean_lib DressingFieldSymanzikQedAeFence where
  roots := #[`DressingFieldSymanzikQedAeFence]

-- DFM-REGGE-GRAVITY-FENCE. Not a default target.
lean_lib DressingFieldReggeGravityFence where
  roots := #[`DressingFieldReggeGravityFence]

lean_lib DressingFieldRelationalTimeFence where
  roots := #[`DressingFieldRelationalTimeFence]

-- DFM-Z1-Z2-COUNTERTERM-FENCE. Not a default target.
lean_lib DressingFieldZ1Z2CountertermFence where
  roots := #[`DressingFieldZ1Z2CountertermFence]

-- PGW-SN-E08-WEIGHTED-L1-DUALITY. Not a default target.
lean_lib WeightedL1Duality where
  roots := #[`WeightedL1Duality]

-- PGW-SN-PROTECTED-ANSWER-TRANSPORT. Not a default target.
lean_lib ProtectedAnswerTransport where
  roots := #[`ProtectedAnswerTransport]

-- FSP-SU2-ADJOINT-REAL-DET. Not a default target.
lean_lib FermionSignSu2AdjointRealDet where
  roots := #[`FermionSignSu2AdjointRealDet]

-- FSP-QCD-CHEMICAL-POTENTIAL-DET. Not a default target.
lean_lib FermionSignQcdChemicalPotentialDet where
  roots := #[`FermionSignQcdChemicalPotentialDet]

-- FSP-LATTICE-WESS-ZUMINO-SUSY. Not a default target.
lean_lib FermionSignLatticeWessZuminoSusy where
  roots := #[`FermionSignLatticeWessZuminoSusy]

-- ADS-CFT-DUALITY-IMPORT. Not a default target.
lean_lib AdsCftDualityImport where
  roots := #[`AdsCftDualityImport]

-- ADS-HAPPY-TOY-NOT-DUALITY-GAP. Not a default target.
lean_lib AdsHappyToyNotDualityGap where
  roots := #[`AdsHappyToyNotDualityGap]

-- FSP-IMAGINARY-MU-REAL-DET. Non-default.
lean_lib FermionSignImaginaryMuRealDet where
  roots := #[`FermionSignImaginaryMuRealDet]

-- TFQ-0008. Not a default target.
lean_lib PathSumCayleyEulerStep where
  roots := #[`PathSumCayleyEulerStep]

-- CQFT-LOCAL-NET-AXIOMS-IMPORT. Not a default target.
lean_lib LocalNetAxiomsImport where
  roots := #[`LocalNetAxiomsImport]

-- LQG-EPRL-VERTEX-IMPORT. Not a default target.
lean_lib LqgEprlVertexImport where
  roots := #[`LqgEprlVertexImport]

-- LQG-CONTINUUM-LIMIT-GAP. Not a default target.
lean_lib LqgContinuumLimitGap where
  roots := #[`LqgContinuumLimitGap]

-- ADS-RT-FORMULA-IMPORT. Not a default target.
lean_lib AdsRtFormulaImport where
  roots := #[`AdsRtFormulaImport]

-- ADS-REGGE-AREA-RT-GAP. Not a default target.
lean_lib AdsReggeAreaRtGap where
  roots := #[`AdsReggeAreaRtGap]

-- CQFT-CAUSAL-FACTORIZATION-IMPORT. Not a default target.
lean_lib CausalFactorizationImport where
  roots := #[`CausalFactorizationImport]

-- CQFT-REEH-SCHLIEDER-THEOREM-IMPORT. Not a default target.
lean_lib ReehSchliederImport where
  roots := #[`ReehSchliederImport]

-- TFQ-0106. Not a default target.
lean_lib CosmologicalCouplingReplay where
  roots := #[`CosmologicalCouplingReplay]

-- TFQ-0090. Not a default target.
lean_lib CochainCurvatureReggeDeficit where
  roots := #[`CochainCurvatureReggeDeficit]

-- TFQ-0107. Not a default target.
lean_lib FieldEquationConstraintReplay where
  roots := #[`FieldEquationConstraintReplay]

-- TFQ-0118. Not a default target.
lean_lib CyclicInclusionCharacterSums where
  roots := #[`CyclicInclusionCharacterSums]

-- TFQ-0119. Not a default target.
lean_lib DyadicDirectLimitCircle where
  roots := #[`DyadicDirectLimitCircle]

-- TFQ-0123. Not a default target.
lean_lib LossLedgerAssociativity where
  roots := #[`LossLedgerAssociativity]

-- PG-WDP-GENESIS-BRIDGE-OBLIGATIONS. Not a default target.
lean_lib PregenesisWdpBridgeObligations where
  roots := #[`PregenesisWdpBridgeObligations]

lean_lib GaussianMatrixRecoveryLift where
  roots := #[`GaussianMatrixRecoveryLift]

lean_lib FiniteDynamicsInstrumentsPathSums where
  roots := #[`FiniteDynamicsInstrumentsPathSums]

lean_lib FiniteGaugeCochainHolonomy where
  roots := #[`FiniteGaugeCochainHolonomy]

lean_lib FiniteQedElectroweakShadow where
  roots := #[`FiniteQedElectroweakShadow]

lean_lib FiniteQcdColorWilsonLoops where
  roots := #[`FiniteQcdColorWilsonLoops]

lean_lib QuaternionQ8GaugeShadow where
  roots := #[`QuaternionQ8GaugeShadow]

lean_lib FiniteGroupoidConvolutionAlgebra where
  roots := #[`FiniteGroupoidConvolutionAlgebra]

lean_lib QuaternionQ8InSU2 where
  roots := #[`QuaternionQ8InSU2]

lean_lib LatticeDiracDoubling where
  roots := #[`LatticeDiracDoubling]

lean_lib WilsonSpeciesCount where
  roots := #[`WilsonSpeciesCount]

lean_lib MesonColorChannels where
  roots := #[`MesonColorChannels]

lean_lib DiquarkAntitripletChannel where
  roots := #[`DiquarkAntitripletChannel]

lean_lib ConfK5TorsionReadings where
  roots := #[`ConfK5TorsionReadings]

lean_lib ContinuumVolumeInterfaceInventory where
  roots := #[`ContinuumVolumeInterfaceInventory]

lean_lib ColorTwinCoverage where
  roots := #[`ColorTwinCoverage]

lean_lib Su3GribovDiamond where
  roots := #[`Su3GribovDiamond]

lean_lib AnyonRibbonRacahGauge where
  roots := #[`AnyonRibbonRacahGauge]

lean_lib RibbonCategoryCatalog where
  roots := #[`RibbonCategoryCatalog]

lean_lib BooleanValuationVsSimplex where
  roots := #[`BooleanValuationVsSimplex]

lean_lib TetronGf2Homology where
  roots := #[`TetronGf2Homology]

lean_lib MajoranaEvaluatorControls where
  roots := #[`MajoranaEvaluatorControls]

lean_lib IntervalMeasurementEvidence where
  roots := #[`IntervalMeasurementEvidence]

lean_lib GravityProxyVsReggeSum where
  roots := #[`GravityProxyVsReggeSum]

lean_lib PregenesisLiftChecklist where
  roots := #[`PregenesisLiftChecklist]

-- PGW-PYTHON-LEAN-CARRIER-BRIDGE. Not a default target.
lean_lib PregenesisPythonLeanCarrierBridge where
  roots := #[`PregenesisPythonLeanCarrierBridge]

-- L1-QM020-THM2B-MINKOWSKI. Not a default target.
lean_lib L1MinkowskiSquareExpansion where
  roots := #[`L1MinkowskiSquareExpansion]

-- PGW-CONTEXT-FIDELITY. Not a default target.
lean_lib PregenesisContextFidelity where
  roots := #[`PregenesisContextFidelity]

-- TFQ-0003. Not a default target.
lean_lib FiniteObstructionTwoComplexes where
  roots := #[`FiniteObstructionTwoComplexes]

-- TFQ-0313. Not a default target.
lean_lib Z4ModuleOperatorAlgebra where
  roots := #[`Z4ModuleOperatorAlgebra]

-- TFQ-0319. Not a default target.
lean_lib TwoMarkCoboundary where
  roots := #[`TwoMarkCoboundary]

-- OPS-RUST-RECEIPTS-AND-LIMITS. Not a default target.
lean_lib ObserverPresheafReceiptLimits where
  roots := #[`ObserverPresheafReceiptLimits]

-- TFQ-0374. Not a default target.
lean_lib FreshLetterRecoveryContracts where
  roots := #[`FreshLetterRecoveryContracts]

-- TFQ-0385. Not a default target.
lean_lib UniformRuleErasesSeparation where
  roots := #[`UniformRuleErasesSeparation]

-- PGW-K-ITEM-DELTA-GRAMMAR. Not a default target.
lean_lib PregenesisKItemDeltaGrammar where
  roots := #[`PregenesisKItemDeltaGrammar]

-- PGW-DECLARED-INPUT-FLOOR. Not a default target.
lean_lib PregenesisDeclaredInputFloor where
  roots := #[`PregenesisDeclaredInputFloor]

-- PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN. Not a default target.
lean_lib PregenesisIsomorphismSoundness where
  roots := #[`PregenesisIsomorphismSoundness]

-- PGW-RUNS-PAST-DECLARED-BOUNDS. Not a default target.
lean_lib PregenesisRunsPastDeclaredBounds where
  roots := #[`PregenesisRunsPastDeclaredBounds]

-- PGW-STREAM-AT-FOUR-ITEMS. Not a default target.
lean_lib PregenesisStreamAtFourItems where
  roots := #[`PregenesisStreamAtFourItems]

-- PGW-DRIVER-B-SEVENTH-EVENT. Not a default target.
lean_lib PregenesisDriverBSeventhEvent where
  roots := #[`PregenesisDriverBSeventhEvent]

-- PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT. Not a default target.
lean_lib PregenesisWdpIncidenceTransport where
  roots := #[`PregenesisWdpIncidenceTransport]

-- PGW-WDP-BRIDGE-ONGOING-TO-WINDOW. Not a default target.
lean_lib PregenesisWdpBridgeOngoing where
  roots := #[`PregenesisWdpBridgeOngoing]

-- PGW-WDP-HANDOFF-TO-L1. Not a default target.
lean_lib PregenesisWdpHandoffToL1 where
  roots := #[`PregenesisWdpHandoffToL1]

-- MUB-PRIME-POWER-CONSTRUCTION. Not a default target.
lean_lib MubPrimePowerConstruction where
  roots := #[`MubPrimePowerConstruction]


-- MUB-PRIME-POWER-CONSTRUCTION (odd characteristic). Not a default target:
-- build with `lake build MubPrimePowerOdd`.
lean_lib MubPrimePowerOdd where
  roots := #[`MubPrimePowerOddCharacteristic]

-- MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE. Not a default target.
lean_lib MajoranaOpenLindbladTransferEnvelope where
  roots := #[`MajoranaOpenLindbladTransferEnvelope]

-- MAJ-OPEN-EVIDENCE-ADEQUACY. Not a default target.
lean_lib MajoranaOpenEvidenceAdequacy where
  roots := #[`MajoranaOpenEvidenceAdequacy]

-- GTH-SHADOW. Not a default target.
lean_lib GenesisToHigherShadow where
  roots := #[`GenesisToHigherShadow]

-- GTH-LANG-CORE. Not a default target.
lean_lib GenesisToHigherLangCore where
  roots := #[`GenesisToHigherLangCore]

-- L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED. Not a default target.
lean_lib L1ResidualSectorWeights where
  roots := #[`L1ResidualSectorWeights]

-- FQ-PRIM-TO-QM-SELECTION-OPEN. Not a default target.
lean_lib PrimToQmSelection where
  roots := #[`PrimToQmSelection]

-- FQ-GAP-U1-CIRCLE. Not a default target.
lean_lib U1CircleIntegerWitness where
  roots := #[`U1CircleIntegerWitness]

-- COMP-C2-STEP3-NOT-WORD-STEP. Not a default target.
lean_lib ComputationC2Step3NotWordStep where
  roots := #[`ComputationC2Step3NotWordStep]

-- COMP-C6-TM0-OUTPUT-FORM-OPEN. Not a default target.
lean_lib ComputationC6Tm0OutputFormOpen where
  roots := #[`ComputationC6Tm0OutputFormOpen]

-- COMP-C7-FIXED-TARGET-OPEN. Not a default target.
lean_lib ComputationC7FixedTargetOpen where
  roots := #[`ComputationC7FixedTargetOpen]

-- COMP-C8-MINIMALITY-FENCE. Not a default target.
lean_lib ComputationC8MinimalityFence where
  roots := #[`ComputationC8MinimalityFence]

-- AUTH-DTM2-INPUT-REQUEST-PLANNED. Not a default target.
lean_lib ComputabilityDtm2InputRequestPlanned where
  roots := #[`ComputabilityDtm2InputRequestPlanned]

-- AUTHF-CARRIER-ADMISSION-GATE. Not a default target.
lean_lib CarrierAdmissionGate where
  roots := #[`CarrierAdmissionGate]

-- FQ-GAP-STONE-CONTINUOUS-TIME. Not a default target.
lean_lib StoneContinuousTimeIntegerSlice where
  roots := #[`StoneContinuousTimeIntegerSlice]

-- FQ-GAP-CONTINUUM-HILBERT-LIFT. Not a default target.
lean_lib ContinuumHilbertLiftIntegerSlice where
  roots := #[`ContinuumHilbertLiftIntegerSlice]

-- FSP-WITTEN-INDEX-INVARIANCE. Not a default target.
lean_lib WittenPairing where
  roots := #[`WittenPairing]

-- PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY. Not a default target.
lean_lib PregenesisWdpPhiWellDefinedL1Duality where
  roots := #[`PregenesisWdpPhiWellDefinedL1Duality]

-- FSP-KITAEV-HONEYCOMB-SOLUTION. Not a default target.
lean_lib KitaevSectorBlock where
  roots := #[`KitaevSectorBlock]

-- FSP-LAUGHLIN-EXCHANGE-PHASE. Not a default target.
lean_lib LaughlinRootAmbiguity where
  roots := #[`LaughlinRootAmbiguity]

-- PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER. Not a default target.
lean_lib ReportFiberDescent where
  roots := #[`ReportFiberDescent]

-- CT-INFORMATION-MEDIA-INTEROPERABILITY. Not a default target.
lean_lib InformationProductBoundary where
  roots := #[`InformationProductBoundary]

-- MAJ-LEGACY-CARRIER-RETRACTION. Not a default target.
lean_lib MajoranaLegacyCarrierRetraction where
  roots := #[`MajoranaLegacyCarrierRetraction]

-- COMP-C3-NO-FIXED-BOUND. Not a default target.
lean_lib ComputationC3NoFixedBound where
  roots := #[`ComputationC3NoFixedBound]

-- COMP-C7-ENCODED-INSTANCE-REDUCTION. Not a default target.
lean_lib ComputationC7EncodedInstanceReduction where
  roots := #[`ComputationC7EncodedInstanceReduction]

-- QCV-CONDITIONAL-VIABILITY-CERTIFICATE. Not a default target.
lean_lib NoisyComputationViabilityCertificate where
  roots := #[`NoisyComputationViabilityCertificate]

-- OPS-OBSERVER-DECLARATION-REFUSAL. Not a default target.
lean_lib ObserverDeclarationRefusal where
  roots := #[`ObserverDeclarationRefusal]

-- OPS-AXIS3-RELABELING. Not a default target.
lean_lib ObserverPresheafAxis3Relabeling where
  roots := #[`ObserverPresheafAxis3Relabeling]

-- GP-IMPORT-COMPLEX-FIELD. Not a default target.
lean_lib ComplexFieldImport where
  roots := #[`ComplexFieldImport]

-- GP-IMPORT-CIRCLE-U1. Not a default target.
lean_lib CircleU1Import where
  roots := #[`CircleU1Import]

-- FQ-GAP-CUSTODY-AND-RECEIPTS. Not a default target.
lean_lib CustodyReceiptNumerals where
  roots := #[`CustodyReceiptNumerals]

lean_lib OriginalTargetNumerals where
  roots := #[`OriginalTargetNumerals]

lean_lib GleasonImport where
  roots := #[`GleasonImport]

lean_lib BfCocycleObstruction where
  roots := #[`BfCocycleObstruction]

lean_lib SignedTriangleSwitching where
  roots := #[`SignedTriangleSwitching]

lean_lib IdentityConvention where
  roots := #[`IdentityConvention]

lean_lib ReggeFiniteAction where
  roots := #[`ReggeFiniteAction]

lean_lib ConstraintKernelProjector where
  roots := #[`ConstraintKernelProjector]

lean_lib MajoranaCosetWeightImport where
  roots := #[`MajoranaCosetWeightImport]

lean_lib TensorProductImport where
  roots := #[`TensorProductImport]

lean_lib CptpClassImport where
  roots := #[`CptpClassImport]

lean_lib ContinuousTimeImport where
  roots := #[`ContinuousTimeImport]

lean_lib ContinuumHilbertImport where
  roots := #[`ContinuumHilbertImport]

lean_lib ContinuousTimeExpGenerator where
  roots := #[`ContinuousTimeExpGenerator]

lean_lib DecoherenceFunctionalGram where
  roots := #[`DecoherenceFunctionalGram]

lean_lib U1ResiduesOrderFour where
  roots := #[`U1ResiduesOrderFour]

lean_lib CptpCompletePositivity where
  roots := #[`CptpCompletePositivity]

lean_lib BornUniquenessIntegerSlice where
  roots := #[`BornUniquenessIntegerSlice]

lean_lib KitaevChainImport where
  roots := #[`KitaevChainImport]

lean_lib FermionSignThetaTermComplexWeight where
  roots := #[`FermionSignThetaTermComplexWeight]

lean_lib Mub6WeylHeisenbergD6 where
  roots := #[`Mub6WeylHeisenbergD6]

lean_lib Mub6FiniteCornerReduction where
  roots := #[`Mub6FiniteCornerReduction]

lean_lib ThresholdTheoremImport where
  roots := #[`ThresholdTheoremImport]

lean_lib NoisyReversibleLimitsImport where
  roots := #[`NoisyReversibleLimitsImport]

lean_lib ComputabilityRiceTheoremImport where
  roots := #[`ComputabilityRiceTheoremImport]

lean_lib ObserverPresheafAxis1WellfoundedAdmission where
  roots := #[`ObserverPresheafAxis1WellfoundedAdmission]

lean_lib TetronFourModeCounts where
  roots := #[`TetronFourModeCounts]

/-- Untwisted finite-group 4D Pachner invariance; independent non-default target. -/
lean_lib «FiniteGroupPachner» where
  srcDir := "."
  roots := #[`FiniteGroupPachner]

-- Conditional continuum interface: DFM-CONTINUUM-INTERFACE. Non-default target.
lean_lib DressingFieldRefinementLimit where
  roots := #[`DressingFieldRefinementLimit]

-- Reviewed module; non-default target.
lean_lib LqgProjectiveLimit where
  roots := #[`LqgProjectiveLimit]

-- Reviewed module; non-default target.
lean_lib L1U1SelectorOtherSegment where
  roots := #[`L1U1SelectorOtherSegment]

-- Reviewed module; non-default target.
lean_lib ObserverPresheafLeanGap where
  roots := #[`ObserverPresheafLeanGap]

-- Reviewed module; non-default target.
lean_lib L1OrthogonalAdditivity where
  roots := #[`L1OrthogonalAdditivity]

-- Reviewed module; non-default target.
lean_lib TensorUniquenessOuterProducts where
  roots := #[`TensorUniquenessOuterProducts]

-- TFQ-0171 finite positive-mass separation. Not a default target.
lean_lib PositivePairMass where
  roots := #[`PositivePairMass]

-- TFQ-0184 cubic count. Non-default target.
lean_lib CubicReflexivityCount where
  roots := #[`CubicReflexivityCount]

-- L1-GS001-GAUGE-L1. Not a default target.
lean_lib L1SignedPermutationGauge where
  roots := #[`L1SignedPermutationGauge]

-- L1-WDP-CH08-C01-REPLICA-L1 scale count. Non-default target.
lean_lib L1ReplicaScale where
  roots := #[`L1ReplicaScale]

-- FSP-MAJORANA-CLIFFORD-PARITY. Not a default target.
lean_lib MajoranaCliffordParity where
  roots := #[`MajoranaCliffordParity]
