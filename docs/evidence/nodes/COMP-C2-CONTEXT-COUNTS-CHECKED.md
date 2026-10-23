# COMP-C2-CONTEXT-COUNTS-CHECKED

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For 2 data and arity 3 there are 19 = 3^3 - 2^3 contexts with a hole and 12 = 3*2^2 with exactly one hole (decide); Rust enumerates n from 0 to 4 and a from 1 to 5, Python n from 0 to 3 and a from 1 to 4, and both match (n+1)^a - n^a and a*n^(a-1).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Finite ranges only; the general formula is the trunk record TFQ-0436.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C2d claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1289
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `allCtxs` | yes | yes | yes | none | `#print axioms allCtxs` |
| `genesis_context_count_n2_a3` | yes | yes | yes | none | `#print axioms genesis_context_count_n2_a3` |
| `genesis_one_hole_count_n2_a3` | yes | yes | yes | none | `#print axioms genesis_one_hole_count_n2_a3` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1289
- check: `cd code/rust && cargo test -p tfqm_wdp context_count_formula_and_one_hole_splits`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `context_count_formula_and_one_hole_splits` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp context_count_formula_and_one_hole_splits` |
- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1289

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `context_counts` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1289_comp_c2_context_counts_checked.md`

- file: [dag/derivations/29_computation/tfq_1289_comp_c2_context_counts_checked.md](../../../dag/derivations/29_computation/tfq_1289_comp_c2_context_counts_checked.md)
- sha256 (`lf-normalised`): `9b5ae28944e647b2166847bdaf76d09aaaf75b503f76e248bc53ba594907a27c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1289
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C2-CONTEXT-COUNTS-CHECKED` `COMPUTED`: [COMP-C2-ONE-HOLE-CONTEXTS](COMP-C2-ONE-HOLE-CONTEXTS.md) (PROVED_LEAN), [PGW-CONTEXT-COUNT-FORMULA](PGW-CONTEXT-COUNT-FORMULA.md) (PROVED_LEAN)

Outgoing (0):

