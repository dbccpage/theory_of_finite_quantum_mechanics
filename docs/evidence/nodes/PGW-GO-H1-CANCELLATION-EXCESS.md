# PGW-GO-H1-CANCELLATION-EXCESS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Climbing round H1, installed as the twenty-second derivation, replaces one sameness sentence of the ninth seed: two results are the same when they differ only in how their terms are written, or only by an xry and an xsy asserted together. Two states are then one result exactly when they have equally many terms and, after one rewriting, the same excess e = M_r − M_s at every ordered pair (gen_iff_same, same_iff_excess), and each result has one plain state up to writing, asserting no pair in both relations (plain_reduced). The fewest changes to a result is Φ(G) = n + Σ|e(x,y)|, the plain state's size, and a shortest sequence is additions only through plain states (fewest_changes).

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

- `proved_lean_below_e3`: grade E0; 4 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 4 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

- Chosen reading C-J1: one more xry and xsy on one pair, x = y allowed, sameness the equivalence generated with rewriting (assumption)

## Bottleneck

For the chosen reading C-J1 only (the unchosen C-J2 and C-J3 give 29 and 1081 results against 673 at two terms and eight rounds); here an addition can undo an addition, so the ninth's no-return for additions does not survive the new sameness.

## Source status

001_genesis_ongoing_h3v7n5qf paper/twentysecond/claim_ledger.md D1 and D4; lean4_core/Twentysecond

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentysecond/Cost.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentysecond/Cost.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentysecond/Plain.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentysecond/Plain.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentysecond/Same.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentysecond/Same.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0483_go_h1_cancellation_excess.md`

- file: [dag/derivations/02_genesis/tfq_0483_go_h1_cancellation_excess.md](../../../dag/derivations/02_genesis/tfq_0483_go_h1_cancellation_excess.md)
- sha256 (`lf-normalised`): `db76068560fe6f5f0ecf23411725c5ddd7336902cea677b877a146f80ee95a2a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0483
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentysecond/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentysecond/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/005_oegenong/levels/level_19_round_r1_cancellation.md`

- file: `omega_engine_education/documentation/005_oegenong/levels/level_19_round_r1_cancellation.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentysecond/state.py::cost`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentysecond/state.py::excess`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentysecond/state.py::plain`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentysecond/Cost.lean::fewest_changes`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentysecond/Plain.lean::plain_reduced`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentysecond/Same.lean::gen_iff_same`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core/Twentysecond/Same.lean::same_iff_excess`

## Absences recorded by the TFQ records

- TFQ-0483 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-H1-CANCELLATION-EXCESS` `DERIVED_LEAN`: [PGW-GO-LEFTOVER-UNBOUNDEDNESS](PGW-GO-LEFTOVER-UNBOUNDEDNESS.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-H2-STATE-RAISING-GAUGE` `DERIVED_LEAN`: [PGW-GO-H2-STATE-RAISING-GAUGE](PGW-GO-H2-STATE-RAISING-GAUGE.md) (PROVED_LEAN)
