# MAJ-KITAEV-SWEETSPOT-EXACT

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the exact Gaussian-rational 2-mode Fock carrier with t = Delta = 1, mu = 0, the Kitaev Hamiltonian is Hermitian, commutes with fermion parity, commutes with gamma_1 and gamma_4, and the bulk invariant is -1.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Fixed L = 2 instance; general L and the BdG spectrum remain imported.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-KITAEV-SWEETSPOT-EXACT claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/majorana/majorana_fock_algebra.rs`

- file: [code/rust/src/majorana/majorana_fock_algebra.rs](../../../code/rust/src/majorana/majorana_fock_algebra.rs)
- sha256 (`bytes`): `5da71d117706660f313b3ab162cf2155ed9b852878651667e066d564a5ba9602`
- cited in: node.rust, record TFQ-1169
- check: `cd code/rust && cargo test -p tfqm_majorana test_kitaev_chain_properties`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bulk_kitaev_invariant` (rust_symbol) | yes | yes | yes | - | - |
| `kitaev_chain` (rust_symbol) | yes | yes | yes | - | - |
| `test_kitaev_chain_properties` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana test_kitaev_chain_properties` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1169_maj_kitaev_sweetspot_exact.md`

- file: [dag/derivations/28_majorana/tfq_1169_maj_kitaev_sweetspot_exact.md](../../../dag/derivations/28_majorana/tfq_1169_maj_kitaev_sweetspot_exact.md)
- sha256 (`lf-normalised`): `9c320b820791961af11a4324a73402379179d2669785707024f2a6aa23e75f31`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1169
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-KITAEV-SWEETSPOT-EXACT` `COMPUTED`: [MAJ-IMPORT-KITAEV-CHAIN](MAJ-IMPORT-KITAEV-CHAIN.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

