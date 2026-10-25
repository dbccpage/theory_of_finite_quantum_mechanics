import Mathlib.Tactic

/-!
# Campaign: FSP-NICOLAI-MAP-CLAIM (TFQ-1205 / FSP-DERIV-041)

Formalizes the finite-lattice Nicolai map Jacobian identities, skew-plus-diagonal
determinant positivity under convex superpotentials, multi-branch sign obstructions,
and scope fences for `FSP-NICOLAI-MAP-CLAIM` (`TFQ-1205`, stage `FERMION_SIGN`,
status `OPEN`):

1. **2-Site and 3-Site Periodic Lattice Nicolai Map & Jacobian Identity**:
   For the discrete lattice model $M_F = D_{\mathrm{kin}} + \mathrm{diag}(W''(\phi))$
   (matching `code/python/src/fsp/cdt_susy_witten_evaluator.py::evaluate_nicolai_map`),
   where $D_{\mathrm{kin}}^T = -D_{\mathrm{kin}}$ is the skew-symmetric finite-difference
   kinetic operator and $w_i = W''(\phi_i) = m + c \phi_i^2$, the Jacobian matrix of
   $\xi(\phi) = D_{\mathrm{kin}} \phi + W'(\phi)$ equals $D_F(\phi)$, with
   $\det J_2(w_0, w_1, \kappa) = w_0 w_1 + \kappa^2$ and
   $\det J_3(w_0, w_1, w_2, \kappa) = w_0 w_1 w_2 + \kappa^2 (w_0 + w_1 + w_2)$.
2. **Strict Positivity for Convex Superpotentials ($W''(\phi_i) > 0$)**:
   Whenever $w_i > 0$ (e.g. $w_i = m + c \phi_i^2$ with $m > 0, c \ge 0$),
   both $\det J_2 > 0$ and $\det J_3 > 0$ for all lattice hopping couplings $\kappa \in \mathbb{Z}$.
3. **Branch Multiplicity, Sign-Indefinite Jacobians & SUSY-Breaking Perturbations**:
   - Under $\xi = \mathcal{N}(\phi)$, the volume element transforms by $|\det J|$ while the
     fermionic Gaussian integral supplies $\det J = \mathrm{sgn}(\det J) \cdot |\det J|$.
   - For non-convex superpotentials ($\xi(\phi) = \phi^2 - c$ or $\xi(\phi) = \phi^3 - 3\phi$),
     $\det J(\phi)$ changes sign across critical points ($\det J = 0$), producing opposite-sign
     branches ($\mathrm{sgn} = \pm 1$).
   - Adding a supersymmetry-breaking perturbation $\Delta M$ with $\delta \cdot w_1 > w_0 w_1 + \kappa^2$
     flips $\det(M_F + \Delta M) < 0$.
4. **Scope Fences (`FSP-NICOLAI-MAP-CLAIM`, status `OPEN` preserved)**:
   - Fences the historical placeholder `NicolaiMapSignSuppressionPredicate t t := (t = t)`
     in `papers/core/fsp/lean4/regge_wdw_core.lean:806-810`, which holds even for negative
     determinants `t = -1 < 0`.
   - Preserves `OPEN` status because Nicolai-map constructions are model-specific in the
     literature and do not provide a general sign-elimination theorem for arbitrary lattice
     fermion models.
-/

namespace CampaignFspNicolaiMapClaim

/-- $2 \times 2$ integer matrix entries $(m_{00}, m_{01}, m_{10}, m_{11})$. -/
@[ext]
structure Mat2 where
  m00 : Int
  m01 : Int
  m10 : Int
  m11 : Int
  deriving DecidableEq, Repr

/-- Matrix addition on `Mat2`. -/
def mat2Add (A B : Mat2) : Mat2 :=
  { m00 := A.m00 + B.m00
    m01 := A.m01 + B.m01
    m10 := A.m10 + B.m10
    m11 := A.m11 + B.m11 }

