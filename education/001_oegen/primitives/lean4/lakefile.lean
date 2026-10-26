import Lake
open Lake DSL

package «genesis_primitives» where
  version := v!"0.1.0"

@[default_target]
lean_lib «GenesisPrimitives» where
  srcDir := "."
  roots := #[
    `Apartness,
    `AttachmentLadder,
    `ControllerCategory,
    `DerivationEngine,
    `EndogenousFidelity,
    `ObserverInventory,
    `PresentationRelativity,
    `PrimitiveContact,
    `PrimitiveDifference,
    `PrimitivePassage,
    `RefusalAndBoundary,
    `RenamingStructure,
    `RepresentedProgress,
    `SeedAndRegime,
    `SimplicialComplex,
    `StableContent,
    `TraceAlgebra,
    `TransitionAndTrace,
    `WeightProfile,
    `AxiomAudit,
    `SupplyErasure
  ]
