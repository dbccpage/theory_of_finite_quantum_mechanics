/-
Exact algebraic model; AuthorityEffect: None.
Explicit low-degree simplicial coboundaries on Fin 5 compose to zero and preserve the displayed curvatures under exact shifts. The ZMod 2 product cocycle is not any displayed 2-coboundary, as detected by the explicit three-term functional. Two supplied integer involutions have commutator -I. Crossed-module identity formulas reduce to reflexivity and do not construct an arbitrary crossed module. There is no identification with Wang-Levin braiding, a path integral, or a unique physical cancellation mechanism.
Historical names are labels; their physical or operational interpretations require separate evidence.
-/

import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic



namespace CampaignFspBf2GroupSignClaim

open Matrix


def d0 {A : Type*} [AddCommGroup A] (c0 : Fin 5 → A) (i j : Fin 5) : A :=
  c0 j - c0 i


def d1 {A : Type*} [AddCommGroup A] (c1 : Fin 5 → Fin 5 → A) (i j k : Fin 5) : A :=
  c1 j k - c1 i k + c1 i j


def d2 {A : Type*} [AddCommGroup A] (c2 : Fin 5 → Fin 5 → Fin 5 → A)
    (i j k l : Fin 5) : A :=
  c2 j k l - c2 i k l + c2 i j l - c2 i j k


def d3 {A : Type*} [AddCommGroup A] (c3 : Fin 5 → Fin 5 → Fin 5 → Fin 5 → A)
    (i j k l m : Fin 5) : A :=
  c3 j k l m - c3 i k l m + c3 i j l m - c3 i j k m + c3 i j k l


theorem simplicial_coboundary_nilpotence_d1d0_d2d1_d3d2 {A : Type*} [AddCommGroup A]
    (c0 : Fin 5 → A) (c1 : Fin 5 → Fin 5 → A) (c2 : Fin 5 → Fin 5 → Fin 5 → A)
    (i j k l m : Fin 5) :
    d1 (d0 c0) i j k = 0 ∧
    d2 (d1 c1) i j k l = 0 ∧
    d3 (d2 c2) i j k l m = 0 := by
  refine ⟨?_, ?_, ?_⟩
  · dsimp [d1, d0]; abel
  · dsimp [d2, d1]; abel
  · dsimp [d3, d2]; abel


theorem bf_cochain_gauge_invariance {A : Type*} [AddCommGroup A]
    (A1 : Fin 5 → Fin 5 → A) (lam : Fin 5 → A)
    (B2 : Fin 5 → Fin 5 → Fin 5 → A) (eta : Fin 5 → Fin 5 → A)
    (i j k l : Fin 5) :
    d1 (fun u v => A1 u v + d0 lam u v) i j k = d1 A1 i j k ∧
    d2 (fun u v w => B2 u v w + d1 eta u v w) i j k l = d2 B2 i j k l := by
  refine ⟨?_, ?_⟩
  · dsimp [d1, d0]; abel
  · dsimp [d2, d1]; abel


theorem bf_z2_level_hopf_link_sign_and_weight_trichotomy (q p lk w_pos w_neg : ℤ) :
    q * p * (-lk) = -(q * p * lk) ∧
    (-1 : ℤ) ^ (1 : ℕ) = -1 ∧
    (w_pos = w_neg → w_pos * 1 + w_neg * (-1) = 0) ∧
    (w_pos ≠ w_neg → w_pos * 1 + w_neg * (-1) ≠ 0) := by
  refine ⟨by ring, rfl, ?_, ?_⟩
  · intro h
    omega
  · intro hne heq
    apply hne
    omega


def omega3Mat : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, -1;
     1, -1]


theorem bf_z3_level_non_involution_and_cos_sum_fence :
    omega3Mat ^ 3 = (1 : Matrix (Fin 2) (Fin 2) ℤ) ∧
    omega3Mat ^ 2 ≠ (1 : Matrix (Fin 2) (Fin 2) ℤ) ∧
    omega3Mat + omega3Mat ^ 2 = -(1 : Matrix (Fin 2) (Fin 2) ℤ) ∧
    Matrix.trace (omega3Mat + omega3Mat ^ 2) = -2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · intro h
    have h00 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℤ => M 0 0) h
    revert h00
    decide
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · decide


def b1Ising : Matrix (Fin 2) (Fin 2) ℤ :=
  !![1, 0;
     0, -1]


def b2Ising : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, 1;
     1, 0]


def wangLevinCommutator : Matrix (Fin 2) (Fin 2) ℤ :=
  b1Ising * b2Ising * b1Ising * b2Ising


theorem wang_levin_ising_commutator_negative_trace_and_abelian_commutation
    (d1_vec d2_vec : Fin 2 → ℤ) :
    b1Ising * b1Ising = 1 ∧
    b2Ising * b2Ising = 1 ∧
    wangLevinCommutator = -(1 : Matrix (Fin 2) (Fin 2) ℤ) ∧
    Matrix.trace wangLevinCommutator = -2 ∧
    Matrix.diagonal d1_vec * Matrix.diagonal d2_vec =
      Matrix.diagonal d2_vec * Matrix.diagonal d1_vec := by
  refine ⟨?_, ?_, ?_, by decide, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · rw [Matrix.diagonal_mul_diagonal, Matrix.diagonal_mul_diagonal]
    congr 1
    ext i
    exact mul_comm (d1_vec i) (d2_vec i)