/-- Determinant of a $2 \times 2$ matrix. -/
def mat2Det (A : Mat2) : Int :=
  A.m00 * A.m11 - A.m01 * A.m10

/-- Skew-symmetric 2-site lattice kinetic matrix $D_{\mathrm{kin}}(\kappa) = \begin{pmatrix} 0 & \kappa \\ -\kappa & 0 \end{pmatrix}$. -/
def skewKinetic2Site (kappa : Int) : Mat2 :=
  { m00 := 0, m01 := kappa, m10 := -kappa, m11 := 0 }

/-- Diagonal 2-site superpotential Hessian $\mathrm{diag}(w_0, w_1)$. -/
def diagPotential2Site (w0 w1 : Int) : Mat2 :=
  { m00 := w0, m01 := 0, m10 := 0, m11 := w1 }

/-- 2-site Nicolai map Jacobian matrix $\partial \xi_i / \partial \phi_j$ for
    $\xi_0 = W'_0(\phi_0) + \kappa \phi_1$, $\xi_1 = -\kappa \phi_0 + W'_1(\phi_1)$. -/
def nicolaiJacobian2Site (w0 w1 kappa : Int) : Mat2 :=
  { m00 := w0, m01 := kappa, m10 := -kappa, m11 := w1 }

/-- 2-site fermion operator $D_F = D_{\mathrm{kin}}(\kappa) + \mathrm{diag}(w_0, w_1)$. -/
def fermionMatrix2Site (w0 w1 kappa : Int) : Mat2 :=
  mat2Add (skewKinetic2Site kappa) (diagPotential2Site w0 w1)

/-- Theorem 1: On the 2-site lattice model, the Jacobian matrix of the Nicolai map
    equals the fermion matrix $D_F = D_{\mathrm{kin}} + \mathrm{diag}(w_0, w_1)$, and its
    determinant satisfies $\det J = \det D_F = w_0 w_1 + \kappa^2$. -/
theorem nicolai_map_2site_jacobian_equals_fermion_matrix (w0 w1 kappa : Int) :
    nicolaiJacobian2Site w0 w1 kappa = fermionMatrix2Site w0 w1 kappa ∧
    mat2Det (nicolaiJacobian2Site w0 w1 kappa) = w0 * w1 + kappa * kappa := by
  refine ⟨?_, ?_⟩
  · ext <;> dsimp [nicolaiJacobian2Site, fermionMatrix2Site, mat2Add, skewKinetic2Site, diagPotential2Site] <;> omega
  · dsimp [mat2Det, nicolaiJacobian2Site]
    ring

/-- Theorem 2: Whenever the local superpotential Hessian diagonal entries are positive
    ($w_0 > 0$ and $w_1 > 0$), the 2-site skew-plus-diagonal Nicolai Jacobian determinant
    is strictly positive ($\det D_F \ge 1 + \kappa^2 > 0$) for every kinetic coupling $\kappa \in \mathbb{Z}$. -/
theorem nicolai_2site_skew_plus_positive_diag_det_pos (w0 w1 kappa : Int)
    (hw0 : 0 < w0) (hw1 : 0 < w1) :
    1 + kappa * kappa ≤ mat2Det (fermionMatrix2Site w0 w1 kappa) ∧
    0 < mat2Det (fermionMatrix2Site w0 w1 kappa) := by
  dsimp [fermionMatrix2Site, mat2Add, skewKinetic2Site, diagPotential2Site, mat2Det]
  have h_prod : 1 ≤ w0 * w1 := by nlinarith
  have h_sq : 0 ≤ kappa * kappa := by nlinarith
  refine ⟨by linarith, by linarith⟩

/-- Local Hessian $W''(\phi) = m + c \phi^2$ of the quartic superpotential $W(\phi) = \frac{1}{2} m \phi^2 + \frac{c}{12} \phi^4$
    used in `cdt_susy_witten_evaluator.py::evaluate_nicolai_map`. -/
def quarticSuperpotentialHessian (m c phi : Int) : Int :=
  m + c * (phi * phi)

