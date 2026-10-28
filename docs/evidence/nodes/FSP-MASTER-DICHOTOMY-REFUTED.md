# FSP-MASTER-DICHOTOMY-REFUTED

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `REFUTED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The claimed dichotomy (each finite quantum system either admits a certified sign-eliminating involution found in polynomial time or is an NP-hard sign obstruction) fails as stated: NP-hardness is a property of input families, the free triangle has no equal-weight involution in its declared basis yet is solved by one-body diagonalization, and zero signed mass need not come from an involution.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The open research content is FSP-EFFICIENT-SAMPLING-OBLIGATIONS: for a stated model family and input encoding, separate exact finite identities, protected sign-free representations, efficient samplers and worst-case hardness.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-056 claims PROVED_LEAN; audited status REFUTED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/fsp/lean4/FermionSignAll.lean`

- file: [papers/core/fsp/lean4/FermionSignAll.lean](../../../papers/core/fsp/lean4/FermionSignAll.lean)
- sha256 (`bytes`): `d86d833204ee0cefd0486bd5cf9622844712608771854534daa4991d62706866`
- cited in: node.lean, node.source, record TFQ-1220
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/FermionSignAll.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `package_mechanization_total` | yes | yes | yes | - | `#print axioms package_mechanization_total` |

- counts toward the grade: yes

### Lean: `papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean`

- file: [papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean](../../../papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean)
- sha256 (`bytes`): `85c88263bbce28035a35b9282b747a7e97959c514a66c3c49fa770d5db49f6cd`
- cited in: node.lean, record TFQ-1220
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_fermion_sign.json](../../../dag/research/lean_replay_campaign_fermion_sign.json) (module `papers.core.fsp.lean4.FrustratedSpectrumObstruction`): recorded sha256 `85c88263bbce28035a35b9282b747a7e97959c514a66c3c49fa770d5db49f6cd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `disjoint_spectra_obstructs_involution` | yes | yes | yes | none | `#print axioms disjoint_spectra_obstructs_involution` |

- counts toward the grade: yes

### Lean: `papers/core/fsp/lean4/MeronCharacter.lean`

- file: [papers/core/fsp/lean4/MeronCharacter.lean](../../../papers/core/fsp/lean4/MeronCharacter.lean)
- sha256 (`bytes`): `0252c6f943a0bdf6a9975a60cbc041c932c58fe9cf335fa3381f1c987b9e1870`
- cited in: node.lean, record TFQ-1220
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_fermion_sign.json](../../../dag/research/lean_replay_campaign_fermion_sign.json) (module `papers.core.fsp.lean4.MeronCharacter`): recorded sha256 `0252c6f943a0bdf6a9975a60cbc041c932c58fe9cf335fa3381f1c987b9e1870` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/MeronCharacter.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `unequal_three_term_cancellation` | yes | yes | yes | none | `#print axioms unequal_three_term_cancellation` |

- counts toward the grade: yes

### Python: `code/python/src/fsp/fermionic_hamiltonian.py`

- file: [code/python/src/fsp/fermionic_hamiltonian.py](../../../code/python/src/fsp/fermionic_hamiltonian.py)
- sha256 (`bytes`): `a4dc86f7f27c56cb8616761b11020be719336fef242972406f07dca87a8b744d`
- cited in: record TFQ-1220

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `free_triangle_analytics` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py`

- file: [code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py](../../../code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py)
- sha256 (`bytes`): `68f3187c2ce37cedf22b138186c54216552ec59163e1b6bc67ddeb519ab4f5ca`
- cited in: record TFQ-1220
- check: `python -m pytest code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py::test_frustrated_triangle_hamiltonian_indexing_obstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_frustrated_triangle_hamiltonian_indexing_obstruction` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py::test_frustrated_triangle_hamiltonian_indexing_obstruction` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1220_fsp_master_dichotomy_refuted.md`

- file: [dag/derivations/26_fsp/tfq_1220_fsp_master_dichotomy_refuted.md](../../../dag/derivations/26_fsp/tfq_1220_fsp_master_dichotomy_refuted.md)
- sha256 (`lf-normalised`): `d00576635036e6ed0fca7dc12e7554a30c7bbf415dffaf8313f7d5048f44895f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1220
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md)
- sha256 (`lf-normalised`): `0a97b32d187a99450605943866d6d4285f0bfd73dcc021c2b69911243066f2f3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-TROYER-WIESE-REDUCTION](FSP-TROYER-WIESE-REDUCTION.md) (IMPORTED_ASSUMPTION), [FSP-HUBBARD-PROTECTED-REPRESENTATIONS](FSP-HUBBARD-PROTECTED-REPRESENTATIONS.md) (CONDITIONAL), [FSP-LATTICE-ANOMALY-INFLOW](FSP-LATTICE-ANOMALY-INFLOW.md) (OPEN), [FSP-IMAGINARY-MU-REAL-DET](FSP-IMAGINARY-MU-REAL-DET.md) (IMPORTED_ASSUMPTION), [FSP-WITTEN-INDEX-INVARIANCE](FSP-WITTEN-INDEX-INVARIANCE.md) (IMPORTED_ASSUMPTION), [FSP-COBORDISM-INTRINSIC-SIGN](FSP-COBORDISM-INTRINSIC-SIGN.md) (OPEN), [FSP-DIRAC-KAHLER-SPINFOAM-CLAIM](FSP-DIRAC-KAHLER-SPINFOAM-CLAIM.md) (OPEN), [FSP-HINGE-LINEON-SIGN-CLAIM](FSP-HINGE-LINEON-SIGN-CLAIM.md) (OPEN), [FSP-FREE-TRIANGLE-REPRESENTATION](FSP-FREE-TRIANGLE-REPRESENTATION.md) (COMPUTATIONALLY_CHECKED), [FSP-INVOLUTION-PAIR-CANCELLATION](FSP-INVOLUTION-PAIR-CANCELLATION.md) (PROVED_LEAN)

Outgoing (0):

