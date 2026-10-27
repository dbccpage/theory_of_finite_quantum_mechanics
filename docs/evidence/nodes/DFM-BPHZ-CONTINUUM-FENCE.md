# DFM-BPHZ-CONTINUUM-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Algebraic cancellation of nested and overlapping UV boundary poles for actual Feynman-parametric integrands, and its use before continuum integration, is not established by the finite artifacts.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 28
- distinct cited Lean declarations covered by a current replay receipt: 28
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

### Lean: `lean4/DressingFieldBphzContinuumFence.lean`

- file: [lean4/DressingFieldBphzContinuumFence.lean](../../../lean4/DressingFieldBphzContinuumFence.lean)
- sha256 (`bytes`): `878e25acc8ba9a63eec10dd9d436f8cb5b578fde0e0faca4e6d736b681a0fcaf`
- cited in: node.lean, receipt dag/research/campaign_dfm-bphz-continuum-fence_lean_replay.json (DressingFieldBphzContinuumFence), record TFQ-1110
- replay: `verified`
  - receipt [dag/research/campaign_dfm-bphz-continuum-fence_lean_replay.json](../../../dag/research/campaign_dfm-bphz-continuum-fence_lean_replay.json) (module `DressingFieldBphzContinuumFence`): recorded sha256 `878e25acc8ba9a63eec10dd9d436f8cb5b578fde0e0faca4e6d736b681a0fcaf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DressingFieldBphzContinuumFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DressingFieldBphzContinuumFence.Subtraction.Projector.kills_remainder` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.Subtraction.Projector.kills_remainder` |
| `DressingFieldBphzContinuumFence.Subtraction.kernelProjector` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.Subtraction.kernelProjector` |
| `DressingFieldBphzContinuumFence.Subtraction.map_remainder` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.Subtraction.map_remainder` |
| `DressingFieldBphzContinuumFence.Subtraction.reduce_absorbs` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.Subtraction.reduce_absorbs` |
| `DressingFieldBphzContinuumFence.Subtraction.reduce_append` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.Subtraction.reduce_append` |
| `DressingFieldBphzContinuumFence.Subtraction.reduce_fixed` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.Subtraction.reduce_fixed` |
| `DressingFieldBphzContinuumFence.Subtraction.reduce_fixed_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.Subtraction.reduce_fixed_iff` |
| `DressingFieldBphzContinuumFence.Subtraction.reduce_idempotent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.Subtraction.reduce_idempotent` |
| `DressingFieldBphzContinuumFence.Subtraction.reduce_killed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.Subtraction.reduce_killed` |
| `DressingFieldBphzContinuumFence.compatible_LG` | yes | yes | yes | none | `#print axioms DressingFieldBphzContinuumFence.compatible_LG` |
| `DressingFieldBphzContinuumFence.compatible_RG` | yes | yes | yes | none | `#print axioms DressingFieldBphzContinuumFence.compatible_RG` |
| `DressingFieldBphzContinuumFence.evaluations_compatible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.evaluations_compatible` |
| `DressingFieldBphzContinuumFence.nested_all_compatible` | yes | yes | yes | none | `#print axioms DressingFieldBphzContinuumFence.nested_all_compatible` |
| `DressingFieldBphzContinuumFence.nested_forest_count` | yes | yes | yes | none | `#print axioms DressingFieldBphzContinuumFence.nested_forest_count` |
| `DressingFieldBphzContinuumFence.not_compatible_LR` | yes | yes | yes | none | `#print axioms DressingFieldBphzContinuumFence.not_compatible_LR` |
| `DressingFieldBphzContinuumFence.numerator_is_7xy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.numerator_is_7xy` |
| `DressingFieldBphzContinuumFence.omitted_graph_remainder` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.omitted_graph_remainder` |
| `DressingFieldBphzContinuumFence.overlapping_excluded_iff` | yes | yes | yes | none | `#print axioms DressingFieldBphzContinuumFence.overlapping_excluded_iff` |
| `DressingFieldBphzContinuumFence.overlapping_forest_count` | yes | yes | yes | none | `#print axioms DressingFieldBphzContinuumFence.overlapping_forest_count` |
| `DressingFieldBphzContinuumFence.quotient_is_seven` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.quotient_is_seven` |
| `DressingFieldBphzContinuumFence.sector_formal_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.sector_formal_zero` |
| `DressingFieldBphzContinuumFence.sector_ne_seven` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.sector_ne_seven` |
| `DressingFieldBphzContinuumFence.sector_value` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.sector_value` |
| `DressingFieldBphzContinuumFence.share_edge_two` | yes | yes | yes | propext | `#print axioms DressingFieldBphzContinuumFence.share_edge_two` |
| `DressingFieldBphzContinuumFence.sixSum_eq_inclusion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.sixSum_eq_inclusion` |
| `DressingFieldBphzContinuumFence.sixSum_is_reduction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.sixSum_is_reduction` |
| `DressingFieldBphzContinuumFence.threeSum_eq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.threeSum_eq` |
| `DressingFieldBphzContinuumFence.witness_half_third` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldBphzContinuumFence.witness_half_third` |

- counts toward the grade: yes

### Python: `checks/independent/dfm-bphz-continuum-fence.py`

- file: [checks/independent/dfm-bphz-continuum-fence.py](../../../checks/independent/dfm-bphz-continuum-fence.py)
- sha256 (`bytes`): `0cad33ad25b1937de952b38c978ac1ef1058f91a938dc39efb5ad18f5be27752`
- cited in: record TFQ-1110
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1110_dfm_bphz_continuum_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1110_dfm_bphz_continuum_fence.md](../../../dag/derivations/24_dressing_field/tfq_1110_dfm_bphz_continuum_fence.md)
- sha256 (`lf-normalised`): `bc83ac990db5aa4d394e5a3ff90a86140075d5f9de9e79e98e4834a3b398d737`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1110
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-bphz-continuum-fence.md`

- file: [dag/derivations/independent/dfm-bphz-continuum-fence.md](../../../dag/derivations/independent/dfm-bphz-continuum-fence.md)
- sha256 (`lf-normalised`): `c3f1dcdb556b82a5398c4423a6e3a54366b441965d3f4fb20d0be2b31bbc77d1`
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
