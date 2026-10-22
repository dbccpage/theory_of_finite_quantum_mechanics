# DS-QM212-MAJORANA-PROBLEM

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Majorana braiding / Clifford generator algebra (gamma_1^2 = I, gamma_2^2 = I, gamma_1 gamma_2 + gamma_2 gamma_1 = 0, and Parity^2 = -I) is mechanized in qm212_majorana_clifford_relations.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Finite Majorana Clifford parity algebra and tetron braid/parity checks are mechanized; experimental device noise models remain external.

## Source status

Majorana Clifford generator anticommutation and parity invariants mechanized in DerivationDagQMClosure.lean and omega_majorana

## Review

- PFP review: [dag/results/DS-QM212-MAJORANA-PROBLEM/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM212-MAJORANA-PROBLEM/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Full gamma/parity/braid matrices and the general rational Clifford/scaled-braid identities are kernel/native checked.
  - does not support: Supply physical mode, braid dynamics, device/noise and tensor interpretation. Canonical normalization and experimental realization are not inferred from the algebra.
  - next test: Supply physical mode, braid dynamics, device/noise and tensor interpretation. Canonical normalization and experimental realization are not inferred from the algebra.

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
| `QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid` |
| `QuantumMechanics.DerivationDagQMClosure.qm212_majorana_clifford_relations` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm212_majorana_clifford_relations` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/lib.rs`

- file: [code/rust/src/wdp/lib.rs](../../../code/rust/src/wdp/lib.rs)
- sha256 (`bytes`): `aa868cc58a3c6fdf1eabfcdd46798329bf560389e83367c574259837d2d3ed4c`
- cited in: record TFQ-0181
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_majorana/src/lib.rs`

- file: `omega_engine/crates_rs/omega_majorana/src/lib.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `code/python/src/majorana/majorana_gf2_diagnostic.py`

- file: [code/python/src/majorana/majorana_gf2_diagnostic.py](../../../code/python/src/majorana/majorana_gf2_diagnostic.py)
- sha256 (`bytes`): `3f7009456f96c97cc161e1aa8f94840e8fb3d52bd6feec74eae5fcb51e9d39ca`
- cited in: record TFQ-0181
- counts toward the grade: yes

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0181_keep_omega_majorana_a_gf_2_diagnostic_and_do_not_treat_it_as_an.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0181_keep_omega_majorana_a_gf_2_diagnostic_and_do_not_treat_it_as_an.md](../../../dag/derivations/22_implementation_sibling/tfq_0181_keep_omega_majorana_a_gf_2_diagnostic_and_do_not_treat_it_as_an.md)
- sha256 (`lf-normalised`): `bcc4f7799cfbb5e0447711f996f366ee7fef956c87762eeda3c1d19981e30530`
- generated view: listed, not counted
- cited in: record TFQ-0181
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/212_microsoft_majorana_problem/qm_212_microsoft_majorana_problem_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/212_microsoft_majorana_problem/qm_212_microsoft_majorana_problem_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0181 lean4: not located

## Routes

Incoming (1):

- `DS-R-MP-UNKNOWN` `DERIVED_LEAN`: [DS-QM120-MERMIN-PERES-F2-OBSTRUCTION](DS-QM120-MERMIN-PERES-F2-OBSTRUCTION.md) (PROVED_LEAN)

Outgoing (7):

- `APP-R-MAJ-F2-PARITY-SCHEDULE` `DERIVED_PROSE`: [MAJ-F2-PARITY-SCHEDULE](MAJ-F2-PARITY-SCHEDULE.md) (DEFINITION)
- `APP-R-MAJ-IMPORT-KITAEV-CHAIN` `CONDITIONAL_ON_IMPORT`: [MAJ-IMPORT-KITAEV-CHAIN](MAJ-IMPORT-KITAEV-CHAIN.md) (IMPORTED_ASSUMPTION)
- `APP-R-MAJ-MAJORANA-BRAID-YB-EXACT` `COMPUTED`: [MAJ-MAJORANA-BRAID-YB-EXACT](MAJ-MAJORANA-BRAID-YB-EXACT.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-MAJ-REALIZATION-PACKET-GAP` `DERIVED_PROSE`: [MAJ-REALIZATION-PACKET-GAP](MAJ-REALIZATION-PACKET-GAP.md) (DEFINITION)
- `UDG-R-TFQ-0182` `COMPUTED`: [TFQ-0182](TFQ-0182.md) (COMPUTATIONALLY_CHECKED)
- `UDG-R-TFQ-0183` `GAP_NO_DERIVATION`: [TFQ-0183](TFQ-0183.md) (OPEN)
- `UDG-R-TFQ-0184` `GAP_NO_DERIVATION`: [TFQ-0184](TFQ-0184.md) (OPEN)
