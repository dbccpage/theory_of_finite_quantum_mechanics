/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import WorldFiniteReconstruction

/-!
# Q12: an inhabited diagonal reconstruction retraction

This file strengthens the existing three-preparation/two-effect fixture by
constructing its exact integer-scaled 2 x 2 diagonal representation.  The
scale is 25.  `encodeState` sends each preparation to its diagonal probability
matrix; `decodeState` recognizes each declared image and rejects two explicit
outside matrices; and `decode_encode` proves a left inverse on every declared
preparation.

The two effects are explicit diagonal projectors.  Their trace pairing with an
encoded state reproduces the declared probability table exactly.  The file
also proves normalization, diagonal nonnegativity, symmetry, projector laws,
and the exact 9/25--16/25 affine identity.

This is a faithful representation of one finite commutative table.  It is not
REC-FULL and does not construct a complex host, general matrix positivity or
order, monoidal products, CPTP/U1 structure, local tomography, instruments, or
Born selection.  Those general reconstruction obligations remain OPEN.

AuthorityEffect: None.
-/

namespace OmegaWorld
namespace ReconstructionQ12

abbrev Matrix2 := Basis2 -> Basis2 -> Int

def zeroMatrix : Matrix2 := fun _row _column => 0

def identityMatrix : Matrix2
  | .zero, .zero => 1
  | .one, .one => 1
  | _, _ => 0

def matrixAdd (left right : Matrix2) : Matrix2 := fun row column =>
  left row column + right row column

def matrixScale (scalar : Int) (matrix : Matrix2) : Matrix2 := fun row column =>
  scalar * matrix row column

def matrixMul (left right : Matrix2) : Matrix2 := fun row column =>
  left row .zero * right .zero column +
    left row .one * right .one column

def trace2 (matrix : Matrix2) : Int :=
  matrix .zero .zero + matrix .one .one

/-- The exact diagonal matrix `25 * rho_state`. -/
def encodeState (state : Preparation) : Matrix2
  | .zero, .zero => (probabilityCount state .zero : Int)
  | .one, .one => (probabilityCount state .one : Int)
  | _, _ => 0

def matrixMatches (left right : Matrix2) : Bool :=
  (left .zero .zero == right .zero .zero) &&
    (left .zero .one == right .zero .one) &&
    (left .one .zero == right .one .zero) &&
    (left .one .one == right .one .one)

/-- A partial decoder: matrices outside the three declared images return `none`. -/
def decodeState (matrix : Matrix2) : Option Preparation :=
  if matrixMatches matrix (encodeState .pureZero) then
    some .pureZero
  else if matrixMatches matrix (encodeState .pureOne) then
    some .pureOne
  else if matrixMatches matrix (encodeState .mixedNineSixteen) then
    some .mixedNineSixteen
  else
    none

theorem decode_encode (state : Preparation) :
    decodeState (encodeState state) = some state := by
  cases state <;> decide

theorem encode_injective (left right : Preparation) :
    encodeState left = encodeState right -> left = right := by
  intro encodedEqual
  have decodedEqual := congrArg decodeState encodedEqual
  rw [decode_encode left, decode_encode right] at decodedEqual
  exact Option.some.inj decodedEqual

theorem encoded_images_pairwise_distinct :
    encodeState .pureZero ≠ encodeState .pureOne /\
      encodeState .pureZero ≠ encodeState .mixedNineSixteen /\
      encodeState .pureOne ≠ encodeState .mixedNineSixteen := by
  constructor
  · intro encodedEqual
    have statesEqual := encode_injective .pureZero .pureOne encodedEqual
    cases statesEqual
  · constructor
    · intro encodedEqual
      have statesEqual :=
        encode_injective .pureZero .mixedNineSixteen encodedEqual
      cases statesEqual
    · intro encodedEqual
      have statesEqual :=
        encode_injective .pureOne .mixedNineSixteen encodedEqual
      cases statesEqual

def malformedMatrix : Matrix2
  | .zero, .zero => 25
  | .zero, .one => 1
  | _, _ => 0

theorem decode_malformed_none : decodeState malformedMatrix = none := by
  decide

/-- A normalized nonnegative diagonal matrix not among the three declared images. -/
def outsideImageDiagonal : Matrix2
  | .zero, .zero => 1
  | .one, .one => 24
  | _, _ => 0

theorem outside_diagonal_trace_twenty_five :
    trace2 outsideImageDiagonal = 25 := by
  decide

theorem outside_diagonal_nonnegative (coord : Basis2) :
    0 <= outsideImageDiagonal coord coord := by
  cases coord <;> decide

theorem outside_diagonal_off_diagonal_zero :
    outsideImageDiagonal .zero .one = 0 /\
      outsideImageDiagonal .one .zero = 0 := by
  decide

theorem decode_outside_diagonal_none :
    decodeState outsideImageDiagonal = none := by
  decide

theorem outside_diagonal_not_encoded (state : Preparation) :
    outsideImageDiagonal ≠ encodeState state := by
  intro encodedEqual
  have zeroEntry :=
    congrFun (congrFun encodedEqual Basis2.zero) Basis2.zero
  cases state <;>
    simp [outsideImageDiagonal, encodeState, probabilityCount] at zeroEntry

