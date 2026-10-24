# Independent Derivation & Scope Narrowing: `FSP-BF-2GROUP-SIGN-CLAIM` (`TFQ-1210` / `FSP-DERIV-046`)

## 1. Node Identity and Epistemic Contract

- **Node ID**: `FSP-BF-2GROUP-SIGN-CLAIM` (`TFQ-1210` / `FSP-DERIV-046`)
- **Stage**: `FERMION_SIGN`
- **Status**: `OPEN` (narrowed to exact finite simplicial cochain, braiding, and $H^3(B\mathbb{Z}_2, \mathbb{Z}_2)$ Postnikov cohomology theorems together with `GIN-C19`–`GIN-C21` model-change scope fences in Lean 4 and an independent exact-arithmetic Python verifier)
- **Lean 4 Module**: [`lean4/CampaignFspBf2GroupSignClaim.lean`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean) (`L4D`, 11 theorems, 0 `sorry`, standard Lean 4 axioms only, 6/6 semantic mutations killed)
- **Independent Python Verifier**: [`checks/independent/fsp-bf-2group-sign-claim.py`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/checks/independent/fsp-bf-2group-sign-claim.py)

---

## 2. Exact Finite Cochain, Braiding, and Postnikov Cohomology Formulation

In [`papers/core/fsp/the_problem_of_the_fermion_sign.md`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/papers/core/fsp/the_problem_of_the_fermion_sign.md#L733-L828) (Sections 9.14–9.16) and [`papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md#L29-L31) (`GIN-C19`–`GIN-C21`), the finite algebraic claims and their scope boundaries decompose into five exact components:

1. **Simplicial Cochain Complex Nilpotence and Discrete BF Gauge Invariance on $\Delta^4$**:
   - On the 4-simplex $\Delta^4$ ($\mathrm{Fin}\ 5$) with values in any commutative additive group $A$, the simplicial coboundaries $d_0, d_1, d_2, d_3$ satisfy exact nilpotence $d_1 \circ d_0 = 0$, $d_2 \circ d_1 = 0$, and $d_3 \circ d_2 = 0$ ([`simplicial_coboundary_nilpotence_d1d0_d2d1_d3d2`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L68-L78)).
   - Under 1-form gauge transformations $A_1 \mapsto A_1 + d_0 \lambda$ and 2-form Kalb-Ramond shifts $B_2 \mapsto B_2 + d_1 \eta$, the discrete curvatures $d_1(A_1 + d_0 \lambda) = d_1 A_1$ and $d_2(B_2 + d_1 \eta) = d_2 B_2$ are strictly invariant ([`bf_cochain_gauge_invariance`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L83-L92)).

2. **Abelian $\mathbb{Z}_k$ BF Braiding Level-Parity Trichotomy (`GIN-C19`)**:
   - Under loop orientation inversion $\mathrm{lk} \mapsto -\mathrm{lk}$, the linking product negates: $q p (-\mathrm{lk}) = - q p \mathrm{lk}$. At level $k = 2$ ($\mathbb{Z}_2$ BF / 3D toric code) with $q = p = \mathrm{lk} = 1$, the Hopf-link phase is $(-1)^1 = -1$; symmetric doublet weights $w_+ = w_-$ cancel ($w_+ - w_- = 0$), whereas thermal orientation asymmetry $w_+ \neq w_-$ leaves a nonzero residual $w_+ - w_- \neq 0$ ([`bf_z2_level_hopf_link_sign_and_weight_trichotomy`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L98-L108)).
   - At level $k = 3$ ($\mathbb{Z}_3$ fractional BF), representing $\omega = e^{2\pi i/3}$ on $\mathbb{Z}[\omega] \cong \mathbb{Z}^2$ by its $\mathrm{SL}(2, \mathbb{Z})$ companion matrix $\mathrm{omega3Mat} = \begin{pmatrix} 0 & -1 \\ 1 & -1 \end{pmatrix}$, we have $\mathrm{omega3Mat}^3 = I_2$, $\mathrm{omega3Mat}^2 \neq I_2$, and $\mathrm{omega3Mat} + \mathrm{omega3Mat}^2 = -I_2$ with trace $-2$ (encoding $2\cos(2\pi/3) = -1 < 0$), showing that orientation-reversal pairing at $k = 3$ produces negative real weight rather than $+1$ ([`bf_z3_level_non_involution_and_cos_sum_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L118-L130)).

3. **Non-Abelian Wang-Levin 3-Loop Braiding Commutator (`GIN-C20`)**:
   - In the 2D internal fusion channel of $SU(2)_2$ (Ising level), the involutive monodromy generators $B_1 = \sigma_z$ and $B_2 = \sigma_x$ satisfy $B_1^2 = B_2^2 = I_2$ and have Borromean group commutator $M_{\text{WL}} = B_1 B_2 B_1^{-1} B_2^{-1} = -I_2$ with negative trace $\mathrm{Tr}(M_{\text{WL}}) = -2 < 0$, whereas diagonal abelian monodromy matrices commute ($D_1 D_2 = D_2 D_1$) ([`wang_levin_ising_commutator_negative_trace_and_abelian_commutation`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L149-L162)).

4. **Strict 2-Group Crossed Module and Nontrivial Postnikov Class $[a] \in H^3(B\mathbb{Z}_2, \mathbb{Z}_2)$ (`GIN-C21`)**:
   - For any group $G$, the conjugation crossed module $(G, G, \mathrm{id}, \mathrm{conj})$ satisfies both the Peiffer identity and the second crossed-module identity ([`crossed_module_conjugation_peiffer_and_identity`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L167-L171)).
   - On $G = \mathbb{Z}_2$ with coefficients in $H = \mathbb{Z}_2$, the cup-product 3-cochain $a(g_1, g_2, g_3) = g_1 g_2 g_3$ satisfies the group 3-cocycle condition $\delta_3 a = 0$ on all $(\mathbb{Z}_2)^4$ and evaluates to $1 \neq 0$ at $(1,1,1)$ ([`postnikov_cup3_is_3cocycle_on_zmod2`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L190-L194)).
   - Every 2-coboundary $\delta_2 b$ ($b : (\mathbb{Z}_2)^2 \to \mathbb{Z}_2$) has vanishing $\mathbb{RP}^3$ 3-cycle pairing $(\delta_2 b)(1,0,0) + (\delta_2 b)(0,0,1) + (\delta_2 b)(1,1,1) = 0$, whereas $a(1,0,0) + a(0,0,1) + a(1,1,1) = 1 \neq 0$, establishing that $\forall b, \delta_2 b \neq a$ (`[a] \neq 0 \in H^3(B\mathbb{Z}_2, \mathbb{Z}_2)`) ([`postnikov_cup3_not_coboundary_in_H3_zmod2`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L203-L213)).
   - Feeding a flat 1-cochain $g = d_0 \phi$ on $\Delta^4$ into $a$ produces a simplicial 3-cochain $C_3(i,j,k,l) = a(g_{ij}, g_{jk}, g_{kl})$ whose simplicial 3-coboundary vanishes identically ($d_3 C_3 = 0$) ([`two_connection_postnikov_3curvature_bianchi`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L218-L230)).

5. **Doubled-Trace Model-Change Scope Fence (`GIN-C20` / `GIN-C21`, Manuscript Line 448)**:
   - While pairing the Postnikov class $a$ with its conjugate $-a$ cancels the cohomology class ($a - a = 0$) and squares $\pm 1$ signs to $+1$ ([`one_form_double_vs_conjugate_two_group_postnikov_cancellation`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L236-L243)), replacing a chiral partition sum $Z$ by $Z^2$ or replacing configuration weights $w_i$ by $w_i^2$ changes the target model ([`doubled_partition_function_changes_target_model_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean#L251-L256)): opposite-sign partition sums $Z_+ = 2$ and $Z_- = -2$ map to the same square $4$, and squaring weights in a canceling doublet $(1, -1)$ changes the sum from $1 + (-1) = 0$ to $1^2 + (-1)^2 = 2 \neq (1 + (-1))^2$.

---

## 3. Summary of Claims (Claim Hygiene Compliance)

1. **What it supports**:
   - Formalizes in Lean 4 ([`lean4/CampaignFspBf2GroupSignClaim.lean`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean)) and an independent exact-arithmetic Python verifier ([`checks/independent/fsp-bf-2group-sign-claim.py`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/checks/independent/fsp-bf-2group-sign-claim.py)) simplicial coboundary nilpotence $d_1 d_0 = d_2 d_1 = d_3 d_2 = 0$, discrete BF gauge invariance, the $\mathbb{Z}_2$ vs $\mathbb{Z}_3$ BF braiding trichotomy, the non-abelian Wang-Levin Ising commutator $M_{\text{WL}} = -I_2$, the nontriviality of the Postnikov 3-cocycle $a(g_1,g_2,g_3) = g_1 g_2 g_3$ in $H^3(B\mathbb{Z}_2, \mathbb{Z}_2)$, and the doubled-trace model-change fence (`GIN-C19`–`GIN-C21`).
2. **What it does not support**:
   - Does not claim that Drinfeld or higher 2-double norm-squaring ($Z \mapsto |Z|^2$) is a model-preserving sign solver for the single chiral BF or 2-group theory (`GIN-C20`–`GIN-C21`), nor does it evaluate continuum path integrals on smooth 4-manifolds.
3. **Narrowest defensible claim**:
   - On finite simplicial and group cochain complexes, $a(g_1, g_2, g_3) = g_1 g_2 g_3$ is a non-exact 3-cocycle in $H^3(B\mathbb{Z}_2, \mathbb{Z}_2)$ whose induced $(-1)^a$ sign cancels under conjugate $[a] \oplus (-[a])$ 2-double pairing only by changing the target partition function from the chiral model to the doubled norm-square model.
4. **Next test needed**:
   - Narrow `FSP-COBORDISM-INTRINSIC-SIGN` (`TFQ-1211` / `FSP-DERIV-047`) in the fermion-sign frontier queue.
