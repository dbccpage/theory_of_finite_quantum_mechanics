# DFM-CKM-PHYSICS-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Derivation of V from dressed Yukawa couplings, the unitarity-triangle reduction to (N_g - 1)(N_g - 2)/2 CP phases, and any statement about measured CP violation are not established.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 24
- distinct cited Lean declarations covered by a current replay receipt: 19
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Yukawa couplings and mass-basis diagonalization
- measured CKM parameters

## Bottleneck

Yukawa couplings, mass-basis diagonalization, a unitarity identification of the counting polynomials, and measured CKM values stay open. The general nonzero-label table classification uses supplied commutative-group rescalings; its restriction to physical unitary mixing matrices is not established.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.7-FENCE claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DressingFieldCkmPhysicsFence.lean`

- file: [lean4/DressingFieldCkmPhysicsFence.lean](../../../lean4/DressingFieldCkmPhysicsFence.lean)
- sha256 (`bytes`): `8366d62e75f6c93527df44a35fa92ae53754237c9a7602f205b5279360f9acdf`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-ckm-physics-fence_lean_replay.json (DressingFieldCkmPhysicsFence), record TFQ-1128
- replay: `verified`
  - receipt [dag/research/campaign_dfm-ckm-physics-fence_lean_replay.json](../../../dag/research/campaign_dfm-ckm-physics-fence_lean_replay.json) (module `DressingFieldCkmPhysicsFence`): recorded sha256 `8366d62e75f6c93527df44a35fa92ae53754237c9a7602f205b5279360f9acdf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DressingFieldCkmPhysicsFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DressingFieldCkmPhysicsFence.Rephasing.act_compose` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.act_compose` |
| `DressingFieldCkmPhysicsFence.Rephasing.act_inverse` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.act_inverse` |
| `DressingFieldCkmPhysicsFence.Rephasing.checkedLabel_none_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.checkedLabel_none_iff` |
| `DressingFieldCkmPhysicsFence.Rephasing.checkedLabel_value` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.checkedLabel_value` |
| `DressingFieldCkmPhysicsFence.Rephasing.coordinatesEquiv` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.coordinatesEquiv` |
| `DressingFieldCkmPhysicsFence.Rephasing.decideRelated_correct` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.decideRelated_correct` |
| `DressingFieldCkmPhysicsFence.Rephasing.free_coordinate_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.free_coordinate_count` |
| `DressingFieldCkmPhysicsFence.Rephasing.normalize_boundary` | yes | yes | yes | propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.normalize_boundary` |
| `DressingFieldCkmPhysicsFence.Rephasing.normalize_idempotent` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.normalize_idempotent` |
| `DressingFieldCkmPhysicsFence.Rephasing.normalize_invariant` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.normalize_invariant` |
| `DressingFieldCkmPhysicsFence.Rephasing.related_iff_normalize` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.Rephasing.related_iff_normalize` |
| `DressingFieldCkmPhysicsFence.constraintCount_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.constraintCount_sum` |
| `DressingFieldCkmPhysicsFence.count_misses_one_quartet` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.count_misses_one_quartet` |
| `DressingFieldCkmPhysicsFence.count_table` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.count_table` |
| `DressingFieldCkmPhysicsFence.cpCount_from_difference` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.cpCount_from_difference` |
| `DressingFieldCkmPhysicsFence.quartet_imag_value` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.quartet_imag_value` |
| `DressingFieldCkmPhysicsFence.quartet_real_value` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.quartet_real_value` |
| `DressingFieldCkmPhysicsFence.quartets_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.quartets_differ` |
| `DressingFieldCkmPhysicsFence.three_generation_split` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldCkmPhysicsFence.three_generation_split` |
| `constraintCount_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms constraintCount_sum` |
| `count_misses_one_quartet` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms count_misses_one_quartet` |
| `count_table` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms count_table` |
| `cpCount_from_difference` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms cpCount_from_difference` |
| `three_generation_split` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms three_generation_split` |

- counts toward the grade: yes

### Python: `checks/independent/dfm-ckm-physics-fence.py`

- file: [checks/independent/dfm-ckm-physics-fence.py](../../../checks/independent/dfm-ckm-physics-fence.py)
- sha256 (`bytes`): `c892785ddff595611d83acaade1166e5d755e00a42d84104d60fdad3b793c48b`
- cited in: node.source, record TFQ-1128
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1128_dfm_ckm_physics_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1128_dfm_ckm_physics_fence.md](../../../dag/derivations/24_dressing_field/tfq_1128_dfm_ckm_physics_fence.md)
- sha256 (`lf-normalised`): `f8ae32b6e385b2d4e241afa3928ad5c0ac16ddd21578b33a6ff1855303c4bfb5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1128
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-ckm-physics-fence.md`

- file: [dag/derivations/independent/dfm-ckm-physics-fence.md](../../../dag/derivations/independent/dfm-ckm-physics-fence.md)
- sha256 (`lf-normalised`): `927aefc8724d93d13ed00782056ecff6219edb2c153138d0be1cfe0de513e0d4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-CKM-PHYSICS-FENCE` `GAP_NO_DERIVATION`: [DFM-JARLSKOG-PYTHAGOREAN-WITNESS](DFM-JARLSKOG-PYTHAGOREAN-WITNESS.md) (COMPUTATIONALLY_CHECKED), [DFM-ELECTROWEAK-CONTINUUM-FENCE](DFM-ELECTROWEAK-CONTINUUM-FENCE.md) (OPEN)

Outgoing (0):