/-- The declared effect is represented by its coordinate projector. -/
def effectProjector : Basis2 -> Matrix2
  | .zero, .zero, .zero => 1
  | .one, .one, .one => 1
  | _, _, _ => 0

def bornCount (state : Preparation) (effect : Basis2) : Int :=
  trace2 (matrixMul (encodeState state) (effectProjector effect))

/-- Exact trace pairing; this is not a theorem selecting the Born rule. -/
theorem born_table_exact (state : Preparation) (effect : Basis2) :
    bornCount state effect = (probabilityCount state effect : Int) := by
  cases state <;> cases effect <;> decide

theorem encoded_trace_twenty_five (state : Preparation) :
    trace2 (encodeState state) = 25 := by
  cases state <;> decide

theorem encoded_diagonal_nonnegative (state : Preparation) (coord : Basis2) :
    0 <= encodeState state coord coord := by
  cases state <;> cases coord <;> decide

theorem encoded_off_diagonal_zero (state : Preparation) :
    encodeState state .zero .one = 0 /\
      encodeState state .one .zero = 0 := by
  cases state <;> decide

theorem encoded_symmetric (state : Preparation) (row column : Basis2) :
    encodeState state row column = encodeState state column row := by
  cases state <;> cases row <;> cases column <;> decide

theorem effect_projector_idempotent (effect : Basis2) :
    matrixMul (effectProjector effect) (effectProjector effect) =
      effectProjector effect := by
  funext row column
  cases effect <;> cases row <;> cases column <;> decide

theorem effect_projectors_orthogonal :
    matrixMul (effectProjector .zero) (effectProjector .one) = zeroMatrix /\
      matrixMul (effectProjector .one) (effectProjector .zero) = zeroMatrix := by
  constructor <;> funext row column <;>
    cases row <;> cases column <;> decide

theorem effect_projectors_resolve_identity :
    matrixAdd (effectProjector .zero) (effectProjector .one) =
      identityMatrix := by
  funext row column
  cases row <;> cases column <;> decide

/-- Exact affine identity for the declared 9/25--16/25 mixed state. -/
theorem mixed_state_affine_identity :
    matrixScale 25 (encodeState .mixedNineSixteen) =
      matrixAdd
        (matrixScale 9 (encodeState .pureZero))
        (matrixScale 16 (encodeState .pureOne)) := by
  funext row column
  cases row <;> cases column <;> decide

/-
The local generic `ConditionalPackage` defined below is just supplied imports
paired with a supplied recovery object.  Its round trips expose that this local
packaging model cannot create either component.  No theorem identifies it with
the separate legacy REC wrapper described by the frontier sources.
-/
structure ConditionalPackage (Imports Recovery : Type) where
  explicitImports : Imports
  conditionalRecovery : Recovery

def packageConditional {Imports Recovery : Type}
    (components : Imports × Recovery) : ConditionalPackage Imports Recovery where
  explicitImports := components.1
  conditionalRecovery := components.2

def exposeConditional {Imports Recovery : Type}
    (package : ConditionalPackage Imports Recovery) : Imports × Recovery :=
  (package.explicitImports, package.conditionalRecovery)

theorem expose_package_roundtrip {Imports Recovery : Type}
    (components : Imports × Recovery) :
    exposeConditional (packageConditional components) = components := by
  cases components
  rfl

theorem package_expose_roundtrip {Imports Recovery : Type}
    (package : ConditionalPackage Imports Recovery) :
    packageConditional (exposeConditional package) = package := by
  cases package
  rfl

