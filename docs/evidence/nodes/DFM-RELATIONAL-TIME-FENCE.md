# DFM-RELATIONAL-TIME-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For U = \[\[0, -1\], \[1, 0\]\] over Q, U^2 = -I, U^4 = I, and U^T U = I. For each t in {0, 1, 2, 3}, (U^{t+1})^T U U^t = I. For psi = (3/5, 4/5), psi·psi = 1 and (U^t)^T (U^t psi) = psi for each such t, while the first components of U psi and of U^2 psi differ from 3/5. A continuous-time reading, a Stone generator, and a Wheeler-DeWitt constraint stay unproved.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuous time and Stone generator
- Hamiltonian constraint of a physical theory

## Bottleneck

The step and the vector are supplied. These four blocks are one witness, not a theorem for every period. Continuous time, a one-parameter unitary group, and a Hamiltonian constraint stay open.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.5-FENCE claims COMPUTATIONALLY_CHECKED; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignDfmRelationalTimeFence.lean`

- file: [lean4/CampaignDfmRelationalTimeFence.lean](../../../lean4/CampaignDfmRelationalTimeFence.lean)
- sha256 (`bytes`): `82780812950910f0bbab83dbc5911fc268437b842392833b1f8a85859764a91c`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-relational-time-fence_lean_replay.json (CampaignDfmRelationalTimeFence), record TFQ-1117
- replay: `verified`
  - receipt [dag/research/campaign_dfm-relational-time-fence_lean_replay.json](../../../dag/research/campaign_dfm-relational-time-fence_lean_replay.json) (module `CampaignDfmRelationalTimeFence`): recorded sha256 `82780812950910f0bbab83dbc5911fc268437b842392833b1f8a85859764a91c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmRelationalTimeFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmRelationalTimeFence.four_blocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.four_blocks` |
| `CampaignDfmRelationalTimeFence.psi_recover` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.psi_recover` |
| `CampaignDfmRelationalTimeFence.step_square_and_order` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRelationalTimeFence.step_square_and_order` |
| `four_blocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms four_blocks` |
| `psi_recover` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms psi_recover` |
| `step_square_and_order` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms step_square_and_order` |
- counts toward the grade: yes

### Python: `checks/independent/dfm-relational-time-fence.py`

- file: [checks/independent/dfm-relational-time-fence.py](../../../checks/independent/dfm-relational-time-fence.py)
- sha256 (`bytes`): `e4ea74d2cff9e54b01093dc20055ae8091ac2fb74bb0062ca756f792ff8f2ad6`
- cited in: node.source, record TFQ-1117
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1117_dfm_relational_time_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1117_dfm_relational_time_fence.md](../../../dag/derivations/24_dressing_field/tfq_1117_dfm_relational_time_fence.md)
- sha256 (`lf-normalised`): `9fbaaa047d688022d5a67dd9e3fcba33164a1a246fd9f794d44973b3b3e67bec`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1117
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-relational-time-fence.md`

- file: [dag/derivations/independent/dfm-relational-time-fence.md](../../../dag/derivations/independent/dfm-relational-time-fence.md)
- sha256 (`lf-normalised`): `a5383b3b5b37ea73920cce7e486696e17b061c38789c7a0ab7f50dff082ebc7e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-RELATIONAL-TIME-FENCE` `GAP_NO_DERIVATION`: [DFM-CLOCK-DRESSING-INTERTWINER](DFM-CLOCK-DRESSING-INTERTWINER.md) (PROVED_PROSE), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (0):

