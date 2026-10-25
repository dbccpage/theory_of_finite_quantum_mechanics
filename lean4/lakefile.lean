
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
    `H001ProbabilitySimplex,
    `H001Rats,
    `H003ReversibilityGate,
    `H004FreeLinearization,
    `H005InnerProductAdmission,
    `H006Envelope,
    `H006PermutationUnitary,
    `H007Complexification,
    `H008PhaseBlindPresentation,
    `H009PhaseFiber,
    `H010Hadamard,
    `H010InterferenceNonDescent,
    `H010Scale,
    `H011Circle,
    `H011U1SelectorBoundary,
    `H012OperatorAlgebraShadow,
    `H013BornPairingBoundary,
    `H013FrameAdditivity,
    `H013QuarticRivalSeparation,
    `H013SameContract,
    `H014BilinearProduct,
    `H014Interface,
    `H014TensorCompositionBoundary,
    `H015CollapseDilations,
    `H015DilationCount,
    `H015IrreversibleFork,
    `H016ContinuousDynamicsFork,
    `H017Extras,
    `H017FiniteHilbertBoundary,
    `H017ExtrasDropone,
    `H017Fin,
    `H017Finish,
    `H017Gleason,
    `H017MatrixFiniteRecovery,
    `H018Channel,
    `H018Density,
    `H019RationalLieSpan,
    `H020CabelloSignPolytope,
    `H021TriangleNetworkComplexCarrier,
    `H022SimplicialAreaLawPageCurve,
    `H023DiscreteSpinfoamAmplitudes,
    `H024FourSimplexSpinfoamS4,
    `H025SpinfoamBoundaryUnitarity,
    `H026MasterConstraintSpinfoamKernel,
    `H027PachnerMasterConstraintFiniteness,
    `H028ArbitraryDegreePolynomialReduction,
    `H029Simplicial3complexCayleyEvolution,
    `H030OctahedralMubCliftonKent,
    `H031OctahedralDepolarizingThreshold,
    `H032DiscretePythagoreanBellChsh,
    `H033PythagoreanPellTsirelsonConvergence,
    `H034CliffordPauliConjugationAndTGateOrbit,
    `H035DiscreteWignerNegativityResource,
    `H036ThreeQubitCodeSyndromeRecovery,
    `H037FourQubitCssSurfaceCode,
    `H038SteaneFanoCodeTransversalGates,
    `H039DiscreteQuantumTeleportation,
    `H040DiscreteSuperdenseCoding,
    `H041PrimePWignerPhaseSpace,
    `H042ShorNineQubitCode,
    `H043DiscretePhaseEstimation,
    `H044SurfaceCodeToricTopology,
    `H045DiscreteGroverSearch,
    `H046DiscreteCliffordSymplectic,
    `H047StoneVonNeumannObstruction,
    `H048RichardsonErrorMitigation,
    `H049QuantumWalkSymmetricCayley,
    `H050MubTomographyInversion,
    `H051Mub4GaloisFieldContextuality,
    `H052CyclotomicTowerDirected,
    `H053EverettForkingTree,
    `H054GleasonCyclotomicObstruction,
    `H055DiscreteDynamicsStone,
    `H056ContinuumLiftBoundary,
    `H057HigherDimConductorBounds,
    `H058EffectFrameBusch,
    `H059RationalSector,
    `H060EmbeddingRelativity,
    `H061DynamicsDichotomy,
    `H062CompositionTensorMub,
    `H063CptpChannelsStinespring,
    `H064ContextualityThresholds,
    `H065CancellationCertificates,
    `H066GrowthRefinement,
    `H067TerminalPriceList,
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
    `H068WeylCcrResidual,
    `H069NormApproximationFrontier,
    `H070HeisenbergRepresentationUniqueness,
    `H071RefinementSubsystemTower,
    `H072TowerTopologicalCompletion,
    `H073ContinuousTimeLocalityLimit,
    `H074OperationalAxiomSelection,
    `H075TensorCommutingCorrelationFrontier,
    `H076LatticeGaugeManybodyBenchmark,
    `H077FiniteOperationalClosureContract,
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
    `H000FinitePresentedCarrier,
    `H002ReportDynamics,
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
    `E003_projection_fiber_primitive_difference,
    `E005_fiber_quotient_equivalence,
    `E008_projection_escape_residual,
    `E009_literal_invariance,
    `E011_fiber_dynamics_congruence,
    `E012_unique_descended_dynamics,
    `E013_selected_projected_map,
    `E018_descent_failure_without_escape,
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
-- or one module at a time, e.g. `lake build Imported.Genesis19l57g1.Derivation.Inertia`.
lean_lib ImportedAtlas where
  roots := #[
    `Imported.Genesis19l57g1.CanonicalMinimizer,
    `Imported.Genesis19l57g1.Derivation,
    `Imported.Genesis19l57g1.Derivation.Apartness,
    `Imported.Genesis19l57g1.Derivation.Attachment,
    `Imported.Genesis19l57g1.Derivation.Basic,
    `Imported.Genesis19l57g1.Derivation.BoundaryCancellation,
    `Imported.Genesis19l57g1.Derivation.Breaking,
    `Imported.Genesis19l57g1.Derivation.Bridge,
    `Imported.Genesis19l57g1.Derivation.CapacityBound,
    `Imported.Genesis19l57g1.Derivation.ClosureSymmetry,
    `Imported.Genesis19l57g1.Derivation.Completion,
    `Imported.Genesis19l57g1.Derivation.Compression,
    `Imported.Genesis19l57g1.Derivation.Constitution,
    `Imported.Genesis19l57g1.Derivation.ContactBridge,
    `Imported.Genesis19l57g1.Derivation.ContactKernel,
    `Imported.Genesis19l57g1.Derivation.ControllerCategory,
    `Imported.Genesis19l57g1.Derivation.CountTransport,
    `Imported.Genesis19l57g1.Derivation.Counting,
    `Imported.Genesis19l57g1.Derivation.DiffInterface,
    `Imported.Genesis19l57g1.Derivation.EndogenousFidelityGenerator,
    `Imported.Genesis19l57g1.Derivation.Erasure,
    `Imported.Genesis19l57g1.Derivation.Ext,
    `Imported.Genesis19l57g1.Derivation.FidelityClosure,
    `Imported.Genesis19l57g1.Derivation.FormRenaming,
    `Imported.Genesis19l57g1.Derivation.FormTransport,
    `Imported.Genesis19l57g1.Derivation.G1Class,
    `Imported.Genesis19l57g1.Derivation.Generator,
    `Imported.Genesis19l57g1.Derivation.GraphGenesis,
    `Imported.Genesis19l57g1.Derivation.HigherStructure,
    `Imported.Genesis19l57g1.Derivation.Horizon,
    `Imported.Genesis19l57g1.Derivation.Inertia,
    `Imported.Genesis19l57g1.Derivation.Initiality,
    `Imported.Genesis19l57g1.Derivation.InterpreterBoundary,
    `Imported.Genesis19l57g1.Derivation.IsoCanon,
    `Imported.Genesis19l57g1.Derivation.IsoCollapse,
    `Imported.Genesis19l57g1.Derivation.LadderGeneral,
    `Imported.Genesis19l57g1.Derivation.LocalStrategy,
    `Imported.Genesis19l57g1.Derivation.Mention,
    `Imported.Genesis19l57g1.Derivation.Minimality,
    `Imported.Genesis19l57g1.Derivation.MinimalityF,
    `Imported.Genesis19l57g1.Derivation.NoOutside,
    `Imported.Genesis19l57g1.Derivation.NoOutsideFidelity,
    `Imported.Genesis19l57g1.Derivation.ObsDescent,
    `Imported.Genesis19l57g1.Derivation.ObserverInventory,
    `Imported.Genesis19l57g1.Derivation.Pigeonhole,
    `Imported.Genesis19l57g1.Derivation.PresentationDescent,
    `Imported.Genesis19l57g1.Derivation.PresentationNaturality,
    `Imported.Genesis19l57g1.Derivation.PresentationRelativity,
    `Imported.Genesis19l57g1.Derivation.PrimDiff,
    `Imported.Genesis19l57g1.Derivation.PrimitiveCats,
    `Imported.Genesis19l57g1.Derivation.PrimitiveContact,
    `Imported.Genesis19l57g1.Derivation.PrimitiveCore,
    `Imported.Genesis19l57g1.Derivation.PrimitivePassage,
    `Imported.Genesis19l57g1.Derivation.Progress,
    `Imported.Genesis19l57g1.Derivation.Quot,
    `Imported.Genesis19l57g1.Derivation.QuotientRetention,
    `Imported.Genesis19l57g1.Derivation.Refusal,
    `Imported.Genesis19l57g1.Derivation.RefusalFrontier,
    `Imported.Genesis19l57g1.Derivation.RenamingStructure,
    `Imported.Genesis19l57g1.Derivation.Represented,
    `Imported.Genesis19l57g1.Derivation.ResidualClosure,
    `Imported.Genesis19l57g1.Derivation.Rounds,
    `Imported.Genesis19l57g1.Derivation.RuleBridge,
    `Imported.Genesis19l57g1.Derivation.SeparationCapacity,
    `Imported.Genesis19l57g1.Derivation.StableContent,
    `Imported.Genesis19l57g1.Derivation.TraceAlgebra,
    `Imported.Genesis19l57g1.Derivation.TransitionAlphabet,
    `Imported.Genesis19l57g1.Derivation.TransitionTransport,
    `Imported.Genesis19l57g1.Derivation.WeightProfile,
    `Imported.Genesis19l57g1.Paper,
    `Imported.Genesis19l57g1.Paper000,
    `Imported.Genesis19l57g1.PaperCanonical,
    `Imported.Genesis19l57g1.PaperOrbit,
    `Imported.Genesis19l57g1.PaperSearch,
    `Imported.Genesis19l57g1.PaperWire,
    `Imported.Genesis19l57g1.Permutation,
    `Imported.Genesis19l57g1.RegimeAction,
    `Imported.Genesis19l57g1.SecondRun,
    `Imported.Genesis19l57g1.SecondRun.Kernel,
    `Imported.Genesis19l57g1.SecondRun.Run,
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
    `Imported.AnomalonBoundary.OntologyBasic,
    `Imported.CoordinateWiseAdditivity.gs003_coordinate_l1,
    `Imported.CoordinateWiseAdditivity.primitive_difference,
    `Imported.OePregen.ListedHistorySummary,
    `Imported.OeGenPrimitives.SupplyErasure,
    `Imported.OeSn.SnCarrier,
    `Imported.OeSn.SnOffImage,
    `Imported.OeSn.SnSyntax,
    `Imported.OeSn.SnTheorems,
    `Imported.OeMssn.MssnObstructionDetector,
    `Imported.OePfp.CarrierOrigin,
    `Imported.OePfp.ThymusScreening,
    `Imported.OeWdp.GenesisIncidence,
    `Imported.SymbolGameLoose.AntimorphicInvolution,
    `Imported.SymbolGameLoose.Demo3ProtocolInvariants,
    `Imported.SymbolGameLoose.Expressivity,
    `Imported.SymbolGameLoose.Family,
    `Imported.SymbolGameLoose.FidelityAdequacy,
    `Imported.SymbolGameLoose.GenesisBellCertificate,
    `Imported.SymbolGameLoose.GenesisContinuation,
    `Imported.SymbolGameLoose.GenesisJoint,
    `Imported.SymbolGameLoose.GenesisJointOperations,
    `Imported.SymbolGameLoose.GenesisSimulation,
    `Imported.SymbolGameLoose.GenesisTrace,
    `Imported.SymbolGameLoose.GrammarCeiling,
    `Imported.SymbolGameLoose.GrammarDepthCeiling,
    `Imported.SymbolGameLoose.LGGR1,
    `Imported.SymbolGameLoose.LGGR2,
    `Imported.SymbolGameLoose.LGGR3,
    `Imported.SymbolGameLoose.Level15AuthorityCalculus,
    `Imported.SymbolGameLoose.Level16IndObject,
    `Imported.SymbolGameLoose.Level17HodgeDecomposition,
    `Imported.SymbolGameLoose.Level18ZeroFloatLaw,
    `Imported.SymbolGameLoose.Level19IharaZetaQuarantine,
    `Imported.SymbolGameLoose.Level20AutopoieticCohomology,
    `Imported.SymbolGameLoose.Level21DiscreteRegge,
    `Imported.SymbolGameLoose.Level22FibredDependentContexts,
    `Imported.SymbolGameLoose.Level23SheafDescent,
    `Imported.SymbolGameLoose.Level80ScopedAuthorization,
    `Imported.SymbolGameLoose.Lib,
    `Imported.SymbolGameLoose.LiftPatchSemantics,
    `Imported.SymbolGameLoose.LpWeakDuality,
    `Imported.SymbolGameLoose.NormalFormsCore,
    `Imported.SymbolGameLoose.OperationTreeFold,
    `Imported.SymbolGameLoose.PrimitiveDifference,
    `Imported.SymbolGameLoose.ReportRepair,
    `Imported.SymbolGameLoose.RuntimeLimits,
    `Imported.SymbolGameLoose.SLevel,
    `Imported.SymbolGameLoose.ShadowBoundary,
    `Imported.SymbolGameLoose.ShadowFactorization,
    `Imported.SymbolGameLoose.SnSymbolGameAndPackets,
    `Imported.SymbolGameLoose.SnTower,
    `Imported.SymbolGameLoose.Stage0LiftNecessity,
    `Imported.SymbolGameLoose.Stage1LiftNecessity,
    `Imported.SymbolGameLoose.Sweeper,
    `Imported.SymbolGameLoose.SymbolGame,
    `Imported.SymbolGameLoose.TokenFrontier,
    `Imported.SymbolGameLoose.TowerLadder,
    `Imported.SymbolGameLoose.TowerZeta,
    `Imported.SymbolGameLoose.TriggerNotLicense,
    `Imported.SymbolGameLoose.TypedPacketShadow,
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

