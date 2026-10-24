Status: AI-drafted, awaiting human review.
AuthorityEffect: None.

# Independent Derivation Note: `FSP-DISCRETE-WDW-CONSTRAINT` (`TFQ-1213` / `FSP-DERIV-049`)

- **Node ID**: `FSP-DISCRETE-WDW-CONSTRAINT` (`TFQ-1213`)
- **Source Record**: `FSP-DERIV-049` (`papers/core/fsp/theory_of_finite_fsp.md:681-693`, `papers/core/fsp/the_problem_of_the_fermion_sign.md:170-173`)
- **Stage**: `FERMION_SIGN`
- **Status**: `OPEN` (`E1 -> E3`, `L4D`)
- **Lean 4 Module**: `lean4/CampaignFspDiscreteWdwConstraint.lean`
- **Independent Checker**: `checks/independent/fsp-discrete-wdw-constraint.py`

---

## 1. Narrowed Mathematical Scope

`FSP-DERIV-049` claims that a discrete Wheeler-DeWitt operator $H_\perp$ on spatial triangulations is non-negative and acts as a projection onto diffeomorphism-invariant states. In `code/python/src/fsp/regge_pachner_wdw.py`, the evaluated model is a direct-sum gauge cochain system $\Omega = (p_{\text{edge}}, h_\perp)^T \in C^1(K) \oplus C^0(K)$ with joint operator $D_{\text{joint}} = [d_0, 0]^T$, while in the continuum the DeWitt kinetic supermetric has indefinite signature $(-, +, +, +, +, +)$. Moreover, Section 2.5 of `papers/core/fsp/the_problem_of_the_fermion_sign.md` (`lines 170-173`) explicitly separates the Wheeler-DeWitt constraint $H_\perp |\Psi\rangle = 0$ from thermal canonical Gibbs ensembles $\operatorname{Tr}(e^{-\beta H})$.

In `lean4/CampaignFspDiscreteWdwConstraint.lean` and `checks/independent/fsp-discrete-wdw-constraint.py`, we replace the missing `ReggePachnerWdw.lean::wheeler_dewitt_constraint_null_kernel` and the `Nat`-only lemma `wdw_defect_unscreenable` (`(p - alpha) + h_wdw > 0`) with 10 kernel-checked theorems over $\mathbb{Q}$ while keeping the node status `OPEN`:
1. Linearity and constant-cochain kernel of $D_{\text{joint}} = [d_0, 0]^T$ (`dJoint_linear_and_constant_kernel`).
2. Signed rational unscreenability $\|h_\perp\|_1 \le \|p - d_0 \alpha\|_1 + \|h_\perp\|_1$, with strict positivity whenever any vertex has $h_\perp(v_0) \ne 0$ (`primal_l1_edge_and_vertex_residual_lower_bound`).
3. Exact strong $\ell_1$ duality on exact-coboundary momentum states $p = d_0 \alpha$ via the dual witness $W^* = (0, \operatorname{sgn}(h_\perp))$ (`strong_duality_direct_sum_wdw_exact_coboundary`).
4. Exact flat ($0$, `.ExactRepair`) vs curved ($45$, `.SplitBrainRefusal`) defect receipts on the $\partial \Delta^5 \cong S^4$ seed (`s4_seed_flat_vs_curved_wdw_defect_mass`).
5. Finite quadratic constraint operator $H_\perp = L^T L$ positive semidefiniteness and null-kernel equivalence (`quadratic_constraint_psd_and_null_kernel_iff`).
6. Idempotent 2-state diffeomorphism-averaging projector $P_{\text{inv}}$ and complementary constraint $H_\perp = I - P_{\text{inv}}$ (`diffeomorphism_averaging_projector_and_constraint_complement`).
7. 2-tick Page-Wootters clock conditioning $H_{\text{PW}}(\Psi_0, \Psi_1) = (0, 0) \iff \Psi_1 = U \Psi_0$ (`page_wootters_clock_system_conditioned_evolution`).
8. Explicit scope fences for DeWitt supermetric indefiniteness (`dewitt_supermetric_indefinite_signature_fence`), Section 2.5 WDW zero-mode kernel vs thermal Gibbs trace distinctness (`wdw_constraint_kernel_vs_thermal_gibbs_trace_fence`), and fermionic sign-sector independence (`wdw_constraint_projection_preserves_fermion_sign_cancellation_fence`).

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - Exact rational primal-dual $\ell_1$ unscreenability and strong duality for the direct-sum Regge-WDW cochain system $D_{\text{joint}} = [d_0, 0]^T$, finite $L^T L$ and idempotent projector kernel equivalences, 2-tick Page-Wootters conditioning, and explicit fences for DeWitt kinetic indefiniteness and Section 2.5 thermal-vs-WDW separation.
2. **What it does not support**:
   - Does not construct a continuum diffeomorphism-invariant Wheeler-DeWitt projector, overcome the indefinite signature of the continuum DeWitt supermetric, or resolve any fermionic path-integral sign problem.
3. **Narrowest defensible claim**:
   - Within the declared finite rational cochain and matrix models, scalar vertex defects $h_\perp \in C^0(K; \mathbb{Q})$ cannot be screened by edge coboundaries $d_0 \alpha$, finite quadratic constraints $L^T L$ are non-negative on $\mathbb{Q}^n$ whereas the continuum DeWitt form $-v_{\text{conf}}^2 + v_{\text{trans}}^2$ is indefinite, and the zero-eigenvalue constraint subspace $\ker(H)$ is distinct from the thermal Gibbs trace.
4. **Next test needed**:
   - Formalize the combinatorial 4D bistellar Pachner moves ($1 \leftrightarrow 5$, $2 \leftrightarrow 4$, $3 \leftrightarrow 3$) on `FSP-PACHNER-INVARIANCE-CLAIM` (`TFQ-1214`) and contrast topological invariant preservation ($\Delta \chi = 0$) with Regge action and WDW defect non-invariance.
