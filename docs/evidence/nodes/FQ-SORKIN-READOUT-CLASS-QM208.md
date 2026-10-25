# FQ-SORKIN-READOUT-CLASS-QM208

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: general I3(alpha*t²+beta*t⁴)=12*beta*abc(a+b+c), hence general vanishing iff beta=0. Exact Q(zeta12) control norms (7,±4) give R_AB invariance iff B=0; no full positivity-cone classification is inferred.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- add-then-square amplitude composition rule (assumption)
- restriction to polynomial readout family (assumption)

## Bottleneck

Unmet after the PFP review: Formalize the embedding-weight/basis-coordinate conversion and full rational readout positivity cone. Polynomial restriction and amplitude addition are admitted, and this is not a classification of all readouts. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM-208 table row: exact finite invariant; residual "add-then-square composition and restriction to the polynomial readout family"

## Review

- PFP review: [dag/results/FQ-SORKIN-READOUT-CLASS-QM208/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-SORKIN-READOUT-CLASS-QM208/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: general I3(alpha*t²+beta*t⁴)=12*beta*abc(a+b+c), hence general vanishing iff beta=0. Exact Q(zeta12) control norms (7,±4) give R_AB invariance iff B=0; no full positivity-cone classification is inferred.
  - does not support: Formalize the embedding-weight/basis-coordinate conversion and full rational readout positivity cone. Polynomial restriction and amplitude addition are admitted, and this is not a classification of all readouts.
  - next test: Formalize the embedding-weight/basis-coordinate conversion and full rational readout positivity cone. Polynomial restriction and amplitude addition are admitted, and this is not a classification of all readouts.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1011
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` |

- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: node.lean, record TFQ-1011
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `born_trace_vs_quartic_readout_and_three_ray_positivity_gap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms born_trace_vs_quartic_readout_and_three_ray_positivity_gap` |
| `qzeta12_rational_readout_cone_and_galois_selection` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms qzeta12_rational_readout_cone_and_galois_selection` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/everett.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/everett.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1011
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1011
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1011
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1011_fq_sorkin_readout_class_qm208.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1011_fq_sorkin_readout_class_qm208.md](../../../dag/derivations/10_finite_qm_core/tfq_1011_fq_sorkin_readout_class_qm208.md)
- sha256 (`lf-normalised`): `8f9d82003e82169a098078f5f192ba4a825891a161ae2cafed4ff6876aa655ff`
- generated view: listed, not counted
- cited in: record TFQ-1011
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md)
- sha256 (`lf-normalised`): `b9adbe593870ae277067c746b426f7b937a9cf98319cd4c8c0b712d9059dd5ac`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-SORKIN-CLASS` `DERIVED_LEAN`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN), [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (1):

- `FQ-R-GAP-BORN-UNIQUENESS` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL)
