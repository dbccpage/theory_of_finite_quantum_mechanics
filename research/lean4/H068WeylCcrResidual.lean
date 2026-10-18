

namespace FableHilbertWalk20260819.H068


structure Mat2 where
  m00 : Int
  m01 : Int
  m10 : Int
  m11 : Int
  deriving DecidableEq, Repr

def tr2 (A : Mat2) : Int := A.m00 + A.m11

def mul2 (A B : Mat2) : Mat2 :=
  ⟨A.m00 * B.m00 + A.m01 * B.m10,
   A.m00 * B.m01 + A.m01 * B.m11,
   A.m10 * B.m00 + A.m11 * B.m10,
   A.m10 * B.m01 + A.m11 * B.m11⟩

def sub2 (A B : Mat2) : Mat2 :=
  ⟨A.m00 - B.m00, A.m01 - B.m01,
   A.m10 - B.m10, A.m11 - B.m11⟩

def smul2 (c : Int) (A : Mat2) : Mat2 :=
  ⟨c * A.m00, c * A.m01, c * A.m10, c * A.m11⟩

def comm2 (A B : Mat2) : Mat2 := sub2 (mul2 A B) (mul2 B A)

def eye2 : Mat2 := ⟨1, 0, 0, 1⟩

theorem tr_mul_comm2 (A B : Mat2) : tr2 (mul2 A B) = tr2 (mul2 B A) := by
  dsimp [tr2, mul2]
  have h0 : A.m00 * B.m00 = B.m00 * A.m00 := by rw [Int.mul_comm]
  have h1 : A.m11 * B.m11 = B.m11 * A.m11 := by rw [Int.mul_comm]
  have h2 : A.m01 * B.m10 = B.m10 * A.m01 := by rw [Int.mul_comm]
  have h3 : A.m10 * B.m01 = B.m01 * A.m10 := by rw [Int.mul_comm]
  omega

theorem tr_comm2_vanishes (Q P : Mat2) : tr2 (comm2 Q P) = 0 := by
  dsimp [comm2, sub2, tr2]
  have h := tr_mul_comm2 Q P
  dsimp [tr2] at h
  omega

theorem tr_smul_eye2 (c : Int) : tr2 (smul2 c eye2) = 2 * c := by
  dsimp [tr2, smul2, eye2]
  omega

theorem ccr_obstruction_d2 (Q P : Mat2) (c : Int) (hc : c ≠ 0) :
    comm2 Q P ≠ smul2 c eye2 := by
  intro h
  have h_tr : tr2 (comm2 Q P) = tr2 (smul2 c eye2) := congrArg tr2 h
  rw [tr_comm2_vanishes Q P, tr_smul_eye2 c] at h_tr
  have : c = 0 := by omega
  contradiction



structure Mat3 where
  m00 : Int
  m01 : Int
  m02 : Int
  m10 : Int
  m11 : Int
  m12 : Int
  m20 : Int
  m21 : Int
  m22 : Int
  deriving DecidableEq, Repr

def tr3 (A : Mat3) : Int := A.m00 + A.m11 + A.m22

def mul3 (A B : Mat3) : Mat3 :=
  ⟨A.m00 * B.m00 + A.m01 * B.m10 + A.m02 * B.m20,
   A.m00 * B.m01 + A.m01 * B.m11 + A.m02 * B.m21,
   A.m00 * B.m02 + A.m01 * B.m12 + A.m02 * B.m22,
   A.m10 * B.m00 + A.m11 * B.m10 + A.m12 * B.m20,
   A.m10 * B.m01 + A.m11 * B.m11 + A.m12 * B.m21,
   A.m10 * B.m02 + A.m11 * B.m12 + A.m12 * B.m22,
   A.m20 * B.m00 + A.m21 * B.m10 + A.m22 * B.m20,
   A.m20 * B.m01 + A.m21 * B.m11 + A.m22 * B.m21,
   A.m20 * B.m02 + A.m21 * B.m12 + A.m22 * B.m22⟩

def sub3 (A B : Mat3) : Mat3 :=
  ⟨A.m00 - B.m00, A.m01 - B.m01, A.m02 - B.m02,
   A.m10 - B.m10, A.m11 - B.m11, A.m12 - B.m12,
   A.m20 - B.m20, A.m21 - B.m21, A.m22 - B.m22⟩

