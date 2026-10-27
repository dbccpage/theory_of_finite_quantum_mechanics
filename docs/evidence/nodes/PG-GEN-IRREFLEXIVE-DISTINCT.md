# PG-GEN-IRREFLEXIVE-DISTINCT

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the Genesis Ongoing model the two given names are distinct terms (a ≠ b), derived from the irreflexivity constraint on the given assertion arb; bra is independent (bra_not_derived). Irreflexive endpoints are distinct in general (irreflexive_endpoints).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Ban on xrx (assumption: a stated part of the seed)

## Bottleneck

The distinctness rests on the ban on xrx being given; when the ban is struck (17th derivation) it is re-derived only under the obstruction rule.

## Source status

D1 a ≠ b from irreflexive witness; given_distinct

## Review

- PFP review: [dag/results/PG-GEN-IRREFLEXIVE-DISTINCT/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-IRREFLEXIVE-DISTINCT/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: All two-term relation tables are checked, and irreflexive related endpoints are generally distinct in Lean.
  - does not support: Relate the bounded tables to the intended Genesis semantics and retain the irreflexivity premise. No assertion of seed-free distinctness, transitivity or orientation selection is made.
  - next test: Relate the bounded tables to the intended Genesis semantics and retain the irreflexivity premise. No assertion of seed-free distinctness, transitivity or orientation selection is made.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoing/H3V7N5QF/Basic.lean`

- file: [lean4/Imported/GenesisOngoing/H3V7N5QF/Basic.lean](../../../lean4/Imported/GenesisOngoing/H3V7N5QF/Basic.lean)
- sha256 (`bytes`): `50978fb46aab1c496615d69b9345f531cbd2e75e33fd5ea0d16a72be7a90c7de`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.H3V7N5QF.Basic`): recorded sha256 `50978fb46aab1c496615d69b9345f531cbd2e75e33fd5ea0d16a72be7a90c7de` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/H3V7N5QF/Basic.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bra_not_derived` | yes | yes | yes | propext | `#print axioms bra_not_derived` |
| `given_distinct` | yes | yes | yes | none | `#print axioms given_distinct` |

- counts toward the grade: yes

### Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean`

- file: [lean4/Imported/PreGenesisToMssn/Paper.lean](../../../lean4/Imported/PreGenesisToMssn/Paper.lean)
- sha256 (`bytes`): `95b210aaa49b592cff7b6c3c53ec558b3e50cebaae659c3df48b25f5ef48c687`
- cited in: node.lean, node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Paper`): recorded sha256 `95b210aaa49b592cff7b6c3c53ec558b3e50cebaae659c3df48b25f5ef48c687` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Paper.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `irreflexive_endpoints` | yes | yes | yes | none | `#print axioms irreflexive_endpoints` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md)
- sha256 (`lf-normalised`): `34530ca3f714274f7f03a1cd5dffcdd1fb76e50ec20749a03a72956e5f93fd1c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0387_irreflexive_endpoints_distinct.md`

- file: [dag/derivations/02_genesis/tfq_0387_irreflexive_endpoints_distinct.md](../../../dag/derivations/02_genesis/tfq_0387_irreflexive_endpoints_distinct.md)
- sha256 (`lf-normalised`): `e12328e8f3d16a8e45be150107ee684e7b4f0720c6aaa50dd95138ac70d51b51`
- generated view: listed, not counted
- cited in: record TFQ-0387
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0387 lean4: declaration obligation: given_distinct and irreflexive_endpoints, with bra left undecided
- TFQ-0387 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/H3V7N5QF/Basic.lean
- TFQ-0387 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Paper.lean
- TFQ-0387 python: missing obligation: a seed checker under genesis_ongoing/code that accepts arb, rejects xrx, and leaves bra unset
- TFQ-0387 rust: missing obligation: no Rust seed module was listed under genesis_ongoing; the ban on xrx still needs a carrier there or an explicit absence

## Routes

Incoming (1):

- `PG-R-IRREFLEXIVE` `DERIVED_LEAN`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN), [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION)

Outgoing (3):

- `APP-R-COMP-C1-CANONICAL-SEPARATED-ALPHABET` `DERIVED_LEAN`: [COMP-C1-CANONICAL-SEPARATED-ALPHABET](COMP-C1-CANONICAL-SEPARATED-ALPHABET.md) (PROVED_LEAN)
- `PG-R-ONGOING-OBSTRUCTION` `DERIVED_LEAN`: [PG-GEN-ONGOING-OBSTRUCTION](PG-GEN-ONGOING-OBSTRUCTION.md) (PROVED_LEAN)
- `PGW-R-D2-INITIAL-POINTED` `DERIVED_LEAN`: [PGW-D2-INITIAL-POINTED](PGW-D2-INITIAL-POINTED.md) (PROVED_LEAN)
