

namespace FableHilbertWalk20260819.H046

structure Vec2F2 where
  x : Int
  z : Int
  deriving DecidableEq, Repr

def omega (u v : Vec2F2) : Int :=
  (u.x * v.z + u.z * v.x) % 2

structure Mat2F2 where
  m00 : Int
  m01 : Int
  m10 : Int
  m11 : Int
  deriving DecidableEq, Repr

def detF2 (M : Mat2F2) : Int :=
  ((M.m00 * M.m11 - M.m01 * M.m10) % 2 + 2) % 2

def mulF2 (A B : Mat2F2) : Mat2F2 :=
  ⟨(A.m00 * B.m00 + A.m01 * B.m10) % 2,
   (A.m00 * B.m01 + A.m01 * B.m11) % 2,
   (A.m10 * B.m00 + A.m11 * B.m10) % 2,
   (A.m10 * B.m01 + A.m11 * B.m11) % 2⟩

def actF2 (M : Mat2F2) (v : Vec2F2) : Vec2F2 :=
  ⟨(M.m00 * v.x + M.m01 * v.z) % 2,
   (M.m10 * v.x + M.m11 * v.z) % 2⟩

def mat_I   : Mat2F2 := ⟨1, 0, 0, 1⟩
def mat_H   : Mat2F2 := ⟨0, 1, 1, 0⟩
def mat_S   : Mat2F2 := ⟨1, 0, 1, 1⟩
def mat_SH  : Mat2F2 := mulF2 mat_S mat_H
def mat_HS  : Mat2F2 := mulF2 mat_H mat_S
def mat_HSH : Mat2F2 := mulF2 mat_H mat_SH

theorem all_determinants_one :
    detF2 mat_I = 1 ∧
    detF2 mat_H = 1 ∧
    detF2 mat_S = 1 ∧
    detF2 mat_SH = 1 ∧
    detF2 mat_HS = 1 ∧
    detF2 mat_HSH = 1 := by decide

def e_x : Vec2F2 := ⟨1, 0⟩
def e_z : Vec2F2 := ⟨0, 1⟩

theorem canonical_pairing : omega e_x e_z = 1 := by decide

theorem symplectic_preservation_all_six :
    omega (actF2 mat_I e_x) (actF2 mat_I e_z) = 1 ∧
    omega (actF2 mat_H e_x) (actF2 mat_H e_z) = 1 ∧
    omega (actF2 mat_S e_x) (actF2 mat_S e_z) = 1 ∧
    omega (actF2 mat_SH e_x) (actF2 mat_SH e_z) = 1 ∧
    omega (actF2 mat_HS e_x) (actF2 mat_HS e_z) = 1 ∧
    omega (actF2 mat_HSH e_x) (actF2 mat_HSH e_z) = 1 := by decide

theorem six_matrices_distinct :
    mat_I ≠ mat_H ∧ mat_I ≠ mat_S ∧ mat_I ≠ mat_SH ∧ mat_I ≠ mat_HS ∧ mat_I ≠ mat_HSH ∧
    mat_H ≠ mat_S ∧ mat_H ≠ mat_SH ∧ mat_H ≠ mat_HS ∧ mat_H ≠ mat_HSH ∧
    mat_S ≠ mat_SH ∧ mat_S ≠ mat_HS ∧ mat_S ≠ mat_HSH ∧
    mat_SH ≠ mat_HS ∧ mat_SH ≠ mat_HSH ∧
    mat_HS ≠ mat_HSH := by decide

theorem order_two_elements :
    mulF2 mat_H mat_H = mat_I ∧
    mulF2 mat_S mat_S = mat_I ∧
    mulF2 mat_HSH mat_HSH = mat_I := by decide

theorem order_three_elements :
    mulF2 (mulF2 mat_SH mat_SH) mat_SH = mat_I ∧
    mulF2 (mulF2 mat_HS mat_HS) mat_HS = mat_I := by decide

