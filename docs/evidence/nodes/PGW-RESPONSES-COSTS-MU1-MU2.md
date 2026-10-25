# PGW-RESPONSES-COSTS-MU1-MU2

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A response (delta) is an ordered finite list of NewDatum, NewForm(arity), NewInst(form, args) and NewRuleAll(form) items applied in order; an instance may name a form added earlier in the same list, and the reverse order is an ill-formed admission. The declared costs are mu1 = item count and mu2 = (item count, sum of new-form arities) compared lexicographically, where the sum counts every NewForm item, including distinct forms of equal arity. A valid response to Separate(i, j) applies, separates the target, and keeps every previously imposed requirement separated, because requirements are persistent constraints.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared item grammar and cost measures mu1 and mu2, genesis_source.txt sections 3.6-3.7 (assumption)

## Bottleneck

Both measures and the item grammar are declared, not derived; bundling a form and an instance into one primitive would change every cost, and the enumerator's canonical item order makes a delta a multiset only up to that convention.

## Source status

genesis_source.txt sections 3.6-3.7 and paper.md section 7 \[definition\]; Basic.lean, Minimality.lean aritySum

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Basic.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Basic.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Basic.lean)
- sha256 (`bytes`): `151fa22bcd2d75b01ec4d924ea3f94cb4b1c020c2a9254471ff013eb43aabcc7`
- cited in: node.lean, record TFQ-0438
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Basic`): recorded sha256 `151fa22bcd2d75b01ec4d924ea3f94cb4b1c020c2a9254471ff013eb43aabcc7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Basic.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `applyDelta` | yes | yes | yes | propext | `#print axioms applyDelta` |
| `validResponse` | yes | yes | yes | propext | `#print axioms validResponse` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)
- sha256 (`bytes`): `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925`
- cited in: node.lean, record TFQ-0438
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Minimality`): recorded sha256 `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `aritySum` | yes | yes | yes | propext | `#print axioms aritySum` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/measure.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/measure.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/response.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/response.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0438_responses_costs_mu1_mu2.md`

- file: [dag/derivations/02_genesis/tfq_0438_responses_costs_mu1_mu2.md](../../../dag/derivations/02_genesis/tfq_0438_responses_costs_mu1_mu2.md)
- sha256 (`lf-normalised`): `3b07753e32e5c751084665242eb3d9655b71023d489f2e7ac122792ecf68a77e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0438
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
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

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::mu1`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::mu2`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::response_valid_naive`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/measure.rs::arity_sum`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/response.rs::response_valid_naive`

## Routes

Incoming (1):

- `PGW-R-RESPONSES-COSTS-MU1-MU2` `DERIVED_PROSE`: [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)

Outgoing (2):

- `PGW-R-CHALLENGE3-CURRENT-REGIME-FAILS` `DERIVED_LEAN`: [PGW-CHALLENGE3-CURRENT-REGIME-FAILS](PGW-CHALLENGE3-CURRENT-REGIME-FAILS.md) (PROVED_LEAN)
- `PGW-R-RESPONSE-EXISTENCE-MARK-PROGRESS` `DERIVED_LEAN`: [PGW-RESPONSE-EXISTENCE-MARK-PROGRESS](PGW-RESPONSE-EXISTENCE-MARK-PROGRESS.md) (PROVED_LEAN)
