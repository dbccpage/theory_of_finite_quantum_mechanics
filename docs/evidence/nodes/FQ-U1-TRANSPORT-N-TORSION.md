# FQ-U1-TRANSPORT-N-TORSION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual finite graph gauge normal forms, relative path phase and N² orbit-invariant counts are exact; cycle identities over ZMod n and pair-cardinality arithmetic are kernel checked.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- non-triviality and order N of the edge phase cochain (assumption)
- finite oriented graph (assumption)

## Bottleneck

Unmet after the PFP review: Prove full graph gauge-orbit classification and the cyclotomic mu_N embedding/order hypotheses for arbitrary graphs/N; no continuous circle or topological connectedness is derived. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Z_N cycle holonomy gauge invariance and exponent-2 vs Z_3/Z_4 separation mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/FQ-U1-TRANSPORT-N-TORSION/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/FQ-U1-TRANSPORT-N-TORSION/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual finite graph gauge normal forms, relative path phase and N² orbit-invariant counts are exact; cycle identities over ZMod n and pair-cardinality arithmetic are kernel checked.
  - does not support: Prove full graph gauge-orbit classification and the cyclotomic mu_N embedding/order hypotheses for arbitrary graphs/N; no continuous circle or topological connectedness is derived.
  - next test: Prove full graph gauge-orbit classification and the cyclotomic mu_N embedding/order hypotheses for arbitrary graphs/N; no continuous circle or topological connectedness is derived.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_u1_transport_n_torsion_and_sign_separation` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_u1_transport_n_torsion_and_sign_separation` |
- counts toward the grade: yes

### Lean: `lean4/H011Circle.lean`

- file: [lean4/H011Circle.lean](../../../lean4/H011Circle.lean)
- sha256 (`bytes`): `6934713287756fd23f2f44a6bab2ed6ee50fbb128f99db492f926c839ff86d9b`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H011Circle`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sign_fails_connectedness_shadow` | yes | yes | yes | - | `#print axioms sign_fails_connectedness_shadow` |
- counts toward the grade: yes

### Lean: `lean4/H011U1SelectorBoundary.lean`

- file: [lean4/H011U1SelectorBoundary.lean](../../../lean4/H011U1SelectorBoundary.lean)
- sha256 (`bytes`): `214f187afdfc0ee196021aa3ce2ab96875b1c13de9b3a560ef1eaf0359622912`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H011U1SelectorBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `u1_selector_boundary` | yes | yes | yes | - | `#print axioms u1_selector_boundary` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/holonomy_interference.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/holonomy_interference.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/u1_graph_connection.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/u1_graph_connection.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md`

- file: [dag/derivations/14_finite_gauge/tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md](../../../dag/derivations/14_finite_gauge/tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md)
- sha256 (`lf-normalised`): `3b89d84355253adb91b6cab1ff8de82e84c48bea6adc7e49603890463649038b`
- generated view: listed, not counted
- cited in: record TFQ-0053 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0054_each_language_must_carry_pure_gauge_iff_every_off_forest_edge_is_1.md`

- file: [dag/derivations/14_finite_gauge/tfq_0054_each_language_must_carry_pure_gauge_iff_every_off_forest_edge_is_1.md](../../../dag/derivations/14_finite_gauge/tfq_0054_each_language_must_carry_pure_gauge_iff_every_off_forest_edge_is_1.md)
- sha256 (`lf-normalised`): `bec1ff23684877868f7c92f7a5a339d288796a72cf8e04e3c4fb96610dd8206f`
- generated view: listed, not counted
- cited in: record TFQ-0054 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md`

- file: [dag/derivations/15_finite_qed/tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md](../../../dag/derivations/15_finite_qed/tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md)
- sha256 (`lf-normalised`): `cc30729fc06fba14ad3a2eb0b87d1af117d3864925ef95ab2f9043aa112cabca`
- generated view: listed, not counted
- cited in: record TFQ-0057 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0053 lean4: not located
- TFQ-0053 python: not located
- TFQ-0053 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/u1_graph_connection.rs
- TFQ-0054 lean4: not located
- TFQ-0054 python: not located
- TFQ-0054 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/u1_gauge_triviality.rs
- TFQ-0057 lean4: not located
- TFQ-0057 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/dirac_ward_takahashi_control.py
- TFQ-0057 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs

## Routes

Incoming (1):

- `FQ-R-U1` `DERIVED_LEAN`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION), [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN)

Outgoing (1):

- `FQ-R-GAP-U1` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-U1-CIRCLE](FQ-GAP-U1-CIRCLE.md) (CONDITIONAL)