-- Campaign target: FSP-HUBBARD-PROTECTED-REPRESENTATIONS.
-- Not a default target: build with `lake build CampaignFspHubbardProtected`.
lean_lib CampaignFspHubbardProtected where
  roots := #[`CampaignFspHubbardProtected]

-- Campaign target 1: L1-IMP-SECTOR-SYMMETRY-LAW
-- Not a default target: build with `lake build CampaignL1SectorSymmetry`
lean_lib CampaignL1SectorSymmetry where
  roots := #[
    `CampaignL1SectorSymmetry
  ]

lean_lib FableGleasonRun2 where
  roots := #[`BornGaussianRationalFrameObstruction, `BornGaussianFrameRays]

-- Derivation Campaign: PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT
lean_lib CampaignPgwPresentationLift where
  roots := #[`CampaignPgwPresentationLift]

-- Campaign Target 3: CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT
-- Not a default target: build with `lake build CampaignCtMediatorEntanglement`.
lean_lib CampaignCtMediatorEntanglement where
  roots := #[
    `CampaignCtMediatorEntanglement
  ]

-- Derivation Campaign Target 5 (TFQ-0016): B2(Q) Semidirect Factorization, Two-Stage Dressing, Discrete Poset Curvature
lean_lib CampaignTfq0016B2Dressing where
  roots := #[`CampaignTfq0016B2Dressing]