/-- Theorem 3: For $m > 0$ and $c \ge 0$, the local superpotential Hessian
    $W''(\phi) = m + c \phi^2$ satisfies $W''(\phi) \ge m > 0$ for all $\phi \in \mathbb{Z}$,
    and the resulting 2-site Nicolai Jacobian determinant is bounded below by $m^2 + \kappa^2 > 0$. -/
theorem nicolai_quadratic_superpotential_hessian_lower_bound (m c phi0 phi1 kappa : Int)
    (hm : 0 < m) (hc : 0 ≤ c) :
    m ≤ quarticSuperpotentialHessian m c phi0 ∧
    m ≤ quarticSuperpotentialHessian m c phi1 ∧
    m * m + kappa * kappa ≤
      mat2Det (fermionMatrix2Site
        (quarticSuperpotentialHessian m c phi0)
        (quarticSuperpotentialHessian m c phi1)
        kappa) := by
  dsimp [quarticSuperpotentialHessian, fermionMatrix2Site, mat2Add, skewKinetic2Site, diagPotential2Site, mat2Det]
  have hsq0 : 0 ≤ phi0 * phi0 := by nlinarith
  have hsq1 : 0 ≤ phi1 * phi1 := by nlinarith
  have h0 : 0 ≤ c * (phi0 * phi0) := mul_nonneg hc hsq0
  have h1 : 0 ≤ c * (phi1 * phi1) := mul_nonneg hc hsq1
  have h_prod : m * m ≤ (m + c * (phi0 * phi0)) * (m + c * (phi1 * phi1)) := by nlinarith
  refine ⟨by linarith, by linarith, by linarith⟩

/-- Determinant of the 3-site periodic skew-plus-diagonal Nicolai matrix
    $M_3(w_0, w_1, w_2, \kappa) = \begin{pmatrix} w_0 & \kappa & -\kappa \\ -\kappa & w_1 & \kappa \\ \kappa & -\kappa & w_2 \end{pmatrix}$
    expanded along the first row. -/
def det3SiteSkewPlusDiag (w0 w1 w2 kappa : Int) : Int :=
  w0 * (w1 * w2 - kappa * (-kappa)) -
  kappa * ((-kappa) * w2 - kappa * kappa) +
  (-kappa) * ((-kappa) * (-kappa) - w1 * kappa)

/-- Theorem 4: On a 3-site periodic ring with skew-symmetric nearest-neighbor hopping $\pm \kappa$,
    the determinant of $D_{\mathrm{kin}} + \mathrm{diag}(w_0, w_1, w_2)$ equals
    $w_0 w_1 w_2 + \kappa^2 (w_0 + w_1 + w_2)$, and is strictly positive whenever $w_0, w_1, w_2 > 0$. -/
theorem nicolai_3site_periodic_skew_plus_diag_det_formula (w0 w1 w2 kappa : Int)
    (hw0 : 0 < w0) (hw1 : 0 < w1) (hw2 : 0 < w2) :
    det3SiteSkewPlusDiag w0 w1 w2 kappa = w0 * w1 * w2 + kappa * kappa * (w0 + w1 + w2) ∧
    0 < det3SiteSkewPlusDiag w0 w1 w2 kappa := by
  have h_eq : det3SiteSkewPlusDiag w0 w1 w2 kappa = w0 * w1 * w2 + kappa * kappa * (w0 + w1 + w2) := by
    dsimp [det3SiteSkewPlusDiag]
    ring
  refine ⟨h_eq, ?_⟩
  rw [h_eq]
  have h_w12 : 0 < w0 * w1 := mul_pos hw0 hw1
  have h_w123 : 0 < w0 * w1 * w2 := mul_pos h_w12 hw2
  have h_sum : 0 < w0 + w1 + w2 := by linarith
  have h_k2 : 0 ≤ kappa * kappa := by nlinarith
  have h_ksum : 0 ≤ kappa * kappa * (w0 + w1 + w2) := by nlinarith
  linarith

