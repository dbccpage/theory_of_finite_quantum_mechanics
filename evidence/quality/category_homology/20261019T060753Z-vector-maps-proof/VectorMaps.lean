import Mathlib.Data.Matrix.Mul
import Mathlib.Algebra.Field.Rat
import Mathlib.Algebra.BigOperators.Group.Finset.Interval

/-! AuthorityEffect: None. Exact finite coordinate operations, ordered context
guards and matrix-vector sums. Rat-valued operations have canonical results;
the Rust raw-pair admission and Q backend correspondence are separate reviewed
obligations. Kind is a static Rust parameter; wire data does not encode it.
No Rust/MIR extraction, basis authentication or allocator theorem is claimed.
-/
namespace TFQM.VectorMaps

open scoped BigOperators

structure Context where
  degree : Int
  family : String
  size : Nat

inductive Refusal where
  | degree (expected got : Int)
  | basis
  | dimension (expected got : Nat)
  deriving DecidableEq

def compatible (left right : Context) : Except Refusal Unit :=
  if left.degree ≠ right.degree then .error (.degree left.degree right.degree)
  else if left.family ≠ right.family then .error .basis
  else if left.size ≠ right.size then .error (.dimension left.size right.size)
  else .ok ()

theorem compatible_iff (left right : Context) :
    compatible left right = .ok () ↔
      left.degree = right.degree ∧ left.family = right.family ∧ left.size = right.size := by
  by_cases degree : left.degree = right.degree <;>
    by_cases family : left.family = right.family <;>
      by_cases size : left.size = right.size <;> simp [compatible, degree, family, size]

theorem degree_first (left right : Context) (different : left.degree ≠ right.degree) :
    compatible left right = .error (.degree left.degree right.degree) := by
  simp [compatible, different]

theorem basis_after_degree (left right : Context) (same : left.degree = right.degree)
    (different : left.family ≠ right.family) : compatible left right = .error .basis := by
  simp [compatible, same, different]

theorem length_after_context (left right : Context) (degree : left.degree = right.degree)
    (family : left.family = right.family) (different : left.size ≠ right.size) :
    compatible left right = .error (.dimension left.size right.size) := by
  simp [compatible, degree, family, different]

def zeroValues (n : Nat) : Fin n → ℚ := fun _ => 0
def addValues {n : Nat} (left right : Fin n → ℚ) : Fin n → ℚ := fun i => left i + right i
def subValues {n : Nat} (left right : Fin n → ℚ) : Fin n → ℚ := fun i => left i - right i
def scaleValues {n : Nat} (scalar : ℚ) (value : Fin n → ℚ) : Fin n → ℚ :=
  fun i => value i * scalar

theorem zero_entry (n : Nat) (i : Fin n) : zeroValues n i = 0 := rfl
theorem add_entry {n : Nat} (left right : Fin n → ℚ) (i : Fin n) :
    addValues left right i = left i + right i := rfl
theorem sub_entry {n : Nat} (left right : Fin n → ℚ) (i : Fin n) :
    subValues left right i = left i - right i := rfl
theorem scalar_entry {n : Nat} (scalar : ℚ) (value : Fin n → ℚ) (i : Fin n) :
    scaleValues scalar value i = value i * scalar := rfl

theorem subtract_then_add {n : Nat} (left right : Fin n → ℚ) :
    addValues (subValues left right) right = left := by
  funext i
  exact sub_add_cancel (left i) (right i)

theorem scaled_sum {n : Nat} (scalar : ℚ) (left right : Fin n → ℚ) :
    scaleValues scalar (addValues left right) =
      addValues (scaleValues scalar left) (scaleValues scalar right) := by
  funext i
  exact add_mul (left i) (right i) scalar

def dotPrefix (row column : Nat → ℚ) : Nat → ℚ
  | 0 => 0
  | n + 1 => dotPrefix row column n + row n * column n

theorem dot_prefix_spec (row column : Nat → ℚ) (n : Nat) :
    dotPrefix row column n = ∑ i ∈ Finset.range n, row i * column i := by
  induction n with
  | zero => simp [dotPrefix]
  | succ n ih => simp [dotPrefix, Finset.sum_range_succ, ih]

theorem matrix_entry {m n : Nat} (matrix : Matrix (Fin m) (Fin n) ℚ)
    (vector : Fin n → ℚ) (row : Fin m) :
    (matrix *ᵥ vector) row = ∑ column, matrix row column * vector column := rfl

theorem matrix_zero {m n : Nat} (matrix : Matrix (Fin m) (Fin n) ℚ) :
    matrix *ᵥ zeroValues n = zeroValues m := Matrix.mulVec_zero matrix

theorem matrix_add {m n : Nat} (matrix : Matrix (Fin m) (Fin n) ℚ)
    (left right : Fin n → ℚ) :
    matrix *ᵥ addValues left right = addValues (matrix *ᵥ left) (matrix *ᵥ right) :=
  Matrix.mulVec_add matrix left right

theorem matrix_scale {m n : Nat} (matrix : Matrix (Fin m) (Fin n) ℚ)
    (scalar : ℚ) (vector : Fin n → ℚ) :
    matrix *ᵥ scaleValues scalar vector = scaleValues scalar (matrix *ᵥ vector) := by
  have before : scaleValues scalar vector = scalar • vector := by
    funext i
    exact mul_comm (vector i) scalar
  have after : scaleValues scalar (matrix *ᵥ vector) = scalar • (matrix *ᵥ vector) := by
    funext i
    exact mul_comm ((matrix *ᵥ vector) i) scalar
  rw [before, after]
  exact Matrix.mulVec_smul matrix scalar vector

#print axioms compatible_iff
#print axioms degree_first
#print axioms basis_after_degree
#print axioms length_after_context
#print axioms zero_entry
#print axioms add_entry
#print axioms sub_entry
#print axioms scalar_entry
#print axioms subtract_then_add
#print axioms scaled_sum
#print axioms dot_prefix_spec
#print axioms matrix_entry
#print axioms matrix_zero
#print axioms matrix_add
#print axioms matrix_scale

end TFQM.VectorMaps
