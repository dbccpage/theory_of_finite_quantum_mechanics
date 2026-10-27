# DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> D_jk = Tr(C_j rho C_k^dagger) is imported with no representation bridge to the programme; positive semidefiniteness (rho\>=0) and trace-one (completeness) are standard consequences under imported premises.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 22
- distinct cited Lean declarations covered by a current replay receipt: 22
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- density operator rho and trace (assumption)
- class operators C_j (assumption)
- complex field (assumption)

## Bottleneck

The formula D_jk = Tr(C_j rho C_k^dagger), a density operator, class operators, and a bridge from finite transport stay imported. Positive semidefiniteness and trace one for a general history model stay imported. The integer Gram square, the determinant identity, and the cleared witnesses (1, 1) over 2 and (3, 4) over 5 are one finite case.

## Source status

\[IMPORTED\] SOURCE_ADMITTED; NO_LEAN (QM_043-C1); C2/C6 \[STANDARD, CONDITIONAL, IMPORTED\]

## Review

- PFP review: [dag/results/DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Actual class-operator Gram tables are positive semidefinite, and exact controls separate class completeness, Kraus completeness, diagonal trace and global weight.
  - does not support: Justify the class-operator family, density and physical history normalization, and formalize the native Gram-table bridge. No general decoherence functional is derived.
  - next test: Justify the class-operator family, density and physical history normalization, and formalize the native Gram-table bridge. No general decoherence functional is derived.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DecoherenceFunctionalGram.lean`

- file: [lean4/DecoherenceFunctionalGram.lean](../../../lean4/DecoherenceFunctionalGram.lean)
- sha256 (`bytes`): `456535c1ea379be8081e785984de7183d3890d78c3e000ce5843f9144c6e2a86`
- cited in: node.lean, receipt dag/research/campaign_ds-qm043-decoherence-functional-import_lean_replay.json (DecoherenceFunctionalGram)
- replay: `verified`
  - receipt [dag/research/campaign_ds-qm043-decoherence-functional-import_lean_replay.json](../../../dag/research/campaign_ds-qm043-decoherence-functional-import_lean_replay.json) (module `DecoherenceFunctionalGram`): recorded sha256 `456535c1ea379be8081e785984de7183d3890d78c3e000ce5843f9144c6e2a86` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DecoherenceFunctionalGram`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DecoherenceFunctionalGram.classSeparates` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.classSeparates` |
| `DecoherenceFunctionalGram.classSum` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.classSum` |
| `DecoherenceFunctionalGram.diagNonneg` | yes | yes | yes | propext | `#print axioms DecoherenceFunctionalGram.diagNonneg` |
| `DecoherenceFunctionalGram.fiveSquare` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.fiveSquare` |
| `DecoherenceFunctionalGram.gramAtOnes` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.gramAtOnes` |
| `DecoherenceFunctionalGram.gramDet` | yes | yes | yes | Quot.sound, propext | `#print axioms DecoherenceFunctionalGram.gramDet` |
| `DecoherenceFunctionalGram.gramProd` | yes | yes | yes | propext | `#print axioms DecoherenceFunctionalGram.gramProd` |
| `DecoherenceFunctionalGram.gramValueNonneg` | yes | yes | yes | propext | `#print axioms DecoherenceFunctionalGram.gramValueNonneg` |
| `DecoherenceFunctionalGram.halfClass` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.halfClass` |
| `DecoherenceFunctionalGram.halfDenom` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.halfDenom` |
| `DecoherenceFunctionalGram.halfGlobal` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.halfGlobal` |
| `DecoherenceFunctionalGram.halfGlobalOne` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.halfGlobalOne` |
| `DecoherenceFunctionalGram.halfSeparates` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.halfSeparates` |
| `DecoherenceFunctionalGram.halfSquares` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.halfSquares` |
| `DecoherenceFunctionalGram.krausHolds` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.krausHolds` |
| `DecoherenceFunctionalGram.krausSquares` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.krausSquares` |
| `DecoherenceFunctionalGram.negMulNeg` | yes | yes | yes | propext | `#print axioms DecoherenceFunctionalGram.negMulNeg` |
| `DecoherenceFunctionalGram.sevenSquare` | yes | yes | yes | none | `#print axioms DecoherenceFunctionalGram.sevenSquare` |
| `DecoherenceFunctionalGram.squareNonneg` | yes | yes | yes | propext | `#print axioms DecoherenceFunctionalGram.squareNonneg` |
| `DecoherenceFunctionalGram.traceSquaresNonneg` | yes | yes | yes | Quot.sound, propext | `#print axioms DecoherenceFunctionalGram.traceSquaresNonneg` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0248 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0248_finite_history_decoherence_matrix.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0248_finite_history_decoherence_matrix.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0248_finite_history_decoherence_matrix.md)
- sha256 (`lf-normalised`): `27696629d6b8396320e708909f4c1abd64b63339fb9a15634ca0398ea578ef6c`
- generated view: listed, not counted
- cited in: record TFQ-0248 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/043_gellmann_hartle_cochain_decoherence/qm_043_gellmann_hartle_cochain_decoherence_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/043_gellmann_hartle_cochain_decoherence/qm_043_gellmann_hartle_cochain_decoherence_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0248 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm

## Routes

Incoming (0):


Outgoing (2):

- `APP-R-FSP-CAR-EXTERIOR-FOCK` `DERIVED_PROSE`: [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)
- `DS-R-DECOHERENCE-FUNCTIONAL` `DERIVED_LEAN`: [DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY](DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY.md) (PROVED_LEAN)

No incoming route.
