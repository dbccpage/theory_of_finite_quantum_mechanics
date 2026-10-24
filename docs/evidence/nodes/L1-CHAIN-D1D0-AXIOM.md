# L1-CHAIN-D1D0-AXIOM

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `ADMITTED_PRIMITIVE`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Flatness d1 o d0 = 0 of the cochain window is assumed in the l1 framework.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- presheaf functoriality / restriction system: assumption

## Bottleneck

Whether the Genesis / WDP fragments derive flatness is for those fragments to say.

## Source status

C18 d1 o d0 = 0: \[DECLARED AXIOM\] assumed via presheaf functoriality; not proved here

## Review

- PFP review: [dag/results/L1-CHAIN-D1D0-AXIOM/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-CHAIN-D1D0-AXIOM/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `ADMITTED_PRIMITIVE`; qualifies for E4: no.
  - narrowest claim: Actual triangle d1*d0 arrays, potential images and flat/nonflat controls, with general telescoping and a defective-row witness in Lean.
  - does not support: Derive functorial restrictions from admitted presheaf data and transport arbitrary finite cochain windows; zero on one potential is insufficient.
  - next test: Derive functorial restrictions from admitted presheaf data and transport arbitrary finite cochain windows; zero on one potential is insufficient.

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
| `QuantumMechanics.DerivationDagQMClosure.qm093_cochain_d1_d0_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm093_cochain_d1_d0_zero` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/cochains.rs`

- file: [code/rust/src/wdp/cochains.rs](../../../code/rust/src/wdp/cochains.rs)
- sha256 (`bytes`): `56119171f22517ed69ba8b086b3001e8f23f46438bbbb8d07962252b58e524a5`
- cited in: record TFQ-0350
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0350_assume_d1_d0_0_only_by_a_declared_certificate_or_the.md`

- file: [dag/derivations/07_l1_emergence/tfq_0350_assume_d1_d0_0_only_by_a_declared_certificate_or_the.md](../../../dag/derivations/07_l1_emergence/tfq_0350_assume_d1_d0_0_only_by_a_declared_certificate_or_the.md)
- sha256 (`lf-normalised`): `8f48154986b12b817d4d0105fa7e1b783fac5b28600d67bf83566ae053f23475`
- generated view: listed, not counted
- cited in: record TFQ-0350
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md`

- file: [dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md](../../../dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md)
- sha256 (`lf-normalised`): `24435b37027494cea1e6541393a74dfaa720915fdab89c57efcf22685a0d8568`
- generated view: listed, not counted
- cited in: record TFQ-0052 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/003_l1_obstruction_framework/l1_obstruction_framework_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/003_l1_obstruction_framework/l1_obstruction_framework_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0052 lean4: not located
- TFQ-0052 python: not located
- TFQ-0052 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/gauge_cochain_complex.rs

## Routes

Incoming (0):


Outgoing (6):

- `APP-R-MAJ-F2-PARITY-SCHEDULE` `DERIVED_PROSE`: [MAJ-F2-PARITY-SCHEDULE](MAJ-F2-PARITY-SCHEDULE.md) (DEFINITION)
- `DS-R-COCHAIN-D1D0` `DERIVED_LEAN`: [DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO](DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO.md) (PROVED_LEAN)
- `DS-R-D1D0-COCHAIN` `DERIVED_LEAN`: [DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO](DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO.md) (PROVED_LEAN)
- `DS-R-MP-FROM-COCHAIN` `DERIVED_LEAN`: [DS-QM120-MERMIN-PERES-F2-OBSTRUCTION](DS-QM120-MERMIN-PERES-F2-OBSTRUCTION.md) (PROVED_LEAN)
- `L1-R-KKT` `DERIVED_LEAN`: [L1-FRAMEWORK-KKT-CERT](L1-FRAMEWORK-KKT-CERT.md) (PROVED_LEAN)
- `L1-R-PHI1-QUOTIENT` `DERIVED_LEAN`: [L1-QM002-O022A-PHI1-QUOTIENT](L1-QM002-O022A-PHI1-QUOTIENT.md) (PROVED_LEAN)

No incoming route.
