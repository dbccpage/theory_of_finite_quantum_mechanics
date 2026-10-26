import Lake
open Lake DSL
package pre_genesis_to_mssn where
  version := v!"1.0.0"
@[default_target]
lean_lib Paper where
  srcDir := "."
  roots := #[`Paper, `Homology, `FreeAbelian, `FreeGroup, `FreeWord, `WedgeHomology, `IntegerAction, `FiniteCoordinates, `GraphHomology, `GraphExtensions, `UnionComponents, `GraphRetraction, `TriangleHomology, `TriangleDegree, `Cochain, `ChainHomotopy, `Observation, `DiscreteCategory, `BellPair, `BellMixture, `WordRecovery, `Replay, `SnSyntax, `SnCarrier, `SnTheorems, `MssnSyntax, `MssnObstructionDetector,
    `MssnFiniteAlgebra, `MssnSimplicialGauge, `MssnSmithNormalForm, `MssnQuantumTransfer]
