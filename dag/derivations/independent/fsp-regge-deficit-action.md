Status: AI-drafted, awaiting human review.
AuthorityEffect: None.

# Independent Derivation Note: `FSP-REGGE-DEFICIT-ACTION` (`TFQ-1212` / `FSP-DERIV-048`)

- **Node ID**: `FSP-REGGE-DEFICIT-ACTION` (`TFQ-1212`)
- **Source Record**: `FSP-DERIV-048` (`papers/core/fsp/theory_of_finite_fsp.md:668-680`, `papers/core/fsp/the_problem_of_the_fermion_sign.md:542-582`)
- **Stage**: `FERMION_SIGN`
- **Status**: `IMPORTED_ASSUMPTION` (Narrowed with explicit `GIN-C13` scope fences)
- **Lean 4 Module**: `lean4/CampaignFspReggeDeficitAction.lean`
- **Independent Checker**: `checks/independent/fsp-regge-deficit-action.py`

---

## 1. Narrowed Mathematical Scope

On a 4D simplicial complex with squared edge lengths $s_{ij}$, the deficit angle at a triangular hinge $h$ is $\epsilon_h = 2\pi - \sum_{\sigma > h} \theta_{h,\sigma}$ and the Regge action is $S_{\text{Regge}} = \sum_h A_h \epsilon_h$. Its continuum convergence under refinement to the Einstein-Hilbert action (Regge 1961; Cheeger-Müller-Schrader 1984) is an external differential-geometric import (`IMPORTED_ASSUMPTION`), and ledger item `GIN-C13` records that Regge calculus carries no fermion-sign content in this package.

In `lean4/CampaignFspReggeDeficitAction.lean` and `checks/independent/fsp-regge-deficit-action.py`, we replace the missing `ReggePachnerWdw.lean::regge_deficit_angle_action_identity` and unbuilt cyclic-assumption file with 10 kernel-checked theorems covering:
1. Exact Heron / Cayley-Menger squared triangle area `heronAreaSq s01 s12 s02` and the hinge classes of `orthogonal_pentatope` ($6$ right triangles with $A_h^2 = 1/4$ and $4$ equilateral triangles with $A_h^2 = 3/4$, summing to $9/2$).
2. Hinge deficit flatness criterion and bilinearity of `reggeAction`.
3. Non-negativity of `reggeAction` when $A_h \ge 0$ and $\epsilon_h \ge 0$, contrasted with negative/zero values under mixed-sign (hyperbolic/saddle) deficits.
4. Simplicial combinatorics and Euler characteristic $\chi(\partial \Delta^5) = 6 - 15 + 20 - 15 + 6 = 2$ of the 4-sphere boundary $\partial \Delta^5$.
5. Exact cyclic holonomy telescoping $(f_1 - f_0) + (f_2 - f_1) + (f_3 - f_2) + (f_0 - f_3) = 0$ for the discrete first Bianchi identity (derived by ring identity rather than assumed).
6. Schläfli variational reduction $\sum_h (dA_h \epsilon_h - A_h d\theta_h) = \sum_h dA_h \epsilon_h$ when $\sum_h A_h d\theta_h = 0$.
7. Exact rational Cheeger-Müller-Schrader refinement bound predicate `defectBoundHolds` matching `code/rust/src/general_relativity/exact_regge/action.rs`.
8. Explicit `GIN-C13` scope fences for fermion-sign independence, Lorentzian half-turn phase sign reversal, and `Nat` vs signed `ℚ` deficit cancellation.

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - Exact rational Cayley-Menger hinge squared areas on `orthogonal_pentatope`, bilinear Regge action identities, $\partial \Delta^5$ Euler characteristic $\chi = 2$, cyclic holonomy telescoping, Schläfli variational reduction, and the `action.rs` rational refinement bound predicate.
2. **What it does not support**:
   - Does not derive Cheeger-Müller-Schrader continuum convergence from finite algebra, and does not provide any fermion-sign resolution from Regge gravity (`GIN-C13`).
3. **Narrowest defensible claim**:
   - Within the finite rational simplicial model, `heronAreaSq` and `reggeAction` satisfy edge-swap symmetry, bilinearity, cyclic Bianchi telescoping, and Schläfli reduction, while remaining independent of fermionic sign sectors $\sigma \in \{-1, +1\}$.
4. **Next test needed**:
   - Couple a discrete spin-connection / Dirac hopping operator on a 4D simplicial triangulation to test how hinge curvature defects interact with fermionic determinant signs.
