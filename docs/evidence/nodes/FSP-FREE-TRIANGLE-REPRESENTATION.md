# FSP-FREE-TRIANGLE-REPRESENTATION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the 3-site spinless triangle, t = 1, U = 0, two fermions, beta = 2 and three Euler slices, the occupation-basis expansion has 27 paths, 6 negative of weight 8/27 and positive weights in {4/9, 1}, so no equal-weight pairing exists there; in the one-body eigenbasis H is diagonal with E in {-1, -1, 2} and Z = 2e^2 + e^-4.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declaration references covered by a current replay receipt: 2
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Frustration alone does not imply disjoint weight spectra or hardness (ledger GIN-C4, INV-DISJOINT-SPEC); the general Lean lemma covers only the step from disjoint spectra to no weight-preserving sign-reversing involution.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-025 claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean`

- file: [papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean](../../../papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean)
- sha256 (`bytes`): `85c88263bbce28035a35b9282b747a7e97959c514a66c3c49fa770d5db49f6cd`
- cited in: node.lean, record TFQ-1191
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_fermion_sign.json](../../../dag/research/lean_replay_campaign_fermion_sign.json) (module `papers.core.fsp.lean4.FrustratedSpectrumObstruction`): recorded sha256 `85c88263bbce28035a35b9282b747a7e97959c514a66c3c49fa770d5db49f6cd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `disjoint_pair_residual_nonzero` | yes | yes | yes | Quot.sound, propext | `#print axioms disjoint_pair_residual_nonzero` |
| `disjoint_spectra_obstructs_involution` | yes | yes | yes | none | `#print axioms disjoint_spectra_obstructs_involution` |

- counts toward the grade: yes

### Python: `code/python/src/fsp/fermionic_hamiltonian.py`

- file: [code/python/src/fsp/fermionic_hamiltonian.py](../../../code/python/src/fsp/fermionic_hamiltonian.py)
- sha256 (`bytes`): `a4dc86f7f27c56cb8616761b11020be719336fef242972406f07dca87a8b744d`
- cited in: record TFQ-1191

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `free_triangle_analytics` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/fsp/hamiltonian_gin_bridge.py`

- file: [code/python/src/fsp/hamiltonian_gin_bridge.py](../../../code/python/src/fsp/hamiltonian_gin_bridge.py)
- sha256 (`bytes`): `e98362f08174e77b61e2ec4e160ba89f98958e0b0f4c88f7604f7d2415cd5661`
- cited in: record TFQ-1191

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `index_hamiltonian_paths` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py`

- file: [code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py](../../../code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py)
- sha256 (`bytes`): `68f3187c2ce37cedf22b138186c54216552ec59163e1b6bc67ddeb519ab4f5ca`
- cited in: record TFQ-1191
- check: `python -m pytest code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py::test_frustrated_triangle_hamiltonian_indexing_obstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_frustrated_triangle_hamiltonian_indexing_obstruction` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py::test_frustrated_triangle_hamiltonian_indexing_obstruction` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1191_fsp_free_triangle_representation.md`

- file: [dag/derivations/26_fsp/tfq_1191_fsp_free_triangle_representation.md](../../../dag/derivations/26_fsp/tfq_1191_fsp_free_triangle_representation.md)
- sha256 (`lf-normalised`): `d72e3cb7374dc789922651a3abd290ff03744ca4ba3aa671db2789141bae7aa1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1191
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-FREE-TRIANGLE-REPRESENTATION` `COMPUTED`: [FSP-SIGNED-HOPPING-PATH-SERIES](FSP-SIGNED-HOPPING-PATH-SERIES.md) (PROVED_PROSE), [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)

Outgoing (2):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
- `APP-R-FSP-TROYER-WIESE-REDUCTION` `CONDITIONAL_ON_IMPORT`: [FSP-TROYER-WIESE-REDUCTION](FSP-TROYER-WIESE-REDUCTION.md) (IMPORTED_ASSUMPTION)
