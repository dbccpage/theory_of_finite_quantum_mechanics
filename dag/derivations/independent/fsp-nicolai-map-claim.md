Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `FSP-NICOLAI-MAP-CLAIM` (`TFQ-1205` / `FSP-DERIV-041`)

AuthorityEffect: None.

## 1. What This Derivation Supports

1. **2-Site and 3-Site Periodic Lattice Nicolai Map Jacobian Identities**:
   On a finite periodic ring with skew-symmetric nearest-neighbor kinetic operator $D_{\mathrm{kin}}(\kappa)^T = -D_{\mathrm{kin}}(\kappa)$ and local superpotential Hessian diagonal $\mathrm{diag}(w_i)$ (matching `code/python/src/fsp/cdt_susy_witten_evaluator.py::evaluate_nicolai_map`), the Jacobian matrix of the lattice Nicolai map $\xi(\phi) = D_{\mathrm{kin}}(\kappa)\phi + W'(\phi)$ equals the fermion matrix $D_F(\phi) = D_{\mathrm{kin}}(\kappa) + \mathrm{diag}(w_i)$ (`nicolai_map_2site_jacobian_equals_fermion_matrix`), with exact determinant formulas
   $$\det J_2(w_0, w_1, \kappa) = w_0 w_1 + \kappa^2, \qquad \det J_3(w_0, w_1, w_2, \kappa) = w_0 w_1 w_2 + \kappa^2(w_0 + w_1 + w_2)$$
   (`nicolai_3site_periodic_skew_plus_diag_det_formula`).
2. **Strict Positivity Under Convex Superpotentials ($W''(\phi_i) > 0$)**:
   Whenever $w_i > 0$ (in particular for the quartic superpotential Hessian $W''(\phi_i) = m + c \phi_i^2 \ge m > 0$ with $m > 0, c \ge 0$), the 2-site and 3-site skew-plus-diagonal Nicolai Jacobian determinants are strictly positive ($\det J_2 \ge m^2 + \kappa^2 > 0$ and $\det J_3 > 0$) for every kinetic coupling $\kappa \in \mathbb{Z}$ (`nicolai_2site_skew_plus_positive_diag_det_pos`, `nicolai_quadratic_superpotential_hessian_lower_bound`).
3. **Branch Multiplicity, Non-Convex Sign Cancellation, and SUSY-Breaking Sign Flips**:
   - Under $\xi = \mathcal{N}(\phi)$, a non-singular branch Jacobian $J \neq 0$ factors as $J = \mathrm{sgn}(J) \cdot |J|$ relative to the positive measure $|J|\,d\phi$ (`nicolai_change_of_variables_branch_sign_decomposition`).
   - For the non-convex fold map $\xi(\phi) = \phi^2 - c$, symmetric preimages $\pm \phi_0$ ($\phi_0 > 0$) share $\xi(\phi_0) = \xi(-\phi_0)$ while carrying opposite Jacobians $\pm 2\phi_0$ whose branch signs cancel (`non_convex_double_well_nicolai_branch_cancellation`).
   - For the non-monotonic cubic map $\xi(\phi) = \phi^3 - 3\phi$, the inner branch $\phi = 0$ has $J(0) = -3 < 0$ while the outer branches $\phi = \pm 2$ have $J(\pm 2) = +9 > 0$ (`non_monotonic_cubic_nicolai_three_branch_sign_defect`).
   - Adding a supersymmetry-breaking perturbation $\Delta M = \mathrm{diag}(-\delta, 0)$ with $\delta \cdot w_1 > w_0 w_1 + \kappa^2$ flips the determinant negative (`susy_breaking_perturbation_induces_negative_determinant`).

## 2. What This Derivation Does Not Support

1. **Historical Placeholder Fence (`regge_wdw_core.lean:806-810`)**:
   As shown in `withdrawn_regge_wdw_core_tautology_fence`, the historical predicate `NicolaiMapSignSuppressionPredicate t t := (t = t)` holds reflexively even for negative determinants `t = -1 < 0` and does not witness $\det D_F > 0$.
2. **Model-Specificity Scope Fence (`OPEN` Status Preserved)**:
   As shown in `nicolai_map_model_specificity_scope_fence`, positive skew-plus-diagonal determinants in 1D/2D off-shell models with convex superpotentials do not establish a general sign-free Nicolai map for arbitrary lattice fermion Hamiltonians or 4D chiral gauge theories.

## 3. Narrowest Defensible Claim

On the 2-site and 3-site periodic skew-plus-diagonal lattice models, the Nicolai Jacobian matrix equals $D_{\mathrm{kin}} + \mathrm{diag}(W''(\phi))$ with strictly positive determinant whenever $W''(\phi_i) > 0$, whereas non-convex superpotentials and supersymmetry-breaking perturbations admit negative branch Jacobians $\det J < 0$, and the node remains `OPEN` outside model-specific convex off-shell constructions.

## 4. Next Test Needed

Construct an explicit off-shell supersymmetric lattice action in $D \ge 2$ dimensions with proven constant global mapping degree $\deg(\mathcal{N}) \neq 0$ and verify observable equivalence across preimage branches.
