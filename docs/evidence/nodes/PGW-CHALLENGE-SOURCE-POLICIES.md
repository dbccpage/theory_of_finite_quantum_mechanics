# PGW-CHALLENGE-SOURCE-POLICIES

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> After Challenge 3 the challenge source is a pair of declared policies. The pair-separation closure policy reissues the admitted separation requirement pattern on collapsed pairs, one challenge branch per automorphism orbit of collapsed pairs, or nothing at the fixpoint where every pair is separated; it reads only profile equality and automorphism structure, supplies no data and imports no new goal kind. At that fixpoint the external continuation policy supplies and admits one fresh opaque token, and runs with this policy disabled are the closed-system baseline. Round 1 of every tree answers the externally imposed Challenge 3 requirement, and later separation rounds answer the closure policy.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

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

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0443_challenge_source_policies.md`

- file: [dag/derivations/02_genesis/tfq_0443_challenge_source_policies.md](../../../dag/derivations/02_genesis/tfq_0443_challenge_source_policies.md)
- sha256 (`lf-normalised`): `7baea08ae5890af70b73f1ce94bf8822d935dc39b156e51dfe6cff5843483ce5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0443
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::closure_challenge_orbits`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs::closure_challenge_orbits`

## Absences recorded by the TFQ records

- TFQ-0443 lean4: no Lean statement of the closure policy; Lean states the selection-free transition relation and its transport (TFQ-0444)

## Routes

Incoming (1):

- `PGW-R-CHALLENGE-SOURCE-POLICIES` `DERIVED_PROSE`: [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `PGW-R-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR` `DERIVED_LEAN`: [PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR](PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR.md) (PROVED_LEAN)
