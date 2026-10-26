import WitnessedDifference.Core

/-!
# Open and nonclaim boundary registry

The constructors below are labels, not propositions and not theorem claims.
This package proves no reconstruction, phenomenology, continuum-time, Born
uniqueness, or cosmogenesis result.
-/

namespace WitnessedDifference.OPEN

inductive Topic where
  | quantumReconstruction
  | phenomenology
  | continuumTime
  | bornUniqueness
  | cosmogenesis
  deriving DecidableEq, Repr

def status : Topic → String
  | .quantumReconstruction => "OPEN"
  | .phenomenology => "OPEN"
  | .continuumTime => "OPEN"
  | .bornUniqueness => "OPEN"
  | .cosmogenesis => "OPEN"

end WitnessedDifference.OPEN

namespace WitnessedDifference.NONCLAIM

structure Boundary where
  topic : OPEN.Topic
  reason : String
  deriving Repr

def registry : List Boundary :=
  [ { topic := .quantumReconstruction
      reason := "Finite observer data do not reconstruct quantum theory." }
  , { topic := .phenomenology
      reason := "Observer packets do not establish phenomenal awareness." }
  , { topic := .continuumTime
      reason := "Finite path duration does not construct continuum time." }
  , { topic := .bornUniqueness
      reason := "Multiplicity normalization is not a Born uniqueness proof." }
  , { topic := .cosmogenesis
      reason := "Relative routing does not establish cosmogenesis." }
  ]

end WitnessedDifference.NONCLAIM