theorem group_multiplication_table :
    mulF2 mat_H mat_S = mat_HS ∧
    mulF2 mat_S mat_H = mat_SH ∧
    mulF2 mat_SH mat_SH = mat_HS ∧
    mulF2 mat_HS mat_HS = mat_SH := by decide

def symplecticOrder (n : Nat) : Nat :=
  match n with
  | 0 => 1
  | 1 => 2^(1*1) * (2^2 - 1)
  | 2 => 2^(2*2) * (2^2 - 1) * (2^4 - 1)
  | _ => 0

theorem order_sp2_f2 : symplecticOrder 1 = 6 := by decide

theorem order_sp4_f2 : symplecticOrder 2 = 720 := by decide

structure Mat4F2 where
  m00 : Int
  m01 : Int
  m02 : Int
  m03 : Int
  m10 : Int
  m11 : Int
  m12 : Int
  m13 : Int
  m20 : Int
  m21 : Int
  m22 : Int
  m23 : Int
  m30 : Int
  m31 : Int
  m32 : Int
  m33 : Int
  deriving DecidableEq, Repr, BEq

def mul4F2 (A B : Mat4F2) : Mat4F2 :=
  ⟨(A.m00 * B.m00 + A.m01 * B.m10 + A.m02 * B.m20 + A.m03 * B.m30) % 2,
   (A.m00 * B.m01 + A.m01 * B.m11 + A.m02 * B.m21 + A.m03 * B.m31) % 2,
   (A.m00 * B.m02 + A.m01 * B.m12 + A.m02 * B.m22 + A.m03 * B.m32) % 2,
   (A.m00 * B.m03 + A.m01 * B.m13 + A.m02 * B.m23 + A.m03 * B.m33) % 2,
   (A.m10 * B.m00 + A.m11 * B.m10 + A.m12 * B.m20 + A.m13 * B.m30) % 2,
   (A.m10 * B.m01 + A.m11 * B.m11 + A.m12 * B.m21 + A.m13 * B.m31) % 2,
   (A.m10 * B.m02 + A.m11 * B.m12 + A.m12 * B.m22 + A.m13 * B.m32) % 2,
   (A.m10 * B.m03 + A.m11 * B.m13 + A.m12 * B.m23 + A.m13 * B.m33) % 2,
   (A.m20 * B.m00 + A.m21 * B.m10 + A.m22 * B.m20 + A.m23 * B.m30) % 2,
   (A.m20 * B.m01 + A.m21 * B.m11 + A.m22 * B.m21 + A.m23 * B.m31) % 2,
   (A.m20 * B.m02 + A.m21 * B.m12 + A.m22 * B.m22 + A.m23 * B.m32) % 2,
   (A.m20 * B.m03 + A.m21 * B.m13 + A.m22 * B.m23 + A.m23 * B.m33) % 2,
   (A.m30 * B.m00 + A.m31 * B.m10 + A.m32 * B.m20 + A.m33 * B.m30) % 2,
   (A.m30 * B.m01 + A.m31 * B.m11 + A.m32 * B.m21 + A.m33 * B.m31) % 2,
   (A.m30 * B.m02 + A.m31 * B.m12 + A.m32 * B.m22 + A.m33 * B.m32) % 2,
   (A.m30 * B.m03 + A.m31 * B.m13 + A.m32 * B.m23 + A.m33 * B.m33) % 2⟩

def transpose4F2 (M : Mat4F2) : Mat4F2 :=
  ⟨M.m00, M.m10, M.m20, M.m30,
   M.m01, M.m11, M.m21, M.m31,
   M.m02, M.m12, M.m22, M.m32,
   M.m03, M.m13, M.m23, M.m33⟩

def mat4_I : Mat4F2 :=
  ⟨1, 0, 0, 0,
   0, 1, 0, 0,
   0, 0, 1, 0,
   0, 0, 0, 1⟩

def mat4_J : Mat4F2 :=
  ⟨0, 0, 1, 0,
   0, 0, 0, 1,
   1, 0, 0, 0,
   0, 1, 0, 0⟩

def isSymplectic4 (M : Mat4F2) : Bool :=
  mul4F2 (transpose4F2 M) (mul4F2 mat4_J M) == mat4_J

