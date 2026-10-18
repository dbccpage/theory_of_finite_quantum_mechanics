

namespace RotationGroups

inductive Coord3 where
  | c0
  | c1
  | c2
  deriving DecidableEq, Repr

abbrev Matrix3Int := Coord3 → Coord3 → Int

def mkMat (a00 a01 a02 a10 a11 a12 a20 a21 a22 : Int) : Matrix3Int :=
  fun i j =>
    match i, j with
    | .c0, .c0 => a00 | .c0, .c1 => a01 | .c0, .c2 => a02
    | .c1, .c0 => a10 | .c1, .c1 => a11 | .c1, .c2 => a12
    | .c2, .c0 => a20 | .c2, .c1 => a21 | .c2, .c2 => a22

def id3 : Matrix3Int :=
  mkMat 1 0 0 0 1 0 0 0 1

def mul3 (A B : Matrix3Int) : Matrix3Int :=
  fun i k =>
    A i .c0 * B .c0 k +
    A i .c1 * B .c1 k +
    A i .c2 * B .c2 k

def transpose3 (A : Matrix3Int) : Matrix3Int :=
  fun i j => A j i

def tr3 (A : Matrix3Int) : Int :=
  A .c0 .c0 + A .c1 .c1 + A .c2 .c2

def det3 (A : Matrix3Int) : Int :=
  A .c0 .c0 * (A .c1 .c1 * A .c2 .c2 - A .c1 .c2 * A .c2 .c1) -
  A .c0 .c1 * (A .c1 .c0 * A .c2 .c2 - A .c1 .c2 * A .c2 .c0) +
  A .c0 .c2 * (A .c1 .c0 * A .c2 .c1 - A .c1 .c1 * A .c2 .c0)

def isOrthogonal (A : Matrix3Int) : Prop :=
  mul3 (transpose3 A) A = id3

def isSpecialOrthogonal (A : Matrix3Int) : Prop :=
  isOrthogonal A ∧ det3 A = 1


structure FiniteMatrixGroup3 (elements : List Matrix3Int) : Prop where
  contains_id : id3 ∈ elements
  closed_mul  : ∀ A B, A ∈ elements → B ∈ elements → mul3 A B ∈ elements
  closed_inv  : ∀ A, A ∈ elements → transpose3 A ∈ elements
  all_so      : ∀ A, A ∈ elements → isSpecialOrthogonal A

def isFaithful (elements : List Matrix3Int) (order : Nat) : Prop :=
  elements.Nodup ∧ elements.length = order

def conductorPriceOctahedral : Nat := 1
def conductorPriceTetrahedral : Nat := 1
def conductorPriceIcosahedral : Nat := 5


def octGenA : Matrix3Int :=
  mkMat 0 (-1) 0 1 0 0 0 0 1

def octGenB : Matrix3Int :=
  mkMat 0 0 1 1 0 0 0 1 0

theorem octGenA_det : det3 octGenA = 1 := by rfl

theorem octGenB_det : det3 octGenB = 1 := by rfl

theorem octGenA_ortho : isOrthogonal octGenA := by
  dsimp [isOrthogonal]
  funext i j
  cases i <;> cases j <;> rfl

theorem octGenB_ortho : isOrthogonal octGenB := by
  dsimp [isOrthogonal]
  funext i j
  cases i <;> cases j <;> rfl

theorem octGenA_so : isSpecialOrthogonal octGenA :=
  ⟨octGenA_ortho, octGenA_det⟩

theorem octGenB_so : isSpecialOrthogonal octGenB :=
  ⟨octGenB_ortho, octGenB_det⟩

theorem octGenA_order4 : mul3 (mul3 (mul3 octGenA octGenA) octGenA) octGenA = id3 := by
  funext i j
  cases i <;> cases j <;> rfl

theorem octGenB_order3 : mul3 (mul3 octGenB octGenB) octGenB = id3 := by
  funext i j
  cases i <;> cases j <;> rfl

theorem octGenAB_order2 : mul3 (mul3 octGenA octGenB) (mul3 octGenA octGenB) = id3 := by
  funext i j
  cases i <;> cases j <;> rfl

theorem octahedral_realization_in_so3_z :
    isSpecialOrthogonal octGenA ∧
    isSpecialOrthogonal octGenB ∧
    mul3 (mul3 (mul3 octGenA octGenA) octGenA) octGenA = id3 ∧
    mul3 (mul3 octGenB octGenB) octGenB = id3 ∧
    mul3 (mul3 octGenA octGenB) (mul3 octGenA octGenB) = id3 :=
  ⟨octGenA_so, octGenB_so, octGenA_order4, octGenB_order3, octGenAB_order2⟩


def icosahedralOrder5TraceEquation (t : Int) : Prop :=
  (2 * t - 1) * (2 * t - 1) = 5

theorem trace_minus_two_ne_order5 : ¬ icosahedralOrder5TraceEquation (-2) := by
  dsimp [icosahedralOrder5TraceEquation]; decide

theorem trace_minus_one_ne_order5 : ¬ icosahedralOrder5TraceEquation (-1) := by
  dsimp [icosahedralOrder5TraceEquation]; decide

theorem trace_zero_ne_order5 : ¬ icosahedralOrder5TraceEquation 0 := by
  dsimp [icosahedralOrder5TraceEquation]; decide

theorem trace_one_ne_order5 : ¬ icosahedralOrder5TraceEquation 1 := by
  dsimp [icosahedralOrder5TraceEquation]; decide

theorem trace_two_ne_order5 : ¬ icosahedralOrder5TraceEquation 2 := by
  dsimp [icosahedralOrder5TraceEquation]; decide

theorem trace_three_ne_order5 : ¬ icosahedralOrder5TraceEquation 3 := by
  dsimp [icosahedralOrder5TraceEquation]; decide

theorem no_int_5k2_eq_1 (k : Int) : 5 * (k * k) ≠ 1 := by
  have h_lin (Y : Int) : 5 * Y ≠ 1 := by omega
  exact h_lin (k * k)

theorem disc5_not_dvd_1 : ¬ (5 ∣ 1) := by decide
theorem disc5_not_dvd_2 : ¬ (5 ∣ 2) := by decide
theorem disc5_not_dvd_3 : ¬ (5 ∣ 3) := by decide
theorem disc5_not_dvd_4 : ¬ (5 ∣ 4) := by decide
theorem disc5_dvd_5 : 5 ∣ 5 := by decide

theorem icosahedral_conductor_ge_5 (n : Nat) (hn : 0 < n) (h_embed : 5 ∣ n) : 5 ≤ n := by
  exact Nat.le_of_dvd hn h_embed

theorem icosahedral_trace_field_lemma :
    (¬ icosahedralOrder5TraceEquation 0) ∧
    (¬ icosahedralOrder5TraceEquation 1) ∧
    (¬ (5 ∣ 1)) ∧
    (5 ∣ 5) :=
  ⟨trace_zero_ne_order5, trace_one_ne_order5, disc5_not_dvd_1, disc5_dvd_5⟩


#print axioms octGenA_order4
#print axioms octGenB_order3
#print axioms octGenAB_order2
#print axioms octahedral_realization_in_so3_z
#print axioms trace_zero_ne_order5
#print axioms disc5_not_dvd_1
#print axioms icosahedral_conductor_ge_5
#print axioms icosahedral_trace_field_lemma

end RotationGroups

private def l5aProvenance : String :=
  "Origin: lean4/RotationGroups.lean Claim: octGenA_det AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
