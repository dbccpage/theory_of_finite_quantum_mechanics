# FQ-GAP-CUSTODY-AND-RECEIPTS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed census, status left OPEN: the claims list in sources/atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml, stopping before application_claims, has 834 records of 14 type labels. In descending count the pairs are FINITE COMPUTATION 160, SCOPE FENCE 156, OPEN 115, DEFINITION 104, EXACT FINITE ALGEBRA 80, CONDITIONAL 57, UNTYPED 48, ASSERTED 36, REFUTED BY AUDIT 31, DECLARED 17, FINITE FIXTURE 12, REFUTED BY COMPUTATION 10, REFUSAL 7, and PARTIAL 1. Those counts sum to 834. Index 6 of that order is UNTYPED with count 48. 48 ≠ 24 and 834 ≠ 189. The gap register entry GAP-FQM-002 has the title 24 claim rows carry no parseable type, and its description contains 24 of 189.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declarations covered by a current replay receipt: 8
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This census is a type-label count of one claims list. It leaves GAP-FQM-017, GAP-FQM-019, GAP-FQM-020, GAP-FQM-022, Zenodo publication, and the README code-companion check untouched. A type-label count is not a derivation that a row is unsupported, and a receipt is not a derivation. The gap sentence 24 of 189 is a different sentence from the current 48 of 834. Status stays OPEN.

## Source status

gap_register GAP-FQM-002/003/004/006..010/012/014/017/019/020/022 (statuses absent or stale in several)

## Review

- PFP review: [dag/results/FQ-GAP-CUSTODY-AND-RECEIPTS/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-GAP-CUSTODY-AND-RECEIPTS/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `OPEN`; qualifies for E4: yes.
  - narrowest claim: Every retained available source is bound to actual bytes; unavailable or changed historical pins remain explicit. Fresh named Lean reports cover only the declarations listed in this run, not an H000-H053 campaign.
  - does not support: Resolve the original claim-row discrepancies, missing-library maps, publication/provenance corrections and full original axiom/build receipts individually. This scoped inventory does not discharge the historical custody register.
  - next test: Resolve the original claim-row discrepancies, missing-library maps, publication/provenance corrections and full original axiom/build receipts individually. This scoped inventory does not discharge the historical custody register.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFqGapCustodyReceipts.lean`

- file: [lean4/CampaignFqGapCustodyReceipts.lean](../../../lean4/CampaignFqGapCustodyReceipts.lean)
- sha256 (`bytes`): `709339f2ed7e14d2517469b93f774efade7f7210257fb3fdaa3c4b742154a6e7`
- cited in: node.lean, node.source, receipt dag/research/campaign_fq-gap-custody-and-receipts_lean_replay.json (CampaignFqGapCustodyReceipts), record TFQ-1023
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-custody-and-receipts_lean_replay.json](../../../dag/research/campaign_fq-gap-custody-and-receipts_lean_replay.json) (module `CampaignFqGapCustodyReceipts`): recorded sha256 `709339f2ed7e14d2517469b93f774efade7f7210257fb3fdaa3c4b742154a6e7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFqGapCustodyReceipts`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `census_length` | yes | yes | yes | none | `#print axioms census_length` |
| `census_sum_eq` | yes | yes | yes | none | `#print axioms census_sum_eq` |
| `ledger_rows_ne_gap_text` | yes | yes | yes | none | `#print axioms ledger_rows_ne_gap_text` |
| `ledger_untyped_ne_gap_text` | yes | yes | yes | none | `#print axioms ledger_untyped_ne_gap_text` |
| `one_untyped_label` | yes | yes | yes | none | `#print axioms one_untyped_label` |
| `untyped_row` | yes | yes | yes | none | `#print axioms untyped_row` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1023
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
- cited in: node.rust, record TFQ-1023
- counts toward the grade: no

### Python: `checks/independent/fq-gap-custody-and-receipts.py`

- file: [checks/independent/fq-gap-custody-and-receipts.py](../../../checks/independent/fq-gap-custody-and-receipts.py)
- sha256 (`bytes`): `17dce6b20b7163eabea37a4a7708759fdeecbb3af9ed56ec831c4d0771df3671`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1023_fq_gap_custody_and_receipts.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1023_fq_gap_custody_and_receipts.md](../../../dag/derivations/10_finite_qm_core/tfq_1023_fq_gap_custody_and_receipts.md)
- sha256 (`lf-normalised`): `5438be1db06ee013696567f182bb20c7d76b1ede176d2e25bb7e66d6385e7a12`
- generated view: listed, not counted
- cited in: record TFQ-1023
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fq-gap-custody-and-receipts.md`

- file: [dag/derivations/independent/fq-gap-custody-and-receipts.md](../../../dag/derivations/independent/fq-gap-custody-and-receipts.md)
- sha256 (`lf-normalised`): `79fc3fcd4921c85beea7fe9609072e2bc7f0d5dfccba972ba4d680154fe276bb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fq-gap-custody-and-receipts_lean_replay.json`

- file: [dag/research/campaign_fq-gap-custody-and-receipts_lean_replay.json](../../../dag/research/campaign_fq-gap-custody-and-receipts_lean_replay.json)
- sha256 (`lf-normalised`): `ff2f9de91c32520dcbc4315bac15cf7abfaade2a2b85e53e110f2e7126f9ea79`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml)
- sha256 (`lf-normalised`): `9db8daae54ec82cab13d7f63cd24d21a793017302b9e8553255fe0c64881f4c7`
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
