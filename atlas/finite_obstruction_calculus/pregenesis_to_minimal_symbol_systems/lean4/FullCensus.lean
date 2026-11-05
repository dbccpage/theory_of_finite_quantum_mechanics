import BellMixture
import BellPair
import ChainHomotopy
import Cochain
import DiscreteCategory
import FiniteCoordinates
import FreeAbelian
import FreeGroup
import FreeWord
import GraphExtensions
import GraphHomology
import GraphRetraction
import Homology
import IntegerAction
import MssnFiniteAlgebra
import MssnObstructionDetector
import MssnQuantumTransfer
import MssnSimplicialGauge
import MssnSmithNormalForm
import MssnSyntax
import Observation
import Paper
import Replay
import SnCarrier
import SnSyntax
import SnTheorems
import TriangleDegree
import TriangleHomology
import UnionComponents
import WedgeHomology
import WordRecovery
import Lean
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let modules : Array Name := #[`BellMixture, `BellPair, `ChainHomotopy, `Cochain, `DiscreteCategory, `FiniteCoordinates, `FreeAbelian, `FreeGroup, `FreeWord, `GraphExtensions, `GraphHomology, `GraphRetraction, `Homology, `IntegerAction, `MssnFiniteAlgebra, `MssnObstructionDetector, `MssnQuantumTransfer, `MssnSimplicialGauge, `MssnSmithNormalForm, `MssnSyntax, `Observation, `Paper, `Replay, `SnCarrier, `SnSyntax, `SnTheorems, `TriangleDegree, `TriangleHomology, `UnionComponents, `WedgeHomology, `WordRecovery]
  for (name, _) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if modules.contains env.header.moduleNames[idx.toNat]! then
        let axioms ← collectAxioms name
        if axioms.isEmpty then
          logInfo m!"'{name}' does not depend on any axioms"
        else
          let names := String.intercalate ", " (axioms.toList.map toString)
          logInfo m!"'{name}' depends on axioms: [{names}]"
