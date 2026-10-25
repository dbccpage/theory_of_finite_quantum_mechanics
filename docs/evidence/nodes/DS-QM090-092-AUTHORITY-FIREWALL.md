# DS-QM090-092-AUTHORITY-FIREWALL

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In a toy zero-defect gate, authorization from a receipt holds exactly when its defect is zero (a definitional iff) and a Boolean non-implication from structure-derived to authorized holds; every run keeps AuthorityEffect None. No constructor-level theorem and no real receipt-validation policy is established.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Define a trusted receipt-validation/packet policy before any real authorization; no general no-constructor theorem, publication terminal or physical claim is proved. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[STANDARD — ENC-1063, MECHANIZED, axiom-free\] (QM-090-C9); QM-091-C1a \[PROVEN, MECHANIZED\]; QM-091-C1b \[PROSE / OPEN\]

## Review

- PFP review: [dag/results/DS-QM090-092-AUTHORITY-FIREWALL/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM090-092-AUTHORITY-FIREWALL/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Toy zero-defect gate arithmetic and logical nonimplication are kernel checked; every run retains AuthorityEffect None.
  - does not support: Define a trusted receipt-validation/packet policy before any real authorization; no general no-constructor theorem, publication terminal or physical claim is proved.
  - next test: Define a trusted receipt-validation/packet policy before any real authorization; no general no-constructor theorem, publication terminal or physical claim is proved.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0272, record TFQ-0275, record TFQ-0277
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` |
| `QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` |
| `QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` |
| `QuantumMechanics.DerivationDagQMClosure.qm090_authority_firewall_zero_defect_iff` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm090_authority_firewall_zero_defect_iff` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0272_interpretations_as_authority_shadows.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0272_interpretations_as_authority_shadows.md](../../../dag/derivations/13_finite_qm_information/tfq_0272_interpretations_as_authority_shadows.md)
- sha256 (`lf-normalised`): `6c195fc19eee75d32fee97a7a26271292bd94e955cd2118335b839fe683c3d70`
- generated view: listed, not counted
- cited in: record TFQ-0272
- counts toward the grade: no

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0275_formal_possibility_is_not_a_physical_terminal.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0275_formal_possibility_is_not_a_physical_terminal.md](../../../dag/derivations/13_finite_qm_information/tfq_0275_formal_possibility_is_not_a_physical_terminal.md)
- sha256 (`lf-normalised`): `0c06e59caa9cf6e89889de2d616dcb14790b6dd396b74cf92ac1887c673db010`
- generated view: listed, not counted
- cited in: record TFQ-0275
- counts toward the grade: no

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0277_typed_authority_boundary_suite.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0277_typed_authority_boundary_suite.md](../../../dag/derivations/13_finite_qm_information/tfq_0277_typed_authority_boundary_suite.md)
- sha256 (`lf-normalised`): `f45813ea68654520b8c881591342a0c38c8266e675f47e144e2af6734aa78028`
- generated view: listed, not counted
- cited in: record TFQ-0277
- counts toward the grade: no

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0278_copenhagen_slot_reserved_as_an_authority_shadow.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0278_copenhagen_slot_reserved_as_an_authority_shadow.md](../../../dag/derivations/13_finite_qm_information/tfq_0278_copenhagen_slot_reserved_as_an_authority_shadow.md)
- sha256 (`lf-normalised`): `13bab7cc5334068682024b2f5a505ec0cd6ca48f568032a5f2421e8a42be2917`
- generated view: listed, not counted
- cited in: record TFQ-0278 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/090_interpretations_as_authority_shadows/qm_090_interpretations_as_authority_shadows_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/090_interpretations_as_authority_shadows/qm_090_interpretations_as_authority_shadows_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/091_deutsch_everett_wolfram_promotion_error/qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/091_deutsch_everett_wolfram_promotion_error/qm_091_deutsch_everett_wolfram_promotion_error_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/092_qm_typed_authority_boundary_suite/qm_092_qm_typed_authority_boundary_suite_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/092_qm_typed_authority_boundary_suite/qm_092_qm_typed_authority_boundary_suite_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `DS-R-AUTHORITY-FIREWALL` `COMPUTED`: [L1-OBSERVER-AXIOMS-H1-H5](L1-OBSERVER-AXIOMS-H1-H5.md) (ADMITTED_PRIMITIVE)

Outgoing (2):

- `DS-R-AUTHORITY-TO-REGISTRY` `DERIVED_LEAN`: [DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY](DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY.md) (PROVED_LEAN)
- `DS-R-EVERETT` `DERIVED_LEAN`: [DS-QM094-EVERETT-RELATIVE-STATE-CONTACT](DS-QM094-EVERETT-RELATIVE-STATE-CONTACT.md) (PROVED_LEAN)
