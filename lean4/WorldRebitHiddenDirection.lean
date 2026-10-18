


namespace OmegaWorld
namespace RebitQ9

inductive Q9AuthorityEffect where
  | none
  deriving DecidableEq

inductive RebitCoord where
  | zero
  | one
  deriving DecidableEq

inductive JointCoord where
  | zeroZero
  | zeroOne
  | oneZero
  | oneOne
  deriving DecidableEq

inductive LocalSymBasis where
  | zeroDiagonal
  | oneDiagonal
  | plusProjectorScaled
  deriving DecidableEq

abbrev Matrix2 := RebitCoord -> RebitCoord -> Int
abbrev Matrix4 := JointCoord -> JointCoord -> Int

def leftCoord : JointCoord -> RebitCoord
  | .zeroZero => .zero
  | .zeroOne => .zero
  | .oneZero => .one
  | .oneOne => .one

def rightCoord : JointCoord -> RebitCoord
  | .zeroZero => .zero
  | .zeroOne => .one
  | .oneZero => .zero
  | .oneOne => .one

def jEntry : Matrix2
  | .zero, .zero => 0
  | .zero, .one => -1
  | .one, .zero => 1
  | .one, .one => 0

def deltaEntry : Matrix4 := fun row column =>
  jEntry (leftCoord row) (leftCoord column) *
    jEntry (rightCoord row) (rightCoord column)

def localBasisEntry : LocalSymBasis -> Matrix2
  | .zeroDiagonal, .zero, .zero => 1
  | .zeroDiagonal, _, _ => 0
  | .oneDiagonal, .one, .one => 1
  | .oneDiagonal, _, _ => 0
  | .plusProjectorScaled, _, _ => 1

def productEntry (left right : LocalSymBasis) : Matrix4 := fun row column =>
  localBasisEntry left (leftCoord row) (leftCoord column) *
    localBasisEntry right (rightCoord row) (rightCoord column)

def productMatrixEntry (left right : Matrix2) : Matrix4 := fun row column =>
  left (leftCoord row) (leftCoord column) *
    right (rightCoord row) (rightCoord column)

def Symmetric2 (matrix : Matrix2) : Prop :=
  forall row column, matrix row column = matrix column row

def rowInner (left right : Matrix4) : JointCoord -> Int
  | .zeroZero =>
      left .zeroZero .zeroZero * right .zeroZero .zeroZero +
      left .zeroZero .zeroOne * right .zeroZero .zeroOne +
      left .zeroZero .oneZero * right .zeroZero .oneZero +
      left .zeroZero .oneOne * right .zeroZero .oneOne
  | .zeroOne =>
      left .zeroOne .zeroZero * right .zeroOne .zeroZero +
      left .zeroOne .zeroOne * right .zeroOne .zeroOne +
      left .zeroOne .oneZero * right .zeroOne .oneZero +
      left .zeroOne .oneOne * right .zeroOne .oneOne
  | .oneZero =>
      left .oneZero .zeroZero * right .oneZero .zeroZero +
      left .oneZero .zeroOne * right .oneZero .zeroOne +
      left .oneZero .oneZero * right .oneZero .oneZero +
      left .oneZero .oneOne * right .oneZero .oneOne
  | .oneOne =>
      left .oneOne .zeroZero * right .oneOne .zeroZero +
      left .oneOne .zeroOne * right .oneOne .zeroOne +
      left .oneOne .oneZero * right .oneOne .oneZero +
      left .oneOne .oneOne * right .oneOne .oneOne

def frobeniusInner (left right : Matrix4) : Int :=
  rowInner left right .zeroZero +
    rowInner left right .zeroOne +
    rowInner left right .oneZero +
    rowInner left right .oneOne

def identityEntry : Matrix4 := fun row column => if row = column then 1 else 0

def matrixMulEntry (left right : Matrix4) : Matrix4 := fun row column =>
  left row .zeroZero * right .zeroZero column +
    left row .zeroOne * right .zeroOne column +
    left row .oneZero * right .oneZero column +
    left row .oneOne * right .oneOne column

def pPlusScaled : Matrix4 := fun row column =>
  identityEntry row column + deltaEntry row column

def pMinusScaled : Matrix4 := fun row column =>
  identityEntry row column - deltaEntry row column

def rhoPlusScaled : Matrix4 := fun row column =>
  4 * identityEntry row column + 2 * deltaEntry row column

def rhoMinusScaled : Matrix4 := fun row column =>
  4 * identityEntry row column - 2 * deltaEntry row column

def trace4 (matrix : Matrix4) : Int :=
  matrix .zeroZero .zeroZero +
    matrix .zeroOne .zeroOne +
    matrix .oneZero .oneZero +
    matrix .oneOne .oneOne

theorem delta_symmetric (row column : JointCoord) :
    deltaEntry row column = deltaEntry column row := by
  cases row <;> cases column <;> decide

theorem delta_nonzero : deltaEntry .zeroZero .oneOne = 1 := by
  decide

theorem product_basis_invisible (left right : LocalSymBasis) :
    frobeniusInner (productEntry left right) deltaEntry = 0 := by
  cases left <;> cases right <;> decide

