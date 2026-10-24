# Pre-Commit Claim Hygiene & Overclaim Review: `FSP-DISCRETE-WDW-CONSTRAINT` (`TFQ-1213`)

- **Date**: 2026-10-24
- **Branch**: `campaign/fsp-discrete-wdw-constraint`
- **Target Node**: `FSP-DISCRETE-WDW-CONSTRAINT` (`TFQ-1213` / `FSP-DERIV-049`)
- **Stage**: `FERMION_SIGN`
- **Status**: `OPEN` (`E1 -> E3`, `L4D`)
- **AuthorityEffect**: `None`

## 1. What It Supports
- `lean4/CampaignFspDiscreteWdwConstraint.lean` (10 exported theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed) formalizes:
  - Linearity and constant-cochain kernel of the direct-sum Regge-WDW operator $D_{\text{joint}} = [d_0, 0]^T$ (`dJoint_linear_and_constant_kernel`).
  - Signed rational unscreenability $\|h_\perp\|_1 \le \|p - d_0 \alpha\|_1 + \|h_\perp\|_1$ and strict positivity whenever any vertex has $h_\perp(v_0) \ne 0$ (`primal_l1_edge_and_vertex_residual_lower_bound`), plus exact strong $\ell_1$ duality on exact-momentum states via $W^* = (0, \operatorname{sgn}(h_\perp))$ (`strong_duality_direct_sum_wdw_exact_coboundary`).
  - Exact flat ($0$, `.ExactRepair`) vs curved ($45$, `.SplitBrainRefusal`) WDW defect receipts on the $\partial \Delta^5 \cong S^4$ seed (`s4_seed_flat_vs_curved_wdw_defect_mass`).
  - Finite quadratic constraint operator $H_\perp = L^T L$ positive semidefiniteness (`quadratic_constraint_psd_and_null_kernel_iff`), idempotent 2-state diffeomorphism projector $P_{\text{inv}}$ and complement $H_\perp = I - P_{\text{inv}}$ (`diffeomorphism_averaging_projector_and_constraint_complement`), and 2-tick Page-Wootters clock conditioning (`page_wootters_clock_system_conditioned_evolution`).
  - Scope fences for DeWitt kinetic supermetric indefiniteness (`dewitt_supermetric_indefinite_signature_fence`), Section 2.5 WDW zero-mode kernel vs thermal Gibbs trace distinctness (`wdw_constraint_kernel_vs_thermal_gibbs_trace_fence`), and fermionic sign-sector independence (`wdw_constraint_projection_preserves_fermion_sign_cancellation_fence`).
- `checks/independent/fsp-discrete-wdw-constraint.py` independently verifies all rational identities and scope fences with zero failures.

## 2. What It Does Not Support
- Does not construct a continuum Wheeler-DeWitt diffeomorphism projector, remove the indefinite signature of the continuum DeWitt supermetric, or claim any fermion-sign resolution from gravitational constraint projection.

## 3. Narrowest Defensible Claim
- Within the declared finite rational cochain and matrix models, scalar vertex defects $h_\perp \in C^0(K; \mathbb{Q})$ are unscreenable by edge coboundaries $d_0 \alpha$, finite quadratic constraints $L^T L$ are non-negative whereas the DeWitt form $-v_{\text{conf}}^2 + v_{\text{trans}}^2$ is indefinite, and the WDW constraint subspace $\ker(H)$ is distinct from the thermal Gibbs trace (Section 2.5).

## 4. Next Test Needed
- Formalize the 4D bistellar Pachner moves ($1 \leftrightarrow 5$, $2 \leftrightarrow 4$, $3 \leftrightarrow 3$) on `FSP-PACHNER-INVARIANCE-CLAIM` (`TFQ-1214`) and contrast Euler characteristic invariance ($\Delta \chi = 0$) with Regge action and WDW defect variation.
