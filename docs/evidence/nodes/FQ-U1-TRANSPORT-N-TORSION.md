# FQ-U1-TRANSPORT-N-TORSION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> N-torsion edge 1-cochain tau with values in mu_N in Q(zeta_N)^x: gauge classes Hom(H_1(G,Z), mu_N) have size N^{beta_1(G)}; relative report phase equals path holonomy tau(p1)tau(p2)^-1. Sign group {+1,-1} fails connectedness under "not exponent two"; Gaussian units and three-cycle meet it.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- non-triviality and order N of the edge phase cochain (assumption)
- finite oriented graph (assumption)

## Bottleneck

Lean states gauge invariance of a triangle holonomy modulo N and small modular facts. The count N^beta_1(G) of gauge classes and the holonomy identity on general graphs are native exact checks on declared graphs, not Lean.

## Source status

Z_N cycle holonomy gauge invariance and exponent-2 vs Z_3/Z_4 separation mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/FQ-U1-TRANSPORT-N-TORSION/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/FQ-U1-TRANSPORT-N-TORSION/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual finite graph gauge normal forms, relative path phase and N² orbit-invariant counts are exact; cycle identities over ZMod n and pair-cardinality arithmetic are kernel checked.
  - does not support: Prove full graph gauge-orbit classification and the cyclotomic mu_N embedding/order hypotheses for arbitrary graphs/N; no continuous circle or topological connectedness is derived.
  - next test: Prove full graph gauge-orbit classification and the cyclotomic mu_N embedding/order hypotheses for arbitrary graphs/N; no continuous circle or topological connectedness is derived.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_u1_transport_n_torsion_and_sign_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_u1_transport_n_torsion_and_sign_separation` |

- counts toward the grade: yes

### Lean: `lean4/HilbertWalkCircle.lean`

- file: [lean4/HilbertWalkCircle.lean](../../../lean4/HilbertWalkCircle.lean)
- sha256 (`bytes`): `c3326f87aa656cbec551fc23ecf89675379ae738888b497b8ecc3c748093acfa`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `HilbertWalkCircle`): recorded sha256 `c3326f87aa656cbec551fc23ecf89675379ae738888b497b8ecc3c748093acfa` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkCircle`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sign_fails_connectedness_shadow` | yes | yes | yes | none | `#print axioms sign_fails_connectedness_shadow` |

- counts toward the grade: yes

### Lean: `lean4/U1SelectorBoundary.lean`

- file: [lean4/U1SelectorBoundary.lean](../../../lean4/U1SelectorBoundary.lean)
- sha256 (`bytes`): `003d1730941ba102f39cdd82a0f647131050d93ef99d3e532c49e2a873a2376a`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `U1SelectorBoundary`): recorded sha256 `003d1730941ba102f39cdd82a0f647131050d93ef99d3e532c49e2a873a2376a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build U1SelectorBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `u1_selector_boundary` | yes | yes | yes | none | `#print axioms u1_selector_boundary` |

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

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
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
- TFQ-0057 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/dirac_ward_takahashi_control.py
- TFQ-0057 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs

## Routes

Incoming (1):

- `FQ-R-U1` `COMPUTED`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION), [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN)

Outgoing (1):

- `FQ-R-GAP-U1` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-U1-CIRCLE](FQ-GAP-U1-CIRCLE.md) (CONDITIONAL)
