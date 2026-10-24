# FQ-FIVE-IMPORT-PROXY-SEPARATION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The five finite diagnostic proxy predicates (AdmitsImport in FiniteQM.lean: phase fiber, quadratic readout, context parity, frame function, clock tower) are pairwise separated by countermodels (5x5 matrix); explicit Born-vs-quartic divergence on psi=(3/5,4/5,0,0) and a 3-ray-vs-PSD gap are witnessed. Separation of proxy predicates is not independence of the physical imports.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- finite proxy predicates chosen by the authors (assumption)

## Bottleneck

Quadratic geometry and Born pairing overlap; no independence theorem exists; bipartite composition and entangled preparation are load-bearing but absent from the five-item cascade.

## Source status

QM-219; paper s13.8.2 corrects the proposed five-import boundary: not proved independent, not a minimal basis for Bell

## Review

- PFP review: [dag/results/FQ-FIVE-IMPORT-PROXY-SEPARATION/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/FQ-FIVE-IMPORT-PROXY-SEPARATION/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: The actual 5x5 proxy separation matrix and intermediate rational matrices are checked independently; Lean computes the same declared predicates and a three-ray counterexample.
  - does not support: Strengthen and justify the physical interfaces before claiming independence of phase/Born/operator/continuous-dynamics imports. Finite proxy separation does not establish that independence.
  - next test: Strengthen and justify the physical interfaces before claiming independence of phase/Born/operator/continuous-dynamics imports. Finite proxy separation does not establish that independence.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1013
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` |
- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: node.lean, record TFQ-1013
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `born_trace_vs_quartic_readout_and_three_ray_positivity_gap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms born_trace_vs_quartic_readout_and_three_ray_positivity_gap` |
| `five_import_mutual_independence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms five_import_mutual_independence` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/foundational_derivation_closure.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/foundational_derivation_closure.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1013
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1013
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_1013_fq_five_import_proxy_separation.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_1013_fq_five_import_proxy_separation.md](../../../dag/derivations/12_finite_qm_structure/tfq_1013_fq_five_import_proxy_separation.md)
- sha256 (`lf-normalised`): `6d9b02f730d42852d682cfc94a97eb579a76c9f053b6300551c0cffa4e0fb0bd`
- generated view: listed, not counted
- cited in: record TFQ-1013
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `X-R-INTERFACE-TO-FIVE-IMPORT-PROXIES` `DERIVED_LEAN`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