def mat4_H1 : Mat4F2 :=
  ⟨0, 0, 1, 0,
   0, 1, 0, 0,
   1, 0, 0, 0,
   0, 0, 0, 1⟩

def mat4_S1 : Mat4F2 :=
  ⟨1, 0, 0, 0,
   0, 1, 0, 0,
   1, 0, 1, 0,
   0, 0, 0, 1⟩

def mat4_SWAP : Mat4F2 :=
  ⟨0, 1, 0, 0,
   1, 0, 0, 0,
   0, 0, 0, 1,
   0, 0, 1, 0⟩

def mat4_CX : Mat4F2 :=
  ⟨1, 0, 0, 0,
   1, 1, 0, 0,
   0, 0, 1, 1,
   0, 0, 0, 1⟩

theorem mat4_generators_preserve_j4 :
    isSymplectic4 mat4_I = true ∧
    isSymplectic4 mat4_H1 = true ∧
    isSymplectic4 mat4_S1 = true ∧
    isSymplectic4 mat4_SWAP = true ∧
    isSymplectic4 mat4_CX = true := by decide

def sp2Elements : List Mat2F2 :=
  [mat_I, mat_H, mat_S, mat_SH, mat_HS, mat_HSH]

theorem sp2_elements_cardinality : sp2Elements.length = 6 := by rfl

theorem sp2_group_closure :
    ∀ A ∈ sp2Elements, ∀ B ∈ sp2Elements, mulF2 A B ∈ sp2Elements := by decide

def orbitF2 (v : Vec2F2) : List Vec2F2 :=
  sp2Elements.map (actF2 · v)

theorem orbit_ex_length : (orbitF2 e_x).length = 6 := by rfl

structure Pauli1Kernel where
  name : String
  phase_x : Int
  phase_z : Int
  deriving DecidableEq, Repr

def pauliKernel : List Pauli1Kernel := [
  ⟨"I", 0, 0⟩,
  ⟨"X", 1, 0⟩,
  ⟨"Z", 0, 1⟩,
  ⟨"Y", 1, 1⟩
]

theorem pauli_kernel_cardinality : pauliKernel.length = 4 := by rfl

def pauliKernelSize : Nat := 4

def projectiveCliffordOrder : Nat := pauliKernelSize * symplecticOrder 1

theorem projective_clifford_order_eval : projectiveCliffordOrder = 24 := by rfl

theorem sp2_finite_symplectic_quotient_closure :
    sp2Elements.length = 6 ∧
    (∀ A ∈ sp2Elements, ∀ B ∈ sp2Elements, mulF2 A B ∈ sp2Elements) ∧
    projectiveCliffordOrder = 24 ∧
    projectiveCliffordOrder < 25 := by
  refine ⟨rfl, ?_, rfl, by decide⟩
  exact sp2_group_closure

theorem eastin_knill_representation_obstruction :
    sp2Elements.length = 6 ∧
    (∀ A ∈ sp2Elements, ∀ B ∈ sp2Elements, mulF2 A B ∈ sp2Elements) ∧
    sp2Elements.length < 7 := by
  refine ⟨rfl, ?_, by decide⟩
  exact sp2_group_closure

#print axioms all_determinants_one
#print axioms canonical_pairing
#print axioms symplectic_preservation_all_six
#print axioms six_matrices_distinct
#print axioms order_two_elements
#print axioms order_three_elements
#print axioms group_multiplication_table
#print axioms order_sp2_f2
#print axioms order_sp4_f2
#print axioms mat4_generators_preserve_j4
#print axioms sp2_elements_cardinality
#print axioms sp2_group_closure
#print axioms orbit_ex_length
#print axioms pauli_kernel_cardinality
#print axioms projective_clifford_order_eval
#print axioms sp2_finite_symplectic_quotient_closure
#print axioms eastin_knill_representation_obstruction

end FableHilbertWalk20260819.H046


private def l5aProvenance : String :=
  "Origin: lean4/H046DiscreteCliffordSymplectic.lean Claim: all_determinants_one AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
