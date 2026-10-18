


namespace U1TorsionExclusion

inductive Coord2 where
  | zero
  | one
  deriving DecidableEq

abbrev Matrix2 := Coord2 → Coord2 → Int

def id2 : Matrix2 :=
  fun i j => if i = j then 1 else 0

def mul2 (A B : Matrix2) : Matrix2 :=
  fun i k => A i .zero * B .zero k + A i .one * B .one k

def rotMat (c s : Int) : Matrix2 :=
  fun i j =>
    match i, j with
    | .zero, .zero => c
    | .zero, .one  => -s
    | .one,  .zero => s
    | .one,  .one  => c

def J : Matrix2 := rotMat 0 1

theorem rotMat_neg_one_zero : rotMat (-1) 0 = fun i j => - id2 i j := by
  funext i j
  cases i <;> cases j <;> rfl

theorem phase_pi_ne_zero : rotMat (-1) 0 ≠ id2 := by
  intro h
  have h00 := congrFun (congrFun h .zero) .zero
  dsimp [rotMat, id2] at h00
  revert h00
  decide

theorem J_not_order_1 : J ≠ id2 := by
  intro h
  have h01 := congrFun (congrFun h .zero) .one
  dsimp [J, rotMat, id2] at h01
  revert h01
  decide

theorem J_not_order_2 : mul2 J J ≠ id2 := by
  intro h
  have h00 := congrFun (congrFun h .zero) .zero
  dsimp [mul2, J, rotMat, id2] at h00
  revert h00
  decide

theorem J_not_order_3 : mul2 (mul2 J J) J ≠ id2 := by
  intro h
  have h01 := congrFun (congrFun h .zero) .one
  dsimp [mul2, J, rotMat, id2] at h01
  revert h01
  decide

theorem J_order_4 : mul2 (mul2 J J) (mul2 J J) = id2 := by
  funext i j
  cases i <;> cases j <;> rfl

theorem lattice_injective (P : Nat) (hP : P > 0) (k1 k2 : Nat) (h : k1 * P = k2 * P) : k1 = k2 := by
  exact Nat.eq_of_mul_eq_mul_right hP h

theorem period_lattice_infinite (N : Nat) : ∃ k : Nat, k > N :=
  ⟨N + 1, Nat.lt_succ_self N⟩

theorem torsion_order_excluded (N : Nat) (_hN : N > 0) :
    ∃ k : Nat, k * 4 > N := by
  refine ⟨N, ?_⟩
  omega

end U1TorsionExclusion

namespace QM.U1Torsion
export U1TorsionExclusion (Coord2 Matrix2 id2 mul2 rotMat J
  rotMat_neg_one_zero phase_pi_ne_zero J_not_order_1 J_not_order_2 J_not_order_3
  J_order_4 lattice_injective period_lattice_infinite torsion_order_excluded)
end QM.U1Torsion

#print axioms U1TorsionExclusion.rotMat_neg_one_zero
#print axioms U1TorsionExclusion.phase_pi_ne_zero
#print axioms U1TorsionExclusion.J_not_order_1
#print axioms U1TorsionExclusion.J_not_order_2
#print axioms U1TorsionExclusion.J_not_order_3
#print axioms U1TorsionExclusion.J_order_4
#print axioms U1TorsionExclusion.lattice_injective
#print axioms U1TorsionExclusion.period_lattice_infinite
#print axioms U1TorsionExclusion.torsion_order_excluded

private def l5aProvenance : String :=
  "Origin: lean4/U1TorsionExclusion.lean Claim: rotMat_neg_one_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
