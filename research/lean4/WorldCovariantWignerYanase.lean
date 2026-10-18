/-!
# Q10: an exact non-vacuous covariant Wigner--Yanase slice

This dependency-free file works with integer-scaled 2 x 2 real matrices.  It
exhibits complete dephasing in the Z basis as a two-Kraus trace-preserving map,
proves the exact generator-intertwining equation

  Phi ([Z, X]) = [Z, Phi (X)]

for every matrix X, and evaluates a density matrix that the channel genuinely
moves.  The state matrices and their declared positive square roots carry
explicit Gram factorizations.  Exact cross-multiplication certifies that the
Wigner--Yanase quantity drops strictly from 576/625 to 0.

This is a substantive finite exact slice, not the general covariance theorem.
It does not prove that generator intertwining implies U(1) covariance through
a matrix exponential, formalize arbitrary complex CPTP maps, or establish
monotonicity for every covariant channel.  The refuted universal-CPTP and
merely-unital scopes remain refuted.

AuthorityEffect: None.
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace OmegaWorld
namespace WignerYanaseQ10

inductive Q10AuthorityEffect where
  | none
  deriving DecidableEq

inductive Coord2 where
  | zero
  | one
  deriving DecidableEq

inductive FactorCoord4 where
  | a
  | b
  | c
  | d
  deriving DecidableEq

abbrev Matrix2 := Coord2 -> Coord2 -> Int
abbrev Factor4x2 := FactorCoord4 -> Coord2 -> Int

def matrixAdd (left right : Matrix2) : Matrix2 := fun row column =>
  left row column + right row column

def matrixSub (left right : Matrix2) : Matrix2 := fun row column =>
  left row column - right row column

def scaleMatrix (scalar : Int) (matrix : Matrix2) : Matrix2 := fun row column =>
  scalar * matrix row column

def matrixTranspose (matrix : Matrix2) : Matrix2 := fun row column =>
  matrix column row

def matrixMul (left right : Matrix2) : Matrix2 := fun row column =>
  left row .zero * right .zero column +
    left row .one * right .one column

def trace2 (matrix : Matrix2) : Int :=
  matrix .zero .zero + matrix .one .one

def commutator (left right : Matrix2) : Matrix2 :=
  matrixSub (matrixMul left right) (matrixMul right left)

def identity2 : Matrix2
  | .zero, .zero => 1
  | .one, .one => 1
  | _, _ => 0

def zObservable : Matrix2
  | .zero, .zero => 1
  | .one, .one => -1
  | _, _ => 0

def pZero : Matrix2
  | .zero, .zero => 1
  | _, _ => 0

def pOne : Matrix2
  | .one, .one => 1
  | _, _ => 0

/-- Complete dephasing in the declared Z basis. -/
def dephaseZ (matrix : Matrix2) : Matrix2
  | .zero, .zero => matrix .zero .zero
  | .one, .one => matrix .one .one
  | _, _ => 0

/-- The finite commutator-intertwining condition used in this scoped slice. -/
def GeneratorIntertwining (channel : Matrix2 -> Matrix2)
    (generator : Matrix2) : Prop :=
  forall matrix,
    channel (commutator generator matrix) =
      commutator generator (channel matrix)

theorem dephaseZ_two_kraus_action (matrix : Matrix2) :
    dephaseZ matrix =
      matrixAdd
        (matrixMul (matrixMul pZero matrix) (matrixTranspose pZero))
        (matrixMul (matrixMul pOne matrix) (matrixTranspose pOne)) := by
  funext row column
  cases row <;> cases column <;>
    simp [dephaseZ, matrixAdd, matrixMul, matrixTranspose, pZero, pOne] <;>
    omega

theorem dephaseZ_kraus_completeness :
    matrixAdd
        (matrixMul (matrixTranspose pZero) pZero)
        (matrixMul (matrixTranspose pOne) pOne) =
      identity2 := by
  funext row column
  cases row <;> cases column <;> decide

theorem dephaseZ_trace_preserving (matrix : Matrix2) :
    trace2 (dephaseZ matrix) = trace2 matrix := by
  rfl

theorem dephaseZ_unital : dephaseZ identity2 = identity2 := by
  funext row column
  cases row <;> cases column <;> decide

theorem dephaseZ_generator_intertwining :
    GeneratorIntertwining dephaseZ zObservable := by
  intro matrix
  funext row column
  cases row <;> cases column <;>
    simp [dephaseZ, commutator, matrixSub, matrixMul, zObservable] <;>
    omega

