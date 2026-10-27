# ADS-REGGE-AREA-RT-GAP

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Open question: whether the exact rational Regge proxy of TFQ-0100 (squared hinge areas weighted by a holonomy defect, which is not the Einstein-Hilbert action) can supply the area term of a finite minimal-surface statement. The imported formula uses the area of a minimal surface in a bulk geometry; the HaPPY patch measures a bond count (one bit per bond). Matching the two needs a dictionary from geometry to network that no source supplies.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No source relates the Regge hinge areas of the repository to bond counts of a tensor network. Checked slice, status unchanged. Narrowed in Lean 4 and an independent Python verifier to three exact non-equivalence fences: (1) on the 20-qubit 6-pentagon HaPPY {5,4} patch (6 tensors, 5 internal bonds, 20 boundary legs), across all 380 proper nonempty contiguous boundary intervals the minimal bond cut intervalMincut takes values {1, 2, 3, 4, 5} with exact multiplicities (50, 90, 110, 100, 30), whereas the 4D orthogonal_pentatope simplex of TFQ-0100 has 6 right-triangle hinges of squared area 1/4 and 4 equilateral-triangle hinges of squared area 3/4 (240 Kuhn pentatopes on closed_s4_cube_boundary) and no single rational constant alpha maps both hinge classes to unit bond weight 1; (2) subdividing a planar surface of linear area A into m equal sub-hinges preserves the linear area sum m * (A / m) = A for all m != 0 but reduces the squared-area sum to m * (A / m)^2 = A^2 / m with strictly positive defect ((m - 1) / m) * A^2 \> 0 for all m \> 1 and A != 0; and (3) the TFQ-0100 rational Regge proxy scales linearly with bulk holonomy defect kappa ((9/2) * kappa on orthogonal_pentatope, vanishing at kappa = 0 as in ReggePachnerWdw flat_vertex_wdw_closure), whereas intervalMincut 2 len varies across (1, 2, 3, 4, 5) at len in {1, 2, 3, 4, 8} (with intervalMincut 0 4 = 1) as a function of the boundary subregion on a fixed background.

## Source status

Explicit gap node; audited against TFQ-0100 and arXiv:hep-th/0603001 eq. (1.5) on 2026-10-22; narrowed to exact carrier/mincut census, squared-area subdivision collapse, and holonomy-defect decoupling fences in Lean 4 and an independent Python verifier on 2026-10-24.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AdsReggeAreaRtGap.lean`

- file: [lean4/AdsReggeAreaRtGap.lean](../../../lean4/AdsReggeAreaRtGap.lean)
- sha256 (`bytes`): `378777ffedad3a7fa58ad034b1ee51c55cb0551bb1b3bdde5de9b684328dd4d3`
- cited in: node.lean, node.source, receipt dag/research/campaign_ads-regge-area-rt-gap_lean_replay.json (AdsReggeAreaRtGap), record TFQ-2211
- replay: `verified`
  - receipt [dag/research/campaign_ads-regge-area-rt-gap_lean_replay.json](../../../dag/research/campaign_ads-regge-area-rt-gap_lean_replay.json) (module `AdsReggeAreaRtGap`): recorded sha256 `378777ffedad3a7fa58ad034b1ee51c55cb0551bb1b3bdde5de9b684328dd4d3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build AdsReggeAreaRtGap`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AdsReggeAreaRtGap.happy_mincut_value_distribution_380` | yes | yes | yes | propext | `#print axioms AdsReggeAreaRtGap.happy_mincut_value_distribution_380` |
