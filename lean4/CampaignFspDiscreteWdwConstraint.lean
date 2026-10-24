/-
Exact algebraic model; AuthorityEffect: None.
Rational residuals obey elementary norm bounds, and a zero-edge/sign-vertex witness has the displayed norm bound and objective equality. No incidence operator, transpose annihilation proposition, optimizer API, or general strong-duality theorem is constructed. A rank-one quadratic form, two supplied 2x2 projectors and a swap constraint have the stated identities. The thermal values 8 and 5 are second-order polynomial traces, not Gibbs exponential traces. The indefinite rational two-variable form is supplied and not derived from continuum DeWitt geometry; no physical Wheeler-DeWitt projector or fermion-sign mechanism follows.
Historical names are labels; their physical or operational interpretations require separate evidence.
-/

import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic



open scoped BigOperators Matrix

namespace CampaignFspDiscreteWdwConstraint


inductive WdwTerminalRoute where
  | ExactRepair
  | SplitBrainRefusal
  deriving DecidableEq, Repr


def d0Edge {n : ℕ} (u v : Fin n) (alpha : Fin n → ℚ) : ℚ :=
  alpha v - alpha u


def dJointScalar {n : ℕ} (_alpha : Fin n → ℚ) (_v : Fin n) : ℚ :=
  0


theorem dJoint_linear_and_constant_kernel
    {n : ℕ} (u v : Fin n) (a b c : ℚ) (alpha beta : Fin n → ℚ) :
    d0Edge u v (fun w => a * alpha w + b * beta w) =
      a * d0Edge u v alpha + b * d0Edge u v beta ∧
    d0Edge u v (fun _ => c) = 0 ∧
    dJointScalar alpha v = 0 := by
  refine ⟨?_, ?_, rfl⟩
  · unfold d0Edge
    ring
  · unfold d0Edge
    ring


def totalJointResidualL1 {m n : ℕ} (p d0alpha : Fin m → ℚ) (hPerp : Fin n → ℚ) : ℚ :=
  (∑ e : Fin m, |p e - d0alpha e|) + (∑ v : Fin n, |hPerp v|)


theorem primal_l1_edge_and_vertex_residual_lower_bound
    {m n : ℕ} (p d0alpha : Fin m → ℚ) (hPerp : Fin n → ℚ) (v0 : Fin n)
    (hv0 : hPerp v0 ≠ 0) :
    (∑ v : Fin n, |hPerp v|) ≤ totalJointResidualL1 p d0alpha hPerp ∧
    totalJointResidualL1 d0alpha d0alpha hPerp = ∑ v : Fin n, |hPerp v| ∧
    |hPerp v0| ≤ totalJointResidualL1 p d0alpha hPerp ∧
    0 < totalJointResidualL1 p d0alpha hPerp := by
  have hedge : 0 ≤ ∑ e : Fin m, |p e - d0alpha e| :=
    Finset.sum_nonneg (fun e _ => abs_nonneg (p e - d0alpha e))
  have hv_le : |hPerp v0| ≤ ∑ v : Fin n, |hPerp v| :=
    Finset.single_le_sum (fun v _ => abs_nonneg (hPerp v)) (Finset.mem_univ v0)
  have hv_pos : 0 < |hPerp v0| := abs_pos.mpr hv0
  refine ⟨?_, ?_, ?_, ?_⟩
  · unfold totalJointResidualL1
    linarith
  · unfold totalJointResidualL1
    simp
  · unfold totalJointResidualL1
    linarith
  · unfold totalJointResidualL1
    linarith


def ratSign (x : ℚ) : ℚ :=
  if 0 < x then 1 else if x < 0 then -1 else 0


def dualObjective {m n : ℕ} (w1 : Fin m → ℚ) (w2 : Fin n → ℚ)
    (p : Fin m → ℚ) (hPerp : Fin n → ℚ) : ℚ :=
  (∑ e : Fin m, w1 e * p e) + (∑ v : Fin n, w2 v * hPerp v)


lemma ratSign_mul_self_and_abs_le_one (x : ℚ) :
    ratSign x * x = |x| ∧ |ratSign x| ≤ 1 := by
  unfold ratSign
  split_ifs with hpos hneg
  · refine ⟨?_, by norm_num⟩
    rw [one_mul, abs_of_pos hpos]
  · refine ⟨?_, by norm_num⟩
    rw [neg_one_mul, abs_of_neg hneg]
  · have hx0 : x = 0 := by linarith
    subst hx0
    simp


theorem strong_duality_direct_sum_wdw_exact_coboundary
    {m n : ℕ} (d0alpha : Fin m → ℚ) (hPerp : Fin n → ℚ) :
    (∀ v : Fin n, |ratSign (hPerp v)| ≤ 1) ∧
    dualObjective (fun _ => 0) (fun v => ratSign (hPerp v)) d0alpha hPerp =
      totalJointResidualL1 d0alpha d0alpha hPerp := by
  refine ⟨fun v => (ratSign_mul_self_and_abs_le_one (hPerp v)).2, ?_⟩
  unfold dualObjective totalJointResidualL1
  simp only [zero_mul, Finset.sum_const_zero, zero_add, sub_self, abs_zero]
  refine Finset.sum_congr rfl (fun v _ => ?_)
  exact (ratSign_mul_self_and_abs_le_one (hPerp v)).1


