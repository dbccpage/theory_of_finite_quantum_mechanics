# FQ-GAP-C500-ORIGINAL-TARGETS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For each of ten C500 blocks the original target contract remains open; closure is recorded only for a scoped statement backed by evidence files (open or invalid bet clauses listed per block, e.g. M2, M5, M7, J1, J2 in Block 10).

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

Scoped resolution is narrower than the original targets; map per-block clauses before citing any C500 target as discharged.

## Source status

GAP-C500-B01..B10 RESOLVED_WITH_SCOPED_EVIDENCE: "original target contract remains open"

## Review

- PFP review: [dag/results/FQ-GAP-C500-ORIGINAL-TARGETS/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-GAP-C500-ORIGINAL-TARGETS/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `OPEN`; qualifies for E4: yes.
  - narrowest claim: The examined records do not discharge the original contracts; their scoped labels and partial evidence are retained without promotion.
  - does not support: Original campaign completion, independent rerun of every cited finite computation, historical freeze certification, or proof that any open target is false.
  - next test: Compare every original target/clause row to raw bound sources and challenge omissions or status promotion.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1025
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
- cited in: node.rust, record TFQ-1025
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md](../../../dag/derivations/10_finite_qm_core/tfq_1025_fq_gap_c500_original_targets.md)
- sha256 (`lf-normalised`): `3832a023cbc510b1e21155da57f5c11b4a0cb16a15bfb0efde6d798cab8a2453`
- generated view: listed, not counted
- cited in: record TFQ-1025
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
