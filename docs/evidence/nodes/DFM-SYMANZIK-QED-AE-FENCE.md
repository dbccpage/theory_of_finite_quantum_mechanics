# DFM-SYMANZIK-QED-AE-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The dossier claim that rational intervals built from U_G bracket the imported 1-to-4-loop QED series a_e to 12 decimal places has no check in the cited replay module.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- 1-to-4-loop QED coefficients of a_e
- fine-structure constant value

## Bottleneck

The edges and the weights are supplied. These eight subsets are one graph, not a theorem for every graph. The QED loop coefficients, the fine-structure constant, and continuum Feynman-parameter integrals stay open.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.1-FENCE claims COMPUTATIONALLY_CHECKED; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignDfmSymanzikQedAeFence.lean`

- file: [lean4/CampaignDfmSymanzikQedAeFence.lean](../../../lean4/CampaignDfmSymanzikQedAeFence.lean)
- sha256 (`bytes`): `d86b09de161d6e3b06396266d1b34e2e0d40192273d5ee97366bba4e680e03ab`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-symanzik-qed-ae-fence_lean_replay.json (CampaignDfmSymanzikQedAeFence), record TFQ-1104
- replay: `verified`
  - receipt [dag/research/campaign_dfm-symanzik-qed-ae-fence_lean_replay.json](../../../dag/research/campaign_dfm-symanzik-qed-ae-fence_lean_replay.json) (module `CampaignDfmSymanzikQedAeFence`): recorded sha256 `d86b09de161d6e3b06396266d1b34e2e0d40192273d5ee97366bba4e680e03ab` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmSymanzikQedAeFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmSymanzikQedAeFence.component_counts` | yes | yes | yes | propext | `#print axioms CampaignDfmSymanzikQedAeFence.component_counts` |
| `CampaignDfmSymanzikQedAeFence.cotree_sums` | yes | yes | yes | propext | `#print axioms CampaignDfmSymanzikQedAeFence.cotree_sums` |
| `CampaignDfmSymanzikQedAeFence.three_bit_masks_are_listed` | yes | yes | yes | propext | `#print axioms CampaignDfmSymanzikQedAeFence.three_bit_masks_are_listed` |
| `component_counts` | yes | yes | yes | propext | `#print axioms component_counts` |
| `cotree_sums` | yes | yes | yes | propext | `#print axioms cotree_sums` |
| `three_bit_masks_are_listed` | yes | yes | yes | propext | `#print axioms three_bit_masks_are_listed` |

- counts toward the grade: yes

### Python: `checks/independent/dfm-symanzik-qed-ae-fence.py`

- file: [checks/independent/dfm-symanzik-qed-ae-fence.py](../../../checks/independent/dfm-symanzik-qed-ae-fence.py)
- sha256 (`bytes`): `ebca2357cd211ca946f3b9f04eaca64e955407d5270576af34242cd1c4803d15`
- cited in: node.source, record TFQ-1104
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1104_dfm_symanzik_qed_ae_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1104_dfm_symanzik_qed_ae_fence.md](../../../dag/derivations/24_dressing_field/tfq_1104_dfm_symanzik_qed_ae_fence.md)
- sha256 (`lf-normalised`): `008175f49e76b5053b2d3467e0c43a028601b227c35d9a14a42451f0f76a862b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1104
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-symanzik-qed-ae-fence.md`

- file: [dag/derivations/independent/dfm-symanzik-qed-ae-fence.md](../../../dag/derivations/independent/dfm-symanzik-qed-ae-fence.md)
- sha256 (`lf-normalised`): `2727b639719b9f8d44baaddaee909cb9927cacf3b2ad4749e1fc4f7516fdddf7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-SYMANZIK-QED-AE-FENCE` `GAP_NO_DERIVATION`: [DFM-TREE-CHANGE-GLZ-SYMANZIK-U](DFM-TREE-CHANGE-GLZ-SYMANZIK-U.md) (COMPUTATIONALLY_CHECKED), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (0):