/-- Sign factor $\mathrm{sgn}(J) \in \{-1, 0, 1\}$ of a branch Jacobian determinant. -/
def branchJacobianSign (J : Int) : Int :=
  if 0 < J then 1 else if J < 0 then -1 else 0

/-- Theorem 5: Under the Nicolai change of variables, the fermionic determinant $J$ on a
    non-singular branch ($J \neq 0$) decomposes as $J = \mathrm{sgn}(J) \cdot |J|$ with
    $\mathrm{sgn}(J) \in \{1, -1\}$, so any branch with $J < 0$ contributes a negative weight
    $-\,|J| < 0$ relative to the positive Gaussian measure $|J|\,d\phi$. -/
theorem nicolai_change_of_variables_branch_sign_decomposition (J : Int) :
    J = branchJacobianSign J * Int.natAbs J ∧
    (0 < J → branchJacobianSign J = 1) ∧
    (J < 0 → branchJacobianSign J = -1) := by
  dsimp [branchJacobianSign]
  split_ifs <;> refine ⟨by omega, fun _ => by omega, fun _ => by omega⟩

/-- 1-site non-convex fold Nicolai map $\xi(\phi) = \phi^2 - c$ and its Jacobian $J(\phi) = 2\phi$. -/
def foldNicolaiMap (c phi : Int) : Int := phi * phi - c
def foldNicolaiJacobian (phi : Int) : Int := 2 * phi

/-- Theorem 6: For the non-convex fold Nicolai map $\xi(\phi) = \phi^2 - c$, every symmetric
    preimage pair $\pm \phi_0$ ($\phi_0 > 0$) maps to the same Gaussian coordinate
    $\xi(\phi_0) = \xi(-\phi_0)$ but carries opposite Jacobian determinants
    $J(\phi_0) = 2\phi_0 > 0$ and $J(-\phi_0) = -2\phi_0 < 0$ whose branch signs cancel:
    $\mathrm{sgn}(J(\phi_0)) + \mathrm{sgn}(J(-\phi_0)) = 0$. -/
theorem non_convex_double_well_nicolai_branch_cancellation (c phi0 : Int) (hphi : 0 < phi0) :
    foldNicolaiMap c phi0 = foldNicolaiMap c (-phi0) ∧
    0 < foldNicolaiJacobian phi0 ∧
    foldNicolaiJacobian (-phi0) < 0 ∧
    branchJacobianSign (foldNicolaiJacobian phi0) +
      branchJacobianSign (foldNicolaiJacobian (-phi0)) = 0 := by
  dsimp [foldNicolaiMap, foldNicolaiJacobian, branchJacobianSign]
  split_ifs <;> refine ⟨by ring, by omega, by omega, by omega⟩

/-- Cubic 1-site Nicolai map $\xi(\phi) = \phi^3 - 3\phi$ and its Jacobian $J(\phi) = 3(\phi^2 - 1)$. -/
def cubicNicolaiMap (phi : Int) : Int := phi * phi * phi - 3 * phi
def cubicNicolaiJacobian (phi : Int) : Int := 3 * (phi * phi - 1)

/-- Theorem 7: For the non-monotonic cubic Nicolai map $\xi(\phi) = \phi^3 - 3\phi$,
    the three preimages $\phi \in \{-2, 0, 2\}$ have Jacobians $J(-2) = 9 > 0$,
    $J(0) = -3 < 0$, and $J(2) = 9 > 0$, witnessing a negative-sign inner branch
    ($\mathrm{sgn}(J(0)) = -1$) alongside two positive outer branches ($\mathrm{sgn}(J(\pm 2)) = +1$). -/
theorem non_monotonic_cubic_nicolai_three_branch_sign_defect :
    cubicNicolaiJacobian (-2) = 9 ∧
    cubicNicolaiJacobian 0 = -3 ∧
    cubicNicolaiJacobian 2 = 9 ∧
    branchJacobianSign (cubicNicolaiJacobian (-2)) = 1 ∧
    branchJacobianSign (cubicNicolaiJacobian 0) = -1 ∧
    branchJacobianSign (cubicNicolaiJacobian 2) = 1 := by
  decide