| `AdsReggeAreaRtGap.linear_area_subdivision_invariant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsReggeAreaRtGap.linear_area_subdivision_invariant` |
| `AdsReggeAreaRtGap.midpoint_and_barycentric_subdivision_witnesses` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsReggeAreaRtGap.midpoint_and_barycentric_subdivision_witnesses` |
| `AdsReggeAreaRtGap.no_fixed_background_regge_function_matches_all_subregion_cuts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsReggeAreaRtGap.no_fixed_background_regge_function_matches_all_subregion_cuts` |
| `AdsReggeAreaRtGap.no_uniform_hinge_to_bond_unit_dictionary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsReggeAreaRtGap.no_uniform_hinge_to_bond_unit_dictionary` |
| `AdsReggeAreaRtGap.regge_action_linear_in_holonomy_defect` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsReggeAreaRtGap.regge_action_linear_in_holonomy_defect` |
| `AdsReggeAreaRtGap.regge_curvature_variation_vs_happy_subregion_variation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsReggeAreaRtGap.regge_curvature_variation_vs_happy_subregion_variation` |
| `AdsReggeAreaRtGap.regge_wdw_flat_vs_curved_dichotomy` | yes | yes | yes | Quot.sound, propext | `#print axioms AdsReggeAreaRtGap.regge_wdw_flat_vs_curved_dichotomy` |
| `AdsReggeAreaRtGap.simplicial_regge_vs_happy_network_carrier_counts` | yes | yes | yes | none | `#print axioms AdsReggeAreaRtGap.simplicial_regge_vs_happy_network_carrier_counts` |
| `AdsReggeAreaRtGap.sq_area_subdivision_defect_formula` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsReggeAreaRtGap.sq_area_subdivision_defect_formula` |
| `AdsReggeAreaRtGap.sq_area_subdivision_defect_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsReggeAreaRtGap.sq_area_subdivision_defect_pos` |
| `AdsReggeAreaRtGap.sq_area_subdivision_scales_inv_m` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsReggeAreaRtGap.sq_area_subdivision_scales_inv_m` |

- counts toward the grade: yes

### Python: `checks/independent/ads-regge-area-rt-gap.py`

- file: [checks/independent/ads-regge-area-rt-gap.py](../../../checks/independent/ads-regge-area-rt-gap.py)
- sha256 (`bytes`): `30504d898a8d40d9825d3c6cd38bd99248db18ef9f4b29e970e11a725d93e5b1`
- cited in: node.source, record TFQ-2211
- counts toward the grade: yes

### Documents and data: `dag/derivations/32_ads_cft/tfq_2211_ads_regge_area_rt_gap.md`

- file: [dag/derivations/32_ads_cft/tfq_2211_ads_regge_area_rt_gap.md](../../../dag/derivations/32_ads_cft/tfq_2211_ads_regge_area_rt_gap.md)
- sha256 (`lf-normalised`): `f108042097aa9a33821b75d8ca5030c4521db07b25360483d50b8774497fe0d7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2211
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ads-regge-area-rt-gap.md`

- file: [dag/derivations/independent/ads-regge-area-rt-gap.md](../../../dag/derivations/independent/ads-regge-area-rt-gap.md)
- sha256 (`lf-normalised`): `19ceff37b4bf875a65213b9f9bb56beab86a588d3d2d7ee3529dfc65bab33b64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-regge-area-rt-gap_independent.json`

- file: [dag/research/campaign_ads-regge-area-rt-gap_independent.json](../../../dag/research/campaign_ads-regge-area-rt-gap_independent.json)
- sha256 (`lf-normalised`): `2ffced2b6c8e425d0ec37f9e8a7a349b76dcc6363ba1d191e308e90946c05d32`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-regge-area-rt-gap_lean_mutation.json`

- file: [dag/research/campaign_ads-regge-area-rt-gap_lean_mutation.json](../../../dag/research/campaign_ads-regge-area-rt-gap_lean_mutation.json)
- sha256 (`lf-normalised`): `8b998339effbc691c15d89a8dfde9555afc133b1a542f7313d6c16f822e15cd9`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-regge-area-rt-gap_lean_replay.json`

- file: [dag/research/campaign_ads-regge-area-rt-gap_lean_replay.json](../../../dag/research/campaign_ads-regge-area-rt-gap_lean_replay.json)
- sha256 (`lf-normalised`): `d74751c4a97a5902295650d700eaa072a4209695db1284955fceace6d41af3ab`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-ADS-REGGE-AREA-RT-GAP` `GAP_NO_DERIVATION`: [ADS-RT-FORMULA-IMPORT](ADS-RT-FORMULA-IMPORT.md) (IMPORTED_ASSUMPTION), [TFQ-0100](TFQ-0100.md) (SOURCE_RECORD)

Outgoing (0):

