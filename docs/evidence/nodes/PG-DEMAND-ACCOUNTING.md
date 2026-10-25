# PG-DEMAND-ACCOUNTING

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For finite sets, |(W minus D) union B| = |W| - |D| + |B| (integer arithmetic) holds when D is a subset of W and the births B avoid the survivors W minus D (births may coincide with discharged elements); in general the identity holds iff |D minus W| = |(W minus D) cap B|, so exactly one violated hypothesis always breaks it and both violated hypotheses can cancel; natural-number truncation can mask a violated subset hypothesis; the identity imposes no constraint on a sequence of counts (the displayed survivor sequence is a chosen ledger example). Proved for Finsets; the list-register readings of Paper.lean and Paper001.lean are not re-proved beyond the filter-based length and Nodup statements.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 17
- cited Lean declaration references covered by a current replay receipt: 17
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/DemandAccounting.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

None recorded.

## Bottleneck

The engine wrapper over preservation.demand_step is not connected; the identification of the active count with the cumulative history is not addressed.

## Source status

Proposition 3 - finite demand accounting (WDP-P001-002 proved)

## Review

- PFP review: [dag/results/PG-DEMAND-ACCOUNTING/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/PG-DEMAND-ACCOUNTING/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: For finite sets, \|(W minus D) union B\| = \|W\| - \|D\| + \|B\| holds when D is inside W and the births avoid W minus D (births may coincide with discharged elements), it fails whenever exactly one of the two hypotheses is violated; when both are violated it holds if and only if \|D minus W\| = \|(W minus D) cap B\| (exact cancellation); and it imposes no constraint on a sequence of counts.
  - does not support: Which demands an engine actually carries; any claim that the displayed survivor sequence (0,1,1,1,0,1,1) is a native or general law (the source itself calls it a chosen ledger example); the preservation.py demand_step frozenset reading and any Python or Rust wrapper over it; multiset or ordered-log registers as a state beyond the filter-based list register of Paper.lean (the erase-based removeAll register of Paper001.lean is not re-proved, and the Nodup conjunct of that List Nat statement is only matched by the filter-based list_register_nodup_iff and the native census); the identification of the active count s_n with the cumulative history \|H_n\|; universes of more than five elements; any physical or thermodynamic interpretation.
  - next test: Supply the missing count wrapper over preservation.demand_step of the opened preservation.py: show that the frozenset next-active set it returns equals the Finset (W minus D) union B of this model, carry the two hypotheses as typed fields of the wrapper, and replay the identity on the wrapper actual outputs.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DemandAccounting.lean`

- file: [lean4/DemandAccounting.lean](../../../lean4/DemandAccounting.lean)
- sha256 (`bytes`): `caa7cae003a1790f98cbc16d56af7ee2d50116c8d2b56b3c5d734da5185ec14c`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (DemandAccounting)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `DemandAccounting`): recorded sha256 `caa7cae003a1790f98cbc16d56af7ee2d50116c8d2b56b3c5d734da5185ec14c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DemandAccounting`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DemandAccounting.card_next_exact` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.card_next_exact` |
| `DemandAccounting.demand_accounting` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.demand_accounting` |
| `DemandAccounting.every_step_is_an_accounting` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.every_step_is_an_accounting` |
| `DemandAccounting.fails_of_excess_without_overlap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.fails_of_excess_without_overlap` |
| `DemandAccounting.fails_without_disjoint` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.fails_without_disjoint` |
| `DemandAccounting.fails_without_subset` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.fails_without_subset` |
| `DemandAccounting.formula_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.formula_iff` |
| `DemandAccounting.holds_accidentally_without_hypotheses` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.holds_accidentally_without_hypotheses` |
| `DemandAccounting.list_length_no_disjointness` | yes | yes | yes | Quot.sound, propext | `#print axioms DemandAccounting.list_length_no_disjointness` |
| `DemandAccounting.list_overlap_not_nodup` | yes | yes | yes | none | `#print axioms DemandAccounting.list_overlap_not_nodup` |
| `DemandAccounting.list_register_nodup_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms DemandAccounting.list_register_nodup_iff` |
| `DemandAccounting.nat_truncation_masks_subset_violation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.nat_truncation_masks_subset_violation` |
| `DemandAccounting.single_violation_fails` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.single_violation_fails` |
| `DemandAccounting.split_not_determined` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DemandAccounting.split_not_determined` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition` |

- counts toward the grade: yes

### Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean`

- file: [lean4/Imported/PreGenesisToMssn/Paper.lean](../../../lean4/Imported/PreGenesisToMssn/Paper.lean)
- sha256 (`bytes`): `5f0ebfc1710b91ce84d4570d7653a3cb8396824adecfaba16fa59a96354b9e12`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Paper`): recorded sha256 `5f0ebfc1710b91ce84d4570d7653a3cb8396824adecfaba16fa59a96354b9e12` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Paper.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `demand_accounting` | yes | yes | yes | Quot.sound, propext | `#print axioms demand_accounting` |

- counts toward the grade: yes

### Lean: `lean4/Imported/SnMssn/Paper001.lean`

- file: [lean4/Imported/SnMssn/Paper001.lean](../../../lean4/Imported/SnMssn/Paper001.lean)
- sha256 (`bytes`): `1a79ddc7a70157834ee80ed3890124aadd149093336ac49776eab3c167b4fb07`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.SnMssn.Paper001`): recorded sha256 `1a79ddc7a70157834ee80ed3890124aadd149093336ac49776eab3c167b4fb07` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/SnMssn/Paper001.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `demand_accounting` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms demand_accounting` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0369_finite_demand_count.md`

- file: [dag/derivations/01_pregenesis/tfq_0369_finite_demand_count.md](../../../dag/derivations/01_pregenesis/tfq_0369_finite_demand_count.md)
- sha256 (`lf-normalised`): `fa811925167931ff378c127826335fa5aefcf0549776626bce3a3e4fa67da6b2`
- generated view: listed, not counted
- cited in: record TFQ-0369
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0333_account_finite_demand_by_s_next_s_d_b_only.md`

- file: [dag/derivations/05_mssn_sn/tfq_0333_account_finite_demand_by_s_next_s_d_b_only.md](../../../dag/derivations/05_mssn_sn/tfq_0333_account_finite_demand_by_s_next_s_d_b_only.md)
- sha256 (`lf-normalised`): `e9332de8aad7a06986b36302ebc06117983e8bb231b14aa925897666c6d96560`
- generated view: listed, not counted
- cited in: record TFQ-0333
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/paper_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/paper_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0333 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean
- TFQ-0333 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py
- TFQ-0369 lean4: declaration obligation: demand_accounting, hypotheses kept in the statement rather than dropped
- TFQ-0369 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean
- TFQ-0369 python: missing obligation: a count wrapper around demand_step that states s_next = s - d + b only when discharged is a subset and births are disjoint
- TFQ-0369 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py
- TFQ-0369 rust: missing obligation: the same cardinality step in crate pre_mssn_preservation, with the two hypotheses as fields

## Routes

Incoming (1):

- `PG-R-DEMAND` `DERIVED_LEAN`: [PG-GEN-NO-RETURN](PG-GEN-NO-RETURN.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-COMP-C4-SUPPLY-GROWTH` `DERIVED_LEAN`: [COMP-C4-SUPPLY-GROWTH](COMP-C4-SUPPLY-GROWTH.md) (PROVED_LEAN)
- `PG-R-REFINE` `DERIVED_LEAN`: [PG-REFINE-SEPARATES](PG-REFINE-SEPARATES.md) (PROVED_LEAN)
