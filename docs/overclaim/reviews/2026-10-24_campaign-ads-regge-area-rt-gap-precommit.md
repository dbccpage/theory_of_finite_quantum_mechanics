Status: AI-drafted, awaiting human review.

# Pre-Commit Overclaim & Falsification Review: `ADS-REGGE-AREA-RT-GAP` (`TFQ-2211`)

**Date:** 2026-10-24  
**Campaign Node:** `ADS-REGGE-AREA-RT-GAP` (`TFQ-2211`, stage `ADS_CFT`)  
**Outcome:** `Narrowed` (`OPEN` status preserved; narrowed to exact carrier and `intervalMincut` value-distribution census on the 380 HaPPY intervals, subdivision collapse of squared hinge areas vs. subdivision invariance of linear areas, and holonomy-defect decoupling fences in Lean 4 and an independent Python verifier)  
**AuthorityEffect:** `None`

---

## 1. Falsification & Boundary Audit

1. **Simplicial Hinge Carrier vs. HaPPY Tensor-Network Cut Spectrum Census**:
   - In `lean4/CampaignAdsReggeAreaRtGap.lean`, `simplicial_regge_vs_happy_network_carrier_counts`, `happy_mincut_value_distribution_380`, and `no_uniform_hinge_to_bond_unit_dictionary` compare the 4D `orthogonal_pentatope` hinge carrier (`6` right triangles of squared area `1/4` and `4` equilateral triangles of squared area `3/4`, plus `240` Kuhn pentatopes on `closed_s4_cube_boundary`) with the 20-qubit 6-pentagon HaPPY `{5,4}` network, where `intervalMincut` across all `380` proper contiguous boundary intervals takes values `{1, 2, 3, 4, 5}` with exact distribution `(50, 90, 110, 100, 30)` and no single rational constant `alpha` maps both hinge classes to unit bond weight `1`.

2. **Subdivision Collapse of Squared Hinge Areas vs. Linear Minimal-Surface Areas**:
   - `linear_area_subdivision_invariant`, `sq_area_subdivision_scales_inv_m`, `sq_area_subdivision_defect_formula`, `sq_area_subdivision_defect_pos`, and `midpoint_and_barycentric_subdivision_witnesses` show over $\mathbb{Q}$ that subdividing a surface of linear area $A$ into $m$ equal sub-hinges preserves the linear area sum $m(A/m) = A$ while reducing the squared-area sum to $m(A/m)^2 = A^2/m$ with positive defect $((m-1)/m)A^2 > 0$ for all $m > 1$ and $A \neq 0$.

3. **Holonomy-Defect Weighting (`κ_h`) Decoupling from Topological Bond Cuts**:
   - Importing `ReggePachnerWdw` (`TFQ-0084`), `regge_wdw_flat_vs_curved_dichotomy`, `regge_action_linear_in_holonomy_defect`, `regge_curvature_variation_vs_happy_subregion_variation`, and `no_fixed_background_regge_function_matches_all_subregion_cuts` show that the `TFQ-0100` rational Regge proxy varies with bulk holonomy defect $\kappa$ (`(9/2) * kappa` on `orthogonal_pentatope`, vanishing at $\kappa = 0$), whereas `intervalMincut 2 len` varies across `{1, 2, 3, 4, 5}` (`len ∈ {1, 2, 3, 4, 8}`, with `intervalMincut 0 4 = 1`) with the boundary subregion at fixed bulk background.

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - In `lean4/CampaignAdsReggeAreaRtGap.lean` (`L4D`), the 12 theorems formalize the exact `380`-interval HaPPY `intervalMincut` distribution `(50, 90, 110, 100, 30)`, the non-existence of a uniform rational conversion factor mapping both `orthogonal_pentatope` hinge classes (`1/4` and `3/4`) to unit bond weight `1`, the $1/m$ subdivision collapse of squared hinge areas (`((m-1)/m)A^2 > 0` for $m > 1, A \neq 0$), and the decoupling between bulk holonomy defect $\kappa$ and boundary subregion minimal cuts.
   - In `checks/independent/ads-regge-area-rt-gap.py`, 463 exact rational and combinatorial checks pass with 0 failures, and 6 of 6 semantic Lean mutations are killed in `dag/research/campaign_ads-regge-area-rt-gap_lean_mutation.json`.
2. **What it does not support**:
   - A dictionary relating the repository's simplicial Regge hinge areas (`TFQ-0100`) to tensor-network bond counts or to continuum Ryu-Takayanagi minimal-surface areas.
3. **Narrowest defensible claim**:
   - On the declared simplicial Regge (`TFQ-0100`, `TFQ-0084`) and 6-pentagon HaPPY (`TFQ-2209`) carriers, squared hinge areas weighted by holonomy defects fail subdivision invariance (`m(A/m)^2 = A^2/m`), vanish on flat backgrounds (`kappa = 0`), and admit no uniform rational conversion constant mapping both `orthogonal_pentatope` hinge classes (`1/4, 3/4`) to unit HaPPY bond cuts (`1..5` distributed as `50, 90, 110, 100, 30` across the 380 intervals).
4. **Next test needed**:
   - Proceed to the next available continuum derivation in `dag/pfp/campaign/derivation_queue.json` (Rank 70: `CQFT-CAUSAL-FACTORIZATION-IMPORT`, `TFQ-2109`).
