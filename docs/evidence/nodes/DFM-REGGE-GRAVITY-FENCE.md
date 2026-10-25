# DFM-REGGE-GRAVITY-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every rational a, b, c, the cosine-law numerators b^2+c^2-a^2, a^2+c^2-b^2 and a^2+b^2-c^2 sum to a^2+b^2+c^2. At lengths 3, 4 and 5 the numerators opposite sides 5, 3 and 4 respectively are 0, 32 and 18, the cosine-law values are 0, 4/5 and 3/5, and those values sum to 7/5. At beta = 1/2 the denominator 1-beta^2 is nonzero, (1+beta^2)/(1-beta^2) = 5/3, 2 beta/(1-beta^2) = 4/3, and the block trace 2(1+beta^2)/(1-beta^2)+2 equals 16/3, which differs from 4 and from 7/5. A 4D Regge complex, a deficit angle, a Spin+ spin-frame dressing, and a continuum gravity reading stay unproved.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Regge calculus to general relativity limit

## Bottleneck

The lengths 3, 4, 5 and beta = 1/2 are supplied data. The block trace is not computed from those lengths. A 4D complex, a deficit angle, a spin-frame dressing, and a continuum reading stay open.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.9-FENCE claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignDfmReggeGravityFence.lean`

- file: [lean4/CampaignDfmReggeGravityFence.lean](../../../lean4/CampaignDfmReggeGravityFence.lean)
- sha256 (`bytes`): `dddcb90d0c502c292a4b7dc9d7f6c5aa9a96c5d550c0f4c2c056b9c8e22d61c6`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-regge-gravity-fence_final_lean_replay.json (CampaignDfmReggeGravityFence), receipt dag/research/campaign_dfm-regge-gravity-fence_integrated_lean_replay.json (CampaignDfmReggeGravityFence), receipt dag/research/campaign_dfm-regge-gravity-fence_lean_replay.json (CampaignDfmReggeGravityFence), receipt dag/research/campaign_dfm-regge-gravity-fence_review_lean_replay.json (CampaignDfmReggeGravityFence), record TFQ-1137
- replay: `verified`
  - receipt [dag/research/campaign_dfm-regge-gravity-fence_final_lean_replay.json](../../../dag/research/campaign_dfm-regge-gravity-fence_final_lean_replay.json) (module `CampaignDfmReggeGravityFence`): recorded sha256 `dddcb90d0c502c292a4b7dc9d7f6c5aa9a96c5d550c0f4c2c056b9c8e22d61c6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/campaign_dfm-regge-gravity-fence_integrated_lean_replay.json](../../../dag/research/campaign_dfm-regge-gravity-fence_integrated_lean_replay.json) (module `CampaignDfmReggeGravityFence`): recorded sha256 `dddcb90d0c502c292a4b7dc9d7f6c5aa9a96c5d550c0f4c2c056b9c8e22d61c6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/campaign_dfm-regge-gravity-fence_lean_replay.json](../../../dag/research/campaign_dfm-regge-gravity-fence_lean_replay.json) (module `CampaignDfmReggeGravityFence`): recorded sha256 `dddcb90d0c502c292a4b7dc9d7f6c5aa9a96c5d550c0f4c2c056b9c8e22d61c6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/campaign_dfm-regge-gravity-fence_review_lean_replay.json](../../../dag/research/campaign_dfm-regge-gravity-fence_review_lean_replay.json) (module `CampaignDfmReggeGravityFence`): recorded sha256 `dddcb90d0c502c292a4b7dc9d7f6c5aa9a96c5d550c0f4c2c056b9c8e22d61c6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmReggeGravityFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmReggeGravityFence.block_trace_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmReggeGravityFence.block_trace_half` |
| `CampaignDfmReggeGravityFence.cosine_sum_ne_block_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmReggeGravityFence.cosine_sum_ne_block_trace` |
| `CampaignDfmReggeGravityFence.lengths_345` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmReggeGravityFence.lengths_345` |
| `CampaignDfmReggeGravityFence.numerator_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmReggeGravityFence.numerator_sum` |
| `block_trace_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms block_trace_half` |
| `cosine_sum_ne_block_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms cosine_sum_ne_block_trace` |
| `lengths_345` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms lengths_345` |
| `numerator_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms numerator_sum` |

- counts toward the grade: yes

### Python: `checks/independent/dfm-regge-gravity-fence.py`

- file: [checks/independent/dfm-regge-gravity-fence.py](../../../checks/independent/dfm-regge-gravity-fence.py)
- sha256 (`bytes`): `5e7a24f60d75815123cef5888460f87c8ec93584c34584d39d0e5d8dcdb0ffa7`
- cited in: node.source, record TFQ-1137
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1137_dfm_regge_gravity_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1137_dfm_regge_gravity_fence.md](../../../dag/derivations/24_dressing_field/tfq_1137_dfm_regge_gravity_fence.md)
- sha256 (`lf-normalised`): `b68a08417546ad04bf9d172c1c7a7ea88353b911eadf99baf555f06bac36a785`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1137
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-regge-gravity-fence.md`

- file: [dag/derivations/independent/dfm-regge-gravity-fence.md](../../../dag/derivations/independent/dfm-regge-gravity-fence.md)
- sha256 (`lf-normalised`): `83f18b3698451d20067f41c0b3751785ed33051d9c3de9c9518367a5fa1798ec`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-REGGE-GRAVITY-FENCE` `GAP_NO_DERIVATION`: [DFM-HINGE-HOLONOMY-WITNESS](DFM-HINGE-HOLONOMY-WITNESS.md) (COMPUTATIONALLY_CHECKED), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (0):