structure DiagonalReconstructionRetraction where
  scale : Nat
  scaleIsTwentyFive : scale = 25
  encode : Preparation -> Matrix2
  decode : Matrix2 -> Option Preparation
  encodeIsDeclared : encode = encodeState
  decodeIsDeclared : decode = decodeState
  leftInverse : forall state, decode (encode state) = some state
  faithful : forall left right, encode left = encode right -> left = right
  encodedImagesDistinct :
    encode .pureZero ≠ encode .pureOne /\
      encode .pureZero ≠ encode .mixedNineSixteen /\
      encode .pureOne ≠ encode .mixedNineSixteen
  effects : Basis2 -> Matrix2
  effectsAreDeclared : effects = effectProjector
  exactPairing : forall state effect,
    trace2 (matrixMul (encode state) (effects effect)) =
      (probabilityCount state effect : Int)
  normalized : forall state, trace2 (encode state) = (scale : Int)
  diagonalNonnegative : forall state coord,
    0 <= encode state coord coord
  offDiagonalZero : forall state,
    encode state .zero .one = 0 /\ encode state .one .zero = 0
  symmetric : forall state row column,
    encode state row column = encode state column row
  effectIdempotent : forall effect,
    matrixMul (effects effect) (effects effect) = effects effect
  effectsOrthogonal :
    matrixMul (effects .zero) (effects .one) = zeroMatrix /\
      matrixMul (effects .one) (effects .zero) = zeroMatrix
  effectsResolveIdentity :
    matrixAdd (effects .zero) (effects .one) = identityMatrix
  affineMixed :
    matrixScale (scale : Int) (encode .mixedNineSixteen) =
      matrixAdd
        (matrixScale 9 (encode .pureZero))
        (matrixScale 16 (encode .pureOne))
  malformedRejected : decode malformedMatrix = none
  outsideDiagonalTrace : trace2 outsideImageDiagonal = (scale : Int)
  outsideDiagonalNonnegative : forall coord,
    0 <= outsideImageDiagonal coord coord
  outsideDiagonalOffDiagonalZero :
    outsideImageDiagonal .zero .one = 0 /\
      outsideImageDiagonal .one .zero = 0
  outsideDiagonalRejected : decode outsideImageDiagonal = none
  outsideDiagonalNotEncoded : forall state,
    outsideImageDiagonal ≠ encode state
  recFullClaimed : Bool
  complexHostConstructed : Bool
  generalPositivityOrderConstructed : Bool
  monoidalStructureConstructed : Bool
  cptpStructureConstructed : Bool
  u1StructureConstructed : Bool
  localTomographyConstructed : Bool
  instrumentHostConstructed : Bool
  bornSelectionConstructed : Bool
  primitiveDifferenceDerivationClaimed : Bool
  legacyConditionalWrapperModeled : Bool
  recFullOpen : recFullClaimed = false
  complexHostOpen : complexHostConstructed = false
  generalPositivityOrderOpen : generalPositivityOrderConstructed = false
  monoidalStructureOpen : monoidalStructureConstructed = false
  cptpStructureOpen : cptpStructureConstructed = false
  u1StructureOpen : u1StructureConstructed = false
  localTomographyOpen : localTomographyConstructed = false
  instrumentHostOpen : instrumentHostConstructed = false
  bornSelectionOpen : bornSelectionConstructed = false
  primitiveDifferenceDerivationOpen :
    primitiveDifferenceDerivationClaimed = false
  legacyConditionalWrapperOpen : legacyConditionalWrapperModeled = false
  authorityEffect : AuthorityEffect
  authorityNone : authorityEffect = .none

def diagonalReconstructionRetraction : DiagonalReconstructionRetraction where
  scale := 25
  scaleIsTwentyFive := rfl
  encode := encodeState
  decode := decodeState
  encodeIsDeclared := rfl
  decodeIsDeclared := rfl
  leftInverse := decode_encode
  faithful := encode_injective
  encodedImagesDistinct := encoded_images_pairwise_distinct
  effects := effectProjector
  effectsAreDeclared := rfl
  exactPairing := born_table_exact
  normalized := encoded_trace_twenty_five
  diagonalNonnegative := encoded_diagonal_nonnegative
  offDiagonalZero := encoded_off_diagonal_zero
  symmetric := encoded_symmetric
  effectIdempotent := effect_projector_idempotent
  effectsOrthogonal := effect_projectors_orthogonal
  effectsResolveIdentity := effect_projectors_resolve_identity
  affineMixed := mixed_state_affine_identity
  malformedRejected := decode_malformed_none
  outsideDiagonalTrace := outside_diagonal_trace_twenty_five
  outsideDiagonalNonnegative := outside_diagonal_nonnegative
  outsideDiagonalOffDiagonalZero := outside_diagonal_off_diagonal_zero
  outsideDiagonalRejected := decode_outside_diagonal_none
  outsideDiagonalNotEncoded := outside_diagonal_not_encoded
  recFullClaimed := false
  complexHostConstructed := false
  generalPositivityOrderConstructed := false
  monoidalStructureConstructed := false
  cptpStructureConstructed := false
  u1StructureConstructed := false
  localTomographyConstructed := false
  instrumentHostConstructed := false
  bornSelectionConstructed := false
  primitiveDifferenceDerivationClaimed := false
  legacyConditionalWrapperModeled := false
  recFullOpen := rfl
  complexHostOpen := rfl
  generalPositivityOrderOpen := rfl
  monoidalStructureOpen := rfl
  cptpStructureOpen := rfl
  u1StructureOpen := rfl
  localTomographyOpen := rfl
  instrumentHostOpen := rfl
  bornSelectionOpen := rfl
  primitiveDifferenceDerivationOpen := rfl
  legacyConditionalWrapperOpen := rfl
  authorityEffect := .none
  authorityNone := rfl

#print axioms decode_encode
#print axioms encode_injective
#print axioms encoded_images_pairwise_distinct
#print axioms decode_outside_diagonal_none
#print axioms outside_diagonal_off_diagonal_zero
#print axioms outside_diagonal_not_encoded
#print axioms born_table_exact
#print axioms encoded_trace_twenty_five
#print axioms encoded_diagonal_nonnegative
#print axioms effect_projector_idempotent
#print axioms effect_projectors_orthogonal
#print axioms effect_projectors_resolve_identity
#print axioms mixed_state_affine_identity
#print axioms expose_package_roundtrip
#print axioms package_expose_roundtrip
#print axioms diagonalReconstructionRetraction

end ReconstructionQ12
end OmegaWorld
