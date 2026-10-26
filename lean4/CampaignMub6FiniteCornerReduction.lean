/-!
One integer 3 by 3 block identity for a forced corner matrix.
AuthorityEffect: None.
The module has no import.
-/

namespace CampaignMub6FiniteCornerReduction

abbrev Mat := Fin 3 → Fin 3 → Int

def mmul (A B : Mat) : Mat :=
  fun i j => A i 0 * B 0 j + A i 1 * B 1 j + A i 2 * B 2 j

def madd (A B : Mat) : Mat :=
  fun i j => A i j + B i j

def mneg (A : Mat) : Mat :=
  fun i j => -A i j

def transp (A : Mat) : Mat :=
  fun i j => A j i

def eye : Mat
  | 0, 0 => 1
  | 1, 1 => 1
  | 2, 2 => 1
  | _, _ => 0

def zero : Mat := fun _ _ => 0

def bMat : Mat
  | 0, 0 => 1
  | 0, 1 => 1
  | 0, 2 => 0
  | 1, 0 => 0
  | 1, 1 => 1
  | 1, 2 => 1
  | 2, 0 => 0
  | 2, 1 => 0
  | 2, 2 => 1

def bInv : Mat
  | 0, 0 => 1
  | 0, 1 => -1
  | 0, 2 => 1
  | 1, 0 => 0
  | 1, 1 => 1
  | 1, 2 => -1
  | 2, 0 => 0
  | 2, 1 => 0
  | 2, 2 => 1

def eMat : Mat
  | 0, 0 => 1
  | 1, 1 => 1
  | 2, 2 => 1
  | _, _ => 0

def cMat : Mat
  | 0, 0 => 0
  | 0, 1 => 1
  | 0, 2 => 0
  | 1, 0 => 0
  | 1, 1 => 0
  | 1, 2 => 1
  | 2, 0 => 1
  | 2, 1 => 0
  | 2, 2 => 0

def dMat : Mat
  | 0, 0 => 1
  | 0, 1 => -1
  | 0, 2 => 0
  | 1, 0 => -1
  | 1, 1 => 1
  | 1, 2 => -1
  | 2, 0 => -1
  | 2, 1 => 0
  | 2, 2 => 0

theorem eq_of_entries (A B : Mat)
    (h00 : A 0 0 = B 0 0) (h01 : A 0 1 = B 0 1) (h02 : A 0 2 = B 0 2)
    (h10 : A 1 0 = B 1 0) (h11 : A 1 1 = B 1 1) (h12 : A 1 2 = B 1 2)
    (h20 : A 2 0 = B 2 0) (h21 : A 2 1 = B 2 1) (h22 : A 2 2 = B 2 2) :
    A = B := by
  funext i j
  match i, j with
  | 0, 0 => exact h00
  | 0, 1 => exact h01
  | 0, 2 => exact h02
  | 1, 0 => exact h10
  | 1, 1 => exact h11
  | 1, 2 => exact h12
  | 2, 0 => exact h20
  | 2, 1 => exact h21
  | 2, 2 => exact h22

theorem b_inv_left : mmul bMat bInv = eye := by
  apply eq_of_entries <;> decide

theorem b_inv_right : mmul bInv bMat = eye := by
  apply eq_of_entries <;> decide

theorem d_formula :
    dMat = mneg (mmul (mmul cMat (transp eMat)) (transp bInv)) := by
  apply eq_of_entries <;> decide

theorem cross_zero :
    madd (mmul cMat (transp eMat)) (mmul dMat (transp bMat)) = zero := by
  apply eq_of_entries <;> decide

theorem zero_cross_ne :
    madd (mmul cMat (transp eMat)) (mmul zero (transp bMat)) ≠ zero := by
  intro h
  have hne : madd (mmul cMat (transp eMat)) (mmul zero (transp bMat)) 0 1 ≠ zero 0 1 := by
    decide
  exact hne (congrFun (congrFun h 0) 1)

#print axioms b_inv_left
#print axioms b_inv_right
#print axioms d_formula
#print axioms cross_zero
#print axioms zero_cross_ne

end CampaignMub6FiniteCornerReduction
