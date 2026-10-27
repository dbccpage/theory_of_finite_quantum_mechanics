# L1-WDP-WITNESS-MASS

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A declared mass m: W -\> R\>=0 on witnesses gives finite additivity by construction. With positive total mass the normalized cell values are nonnegative and sum to one (P01); atom-mass uniqueness holds on finite Boolean algebras (O01). WDP 8.1: plurality or number is not derived from one cut. WDP-CH09-N01: a finite witness valuation is not chance, frequency, or the Born rule.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

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
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification` |
| `QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1` |

- counts toward the grade: yes

### Lean: `lean4/ProbabilitySimplex.lean`

- file: [lean4/ProbabilitySimplex.lean](../../../lean4/ProbabilitySimplex.lean)
- sha256 (`bytes`): `94547b50c80b02dfef733d5adb798e338d8a6feeebe02e82dade7f5ebe9f7f8a`
- cited in: record TFQ-0167 (shared)
- replay: `none`
- check: `cd lean4 && lake build ProbabilitySimplex`
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

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md)
- sha256 (`lf-normalised`): `1596c27b09af32aec26710dacafcbe1dcb5081bc06d35d094b4c0b0353932e64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0358_normalize_a_declared_positive_witness_mass_to_cell_values_that_are_nonnegative.md`

- file: [dag/derivations/07_l1_emergence/tfq_0358_normalize_a_declared_positive_witness_mass_to_cell_values_that_are_nonnegative.md](../../../dag/derivations/07_l1_emergence/tfq_0358_normalize_a_declared_positive_witness_mass_to_cell_values_that_are_nonnegative.md)
- sha256 (`lf-normalised`): `d421be4a39c66f770ca866ae5652bcc45115e5a81fe21d41a1e988078e03da27`
- generated view: listed, not counted
- cited in: record TFQ-0358
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md](../../../dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md)
- sha256 (`lf-normalised`): `f76075556be2935a7fa3b215d691a46daef041554f57a0c3c42faba6c6368459`
- generated view: listed, not counted
- cited in: record TFQ-0167 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:10accdc18b88414a6a931a9e7fc887c41090315925cc258605a210ae3a97c286::try_from_weights`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`

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
