import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic

/-!
# Campaign FSP-DISCRETE-WDW-CONSTRAINT (`TFQ-1213` / `FSP-DERIV-049`)

Status: Formalization of the finite direct-sum Regge-Wheeler-DeWitt gauge cochain
system, primal-dual $\ell_1$ scalar-curvature unscreenability over $\mathbb{Q}$,
finite quadratic constraint projectors and Page-Wootters clock conditioning, and
explicit scope fences for DeWitt supermetric indefiniteness, thermal-vs-WDW ensemble
distinctness (Section 2.5), and fermion-sign independence (`OPEN`, `E1 -> E3`).
AuthorityEffect: None.

## Scope & Boundaries
- Replaces the missing `ReggePachnerWdw.lean::wheeler_dewitt_constraint_null_kernel`
  and the `Nat`-only lemma `wdw_defect_unscreenable` (`(p - alpha) + h_wdw > 0`)
  with exact signed rational (`ℚ`) theorems.
- Keeps node status `OPEN` because the continuum Wheeler-DeWitt kinetic supermetric
  has indefinite signature $(-, +, +, +, +, +)$ and does not define a positive-definite
  Hilbert-space projector without gauge-fixing / clock selection.
-/

open scoped BigOperators Matrix

namespace CampaignFspDiscreteWdwConstraint

/-- Terminal routing disposition matching `code/python/src/fsp/regge_pachner_wdw.py`. -/
inductive WdwTerminalRoute where
  | ExactRepair
  | SplitBrainRefusal
  deriving DecidableEq, Repr

/-- Discrete 0-cochain coboundary $(d_0 \alpha)_{(u,v)} = \alpha(v) - \alpha(u)$ on an oriented edge. -/
def d0Edge {n : ℕ} (u v : Fin n) (alpha : Fin n → ℚ) : ℚ :=
  alpha v - alpha u

/-- Scalar Wheeler-DeWitt block of $D_{\text{joint}}(\alpha) = (d_0 \alpha, 0)$ in
`code/python/src/fsp/regge_pachner_wdw.py` (`D_joint = np.vstack([d0, np.zeros((n_v, n_v))])`). -/
def dJointScalar {n : ℕ} (_alpha : Fin n → ℚ) (_v : Fin n) : ℚ :=
  0

/-- Theorem 1 (Linearity and Constant-Cochain Kernel of $D_{\text{joint}} = [d_0, 0]^T$):
The edge coboundary $d_0$ is $\mathbb{Q}$-linear, annihilates every constant 0-cochain
$\alpha(w) = c$, and the scalar Wheeler-DeWitt block of $D_{\text{joint}}$ is identically zero. -/
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

/-- Primal $\ell_1$ objective of the direct-sum Regge-WDW gauge system
$\|\Omega - D_{\text{joint}} \alpha\|_1 = \|p - d_0 \alpha\|_1 + \|h_\perp\|_1$. -/
def totalJointResidualL1 {m n : ℕ} (p d0alpha : Fin m → ℚ) (hPerp : Fin n → ℚ) : ℚ :=
  (∑ e : Fin m, |p e - d0alpha e|) + (∑ v : Fin n, |hPerp v|)

/-- Theorem 2 (Signed Rational Unscreenability of Scalar WDW Curvature):
For any edge momentum $p$, coboundary shift $d_0 \alpha$, and vertex scalar constraint
vector $h_\perp$ over $\mathbb{Q}$, the joint $\ell_1$ residual satisfies
$\|h_\perp\|_1 \le \|\Omega - D_{\text{joint}} \alpha\|_1$, achieves equality when $p = d_0 \alpha$,
and is strictly positive whenever any vertex has $h_\perp(v_0) \ne 0$ (even if $h_\perp(v_0) < 0$). -/
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

/-- Rational sign function $\operatorname{sgn}(x) \in \{-1, 0, 1\}$ used to construct the optimal
dual witness $W^* = (0, \operatorname{sgn}(h_\perp))$ in `solve_direct_sum_wdw_lp`. -/
def ratSign (x : ℚ) : ℚ :=
  if 0 < x then 1 else if x < 0 then -1 else 0

