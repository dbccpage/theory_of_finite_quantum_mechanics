

namespace HilbertWalk.CliffordPauliConjugationAndTGateOrbit

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


theorem hadamard_squared : mat_mul mat_H mat_H = mat_smul 2 mat_I := by rfl

theorem hadamard_conjugates_X_to_Z :
    mat_mul (mat_mul mat_H mat_X) mat_H = mat_smul 2 mat_Z := by rfl

theorem hadamard_conjugates_Z_to_X :
    mat_mul (mat_mul mat_H mat_Z) mat_H = mat_smul 2 mat_X := by rfl

theorem hadamard_conjugates_Y_to_neg_Y :
    mat_mul (mat_mul mat_H mat_Y) mat_H = mat_smul (-2) mat_Y := by rfl


theorem phase_fourth_is_I :
    mat_mul (mat_mul (mat_mul mat_S mat_S) mat_S) mat_S = mat_I := by rfl

theorem phase_conjugates_X_to_Y :
    mat_mul (mat_mul mat_S mat_X) (mat_adj mat_S) = mat_Y := by rfl

theorem phase_conjugates_Y_to_neg_X :
    mat_mul (mat_mul mat_S mat_Y) (mat_adj mat_S) = mat_smul (-1) mat_X := by rfl

theorem phase_conjugates_Z_to_Z :
    mat_mul (mat_mul mat_S mat_Z) (mat_adj mat_S) = mat_Z := by rfl


def mat_X_plus_Y : Mat2 := mat_add mat_X mat_Y

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

end HilbertWalk.CliffordPauliConjugationAndTGateOrbit

private def l5aProvenance : String :=
  "Origin: lean4/CliffordPauliConjugationAndTGateOrbit.lean Claim: hadamard_squared AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
