# LQG-TURAEV-VIRO-1992-SOURCE

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `SOURCE_RECORD`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Turaev and Viro (1992) define a purely combinatorial invariant of 3-manifolds as a state sum over a triangulation, built from the quantum 6j symbols of U_q(sl_2) at a root of unity; it does not depend on the triangulation. This node records the paper by title and journal reference.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Record only. The paper has no arXiv record and is not held in the checkout.

## Source status

Published source cited by title, authors and identifier (checked against the arXiv or DOI record on 2026-10-21); no derivation from it is read, audited or reproduced in this repository.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/general_relativity/spin_foam.rs`

- file: [code/rust/src/general_relativity/spin_foam.rs](../../../code/rust/src/general_relativity/spin_foam.rs)
- sha256 (`bytes`): `8ab22473e5ebc36ab2cb23247e2d6835664bab9ac0e9f0f26b6ab9b4fd63892e`
- cited in: node.source
- note: no test is cited for this symbol; its crate is tfqm_general_relativity
- counts toward the grade: yes

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2310_lqg_turaev_viro_1992_source.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2310_lqg_turaev_viro_1992_source.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2310_lqg_turaev_viro_1992_source.md)
- sha256 (`lf-normalised`): `f277faaf99061ffdee4eeb8ea1dec368618463b771656c4ceb7cdcb2384a63ed`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2310
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:doi:10.1016/0040-9383(92)90015-A`

## Routes

Incoming (1):

- `FRO-R-LQG-TURAEV-VIRO-1992-SOURCE` `RECORD_PARENT`: [TFQ-0198](TFQ-0198.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `FRO-R-LQG-TV-LEVEL2-PENTAGON-TARGET` `DERIVED_LEAN`: [LQG-TV-LEVEL2-PENTAGON-TARGET](LQG-TV-LEVEL2-PENTAGON-TARGET.md) (PROVED_LEAN)