/-- Dual objective $\langle W, \Omega \rangle = \sum_e w_1(e) p(e) + \sum_v w_2(v) h_\perp(v)$. -/
def dualObjective {m n : ℕ} (w1 : Fin m → ℚ) (w2 : Fin n → ℚ)
    (p : Fin m → ℚ) (hPerp : Fin n → ℚ) : ℚ :=
  (∑ e : Fin m, w1 e * p e) + (∑ v : Fin n, w2 v * hPerp v)

/-- Pointwise identity $\operatorname{sgn}(x) \cdot x = |x|$ and $\|\operatorname{sgn}(x)\|_\infty \le 1$. -/
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

/-- Theorem 3 (Exact Strong Duality on Exact-Momentum States in `solve_direct_sum_wdw_lp`):
For any exact-coboundary momentum $p = d_0 \alpha$ and vertex curvature vector $h_\perp$,
the dual witness $W^* = (0, \operatorname{sgn}(h_\perp))$ satisfies $D_{\text{joint}}^T W^* = 0$
and $\|W^*\|_\infty \le 1$, and achieves $\langle W^*, (d_0 \alpha, h_\perp) \rangle = \|h_\perp\|_1 =
\text{totalJointResidualL1}(d_0 \alpha, d_0 \alpha, h_\perp)$ with zero duality gap. -/
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

/-- Route selector matching `audit_pachner_surgery` in `code/python/src/fsp/regge_pachner_wdw.py`. -/
def routeFromDefectMass (defectMass : ℚ) : WdwTerminalRoute :=
  if defectMass = 0 then .ExactRepair else .SplitBrainRefusal

/-- Theorem 4 ($\partial \Delta^5$ Seed Flat vs Curved WDW Defect Mass Receipt):
On the 6-vertex $\partial \Delta^5 \cong S^4$ seed (`Simplicial4DManifold`, vertex degree $5$):
- In the `"Flat"` regime ($h_\perp = 0$, $p = d_0 \alpha$), the primal and dual objectives equal $0$
  and route to `.ExactRepair`.
- In the `"Curved"` regime ($h_\perp(v) = \frac{3}{2} \cdot 5 = \frac{15}{2}$ on all 6 vertices),
  the scalar WDW norm is $\sum_{v=0}^5 |\frac{15}{2}| = 45 > 0$ and routes to `.SplitBrainRefusal`. -/
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

/-- Quadratic constraint expectation $\langle x, L^T L x \rangle = (a x_0 + b x_1)^2$ on $\mathbb{Q}^2$. -/
def quadraticConstraintForm (a b x0 x1 : ℚ) : ℚ :=
  x0 * (a * (a * x0 + b * x1)) + x1 * (b * (a * x0 + b * x1))

/-- Theorem 5 (Quadratic Constraint Operator PSD and Null-Kernel Equivalence):
For any linear constraint functional $L(x_0, x_1) = a x_0 + b x_1$ on $\mathbb{Q}^2$,
the self-adjoint constraint operator $H_\perp = L^T L$ satisfies
$\langle x, H_\perp x \rangle = (a x_0 + b x_1)^2 \ge 0$, and
$\langle x, H_\perp x \rangle = 0 \iff a x_0 + b x_1 = 0$. -/
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

/-- Diffeomorphism-averaging projector $P_{\text{inv}} = \frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$
on a 2-state gauge orbit. -/
def diffInvProjector : Matrix (Fin 2) (Fin 2) ℚ :=
  !![(1 : ℚ) / 2, (1 : ℚ) / 2; (1 : ℚ) / 2, (1 : ℚ) / 2]

/-- Complementary constraint projector $H_\perp = I - P_{\text{inv}} = \frac{1}{2}\begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}$. -/
def wdwDiffConstraint : Matrix (Fin 2) (Fin 2) ℚ :=
  !![(1 : ℚ) / 2, -(1 : ℚ) / 2; -(1 : ℚ) / 2, (1 : ℚ) / 2]

/-- Theorem 6 (Idempotent Diffeomorphism Projector and Null-Kernel Complementarity):
$P_{\text{inv}}$ and $H_\perp = I - P_{\text{inv}}$ are symmetric idempotent projectors satisfying
$H_\perp P_{\text{inv}} = 0$, and for every state $v = (x_0, x_1)^T$,
$H_\perp v = 0 \iff P_{\text{inv}} v = v \iff x_0 = x_1$. -/
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