-- Campaign: FSP-WILSON-DIRAC-GAMMA5. Not a default target.
lean_lib CampaignFspWilsonDiracGamma5 where
  roots := #[`CampaignFspWilsonDiracGamma5]

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
lean_lib CampaignGenesisContextDecision where
  roots := #[`CampaignGenesisContextDecision]

-- Finite regulator obstruction; not a default target.
lean_lib CampaignFspLatticeAnomalyInflow where
  roots := #[`CampaignFspLatticeAnomalyInflow]

-- Operational hypotheses and exact countermodels. Not a default build target.
lean_lib CampaignTransitionProbability where
  roots := #[`CampaignTransitionProbability]

-- Campaign: DFM-BPHZ-CONTINUUM-FENCE. Not a default target.
lean_lib CampaignDfmBphzContinuumFence where
  roots := #[`CampaignDfmBphzContinuumFence]

-- Compile the immutable, provenance-bound Genesis source through the shared cache.
lean_lib CampaignGenesisSealedSource where
  srcDir := "../atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4"
  roots := #[`Derivation.Basic, `Derivation.Erasure, `Derivation.Inertia, `SecondRun.Run]
  globs := #[.submodules `Derivation, .submodules `SecondRun]

-- Exact array/copy/source partial replay transport. Non-default.
lean_lib CampaignGenesisReplayRefinement where
  roots := #[`CampaignGenesisReplayRefinement]

