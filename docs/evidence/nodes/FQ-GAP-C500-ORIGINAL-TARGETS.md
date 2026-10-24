# FQ-GAP-C500-ORIGINAL-TARGETS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed census, status left OPEN: the gap register sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml has ten entries GAP-C500-B01 through GAP-C500-B10 in that order. Each title is C500 Block NN original target contract remains open, with NN the two-digit index from 01 through 10. Each status field is RESOLVED_WITH_SCOPED_EVIDENCE and each resolution field is RESOLVED. Each entry lists 25 targets, and those targets run from C500-T301 through C500-T550, 250 targets in all. The open_or_invalid_bet_clauses lists are B01 empty, B02 M2 M5, B03 M1 M3 M5 J2, B04 M3 M5, B05 M2 M5 M6 J2, B06 M5, B07 M6, B08 M6, B09 M6, and B10 M2 M5 M7 J1 J2. Those lists have lengths 0, 2, 4, 2, 4, 1, 1, 1, 1, and 5, and the lengths sum to 21. The Block 09 description contains the text x^4-6*x^2+5. For the integer polynomial n^4 - 6*n^2 + 5, the value at 1 is 0, the value at -1 is 0, and 5*5 - 6*5 + 5 = 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This census records the ten block titles, the status field RESOLVED_WITH_SCOPED_EVIDENCE, the resolution field RESOLVED, the 250 target ids, and the clause lists. It leaves the original target contracts, the named evidence files, and any real-number reading of the spectrum text untouched. A clause list is not a derivation that a bet is invalid, and a receipt is not a derivation. The title sentence is a different sentence from the status field. Status stays OPEN.

## Source status

GAP-C500-B01..B10 RESOLVED_WITH_SCOPED_EVIDENCE: "original target contract remains open"

## Review

- PFP review: [dag/results/FQ-GAP-C500-ORIGINAL-TARGETS/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-GAP-C500-ORIGINAL-TARGETS/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `OPEN`; qualifies for E4: yes.
  - narrowest claim: The examined records do not discharge the original contracts; their scoped labels and partial evidence are retained without promotion.
  - does not support: Original campaign completion, independent rerun of every cited finite computation, historical freeze certification, or proof that any open target is false.
  - next test: Compare every original target/clause row to raw bound sources and challenge omissions or status promotion.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFqGapC500Blocks.lean`

- file: [lean4/CampaignFqGapC500Blocks.lean](../../../lean4/CampaignFqGapC500Blocks.lean)
- sha256 (`bytes`): `c62beca8381b733facbb47a957f171488cdcc26f64ebfb0e92e921916c0bc035`
- cited in: node.lean, node.source, receipt dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json (CampaignFqGapC500Blocks), record TFQ-1025
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json](../../../dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json) (module `CampaignFqGapC500Blocks`): recorded sha256 `c62beca8381b733facbb47a957f171488cdcc26f64ebfb0e92e921916c0bc035` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFqGapC500Blocks`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `c500_block01_clauses` | yes | yes | yes | none | `#print axioms c500_block01_clauses` |
| `c500_block10_clauses` | yes | yes | yes | none | `#print axioms c500_block10_clauses` |
| `c500_block10_length` | yes | yes | yes | none | `#print axioms c500_block10_length` |
| `c500_block_count` | yes | yes | yes | none | `#print axioms c500_block_count` |
| `c500_clause_sum` | yes | yes | yes | none | `#print axioms c500_clause_sum` |
| `c500_target_last` | yes | yes | yes | none | `#print axioms c500_target_last` |
| `c500_target_product` | yes | yes | yes | none | `#print axioms c500_target_product` |
| `ising_poly_neg_one` | yes | yes | yes | none | `#print axioms ising_poly_neg_one` |
| `ising_poly_on_square_five` | yes | yes | yes | none | `#print axioms ising_poly_on_square_five` |
| `ising_poly_one` | yes | yes | yes | none | `#print axioms ising_poly_one` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1025
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_gap_c500_ten_blocks_and_custody_axiom_audit_certificate` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_c500_ten_blocks_and_custody_axiom_audit_certificate` |
| `QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1025
- counts toward the grade: no

### Python: `checks/independent/fq-gap-c500-original-targets.py`

- file: [checks/independent/fq-gap-c500-original-targets.py](../../../checks/independent/fq-gap-c500-original-targets.py)
- sha256 (`bytes`): `95eeb78403e80e94edb733ce28df122bfbb9f38654b00c96b2c68655188a2c03`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md](../../../dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md)
- sha256 (`lf-normalised`): `e5a1eaa6c722e2f1ee391d4d15f70677988960e756f4d9cbaee30a90ce1b8b8b`
- generated view: listed, not counted
- cited in: record TFQ-1025
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fq-gap-c500-original-targets.md`

- file: [dag/derivations/independent/fq-gap-c500-original-targets.md](../../../dag/derivations/independent/fq-gap-c500-original-targets.md)
- sha256 (`lf-normalised`): `b4bb038fa94d5873b6ae9a859b72e843e2a27a53bebbb21e867e6ee14fed04b0`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json`

- file: [dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json](../../../dag/research/campaign_fq-gap-c500-original-targets_lean_replay.json)
- sha256 (`lf-normalised`): `14d167514a3e04cbb5a28a5c9919abdae81ed1a1398398c8eed312f2f7d0dab2`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (0):


Outgoing (0):


No incoming route.
