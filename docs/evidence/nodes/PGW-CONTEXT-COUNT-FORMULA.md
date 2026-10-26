# PGW-CONTEXT-COUNT-FORMULA

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a regime with n admitted data, a form of arity a has (n+1)^a − n^a well-formed contexts: each slot is a hole or one of n data, less the n^a hole-free tuples, so |Ctx(R)| = Σ_f ((n+1)^{a_f} − n^{a_f}), with distinct form identifiers kept disjoint even when their arities coincide. The companion Lean module establishes the per-form count for the recursive word enumeration (contextWords_length), characterizes its members as exactly the well-formed words of that length containing a hole (contextWords_mem), and shows the enumeration has no repetitions (contextWords_nodup). The standalone replay checks the formula against the frozen Python enumeration in 35 cases (n from 0 to 4, arity 1 to 7), and Python and Rust enumerate the contexts independently.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

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

### Lean: `lean4/Imported/Genesis19l57g1/Paper.lean`

- file: [lean4/Imported/Genesis19l57g1/Paper.lean](../../../lean4/Imported/Genesis19l57g1/Paper.lean)
- sha256 (`bytes`): `9503a9507c67532a9c0a7a51eb8f3ea66fc8c3371692bab8579b04e77ba4b89c`
- cited in: node.lean, record TFQ-0436
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Paper`): recorded sha256 `9503a9507c67532a9c0a7a51eb8f3ea66fc8c3371692bab8579b04e77ba4b89c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Paper.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `contextWords_length` | yes | yes | yes | Quot.sound, propext | `#print axioms contextWords_length` |
| `contextWords_mem` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms contextWords_mem` |
| `contextWords_nodup` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms contextWords_nodup` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0436_context_count_formula.md`

- file: [dag/derivations/02_genesis/tfq_0436_context_count_formula.md](../../../dag/derivations/02_genesis/tfq_0436_context_count_formula.md)
- sha256 (`lf-normalised`): `6cb475beb3074fcb60189da7c59038c405a2d353c0f2b8d5099b2b2e115865a7`
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

- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::contexts`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/reproduce.py::python_replay`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs::a_binary_form_over_two_data_has_five_contexts`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs::contexts`

## Routes

Incoming (1):

- `PGW-R-CONTEXT-COUNT-FORMULA` `DERIVED_LEAN`: [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)

Outgoing (1):

- `APP-R-COMP-C2-CONTEXT-COUNTS-CHECKED` `COMPUTED`: [COMP-C2-CONTEXT-COUNTS-CHECKED](COMP-C2-CONTEXT-COUNTS-CHECKED.md) (COMPUTATIONALLY_CHECKED)