def routeFromDefectMass (defectMass : ℚ) : WdwTerminalRoute :=
  if defectMass = 0 then .ExactRepair else .SplitBrainRefusal


theorem s4_seed_flat_vs_curved_wdw_defect_mass :
    let hFlat : Fin 6 → ℚ := fun _ => 0
    let hCurved : Fin 6 → ℚ := fun _ => (15 : ℚ) / 2
    let pZero : Fin 15 → ℚ := fun _ => 0
    totalJointResidualL1 pZero pZero hFlat = 0 ∧
    routeFromDefectMass (totalJointResidualL1 pZero pZero hFlat) = .ExactRepair ∧
    totalJointResidualL1 pZero pZero hCurved = 45 ∧
    routeFromDefectMass (totalJointResidualL1 pZero pZero hCurved) = .SplitBrainRefusal := by
  dsimp only
  unfold totalJointResidualL1 routeFromDefectMass
  norm_num


def quadraticConstraintForm (a b x0 x1 : ℚ) : ℚ :=
  x0 * (a * (a * x0 + b * x1)) + x1 * (b * (a * x0 + b * x1))


theorem quadratic_constraint_psd_and_null_kernel_iff
    (a b x0 x1 : ℚ) :
    quadraticConstraintForm a b x0 x1 = (a * x0 + b * x1) ^ 2 ∧
    0 ≤ quadraticConstraintForm a b x0 x1 ∧
    (quadraticConstraintForm a b x0 x1 = 0 ↔ a * x0 + b * x1 = 0) := by
  have hsq : quadraticConstraintForm a b x0 x1 = (a * x0 + b * x1) ^ 2 := by
    unfold quadraticConstraintForm
    ring
  refine ⟨hsq, ?_, ?_⟩
  · rw [hsq]
    exact sq_nonneg (a * x0 + b * x1)
  · rw [hsq]
    exact sq_eq_zero_iff


def diffInvProjector : Matrix (Fin 2) (Fin 2) ℚ :=
  !![(1 : ℚ) / 2, (1 : ℚ) / 2; (1 : ℚ) / 2, (1 : ℚ) / 2]


def wdwDiffConstraint : Matrix (Fin 2) (Fin 2) ℚ :=
  !![(1 : ℚ) / 2, -(1 : ℚ) / 2; -(1 : ℚ) / 2, (1 : ℚ) / 2]


