/-!
# Refusal Disciplines, Represented Worlds & Constitution (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/Refusal.lean
- lean4/Derivation/Represented.lean
- lean4/Derivation/Constitution.lean

Classification: Refusal semantics, world models, and metatheoretic boundaries.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.RefusalAndBoundary

abbrev Token := String
abbrev Pair := Nat × Nat
abbrev View := List Nat

/-- Refusal comparison events. -/
inductive REvent where
  | sup (tok : Token)
  | adm (tok : Token)
  | form
  | inst (idx : Nat)
deriving Repr, DecidableEq

/-- Refusal comparison state (RState). -/
structure RState where
  data : List Token
  tags : List Nat
  refusals : Nat
  hasForm : Bool
  insts : List Nat
deriving Repr, DecidableEq

/-- The represented-progress world state. -/
structure World where
  data : List Nat
  views : List View
  reqs : List Pair
  refusals : List Pair
  budget : Nat
  augLicensed : Bool
  notes : List Nat
deriving Repr, DecidableEq

/-- Constitution Description: six independent toggles of the sealed kernel. -/
structure ConstitutionDesc where
  dedupAdmit : Bool
  guardRequire : Bool
  guardAccept : Bool
  gateBudget : Bool
  gateLicense : Bool
  certRefusal : Bool
deriving Repr, DecidableEq

/-- Controller Category Description. -/
structure KindDesc where
  name : String
  hasObstruction : Bool
  hasDeclaredObs : Bool
  isHalted : Bool
deriving Repr, DecidableEq

end GenesisPrimitives.RefusalAndBoundary
