



namespace U1AngleAddition

inductive Coord2 where
  | zero
  | one
  deriving DecidableEq

abbrev Matrix2 := Coord2 → Coord2 → Int

def id2 : Matrix2 :=
  fun i j => if i = j then 1 else 0

def mul2 (A B : Matrix2) : Matrix2 :=
  fun i k => A i .zero * B .zero k + A i .one * B .one k

def transpose2 (A : Matrix2) : Matrix2 :=
  fun i j => A j i

def det2 (A : Matrix2) : Int :=
  A .zero .zero * A .one .one - A .zero .one * A .one .zero

def rotMat (c s : Int) : Matrix2 :=
  fun i j =>
    match i, j with
    | .zero, .zero => c
    | .zero, .one  => -s
    | .one,  .zero => s
    | .one,  .one  => c

theorem det2_rotMat (c s : Int) : det2 (rotMat c s) = c * c + s * s := by
  dsimp [det2, rotMat]
  rw [Int.neg_mul, Int.sub_neg]

theorem transpose_mul_rotMat (c s : Int) :
    mul2 (transpose2 (rotMat c s)) (rotMat c s) = fun i j => (c * c + s * s) * id2 i j := by
  funext i j
  cases i <;> cases j
  · dsimp [mul2, transpose2, rotMat, id2]
    omega
  · dsimp [mul2, transpose2, rotMat, id2]
    rw [Int.mul_neg, Int.mul_comm s c]
    omega
  · dsimp [mul2, transpose2, rotMat, id2]
    rw [Int.neg_mul, Int.mul_comm c s]
    omega
  · dsimp [mul2, transpose2, rotMat, id2]
    rw [Int.neg_mul_neg]
    omega

structure CirclePoint where
  c : Int
  s : Int
  unit : c * c + s * s = 1

theorem rotMat_special_orthogonal (p : CirclePoint) :
    det2 (rotMat p.c p.s) = 1 ∧ mul2 (transpose2 (rotMat p.c p.s)) (rotMat p.c p.s) = id2 := by
  have hdet := det2_rotMat p.c p.s
  have horth := transpose_mul_rotMat p.c p.s
  rw [p.unit] at hdet horth
  refine ⟨hdet, ?_⟩
  rw [horth]
  funext i j
  cases i <;> cases j <;> rfl

theorem rotMat_mul_homomorphism (c1 s1 c2 s2 : Int) :
    mul2 (rotMat c1 s1) (rotMat c2 s2) =
    rotMat (c1 * c2 - s1 * s2) (s1 * c2 + c1 * s2) := by
  funext i j
  cases i <;> cases j
  · dsimp [mul2, rotMat]
    rw [Int.neg_mul]
    omega
  · dsimp [mul2, rotMat]
    rw [Int.mul_neg, Int.neg_mul]
    omega
  · dsimp [mul2, rotMat]
  · dsimp [mul2, rotMat]
    rw [Int.mul_neg]
    omega

def circleId : CirclePoint :=
  ⟨1, 0, by decide⟩

theorem rotMat_identity : rotMat 1 0 = id2 := by
  funext i j
  cases i <;> cases j <;> rfl

def J : Matrix2 := rotMat 0 1

theorem J_squared_eq_neg_id : mul2 J J = fun i j => - id2 i j := by
  have h := rotMat_mul_homomorphism 0 1 0 1
  dsimp [J]
  rw [h]
  dsimp [rotMat]
  funext i j
  cases i <;> cases j <;> rfl

theorem J_fourth_eq_id : mul2 (mul2 J J) (mul2 J J) = id2 := by
  funext i j
  cases i <;> cases j <;> rfl

theorem one_parameter_group_law
    (c s : Nat → Int)
    (h_add_c : ∀ θ1 θ2, c (θ1 + θ2) = c θ1 * c θ2 - s θ1 * s θ2)
    (h_add_s : ∀ θ1 θ2, s (θ1 + θ2) = s θ1 * c θ2 + c θ1 * s θ2)
    (θ1 θ2 : Nat) :
    rotMat (c (θ1 + θ2)) (s (θ1 + θ2)) = mul2 (rotMat (c θ1) (s θ1)) (rotMat (c θ2) (s θ2)) := by
  rw [rotMat_mul_homomorphism]
  rw [h_add_c θ1 θ2, h_add_s θ1 θ2]

end U1AngleAddition

namespace QM.U1Transport
export U1AngleAddition (Coord2 Matrix2 id2 mul2 transpose2 det2 rotMat CirclePoint circleId J
  det2_rotMat transpose_mul_rotMat rotMat_special_orthogonal rotMat_mul_homomorphism
  rotMat_identity J_squared_eq_neg_id J_fourth_eq_id one_parameter_group_law)
end QM.U1Transport

#print axioms U1AngleAddition.det2_rotMat
#print axioms U1AngleAddition.transpose_mul_rotMat
#print axioms U1AngleAddition.rotMat_special_orthogonal
#print axioms U1AngleAddition.rotMat_mul_homomorphism
#print axioms U1AngleAddition.rotMat_identity
#print axioms U1AngleAddition.J_squared_eq_neg_id
#print axioms U1AngleAddition.J_fourth_eq_id
#print axioms U1AngleAddition.one_parameter_group_law

private def l5aProvenance : String :=
  "Origin: lean4/U1AngleAddition.lean Claim: det2_rotMat AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