theorem crossed_module_conjugation_peiffer_and_identity {G : Type*} [Group G]
    (g h h1 h2 : G) :
    (fun x : G => x) (g * h * g⁻¹) = g * (fun x : G => x) h * g⁻¹ ∧
    ((fun x : G => x) h1) * h2 * ((fun x : G => x) h1)⁻¹ = h1 * h2 * h1⁻¹ := by
  exact ⟨rfl, rfl⟩


def postnikovCup3 (g1 g2 g3 : ZMod 2) : ZMod 2 :=
  g1 * g2 * g3


def groupCoboundary3 (a : ZMod 2 → ZMod 2 → ZMod 2 → ZMod 2)
    (g1 g2 g3 g4 : ZMod 2) : ZMod 2 :=
  a g2 g3 g4 - a (g1 + g2) g3 g4 + a g1 (g2 + g3) g4 - a g1 g2 (g3 + g4) + a g1 g2 g3


def groupCoboundary2 (b : ZMod 2 → ZMod 2 → ZMod 2)
    (g1 g2 g3 : ZMod 2) : ZMod 2 :=
  b g2 g3 - b (g1 + g2) g3 + b g1 (g2 + g3) - b g1 g2


theorem postnikov_cup3_is_3cocycle_on_zmod2 :
    (∀ g1 g2 g3 g4 : ZMod 2, groupCoboundary3 postnikovCup3 g1 g2 g3 g4 = 0) ∧
    postnikovCup3 1 1 1 = 1 ∧
    postnikovCup3 1 1 1 ≠ 0 := by
  refine ⟨by decide, rfl, by decide⟩


def rp3CyclePairing (c : ZMod 2 → ZMod 2 → ZMod 2 → ZMod 2) : ZMod 2 :=
  c 1 0 0 + c 0 0 1 + c 1 1 1


theorem postnikov_cup3_not_coboundary_in_H3_zmod2 :
    (∀ b : ZMod 2 → ZMod 2 → ZMod 2, rp3CyclePairing (groupCoboundary2 b) = 0) ∧
    rp3CyclePairing postnikovCup3 = 1 ∧
    (∀ b : ZMod 2 → ZMod 2 → ZMod 2, groupCoboundary2 b ≠ postnikovCup3) := by
  refine ⟨by decide, rfl, ?_⟩
  intro b hb
  have h0 : rp3CyclePairing (groupCoboundary2 b) = 0 := by
     revert b; decide
  rw [hb] at h0
  revert h0
  decide


theorem two_connection_postnikov_3curvature_bianchi (phi : Fin 5 → ZMod 2)
    (i j k l m : Fin 5) :
    let g := d0 phi
    let C3 (u v w x : Fin 5) : ZMod 2 := postnikovCup3 (g u v) (g v w) (g w x)
    d3 C3 i j k l m = 0 := by
  intro g C3
  have h1 : g i k = g i j + g j k := by dsimp [g, d0]; abel
  have h2 : g j l = g j k + g k l := by dsimp [g, d0]; abel
  have h3 : g k m = g k l + g l m := by dsimp [g, d0]; abel
  have hcocycle := (postnikov_cup3_is_3cocycle_on_zmod2).1 (g i j) (g j k) (g k l) (g l m)
  dsimp [d3, C3]
  rw [h1, h2, h3]
  exact hcocycle


theorem one_form_double_vs_conjugate_two_group_postnikov_cancellation
    (g1 g2 g3 : ZMod 2) (n : ℕ) :
    postnikovCup3 1 1 1 + 0 = 1 ∧
    postnikovCup3 g1 g2 g3 - postnikovCup3 g1 g2 g3 = 0 ∧
    ((-1 : ℤ) ^ n) * ((-1 : ℤ) ^ n) = 1 := by
  refine ⟨rfl, sub_self _, ?_⟩
  rw [← pow_add, ← two_mul, pow_mul]
  simp


theorem doubled_partition_function_changes_target_model_fence :
    ((2 : ℤ) ≠ (-2 : ℤ) ∧ (2 : ℤ) ^ 2 = (-2 : ℤ) ^ 2) ∧
    ((1 : ℤ) + (-1 : ℤ) = 0 ∧
     (1 : ℤ) ^ 2 + (-1 : ℤ) ^ 2 = 2 ∧
     ((1 : ℤ) + (-1 : ℤ)) ^ 2 ≠ (1 : ℤ) ^ 2 + (-1 : ℤ) ^ 2) := by
   decide

end CampaignFspBf2GroupSignClaim

#print axioms CampaignFspBf2GroupSignClaim.simplicial_coboundary_nilpotence_d1d0_d2d1_d3d2
#print axioms CampaignFspBf2GroupSignClaim.bf_cochain_gauge_invariance
#print axioms CampaignFspBf2GroupSignClaim.bf_z2_level_hopf_link_sign_and_weight_trichotomy
#print axioms CampaignFspBf2GroupSignClaim.bf_z3_level_non_involution_and_cos_sum_fence
#print axioms CampaignFspBf2GroupSignClaim.wang_levin_ising_commutator_negative_trace_and_abelian_commutation
#print axioms CampaignFspBf2GroupSignClaim.crossed_module_conjugation_peiffer_and_identity
#print axioms CampaignFspBf2GroupSignClaim.postnikov_cup3_is_3cocycle_on_zmod2
#print axioms CampaignFspBf2GroupSignClaim.postnikov_cup3_not_coboundary_in_H3_zmod2
#print axioms CampaignFspBf2GroupSignClaim.two_connection_postnikov_3curvature_bianchi
#print axioms CampaignFspBf2GroupSignClaim.one_form_double_vs_conjugate_two_group_postnikov_cancellation
#print axioms CampaignFspBf2GroupSignClaim.doubled_partition_function_changes_target_model_fence
