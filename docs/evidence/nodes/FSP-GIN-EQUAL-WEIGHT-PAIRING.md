# FSP-GIN-EQUAL-WEIGHT-PAIRING

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the four-site periodic ring, U = 0, two spin-up fermions, beta = 3/2 and four Euler slices, all 32 negative Euler-transfer paths are matched to disjoint positive paths of exactly equal rational weight within one weight fiber, and a posting-list query over k modes uses k posting-list operations.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 1
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Pairing is on exact weight fibers of enumerated paths, not a spectator-preserving symmetry (INV-GIN-PARITY); it does not preserve general observables, and path enumeration grows exponentially. CT-AUX update stability for multi-orbital models has no evidence here.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-029 claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/fsp/lean4/FermionGinCore.lean`

- file: [papers/core/fsp/lean4/FermionGinCore.lean](../../../papers/core/fsp/lean4/FermionGinCore.lean)
- sha256 (`bytes`): `256bae210455bd503809c9ef8a10e44b6692daa633ac8e13e253dcf78995d0b8`
- cited in: node.lean, record TFQ-1194
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_fermion_sign.json](../../../dag/research/lean_replay_campaign_fermion_sign.json) (module `papers.core.fsp.lean4.FermionGinCore`): recorded sha256 `256bae210455bd503809c9ef8a10e44b6692daa633ac8e13e253dcf78995d0b8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/FermionGinCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `involution_pair_cancels_sign` | yes | yes | yes | propext | `#print axioms involution_pair_cancels_sign` |

- counts toward the grade: yes

### Python: `code/python/src/fsp/ct_aux_streaming_gin_engine.py`

- file: [code/python/src/fsp/ct_aux_streaming_gin_engine.py](../../../code/python/src/fsp/ct_aux_streaming_gin_engine.py)
- sha256 (`bytes`): `a72f168b1137e491f9b06d0fe0e4955ed1a0f44b903dd76b2049a971b8ede16a`
- cited in: record TFQ-1194
- counts toward the grade: yes

### Python: `code/python/src/fsp/hamiltonian_gin_bridge.py`

- file: [code/python/src/fsp/hamiltonian_gin_bridge.py](../../../code/python/src/fsp/hamiltonian_gin_bridge.py)
- sha256 (`bytes`): `e98362f08174e77b61e2ec4e160ba89f98958e0b0f4c88f7604f7d2415cd5661`
- cited in: record TFQ-1194

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HamiltonianGinBridge` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py`

- file: [code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py](../../../code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py)
- sha256 (`bytes`): `68f3187c2ce37cedf22b138186c54216552ec59163e1b6bc67ddeb519ab4f5ca`
- cited in: record TFQ-1194
- check: `python -m pytest code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py::test_bipartite_hamiltonian_indexing_and_sign_repair`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_bipartite_hamiltonian_indexing_and_sign_repair` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py::test_bipartite_hamiltonian_indexing_and_sign_repair` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1194_fsp_gin_equal_weight_pairing.md`

- file: [dag/derivations/26_fsp/tfq_1194_fsp_gin_equal_weight_pairing.md](../../../dag/derivations/26_fsp/tfq_1194_fsp_gin_equal_weight_pairing.md)
- sha256 (`lf-normalised`): `f82b7690b3cc753c61f7f618bfbe7bf68a74ad350122e2a0db90ad411fb10e79`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1194
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
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-GIN-EQUAL-WEIGHT-PAIRING` `COMPUTED`: [FSP-INVOLUTION-PAIR-CANCELLATION](FSP-INVOLUTION-PAIR-CANCELLATION.md) (PROVED_LEAN)

Outgoing (0):

