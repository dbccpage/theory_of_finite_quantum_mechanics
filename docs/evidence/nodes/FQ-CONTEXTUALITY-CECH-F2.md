# FQ-CONTEXTUALITY-CECH-F2

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Over F2 the cochain complex of a finite measurement scenario satisfies d1 d0 = 0. The Cabello scenario X1 has no global section. No +/-1 assignment of the Mermin-Peres square has all row products +1 and column products +1, +1, -1.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_not_current`: lean4/DualWitness.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

- declared measurement scenarios and contexts (assumption)

## Bottleneck

In Lean: d1 d0 = 0 for every finite scenario (differential_squares_to_zero), no global section for the Cabello scenario X1 (x1_has_no_global_section), and the Mermin-Peres parity contradiction (mermin_peres_parity_obstruction). The Peres-Mermin incidence rank 8 is a native exact computation and is not part of this statement.

## Source status

paper s13.8.3; ContextualityObstruction.lean compiles a d0^2=0 cochain complex and no-global-section witnesses

## Review

- PFP review: [dag/results/FQ-CONTEXTUALITY-CECH-F2/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-CONTEXTUALITY-CECH-F2/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Two explicit degree-two parity covers and a genuine global-section control, exact matrices/ranks and literal source kernel parity/differential signatures.
  - does not support: Conflation of incidence rank with overlap rank, general sheaf equivalence, a kernel proof of the native rank outputs, or physical reconstruction.
  - next test: Challenge a matrix entry, rank, discrepancy, annihilator or global section and preserve actual coordinate maps.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ContextualityObstruction.lean`

- file: [lean4/ContextualityObstruction.lean](../../../lean4/ContextualityObstruction.lean)
- sha256 (`bytes`): `712a6a817e5b6991910e8e6ed1a394997262e62b71fc89908426866e60773627`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `ContextualityObstruction`): recorded sha256 `712a6a817e5b6991910e8e6ed1a394997262e62b71fc89908426866e60773627` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ContextualityObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `differential_squares_to_zero` | yes | yes | yes | propext | `#print axioms differential_squares_to_zero` |
| `x1_has_no_global_section` | yes | yes | yes | Quot.sound, propext | `#print axioms x1_has_no_global_section` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: record TFQ-0250 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`
- counts toward the grade: no

### Lean: `lean4/DualWitness.lean`

- file: [lean4/DualWitness.lean](../../../lean4/DualWitness.lean)
- sha256 (`bytes`): `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7`
- cited in: node.lean
- replay: `failed`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DualWitness`): recorded sha256 `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: no; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build DualWitness`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mermin_peres_parity_obstruction` | yes | yes | yes | - | `#print axioms mermin_peres_parity_obstruction` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/contextuality_obstruction.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/contextuality_obstruction.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/parity_context_packet.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/parity_context_packet.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0250_mermin_peres_contextuality_on_a_finite_cochain.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0250_mermin_peres_contextuality_on_a_finite_cochain.md](../../../dag/derivations/12_finite_qm_structure/tfq_0250_mermin_peres_contextuality_on_a_finite_cochain.md)
- sha256 (`lf-normalised`): `557a53d1afb9d856952c871b81e9a733c8e8224a6a47012fac461759b0f157c9`
- generated view: listed, not counted
- cited in: record TFQ-0250 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0250 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0250 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/kochen_specker.rs

## Routes

Incoming (1):

- `FQ-R-CONTEXTUALITY` `DERIVED_LEAN`: [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN), [FQ-CABELLO-NO-INTEGER-FRAME](FQ-CABELLO-NO-INTEGER-FRAME.md) (PROVED_LEAN)

Outgoing (1):

- `DS-R-MERMIN-PERES-F2` `DERIVED_LEAN`: [DS-QM120-MERMIN-PERES-F2-OBSTRUCTION](DS-QM120-MERMIN-PERES-F2-OBSTRUCTION.md) (PROVED_LEAN)
