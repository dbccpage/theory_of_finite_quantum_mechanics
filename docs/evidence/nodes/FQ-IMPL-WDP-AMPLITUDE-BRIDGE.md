# FQ-IMPL-WDP-AMPLITUDE-BRIDGE

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact bounded phase/holonomy/readout controls and a general positive-power mod5 residue induction are retained with literal gauge/norm kernel identities.

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

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- unit phase u=(3+4i)/5 over Q(i) (assumption)
- oriented graph and integer cochains (assumption)

## Bottleneck

Unmet after the PFP review: Formalize the Gaussian numerator/denominator transport and the rational-additive-group obstruction to a homomorphism sending1 to this u. Do not infer a preferred readout or a general phase-selection theorem. The broader source statement is kept in pfp_review.prior_statement.

## Source status

"Executable finite evidence; AuthorityEffect: None" for WDP-CH19-P11 and P12; residual WDP-CH19-O03 open

## Review

- PFP review: [dag/results/FQ-IMPL-WDP-AMPLITUDE-BRIDGE/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/FQ-IMPL-WDP-AMPLITUDE-BRIDGE/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact bounded phase/holonomy/readout controls and a general positive-power mod5 residue induction are retained with literal gauge/norm kernel identities.
  - does not support: Formalize the Gaussian numerator/denominator transport and the rational-additive-group obstruction to a homomorphism sending1 to this u. Do not infer a preferred readout or a general phase-selection theorem.
  - next test: Formalize the Gaussian numerator/denominator transport and the rational-additive-group obstruction to a homomorphism sending1 to this u. Do not infer a preferred readout or a general phase-selection theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1026
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` |
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1026
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, node.source, record TFQ-1026
- counts toward the grade: no

### Documents and data: `dag/derivations/21_implementation_core/tfq_1026_fq_impl_wdp_amplitude_bridge.md`

- file: [dag/derivations/21_implementation_core/tfq_1026_fq_impl_wdp_amplitude_bridge.md](../../../dag/derivations/21_implementation_core/tfq_1026_fq_impl_wdp_amplitude_bridge.md)
- sha256 (`lf-normalised`): `de96fa0860790ae2830f71377bbd3322dd93ed6450113450bddda20a1dcc0538`
- generated view: listed, not counted
- cited in: record TFQ-1026
- counts toward the grade: no

## Routes

Incoming (1):

- `FQ-R-AMPLITUDE-BRIDGE` `DERIVED_LEAN`: [FQ-IMPL-REALIFICATION-ADAPTER](FQ-IMPL-REALIFICATION-ADAPTER.md) (PROVED_LEAN)

Outgoing (1):

- `FQ-R-GAP-U1` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-U1-CIRCLE](FQ-GAP-U1-CIRCLE.md) (CONDITIONAL)
