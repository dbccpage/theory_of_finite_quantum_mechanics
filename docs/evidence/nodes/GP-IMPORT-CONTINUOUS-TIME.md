# GP-IMPORT-CONTINUOUS-TIME

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Continuous time, topology, a one-parameter unitary group and Stone's theorem. The two-state toggle has no report-level square root; after complex coefficients, interpolants exist at scale 4 and are not unique.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuous time: assumption
- topology on the carrier: assumption
- one-parameter group: assumption
- Stone's theorem: import

## Bottleneck

Finite substitutes: exact rational Cayley transform in SO(8,Q); hyperoctahedral signed permutations with irreversible monotone residue.

## Source status

imported / refused on this host

## Review

- PFP review: [dag/results/GP-IMPORT-CONTINUOUS-TIME/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-CONTINUOUS-TIME/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Complete Boolean square-root obstruction and both exact complex unitary square roots of toggle; generic projector-square algebra and Boolean enumeration in Lean.
  - does not support: Supply topology, continuous time and the one-parameter group; invoke Stone only under its hypotheses. Square roots alone do not define continuous dynamics.
  - next test: Supply topology, continuous time and the one-parameter group; invoke Stone only under its hypotheses. Square roots alone do not define continuous dynamics.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1034
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` |
- counts toward the grade: yes

### Lean: `lean4/H016ContinuousDynamicsFork.lean`

- file: [lean4/H016ContinuousDynamicsFork.lean](../../../lean4/H016ContinuousDynamicsFork.lean)
- sha256 (`bytes`): `906b145d8626c1887b1075e9b900858ca3f0c16df6fa65a2d8a87aa68b06de85`
- cited in: node.lean, record TFQ-1034
- replay: `none`
- check: `cd lean4 && lake build H016ContinuousDynamicsFork`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `toggle` | yes | yes | no | - | `#print axioms toggle` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1034
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1034_gp_import_continuous_time.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1034_gp_import_continuous_time.md](../../../dag/derivations/08_l1_to_l2/tfq_1034_gp_import_continuous_time.md)
- sha256 (`lf-normalised`): `0f46468a432525379356e6aba79a465137949a1d6d6fbc2cf0c194e6b2076a36`
- generated view: listed, not counted
- cited in: record TFQ-1034
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/continuum_price_ledger.yaml`

- file: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/continuum_price_ledger.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/gap_register.yaml`

- file: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/gap_register.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (0):


Outgoing (2):

- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

No incoming route.
