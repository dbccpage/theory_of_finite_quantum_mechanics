import PrimitivePassage

/-!
# Transition Alphabet, Trace Monoid & Records (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/TransitionAlphabet.lean
- lean4/Derivation/TraceAlgebra.lean

Classification: Transition monoid, trace calculus, and DDC operational alphabet.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.TransitionAndTrace

open GenesisPrimitives.PrimitivePassage

/-- Obstruction Effect: qualitative change in the active-obstruction set. -/
inductive ObstEffect where
  | removed
  | created
  | preserved
  | untouched
deriving Repr, DecidableEq

/-- Guard Kind for transitions. -/
inductive GuardKind where
  | freshOcc
  | wfAssert
  | assertedWit
  | witnessedProt
  | preObservational
  | refineOk
  | colOk
  | obstRefuse
  | budgetMove
  | licenseMove
  | activeHalt
deriving Repr, DecidableEq

/-- Budget Delta Classification. -/
inductive BudgetDelta where
  | unchanged
  | spentOne
  | rewritten
deriving Repr, DecidableEq

/-- Continuity Classification: absorbing terminal vs continuation. -/
inductive Continuity where
  | absorption
  | continuation
deriving Repr, DecidableEq

/-- Origin: environment-driven vs internal response. -/
inductive Origin where
  | env
  | int
deriving Repr, DecidableEq

/-- Profile structure carrying effect data. -/
structure Profile where
  fieldDelta : List Bool
  guard : GuardKind
  obst : ObstEffect
  budget : BudgetDelta
  cont : Continuity
  orig : Origin
  accepted : Bool
deriving Repr, DecidableEq

/-- Typed Transition Record (TRecord). -/
structure TRecord where
  pre : PState
  ev : PEvent
  guard : GuardKind
  post : PState
  spend : BudgetDelta
  profile : Profile
deriving Repr, DecidableEq

end GenesisPrimitives.TransitionAndTrace
