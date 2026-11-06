# DFM-GRIBOV-CONTINUUM-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Statements about the continuum Gribov-Singer obstruction, the Gribov horizon of the Faddeev-Popov operator, ghost-free continuum quantization, or the Yang-Mills mass gap are not established by the finite diamond checks.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuum Yang-Mills theory
- Faddeev-Popov quantization

## Bottleneck

The recorded comparison is this pair of quadratic forms on two generators of one diagonal matrix. A refinement family of lattices, an operator spectrum, and a limit theorem stay open before any continuum transport.

## Source status

dag/derivations/24_dressing_field/ravera_dfm_dossier.md record DFM-P3.8-FENCE claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DressingFieldGribovContinuumFence.lean`

- file: [lean4/DressingFieldGribovContinuumFence.lean](../../../lean4/DressingFieldGribovContinuumFence.lean)
- sha256 (`bytes`): `5fc39e796df35b9b985b8b6371a866c117a3c61f9671ee8a25f98b60a04b12b7`
- cited in: node.lean, node.source, receipt evidence/lean_receipts/campaign_dfm-gribov-continuum-fence_lean_replay.json (DressingFieldGribovContinuumFence), record TFQ-1132
- replay: `verified`
  - receipt [evidence/lean_receipts/campaign_dfm-gribov-continuum-fence_lean_replay.json](../../../evidence/lean_receipts/campaign_dfm-gribov-continuum-fence_lean_replay.json) (module `DressingFieldGribovContinuumFence`): recorded sha256 `5fc39e796df35b9b985b8b6371a866c117a3c61f9671ee8a25f98b60a04b12b7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DressingFieldGribovContinuumFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DressingFieldGribovContinuumFence.forms_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldGribovContinuumFence.forms_differ` |
| `DressingFieldGribovContinuumFence.h12_square` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldGribovContinuumFence.h12_square` |
| `DressingFieldGribovContinuumFence.h23_square` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldGribovContinuumFence.h23_square` |
| `DressingFieldGribovContinuumFence.omega1_square_and_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldGribovContinuumFence.omega1_square_and_det` |
| `DressingFieldGribovContinuumFence.trace_pair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldGribovContinuumFence.trace_pair` |
| `forms_differ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms forms_differ` |
| `h12_square` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms h12_square` |
| `h23_square` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms h23_square` |
| `omega1_square_and_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms omega1_square_and_det` |
| `trace_pair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms trace_pair` |

- counts toward the grade: yes

### Python: `checks/independent/dfm-gribov-continuum-fence.py`

- file: [checks/independent/dfm-gribov-continuum-fence.py](../../../checks/independent/dfm-gribov-continuum-fence.py)
- sha256 (`bytes`): `0c002a142eb5b80fda598f127763dd9a2ade4345578c2cd3b73cee23713e6638`
- cited in: node.source, record TFQ-1132
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/ravera_dfm_dossier.md`

- file: [dag/derivations/24_dressing_field/ravera_dfm_dossier.md](../../../dag/derivations/24_dressing_field/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `a41d66a41925e1236c1c506bfb4e3fa7222de96f7211faa6981d14b677cbe36b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1132_dfm_gribov_continuum_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1132_dfm_gribov_continuum_fence.md](../../../dag/derivations/24_dressing_field/tfq_1132_dfm_gribov_continuum_fence.md)
- sha256 (`lf-normalised`): `413051784fd9ec7618ee38d3d76a1b8ae8f44cac30ed649a76d869dd8345867d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1132
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-gribov-continuum-fence.md`

- file: [dag/derivations/independent/dfm-gribov-continuum-fence.md](../../../dag/derivations/independent/dfm-gribov-continuum-fence.md)
- sha256 (`lf-normalised`): `19149f01a88b5d6441c19665a2d0e2e91ea0a1c4185edd2294ca8f8b6be544e6`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-GRIBOV-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-SU3-GRIBOV-COPIES-DIAMOND](DFM-SU3-GRIBOV-COPIES-DIAMOND.md) (COMPUTATIONALLY_CHECKED), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (0):

