# Independent Derivation Note: `ADS-REGGE-AREA-RT-GAP` (`TFQ-2211`)

**AuthorityEffect:** None.
**Node:** `ADS-REGGE-AREA-RT-GAP` (`TFQ-2211`, stage `ADS_CFT`, status `OPEN`)
**Outcome Class:** Narrowed (`OPEN` status preserved; narrowed to three exact finite/rational non-equivalence fences between the repository's `TFQ-0100` rational Regge squared-area proxy, continuum minimal-surface area, and discrete 6-pentagon HaPPY `{5,4}` bond-cut counts in [CampaignAdsReggeAreaRtGap.lean](../../../lean4/CampaignAdsReggeAreaRtGap.lean) and [ads-regge-area-rt-gap.py](../../../checks/independent/ads-regge-area-rt-gap.py)).

---

## 1. Statement & Scope Boundary

`ADS-REGGE-AREA-RT-GAP` (`TFQ-2211`) asks whether the exact rational Regge proxy of `TFQ-0100` ([action.rs](../../../code/rust/src/general_relativity/exact_regge/action.rs), [sphere.rs](../../../code/rust/src/general_relativity/exact_regge/sphere.rs))—which sums Cayley-Menger squared hinge areas $A_h^2 \in \mathbb{Q}$ weighted by rational holonomy defects $\kappa_h \in \mathbb{Q}$—can supply the area term of a finite Ryu-Takayanagi minimal-surface statement, or match the discrete bond-cut count (one bit per bond) of the 6-pentagon HaPPY `{5,4}` patch ([FrontierHappyMincut.lean](../../../lean4/FrontierHappyMincut.lean), `TFQ-2209`).

No source supplies a dictionary between the two carriers. We narrow `ADS-REGGE-AREA-RT-GAP` by proving three exact non-equivalence fences in Lean 4 and cross-checking them in Python.

---

## 2. Three Formalized Non-Equivalence Fences

### 2.1 Simplicial Hinge Carrier vs. HaPPY Tensor-Network Cut Spectrum Census

1. **Simplicial vs. Tensor-Network Carrier Counts**:
   In `TFQ-0100` ([sphere.rs](../../../code/rust/src/general_relativity/exact_regge/sphere.rs)), the `orthogonal_pentatope` 4-simplex $\Delta^4$ has $5$ vertices, $10$ edges, $10$ triangular hinges ($6$ right triangles with $A_h^2 = 1/4$ and $4$ equilateral triangles with $A_h^2 = 3/4$), and $5$ tetrahedral facets ($5 + 10 = 10 + 5$), while `closed_s4_cube_boundary` has $10 \times 4! = 240$ pentatope charts ([`simplicial_regge_vs_happy_network_carrier_counts`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L90-L96)).
2. **Exact `intervalMincut` Value Distribution on the 6-Pentagon HaPPY Patch**:
   On the 20-qubit 6-pentagon HaPPY `{5,4}` star network (`6` tensors, `5` internal bulk bonds, `20` boundary legs), across all `380` proper nonempty contiguous boundary intervals $(s, \ell)$, the minimal bond cut `intervalMincut s l` takes only integer values in $\{1, 2, 3, 4, 5\}$ with exact multiplicities
   $$(N_1, N_2, N_3, N_4, N_5) = (50, 90, 110, 100, 30), \qquad \sum_{k=1}^5 N_k = 380$$
   ([`happy_mincut_value_distribution_380`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L109-L120)).
3. **No Single Hinge-to-Bond Unit Dictionary**:
   No single rational conversion factor $\alpha \in \mathbb{Q}$ can map both squared-area classes ($1/4$ and $3/4$) of `orthogonal_pentatope` to the HaPPY unit bond weight $1$; normalizing $\alpha \cdot (1/4) = 1$ forces $\alpha = 4$, mapping each equilateral hinge to $3$ and the 10-hinge pentatope sum to $18$ ([`no_uniform_hinge_to_bond_unit_dictionary`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L133-L144)).

### 2.2 Subdivision Collapse of Squared Hinge Areas vs. Subdivision Invariance of Linear Areas

When a planar surface element of linear area $A$ is subdivided into $m$ congruent sub-hinges of linear area $A/m$ each:
- The **linear area sum** is invariant under subdivision for every $m \neq 0$:
  $$\mathrm{linearAreaSubdivisionSum}(A, m) = m \cdot \frac{A}{m} = A$$
  ([`linear_area_subdivision_invariant`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L167-L170)).
- The **squared-area sum** drops by $1/m$:
  $$\mathrm{sqAreaSubdivisionSum}(A, m) = m \cdot \left(\frac{A}{m}\right)^2 = \frac{A^2}{m}$$
  ([`sq_area_subdivision_scales_inv_m`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L174-L177)).
- The **subdivision defect** satisfies
  $$\mathrm{sqAreaSubdivisionDefect}(A, m) = A^2 - m\left(\frac{A}{m}\right)^2 = \frac{m - 1}{m} A^2 > 0 \quad (\forall m > 1, A \neq 0)$$
  ([`sq_area_subdivision_defect_formula`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L180-L183), [`sq_area_subdivision_defect_pos`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L188-L199), and [`midpoint_and_barycentric_subdivision_witnesses`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L205-L214)). Thus unregularized squared hinge areas collapse toward $0$ under triangulation refinement instead of defining a refinement-stable minimal-surface area.

### 2.3 Holonomy-Defect Weighting (`κ_h`) Decoupling from Topological Bond Cuts

Importing [`ReggePachnerWdw`](../../../lean4/ReggePachnerWdw.lean) (`TFQ-0084`):
- A flat simplicial vertex ($d = 0$ on all incident bones) has `evaluateH_Wdw v = 0`, whereas any positive bone defect $d > 0$ yields `evaluateH_Wdw v > 0` ([`regge_wdw_flat_vs_curved_dichotomy`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L228-L235)).
- On the fixed `orthogonal_pentatope` geometry ($\sum_h A_h^2 = 9/2$), varying the uniform holonomy defect $\kappa$ scales the Regge proxy $\frac{9}{2}\kappa$ linearly in $\kappa$ without altering the combinatorial complex ([`regge_action_linear_in_holonomy_defect`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L241-L255)), whereas on the fixed 6-pentagon HaPPY network `intervalMincut 2 len` varies across $(1, 2, 3, 4, 5)$ at $\mathrm{len} \in \{1, 2, 3, 4, 8\}$ (and `intervalMincut 0 4 = 1`) purely as a function of the boundary subregion while the flat-background Regge proxy ($\kappa = 0$) remains $0$ ([`regge_curvature_variation_vs_happy_subregion_variation`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L262-L270) and [`no_fixed_background_regge_function_matches_all_subregion_cuts`](../../../lean4/CampaignAdsReggeAreaRtGap.lean#L276-L283)).
