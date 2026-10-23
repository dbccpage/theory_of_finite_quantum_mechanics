# DFM-BPHZ-CONTINUUM-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the declared overlapping edge sets L = {0,1,2}, R = {2,3,4} and G = {0,1,2,3,4}, a Zimmermann forest is a subset whose members are pairwise nested or disjoint, and the forests are exactly the six subsets in which L and R do not both occur. For the order-0 evaluations T_L I(x,y) = I(0,y), T_R I(x,y) = I(x,0) and T_G I(x,y) = I(0,0), the signed six-forest sum equals I(x,y) - I(0,y) - I(x,0) + I(0,0). For the declared numerator N(x,y) = 2 + 3x + 5y + 7xy that sum is 7xy, so the quotient by xy equals 7 wherever xy is nonzero. The three-forest sum that omits G equals 7xy - 2, and its quotient is 7 - 2/(xy). At (x,y) = (1/2, 1/3) the two quotients are 7 and -5. Algebraic cancellation for actual Feynman-parametric integrands, and any use of this identity before continuum integration, is not established.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 17
- cited Lean declarations covered by a current replay receipt: 17
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuum loop-momentum integration

## Bottleneck

The six-forest count, the order-0 collapse, and the quotient 7 are recorded only for these three edge sets and this numerator. A forest formula on actual Feynman-parametric integrands, a subtraction operator of positive degree, and a convergence statement before continuum integration remain open. The nested sector kernel at z = 3/5 gives 9/50, which is a different identity.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.3-FENCE claims COMPUTATIONALLY_CHECKED; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignDfmBphzContinuumFence.lean`

- file: [lean4/CampaignDfmBphzContinuumFence.lean](../../../lean4/CampaignDfmBphzContinuumFence.lean)
- sha256 (`bytes`): `cd03332ae8a26bce3741327cc8b3c3fe772d23f7e0b4b2dda38cdb26e5b91bcf`
- cited in: node.lean, receipt dag/research/campaign_dfm-bphz-continuum-fence_lean_replay.json (CampaignDfmBphzContinuumFence), record TFQ-1110
- replay: `verified`
  - receipt [dag/research/campaign_dfm-bphz-continuum-fence_lean_replay.json](../../../dag/research/campaign_dfm-bphz-continuum-fence_lean_replay.json) (module `CampaignDfmBphzContinuumFence`): recorded sha256 `cd03332ae8a26bce3741327cc8b3c3fe772d23f7e0b4b2dda38cdb26e5b91bcf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmBphzContinuumFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmBphzContinuumFence.compatible_LG` | yes | yes | yes | none | `#print axioms CampaignDfmBphzContinuumFence.compatible_LG` |
| `CampaignDfmBphzContinuumFence.compatible_RG` | yes | yes | yes | none | `#print axioms CampaignDfmBphzContinuumFence.compatible_RG` |
| `CampaignDfmBphzContinuumFence.nested_all_compatible` | yes | yes | yes | none | `#print axioms CampaignDfmBphzContinuumFence.nested_all_compatible` |
| `CampaignDfmBphzContinuumFence.nested_forest_count` | yes | yes | yes | none | `#print axioms CampaignDfmBphzContinuumFence.nested_forest_count` |
| `CampaignDfmBphzContinuumFence.not_compatible_LR` | yes | yes | yes | none | `#print axioms CampaignDfmBphzContinuumFence.not_compatible_LR` |
| `CampaignDfmBphzContinuumFence.numerator_is_7xy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmBphzContinuumFence.numerator_is_7xy` |
| `CampaignDfmBphzContinuumFence.omitted_graph_remainder` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmBphzContinuumFence.omitted_graph_remainder` |
| `CampaignDfmBphzContinuumFence.overlapping_excluded_iff` | yes | yes | yes | none | `#print axioms CampaignDfmBphzContinuumFence.overlapping_excluded_iff` |
| `CampaignDfmBphzContinuumFence.overlapping_forest_count` | yes | yes | yes | none | `#print axioms CampaignDfmBphzContinuumFence.overlapping_forest_count` |
| `CampaignDfmBphzContinuumFence.quotient_is_seven` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmBphzContinuumFence.quotient_is_seven` |
| `CampaignDfmBphzContinuumFence.sector_formal_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmBphzContinuumFence.sector_formal_zero` |
| `CampaignDfmBphzContinuumFence.sector_ne_seven` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmBphzContinuumFence.sector_ne_seven` |
| `CampaignDfmBphzContinuumFence.sector_value` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmBphzContinuumFence.sector_value` |
| `CampaignDfmBphzContinuumFence.share_edge_two` | yes | yes | yes | propext | `#print axioms CampaignDfmBphzContinuumFence.share_edge_two` |
| `CampaignDfmBphzContinuumFence.sixSum_eq_inclusion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmBphzContinuumFence.sixSum_eq_inclusion` |
| `CampaignDfmBphzContinuumFence.threeSum_eq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmBphzContinuumFence.threeSum_eq` |
| `CampaignDfmBphzContinuumFence.witness_half_third` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmBphzContinuumFence.witness_half_third` |
- counts toward the grade: yes

### Python: `checks/independent/dfm-bphz-continuum-fence.py`

- file: [checks/independent/dfm-bphz-continuum-fence.py](../../../checks/independent/dfm-bphz-continuum-fence.py)
- sha256 (`bytes`): `7c0c0536b49de93f95ef86ba6ce3bc5b6cb7ddf15f7146fdb2d655b00745836c`
- cited in: record TFQ-1110
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1110_dfm_bphz_continuum_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1110_dfm_bphz_continuum_fence.md](../../../dag/derivations/24_dressing_field/tfq_1110_dfm_bphz_continuum_fence.md)
- sha256 (`lf-normalised`): `21758af3c53fbc6b73c114abc61d10af4811ee7a354cef4c83f3470254687ea9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1110
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-bphz-continuum-fence.md`

- file: [dag/derivations/independent/dfm-bphz-continuum-fence.md](../../../dag/derivations/independent/dfm-bphz-continuum-fence.md)
- sha256 (`lf-normalised`): `90265f93e2d5c066615de056d04da04c6e29fa227b62a1fb7f44e7a4732bf764`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-BPHZ-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-BPHZ-SECTOR-KERNEL](DFM-BPHZ-SECTOR-KERNEL.md) (COMPUTATIONALLY_CHECKED), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (1):

- `APP-R-DFM-Z1-Z2-COUNTERTERM-FENCE` `GAP_NO_DERIVATION`: [DFM-Z1-Z2-COUNTERTERM-FENCE](DFM-Z1-Z2-COUNTERTERM-FENCE.md) (OPEN)
