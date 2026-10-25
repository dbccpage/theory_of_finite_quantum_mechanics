# MAJ-MAJORANA-BRAID-YB-EXACT

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For 3 to 10 Majoranas the exact signed-permutation exchange action satisfies b_i b_{i+1} b_i = b_{i+1} b_i b_{i+1}, far commutativity, and composition with its inverse gives the identity.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
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

Fixed counts 3..10; this is the Majorana exchange action, not the Ising 2x2 representation.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-MAJORANA-BRAID-YB claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/majorana/braid_action.rs`

- file: [code/rust/src/majorana/braid_action.rs](../../../code/rust/src/majorana/braid_action.rs)
- sha256 (`bytes`): `a410d23be7fcd5eaa7343f187ccfb21222279f33e28d49a5d34909970dda5b67`
- cited in: node.rust, record TFQ-1172
- check: `cd code/rust && cargo test -p tfqm_majorana yang_baxter_far_commutativity_inverse_and_parity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `MajoranaBraidAction` (rust_symbol) | yes | yes | yes | - | - |
| `yang_baxter_far_commutativity_inverse_and_parity` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana yang_baxter_far_commutativity_inverse_and_parity` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1172_maj_majorana_braid_yb_exact.md`

- file: [dag/derivations/28_majorana/tfq_1172_maj_majorana_braid_yb_exact.md](../../../dag/derivations/28_majorana/tfq_1172_maj_majorana_braid_yb_exact.md)
- sha256 (`lf-normalised`): `fb730e61ebd5d0ee0b07a45966653d18a55d79424d7697c3d90f2c76ae04460e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1172
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-MAJORANA-BRAID-YB-EXACT` `COMPUTED`: [MAJ-IMPORT-ISING-ANYONS](MAJ-IMPORT-ISING-ANYONS.md) (IMPORTED_ASSUMPTION), [DS-QM212-MAJORANA-PROBLEM](DS-QM212-MAJORANA-PROBLEM.md) (PROVED_LEAN)

Outgoing (0):