-- Certified carrier bridge reuses the sealed Genesis source library above.
lean_lib CampaignGenesisCarrierBridge where
  roots := #[`CampaignGenesisCarrierBridge]

-- Declared demand-policy extension. Non-default.
lean_lib CampaignGenesisDemandPolicy where
  roots := #[`CampaignGenesisDemandPolicy]

-- Supplied rooted-tree Borel dressing. Non-default.
lean_lib CampaignDfmHierarchicalBorel where
  roots := #[`CampaignDfmHierarchicalBorel]

-- Campaign: DFM-ELECTROWEAK-CONTINUUM-FENCE. Not a default target.
lean_lib CampaignDfmElectroweakContinuumFence where
  roots := #[`CampaignDfmElectroweakContinuumFence]

-- Exact no-return engine replay, reusing the sealed source library.
lean_lib CampaignGenesisNoReturn where
  roots := #[`CampaignGenesisNoReturn]

-- Immutable Genesis-Ongoing dependencies; non-default source and proof targets.
lean_lib CampaignGenesisOngoingSource where
  srcDir := "../atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4"
  roots := #[`H3V7N5QF.Answers, `Second.Cost]
  globs := #[.submodules `H3V7N5QF, .submodules `Second]

lean_lib CampaignGenesisOngoingRename where
  roots := #[`CampaignGenesisOngoingRename]

