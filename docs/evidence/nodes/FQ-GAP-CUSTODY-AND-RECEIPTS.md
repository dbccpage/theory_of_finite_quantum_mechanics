# FQ-GAP-CUSTODY-AND-RECEIPTS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Receipt and custody items: 48 (ledger) vs 24 (GAP-FQM-002 text) untyped claim rows; GAP-FQM-017 QM_208-211 claim maps point at nonexistent *_lib libraries (tautology tests); GAP-FQM-019 eight claims need a Mathlib build to promote; GAP-FQM-020 QM_122 axiom report covers 22 of 53 files and hides a Classical.choice dependency (H019.basisGen8_eval_pos); GAP-FQM-022 QM_122 provenance cites nonexistent sources; QM_020 and QM_080 are published (Zenodo) and not free to rewrite; README states the code-companion --check fails on the current tree.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Receipts are not proofs: a stale receipt over H000..H018 coexists with Lean headers that say "Candidate only"; replay against a clean Lean build is not claimed.

## Source status

gap_register GAP-FQM-002/003/004/006..010/012/014/017/019/020/022 (statuses absent or stale in several)

## Review

- PFP review: [dag/results/FQ-GAP-CUSTODY-AND-RECEIPTS/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-GAP-CUSTODY-AND-RECEIPTS/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `OPEN`; qualifies for E4: yes.
  - narrowest claim: Every retained available source is bound to actual bytes; unavailable or changed historical pins remain explicit. Fresh named Lean reports cover only the declarations listed in this run, not an H000-H053 campaign.
  - does not support: Resolve the original claim-row discrepancies, missing-library maps, publication/provenance corrections and full original axiom/build receipts individually. This scoped inventory does not discharge the historical custody register.
  - next test: Resolve the original claim-row discrepancies, missing-library maps, publication/provenance corrections and full original axiom/build receipts individually. This scoped inventory does not discharge the historical custody register.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1023
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_gap_c500_ten_blocks_and_custody_axiom_audit_certificate` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_c500_ten_blocks_and_custody_axiom_audit_certificate` |
| `QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1023
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1023_fq_gap_custody_and_receipts.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1023_fq_gap_custody_and_receipts.md](../../../dag/derivations/10_finite_qm_core/tfq_1023_fq_gap_custody_and_receipts.md)
- sha256 (`lf-normalised`): `dbe610031d0d821f961eaee542acfd34b1499fcef6b8c8b80c1bc7983aa4a0c0`
- generated view: listed, not counted
- cited in: record TFQ-1023
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (0):


Outgoing (0):


No incoming route.
