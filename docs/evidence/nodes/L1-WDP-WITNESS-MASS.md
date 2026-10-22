# L1-WDP-WITNESS-MASS

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A declared mass m: W -\> R\>=0 on witnesses gives finite additivity by construction. With positive total mass the normalized cell values are nonnegative and sum to one (P01); atom-mass uniqueness holds on finite Boolean algebras (O01). WDP 8.1: plurality or number is not derived from one cut. WDP-CH09-N01: a finite witness valuation is not chance, frequency, or the Born rule.

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

- nonnegative real mass assignment on witnesses: assumption

## Bottleneck

The mass is declared. No source read derives the mass from Phi1, Gamma2 or from the cochain window.

## Source status

WDP 8.2 declared mass; WDP-CH08-D01, P01, O01; 8.1 'matching before number'

## Review

- PFP review: [dag/results/L1-WDP-WITNESS-MASS/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-WDP-WITNESS-MASS/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: Exact atom and cell normalization, negative/zero refusal and generic rational normalization identity in Lean.
  - does not support: Prove arbitrary finite Boolean-algebra valuation uniqueness and source carrier refinement; declared mass does not derive probability interpretation.
  - next test: Prove arbitrary finite Boolean-algebra valuation uniqueness and source carrier refinement; declared mass does not derive probability interpretation.

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
| `QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification` |
| `QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1` |
- counts toward the grade: yes

### Lean: `lean4/H001ProbabilitySimplex.lean`

- file: [lean4/H001ProbabilitySimplex.lean](../../../lean4/H001ProbabilitySimplex.lean)
- sha256 (`bytes`): `a466cf99bcf45d5ba786f52361702a2988400bd210a234cf5f783366a8a47228`
- cited in: record TFQ-0167 (shared)
- replay: `none`
- check: `cd lean4 && lake build H001ProbabilitySimplex`
- counts toward the grade: no

### Rust: `code/rust/src/category_theory/foundations/finite_set.rs`

- file: [code/rust/src/category_theory/foundations/finite_set.rs](../../../code/rust/src/category_theory/foundations/finite_set.rs)
- sha256 (`bytes`): `6c154362ed87f04513aa3e3f705ca79a7fbda10be3e797fccf805b6b6ac81f5d`
- cited in: record TFQ-0167 (shared)
- note: no test is cited for this symbol; its crate is tfqm_category_theory
- counts toward the grade: no

### Rust: `code/rust/src/finite_probability/simplex.rs`

- file: [code/rust/src/finite_probability/simplex.rs](../../../code/rust/src/finite_probability/simplex.rs)
- sha256 (`bytes`): `f806fa8ae31e1d13be6cfe1ba131d1ae33c5778f7448c58601e5f2ed6eb7791f`
- cited in: record TFQ-0167 (shared)
- note: no test is cited for this symbol; its crate is tfqm_finite_probability
- counts toward the grade: no

### Rust: `code/rust/src/wdp/lib.rs`

- file: [code/rust/src/wdp/lib.rs](../../../code/rust/src/wdp/lib.rs)
- sha256 (`bytes`): `aa868cc58a3c6fdf1eabfcdd46798329bf560389e83367c574259837d2d3ed4c`
- cited in: record TFQ-0167 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_finite_probability/src/simplex.rs`

- file: `omega_engine/crates_rs/omega_finite_probability/src/simplex.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0358_normalize_a_declared_positive_witness_mass_to_cell_values_that_are_nonnegative.md`

- file: [dag/derivations/07_l1_emergence/tfq_0358_normalize_a_declared_positive_witness_mass_to_cell_values_that_are_nonnegative.md](../../../dag/derivations/07_l1_emergence/tfq_0358_normalize_a_declared_positive_witness_mass_to_cell_values_that_are_nonnegative.md)
- sha256 (`lf-normalised`): `d421be4a39c66f770ca866ae5652bcc45115e5a81fe21d41a1e988078e03da27`
- generated view: listed, not counted
- cited in: record TFQ-0358
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md](../../../dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md)
- sha256 (`lf-normalised`): `1b9b4d68b36532db18e1b689ae85fc7d4cdb38c1031f1712b8b8f64fb01530e6`
- generated view: listed, not counted
- cited in: record TFQ-0167 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0167 python: not located

## Routes

Incoming (0):


Outgoing (5):

- `L1-R-DECLARED-MASS-TO-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)
- `UDG-R-TFQ-0168` `COMPUTED`: [TFQ-0168](TFQ-0168.md) (COMPUTATIONALLY_CHECKED)
- `UDG-R-TFQ-0169` `COMPUTED`: [TFQ-0169](TFQ-0169.md) (COMPUTATIONALLY_CHECKED)
- `UDG-R-TFQ-0170` `COMPUTED`: [TFQ-0170](TFQ-0170.md) (COMPUTATIONALLY_CHECKED)
- `UDG-R-TFQ-0171` `GAP_NO_DERIVATION`: [TFQ-0171](TFQ-0171.md) (OPEN)

No incoming route.