lean_lib CampaignGenesisOngoingRefinement where
  roots := #[`CampaignGenesisOngoingRefinement]

-- Explicit comparison classes, reusing the sealed source library above.
lean_lib CampaignGenesisProcessComparison where
  roots := #[`CampaignGenesisProcessComparison]

-- Campaign: DFM-CKM-PHYSICS-FENCE. Not a default target.
lean_lib CampaignDfmCkmPhysicsFence where
  roots := #[`CampaignDfmCkmPhysicsFence]

-- Campaign target: DFM-CONTINUUM-INTERFACE.
-- Not a default target: build with `lake build CampaignDfmContinuumInterface`.
lean_lib CampaignDfmContinuumInterface where
  roots := #[`CampaignDfmContinuumInterface]

-- Campaign: FSP-U1-WILSON-ACTION. Not a default target.
lean_lib CampaignFspU1WilsonAction where
  roots := #[`CampaignFspU1WilsonAction]


-- Campaign: DFM-GRIBOV-CONTINUUM-FENCE. Not a default target.
lean_lib CampaignDfmGribovContinuumFence where
  roots := #[`CampaignDfmGribovContinuumFence]

-- Campaign: DFM-SYMANZIK-QED-AE-FENCE. Not a default target.
lean_lib CampaignDfmSymanzikQedAeFence where
  roots := #[`CampaignDfmSymanzikQedAeFence]

-- Campaign: DFM-REGGE-GRAVITY-FENCE. Not a default target.
lean_lib CampaignDfmReggeGravityFence where
  roots := #[`CampaignDfmReggeGravityFence]

lean_lib CampaignDfmRelationalTimeFence where
  roots := #[`CampaignDfmRelationalTimeFence]

-- Campaign: DFM-Z1-Z2-COUNTERTERM-FENCE. Not a default target.
lean_lib CampaignDfmZ1Z2CountertermFence where
  roots := #[`CampaignDfmZ1Z2CountertermFence]

-- Campaign: PGW-SN-E08-WEIGHTED-L1-DUALITY. Not a default target.
lean_lib CampaignSnE08WeightedL1Duality where
  roots := #[`CampaignSnE08WeightedL1Duality]

-- Campaign: PGW-SN-PROTECTED-ANSWER-TRANSPORT. Not a default target.
lean_lib CampaignSnProtectedAnswerTransport where
  roots := #[`CampaignSnProtectedAnswerTransport]

-- Campaign: FSP-SU2-ADJOINT-REAL-DET. Not a default target.
lean_lib CampaignFspSu2AdjointRealDet where
  roots := #[`CampaignFspSu2AdjointRealDet]

