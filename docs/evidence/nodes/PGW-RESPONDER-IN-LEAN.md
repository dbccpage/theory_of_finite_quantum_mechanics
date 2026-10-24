# PGW-RESPONDER-IN-LEAN

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN: in one declared shadow, a demand is read only for the collapsed kind with the uniform-rule flag false. Of the four flag pairs, the read count is 1. The copied mark, a form of arity 1 followed by argument list \[0\], and the copied link, a form of arity 2 followed by \[0, 1\], each have length 2. Item-count cost mu1 is 2 for both, so the two lists tie at cost 2. The pair cost mu2 is (2, 1) for the mark and (2, 2) for the link, and (2, 1) precedes (2, 2) because the item counts are equal and 1 \< 2. Both lists lie inside the shadow bound of length at most 2 and new-form arity sum at most 2 with no rule item. A two-item list that contains a rule item lies outside that bound. One three-item list has length 3 and lies outside the length bound 2. This shadow does not state the sealed responder, and the node status stays OPEN.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- cited Lean declarations covered by a current replay receipt: 9
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The shadow reads one declared flag table and compares two copied lists. It does not state a minimum, a cost, or a tie of the sealed responder in the second derivation's packages (S-3). It does not refuse a regime that holds a uniform rule (S-1), and it does not read or refuse a same pair that is separable (S-2). The length bound 2 is not identified with the grammar (S-4). Attempt one's G-4 and attempt two's H-1 stay open. Status stays OPEN.

## Source status

continuation.txt §13 Responses in Lean (S-1 to S-4) and attempt one's leftovers (G-4)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwResponderInLean.lean`

- file: [lean4/CampaignPgwResponderInLean.lean](../../../lean4/CampaignPgwResponderInLean.lean)
- sha256 (`bytes`): `a34f1b2c2c613cd3b2dd699af64e683c19d04bfa57b48d659bb8d4cd9bb313b9`
- cited in: node.lean, receipt dag/research/campaign_pgw-responder-in-lean_lean_replay.json (CampaignPgwResponderInLean), record TFQ-0496
- replay: `verified`
  - receipt [dag/research/campaign_pgw-responder-in-lean_lean_replay.json](../../../dag/research/campaign_pgw-responder-in-lean_lean_replay.json) (module `CampaignPgwResponderInLean`): recorded sha256 `a34f1b2c2c613cd3b2dd699af64e683c19d04bfa57b48d659bb8d4cd9bb313b9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwResponderInLean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwBound_inside` | yes | yes | yes | propext | `#print axioms pgwBound_inside` |
| `pgwMark_link_shape` | yes | yes | yes | propext | `#print axioms pgwMark_link_shape` |
| `pgwMu1_tie` | yes | yes | yes | none | `#print axioms pgwMu1_tie` |
| `pgwMu2_mark_before_link` | yes | yes | yes | propext | `#print axioms pgwMu2_mark_before_link` |
| `pgwMu2_pairs` | yes | yes | yes | propext | `#print axioms pgwMu2_pairs` |
| `pgwRead_count` | yes | yes | yes | none | `#print axioms pgwRead_count` |
| `pgwRead_table` | yes | yes | yes | none | `#print axioms pgwRead_table` |
| `pgwRuled_outside` | yes | yes | yes | propext | `#print axioms pgwRuled_outside` |
| `pgwThree_outside` | yes | yes | yes | propext | `#print axioms pgwThree_outside` |
- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-responder-in-lean.py`

- file: [checks/independent/pgw-responder-in-lean.py](../../../checks/independent/pgw-responder-in-lean.py)
- sha256 (`bytes`): `23babf8927ee4cee051a24a80fbb07083ecb5d8dcb295ae9cf9a71285b7f9232`
- cited in: record TFQ-0496
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0496_responder_in_lean.md`

- file: [dag/derivations/02_genesis/tfq_0496_responder_in_lean.md](../../../dag/derivations/02_genesis/tfq_0496_responder_in_lean.md)
- sha256 (`lf-normalised`): `227f1e7afee5e52241c5f5c516f986a7897794efa6912d1a6ecd0058ee6fbc28`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0496
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-responder-in-lean.md`

- file: [dag/derivations/independent/pgw-responder-in-lean.md](../../../dag/derivations/independent/pgw-responder-in-lean.md)
- sha256 (`lf-normalised`): `d63878b869ecd1fab7e1f777254c1c7a6b2669ae79c24923cc0ad8966dd6808c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-responder-in-lean_lean_replay.json`

- file: [dag/research/campaign_pgw-responder-in-lean_lean_replay.json](../../../dag/research/campaign_pgw-responder-in-lean_lean_replay.json)
- sha256 (`lf-normalised`): `b66ab92285e675acab3502a573c93095d9c8935255e46791c22ce4820c98d23b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::min_responses`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs::min_responses`

## Absences recorded by the TFQ records

- TFQ-0496 lean4: sealed responder minimum, cost and tie in the second derivation's packages (S-3)

## Routes

Incoming (1):

- `PGW-R-RESPONDER-IN-LEAN` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION), [PGW-K-ITEM-DELTA-GRAMMAR](PGW-K-ITEM-DELTA-GRAMMAR.md) (OPEN)

Outgoing (0):

