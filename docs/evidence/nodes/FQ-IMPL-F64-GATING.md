# FQ-IMPL-F64-GATING

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Float policy for tracked Rust: "sealed: agreed use only, each entry added or raised by Jeremy (dbccpage) alone, class SEARCH_OR_SOLVER or DIAGNOSTIC_ONLY; a float may propose but never authorize a result. legacy_debt: float use present when the gate was introduced on 2026-10-16 (origin/main bef50fb2e); it may only shrink." sealed is empty; legacy_debt counts per crate: omega_quantum_physics 35 files, omega_mub 20, omega_wdp 9, omega_local_green_global_red_lggr 8, omega_lifts 3, omega_majorana 2, omega_measurement 2. engine_bridge.rs is the diagnostic f64 lens ("numerical result never certifies an exact state or theorem").

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- floating point as diagnostic only (assumption)

## Bottleneck

Exact faces use BigRational/Q(i)/Q(zeta_n); f64 faces are legacy debt, not agreed use. Which quantum_physics results still route through f64 is not audited here.

## Source status

omega_engine_operations/use_cases/cicd/f64_contract.json schema omega.f64_contract.v1, authority_effect None; sealed: {} ; legacy_debt: 370 files

## Review

- PFP review: [dag/results/FQ-IMPL-F64-GATING/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/FQ-IMPL-F64-GATING/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `consistent`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: Exact integer differences and bounded binary64 diagnostic rounding collisions are retained; distinctness and the literal rounding-model collision are kernel checked.
  - does not support: Audit the full tracked Rust policy/ledger and prove an IEEE754-model transport before making repository-wide gating claims. A diagnostic collision or declared zero authority tag is not an implemented global enforcement theorem.
  - next test: Audit the full tracked Rust policy/ledger and prove an IEEE754-model transport before making repository-wide gating claims. A diagnostic collision or declared zero authority tag is not an implemented global enforcement theorem.

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
| `QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall` |
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` |
- counts toward the grade: yes

### Lean: `lean4/PrimitiveLiftCertificate.lean`

- file: [lean4/PrimitiveLiftCertificate.lean](../../../lean4/PrimitiveLiftCertificate.lean)
- sha256 (`bytes`): `62f111c027a1653c3bdca013d864cb4a090bf6837abbfbbac6fb8f1f2d9d5f9a`
- cited in: record TFQ-0188
- replay: `none`
- check: `cd lean4 && lake build PrimitiveLiftCertificate`
- counts toward the grade: yes

### Rust: `code/rust/src/category_theory/monoidal/mod.rs`

- file: [code/rust/src/category_theory/monoidal/mod.rs](../../../code/rust/src/category_theory/monoidal/mod.rs)
- sha256 (`bytes`): `adcbdf082068ffd2da2d6d7ab6f4061cd88c595c048d02b33832132fd3588a62`
- cited in: record TFQ-0179
- note: no test is cited for this symbol; its crate is tfqm_category_theory
- counts toward the grade: yes

### Rust: `code/rust/src/mub/src/omega_native/d6_exact_sos.rs`

- file: [code/rust/src/mub/src/omega_native/d6_exact_sos.rs](../../../code/rust/src/mub/src/omega_native/d6_exact_sos.rs)
- sha256 (`bytes`): `4c9d104916d7e1a8128a979a3e96a9fb563c1cbe316f53be2f8c933f3e7e23cf`
- cited in: record TFQ-0179
- note: no test is cited for this symbol; its crate is tfqm_mub
- counts toward the grade: yes

### Rust: `code/rust/src/mub/src/omega_native/d6_sos_float_sdp.rs`

- file: [code/rust/src/mub/src/omega_native/d6_sos_float_sdp.rs](../../../code/rust/src/mub/src/omega_native/d6_sos_float_sdp.rs)
- sha256 (`bytes`): `31b90be076ba73c5e7367c0ba9e440ad70a4dfa54879157d64753734911efd3f`
- cited in: record TFQ-0179
- note: no test is cited for this symbol; its crate is tfqm_mub
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/engine_bridge.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/engine_bridge.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `omega_engine_operations/use_cases/cicd/f64_contract_gate.py`

- file: `omega_engine_operations/use_cases/cicd/f64_contract_gate.py`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0179_keep_omega_mub_float_cross_checks_from_authorizing_a_mub_6_existence_claim.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0179_keep_omega_mub_float_cross_checks_from_authorizing_a_mub_6_existence_claim.md](../../../dag/derivations/22_implementation_sibling/tfq_0179_keep_omega_mub_float_cross_checks_from_authorizing_a_mub_6_existence_claim.md)
- sha256 (`lf-normalised`): `5076a6296a0d3ee1f01265c6807ea769d5e2529a405f3140552705e8ab8e34c1`
- generated view: listed, not counted
- cited in: record TFQ-0179
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0188_refuse_the_f64_lift_scale_on_cycleliftspec_as_a_licence_for_an_exact.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0188_refuse_the_f64_lift_scale_on_cycleliftspec_as_a_licence_for_an_exact.md](../../../dag/derivations/22_implementation_sibling/tfq_0188_refuse_the_f64_lift_scale_on_cycleliftspec_as_a_licence_for_an_exact.md)
- sha256 (`lf-normalised`): `62b613072f2ecc85322fd9d1ced77537fe961a0f434cd0e84b0834671f4e5c7a`
- generated view: listed, not counted
- cited in: record TFQ-0188
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0192_keep_diagnostic_floats_and_display_conversions_out_of_governance_and_out_of.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0192_keep_diagnostic_floats_and_display_conversions_out_of_governance_and_out_of.md](../../../dag/derivations/22_implementation_sibling/tfq_0192_keep_diagnostic_floats_and_display_conversions_out_of_governance_and_out_of.md)
- sha256 (`lf-normalised`): `a66729e619d59a1cff501467c6b4425a0974f4defb279bff52126a17b0d17495`
- generated view: listed, not counted
- cited in: record TFQ-0192
- counts toward the grade: no

### Documents and data: `omega_engine_operations/use_cases/cicd/f64_contract.json`

- file: `omega_engine_operations/use_cases/cicd/f64_contract.json`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0179 lean4: not located
- TFQ-0179 python: not located
- TFQ-0188 python: not located
- TFQ-0188 rust: no local rust twin located for omega_engine/crates_rs/omega_lifts/src/cycle_lift_result.rs
- TFQ-0188 rust: no local rust twin located for omega_engine/crates_rs/omega_lifts/src/cycle_lift_spec.rs
- TFQ-0188 rust: no local rust twin located for omega_engine/crates_rs/omega_lifts/src/lift_primitive.rs
- TFQ-0192 lean4: not located
- TFQ-0192 python: not located
- TFQ-0192 rust: no local rust twin located for omega_engine/crates_rs/omega_measurement/src/documentary_traceability.rs
- TFQ-0192 rust: no local rust twin located for omega_engine/crates_rs/omega_measurement/src/measurement_access.rs
- TFQ-0192 rust: no local rust twin located for omega_engine/crates_rs/omega_measurement/src/measurement_kernel.rs

## Routes

Incoming (0):


Outgoing (0):


No incoming route.