-- Campaign: FSP-QCD-CHEMICAL-POTENTIAL-DET. Not a default target.
lean_lib CampaignFspQcdChemicalPotentialDet where
  roots := #[`CampaignFspQcdChemicalPotentialDet]

-- Campaign: FSP-LATTICE-WESS-ZUMINO-SUSY. Not a default target.
lean_lib CampaignFspLatticeWessZuminoSusy where
  roots := #[`CampaignFspLatticeWessZuminoSusy]

-- Campaign: ADS-CFT-DUALITY-IMPORT. Not a default target.
lean_lib CampaignAdsCftDualityImport where
  roots := #[`CampaignAdsCftDualityImport]

-- Campaign: ADS-HAPPY-TOY-NOT-DUALITY-GAP. Not a default target.
lean_lib CampaignAdsHappyToyNotDualityGap where
  roots := #[`CampaignAdsHappyToyNotDualityGap]

-- Campaign: FSP-IMAGINARY-MU-REAL-DET. Non-default.
lean_lib CampaignFspImaginaryMuRealDet where
  roots := #[`CampaignFspImaginaryMuRealDet]

-- Campaign: TFQ-0008. Not a default target.
lean_lib CampaignTfq0008FiniteDynamics where
  roots := #[`CampaignTfq0008FiniteDynamics]

-- Campaign: CQFT-LOCAL-NET-AXIOMS-IMPORT. Not a default target.
lean_lib CampaignCqftLocalNetAxiomsImport where
  roots := #[`CampaignCqftLocalNetAxiomsImport]

-- Campaign: LQG-EPRL-VERTEX-IMPORT. Not a default target.
lean_lib CampaignLqgEprlVertexImport where
  roots := #[`CampaignLqgEprlVertexImport]

-- Campaign: LQG-CONTINUUM-LIMIT-GAP. Not a default target.
lean_lib CampaignLqgContinuumLimitGap where
  roots := #[`CampaignLqgContinuumLimitGap]

-- Campaign: ADS-RT-FORMULA-IMPORT. Not a default target.
lean_lib CampaignAdsRtFormulaImport where
  roots := #[`CampaignAdsRtFormulaImport]

-- Campaign: ADS-REGGE-AREA-RT-GAP. Not a default target.
lean_lib CampaignAdsReggeAreaRtGap where
  roots := #[`CampaignAdsReggeAreaRtGap]

-- Campaign: CQFT-CAUSAL-FACTORIZATION-IMPORT. Not a default target.
lean_lib CampaignCqftCausalFactorizationImport where
  roots := #[`CampaignCqftCausalFactorizationImport]

-- Campaign: CQFT-REEH-SCHLIEDER-THEOREM-IMPORT. Not a default target.
lean_lib CampaignCqftReehSchliederTheoremImport where
  roots := #[`CampaignCqftReehSchliederTheoremImport]

-- Campaign: TFQ-0106. Not a default target.
lean_lib CampaignTfq0106FiniteQg where
  roots := #[`CampaignTfq0106FiniteQg]

-- Campaign: TFQ-0090. Not a default target.
lean_lib CampaignTfq0090FiniteQg where
  roots := #[`CampaignTfq0090FiniteQg]

-- Campaign: TFQ-0107. Not a default target.
lean_lib CampaignTfq0107FiniteQg where
  roots := #[`CampaignTfq0107FiniteQg]

-- Campaign: TFQ-0118. Not a default target.
lean_lib CampaignTfq0118ContinuumInterface where
  roots := #[`CampaignTfq0118ContinuumInterface]

-- Campaign: TFQ-0119. Not a default target.
lean_lib CampaignTfq0119ContinuumInterface where
  roots := #[`CampaignTfq0119ContinuumInterface]

-- Campaign: TFQ-0123. Not a default target.
lean_lib CampaignTfq0123ContinuumInterface where
  roots := #[`CampaignTfq0123ContinuumInterface]

-- Campaign: PG-WDP-GENESIS-BRIDGE-OBLIGATIONS. Not a default target.
lean_lib CampaignPgwWdpBridgeObligations where
  roots := #[`CampaignPgwWdpBridgeObligations]

