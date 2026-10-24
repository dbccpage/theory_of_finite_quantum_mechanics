# FQ-GAP-CORPUS-REWRITE

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The whole-program QM rewrite is not complete; the consolidation narrows its scope without discharging it.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Complete or retire the rewrite; no derivation content.

## Source status

GAP-F001-S000-003 (book lifecycle admission); deferred tag in book README

## Review

- PFP review: [dag/results/FQ-GAP-CORPUS-REWRITE/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-GAP-CORPUS-REWRITE/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `OPEN`; qualifies for E4: yes.
  - narrowest claim: The captured source scope is inventoried with exact byte/newline/literal counts and cryptographic source custody; a proper subset cannot discharge a missing obligation.
  - does not support: Create a claim-by-claim whole-corpus rewrite/retirement ledger with original exit contracts and independently checked content; captured filenames and constant flags cannot supply it.
  - next test: Create a claim-by-claim whole-corpus rewrite/retirement ledger with original exit contracts and independently checked content; captured filenames and constant flags cannot supply it.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1024
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
- cited in: node.rust, record TFQ-1024
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1024_fq_gap_corpus_rewrite.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1024_fq_gap_corpus_rewrite.md](../../../dag/derivations/10_finite_qm_core/tfq_1024_fq_gap_corpus_rewrite.md)
- sha256 (`lf-normalised`): `65797e426e00d18ddfde5cbe8ab564c01dcd2bbae6de5a6ab6e2e126a7043ef3`
- generated view: listed, not counted
- cited in: record TFQ-1024
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (0):


Outgoing (0):


No incoming route.
