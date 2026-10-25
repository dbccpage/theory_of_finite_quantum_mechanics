# FQ-POSITIVE-WEIGHTS-ADMITTED

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Positive normalized L1 weights on preparations are additional carrier data; a bare distinction relation does not supply them. Every finite Bell/CHSH statement below takes them as given.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- positive normalized preparation weights (assumption)

## Bottleneck

Derive positivity and normalization from native histories; this is the first derivation target the paper names (Source Notes s6 / s13.9).

## Source status

paper s13.8.2 table: "positivity and normalized preparation weights are admitted data"

## Review

- PFP review: [dag/results/FQ-POSITIVE-WEIGHTS-ADMITTED/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-POSITIVE-WEIGHTS-ADMITTED/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: The general two-weight rational convex bound is proved with explicit nonnegativity and score bounds; distinct positive normalized preparations, a signed violation and an unnormalized scaled control are checked.
  - does not support: Derive a preparation measure from native histories with a stated selection principle. Same-carrier examples only show insufficiency of that bare carrier; no stronger impossibility theorem is claimed.
  - next test: Derive a preparation measure from native histories with a stated selection principle. Same-carrier examples only show insufficiency of that bare carrier; no stronger impossibility theorem is claimed.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1008
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1008
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1008_fq_positive_weights_admitted.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1008_fq_positive_weights_admitted.md](../../../dag/derivations/10_finite_qm_core/tfq_1008_fq_positive_weights_admitted.md)
- sha256 (`lf-normalised`): `6dfcea8291152b1f78e148bf6c0c00ad04d90719394aaab127fd60e90ec6f096`
- generated view: listed, not counted
- cited in: record TFQ-1008
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `X-R-WEIGHTS-DECLARED-TO-FQ-POSITIVE-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)

Outgoing (2):

- `FQ-R-BELL-CLASSICAL` `DERIVED_LEAN`: [FQ-BELL-CLASSICAL-JOINT-EXTENSION](FQ-BELL-CLASSICAL-JOINT-EXTENSION.md) (PROVED_LEAN)
- `FQ-R-GAP-PRIM-TO-INTERFACE` `GAP_NO_DERIVATION`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)
