# FQ-IMPL-PAIRING-AUDIT

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual state/projector arrays and pairing differences plus a negative nonlinear extension are exact; off-diagonal and polynomial-negative identities are kernel checked.

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

- declared packet and candidate pairings (assumption)

## Bottleneck

Unmet after the PFP review: Run the full source registry and its complete positivity/normalization/composite contracts, then justify a uniqueness theorem if available. This small packet neither selects Born nor makes every nonlinear alternative physically admissible. The broader source statement is kept in pfp_review.prior_statement.

## Source status

module docs: "every candidate probability pairing is graded by the same finite checks on a declared packet, and no check selects the Born pairing"

## Review

- PFP review: [dag/results/FQ-IMPL-PAIRING-AUDIT/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/FQ-IMPL-PAIRING-AUDIT/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual state/projector arrays and pairing differences plus a negative nonlinear extension are exact; off-diagonal and polynomial-negative identities are kernel checked.
  - does not support: Run the full source registry and its complete positivity/normalization/composite contracts, then justify a uniqueness theorem if available. This small packet neither selects Born nor makes every nonlinear alternative physically admissible.
  - next test: Run the full source registry and its complete positivity/normalization/composite contracts, then justify a uniqueness theorem if available. This small packet neither selects Born nor makes every nonlinear alternative physically admissible.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1028
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges` |
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/21_implementation_core/tfq_1028_fq_impl_pairing_audit.md`

- file: [dag/derivations/21_implementation_core/tfq_1028_fq_impl_pairing_audit.md](../../../dag/derivations/21_implementation_core/tfq_1028_fq_impl_pairing_audit.md)
- sha256 (`lf-normalised`): `a5c09229b303a4ec2d40460074e33c31d4f9deeeebe6e7651f96423821a2baba`
- generated view: listed, not counted
- cited in: record TFQ-1028
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_fq_core_and_k23_duality_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:c8f020f9abf33d6d86e8630fd8f9d3da0bb1db91835d6dfcbe56cfa4709cad7e::Pairing`
- `external:sha256:c8f020f9abf33d6d86e8630fd8f9d3da0bb1db91835d6dfcbe56cfa4709cad7e:3`

## Routes

Incoming (1):

- `FQ-R-PAIRING-AUDIT` `COMPUTED`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

