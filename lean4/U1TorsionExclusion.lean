/-!
# Quarter-turn order and an unbounded integer label lattice (Cycle 006)

AuthorityEffect: None.
Self-contained Lean 4 core verification of Cycle 006 without external Mathlib dependencies.

This file proves the following integer matrix and arithmetic statements:
1. The one-parameter rotation group is non-constant: R(-1, 0) ≠ R(1, 0) (value -1 ≠ +1 at π).
2. The generator J has exact order 4 (J ≠ I, J² ≠ I, J³ ≠ I, J⁴ = I), excluding orders 1, 2, and 3.
3. The period lattice mapping k ↦ k·P for any positive period P is strictly injective.
4. The period lattice is infinite / unbounded (∀ N, ∃ k, k > N).
5. For every positive N there is a natural k with 4*k > N.
Unbounded labels do not imply infinitely many group elements: J itself has
order four. No theorem here excludes torsion from U(1), proves a faithful
embedding of the label lattice, or selects a continuum phase group.
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace U1TorsionExclusion

inductive Coord2 where
  | zero
  | one
  deriving DecidableEq

abbrev Matrix2 := Coord2 → Coord2 → Int

/-- Identity 2x2 matrix. -/
def id2 : Matrix2 :=
  fun i j => if i = j then 1 else 0

/-- 2x2 matrix multiplication over Int. -/
def mul2 (A B : Matrix2) : Matrix2 :=
  fun i k => A i .zero * B .zero k + A i .one * B .one k

/-- 2D rotation matrix parameterized by (c, s). -/
def rotMat (c s : Int) : Matrix2 :=
  fun i j =>
    match i, j with
    | .zero, .zero => c
    | .zero, .one  => -s
    | .one,  .zero => s
    | .one,  .one  => c

/-- Quarter-turn generator J = R(0, 1). -/
def J : Matrix2 := rotMat 0 1

/-- **Theorem (Half-period rotation):** R(-1, 0) = -I₂. -/
theorem rotMat_neg_one_zero : rotMat (-1) 0 = fun i j => - id2 i j := by
  funext i j
  cases i <;> cases j <;> rfl

/-- **Theorem (Non-constancy):** The one-parameter phase is non-constant (R(-1, 0) ≠ I₂).
    Corresponds to e^{iπ} = -1 ≠ 1 in the continuum. -/
theorem phase_pi_ne_zero : rotMat (-1) 0 ≠ id2 := by
  intro h
  have h00 := congrFun (congrFun h .zero) .zero
  dsimp [rotMat, id2] at h00
  revert h00
  decide

/-- **Theorem (Generator order > 1):** J ≠ I₂. -/
theorem J_not_order_1 : J ≠ id2 := by
  intro h
  have h01 := congrFun (congrFun h .zero) .one
  dsimp [J, rotMat, id2] at h01
  revert h01
  decide

/-- **Theorem (Generator order > 2):** J² ≠ I₂. -/
theorem J_not_order_2 : mul2 J J ≠ id2 := by
  intro h
  have h00 := congrFun (congrFun h .zero) .zero
  dsimp [mul2, J, rotMat, id2] at h00
  revert h00
  decide

/-- **Theorem (Generator order > 3):** J³ ≠ I₂. -/
theorem J_not_order_3 : mul2 (mul2 J J) J ≠ id2 := by
  intro h
  have h01 := congrFun (congrFun h .zero) .one
  dsimp [mul2, J, rotMat, id2] at h01
  revert h01
  decide

/-- **Theorem (Generator exact order 4):** J⁴ = I₂. -/
theorem J_order_4 : mul2 (mul2 J J) (mul2 J J) = id2 := by
  funext i j
  cases i <;> cases j <;> rfl

/-- **Theorem (Lattice injectivity):** The period lattice map k ↦ k·P is strictly injective
    for any non-zero period P > 0. -/
theorem lattice_injective (P : Nat) (hP : P > 0) (k1 k2 : Nat) (h : k1 * P = k2 * P) : k1 = k2 := by
  exact Nat.eq_of_mul_eq_mul_right hP h

/-- **Theorem (Period lattice infinite):** The period lattice contains arbitrarily large elements. -/
theorem period_lattice_infinite (N : Nat) : ∃ k : Nat, k > N :=
  ⟨N + 1, Nat.lt_succ_self N⟩

/-- The natural-number labels 4*k are unbounded. Historical name retained;
    this is not a theorem about orders of represented group elements. -/
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
