# FQ-IMPL-WDP-AMPLITUDE-BRIDGE

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> tfqm_wdp amplitude_bridge.rs is the only artifact for WDP-CH19-P11/P12: with unit phase u=(3+4i)/5, integer edge cochains give transports u^{a_e}; adding a coboundary conjugates transports and leaves cycle holonomy unchanged; both readouts N(z1+z2) and N(z1+z2)^2 are common-phase invariant and left free; no homomorphism (Q,+) -\> U(1)(Q(i)) sends 1 to u, and u^n != 1 for every n \>= 1 (certified via (3+4i)^n mod 5).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- unit phase u=(3+4i)/5 over Q(i) (assumption)
- oriented graph and integer cochains (assumption)

## Bottleneck

WDP-CH19-P11/P12 mechanized in WdpBatch4.lean alongside amplitude_bridge.rs; continuous U(1) Lie-group topologies remain outside the finite Gaussian-rational carrier.

## Source status

MECHANIZED in WdpBatch4.lean and verified by amplitude_bridge.rs

## Review

- PFP review: [evidence/results/FQ-IMPL-WDP-AMPLITUDE-BRIDGE/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../evidence/results/FQ-IMPL-WDP-AMPLITUDE-BRIDGE/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact bounded phase/holonomy/readout controls and a general positive-power mod5 residue induction are retained with literal gauge/norm kernel identities.
  - does not support: Formalize the Gaussian numerator/denominator transport and the rational-additive-group obstruction to a homomorphism sending1 to this u. Do not infer a preferred readout or a general phase-selection theorem.
  - next test: Formalize the Gaussian numerator/denominator transport and the rational-additive-group obstruction to a homomorphism sending1 to this u. Do not infer a preferred readout or a general phase-selection theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean)
- sha256 (`bytes`): `5139307750119e0e6f022ae813972e4625d02908d37d9067e6942e532181b6dd`
- cited in: node.lean, record TFQ-1026
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch4.gintPow34_im_ne_zero` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.gintPow34_im_ne_zero` |
| `WitnessedDifference.WdpBatch4.pythagorean_phase_unit_norm` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.pythagorean_phase_unit_norm` |
| `WitnessedDifference.WdpBatch4.readout_quadratic_ne_quartic` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.readout_quadratic_ne_quartic` |
| `WitnessedDifference.WdpBatch4.readout_quadratic_phase_invariant` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.readout_quadratic_phase_invariant` |
| `WitnessedDifference.WdpBatch4.readout_quartic_phase_invariant` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.readout_quartic_phase_invariant` |
| `WitnessedDifference.WdpBatch4.triangle_holonomy_coboundary_invariant` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.triangle_holonomy_coboundary_invariant` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/21_implementation_core/tfq_1026_fq_impl_wdp_amplitude_bridge.md`

- file: [dag/derivations/21_implementation_core/tfq_1026_fq_impl_wdp_amplitude_bridge.md](../../../dag/derivations/21_implementation_core/tfq_1026_fq_impl_wdp_amplitude_bridge.md)
- sha256 (`lf-normalised`): `ab8847fd1cfdb01822e86735f125738c1c1d112750531b00aa26f6e805ac45f7`
- generated view: listed, not counted
- cited in: record TFQ-1026
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_fq_core_and_k23_duality_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:77726675ace7bc93c8e8203260618f203aa20359b38d15cd48dee38f04c7a89f::readout_quadratic`
- `external:sha256:77726675ace7bc93c8e8203260618f203aa20359b38d15cd48dee38f04c7a89f::readout_quartic`
- `external:sha256:77726675ace7bc93c8e8203260618f203aa20359b38d15cd48dee38f04c7a89f::same_up_to_common_phase`
- `external:sha256:77726675ace7bc93c8e8203260618f203aa20359b38d15cd48dee38f04c7a89f::u_power_is_never_one`
- `external:sha256:77726675ace7bc93c8e8203260618f203aa20359b38d15cd48dee38f04c7a89f:1`

## Routes

Incoming (1):

- `FQ-R-AMPLITUDE-BRIDGE` `DERIVED_LEAN`: [FQ-IMPL-REALIFICATION-ADAPTER](FQ-IMPL-REALIFICATION-ADAPTER.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `FQ-R-GAP-U1` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-U1-CIRCLE](FQ-GAP-U1-CIRCLE.md) (CONDITIONAL)