lean_lib CampaignTfq0006L1ToL2 where
  roots := #[`CampaignTfq0006L1ToL2]

lean_lib CampaignTfq0008FiniteQmDynamics where
  roots := #[`CampaignTfq0008FiniteQmDynamics]

lean_lib CampaignTfq0009FiniteGauge where
  roots := #[`CampaignTfq0009FiniteGauge]

lean_lib CampaignTfq0010FiniteQed where
  roots := #[`CampaignTfq0010FiniteQed]

lean_lib CampaignTfq0011FiniteQcd where
  roots := #[`CampaignTfq0011FiniteQcd]

lean_lib CampaignTfq0012FiniteQcd where
  roots := #[`CampaignTfq0012FiniteQcd]

lean_lib CampaignTfq0014FiniteQcd where
  roots := #[`CampaignTfq0014FiniteQcd]

lean_lib CampaignTfq0017FiniteQcd where
  roots := #[`CampaignTfq0017FiniteQcd]

lean_lib CampaignTfq0026FiniteQcd where
  roots := #[`CampaignTfq0026FiniteQcd]

lean_lib CampaignTfq0027FiniteQcd where
  roots := #[`CampaignTfq0027FiniteQcd]

lean_lib CampaignTfq0032FiniteQcd where
  roots := #[`CampaignTfq0032FiniteQcd]

lean_lib CampaignTfq0033FiniteQcd where
  roots := #[`CampaignTfq0033FiniteQcd]

lean_lib CampaignTfq0038FiniteQcd where
  roots := #[`CampaignTfq0038FiniteQcd]

lean_lib CampaignTfq0039FiniteQcd where
  roots := #[`CampaignTfq0039FiniteQcd]

lean_lib CampaignTfq0040FiniteQcd where
  roots := #[`CampaignTfq0040FiniteQcd]

lean_lib CampaignTfq0042FiniteQcd where
  roots := #[`CampaignTfq0042FiniteQcd]

lean_lib CampaignTfq0044FiniteTopological where
  roots := #[`CampaignTfq0044FiniteTopological]

lean_lib CampaignTfq0050FiniteTopological where
  roots := #[`CampaignTfq0050FiniteTopological]

lean_lib CampaignTfq0171ImplementationSibling where
  roots := #[`CampaignTfq0171ImplementationSibling]

lean_lib CampaignTfq0183ImplementationSibling where
  roots := #[`CampaignTfq0183ImplementationSibling]

lean_lib CampaignTfq0184ImplementationSibling where
  roots := #[`CampaignTfq0184ImplementationSibling]

lean_lib CampaignTfq0191ImplementationSibling where
  roots := #[`CampaignTfq0191ImplementationSibling]

lean_lib CampaignTfq0199ImplementationSibling where
  roots := #[`CampaignTfq0199ImplementationSibling]

lean_lib CampaignTfq0376Pregenesis where
  roots := #[`CampaignTfq0376Pregenesis]

-- Campaign: PGW-PYTHON-LEAN-CARRIER-BRIDGE. Not a default target.
lean_lib CampaignPgwPythonLeanCarrierBridge where
  roots := #[`CampaignPgwPythonLeanCarrierBridge]

-- Campaign: PGW-CONTEXT-FIDELITY. Not a default target.
lean_lib CampaignPgwContextFidelity where
  roots := #[`CampaignPgwContextFidelity]

-- Campaign: TFQ-0003. Not a default target.
lean_lib CampaignTfq0003FiniteObstruction where
  roots := #[`CampaignTfq0003FiniteObstruction]

-- Campaign: TFQ-0313. Not a default target.
lean_lib CampaignTfq0313OperatorAlgebraShadow where
  roots := #[`CampaignTfq0313OperatorAlgebraShadow]

-- Campaign: TFQ-0319. Not a default target.
lean_lib CampaignTfq0319UnjoinedReceipt where
  roots := #[`CampaignTfq0319UnjoinedReceipt]

-- Campaign: TFQ-0374. Not a default target.
lean_lib CampaignTfq0374ThreeRecoveryContracts where
  roots := #[`CampaignTfq0374ThreeRecoveryContracts]

-- Campaign: TFQ-0385. Not a default target.
lean_lib CampaignTfq0385RuleErasesSeparation where
  roots := #[`CampaignTfq0385RuleErasesSeparation]