def smul3 (c : Int) (A : Mat3) : Mat3 :=
  ⟨c * A.m00, c * A.m01, c * A.m02,
   c * A.m10, c * A.m11, c * A.m12,
   c * A.m20, c * A.m21, c * A.m22⟩

def comm3 (A B : Mat3) : Mat3 := sub3 (mul3 A B) (mul3 B A)

def eye3 : Mat3 :=
  ⟨1, 0, 0,
   0, 1, 0,
   0, 0, 1⟩

theorem tr_mul_comm3 (A B : Mat3) : tr3 (mul3 A B) = tr3 (mul3 B A) := by
  dsimp [tr3, mul3]
  have h00 : A.m00 * B.m00 = B.m00 * A.m00 := by rw [Int.mul_comm]
  have h11 : A.m11 * B.m11 = B.m11 * A.m11 := by rw [Int.mul_comm]
  have h22 : A.m22 * B.m22 = B.m22 * A.m22 := by rw [Int.mul_comm]
  have h01 : A.m01 * B.m10 = B.m10 * A.m01 := by rw [Int.mul_comm]
  have h02 : A.m02 * B.m20 = B.m20 * A.m02 := by rw [Int.mul_comm]
  have h10 : A.m10 * B.m01 = B.m01 * A.m10 := by rw [Int.mul_comm]
  have h12 : A.m12 * B.m21 = B.m21 * A.m12 := by rw [Int.mul_comm]
  have h20 : A.m20 * B.m02 = B.m02 * A.m20 := by rw [Int.mul_comm]
  have h21 : A.m21 * B.m12 = B.m12 * A.m21 := by rw [Int.mul_comm]
  omega

theorem tr_comm3_vanishes (Q P : Mat3) : tr3 (comm3 Q P) = 0 := by
  dsimp [comm3, sub3, tr3]
  have h := tr_mul_comm3 Q P
  dsimp [tr3] at h
  omega

theorem tr_smul_eye3 (c : Int) : tr3 (smul3 c eye3) = 3 * c := by
  dsimp [tr3, smul3, eye3]
  omega

theorem ccr_obstruction_d3 (Q P : Mat3) (c : Int) (hc : c ≠ 0) :
    comm3 Q P ≠ smul3 c eye3 := by
  intro h
  have h_tr : tr3 (comm3 Q P) = tr3 (smul3 c eye3) := congrArg tr3 h
  rw [tr_comm3_vanishes Q P, tr_smul_eye3 c] at h_tr
  have : c = 0 := by omega
  contradiction



structure Mat2Z2 where
  m00 : Bool
  m01 : Bool
  m10 : Bool
  m11 : Bool
  deriving DecidableEq, Repr

def badd (x y : Bool) : Bool := x != y
def bmul (x y : Bool) : Bool := x && y

def mul2Z2 (A B : Mat2Z2) : Mat2Z2 :=
  ⟨badd (bmul A.m00 B.m00) (bmul A.m01 B.m10),
   badd (bmul A.m00 B.m01) (bmul A.m01 B.m11),
   badd (bmul A.m10 B.m00) (bmul A.m11 B.m10),
   badd (bmul A.m10 B.m01) (bmul A.m11 B.m11)⟩

def comm2Z2 (A B : Mat2Z2) : Mat2Z2 :=
  let AB := mul2Z2 A B
  let BA := mul2Z2 B A
  ⟨badd AB.m00 BA.m00, badd AB.m01 BA.m01,
   badd AB.m10 BA.m10, badd AB.m11 BA.m11⟩

def eye2Z2 : Mat2Z2 := ⟨true, false, false, true⟩

def P_char2 : Mat2Z2 := ⟨false, true, false, false⟩
def Q_char2 : Mat2Z2 := ⟨false, false, true, false⟩

theorem char2_ccr_countermodel : comm2Z2 P_char2 Q_char2 = eye2Z2 := by
  decide



def X_shift2 : Mat2 := ⟨0, 1, 1, 0⟩

def Z_clock2 : Mat2 := ⟨1, 0, 0, -1⟩

theorem x_order_2 : mul2 X_shift2 X_shift2 = eye2 := by decide

theorem z_order_2 : mul2 Z_clock2 Z_clock2 = eye2 := by decide

theorem weyl_relation_d2 : mul2 Z_clock2 X_shift2 = smul2 (-1) (mul2 X_shift2 Z_clock2) := by decide



structure Eisenstein where
  a : Int
  b : Int
  deriving DecidableEq, Repr

