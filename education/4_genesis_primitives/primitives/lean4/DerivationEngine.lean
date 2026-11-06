import SeedAndRegime

/-!
# Genesis Derivation Engine, Tree, Nodes & Records (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/Rounds.lean
- lean4/Derivation/Completion.lean

Classification: Autonomous tree exploration, branch quotienting, and evidence ledgers.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.DerivationEngine

open GenesisPrimitives.SeedAndRegime

abbrev Pair := Nat × Nat

/-- Surviving reading specification (Reading L vs Reading F). -/
structure Reading where
  name : String
  description : String
  genesis : List Event
  target : Pair
deriving Repr, DecidableEq

/-- Node in the derivation branch tree. -/
structure Node where
  nodeId : Nat
  history : List Event
  regime : Regime
  depth : Nat
  status : String
  mergedCount : Nat
  certified : Bool
deriving Repr, DecidableEq

/-- Directed edge in the derivation branch tree. -/
structure Edge where
  parent : Nat
  child : Nat
  roundNo : Nat
  challenge : String
  responseLabel : String
  response : Delta
  tieClasses : Nat
  classSize : Nat
  cost : Nat × Nat
  orbits : Nat
deriving Repr, DecidableEq

/-- Generator round record. -/
structure RoundRecord where
  roundNo : Nat
  obstructionsBefore : Nat
  firstPair : Option Pair
  repairs : Nat
  importsThisRound : Nat
  obstructionsAfter : Nat
deriving Repr, DecidableEq

end GenesisPrimitives.DerivationEngine
