# FQ-IMPL-F64-GATING

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Float policy for tracked Rust: "sealed: agreed use only, each entry added or raised by Jeremy (dbccpage) alone, class SEARCH_OR_SOLVER or DIAGNOSTIC_ONLY; a float may propose but never authorize a result. legacy_debt: float use present when the gate was introduced on 2026-10-16 (origin/main bef50fb2e); it may only shrink." sealed is empty; legacy_debt counts per crate: omega_quantum_physics 35 files, omega_mub 20, omega_wdp 9, omega_local_green_global_red_lggr 8, omega_lifts 3, omega_majorana 2, omega_measurement 2. engine_bridge.rs is the diagnostic f64 lens ("numerical result never certifies an exact state or theorem").

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- floating point as diagnostic only (assumption)

## Bottleneck

Exact faces use BigRational/Q(i)/Q(zeta_n); f64 faces are legacy debt, not agreed use. Which quantum_physics results still route through f64 is not audited here.

## Source status

external:sha256:6ae8c7c272743af5f672a868ca9ad528f1753b9e66b179994b5d35ad0113c5d1 schema omega.f64_contract.v1, authority_effect None; sealed: {} ; legacy_debt: 370 files

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
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall` |
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` |

- counts toward the grade: yes

### Lean: `lean4/PrimitiveLiftCertificate.lean`

- file: [lean4/PrimitiveLiftCertificate.lean](../../../lean4/PrimitiveLiftCertificate.lean)
- sha256 (`bytes`): `73da713572ba165ec504c7abe70f3a19a15ede07357f7b85872d107dd8a31293`
- cited in: record TFQ-0188
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_implementation.json](../../../dag/research/lean_replay_campaign_implementation.json) (module `PrimitiveLiftCertificate`): recorded sha256 `73da713572ba165ec504c7abe70f3a19a15ede07357f7b85872d107dd8a31293` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build PrimitiveLiftCertificate`
- counts toward the grade: yes

### Rust: `code/rust/src/category_theory/monoidal/mod.rs`

- file: [code/rust/src/category_theory/monoidal/mod.rs](../../../code/rust/src/category_theory/monoidal/mod.rs)
- sha256 (`bytes`): `adcbdf082068ffd2da2d6d7ab6f4061cd88c595c048d02b33832132fd3588a62`
- cited in: record TFQ-0179
- note: no test is cited for this symbol; its crate is tfqm_category_theory
- counts toward the grade: yes

### Rust: `code/rust/src/mub/native/d6_exact_sos.rs`

- file: [code/rust/src/mub/native/d6_exact_sos.rs](../../../code/rust/src/mub/native/d6_exact_sos.rs)
- sha256 (`bytes`): `04c6547bc35ec8ffc30263c446ddce9b88b4e643cc5a1bd894a0afd8a6ac69b8`
- cited in: record TFQ-0179
- note: no test is cited for this symbol; its crate is tfqm_mub
- counts toward the grade: yes

### Rust: `code/rust/src/mub/native/d6_sos_float_sdp.rs`

- file: [code/rust/src/mub/native/d6_sos_float_sdp.rs](../../../code/rust/src/mub/native/d6_sos_float_sdp.rs)
- sha256 (`bytes`): `d29187fe7c4dbf10a165e2e8243ca02f02d7c196d231368ec48349ecf62a1e65`
- cited in: record TFQ-0179
- note: no test is cited for this symbol; its crate is tfqm_mub
- counts toward the grade: yes

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0179_keep_omega_mub_float_cross_checks_from_authorizing_a_mub_6_existence_claim.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0179_keep_omega_mub_float_cross_checks_from_authorizing_a_mub_6_existence_claim.md](../../../dag/derivations/22_implementation_sibling/tfq_0179_keep_omega_mub_float_cross_checks_from_authorizing_a_mub_6_existence_claim.md)
- sha256 (`lf-normalised`): `b2cf15cc24f6584b2f86394950877d14017e77ff341e2908c78d8b87885afc31`
- generated view: listed, not counted
- cited in: record TFQ-0179
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0188_refuse_the_f64_lift_scale_on_cycleliftspec_as_a_licence_for_an_exact.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0188_refuse_the_f64_lift_scale_on_cycleliftspec_as_a_licence_for_an_exact.md](../../../dag/derivations/22_implementation_sibling/tfq_0188_refuse_the_f64_lift_scale_on_cycleliftspec_as_a_licence_for_an_exact.md)
- sha256 (`lf-normalised`): `303e9bfd8839de202416f2852b8fa9015dde0135d3c50ef84365a680f018522b`
- generated view: listed, not counted
- cited in: record TFQ-0188
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0192_keep_diagnostic_floats_and_display_conversions_out_of_governance_and_out_of.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0192_keep_diagnostic_floats_and_display_conversions_out_of_governance_and_out_of.md](../../../dag/derivations/22_implementation_sibling/tfq_0192_keep_diagnostic_floats_and_display_conversions_out_of_governance_and_out_of.md)
- sha256 (`lf-normalised`): `dda7baebd789bea679daa6cd553190a483e2d0ed5cac8efecf30bdcde81e9cd2`
- generated view: listed, not counted
- cited in: record TFQ-0192
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:6ae8c7c272743af5f672a868ca9ad528f1753b9e66b179994b5d35ad0113c5d1:1`
- `external:sha256:759a26347ca8bdc640e99bf834323b5fa222daa326765c5c5bdc95e618b126ed:1`
- `external:sha256:8a8eb6cdf84a34d0de92f887c5efc2d394dbc6aed7be3b70394c09b72d36f078::DiagnosticBridgeError`

## Absences recorded by the TFQ records

- TFQ-0179 lean4: not located
- TFQ-0179 python: not located
- TFQ-0188 python: not located
- TFQ-0188 rust: no local rust twin located for external:sha256:2908042afeabf18585e04298b65ebe3d19f65c7d68d6e6761fce9a908e9a59d7
- TFQ-0188 rust: no local rust twin located for external:sha256:7cdc5e0bce6c29a1598347459d048b0b89de2fe7170e1892096c2f9e93c3db89
- TFQ-0188 rust: no local rust twin located for external:sha256:c58c7a83c804699a86ad761d7e3f9456f56daa0c1ba50dcff68378049955b99c
- TFQ-0192 lean4: not located
- TFQ-0192 python: not located
- TFQ-0192 rust: no local rust twin located for external:sha256:07e63c53da4b64ecfc4fa925a1544eccb27b590bfd3e257b35947c3c15a3ca73
- TFQ-0192 rust: no local rust twin located for external:sha256:0d9d32875b0dda27f266bef37af470f35769ab924210bd90b9ed923958b2baf3
- TFQ-0192 rust: no local rust twin located for external:sha256:e7de14f3a7ac549411872b110b09968dc2178ab76ed8099b8871e949a9d69b7a

## Routes

Incoming (0):


Outgoing (0):


No incoming route.