def ez : Eisenstein := ⟨0, 0⟩
def eone : Eisenstein := ⟨1, 0⟩
def eomega : Eisenstein := ⟨0, 1⟩
def eomega2 : Eisenstein := ⟨-1, -1⟩

def eadd (x y : Eisenstein) : Eisenstein := ⟨x.a + y.a, x.b + y.b⟩
def esub (x y : Eisenstein) : Eisenstein := ⟨x.a - y.a, x.b - y.b⟩
def emul (x y : Eisenstein) : Eisenstein :=
  ⟨x.a * y.a - x.b * y.b,
   x.a * y.b + x.b * y.a - x.b * y.b⟩

instance : Zero Eisenstein := ⟨ez⟩
instance : One Eisenstein := ⟨eone⟩
instance : Add Eisenstein := ⟨eadd⟩
instance : Sub Eisenstein := ⟨esub⟩
instance : Mul Eisenstein := ⟨emul⟩

structure Mat3E where
  m00 : Eisenstein
  m01 : Eisenstein
  m02 : Eisenstein
  m10 : Eisenstein
  m11 : Eisenstein
  m12 : Eisenstein
  m20 : Eisenstein
  m21 : Eisenstein
  m22 : Eisenstein
  deriving DecidableEq, Repr

def mul3E (A B : Mat3E) : Mat3E :=
  ⟨A.m00 * B.m00 + A.m01 * B.m10 + A.m02 * B.m20,
   A.m00 * B.m01 + A.m01 * B.m11 + A.m02 * B.m21,
   A.m00 * B.m02 + A.m01 * B.m12 + A.m02 * B.m22,
   A.m10 * B.m00 + A.m11 * B.m10 + A.m12 * B.m20,
   A.m10 * B.m01 + A.m11 * B.m11 + A.m12 * B.m21,
   A.m10 * B.m02 + A.m11 * B.m12 + A.m12 * B.m22,
   A.m20 * B.m00 + A.m21 * B.m10 + A.m22 * B.m20,
   A.m20 * B.m01 + A.m21 * B.m11 + A.m22 * B.m21,
   A.m20 * B.m02 + A.m21 * B.m12 + A.m22 * B.m22⟩

def smul3E (c : Eisenstein) (A : Mat3E) : Mat3E :=
  ⟨c * A.m00, c * A.m01, c * A.m02,
   c * A.m10, c * A.m11, c * A.m12,
   c * A.m20, c * A.m21, c * A.m22⟩

def eye3E : Mat3E :=
  ⟨eone, ez, ez,
   ez, eone, ez,
   ez, ez, eone⟩

def X_shift3 : Mat3E :=
  ⟨ez, ez, eone,
   eone, ez, ez,
   ez, eone, ez⟩

def Z_clock3 : Mat3E :=
  ⟨eone, ez, ez,
   ez, eomega, ez,
   ez, ez, eomega2⟩

theorem x_order_3 : mul3E (mul3E X_shift3 X_shift3) X_shift3 = eye3E := by decide

theorem z_order_3 : mul3E (mul3E Z_clock3 Z_clock3) Z_clock3 = eye3E := by decide

theorem weyl_relation_d3 : mul3E Z_clock3 X_shift3 = smul3E eomega (mul3E X_shift3 Z_clock3) := by decide



def finite_differentiation_refusal : Prop :=
  ∀ (Q P : Mat3) (c : Int), c ≠ 0 → comm3 Q P ≠ smul3 c eye3

theorem refuse_finite_differentiation_to_ccr : finite_differentiation_refusal :=
  ccr_obstruction_d3



#print axioms tr_mul_comm2
#print axioms tr_comm2_vanishes
#print axioms tr_smul_eye2
#print axioms ccr_obstruction_d2
#print axioms tr_mul_comm3
#print axioms tr_comm3_vanishes
#print axioms tr_smul_eye3
#print axioms ccr_obstruction_d3
#print axioms char2_ccr_countermodel
#print axioms x_order_2
#print axioms z_order_2
#print axioms weyl_relation_d2
#print axioms x_order_3
#print axioms z_order_3
#print axioms weyl_relation_d3
#print axioms refuse_finite_differentiation_to_ccr

end FableHilbertWalk20260819.H068

private def l5aProvenance : String :=
  "Origin: lean4/H068WeylCcrResidual.lean Claim: tr_mul_comm2 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
