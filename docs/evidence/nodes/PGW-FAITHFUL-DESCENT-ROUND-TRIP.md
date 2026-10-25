# PGW-FAITHFUL-DESCENT-ROUND-TRIP

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For supplied translations f : P → Q and g : Q → P, injective maps i : P → C and j : Q → C with i = j ∘ f and j = i ∘ g exist if and only if g ∘ f = id_P and f ∘ g = id_Q (faithful_descent_iff_round_trip_coherent). One direction substitutes the identifying equations and cancels the injective maps (faithful_descent_to_coherent); the other takes C = P, i = id and j = g. A failed round trip for this declared pair therefore excludes a faithful common carrier that eliminates the presentation index.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Failure concerns the declared translation pair only: another pair of translations may still close, and no common world prior to P and Q is assumed.

## Source status

paper.md section 10 (ledger WDP-P000-021); PresentationDescent.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean)
- sha256 (`bytes`): `0031439e3cf7216aa25ed09bcc97dc19f42931238a4f53691d1789b023caab92`
- cited in: node.lean, node.source, record TFQ-0458
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.PresentationDescent`): recorded sha256 `0031439e3cf7216aa25ed09bcc97dc19f42931238a4f53691d1789b023caab92` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `faithful_descent_iff_round_trip_coherent` | yes | yes | yes | none | `#print axioms faithful_descent_iff_round_trip_coherent` |
| `faithful_descent_to_coherent` | yes | yes | yes | none | `#print axioms faithful_descent_to_coherent` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0458_faithful_descent_round_trip.md`

- file: [dag/derivations/02_genesis/tfq_0458_faithful_descent_round_trip.md](../../../dag/derivations/02_genesis/tfq_0458_faithful_descent_round_trip.md)
- sha256 (`lf-normalised`): `862a266bc6c59d8e826dee7ce68e2df5572f5cc3da0a25f932da06b79dd71f24`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0458
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/fixtures/historical_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/fixtures/historical_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0458 python: no Python check of presentation descent
- TFQ-0458 rust: no Rust check of presentation descent

## Routes

Incoming (1):

- `PGW-R-FAITHFUL-DESCENT-ROUND-TRIP` `DERIVED_LEAN`: [PGW-QUOTIENT-RETENTION](PGW-QUOTIENT-RETENTION.md) (PROVED_LEAN)

Outgoing (0):

