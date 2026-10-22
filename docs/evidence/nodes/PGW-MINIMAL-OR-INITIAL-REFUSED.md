# PGW-MINIMAL-OR-INITIAL-REFUSED

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_PROSE`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Question 10 asks whether the final process is minimal or initial among a defined class of finite processes satisfying the same challenges. The sealed answer is that the claim is refused and tagged unresolved: no such initiality or minimality property was established. What is established is narrower: determinism of the artifacts across the exercised runs and platforms is a finite computation (byte-identical artifacts are repeated-run agreement, not an engine theorem), completeness of enumerations within declared bounds is a bounded theorem under its ledger conditions, and the per-stage minimality and uniqueness results are theorems with their stated scopes. An earlier wording, what is proved: determinism of the engine, was corrected on 2026-09-08.

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

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

None recorded.

## Bottleneck

The later Derivation/Initiality.lean establishes minimality only relative to a declared 64-member constitution class and probe battery; that supplementary result does not answer Question 10 for the sealed process.

## Source status

genesis_source.txt question 10 claim refused \[unresolved\]; written refusal with scoped alternatives

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Initiality.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Initiality.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0453_minimal_or_initial_refused.md`

- file: [dag/derivations/02_genesis/tfq_0453_minimal_or_initial_refused.md](../../../dag/derivations/02_genesis/tfq_0453_minimal_or_initial_refused.md)
- sha256 (`lf-normalised`): `ca8791aad4fb45701f9c3a86c69fe3da588146b50044439d66fe65252a4b9089`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0453
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0453 lean4: no Lean statement of minimality or initiality among finite processes satisfying the sealed challenges
- TFQ-0453 python: no Python check; artifact determinism is repeated-run byte agreement, not a program
- TFQ-0453 rust: no Rust check; artifact determinism is repeated-run byte agreement, not a program

## Routes

Incoming (1):

- `PGW-R-MINIMAL-OR-INITIAL-REFUSED` `DERIVED_PROSE`: [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) (PROVED_PROSE)

Outgoing (1):

- `PGW-R-SEALED-TERMINAL-STATEMENT` `DERIVED_PROSE`: [PGW-SEALED-TERMINAL-STATEMENT](PGW-SEALED-TERMINAL-STATEMENT.md) (PROVED_PROSE)
