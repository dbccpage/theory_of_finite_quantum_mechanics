# PGW-CONTEXT-COUNT-FORMULA

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a regime with n admitted data, a form of arity a has (n+1)^a − n^a well-formed contexts: each slot is a hole or one of n data, less the n^a hole-free tuples, so |Ctx(R)| = Σ_f ((n+1)^{a_f} − n^{a_f}), with distinct form identifiers kept disjoint even when their arities coincide. The companion Lean module establishes the per-form count for the recursive word enumeration (contextWords_length), characterizes its members as exactly the well-formed words of that length containing a hole (contextWords_mem), and shows the enumeration has no repetitions (contextWords_nodup). The standalone replay checks the formula against the frozen Python enumeration in 35 cases (n from 0 to 4, arity 1 to 7), and Python and Rust enumerate the contexts independently.

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

- `proved_lean_below_e3`: grade E0; 3 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 3 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

None recorded.

## Bottleneck

The Lean statement is a companion result for the slot words of one form; the sum over forms is the written corollary of ledger row WDP-P000-015, which attributes it to no compiled source theorem, and large arities make profile enumeration expensive.

## Source status

paper.md section 6 counting corollary (ledger WDP-P000-015); companion Paper.lean contextWords theorems

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Paper.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Paper.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0436_context_count_formula.md`

- file: [dag/derivations/02_genesis/tfq_0436_context_count_formula.md](../../../dag/derivations/02_genesis/tfq_0436_context_count_formula.md)
- sha256 (`lf-normalised`): `b4ae351527fbf44cf00049abc978a144238ee285fdfc9e098b303f69d76a5291`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0436
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

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::contexts`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/reproduce.py::python_replay`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs::a_binary_form_over_two_data_has_five_contexts`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs::contexts`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Paper.lean::contextWords_length`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Paper.lean::contextWords_mem`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Paper.lean::contextWords_nodup`

## Routes

Incoming (1):

- `PGW-R-CONTEXT-COUNT-FORMULA` `DERIVED_LEAN`: [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)

Outgoing (1):

- `APP-R-COMP-C2-CONTEXT-COUNTS-CHECKED` `COMPUTED`: [COMP-C2-CONTEXT-COUNTS-CHECKED](COMP-C2-CONTEXT-COUNTS-CHECKED.md) (COMPUTATIONALLY_CHECKED)
