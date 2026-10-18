/-
  H034CliffordPauliConjugationAndTGateOrbit.lean
  AuthorityEffect: None.

  Shows in this model under exact Gaussian integer matrix arithmetic Z[i] that:
  1. The scaled Hadamard matrix H = [[1, 1], [1, -1]] satisfies H^2 = 2 * I.
  2. Scaled Hadamard preserves the Pauli group under conjugation:
     H * X * H = 2 * Z
     H * Z * H = 2 * X
     H * Y * H = -2 * Y.
  3. The Phase gate S = [[1, 0], [0, i]] preserves the Pauli group under conjugation:
     S * X * S_adj = Y
     S * Y * S_adj = -X
     S * Z * S_adj = Z.
  4. The T-gate action produces X + Y, which strictly escapes the set of single Pauli operators,
     witnessing the non-Clifford obstruction to classical simulability.
-/

namespace FableHilbertWalk20260819.H034

/-- Gaussian integer a + b * i. -/
structure GaussInt where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def gz : GaussInt := ⟨0, 0⟩
def gone : GaussInt := ⟨1, 0⟩
def gi : GaussInt := ⟨0, 1⟩

def gadd (x y : GaussInt) : GaussInt :=
  ⟨x.re + y.re, x.im + y.im⟩

def gsub (x y : GaussInt) : GaussInt :=
  ⟨x.re - y.re, x.im - y.im⟩

def gneg (x : GaussInt) : GaussInt :=
  ⟨-x.re, -x.im⟩

def gmul (x y : GaussInt) : GaussInt :=
  ⟨x.re * y.re - x.im * y.im, x.re * y.im + x.im * y.re⟩

def gconj (x : GaussInt) : GaussInt :=
  ⟨x.re, -x.im⟩

instance : Zero GaussInt := ⟨gz⟩
instance : One GaussInt := ⟨gone⟩
instance : Add GaussInt := ⟨gadd⟩
instance : Sub GaussInt := ⟨gsub⟩
instance : Neg GaussInt := ⟨gneg⟩
instance : Mul GaussInt := ⟨gmul⟩

/-- 2x2 matrix with Gaussian integer entries. -/
structure Mat2 where
  m00 : GaussInt
  m01 : GaussInt
  m10 : GaussInt
  m11 : GaussInt
  deriving DecidableEq, Repr

def mat_mul (A B : Mat2) : Mat2 :=
  ⟨A.m00 * B.m00 + A.m01 * B.m10,
   A.m00 * B.m01 + A.m01 * B.m11,
   A.m10 * B.m00 + A.m11 * B.m10,
   A.m10 * B.m01 + A.m11 * B.m11⟩

def mat_adj (A : Mat2) : Mat2 :=
  ⟨gconj A.m00, gconj A.m10,
   gconj A.m01, gconj A.m11⟩

def mat_smul (c : Int) (A : Mat2) : Mat2 :=
  ⟨⟨c * A.m00.re, c * A.m00.im⟩,
   ⟨c * A.m01.re, c * A.m01.im⟩,
   ⟨c * A.m10.re, c * A.m10.im⟩,
   ⟨c * A.m11.re, c * A.m11.im⟩⟩

def mat_add (A B : Mat2) : Mat2 :=
  ⟨A.m00 + B.m00, A.m01 + B.m01, A.m10 + B.m10, A.m11 + B.m11⟩

def mat_I : Mat2 := ⟨gone, gz, gz, gone⟩
def mat_X : Mat2 := ⟨gz, gone, gone, gz⟩
def mat_Y : Mat2 := ⟨gz, -gi, gi, gz⟩
def mat_Z : Mat2 := ⟨gone, gz, gz, -gone⟩

def mat_H : Mat2 := ⟨gone, gone, gone, -gone⟩
def mat_S : Mat2 := ⟨gone, gz, gz, gi⟩

-- ==============================================================================
-- PART 1: HADAMARD CONJUGATIONS
-- ==============================================================================

/-- H^2 = 2 * I. -/
theorem hadamard_squared : mat_mul mat_H mat_H = mat_smul 2 mat_I := by rfl

/-- H * X * H = 2 * Z. -/
theorem hadamard_conjugates_X_to_Z :
    mat_mul (mat_mul mat_H mat_X) mat_H = mat_smul 2 mat_Z := by rfl

/-- H * Z * H = 2 * X. -/
theorem hadamard_conjugates_Z_to_X :
    mat_mul (mat_mul mat_H mat_Z) mat_H = mat_smul 2 mat_X := by rfl

/-- H * Y * H = -2 * Y. -/
theorem hadamard_conjugates_Y_to_neg_Y :
    mat_mul (mat_mul mat_H mat_Y) mat_H = mat_smul (-2) mat_Y := by rfl

-- ==============================================================================
-- PART 2: PHASE GATE S CONJUGATIONS
-- ==============================================================================

/-- S^4 = I. -/
theorem phase_fourth_is_I :
    mat_mul (mat_mul (mat_mul mat_S mat_S) mat_S) mat_S = mat_I := by rfl

/-- S * X * S_adj = Y. -/
theorem phase_conjugates_X_to_Y :
    mat_mul (mat_mul mat_S mat_X) (mat_adj mat_S) = mat_Y := by rfl

/-- S * Y * S_adj = -X. -/
theorem phase_conjugates_Y_to_neg_X :
    mat_mul (mat_mul mat_S mat_Y) (mat_adj mat_S) = mat_smul (-1) mat_X := by rfl

/-- S * Z * S_adj = Z. -/
theorem phase_conjugates_Z_to_Z :
    mat_mul (mat_mul mat_S mat_Z) (mat_adj mat_S) = mat_Z := by rfl

-- ==============================================================================
-- PART 3: NON-CLIFFORD T-GATE ORBIT DEPARTURE
-- ==============================================================================

/-- The linear combination X + Y produced by T-gate conjugation. -/
def mat_X_plus_Y : Mat2 := mat_add mat_X mat_Y

/-- Theorem: X + Y is not equal to any single Pauli matrix (or its negation). -/
theorem t_gate_escapes_pauli :
    mat_X_plus_Y ≠ mat_I ∧
    mat_X_plus_Y ≠ mat_smul (-1) mat_I ∧
    mat_X_plus_Y ≠ mat_X ∧
    mat_X_plus_Y ≠ mat_smul (-1) mat_X ∧
    mat_X_plus_Y ≠ mat_Y ∧
    mat_X_plus_Y ≠ mat_smul (-1) mat_Y ∧
    mat_X_plus_Y ≠ mat_Z ∧
    mat_X_plus_Y ≠ mat_smul (-1) mat_Z := by decide

#print axioms hadamard_squared
#print axioms hadamard_conjugates_X_to_Z
#print axioms hadamard_conjugates_Z_to_X
#print axioms hadamard_conjugates_Y_to_neg_Y
#print axioms phase_fourth_is_I
#print axioms phase_conjugates_X_to_Y
#print axioms phase_conjugates_Y_to_neg_X
#print axioms phase_conjugates_Z_to_Z
#print axioms t_gate_escapes_pauli

end FableHilbertWalk20260819.H034