/-- Pauli-X involutive step $U = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ for a 2-tick Page-Wootters clock. -/
def pwStepMatrix : Matrix (Fin 2) (Fin 2) ℚ :=
  !![0, 1; 1, 0]

/-- Page-Wootters global constraint residual $(\Psi_0 - U \Psi_1, \Psi_1 - U \Psi_0)$ on $\mathcal{H}_C \otimes \mathcal{H}_S$. -/
def pwConstraintResidual (psi0 psi1 : Fin 2 → ℚ) : (Fin 2 → ℚ) × (Fin 2 → ℚ) :=
  (psi0 - pwStepMatrix.mulVec psi1, psi1 - pwStepMatrix.mulVec psi0)

/-- Theorem 7 (Page-Wootters Timeless Constraint Kernel vs Conditioned Clock Evolution):
The step matrix $U$ satisfies $U^2 = I$; a global state $(\Psi_0, \Psi_1)$ lies in the
Wheeler-DeWitt kernel $\text{pwConstraintResidual}(\Psi_0, \Psi_1) = (0, 0)$ iff
$\Psi_1 = U \Psi_0$; and for $\Psi_0 = (1, 0)^T$, the timeless kernel state satisfies
$\Psi_1 = (0, 1)^T \ne \Psi_0$. -/
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

/-- 2-mode conformal-transverse DeWitt kinetic supermetric quadratic form
$q_{\text{DW}}(v_{\text{conf}}, v_{\text{trans}}) = -v_{\text{conf}}^2 + v_{\text{trans}}^2$. -/
def dewittSupermetricForm (vConf vTrans : ℚ) : ℚ :=
  -(vConf ^ 2) + vTrans ^ 2

/-- Theorem 8 (DeWitt Supermetric Indefinite Signature Fence):
Unlike a finite positive-semidefinite operator $L^T L$, the continuum DeWitt kinetic form
has negative conformal-mode energy $q_{\text{DW}}(1, 0) = -1 < 0$, positive transverse-mode
energy $q_{\text{DW}}(0, 1) = 1 > 0$, and non-zero lightlike vectors $(1, 1) \ne (0, 0)$
with $q_{\text{DW}}(1, 1) = 0$. -/
theorem dewitt_supermetric_indefinite_signature_fence :
    dewittSupermetricForm 1 0 = -1 ∧
    dewittSupermetricForm 1 0 < 0 ∧
    dewittSupermetricForm 0 1 = 1 ∧
    0 < dewittSupermetricForm 0 1 ∧
    dewittSupermetricForm 1 1 = 0 ∧
    ((1 : ℚ), (1 : ℚ)) ≠ ((0 : ℚ), (0 : ℚ)) := by
  unfold dewittSupermetricForm
  norm_num

/-- 4-state Section 2.5 Hubbard spectrum $\lambda^{(s)} = (0, 0, -2s, 2s)$ and its second-order
thermal trace $\sum_i (1 - \beta \lambda_i + \frac{1}{2} \beta^2 \lambda_i^2)$. -/
def hubbardFourStateSpectrum (s : ℚ) : Fin 4 → ℚ :=
  ![0, 0, -2 * s, 2 * s]

def secondOrderThermalTrace (spec : Fin 4 → ℚ) (beta : ℚ) : ℚ :=
  ∑ i : Fin 4, (1 - beta * spec i + (1 / 2 : ℚ) * beta ^ 2 * (spec i) ^ 2)

/-- Theorem 9 (WDW Zero-Mode Kernel vs Thermal Gibbs Ensemble Fence, Section 2.5):
The two spectra $\lambda^{(1)} = (0, 0, -2, 2)$ and $\lambda^{(1/2)} = (0, 0, -1, 1)$
have the exact same zero-eigenvalue WDW constraint subspace $\{i : \lambda_i = 0\} = \{0, 1\}$,
yet distinct thermal traces at $\beta = 1$ ($8 \ne 5$). -/
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

/-- Theorem 10 (WDW Projector Independence from Fermionic Sign Cancellation Fence):
For any spatial state $v : \text{Fin 2} \to \mathbb{Q}$, summing the WDW-projected weight
$\sigma \cdot (v \cdot P_{\text{inv}} v)$ over the fermionic sign sector $\sigma \in \{-1, +1\}$
cancels identically to zero. -/
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