theorem diffeomorphism_averaging_projector_and_constraint_complement
    (x0 x1 : ℚ) :
    diffInvProjector * diffInvProjector = diffInvProjector ∧
    wdwDiffConstraint * wdwDiffConstraint = wdwDiffConstraint ∧
    diffInvProjectorᵀ = diffInvProjector ∧
    wdwDiffConstraint * diffInvProjector = 0 ∧
    (wdwDiffConstraint.mulVec ![x0, x1] = 0 ↔ x0 = x1) ∧
    (diffInvProjector.mulVec ![x0, x1] = ![x0, x1] ↔ x0 = x1) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext i j
    fin_cases i <;> fin_cases j <;>
      · simp [diffInvProjector, Matrix.mul_apply, Fin.sum_univ_two]
        norm_num
  · ext i j
    fin_cases i <;> fin_cases j <;>
      · simp [wdwDiffConstraint, Matrix.mul_apply, Fin.sum_univ_two]
        norm_num
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [diffInvProjector]
  · ext i j
    fin_cases i <;> fin_cases j <;>
      · simp [wdwDiffConstraint, diffInvProjector, Matrix.mul_apply, Fin.sum_univ_two]
        norm_num
  · constructor
    · intro h
      have h0 := congr_fun h 0
      simp [wdwDiffConstraint, Matrix.mulVec, dotProduct, Fin.sum_univ_two] at h0
      linarith
    · intro h
      subst h
      ext i
      fin_cases i <;>
        · simp [wdwDiffConstraint, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
          ring
  · constructor
    · intro h
      have h0 := congr_fun h 0
      simp [diffInvProjector, Matrix.mulVec, dotProduct, Fin.sum_univ_two] at h0
      linarith
    · intro h
      subst h
      ext i
      fin_cases i <;>
        · simp [diffInvProjector, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
          ring


def pwStepMatrix : Matrix (Fin 2) (Fin 2) ℚ :=
  !![0, 1; 1, 0]


def pwConstraintResidual (psi0 psi1 : Fin 2 → ℚ) : (Fin 2 → ℚ) × (Fin 2 → ℚ) :=
  (psi0 - pwStepMatrix.mulVec psi1, psi1 - pwStepMatrix.mulVec psi0)


theorem page_wootters_clock_system_conditioned_evolution
    (psi0 psi1 : Fin 2 → ℚ) :
    pwStepMatrix * pwStepMatrix = 1 ∧
    (pwConstraintResidual psi0 psi1 = (0, 0) ↔ psi1 = pwStepMatrix.mulVec psi0) ∧
    pwConstraintResidual ![1, 0] ![0, 1] = (0, 0) ∧
    (![(0 : ℚ), 1] : Fin 2 → ℚ) ≠ ![(1 : ℚ), 0] := by
  have hU2 : pwStepMatrix * pwStepMatrix = 1 := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [pwStepMatrix, Matrix.mul_apply, Fin.sum_univ_two]
  have hiff : ∀ a b : Fin 2 → ℚ, pwConstraintResidual a b = (0, 0) ↔ b = pwStepMatrix.mulVec a := by
    intro a b
    constructor
    · intro h
      have h2 := congr_arg Prod.snd h
      exact sub_eq_zero.mp h2
    · intro h
      subst h
      unfold pwConstraintResidual
      rw [Matrix.mulVec_mulVec, hU2, Matrix.one_mulVec, sub_self, sub_self]
  refine ⟨hU2, hiff psi0 psi1, ?_, ?_⟩
  · rw [hiff]
    ext i
    fin_cases i <;>
      · dsimp [pwStepMatrix, Matrix.mulVec, dotProduct]
        rw [Fin.sum_univ_two]
        norm_num
  · intro h
    have h0 := congr_fun h 0
    norm_num at h0


def dewittSupermetricForm (vConf vTrans : ℚ) : ℚ :=
  -(vConf ^ 2) + vTrans ^ 2


theorem dewitt_supermetric_indefinite_signature_fence :
    dewittSupermetricForm 1 0 = -1 ∧
    dewittSupermetricForm 1 0 < 0 ∧
    dewittSupermetricForm 0 1 = 1 ∧
    0 < dewittSupermetricForm 0 1 ∧
    dewittSupermetricForm 1 1 = 0 ∧
    ((1 : ℚ), (1 : ℚ)) ≠ ((0 : ℚ), (0 : ℚ)) := by
  unfold dewittSupermetricForm
  norm_num


def hubbardFourStateSpectrum (s : ℚ) : Fin 4 → ℚ :=
  ![0, 0, -2 * s, 2 * s]

def secondOrderThermalTrace (spec : Fin 4 → ℚ) (beta : ℚ) : ℚ :=
  ∑ i : Fin 4, (1 - beta * spec i + (1 / 2 : ℚ) * beta ^ 2 * (spec i) ^ 2)


theorem wdw_constraint_kernel_vs_thermal_gibbs_trace_fence :
    (∀ i : Fin 4, (hubbardFourStateSpectrum 1 i = 0 ↔ hubbardFourStateSpectrum (1 / 2) i = 0)) ∧
    secondOrderThermalTrace (hubbardFourStateSpectrum 1) 1 = 8 ∧
    secondOrderThermalTrace (hubbardFourStateSpectrum (1 / 2)) 1 = 5 ∧
    secondOrderThermalTrace (hubbardFourStateSpectrum 1) 1 ≠
      secondOrderThermalTrace (hubbardFourStateSpectrum (1 / 2)) 1 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro i
    fin_cases i <;>
      · simp [hubbardFourStateSpectrum]
  · simp [secondOrderThermalTrace, hubbardFourStateSpectrum, Fin.sum_univ_four]
    norm_num
  · simp [secondOrderThermalTrace, hubbardFourStateSpectrum, Fin.sum_univ_four]
    norm_num
  · simp [secondOrderThermalTrace, hubbardFourStateSpectrum, Fin.sum_univ_four]
    norm_num


theorem wdw_constraint_projection_preserves_fermion_sign_cancellation_fence
    (v : Fin 2 → ℚ) :
    (1 : ℚ) * (v ⬝ᵥ diffInvProjector.mulVec v) +
      (-1 : ℚ) * (v ⬝ᵥ diffInvProjector.mulVec v) = 0 := by
  ring

#print axioms dJoint_linear_and_constant_kernel
#print axioms primal_l1_edge_and_vertex_residual_lower_bound
#print axioms strong_duality_direct_sum_wdw_exact_coboundary
#print axioms s4_seed_flat_vs_curved_wdw_defect_mass
#print axioms quadratic_constraint_psd_and_null_kernel_iff
#print axioms diffeomorphism_averaging_projector_and_constraint_complement
#print axioms page_wootters_clock_system_conditioned_evolution
#print axioms dewitt_supermetric_indefinite_signature_fence
#print axioms wdw_constraint_kernel_vs_thermal_gibbs_trace_fence
#print axioms wdw_constraint_projection_preserves_fermion_sign_cancellation_fence

end CampaignFspDiscreteWdwConstraint