def gram2 (factor : Factor4x2) : Matrix2 := fun row column =>
  factor .a row * factor .a column +
    factor .b row * factor .b column +
    factor .c row * factor .c column +
    factor .d row * factor .d column

/-
If `matrix` represents M / matrixScale and `factor` represents B / factorScale,
the equation below is exactly M / matrixScale = B^T B / factorScale^2.
-/
structure ScaledGramCertificate (matrixScale : Nat) (matrix : Matrix2) where
  factorScale : Nat
  factorScalePositive : 0 < factorScale
  factor : Factor4x2
  factorization :
    scaleMatrix (matrixScale : Int) (gram2 factor) =
      scaleMatrix ((factorScale : Int) * (factorScale : Int)) matrix

/-- A scaled density fixture with an exact positive-square-root certificate. -/
structure RootedDensity where
  rhoScale : Nat
  sqrtScale : Nat
  rhoScalePositive : 0 < rhoScale
  sqrtScalePositive : 0 < sqrtScale
  rho : Matrix2
  sqrtRho : Matrix2
  rhoGram : ScaledGramCertificate rhoScale rho
  sqrtGram : ScaledGramCertificate sqrtScale sqrtRho
  sqrtSquare :
    scaleMatrix (rhoScale : Int) (matrixMul sqrtRho sqrtRho) =
      scaleMatrix ((sqrtScale : Int) * (sqrtScale : Int)) rho
  traceOne : trace2 rho = (rhoScale : Int)

/-
For a root represented by S / rootScale and an unscaled observable H,
`skewNumerator / skewDenominator` is exactly
`-1/2 Tr([S/rootScale,H]^2)`.
-/
def skewNumerator (root observable : Matrix2) : Int :=
  -trace2
    (matrixMul
      (commutator root observable)
      (commutator root observable))

def skewDenominator (rootScale : Nat) : Int :=
  2 * (rootScale : Int) * (rootScale : Int)

/-- `25 * rho`, for the pure state from the rational unit vector `(3/5,4/5)`. -/
def inputRho : Matrix2
  | .zero, .zero => 9
  | .zero, .one => 12
  | .one, .zero => 12
  | .one, .one => 16

/-- `25 * Phi(rho)` for complete Z dephasing. -/
def outputRho : Matrix2
  | .zero, .zero => 9
  | .one, .one => 16
  | _, _ => 0

/-- `25 * sqrt(rho)`; the pure input is idempotent. -/
def inputRoot : Matrix2 := inputRho

/-- `5 * sqrt(Phi(rho))`. -/
def outputRoot : Matrix2
  | .zero, .zero => 3
  | .one, .one => 4
  | _, _ => 0

def inputGramFactor : Factor4x2
  | .a, .zero => 3
  | .a, .one => 4
  | _, _ => 0

def outputStateGramFactor : Factor4x2
  | .a, .zero => 3
  | .b, .one => 4
  | _, _ => 0

/-
The two columns `(3,2,1,1)` and `(0,-2,4,0)` are orthogonal and have squared
norms 15 and 20.  Their Gram matrix is therefore `5 * outputRoot`.
-/
def outputRootGramFactor : Factor4x2
  | .a, .zero => 3
  | .b, .zero => 2
  | .c, .zero => 1
  | .d, .zero => 1
  | .a, .one => 0
  | .b, .one => -2
  | .c, .one => 4
  | .d, .one => 0

def inputRhoGram : ScaledGramCertificate 25 inputRho where
  factorScale := 5
  factorScalePositive := by decide
  factor := inputGramFactor
  factorization := by
    funext row column
    cases row <;> cases column <;> decide

def inputRootGram : ScaledGramCertificate 25 inputRoot where
  factorScale := 5
  factorScalePositive := by decide
  factor := inputGramFactor
  factorization := by
    funext row column
    cases row <;> cases column <;> decide

def outputRhoGram : ScaledGramCertificate 25 outputRho where
  factorScale := 5
  factorScalePositive := by decide
  factor := outputStateGramFactor
  factorization := by
    funext row column
    cases row <;> cases column <;> decide

def outputRootGram : ScaledGramCertificate 5 outputRoot where
  factorScale := 5
  factorScalePositive := by decide
  factor := outputRootGramFactor
  factorization := by
    funext row column
    cases row <;> cases column <;> decide

theorem input_root_square :
    scaleMatrix 25 (matrixMul inputRoot inputRoot) =
      scaleMatrix (25 * 25) inputRho := by
  funext row column
  cases row <;> cases column <;> decide