theorem all_symmetric_product_matrices_invisible
    (left right : Matrix2) (leftSymmetric : Symmetric2 left)
    (rightSymmetric : Symmetric2 right) :
    frobeniusInner (productMatrixEntry left right) deltaEntry = 0 := by
  have leftOffDiagonal := leftSymmetric .zero .one
  have rightOffDiagonal := rightSymmetric .zero .one
  simp [frobeniusInner, rowInner, productMatrixEntry, deltaEntry, jEntry,
    leftCoord, rightCoord, leftOffDiagonal, rightOffDiagonal]
  omega

theorem pPlus_scaled_idempotent (row column : JointCoord) :
    matrixMulEntry pPlusScaled pPlusScaled row column =
      2 * pPlusScaled row column := by
  cases row <;> cases column <;> decide

theorem pMinus_scaled_idempotent (row column : JointCoord) :
    matrixMulEntry pMinusScaled pMinusScaled row column =
      2 * pMinusScaled row column := by
  cases row <;> cases column <;> decide

theorem rho_scaled_unit_trace :
    trace4 rhoPlusScaled = 16 ∧ trace4 rhoMinusScaled = 16 := by
  decide

theorem rho_scaled_distinct :
    rhoPlusScaled .zeroZero .oneOne ≠ rhoMinusScaled .zeroZero .oneOne := by
  decide

theorem rho_product_statistics_equal (left right : LocalSymBasis) :
    frobeniusInner (productEntry left right) rhoPlusScaled =
      frobeniusInner (productEntry left right) rhoMinusScaled := by
  cases left <;> cases right <;> decide

theorem rho_all_symmetric_product_statistics_equal
    (left right : Matrix2) (leftSymmetric : Symmetric2 left)
    (rightSymmetric : Symmetric2 right) :
    frobeniusInner (productMatrixEntry left right) rhoPlusScaled =
      frobeniusInner (productMatrixEntry left right) rhoMinusScaled := by
  have invisible := all_symmetric_product_matrices_invisible
    left right leftSymmetric rightSymmetric
  simp [frobeniusInner, rowInner, productMatrixEntry, rhoPlusScaled,
    rhoMinusScaled, identityEntry, deltaEntry, jEntry, leftCoord, rightCoord]
    at invisible ⊢
  omega

theorem rho_pPlus_scaled_separator :
    frobeniusInner pPlusScaled rhoPlusScaled = 24 ∧
      frobeniusInner pPlusScaled rhoMinusScaled = 8 := by
  decide

structure HiddenDirectionWitness where
  delta : Matrix4
  delta_is_declared : delta = deltaEntry
  symmetric : forall row column, delta row column = delta column row
  nonzero : delta .zeroZero .oneOne = 1
  productInvisible : forall left right,
    frobeniusInner (productEntry left right) delta = 0
  allSymmetricProductInvisible : forall left right,
    Symmetric2 left → Symmetric2 right →
      frobeniusInner (productMatrixEntry left right) delta = 0
  authorityEffect : Q9AuthorityEffect
  authority_none : authorityEffect = .none

def hiddenDirectionWitness : HiddenDirectionWitness where
  delta := deltaEntry
  delta_is_declared := rfl
  symmetric := delta_symmetric
  nonzero := delta_nonzero
  productInvisible := product_basis_invisible
  allSymmetricProductInvisible := all_symmetric_product_matrices_invisible
  authorityEffect := .none
  authority_none := rfl

structure RhoPairWitness where
  scale : Nat
  scale_is_sixteen : scale = 16
  rhoPlus : Matrix4
  rhoMinus : Matrix4
  plus_is_declared : rhoPlus = rhoPlusScaled
  minus_is_declared : rhoMinus = rhoMinusScaled
  traceScaled : trace4 rhoPlus = (scale : Int) ∧
    trace4 rhoMinus = (scale : Int)
  distinct : rhoPlus .zeroZero .oneOne ≠ rhoMinus .zeroZero .oneOne
  sameProductStatistics : forall left right,
    frobeniusInner (productEntry left right) rhoPlus =
      frobeniusInner (productEntry left right) rhoMinus
  allSymmetricProductStatistics : forall left right,
    Symmetric2 left → Symmetric2 right →
      frobeniusInner (productMatrixEntry left right) rhoPlus =
        frobeniusInner (productMatrixEntry left right) rhoMinus
  pPlusScaledSeparator : frobeniusInner pPlusScaled rhoPlus = 24 ∧
    frobeniusInner pPlusScaled rhoMinus = 8
  authorityEffect : Q9AuthorityEffect
  authority_none : authorityEffect = .none

def rhoPairWitness : RhoPairWitness where
  scale := 16
  scale_is_sixteen := rfl
  rhoPlus := rhoPlusScaled
  rhoMinus := rhoMinusScaled
  plus_is_declared := rfl
  minus_is_declared := rfl
  traceScaled := rho_scaled_unit_trace
  distinct := rho_scaled_distinct
  sameProductStatistics := rho_product_statistics_equal
  allSymmetricProductStatistics := rho_all_symmetric_product_statistics_equal
  pPlusScaledSeparator := rho_pPlus_scaled_separator
  authorityEffect := .none
  authority_none := rfl

#print axioms hiddenDirectionWitness
#print axioms rhoPairWitness
#print axioms all_symmetric_product_matrices_invisible
#print axioms rho_all_symmetric_product_statistics_equal
#print axioms rho_pPlus_scaled_separator

end RebitQ9
end OmegaWorld

private def l5aProvenance : String :=
  "Origin: lean4/WorldRebitHiddenDirection.lean Claim: delta_symmetric AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
