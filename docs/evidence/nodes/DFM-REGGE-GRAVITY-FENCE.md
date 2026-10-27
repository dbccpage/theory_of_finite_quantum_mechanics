# DFM-REGGE-GRAVITY-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A 4D Regge complex with dressed hinge holonomies from edge lengths, a Spin+(1,3; Q(i)) spin-frame dressing of simplex spinors preserving a discrete Dirac action (the dossier's next test), and any continuum gravity reading are not constructed.

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

### Lean: `lean4/DressingFieldReggeGravityFence.lean`

- file: [lean4/DressingFieldReggeGravityFence.lean](../../../lean4/DressingFieldReggeGravityFence.lean)
- sha256 (`bytes`): `09c0b7b66c1a4b90a66f96dc648c22a64ce5519a7a1f1401a217e0f05b6a6d80`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-regge-gravity-fence_final_lean_replay.json (DressingFieldReggeGravityFence), receipt dag/research/campaign_dfm-regge-gravity-fence_integrated_lean_replay.json (DressingFieldReggeGravityFence), receipt dag/research/campaign_dfm-regge-gravity-fence_lean_replay.json (DressingFieldReggeGravityFence), receipt dag/research/campaign_dfm-regge-gravity-fence_review_lean_replay.json (DressingFieldReggeGravityFence), record TFQ-1137
- replay: `verified`
  - receipt [dag/research/campaign_dfm-regge-gravity-fence_final_lean_replay.json](../../../dag/research/campaign_dfm-regge-gravity-fence_final_lean_replay.json) (module `DressingFieldReggeGravityFence`): recorded sha256 `09c0b7b66c1a4b90a66f96dc648c22a64ce5519a7a1f1401a217e0f05b6a6d80` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/campaign_dfm-regge-gravity-fence_integrated_lean_replay.json](../../../dag/research/campaign_dfm-regge-gravity-fence_integrated_lean_replay.json) (module `DressingFieldReggeGravityFence`): recorded sha256 `09c0b7b66c1a4b90a66f96dc648c22a64ce5519a7a1f1401a217e0f05b6a6d80` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/campaign_dfm-regge-gravity-fence_lean_replay.json](../../../dag/research/campaign_dfm-regge-gravity-fence_lean_replay.json) (module `DressingFieldReggeGravityFence`): recorded sha256 `09c0b7b66c1a4b90a66f96dc648c22a64ce5519a7a1f1401a217e0f05b6a6d80` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/campaign_dfm-regge-gravity-fence_review_lean_replay.json](../../../dag/research/campaign_dfm-regge-gravity-fence_review_lean_replay.json) (module `DressingFieldReggeGravityFence`): recorded sha256 `09c0b7b66c1a4b90a66f96dc648c22a64ce5519a7a1f1401a217e0f05b6a6d80` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DressingFieldReggeGravityFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DressingFieldReggeGravityFence.block_trace_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldReggeGravityFence.block_trace_half` |
| `DressingFieldReggeGravityFence.cosine_sum_ne_block_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldReggeGravityFence.cosine_sum_ne_block_trace` |
| `DressingFieldReggeGravityFence.lengths_345` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldReggeGravityFence.lengths_345` |
| `DressingFieldReggeGravityFence.numerator_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldReggeGravityFence.numerator_sum` |
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
- sha256 (`lf-normalised`): `e655375dc1c4539fc46a86814fc4d030f7ea570710990dbb58aac29ccaf356de`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1137
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-regge-gravity-fence.md`

- file: [dag/derivations/independent/dfm-regge-gravity-fence.md](../../../dag/derivations/independent/dfm-regge-gravity-fence.md)
- sha256 (`lf-normalised`): `4ad0746da428eedae956e80e65fbea990fdb3d9c965436c1770a36ee7e0fe723`
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

