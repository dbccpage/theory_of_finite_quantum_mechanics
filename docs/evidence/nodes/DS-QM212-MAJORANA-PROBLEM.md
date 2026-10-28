# DS-QM212-MAJORANA-PROBLEM

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Majorana braiding / Clifford generator algebra (gamma_1^2 = I, gamma_2^2 = I, gamma_1 gamma_2 + gamma_2 gamma_1 = 0, and Parity^2 = -I) is mechanized in qm212_majorana_clifford_relations.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Finite Majorana Clifford parity algebra and tetron braid/parity checks are mechanized; experimental device noise models remain external.

## Source status

Majorana Clifford generator anticommutation and parity invariants mechanized in DerivationDagQMClosure.lean and tfqm_majorana

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
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid` |
| `QuantumMechanics.DerivationDagQMClosure.qm212_majorana_clifford_relations` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm212_majorana_clifford_relations` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/lib.rs`

- file: [code/rust/src/wdp/lib.rs](../../../code/rust/src/wdp/lib.rs)
- sha256 (`bytes`): `9111d9c82247cc2f1e8176b0a0285a788fcd1d2bc6cd2c1d3be81f84f431d235`
- cited in: record TFQ-0181
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0181_keep_tfqm_majorana_a_gf_2_diagnostic_and_do_not_treat_it_as_an.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0181_keep_tfqm_majorana_a_gf_2_diagnostic_and_do_not_treat_it_as_an.md](../../../dag/derivations/22_implementation_sibling/tfq_0181_keep_tfqm_majorana_a_gf_2_diagnostic_and_do_not_treat_it_as_an.md)
- sha256 (`lf-normalised`): `8c6704c7b5aaebd68eb5e709f67e9c0446a158331273d882ddc17f764db435db`
- generated view: listed, not counted
- cited in: record TFQ-0181
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:4af94b48802f547227ece7d358369dd29800fa80fc78ee087c3dd70e8fa0d46c`
- `external:sha256:5bc77d81deffd5ac0cfe0c3273f152b28c281ff38f60a61f8c3fdca45257b322`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_ds_qm_dynamics_structure_and_majorana_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`

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
