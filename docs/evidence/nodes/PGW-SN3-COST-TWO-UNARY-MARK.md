# PGW-SN3-COST-TWO-UNARY-MARK

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(3) requires the admitted opaque data \<a\> and \<ab\> to be separated, starting from a form-less, instance-less regime and counting each admitted item once. No response of at most one item separates the pair (cost1_insufficient_general), and one new unary form with one instance at a demanded endpoint does, so the minimum item count is 2 in both readings. Under item count the minima tie: at max_items 2 and max_arity 2 reading L has 6 valid deltas in 3 classes (unary mark, binary link, binary self-loop) and reading F has 10 in 5, and in reading L the tie class over all arities is countably infinite. Under the lexicographic cost mu2 = (items, new-form arity sum) the unique minimum up to source isomorphism is the unary mark (2,1), in reading L (mu2_unique) and reading F (mu2_unique_F).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared response grammar NewDatum, NewForm, NewInst, NewRuleAll and the costs mu1 and mu2 of the sealed Genesis account (assumption)

## Bottleneck

The mu2 minimizer is a unary mark, not a binary edge: a binary link is one of the tied mu1 responses and an edge reading is an additional interpretation. S3Separation.cost_floor in sn_core.py is a fixture parameter, and testing that it equals 2 does not reprove minimality; the cost belongs to this item grammar only.

## Source status

genesis_source.txt section 7 (Challenge 3, mu1 ties, mu2 uniqueness); Lean Derivation/Minimality and MinimalityF

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)
- sha256 (`bytes`): `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925`
- cited in: node.lean, record TFQ-0514
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Minimality`): recorded sha256 `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cost1_insufficient_general` | yes | yes | yes | propext | `#print axioms cost1_insufficient_general` |
| `mu2_unique` | yes | yes | yes | Quot.sound, propext | `#print axioms mu2_unique` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/MinimalityF.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/MinimalityF.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/MinimalityF.lean)
- sha256 (`bytes`): `d9886a5c94b65a96b4f3364c3bb6cd63064a843e57d2afff536035ced039242f`
- cited in: node.lean, record TFQ-0514
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.Genesis19l57g1.Derivation.MinimalityF`): recorded sha256 `d9886a5c94b65a96b4f3364c3bb6cd63064a843e57d2afff536035ced039242f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/MinimalityF.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mu2_unique_F` | yes | yes | yes | Quot.sound, propext | `#print axioms mu2_unique_F` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0514_sn3_cost_two_unary_mark.md`

- file: [dag/derivations/05_mssn_sn/tfq_0514_sn3_cost_two_unary_mark.md](../../../dag/derivations/05_mssn_sn/tfq_0514_sn3_cost_two_unary_mark.md)
- sha256 (`lf-normalised`): `255d02540738651ece5992e2386d11d53a70871553395ee9403ff5bbb032f2e3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0514
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_03_abstract_simplices.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_03_abstract_simplices.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::iter_cost2_deltas`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::mu2`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs::min_responses`

## Routes

Incoming (1):

- `PGW-R-SN3-COST-TWO-UNARY-MARK` `DERIVED_LEAN`: [PGW-SN2-OPAQUE-COLLAPSE](PGW-SN2-OPAQUE-COLLAPSE.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-SN-ENDPOINT-LEMMA` `DERIVED_LEAN`: [PGW-SN-ENDPOINT-LEMMA](PGW-SN-ENDPOINT-LEMMA.md) (PROVED_LEAN)
- `PGW-R-SN4-POLICY-CLOSURE-CYCLE-SPACE` `DERIVED_PROSE`: [PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE](PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE.md) (PROVED_PROSE)
