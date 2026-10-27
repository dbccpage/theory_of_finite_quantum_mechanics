# DFM-Z1-Z2-COUNTERTERM-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The contraction q_mu I_Lambda^mu = I_Sigma(p) - I_Sigma(p+q) of the one-loop vertex integrand and the resulting counterterm equality Z_1/Z_2 = 1 are not computed by the cited replay.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- gauge-invariant BPHZ subtraction scheme
- continuum loop integration

## Bottleneck

The recorded check is this inverse-propagator identity and one rational loop momentum. A gauge-invariant BPHZ subtraction scheme and continuum loop integration stay imported, so Z_1/Z_2 remains conditional.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.4-FENCE claims COMPUTATIONALLY_CHECKED; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DressingFieldZ1Z2CountertermFence.lean`

- file: [lean4/DressingFieldZ1Z2CountertermFence.lean](../../../lean4/DressingFieldZ1Z2CountertermFence.lean)
- sha256 (`bytes`): `b659387aa156095a4c861ee8e922918cdf6b71a88529c5e23e2a26f5f62fafaf`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-z1-z2-counterterm-fence_lean_replay.json (DressingFieldZ1Z2CountertermFence), record TFQ-1114
- replay: `verified`
  - receipt [dag/research/campaign_dfm-z1-z2-counterterm-fence_lean_replay.json](../../../dag/research/campaign_dfm-z1-z2-counterterm-fence_lean_replay.json) (module `DressingFieldZ1Z2CountertermFence`): recorded sha256 `b659387aa156095a4c861ee8e922918cdf6b71a88529c5e23e2a26f5f62fafaf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DressingFieldZ1Z2CountertermFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DressingFieldZ1Z2CountertermFence.contraction` | yes | yes | yes | none | `#print axioms DressingFieldZ1Z2CountertermFence.contraction` |
| `DressingFieldZ1Z2CountertermFence.contraction_entries` | yes | yes | yes | none | `#print axioms DressingFieldZ1Z2CountertermFence.contraction_entries` |
| `DressingFieldZ1Z2CountertermFence.inverse_difference` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldZ1Z2CountertermFence.inverse_difference` |
| `DressingFieldZ1Z2CountertermFence.propagator_values` | yes | yes | yes | none | `#print axioms DressingFieldZ1Z2CountertermFence.propagator_values` |
| `DressingFieldZ1Z2CountertermFence.sandwich` | yes | yes | yes | none | `#print axioms DressingFieldZ1Z2CountertermFence.sandwich` |
| `contraction` | yes | yes | yes | none | `#print axioms contraction` |
| `contraction_entries` | yes | yes | yes | none | `#print axioms contraction_entries` |
| `inverse_difference` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms inverse_difference` |
| `propagator_values` | yes | yes | yes | none | `#print axioms propagator_values` |
| `sandwich` | yes | yes | yes | none | `#print axioms sandwich` |

- counts toward the grade: yes

### Python: `checks/independent/dfm-z1-z2-counterterm-fence.py`

- file: [checks/independent/dfm-z1-z2-counterterm-fence.py](../../../checks/independent/dfm-z1-z2-counterterm-fence.py)
- sha256 (`bytes`): `a5ccfe72d0a135be03328e30e84036db839d646112f5a6c484a83186239ff556`
- cited in: node.source, record TFQ-1114
- counts toward the grade: yes

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1114_dfm_z1_z2_counterterm_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1114_dfm_z1_z2_counterterm_fence.md](../../../dag/derivations/24_dressing_field/tfq_1114_dfm_z1_z2_counterterm_fence.md)
- sha256 (`lf-normalised`): `21f6c3181e79ddfa0b14966a3ebb1d530eb39bc2f69e2a66189f5895b5a53987`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1114
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-z1-z2-counterterm-fence.md`

- file: [dag/derivations/independent/dfm-z1-z2-counterterm-fence.md](../../../dag/derivations/independent/dfm-z1-z2-counterterm-fence.md)
- sha256 (`lf-normalised`): `0fa288b82e6de1c92218547c35f0aab1de81ebae944a4e0a8468bb3eb2efc91e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-Z1-Z2-COUNTERTERM-FENCE` `GAP_NO_DERIVATION`: [DFM-CLIFFORD-WARD-TAKAHASHI](DFM-CLIFFORD-WARD-TAKAHASHI.md) (PROVED_PROSE), [DFM-BPHZ-CONTINUUM-FENCE](DFM-BPHZ-CONTINUUM-FENCE.md) (OPEN), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (0):