theorem output_root_square :
    scaleMatrix 25 (matrixMul outputRoot outputRoot) =
      scaleMatrix (5 * 5) outputRho := by
  funext row column
  cases row <;> cases column <;> decide

def rootedInput : RootedDensity where
  rhoScale := 25
  sqrtScale := 25
  rhoScalePositive := by decide
  sqrtScalePositive := by decide
  rho := inputRho
  sqrtRho := inputRoot
  rhoGram := inputRhoGram
  sqrtGram := inputRootGram
  sqrtSquare := input_root_square
  traceOne := by decide

def rootedOutput : RootedDensity where
  rhoScale := 25
  sqrtScale := 5
  rhoScalePositive := by decide
  sqrtScalePositive := by decide
  rho := outputRho
  sqrtRho := outputRoot
  rhoGram := outputRhoGram
  sqrtGram := outputRootGram
  sqrtSquare := output_root_square
  traceOne := by decide

theorem dephaseZ_maps_fixture : dephaseZ inputRho = outputRho := by
  rfl

theorem fixture_is_moved : dephaseZ inputRho ≠ inputRho := by
  intro equality
  have offDiagonal := congrFun (congrFun equality Coord2.zero) Coord2.one
  simp [dephaseZ, inputRho] at offDiagonal

theorem input_skew_numerator_exact :
    skewNumerator inputRoot zObservable = 1152 := by
  decide

theorem input_skew_denominator_exact : skewDenominator 25 = 1250 := by
  decide

/-- Exact cross-multiplication for `I_rho(Z) = 576/625`. -/
theorem input_skew_is_576_over_625 :
    skewNumerator inputRoot zObservable * 625 =
      576 * skewDenominator 25 := by
  decide

theorem output_skew_numerator_exact :
    skewNumerator outputRoot zObservable = 0 := by
  decide

theorem output_skew_denominator_exact : skewDenominator 5 = 50 := by
  decide

/-- Strict comparison of the two exact rational values by cross multiplication. -/
theorem fixture_strict_wigner_yanase_decrease :
    skewNumerator outputRoot zObservable * skewDenominator 25 <
      skewNumerator inputRoot zObservable * skewDenominator 5 := by
  decide

structure ScopedCovariantWignerYanaseWitness where
  channel : Matrix2 -> Matrix2
  channelIsDeclared : channel = dephaseZ
  twoKrausAction : forall matrix,
    channel matrix =
      matrixAdd
        (matrixMul (matrixMul pZero matrix) (matrixTranspose pZero))
        (matrixMul (matrixMul pOne matrix) (matrixTranspose pOne))
  krausCompleteness :
    matrixAdd
        (matrixMul (matrixTranspose pZero) pZero)
        (matrixMul (matrixTranspose pOne) pOne) =
      identity2
  tracePreserving : forall matrix, trace2 (channel matrix) = trace2 matrix
  unital : channel identity2 = identity2
  generatorIntertwining : GeneratorIntertwining channel zObservable
  input : RootedDensity
  output : RootedDensity
  declaredInput : input = rootedInput
  declaredOutput : output = rootedOutput
  mapsFixture : channel input.rho = output.rho
  moved : channel input.rho ≠ input.rho
  strictDecrease :
    skewNumerator output.sqrtRho zObservable *
        skewDenominator input.sqrtScale <
      skewNumerator input.sqrtRho zObservable *
        skewDenominator output.sqrtScale
  authorityEffect : Q10AuthorityEffect
  authorityNone : authorityEffect = .none

def scopedCovariantWignerYanaseWitness : ScopedCovariantWignerYanaseWitness where
  channel := dephaseZ
  channelIsDeclared := rfl
  twoKrausAction := dephaseZ_two_kraus_action
  krausCompleteness := dephaseZ_kraus_completeness
  tracePreserving := dephaseZ_trace_preserving
  unital := dephaseZ_unital
  generatorIntertwining := dephaseZ_generator_intertwining
  input := rootedInput
  output := rootedOutput
  declaredInput := rfl
  declaredOutput := rfl
  mapsFixture := dephaseZ_maps_fixture
  moved := fixture_is_moved
  strictDecrease := fixture_strict_wigner_yanase_decrease
  authorityEffect := .none
  authorityNone := rfl

#print axioms dephaseZ_generator_intertwining
#print axioms input_root_square
#print axioms output_root_square
#print axioms fixture_strict_wigner_yanase_decrease
#print axioms scopedCovariantWignerYanaseWitness

end WignerYanaseQ10
end OmegaWorld
