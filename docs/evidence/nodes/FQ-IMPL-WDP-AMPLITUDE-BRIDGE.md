# FQ-IMPL-WDP-AMPLITUDE-BRIDGE

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> omega_wdp amplitude_bridge.rs is the only artifact for WDP-CH19-P11/P12: with unit phase u=(3+4i)/5, integer edge cochains give transports u^{a_e}; adding a coboundary conjugates transports and leaves cycle holonomy unchanged; both readouts N(z1+z2) and N(z1+z2)^2 are common-phase invariant and left free; no homomorphism (Q,+) -\> U(1)(Q(i)) sends 1 to u, and u^n != 1 for every n \>= 1 (certified via (3+4i)^n mod 5).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- unit phase u=(3+4i)/5 over Q(i) (assumption)
- oriented graph and integer cochains (assumption)

## Bottleneck

The claims are about a Rust artifact and are backed by its native exact tests. The cited Lean is integer arithmetic (3^2 + 4^2 = 5^2 and similar) and does not state the claims.

## Source status

"Executable finite evidence; AuthorityEffect: None" for WDP-CH19-P11 and P12; residual WDP-CH19-O03 open

## Review

- PFP review: [dag/results/FQ-IMPL-WDP-AMPLITUDE-BRIDGE/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/FQ-IMPL-WDP-AMPLITUDE-BRIDGE/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact bounded phase/holonomy/readout controls and a general positive-power mod5 residue induction are retained with literal gauge/norm kernel identities.
  - does not support: Formalize the Gaussian numerator/denominator transport and the rational-additive-group obstruction to a homomorphism sending1 to this u. Do not infer a preferred readout or a general phase-selection theorem.
  - next test: Formalize the Gaussian numerator/denominator transport and the rational-additive-group obstruction to a homomorphism sending1 to this u. Do not infer a preferred readout or a general phase-selection theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1026
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` |
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` |

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
- sha256 (`lf-normalised`): `1c0c27f4dd1a65b271f0b43d6db955cf561a21ffeb9db78618cbe8a8898e7012`
- generated view: listed, not counted
- cited in: record TFQ-1026
- counts toward the grade: no

## Routes

Incoming (1):

- `FQ-R-AMPLITUDE-BRIDGE` `COMPUTED`: [FQ-IMPL-REALIFICATION-ADAPTER](FQ-IMPL-REALIFICATION-ADAPTER.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `FQ-R-GAP-U1` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-U1-CIRCLE](FQ-GAP-U1-CIRCLE.md) (CONDITIONAL)
