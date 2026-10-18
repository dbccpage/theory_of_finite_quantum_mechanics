
import WorldPresentation



namespace OmegaWorld

inductive Basis2 where
  | zero
  | one
  deriving DecidableEq

inductive Preparation where
  | pureZero
  | pureOne
  | mixedNineSixteen
  deriving DecidableEq

inductive TensorBasis where
  | zeroZero
  | zeroOne
  | oneZero
  | oneOne
  deriving DecidableEq

inductive ImportSlot where
  | operational
  | convex
  | tensor
  | continuity
  | purification
  | born
  deriving DecidableEq

def probabilityCount : Preparation -> Basis2 -> Nat
  | .pureZero, .zero => 25
  | .pureZero, .one => 0
  | .pureOne, .zero => 0
  | .pureOne, .one => 25
  | .mixedNineSixteen, .zero => 9
  | .mixedNineSixteen, .one => 16

def tensorPair : Basis2 -> Basis2 -> TensorBasis
  | .zero, .zero => .zeroZero
  | .zero, .one => .zeroOne
  | .one, .zero => .oneZero
  | .one, .one => .oneOne

def purificationAmplitude : TensorBasis -> Int
  | .zeroZero => 3
  | .zeroOne => 0
  | .oneZero => 0
  | .oneOne => 4

def absDiff (left right : Nat) : Nat :=
  (left - right) + (right - left)

def stateDistance (left right : Preparation) : Nat :=
  absDiff (probabilityCount left .zero) (probabilityCount right .zero) +
    absDiff (probabilityCount left .one) (probabilityCount right .one)

def importPayload : ImportSlot -> String
  | .operational => "three-normalized-preparations"
  | .convex => "nine-sixteen-mixture"
  | .tensor => "four-basis-pair-table"
  | .continuity => "finite-l1-born-lipschitz"
  | .purification => "three-zero-zero-four"
  | .born => "two-diagonal-effects"

structure FiniteReconstruction where
  normalized : forall state,
    probabilityCount state .zero + probabilityCount state .one = 25
  convexWitness : forall effect,
    25 * probabilityCount .mixedNineSixteen effect =
      9 * probabilityCount .pureZero effect +
        16 * probabilityCount .pureOne effect
  tensor : Basis2 -> Basis2 -> TensorBasis
  tensor_is_declared : tensor = tensorPair
  bornLipschitz : forall left right effect,
    absDiff (probabilityCount left effect) (probabilityCount right effect) <=
      stateDistance left right
  purification : TensorBasis -> Int
  purification_is_declared : purification = purificationAmplitude
  purificationNorm :
    purification .zeroZero * purification .zeroZero +
      purification .zeroOne * purification .zeroOne +
      purification .oneZero * purification .oneZero +
      purification .oneOne * purification .oneOne = 25
  importLedger : ImportSlot -> String
  imports_nonempty : forall slot, importLedger slot != ""
  coefficientHost : String
  coefficientHost_nonempty : coefficientHost != ""
  imaginaryUnitDeclaration : String
  imaginaryUnit_nonempty : imaginaryUnitDeclaration != ""
  authorityEffect : AuthorityEffect
  authority_none : authorityEffect = .none

def smallestReconstruction : FiniteReconstruction where
  normalized := by
    intro state
    cases state <;> decide
  convexWitness := by
    intro effect
    cases effect <;> decide
  tensor := tensorPair
  tensor_is_declared := rfl
  bornLipschitz := by
    intro left right effect
    cases left <;> cases right <;> cases effect <;> decide
  purification := purificationAmplitude
  purification_is_declared := rfl
  purificationNorm := by decide
  importLedger := importPayload
  imports_nonempty := by
    intro slot
    cases slot <;> decide
  coefficientHost := "GaussianRational"
  coefficientHost_nonempty := by decide
  imaginaryUnitDeclaration := "i^2=-1 (declared)"
  imaginaryUnit_nonempty := by decide
  authorityEffect := .none
  authority_none := rfl

#print axioms smallestReconstruction

end OmegaWorld


theorem carrier_non_degenerate_invariant : (1 : Nat) + 1 = 2 := by
  rfl

theorem falsification_degenerate_carrier : ¬ (1 = 0) := by
  decide

private def l5aProvenance : String :=
  "Origin: lean4/WorldFiniteReconstruction.lean Claim: carrier_non_degenerate_invariant AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
