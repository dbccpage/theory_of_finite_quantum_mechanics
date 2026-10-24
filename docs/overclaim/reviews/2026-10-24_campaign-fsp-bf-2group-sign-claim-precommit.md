# Pre-Commit Claim Hygiene & Scope Review: `FSP-BF-2GROUP-SIGN-CLAIM` (`TFQ-1210`)

- **Date**: 2026-10-24
- **Branch**: `campaign/fsp-bf-2group-sign-claim`
- **Target Node**: `FSP-BF-2GROUP-SIGN-CLAIM` (`TFQ-1210` / `FSP-DERIV-046`, `FERMION_SIGN`)
- **Status**: `OPEN` (narrowed to exact finite simplicial cochain, braiding, and $H^3(B\mathbb{Z}_2, \mathbb{Z}_2)$ Postnikov cohomology theorems together with `GIN-C19`–`GIN-C21` model-change scope fences, `E1 -> E3`)

## 1. What It Supports
- Formalizes in [`lean4/CampaignFspBf2GroupSignClaim.lean`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspBf2GroupSignClaim.lean) (`L4D`, 11 theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed) and [`checks/independent/fsp-bf-2group-sign-claim.py`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/checks/independent/fsp-bf-2group-sign-claim.py) (`checks=4326`, `failures=0`) the finite cochain, braiding, and cohomology components of `TFQ-1210`:
  1. Simplicial coboundary nilpotence $d_1 \circ d_0 = 0$, $d_2 \circ d_1 = 0$, $d_3 \circ d_2 = 0$ on $\Delta^4$ and discrete BF 1-form/2-form gauge invariance.
  2. Abelian $\mathbb{Z}_k$ BF braiding level-parity trichotomy (`GIN-C19`): Hopf-link sign $-1$ at $k = 2$ with equal-weight doublet cancellation vs orientation-asymmetry residual, and the $\mathrm{SL}(2, \mathbb{Z})$ cyclotomic companion matrix at $k = 3$ showing $\mathrm{omega3Mat}^2 \neq I_2$ and $\mathrm{omega3Mat} + \mathrm{omega3Mat}^2 = -I_2$ (trace $-2$).
  3. Non-abelian Wang-Levin 3-loop Borromean braiding commutator in the 2D $SU(2)_2$ (Ising) fusion channel (`GIN-C20`), yielding $M_{\text{WL}} = -I_2$ with negative trace $-2$, contrasted with commuting diagonal abelian monodromy matrices.
  4. Conjugation strict crossed-module Peiffer laws and non-exactness of the cup-product Postnikov 3-cocycle $a(g_1, g_2, g_3) = g_1 g_2 g_3$ in $H^3(B\mathbb{Z}_2, \mathbb{Z}_2)$ ($\forall b : (\mathbb{Z}_2)^2 \to \mathbb{Z}_2, \delta_2 b \neq a$) (`GIN-C21`).
  5. Explicit model-change scope fence (`GIN-C20`–`GIN-C21`, manuscript line 448): squaring a partition sum ($Z \mapsto Z^2$) or squaring configuration weights ($w_i \mapsto w_i^2$) collapses $Z_+ = 2$ and $Z_- = -2$ to $4$ and alters $(1 + (-1))^2 = 0$ to $1^2 + (-1)^2 = 2$.

## 2. What It Does Not Support
- Does not claim that Drinfeld or higher 2-double norm-squaring ($Z \mapsto |Z|^2$) is a model-preserving sign solver for the single chiral BF or 2-group theory (`GIN-C20`–`GIN-C21`), nor does it evaluate continuum path integrals on smooth 4-manifolds.

## 3. Narrowest Defensible Claim
- On finite simplicial and group cochain complexes, $a(g_1, g_2, g_3) = g_1 g_2 g_3$ is a non-exact 3-cocycle in $H^3(B\mathbb{Z}_2, \mathbb{Z}_2)$ whose induced $(-1)^a$ sign cancels under conjugate $[a] \oplus (-[a])$ 2-double pairing only by changing the target partition function from the chiral model to the doubled norm-square model.

## 4. Next Test Needed
- Narrow `FSP-COBORDISM-INTRINSIC-SIGN` (`TFQ-1211` / `FSP-DERIV-047`) in the fermion-sign frontier queue.
