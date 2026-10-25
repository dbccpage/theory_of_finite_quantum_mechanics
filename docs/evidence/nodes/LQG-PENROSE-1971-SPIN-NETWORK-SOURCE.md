# LQG-PENROSE-1971-SPIN-NETWORK-SOURCE

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `SOURCE_RECORD`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Penrose (1971) starts from angular momentum, whose spectrum is discrete, and asks whether space can be built up by applying the rules for combining angular momenta; the construction is the origin of spin networks. This node records the chapter by title and publication details.

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

Record only. The 1971 book chapter has no arXiv record and is not held in the checkout; Penrose's trivalent admissibility rules are verified in Rovelli-Smolin (arXiv:gr-qc/9505006 Section 2 p. 12) and Roberts (arXiv:math-ph/9812013 Section 2 pp. 24-27).

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

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2300_lqg_penrose_1971_spin_network_source.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2300_lqg_penrose_1971_spin_network_source.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2300_lqg_penrose_1971_spin_network_source.md)
- sha256 (`lf-normalised`): `34a63fe23bde0439a3104301ae6bca3512b1b883d1a711f55cdfd112823ea49f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2300
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:book:Penrose-1971-Angular-momentum-combinatorial-space-time`

## Routes

Incoming (1):

- `FRO-R-LQG-PENROSE-1971-SPIN-NETWORK-SOURCE` `RECORD_PARENT`: [TFQ-0198](TFQ-0198.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `FRO-R-LQG-SPIN-NETWORK-KINEMATICS-SOURCE` `RECORD_PARENT`: [LQG-SPIN-NETWORK-KINEMATICS-SOURCE](LQG-SPIN-NETWORK-KINEMATICS-SOURCE.md) (SOURCE_RECORD)