/-- Theorem 8: Adding a supersymmetry-breaking perturbation $\Delta M = \mathrm{diag}(-\delta, 0)$
    with $\delta \cdot w_1 > w_0 w_1 + \kappa^2$ ($w_1 > 0$) to `fermionMatrix2Site w0 w1 kappa`
    makes the perturbed fermion determinant $(w_0 - \delta) w_1 + \kappa^2 < 0$ strictly negative. -/
theorem susy_breaking_perturbation_induces_negative_determinant (w0 w1 kappa delta : Int)
    (hw0 : 0 < w0) (hw1 : 0 < w1) (h_break : w0 * w1 + kappa * kappa < delta * w1) :
    0 < mat2Det (fermionMatrix2Site w0 w1 kappa) ∧
    mat2Det (fermionMatrix2Site (w0 - delta) w1 kappa) < 0 := by
  dsimp [fermionMatrix2Site, mat2Add, skewKinetic2Site, diagPotential2Site, mat2Det]
  have h_pos : 0 < w0 * w1 + kappa * kappa := by nlinarith
  refine ⟨by linarith, by linarith⟩

/-- Historical placeholder predicate from `papers/core/fsp/lean4/regge_wdw_core.lean:806-810`. -/
def NicolaiMapSignSuppressionPredicate (t1 t2 : Int) : Prop := t1 = t2

/-- Theorem 9: Scope fence against the historical `NicolaiMapSignSuppressionPredicate t t`
    placeholder in `regge_wdw_core.lean:806-810`: the predicate `t = t` holds for
    a negative fermion determinant `t = -1 < 0` and therefore does not witness positivity
    $\det D_F > 0$. -/
theorem withdrawn_regge_wdw_core_tautology_fence :
    NicolaiMapSignSuppressionPredicate (-1) (-1) ∧ (-1 : Int) < 0 := by
  exact ⟨rfl, by decide⟩

/-- Scope fence structure (`FSP-NICOLAI-MAP-CLAIM`): separates 1D/2-site convex skew-plus-diagonal
    determinant positivity from claims of universal sign elimination for arbitrary lattice fermion models. -/
structure NicolaiModelInterpretation where
  convexSkewDetPositive : Bool
  unbrokenResidualZero : Bool
  generalizesToArbitraryLatticeFermions : Bool
  deriving DecidableEq, Repr

/-- Projection retaining only the verified convex skew-plus-diagonal lattice properties. -/
def nicolaiVerifiedCore (x : NicolaiModelInterpretation) : Bool × Bool :=
  (x.convexSkewDetPositive, x.unbrokenResidualZero)

/-- Theorem 10: Scope fence (`FSP-NICOLAI-MAP-CLAIM`) — the verified positivity of
    $\det(D_{\mathrm{kin}} + \mathrm{diag}(W''(\phi))) > 0$ on the convex 1D/2-site lattice
    model is compatible with both asserting and withholding generalization to arbitrary
    lattice fermion theories, justifying keeping the node status `OPEN`. -/
theorem nicolai_map_model_specificity_scope_fence :
    let overclaimedInterp : NicolaiModelInterpretation :=
      { convexSkewDetPositive := true
        unbrokenResidualZero := true
        generalizesToArbitraryLatticeFermions := true }
    let scopedInterp : NicolaiModelInterpretation :=
      { convexSkewDetPositive := true
        unbrokenResidualZero := true
        generalizesToArbitraryLatticeFermions := false }
    nicolaiVerifiedCore overclaimedInterp = nicolaiVerifiedCore scopedInterp ∧
    overclaimedInterp ≠ scopedInterp ∧
    overclaimedInterp.generalizesToArbitraryLatticeFermions ≠
      scopedInterp.generalizesToArbitraryLatticeFermions := by
  decide

end CampaignFspNicolaiMapClaim
