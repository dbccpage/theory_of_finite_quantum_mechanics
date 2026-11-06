# PGW-SEALED-TERMINAL-STATEMENT

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Section 11 of the sealed manuscript states the terminal result within the declared metatheory and candidate grammar, with one tag per clause. Clauses (a) to (c) are theorems: the initial inscription generates nothing and supply without admission never changes state; admission without judgment structure yields total collapse, so admission need not increase expressive power; and the first separation costs exactly two items in both readings. Clause (d) is a theorem for reading L (three tied mu1 classes and an infinite arity family), a bounded theorem for the five reading-F classes, and a theorem for mu2 uniqueness up to isomorphism in both readings, and clause (e) is the response-existence theorem. Clause (f) is a bounded theorem: no endogenous demand generator was derived and closure terminates within n(n−1)/2 rounds, 1 and 3 rounds in the baselines. Clause (g) is a finite computation, the external policy reaching depth 15 with mu2 quotient trees of 963 and 1847 nodes, and clause (h) is unresolved: both admission readings survive.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The clauses keep separate tags: (f) is bounded, (g) is a finite computation whose continuation past the exported depths is unresolved, (h) is unresolved, and no unboundedness or reading selection is claimed.

## Source status

Section 11 terminal clauses (a)-(f) composite verification mechanized in WdpBatch7.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch7.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch7.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch7.lean)
- sha256 (`bytes`): `325cb7b3dd05bf6b4c4f5081935af36bbddc9493b7404f2bb3cce46bc0e32fc5`
- cited in: node.lean, record TFQ-0454
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch7.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch7.sealed_terminal_clauses_a_to_f_bundle` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch7.sealed_terminal_clauses_a_to_f_bundle` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0454_sealed_terminal_statement.md`

- file: [dag/derivations/02_genesis/tfq_0454_sealed_terminal_statement.md](../../../dag/derivations/02_genesis/tfq_0454_sealed_terminal_statement.md)
- sha256 (`lf-normalised`): `ad7de2e55e073ef2302e36955963a2c9d9b953398539317e903a2d2a07e6b5d1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0454
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0454 python: no Python check of the composed statement; its clauses carry their own checks
- TFQ-0454 rust: no Rust check of the composed statement; its clauses carry their own checks

## Routes

Incoming (1):

- `PGW-R-SEALED-TERMINAL-STATEMENT` `DERIVED_LEAN`: [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) (PROVED_LEAN), [PGW-IDENTITY-IS-INDEX-NOT-PROFILE](PGW-IDENTITY-IS-INDEX-NOT-PROFILE.md) (PROVED_LEAN), [PGW-MINIMAL-OR-INITIAL-REFUSED](PGW-MINIMAL-OR-INITIAL-REFUSED.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-D2-INITIAL-POINTED` `DERIVED_LEAN`: [PGW-D2-INITIAL-POINTED](PGW-D2-INITIAL-POINTED.md) (PROVED_LEAN)
- `PGW-R-GENESIS-THREE-AXIS-VERDICT` `COMPUTED`: [PGW-GENESIS-THREE-AXIS-VERDICT](PGW-GENESIS-THREE-AXIS-VERDICT.md) (COMPUTATIONALLY_CHECKED)