-- Campaign: PGW-K-ITEM-DELTA-GRAMMAR. Not a default target.
lean_lib CampaignPgwKItemDeltaGrammar where
  roots := #[`CampaignPgwKItemDeltaGrammar]

-- Campaign: PGW-DECLARED-INPUT-FLOOR. Not a default target.
lean_lib CampaignPgwDeclaredInputFloor where
  roots := #[`CampaignPgwDeclaredInputFloor]

-- Campaign: PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN. Not a default target.
lean_lib CampaignPgwIsomorphismSoundnessInLean where
  roots := #[`CampaignPgwIsomorphismSoundnessInLean]

-- Campaign: PGW-RUNS-PAST-DECLARED-BOUNDS. Not a default target.
lean_lib CampaignPgwRunsPastDeclaredBounds where
  roots := #[`CampaignPgwRunsPastDeclaredBounds]

-- Campaign: PGW-STREAM-AT-FOUR-ITEMS. Not a default target.
lean_lib CampaignPgwStreamAtFourItems where
  roots := #[`CampaignPgwStreamAtFourItems]

-- Campaign: PGW-DRIVER-B-SEVENTH-EVENT. Not a default target.
lean_lib CampaignPgwDriverBSeventhEvent where
  roots := #[`CampaignPgwDriverBSeventhEvent]

-- Campaign: PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT. Not a default target.
lean_lib CampaignPgwWdpIncidenceTransport where
  roots := #[`CampaignPgwWdpIncidenceTransport]

-- Campaign: PGW-WDP-BRIDGE-ONGOING-TO-WINDOW. Not a default target.
lean_lib CampaignPgwWdpBridgeOngoing where
  roots := #[`CampaignPgwWdpBridgeOngoing]

-- Campaign: PGW-WDP-HANDOFF-TO-L1. Not a default target.
lean_lib CampaignPgwWdpHandoffToL1 where
  roots := #[`CampaignPgwWdpHandoffToL1]

-- Campaign: MUB-PRIME-POWER-CONSTRUCTION. Not a default target.
lean_lib CampaignMubPrimePowerConstruction where
  roots := #[`CampaignMubPrimePowerConstruction]

-- Campaign: MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE. Not a default target.
lean_lib CampaignMajOpenLindbladTransferEnvelope where
  roots := #[`CampaignMajOpenLindbladTransferEnvelope]

-- Campaign: MAJ-OPEN-EVIDENCE-ADEQUACY. Not a default target.
lean_lib CampaignMajOpenEvidenceAdequacy where
  roots := #[`CampaignMajOpenEvidenceAdequacy]

-- Campaign: GTH-SHADOW. Not a default target.
lean_lib CampaignGthShadow where
  roots := #[`CampaignGthShadow]

-- Campaign: GTH-LANG-CORE. Not a default target.
lean_lib CampaignGthLangCore where
  roots := #[`CampaignGthLangCore]

-- Campaign: L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED. Not a default target.
lean_lib CampaignL1ResidualSectorWeights where
  roots := #[`CampaignL1ResidualSectorWeights]

-- Campaign: FQ-PRIM-TO-QM-SELECTION-OPEN. Not a default target.
lean_lib CampaignFqPrimToQmSelection where
  roots := #[`CampaignFqPrimToQmSelection]

-- Campaign: FQ-GAP-U1-CIRCLE. Not a default target.
lean_lib CampaignFqGapU1Circle where
  roots := #[`CampaignFqGapU1Circle]

-- Campaign: COMP-C2-STEP3-NOT-WORD-STEP. Not a default target.
lean_lib CampaignCompC2Step3NotWordStep where
  roots := #[`CampaignCompC2Step3NotWordStep]

-- Campaign: COMP-C6-TM0-OUTPUT-FORM-OPEN. Not a default target.
lean_lib CampaignCompC6Tm0OutputFormOpen where
  roots := #[`CampaignCompC6Tm0OutputFormOpen]

-- Campaign: COMP-C7-FIXED-TARGET-OPEN. Not a default target.
lean_lib CampaignCompC7FixedTargetOpen where
  roots := #[`CampaignCompC7FixedTargetOpen]
