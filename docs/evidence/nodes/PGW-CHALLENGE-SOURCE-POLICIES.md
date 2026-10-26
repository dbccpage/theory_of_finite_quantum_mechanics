# PGW-CHALLENGE-SOURCE-POLICIES

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> After Challenge 3 the challenge source is a pair of declared policies. The pair-separation closure policy reissues the admitted separation requirement pattern on collapsed pairs, one challenge branch per automorphism orbit of collapsed pairs, or nothing at the fixpoint where every pair is separated; it reads only profile equality and automorphism structure, supplies no data and imports no new goal kind. At that fixpoint the external continuation policy supplies and admits one fresh opaque token, and runs with this policy disabled are the closed-system baseline. Round 1 of every tree answers the externally imposed Challenge 3 requirement, and later separation rounds answer the closure policy.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared pair-separation closure policy and external continuation policy, genesis_source.txt sections 3.9-3.10 (assumption)

## Bottleneck

A collapsed pair is not an active obstruction by itself; the declared policy makes it one, its orbit-representative selection is also declared, and choosing it among conceivable policies is a declared-metatheory judgment, not a derived transition.

## Source status

genesis_source.txt sections 3.9-3.10 and 8.1 \[declared metatheory\]

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs)
- sha256 (`bytes`): `f9de5073d9258eac42c4e875a0c61f35f8ae2470dc4695097195387f270ec21a`
- cited in: node.rust, record TFQ-0443

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closure_challenge_orbits` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py)
- sha256 (`bytes`): `23803a3dcce2adf0dee623caba33791d41a25d2da3fdfd226da3cad2ee140b5e`
- cited in: record TFQ-0443

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closure_challenge_orbits` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0443_challenge_source_policies.md`

- file: [dag/derivations/02_genesis/tfq_0443_challenge_source_policies.md](../../../dag/derivations/02_genesis/tfq_0443_challenge_source_policies.md)
- sha256 (`lf-normalised`): `991a8927f6ee5b88489bb3d595f6044e939726216bd2a574ed2861781d4254e6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0443
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0443 lean4: no Lean statement of the closure policy; Lean states the selection-free transition relation and its transport (TFQ-0444)

## Routes

Incoming (1):

- `PGW-R-CHALLENGE-SOURCE-POLICIES` `DERIVED_PROSE`: [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `PGW-R-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR` `DERIVED_LEAN`: [PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR](PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR.md) (PROVED_LEAN)
